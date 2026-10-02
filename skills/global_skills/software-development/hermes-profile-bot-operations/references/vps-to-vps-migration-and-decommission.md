# VPS-to-VPS Migration & Safe Decommission

Gunakan saat memindahkan Hermes (multi-profile + 9router) dari satu VPS ke VPS
baru, DAN saat sir minta "hapus VPS lama". Kasus nyata: 12 Jul 2026, migrasi
VPS-Zeus lama (43.134.233.101) → VPS baru (43.134.179.61).

## ⚠️ ATURAN #1: JANGAN hapus VPS lama sebelum audit data non-Hermes

"Hapus VPS lama" adalah aksi **destruktif permanen**. Sebelum menyentuh apa
pun, WAJIB audit — karena VPS produksi biasanya menyimpan JAUH lebih banyak
dari sekadar Hermes.

Kasus nyata: sir bilang "hapus VPS lama" mengira migrasi Hermes = migrasi
segalanya. Ternyata `/home/ubuntu/` menyimpan **~13GB project bisnis**
(clario CRM, mlb-parlay, srs5g-session, evidence_*, backups, dll) yang TIDAK
ikut termigrasi karena bukan bagian Hermes. Kalau langsung dihapus, semua
hilang permanen.

**Prosedur audit wajib sebelum decommission:**
```bash
# 1. Daftar SEMUA folder home + ukuran (di VPS LAMA)
cd ~; for d in */; do du -sh "$d" 2>/dev/null; done | sort -rh

# 2. Daftar folder home di VPS BARU untuk komparasi
ls -d ~/*/ | sed 's|/home/ubuntu/||; s|/$||' | sort

# 3. Yang ADA di lama tapi TIDAK di baru = data unik yang akan HILANG
```
Jangan asumsikan "migrasi Hermes = migrasi semua". Tampilkan tabel data unik
ke sir, minta keputusan eksplisit (backup dulu / hapus Hermes saja / hapus
total / tunda) via clarify SEBELUM aksi destruktif.

## Verifikasi sinkronisasi Hermes (lama vs baru vs local)

Bandingkan tiga hal per lokasi sebelum menyatakan "sudah sinkron":
```bash
# Profiles
ls ~/.hermes/profiles/
# Model default per profile
for p in $(ls ~/.hermes/profiles/); do echo "$p -> $(grep -m1 'default:' ~/.hermes/profiles/$p/config.yaml | sed 's/.*default:[[:space:]]*//')"; done
# Skill count
find ~/.hermes/skills -name SKILL.md | wc -l
# Memory/USER bytes per profile (deteksi drift)
for p in $(ls ~/.hermes/profiles/); do echo "$p M=$(wc -c <~/.hermes/profiles/$p/memories/MEMORY.md 2>/dev/null) U=$(wc -c <~/.hermes/profiles/$p/memories/USER.md 2>/dev/null)"; done
```
**Pitfall:** memory hermes-support kadang root-owned di VPS lama (root
service) → `wc` gagal "Permission denied", TAMPAK 0 byte padahal berisi.
Baca dengan `sudo cat` untuk cek isi sebenarnya, lalu `diff` lama vs baru.
Selisih byte kecil biasanya cuma perbedaan catatan "primary VPS" — cek diff
isinya, jangan panik.

## Teknik transfer VPS-baru ← VPS-lama (rsync langsung, bukan lewat local)

VPS-ke-VPS jauh lebih cepat daripada lewat local. VPS baru biasanya sudah
punya `rsync` + `sshpass`.

**Password auth aman (jangan bocor ke `ps aux`):**
```bash
# ❌ JANGAN: sshpass -p 'password' ...  (password muncul di ps aux)
# ✅ PAKAI: password via env var, sshpass -e
export SSHPASS='<old_vps_password>'
sshpass -e ssh -o StrictHostKeyChecking=no ubuntu@OLD_IP 'echo AUTH_OK'
```

**Pitfall: `~` tidak ter-expand di sisi remote sender.** Kalau kirim banyak
path sekaligus (`ubuntu@old:'~/a ~/b ~/c'`), rsync menggabung jadi satu string
literal → `change_dir failed: No such file`. **Fix: loop per folder dengan
path ABSOLUT + `--relative` dan `/./` marker:**
```bash
export SSHPASS='<pass>'
mkdir -p ~/vps-lama-backup
while read -r d; do
  [ -z "$d" ] && continue
  sshpass -e rsync -az --relative \
    -e "ssh -o StrictHostKeyChecking=no -o ConnectTimeout=15" \
    "ubuntu@OLD_IP:/home/ubuntu/./$d" ~/vps-lama-backup/
done < folder_list.txt
```
Backup ke direktori TERPISAH (`~/vps-lama-backup/`), JANGAN timpa project
aktif yang sudah ada versinya di VPS baru. Jalankan via `nohup ... &` + log
file untuk transfer besar, lalu poll `pgrep -af rsync` + `tail log`.

**File root-owned/700 di sisi lama** (mis. seluruh `~/.hermes/` dari root
service): rsync biasa akan skip / permission denied. Fix: `--rsync-path="sudo -n rsync"`
agar rsync di remote jalan sebagai root (butuh passwordless sudo di VPS lama —
cek dulu `sudo -n true`).

## ⚠️ Pitfall workflow: JANGAN gabung `sleep` panjang + SSH dalam satu command

Saat memantau transfer background, godaan untuk `sleep 90; ssh ... 'cek status'`.
Ini SALAH — foreground tool punya batas ~60 detik, jadi `sleep 65/90` + koneksi
SSH pasti timeout (exit 124) walau transfer sendiri baik-baik saja. Sir menegur
langsung soal ini ("sleep tadi untuk apa?").

