---
name: hermes-telegram-vps-migration
description: Migrasi Hermes + multi-profile Telegram bot ke VPS untuk operasi 24/7 dengan cutover aman (hindari konflik polling token), termasuk verifikasi systemd linger dan health checks.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Hermes Telegram VPS Migration (24/7)

Gunakan skill ini saat ingin memindahkan setup Hermes Telegram (default + banyak profile) dari mesin lama ke VPS agar berjalan 24 jam.

## Kapan dipakai
- User minta bot pindah ke VPS / always-on 24/7.
- Ada beberapa profile Hermes dengan token bot berbeda.
- Butuh cutover cepat tanpa bentrok polling Telegram.
- RECOVERY: VPS di-reset/rebuild sehingga profiles + 9router hilang dan semua bot
  bisu; perlu restore penuh dari VPS lama yang datanya masih utuh.

## Referensi
- `references/post-reset-recovery-playbook.md` — playbook lengkap recovery pasca
  reset/rebuild VPS: diagnosa box minimal, transfer VPS-ke-VPS, migrasi 9router,
  pitfall rsync exit-23 (file root:root 600), unit systemd per-profile tidak ikut
  rsync, dan verifikasi Telegram-connect non-invasif via `ss -tnp`.

## Prasyarat
1. Akses SSH ke VPS (IP, user, password/key).
2. Port SSH terbuka.
3. Mesin sumber punya data `~/.hermes` yang ingin dipindahkan.

## Prosedur inti
1) Verifikasi akses VPS dulu
- Uji koneksi SSH dan cek OS.
- Contoh cek cepat:
  - `uname -a`
  - `cat /etc/os-release`

2) Siapkan arsip migrasi dari mesin sumber (jangan bawa yang tidak perlu)
- Umumnya cukup:
  - `config.yaml`
  - `.env`
  - `auth.json`
  - `profiles/`
  - `skills/`
  - (opsional) `sessions/`
- Hindari memindah seluruh source tree `~/.hermes/hermes-agent` jika tidak perlu (biasanya besar).

3) Transfer ke VPS
- Upload archive ke `/root/` (atau home user target).
- Pastikan file sampai utuh sebelum ekstrak.

4) Install Hermes di VPS (jika belum ada)
- Install dependency dasar: `curl git python3 python3-venv python3-pip`.
- Jalankan installer resmi Hermes.
- Catatan: beberapa script installer tidak menerima flag `--yes`; gunakan mode interaktif terarah (mis. `yes | ...`) bila perlu.

5) Restore config/profile
- Backup state lama di VPS dulu.
- Ekstrak archive ke `~/.hermes` user yang akan menjalankan gateway.
- Setelah ekstrak, rapikan ownership agar sesuai user runtime (sering perlu `chown -R <user>:<group> ~/.hermes`).

6) Install + start semua gateway service di VPS
- Untuk default: `hermes gateway install && hermes gateway start`
- Untuk profile: `hermes --profile <name> gateway install && ... start`
- Verifikasi:
  - `hermes profile list`
  - `systemctl --user status <service>`

7) Cutover aman (sangat penting)
- Matikan semua gateway di mesin lama setelah VPS naik.
- Jika tidak, akan muncul error Telegram:
  - `Conflict: terminated by other getUpdates request`
- Ini tanda ada dua instance memakai token bot yang sama.

8) Verifikasi 24/7
- Cek semua service aktif.
- Pastikan `linger` aktif untuk user service:
  - `loginctl show-user <user> -p Linger`
  - harus `Linger=yes`

## Checklist verifikasi akhir
- Semua profile status `running/active`.
- Log tidak terus-menerus memunculkan conflict polling Telegram.
- Service survive setelah logout SSH.

## Pitfalls (temuan lapangan)
- Menjalankan `ssh -tt` dalam proses background non-interaktif bisa memunculkan warning `tcsetattr: Inappropriate ioctl for device`.
  - Solusi: jalankan foreground, atau hilangkan kebutuhan TTY.
- Setelah restore, ownership file profile bisa tetap UID dari mesin asal (mis. 1000:1000) saat runtime user berbeda.
  - Solusi: normalisasi `chown -R`.
