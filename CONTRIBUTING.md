# Fin3000 AI Plugins

Independent distribution source for the Fin3000 OpenAI/Codex and Claude Code
plugins. The Fin3000 workspace rules apply when this repository is worked on
inside that workspace.

- Work in a `feature/*` Git worktree; `main` is MR-only.
- Keep all `skills/*/SKILL.md` files host-neutral and byte-identical in
  both generated archives.
- Keep platform metadata separate: `.codex-plugin/`, `.codex-plugin/mcp.json` (packaged as
  `.mcp.json`, the published ChatGPT MCP endpoint) and `agents/openai.yaml` are OpenAI-only; `.claude-plugin/` and `.mcp.json` are Claude-only.
- Never store OAuth tokens, API tokens, client secrets or customer data here.
  The only MCP endpoint is `https://api.fin3000.com/mcp`; authentication is
  negotiated by the host through the server's OAuth discovery.
- Commit only Markdown, text, JSON, YAML and PNG files. Packaging and
  validation are maintained in the Fin3000 backend repository.
- Do not publish, upload, create a marketplace, push or release without the
  user's explicit approval. Generated ZIP files belong in ignored `dist/`.
