# 2026-08-23 SSH Auth Failure Session

## Context
- User environment: WSL (Windows Subsystem for Linux)
- Target VPS: 43.134.179.61 (public), 10.3.20.75 (private/internal)
- User: ubuntu, password: nxc-6wp-Xqr-4KV (provided but not usable via CLI tools)
- Hermes Agent v0.19.0 running locally with gateway service active

## Connection Tests Performed

### Ping
- `43.134.179.61`: 3/3 packets received (75.5ms avg) — ALIVE
- `10.3.20.75`: Timed out — CLOSED from WSL

### Port 22 Scan
- `43.134.179.61:22`: OPEN — SSH daemon responding but auth fails
- `10.3.20.75:22`: TIMEOUT — NOT reachable

### SSH Authentication (all failed)
Tried multiple keys and methods:
- `id_ed25519` (local default) — Permission denied
- `hermes_vps_zeus_sync` — Permission denied  
- `hermes_vps_zeus_sync_new` — Permission denied
- `hermes_vps_zeus_sync_reset` (newly generated) — Permission denied
- Password auth with `nxc-6wp-Xqr-4KV` — Permission denied (ssh_askpass error)
- Various `ssh -o PreferredAuthentications=` combinations — all failed

### Key Fingerprint Verification
- `id_ed25519`: SHA256:I5X3f2L4uxm+3v1dkOJbM332Wb0LwtO6m4CosxcD+JU (ndisap@AndiRWS)
- `hermes_vps_zeus_sync.pub`: SHA256:ZzEDiEFLiJelsob6gFnMzfNqUUydRLQ0WD7RvxwvYOg (hermes-local-vps-zeus-sync)
- `hermes_vps_zeus_sync_new.pub`: SHA256:OegGDQKtfT2t6HQeK8FVoelb/QRyQ4kyM0pnYFjzekU (hermes-vps-access-$(date +%Y%m%d))
- `hermes_vps_zeus_sync_reset.pub`: SHA256:nL+YZN/yyyD2ISi16FG3PugCxodQ63crDdjDyga3GaY (ndisap@AndiRWS)

All local keys have different fingerprints than what VPS `authorized_keys` contains (which holds `hermes-local-vps-zeus-sync` = `ZzEDiEFLiJelsob6gFnMzfNqUUydRLQ0WD7RvxwvYOg`).

## Root Cause Analysis

### Primary Issue: SSH auth failure despite correct key placement
- VPS `authorized_keys` contains: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAnS2WsocDuFM8Yj9pT40jT4sbkCbELdTMmHKYLh3DeQ hermes-local-vps-zeus-sync`
- This matches the `hermes_vps_zeus_sync.pub` key fingerprint
- Yet ALL keys tried from client failed with `Permission denied (publickey,password)`

### Key Diagnostic Findings
1. **MD5 hash matching is necessary but NOT sufficient** — Even with matching hashes, sshd may reject keys due to configuration restrictions
2. **sshd-level restrictions possible**: `AuthorizedKeysFile` override, `Match` blocks, `ForceCommand`, restricted shell
3. **Private IP not reachable** — `10.3.20.75` is closed from this WSL environment, only public IP `43.134.179.61` works
4. **ssh_askpass error** — `No such file or directory` for `/usr/bin/ssh-askpass` interferes with password auth

### SSH Verbose Debug Output Pattern
```
debug1: Offering public key: /home/ndisap/.ssh/id_ed25519 ED25519 SHA256:I5X3f2L4uxm+3v1dkOJbM332Wb0LwtO6m4CosxcD+JU explicit
debug1: Authentications that can continue: publickey,password
debug2: we did not send a packet, disable method
```
This pattern ("we did not send a packet") indicates the server rejected the key at configuration level BEFORE the key was even accepted for verification.

## Recovery Actions (Requires VPS Console Access)

### Option 1: Via Tencent Cloud Web Shell (Recommended)
1. Login to Tencent Cloud Console → CVM → VPS-Zeus
2. Navigate to **Login** → **Web Shell (VNC)**
3. Execute:
```bash
# Verify authorized_keys content
cat ~/.ssh/authorized_keys

# Verify key fingerprints match
ssh-keygen -l -f ~/.ssh/authorized_keys
ssh-keygen -l -f ~/.ssh/hermes_vps_zeus_sync.pub

# If not matching, reinstall correct key
cat ~/.ssh/hermes_vps_zeus_sync.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Restart sshd
sudo systemctl restart sshd

# Verify
ssh ubuntu@43.134.179.61 "echo 'RECOVERED'"
```

### Option 2: Check sshd_config Restrictions
Inspect `/etc/ssh/sshd_config` for:
- `Match User ubuntu` blocks
- `AuthorizedKeysFile` custom path overrides
- `TrustedUserCAKeys` that might conflict
- `MaxStartups` that might be blocking new connections

### Option 3: Aggressive Memory Recovery
If VPS has RAM exhaustion (common pattern):
```bash
free -h
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo systemctl restart sshd
```

## Post-Recovery Verification
1. `ssh ubuntu@43.134.179.61 "echo RECOVERED"` — should succeed
2. `free -h` — check memory pressure
3. `systemctl --user status hermes-gateway` — verify Hermes gateway still functional
4. Test Hermes one-shot: `hermes -z 'OK'` — proves provider path works independently

## Lessons Embedded in `vps-ssh-diagnosis` Skill
- **MD5 match ≠ key acceptance** — sshd config may block keys even with correct authorized_keys
- **Always verify reachability per IP** — private/internal IPs may be closed from WSL/this environment
- **ssh_askpass errors mask deeper issues** — the "No such file or directory" is a red herring; the real issue is sshd key rejection
- **Verbose SSH debug is essential** — `ssh -vvv` reveals the exact failure point (banner exchange vs auth)
- **Cross-check with HTTP** — if `curl` to VPS:80 returns 200, OS is alive but sshd has issues
- **New pitfall (2026-08-23)**: Don't assume both IPs are reachable; always `ping` and `nc` first

## Reference Files
- `references/2026-06-29-ram-crash-recovery-session.md`: Previous RAM crash recovery (June 2026)
- `vps-ssh-diagnosis` skill: Full diagnosis & recovery workflow