- `hermes profile list` bisa sempat menampilkan `stopped` walau service baru start; cross-check dengan `systemctl --user is-active`.
- Saat health-check `systemctl --user --failed`, bisa muncul service desktop (mis. `xdg-desktop-portal*`, `xfce4-notifyd`) yang tidak terkait Hermes gateway.
  - Dampak: status terlihat "ada failed" padahal bot tetap sehat.
  - Opsi jika ingin dashboard bersih: disable+mask service desktop yang tidak dipakai di VPS headless, lalu `systemctl --user reset-failed`.
  - Tetap prioritaskan verifikasi unit `hermes-gateway*` untuk status operasional bot.
- Saat rename profile (`hermes profile rename lama baru`), unit service lama akan dihapus. Wajib `gateway install` + `gateway start` lagi untuk nama profile baru, lalu verifikasi unit `hermes-gateway-<nama-baru>` aktif.
- Setelah rename/cutover, kadang masih ada jejak unit lama di daftar `systemctl --user` (mis. `not-found failed`). Ini bukan bot aktif, tapi mengganggu health-check.
  - Cleanup aman:
    - `systemctl --user stop hermes-gateway-<nama-lama>.service || true`
    - `systemctl --user disable hermes-gateway-<nama-lama>.service || true`
    - `rm -f ~/.config/systemd/user/hermes-gateway-<nama-lama>.service`
    - `systemctl --user daemon-reload`
    - `systemctl --user reset-failed hermes-gateway-<nama-lama>.service || true`
  - Verifikasi ulang: `systemctl --user list-units --type=service --all "hermes-gateway*"`
- Saat membuat profile bot baru dari clone (`--clone-from`), selalu set ulang `.env` profile target (minimal `TELEGRAM_BOT_TOKEN`, `GATEWAY_ALLOW_ALL_USERS=false`, `TELEGRAM_ALLOWED_USERS=<id>`). Jangan asumsi nilai clone sudah aman untuk produksi.
- Jika bot membalas "re-authenticate" / log menunjukkan `No Codex credentials stored. Run \`hermes auth\``, cek apakah `auth.json` ada di profile target (`~/.hermes/profiles/<profile>/auth.json`).
  - Perbaikan cepat: salin `~/.hermes/auth.json` ke file auth profile target (jika memang memakai kredensial akun yang sama), lalu restart gateway profile.
- Jika log menunjukkan `HTTP 401 ... token_invalidated` pada `openai-codex`, sekadar menyalin `auth.json` lama ke profile tidak cukup; lakukan re-auth device flow di mesin runtime (mis. VPS root):
  - `hermes auth add openai-codex --type oauth --no-browser --timeout 600`
  - Buka URL device code dan authorize.
  - Cek `hermes auth list`; jika ada credential lama invalid sebagai credential aktif, hapus credential lama (mis. `hermes auth remove openai-codex 1`) sehingga credential baru menjadi aktif.
  - Salin `/root/.hermes/auth.json` baru ke semua profile bot yang memakai Codex (`/root/.hermes/profiles/<profile>/auth.json`), lalu restart service profile.
  - Verifikasi setelah 30-90 detik: service aktif dan log terbaru bersih dari `401|token_invalidated|authenticate`.
- Untuk multi-profile bot di VPS, setelah re-auth Codex sukses, samakan auth store ke semua profile terkait sebelum restart massal. Jika tidak, satu profile bisa sehat sementara profile lain tetap memakai token lama.
- Jika log menunjukkan `HTTP 401`, `token_invalidated`, atau `Your authentication token has been invalidated`, jangan hanya menyalin `auth.json` antar profile. Itu menandakan OAuth/Codex token sudah tidak valid atau di-refresh oleh client lain.
  - Root-cause check: lihat log window terbaru pada unit profile (`journalctl --user -u hermes-gateway-<profile> --since "30 minutes ago"`) dan cari `401|token_invalidated|auth|authenticate`.
  - Cek keberadaan/mtime/hash `~/.hermes/auth.json` dan `~/.hermes/profiles/<profile>/auth.json` tanpa membocorkan isi token.
  - Jika copy global auth ke profile + restart masih menghasilkan 401, lakukan re-auth interaktif pada environment runtime yang menjalankan gateway (mis. VPS root): `hermes auth`.
  - Setelah re-auth sukses, salin auth baru ke profile target bila profile memakai auth terpisah: `cp -a ~/.hermes/auth.json ~/.hermes/profiles/<profile>/auth.json`, lalu restart unit profile.
  - Jangan mengandalkan command `codex` selalu tersedia di VPS; pada beberapa install Hermes hanya `hermes` yang ada, sehingga prosedur praktisnya adalah `hermes auth` langsung.
  - Catatan: service bisa tetap `active` walau request Telegram gagal auth; status aktif saja tidak membuktikan token valid. Verifikasi dengan log setelah user mengirim teks biasa.
