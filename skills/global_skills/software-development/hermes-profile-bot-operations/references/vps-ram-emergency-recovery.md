# VPS RAM Emergency Recovery

## Deteksi

```bash
# SSH timeout "during banner exchange"
ssh -o ConnectTimeout=10 user@VPS_IP "echo OK"
# → "Connection timed out during banner exchange"

# Tapi ping OK + port 22 terbuka
ping -c 1 VPS_IP          # ✅ sukses
nc -zv -w5 VPS_IP 22      # ✅ port 22 terbuka
```

Ini berarti VPS **hidup** tapi **sshd tidak bisa fork** karena RAM habis.

## Recovery via VNC Console

Satu-satunya cara masuk adalah via VPS provider console (Tencent Cloud, AWS, dll):

```bash
# Setelah login VNC
# 1. Cek kondisi
free -h
# total=1.9Gi, used=1.8Gi, available=<200MB → kritis

# 2. Bersihkan cache pagecache (aman, data ga hilang)
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches

# 3. Cek swap
swapon --show
# Kalau swap penuh 2Gi/2Gi → perlu dikosongkan

# 4. Kosongkan swap — tapi HANYA jika available RAM > swap used!
sudo swapoff -a && sudo swapon -a

# 5. Restart sshd
sudo systemctl restart sshd

# 6. Cek proses boros
ps aux --sort=-%mem | head -10
```

## ⚠️ CRITICAL: Jangan pernah swapoff dari gateway Telegram

Perintah `sudo swapoff -a` dari **gateway Telegram** (lewat hermes-support) bisa menyebabkan **VPS hang total**.

**Kenapa beda dari SSH:**
- SSH dari WSL: client di luar VPS, tidak terpengaruh OOM
- Gateway Telegram: proses hermes-support berjalan DI DALAM VPS → **ikut kena OOM** saat RAM habis
- Akibat: gateway mati + SSH hilang → VPS tidak bisa diakses sama sekali → perlu restart dari console

**Aturan:**
- swapoff hanya dari SSH langsung (bukan dari gateway agent)
- Dari Telegram cukup clear cache: `sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches`
- Alternatif: restart VPS dari console untuk reset total

## Identifikasi Service Critical vs Non-Critical

Saat darurat RAM, jangan asal matikan service:

### WAJIB jalan (JANGAN di-stop tanpa instruksi sir):
| Service | Fungsi |
|---------|--------|
| nginx | Web server + reverse proxy untuk semua app |
| **next-server (port 20128)** | **9router dashboard/API — provider LLM SEMUA profile** |
| mysqld | Database Clario CRM + MenyalaAi |
| fail2ban | Security |
| hermes-gateway-* | Semua 8 profile gateway |

**⚠️ 9router berjalan sebagai `next-server` (v16.2.1), listening di port 20128.** Jika melihat proses `next-server` yang makan 80MB+, INI ADALAH 9ROUTER — jangan dimatikan. Ini adalah LLM proxy yang dipakai oleh SEMUA profile gateway Hermes.

### Bisa di-stop/dihapus saat darurat:
| Service | Efek free |
|---------|-----------|
| Docker | ~100MB + disk |
| PostgreSQL | ~50MB (jika db project sudah dihapus) |
| ModemManager | ~10MB (tidak berguna di VPS) |
| Clario artisan serve | ~50MB (Laravel CRM, jika tidak dipakai) |
| MenyalaAi | ~30MB (Flask app, jika tidak dipakai) |

## Pitfall: swapoff timeout karena RAM tidak cukup

Jika `available RAM < swap used`, `sudo swapoff -a` akan **hang** karena kernel tidak bisa memindahkan swap content ke RAM yang penuh.

**Ciri:** Command `sudo swapoff -a` berjalan >30 detik tanpa output (timeout di SSH).

**Fix bertahap:**

1. **Jangan paksa swapoff** — kill proses boros dulu:
   ```bash
   # Cari proses dengan RES tertinggi (selain gateway yang perlu jalan)
   ps aux --sort=-%mem | head -15
   
   # Kill MySQL sementara jika tidak dibutuhkan
   sudo systemctl stop mysql
   
   # Atau kill proses non-esensial lain
   sudo kill -9 <PID>
   ```

2. **Cek available RAM naik**:
   ```bash
   free -h
   ```

3. **Baru swapoff** setelah available RAM > swap used:
   ```bash
   sudo swapoff -a && sudo swapon -a
   ```

4. **Hidupkan kembali** service yang dimatikan:
   ```bash
   sudo systemctl start mysql
   ```

**Alternatif:** Biarkan swap penuh — VPS tetap stabil meski lambat. Swap hanya masalah performa, bukan stabilitas. Yang penting gateway tetap jalan.

## Pencegahan Jangka Panjang

- **Upgrade RAM VPS** — 1.9GB terlalu kecil untuk 8 gateway Hermes + MySQL. Minimal 4GB.
- **Kurangi jumlah profile** — setiap gateway makan ~140MB RAM.
- **Matikan service tidak esensial** — Docker, ModemManager, PostgreSQL, project folder besar.
- **Cron pembersihan RAM** — periodic `drop_caches` + restart service berat.
- **Batch restart menyebabkan memory crash** — restart >3 profile bersamaan bisa bikin memory spike hingga SSH hilang. Restart satu per satu dengan jeda 5 detik dan verifikasi memory tiap langkah.
