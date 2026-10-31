# Fin3000 für Claude und Codex

**Claude macht deine Buchhaltung – du gibst nur frei.** Belege suchen,
Kontoauszüge abgleichen, Buchungen nachtragen: Fin3000 verbindet Claude und
Codex per OAuth mit deiner Buchhaltung, gemacht für Selbstständige,
Freelancer, GbR, UG und GmbH in Deutschland.

Sag einfach „Mach meine Buchhaltung für Oktober“: Claude ordnet Belege den
Kontobewegungen zu, schlägt die Kontierung nach SKR03 oder SKR04 vor und
bucht, sobald du zustimmst. Offene Posten, überfällige Kunden, BWA und
UStVA-Status hast du mit einer Frage im Blick, Rechnungsentwürfe entstehen in
Sekunden. Jede Änderung zeigt dir Claude vorher; Zahlungen, Rechnungsversand
und Steuerübermittlung bleiben bei dir. Deine Buchhaltungsdaten liegen
ausschließlich in deutschen Rechenzentren, mehrere Firmen bleiben sauber
getrennt, und der DATEV-Export für deine Steuerkanzlei ist eingebaut.

## Schnellstart

**Voraussetzungen:** ein Fin3000-Konto, du bist dort Admin, und der
KI-Assistent ist unter Einstellungen → Funktionen eingeschaltet
(<https://app.fin3000.com/features>).

**claude.ai und Claude Desktop (Connector):** Einstellungen → Connectors →
benutzerdefinierten Connector hinzufügen → URL `https://api.fin3000.com/mcp`
→ Verbinden. Fin3000 öffnet die Anmeldung und die Freigabe.

**Claude Code (dieses Plugin):**

```bash
claude plugin marketplace add Fin3000/fin3000-ai-plugins
claude plugin install fin3000@fin3000-plugins
```

Danach `/reload-plugins`. Beim ersten Fin3000-Aufruf öffnet sich die
Anmeldung; erscheint sie nicht, `/mcp` → `fin3000` → Authenticate.

**Codex:** Plugin `fin3000` aus dem OpenAI-Paket installieren, danach
dieselbe OAuth-Anmeldung.

**Erste Frage:** „Welche Kundenrechnungen sind überfällig?“ Claude antwortet
mit Kunde, Betrag, Fälligkeit und einem Link in deine Fin3000-Daten.

## Die acht Skills

| Skill | Wofür | Schreibt? |
|---|---|---|
| `fin3000-einstieg` | Einstieg: Firmen, Möglichkeiten, Vorschau und Bestätigung erklären | nein |
| `fin3000-buchhaltung` | BWA, Einnahmen, Ausgaben, offene Posten verstehen | nein |
| `fin3000-monatsabschluss` | Monatsabschluss vorbereiten (nur prüfen) | nein |
| `fin3000-rechnungen` | Rechnung schreiben (auch §25a), offene Rechnungen prüfen | ja, nach deiner Bestätigung |
| `fin3000-kunden` | Kunden und Lieferanten suchen, anlegen, ändern | ja, nach deiner Bestätigung |
| `fin3000-belege` | Belege hochladen, Eingangsrechnungen prüfen, Beleg einer Zahlung zuordnen | ja, nach deiner Bestätigung |
| `fin3000-firma-einrichten` | Firmendaten, Rechnungslayout mit Muster, Belegpostfach | ja, nach deiner Bestätigung (nur Kontoinhaber) |
| `fin3000-buchhaltung-vervollstaendigen` | „Erledige meine Buchhaltung“: Belege, Kontierung, Buchungen, offene Aufgaben | ja, mit gespeicherten oder einmal bestätigten Freigaben |

## Aktualisieren

Fremde Marketplaces aktualisieren sich nicht von selbst:

```bash
claude plugin marketplace update fin3000-plugins
claude plugin update fin3000@fin3000-plugins
```

Danach `/reload-plugins`. Die bestehende Fin3000-Verbindung bleibt erhalten.

## Entfernen

```bash
claude plugin uninstall fin3000@fin3000-plugins
```

Trenne die Verbindung zusätzlich in Fin3000 unter Sicherheit
(<https://app.fin3000.com/security>), damit kein Zugriff bestehen bleibt.

## Hilfe

- Anleitung: <https://fin3000.com/hilfe/ki-assistent-mit-mcp-verbinden/>
- Kontakt: <https://fin3000.com/kontakt/>
- Datenschutz: <https://fin3000.com/datenschutz/>

---

## For maintainers

This repository is the distribution source for the Fin3000 plugins for
OpenAI/Codex and Claude Code. Both packages use the same eight host-neutral
skills and connect to the OAuth-protected remote MCP endpoint
`https://api.fin3000.com/mcp`. The production MCP server lives in the Fin3000
backend repository under `src/mcp_server`; these sources are packaged and
uploaded to each AI host independently.

### Layout

```text
.codex-plugin/plugin.json          OpenAI/Codex manifest
.app.json                          OpenAI mapping to the published ChatGPT MCP connection
.claude-plugin/plugin.json         Claude Code manifest incl. directory fields
.claude-plugin/marketplace.json    Claude Code marketplace catalog
.claude-plugin/icon.png            512px directory icon (copy of the app icon)
.mcp.json                          Claude remote-MCP configuration
skills/*/SKILL.md                  shared host-neutral workflows
skills/*/agents/openai.yaml        OpenAI-only presentation metadata
scripts/build_plugin_archives.py   deterministic package builder
tests/test_build_plugin_archives.py
```

### Build and verify

```bash
python3 -m unittest tests.test_build_plugin_archives
python3 scripts/build_plugin_archives.py
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate . --strict
unzip -t dist/fin3000-plugin-source.zip
unzip -t dist/fin3000-claude-plugin-source.zip
sha256sum dist/fin3000-plugin-source.zip dist/fin3000-claude-plugin-source.zip
```

The builder uses fixed timestamps, file modes and ordering, so repeated builds
from the same commit are byte-identical. It fails closed if a skill is
missing, manifest versions differ, the Codex name is not the OpenAI app ID, the manifest icon is missing or
not a PNG, or the Claude MCP configuration contains anything other than the
Fin3000 HTTPS endpoint. Every file the Claude manifest references ships in the
Claude archive.

Uploading, directory submission and legal acceptance are separate manual
release steps; see `docs/runbooks/anthropic-connector-submission.md` in the
backend repository.
