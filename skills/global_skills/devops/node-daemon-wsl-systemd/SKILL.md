---
name: node-daemon-wsl-systemd
description: >-
  Run and keep alive local Node.js CLI daemons (9Router LLM gateway, and other
  shebang-script node tools) as systemd user services on headless WSL.
  Covers two recurring failure modes that look like crashes but are not: clean self-exit
  on headless WSL, and exit 127 because the env node shebang can't find node in the
  systemd user PATH.
category: devops
triggers:
  - 9router jalan lalu langsung keluar / Exiting tanpa error
  - systemd user service status 127 / env node not found
  - node CLI daemon tidak bisa dijalankan sebagai service di WSL headless
  - keep node gateway daemon alive via systemctl --user
---

# Node CLI Daemon as systemd User Service on Headless WSL

When a Node.js CLI daemon (9Router is the main case here) "won't stay up" on WSL, it is almost always one of two NON-crash failures. Symptoms overlap (service keeps dying), so diagnose by checking the exit code before assuming a signal kill or a missing binary.

## Two failure modes (and fixes)

### 1. Clean self-exit (no --skip-update) — the "0ms Ready → Exiting" pattern

**Symptom:** logs show the Next.js/CLI banner (`✓ Ready in 0ms`), the DB driver line, then `Exiting...` twice and the process exits **cleanly with code 0**. Health checks still return `HTTP 000` / no port bind.

**Cause:** on headless WSL (no display, no system tray), 9router's **auto-update check tears the process down** shortly after it reports ready. It is not a crash and not a signal — it exits on its own.

**Diagnosis tip:** run it under a wrapper that records the real status:
```bash
# ~/.9router/logs/run-9router.sh
cd ~/.9router
/home/ndisap/.hermes/node/bin/9router --no-browser --host 127.0.0.1 --log > run.log 2>&1
echo "REAL_FINAL_EXIT_CODE=$?" >> run.log
```
A clean `REAL_FINAL_EXIT_CODE=0` (not 128+N) = self-exit, not SIGTERM/SIGKILL. That points straight at `--skip-update`.

**Fix:** always pass `--skip-update` on headless. `--no-browser` alone is not enough.

```bash
~/.hermes/node/bin/9router --no-browser --host 127.0.0.1 --skip-update
```

### 2. exit 127 / `env: 'node': No such file or directory` under systemd

**Cause:** the CLI (e.g. `~/.hermes/node/bin/9router`) is a symlink to a `cli.js` whose shebang is `#!/usr/bin/env node`. systemd user services get a **minimal PATH that excludes `~/.hermes/node/bin`**, where the actual `node` binary lives, so `env` cannot find it → `status=127`/`exit-code` restart loop.

**Fix:** add `~/.hermes/node/bin` to `Environment=PATH=` in the unit.
```ini
Environment=PATH=/home/ndisap/.hermes/node/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

## Known-good unit (local WSL, 9Router)

```ini
# ~/.config/systemd/user/9router.service
[Unit]
Description=9Router - Local LLM Gateway
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/ndisap/.9router
ExecStart=/home/ndisap/.hermes/node/bin/9router --no-browser --host 127.0.0.1 --skip-update
Restart=on-failure
RestartSec=3
Environment=PATH=/home/ndisap/.hermes/node/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
StandardOutput=append:/home/ndisap/.9router/logs/9router-service.log
StandardError=append:/home/ndisap/.9router/logs/9router-service.log

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now 9router.service
```

## Replicating to a VPS (or any second host)

The same unit pattern carries to another host, but two additional failure modes appear because rsync of `~/.9router` often **skips the empty `logs/` folder**:

- **`status=209/STDOUT`** immediate exit: `StandardOutput=append:/home/<user>/.9router/logs/9router-service.log` fails to open when `~/.9router/logs/` does not exist yet on the remote. Fix: `mkdir -p ~/.9router/logs` on the target **before** enabling the service.
- **`status=127`** — same PATH cause: ensure `Environment=PATH=<hermes-root>/node/bin:...` points at the actual node on that host, and that `ExecStart` uses the remote home path.

`~/.hermes/node` (317MB, includes the `9router` CLI + node binary) is transferable via rsync and must land on the target before the unit runs. Data lives in `~/.9router` (db/, jwt-secret, machine-id, auth/) — rsync that too but **exclude `logs/`** then recreate it. After `systemctl --user enable --now 9router.service`, a quick-start self-exit like the local case may not appear because `--skip-update` is already in the unit; still confirm the four checks below on the remote.

## Verification (not just "it stays up")

```bash
ss -talnp | grep 20128            # expect LISTEN on 127.0.0.1:20128
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:20128/v1/models   # expect 200
systemctl --user is-active 9router   # expect active
```

## Pitfalls

- **WSL systemd user services may need `loginctl enable-linger ndisap`** (or manual start) to persist after the user session ends. Enable alone is not enough if linger is off.
- **Headless 9Router has no system tray** — that is expected. The HTTP server still serves; don't read "system tray mode" as a failure.
- **Don't kill via `pkill -f 9router` in a foreground interactive shell:** the pattern can match the invoking shell itself and kill it (exit -15). Use the Hermes process handle / `systemctl restart`, or a precise `pkill -f '9router --no-browser'` from an isolated context.
- node_modules lives at `~/.hermes/node` because the default npm prefix (/usr) needs root; always run the CLI and set PATH from `~/.hermes/node/bin`.
- **9Router remote dashboard access requires INITIAL_PASSWORD** — When accessing 9Router dashboard from outside (not localhost), it shows "Default password must be changed before remote access." Fix: add `Environment=INITIAL_PASSWORD=your-password` to the systemd service unit.

## Interactive password delivery via Hermes background PTY (no sshpass/expect/sudo)

Sometimes you need to authenticate to an interactive remote (SSH) or CLI that asks for a password, but the box has no `sshpass`, no `expect`, and you cannot `apt install` (no sudo). The proven method that needs **nothing installed** is to run the client as a Hermes background process with a PTY and pump the password in via the process handle — the password never appears in argv, so it is safe from `ps`/history.

```
1. terminal(background=true, pty=true, command="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ubuntu@<IP>")
2. process(action='poll') on the session to confirm the "password:" prompt has appeared before sending.
3. process(action='submit', data="<password>") — raw bytes, no newline toggling needed.
4. poll again for the remote shell prompt, then submit a multistep verifier (hostname; systemd checks; curl health) on one line and `exit`.
```

Why this beats pexpect for the common case: no venv, no `pip install`, works even when the sandbox blocks `&`-backgrounding in foreground commands. Keep the password out of the chat echo afterward.

## Related

- For SSH-specific diagnosis (banner timeout, sshd-level key rejection, provider console recovery) see the `vps-ssh-diagnosis` and `vps-ssh-password-connectivity` skills (agent/SSH coverage) — use this PTY-submit method to get the session in.
- For full 9Router provider/config/API-key coverage see the `hermes-provider-management` skill
(reference `references/9router-setup.md`). This skill is specifically about keeping the node
daemon alive and auto-starting on headless local WSL.