---
name: hermes-provider-management
description: >-
  Configure, operate, and sync Hermes providers (custom OpenAI-compatible endpoints,
  9Router proxy) across local and VPS multi-profile infrastructure. Covers setup,
  diagnostics, updates, multi-profile sync, API key management, and YAML editing.
category: devops
triggers:
  - set up custom provider / proxy / endpoint for Hermes
  - 9router rusak / mati / error / update
  - sync provider/model config across all profiles
  - ubah provider ke deepseek / minimax / custom
  - gateway service restart after config change
  - YAML corruption recovery in Hermes configs
  - add provider to 9Router on VPS
---

# Hermes Provider Management

Umbrella skill for managing Hermes providers — configuring custom endpoints, operating the 9Router proxy, syncing config across multi-profile infrastructure, and troubleshooting.

## 1. Custom Provider Setup (Generic)

Configure any OpenAI-compatible endpoint (9Router, Ollama, vLLM, LM Studio, LiteLLM, LocalAI, private aggregator) as Hermes' main inference provider.

### Step 1 — Verify the Endpoint

```bash
curl -s <endpoint>/v1/models -H "Authorization: Bearer <api_key>" | head -20
```

Expected: JSON with a `data` array of model objects.

### Step 2 — Configure Provider as `custom`

```bash
hermes config set model.provider custom
hermes config set model.base_url <endpoint>   # e.g. http://localhost:20128/v1
hermes config set model.default <model_id>    # e.g. ds/deepseek-v4-flash
```

**⚠️ CRITICAL:** Provider MUST be `custom`. Do NOT use `openai` — Hermes rejects `provider: openai` as unknown.

### Step 3 — API Key in `.env` (NOT in `config.yaml`)

```bash
echo 'OPENAI_API_KEY=<your-api-key>' >> ~/.hermes/.env
```

**Two pitfalls:**
1. **`api_key` in config.yaml overrides `.env`.** An empty `api_key: ''` causes silent auth failure (empty key sent). Remove it:
   ```bash
   sed -i '/^  api_key:/d' ~/.hermes/config.yaml
   ```
2. **`OPENAI_API_KEY` is the env var Hermes reads** for `provider: custom`. Other names (`CUSTOM_API_KEY`, etc.) are NOT picked up.

### Step 4 — Register in `custom_providers` (Optional)

Enables model listing in `hermes model` and `hermes doctor`:

```yaml
custom_providers:
  - name: <friendly-name>         # e.g. 9router, local-ollama
    base_url: <endpoint>
    api_mode: chat_completions
    models:
      <model-1>: {}
      <model-2>: {}
```

Vendor-prefixed slugs (`ds/deepseek-v4-flash`, `minimax/MiniMax-M2.7`) work correctly with `provider: custom`.

**⚠️ CRITICAL — OpenRouter intercepts vendor-prefixed models:** When `OPENROUTER_API_KEY` is set in `.env`, Hermes internally routes models with vendor prefixes like `ds/` to OpenRouter, **completely ignoring** `model.base_url` and `model.provider: custom`. The request goes to `https://openrouter.ai/api/v1` instead of your custom endpoint.

Workarounds:
- **Remove `OPENROUTER_API_KEY`** from the profile's `.env` if OpenRouter is not needed for that profile.
- **Use a model slug without a vendor prefix** that OpenRouter doesn't recognize (e.g. `minimax/MiniMax-M2.7` instead of `ds/deepseek-v4-flash`).
- **Use a model slug that's not routed by Hermes** — only `ds/` prefix is known to trigger this; `minimax/` does not.

To verify which endpoint Hermes is actually sending to, check the request dump files:
```bash
ls -t ~/.hermes/profiles/<profile>/sessions/request_dump_*.json | head -1
python3 -c "import json; d=json.load(open('...')); print(d['request']['url'])"
```

### Step 5 — Verify

```bash
hermes doctor | grep -A 5 "Model"
hermes chat -q "test: balas ok saja" -v
```

---

## 2. 9Router Proxy Operations

