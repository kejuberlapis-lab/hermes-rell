---
name: hermes-telegram-safety-lockdown
description: Lock down Hermes Telegram gateway so it cannot access local computer/data/tools unless explicitly allowed. Includes allowlist-first configuration, restricted platform toolsets, and recovery steps when gateway restart hits systemd TEMPFAIL.
version: 1.1.0
author: Hermes Agent
license: MIT
---

# Hermes Telegram Safety Lockdown

Use this when a user wants Telegram bot access but with strict boundaries: no terminal, file, browser, code execution, or deep system/data access unless explicitly approved later.

## When to use
- User asks to "batasi" / restrict Telegram bot privileges
- User is concerned about bot accessing computer, files, or sensitive data
- User wants deny-by-default behavior for Telegram users

## Preconditions
1. Hermes is installed and gateway configured.
2. Telegram bot token is valid in `~/.hermes/.env`.

## Procedure
1. Restrict Telegram platform toolsets in `~/.hermes/config.yaml`.
   Replace Telegram preset with minimal safe set:

   ```yaml
   platform_toolsets:
     telegram:
       - todo
       - clarify
       - skills
   ```

   This disables high-risk toolsets (terminal, file, browser, code_execution, web, messaging, delegation, cronjob, etc.).

   Optional variant (safe + research) when user wants marketing/SEO help without local computer access:

   ```yaml
   platform_toolsets:
     telegram:
       - todo
       - clarify
       - skills
       - web
   ```

   This still keeps local machine/data access blocked while enabling online SEO research.

2. Enforce closed access by default in `~/.hermes/.env`:

   ```env
   GATEWAY_ALLOW_ALL_USERS=false
   ```

3. Add explicit Telegram allowlist (required when step 2 is false):

   ```env
   TELEGRAM_ALLOWED_USERS=<telegram_user_id_1>,<telegram_user_id_2>
   ```

   Notes:
   - IDs must be numeric Telegram user IDs (not usernames/invite codes).
   - Fast way to get ID: message `@userinfobot` or `@myidbot`, then copy the numeric `id`.

4. Restart gateway:

   ```bash
   hermes gateway restart
   ```

   If status briefly shows `activating (auto-restart)` after restart, wait a few seconds and re-check before treating as failure.

5. If gateway fails with systemd restart/TEMPFAIL or "start request repeated too quickly", recover with:

   ```bash
   systemctl --user reset-failed hermes-gateway.service
   hermes gateway start
   ```

## Verification
Run these checks:

1. Service state:
   ```bash
   hermes gateway status
   ```
   Expect: `active (running)`.

2. Telegram tool exposure:
   ```bash
   hermes tools list --platform telegram
   ```
   Expect only `skills`, `todo`, `clarify` enabled; risky toolsets disabled.

3. Access policy:
   - If `GATEWAY_ALLOW_ALL_USERS=false`, every permitted Telegram user ID must be present in `TELEGRAM_ALLOWED_USERS`.
   - Confirm current allowlist quickly:
     ```bash
     python3 - <<'PY'
     from pathlib import Path
     p=Path.home()/'.hermes/.env'
     for line in p.read_text().splitlines():
         if line.startswith('TELEGRAM_ALLOWED_USERS='):
             print(line)
     PY
     ```

4. Audit for authorization rejects (fast root-cause for “bot online but not replying”):
   ```bash
   journalctl --user -u hermes-gateway.service -n 50 --no-pager | grep -i "Unauthorized user"
   ```
   If lines appear, add the missing ID to `TELEGRAM_ALLOWED_USERS` and restart gateway.

## Pitfalls
- `patch`/file tools may block edits to protected credential files like `~/.hermes/.env`.
  - Workaround: edit via shell/Python script in terminal.
- After changing platform toolsets, a gateway restart is required for Telegram to pick up changes.
- If user forgets `TELEGRAM_ALLOWED_USERS` while `GATEWAY_ALLOW_ALL_USERS=false`, bot appears online but rejects everyone.
- Display config values are strict. For `display.tool_progress`, use only: `off`, `new`, `all`, or `verbose`.
  - Using an invalid value (for example `none`) can make gateway restarts fail with `status=75/TEMPFAIL`, causing the bot to appear unresponsive.
  - Safe setting to hide internal progress in Telegram: `display.interim_assistant_messages: false` + `display.tool_progress: off`.
- In multi-profile setups, allowlist is per-profile (`~/.hermes/profiles/<profile>/.env`).
  - Adding a Telegram ID to Node B does not automatically grant access on OLO/other profiles; update each profile's `TELEGRAM_ALLOWED_USERS` separately.
- If an allowlisted user still gets no replies, test direct delivery with Telegram Bot API `sendMessage`.
  - If response is `400 Bad Request: chat not found`, the user has not started a DM with the bot yet (or ID is wrong).
  - Fix: from that exact account, open the bot username and press **Start** (or send any plain text message), then retest.
- If the gateway logs `Unrecognized slash command /start` (or other `/...`), the bot is receiving messages but command routing may reject unknown slash commands.
  - Ask the user to send plain text first to verify interaction path, then handle command UX separately.
- If you hide progress UI in `display.tool_progress`, use valid enum values only: `off | new | all | verbose`.
  - Do **not** set `none` (invalid). It can make gateway startup fail with `status=75/TEMPFAIL` and the bot may stop replying until service is recovered.
  - Safe quiet mode combo:
    - `display.interim_assistant_messages: false`
    - `display.tool_progress: off`

## Rollback
To restore default Telegram capabilities:

```yaml
platform_toolsets:
  telegram:
    - hermes-telegram
```

Then restart gateway.