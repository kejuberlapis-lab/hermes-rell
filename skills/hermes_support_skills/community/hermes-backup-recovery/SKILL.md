---
name: backup-recovery
description: >-
  Back up, verify, and restore a long-running Hermes deployment's state (memory, learned
  skills, config, chat history). Use when the user asks to protect against data loss, set up
  scheduled encrypted backups, run a restore drill, check whether backups are healthy, or
  recover after a crash or disk failure. Designed for always-on agents where losing state is
  not acceptable. Provider- and hardware-agnostic.
---

# Hermes backup & recovery

Keep an always-on Hermes instance recoverable. This skill wraps four small scripts in `scripts/`
that do the actual work; your job is to run the right one with the right environment and report the
result clearly.

## What gets protected

Everything under `$HERMES_HOME` — the directory where Hermes keeps memory, skills, config, and chat
history. Confirm the real path with the user before running anything; do not guess it.

## Configuration (environment variables)

| Variable | Used by | Meaning |
|---|---|---|
| `HERMES_HOME` | backup, healthcheck | Hermes data directory to protect |
| `BACKUP_DIR` | all | Where encrypted backups are written/read |
| `AGE_RECIPIENT` | backup | `age` public key (`age1...`) to encrypt to |
| `AGE_IDENTITY` | verify, restore | `age` private key file (keys.txt) to decrypt with |
| `KEEP` | backup | How many backups to retain (default 14) |
| `RESTORE_TARGET` | restore | Directory to restore into |
| `HERMES_SERVICE` | healthcheck | systemd unit name (default `hermes`) |
| `MAX_BACKUP_AGE_H` | healthcheck | Warn if newest backup is older than this (default 26) |

The **private key (`AGE_IDENTITY`) must live off the box**, not next to the backups. If it sits on the
same machine, an attacker or a disk failure takes both.

## How to run each task

- **Back up now** → `scripts/backup.sh`. Requires `HERMES_HOME`, `BACKUP_DIR`, `AGE_RECIPIENT`.
  Produces a timestamped, encrypted `hermes-<ts>.tar.gz.age` plus a `.sha256`, and prunes old backups
  beyond `KEEP`.
- **Verify a backup** → `scripts/verify.sh [file]`. Requires `BACKUP_DIR`, `AGE_IDENTITY`. Checks the
  checksum and test-decrypts + lists the archive. Defaults to the newest backup if no file is given.
  **Run this after every scheduled backup** — a backup you can't decrypt is worthless.
- **Restore** → `scripts/restore.sh [--apply] <file>`. Requires `AGE_IDENTITY`, `RESTORE_TARGET`.
  **Dry-run by default** (lists what it would write); only `--apply` actually writes. After a real
  restore, tell the user to review the target and restart Hermes.
- **Health check** → `scripts/healthcheck.sh`. Exits 0 if healthy, 1 if attention is needed (service
  down, disk >90%, or no recent backup). Good on a timer wired to a notification.

## Guardrails

- Never print or log the contents of `AGE_IDENTITY` or any provider key.
- Never delete backups except through `backup.sh`'s own `KEEP` retention. Do not "clean up" backups on
  your own initiative.
- Before a real (`--apply`) restore, confirm with the user — it overwrites files in `RESTORE_TARGET`.
- If a script exits non-zero, report the exact failure; do not retry blindly or fabricate success.

## Scheduling

For unattended operation, run `backup.sh` on a nightly systemd timer and `healthcheck.sh` a bit later,
routing a non-zero health result to whatever channel the user watches. See the companion guide
[Running Hermes 24/7 on dedicated hardware](https://github.com/JimmyHuang2002/hermes-always-on).
