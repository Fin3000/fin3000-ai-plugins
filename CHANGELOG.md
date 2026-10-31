# Changelog

All notable changes to the Fin3000 AI plugin packages are documented here.

## [Unreleased]

### Fixed

- The OpenAI package declares the published MCP endpoint `https://api.fin3000.com/mcp` via `mcpServers: ./.mcp.json` (Codex format). App references (`apps`/`.app.json`) are not accepted for submission.

### Changed

- The OpenAI/Codex manifest name is the existing OpenAI portal app ID (`app-6a992ccc86a881918e84f1ec15f558cf`); the portal rejects packages whose name differs from the published app. The Claude manifest keeps `fin3000`.

## [1.1.0] - 2026-10-30

Version jumps to 1.1.0 so the package number is unambiguously above the
1.0.0 shown in the ChatGPT plugin listing.

### Added

- `fin3000-einstieg` („Mit Fin3000 arbeiten“): orientation via `get_context` and `get_capabilities`, which skill fits which task, preview/confirmation rules, limits, feature activation and product feedback.
- `fin3000-firma-einrichten` („Firma einrichten“): owner-only company setup with `get_company_setup`, MUSTER invoice preview, two-step `configure_company_setup` and `rename_receiving_address`; tax choices only from the user.
- `fin3000-belege` („Belege und Eingangsrechnungen“): inventory before upload, native upload/status flow, correcting and confirming incoming invoices, linking one receipt File to one transaction.
- `fin3000-kunden` („Kunden und Lieferanten“): search, read, create and patch partners with preview/confirmation; booking default only with explicit consent.

### Changed

- `fin3000-rechnungen` is presented as „Rechnung schreiben“ and points customer-only work to `fin3000-kunden`; offers, finalization and sending stay in the app.

## [0.3.0] - 2026-10-29

Release only after the backend with §25a without a saved purchase is deployed
(older servers reject `MARGIN_25A` without `margin_acquisition_id`).

### Changed

- §25a ohne Ankauf und ohne Einkaufspreis: `tax_scheme=MARGIN_25A` mit dem Endpreis genügt; Einkaufspreis (`unit_purchase_price`), Art, Herkunft und gespeicherter Ankauf sind optional, ein Einkaufspreis wird nur übergeben, wenn Nutzer oder Beleg ihn nennen. Two documented ways (position fields or saved purchase), advisories relayed as hints, DATEV IST export limitation kept.
- `feature_inactive` is distinguished by `details.feature` (`margin_taxation` = Differenzbesteuerung, otherwise the AI assistant).
- Shared bookkeeping instructions inventory existing invoices and published files, distinguish mailbox configuration from firm assignment, and recover native document requests by their original IDs.
- Preserve source accounting commands, explicit EUR tax evidence, unknown account policy and human clarification tasks throughout completion.


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
