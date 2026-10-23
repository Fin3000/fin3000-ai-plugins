---
name: fin3000-monatsabschluss
description: Bereite den Monatsabschluss in Fin3000 vor (nur prüfen) - mit der nativen Buchhaltungsprüfung, offenen Posten, UStVA-Status und vorläufiger BWA für eine Firma und einen Monat; nutze den Skill für eine Abschluss-Checkliste, nicht zum Erledigen, Festschreiben oder Übermitteln. Zum Erledigen dient fin3000-buchhaltung-vervollstaendigen.
---

# Fin3000 Monatsabschluss vorbereiten (nur prüfen)

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
   - `get_bookkeeping_status` und danach `check_bookkeeping` für dieselbe Firma
     und denselben Zeitraum. Das ist die native Prüfung derselben Befunde, die
     `fin3000-buchhaltung-vervollstaendigen` abarbeitet; folge jedem Cursor und
     starte bei `check_stale` neu. Null offene Zeilen sind kein Beleg für
     Vollständigkeit, solange Abdeckungsgrenzen gemeldet werden;
   - `search_incoming_invoices`, `search_transactions` und
     `search_journal_entries` nur, um einzelne Befunde zu belegen;
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

- Dieser Workflow ist vollständig lesend. Rufe ausschließlich Werkzeuge mit
  `readOnlyHint=true` auf. Will der Nutzer die gefundenen Punkte erledigen,
  wechsle ausdrücklich zu `fin3000-buchhaltung-vervollstaendigen`.
- Wo ein Werkzeug keinen Firmenfilter bietet, beschreibe das Ergebnis als
  kontoweit und ordne es keiner Firma erfunden zu.
- `unbooked` ist der MCP-Wert; verwende nicht den REST-Begriff
  `needs_booking`.
- Ein Statusabruf übermittelt keine UStVA. Behaupte niemals ELSTER-/DATEV-
  Versand, Festschreibung, Periodenabschluss oder steuerliche Prüfung.
- Fehlende Daten sind kein Beleg dafür, dass der Sachverhalt erledigt ist.

## Wenn etwas nicht klappt

- **Nicht verbunden oder Anmeldung abgelaufen:** Bitte den Nutzer, Fin3000 im
  Host neu zu verbinden (in Claude „Verbinden“ bzw. `/mcp` → Authenticate).
  Nichts raten, nichts aus alten Antworten übernehmen.
- **Werkzeug fehlt in der Liste:** Der Server oder das Plugin ist älter als
  dieser Skill. Plugin und Verbindung neu laden lassen. Ein fehlendes Werkzeug
  ist kein Hinweis auf ein fehlendes Abo und kein Grund, ein anderes
  Schreibwerkzeug zu verwenden.
- **`feature_inactive`:** Der KI-Assistent ist im Fin3000-Konto ausgeschaltet.
  Der Admin schaltet ihn unter Einstellungen → Funktionen ein
  (https://app.fin3000.com/features).
- **Keine Berechtigung:** Das Konto darf diesen Bereich nicht sehen. Den Admin
  des Fin3000-Kontos fragen; keine Ersatzdaten liefern.
