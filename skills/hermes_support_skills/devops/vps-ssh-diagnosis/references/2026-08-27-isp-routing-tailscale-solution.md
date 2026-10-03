# 2026-08-27: ISP Routing Block → Tailscale Solution

## Problem
- SSH to VPS 43.134.179.61 completely unreachable from WSL (Ubuntu 26.04, ISP: Telkom Indonesia 125.166.x.x)
- All ports timeout: ping, SSH, HTTP, nc — even after VPS reboot and SSH reset via console
- Windows tracert showed routing dying at hop 12 (backbone internasional Telkom → Tencent Cloud)
- User confirmed: VPS Running, IP unchanged, security groups fully open

## Diagnosis Path
1. `ping` → 100% loss
2. `nc -zv port 22` → timeout (but earlier session showed TCP connect succeeded intermittently)
3. `ssh -vvv` → "Connection timed out during banner exchange"
4. `tracert` from Windows → dies at hop 12 (10.162.5.206 → all timeout)
5. Telegram Bot API probe → bot alive, 6 pending updates (gateway dead, VPS alive)
6. Multiple SSH attempts with different keys → all timeout

## Root Cause
ISP Telkom Indonesia routing to Tencent Cloud IP range (43.134.x.x) was broken at backbone level. Not a VPS issue — the server was reachable via Telegram infrastructure (different routing path).

## Solution
Install Tailscale on VPS via Tencent Cloud Console VNC to create VPN mesh bypass.

## Additional Lessons (second attempt)
1. **Tailscale requires BOTH sides to join the network** — installing on VPS only gives Tailscale IP but client can't reach it without its own Tailscale. User refused to install Tailscale on WSL.
2. **All ports open but no services responding** — `nc -zv` succeeds on ALL ports (22, 80, 443, 20128) but SSH banner times out and HTTP returns empty. Indicates VPS services crashed/hung, not a routing issue. Fix: reboot via console.
3. **Post-reboot regression** — After reboot, even TCP (nc) can timeout if VPS is still booting. Wait 60-90s before retrying.
4. **Reverse SSH tunnel via serveo.net/localhost.run** — Alternative when user refuses to install VPN/tunnel software on local machine. Run `ssh -R 0:localhost:22 serveo.net` on VPS console to create a public SSH endpoint.
5. **User preference: don't repeat rejected solutions** — Once user says "jangan tailscale" or "ga", stop suggesting it and move to next alternative.

## User Frustration Signal
User said "coba lagi" (try again) 5+ times, "sudah coba ulangin dari awal" (tried from scratch), and "ga" when asked to try from HP hotspot. This indicates they wanted a **solution**, not more SSH retries. After 2-3 failed attempts with consistent timeout pattern, should have jumped to tunnel solution immediately.

## Lessons
1. When tracert shows routing death at specific hop, SSH will never work — go to tunnel immediately
2. Telegram Bot API is reliable out-of-band probe when direct TCP is unreachable
3. User frustration with repeated "try again" = they want solutions, not retries
4. Tailscale is simplest tunnel solution (one-line install, free, works through most firewalls)
