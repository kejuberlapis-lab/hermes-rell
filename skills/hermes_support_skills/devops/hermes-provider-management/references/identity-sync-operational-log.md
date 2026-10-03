# Identity Sync Operational Logging

## When to use
- User requests identity, SOUL, rules, persona updates, or sync across local/VPS/Telegram.
- Recording important policy/persona changes to a Markdown operational log.

## Steps
1. Load relevant skill/rule context.
2. Discover existing log/identity markdown files.
3. Default path: `~/.hermes/ops-logs/operational-log.md` or the relevant profile directory.
4. Check actual time with `date -u` for log timestamps.
5. Verify local data first: file exists, hash/content correct.
6. If VPS sync needed, check SSH access and target Hermes path.
7. Never display tokens, API keys, passwords, secrets, private keys, or credential content.
8. For skill sync between profiles/hosts: do NOT use `rsync --delete` on broad skill roots with include/exclude patterns — it may delete unrelated skill directories. Use allowlist without delete, or target specific skill directories one-by-one.
9. Record only a safe summary: what changed, path, hash/verification, success/pending status.
10. **For 1-KESATUAN sync** (local/VPS/Telegram as one entity):
    - Model, provider, and base_url MUST be identical on all sides (currently: deepseek/deepseek-v4-flash).
    - API keys are NOT auto-synced — copy manually via Python subprocess + SCP script.
    - Do NOT sync `.env`, Telegram tokens, raw session databases.
    - Ensure only one Telegram runner is active (VPS as primary; delete local gateway service file).
    - Follow `references/local-vps-telegram-sync.md` for the full procedure.
11. For syncing all bot profiles, record a safe matrix summary: skill count, toolset/config similarity to reference profile, active gateways, backup paths, and pending items awaiting approval. Never include secret lists, `.env` contents, or Telegram tokens.

## Log format (compact)
```md
## YYYY-MM-DD HH:MM UTC — Identity/Policy Sync
- Scope:
- Local:
- VPS/Telegram:
- Verification:
- Notes:
```
