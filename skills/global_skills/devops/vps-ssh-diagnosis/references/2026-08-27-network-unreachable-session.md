# Session 2026-08-27: Network-Level Unreachable

## Problem
VPS 43.134.179.61 completely unreachable from WSL. All connection methods failed:
- `ping` → 100% packet loss
- `ssh` (all keys, all users) → Connection timed out
- `curl` (ports 80, 443, 20128) → timeout / connection refused
- `nc -zv` (ports 22, 80, 443, 20128) → timeout

## Environment
- Client IP: 125.166.103.191 (Indonesian ISP)
- WSL2 on Windows host
- VPS provider: Tencent Cloud
- VPS IP: 43.134.179.61 (confirmed unchanged by user)

## User-Confirmed Status
- Tencent Cloud console: instance Running
- Security groups: all TCP ports opened
- IP address: confirmed not changed

## Diagnosis
- Not an SSH/sshd issue — ALL TCP connections timeout, not just SSH
- Not a firewall/security group issue — user confirmed open
- Not a VPS-side issue — user confirmed via console
- Client-side network routing problem
- Most likely: ISP routing to Tencent Cloud IP range blocked/degraded

## Resolution Not Achieved
Session ended without resolving — suggested:
1. Cross-check from Windows PowerShell (not WSL)
2. Test from different network (mobile hotspot)
3. Contact Tencent Cloud support if routing issue confirmed

## Key Learning
- When ALL connections timeout (not just SSH), it's a network routing issue, not server-side
- Always test from Windows host when diagnosing from WSL
- WSL2 NAT networking may route differently than Windows host
- ISP-level routing blocks to certain cloud providers are real, especially in SEA
