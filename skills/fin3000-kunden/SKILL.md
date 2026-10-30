---
name: fin3000-kunden
description: Verwalte Kunden und Lieferanten in Fin3000 – suchen, Stammdaten und Adressen nachschlagen, neu anlegen, ändern und die bisherige Kontierung eines Partners einsehen; nutze den Skill bei „Leg den Kunden … an“, „Ändere die Adresse von …“ oder „Was wissen wir über …?“. Für Kunde plus Rechnung in einem Schritt dient fin3000-rechnungen.
---

# Kunden und Lieferanten

## Finden und nachschlagen

1. Rufe `get_context` auf, wenn die Firma gebraucht wird.
2. `search_clients` sucht Kunden und Lieferanten nach Name, Firma, Kunden- oder
   Lieferantennummer (`kind`: `customer`, `supplier` oder `both`). Mehrere
   Treffer zeigen und nachfragen, nie den erstbesten nehmen.
3. `get_client` liefert alle Stammdaten mit Adressen, E-Mails, Telefonnummern,
   Zahlungsbedingungen und deren stabilen IDs. Inaktive Partner nur auf
   ausdrücklichen Wunsch (`include_inactive`).
4. Für „Wie buchen wir diesen Lieferanten normalerweise?“ `get_client_account_context`
   mit Firma und Partner: zeigt Standardkonto, eigene bestätigte Buchungen und
   Belege. Steuerliche Behandlung daraus nicht ableiten, nur zeigen.

## Neu anlegen

1. Vorher mit `search_clients` prüfen, ob es den Partner schon gibt. Eine
   Dublette nur auf ausdrücklichen Wunsch (`allow_duplicate`).
2. Soll für einen neuen Kunden gleich eine Rechnung entstehen, nicht hier
   anlegen, sondern `fin3000-rechnungen` (`create_invoice_draft` mit
   `new_customer`): eine Vorschau, eine Bestätigung.
3. Sonst `create_client` mit Rechnungsadresse und den genannten Stammdaten ohne
   Token: Vorschau vollständig zeigen, ausdrücklich bestätigen lassen, dann mit
   identischen Angaben plus `confirmation_token` speichern.
4. Nur übergeben, was der Nutzer oder ein Beleg nennt. Keine USt-IdNr.,
   Steuernummer, Leitweg-ID oder Zahlungsziele erfinden.
5. Ein Standard-Buchungskonto (`default_book_account_id`) ist ein
   Buchungsvorschlag und braucht `confirm_booking_default=true` sowie eine
   ausdrückliche Zustimmung. Erlös- und Steuerkonten gehören an
   Rechnungspositionen, nicht hierher.

## Ändern

1. Erst `get_client`, um die IDs der betroffenen Adresse, E-Mail oder
   Telefonnummer zu kennen.
2. `update_client` mit nur den zu ändernden Feldern (`changes`) ohne Token: Die
   Vorschau zeigt vorher/nachher und betroffene offene Rechnungsentwürfe.
   Ausdrücklich bestätigen lassen, dann mit identischen Angaben plus Token
   speichern. Nicht genannte Kontakte, Adressen und Bankdaten bleiben erhalten.
3. Kommt die Änderung zusammen mit einer neuen Rechnung, `customer_changes` in
   `create_invoice_draft` verwenden (eine Bestätigung für beides).

## Grenzen

- Keine Partner löschen oder zusammenführen; das geschieht in der Fin3000-App.
- Eine gespeicherte Debitorennummer steuert derzeit keine Buchungskonten.
- Bei `busy` kurz warten und denselben Aufruf höchstens zweimal wiederholen;
  bei unklarem Ausgang nur mit demselben Token, bei `preview_changed` neue
  Vorschau und neue Bestätigung.

## Wenn etwas nicht klappt

- **Nicht verbunden oder Anmeldung abgelaufen:** Bitte den Nutzer, Fin3000 im
  Host neu zu verbinden. Nichts raten, nichts aus alten Antworten übernehmen.
- **Werkzeug fehlt in der Liste:** Rolle oder Zugriffsstufe erlauben es nicht,
  oder Server bzw. Plugin sind älter als dieser Skill. Kein anderes
  Schreibwerkzeug als Ersatz verwenden.
- **`feature_inactive`:** Der KI-Assistent ist ausgeschaltet; der Admin schaltet
  ihn unter Einstellungen → Funktionen ein (https://app.fin3000.com/features).
- **Keine Berechtigung:** Den Admin des Fin3000-Kontos fragen; keine
  Ersatzdaten liefern.
