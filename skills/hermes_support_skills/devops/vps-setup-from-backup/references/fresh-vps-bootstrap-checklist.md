# Fresh VPS Bootstrap Checklist

Checklist lengkap saat bootstrap VPS baru dari OS reset.

## Pre-flight
- [ ] VPS SSH accessible (via Tencent Console VNC jika port 22 belum open)
- [ ] Password diketahui (username `ubuntu`)

## SSH Access Setup
- [ ] Compile sshpass dari source (jika apt tidak tersedia): download sshpass-1.09.tar.gz → `./configure && make` → copy ke `~/.local/bin/sshpass`
- [ ] Tambah public key ke VPS: `cat ~/.ssh/id_ed25519.pub | sshpass -p 'PASS' ssh ubuntu@VPS 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'`
- [ ] Setup SSH config alias (`vps-zeus`) di `~/.ssh/config`
- [ ] Verify key-based auth: `ssh vps-zeus 'echo OK'`

## SSH Auto-Recovery
- [ ] Buat script `~/keep_ssh_alive.sh` di VPS (cek sshd + allow port 22)
- [ ] Set cron: `*/5 * * * * ~/keep_ssh_alive.sh`

## Hermes Install
- [ ] Run installer: `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`
- [ ] Finish npm install jika timeout: `export PATH="$HOME/.hermes/node/bin:$PATH" && cd ~/.hermes/hermes-agent && npm install`
- [ ] Verify: `~/.hermes/hermes-agent/venv/bin/hermes --version`

## 9Router Install
- [ ] `npm install -g 9router`
- [ ] First run untuk trigger native compilation: `timeout 60 node cli.js --no-browser --skip-update`
- [ ] Symlink: `ln -sf ~/.local/lib/node_modules/9router/cli.js ~/.local/bin/9router`

## 9Router Systemd Service
- [ ] `sudo loginctl enable-linger ubuntu`
- [ ] Buat service file: `~/.config/systemd/user/9router.service`
- [ ] Set `INITIAL_PASSWORD` di environment (agar dashboard bisa diakses dari luar)
- [ ] `systemctl --user daemon-reload && enable && start 9router.service`
- [ ] Verify port: `ss -tlnp | grep 20128`

## 9Router API Key
- [ ] Buka `http://VPS_IP:20128` di browser
- [ ] Login dengan INITIAL_PASSWORD
- [ ] Menu API Keys → Create API Key
- [ ] Copy key untuk config Hermes

## Hermes Config
- [ ] Buat `~/.hermes/config.yaml` dengan custom provider pointing ke `localhost:20128/v1`
- [ ] Set API key dari 9Router dashboard
- [ ] Set model default (misal `deepseek/deepseek-v4-flash`)

## Network
- [ ] Buka port 20128 di Tencent Cloud Security Group (agar dashboard bisa diakses dari luar)
- [ ] Verify dari lokal: `nc -zv VPS_IP 20128`

## Profile Setup (multi-profile)
- [ ] Create profile directories
- [ ] Create SOUL.md untuk setiap profile
- [ ] Create config.yaml untuk setiap profile (pointing ke VPS 9Router)
- [ ] Enable Telegram plugin: `config["plugins"]["enabled"].append("platforms/telegram")`
- [ ] Symlink .env ke semua profile: `ln -sf ~/.hermes/.env ~/.hermes/profiles/<p>/.env`
- [ ] Stop + disable default gateway: `systemctl --user stop hermes-gateway && disable hermes-gateway`
- [ ] Install gateway untuk setiap profile
- [ ] Verify semua gateway running

## Sync dari Local
- [ ] Copy .env, config.yaml, SOUL.md
- [ ] Copy skills via tar + SCP
- [ ] Copy memories via tar + SCP
- [ ] Copy state.db (opsional, bisa timeout)

## Verification
- [ ] `curl -s http://localhost:20128/v1/models | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Models: {len(d.get(\"data\",[]))}')" `
- [ ] `systemctl --user list-units --type=service --state=running | grep -E "hermes|9router"`
- [ ] Test inference: `curl -s -X POST http://localhost:20128/v1/chat/completions -H 'Content-Type: application/json' -H 'Authorization: Bearer API_KEY' -d '{"model":"deepseek/deepseek-v4-flash","messages":[{"role":"user","content":"Hi"}],"max_tokens":10}'`
- [ ] Test bot responds on Telegram
