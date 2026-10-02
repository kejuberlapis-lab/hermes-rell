---
name: vps-ssh-diagnosis
description: "Diagnose and recover from SSH connection failures on remote VPS — specifically the 'timeout during banner exchange' pattern where TCP port 22 is open but sshd doesn't respond. Covers step-by-step diagnosis, root cause identification, and recovery via alternative console access."
version: 1.0.0
author: Hermes Agent
tags: [ssh, vps, diagnosis, recovery, sshd, banner-exchange, timeout]
---

# VPS SSH Diagnosis & Recovery

Diagnose why SSH to a known VPS is failing. Focused on the specific pattern where:
- `ping` succeeds (VPS alive)
- `nc -zv` confirms port 22 is open (TCP reachable)
- SSH connects but **times out during banner exchange** — sshd accepted TCP but never sent its version string

## Trigger

Use this skill when:
- SSH connection fails with "Connection timed out during banner exchange"
- User reports VPS not responding to SSH
- User suspects resource exhaustion on VPS
- ALL connections (ping, SSH, HTTP, nc) time out completely — indicates network-level unreachable, not sshd issue
- VPS OS was recently reset/reinstalled — host keys and password both change

## Step-by-Step Diagnosis

### 1. Basic Connectivity Check

```bash
ping -c 2 -W 5 <VPS_IP>
```

- ✅ Success = VPS alive, network OK
- ❌ Failure = network down or VPS offline → check Tencent Cloud console

### 2. Port 22 Reachability

```bash
nc -zv -w5 <VPS_IP> 22
```

- ✅ "succeeded" = port open, TCP handshake works
- ❌ Failed = firewall/security group blocking, or VPS down

### 3. Systematic User × Key Matrix Test

Before concluding SSH is broken, test ALL user+key combinations. Previous sessions falsely concluded "all keys rejected" because only `root` was tried — access worked fine with `ubuntu` + `id_ed25519`.

```bash
VPS_IP="<VPS_IP>"
for user in ubuntu root; do
  for key in ~/.ssh/id_ed25519 ~/.ssh/hermes_vps_zeus_sync ~/.ssh/hermes_vps_zeus_sync_new ~/.ssh/hermes_vps_zeus_sync_reset; do
    echo "--- $user × $(basename $key) ---"
    ssh -o ConnectTimeout=5 -o BatchMode=yes -i "$key" "$user@$VPS_IP" "echo OK" 2>&1 | tail -2
  done
done
```

**Pitfall**: Don't assume `root` is the SSH user. Many VPS providers (Tencent, AWS, DO) default to `ubuntu` or a non-root user. Always test `ubuntu` first.

**Session 2026-08-24 lesson**: On VPS 43.134.179.61, `root` was rejected for ALL keys (including `id_ed25519`, `hermes_vps_zeus_sync`, etc.), but `ubuntu` + `id_ed25519` worked immediately. The VPS had been reconfigured to disable root login. Previous session (2026-08-23) spent hours trying only `root` and concluded "all keys rejected" — wasted effort. Always try `ubuntu` user first.

### 4. Verbose SSH (diagnose the failure point)

```bash
ssh -vvv -o ConnectTimeout=10 -o StrictHostKeyChecking=no ubuntu@<VPS_IP> "echo OK" 2>&1 | tail -30
```

Key diagnostic indicators in the output:

| Signal | Meaning |
|--------|---------|
| `Connection established` | TCP 3-way handshake complete |
| `Local version string SSH-2.0-...` | Client sent its version |
| `Connection timed out during banner exchange` | ⚠️ **Server never sent SSH banner back** |
| `Permission denied` | Auth failure, not resource issue |

### 4. Interpreting "Time out during banner exchange"

**Root cause: sshd accepted TCP connection but cannot fork to handle it.**

Common causes in order:
1. **RAM exhaustion** (most common on small VPS) — system memory full, sshd can't allocate new process
2. **MaxStartups limit** — too many concurrent SSH connections hitting server limit
3. **sshd hang/crash** — sshd daemon itself stuck or crashed
4. **OOM kill** — sshd was killed by OOM killer, systemd hasn't restarted it yet

**Cross-check:** If port 80/443 responds (e.g., nginx returns 200), the VPS is alive but resource-starved.

### 5. Check VPS Liveness via HTTP

```bash
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 http://<VPS_IP>:80/
```

