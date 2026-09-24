---
name: fin3000-rechnungen
description: Prüfe Kundenrechnungen, Forderungen und offene Posten in Fin3000 oder bereite einen bestätigungspflichtigen Rechnungsentwurf vor; nutze den Skill bei Fragen zu Rechnungen, Rechnung schreiben, Kunden und Zahlungseingängen, nicht für Versand, Finalisierung oder Mahnungen.
---

# Fin3000 Rechnungen

Prüfe bestehende Rechnungen oder führe den sicheren Vorschau- und
Bestätigungsablauf für Stammdaten und Rechnungsentwürfe aus.

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
5. Wenn Kunde und Entwurf neu angelegt werden sollen, behandle sie als zwei
   getrennte Schreibvorgänge mit zwei Vorschauen und zwei Bestätigungen.
6. Melde nach Erfolg die erzeugte ID, den Status `DRAFT`, die betroffene
   Business Unit und den Fin3000-Link. Wiederhole einen bestätigten Aufruf nicht
   eigenmächtig.

## Grenzen

- Fin3000 kann über diesen Workflow nur einen Rechnungsentwurf anlegen. Es kann
  ihn nicht finalisieren, festschreiben, bezahlen, versenden oder öffentlich
  bereitstellen.
- Keine Sammelanlagen und keine stillen Folgeschreibvorgänge.
- Eine ursprüngliche Bitte wie „Erstelle eine Rechnung“ ist keine Bestätigung
  der anschließend erzeugten Vorschau.
- Erfinde keine Kunden-ID, Rechnungsposition, Steuerangabe oder Zahlung.
