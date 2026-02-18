# TOOLS.md – Lokale Tool-Notizen & Konfiguration

## Datenquellen (Google Sheets)

### AUFTRAGGEBER_Liste
- **Zweck:** Liste aller 805 Auftraggeber (fortlaufend nummeriert)
- **Link:** https://docs.google.com/spreadsheets/d/1T5Djl04Qtfr6D78IL7p1VuKToJUx2YdKWnjrBOXScxc/edit
- **Hinweis:** Nur lesen. Nie bearbeiten.

### PROGRESS_TRACKER
- **Zweck:** Speichert die zuletzt bearbeitete Auftraggeber-Nummer + Recherche-Log
- **Link:** https://docs.google.com/spreadsheets/d/1U4GdjR58phiA_kL13kcBBCIqUQg9Lc5Thesl4mSVWj4/edit
- **Felder pro Eintrag:**
  - Auftraggeber-Nummer
  - Suchbegriff
  - Ergebnis (Treffer / Kein Treffer)
  - Zeitstempel
- **Hinweis:** Nach JEDER web_search sofort aktualisieren!

### ANGEBOTE_Liste
- **Zweck:** Alle bereits gefundenen Projekte (Duplikat-Prüfung + neue Einträge)
- **Link:** https://docs.google.com/spreadsheets/d/1aF3bqQSK8twh5C2nspwlHqw65KRF0iBLeX2YnOkw3do/edit
- **Spalten für neue Einträge:**
  - City (Stadt)
  - Address (Adresse)
  - Asset Name (Projektname)
  - Investor Developer (Unternehmen)
  - Opening (Fertigstellungsdatum)
  - No. of Beds (Anzahl Wohneinheiten/Betten)

⚠️ **Wichtig:** Die tatsächlichen Google Sheet Links müssen vom User eingetragen werden. Die Platzhalter oben ersetzen!

---

## Recherche-Tool

### web_search (Perplexity Sonar Pro)
- **Strategie:** 1 Suchabfrage pro Auftraggeber
- **Suchformel:** `[Auftraggeber-Name] + "Studentenwohnheim"` ODER `"Wohnungsprojekt"` ODER `"Neubau"`
- **Filter:** 50+ Einheiten, Baubeginn Q3 2026–2028, Region DE/AT
- **Tipp:** Bei unklaren Ergebnissen, Auftraggeber-Name mit Stadtname kombinieren

---

## Versand: Telegram

### Bot-Konfiguration
- **Bot Token:** `8415926959:AAEOI6koO0uuevYs2REKgUkVkMP3xsspmzc`
- **Chat ID:** `7627639740`
- **API Endpoint:** `https://api.telegram.org/bot<TOKEN>/sendMessage`

### Nachricht-Template

```
📊 WOCHENBERICHT Studentenwohnheime
📅 KW XX | DD.MM.YYYY

✅ 5 neue Projekte gefunden:

1️⃣ [Projektname] – [Stadt], [Land]
🏗️ Baubeginn: [Quartal/Jahr]
🏢 [Unternehmen]
📐 [Anzahl] Einheiten

2️⃣ [Projektname] – [Stadt], [Land]
🏗️ Baubeginn: [Quartal/Jahr]
🏢 [Unternehmen]
📐 [Anzahl] Einheiten

3️⃣ ...
4️⃣ ...
5️⃣ ...

📋 Vollständiger Bericht: per E-Mail

🔄 Nächster Auftraggeber: #[Nummer]
```

---

## Versand: E-Mail

- **Empfänger:** cyclus2000akan@gmail.com
- **Betreff:** `Wochenbericht Studentenwohnheime KW XX – DD.MM.YYYY`
- **Inhalt:** Vollständiger Wochenbericht als Anhang
- **Dateiname:** `wochenbericht_DD-MM-YYYY.txt`

---

## Zeitplan (Cron)

- **Automatischer Start:** Jeden Montag um 06:35 Uhr
- **Deadline:** Bericht fertig + versendet bis spätestens Montag 06:35 Uhr
- **Modus:** Isolierte Session (kein Zusammenhang mit laufenden Chats)

---

## Fallback-Strategie

Wenn nach komplettem Durchlauf der Auftraggeber-Liste keine 5 Treffer: Bundesland-Recherche starten in dieser Reihenfolge:

1. Bayern
2. Baden-Württemberg
3. NRW
4. Niedersachsen
5. Hessen
6. Sachsen
7. Berlin
8. Hamburg
9. Weitere Bundesländer + Österreich

Suchbegriffe: `"Studentenwohnheim Neubau [Bundesland] 2026 2027 2028"`

---

## Notizen

- Keine lokalen Dateien (.txt, .csv) verwenden — alles lebt in Google Sheets
- Google Sheets sind die einzige Datenquelle
- Platform-Formatierung: Telegram unterstützt kein Markdown — Emojis + Plaintext verwenden
