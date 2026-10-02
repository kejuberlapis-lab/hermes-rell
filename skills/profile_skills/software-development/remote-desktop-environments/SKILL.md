---
name: remote-desktop-environments
description: Use when setting up or tuning Linux XRDP GUI, Wine, & MT5.
tags: [xrdp, rdp, xfce, wine, metatrader, gui, latency, performance, scrolling, resolution]
---

# Remote Desktop Environments (XRDP, XFCE & Wine)

Standard operating procedures, performance tuning, and troubleshooting rules for managing headless Linux remote desktop environments (XRDP + XFCE4) and Windows application emulation (Wine / MetaTrader 5).

---

## 1. XRDP Performance & Low-Latency Tuning

### XFCE Desktop Optimization
By default, XFCE enables window compositing and desktop animations that force full-frame redraws over RDP, causing significant cursor lag and high CPU/bandwidth consumption.

Execute the following configuration for active X11 displays:
```bash
# Disable compositing, vblank sync, and shadow rendering
xfconf-query -c xfwm4 -p /general/use_compositing -s false --create -t bool
xfconf-query -c xfwm4 -p /general/vblank_mode -s off --create -t string
xfconf-query -c xfwm4 -p /general/shadow_opacity -s 0 --create -t int
xfconf-query -c xfwm4 -p /general/show_dock_shadow -s false --create -t bool
xfconf-query -c xfwm4 -p /general/show_frame_shadow -s false --create -t bool
xfconf-query -c xfwm4 -p /general/show_popup_shadow -s false --create -t bool

# Disable GTK animations & cursor blinking (prevents continuous idle frame redraws)
xfconf-query -c xsettings -p /Gtk/EnableAnimations -s false --create -t bool
xfconf-query -c xsettings -p /Gtk/CursorBlink -s false --create -t bool
xfconf-query -c xsettings -p /Gtk/ButtonImages -s false --create -t bool
```

### Pointer & Scroll Speed Stabilization (Anti-Hyper-Scroll)
Touch gestures and trackpads over RDP frequently flood GTK applications with mouse wheel (Button 4/5) events, causing menus and charts to scroll uncontrollably fast.

Configure GTK and XFCE pointer settings to lock 1:1 linear scrolling:
```bash
# GTK 3.0 Configuration (~/.config/gtk-3.0/settings.ini)
mkdir -p ~/.config/gtk-3.0
cat << 'EOF' > ~/.config/gtk-3.0/settings.ini
[Settings]
gtk-enable-smooth-scrolling = false
gtk-mouse-double-click-time = 400
gtk-mouse-double-click-distance = 5
gtk-cursor-blink = false
EOF

# GTK 2.0 Configuration (~/.gtkrc-2.0)
cat << 'EOF' > ~/.gtkrc-2.0
gtk-mouse-double-click-time = 400
gtk-mouse-double-click-distance = 5
EOF

# Lock pointer acceleration curve in active display
xfconf-query -c pointers -p /Default/Threshold -s 4 --create -t int
xfconf-query -c pointers -p /Default/Acceleration -s 1.0 --create -t double
```
*User note for mobile clients:* In the mobile Microsoft RD Client top menu, switch control mode from **Touch Mode** to **Mouse Pointer Mode** (Trackpad) to achieve single-pixel accuracy.

### XRDP Color Depth & Retina / macOS Client Compatibility (`max_bpp`)
- **macOS / Retina Screen Trap:** Modern macOS clients (Microsoft Remote Desktop on Mac / iOS) negotiate 32-bit color depth by default (`Client requested 32 bpp color depth, but server configuration is limited to 24 bpp`). When `max_bpp` is locked at 24, the client fails to render frames properly and presents a blank/black screen.
- **Solution:** Configure `max_bpp=32` under `[Globals]` in `/etc/xrdp/xrdp.ini` to ensure full multi-platform compatibility across macOS, Windows, iPhone, and Android.
- Enable `tcp_nodelay=true`, `tcp_keepalive=true`, and `use_compression=yes`.
- Enlarge TCP send/receive buffers to `4194304` (4MB).
- Set `autorun=Xorg` under `[Globals]` to enable direct seamless login when credentials are saved in client apps.

### Resolution Mismatch & Mobile-to-Desktop Viewport Locking
- **Trap:** When a user connects from a mobile phone (e.g. portrait mode), XRDP/xorgxrdp locks the virtual display geometry to a tall viewport (e.g. `1268x2600`). When reconnecting from a desktop or laptop (landscape), the client viewport clips to the upper black chart area, giving the false appearance of a blank or frozen screen.
- **Non-Destructive Fix (Zero-Downtime):** Add standard landscape modes directly to the active virtual display using `xrandr` without restarting Xorg or interfering with running processes:
  ```bash
  DISPLAY=:<display> xrandr --newmode "1920x1080_60.00" 173.00 1920 2048 2248 2576 1080 1083 1088 1120 -hsync +vsync 2>/dev/null || true
  DISPLAY=:<display> xrandr --addmode rdp0 "1920x1080_60.00" 2>/dev/null || true
  DISPLAY=:<display> xrandr --newmode "1440x900_60.00" 106.50 1440 1528 1672 1904 900 903 909 934 -hsync +vsync 2>/dev/null || true
  DISPLAY=:<display> xrandr --addmode rdp0 "1440x900_60.00" 2>/dev/null || true
  ```
