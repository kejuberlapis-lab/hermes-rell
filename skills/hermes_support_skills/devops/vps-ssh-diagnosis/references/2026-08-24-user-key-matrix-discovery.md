# 2026-08-24 SSH Access Discovery: User × Key Matrix

## Summary
SSH to VPS 43.134.179.61 was assumed broken because all attempts with `root` user failed. Testing `ubuntu` user with `id_ed25519` key succeeded immediately.

## Timeline
- Previous session (Aug 23): Tried `root` + all 4 keys → all rejected. Concluded "VPS reinstalled, SSH broken."
- This session (Aug 24): User asked to try again. Tested `ubuntu@43.134.179.61` with `id_ed25519` → SUCCESS.

## What worked
```bash
ssh -o ConnectTimeout=5 -o BatchMode=yes -i ~/.ssh/id_ed25519 ubuntu@43.134.179.61 "echo OK"
# Output: ok (exit 0)
```

## What failed
```bash
# All root attempts:
ssh -i <any_key> root@43.134.179.61 "echo OK"
# → Permission denied (publickey,password)

# ubuntu with hermes_vps_zeus_sync key:
ssh -i ~/.ssh/hermes_vps_zeus_sync ubuntu@43.134.179.61 "echo OK"
# → Permission denied (publickey,password)
```

## Lesson
Always test a matrix of users × keys before concluding SSH is broken. The VPS likely has `PermitRootLogin no` or similar restriction, while `ubuntu` has the authorized key.

## VPS Status After Access
- Hostname: VM-20-75-ubuntu
- Uptime: 1 day 7 hours
- CPU: 2 cores, load 0.07
- Memory: 1.0G / 7.5G
- Disk: 14G / 79G (19%)
- 9Router: active (port 20128 accessible)
- Hermes Gateway: active (running)
- Telegram token: rejected (needs new token)
