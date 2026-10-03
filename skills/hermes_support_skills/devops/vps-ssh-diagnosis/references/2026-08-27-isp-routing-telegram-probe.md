# 2026-08-27: ISP Routing Failure + Telegram Bot API Probe

## Problem
VPS 43.134.179.61 completely unreachable from local WSL (Ubuntu 26.04, IP 125.166.103.191).
- Ping: 100% packet loss
- SSH (all keys, all users): timeout on all ports
- HTTP/nc: timeout on ports 22, 80, 443, 20128
- User confirmed: VPS Running in Tencent Console, IP unchanged, security groups fully open (all TCP)

## Diagnosis
- From WSL: all connections timeout → network-level issue
- From Windows PowerShell `tracert 43.134.179.61`: routing dies at hop 12
  - Hops 1-5: local → ISP (Telkom Indonesia, IPs 180.252.x.x, 36.66.x.x)
  - Hops 9-11: transit/Tencent backbone (10.200.x.x, 10.162.x.x)
  - Hops 12-30: all timeout → ISP backbone cannot route to Tencent Cloud IP range

## Key Technique: Telegram Bot API as Out-of-Band Probe
When SSH is completely unreachable, the Telegram Bot API can determine if VPS services are alive:

```bash
BOT_TOKEN="8647139031:AAFW9BnAbayXhYPi8m3hM6EXnChWA3KdNu4"
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getMe" 
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo"
```

Result for this VPS:
- `getMe`: ok=true → bot account exists and is registered with Telegram
- `getWebhookInfo`: url="" (empty), pending_update_count=6 → gateway NOT running
- Conclusion: VPS is alive, gateway process is down, ISP routing is the problem

## Alternative Diagnostic: Windows tracert
When WSL lacks `traceroute`, use PowerShell:
```powershell
powershell.exe -Command "tracert 43.134.179.61"
```
This shows exactly which hop the routing dies at.

## Resolution Options Considered
1. **Cloudflare WARP** — best option but requires Windows-side install (WSL lacks sudo for apt)
2. **Tencent Cloud VNC/Serial Console** — user can access via browser to restart gateway
3. **Mobile hotspot** — different ISP = different routing path
4. **Proxy/tunnel** — free proxies unreliable; needs proper VPN

## Environment Details
- Local: WSL Ubuntu 26.04 on Windows, IP 125.166.103.191 (Indonesian ISP, likely Telkom)
- VPS: Tencent Cloud 43.134.179.61, user=ubuntu, key=id_ed25519
- Windows network adapters: Wi-Fi (Realtek), TAP-Windows (disconnected), VirtualBox, Hyper-V WSL
- No VPN/proxy actively running on Windows
