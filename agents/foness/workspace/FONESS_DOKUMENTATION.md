# FONESS AGENT — Komplette Projektdokumentation

---

## 1. ÜBERSICHT

| Eigenschaft | Wert |
|---|---|
| **Agent-Name** | Foness 🏗️ |
| **Zweck** | Wöchentlich 5 neue Studentenwohnheim-/Wohnungsprojekte in DE/AT finden |
| **Plattform** | OpenClaw (Docker-Container) |
| **LLM-Modell** | MiniMax M2.5 (reasoning: true, contextWindow: 200k, maxTokens: 8192) |
| **Web-Search** | Perplexity Sonar Pro (API Key: `pplx-XXXX_REDACTED_XXXX`) |
| **Google Sheets** | via `gog` CLI v0.9.0 (Account: info@wappreport.com) |
| **User** | Akan Celik, Dornbirn/AT, Timezone Europe/Vienna |
| **Zeitplan** | Jeden Montag 06:35 Uhr (Cron — NOCH NICHT EINGERICHTET) |
| **Output** | Telegram-Nachricht + E-Mail-Bericht |

---

## 2. ARCHITEKTUR

```
┌─────────────────────────────────────────────────────┐
│  Hostinger VPS (Ubuntu)                             │
│                                                     │
│  ┌─────────────────────────────────────────────┐    │
│  │  Docker: openclaw-rmys-openclaw-1            │    │
│  │                                              │    │
│  │  OpenClaw Runtime                            │    │
│  │  ├── Agent: main (Default)                   │    │
│  │  │   └── subagent: foness                    │    │
│  │  ├── Agent: foness                           │    │
│  │  │   ├── Model: MiniMax M2.5                 │    │
│  │  │   ├── Workspace: /data/.openclaw/agents/  │    │
│  │  │   │             foness/workspace/         │    │
│  │  │   ├── Tools: web_search (Perplexity)      │    │
│  │  │   ├── Tools: gog (Google Sheets)          │    │
│  │  │   ├── Tools: exec (bash)                  │    │
│  │  │   └── Tools: read/write (files)           │    │
│  │  │                                           │    │
│  │  ├── Telegram Plugin (Bot: 8415926959)       │    │
│  │  ├── WhatsApp Plugin                         │    │
│  │  └── Gateway: Port 18789, bind: lan          │    │
│  └──────────────────────────────────────────────┘   │
│                                                     │
│  Cloudflare Tunnel → HTTPS → localhost:18789        │
│  gog CLI: /home/linuxbrew/.linuxbrew/bin/gog        │
└─────────────────────────────────────────────────────┘
```

---

## 3. DATEIEN & PFADE

### 3.1 Foness Agent Workspace
```
/data/.openclaw/agents/foness/workspace/
├── AGENTS.md          (7.5 KB) — Workflow-Definition, Hauptschleife, 6 Schritte
├── SOUL.md            (2.8 KB) — Persönlichkeit, Verhalten, Qualitätsstandards
├── TOOLS.md           (4.9 KB) — Google Sheet Links, Suchformeln, Telegram, E-Mail
├── IDENTITY.md        (282 B)  — Name, Emoji, Tagline
├── USER.md            (1.0 KB) — Akan Celik, Kontaktdaten, Erwartungen
├── MEMORY.md          (1.0 KB) — Langzeitgedächtnis (Platzhalter, noch leer)
├── HEARTBEAT.md       (902 B)  — Proaktive Checks (Montag/Täglich/Wöchentlich)
└── memory/
    └── 2026-02-16.md  (857 B)  — Tagesnotiz (Onboarding-Protokoll)
```

### 3.2 OpenClaw Hauptkonfiguration
```
/docker/openclaw-rmys/data/.openclaw/openclaw.json
```
(Im Container sichtbar als: `/data/.openclaw/openclaw.json`)

### 3.3 OpenClaw Haupt-Workspace (NICHT Foness)
```
/data/.openclaw/workspace/
├── AGENTS.md, BOOTSTRAP.md, BOOT.md, GITHUB_SETUP.md
├── HEARTBEAT.md, IDENTITY.md, MEMORY.md, SOUL.md
├── TOOLS.md, USER.md, infos.md
└── skills/ (self-improving-agent, sonoscli, supermemory, youtube-watcher)
```