- If this returns 200/3xx, web server works → confirms OS alive but sshd broken

### 6. ALL Connections Timeout — Network-Level Unreachable

**When ping, SSH, HTTP, AND nc all timeout completely**, the issue is NOT sshd or server-side. It's a **client-side network routing problem** — the VPS IP is unreachable from your network.

**Key distinction:**
- Banner exchange timeout = SSH connects, server doesn't respond → server issue
- ALL ports timeout = nothing connects at all → network/routing issue

**Diagnostic checklist for "all connections timeout":**

```bash
# 1. Verify your external IP (confirms internet works)
curl -s https://api.ipify.org

# 2. Test multiple ports systematically
VPS_IP="<VPS_IP>"
for port in 22 80 443 20128; do
  nc -zv -w 3 $VPS_IP $port 2>&1 | tail -1
done

# 3. Check if it's WSL-specific vs host-wide
# From Windows PowerShell/CMD:
# ping <VPS_IP>
# tracert <VPS_IP>
# If Windows works but WSL doesn't → WSL networking issue
```

**Common causes (from most to least likely):**
1. **ISP routing block** — some ISPs block or deprioritize traffic to certain cloud provider IP ranges (Tencent Cloud in particular). User confirmed security groups are open, VPS status is Running, IP unchanged → routing issue.
2. **WSL networking limitation** — WSL2 NAT networking may route differently than Windows host. Always cross-check from Windows PowerShell.
3. **Windows firewall** — local firewall blocking outbound to specific IPs/ports.
4. **VPS actually down** — despite console showing "Running", the instance may be hung at hypervisor level.

### 5a. Probe VPS Services via Telegram Bot API

**When SSH is completely unreachable, use the Telegram Bot API as an out-of-band health probe.** The Bot API (api.telegram.org) routes through Telegram's global infrastructure, which often has different peering than direct ISP→cloud paths. This works even when direct TCP connections are blocked by ISP routing.

```bash
BOT_TOKEN="<telegram_bot_token>"

# Step 1: Check if bot account exists and is registered
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getMe" | python3 -m json.tool

# Step 2: Check if gateway process is alive (polling vs webhook)
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo" | python3 -m json.tool
```

**Interpreting results:**

| `getMe` ok | `getWebhookInfo` url | pending_updates | Meaning |
|---|---|---|---|
| true | empty | > 0 | Bot registered but **gateway NOT running** (accumulating unprocessed updates) |
| true | empty | 0 | Bot registered, gateway was recently active |
| true | non-empty | any | Gateway configured with webhook (check webhook status) |
| false | any | any | Bot token invalid or bot was deleted |

**Key insight:** If `getMe` returns ok=true but `pending_update_count` keeps growing, the VPS is alive (Telegram can reach the bot account) but the Hermes gateway process is not polling for updates. This confirms the VPS OS is running — just the gateway service needs restart.

**This is the fastest way to distinguish "VPS down" from "gateway down" when SSH is unreachable.**

**Session 2026-08-27 lesson**: VPS 43.134.179.61 was completely unreachable via SSH/HTTP from Indonesian ISP. But `getMe` returned ok=true and `getWebhookInfo` showed 6 pending updates with empty webhook URL. This proved: (a) VPS was alive, (b) gateway process was dead, (c) only the ISP→Tencent routing was broken. Without this probe, we'd have had to guess whether the VPS was down or just unreachable.

**Resolution path:**
1. Cross-check: ask user to test `ping <VPS_IP>` from Windows PowerShell/CMD directly
2. If Windows also fails: ISP or cloud provider routing issue → suggest testing from different network (mobile hotspot)
3. If Windows succeeds but WSL fails: WSL networking config issue (check `.wslconfig`, try `networkingMode=bridged`)
4. If user confirms VPS is up via console but client can't reach: suggest cloud provider support ticket for routing investigation

**Session 2026-08-27 lesson**: VPS 43.134.179.61 was completely unreachable from WSL (all ports timeout). User confirmed via Tencent Cloud console: instance Running, IP unchanged, security groups fully open. Ping from WSL: 100% packet loss. This was an ISP/routing issue — the Indonesian ISP (IP 125.166.x.x) could not route to Tencent Cloud's IP range. The VPS was actually fine. Testing from a different network would have resolved it faster.

## Recovery via Console

When SSH is completely down, need **out-of-band access** via cloud provider console:

### Tencent Cloud (this user's setup)

