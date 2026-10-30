---
name: fin3000-einstieg
description: Erkläre und starte die Arbeit mit Fin3000 – welche Firmen verbunden sind, was die KI lesen und ändern darf, wie Vorschau und Bestätigung funktionieren und welcher Fin3000-Skill zur Aufgabe passt; nutze den Skill bei „Was kannst du mit Fin3000?“, „Wie fange ich an?“, beim ersten Kontakt oder wenn unklar ist, wo ein Auftrag hingehört.
---

# Mit Fin3000 arbeiten

Fin3000 ist eine Buchhaltung für Selbstständige, Freelancer, GbR, UG und GmbH
in Deutschland. Über diese Verbindung liest die KI die Daten des verbundenen
Kontos und bereitet Änderungen vor. Rechnungen, Kunden, Buchungen und
Einstellungen werden erst gespeichert, wenn der Nutzer die Vorschau
ausdrücklich bestätigt hat.

## Zuerst orientieren

1. Rufe `get_context` auf. Es liefert die Firmen (Business Units) mit ihren IDs,
   die Zugriffsstufe der Verbindung, die erlaubten Werkzeuge und die aktiven
   Funktionen. Verwende nur diese Firmen und IDs; nie Namen oder IDs raten.
2. Hat das Konto mehrere Firmen und ist die gemeinte nicht eindeutig, frage
   nach. Werte mehrerer Firmen nur auf ausdrücklichen Wunsch zusammenfassen.
3. Für die Frage „Was geht hier alles?“ oder bei einem Werkzeug, das in der
   Liste fehlt, rufe `get_capabilities` auf. Es zeigt jede Fähigkeit, ob sie
   über diese Verbindung verfügbar ist und was nur in der Fin3000-App geht.
   Ergebnisse kommen seitenweise (`next_cursor`); für eine vollständige
   Übersicht allen Seiten folgen, sonst als Auswahl kennzeichnen.
4. Erkläre dem Nutzer in wenigen Sätzen, was mit seiner Verbindung möglich ist.
   Keine Werkzeugnamen auflisten, sondern Aufgaben in seiner Sprache.

## Welcher Skill passt

| Der Nutzer möchte … | Skill |
|---|---|
| Zahlen sehen: BWA, Umsatz, Gewinn, offene Posten | `fin3000-buchhaltung` |
| eine Rechnung schreiben oder offene Rechnungen prüfen | `fin3000-rechnungen` |
| Kunden oder Lieferanten suchen, anlegen, ändern | `fin3000-kunden` |
| Belege hochladen, Eingangsrechnungen prüfen, Beleg zu Zahlung zuordnen | `fin3000-belege` |
| „Mach meine Buchhaltung“: zuordnen, kontieren, buchen | `fin3000-buchhaltung-vervollstaendigen` |
| prüfen, ob der Monat fertig ist | `fin3000-monatsabschluss` |
| Firma, Rechnungslayout oder Belegpostfach einrichten | `fin3000-firma-einrichten` |

## So funktionieren Änderungen

- **Erst Vorschau, dann Bestätigung.** Bei Rechnungen, Kunden, Buchungen,
  Korrekturen, Zuordnungen und Einstellungen speichert der erste Aufruf nichts,
  sondern liefert eine Vorschau und einen `confirmation_token`. Zeige die Vorschau vollständig und frage ausdrücklich,
  ob gespeichert werden soll.
- Erst nach einem klaren Ja denselben Aufruf mit identischen Angaben plus Token
  wiederholen. Ändert sich etwas, gibt es eine neue Vorschau und eine neue
  Bestätigung. Die ursprüngliche Bitte („Schreib eine Rechnung“) ist keine
  Bestätigung der Vorschau.
- Ist die Antwort verloren gegangen oder unklar, denselben Aufruf mit demselben
  Token wiederholen. Nie einen zweiten Datensatz anlegen, um sicherzugehen.
- Ausnahme: Belege hochladen und vorhandene Dateien weiterverarbeiten haben
  keine Vorschau. Das nur auf ausdrücklichen Wunsch starten (siehe
  `fin3000-belege`).
- Bei einem ausdrücklich erteilten Buchhaltungsauftrag kann Fin3000 mit einer
  gespeicherten Freigabe arbeiten (siehe `fin3000-buchhaltung-vervollstaendigen`).
- Fin3000 gibt Hinweise statt Verboten. Hinweise (`advisories`) in eigenen
  Worten weitergeben; die Entscheidung trifft der Nutzer.
- Ergebnisse enthalten Links in die Fin3000-App. Gib sie weiter, damit der
  Nutzer dort nachsehen oder weitermachen kann.

## Was die KI nicht tut

- Rechnungen finalisieren, versenden oder bezahlen, an ELSTER oder DATEV
  übermitteln, Bankverbindungen herstellen, Zugangsdaten eingeben. Das bleibt in
  der Fin3000-App beim Nutzer.
- Steuerliche Tatsachen erfinden oder schätzen (Steuersatz, Einkaufspreis,
  Vorsteuer). Fehlt etwas, nachfragen oder als unbekannt kennzeichnen.
- Steuer- oder Rechtsberatung leisten. Werte sind vorläufig, bis der Nutzer
  oder sein Steuerberater sie geprüft hat.

## Funktionen und Feedback

- Manche Funktionen sind Zusatzfunktionen, z. B. Differenzbesteuerung (§ 25a).
  Fehlt eine, schaltet der Admin sie unter Einstellungen → Funktionen ein
  (https://app.fin3000.com/features). Die KI schaltet nichts selbst ein.
- Wünscht sich der Nutzer eine Verbesserung oder neue Funktion, kann der
  Kontoinhaber sie mit `submit_product_feedback` einreichen (Vorschau, dann
  Bestätigung); `search_product_feedback` zeigt eigene Einreichungen. Fehler
  oder dringende Probleme gehören an support@fin3000.com.

## Wenn etwas nicht klappt

- **Nicht verbunden oder Anmeldung abgelaufen:** Bitte den Nutzer, Fin3000 im
  Host neu zu verbinden (in Claude „Verbinden“ bzw. `/mcp` → Authenticate, in
  ChatGPT unter Apps). Nichts raten, nichts aus alten Antworten übernehmen.
- **Werkzeug fehlt in der Liste:** Zugriffsstufe oder Rolle erlauben es nicht,
  oder Server bzw. Plugin sind älter als dieser Skill. `get_capabilities`
  zeigt den Grund. Kein anderes Schreibwerkzeug als Ersatz verwenden.
- **`feature_inactive`:** `details.feature` nennt die Funktion; der Admin
  schaltet sie unter Einstellungen → Funktionen ein. Ohne Angabe ist der
  KI-Assistent selbst ausgeschaltet (gleicher Ort).
- **Keine Berechtigung:** Das Konto darf diesen Bereich nicht sehen. Den Admin
  des Fin3000-Kontos fragen; keine Ersatzdaten liefern.
