# Changelog

All notable changes to the Fin3000 AI plugin packages are documented here.

## [Unreleased]

## [0.2.1] - 2026-10-24

### Changed

- Sales copy in manifests, marketplace, README and skill metadata: „Claude macht deine Buchhaltung – du gibst nur frei“, target group now Selbstständige, Freelancer, GbR, UG und GmbH; keywords `ug` and `gmbh` added.

## [0.2.0] - 2026-10-23

### Added

- Shared fourth workflow for delegated bookkeeping completion, including durable authority/recovery, native source intake and source-verified task upkeep.
- Anthropic directory fields in the Claude manifest: 512px PNG icon, documentation, support and terms URLs, license.
- German quick start for claude.ai, Claude Code and Codex, including update and uninstall steps.
- Every skill names what to do when the connection, a tool, the feature or a permission is missing.

### Changed

- German marketplace description, tags and keywords that start with the search term „Buchhaltung“.
- `fin3000-buchhaltung` and `fin3000-monatsabschluss` call only read-only tools (`readOnlyHint=true`) instead of excluding three named write tools, and point to the writing skills for changes.
- `fin3000-monatsabschluss` builds its checklist on the native `get_bookkeeping_status`/`check_bookkeeping` and is labelled „nur prüfen“.
- `fin3000-rechnungen` saves a new customer and the invoice draft after one preview and one approval (`new_customer`), matching the server contract.

## [0.1.0] - 2026-09-30

### Added

- A square Fin3000 icon and the public privacy-policy URL required for a
  complete Anthropic Plugin Directory listing.
- An Apache 2.0 license in the plugin root and both generated source archives
  so Anthropic's directory policy check can verify the distribution license.
- A public Claude Code marketplace catalog with copy-paste installation from
  `Fin3000/fin3000-ai-plugins`.
- A shared, host-neutral set of three Fin3000 accounting skills for
  OpenAI/Codex and Claude Code.
- Separate platform manifests and a secret-free Claude remote-MCP
  configuration for `https://api.fin3000.com/mcp`.
- A deterministic builder and contract tests for the OpenAI and Claude source
  archives.
