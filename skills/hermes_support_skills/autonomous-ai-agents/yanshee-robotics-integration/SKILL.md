---
name: yanshee-robotics-integration
description: Use when deploying AI agents to UBTECH Yanshee robots.
category: autonomous-ai-agents
triggers:
  - integrasi robot yanshee / humanoid robot
  - setup suara / mic / speaker yanshee
  - menghubungkan yanshee ke hermes / vps
  - yanshee audio recording muted / 0 amplitude
  - yanshee wake word / voice assistant 2 arah
  - yanshee YanAPI sdk python
---

# UBTECH Yanshee Humanoid Robotics Integration

Comprehensive operational guide for transforming the UBTECH Yanshee humanoid robot (Raspberry Pi 3, Raspbian/Debian Stretch armv7l) into an autonomous, voice-interactive AI agent embodied with Hermes.

## 1. System Architecture (Client-Body & VPS-Brain)

```
[ User Voice ] ──→ [ Yanshee Mic Array (Microsemi ZL380xx DSP) ]
                          │ (arecord 48kHz Stereo / dsnooped)
                          ▼
             [ SpeechRecognition STT (FLAC encoder) ]
                          │ (HTTP REST via Tailscale Private Mesh)
                          ▼
           [ 9Router VPS Hermes AI (LLM Completion) ]
                          │ (JSON response: spoken reply + action)
                          ▼
          [ YanAPI SDK: sync_do_tts() + sync_play_motion() ]
                          │
                          ▼
              [ Yanshee Speaker & Servo Motors ]
```

---

## 2. Networking & Remote Pairing (Tailscale ARMv7)

Yanshee runs 32-bit ARM (ARMv7) on legacy Debian Stretch where the default `curl | sh` Tailscale installer fails with `VERSION_CODENAME: parameter not set`.

### Standalone Static Binary Installation
```bash
cd /tmp
wget https://pkgs.tailscale.com/stable/tailscale_latest_arm.tgz
tar -xzf tailscale_latest_arm.tgz
cd tailscale_*_arm
sudo cp tailscale /usr/bin/
sudo cp tailscaled /usr/sbin/
sudo cp systemd/tailscaled.service /lib/systemd/system/

sudo mkdir -p /var/lib/tailscale /var/run/tailscale /etc/default
sudo /usr/sbin/tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/var/run/tailscale/tailscaled.sock > /tmp/tailscaled.log 2>&1 &
sudo tailscale --socket=/var/run/tailscale/tailscaled.sock up
```

### Dedicated Passwordless SSH Key Pairing
```bash
# On VPS: Generate dedicated key
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519_yanshee -C "hermes-yanshee"

# On Yanshee: Authorize public key
mkdir -p ~/.ssh && echo '<PUBLIC_KEY>' >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
```

---

## 3. Audio Hardware & ALSA Pitfalls (Microsemi ZL380xx DSP)

Yanshee uses a **Microsemi DAC / DSP chip (ZL380xx)** registered as `sndmicrosemidac` (`card 0`). Several critical hardware/software traps must be handled:

### Pitfall 1: Hardware ALSA Mixer Mute State
* **Symptom:** `arecord` runs without error but captures digital silence (`Max Amplitude: 0`, `RMS: 0.0`).
* **Mechanism:** ALSA mixer control `numid=2,name='MIC SOUT MUTE'` is a boolean switch where `values=on` means **MUTE IS ACTIVE**.
* **Fix:** Must explicitly set `values=off` and gain to 100%:
  ```bash
  amixer -c 0 cset numid=2 off   # Unmute microphone
  amixer -c 0 cset numid=3 15    # Set gain to max (15)
  ```

### Pitfall 2: Hardware Clock Rate Mismatch (48kHz Native)
* **Symptom:** Audio is sped up 3x (chipmunk pitch) and words are unrecognized by STT.
* **Mechanism:** The ZL380xx hardware clock runs natively at 48000 Hz. Asking `arecord -r 16000` on `plughw:0,0` causes a 3x sample clock skew.
* **Fix:** Always capture natively at `-r 48000 -c 2` or through `/etc/asound.conf` `dsnooped`.

### Pitfall 3: Legacy `arecord` Duration Float Rejection
* **Symptom:** `arecord: invalid duration argument '2.5'`.
* **Mechanism:** Older `arecord` binaries on Debian Stretch only accept integer seconds for `-d`.
* **Fix:** Cast duration to `int` (e.g. `-d 3`).