### 3.4 Docker Container
```
Container:     openclaw-rmys-openclaw-1
Mounts:
  /docker/openclaw-rmys/data  →  /data
  /home/linuxbrew/.linuxbrew  →  /home/linuxbrew/.linuxbrew
  /usr/bin/rclone             →  /usr/local/bin/rclone
  /var/run/docker.sock        →  /var/run/docker.sock
```

---

## 4. GOOGLE SHEETS (3 Datenquellen)

### 4.1 AUFTRAGGEBER_Liste (nur lesen)
- **Sheet ID:** `1T5Djl04Qtfr6D78IL7p1VuKToJUx2YdKWnjrBOXScxc`
- **Tab:** Standardblatt (kein Name = default)
- **Format:** `| Nr. | Name,Stadt |`
- **Beispiel:** `| 1. | 360 Operator,Nuremberg |`
- **Umfang:** 805 Zeilen (#1 bis #805)
- **Zugriff:** `gog sheets get <ID> "A<N>:B<N>" --account info@wappreport.com`

### 4.2 PROGRESS_TRACKER (lesen + schreiben)
- **Sheet ID:** `1U4GdjR58phiA_kL13kcBBCIqUQg9Lc5Thesl4mSVWj4`
- **Tab:** `Tabellenblatt1`
- **Format:** ACHTUNG — unstrukturiert! Daten über mehrere Zeilen verteilt:
  ```
  Zeile 1: "212", "Die Gemeinnützige"
  Zeile 2: "Lübeck", "Kein Treffer", "Kein neues Projekt 2026-2028"
  ```
- **Aktueller Stand:** Letzte reguläre Nummer = #215 (K.St.V. Alamannia, Tübingen)
- **Danach:** Fallback-Eintrag ("5 Treffer via Fallback, KW 7 - 16.02.2026")
- **Danach:** #216 (Diözese Rottenburg-Stuttgart, TREFFER)
- **Zugriff:** `gog sheets get <ID> "A1:F20" --account info@wappreport.com`
- **Schreiben:** `gog sheets append <ID> "<range>" "<values>"`

### 4.3 ANGEBOTE_Liste (lesen + schreiben)
- **Sheet ID:** `1aF3bqQSK8twh5C2nspwlHqw65KRF0iBLeX2YnOkw3do`
- **Header:** `City | Address | Asset Name | Investor Developer | Opening | No. of Beds`
- **Umfang:** ~100 Zeilen (bestehende Projekte)
- **Beispiel:** `Aachen | Beverstraße 32A | LIF | Cube Real Estate GmbH | 2025 | 64`

---

## 5. WORKFLOW (SOLL-Zustand laut AGENTS.md)

```
START
  │
  ├─ Lies PROGRESS_TRACKER → letzte_nummer (aktuell: ~216)
  │
  ▼
┌─────────────────────────────── SCHLEIFE ───────────────────────────┐
│                                                                     │
│  Schritt 1: Lade EINEN Auftraggeber (#aktuelle_nummer)              │
│       ↓                                                             │
│  Schritt 2: web_search Suchabfrage 1 (Projektsuche)                │
│       ↓                                                             │
│  PROGRESS_TRACKER aktualisieren (Nummer, Suchbegriff, Ergebnis)     │
│       ↓                                                             │
│  Kein Treffer? → aktuelle_nummer + 1 → ZURÜCK zu Schritt 1         │
│       ↓                                                             │
│  Treffer? → Schritt 3: Duplikat-Check gegen ANGEBOTE_Liste          │
│       ↓                                                             │
│  Duplikat? → aktuelle_nummer + 1 → ZURÜCK zu Schritt 1             │
│       ↓                                                             │
│  NEU? → Suchabfrage 2 (Kontaktsuche) + Suchabfrage 3 (LinkedIn)    │
│       ↓                                                             │
│  Schritt 4: 15 Felder ausfüllen                                    │
│       ↓                                                             │
│  Kein Ansprechpartner? → Treffer ungültig → weiter                  │
│       ↓                                                             │
│  Gültiger Treffer → treffer_zaehler + 1                             │
│       ↓                                                             │
│  treffer_zaehler < 5? → aktuelle_nummer + 1 → ZURÜCK zu Schritt 1  │
│                                                                     │
└─────────────────── BIS treffer_zaehler == 5 ────────────────────────┘
  │
  ▼
Schritt 6: Report erstellen
  ├─ ANGEBOTE_Liste aktualisieren (neue Projekte eintragen)
  ├─ PROGRESS_TRACKER aktualisieren (letzte Nummer + Datum)
  ├─ Telegram-Nachricht senden
  ├─ E-Mail mit vollständigem Bericht senden
  └─ memory/YYYY-MM-DD.md schreiben
```

---

## 6. SCHNITTSTELLEN (I/O)

### 6.1 Input
| Quelle | Tool | Zweck |
|--------|------|-------|
| AUFTRAGGEBER_Liste | `gog sheets get` | Auftraggeber-Name + Stadt lesen |
| PROGRESS_TRACKER | `gog sheets get` | Letzte bearbeitete Nummer lesen |
| ANGEBOTE_Liste | `gog sheets get` | Duplikat-Check (bestehende Projekte) |
| Internet | `web_search` (Perplexity Sonar Pro) | Projekt-Recherche, Kontakt-Suche, LinkedIn |

### 6.2 Output
| Ziel | Tool | Zweck |
|------|------|-------|
| PROGRESS_TRACKER | `gog sheets append/update` | Fortschritt loggen |
| ANGEBOTE_Liste | `gog sheets append` | Neue Projekte eintragen |
| Telegram | Bot API (Token: `8415926959:...`, Chat: `7627639740`) | Kurzbericht |
| E-Mail | `gog gmail send` (an cyclus2000akan@gmail.com) | Vollständiger Bericht |
| memory/ | Datei schreiben | Tagesnotiz |

### 6.3 Suchabfragen (3 pro Treffer)
| # | Abfrage | Wann | Ziel |
|---|---------|------|------|
| 1 | `[Name] Studentenwohnheim OR Wohnungsprojekt 2026 2027 2028 DE AT` | IMMER (jeder Auftraggeber) | Projekt finden |
| 2 | `[Unternehmen] Ansprechpartner OR Geschäftsführer Kontakt Telefon` | Nur bei Treffer | Kontaktdaten |
| 3 | `[Unternehmen] site:linkedin.com` | Nur bei Treffer | LinkedIn-Profile |

---

## 7. 15 PFLICHTFELDER PRO PROJEKT

| # | Feld | Pflicht | Quelle |
|---|------|---------|--------|
| 1 | Projektname | PFLICHT | Suchabfrage 1 |
| 2 | Kurzbeschreibung + URL | PFLICHT + QUELLE | Suchabfrage 1 |
| 3 | Unternehmen + URL | PFLICHT | Suchabfrage 1 |
| 4 | Standort (Stadt, Land) | PFLICHT | Suchabfrage 1 |
| 5 | Typ (PBSA / Wohnungsprojekt) | PFLICHT | Suchabfrage 1 |
| 6 | Status (geplant/im Bau/fertig) | PFLICHT + QUELLE | Suchabfrage 1 |
| 7 | Architekt | SOLL | Suchabfrage 1/2 |
| 8 | Projektumfang (50+ Einheiten) | PFLICHT | Suchabfrage 1 |
| 9 | **Ansprechpartner (Name, Tel, E-Mail)** | **ABSOLUT PFLICHT** | Suchabfrage 2 |
| 10 | Direkte Links | PFLICHT + QUELLE | Suchabfrage 1 |
| 11 | Baubeginn | PFLICHT | Suchabfrage 1 |
| 12 | Fertigstellung | SOLL | Suchabfrage 1 |
| 13 | Verantwortliche/r | SOLL | Suchabfrage 2 |
| 14 | LinkedIn Ansprechpartner | PFLICHT | Suchabfrage 3 |
| 15 | LinkedIn Unternehmen | PFLICHT | Suchabfrage 3 |

**Validierung:** Min. 10/15 Felder + 4 mit Quellen + Ansprechpartner PFLICHT

---

## 8. KONFIGURATION (openclaw.json)

### Agent-Definition
```json
{
  "id": "foness",
  "name": "foness",
  "workspace": "/data/.openclaw/agents/foness/workspace",
  "model": { "primary": "minimax-portal/MiniMax-M2.5" }
}
```

### LLM-Modell
```json
"minimax-portal": {
  "baseUrl": "https://api.minimax.io/anthropic",
  "apiKey": "minimax-oauth",
  "api": "anthropic-messages",
  "models": [
    { "id": "MiniMax-M2.5", "reasoning": true, "contextWindow": 200000, "maxTokens": 8192 }
  ]
}
```

### Web-Search
```json
"tools": {
  "web": {
    "search": {
      "provider": "perplexity",
      "perplexity": { "apiKey": "pplx-XXXX_REDACTED_XXXX" }
    }
  }
}
```
- OpenClaw unterstützt intern: `perplexity/sonar` und `perplexity/sonar-pro`
- KEIN `sonar-reasoning-pro` verfügbar

### Telegram
```json
"telegram": {
  "enabled": true,
  "botToken": "8415926959:AAEOI6koO0uuevYs2REKgUkVkMP3xsspmzc",
  "dmPolicy": "allowlist",
  "allowFrom": ["7627639740"]
}
```

### Gateway
```json
"gateway": {
  "port": 18789, "bind": "lan",
  "auth": { "mode": "token", "token": "qzBZjAfAmERo6YBD0JMTM0VMLfgyL02O" }
}
```

---

## 9. BEKANNTE BUGS & PROBLEME

### Bug 1: Agent bricht nach ~10 Auftraggebern ab → springt zu Fallback
- **Symptom:** "2 Treffer nach 10 Auftraggebern → Fallback-Strategie"
- **Ursache:** AGENTS.md Zeile 45 enthält `} BIS treffer_zaehler == 5 ODER 80 Auftraggeber geprüft` — das LLM (MiniMax M2.5) interpretiert die Fallback-Strategie als attraktive Abkürzung und springt nach ~10 Versuchen dorthin
- **Root Cause:** Schritt 5 (Zeile 140-144) erwähnt Fallback zu prominent, das Modell sieht es als "effizienter" und optimiert seinen Weg dorthin
- **Fix nötig:** Fallback komplett aus dem Hauptworkflow entfernen, nur als allerletzten Abschnitt am Ende, mit explizitem Verbot vor 80 Auftraggebern

### Bug 2: Agent lädt 5 Auftraggeber gleichzeitig statt einzeln
- **Symptom:** "Nächste Auftraggeber #216–220"
- **Ursache:** AGENTS.md beschrieb nicht explizit genug "nur einer"
- **Status:** Teilweise gefixt (Zeile 52 enthält jetzt Warnung), aber Modell ignoriert es teilweise

### Bug 3: Fehlende Ansprechpartner-Daten (Felder 7, 9, 13, 14, 15)
- **Symptom:** Projekte ohne Kontaktdaten, ohne LinkedIn, ohne Architekt
- **Ursache:** Nur 1 Suchabfrage pro Auftraggeber statt 3. Suchabfragen 2+3 wurden nicht durchgeführt
- **Status:** AGENTS.md + TOOLS.md wurden mit 3 Suchformeln ergänzt, noch nicht verifiziert

### Bug 4: PROGRESS_TRACKER hat unstrukturiertes Format
- **Symptom:** Daten über 2-3 Zeilen pro Eintrag verteilt statt in einer Zeile
- **Ursache:** Agent schreibt mehrzeilig statt alle Felder in eine Zeile
- **Impact:** Erschwert das Auslesen der letzten Nummer

### Bug 5: MEMORY.md enthält nur Platzhalter
- **Symptom:** "Letzte bearbeitete Nummer: [wird nach Bootstrap ausgefüllt]"
- **Ursache:** Agent aktualisiert MEMORY.md nicht nach Läufen
- **Impact:** Gering, solange PROGRESS_TRACKER funktioniert

### Nicht eingerichtet: Cron-Job
- **Soll:** Jeden Montag 06:35 Uhr automatisch starten
- **Ist:** Muss noch in openclaw.json als `"cron"` Eintrag ergänzt werden

---

## 10. VERFÜGBARE LLM-MODELLE

| Provider | Modell | Alias | Kosten |
|----------|--------|-------|--------|
| minimax-portal | MiniMax-M2.5 | minimax-m2.5 | Kostenlos (OAuth) |
| minimax-portal | MiniMax-M2.1 | minimax-m2.1 | Kostenlos (OAuth) |
| nvidia-nim | Kimi K2 Instruct | Kimi K2 Instruct | Kostenlos |
| openai | GPT-5.2, 5.1-codex, 5, 5-mini, 4.1 | div. | API Key nötig |
| anthropic | Claude Opus 4.6, Sonnet 4.5, Haiku 4.5 | div. | API Key nötig |
| google | Gemini 3 Pro/Flash, 2.5 Flash/Lite | div. | API Key nötig |

**Aktuell aktiv:** MiniMax M2.5 (kostenlos, reasoning: true, 200k context)

---

## 11. NETZWERK & ZUGRIFF

- **Intern:** Docker Container lauscht auf Port 18789, bound to `lan`
- **Extern:** Cloudflare Tunnel → HTTPS → localhost:18789
- **Docker Port:** `127.0.0.1:18789:18789` (nur localhost)
- **Auth:** Token-basiert (`qzBZjAfAmERo6YBD0JMTM0VMLfgyL02O`)
- **Sandbox:** Docker-in-Docker, mode: non-main, network: bridge

---

## 12. STARTBEFEHL FÜR ECHTLAUF

Im OpenClaw-Dashboard an Foness senden:
```
Lies alle deine Workspace-Dateien (SOUL.md, USER.md, TOOLS.md, AGENTS.md, MEMORY.md) und führe den kompletten Wochenbericht-Workflow aus (AGENTS.md Schritt 1–6). Echtlauf — Google Sheets aktualisieren, Bericht per Telegram und E-Mail senden.
```

---

## 13. NOCH AUSSTEHENDE ARBEITEN

1. **Bug 1 fixen:** AGENTS.md — Fallback aus Hauptworkflow entfernen, Schleifenlogik verschärfen
2. **Cron-Job einrichten:** `openclaw.json` → `"cron"` Eintrag für Montag 06:35
3. **MEMORY.md automatisch aktualisieren:** Agent soll nach jedem Lauf Fortschritt eintragen
4. **PROGRESS_TRACKER Format standardisieren:** Alle Felder in einer Zeile
5. **Echtlauf verifizieren:** Prüfen ob Agent wirklich einzeln durchiteriert bis 5 Treffer

---

## 14. UPLOAD-PLAN: Google Drive openclaw/foness

### Ziel
Alle Workspace-Dateien + diese Dokumentation nach `gdrive:openclaw/foness` hochladen.

### Google Drive Ziel
- **Ordner:** `openclaw/foness`
- **Folder ID:** `1_J-oVpcUSBUZHApjEPUiCcdUGKTR0IWf`
- **Account:** `info@wappreport.com`

### Dateien zum Upload (9 Dateien)
| Datei | Pfad im Container |
|-------|--------------------|
| FONESS_DOKUMENTATION.md | (wird aus Plan-Datei kopiert) |
| AGENTS.md | /data/.openclaw/agents/foness/workspace/AGENTS.md |
| SOUL.md | /data/.openclaw/agents/foness/workspace/SOUL.md |
| TOOLS.md | /data/.openclaw/agents/foness/workspace/TOOLS.md |
| IDENTITY.md | /data/.openclaw/agents/foness/workspace/IDENTITY.md |
| USER.md | /data/.openclaw/agents/foness/workspace/USER.md |
| MEMORY.md | /data/.openclaw/agents/foness/workspace/MEMORY.md |
| HEARTBEAT.md | /data/.openclaw/agents/foness/workspace/HEARTBEAT.md |
| memory/2026-02-16.md | /data/.openclaw/agents/foness/workspace/memory/2026-02-16.md |

### Befehle
```bash
# 1. Dokumentation ins Workspace kopieren
cp /root/.claude/plans/glowing-baking-pumpkin.md /data/.openclaw/agents/foness/workspace/FONESS_DOKUMENTATION.md

# 2. Jede Datei einzeln hochladen mit gog drive upload
PARENT="1_J-oVpcUSBUZHApjEPUiCcdUGKTR0IWf"
ACCOUNT="info@wappreport.com"

for file in FONESS_DOKUMENTATION.md AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md MEMORY.md HEARTBEAT.md; do
  docker exec openclaw-rmys-openclaw-1 /home/linuxbrew/.linuxbrew/bin/gog drive upload \
    "/data/.openclaw/agents/foness/workspace/$file" \
    --parent "$PARENT" --account "$ACCOUNT" --no-input
done

# 3. Tagesnotiz
docker exec openclaw-rmys-openclaw-1 /home/linuxbrew/.linuxbrew/bin/gog drive upload \
  "/data/.openclaw/agents/foness/workspace/memory/2026-02-16.md" \
  --name "2026-02-16_tagesnotiz.md" --parent "$PARENT" --account "$ACCOUNT" --no-input
```

### Verifikation
```bash
docker exec openclaw-rmys-openclaw-1 /home/linuxbrew/.linuxbrew/bin/gog drive ls \
  --parent 1_J-oVpcUSBUZHApjEPUiCcdUGKTR0IWf --account info@wappreport.com --plain
```
