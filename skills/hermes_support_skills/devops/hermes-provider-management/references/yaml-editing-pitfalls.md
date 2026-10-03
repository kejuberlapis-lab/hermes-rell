# YAML Editing Pitfalls (Profile Configs)

Hermes profile configs are YAML. Shell-based editing (`sed`) and `yaml.dump` both have sharp edges that silently corrupt files. Documented here so the next sync session doesn't rediscover each one.

## sed inline editing traps

### Joining lines instead of keeping structure

**Problem:** `sed` substitution on YAML block sequences often joins lines:
```
# Before (valid YAML):
custom_providers:
  - name: 9router
    base_url: http://localhost:20128/v1

# After (INVALID YAML):
custom_providers:
- name: 9router    base_url: http://localhost:20128/v1
```

**Cause:** `sed` address ranges with `a` (append) can write the new content on the same line as the target when newlines aren't explicit enough.

**Fix:** Prefer `hermes config set KEY VAL` for single-value changes. For multi-line YAML blocks, use Python `yaml.safe_load` + `yaml.dump` instead.

### YAML anchors can't survive sed

**Problem:** `sed` does not understand YAML anchors (`&anchor`, `*anchor`), aliases, or flow scalars. It treats them as plain text, so substitutions can break cross-references used by `hermes config set` output.

**Fix:** If the config uses anchors (uncommon in Hermes profiles — but possible if `hermes setup` generated them), use Python YAML, not sed.

## Python yaml.dump formatting quirks

### `default_flow_style=False` is required for block sequences

**Wrong** (produces inline JSON-style YAML):
```python
yaml.dump(cfg, f)
# → custom_providers: [{name: 9router, base_url: 'http://...'}]
```

**Right** (produces block list readable by humans):
```python
yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)
```

### `sort_keys=False` to preserve field order

`yaml.dump` sorts dict keys alphabetically by default (`allow_unicode` first, then `api_key`, then `base_url`, etc.). This scrambles the `model` section into unreadable order. Always pass `sort_keys=False`.

### Full safe write recipe

```python
import yaml

path = '/home/ubuntu/.hermes/profiles/hermes-support/config.yaml'
with open(path) as f:
    cfg = yaml.safe_load(f)

# Modify cfg dict in place...

with open(path, 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, sort_keys=False,
              allow_unicode=True, width=200)
```

The `width=200` prevents long strings from wrapping mid-word.

## When to use which approach

| Change type | Tool | Reason |
|-------------|------|--------|
| Single scalar (`model.provider`, `model.base_url`) | `hermes config set KEY VAL` | Hermes handles YAML correctly, validates, and creates backup hooks |
| Single-line removal (`api_key: ''`) | `sed -i '/^  api_key:/d' config.yaml` | Simple and reliable when the line pattern is unambiguous |
| Multi-line YAML block (custom_providers, providers, plugins) | Python `yaml.safe_load` + `yaml.dump` | `sed` address ranges mutilate YAML structure; Python preserves it |
| Bulk same edit across N profiles | Loop over `hermes config set` per profile, or Python for block edits | Mixed: shell loop for scalars, Python loop for blocks |
