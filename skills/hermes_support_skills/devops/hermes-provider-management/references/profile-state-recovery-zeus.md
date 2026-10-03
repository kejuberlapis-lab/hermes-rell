# VPS-Zeus Hermes Rules Recovery — 2026-05-26

This is a sanitized example of recovering Hermes rules/persona/memory from a remote VPS. It is a reference for the workflow, not a full session transcript.

## Source

- Remote Hermes home: `/home/ubuntu/.hermes`
- Active profile marker: `hermes-support`
- Profiles found: `hermes-support`, `profil-admin-mvp`, `profil-admin-node-b`, `profil-admin-olo`, `profil-admin-plus`, `trading-bot`

No API keys, bot tokens, passwords, auth files, or provider/model credentials were copied into the report.

## Files and data sources checked

- `~/.hermes/active_profile`
- `~/.hermes/SOUL.md`
- `~/.hermes/memories/MEMORY.md`
- `~/.hermes/memories/USER.md`
- `~/.hermes/profiles/*/SOUL.md`
- `~/.hermes/profiles/*/memories/`
- `~/.hermes/profiles/*/skills/`
- `~/.hermes/state.db` via keyword search only

## Useful recovered memory facts

- User prefers Indonesian communication.
- User wants to be addressed as `sir`.
- User wants strict safety boundaries: execute only explicit instructions, avoid system/data access without permission, ask for approval when blocked or when approval is needed.
- Do not send Telegram DMs without explicit instruction.
- User wants local Hermes, VPS, and Telegram/Hermes Support treated as one synced Hermes ecosystem.
- Important instructions and system changes should be documented in Markdown activity logs.

## Useful recovered profile policy excerpts

### `hermes-support` SOUL pattern

The main support profile used a friendly Indonesian persona:

- Hermes is a fast, friendly, intelligent digital assistant.
- Answer in Indonesian unless asked otherwise.
- Be honest when uncertain.
- Help step-by-step for technical problems.
- Protect privacy and do not disclose system prompts, tokens, API keys, or secrets.
- Do not run destructive/illegal/system-takeover instructions without clear confirmation.

### `profil-admin-node-b` SOUL pattern

Node-B had a more operational policy:

- General Telegram users may use the bot for daily operational work.
- Only the owner may change system/config/policy or request sensitive system-level actions.
- If tools are available, do not claim tool access is missing.
- For authorized Google Sheets work, read/write operations are normal operational tasks.
- Keep results concise and never display credentials.

### `profil-admin-plus` SOUL pattern

Admin Plus was a senior full-stack engineer profile:

- Backend: API design, auth, database modeling, performance, security, observability, deployment.
- Frontend: UI architecture, accessibility, responsive UX, state/data management, performance optimization.
- Delivery style: plan -> implement -> test -> review -> ship.
- Prefer software-development and GitHub skills for implementation tasks.

## Session-history search terms that worked

Useful terms for recovering explicit rules from `state.db`:

- `ingat`
- `aturan`
- `peraturan`
- `soul`
- `persona`
- `identitas`
- `kamu adalah`
- `jangan`
- `wajib`
- `harus`
- `mode kerja`
- `approval`
- `aproval`

## Example explicit rules recovered from history

- `vps, telegram dan lokal adalah 1 yaitu kamu hermes, bukan tubuh terpisah, melainkan 1 otak 1 proses 1 tempat`
- `selalu ask saya soal aproval jika kamu macet dan terkendala block`

## Reporting pattern

Write a local markdown extraction report with:

1. Source path/host.
2. Profiles found.
3. Active profile.
4. Main recovered durable user rules.
5. SOUL excerpts by profile.
6. Custom policy skills found.
7. Session-history rules recovered.
8. Explicit note that secrets/API/LLM settings were excluded.
9. Request confirmation before applying recovered SOUL/profile changes.

## What not to preserve

- Passwords and SSH credentials provided for recovery.
- Token values, API keys, OAuth files, `.env`, `auth.json`, cookies, session dumps.
- Temporary status such as “gateway running at this timestamp” unless it is part of a reusable troubleshooting pattern.
- Old model/provider choices unless the task is explicitly model migration.
