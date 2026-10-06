---
name: humanoid-robot-voice-integration
description: Use when integrating AI voice on humanoid robots or RasPi.
---

# Humanoid Robot Voice & AI Agent Integration

This skill outlines the standard architecture and implementation patterns for cloning and deploying Hermes AI Agent into humanoid robots and embedded Linux devices (such as UBTECH Yanshee / Raspberry Pi ARMv7/ARM64).

## Architecture: Hybrid Cloud-Edge Pattern

Embedded humanoid robots have limited onboard compute (e.g., Raspberry Pi 3/4 32-bit/64-bit). The recommended architecture separates edge hardware I/O from heavy LLM reasoning:

1. **Edge Client (Robot Body):**
   - Audio Capture via hardware microphone array & ALSA.
   - Wake Word & Voice Activity Detection.
   - Speech-to-Text (STT) via Google Speech / Whisper.
   - Text-to-Speech (TTS) via onboard robot SDK (e.g., `YanAPI.sync_do_tts`).
   - Hardware actuators: servo motion, music playback (`mpg123`), LED status.
2. **Private Cloud / Gateway (Hermes Brain):**
   - LLM Router (9Router / Hermes VPS) serving fast reasoning models (e.g. `ag/gemini-3.7-flash-high` / `ag/gemini-3.8-flash-low`).
   - Private mesh VPN connection (Tailscale) linking Edge and Cloud securely without opening public inbound ports.

---

## Step-by-Step Deployment Procedure

### 1. Private Mesh Networking (Tailscale)
Connect the robot to the agent's VPS network:
- For legacy 32-bit ARM Linux (e.g. Raspbian Stretch), standard apt repository scripts may fail. Use standalone ARM static binaries: `https://pkgs.tailscale.com/stable/tailscale_latest_arm.tgz`.
- Ensure daemon state directories exist: `/var/lib/tailscale` and `/var/run/tailscale`.
- Run daemon: `tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/var/run/tailscale/tailscaled.sock`.
- Authorize SSH key exchange (`~/.ssh/authorized_keys`) from VPS to robot for automated management.

### 2. Hardware Audio & DSP Unlocking
Humanoid robots with onboard DSP chips (e.g., Microsemi ZL380xx) often have ALSA hardware mixer quirks:
- **Unmute Capture:** In ALSA controls, `MUTE=on` means muted. Set `amixer -c 0 cset numid=2 off` to unmute the microphone.
- **Microphone Gain:** Maximize capture sensitivity: `amixer -c 0 cset numid=3 15`.
- **Clock & Channel Matching:** If DSP hardware clock is 48000 Hz stereo, recording at 16000 Hz directly may produce 3x accelerated playback. Always record at native DSP rate (`arecord -D plughw:0,0 -f S16_LE -r 48000 -c 2`).
- **Missing Encoder Dependency:** `SpeechRecognition` requires the CLI utility `flac` to encode audio payloads. Always ensure `sudo apt-get install -y flac` is installed.

### 3. Conversational Multi-Turn UX & Audio Chime
To prevent speech clipping and awkward interaction delays:
- **Audio Chime Cue:** Play a crisp cue sound (e.g., `/opt/yanshee/lib/voice/audio/tips/ding.wav` via `aplay -D default -q ding.wav`) immediately before the microphone opens so the user knows exactly when to start speaking.
- **Echo Prevention Delay:** Insert `time.sleep(0.4)` after TTS completes so the microphone does not record the robot's own speaker echo.
- **Multi-Turn Continuation:** When wake word triggers, open a multi-turn conversation session. Do NOT return to standby after a single answer; allow the user to ask follow-up questions directly until a silence timeout (e.g., 2-3 cycles / ~10-15s) or exit phrase ("cukup", "selesai") is reached.

### 4. Hardware Command Execution & Multimedia
Allow the robot to execute physical hardware commands alongside conversation:
- **Music Playback:** Route song queries to local background players (`mpg123 -a default /path/to/song.mp3 &`) and support instant voice stops (`killall mpg123`).
- **Systemd Service:** Keep the agent alive as a persistent background daemon:
  ```ini
  [Unit]
  Description=Humanoid AI Agent Voice Service
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
