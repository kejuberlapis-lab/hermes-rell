# 9Router — AI Router & Token Saver (Session Notes)

9Router is a local AI proxy/router that sits between your AI tools and 40+ providers.
Free, auto-fallback, token compression (RTK), multi-account round-robin.

## Quick Install & Run

```bash
npm install -g 9router          # Install
9router                         # Start — opens dashboard at http://localhost:20128
```

## Dashboard

- URL: `http://localhost:20128`
- Next.js 16 SPA, SQLite backend at `~/.9router/db/data.sqlite`
- Requires login (register from browser dashboard)
- Shows API key after login — copy this key for Hermes config

## CLI Options

```
Options:
  -p, --port <port>   Port (default: 20128)
  -H, --host <host>   Host (default: 0.0.0.0)
  -n, --no-browser    Don't open browser
  -l, --log           Show logs
  -t, --tray          System tray mode (background)
  --skip-update       Skip auto-update check
```

## Hermes Integration

### Main Provider Config

```bash
# Step 1: Configure Hermes
hermes config set model.provider custom
hermes config set model.base_url http://localhost:20128/v1
hermes config set model.default ds/deepseek-v4-flash

# Step 2: API key in .env (NOT in config.yaml!)
echo 'OPENAI_API_KEY=<9router-api-key>' >> ~/.hermes/.env

# Step 3: Remove api_key from config.yaml if accidentally set
sed -i '/^  api_key:/d' ~/.hermes/config.yaml

# Step 4: Register in custom_providers (optional)
# Edit ~/.hermes/config.yaml and add:
# custom_providers:
#   - name: 9router
#     base_url: http://localhost:20128/v1
#     api_mode: chat_completions
#     models:
#       ds/deepseek-v4-flash: {}
#       ds/deepseek-v4-pro: {}
#       ds/deepseek-chat: {}
#       minimax/MiniMax-M2.7: {}
```

### Starting Server (Background)

```bash
# Run in background
nohup 9router -l --skip-update > /tmp/9router.log 2>&1 &

# Or with systemd user service (for persistence)
```

### Model Naming

9Router uses vendor-prefixed model slugs:
- `ds/deepseek-v4-flash` — DeepSeek V4 Flash
- `ds/deepseek-v4-pro` — DeepSeek V4 Pro
- `ds/deepseek-chat` — DeepSeek Chat
- `ds/deepseek-reasoner` — DeepSeek Reasoner
- `minimax/MiniMax-M2.7` — MiniMax M2.7 (has reasoning output)
- `minimax/MiniMax-M2.5` — MiniMax M2.5
- `minimax/MiniMax-M2.1` — MiniMax M2.1

These vendor-prefixed slugs work correctly with `provider: custom` in Hermes.

## Updating 9Router

```bash
# Check versions
~/.hermes/node/bin/9router --version          # installed
npm view 9router version                        # latest

# Must set prefix to avoid EACCES on system global
~/.hermes/node/bin/npm config set prefix ~/.hermes/node

# Update
~/.hermes/node/bin/npm update -g 9router

# After update: check symlink (npm can change the target)
ls -la ~/.hermes/node/bin/9router

# Fix if broken
ln -sf ~/.hermes/node/lib/node_modules/9router/cli.js ~/.hermes/node/bin/9router

# Stop, start fresh
kill $(pgrep -f "9router") 2>/dev/null
9router --host 0.0.0.0 --port 20128 --no-browser --log --skip-update
```

### Upgrade Side Effects

- v0.4.63 → v0.4.66: SQLite schema may change. Backup is created at `~/.9router/db/backups/upgrade-*/`
- After upgrade, the new process may use a different DB format that `sqlite3 .dump` can't read directly
- API keys are stored **masked** in the database — 9Router encrypts/obfuscates them. Don't rely on `strings` or direct SQLite queries to extract keys.
- Service needs restart after update if managed via systemd

## Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| Server dies on first request | Process killed by OOM or port conflict | Restart; verify port free with `lsof -i:20128` |
| `curl: (7) Failed to connect` | Server not ready yet | Wait 3-5 seconds after startup |
| Empty page in browser | SPA needs JavaScript | Ensure browser has JS enabled |
| API returns `Unauthorized` | Missing or wrong API key | Check key from dashboard |
| `[402] insufficient balance` | MiniMax API key has run out of credits | Update MiniMax key in dashboard, or use a different provider key |
| Can't login to dashboard | API key mismatch or lockout | Wait for lockout to expire (30-120s), or reset via Settings in browser UI |

## MiniMax-M2.7 via 9Router

MiniMax-M2.7 works through 9Router on VPS. It has reasoning output (shows `<think>` tags with chain-of-thought before the final answer). Known behaviors:

- **VPS:** Works reliably with proper MiniMax API key (tested: response OK)
- **Local:** Error 402 `insufficient balance` if the MiniMax API key has run out of credits
- **Latency:** Can be slower than DeepSeek (3-49s per call reported)
- The key stored in 9Router's database is obfuscated — updating it requires the dashboard UI

## Systemd Service (VPS Persistence)

9Router on VPS runs via systemd user service at `~/.config/systemd/user/9router.service`.

### Checking Status

```bash
systemctl --user status 9router.service    # Status + recent logs
systemctl --user is-active 9router.service  # active/inactive/failed
journalctl --user -u 9router.service -n 40 # Full journal logs
```

### Service File

Standard service file:

```ini
[Unit]
Description=9router server
After=network.target

[Service]
Type=simple
ExecStart=/home/ubuntu/.hermes/node/bin/9router --host 0.0.0.0 --port 20128 --no-browser --log --skip-update
Restart=always
RestartSec=5
Environment=PATH=/home/ubuntu/.hermes/node/bin:/usr/local/bin:/usr/bin:/bin
WorkingDirectory=/home/ubuntu

[Install]
WantedBy=default.target
```

### Exit Code 203/EXEC — Symlink Broken

9Router is a Node.js CLI (`cli.js`). The binary at `~/.hermes/node/bin/9router` is a **symlink** to the actual module. If Node.js is reinstalled or modules are moved, the symlink breaks and systemd fails with `status=203/EXEC`.

**Symptoms:**
- `systemctl --user status` shows `status=203/EXEC`, restart counter climbing
- No log output from 9Router itself (it never ran)

**Diagnosis:**
```bash
# Check the symlink target
ls -la ~/.hermes/node/bin/9router
# Output: ~/.hermes/node/bin/9router -> /usr/local/lib/node_modules/9router/cli.js
# If that path doesn't exist, it's broken

# Find where 9router module actually lives
find ~/.hermes/node/lib -name "9router" -type d
# Expected: ~/.hermes/node/lib/node_modules/9router/

# Check system npm too
npm root -g
ls -la $(npm root -g) | grep 9router
```

**Fix:**
```bash
ln -sf ~/.hermes/node/lib/node_modules/9router/cli.js ~/.hermes/node/bin/9router
systemctl --user restart 9router.service
```

After fix, verify:
```bash
systemctl --user is-active 9router.service  # Should say "active"
ss -tlnp | grep 20128                        # Should show listener
curl -s http://localhost:20128/v1/models -m 5 | head -10  # Should return JSON
```

### Common systemd-related pitfalls
- On VPS, **systemd user services survive logout** via `loginctl enable-linger` — already set
- If service keeps restarting rapidly (restart counter 200+), stop it first with `systemctl --user stop 9router.service`, fix the symlink, then `systemctl --user start 9router.service`
- `Restart=always` will keep trying forever — don't leave a broken config unattended (can DOS your own server with restart spam)
