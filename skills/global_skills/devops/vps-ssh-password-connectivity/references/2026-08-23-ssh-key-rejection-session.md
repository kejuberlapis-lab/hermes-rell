# 2026-08-23 SSH Key Authentication Failure Session

**Date**: August 23, 2026  
**User**: ndisap  
**VPS**: 43.134.179.61 (IP public), 10.3.20.75 (IP private)  
**Username**: ubuntu  
**Issue**: SSH key authentication failed despite correct key placement in `authorized_keys`

## Summary

SSH key-based authentication to VPS `43.134.179.61` failed even though the public key `hermes_vps_zeus_sync.pub` was correctly placed in `~/.ssh/authorized_keys` on the VPS. Both key auth and password auth were rejected.

## Key Details

### Key Fingerprints
- Client key: `hermes_vps_zeus_sync` → ED25519 SHA256: `ZzEDiEFLiJelsob6gFnMzfNqUUydRLQ0WD7RvxwvYOg`
- Public key file: `hermes_vps_zeus_sync.pub` → MD5: `5cc2b565eabaa1abeb5ab50fdbd5d2dd`
- `authorized_keys` on VPS: MD5 `5cc2b565eabaa1abeb5ab50fdbd5d2dd` ✅ (matches key file)

### Authentication Attempts & Results

| Method | Result | Notes |
|--------|--------|-------|
| Public key `hermes_vps_zeus_sync` | ❌ Rejected | Key offered but server immediately disabled method |
| Public key `id_ed25519` | ❌ Rejected | Different key, also rejected |
| Password `galaxy-67#-desert` | ❌ Rejected | Explicitly forced via `PreferredAuthentications=password` |
| Manual socket connect | ❌ "Invalid SSH identification string" | Not an SSH server responding |

### SSH Debug Output Pattern

```
debug1: Offering public key: /home/ndisap/.ssh/hermes_vps_zeus_sync ED25519 SHA256:ZzEDiEFLiJelsob6gFnMzfNqUUydRLQ0WD7RvxwvYOg explicit
debug2: we sent a publickey packet, wait for reply
debug1: Authentications that can continue: publickey,password
debug2: we did not send a packet, disable method    ← KEY PATTERN
debug1: No more authentication methods to try.
ubuntu@43.134.179.61: Permission denied (publickey,password).
```

**Critical observation**: Server receives the publickey packet but immediately disables the auth method without further processing. This indicates an sshd-level restriction, NOT a key format or compatibility issue.

## Historical Context

- SSH worked successfully earlier (session `20260804_205203_02ce1c` on Aug 4, 2026)
- Skill `vps-ssh-password-connectivity` and `vps-ssh-diagnosis` were both active during that session
- Failure mode appeared suddenly; no configuration changes were logged by user

## Root Cause (Likely)

The sshd on VPS has a configuration restriction that prevents key-based auth, such as:

1. `AuthorizedKeysFile` pointing to a different file or `/dev/null`
2. `Match` blocks restricting keys by source IP, user, or group
3. `ForceCommand` or restricted shell for `ubuntu` user
4. `TrustedUserCAKeys` or `TrustedAdminCAKeys` overriding authorized_keys

## Recovery Actions (Requires VPS Console Access)

Since SSH is completely inaccessible, out-of-band access is needed:

### Tencent Cloud Console Access

1. Login to Tencent Cloud Console
2. Navigate to CVM → VPS-Zeus → **Login** → **Web Shell (VNC)**
3. Execute:

```bash
# 1. Verify authorized_keys content
cat ~/.ssh/authorized_keys

# 2. Check sshd_config for restrictions
cat /etc/ssh/sshd_config | grep -E "^(AuthorizedKeysFile|Match|ForceCommand)"

# 3. Fix: Ensure authorized_keys has correct key and no restrictions
> ~/.ssh/authorized_keys
cat ~/.ssh/hermes_vps_zeus_sync.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# 4. Restart sshd
sudo systemctl restart sshd

# 5. Verify SSH is restored
ssh -o BatchMode=yes -o ConnectTimeout=5 -o PreferredAuthentications=publickey -i ~/.ssh/hermes_vps_zeus_sync ubuntu@43.134.179.61 "echo 'SUCCESS'"
```

### Alternative: Re-generate Key Pair

If the key itself is suspected to be corrupted or blocked:

```bash
# Generate new key pair locally
ssh-keygen -t ed25519 -f ~/.ssh/hermes_vps_zeus_sync_new -N '' -C 'hermes-local-vps-zeus-sync-new'

# Copy public key to VPS via console
cat ~/.ssh/hermes_vps_zeus_sync_new.pub

# Add to authorized_keys on VPS (via console)
> ~/.ssh/authorized_keys
# Paste the new public key content

# Test SSH
ssh -o BatchMode=yes -o ConnectTimeout=5 -i ~/.ssh/hermes_vps_zeus_sync_new ubuntu@43.134.179.61 "echo 'SUCCESS'"
```

## Lessons Learned

1. **Matching MD5 hashes ≟ guaranteed auth** — Even when `authorized_keys` and the public key file have identical MD5 hashes, the SSH server may still reject the key due to config restrictions.

2. **Debug pattern is diagnostic** — The pattern `debug1: Offering public key` → `debug2: we sent a publickey packet, wait for reply` → `debug1: Authentications that can continue: publickey,password` → `debug2: we did not send a packet, disable method` is a strong indicator of sshd-level restriction.

3. **Don't assume key issue** — "permission denied (publickey,password)" means BOTH auth methods failed, not just key-based auth.

4. **Historical sessions matter** — This capability (SSH to this VPS) worked before (Aug 4, 2026). Sudden failure suggests VPS configuration changed or security policy was updated.

5. **VPS console is fallback** — When SSH is completely inaccessible, Tencent Cloud Web Shell provides out-of-band access to diagnose and fix sshd configuration.

## Related Skills Updated

- `devops/vps-ssh-password-connectivity` — Added pitfall about sshd-level key rejection despite correct key placement
- `devops/vps-ssh-diagnosis` — Added same pitfall for banner-exchange and key rejection patterns

## References

- `references/2026-06-29-ram-crash-recovery-session.md` — Earlier VPS RAM crash recovery session
- Skill: `vps-ssh-password-connectivity` — Password-based SSH troubleshooting
- Skill: `vps-ssh-diagnosis` — SSH diagnosis for banner exchange timeouts