---
name: xrdp-live-session-resilience
description: Use when fixing or bridging live XRDP GUI sessions.
tags: [xrdp, xfce, remote-desktop, vnc, live-trading, metatrader, wine, session-recovery]
---

# XRDP Live Session Resilience & Zero-Downtime Recovery

Playbook for troubleshooting, recovering, and bridging headless Linux XRDP / XFCE4 desktop sessions running mission-critical 24/7 applications (e.g. Wine / MetaTrader 5 algo trading) without process kills or downtime.

---

## 1. Dead FUSE Mount Traps (`thinclient_drives`)

### Problem & Mechanism
When an RDP client abruptly disconnects or `xrdp-chansrv` crashes/resets, the Windows shared drive mount at `/home/ubuntu/thinclient_drives` remains mounted as an unresponsive/stale FUSE filesystem.
Any subsequent X11 process, Xorg driver, desktop manager, `xdotool`, `wmctrl`, or bash command that accesses `/home/ubuntu` or queries window trees becomes blocked in uninterruptible kernel sleep (`D` state / I/O wait), causing reconnection attempts to time out, freeze, or render a black screen.

### Non-Destructive Remediation
Unmount stale FUSE mount points before executing X11 probes or restarting services:
```bash
fusermount -u -z /home/ubuntu/thinclient_drives 2>/dev/null || true
fusermount -u -z /home/ubuntu/.cache/doc 2>/dev/null || true
sudo fusermount3 -u -z /run/user/1000/doc 2>/dev/null || true
```

---

## 2. Multi-Display Session Allocation Mismatch

### Problem & Mechanism
XRDP sesman often allocates a new virtual display (e.g., `:15` after `:14`) when a user connects from a new IP, different screen resolution, or after a network drop. Single-instance background applications (like `terminal64.exe` / MetaTrader 5) continue running intact on the original display (`:14`). The user logs into a blank desktop on `:15` and assumes the application crashed.

### Strict Rule: No Killing 24/7 Applications
Never kill or restart Wine / MT5 or mass-kill Xorg processes to "fix" a blank screen. Live positions, trailing stop orders, and EA execution states will be lost.

### Zero-Downtime Live Display Bridge Procedure
1. **Identify Application Display:**
   ```bash
   ps aux | grep -i terminal64
   # Verify DISPLAY env variable in /proc/<PID>/environ
   sudo tr '\0' '\n' < /proc/<PID>/environ | grep "^DISPLAY="
   ```
2. **Bind Local VNC Server to Application Display:**
   Attach `x11vnc` directly to the running application display (e.g., `:14`) without restarting Xorg:
   ```bash
   x11vnc -display :14 -auth ~/.Xauthority -rfbport 5914 -forever -shared -bg -nopw -noxdamage
   ```
3. **Project to Active User Display:**
   Launch the VNC viewer on the user's current active RDP display (e.g., `:15`):
   ```bash
   DISPLAY=:15 XAUTHORITY=~/.Xauthority xtigervncviewer -FullScreen 127.0.0.1:5914 &
   ```
4. **Permanent Desktop Shortcut:**
   Place a quick launcher on the desktop so the user can summon the live trading workspace in any future session with 1 click:
   ```ini
   # /home/ubuntu/Desktop/Lihat_MT5_Live.desktop
   [Desktop Entry]
   Version=1.0
   Type=Application
   Name=Lihat MT5 Live (24 Jam)
   Exec=xtigervncviewer -FullScreen 127.0.0.1:5914
   Icon=wine
   Terminal=false
   StartupNotify=true
   ```
   Make executable: `chmod +x /home/ubuntu/Desktop/Lihat_MT5_Live.desktop`

---

## 3. Non-Destructive Visual Verification

When diagnosing desktop state, avoid tools that can hang. Capture the root window framebuffer directly using FFmpeg and inspect with vision tools:
```bash
ffmpeg -f x11grab -video_size 1468x923 -i :<display> -vframes 1 /tmp/rdp_verify.png -y
```