- Jika Telegram bot menampilkan `No Codex credentials stored` lalu setelah auth disalin muncul `HTTP 400 ... The 'gpt-5.5-codex' model is not supported when using Codex with a ChatGPT account`, ini bukan masalah Telegram token, melainkan model Codex tidak kompatibel dengan akun ChatGPT tersebut.
  - Perbaikan praktis yang terbukti: set semua profile Telegram Codex ke model supported yang sebelumnya jalan, mis. `gpt-5.3-codex`, tetap `provider: openai-codex`.
  - Samakan auth semua profile ke global auth runtime: backup lalu `cp -a ~/.hermes/auth.json ~/.hermes/profiles/<profile>/auth.json`; jalankan `hermes auth reset openai-codex` dan `hermes --profile <profile> auth reset openai-codex` bila credential tertanda exhausted.
  - Validasi token Telegram secara terpisah dengan Bot API `getMe` untuk tiap profile agar tidak keliru mendiagnosis model/auth sebagai token bot rusak.
  - Restart semua unit profile, tunggu 30-60 detik karena status bisa `activating`, lalu cek `hermes profile list` dan `systemctl --user is-active hermes-gateway-<profile>`.
  - Verifikasi request path tanpa menunggu user: jalankan `hermes --profile <profile> chat -q "Jawab persis: OK" --quiet` dari VPS. Jika ini menghasilkan `OK`, provider/model/auth profile sudah valid.
  - Setelah restart, cek log window terbaru untuk `gpt-5.5-codex|not supported|No Codex credentials|hermes auth|hermes model|401|429|conflict|getUpdates`.
- Jika restart profile menghasilkan `status=75/TEMPFAIL`, lakukan recovery systemd:
  - `systemctl --user reset-failed hermes-gateway-<profile>`
  - `hermes --profile <profile> gateway start`
- Di Telegram, `/start` bisa tercatat sebagai `Unrecognized slash command /start` pada beberapa konfigurasi gateway.
  - Uji bot dengan kirim **teks biasa** (mis. "halo") untuk validasi request/reply path, bukan slash command.
- Jika user melaporkan "Telegram belum sinkron ke VPS" atau minta "semua profile Telegram berjalan seperti sebelumnya", jangan langsung asumsi bot down.
  - Lakukan urutan verifikasi cepat:
    1) `systemctl --user is-active hermes-gateway-<profile>`
    2) validasi token bot profile dengan `getMe` (harus `ok=true`)
    3) cek log **window terbaru** (2-5 menit) untuk `conflict|getUpdates|429|unauthorized|timeout`, bukan hanya log historis lama
    4) jika perlu, restart unit profile lalu monitor log 1-3 menit
  - Catatan: log conflict lama bisa menipu (historical noise). Patokan utama adalah status aktif + error window terbaru.
  - Jika VPS profile sudah aktif tetapi log default/profile menampilkan `Telegram polling conflict ... terminated by other getUpdates request`, cek juga gateway lokal/mesin sumber. Pada setup user dengan WSL lokal + VPS-Zeus, konflik bisa berasal dari `hermes-gateway.service` lokal yang masih running memakai token sama. Solusi cutover aman: hentikan gateway lokal (`systemctl --user stop hermes-gateway.service`) setelah mendapat approval native, lalu verifikasi ulang log VPS 20-30 detik kemudian.
  - Saat ingin mengembalikan profile multi-bot ke kondisi pra-perubahan agent, cari backup profile seperti `~/.hermes/profiles/<profile>/config.yaml.bak_*`, bandingkan `model`, `provider`, `approvals`, `platform_toolsets.telegram`, dan `display`. Untuk hemat token yang stabil di Telegram, set `display.personality: concise`, `display.interim_assistant_messages: false`, dan `display.tool_progress: off` (enum valid). Setelah edit config profile, restart/install tiap unit profile di VPS: `hermes --profile <profile> gateway install` lalu `hermes --profile <profile> gateway restart`/`start`, kemudian verifikasi `hermes profile list` dan `systemctl --user list-units "hermes-gateway*"`.
