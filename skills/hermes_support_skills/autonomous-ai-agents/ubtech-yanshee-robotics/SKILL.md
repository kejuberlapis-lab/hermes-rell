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
4. **Tailscale VPN:** Install standalone ARM 32-bit binary (`tailscale_latest_arm.tgz`) for persistent remote access from VPS cloud without port forwarding.

### SSH Access
- **Default User:** `pi`
- **Default Password:** `raspberry` (most firmware versions) or `yanapi` / `ubtech`
- **Initial Hardening:** Run `passwd` immediately after first login.

---

## 2. Audio Hardware & ALSA Configuration

Yanshee uses a **Microsemi DAC zl380xx** DSP chip with a built-in microphone array (`card 0, device 0: Microsemi DAC zl380xx-dai-0`).

### ⚠️ Critical Audio Capture & Mixer Pitfalls

1. **Hardware Mute Switch (`MIC SOUT MUTE`):**
   On boot, ALSA mixer `MIC SOUT MUTE` is often set to `values=on` (which means Muted!), causing `arecord` to capture digital 0 silence.
   **Rule:** Always unmute and set max gain before running voice loops:
   ```bash
   amixer -c 0 cset numid=2 off  # Unmute MIC SOUT MUTE
   amixer -c 0 cset numid=3 15   # Max capture gain (0-15)
   amixer -c 0 sset DAC 14       # Default speaker volume (70%)
   ```

2. **Stereo Requirement:**
   Direct mono recording (`-c 1`) or hardware-direct device (`hw:0,0`) fails with `arecord: set_params: Channels count non available`.
   **Rule:** Always use the ALSA plugin layer `plughw:0,0` with **2 channels (stereo, 48000 Hz or 16000 Hz)**:
   ```bash
   arecord -D plughw:0,0 -f S16_LE -r 48000 -c 2 -d 3 /tmp/test_mic.wav && aplay -D plughw:0,0 /tmp/test_mic.wav
   ```

3. **Mandatory `flac` Dependency:**
   `speech_recognition` (`r.recognize_google`) fails silently with `OSError: FLAC conversion utility not available` on Raspbian unless installed:
   ```bash
   sudo apt-get install -y flac
   ```

4. **ALSA Full-Duplex Clash & `mpg123` Segfault:**
   - Raw `plughw:0,0` cannot open `arecord` and `mpg123` concurrently (causes `Slave PCM not usable: Broken configuration`).
   - Do NOT pass `-f <scale>` (e.g. `-f 18000`) to `mpg123` on ARMv7 32-bit; it causes integer overflow segmentation faults. Use `amixer -c 0 sset DAC <0-20>` for volume scaling instead.

---

## 3. Hardware Controls: Voice Volume & Chest Button

### Hardware Volume Control
Map voice intents ("kecilkan volume", "besarkan volume") directly to ALSA DAC steps:
- Decrease: `amixer -c 0 sset DAC 4-`
- Increase: `amixer -c 0 sset DAC 4+`

### Push-to-Talk / Stop via Chest Button
Subscribe to the native ROS topic `/hal_button_info` using a Python 2 bridge daemon (`hermes-button.service`) to flag button presses without invoking ALSA audio devices.

---

## 4. Two-Way AI Voice Conversation Pipeline

To achieve seamless multi-turn conversation:
1. **Audio Chime Cue:** Play `/opt/yanshee/lib/voice/audio/tips/ding.wav` via `aplay -D plughw:0,0` to signal to the user that the mic is listening.
2. **Capture:** Record audio using `arecord -D plughw:0,0 -f S16_LE -r 48000 -c 2 -d 4`.
3. **STT:** Transcribe via `speech_recognition` in `id-ID`.
4. **Brain (LLM):** Send prompt to 9Router VPS endpoint (`http://100.114.89.30:20128/v1/chat/completions`) with a concise system prompt and comma-spaced pauses for natural TTS pacing.
5. **Speak:** Output AI answer via `YanAPI.sync_do_tts(reply)`.
6. **Multi-Turn Loop:** Keep listening for follow-up questions for 3 cycles before returning to standby.
