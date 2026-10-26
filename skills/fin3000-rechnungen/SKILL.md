---
name: fin3000-rechnungen
description: Prüfe Kundenrechnungen, Forderungen und offene Posten in Fin3000 oder bereite einen bestätigungspflichtigen Rechnungsentwurf vor; nutze den Skill bei Fragen zu Rechnungen, Rechnung schreiben, Kunden und Zahlungseingängen, nicht für Versand, Finalisierung oder Mahnungen.
---

# Fin3000 Rechnungen

Prüfe bestehende Rechnungen oder führe den sicheren Vorschau- und
Bestätigungsablauf für Stammdaten und Rechnungsentwürfe aus.

Bei einem ausdrücklichen Auftrag zum Erledigen oder Korrigieren verwende
`fin3000-buchhaltung-vervollstaendigen`. Dessen Revision 1 prüft vorhandene
Rechnungen und veröffentlichte Dateien vor neuen Uploads. Ein Ownerpostfach ohne
feste Firmenbindung ist nicht automatisch unkonfiguriert. Fehlende Revision oder
Werkzeuge im Host als Abdeckungsgrenze nennen; keine Parameter erfinden und
keine Vollständigkeit aus einer einzelnen Suchseite ableiten.

## Bestehende Rechnungen prüfen

1. Rufe `get_context` auf und löse die gewünschte Business Unit eindeutig auf.
2. Nutze `search_clients`, wenn der Kunde nicht eindeutig ist.
3. Nutze `list_open_items` mit der Forderungsseite für offene oder überfällige
   Kundenrechnungen. Nutze `search_sales_documents` für eine allgemeinere
   Belegsuche und `get_sales_document` erst mit einer gefundenen Dokument-ID.
4. Gib Status, Fälligkeit, offene Beträge, Business Unit und verfügbare
   Fin3000-Links wieder, ohne einen Zahlungseingang zu behaupten.

## Kunden und Rechnungsentwürfe vorbereiten

1. Suche vor einer Kundenanlage mit `search_clients` nach einem bestehenden
   passenden Datensatz. Lege nur auf ausdrücklichen Wunsch einen neuen Kunden
   mit `create_client` an.
2. Der erste Aufruf eines Schreibwerkzeugs dient ausschließlich der Vorschau.
   Zeige die Wirkung verständlich an und frage danach separat nach einer
   ausdrücklichen Bestätigung.
3. Verwende den zurückgegebenen `confirmation_token` nur nach dieser
   Bestätigung und nur mit unverändertem Payload. Bei jeder Änderung an Kunde,
   Business Unit, Positionen, Menge, Preis oder Text fordere eine neue Vorschau
   an.
4. Löse für einen Rechnungsentwurf den Kunden mit `search_clients` und die
   Business Unit mit `get_context` auf. Frage bei fehlenden oder mehrdeutigen
   Positionen, Mengen oder Preisen nach, bevor du `create_invoice_draft`
   aufrufst.
5. Soll für einen neuen Kunden direkt eine Rechnung entstehen, übergib den
   Kunden als `new_customer` mit vollständiger Rechnungsadresse an
   `create_invoice_draft`. Fin3000 zeigt Kunde und Entwurf in **einer**
   Vorschau und speichert beides nach **einer** Bestätigung atomar. Nutze
   `create_client` nur, wenn ausschließlich ein Kunde angelegt werden soll.
   Bei mehreren Adressen eines Kunden `billing_address_id` wählen, nie raten.
6. Melde nach Erfolg die erzeugte ID, den Status `DRAFT`, die betroffene
   Business Unit und den Fin3000-Link. Wiederhole einen bestätigten Aufruf nicht
   eigenmächtig.

## Einzelne Waren nach §25a abrechnen

- Suche vorhandene Ankäufe mit `list_margin_acquisitions` vollständig und lies
  die passende Grundlage mit `get_margin_acquisition`. Firmenbindung, Original,
  tatsächlichen EUR-Einkaufspreis, Menge und steuerliche Voraussetzungen prüfen.
  Produktkosten, Banktexte oder ein fehlender Steuerausweis sind kein Nachweis.
- Fehlt die Grundlage, nutze `save_margin_acquisition`: Vorschau zeigen und
  separat bestätigen lassen. EU-Lieferung und Eignung des Verkäufers nur bei
  ausdrücklich geklärtem Sachverhalt bestätigen. Dies speichert eine Grundlage,
  keine zusätzliche Aufwands- oder Lagerbuchung.
- Übergebe an `create_invoice_draft` pro belegter Warenposition ausdrücklich
  `tax_scheme=MARGIN_25A`, `margin_acquisition_id`, Menge und vollen Verkaufspreis.
  Der normale Steuerfall/Konto8191 allein reicht nicht. Zeige auch die private
  Margenberechnung; sie gehört nicht auf die Kundenrechnung. Den Entwurf erst
  nach separater Bestätigung speichern. Ein leerer Einkaufspreis ist ungeklärt;
  null Euro nur bei nachgewiesen unentgeltlichem Erwerb.
- Native Finalisierung erzeugt interne Margensteuer und den gesetzlichen
  Warenhinweis ohne gesonderten Steuerausweis auf Kunden-PDF/XML. Originalbeleg
  und Aufwandsbuchung separat vollständig prüfen. MCP finalisiert nicht.
- Unterstützt ist die belegte Einzeldifferenz für normale Rechnungen und
  vollständigen nativen Storno. Gesamtdifferenz, Sonderankäufe nach §25aAbs2,
  Anzahlungen, Teilrückgaben, Skonto, Fremdwährungsankäufe, Nicht-EU-Ausfuhren
  und Kleinunternehmer sind nicht enthalten. Native Istversteuerung bleibt
  möglich; DATEV-Export positiver IST-Margen ist noch gesperrt. Keine andere
  Kontierung verwenden, um diese Grenze zu umgehen.

## Grenzen

- Fin3000 kann über diesen Workflow nur einen Rechnungsentwurf anlegen. Es kann
  ihn nicht finalisieren, festschreiben, bezahlen, versenden oder öffentlich
  bereitstellen.
- Keine Sammelanlagen und keine stillen Folgeschreibvorgänge. Buchen,
  Zahlungen ausgleichen und Belege zuordnen gehören zu
  `fin3000-buchhaltung-vervollstaendigen`.
- Eine ursprüngliche Bitte wie „Erstelle eine Rechnung“ ist keine Bestätigung
  der anschließend erzeugten Vorschau.
- Erfinde keine Kunden-ID, Rechnungsposition, Steuerangabe oder Zahlung.

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
