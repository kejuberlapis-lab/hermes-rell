---
name: humanoid-robotics-voice-and-hardware-integration
description: Use when integrating AI voice agents into humanoid robots.
---

# Humanoid Robotics Voice & Hardware Integration

Integrate bidirectional voice conversations, AI reasoning, wake words, and hardware control onto edge humanoid robots (UBTECH Yanshee, Raspberry Pi ARMv7/aarch64, ROS-based platforms) paired with cloud/VPS LLM endpoints.

---

## 1. Network & Remote Bridge Architecture

- **Tailscale Mesh Network:** Connect the edge robot (behind NAT/LAN Wi-Fi) to the cloud/VPS LLM backend using Tailscale (`tailscaled`).
  - *On legacy 32-bit ARM (ARMv7l):* If `curl | sh` fails due to missing `VERSION_CODENAME`, download standalone static binaries (`tailscale_latest_arm.tgz`) and run daemon manually with custom sockets (`/var/run/tailscale/tailscaled.sock`).
- **Passwordless SSH Keypair:** Generate dedicated ed25519 key on VPS and authorize on robot (`~/.ssh/authorized_keys`) for non-interactive deployments and systemd maintenance.

---

## 2. Hardware Audio & DSP Configuration (ALSA / Microsemi ZL380xx)

Humanoid robots often route multi-microphone arrays through specialized DSP audio codecs (e.g. Microsemi ZL380xx) on I2S.

### Hardware Gates & Unmuting
1. **ALSA Unmute & Sensitivity:**
   ```bash
   # MUTE control is active-boolean: 'off' means unmuted!
   amixer -c 0 cset numid=2 off
   amixer -c 0 cset numid=3 15    # Maximum microphone gain
   amixer -c 0 sset DAC 18        # Calibrated speaker output (~85%)
   ```
2. **Native Sample Rate Locking:**
   - Always record at native DSP clock (`-r 48000 -c 2 -f S16_LE` on `plughw:0,0`).
   - *Pitfall:* Recording at 16000 Hz when DSP runs at 48000 Hz causes 3x playback speedup and corrupts STT audio.
3. **STT Utility Dependency:**
   - Install `flac` (`sudo apt-get install -y flac`). Without `flac`, Python `speech_recognition` fails with silent `OSError`.

---

## 3. Conversational Pipeline & Audio Timing

```
[Standby Wake Word Loop (2s)]
       │ (e.g. "Halo Hermes", "Robot", "Yanshee")
       ▼
[Robot Answers: "Ya, sir?"] ──► [Play Chime: ding.wav]
                                        │
                                        ▼
                         [Active Interaction Loop (4s)]
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
            [User Speaks Command]                   [Silence Timeout]
                    │                                (3 cycles -> Sleep)
                    ▼
          [LLM Query to VPS]
                    │
                    ▼
          [TTS Robot Response]
                    │
                    ▼
         [Play Chime: ding.wav] ──► (Loop continues for follow-up questions)
```

### Critical Voice UX Rules
- **Sound Cue (Chime):** Always play a clear audio chime (`ding.wav`) immediately before opening the microphone so the user knows exactly when to start speaking.
- **Speaker Drain Delay:** Insert `time.sleep(0.4)` to `0.5` after TTS playback before opening the mic to prevent the robot from recording its own speaker echo.
- **TTS Pacing:** Format AI output with commas and short clauses (`text.replace(". ", ", ")`) to enforce natural pauses on robotic speech synthesizers.
- **Multi-Turn Continuity:** Keep the interaction session open after answering so the user can ask consecutive questions without repeating the wake word.

---

## 4. Hardware Actuation & Multimedia Playback

### Avoiding Hardware Collisions
- *Pitfall:* Raw ALSA hardware devices (`plughw:0,0`) cannot handle concurrent capture (`arecord`) and playback (`mpg123`) simultaneously. Never spawn background recording while playing music or motors on raw HW; it causes PCM device collisions (`Broken configuration`) and crashes playback.
- *Pitfall:* Do not pass custom scale flags like `-f 18000` to `mpg123` on 32-bit ARM Linux; it triggers integer overflow segmentation faults. Use native `mpg123 -a plughw:0,0 -q <file>`.

### ROS Physical Button Bridge (Push-to-Talk / Push-to-Stop)
Bridge robot physical buttons (e.g. chest button on ROS topic `/hal_button_info`) via a lightweight Python ROS node to an IPC flag (`/tmp/button_pressed.flag`):
```python
import rospy
from std_msgs.msg import Int32

def callback(msg):
    with open('/tmp/button_pressed.flag', 'w') as f:
        f.write(str(msg.data))

rospy.init_node('hermes_button_bridge', anonymous=True)
rospy.Subscriber('/hal_button_info', Int32, callback)
rospy.spin()
```
This provides instant hardware push-to-stop/talk without consuming audio channels.