9Router is the proxy OpenAI-compatible endpoint used as the main Hermes provider. Each host (WSL, VPS) can run its own instance on **port 20128**. The recommended architecture is a **single VPS instance** shared by all profiles.

### Quick Status Check

```bash
# Port listener
ss -tlnp | grep 20128

# Process
ps aux | grep 9router | grep -v grep

# Systemd (VPS)
systemctl --user is-active 9router.service
systemctl --user status 9router.service | head -15

# API test
curl -s -o /dev/null -w "HTTP %{http_code} | %{time_total}s" http://localhost:20128/v1/models -m 5

# Models
curl -s http://localhost:20128/v1/models -m 5 | python3 -c "
import sys,json
d=json.load(sys.stdin)
for m in d.get('data',[]):
    print(f'  - {m[\"id\"]}')
"
```

### Dashboard

| Location | URL |
|----------|-----|
| Local (WSL) | `http://localhost:20128/` |
| VPS (public) | `http://<vps-ip>:20128/` |

Login requires the API key from config.

### Fix: Broken Symlink (exit code 203/EXEC)

**Symptom:** systemd loop restart, `status=203/EXEC`, restart counter climbing, no 9Router log output.

**Cause:** The symlink at `~/.hermes/node/bin/9router` points to a non-existent path.

**Fix:**
```bash
# Find the actual module
find ~/.hermes/node/lib -name "9router" -type d
# Expected: ~/.hermes/node/lib/node_modules/9router/

# Fix symlink
ln -sf ~/.hermes/node/lib/node_modules/9router/cli.js ~/.hermes/node/bin/9router

# Verify
~/.hermes/node/bin/9router --version
systemctl --user restart 9router.service
```

### Update 9Router

```bash
# Set correct npm prefix (prevents EACCES)
~/.hermes/node/bin/npm config set prefix ~/.hermes/node

# Update
~/.hermes/node/bin/npm update -g 9router

# After update: check symlink
ls -la ~/.hermes/node/bin/9router

# Verify version
~/.hermes/node/bin/9router --version
```

**⚠️ Upgrade side effects:**
- Storage backend differs by version: v0.4.63 and below use **SQLite** (`~/.9router/db/data.sqlite`), v0.4.66+ use **`db.json`**. Do not confuse files across versions.
- Upgrade creates a backup at `~/.9router/db/backups/upgrade-*/`.
- API keys are stored **masked** in the database — do not rely on `strings` or direct SQLite queries to extract them.

### Manual Start (WSL — no systemd)

```bash
export PATH="/home/ndisap/.hermes/node/bin:$PATH"
nohup 9router --host 0.0.0.0 --port 20128 --no-browser --log --skip-update > /tmp/9router.log 2>&1 &
```

### VPS Systemd Service

Service file at `~/.config/systemd/user/9router.service`:

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

### Single-Instance Architecture (Recommended)

Run one 9Router on VPS-Zeus, point all profiles (local WSL, VPS default, all Telegram bots) to it:

```
WSL (local) ──http://<vps-ip>:20128/v1──┐
VPS default ──http://localhost:20128/v1──┤
hermes-support ──localhost:20128/v1──────┤──→ 9Router (VPS)
profil-admin-mvp ──localhost:20128/v1────┤
...other profiles────────────────────────┘
```

Migration: kill local 9Router, update Hermes `model.base_url` to VPS IP, copy VPS 9Router API key to every profile's `.env` as `OPENAI_API_KEY`.

---

## 3. Multi-Profile Sync Procedure

After any provider/model config change, sync across all profiles and restart gateways.

### Step 1 — Identify All Affected Profiles

**Local:** `~/.hermes/config.yaml` (default profile)

**VPS profiles** (via SSH):
```
~/.hermes/profiles/hermes-support/
~/.hermes/profiles/profil-admin-mvp/
~/.hermes/profiles/profil-admin-node-b/
~/.hermes/profiles/profil-admin-olo/
~/.hermes/profiles/profil-admin-plus/
```

**Don't forget** the VPS default profile (`~/.hermes/config.yaml` on VPS).

### Step 2 — Check API Key Availability

