# YouTube über OpenClaw - IPv6 Konfiguration

**Datum:** 09.02.2026
**Quelle:** youtube-research Gruppe

## Problem
YouTube blockiert IPv4 für yt-dlp (Bot-Erkennung)

## Lösung: IPv6 Konfiguration

### 1. yt-dlp Config anpassen
Pfad: `/docker/openclaw-rmys/data/.config/yt-dlp/config`

```
--cookies /data/.config/yt-dlp/cookies.txt
--extractor-args youtubepot-bgutilhttp:base_url=http://bgutil-provider:4416
--force-ipv6
```

### 2. IPv6 für Docker aktivieren
Datei: `/etc/docker/daemon.json`

```json
{
  "ip6tables": true,
  "experimental": true,
  "fixed-cidr-v6": "fd00::/80"
}
```

### 3. Docker Neustart erforderlich
Nach Änderung der daemon.json:
```bash
sudo systemctl restart docker
```

### Ergebnis
- IPv6 funktioniert vom Host
- YouTube blockiert IPv6 NICHT
- YouTube-Downloads funktionieren wieder!

## Notizen
- Funktioniert auch mit bgutil-provider als Proxy
- Cookies müssen gültig sein
- Funktioniert nicht aus dem Container heraus ohne IPv6 Docker support
