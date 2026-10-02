---
name: crypto-spot-bot-setup
description: Setup bot trading crypto spot secara aman dengan API exchange, isolasi profile Hermes, mode analyze-only dulu, lalu rollout bertahap ke live trading.
version: 1.0.0
author: Hermes Agent
---

# Crypto Spot Bot Setup

Gunakan skill ini saat user ingin membangun bot trading spot otomatis (Bybit/OKX/Binance/dll) via API.

## Trigger
- User minta setup API exchange untuk bot.
- User minta analisa market otomatis + opsi eksekusi order.
- User ingin bot terpisah agar tidak mengganggu asisten utama.

## Prinsip wajib
1. **Keamanan dulu**: jangan tampilkan/ulang API key dan secret di chat.
2. **Permission minimal**: Read + Spot Trade, **tanpa Withdraw**.
3. **Isolasi operasional**: gunakan profile Hermes terpisah untuk trading.
4. **Rollout bertahap**: Analyze-only → paper/simulasi → live kecil.
5. **Fail-safe**: daily loss cap, max posisi, kill switch.

## Runbook cepat
1. Tentukan exchange yang cocok modal kecil user (cek minimum order per pair).
2. Siapkan API key dengan permission minimal dan IP whitelist bila memungkinkan.
3. Buat profile bot terpisah:
   - `hermes profile create <nama-bot> --clone`
4. Bersihkan kredensial exchange lama saat user pindah exchange.
5. Pasang script `analyze-only` dulu (tanpa order).
6. Jalankan verifikasi read-only API.
7. Jadwalkan analisa periodik via cron (mis. 5 menit).
   - Untuk job deterministik (hanya menjalankan script), **utamakan cron mode no-agent/script-only** agar tidak ada interpretasi LLM yang mengubah command.
   - Hindari prompt cron yang bergantung pada `source` shell; lebih stabil jika script Python memuat `.env` sendiri.
8. Lakukan handoff konteks ke profile trading bot: simpan ringkasan operasional ke file profile (mis. `TRADING_HANDOFF_CONTEXT.md`) dan patch `SOUL.md` agar bot merujuk env/guardrail/script lokal profile trading.
9. Hanya aktifkan order live setelah user approve eksplisit.

## Pitfalls
- Jangan lanjut eksekusi order saat koneksi API belum lolos read-only check.
- Jangan campur env bot utama dan bot trading.
- Saat pindah exchange, hapus env/key lama untuk menghindari salah endpoint/salah kredensial.
- Jika muncul `authentication failed` di bot, jangan langsung asumsi API exchange salah: cek dulu runtime model provider profile bot (seringnya masih mengarah ke provider lain yang butuh auth terpisah).
- Jangan pakai `/start` sebagai indikator health utama Hermes gateway; command itu bisa dianggap unknown command. Gunakan pesan teks biasa untuk uji respons end-to-end.

## Troubleshooting cepat: bot jalan tapi auth gagal
1. Verifikasi API exchange dulu dengan script read-only (pastikan masalah bukan di exchange).
2. Cek config profile bot trading (bukan profile utama):
   - `model.provider`
   - `model.default`
   - `fallback_providers`
3. Untuk setup OpenRouter-only yang stabil di bot terpisah:
   - set `model.provider: openrouter`
   - set `model.default: openrouter/auto`
   - set `fallback_providers: ["openrouter"]`
4. Restart gateway profile bot dengan replace agar instance lama tidak bentrok.
5. Uji dari Telegram memakai pesan teks biasa (`tes`, `cek market`) lalu cek log jika perlu.

## Output yang disarankan ke user
- Status koneksi API (OK/GAGAL)
- Mode saat ini (ANALYZE_ONLY / PAPER / LIVE)
- Pair yang dipantau
- Jadwal cron aktif

## Referensi skill
- `references/bybit-minimal-setup.md` — alur praktis Bybit modal kecil + checklist verifikasi
- `references/hermes-gateway-auth-failure-pattern.md` — pola diagnosis saat exchange API OK tapi auth bot gagal di runtime provider model
- `references/cron-hardening-deterministic-jobs.md` — hardening cron untuk job trading deterministik (hindari reinterpretasi LLM/default_api, stabilisasi env/path)
- `references/profile-trading-bot-context-handoff.md` — cara memindahkan konteks operasional trading ke profile bot terpisah (SOUL + handoff file + probe verifikasi)