1. Login to Tencent Cloud Console
2. Navigate to CVM → VPS-Zeus → **Login** → **Web Shell (VNC)**
3. Execute recovery commands:

```bash
# 1. Check memory pressure
free -h

# 2. Drop page cache (safe, no data loss)
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches

# 3. Check top memory consumers
ps aux --sort=-%mem | head -15

# 4. Restart sshd
sudo systemctl restart sshd

# 5. Verify sshd is running
sudo systemctl status sshd --no-pager

# 6. After SSH restored, check Hermes profiles
systemctl --user list-units --type=service | grep hermes
```

### Aggressive Recovery (if normal cleanup insufficient)

```bash
# Kill top memory consumers (check what they are first)
ps aux --sort=-%mem | head -5
sudo kill -9 <PID>  # confirm process identity first

# Or restart Hermes gateway to free agent memory
systemctl --user restart hermes-gateway
```

### Emergency Memory Recovery — Docker/Container Cleanup

If the VPS runs Docker containers (n8n, databases, etc.) that are consuming significant RAM, removing them can free critical memory:

```bash
# 1. Stop and remove Docker containers
docker stop <container_name> 2>/dev/null
docker rm <container_name> 2>/dev/null

# 2. Remove volumes to free disk+memory cache
docker volume rm <volume_name> 2>/dev/null

# 3. Prune all unused Docker resources
docker system prune -af --volumes 2>/dev/null

# 4. If Docker daemon itself is resource-heavy, uninstall
sudo systemctl stop docker docker.socket containerd 2>/dev/null
sudo apt remove --purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 5. Clean residual deps and data
sudo apt autoremove --purge -y
sudo rm -rf /var/lib/docker /etc/docker 2>/dev/null
```

**⚠️ `docker system prune -af --volumes`** can hang if Docker daemon is busy. If it times out, skip to uninstall directly.

### Emergency Memory Recovery — When sshd Still Won't Start

If VNC console shows RAM starvation but sshd won't restart:

```bash
# The nuclear option — cleanest reset
sudo reboot
```

After reboot:
1. SSH in and immediately run cleanup before services eat RAM again
2. `sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches`
3. Remove or disable non-essential services (Docker, n8n, MySQL if not needed)
4. Then start Hermes profiles one by one to avoid memory spike
## ISP Routing Block → Tunnel Solution (skip retries)

**When ISP routing to VPS is confirmed broken (tracert dies, all ports timeout from both WSL and Windows), DO NOT keep retrying SSH.** Jump directly to tunnel/VPN solution.

### Diagnosis is Complete When:
- `tracert` shows routing dying at specific hop (e.g., hop 12+)
- `nc -zv` to port 22 times out consistently
- Windows `Test-NetConnection` also times out (rules out WSL-specific issue)
- User confirms VPS is Running in cloud console, IP unchanged, security groups open

### Tunnel Solutions (install via cloud console VNC):

**1. Tailscale (recommended — simplest)**
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```
Login via link, get Tailscale IP (100.x.x.x), SSH via that IP.

**⚠️ CRITICAL: Tailscale requires BOTH sides to join the network.** If Tailscale is installed on VPS but NOT on the local machine, the Tailscale IP (100.x.x.x) is unreachable. Either install Tailscale on both sides, or use a different tunnel method.

**2. Reverse SSH tunnel via serveo.net / localhost.run (no install on client needed)**
Run on VPS console — creates public endpoint that forwards to VPS SSH:
```bash
# Option A: serveo.net
ssh -R 0:localhost:22 serveo.net

# Option B: localhost.run
ssh -R 80:localhost:22 localhost.run
```
Get the public address (e.g. `ssh://xxx.serveo.net`) and SSH from client to that address. **No installation needed on client side** — only requires `ssh` on VPS. Best option when user refuses to install software on local machine.

**3. Cloudflare WARP**
```bash
curl -fsSL https://pkg.cloudflareclient.com/install.sh | sudo bash
sudo warp-cli registration new
sudo warp-cli connect
```

**4. FRP (manual but reliable)**
Requires a third-party server with public IP.

### User Frustration Signals

**Signal 1: "coba lagi" repeated** — When user says "coba lagi" (try again) multiple times after SSH fails, they want a **solution**, not more retries. After 2-3 failed SSH attempts with consistent timeout pattern, immediately propose tunnel/VPN approach instead of retrying same command.

