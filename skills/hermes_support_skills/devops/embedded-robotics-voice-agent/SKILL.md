---
name: embedded-robotics-voice-agent
description: Use when building embedded robotics voice agents with ALSA.
---

# Embedded Robotics & Voice Agent Integration

Use this skill when deploying Hermes or LLM agent instances onto edge Linux systems (such as Raspberry Pi, humanoid robots like UBTECH Yanshee, or ARM SBCs) with full-duplex 2-way voice communication, hardware audio routing, and physical command execution.

## 1. Edge Audio & Hardware DSP Architecture

1. **Hardware Rate Matching:**
   - Always query the hardware DSP clock rate using ALSA tools before configuring recording loops.
   - If an I2S/DSP chip runs at 48000 Hz, requesting 16000 Hz directly on `hw:` or `plughw:` will record at 3x clock speed, corrupting audio samples. Record at native rate (48kHz) and downsample in software if needed.

2. **ALSA Mixer & Hardware Unmuting:**
   - On factory/OEM robot OS builds, microphone ADCs or DSP capture channels are frequently locked or muted by default mixer controls (e.g. `MIC SOUT MUTE: on` or `DAC: 0`).
   - Explicitly enforce unmuting and set gain before starting the voice daemon:
     ```bash
     amixer -c 0 cset numid=2 off # Unmute capture switch
     amixer -c 0 cset numid=3 15  # Set max gain
     ```

3. **Required Codec Utilities:**
   - Python `SpeechRecognition` requires the system `flac` binary to compress WAV files prior to transmission. Always ensure `flac` is installed (`sudo apt-get install -y flac`) to prevent silent STT failures.

---

## 2. Conversational Voice Engine (Multi-Turn Architecture)

To provide a natural, hands-free conversational experience without requiring repeated wake-words:

1. **Audio Chime Cue (Ding Sound):**
   - Play a short, crisp audio chime (`ding.wav`) via `aplay -D plughw:X,Y` immediately after the wake word acknowledgment to signal clearly to the user that the microphone is open and recording.
   - Enforce a 0.3–0.5s pause after robot TTS finishes speaking before opening the microphone to prevent the robot from recording its own speaker echo.

2. **Continuous Multi-Turn Session:**
   - Once triggered by a wake word, do not immediately drop back to standby mode after a single answer.
   - Maintain an active conversational loop that listens for follow-up questions for 2–3 consecutive cycles (8–12 seconds).
   - Only return to sleep/standby mode if consecutive silence is detected or explicit dismissal phrases ("selesai", "terima kasih", "cukup", "tidur") are spoken.

3. **Low-Latency LLM Routing:**
   - For real-time spoken conversation, route queries to low-latency fast models (such as `ag/gemini-3.7-flash-high` / `ag/gemini-3.8-flash-low` with strict `max_tokens: 60`).
   - Format responses with natural comma pauses (`replace('. ', ', ')`) so embedded TTS synthesizers speak with relaxed, natural cadence rather than rushed machine speed.

---

## 3. Physical Hardware Execution & Multimedia Isolation

1. **Separation of Voice vs. Music Modes:**
   - When the user commands media playback (e.g., MP3 or radio stream via `mpg123`), transition the state machine into a dedicated **Music Playback Mode**.
   - Suppress the audio chime ("Ding!") and active conversational TTS while music is playing to prevent audio device lockups (`EBUSY`) on ALSA.
   - Run a quiet, low-overhead background listener to detect pause/stop keywords (`"stop musik"`, `"matikan lagu"`, `"berhenti"`) and kill the audio process gracefully.

2. **Direct Hardware Audio Routing:**
   - Route media players directly to the hardware amplifier device (`plughw:0,0`) rather than virtual software sinks (`default`) on embedded Linux distributions that lack a running PulseAudio/PipeWire daemon.
