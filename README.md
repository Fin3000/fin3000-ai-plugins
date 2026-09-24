# Fin3000 AI Plugins

This repository contains the distribution source for the Fin3000 plugins for
OpenAI/Codex and Claude Code. Both packages use the same three Fin3000 skills
and connect to the existing OAuth-protected remote MCP endpoint:

```text
https://api.fin3000.com/mcp
```

The plugins are not part of the Django runtime image. The production MCP
server remains in the separate Fin3000 backend repository under
`src/mcp_server`; these sources are packaged and uploaded to the respective AI
host independently.

## Layout

```text
.codex-plugin/plugin.json          OpenAI/Codex manifest
.claude-plugin/plugin.json         Claude Code manifest
.mcp.json                          Claude remote-MCP configuration
skills/*/SKILL.md                  shared host-neutral workflows
skills/*/agents/openai.yaml        OpenAI-only presentation metadata
scripts/build_plugin_archives.py   deterministic package builder
tests/test_build_plugin_archives.py
```

## Build and verify

```bash
python3 -m unittest tests.test_build_plugin_archives
python3 scripts/build_plugin_archives.py
claude plugin validate . --strict
unzip -t dist/fin3000-plugin-source.zip
unzip -t dist/fin3000-claude-plugin-source.zip
sha256sum dist/fin3000-plugin-source.zip \
  dist/fin3000-claude-plugin-source.zip
```

The builder uses fixed timestamps, file modes and ordering. Repeated builds
from the same commit therefore produce byte-identical archives and SHA-256
hashes. It fails closed if a skill is missing, manifest names or versions
differ, or the Claude MCP configuration contains anything other than the
Fin3000 HTTPS endpoint.

The OpenAI archive contains the Codex manifest, all three skills and their
OpenAI agent metadata. The Claude archive contains the Claude manifest,
`.mcp.json` and the same three skill files. Neither archive contains secrets or
metadata belonging only to the other platform.

Uploading, marketplace publication and legal acceptance are separate manual
release steps and are not performed by the build script.
