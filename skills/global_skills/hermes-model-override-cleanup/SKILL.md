---
name: hermes-model-override-cleanup
description: >-
  Diagnose and fix stuck model overrides in Hermes multi-profile deployments.
  Covers the dual-location issue where model overrides persist in both sessions.json
  AND state.db gateway_routing table, causing bots to report wrong models despite
  correct config.yaml. Also covers TELEGRAM_ALLOWED_USERS access control for
  multi-role bot access (all users chat, only supermasters approve).
category: devops
triggers:
  - bot reports wrong model despite correct config
  - model stuck on old value after config change
  - model_override persists after restart
  - bot says "I'm using X" but config says Y
  - Telegram bot model mismatch
  - bot doesn't respond to certain users
  - TELEGRAM_ALLOWED_USERS configuration
  - user access control for Telegram bots
---

# Hermes Model Override Cleanup

Fix stuck model overrides in Hermes multi-profile deployments. This is a common issue where the bot reports a different model than what's configured in `config.yaml`.

## When to Use

- Bot Telegram reports model X but config.yaml says model Y
- Config change didn't take effect after restart
- Model appears "stuck" on an old value
- User asks "what model are you using?" and bot gives wrong answer

## Root Cause: Dual-Location Storage

Model overrides are stored in **TWO places**:

### Location 1: `sessions.json` (file mirror)
```
~/.hermes/profiles/<profile>/sessions/sessions.json
```
Contains per-chat `model_override` entries in the session routing data.

### Location 2: `state.db` gateway_routing table (PRIMARY source)
```
~/.hermes/profiles/<profile>/state.db
```
Table: `gateway_routing`, column: `entry_json` (JSON with `model_override` field).

**Critical:** Gateway reads from `state.db` as the primary source. Clearing only `sessions.json` will NOT fix the issue — the database override persists and gets reloaded on restart.

## Diagnosis

### Check sessions.json
```python
import json
with open('/home/ubuntu/.hermes/profiles/<profile>/sessions/sessions.json') as f:
    data = json.load(f)
for k, v in data.items():
    if isinstance(v, dict) and 'model_override' in v:
        print(f"FOUND: {v.get('display_name', k)} -> {v['model_override']}")
```

### Check state.db gateway_routing
```python
import sqlite3, json
conn = sqlite3.connect('/home/ubuntu/.hermes/profiles/<profile>/state.db')
cur = conn.cursor()
cur.execute('SELECT session_key, entry_json FROM gateway_routing')
for row in cur.fetchall():
    entry = json.loads(row[1])
    if 'model_override' in entry:
        print(f"FOUND: {row[0]} -> {entry['model_override']}")
```

## Fix Procedure (MUST follow this exact order)

### Step 1: STOP gateway process FIRST
```bash
pkill -f 'hermes_cli.main --profile <profile>'
sleep 3
```

**Why:** If gateway is running, it holds the old model in memory and may overwrite your database changes on shutdown.

### Step 2: Clear model_override from state.db
```python
import sqlite3, json

db_path = '/home/ubuntu/.hermes/profiles/<profile>/state.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute('SELECT session_key, entry_json FROM gateway_routing')
for row in cur.fetchall():
    entry = json.loads(row[1])
    if 'model_override' in entry:
        print(f"Clearing: {row[0]}")
        del entry['model_override']
        cur.execute('UPDATE gateway_routing SET entry_json = ? WHERE session_key = ?',
                    (json.dumps(entry), row[0]))

conn.commit()
conn.close()
```

### Step 3: Clear model_override from sessions.json
```python
import json

path = '/home/ubuntu/.hermes/profiles/<profile>/sessions/sessions.json'
with open(path) as f:
    data = json.load(f)

for key, val in data.items():
    if isinstance(val, dict) and 'model_override' in val:
        del val['model_override']

with open(path, 'w') as f:
    json.dump(data, f, indent=2)
```

### Step 4: RESTART gateway
```bash
systemctl --user restart hermes-gateway.service
```

