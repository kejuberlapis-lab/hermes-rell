# Bybit Minimal Setup (Modal Kecil, Analyze-Only Dulu)

## Tujuan
Membuat baseline bot spot yang aman untuk modal kecil (contoh $10) tanpa langsung eksekusi order.

## Checklist API
- Buat API key Bybit.
- Permission:
  - Read: ON
  - Spot Trade: ON
  - Withdraw: OFF
- Aktifkan IP whitelist jika infrastruktur sudah tetap.

## Env minimal
- `BYBIT_API_KEY`
- `BYBIT_API_SECRET`

## Verifikasi read-only
1. Jalankan script koneksi read-only.
2. Hasil minimal yang diharapkan: koneksi OK dan akun terbaca.
3. Jika gagal, stop rollout live dan perbaiki auth dulu.

## Analyze-only baseline
- Pantau 1-3 pair dulu (contoh BTC/USDT, ETH/USDT, XRP/USDT).
- Timeframe awal: 15m.
- Output: trend + signal, tanpa place order.

## Isolasi profile
- Buat profile khusus bot trading agar tidak ganggu asisten utama.
- Simpan env dan cron di profile bot tersebut.

## Jadwal aman
- Cron tiap 5 menit untuk analisa.
- Kirim ringkasan singkat ke channel asal.

## Catatan operasional
- Saat ganti exchange, hapus key/env exchange lama terlebih dulu.
- Jangan menampilkan ulang nilai API key/secret dalam output.
