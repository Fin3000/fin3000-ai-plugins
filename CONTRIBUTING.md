# Fin3000 AI Plugins

Distribution source for the Fin3000 Claude Code plugin. The Fin3000 workspace
rules apply when this repository is worked on inside that workspace.

- Work in a `feature/*` Git worktree; `main` is MR-only.
- Keep all `skills/*/SKILL.md` files host-neutral.
- This repository holds only the Claude plugin: `.claude-plugin/`, `.mcp.json`
  and `skills/`. Metadata for other AI hosts is maintained in the Fin3000
  backend repository.
- Never store OAuth tokens, API tokens, client secrets or customer data here.
  The only MCP endpoint is `https://api.fin3000.com/mcp`; authentication is
  negotiated by the host through the server's OAuth discovery.
- Commit only Markdown, text, JSON and PNG files. Packaging and validation are
  maintained in the Fin3000 backend repository.
- Do not publish, upload, create a marketplace, push or release without the
  user's explicit approval. Generated ZIP files belong in ignored `dist/`.
