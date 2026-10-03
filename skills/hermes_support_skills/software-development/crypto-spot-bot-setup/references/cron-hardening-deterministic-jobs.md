# Cron hardening untuk bot trading (deterministik)

## Gejala umum
- Cron mengirim respons yang tidak menjalankan command asli (contoh: mencoba `default_api` atau mengubah path python).
- Cron gagal memuat env karena `source` tidak tersedia di shell.
- Job lama masih nyangkut setelah edit/remove (instance gateway lama belum terganti).

## Pola fix yang stabil
1. Untuk eksekusi script murni, pakai **job script-only / no-agent** bila tersedia.
2. Jika masih memakai prompt job agent:
   - kunci command exact,
   - minta satu tool saja (`terminal`),
   - larang reinterpretasi command.
3. Jangan bergantung `source .../.env` di prompt cron; load `.env` di script Python.
4. Setelah edit/remove job, restart gateway profile bot dengan replace agar instance lama tidak carry state.
5. Verifikasi hasil dengan run manual sekali sebelum menunggu tick rutin.

## Checklist verifikasi
- Python executable path benar dan executable.
- Script bisa jalan manual dari profile trading.
- Last run cron = ok.
- Pesan yang masuk ke Telegram sesuai format yang diinginkan.
