# Recovery pasca-reset/rebuild VPS (multi-profile + 9router)

Gunakan saat user bilang "VPS di-reset" / bot semua tak respon dan ternyata box
sudah balik ke image minimal (profiles hilang, 9router hilang, config lama).
Sumber restore: VPS lama yang datanya masih utuh (gateway sudah disabled = aman).

## Gejala khas box hasil reset/rebuild
- `uptime` baru beberapa menit; config.yaml mtime = tanggal image lama.
- `~/.hermes/profiles/` TIDAK ADA; `~/.9router` TIDAK ADA.
- Cuma 1 gateway/platform yang tersisa (mis. plugin bawaan image), adapter gagal:
  `config validation failed` -> `adapter creation failed` -> `No adapter available`.
- RAM used kecil (mis. <1GB) mengonfirmasi hanya 1 (atau 0) gateway jalan —
  kalau setup penuh 8 gateway, RAM pasti beberapa GB.
- Private IP bisa berubah 1 oktet setelah rebuild (catat ulang di memory).

## Diagnosa awal (read-only, jangan ubah apa pun dulu)
1. Cek liveness: `bash -c 'echo > /dev/tcp/<ip>/22'` + ping.
2. SSH (butuh password per-VPS; key auth ditolak setelah rebuild).
3. `hostname; hostname -I; uptime -s` — konfirmasi identitas & waktu rebuild.
4. `free -h; df -h /` — health.
5. `ls ~/.hermes/profiles/ || echo none` ; `systemctl is-active 9router.service`.
6. `journalctl --user -u <gateway> -n 40` untuk penyebab adapter gagal.

## Verifikasi sumber (VPS lama)
- SSH ke VPS lama (password BEDA dari VPS baru — minta ke user, jangan tebak;
  hanya 1 percobaan lalu berhenti agar tidak kena fail2ban).
- `ls ~/.hermes/profiles/` + `du -sh ~/.hermes/profiles/*` — pastikan data ada.
- Cek versi Hermes kedua VPS: config lama boleh dimigrasi MAJU (baru >= lama).
  Jika tujuan lebih baru, `hermes doctor --fix` menangani migrasi config.
- Konfirmasi gateway lama semua `disabled` (aman, tak konflik polling).

## Transfer VPS-ke-VPS langsung (bukan lewat lokal)
1. Otorisasi SSH key OLD->NEW: ambil `~/.ssh/id_ed25519.pub` OLD, append ke
   `~/.ssh/authorized_keys` NEW (idempotent, cek marker dulu).
2. Setelah rebuild, host key NEW berubah -> di OLD muncul
   "REMOTE HOST IDENTIFICATION HAS CHANGED" saat ssh. Ini WAJAR, bukan serangan.
   Bersihkan: `ssh-keygen -f ~/.ssh/known_hosts -R <new-ip>` lalu ssh accept-new.
3. rsync sebagai BACKGROUND job di OLD (nohup) supaya tahan putus koneksi;
   `--info=progress2 --partial --timeout=120` + SSH keepalive
   `-o ServerAliveInterval=15 -o ServerAliveCountMax=3`.
