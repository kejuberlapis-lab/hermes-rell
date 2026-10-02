# 9Router VPS Setup — 25 Aug 2026

## Summary
Set up 9Router on VPS 43.134.179.61 as independent provider for profile bots.

## What Was Done

### 1. Bind Address Change (127.0.0.1 → 0.0.0.0)
Default 9Router binds to localhost only. To access from outside:
```bash
sed -i 's/--host 127.0.0.1/--host 0.0.0.0/' ~/.config/systemd/user/9router.service
systemctl --user daemon-reload && systemctl --user restart 9router.service
```
Verify: `ss -tlnp | grep 20128` → should show `0.0.0.0:20128`

### 2. Port Security Group
VPS is Tencent Cloud (CVM). Port 20128 was already open in security group (tested with bash TCP connect). No additional firewall config needed (UFW inactive, iptables ACCEPT).

### 3. API Key Creation in SQLite
9Router v0.5.55 stores API keys in `~/.9router/db/data.sqlite` table `apiKeys`.
Schema: `id TEXT, key TEXT, name TEXT, machineId TEXT, isActive INTEGER, createdAt TEXT`

Created via Python:
```python
import sqlite3, secrets
key = f'nrouter_{secrets.token_hex(32)}'
db.execute('INSERT INTO apiKeys (id, key, name, machineId, isActive, createdAt) VALUES (?,?,?,?,1,?)',
    (secrets.token_hex(16), key, 'VPS 9Router Key', 'vps-zeus-43.134.179.61', datetime.utcnow().isoformat()))
db.commit()
```
After insert, restart 9Router to pick up new key.

### 4. Dashboard Login Password
- Dashboard at `http://43.134.179.61:20128/login`
- Password stored in `~/.9router/auth/cli-secret`
- `/api/auth/reset-password` requires CLI token (machine-id) and only works from localhost
- To reset: `openssl rand -hex 32 > ~/.9router/auth/cli-secret && systemctl --user restart 9router.service`

### 5. Available Models (default, no providers configured)
11 models available without any provider setup:
- Hermes
- ds/deepseek-v4-pro, ds/deepseek-v4-pro-max, ds/deepseek-v4-pro-none
- ds/deepseek-v4-flash, ds/deepseek-chat, ds/deepseek-reasoner
- minimax/MiniMax-M3, MiniMax-M2.7, MiniMax-M2.5, MiniMax-M2.1

### 6. VPS Config Updated to 9Router
Changed config.yaml model section from OpenRouter to 9Router:
```yaml
model:
  base_url: http://localhost:20128/v1
  default: mimo/mimo-v2.5
  provider: custom
  api_key: sk-ad6...e3ea
```
Used `awk` for line replacement when `sed` and Python string replace failed (encoding issue).

### 7. Multi-Profile Setup
Created 5 profiles with SOUL.md + gateway install:
- hermes-support, profil-admin-mvp, profil-admin-node-b, profil-admin-olo, profil-admin-plus
- All gateways running, all pointing to 9Router (localhost:20128)

## Issues Found
- Telegram bot token `864713...dNu4` still rejected by Telegram servers
- OpenRouter credits exhausted (HTTP 402) — old config, now switched to 9Router
- 9Router has no custom providers configured yet (only default models)
- Dashboard password unknown — reset needed from VPS console

## Key Files
- Service: `~/.config/systemd/user/9router.service`
- DB: `~/.9router/db/data.sqlite` (or `~/.hermes/node/lib/node_modules/9router/app/cli/.build-home/.9router/db/data.sqlite`)
- Auth: `~/.9router/auth/cli-secret` (dashboard password)
- JWT: `~/.9router/jwt-secret`
- Machine ID: `~/.9router/machine-id`
