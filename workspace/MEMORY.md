# MEMORY.md - Long-Term Memory

## User Preferences
- **Always add confirmation, feedback, or a question to every response** - This is a hard requirement from Akan
- Stay humorous and entertaining
- Use cool emojis
- Language: German (informal "du") - **IMMER** auf Deutsch antworten, auch bei Audio/TTS nach Telegram!
- **Audio-Antworten:** Wenn Nutzer "Audio Nachricht" oder "antworte per Voice" sagt/schreibt → mit TTS über Telegram antworten (nur dann!)
- **Web Search:** NUR Perplexity nutzen, NIE auf Brave verweisen
- **Memory-Pflicht:** VOR JEDER Antwort MEMORY.md UND memory/2026-XX-XX.md lesen → immer den Chatverlauf kennen!
- **Speicherregel:** "merke dir das" → speichert in MEMORY.md (lokal) UND SuperMemory (cloud)

## About Akan
- Works in AI & AI automation
- Telegram ID: 7627639740
- Email: info@wappreport.com
- Timezone: Europe/Berlin
- **Google Kalender:** IMMER beide Kalender checken: info@wappreport.com UND akan@wappreport.com

## Setup History
- 2026-02-14: Initial workspace setup with Neo (AI assistant)
- Google Workspace connected (gog CLI) - Gmail, Calendar, Drive, Sheets, Docs
- Created first Google Sheet "Akan Testo" in openclaw-backup/foness folder

## Teamstruktur
| Wer | Was | Modell |
|-----|-----|--------|
| Neo (ich) | Assistant, Recherche, Memory | MiniMax M2.5 |
| foness | Wochenbericht Research (5 Projekte/Woche) | Perplexity Sonar Pro |

## Wichtige Entscheidungen
1. **Perplexity statt Brave** – bessere Ergebnisse
2. **Voice nur auf Anfrage** – "antworte per Voice"
3. **Beide Google Kalender** – info@ + akan@wappreport.com
4. **Gruppen nur mit Mention** – Spam vermeiden

## Gewonnene Erkenntnisse
- ✅ Google Workspace Integration funktioniert super
- ✅ Memory-System (lokal + SuperMemory) läuft
- ❌ YouTube-Transkription blockiert (Bot-Erkennung)
- ❌ Gruppen-Nachrichten kommen manchmal nicht durch

## Aktive Projekte
- Telegram-Gruppen-Setup optimieren
- Heartbeat-Checks etablieren

## OpenClaw Dashboard Fix (16.02.2026)
- Problem: Dashboard-Dateien (Agents → Files) wurden nicht persistent gespeichert
- Ursache: gateway.trustedProxies war auf ["127.0.0.1/32"] beschränkt
- Verbindung: Browser → Cloudflare Tunnel → Hostinger-Proxy (:57040) → OpenClaw Gateway (:18789)
- Der Hostinger-Proxy leitete X-Forwarded-For Headers weiter, Gateway erkannte externe IPs nicht als lokal
- Fix: trustedProxies auf ["0.0.0.0/0", "::0/0"] erweitert (sicher weil Port an 127.0.0.1 gebunden)
- Ergebnis: Dateien speichern, Agenten anlegen, Config-Änderungen funktionieren jetzt
- Lock-Files durch alte Crash-Sessions (ungültiger Cron-Key) verursacht