4. Path yang dibawa: config.yaml .env auth.json SOUL.md active_profile
   profiles/ skills/ memories/ sessions/ cron/ kanban.db.
   Exclude: image_cache/ audio_cache/ document_cache/ logs/ *.log media/
   __pycache__/ *.pyc .cache/  (dan profiles/*/home/.cache = regenerable, besar).
5. Poll berkala via `tail` log + `pgrep -af 'rsync -az'`. File kecil (sessions/)
   melambatkan throughput — normal.

## PITFALL: rsync exit code 23 = "some files not transferred"
- BUKAN fatal. Cari file mana yang gagal SEBELUM menyimpulkan:
  `grep -iE 'rsync:|denied|failed' <log>`.
- Penyebab tersering di sini: sebagian file profile milik `root:root` mode `600`
  (ditinggalkan saat cutover lama dijalankan sebagai root). User `ubuntu` tak bisa
  baca -> "Permission denied (13)". Biasanya file penting: profile config.yaml,
  memories/MEMORY.md.
- FIX (butuh sudo NOPASSWD di OLD):
  `sudo install -D -m644 -o ubuntu -g ubuntu ~/.hermes/<path> /tmp/rootfix/<path>`
  untuk tiap file, lalu `rsync -a /tmp/rootfix/profiles ubuntu@NEW:~/.hermes/`.
- Verifikasi tak ada file unreadable tersisa:
  `find ~/.hermes/profiles -type f ! -readable`.

## Migrasi 9router
- 9router = systemd USER service, diinstall via npm. Cek versi OLD:
  `9router --version` (mis. 0.5.20), prefix `npm config get prefix`
  (mis. `~/.hermes/node`, binary symlink `~/.hermes/node/bin/9router`).
- Install versi SAMA di NEW dgn prefix sama:
  `npm install --prefix ~/.hermes/node -g 9router@<ver>`.
- Transfer HANYA data esensial (skip runtime/ = node_modules+chromium, regenerable):
  `~/.9router/db/data.sqlite` (bisa ~1.4G) + `jwt-secret` + `machine-id` +
  `auth/` + `db.json`. Exclude: runtime/ logs/ mitm/ request-details.json
  usage.json log.txt *.backup-* data.sqlite-wal data.sqlite-shm.
- Tulis unit `~/.config/systemd/user/9router.service` (mirror OLD):
  `ExecStart=<prefix>/bin/9router --host 0.0.0.0 --port 20128 --no-browser --log --skip-update`
  `Restart=always`, `WantedBy=default.target`.
- `chown -R ubuntu:ubuntu ~/.9router` -> `systemctl --user enable --now 9router.service`.
- Health: `ss -ltnp | grep 20128` + `curl -s localhost:20128/v1/models` (HTTP 200).

## PITFALL: unit systemd per-profile TIDAK ada di ~/.hermes
- Unit gateway per-profile hidup di `~/.config/systemd/user/hermes-gateway-<p>.service`,
  jadi TIDAK ikut ter-rsync saat memindah `~/.hermes`.
- Pasca-restore, tiap profile wajib:
  `hermes --profile <p> gateway install` lalu `... gateway start`.
- Profile yang di OLD punya token tapi belum pernah dibuat unit-nya -> tetap perlu
  `gateway install` dari nol.

## Migrasi config (doctor)
- `hermes doctor --fix` di NEW. Config v26 kompatibel dgn v0.18.2 (tak perlu ubah versi).
- Warning DEEPSEEK/MINIMAX/GITHUB key di .env boleh diabaikan bila gateway hanya
  bicara ke 9router lokal (base_url localhost:20128/v1) — key provider asli ada di
  dalam 9router (sqlite), bukan di .env profile.
- `hermes profile list` -> semua profile terbaca (paywall-bot tanpa config = wajar
  jika memang non-bot).

## Cutover aman + verifikasi (utamakan CANARY)
- Nyalakan 1 profile dulu (mis. hermes-support), verifikasi, baru sisanya.
- Verifikasi provider path TANPA Telegram: `hermes --profile <p> chat -q 'Jawab persis: OK' --quiet`.
- Verifikasi Telegram CONNECT secara non-invasif (hormati user yang tak mau token
  di-curl ke endpoint eksternal): ambil PID gateway
  `systemctl --user show hermes-gateway-<p>.service -p MainPID --value`, lalu
  `ss -tnp | grep pid=<PID>` — harus ada ESTAB ke `149.154.x:443` / `91.108.x:443`
  (DC Telegram). Log "Connecting (attempt 1/8)" TANPA retry 2/8 dst = sukses di
  attempt pertama.
- Cek log window terbaru untuk `conflict|getUpdates|401|429|unauthorized`.
- Minta user tes kirim TEKS BIASA ("halo") ke bot, bukan slash command.

## Rekonsiliasi profile "hilang"/ganjil (bukan akibat migrasi)
- Profile tanpa `TELEGRAM_BOT_TOKEN` di .env = memang non-bot, jangan dinyalakan.
- Unit gateway orphan yg folder profile-nya sudah tak ada = profile lama yang sudah
  di-rename (bandingkan ExecStart `--profile X` antar unit untuk memastikan).
- Selalu bedakan "data hilang" vs "memang tak pernah ada / regenerable" sebelum lapor.
