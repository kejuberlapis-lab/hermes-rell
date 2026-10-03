# Profile Skills/Tools Sync Across Hermes Bot Profiles

Use when sir asks that every bot profile has the same available skills/tools while preserving each profile's bot setup.

## Goal
Keep profiles operationally aligned without copying secrets or destroying profile-specific setup.

## Safe sync pattern
1. Pick a reference profile for operational config, usually `hermes-support`.
2. Discover all profiles under `~/.hermes` and `~/.hermes/profiles/<name>/`.
3. Build a union of installed skill directories across profiles by locating `skills/**/SKILL.md`.
4. Prefer the reference profile's copy when the same skill exists with different content, but do not overwrite an existing per-profile skill unless sir explicitly requests canonical replacement.
5. Copy only missing skill directories into each profile.
6. Sync safe config keys from the reference profile only:
   - `platform_toolsets`
   - `toolsets`
   - `skills` / skills enablement config
   - selected non-secret `memory`, `approvals`, and display keys if requested
7. Never sync or print:
   - `.env`
   - token/API key/password/auth/private key/session cookie
   - raw `state.db` or gateway session data
   - Telegram allowlists/channel routing unless sir explicitly asks
8. Back up every touched profile's `config.yaml` and `skills/` before edits.
9. Restart only the named gateway units that actually correspond to bot profiles, after scope/approval is clear.
10. Verify with a compact matrix: skill count, `platform_toolsets_same_as_reference`, `toolsets_same_as_reference`, `skills_config_same_as_reference`, Telegram/CLI tool count, and active gateway units.

## Pitfalls
- Do not use broad `rsync --delete` on profile `skills/`; it can erase skills that only exist in one profile.
- Do not overwrite same-named skill conflicts silently. Prefer reference profile for future missing copies, but preserve existing installed copies unless sir asks to normalize content too.
- A running default `hermes-gateway.service` can coexist with named profile units. Treat disable/stop of a duplicate service as a separate sensitive operation requiring explicit approval if previously blocked.
- Toolset/config changes usually require gateway restart or a new session before Telegram sees them.

## Verification shape
```json
{
  "profile": "profil-admin-node-b",
  "skill_count": 137,
  "platform_toolsets_same_as_reference": true,
  "toolsets_same_as_reference": true,
  "skills_config_same_as_reference": true,
  "telegram_tool_count": 25,
  "cli_tool_count": 25
}
```