### Step 5: Verify
```python
import sqlite3, json
db = sqlite3.connect('/home/ubuntu/.hermes/profiles/<profile>/state.db')
cur = db.cursor()
cur.execute('SELECT session_key, entry_json FROM gateway_routing')
for row in cur.fetchall():
    entry = json.loads(row[1])
    name = entry.get('display_name', row[0])
    if 'model_override' in entry:
        print(f"STILL HAS OVERRIDE: {name}")
    else:
        print(f"OK: {name}")
```

## Sync custom_providers Across Profiles

When ensuring all profiles use the same custom provider (e.g., 9Router), use Python yaml.safe_load + yaml.dump (NOT sed):

```python
import yaml, os, glob

ref_providers = [
    'minimax/MiniMax-M3', 'minimax/MiniMax-M2.7', 'minimax/MiniMax-M2.5',
    'xai/grok-4', 'groq/llama-3.3-70b-versatile', 'cerebras/gpt-oss-120b',
    'ag/gemini-3-flash-agent', 'ag/gemini-3.5-flash-low', 'ag/gemini-3-flash',
    'mimo/mimo-v2.5-pro', 'mimo/mimo-v2.5',
    # ... full list from hermes-support reference
]

profiles_dir = os.path.expanduser('~/.hermes/profiles')
for profile_dir in sorted(glob.glob(os.path.join(profiles_dir, '*'))):
    if not os.path.isdir(profile_dir):
        continue
    name = os.path.basename(profile_dir)
    config_path = os.path.join(profile_dir, 'config.yaml')
    
    if not os.path.exists(config_path):
        continue
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f) or {}
    
    cp = config.get('custom_providers', [])
    ninerouter = None
    for p in cp:
        if isinstance(p, dict) and p.get('name') == '9router':
            ninerouter = p
            break
    
    if ninerouter is None:
        ninerouter = {
            'name': '9router',
            'base_url': 'http://localhost:20128/v1',
            'discover_models': True,
            'models': ref_providers
        }
        cp.append(ninerouter)
        config['custom_providers'] = cp
    else:
        ninerouter['base_url'] = 'http://localhost:20128/v1'
        ninerouter['discover_models'] = True
        ninerouter['models'] = ref_providers
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"Updated: {name}")
```

**Key settings for each profile:**
- `provider: custom` in model section
- `base_url: http://localhost:20128/v1` in model section
- `custom_providers` with `name: 9router`, `discover_models: true`, full models list

## Root Cause: 4-Location Storage (Updated)

Model overrides are stored in **FOUR places**:

### Location 1: `sessions.json` (file mirror)
```
~/.hermes/profiles/<profile>/sessions/sessions.json
```
Contains per-chat `model_override` entries in the session routing data.

### Location 2: `state.db` gateway_routing table (PRIMARY source for routing)
```
~/.hermes/profiles/<profile>/state.db
```
Table: `gateway_routing`, column: `entry_json` (JSON with `model_override` field).

### Location 3: `state.db` sessions table (session-level model/provider)
```
~/.hermes/profiles/<profile>/state.db
```
Table: `sessions`, columns: `model`, `billing_provider`, `billing_base_url`.
This stores the model/provider used for each session. Must also be updated!

### Location 4: `config.yaml` (default model)
```
~/.hermes/profiles/<profile>/config.yaml
```
Section: `model.default`, `model.provider`, `model.base_url`.

**Critical:** Gateway reads from `state.db` as the primary source. Clearing only `sessions.json` will NOT fix the issue — the database override persists and gets reloaded on restart.

## CRITICAL: custom_providers.name MUST be "9router"

When user changes model via `/model` command in Telegram, Hermes stores the provider as `custom:<name>` where `<name>` comes from `custom_providers[0].name` in config.yaml.

**If name is "custom"** → provider stored as `custom:custom` (BUG!) → 429 errors
**If name is "9router"** → provider stored as `custom:9router` (CORRECT) → works

**Always verify:** `custom_providers[0].name` must be `"9router"`, not `"custom"`.

```python
# Check and fix custom_providers name
import yaml
config_path = '/home/ubuntu/.hermes/profiles/<profile>/config.yaml'
with open(config_path) as f:
    config = yaml.safe_load(f) or {}
cp = config.get('custom_providers', [])
if cp and cp[0].get('name') != '9router':
    print("BUG FOUND: name is '%s', must be '9router'" % cp[0].get('name'))
    cp[0]['name'] = '9router'
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print("FIXED")
```

