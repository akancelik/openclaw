---
name: supermemory
description: Store and retrieve memories using the SuperMemory API. Add content, search memories, and chat with your knowledge base.
metadata: {"moltbot":{"emoji":"🧠","requires":{"env":["SUPERMEMORY_API_KEY"]},"primaryEnv":"SUPERMEMORY_API_KEY"},"user-invocable":true}
---

# SuperMemory

Store, search, and chat with your personal knowledge base using SuperMemory's API.

## WICHTIG

- Der API-Key wird automatisch aus der Umgebungsvariable `SUPERMEMORY_API_KEY` gelesen.
- NIEMALS den API-Key hardcoden oder aus dieser Datei lesen.
- IMMER den `supermemory` CLI-Befehl verwenden (siehe unten).
- NIEMALS curl oder web_fetch für die SuperMemory API verwenden.

## Usage — NUR diese Befehle verwenden

### Add a Memory

```bash
supermemory add "Your memory content here"
supermemory add "Important project details" "description"
```

### Search Memories

```bash
supermemory search "search query"
```

### Chat with Memories

```bash
supermemory chat "What do you know about my projects?"
```

## Beispiele

- "Merke dir X" → `supermemory add "X" "kurze beschreibung"`
- "Was weisst du über Y?" → `supermemory search "Y"`
- "Fasse zusammen was du über Z weisst" → `supermemory chat "Was weiss ich über Z?"`