**Pola benar untuk poll background job:**
- Cek cepat sekali jalan (tanpa sleep): `pgrep -f rsync | wc -l` + `du -sh` + `tail log`.
- Kalau perlu jeda, taruh loop jeda PENDEK di sisi REMOTE dan jaga total < ~50s:
  ```bash
  # di dalam SATU ssh call, total < 50s:
  for n in $(seq 1 6); do c=$(pgrep -f 'rsync.*OLD_IP'|grep -v grep|wc -l); \
    [ "$c" = 0 ] && { echo DONE; break; }; sleep 7; done; \
    echo "size=$(du -sh ~/dest|cut -f1) exit=$(grep -oE 'EXIT=[0-9]+' log)"
  ```
- Jangan poll tiap 3-5 detik berturut-turut (boros). Jeda internal ~40-45s per cek.

## Verifikasi integritas backup — file count, BUKAN cuma ukuran

**Pitfall: backup bisa JUSTRU lebih besar dari sumber, dan itu NORMAL.**
rsync tanpa flag `-H` memecah hardlink jadi file terpisah → ukuran `du` naik
(mis. clario 239MB→250MB). Ini bukan korupsi; data justru lengkap.

Verifikasi yang benar = bandingkan **jumlah file**, bukan byte:
```bash
# kedua sisi harus sama
find . -type f | wc -l       # file count
find . -type l | wc -l       # symlink count
find . -type f -links +1 | wc -l   # hardlink count (beda antar sisi = wajar)
```
File count + symlink count identik = backup utuh, aman untuk hapus sumber.

## Verifikasi arsip = versi TERAKHIR sumber + tidak ada folder ganda

Sir minta eksplisit: "pastikan isinya file terakhir dari VPS" dan "tidak
double folder". Dua cek wajib:

**1. Isi = versi terakhir (bukan snapshot basi):** bandingkan mtime + size
file kunci kedua sisi, plus 10 file termodifikasi terakhir.
```bash
# jalankan di kedua sisi, bandingkan output:
stat -c '%Y %s' <path>/state.db                 # mtime epoch + size
find <path> -type f -printf '%T@ %p\n' | sort -rn | head -10
```
mtime + size identik = arsip menangkap keadaan terakhir. state.db (history
percakapan) adalah indikator terbaik karena selalu berubah saat bot aktif.

**2. Tidak ada folder bersarang ganda** (kesalahan rsync trailing-slash klasik):
```bash
ls -d ~/vps-lama-backup/hermes-lama/hermes-lama 2>/dev/null && echo GANDA! || echo OK
```
Pakai `src/` (trailing slash) → isi src masuk langsung ke dest. Tanpa slash →
`dest/src/...`. Selalu verifikasi struktur top-level setelah selesai.

**Pitfall heredoc quote-conflict via SSH:** script perbandingan yang pakai
`awk '{print $1}'` / `find -printf '...'` dengan single-quote sering pecah saat
dibungkus `ssh remote 'bash << EOF ...'` (`unexpected EOF looking for matching '`).
Fix: tulis script ke FILE (`sftp put` / `scp`), lalu jalankan
`ssh remote 'bash /tmp/cmp.sh <arg>'`. Bebas masalah escaping.

## Active vs Archive — jangan over-archive data Hermes yang redundan

Sir menantang: "apa guna arsip? kan mau jalankan semua di VPS baru." Pisahkan
dua konsep dengan tegas:
- **AKTIF** (`~/.hermes/`): profile/skill/memory/config LIVE yang menjalankan
  bot. Sudah beres via sync, TIDAK tergantung arsip.
- **ARSIP** (`~/vps-lama-backup/`): jaring pengaman, BUKAN untuk operasional.

Yang benar-benar tak tergantikan = **data non-Hermes** (project bisnis) yang
tidak ikut migrasi. Arsip data Hermes lama (state.db/log/sessions) sebagian
besar REDUNDAN dengan yang sudah live di VPS baru — gunanya cuma "kalau mau
lihat history lama". Tawarkan ke sir untuk buang arsip Hermes redundan &
simpan hanya project bisnis, biar disk efisien. Jangan menyalin puluhan ribu
file skill per-profile "demi kelengkapan" tanpa mengonfirmasi nilainya dulu.

## Sync skill ke LOCAL (yang tidak punya sshpass)

Local WSL sering tidak punya `sshpass`/`sudo` yang cocok. Pakai paramiko via
`uv run --with paramiko` + SFTP:
1. Di VPS: `tar czf /tmp/skills_sync.tgz -C ~/.hermes/skills <daftar folder>`
2. SFTP `.get()` tarball ke local
3. Ekstrak dengan **keep-existing** agar TIDAK menimpa skill yang baru
   dipatch di local:
   ```bash
   tar xzkf /tmp/skills_sync.tgz -C ~/.hermes/skills   # -k = keep existing
   ```
**Pitfall:** jangan overwrite skill yang sudah ada di local — bisa menimpa
patch lokal yang lebih baru dengan versi lama VPS. Hitung union: local_final =
skill_vps + skill_unik_local. Verifikasi patch penting masih ada
(`grep -l '<marker>' <skill file>`).

## Guardrail

- Password VPS lama/baru dari sir dipakai per-sesi via env; jangan simpan ke
  memory/log, jangan echo ke terminal.
- Aksi destruktif (hapus VPS, rm -rf project) HANYA setelah backup terverifikasi
  DAN approval eksplisit sir via clarify.
- Satu token Telegram = satu VPS. Saat migrasi, stop+disable SEMUA gateway di
  VPS lama sebelum VPS baru jadi runner tunggal (lihat
  `telegram-gateway-recovery-vps-primary.md`).
