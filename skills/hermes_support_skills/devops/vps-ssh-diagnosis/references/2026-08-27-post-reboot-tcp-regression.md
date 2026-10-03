# 2026-08-27: Post-Reboot TCP Regression + ISP Routing

## Timeline

1. SSH to 43.134.179.61 failed with "Connection timed out during banner exchange"
2. Diagnosis: TCP connect OK (nc succeeds), but SSH banner never received
3. Root cause: sshd/services hung on VPS, not network issue
4. User rebooted VPS via Tencent Cloud Console
5. After reboot: TCP also stopped working (nc to port 22 also timed out)
6. User enabled SSH via console, still couldn't connect
7. Session ended with VPS unreachable

## Key Findings

### Pattern: TCP works → Reboot → TCP also fails

Before reboot:
- `nc -zv -w5 43.134.179.61 22` → "succeeded" (TCP open)
- SSH banner exchange → timeout (sshd not responding)
- Diagnosis: services hung, not network issue

After reboot:
- `nc -zv -w5 43.134.179.61 22` → timeout (TCP also fails now)
- SSH → timeout
- Diagnosis: VPS still booting, or security group reset, or network path changed

### ISP Routing Context

- Client IP: 125.166.103.191 (Indonesian ISP, likely Telkom)
- VPS IP: 43.134.179.61 (Tencent Cloud)
- tracert showed: hops 1-11 OK, hop 12-30 all timeout
- Traffic died after entering Tencent/transit network (10.162.5.206)
- All TCP ports (22, 80, 443, 20128, 2222, 8022) showed "succeeded" via nc
- But no service responded on any port → services hung, not firewall

### Telegram Bot API as Out-of-Band Probe

- `getMe` returned ok=true → bot account exists
- `getWebhookInfo` showed: url empty, pending_update_count=6
- Conclusion: VPS alive, gateway process not running
- This proved VPS was alive even when SSH/HTTP unreachable

## Lessons

1. **TCP open + no service response = services hung** — different from network unreachable
2. **Post-reboot regression** — reboot can temporarily make things worse (services not started yet)
3. **Telegram Bot API probe** — fastest way to check VPS health when SSH unreachable
4. **User preference** — keep trying automated approaches before suggesting manual console access
