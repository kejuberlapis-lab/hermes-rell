# hermes-backup-recovery

A small, transparent [Agent Skill](https://agentskills.io) for keeping a long-running
[Hermes Agent](https://github.com/NousResearch/hermes-agent) recoverable: **encrypted backups**,
**verification**, **restore drills**, and a **health check** — for always-on agents where losing
state is not an option.

It's four short bash scripts plus a [`SKILL.md`](SKILL.md) so Hermes can run them itself. No lock-in,
nothing to sign up for, works on any hardware. Encryption is [`age`](https://github.com/FiloSottile/age);
archives are plain `tar.gz` you can open by hand.

## What it protects

Everything under `$HERMES_HOME` — Hermes's memory, learned skills, config, and chat history.

## Quick start

```bash
# 1. install age:  https://github.com/FiloSottile/age
# 2. generate a keypair; keep the private key OFF the box you're backing up
age-keygen -o keys.txt          # prints the public key (age1...)

# 3. back up
export HERMES_HOME="$HOME/.hermes"      # your real Hermes data dir
export BACKUP_DIR="/backups"
export AGE_RECIPIENT="age1...public..."
./scripts/backup.sh

# 4. verify (do this after every backup)
export AGE_IDENTITY="/secure/offbox/keys.txt"
./scripts/verify.sh

# 5. restore drill (dry-run first, then --apply)
export RESTORE_TARGET="/tmp/restore-drill"
./scripts/restore.sh /backups/hermes-<timestamp>.tar.gz.age
./scripts/restore.sh --apply /backups/hermes-<timestamp>.tar.gz.age

# 6. health check (exit 0 = healthy)
./scripts/healthcheck.sh
```

See [`SKILL.md`](SKILL.md) for every environment variable and the guardrails Hermes follows when it
runs these itself.

## Use it as a Hermes skill

Drop this folder into your Hermes skills directory (or point Hermes at it) so the agent can back up and
recover on request or on a schedule. The skill follows the open [agentskills.io](https://agentskills.io)
format, so it also works with other skills-compatible agents.

## Scheduling & the bigger picture

For unattended nightly backups + health alerts and for keeping Hermes up 24/7 in the first place, see the
companion guide: **[Running Hermes 24/7 on dedicated hardware](https://github.com/JimmyHuang2002/hermes-always-on)**.

## Who maintains this

Built and maintained by the [MangoTart](https://mangot.art) team — MangoTart ships a small always-on
computer with Hermes, backups and recovery preconfigured, and we extracted this skill from that work so
anyone running Hermes on their own hardware can use it. The skill has no dependency on MangoTart.

## License

[MIT](LICENSE).