| Provider | API Key Env Var | Availability |
|----------|----------------|-------------|
| `deepseek` | `DEEPSEEK_API_KEY` | All profiles |
| `minimax` | `MINIMAX_API_KEY` | hermes-support + local + (tentative) profil-admin-mvp |
| `custom` (9Router proxy) | `OPENAI_API_KEY` | All profiles |
| `openrouter` | `OPENROUTER_API_KEY` | **PERMANENTLY FORBIDDEN** — never use |

### Step 3 — Set Config on Local First

```bash
hermes config set model.provider <provider>
hermes config set model.default <model>
hermes config | grep -E '^model:|^  provider:|^  default:'
```

### Step 4 — Sync to All VPS Profiles

**Via SSH with full binary path** (bare `hermes` NOT in PATH in non-interactive SSH):

```bash
ssh ubuntu@<vps-ip>
HERMES=~/.hermes/hermes-agent/venv/bin/hermes
for p in hermes-support profil-admin-mvp profil-admin-node-b profil-admin-olo profil-admin-plus; do
  echo "=== $p ==="
  $HERMES --profile $p config set model.provider <provider>
  $HERMES --profile $p config set model.default <model>
done
```

**⚠️ CRITICAL:** Always use `--profile NAME` flag. Running `cd ~/.hermes/profiles/<name> && hermes config set ...` writes to the **currently active profile**, not the one you cd'd into.

**For custom provider sync**, every profile additionally needs:
```bash
# Remove stale api_key: '' from config.yaml
for p in hermes-support profil-admin-mvp profil-admin-node-b profil-admin-olo profil-admin-plus; do
  sed -i '/^  api_key:/d' ~/.hermes/profiles/$p/config.yaml
done

# Add OPENAI_API_KEY to each .env
for p in hermes-support profil-admin-mvp profil-admin-node-b profil-admin-olo profil-admin-plus; do
  ENV=~/.hermes/profiles/$p/.env
  grep -q OPENAI_API_KEY $ENV 2>/dev/null || \
    echo -e "\n# 9Router proxy\nOPENAI_API_KEY=$VPS_9R_KEY" >> $ENV
done

# Add custom_providers section (YAML block — use Python yaml.dump, NOT sed)
# See Section 5 (YAML Editing) for the safe approach
```

### Step 5 — Restart All Gateways

```bash
ssh ubuntu@<vps-ip> "systemctl --user restart \
  hermes-gateway-hermes-support.service \
  hermes-gateway-profil-admin-mvp.service \
  hermes-gateway-profil-admin-node-b.service \
  hermes-gateway-profil-admin-olo.service \
  hermes-gateway-profil-admin-plus.service"
```

Wait ~15s, then verify:

```bash
ssh ubuntu@<vps-ip> "systemctl --user status hermes-gateway-hermes-support.service | head -10"
```

### Step 6 — Check for Error Residue

```bash
ssh ubuntu@<vps-ip> "journalctl --user -u hermes-gateway-hermes-support.service --since '1 minute ago' | grep -iE 'error|failed|warning' | grep -v 'Shutdown\|SIGTERM' | tail -10"
```

---

## 4. Provider Matrix & Known Configurations

### Provider Matrix (What Works Where)

| Profile | deepseek | custom (9Router) | minimax | Current Active |
|---------|----------|-----------------|---------|----------------|
| hermes-support | ✅ | ✅ | ✅ | 9Router → minimax/MiniMax-M2.7 |
| profil-admin-mvp | ✅ | ✅ | ✅ | 9Router → minimax/MiniMax-M2.7 |
| profil-admin-node-b | ✅ | ✅ | ❌ | 9Router → minimax/MiniMax-M2.7 |
| profil-admin-olo | ✅ | ✅ | ❌ | 9Router → minimax/MiniMax-M2.7 |
| profil-admin-plus | ✅ | ✅ | ❌ | 9Router → minimax/MiniMax-M2.7 |
| Local | ✅ | ✅ | ✅ | 9Router → minimax/MiniMax-M2.7 |

