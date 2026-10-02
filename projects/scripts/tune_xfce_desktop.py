import subprocess
import os

env = os.environ.copy()
env['DISPLAY'] = ':10'

commands = [
    # Window Manager (xfwm4) - Disable all heavy rendering
    ['xfconf-query', '-c', 'xfwm4', '-p', '/general/use_compositing', '-s', 'false', '--create', '-t', 'bool'],
    ['xfconf-query', '-c', 'xfwm4', '-p', '/general/vblank_mode', '-s', 'off', '--create', '-t', 'string'],
    ['xfconf-query', '-c', 'xfwm4', '-p', '/general/shadow_delta_height', '-s', '0', '--create', '-t', 'int'],
    ['xfconf-query', '-c', 'xfwm4', '-p', '/general/shadow_delta_width', '-s', '0', '--create', '-t', 'int'],
    ['xfconf-query', '-c', 'xfwm4', '-p', '/general/shadow_opacity', '-s', '0', '--create', '-t', 'int'],
    ['xfconf-query', '-c', 'xfwm4', '-p', '/general/show_dock_shadow', '-s', 'false', '--create', '-t', 'bool'],
    ['xfconf-query', '-c', 'xfwm4', '-p', '/general/show_frame_shadow', '-s', 'false', '--create', '-t', 'bool'],
    ['xfconf-query', '-c', 'xfwm4', '-p', '/general/show_popup_shadow', '-s', 'false', '--create', '-t', 'bool'],
    ['xfconf-query', '-c', 'xfwm4', '-p', '/general/tile_on_move', '-s', 'false', '--create', '-t', 'bool'],
    ['xfconf-query', '-c', 'xfwm4', '-p', '/general/box_move', '-s', 'false', '--create', '-t', 'bool'],
    ['xfconf-query', '-c', 'xfwm4', '-p', '/general/box_resize', '-s', 'false', '--create', '-t', 'bool'],

    # GTK / System Settings (xsettings) - Zero Animation & Instant Response
    ['xfconf-query', '-c', 'xsettings', '-p', '/Gtk/EnableAnimations', '-s', 'false', '--create', '-t', 'bool'],
    ['xfconf-query', '-c', 'xsettings', '-p', '/Gtk/CursorBlink', '-s', 'false', '--create', '-t', 'bool'],
    ['xfconf-query', '-c', 'xsettings', '-p', '/Gtk/ButtonImages', '-s', 'false', '--create', '-t', 'bool'],
    ['xfconf-query', '-c', 'xsettings', '-p', '/Gtk/MenuImages', '-s', 'false', '--create', '-t', 'bool'],

    # Desktop Icons (xfce4-desktop) - Stop heavy thumbnail disk I/O
    ['xfconf-query', '-c', 'xfce4-desktop', '-p', '/desktop-icons/file-icons/show-thumbnails', '-s', 'false', '--create', '-t', 'bool'],

    # Power Manager - Never sleep or blank screen during RDP session
    ['xfconf-query', '-c', 'xfce4-power-manager', '-p', '/xfce4-power-manager/blank-on-ac', '-s', '0', '--create', '-t', 'int'],
    ['xfconf-query', '-c', 'xfce4-power-manager', '-p', '/xfce4-power-manager/dpms-on-ac-sleep', '-s', '0', '--create', '-t', 'int'],
    ['xfconf-query', '-c', 'xfce4-power-manager', '-p', '/xfce4-power-manager/dpms-on-ac-off', '-s', '0', '--create', '-t', 'int'],
]

for cmd in commands:
    try:
        res = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=5)
        # print("OK:", cmd[2], cmd[4], "->", res.stdout.strip())
    except Exception as e:
        print("FAIL:", cmd, e)

print("All XFCE desktop parameters tuned for ultra-low latency RDP!")
