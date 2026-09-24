# Fin3000 AI Plugins

Independent distribution source for the Fin3000 OpenAI/Codex and Claude Code
plugins. The Fin3000 workspace `AGENTS.md` applies when this repository is
worked on inside that workspace.

- Work in a `feature/*` Git worktree; `main` is MR-only.
- Before edits run the workspace `scripts/changed-files.sh` once for all
  intended paths. Repository name: `tools/fin3000-ai-plugins`.
- Keep the three `skills/*/SKILL.md` files host-neutral and byte-identical in
  both generated archives.
- Keep platform metadata separate: `.codex-plugin/` and `agents/openai.yaml`
  are OpenAI-only; `.claude-plugin/` and `.mcp.json` are Claude-only.
- Never store OAuth tokens, API tokens, client secrets or customer data here.
  The only MCP endpoint is `https://api.fin3000.com/mcp`; authentication is
  negotiated by the host through the server's OAuth discovery.
- Run `python3 -m unittest tests.test_build_plugin_archives`, build both
  archives, validate the Claude plugin with `claude plugin validate . --strict`
  and finish with `git diff --check`.
- Do not publish, upload, create a marketplace, push or release without the
  user's explicit approval. Generated ZIP files belong in ignored `dist/`.