- Dalam sesi agent dengan approval-gate aktif, teks user seperti "approval/aproval" di chat **tidak otomatis** membuka blokir command berisiko (stop/start/restart service).
  - Indikasi: tool result mengembalikan `BLOCKED: User denied` meskipun user sudah mengiyakan via chat.
  - Tindakan benar: minta user menyetujui prompt approval native sistem/UI pada saat command dieksekusi, lalu ulangi command setelah approval UI diberikan.
  - Jangan loop retry agresif saat status masih `BLOCKED`; tunggu approval native dulu agar tidak membuang iterasi.
- Saat user mengubah "SOUL" lewat chat bot, agent bisa salah menulis ke file template/global (mis. `~/.hermes/hermes-agent/hermes_cli/default_soul.py`) alih-alih profile aktif.
  - Patokan benar: profile aktif harus tersimpan di `~/.hermes/profiles/<profile>/SOUL.md`.
  - Verifikasi pasca-perubahan dengan hash lokal vs VPS (`sha256sum`) agar identitas profile benar-benar sinkron.

## Sinkronisasi berkelanjutan (opsional, source -> VPS)
Jika user ingin perubahan di mesin sumber otomatis tercermin di VPS:
1. Siapkan SSH key-based auth dulu (hindari password prompt pada job otomatis).
2. Pakai `rsync` terjadwal dengan exclude folder cache/log besar.
3. Setelah sync, restart gateway service di VPS agar config/profile terbaru ter-load.

Contoh pola command:
- `rsync -az --delete --exclude logs/ --exclude image_cache/ --exclude audio_cache/ ~/.hermes/ root@<vps>:/root/.hermes/`
- lalu: `systemctl --user restart hermes-gateway hermes-gateway-<profile1> ...`

Catatan troubleshooting:
- `rsync error code 255` sering karena SSH putus/di-interrupt, auth non-interaktif gagal, atau remote menutup koneksi saat transfer panjang.
- Verifikasi dengan `ssh -o BatchMode=yes ...` sebelum menjadwalkan sync.
- `--contimeout` **tidak valid** untuk mode remote-shell SSH biasa (hanya untuk rsync daemon). Jika dipakai, rsync gagal dengan syntax/usage error.
- Untuk koneksi yang suka putus, tambahkan opsi SSH keepalive pada rsync: `-o ServerAliveInterval=15 -o ServerAliveCountMax=3`.
- Jalankan sync dengan retry terkontrol (mis. 3 percobaan, jeda eksponensial) sebelum menandai gagal.
- Jika menjalankan job panjang, selalu tulis output ke file log dan tampilkan progress (`rsync --info=progress2`) agar user tidak merasa proses "diam".
- Saat memakai background process, pantau berkala (`process poll`/`process log`) dan laporkan status singkat ke user (running/completed/failed).
- Untuk kebutuhan "history lokal dan VPS selalu sama", lebih aman pakai pola dua arah berurutan: pull dari VPS -> push lokal ke VPS untuk folder tertentu (`ops-logs/`, `sessions/`).
- Jika butuh mode hampir real-time untuk **satu profile bot** (mis. `hermes-support`), gunakan daemon loop sinkron cepat (mis. tiap 2 detik) khusus folder profile tersebut, bukan full `~/.hermes`.
  - Praktik yang stabil: `rsync -az --update` dua arah (pull lalu push), exclude `state.db*`, `logs/`, dan lock file cron.
  - Hindari `--delete` pada sinkron dua arah cepat, karena dapat memicu race/tukar-hapus saat perubahan datang dari dua sisi dalam interval rapat.
