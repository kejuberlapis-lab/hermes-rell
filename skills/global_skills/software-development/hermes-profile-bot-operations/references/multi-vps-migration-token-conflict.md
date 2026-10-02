# Multi-VPS Migration: Telegram Token Conflict

Playbook untuk kasus dua VPS berbeda rebutan satu token bot Telegram — biasanya
muncul saat sir migrasi ke VPS baru tapi VPS lama masih jalan.

## Kronologi sesi referensi (12 Jul 2026)

Gejala: sir lapor "hermes-support tidak respon". Ternyata bukan mati total —
bot kadang balas kadang tidak.

Root cause: sir migrasi ke VPS baru (43.134.179.61). VPS-Zeus lama
(43.134.233.101) masih menjalankan 8 gateway dan ikut polling token yang sama.

### Yang ditemukan di tiap host

VPS baru (43.134.179.61) — SEHAT:
- hermes-support baru balas pesan sir ("halo" → 2.9s, "Gimana cara nya" → 0.4s)
- 9router aktif port 20128, RAM 7.5GB, 8 gateway user service
- kena polling conflict berulang

VPS lama (43.134.233.101):
- proses lama PID 379964 macet 1 jam, pegang gateway.lock, stuck loop conflict
- root systemd service loop `Gateway already running (PID 379964)` status=1/FAILURE
- state Telegram basi ~46 menit (updated_at tidak maju)

### Aksi (setelah approval sir)

VPS lama di-decommission:
```
sudo systemctl stop hermes-gateway-hermes-support.service
sudo systemctl disable hermes-gateway-hermes-support.service   # root service = biang loop
for p in hermes-support ais avrel-jago profil-admin-mvp profil-admin-node-b \
         profil-admin-olo profil-admin-plus profil-admin-rofc; do
  systemctl --user stop hermes-gateway-$p.service
done
# verifikasi: ps aux | grep 'gateway run' | grep -v grep  → 0 baris
```

### Verifikasi konflik berhenti

- Waktu server VPS baru: 15:31:59 CST
- Conflict terakhir semua profile mentok di 15:28–15:29 (persis saat proses VPS
  lama sekarat)
- Tunggu ~2-3 menit, timestamp conflict TIDAK maju lagi → resolved

## Checklist ringkas (reusable)

1. [ ] Konek ke KEDUA VPS, bandingkan kesehatan (inbound/response terbaru,
       9router, RAM, gateway state). Pilih yang sehat sebagai primary.
2. [ ] Approval sir sebelum matikan gateway massal.
3. [ ] Di VPS decommission: stop+disable ROOT service → stop semua USER service
       → verifikasi 0 proses.
4. [ ] Tunggu ~60s, cek timestamp conflict terakhir vs `date` server. Tidak maju
       = beres.
5. [ ] Update memory: primary baru + lama decommissioned. Satu token = satu VPS.

## Catatan penting

- Telegram getUpdates lease expiry ~20-50s → conflict sisa setelah kill itu wajar.
- Jangan filter log pakai UTC (`date -u`) kalau log ditulis waktu lokal — false
  negative. Baca timestamp asli, bandingkan sesama waktu server.
- SSH ke VPS password-only dari WSL: paramiko via `uv run --with paramiko`,
  password lewat env var. Jangan `sleep` panjang di dalam blok SSH yang dibungkus
  `timeout` pendek.
