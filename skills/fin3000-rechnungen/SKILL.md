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
   Positionen, Mengen oder Verkaufspreisen nach, bevor du `create_invoice_draft`
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

## Waren nach §25a (Differenzbesteuerung) abrechnen

- §25a ist eine Steuerart der Position, kein Konto. Setze an der Warenposition
  `tax_scheme=MARGIN_25A` und als `unit_price` den vollen Kundenpreis (Endpreis,
  keine Umsatzsteuer aufschlagen). Hat das Produkt §25a als Steuerart, genügt
  `product_id`. Übergib nie ein §25a-Konto (z. B. 8191) als `account_id`.
- Mehr ist nicht nötig. Frage nicht von dir aus nach Einkaufspreis, Ankaufsbeleg,
  Verkäufer oder Bestätigungen. Ohne Einkaufspreis versteuert Fin3000 den vollen
  Verkaufspreis; Gebrauchtgegenstand und Kauf von Privatperson gelten als
  sichtbar gekennzeichnete Annahme.
- Optional, nur wenn der Nutzer oder ein Beleg es nennt: `unit_purchase_price`
  (Einkaufspreis je Stück in EUR), `goods_kind` (`USED_GOODS`, `ART`,
  `COLLECTORS_ANTIQUES`), `acquired_from` (`PRIVATE_SELLER`, `SMALL_BUSINESS`,
  `MARGIN_RESELLER`, `EXEMPT_SUPPLIER`), `art_flat_rate` (nur bei `ART`).
  Einkaufspreis nie schätzen und nicht aus Verkaufspreis, Marktwert oder
  früheren Gesprächen ableiten. `0` nur bei ausdrücklich unentgeltlichem Erwerb.
- Hat das Produkt Einkaufskosten, übernimmt Fin3000 sie „aus Produkt“ und meldet
  das. Sagt der Nutzer, der Wert stimmt nicht, übergib den genannten Preis oder
  `unit_purchase_price: null` (unbekannt).
- Zwei Wege, beide freiwillig: direkt an der Position (oben) oder über einen
  gespeicherten Ankauf. Nennt der Nutzer einen Ankauf, such ihn mit
  `list_margin_acquisitions` und übergib `margin_acquisition_id`; die übrigen
  §25a-Felder dann weglassen. Einen Ankauf mit `save_margin_acquisition` nur auf
  ausdrücklichen Wunsch anlegen (eigene Vorschau und Bestätigung).
  `ready=false` heißt nur, dass freiwillige Angaben fehlen.
- Zeige die §25a-Zeile der Vorschau und gib Hinweise (`advisories`) in eigenen
  Worten als Hinweis weiter, nicht als Fehler und nicht als Pflichtfrage.
  Einkauf, Marge und interne Umsatzsteuer stehen nicht auf der Kundenrechnung.
  MCP finalisiert nicht.
- Beispiel: „Kommode, 150 €, §25a“ → `items=[{"title": "Kommode, Eiche, gebraucht",
  "unit_price": "150.00", "tax_scheme": "MARGIN_25A"}]`, Vorschau zeigen, einmal
  bestätigen lassen.
- Nicht enthalten (Fin3000 meldet es): Gesamtdifferenz, Sonderankäufe nach §25a
  Abs. 2, Anzahlungen und Teilrechnungen, Teilrückgaben, Skonto, Kleinunternehmer.
  DATEV-Export positiver IST-Margen ist noch gesperrt; native Istversteuerung
  bleibt möglich. Lieferung außerhalb der EU ergibt einen Hinweis (§ 4 Nr. 1a
  UStG prüfen). Keine andere Kontierung verwenden, um eine Grenze zu umgehen.
- Lehnt der Server `MARGIN_25A` ohne `margin_acquisition_id` ab, ist er älter
  als dieser Skill: nichts erfinden, den Nutzer informieren.

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
- **`feature_inactive`:** `details.feature` nennt die Funktion. Bei
  `margin_taxation` ist die Differenzbesteuerung nicht aktiviert: der Admin
  schaltet „Differenzbesteuerung (§ 25a)“ unter Einstellungen → Funktionen ein
  (https://app.fin3000.com/features), oder die Position wird auf Wunsch normal
  besteuert. Sonst ist der KI-Assistent ausgeschaltet (gleicher Ort).
- **Keine Berechtigung:** Das Konto darf diesen Bereich nicht sehen. Den Admin
  des Fin3000-Kontos fragen; keine Ersatzdaten liefern.
