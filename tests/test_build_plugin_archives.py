from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
SCRIPTS = REPOSITORY / "scripts"
PLUGIN_SOURCE = REPOSITORY
SKILLS = (
    "fin3000-buchhaltung",
    "fin3000-monatsabschluss",
    "fin3000-rechnungen",
)


def load_packager_module():
    path = SCRIPTS / "build_plugin_archives.py"
    spec = importlib.util.spec_from_file_location(
        "build_plugin_archives", path
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


packager = load_packager_module()


class Fin3000PluginArchiveTests(unittest.TestCase):
    def build(self, output: Path):
        return packager.build_archives(PLUGIN_SOURCE, output)

    def test_archives_have_one_root_and_platform_specific_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            results = {result.target: result for result in self.build(root)}
            with zipfile.ZipFile(results["openai"].path) as archive:
                openai_members = set(archive.namelist())
            with zipfile.ZipFile(results["claude"].path) as archive:
                claude_members = set(archive.namelist())

        self.assertTrue(
            all(member.startswith("fin3000/") for member in openai_members)
        )
        self.assertTrue(
            all(member.startswith("fin3000/") for member in claude_members)
        )
        expected_skills = {
            f"fin3000/skills/{name}/SKILL.md" for name in SKILLS
        }
        self.assertEqual(
            openai_members,
            {
                "fin3000/LICENSE",
                "fin3000/.codex-plugin/plugin.json",
                *expected_skills,
                *{
                    f"fin3000/skills/{name}/agents/openai.yaml"
                    for name in SKILLS
                },
            },
        )
        self.assertEqual(
            claude_members,
            {
                "fin3000/LICENSE",
                "fin3000/.claude-plugin/icon.svg",
                "fin3000/.claude-plugin/plugin.json",
                "fin3000/.mcp.json",
                *expected_skills,
            },
        )

    def test_both_archives_copy_the_same_three_skill_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            results = {
                result.target: result for result in self.build(Path(directory))
            }
            with zipfile.ZipFile(results["openai"].path) as openai_archive:
                with zipfile.ZipFile(results["claude"].path) as claude_archive:
                    for name in SKILLS:
                        member = f"fin3000/skills/{name}/SKILL.md"
                        source = (PLUGIN_SOURCE / "skills" / name / "SKILL.md").read_bytes()
                        self.assertEqual(source, openai_archive.read(member))
                        self.assertEqual(source, claude_archive.read(member))

    def test_build_is_byte_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = {result.target: result for result in self.build(root / "first")}
            second = {result.target: result for result in self.build(root / "second")}

            for target in ("openai", "claude"):
                with self.subTest(target=target):
                    self.assertEqual(first[target].sha256, second[target].sha256)
                    self.assertEqual(
                        first[target].path.read_bytes(), second[target].path.read_bytes()
                    )

    def test_manifests_and_mcp_transport_share_the_expected_contract(self):
        codex = json.loads(
            (PLUGIN_SOURCE / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        claude = json.loads(
            (PLUGIN_SOURCE / ".claude-plugin/plugin.json").read_text(
                encoding="utf-8"
            )
        )
        mcp = json.loads(
            (PLUGIN_SOURCE / ".mcp.json").read_text(encoding="utf-8")
        )

        self.assertEqual(codex["name"], claude["name"])
        self.assertEqual(codex["version"], claude["version"])
        self.assertEqual(
            mcp,
            {
                "mcpServers": {
                    "fin3000": {
                        "type": "http",
                        "url": "https://api.fin3000.com/mcp",
                    }
                }
            },
        )

    def test_claude_marketplace_installs_the_repository_root_plugin(self):
        manifest = json.loads(
            (PLUGIN_SOURCE / ".claude-plugin/plugin.json").read_text(
                encoding="utf-8"
            )
        )
        marketplace = json.loads(
            (PLUGIN_SOURCE / ".claude-plugin/marketplace.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(marketplace["name"], "fin3000-plugins")
        self.assertEqual(marketplace["owner"]["name"], "Ideal3000 GmbH")
        self.assertEqual(len(marketplace["plugins"]), 1)
        self.assertEqual(
            marketplace["plugins"][0],
            {
                "name": manifest["name"],
                "source": "./",
                "description": (
                    "Buchhaltungs-Workflows für Freelancer, Selbstständige "
                    "und GbRs mit dem OAuth-geschützten Fin3000-MCP-Server."
                ),
                "category": "Finance",
                "tags": ["accounting", "invoices", "finance", "germany"],
            },
        )
        self.assertEqual(
            manifest["repository"],
            "https://github.com/Fin3000/fin3000-ai-plugins",
        )
        self.assertEqual(
            manifest["privacyPolicyUrl"],
            "https://fin3000.com/datenschutz/",
        )

        icon = ET.parse(PLUGIN_SOURCE / ".claude-plugin/icon.svg").getroot()
        self.assertEqual(icon.attrib["width"], "256")
        self.assertEqual(icon.attrib["height"], "256")
        self.assertEqual(icon.attrib["viewBox"], "0 0 96 96")

    def test_missing_openai_companion_metadata_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "fin3000"
            shutil.copytree(PLUGIN_SOURCE, source)
            missing = source / "skills/fin3000-buchhaltung/agents/openai.yaml"
            missing.unlink()

            with self.assertRaisesRegex(
                packager.PackagingError, "OpenAI agent metadata is missing"
            ):
                packager.build_archives(source, Path(directory) / "output")

    def test_missing_license_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "fin3000"
            shutil.copytree(PLUGIN_SOURCE, source)
            (source / "LICENSE").unlink()

            with self.assertRaisesRegex(
                packager.PackagingError, "required license is missing"
            ):
                packager.build_archives(source, Path(directory) / "output")


if __name__ == "__main__":
    unittest.main()
