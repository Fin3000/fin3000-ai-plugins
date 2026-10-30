---
name: fin3000-firma-einrichten
description: Richte eine Firma in Fin3000 ein oder ändere ihre Einstellungen – Firmendaten, Anschrift, Kontakt, Bankverbindung für Rechnungen, Rechnungsnummern und Zahlungsziele, Rechnungsdesign mit Mustervorschau und Belegpostfach; nutze den Skill bei „Richte meine Firma ein“, „Wie sieht meine Rechnung aus?“ oder Änderungen an Stammdaten der eigenen Firma, nicht für Kunden oder Buchungen.
---

# Firma einrichten

Führe den Kontoinhaber durch die Einrichtung seiner Firma. Zeige zuerst, was
schon da ist, frage nur Fehlendes ab, zeige ein Rechnungsmuster und speichere
erst nach Bestätigung.

Nur der aktive Kontoinhaber kann diese Werkzeuge nutzen. Einstellungen lesen
und das Rechnungsmuster anzeigen geht auch mit einer lesenden Verbindung; zum
Speichern und Umbenennen braucht die Verbindung zusätzlich Schreibzugriff.
Fehlen die Werkzeuge, das erklären und auf die Fin3000-App verweisen.

## Vorgehen

1. Rufe `get_context` auf und danach `get_company_setup`. Bei genau einer Firma
   wird sie automatisch gewählt, sonst die gemeinte Firma ausdrücklich angeben
   (`business_unit_id`).
2. Lies `current_setup` als vorhandene Werte und `field_metadata` als deren
   Herkunft. Zeige dem Nutzer kurz: was steht schon fest, was ist eine
   unbestätigte Annahme aus der Registrierung, was fehlt.
3. Frage nur nach fehlenden oder unbestätigten Angaben, in kleinen Gruppen:
   Firma und Rechtsform, Anschrift, Kontakt, Bankverbindung für Rechnungen,
   Rechnungsnummern und Zahlungsziel, Design, Belegpostfach.
4. Steuerliche Angaben nie selbst wählen oder ableiten: Umsatzsteuer-Regelung
   (`vat_regime`, z. B. Kleinunternehmer), Soll- oder Istversteuerung
   (`vat_calculation_method`, nur mit Wirksamkeitsdatum
   `vat_calculation_method_effective_from`), Steuernummer, USt-IdNr. und
   Finanzamt kommen ausschließlich vom Nutzer. Bei Unsicherheit auf den
   Steuerberater verweisen, nichts vorschlagen.
5. Zeige vor dem Speichern ein Rechnungsmuster mit `preview_invoice_layout` und
   denselben geplanten Änderungen (`setup`). Das Muster ist als MUSTER markiert,
   speichert nichts und vergibt keine Rechnungsnummer. Kann der Host kein PDF
   anzeigen, `text_preview` zeigen.
6. Rufe `configure_company_setup` mit `setup` ohne Token auf. Das ist nur die
   Vorschau: Zeige alle Änderungen, Auswirkungen und betroffenen Bereiche
   vollständig und frage ausdrücklich nach Bestätigung.
7. Erst nach einem klaren Ja denselben Aufruf mit identischem `setup` plus
   `confirmation_token` wiederholen. Danach `get_company_setup` erneut lesen und
   die verbleibenden fehlenden Angaben nennen.

## Wichtige Regeln

- Weggelassene Felder bleiben unverändert; `null` leert nur optionale Felder.
  Nur übergeben, was sich wirklich ändern soll.
- Ist die Vorschau veraltet (`setup_changed`), aktuellen Stand neu lesen,
  Änderungen neu zeigen und neu bestätigen lassen. Bei `setup_busy` oder einer
  unklaren Antwort denselben Token später erneut verwenden; nicht neu schreiben.
- `state=committed` mit `warnings` heißt: gespeichert, aber eine Folgeaktion ist
  fehlgeschlagen. Warnung zeigen, nicht erneut speichern.
- Bankverbindung hier ist nur die IBAN, die auf Rechnungen steht. Eine
  Bankanbindung für Kontoumsätze, ein eigener Mailserver (SMTP),
  ELSTER-Zertifikat und Abos werden in der Fin3000-App eingerichtet.
- Logo und Briefpapier können nur als bereits hochgeladene Datei
  (`logo_file_id`, `letterhead_file_id`) gesetzt werden; das Hochladen selbst
  geschieht in der App.

## Belegpostfach

- `receiving` regelt das Belegpostfach: aktiv oder nicht, erlaubte Absender
  (`allowed_senders`) und optional eine feste Firma für eingehende Belege.
- Die Adresse des Postfachs ändert nur `rename_receiving_address` mit eigener
  Vorschau: alte und neue Adresse, Reservierung der alten Adresse und
  Aufräumarbeiten zeigen, dann mit Token bestätigen. Belege an die alte Adresse
  bleiben erhalten.

## Grenzen

- Keine erfundenen Firmendaten, keine Platzhalter wie „Musterstraße“ in echten
  Einstellungen.
- Die ursprüngliche Bitte „Richte meine Firma ein“ ist keine Bestätigung der
  späteren Vorschau.
- Kunden und Lieferanten gehören zu `fin3000-kunden`, Rechnungen zu
  `fin3000-rechnungen`.

## Wenn etwas nicht klappt

- **Nicht verbunden oder Anmeldung abgelaufen:** Bitte den Nutzer, Fin3000 im
  Host neu zu verbinden. Nichts raten, nichts aus alten Antworten übernehmen.
- **Werkzeug fehlt in der Liste:** Nur der Kontoinhaber hat die
  Einrichtungswerkzeuge, zum Speichern zusätzlich mit Schreibzugriff; oder
  Server bzw. Plugin sind älter als dieser Skill. Die Einstellungen sind dann in der Fin3000-App unter Einstellungen
  erreichbar.
- **`feature_inactive`:** Der KI-Assistent ist ausgeschaltet; der Admin schaltet
  ihn unter Einstellungen → Funktionen ein (https://app.fin3000.com/features).
- **Keine Berechtigung:** Den Kontoinhaber fragen; keine Ersatzdaten liefern.
