# Godmode Merge Pattern

## Problem
`hermes-godmode` (https://github.com/vissu233549/hermes-godmode) is a config/restore pack, NOT a skill. Running `restore.sh` overwrites the entire config including 9Router settings.

## Solution: Selective Merge
Extract useful settings from godmode config and merge into existing config WITHOUT touching model/provider.

```python
import yaml

with open("/tmp/hermes-godmode/config.yaml", "r") as f:
    godmode = yaml.safe_load(f)

with open("~/.hermes/profiles/<profile>/config.yaml", "r") as f:
    current = yaml.safe_load(f)

# Merge these sections from godmode
merge_keys = [
    "agent", "display", "memory", "curator", "cron",
    "compression", "skills", "kanban", "code_execution",
    "session_reset", "streaming", "lsp"
]

for key in merge_keys:
    if key in godmode:
        current[key] = godmode[key]

# ALWAYS keep manual approval
current["approvals"]["mode"] = "manual"

# NEVER overwrite model/provider sections
# (model, custom_providers, fallback_providers stay as-is)

with open("~/.hermes/profiles/<profile>/config.yaml", "w") as f:
    yaml.dump(current, f, default_flow_style=False, sort_keys=False)
```

## What Godmode Adds
- `agent.environment_probe: true` — auto-detect environment
- `agent.task_completion_guidance: true` — better task completion
- `display.interim_assistant_messages: true` — show progress
- `display.turn_completion_explainer: true` — explain what happened
- `display.busy_ack_detail: true` — acknowledge user input
- `display.long_running_notifications: true` — notify on long tasks
- `memory.memory_enabled: true` — persistent memory
- `skills.inline_shell: false` — safer shell execution
- `session_reset.mode: both` — auto-reset idle sessions
- `code_execution.mode: project` — project-level execution

## User Preferences
- `approvals.mode: manual` — ALWAYS, never auto-approve
- 9Router ONLY — no OpenRouter, no fallback providers
- Model list: only active models, not discover_models: true