- Ingat batas arsitektur: jika sinkron dijalankan oleh mesin lokal (cron/daemon lokal), maka saat lokal offline sinkron berhenti sementara; VPS bot tetap jalan, tapi mirror history baru lanjut saat lokal online lagi.
- Jika semua service profile diubah ke `HERMES_HOME` global yang sama (mis. `/root/.hermes`), jangan jalankan banyak `hermes-gateway-*` bersamaan dengan state yang sama. Ini memicu kontensi lock/state dan crash loop (`status=1/FAILURE`, `Start request repeated too quickly`). Untuk mode “1 otak/1 proses”, aktifkan hanya satu service gateway (mis. `hermes-gateway-hermes-support`) dan disable service gateway lain.
- Pada auto-sync, restart service jangan dipicu oleh pola terlalu luas (mis. setiap ada output `>` dari rsync), karena akan menyebabkan restart storm. Trigger restart hanya saat file kritikal berubah (`config.yaml`, `.env`, `auth.json`, `SOUL.md`) dan idealnya restart hanya unit yang dipakai (single gateway aktif), bukan semua unit profile.
- Saat user minta perubahan “1 otak/history/rule” berlaku di lokal + VPS + Telegram untuk satu profile (mis. `hermes-support`), lakukan perubahan di lokal terlebih dulu lalu sinkronkan eksplisit ke VPS dan profile Telegram terkait:
  1) Buat/ubah skill di `~/.hermes/skills/<category>/<skill>/SKILL.md`.
  2) Salin juga ke profile aktif lokal: `~/.hermes/profiles/<profile>/skills/<category>/<skill>/SKILL.md`.
  3) `rsync` kedua file ke VPS global dan profile: `/home/ubuntu/.hermes/skills/...` dan `/home/ubuntu/.hermes/profiles/<profile>/skills/...`.
  4) Verifikasi hash lokal/VPS dengan `sha256sum`.
  5) Jika skill harus selalu aktif untuk profile Telegram, tambahkan ke `~/.hermes/profiles/<profile>/config.yaml` pada `skills.auto_load: [<skill>]` (pertahankan setting hemat token seperti `display.interim_assistant_messages: false` dan `display.tool_progress: off`).
  6) Sinkronkan config profile ke VPS, restart hanya unit profile terkait (`hermes --profile <profile> gateway restart`), tunggu 30-60 detik, lalu verifikasi `hermes profile list`, `systemctl --user is-active`, log terbaru, dan test `hermes --profile <profile> chat -q ... --quiet`.
- Pada auto-sync, restart service jangan dipicu oleh pola terlalu luas (mis. setiap ada output `>` dari rsync), karena akan menyebabkan restart storm. Trigger restart hanya saat file kritikal berubah (`config.yaml`, `.env`, `auth.json`, `SOUL.md`) dan idealnya restart hanya unit yang dipakai (single gateway aktif), bukan semua unit profile.

## Update Hermes lokal + VPS multi-profile
Saat user minta `update hermes` pada setup WSL lokal + VPS-Zeus + multi-profile Telegram:
1. Precheck versi dan status:
   - Lokal: `hermes --version && hermes profile list`
   - VPS: `/home/ubuntu/.local/bin/hermes --version && /home/ubuntu/.local/bin/hermes profile list`
2. Backup sebelum update, minimal `config.yaml`, `.env`, `auth.json`, `profiles/`, `skills/`:
   - Lokal: `(cd ~/.hermes && tar -czf backups/pre_update_local_$(date +%Y%m%d_%H%M%S).tgz config.yaml .env auth.json profiles skills)`
   - VPS: sama di `/home/ubuntu/.hermes/backups/`.
