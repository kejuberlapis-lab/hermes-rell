---
name: crypto-spot-trading-automation
description: Workflow aman untuk setup dan operasi trading otomatis crypto spot via API (fokus Binance), termasuk mode paper/live, risk gate, dan manajemen asymmetric key.
version: 1.0.0
author: Hermes Agent
---

# Crypto Spot Trading Automation

Gunakan skill ini saat user ingin membangun atau mengoperasikan bot trading **spot** yang bisa analisa market dan eksekusi order via API.

## Prinsip inti
1. Mulai dari **spot-only** (hindari leverage/futures pada fase awal).
2. Default ke **paper/simulasi dulu**, baru live kecil.
3. Terapkan risk gate sebelum order: risk per trade, max daily loss, max posisi, cooldown.
4. Credential hygiene: API key read/trade only, withdraw OFF, secret tidak pernah ditampilkan.

## Urutan kerja standar
1. Konfirmasi exchange target (default: Binance).
2. Setup API permission aman:
   - Enable: Read, Spot Trading
   - Disable: Withdraw
   - (Opsional) IP whitelist jika sudah pakai VPS tetap.
3. Jika pakai **asymmetric key**:
   - Generate private/public key pair sekali.
   - Upload **public key** ke exchange.
   - Simpan private key lokal dengan permission ketat.
4. Verifikasi read-only endpoint signed sebelum live trading.
5. Jalankan paper trading (7–14 hari), evaluasi metrik (winrate, drawdown, expectancy).
6. Baru aktifkan live dengan ukuran kecil dan guardrail tetap aktif.

## Pitfalls penting
- **Jangan regenerate key pair tanpa sengaja** setelah public key sudah terdaftar di exchange.
  - Jika key pair berubah, public key di exchange juga harus diganti.
  - Jika user ingin tetap pakai public key lama, private key pasangannya wajib tersedia di host.
- Untuk exchange yang pakai HMAC (mis. Bybit/OKX), **tidak perlu RSA public/private key**. Gunakan API key + secret sesuai docs exchange.
- Jangan kirim/echo API key, private key, seed, token ke chat.
- Jangan langsung live sebelum lolos uji signed read-only + paper trading.

## Operasional bot terpisah (wajib untuk reliability)
1. Gunakan **profile Hermes terpisah** untuk bot trading (mis. `trading-bot`) agar env/config/cron tidak mengganggu asisten utama.
2. Simpan credential trading hanya di `.env` profile bot tersebut.
3. Set provider model profile bot ke provider yang siap pakai (mis. OpenRouter) untuk menghindari auth error runtime pada cron/gateway.
4. Untuk job analisa berkala, hindari prompt yang bergantung pada `source` shell; lebih stabil jika script Python membaca `.env` langsung.
5. Jika cron hanya perlu menjalankan command deterministik, pakai instruksi yang memaksa satu command exact (atau mode script-only/no-agent jika tersedia) agar tidak terjadi halusinasi eksekusi (contoh salah pakai `default_api`).

## Standar respons saat user kirim secret
- Terima eksekusi yang diminta.
- Samarkan secret di output.
- Ingatkan singkat soal keamanan (rotate/revoke) tanpa memaksa jika user menolak.

## Mode komunikasi untuk user yang minta "analisa dulu"
Jika user menegaskan gaya "jangan langsung kasih langkah berikutnya", gunakan pola ini:
1. Mulai dari **analisa arah/tujuan** user terlebih dahulu (apa yang mau dicapai, horizon waktu, toleransi risiko).
2. Berikan **diagnosis + opsi** tanpa langsung mengeluarkan checklist aksi.
3. Hindari menutup jawaban dengan CTA otomatis seperti "ketik X untuk lanjut" kecuali user minta.
4. Keluarkan langkah detail hanya saat user memberi trigger eksplisit: "kasih langkah", "eksekusi", atau padanan jelas.
5. Untuk topik modal kecil (mis. $10), tekankan realisme probabilitas dan risk containment, bukan janji hasil.

## Referensi
- Lihat `references/binance-asymmetric-key-runbook.md` untuk runbook detail setup/verifikasi asymmetric key Binance.
- Lihat `references/bybit-profile-cron-hardening.md` untuk pola bot terpisah + hardening cron analyze-only pada Bybit.