## Stuck Session (No Assistant Response)

When a bot receives messages but never responds (all user messages, zero assistant messages), the session is stuck. This causes the bot to appear "dead" — messages arrive but no reply comes.

### Diagnosis
```python
import sqlite3
conn = sqlite3.connect('/home/ubuntu/.hermes/profiles/<profile>/state.db')
cur = conn.cursor()
cur.execute('SELECT role, content FROM messages WHERE session_id = "<session_id>" ORDER BY rowid')
for row in cur.fetchall():
    print(f"{row[0]}: {row[1][:80] if row[1] else '(empty)'}")
# If ALL messages are "user" with 0 "assistant" → session is stuck
```

### Fix
```python
import sqlite3, json

# 1. Stop gateway first
# systemctl --user stop hermes-gateway-<profile>.service

# 2. Delete stuck messages + session from state.db
conn = sqlite3.connect('/home/ubuntu/.hermes/profiles/<profile>/state.db')
cur = conn.cursor()
cur.execute('DELETE FROM messages WHERE session_id = "<session_id>"')
cur.execute('DELETE FROM sessions WHERE id = "<session_id>"')
conn.commit()
conn.close()

# 3. Remove from sessions.json
path = '/home/ubuntu/.hermes/profiles/<profile>/sessions/sessions.json'
with open(path) as f:
    data = json.load(f)
key_to_remove = None
for k, v in data.items():
    if isinstance(v, dict) and v.get('session_id') == '<session_id>':
        key_to_remove = k
        break
if key_to_remove:
    del data[key_to_remove]
with open(path, 'w') as f:
    json.dump(data, f, indent=2)

# 4. Restart gateway — new session auto-created on next user message
```

## Pitfalls

1. **Clearing only sessions.json doesn't work** — state.db gateway_routing is the primary source
2. **Gateway must be stopped BEFORE updating state.db** — otherwise mem-cache overwrites changes and regenerates files
3. **yaml.dump reorders keys** — use `sort_keys=False` to preserve original order
4. **sed is unsafe for YAML blocks** — use Python yaml module for custom_providers sections
5. **`discover_models: true` is required** — without it, model list won't populate in Telegram /model command
6. **Check ALL 4 locations when diagnosing** — sessions.json, state.db gateway_routing, state.db sessions table, AND custom_providers name
7. **custom_providers.name MUST be "9router"** — if it's "custom", /model stores provider as "custom:custom" causing 429 errors
8. **Billing_provider in sessions table must also be updated** — not just gateway_routing
9. **Gateway regenerates sessions.json from memory on restart** — must stop gateway FIRST, then clear ALL locations, then restart
10. **Stuck session = all user messages, zero assistant** — bot receives messages but never replies; delete stuck session from state.db messages + sessions tables and sessions.json
11. **`systemctl --user restart hermes-gateway.service` only restarts default profile** — per-profile services are `hermes-gateway-<name>.service` and need separate `start`/`stop`
12. **After clearing overrides, always verify state.db sessions table** — the `billing_provider` column may still have old value like `custom` instead of `custom:9router`

## Verification Checklist

After fix, verify:
- [ ] `state.db` gateway_routing has no model_override entries
- [ ] `sessions.json` has no model_override entries
- [ ] `state.db` sessions table has correct billing_provider (custom:9router)
- [ ] `custom_providers[0].name` is "9router" (not "custom")
- [ ] Gateway process is running with fresh start
- [ ] Bot reports correct model when asked "kamu pakai model apa"
- [ ] All profiles have consistent custom_providers configuration
- [ ] TELEGRAM_ALLOWED_USERS is commented out (except ais)
- [ ] 9Router is responding (curl http://127.0.0.1:20128/v1/models)

## Referensi
- `references/supermaster-access-control.md`: konfigurasi akses supermaster untuk multi-role access.
- `references/9router-model-list.md`: daftar model 9Router dan verifikasi konfigurasi.