3. Jalankan update lokal dan VPS. `hermes update` bisa butuh approval native karena dapat restart gateway/kill agent.
4. Sebelum update, cek `git status --short` di dalam `~/.hermes/hermes-agent`. Jika ada local changes, JANGAN langsung andalkan auto-stash (stash-pop bisa konflik saat pull ribuan commit). Alih-alih:
   - INSPEKSI dulu: `git diff HEAD -- <file>` untuk tiap `M`. Sering ternyata perubahan itu junk/superseded — mis. `M gateway/platforms/qqbot/adapter.py` yang cuma 1 baris gaya-upstream, atau puluhan `D` file aset (font woff2, infographic png, contoh skill) hasil disk-cleanup yang akan dikembalikan oleh pull.
   - Jika semua perubahan junk/superseded (bukan hotfix custom user), bersihkan tree dulu setelah minta izin (destruktif): `git reset --hard HEAD && git clean -fd`. Repo kode 100% bisa dipulihkan dari GitHub; data user (config/.env/auth/profiles) TIDAK tersentuh karena bukan bagian repo.
   - PITFALL `git clean -fd`: bisa menghapus file untracked penanda seperti `.install_method`. Ini ternyata harmless (updater deteksi metode install via path venv), tapi INSPEKSI untracked (`git status --short | grep '^??'`) sebelum clean agar tidak kaget.
   - Jika tetap memilih auto-stash dan updater berakhir `Update complete`, lanjutkan verifikasi; jangan langsung rollback. Catat stash ref, cek `git status` setelahnya.
   - `hermes update` jalan lama (pull ribuan commit + build web UI, ~5-6 menit untuk gap besar). Jalankan sebagai BACKGROUND job dengan notify_on_complete, pantau tahap log: fetch -> pull -> deps -> refresh backend -> build web UI (tsc+vite, paling lama) -> sync skills -> migrasi config -> drain+restart gateway. Updater juga otomatis bikin pre-update snapshot (`<ts>-pre-update`) sebagai jaring pengaman ekstra.
5. Jalankan `hermes doctor --fix` di lokal dan VPS setelah update. Pada update v0.10.0 → v0.14.0, ini memigrasi config v22 → v23 dan menambahkan default curator/auxiliary.curator.
6. Restart gateway setelah migrasi config:
   - CATATAN: versi updater terbaru (terlihat pada update ke v0.19.0) sudah OTOMATIS drain (graceful, up to 195s) + restart SEMUA unit gateway di akhir `hermes update` — tidak perlu restart manual. Cukup verifikasi.
   - Jika perlu restart manual (versi lama / gateway tak ikut ter-restart):
     - default: `/home/ubuntu/.local/bin/hermes gateway restart`
     - profile: `/home/ubuntu/.local/bin/hermes --profile <profile> gateway restart`
     - Jika status sementara `activating`, tunggu 30-60 detik lalu cek ulang.
7. Verifikasi akhir:
   - `/home/ubuntu/.local/bin/hermes profile list` menunjukkan semua profile `running`.
   - `systemctl --user is-active hermes-gateway*.service` active.
   - Test provider/profile: `/home/ubuntu/.local/bin/hermes --profile hermes-support chat -q "Jawab persis: OK FINAL" --quiet` harus menjawab OK.
   - Cek log window terbaru untuk `error|exception|traceback|No Codex|401|400|429|conflict|not supported`.

Pitfalls update:
- "Up to date" bisa FALSE NEGATIVE. Terlihat saat lokal v0.17.0 melaporkan "Up to date" padahal VPS sudah v0.18.2 dan remote jauh lebih baru. Penyebab: ref `origin/main` lokal basi (belum di-fetch), jadi `git rev-list --count HEAD..@{u}` = 0. Buktikan versi asli dengan `git fetch --dry-run` (menampilkan range commit baru mis. `b699d27a4..76e17bc32 main`) sebelum menyimpulkan "sudah terbaru". Update tetap perlu dijalankan.
- Setelah update, `hermes --version` bisa sudah naik (mis. v0.14.0) tetapi tetap menampilkan `Update available: ... commits behind`; jangan pakai pesan itu sebagai satu-satunya indikator gagal. Verifikasi fungsional lewat doctor/profile/gateway/chat-test.
- Migrasi config bisa lompat banyak versi sekaligus (terlihat: lokal v24 -> v31 dalam sekali update ke v0.19.0). `hermes doctor --fix` / updater menangani ini otomatis; verifikasi `hermes profile list` + gateway active sesudahnya.
- `hermes doctor --fix` perlu dijalankan di kedua environment (lokal dan VPS); update kode saja belum tentu migrasi config aktif.
- Update dapat meninggalkan file generated/untracked atau modified lockfile (`web/package-lock.json`, `uv.lock`, docs/tests/tools baru). Jika Hermes berjalan sehat, catat sebagai repo cleanliness issue terpisah, bukan blocker Telegram.

## Rollback cepat
- Stop service gateway di VPS.
- Restore backup `~/.hermes` lama di VPS.
- Start ulang service yang lama.
- Jika perlu, aktifkan lagi gateway di mesin sumber sementara.