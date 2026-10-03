---
name: ubuntu-xrdp-xfce-setup
description: Install and troubleshoot XRDP on Ubuntu VPS using XFCE, including service/port checks and common remote desktop login failures.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Ubuntu XRDP + XFCE Setup

Use this when a user cannot connect with Windows Remote Desktop (mstsc) to an Ubuntu VPS, or asks to enable GUI/RDP access.

## Preconditions
1. You have SSH access to the VPS (IP, user, auth method).
2. OS is Ubuntu/Debian-like.
3. User accepts system changes (package install + service config edits).

## Fast diagnosis (before changing anything)
Run these checks remotely:

1) OS:
- `cat /etc/os-release`

2) XRDP package/service:
- `dpkg -l | grep -E '^ii\s+xrdp\b'`
- `systemctl is-enabled xrdp`
- `systemctl is-active xrdp`
- `systemctl status xrdp --no-pager -n 20`

3) Port listen:
- `ss -tulpn | grep ':3389'`

4) Firewall:
- `ufw status`

5) Desktop environment presence:
- `dpkg -l | grep -E '^ii\s+(xfce4|gnome-shell|ubuntu-desktop)\b'`

Interpretation:
- If xrdp not installed + 3389 not listening + no desktop installed, mstsc login failure is expected.

## Install & configure (recommended lightweight path)

```bash
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y xfce4 xfce4-goodies xrdp xorgxrdp
adduser xrdp ssl-cert || true
printf 'startxfce4\n' > ~/.xsession
chmod 644 ~/.xsession
```

Set `/etc/xrdp/startwm.sh` to prefer user session and XFCE fallback:

```sh
#!/bin/sh
if [ -r /etc/profile ]; then
  . /etc/profile
fi
if [ -r ~/.profile ]; then
  . ~/.profile
fi
if [ -r ~/.xsession ]; then
  exec /bin/sh ~/.xsession
fi
exec startxfce4
```

Then:

```bash
chmod +x /etc/xrdp/startwm.sh
systemctl enable xrdp
systemctl restart xrdp
```

## Verification

```bash
systemctl is-enabled xrdp   # expected: enabled
systemctl is-active xrdp    # expected: active
ss -tulpn | grep ':3389'    # expected: LISTEN by xrdp
```

Client login instructions (Windows mstsc):
- Computer: `<VPS_IP>`
- Session: `Xorg`
- Username/password: Linux account credentials

## Common pitfalls
1. Cloud firewall/security group blocks TCP 3389 even if service is active.
2. Local UFW may still need explicit allow rule:
   - `ufw allow 3389/tcp`
3. Root RDP login may be restricted by policy in some hardened images. If so, create normal user and test with that account.
4. If black screen appears, inspect:
   - `/var/log/xrdp.log`
   - `/var/log/xrdp-sesman.log`

## SSH automation note (password-only environments)
If `sshpass` is unavailable and cannot be installed, use a Python venv with `pexpect` to automate password prompts safely for one-off diagnostics and setup.
