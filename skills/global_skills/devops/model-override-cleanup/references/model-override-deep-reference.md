# Model Override Locations — Deep Reference

## state.db Schema

### gateway_routing table
| Column | Type | Description |
|--------|------|-------------|
| scope | TEXT | Path to sessions dir |
| session_key | TEXT | `agent:main:telegram:dm:<user_id>` |
| entry_json | TEXT | JSON: session routing info + `model_override` |
| updated_at | REAL | Timestamp |

**entry_json structure:**
```json
{
  "session_key": "agent:main:telegram:dm:661471478",
  "session_id": "20260803_200448_313ba88c",
  "display_name": "andi saputra",
  "model_override": {
    "model": "ag/gemini-3-flash",
    "provider": "custom:custom",
    "base_url": "http://localhost:20128/v1"
  }
}
```

### sessions table
| Column | Type | Description |
|--------|------|-------------|
| id | TEXT | Session ID |
| model | TEXT | Model used for this session |
| billing_provider | TEXT | Provider name (e.g. `custom:9router`) |
| billing_base_url | TEXT | Base URL used |
| user_id | TEXT | Telegram user ID |

**Key:** Even after clearing `model_override`, the `sessions` table retains the old `model` and `billing_provider`. This controls what provider is used at runtime for that session.

## `custom:custom` vs `custom:9router`

The `provider` field in `model_override` uses format `custom:<name>` where `<name>` matches the `name` field in `custom_providers` list.

```yaml
custom_providers:
  - name: 9router    # ← this is the provider name
    base_url: http://localhost:20128/v1
```

So `provider: "custom:9router"` routes to the 9router entry.
But `provider: "custom:custom"` tries to find a provider named "custom" — which doesn't exist, causing 429/auth errors.

## Detection Script

```python
import json, sqlite3, os, glob

profiles_dir = os.path.expanduser('~/.hermes/profiles')
for profile_dir in sorted(glob.glob(os.path.join(profiles_dir, '*'))):
    if not os.path.isdir(profile_dir):
        continue
    name = os.path.basename(profile_dir)

    # Check sessions.json
    sj_path = os.path.join(profile_dir, 'sessions', 'sessions.json')
    if os.path.exists(sj_path):
        with open(sj_path) as f:
            data = json.load(f)
        for k, v in data.items():
            if isinstance(v, dict) and 'model_override' in v:
                mo = v['model_override']
                chat = v.get('display_name', k)
                provider = mo.get('provider', '?')
                model = mo.get('model', '?')
                if 'custom:custom' in provider:
                    print(f'BUG {name}/{chat}: model={model} provider={provider}')
                else:
                    print(f'OK  {name}/{chat}: model={model} provider={provider}')
```

## Telegram Access Control

| Config | Value | Effect |
|--------|-------|--------|
| `.env` `TELEGRAM_ALLOWED_USERS` | `#` (commented) | All users can chat |
| `.env` `TELEGRAM_ALLOWED_USERS` | `661471478,5955713269` | Only these users can chat |
| `config.yaml` `approvals.mode` | `auto` | Destructive cmds need approval |
| `config.yaml` `approvals.mode` | `off` | No approval needed (YOLO) |
| `config.yaml` `telegram.allowed_chats` | `''` | All chats allowed |
| `config.yaml` `telegram.require_mention` | `true` | Bot only responds when @mentioned in groups |
