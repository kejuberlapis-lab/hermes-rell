---
name: embedded-robotics-ai-agent-integration
description: Use when deploying AI agents on humanoid robots or edge IoT.
---

# Embedded Robotics & Humanoid AI Agent Integration

Standard operating playbook for embedding autonomous AI Agents (Hermes) into Linux-based edge robotics (such as UBTECH Yanshee humanoid robot, Raspberry Pi ARMv7/aarch64, ROS platforms) for real-time bidirectional voice conversation and hardware control.

---

## 1. System Architecture: Hybrid Cloud-Edge Topology

When running LLMs on compute-constrained edge hardware (e.g. Raspberry Pi 3/4 32-bit):
1. **Edge Client (Robot Body):** Handles microphone capture, audio preprocessing, TTS speech playback (`YanAPI.sync_do_tts`), servo movement, and hardware button triggers.
2. **Brain Node (VPS / Router):** Runs LLM routing (9Router / Hermes Gateway) with low-latency models (`ag/gemini-3.7-flash-high` or ultra-fast flash tiers).
3. **Private Mesh Network (Tailscale):** Connects edge robots on local Wi-Fi / NAT directly to VPS cloud over encrypted WireGuard tunnel without public IP or port-forwarding requirements.

---

## 2. Hardware Audio & ALSA Traps on Embedded DSPs

### A. ALSA Mixer Mute Switches
* **Trap:** Edge audio DSP codecs (e.g. Microsemi ZL380xx) frequently initialize with hardware mute switches ON by default (`MIC SOUT MUTE: values=on`), resulting in flat zero amplitude (complete digital silence) during raw `arecord`.
* **Rule:** Explicitly unmute and calibrate gain via `amixer` before capturing:
  ```bash
  amixer -c 0 cset numid=2 off  # Unmute MIC SOUT MUTE
  amixer -c 0 cset numid=3 15   # Maximize capture gain (0-15)
  ```

### B. Hardware Clock Frequency Alignment
* **Trap:** Requesting a 16000 Hz sample rate directly on hardware codecs locked to 48000 Hz causes 3x playback/record speed distortion ("chipmunk effect"), destroying speech recognition.
* **Rule:** Record at native hardware rate and channels:
  ```bash
  arecord -D plughw:0,0 -f S16_LE -r 48000 -c 2 -d 3 /tmp/capture.wav
  ```

### C. Missing Audio Compression Utilities
* **Trap:** Python `SpeechRecognition` (`recognize_google`) fails silently with `OSError: FLAC conversion utility not available` if `flac` is not installed on minimal Linux distros.
* **Rule:** Always verify and install `flac` during edge bootstrap:
  ```bash
  sudo apt-get install -y flac mpg123
  ```

---

## 3. Bidirectional Voice Timing & Anti-Clipping Protocol

### A. Audio Chime Cue ("Ding!" Sound)
* Always play a short distinct chime (`ding.wav`) immediately before opening the microphone.
* Without a sound cue, users start speaking before the recording window opens or while the speaker buffer is discharging, resulting in clipped initial words.

### B. TTS Echo Elimination Delay
* Never open the microphone immediately upon TTS API return. The hardware audio amplifier buffer retains sound for 300–500ms after function exit.
* Add an explicit `time.sleep(0.4 - 0.5)` between `sync_do_tts()` and `arecord` to prevent the robot from recording and transcribing its own synthesized voice.

### C. Multi-Turn Conversational Session State
* Avoid single-shot wake-word loops that force the user to say *"Halo Robot"* before every single sentence.
* Implement a **Conversation State Machine**:
  1. **Standby Mode:** Listens in 2-second low-cost chunks for Wake Words (`"Halo Hermes"`, `"Yanshee"`, `"Robot"`).
  2. **Active Multi-Turn Mode:** Once triggered, keeps the session alive. After answering, immediately plays a *"Ding!"* and listens for follow-up questions.
  3. **Auto-Sleep:** If 3 consecutive cycles (~12-15s) detect no user speech, announce *"Saya standby dulu ya, sir"* and gracefully return to Standby.

---

## 4. Hardware Push-to-Talk / Push-to-Stop Integration

* **ROS Topic Bridge:** Humanoid robots with physical chest buttons (e.g. `/hal_button_info`) should bridge button events to the agent loop via ROS subscriber (`std_msgs/Int32`).
* **Dual-Trigger Fallback:** Allow both voice commands (*"Stop musik"*, *"Matikan"*) and physical button presses to interrupt long-running tasks, music playback, or movements instantly.

---

## 5. Multimedia Playback & Acoustic Ducking Calibration

* **Direct Hardware Output:** Route MP3 players (`mpg123`) directly to the physical DAC (`plughw:0,0`).
* **Volume Ducking Balance:** Calibrate media volume to ~50–60% (`mpg123 -f 18000`) during playback. Playing at 100% acoustic volume overpowers the adjacent head microphones, making voice cancellation impossible.
