# 2026-08-23 SSH Reachability Session

## Context
Hermes Agent session attempting SSH connection to VPS `43.134.179.61` (user=ubuntu) from WSL environment.

## Key Findings

### 1. Public IP Reachable, Auth Fails
- `43.134.179.61`: Port 22 OPEN, ICMP ping OK
- SSH auth: `Permission denied (publickey,password)` — all keys tried failed
- Kunci SSH `hermes_vps_zeus_sync.pub` seharusnya match dengan `authorized_keys` di VPS (SHA256 sama)
- Masalah: `ssh_askpass` error dan permission denied, bukan key mismatch

### 2. Private IP Unreachable
- `10.3.20.75`: Port 22 CLOSED/TIMEOUT from WSL
- Alias `vps-zeus` / internal network not accessible from this session
- Only public IP `43.134.179.61` accessible from this session

### 3. Diagnostic Steps Performed
```bash
# Ping both IPs
ping -c 3 43.134.179.61   # OK
ping -c 3 10.3.20.75      # Timeout

# Port check
nc -zv -w5 43.134.179.61 22  # Open
nc -zv -w5 10.3.20.75 22    # Closed/Timeout

# SSH verbose
ssh -vvv ubuntu@43.134.179.61 2>&1 | grep -E "(Connection established|banner|timed out|permission)"
```

### 4. SSH Key Details
- Local keys: `id_ed25519`, `hermes_vps_zeus_sync`, `hermes_vps_zeus_sync_new`, `hermes_vps_zeus_sync_reset`
- VPS `authorized_keys`: Contains `hermes-local-vps-zeus-sync` (same SHA256 as local `hermes_vps_zeus_sync.pub`)
- Key permission: Already `chmod 600` applied
- Issue persists despite key match — likely sshd config restriction

### 5. Recovery Path (Not Completed from WSL)
- Required VPS console access (Tencent Cloud Web Shell) to inspect `/etc/ssh/sshd_config`
- Could not execute recovery commands from this session
- Key reset created: `~/.ssh/hermes_vps_zeus_sync_reset` (new key pair)

## Lessons
1. **Always verify IP reachability first** — use `ping` and `nc` before SSH attempts
2. **Private/internal IPs may not be reachable from WSL** — target public IP exclusively
3. **Key match ≠ SSH success** — sshd config may block key acceptance even with correct authorized_keys
4. **`ssh_askpass` errors obscure the real issue** — focus on debug output and sshd config
5. **Backup SSH keys locally** — new key `hermes_vps_zeus_sync_reset` created before attempting recovery

## Reference Commands
```bash
# Verify reachability
ping -c 3 <IP>
nc -zv -w5 <IP> 22

# Check key matching
ssh-keygen -lf ~/.ssh/hermes_vps_zeus_sync.pub
ssh-keygen -lf ~/.ssh/authorized_keys  # (from remote)

# New key generation (if needed)
ssh-keygen -t ed25519 -f ~/.ssh/hermes_vps_zeus_sync_reset -N ""
```