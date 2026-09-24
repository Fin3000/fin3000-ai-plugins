#!/usr/bin/env python3
"""Build deterministic OpenAI and Claude source archives for Fin3000."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path


ARCHIVE_ROOT = Path("fin3000")
EXPECTED_SKILLS = (
    "fin3000-buchhaltung",
    "fin3000-monatsabschluss",
    "fin3000-rechnungen",
)
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


class PackagingError(RuntimeError):
    """Raised when the shared plugin source violates its package contract."""


@dataclass(frozen=True)
class ArchiveSpec:
    target: str
    filename: str
    files: tuple[Path, ...]


@dataclass(frozen=True)
class BuildResult:
    target: str
    path: Path
    sha256: str
    members: tuple[str, ...]


def load_json(path: Path) -> dict[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise PackagingError(f"required file is missing: {path}") from error
    except json.JSONDecodeError as error:
        raise PackagingError(f"invalid JSON in {path}: {error}") from error
    if not isinstance(data, dict):
        raise PackagingError(f"JSON root must be an object: {path}")
    return data


def validate_source(source: Path) -> tuple[Path, ...]:
    codex_manifest = source / ".codex-plugin/plugin.json"
    claude_manifest = source / ".claude-plugin/plugin.json"
    mcp_config = source / ".mcp.json"
    codex_data = load_json(codex_manifest)
    claude_data = load_json(claude_manifest)
    mcp_data = load_json(mcp_config)

    for field in ("name", "version"):
        if codex_data.get(field) != claude_data.get(field):
            raise PackagingError(
                f"manifest {field} differs: "
                f"{codex_data.get(field)!r} != {claude_data.get(field)!r}"
            )

    expected_mcp = {
        "mcpServers": {
            "fin3000": {
                "type": "http",
                "url": "https://api.fin3000.com/mcp",
            }
        }
    }
    if mcp_data != expected_mcp:
        raise PackagingError(
            ".mcp.json must contain only the OAuth-capable Fin3000 HTTP endpoint"
        )

    skills_root = source / "skills"
    discovered = tuple(
        sorted(path.parent.name for path in skills_root.glob("*/SKILL.md"))
    )
    if discovered != EXPECTED_SKILLS:
        raise PackagingError(
            f"expected skills {EXPECTED_SKILLS!r}, discovered {discovered!r}"
        )

    skill_files: list[Path] = []
    for name in EXPECTED_SKILLS:
        skill = skills_root / name / "SKILL.md"
        openai_agent = skills_root / name / "agents/openai.yaml"
        if not skill.is_file():
            raise PackagingError(f"required skill is missing: {skill}")
        if not openai_agent.is_file():
            raise PackagingError(f"OpenAI agent metadata is missing: {openai_agent}")
        skill_files.append(skill.relative_to(source))

    return tuple(skill_files)


def archive_specs(source: Path) -> dict[str, ArchiveSpec]:
    skills = validate_source(source)
    openai_agents = tuple(
        Path("skills") / name / "agents/openai.yaml" for name in EXPECTED_SKILLS
    )
    return {
        "openai": ArchiveSpec(
            target="openai",
            filename="fin3000-plugin-source.zip",
            files=(Path(".codex-plugin/plugin.json"), *skills, *openai_agents),
        ),
        "claude": ArchiveSpec(
            target="claude",
            filename="fin3000-claude-plugin-source.zip",
            files=(Path(".claude-plugin/plugin.json"), Path(".mcp.json"), *skills),
        ),
    }


def write_archive(source: Path, output: Path, spec: ArchiveSpec) -> BuildResult:
    output.parent.mkdir(parents=True, exist_ok=True)
    members: list[str] = []
    with zipfile.ZipFile(
        output,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for relative in sorted(spec.files, key=lambda path: path.as_posix()):
            source_file = source / relative
            if not source_file.is_file():
                raise PackagingError(f"archive input is missing: {source_file}")
            member = (ARCHIVE_ROOT / relative).as_posix()
            info = zipfile.ZipInfo(member, date_time=FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source_file.read_bytes(), compresslevel=9)
            members.append(member)

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    return BuildResult(
        target=spec.target,
        path=output,
        sha256=digest,
        members=tuple(members),
    )


def build_archives(
    source: Path,
    output_dir: Path,
    targets: tuple[str, ...] = ("openai", "claude"),
) -> tuple[BuildResult, ...]:
    source = source.resolve()
    specs = archive_specs(source)
    unknown = tuple(target for target in targets if target not in specs)
    if unknown:
        raise PackagingError(f"unknown archive target(s): {', '.join(unknown)}")
    return tuple(
        write_archive(source, output_dir / specs[target].filename, specs[target])
        for target in targets
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    repository = Path(__file__).resolve().parents[1]
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=repository,
        help="shared Fin3000 plugin source directory",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=repository / "dist",
        help="directory for the generated ZIP archives",
    )
    parser.add_argument(
        "--target",
        choices=("all", "openai", "claude"),
        default="all",
        help="archive family to build",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_args(argv)
    targets = (
        ("openai", "claude")
        if arguments.target == "all"
        else (arguments.target,)
    )
    try:
        results = build_archives(
            source=arguments.source_dir,
            output_dir=arguments.output_dir.resolve(),
            targets=targets,
        )
    except PackagingError as error:
        print(f"PLUGIN_PACKAGE_ERROR: {error}", file=sys.stderr)
        return 1

    for result in results:
        print(f"{result.target}: {result.path}")
        print(f"sha256: {result.sha256}")
        for member in result.members:
            print(f"  {member}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
