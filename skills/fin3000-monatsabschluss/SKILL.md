---
name: fin3000-monatsabschluss
description: Bereite den Monatsabschluss in Fin3000 vor, indem du Eingangsrechnungen, unkontierte Banktransaktionen, Journalbuchungen, offene Posten, UStVA-Status und BWA für einen Zeitraum prüfst; nutze den Skill für eine Abschluss-Checkliste, nicht zum Festschreiben oder Übermitteln.
---

# Fin3000 Monatsabschluss

Erstelle eine lesende, nachvollziehbare Checkliste zur Vorbereitung eines
Monatsabschlusses. Der Skill schließt keine Periode und nimmt keine
Steuerübermittlung vor.

## Vorgehen

1. Rufe `get_context` auf. Ermittle den gewünschten Monat und, soweit für das
   jeweilige Werkzeug unterstützt, die Business Unit. Frage nach, wenn Monat
   oder Firma mehrdeutig ist.
2. Verwende für alle Aufrufe denselben vollständigen ISO-Zeitraum vom ersten
   bis zum letzten Kalendertag des Monats.
3. Prüfe nur die für den Auftrag verfügbaren Bereiche:
   - `search_incoming_invoices` für Eingangsrechnungen im Zeitraum;
   - `search_transactions` mit `booking_status="unbooked"` für die offene,
     geschäftliche und technisch buchbare Transaktions-Worklist;
   - `search_journal_entries` für vorhandene Buchungen;
   - `list_open_items` für offene Forderungen und, ohne falschen BU-Bezug,
     Verbindlichkeiten;
   - `get_vat_return_status` für den vorhandenen UStVA-/ELSTER-Status;
   - `get_financial_report` für die vorläufige BWA der eindeutig gewählten
     Business Unit.
4. Folge Cursorn nur so weit, wie es für eine vollständige Aussage nötig ist.
   Wenn die Ergebnismenge nicht vollständig gelesen wurde, nenne die
   verbleibende Pagination statt Vollständigkeit zu behaupten.
5. Gib das Ergebnis als Checkliste mit `Erledigt`, `Prüfen` und
   `Nicht beurteilbar` aus. Nenne je Punkt Datenzeitraum, angewandten Scope,
   Anzahl oder relevante Beträge sowie die gelieferten Fin3000-Links.
6. Schließe mit einer priorisierten Liste offener Arbeiten und kennzeichne die
   BWA als vorläufig.

## Grenzen

- Dieser Workflow ist standardmäßig vollständig lesend. Rufe
  `categorize_transaction`, `create_client` und `create_invoice_draft` nicht
  als Teil des Monatsabschluss-Checks auf.
- Transaktionen, Eingangsrechnungen und Journaldaten besitzen in den
  vorhandenen MCP-Werkzeugen keinen frei wählbaren BU-Filter. Beschreibe solche
  Ergebnisse als kontoweit und ordne sie keiner Firma erfunden zu.
- `unbooked` ist der MCP-Wert; verwende nicht den REST-Begriff
  `needs_booking`.
- Ein Statusabruf übermittelt keine UStVA. Behaupte niemals ELSTER-/DATEV-
  Versand, Festschreibung, Periodenabschluss oder steuerliche Prüfung.
- Fehlende Daten sind kein Beleg dafür, dass der Sachverhalt erledigt ist.