- **Diagnostic Capture:** Capture the root framebuffer safely without intrusive tools:
  ```bash
  DISPLAY=:<display> xwd -root -out /tmp/screen.xwd
  ffmpeg -y -i /tmp/screen.xwd /tmp/screen.png
  ```
  Then inspect with vision tools to verify actual window rendering.

### Linux Kernel & Network Stack Tuning
```ini
# /etc/sysctl.d/99-rdp-performance.conf
net.core.rmem_max=16777216
net.core.wmem_max=16777216
net.ipv4.tcp_rmem=4096 87380 16777216
net.ipv4.tcp_wmem=4096 65536 16777216
net.ipv4.tcp_notsent_lowat=16384
net.ipv4.tcp_slow_start_after_idle=0
net.ipv4.tcp_fastopen=3
vm.swappiness=10
```

---

## 2. Session Isolation, Persistence & Reconnection Stability

### Agent Background Process Persistence (`persist_on_release`)
- **Pitfall:** Launching MetaTrader 5 or Wine applications via agent terminal tools without lifecycle persistence flags causes the process to receive `SIGTERM (exit code -15)` and terminate when agent sessions refresh, context compressions run, or session boundaries occur. Shell-level background wrappers (`nohup ... &`) are rejected by terminal tools in foreground mode.
- **Rule:** Always launch 24/7 background GUI applications using:
  ```json
  terminal(
    command="DISPLAY=:<active_display> wine \"/home/ubuntu/.wine/drive_c/Program Files/MetaTrader 5/terminal64.exe\"",
    background=true,
    persist_on_release=true
  )
  ```
- **Verification:** Confirm process startup and active window tree:
  ```bash
  ps aux | grep -E "terminal64|wine"
  DISPLAY=:<active_display> xwininfo -root -tree | head -n 25
  ```

### DPMS Screen Blanking & Black Screen on Reconnect Fix
- **Mechanism:** When a user disconnects or locks their client, the X server enables power-saving DPMS screen blanking. On reconnect, XRDP re-attaches to the existing session, but the display remains black/blank because no wake event occurred.
- **Solution:** Configure `/etc/xrdp/reconnectwm.sh` to explicitly wake the X screen and disable DPMS upon every reconnection:
  ```sh
  #!/bin/sh
  # Wake up screen and disable DPMS/Screensaver on reconnect
  xset s off 2>/dev/null || true
  xset -dpms 2>/dev/null || true
  xset s reset 2>/dev/null || true
  ```
  Ensure permissions are executable: `sudo chmod +x /etc/xrdp/reconnectwm.sh`.

### Strict Rule: 24/7 Live Trading Non-Intervention & No Indiscriminate Kills
- **Rule:** Never execute mass process kills (`kill -9`, `pkill Xorg`, `pkill terminal64`, or restarting XRDP service) during active trading operations or when MT5 is running 24/7.
- **Why:** Killing Xorg / Wine wipes the active GUI desktop session state, closes live market positions, resets trailing stop trackers, and deletes pending order matrices. Only the user has authorization to restart or stop live trading.
- **Troubleshooting Without Killing:** When diagnosing display or network issues, use non-destructive read-only probes (`ps aux | grep terminal64`, checking `/var/run/xrdp/sockdir/`, checking `/tmp/.X11-unix/`).

### Canonical `startwm.sh` Fix
When clients reconnect with different screen resolutions, systemd/D-Bus environment variables from previous sessions conflict and cause `xfce4-session` / `xfwm4` to exit immediately (`cannot open display: :11.0` or signal 137).

Always configure `/etc/xrdp/startwm.sh` as follows:
```sh
#!/bin/sh
if test -r /etc/profile; then . /etc/profile; fi
if test -r ~/.profile; then . ~/.profile; fi

# Crucial: unset existing bus addresses to allow clean session creation
unset DBUS_SESSION_BUS_ADDRESS
unset XDG_RUNTIME_DIR

export DESKTOP_SESSION=xfce
export XDG_CURRENT_DESKTOP=XFCE
export XDG_SESSION_DESKTOP=xfce

exec startxfce4
```

### Multi-Display Session Orphan & Single-Instance Application Trap
- **Mechanism:** When a user rotates a mobile client (portrait to landscape) or reconnects from a new IP/resolution, XRDP sesman often allocates a new display (e.g. `:13` after `:12`). Single-instance Wine applications (like `terminal64.exe` / MetaTrader 5) continue running on the orphaned display `:12`. When the user clicks MT5 on the new display `:13`, MT5 detects the running process on `:12`, focuses the hidden window on `:12`, and appears completely unresponsive or closed on `:13`.
- **Diagnostic:** Inspect active X11 displays and sockets:
  ```bash
  ls -la /tmp/.X11-unix/
  ps aux | grep -E "Xorg|terminal64|wine"
  ```
