---
name: embedded-robotics-agent-integration
description: Use when deploying Hermes AI agents onto robotics hardware.
category: autonomous-ai-agents
triggers:
  - deploy Hermes to robot / humanoid hardware
  - integrate Yanshee / Raspberry Pi robot with Hermes
  - embedded Linux audio capture and TTS for AI agents
  - legacy Python 3.5 ARM robotics environment integration
  - Tailscale mesh setup on legacy embedded Debian/Raspbian
---

# Embedded Robotics & Humanoid Agent Integration

Class-level guide for deploying, networking, and supervising autonomous Hermes AI agents on embedded Linux robotics hardware (such as Raspberry Pi-based humanoid robots like UBTECH Yanshee).

---

## 1. Network Mesh Setup (Tailscale on Legacy ARM Linux)

When the embedded robot operates behind a local NAT/Wi-Fi router and needs bidirectional SSH/API access with a cloud VPS without port forwarding:

### Step 1 — Install Standalone Static ARM Tarball
Embedded robotics distributions (e.g. Debian 9 Stretch / Raspbian Jessie) often lack standard codenames for automated shell installers. Use the official static binary:

```bash
cd /tmp
wget https://pkgs.tailscale.com/stable/tailscale_latest_arm.tgz
tar -xzf tailscale_latest_arm.tgz
cd tailscale_*_arm
sudo cp tailscale /usr/bin/
sudo cp tailscaled /usr/sbin/
sudo cp systemd/tailscaled.service /lib/systemd/system/
sudo systemctl daemon-reload
```

### Step 2 — Initialize State & Socket Directories
Legacy systemd environments may fail to auto-create runtime directories for `tailscaled`:

```bash
sudo mkdir -p /var/lib/tailscale /var/run/tailscale /etc/default
sudo /usr/sbin/tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/var/run/tailscale/tailscaled.sock > /tmp/tailscaled.log 2>&1 &
sudo tailscale --socket=/var/run/tailscale/tailscaled.sock up
```

### Step 3 — Passwordless Dedicated SSH Key
Generate a dedicated SSH key pair on the VPS (`~/.ssh/id_ed25519_robot`) and append the public key to the robot's `~/.ssh/authorized_keys` with strict permissions (`chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys`).

---

## 2. Audio Hardware & ALSA Capture Pipeline

Embedded robots often use dedicated DSP / DAC hardware (e.g. Microsemi ZL380xx microphone array).

### Critical ALSA Rules & Pitfalls:
1. **Channel Count Enforcement:** Microphone arrays on robotics DACs typically reject mono (`-c 1`) with `Channels count non available`. Always capture in **Stereo 16kHz** (`-c 2 -r 16000 -f S16_LE -D plughw:0,0`).
2. **Integer Duration Only:** In `arecord`, `-d` requires an **integer** (e.g. `-d 3`). Decimal floats like `-d 2.5` crash with `arecord: invalid duration argument`.
3. **Hardware Exclusivity:** The ALSA PCM capture device `/dev/snd/pcmC0D0c` cannot be opened concurrently by multiple processes. If background voice daemons or duplicate script instances run, `arecord` fails with `Device or resource busy`. Always ensure a single process owns the capture loop.

---

## 3. Legacy Python Compatibility (ARM 32-bit / Python 3.5)

Many robotics SDKs (e.g. YanAPI, ROS Kinetic) are pinned to Python 3.5:

1. **No F-Strings:** Python 3.5 syntax rejects f-strings (`f"text {var}"`). Always use `.format()` or string concatenation.
2. **Pip Wheel Staging:** Legacy embedded boards may encounter SSL handshake timeouts during pip downloads. Download pre-built `*.whl` packages on the host VPS and transfer via `scp` for offline `pip3 install /tmp/*.whl`.

---

## 4. Cloud Brain Routing (9Router / OpenAI-Compatible API)

Embedded boards have limited onboard compute. Run inference through the cloud VPS proxy (9Router):

```python
import requests

ROUTER_URL = "http://<tailscale-vps-ip>:20128/v1/chat/completions"
MODEL_NAME = "ag/gemini-3.7-flash-high"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + API_KEY
}
payload = {
    "model": MODEL_NAME,
    "messages": history,
    "max_tokens": 120,
    "temperature": 0.7,
    "stream": False  # Crucial: disable streaming for clean JSON parsing on embedded clients
}
res = requests.post(ROUTER_URL, headers=headers, json=payload, timeout=12)
reply = res.json()["choices"][0]["message"]["content"].strip()
```

---

## 5. Voice Wake-Word Loop & Systemd Supervision

### Resilient Wake-Word Matching:
Online STT engines in non-native languages may transcribe names phonetically (e.g. *"hermis"*, *"yansi"*, *"hemes"*). Define an expanded alias list:

```python
WAKE_WORDS = [
    "hermes", "hermis", "hermas", "hemes", "ermis", "ermes", "kermes",
    "yanshee", "yansi", "yanshe", "yanchi", "yan si",
    "halo", "hallo", "hai", "robot", "bot", "tes"
]
```

### Persistent Background Systemd Unit:
To ensure 24/7 autonomous uptime and auto-restart on boot, configure `/etc/systemd/system/hermes-robot.service`:

```ini
[Unit]
Description=Hermes AI Agent Robot Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 -u /home/pi/hermes_robot.py
Restart=always
RestartSec=3
StandardOutput=append:/home/pi/hermes_robot.log
StandardError=append:/home/pi/hermes_robot.log

[Install]
WantedBy=multi-user.target
```

Enable and start with:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now hermes-robot.service
```