**Rule:** For cross-profile sync, `deepseek`/`deepseek-v4-flash` works everywhere. `minimax` works only in profiles with `MINIMAX_API_KEY`.

### 9Router VPS Provider Configurations (db.json)

Each provider in `~/.9router/db.json`:

| Provider | `provider` field | `baseUrl` | Auth |
|----------|-----------------|-----------|------|
| DeepSeek | `deepseek` | `https://api.deepseek.com/v1` | apikey |
| MiniMax | `minimax` | `https://api.minimax.io/v1` | apikey |
| Codex (GitHub Copilot) | `codex` | — | oauth |
| OpenRouter | `openrouter` | — | apikey |

### Adding a Provider to 9Router on VPS

1. SSH into VPS
2. Edit `~/.9router/db.json` — use Python `json` module, never `sed` on JSON
3. Add connection entry with UUID, provider key, `authType`, `name`, `apiKey`, optional `baseUrl`
4. Optionally add model nodes under `providerNodes`
5. Restart 9Router: `pkill -f 9router; nohup ~/.hermes/node/bin/9router --host 0.0.0.0 --port 20128 --no-browser --log --skip-update > /tmp/9router.log 2>&1 &`
6. Verify: `curl -s http://localhost:20128/v1/models | python3 -m json.tool | head -20`

### MiniMax API Key Format Validation

MiniMax API keys have a specific format. Wrong format = silent HTTP 401.

**❌ Wrong patterns:**
- Base64-encoded strings (starting with `c2st`)
- `sk-cp-...` prefix (OpenCode/reverse-proxy key format)
- `sk-api-...` prefix (OpenAI-style — rejected by MiniMax)

**✅ Correct:** Raw ASCII, MiniMax-specific format, obtained from https://platform.minimax.io

**Detection:**
```bash
# Decode if base64
echo "c2stY3At..." | base64 -d
# → sk-cp-... → NOT a MiniMax key

# Test API key directly
curl -s -o /dev/null -w "%{http_code}" \
  https://api.minimax.io/v1/models \
  -H "Authorization: Bearer $MINIMAX_API_KEY"
# Returns 401 → wrong format or expired
```

### Auxiliary Title Generation

When title generation fails (auto routing blocked):

**Option A — Explicit provider:**
```bash
hermes config set auxiliary.title_generation.provider deepseek
hermes config set auxiliary.title_generation.model deepseek-v4-flash
```

**Option B — Disable:**
```bash
hermes config set auxiliary.title_generation.provider ''
```

User prefers Option A when deepseek is the primary provider.

---

## 5. YAML Editing Best Practices

### Safe Editing Guide

| Change type | Tool | Reason |
|-------------|------|--------|
| Single scalar (`model.provider`, `model.base_url`) | `hermes config set KEY VAL` | Handles YAML correctly, validates |
| Single-line removal (`api_key: ''`) | `sed -i '/^  api_key:/d' config.yaml` | Simple, reliable for unambiguous patterns |
| Multi-line YAML block (custom_providers, plugins) | Python `yaml.safe_load` + `yaml.dump` | `sed` address ranges corrupt YAML structure |
| Bulk same edit across N profiles | Loop `hermes config set --profile $p` for scalars; Python for blocks | Mixed approach |

### Python Safe-Write Recipe

```python
import yaml

path = '/path/to/config.yaml'
with open(path) as f:
    cfg = yaml.safe_load(f)

# Modify cfg dict in place...

with open(path, 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, sort_keys=False,
              allow_unicode=True, width=200)
```

**Critical flags:** `default_flow_style=False` (block format, not inline JSON-style), `sort_keys=False` (preserve field order), `width=200` (prevent long-string wrapping).

### `sed` Traps

- **Line joining:** `sed` address ranges with `a` (append) can write new content on the same line as the target when newlines aren't explicit enough → corrupts multi-line YAML blocks
- **YAML anchors:** `sed` cannot handle anchors (`&anchor`) or aliases (`*anchor`) — treats them as plain text
- **Always backup first:** `cp config.yaml config.yaml.bak.$(date +%Y%m%d_%H%M%S)`

### YAML Corruption Recovery