- **Recovery:** Identify the active display currently connected to the client (check `/var/run/xrdp/sockdir/` or screenshot each display via `ffmpeg -f x11grab -i :<display> -vframes 1 /tmp/test.png`). Terminate the orphaned Xorg/Wine processes on the dead display, then relaunch the application directly on the active display (`DISPLAY=:<active_display> wine ...`).

---

## 3. Mobile RD Client & Connection Troubleshooting

### Pitfall: Private Subnet vs Public IP in `.rdp` Profiles
Always check that the generated `.rdp` file or connection profile specifies the cloud provider's external **Public IP** (`curl -s -4 ifconfig.me`), not the internal private VPC interface IP (`10.x.x.x`). A private IP causes mobile clients to hang indefinitely on *"Configuring remote PC..."*.

### Preventing Handshake Stalls
- For self-signed certificates where mobile clients stall on TLS verification:
  In `/etc/xrdp/xrdp.ini`, set `security_layer=negotiate` or `security_layer=rdp` and `crypt_level=high`.
- In `.rdp` client configuration files:
  ```ini
  full address:s:<PUBLIC_IP>:3389
  username:s:ubuntu
  session bpp:i:24
  authentication level:i:2
  prompt for credentials:i:0
  negotiate security layer:i:1
  ```
- Ensure SSL certificate keys are readable if TLS is enforced:
  ```bash
  sudo chown root:ssl-cert /etc/ssl/private/ssl-cert-snakeoil.key
  sudo chmod 640 /etc/ssl/private/ssl-cert-snakeoil.key
  sudo adduser xrdp ssl-cert
  ```

---

## 4. Wine & MetaTrader 5 Emulation Rules

### Anti-Debugger Detection in Wine 11+
Bleeding-edge Wine releases (e.g. Wine 11.x development branch) trigger anti-tamper / VMProtect protection inside `mt5setup.exe` ("A debugger has been found running in your system").
- Pin and use **Wine Stable (Wine 10.0-stable)**:
  ```bash
  sudo apt install --allow-downgrades -y winehq-stable=10.0.0.0~noble-1 wine-stable=10.0.0.0~noble-1
  sudo apt-mark hold winehq-stable wine-stable wine-stable-amd64 wine-stable-i386
  ```

### Non-Interactive Mono & Gecko Provisioning
Pre-download and silently install Mono and Gecko MSIs into the Wine prefix to prevent blocking GUI modal popups:
```bash
mkdir -p ~/.cache/wine
curl -fsSL https://dl.winehq.org/wine/wine-mono/9.4.0/wine-mono-9.4.0-x86.msi -o ~/.cache/wine/wine-mono-9.4.0-x86.msi
curl -fsSL https://dl.winehq.org/wine/wine-gecko/2.47.4/wine-gecko-2.47.4-x86_64.msi -o ~/.cache/wine/wine-gecko-2.47.4-x86_64.msi
wine msiexec /i ~/.cache/wine/wine-mono-9.4.0-x86.msi /qn
wine msiexec /i ~/.cache/wine/wine-gecko-2.47.4-x86_64.msi /qn
```

### Broker Server Hostname / Port Explicit Resolution
If MetaTrader 5 reports `authorization on <Broker>-Real failed (Invalid account)` despite correct account ID and password:
1. Verify whether the broker account was created for **MT4 vs MT5** (MT4 accounts cannot authenticate on MT5).
2. Override generic broker server names with the broker's explicit IP or domain and port (e.g., `mt5.real.trade-hw.online:443`).
3. Ensure trading passwords (set in personal dashboard) are distinct from web portal login credentials.

### Desktop Shortcuts & Hidden File Visibility for MQL5 Folders
Because `.wine` is a hidden directory (`.` prefix), provide desktop shortcuts and enable hidden file visibility so users can easily place Expert Advisors (`.mq5`/`.ex5`) and indicators:
```bash
# Enable hidden file visibility in Thunar & XFCE Desktop
xfconf-query -c thunar -p /last-show-hidden -s true --create -t bool
xfconf-query -c xfce4-desktop -p /desktop-icons/file-icons/show-hidden-files -s true --create -t bool

# Create convenient desktop symlinks
ln -sfn "/home/ubuntu/.wine/drive_c/Program Files/MetaTrader 5/MQL5/Experts" /home/ubuntu/Desktop/Folder_EA_Experts
ln -sfn "/home/ubuntu/.wine/drive_c/Program Files/MetaTrader 5/MQL5" /home/ubuntu/Desktop/Folder_MQL5_Utama
```

### Native Web Browser Provisioning
To avoid "Input/output error" when launching default web links from XFCE or MT5, install a full native browser:
```bash
sudo apt install -y google-chrome-stable
sudo update-alternatives --set x-www-browser /usr/bin/google-chrome-stable
```