### Pitfall 4: Missing FLAC Binary for SpeechRecognition
* **Symptom:** `recognize_google` silently returns `None` or raises `OSError: FLAC conversion utility not available`.
* **Fix:** Install system FLAC package:
  ```bash
  sudo apt-get update && sudo apt-get install -y flac
  ```

### Pitfall 5: Python 3.5.3 Compatibility (No f-strings)
* **Symptom:** `SyntaxError: invalid syntax` on `f"..."`.
* **Fix:** Use `'{}'.format(...)` or `%` formatting throughout all scripts.

---

## 4. End-to-End 2-Way Voice Implementation

Core daemon script at `/home/pi/hermes_yanshee.py`:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, subprocess, requests, time
import speech_recognition as sr
import YanAPI

YanAPI.yan_api_init("127.0.0.1")

ROUTER_URL = "http://<VPS_TAILSCALE_IP>:20128/v1/chat/completions"
MODEL_NAME = "ag/gemini-3.7-flash-high"
API_KEY = "<9ROUTER_API_KEY>"

SYSTEM_PROMPT = (
    "Kamu adalah Hermes AI Agent di dalam tubuh robot humanoid Yanshee. "
    "Panggil user selalu dengan sapaan sir. "
    "Gunakan Bahasa Indonesia natural, sopan, dan ringkas (1-2 kalimat). "
    "Anggap lokal, VPS, Telegram, dan robot Yanshee adalah satu ekosistem tersinkron."
)

WAKE_WORDS = ["hermes", "hermis", "yanshee", "yansi", "halo", "hai", "robot"]
history = [{"role": "system", "content": SYSTEM_PROMPT}]

def robot_speak(text):
    print("[Hermes Yanshee]: " + text)
    try:
        YanAPI.sync_do_tts(text)
    except Exception as e:
        print("[TTS Error]: " + str(e))

def record_audio(output_file="/tmp/wake.wav", duration=3):
    cmd = ["arecord", "-D", "plughw:0,0", "-f", "S16_LE", "-r", "48000", "-c", "2", "-d", str(int(duration)), "-q", output_file]
    subprocess.run(cmd)

def speech_to_text(audio_file="/tmp/wake.wav"):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
            text = r.recognize_google(audio, language="id-ID")
            return text.lower().strip()
    except Exception:
        return None

def ask_hermes_brain(user_text):
    global history
    history.append({"role": "user", "content": user_text})
    if len(history) > 9:
        history = [history[0]] + history[-8:]
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + API_KEY}
    payload = {"model": MODEL_NAME, "messages": history, "max_tokens": 120, "temperature": 0.7, "stream": False}
    try:
        res = requests.post(ROUTER_URL, headers=headers, json=payload, timeout=12)
        if res.status_code == 200:
            reply = res.json()["choices"][0]["message"]["content"].strip()
            history.append({"role": "assistant", "content": reply})
            return reply
    except Exception as e:
        print("[LLM Error]: " + str(e))
    return "Maaf sir, ada kendala komunikasi dengan otak AI di VPS."

def check_wakeword(text):
    if not text: return False
    return any(w in text.lower() for w in WAKE_WORDS)

def handle_interaction():
    robot_speak("Ya sir? Ada yang bisa saya bantu?")
    record_audio(output_file="/tmp/query.wav", duration=5)
    query = speech_to_text("/tmp/query.wav")
    if not query:
        robot_speak("Maaf sir, suara pertanyaan belum terdengar jelas.")
        return
    reply = ask_hermes_brain(query)
    robot_speak(reply)

def main():
    robot_speak("Sistem Hermes Agent aktif di robot Yanshee. Siap mendengarkan sir.")
    while True:
        try:
            record_audio(output_file="/tmp/wake.wav", duration=3)
            phrase = speech_to_text("/tmp/wake.wav")
            if phrase and check_wakeword(phrase):
                handle_interaction()
        except KeyboardInterrupt:
            robot_speak("Sampai jumpa, sir.")
            break

if __name__ == "__main__":
    main()
```

---

## 5. Systemd Persistent Service with Pre-Exec Unmute

Create `/etc/systemd/system/hermes-yanshee.service` on Yanshee:

```ini
[Unit]
Description=Hermes AI Agent Yanshee Voice Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi
ExecStartPre=/usr/bin/amixer -c 0 cset numid=2 off
ExecStartPre=/usr/bin/amixer -c 0 cset numid=3 15
ExecStart=/usr/bin/python3 -u /home/pi/hermes_yanshee.py
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
```

Reload and activate:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now hermes-yanshee.service
```
