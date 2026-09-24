---
name: fin3000-buchhaltung
description: Analysiere die Buchhaltung von Freelancern, Selbstständigen und GbRs in Fin3000, insbesondere BWA, Einnahmen, Ausgaben, Gewinn und offene Posten; nutze den Skill für Finanzüberblicke und Vergleiche, nicht für Monatsabschluss-Checklisten oder das Erstellen von Rechnungen.
---

# Fin3000 Buchhaltung

Erstelle einen belegbaren, grundsätzlich nur lesenden Finanzüberblick aus den
Fin3000-Daten des verbundenen Kontos.

## Vorgehen

1. Rufe zuerst `get_context` auf. Verwende ausschließlich die dort gelieferten
   Business Units und Fähigkeiten.
2. Ist die gewünschte Business Unit nicht eindeutig, frage nach. Erfinde oder
   errate weder Namen noch IDs. Bei einem Vergleich rufe die BU-fähigen Tools
   für jede Business Unit getrennt auf.
3. Wähle nur die zum Auftrag passenden Werkzeuge:
   - `get_financial_report` für BWA, Einnahmen, Ausgaben und Ergebnis;
   - `list_open_items` für offene Forderungen oder Verbindlichkeiten;
   - `search_sales_documents` und danach bei Bedarf `get_sales_document` für
     Ausgangsbelege;
   - `search_incoming_invoices` für Eingangsrechnungen;
   - `search_transactions` für Bank- und Kassenbewegungen;
   - `search_journal_entries` für Buchungen;
   - `get_vat_return_status` nur für den vorhandenen UStVA-/ELSTER-Status.
4. Übernimm Zeitraum, Währung, Scope und vorläufigen Status aus den Ergebnissen.
   Ein fehlender `year_to_date`-Block ist unbekannt und niemals als null zu
   interpretieren.
5. Gib pro Business Unit einen getrennten Abschnitt aus. Nenne Kennzahlen,
   Zeitraum und Datenbasis und verlinke die von Fin3000 gelieferten Deep-Links.
   Aggregiere mehrere Firmen nur auf ausdrücklichen Wunsch und kennzeichne die
   Addition als kontenübergreifende Zusammenfassung.

## Fachliche Grenzen

- Dieser Skill liest und erklärt. Rufe weder `create_client`,
  `create_invoice_draft` noch `categorize_transaction` auf.
- Verbindlichkeiten, Eingangsrechnungen, Transaktionen oder Journalbereiche
  dürfen nicht als BU-genau bezeichnet werden, wenn das jeweilige Tool nur den
  Owner-Scope liefert. Weise den Scope sichtbar aus.
- Stelle vorläufige Werte nicht als Jahresabschluss, Steuererklärung oder
  Steuerberatung dar.
- Sende nichts an ELSTER oder DATEV und behaupte keine Finalisierung, Zahlung
  oder Festschreibung.
- Erfinde keine fehlenden Zahlen. Benenne leere, nicht verfügbare und nicht
  berechtigte Ergebnisse unterschiedlich.
