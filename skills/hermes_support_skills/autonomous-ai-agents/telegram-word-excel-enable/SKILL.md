---
name: telegram-word-excel-enable
description: Enable Hermes Telegram bot to process Word/Excel files and return generated files while keeping terminal access disabled.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Enable Word/Excel handling on Telegram (safe profile)

Use this when a user wants Telegram bot capabilities for `.docx` and `.xlsx` tasks (read/edit/generate/export), but does NOT want broad local machine access.

## Outcome
Telegram bot can:
- read/write files via `file` toolset
- run Python document transforms via `code_execution`
- return output files in chat

Telegram bot still cannot use shell if `terminal` stays disabled.

## Prerequisites
- Hermes gateway installed and running
- Telegram user already allowlisted (if `GATEWAY_ALLOW_ALL_USERS=false`)
- Hermes runtime venv exists at `~/.hermes/hermes-agent/venv`

## Procedure

1) Enable Telegram platform toolsets in `~/.hermes/config.yaml`

Set `platform_toolsets.telegram` to include at least:

```yaml
platform_toolsets:
  telegram:
    - todo
    - clarify
    - skills
    - web
    - file
    - code_execution
```

Keep `terminal` disabled unless explicitly approved by user.

2) Install Word/Excel Python libraries into Hermes gateway venv

Important: install into the Hermes venv (not system Python).

```bash
/home/<user>/.hermes/hermes-agent/venv/bin/python -m ensurepip --upgrade
/home/<user>/.hermes/hermes-agent/venv/bin/python -m pip install python-docx openpyxl pandas xlsxwriter
```

3) Verify imports in the same Hermes venv

```bash
/home/<user>/.hermes/hermes-agent/venv/bin/python - <<'PY'
for m in ['docx','openpyxl','pandas','xlsxwriter']:
    __import__(m)
    print(m+':ok')
PY
```

4) Restart gateway

```bash
hermes gateway restart
```

If restart fails with `status=75/TEMPFAIL` or auto-restart loop:

```bash
systemctl --user reset-failed hermes-gateway.service
hermes gateway start
```

5) Verify Telegram tool exposure

```bash
hermes tools list --platform telegram
```

Expect `file` and `code_execution` enabled.

## Pitfalls / Lessons learned

- Using system Python may hit PEP 668 "externally-managed-environment" and won’t affect Hermes runtime.
- `~/.hermes/hermes-agent/venv` may initially lack pip; run `ensurepip` first.
- Installing with `/usr/bin/python3 -m pip --user` does not guarantee Hermes gateway can import those packages.
- Config changes may appear in `hermes tools list --platform telegram` before a full gateway restart; restart is still recommended for deterministic behavior.

## Security notes

- `file + code_execution` allows file processing, but is still more constrained than enabling `terminal`.
- Keep allowlist enforced for Telegram users when operating in strict mode.
- Do not enable `browser`, `terminal`, or `messaging` unless user explicitly permits.
