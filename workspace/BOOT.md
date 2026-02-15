---
summary: "Agent boot instructions"
---

# Voice Reply Rule

When the user says or writes "antworte per Voice" (or similar like "antwort per voice", "voice antwort", "per voice antworten"), respond with your reply wrapped in the correct TTS tags so a voice message is generated automatically.

The correct tag format is: [[tts:text]]spoken text here[[/tts:text]]

Example:
User: "Wie wird das Wetter morgen? antworte per Voice"
You: [[tts:text]]Das Wetter morgen wird sonnig mit Temperaturen um die 15 Grad.[[/tts:text]]

Important:
- Use EXACTLY [[tts:text]] to open and [[/tts:text]] to close — no other format
- Do NOT use [[tts]] without the colon — that does not work
- The text between the tags will be spoken as a voice message
- Do NOT include emojis or markdown inside the tts:text tags — only plain spoken text
- Respond in the same language as the user (usually German)
- Keep voice replies concise and natural-sounding (under 1500 characters)
- You can optionally include visible text OUTSIDE the tags too
