# HEARTBEAT.md – Foness Proaktive Checks

## Montag-Check (Hauptlauf)

- [ ] Ist heute Montag? → Wenn ja: Starte den vollständigen Wochenbericht-Workflow (AGENTS.md Schritt 1–6)
- [ ] Prüfe PROGRESS_TRACKER: Letzte bearbeitete Auftraggeber-Nummer aktuell?
- [ ] Prüfe ANGEBOTE_Liste: Letzte Einträge korrekt formatiert?

## Täglicher Quick-Check (Di–So)

- [ ] Wurde der Wochenbericht diese Woche bereits versendet?
- [ ] Gibt es offene Fehler im letzten Recherche-Durchlauf? (memory/ prüfen)
- [ ] Falls Montags-Bericht fehlgeschlagen → Nachlauf starten

## Wöchentliche Memory-Pflege

- [ ] memory/YYYY-MM-DD.md Dateien der letzten Woche durchlesen
- [ ] Relevante Erkenntnisse in MEMORY.md übertragen
- [ ] Veraltete Einträge in MEMORY.md entfernen

## Stille Zeiten

- 23:00–06:00 Uhr: Keine Nachrichten senden (außer Montag 06:35 Cron)
- Wenn nichts zu tun ist: HEARTBEAT_OK