Symptom: `yaml.scanner.ScannerError: mapping values are not allowed here`

Recovery:
1. Restore from backup: `cp ~/backup-hermes-vps-<timestamp>/<profile>-config.yaml ~/.hermes/profiles/<profile>/config.yaml`
2. Re-apply intended changes using correct method per table above
3. Verify: `python3 -c "import yaml; yaml.safe_load(open('config.yaml')); print('valid')"`
4. Restart gateway services

---

## 6. Troubleshooting

### Quick Diagnostic (Endpoint Down)

```bash
# 1. Check port
ss -tlnp | grep 20128 || echo "NOT LISTENING"

# 2. Systemd status (if managed)
systemctl --user status 9router.service | head -10

# 3. HTTP test
curl -s -o /dev/null -w "HTTP %{http_code} | %{time_total}s" http://localhost:20128/v1/models -m 5

# 4. Process check
ps aux | grep -E "9router|node.*20128" | grep -v grep

# 5. VPS vs Local — each host runs its own 9Router instance
curl -s http://localhost:20128/v1/models -m 5 | head -5
ssh ubuntu@<vps-ip> 'curl -s http://localhost:20128/v1/models -m 5 | head -5'
```

### Common Error Table

| Error | Cause | Fix |
|-------|-------|-----|
| `Unknown provider 'openai'` | Set `provider: openai` instead of `custom` | `hermes config set model.provider custom` |
| API calls hang / auth errors | `api_key: ''` in config.yaml overrides `.env` | `sed -i '/^  api_key:/d' config.yaml` |
| API key not found | Key in wrong env var | Must be `OPENAI_API_KEY` in `.env` |
| `status=203/EXEC` — crashes immediately | Broken symlink to Node.js CLI | `ln -sf <actual-cli.js> ~/.hermes/node/bin/<tool>` then restart |
| `HTTP 000` / connection refused | 9Router not running | Check port, systemd, symlinks |
| `HTTP 404: No endpoints available (guardrail)` | `auto` routing blocked | Set auxiliary provider explicitly |
| `Provider 'minimax' set but no API key found` | Profile lacks `MINIMAX_API_KEY` | Switch to `deepseek` |
| Service restarted but error persists | Old config cached in memory | Kill old PID, restart clean |
| `HTTP 500: unknown error, 999 (1000) — MiniMax-M3` | MiniMax deprecated M3 model | Rollback to MiniMax-M2.7 or MiniMax-M2.5 |
| Model routed to OpenRouter despite `provider: custom` + `base_url` set | `OPENROUTER_API_KEY` in `.env` causes Hermes to intercept vendor-prefixed models (`ds/`) | Remove `OPENROUTER_API_KEY`, use non-prefixed model slug, or check via request_dump |
| Config changes not reflected in Telegram | Service not restarted | `systemctl --user restart hermes-gateway-<profile>.service` |

---

## 7. Profile State Recovery

Use when restoring, inspecting, migrating, or recovering Hermes behavior from another machine/profile after reinstall, VPS migration, Telegram bot move, or profile reset.

### Scope (recover only)
- `SOUL.md` persona and policy text.
- `memories/MEMORY.md` and `memories/USER.md` durable preferences.
- Custom agent-created skills that encode policies/runbooks.
- Session-history snippets with explicit user rules.
- Profile inventory and active profile markers.

### Do NOT copy or display
- `.env`, `auth.json`, provider credentials, OAuth tokens, Telegram bot tokens, passwords, API keys, private keys, cookies, sessions.
- Raw model/provider/LLM config (unless user explicitly asks for config migration; even then redact values).

### Recovery workflow

