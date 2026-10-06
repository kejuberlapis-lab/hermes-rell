---
name: ubtech-yanshee-robotics
description: >-
  Use when integrating AI models or YanAPI SDK on Yanshee.
category: autonomous-ai-agents
triggers:
  - integrate AI or LLM with UBTECH Yanshee robot
  - setup voice STT / TTS on Yanshee Raspberry Pi
  - debug YanAPI hardware, mic array audio, or motion errors
  - 2-way voice conversation loop on Yanshee
---

# UBTECH Yanshee Robotics & AI Integration

Guidelines, hardware configurations, and proven workflows for integrating AI agents (Hermes, LLM endpoints, 9Router) into the UBTECH Yanshee humanoid robot running Raspberry Pi (Debian/Raspbian).

---

## 1. Network Discovery & SSH Setup

### IP Discovery
1. **Chest Button Voice Broadcast:** Press the chest button 1–2 times when booted; Yanshee announces its IP address via speaker.
2. **Yanshee Mobile App:** Check robot info under network settings.
3. **mDNS Hostname:** `ping yanshee.local` or `ping raspberrypi.local` from the same LAN.

### SSH Access
- **Default User:** `pi`
- **Default Password:** `raspberry` (most firmware versions) or `yanapi` / `ubtech`
- **Initial Hardening:** Run `passwd` immediately after first login.

---

## 2. Audio Hardware & ALSA Configuration

Yanshee uses a **Microsemi DAC zl380xx** DSP chip with a built-in microphone array (`card 0, device 0: Microsemi DAC zl380xx-dai-0`).

### ⚠️ Critical Audio Capture Pitfall
Direct mono recording (`-c 1`) or hardware-direct device (`hw:0,0`) fails with:
`arecord: set_params: Channels count non available`

**Rule:** Always use the ALSA plugin layer `plughw:0,0` with **2 channels (stereo)**:

```bash
# Validated recording test (3 seconds stereo, 16kHz)
arecord -D plughw:0,0 -f S16_LE -r 16000 -c 2 -d 3 /tmp/test_mic.wav && aplay -D plughw:0,0 /tmp/test_mic.wav
```

---

## 3. YanAPI SDK Fundamentals

Yanshee provides `YanAPI` in Python 3 on the Raspberry Pi.

```python
import YanAPI

# Mandatory initialization before any hardware calls
YanAPI.yan_api_init("127.0.0.1")

# Text-to-Speech (TTS)
YanAPI.sync_do_tts("Halo sir, saya robot Yanshee.")

# Motion execution (ensure robot is standing safely)
# Available directions/names: 'wave', 'bow', 'walk', etc.
# Note: Error 106 indicates invalid direction parameter for the given motion action.
```

---

## 4. Two-Way AI Voice Conversation Pipeline

To achieve low-latency two-way voice interaction:
1. **Capture:** Record audio from mic array using `arecord` (`-D plughw:0,0 -c 2 -r 16000`).
2. **STT:** Transcribe via `speech_recognition` (`r.recognize_google(audio, language="id-ID")`) or remote Whisper API.
3. **Brain (LLM):** Send transcribed text to OpenAI-compatible endpoint (e.g. 9Router VPS or Groq).
   - Enforce concise system prompt (1–2 sentences) so spoken responses remain natural and quick.
4. **Speak:** Output AI answer via `YanAPI.sync_do_tts(reply)`.

---

## 5. Standard Bridge Template

```python
import subprocess
import requests
import speech_recognition as sr
import YanAPI

YanAPI.yan_api_init("127.0.0.1")

def record_audio(output_file="/tmp/input.wav", duration=4):
    cmd = ["arecord", "-D", "plughw:0,0", "-f", "S16_LE", "-r", "16000", "-c", "2", "-d", str(duration), "-q", output_file]
    subprocess.run(cmd)

def speech_to_text(audio_file="/tmp/input.wav"):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            return r.recognize_google(r.record(source), language="id-ID")
    except Exception:
        return None
```