**Signal 2: Don't repeat rejected solutions** — Once user rejects a solution (e.g. "jangan tailscale", "engga", "ga"), STOP suggesting it. Move to the next alternative immediately. Repeating rejected suggestions causes frustration. Track which solutions the user has declined and skip them.

## Pitfalls

- **Don't assume SSH key issue** — "timeout during banner exchange" happens BEFORE auth stage. This is not an auth problem.
- **Don't keep retrying SSH** — if sshd can't fork, more attempts just add to MaxStartups load. Switch to console access.
- **SSH ControlMaster sockets can mask the problem** — if a stale control socket exists (`~/.ssh/control*`), client tries to reuse it. Disable with `-o ControlMaster=no`.
- **`free -h` shows low "available" memory as the real signal** — cached/buffered memory is reclaimable and NOT the problem. Watch "available" column, not "used".
- **`swapoff -a` fails when RAM is insufficient** — `swapoff` requires enough free RAM to load the entire swap contents back into memory. If swap is 1.3GB and available RAM is only 157MB, `swapoff -a` will timeout or fail. Fix: free RAM first (kill processes, drop caches) before attempting swapoff. Or accept that swap stays full until a reboot.
- **Batch restart of Hermes profiles triggers memory spike** — restarting 6+ gateway profiles simultaneously causes a memory spike that can crash sshd. Always restart sequentially with `sleep 3` between each, and verify `free -h` before restarting the next batch.
- **After VPS reboot, services restart faster than SSH comes up** — the new boot sequence restarts all Hermes gateways, MySQL, etc. within seconds. If you SSH too early, sshd is up but the memory spike from services hasn't settled yet. Wait 15-30s after boot, or SSH with a longer `ConnectTimeout`.
- **Post-reboot TCP regression** — Sometimes TCP works initially (nc succeeds, but SSH banner fails) but AFTER a VPS reboot, even TCP connections time out. This happens when: (a) VPS is still booting and services haven't started, (b) security group/iptables reset on reboot and blocks ports, or (c) the reboot triggered a different network path. After reboot, always verify with `nc -zv -w5 <IP> 22` before attempting SSH. If nc also fails, wait 60-90s for full boot, then check via console: `sudo ss -tlnp | grep 22` and `sudo systemctl status ssh`.
- **User preference: exhaust automated approaches before suggesting manual steps** — When SSH/VPS is unreachable, keep trying different automated methods (different keys, ports, Telegram API probe, alternative IPs) before asking the user to manually intervene via cloud console. The user gets frustrated by premature "you need to do this manually" suggestions. Only suggest console access after 3+ automated attempts have been exhausted.
- **sshd-level key rejection despite correct key placement** — Even when the correct public key is in `~/.ssh/authorized_keys` and MD5 hashes match, the server may still reject the key. Indicates sshd config restriction: `AuthorizedKeysFile` override, `Match` blocks, `ForceCommand`, or `TrustedUserCAKeys`. Recovery requires VPS console access (Tencent Cloud Web Shell) to inspect `/etc/ssh/sshd_config`.
- **Private IP unreachable from WSL** — Private IP (e.g. `10.3.20.75`) is not reachable from WSL. Only public IP works. Always target public IP exclusively when working from WSL. Verify with `ping` + `nc` before SSH.
- **Pitfall: Assuming both IPs are reachable** — User may conflate `vps` alias with a single IP. Verify which IP is active before running SSH/diagnosis commands.
- **`ssh-copy-id` may fail without `ssh-askpass`** — on minimal VPS setups, `ssh-askpass` is not installed. Use alternative: `cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys`. The key pair `hermes_vps_zeus_sync` (ED25519) is pre-generated in `~/.ssh/` for VPS-Zeus access.
- **Host key verification** — ensure VPS IP is in `~/.ssh/known_hosts` to avoid man-in-the-middle prompts. Use `-o StrictHostKeyChecking=no` only for initial setup, then verify fingerprint matches.
- **WSL vs Windows host networking** — When running from WSL, ALL connections timeout can mean the VPS is unreachable from WSL's NAT network even though Windows host can reach it. Always ask user to cross-check from Windows PowerShell before concluding the VPS is down. WSL2 uses a virtual network adapter that may route differently than the host.
- **Cloudflare WARP requires Windows-side install** — WARP cannot be installed from WSL without sudo access to apt. The install must happen on Windows (download MSI from 1.1.1.1 website or via PowerShell as admin). After WARP is active on Windows, WSL traffic routes through it automatically.
- **Tracert/traceroute not in WSL by default** — WSL Ubuntu doesn't include `traceroute`. Use `powershell.exe -Command "tracert <IP>"` from WSL to run Windows tracert, or install `traceroute` package in WSL if sudo is available.
- **All ports open (nc succeeds) but no service responds** — If `nc -zv` succeeds on ALL ports (22, 80, 443, 20128, etc.) but SSH banner exchange times out and HTTP returns empty, the VPS services have crashed/hung. The OS kernel is still accepting TCP connections but no userspace service is handling them. This is different from "banner exchange timeout" (which is sshd-specific). Fix: reboot VPS via cloud console.
- **Post-reboot: all ports timeout = services not started yet** — After a VPS reboot, if even `nc -zv` times out, the boot process may still be ongoing. Wait 60-90s. If still timeout after 2 minutes, check console: `sudo ss -tlnp` to see if sshd is listening, and `sudo systemctl status ssh` for status.
- **sshd.service alias error on fresh OS** — On Ubuntu 22.04+ and some other distros, `sshd.service` is an alias to `ssh.service`. Running `sudo systemctl restart sshd` gives "refusing to operate on alias name or linked unit file". Fix: use `sudo systemctl restart ssh` (without 'd'). This happens on fresh OS installs where the default service name changed.
- **After VPS OS reset: password AND host keys both change** — The old password from before the reset won't work. You need the NEW password from the cloud console. Also clear `known_hosts` for that IP, or SSH shows "REMOTE HOST IDENTIFICATION HAS CHANGED" and blocks connection. Sequence: (1) clear known_hosts, (2) get new password from console, (3) test SSH.

