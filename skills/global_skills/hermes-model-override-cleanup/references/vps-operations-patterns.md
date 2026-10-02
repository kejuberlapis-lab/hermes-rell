# VPS Operations Patterns

## SSH Access via SSH_ASKPASS

When password auth is needed and sshpass is not installed:

```bash
# Create temporary askpass script
echo '#!/bin/bash
echo "PASSWORD"' > /tmp/askpass.sh
chmod +x /tmp/askpass.sh

# Use for SSH
DISPLAY=:0 SSH_ASKPASS=/tmp/askpass.sh SSH_ASKPASS_REQUIRE=force \
  setsid ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no \
  -o PubkeyAuthentication=no user@host "command"

# Clean up after
rm -f /tmp/askpass.sh
```

**SECURITY:** Password sent in chat is exposed. Remind user to change after use.

## VPS Disk Cleanup (Safe Targets)

When disk is >90% on VPS:

| Target | Command | Estimated Space |
|--------|---------|-----------------|
| /tmp leftovers | `sudo rm -rf /tmp/pip-* /tmp/go-build*` | ~1.5GB |
| pip cache | `pip cache purge` | ~1.2GB |
| uv cache | `uv cache clean` | ~980MB |
| npm cache | `npm cache clean --force` | ~932MB |
| go-build cache | `rm -rf ~/.cache/go-build` | ~382MB |
| 9router old backups | `rm -rf ~/.9router/backups/pre_upgrade_*` | ~3.6GB |
| journal logs | `sudo journalctl --vacuum-time=3d` | ~300MB |

**Always backup configs before cleanup.**

## Model Verification Checklist (Quick)

```python
# Run on VPS to verify all profiles
import yaml, os, glob
profiles_dir = os.path.expanduser('~/.hermes/profiles')
for p in sorted(glob.glob(os.path.join(profiles_dir, '*'))):
    if not os.path.isdir(p): continue
    name = os.path.basename(p)
    cfg = os.path.join(p, 'config.yaml')
    if not os.path.exists(cfg): continue
    with open(cfg) as f:
        c = yaml.safe_load(f) or {}
    m = c.get('model', {})
    cp = c.get('custom_providers', [])
    cp_name = cp[0].get('name', '?') if cp else 'none'
    print(f"{name} | model={m.get('default','?')} | provider={m.get('provider','?')} | cp_name={cp_name}")
```
