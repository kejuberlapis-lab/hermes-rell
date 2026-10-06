---
name: humanoid-robotics-yanshee
description: >-
  Use when integrating AI agents on UBTECH Yanshee robot.
category: autonomous-ai-agents
triggers:
  - integrate AI or LLM with UBTECH Yanshee robot
  - setup voice STT / TTS on Yanshee Raspberry Pi
  - debug YanAPI hardware, mic array audio, or motion errors
  - 2-way voice conversation loop on Yanshee
  - connect Yanshee to VPS via Tailscale
---

# UBTECH Yanshee Humanoid Robotics & AI Integration

Complete engineering reference for deploying and running autonomous AI agents (Hermes, custom LLMs, 9Router) inside the UBTECH Yanshee humanoid robot (Raspberry Pi 3, Debian 9 Stretch ARMv7l).

---

## 1. Network Discovery & SSH Access

### IP Discovery
- **Chest Button Broadcast:** Press chest button 1–2 times when booted; Yanshee announces its assigned IP address via speaker.
- **mDNS Hostname:** `ping yanshee.local` or `ping raspberrypi.local`.
- **Yanshee Mobile App:** Check device info in Wi-Fi settings.

### SSH Access & Hardening
- **Default User:** `pi`
- **Default Password:** `raspberry` (or `yanapi` on some revisions).
- **Hardening:** Run `passwd` immediately after login.
- **SSH Key Auth:** Append host public key to `~/.ssh/authorized_keys` with `chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys`.

---

## 2. Remote VPS Mesh Networking (Tailscale on Legacy ARMv7)

Yanshee runs Debian 9 (Stretch) on 32-bit ARMv7 (`armv7l`), where the standard automated installer fails with `VERSION_CODENAME: parameter not set`.

### Installation Procedure
```bash
cd /tmp
wget https://pkgs.tailscale.com/stable/tailscale_latest_arm.tgz
tar -xzf tailscale_latest_arm.tgz
cd tailscale_*_arm
sudo cp tailscale /usr/bin/
sudo cp tailscaled /usr/sbin/
sudo mkdir -p /var/lib/tailscale /var/run/tailscale /etc/default

# Start daemon with explicit socket and state paths
sudo /usr/sbin/tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/var/run/tailscale/tailscaled.sock > /tmp/tailscaled.log 2>&1 &
sleep 2
sudo tailscale --socket=/var/run/tailscale/tailscaled.sock up
```
Check virtual IP with `tailscale --socket=/var/run/tailscale/tailscaled.sock ip -4`.

---

## 3. Audio Hardware & ALSA Configuration

Yanshee uses a **Microsemi DAC zl380xx** DSP chip with a built-in microphone array (`card 0, device 0: Microsemi DAC zl380xx-dai-0`).

### ⚠️ Critical Audio Capture Pitfall
Direct mono recording (`-c 1`) or hardware-direct device (`hw:0,0`) fails with:
`arecord: set_params: Channels count non available`

**Rule:** Always use the ALSA plugin layer `plughw:0,0` with **2 channels (stereo)** and 16000 Hz:

```bash
# Validated recording test (3 seconds stereo, 16kHz)
arecord -D plughw:0,0 -f S16_LE -r 16000 -c 2 -d 3 /tmp/test_mic.wav && aplay -D plughw:0,0 /tmp/test_mic.wav
```

---

## 4. Python Environment Quirks on Yanshee

1. **Python 3.5.3 (No f-strings):**
   - Debian Stretch uses Python 3.5.3 where `f"..."` causes `SyntaxError: invalid syntax`.
   - **Rule:** Always use `"{}".format(...)` or string concatenation (`+`).
2. **Pip SSL / TLS Certificate Issues:**
   - Pip may throw SSL handshake errors against `piwheels.org`.
   - **Workaround:** Download `.whl` files on the host/VPS (`pip download SpeechRecognition -d /tmp/wheels/`), SCP to Yanshee, and install locally via `python3 -m pip install /tmp/<file>.whl`.

---

## 5. YanAPI SDK & Two-Way Voice Pipeline

```python
import YanAPI

# Mandatory initialization before any hardware calls
YanAPI.yan_api_init("127.0.0.1")

# Text-to-Speech (TTS)
YanAPI.sync_do_tts("Halo sir, saya robot Yanshee.")
```

### Two-Way AI Voice Conversation Pipeline
1. **Wake Word Detection:** Continuously record short 2.5s audio chunks and check for wake words (`"halo hermes"`, `"halo yanshee"`).
2. **Prompt Acknowledgment:** Speak a quick confirmation (`"Ya sir?"`).
3. **Capture Query:** Record user query for 4.5s.
4. **Brain (LLM Request):** Send transcribed text to OpenAI-compatible endpoint (e.g. 9Router VPS via Tailscale).
   - **Critical:** 9Router streams SSE chunks by default; explicitly pass `"stream": False` in payload for complete synchronous JSON response.
   - Enforce concise system prompt (1–2 sentences) so spoken responses remain natural.
5. **Speak:** Output AI answer via `YanAPI.sync_do_tts(reply)`.