## Post-OS-Reset Diagnosis (special case)

When VPS OS has been reset/reinstalled, the failure pattern is different from resource exhaustion:

### Symptoms
- Port 22 open (nc succeeds) ✓
- SSH shows "REMOTE HOST IDENTIFICATION HAS CHANGED" warning
- OR: SSH connects but "Permission denied (publickey,password)" with BOTH key AND password failing
- Old password no longer works (password changes on OS reset)

### Root Cause
After OS reset:
1. **Host keys change** — new OS generates new SSH host keys → old `known_hosts` entry is stale
2. **Password changes** — the default password is reset to whatever was set during reimage
3. **authorized_keys may be empty** — fresh OS install starts with no SSH keys authorized

### Fix Sequence
```bash
# 1. Clear stale known_hosts
ssh-keygen -f ~/.ssh/known_hosts -R 'VPS_IP'

# 2. Get NEW password from Tencent Cloud Console (old one won't work)

# 3. Verify port is open
nc -zv -w 5 VPS_IP 22

# 4. Test SSH with new password
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no \
    -o PreferredAuthentications=password \
    -o PubkeyAuthentication=no \
    ubuntu@VPS_IP echo 'VPS OK'
```

### If "Permission denied" even with correct new password
- Check via VNC console: `sudo grep PasswordAuthentication /etc/ssh/sshd_config`
- Some distros (Ubuntu 22.04+) default to `PasswordAuthentication no`
- Fix: `sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config && sudo systemctl restart ssh`
- Then add SSH key: `cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys`

### If "refusing to operate on alias name or linked unit file" when restarting sshd
```bash
# The service is aliased — use the real name
sudo systemctl restart ssh   # not sshd
sudo systemctl enable ssh    # not sshd
```

## Verification

After recovery:
1. SSH in from client: `ssh ubuntu@<VPS_IP> "echo RECOVERED"`
2. Check system resources: `free -h && uptime`
3. Verify service status: `systemctl --user status hermes-gateway 2>/dev/null || true`

## Reference

- `references/2026-06-29-ram-crash-recovery-session.md`: Full session timeline from June 29, 2026 recovery operation.
- `references/2026-08-24-user-key-matrix-discovery.md`: Lesson that SSH access requires testing user×key matrix, not just root+one-key.
- `references/2026-08-27-network-unreachable-session.md`: When ALL connections timeout (not just SSH), it's a client-side network routing issue, not server-side. ISP routing blocks to cloud providers.
- `references/2026-08-27-isp-routing-telegram-probe.md`: ISP routing failure to Tencent Cloud + Telegram Bot API as out-of-band VPS health probe when SSH is unreachable.
