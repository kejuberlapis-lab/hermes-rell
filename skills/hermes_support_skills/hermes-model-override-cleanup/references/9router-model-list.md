# 9Router Model List and Verification

## Available Models on VPS 9Router (localhost:20128/v1)

As of August 2026:

```
ADR/claude-sonnet-4.5
ADR/glm-4.7-flash
ADR/grok-4.5
ADR/mimo-v2.5-pro
ag/claude-opus-4-6-thinking
ag/gemini-3-flash
ag/gemini-3-flash-agent
ag/gemini-pro-agent
ag/gpt-oss-120b-medium
cx/gpt-5.4
cx/gpt-5.4-mini
cx/gpt-5.4-mini-review
cx/gpt-5.4-review
cx/gpt-5.5
cx/gpt-5.5-review
cx/gpt-5.6-luna
cx/gpt-5.6-luna-review
cx/gpt-5.6-terra
cx/gpt-5.6-terra-review
mimo/mimo-v2.5
mimo/mimo-v2.5-pro
```

## Default Models per Profile

| Profile | Default Model |
|---------|---------------|
| hermes-support | mimo/mimo-v2.5 |
| avrel-jago | ag/gemini-3.5-flash-low |
| botavrell2 | mimo/mimo-v2.5 |
| profil-admin-mvp | mimo/mimo-v2.5 |
| profil-admin-node-b | ag/gemini-3-flash |
| profil-admin-olo | mimo/mimo-v2.5 |
| profil-admin-rofc | mimo/mimo-v2.5 |
| ais | mimo/mimo-v2.5 |

## Verification Commands

### Check 9Router is running
```bash
curl -s http://127.0.0.1:20128/v1/models | python3 -c 'import sys,json; d=json.load(sys.stdin); print(f"Models: {len(d.get(\"data\",[]))}")'
```

### Check custom_providers name
```python
import yaml
config_path = '/home/ubuntu/.hermes/profiles/<profile>/config.yaml'
with open(config_path) as f:
    config = yaml.safe_load(f) or {}
cp = config.get('custom_providers', [])
if cp:
    print(f"Name: {cp[0].get('name')}")  # Must be "9router"
    print(f"Discover: {cp[0].get('discover_models')}")
    print(f"Models: {len(cp[0].get('models', []))}")
```

### Check all profiles have correct config
```python
import yaml, os, glob
profiles_dir = os.path.expanduser('~/.hermes/profiles')
for p in sorted(glob.glob(os.path.join(profiles_dir, '*'))):
    if not os.path.isdir(p): continue
    name = os.path.basename(p)
    cfg = os.path.join(p, 'config.yaml')
    if not os.path.exists(cfg): continue
    with open(cfg) as f:
        c = yaml.safe_load(f) or {}
    model = c.get('model', {}).get('default', '?')
    provider = c.get('model', {}).get('provider', '?')
    cp_name = c.get('custom_providers', [{}])[0].get('name', '?')
    print(f"{name}: model={model} provider={provider} cp_name={cp_name}")
```

## Common Issues

1. **429 errors after model change** — Check custom_providers.name is "9router" not "custom"
2. **Model not showing in /model menu** — Ensure discover_models: true
3. **Wrong provider stored** — Must stop gateway before clearing overrides
