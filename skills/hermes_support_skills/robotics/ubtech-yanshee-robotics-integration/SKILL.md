---
name: ubtech-yanshee-robotics-integration
description: Use when integrating UBTECH Yanshee robot with Hermes AI.
category: robotics
triggers:
  - integrasi robot yanshee dengan Hermes
  - setup yanshee voice wakeword
  - troubleshooting audio mic array yanshee
  - install tailscale di yanshee raspberry pi armv7l
  - kontrol servo dan YanAPI yanshee
---

# UBTECH Yanshee Robotics Integration with Hermes

Integration guide for connecting UBTECH Yanshee humanoid robots (Raspberry Pi 3, ARMv7l 32-bit) with Hermes AI Agent and LLM inference endpoints.

## 1. Hardware Architecture & System Defaults

- **Compute Board:** Raspberry Pi 3 Model B (Debian/Raspbian armv7l, Linux 4.14 kernel).
- **Default SSH Credentials:** Username: `pi`, Default Password: `raspberry`.
- **IP Discovery:**
  - Double-click the Chest Button to broadcast the IP address via the internal speaker.
  - Check connected devices in the mobile Yanshee App under Robot Info.
  - Discover via mDNS: `ping yanshee.local`.
- **Core SDK:** `YanAPI` Python module (`YanAPI.yan_api_init('127.0.0.1')`).

---

## 2. Networking: Tailscale on Legacy Raspbian (ARMv7l)

The standard automated installer (`curl | sh`) fails on Yanshee's custom Raspbian image with `VERSION_CODENAME: parameter not set`. Use the standalone static ARM binary:

```bash
cd /tmp
wget https://pkgs.tailscale.com/stable/tailscale_latest_arm.tgz
tar -xzf tailscale_latest_arm.tgz
cd tailscale_*_arm
sudo cp tailscale /usr/bin/
sudo cp tailscaled /usr/sbin/
sudo mkdir -p /var/lib/tailscale /var/run/tailscale /etc/default

# Launch daemon in background with explicit state/socket paths
sudo /usr/sbin/tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/var/run/tailscale/tailscaled.sock > /tmp/tailscaled.log 2>&1 &
sleep 2

# Authenticate
sudo tailscale --socket=/var/run/tailscale/tailscaled.sock up
```

---

## 3. Audio & Microphone Array Configuration

- **Hardware:** Microsemi DAC / DSP chip (`sndmicrosemidac`, `zl380xx-dai-0` on `card 0, device 0`).
- **ALSA Recording Pitfall:** The Microsemi DSP capture interface strictly requires **2 channels (Stereo `-c 2`)** and the `plughw` converter. Mono recording (`-c 1`) fails with `Channels count non available`.

### Validated Audio Capture & Playback Commands

```bash
# Record 3 seconds test audio (Stereo 16kHz)
arecord -D plughw:0,0 -f S16_LE -r 16000 -c 2 -d 3 /tmp/test_mic.wav

# Playback test audio through Yanshee internal speaker
aplay -D plughw:0,0 /tmp/test_mic.wav
```

---

## 4. Two-Way Voice & Wake Word Pipeline

Integrate continuous wake word detection, speech-to-text, LLM inference via 9Router proxy, and speech response:

```python
#!/usr/bin/env python3
import subprocess
import requests
import speech_recognition as sr
import YanAPI

# 1. Initialize YanAPI
YanAPI.yan_api_init("127.0.0.1")

# 2. Audio Capture
def record_audio(output_file="/tmp/yanshee_input.wav", duration=3):
    cmd = [
        "arecord", "-D", "plughw:0,0", "-f", "S16_LE",
        "-r", "16000", "-c", "2", "-d", str(duration), "-q", output_file
    ]
    subprocess.run(cmd)

# 3. Speech-to-Text
def speech_to_text(audio_file="/tmp/yanshee_input.wav"):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            data = r.record(source)
            return r.recognize_google(data, language="id-ID").lower().strip()
    except Exception:
        return None

# 4. LLM Completion via 9Router / OpenAI Endpoint
def ask_hermes(prompt, history, router_url, model_name, api_key):
    history.append({"role": "user", "content": prompt})
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    payload = {
        "model": model_name,
        "messages": history,
        "max_tokens": 120,
        "temperature": 0.7
    }
    res = requests.post(router_url, headers=headers, json=payload, timeout=10)
    if res.status_code == 200:
        reply = res.json()["choices"][0]["message"]["content"].strip()
        history.append({"role": "assistant", "content": reply})
        return reply
    return "Maaf sir, terjadi kendala komunikasi ke server."

# 5. Robot Speech Output
def robot_speak(text):
    YanAPI.sync_do_tts(text)
```

---

## 5. Pitfalls & Operational Rules

1. **Keep Responses Concise for TTS:** LLM system prompt must enforce 1-2 short sentences so the robot does not speak lengthy paragraphs that block subsequent wake word detection.
2. **Servo Safe Positions:** When testing movement with `YanAPI.sync_play_motion(name=...)`, ensure the robot is either seated or stabilized on a level surface to prevent falling.
3. **Password Security:** Always prompt the user to change the default `raspberry` password immediately after initial SSH access via `passwd`.
