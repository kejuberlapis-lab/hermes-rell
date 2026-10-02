# Bybit profile split + cron hardening (ringkas)

## Tujuan
Menjalankan bot analisa market Bybit secara terpisah dari asisten utama, stabil di Telegram, dan minim false error.

## Pola yang terbukti
1. Buat profile terpisah (`trading-bot`).
2. Simpan `BYBIT_API_KEY` + `BYBIT_API_SECRET` hanya di `.env` profile tersebut.
3. Verifikasi read-only via CCXT sebelum cron.
4. Jalankan gateway profile bot sendiri.
5. Untuk cron analisa, gunakan command Python yang fixed ke script analyzer.
6. Script analyzer sebaiknya load `.env` sendiri (hindari ketergantungan `source`).

## Gejala & perbaikan
- Gejala: auth provider gagal pada cron/gateway.
  - Perbaikan: set provider profile bot ke provider valid (mis. OpenRouter) + restart gateway profile tersebut.
- Gejala: cron memberi error shell `source` tidak ada / env tidak kebaca.
  - Perbaikan: load `.env` di script Python, bukan di shell cron.
- Gejala: agent cron mengarang eksekusi (mis. `default_api` undefined).
  - Perbaikan: pakai prompt command-exact deterministik atau mode script-only/no-agent.

## Checklist sebelum live
- Analyze-only stabil beberapa siklus.
- Alert format jelas (pair, trend, signal, timestamp).
- Risk gate siap (max daily loss, max positions, cooldown) sebelum aktifkan order live.