1. **Clarify source access** — remote (host/IP/SSH) or local (`HERMES_HOME` / `~/.hermes` and profiles).
2. **Connect and discover read-only** — locate Hermes home, check `active_profile`, `SOUL.md`, `memories/`, `profiles/*/SOUL.md`, `profiles/*/memories/`, `profiles/*/skills/`. Exclude `node_modules`, `venv`, `.git`, logs, caches, secrets.
3. **Extract profile/persona policy** — read root and profile `SOUL.md` files. Preserve exact policy text but redact identifiers.
4. **Extract durable memories** — read `memories/MEMORY.md` and `memories/USER.md`. Import only still-useful facts; skip stale task progress, old PRs, credentials.
5. **Search session history for explicit rules** — query `state.db` for terms: `ingat`, `aturan`, `peraturan`, `soul`, `persona`, `identitas`, `wajib`, `jangan`, `approval`, `approval`, `mode kerja`. Prefer explicit user statements over tool noise.
6. **Extract custom policy skills** — inspect agent-created or user-specific skills. Capture class-level reusable policies, not one-off task narratives.
7. **Write sanitized recovery report** — save local markdown listing source, profiles, recovered rules, SOUL excerpts, memory facts, relevant custom skills, and what was excluded. State that secrets/API/LLM settings were not copied.
8. **Apply only after explicit user approval** — updating local `SOUL.md`, profile `SOUL.md`, skills, or config changes active behavior. Save compact durable preferences to memory when clearly useful.

### SQLite query pattern (read-only)

```python
terms = ['ingat','aturan','peraturan','soul','persona','identitas','wajib','jangan','approval','approval','mode kerja']
for term in terms:
    cur.execute('''
      select m.id, m.session_id, m.role, substr(m.content,1,1200) content, s.title
      from messages m left join sessions s on s.id=m.session_id
      where lower(m.content) like ?
      order by m.id desc limit 12
    ''', ('%' + term.lower() + '%',))
```

### Pitfalls
- **Do not over-import memory** — environment details and temporary states become stale.
- **Do not harden transient failures** — record the setup fix only when broadly useful.
- **Do not apply active persona silently** — reading is safe; replacing `SOUL.md` changes behavior.
- **Do not leak credentials in summaries** — redact password/token/API-key patterns.
- **Profile scope matters** — root `~/.hermes` and `~/.hermes/profiles/<name>` have separate memories, skills, env, and SOUL files.

See `references/profile-state-recovery-zeus.md` for an example sanitized extraction report.

---

## 8. Auth Failure Fallback & User Notification

When an auth failure or API timeout occurs, follow the policy in `references/maintenance-fallback-notification.md`:

- Replace all technical error messages with: *"Sedang maintenance. Silakan coba beberapa saat lagi."*
- Never expose internals (stack traces, endpoints, credential hints) to users.
- Implement 1-3 internal retries before showing the message.
- Use the auth error diagnosis matrix to quickly root-cause provider errors without leaking secrets.

---

## 9. Identity Sync Operational Logging

When identity/persona/policy changes are applied across local/VPS/Telegram, record them in a markdown operational log:

- Default path: `~/.hermes/ops-logs/operational-log.md` (or profile-specific).
- Never display tokens, API keys, passwords, or secrets in the log.
- For 1-KESATUAN sync: model, provider, and base_url MUST match across all sides.
- API keys are NOT auto-synced — copy via Python subprocess + SCP script.
- See `references/identity-sync-operational-log.md` for full procedure and log format.
- See `references/local-vps-telegram-sync.md` for the complete sync procedure.
- Do NOT use `rsync --delete` on broad skill roots when syncing.

---

## References

- `references/9router-setup.md` — 9Router install, run, CLI options, MiniMax-M2.7 behavior, systemd service details
- `references/9router-provider-setup.md` — VPS db.json provider schema, adding providers to 9Router, API key redaction workarounds
- `references/provider-api-key-matrix.md` — which `.env` keys exist in which profile (audit-generated)
- `references/yaml-editing-pitfalls.md` — detailed sed vs Python YAML trade-offs, examples, corner cases
- `references/profile-state-recovery-zeus.md` — example sanitized extraction report from VPS-backed Hermes/Telegram recovery session
- `references/maintenance-fallback-notification.md` — auth error → user-friendly message policy and diagnosis matrix
- `references/identity-sync-operational-log.md` — identity/persona/policy change logging procedure
- `references/local-vps-telegram-sync.md` — full procedure for 1-KESATUAN sync across local/VPS/Telegram
