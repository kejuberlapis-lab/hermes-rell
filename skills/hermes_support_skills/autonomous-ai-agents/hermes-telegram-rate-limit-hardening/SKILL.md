---
name: hermes-telegram-rate-limit-hardening
description: Hardening Hermes Telegram profile agar lebih tahan 429/rate-limit dengan fallback model, pengurangan token burn, dan verifikasi log pasca-deploy.
version: 1.1.0
author: Hermes Agent
license: MIT
---

# Hermes Telegram Rate-Limit Hardening

Gunakan skill ini saat bot Telegram Hermes sering lambat, diam, atau kena 429 (rate-limit) pada model utama.

## Kapan dipakai
- Ada log HTTP 429 / rate-limit dari provider model.
- Bot respons intermiten saat traffic naik.
- User minta bot “lebih tahan limit” tapi tetap ringkas dan konsisten.

## Prasyarat
1. Gateway profile sudah berjalan (systemd user service).
2. Anda tahu path profil target:
   - `~/.hermes/profiles/<profile>/config.yaml`
3. Restart service profil tersedia:
   - `hermes-gateway-<profile>.service`

## Prosedur inti
1. Kurangi beban percakapan per request di profil target:

   ```yaml
   agent:
     max_turns: 35
     reasoning_effort: minimal
   ```

   Catatan: menurunkan `max_turns` biasanya menurunkan konsumsi token dan peluang kena limit pada sesi panjang.

2. Tambahkan fallback model ringan:

   ```yaml
   model:
     provider: openai-codex
     default: gpt-5.3-codex

   fallback_model:
     provider: openai-codex
     model: gpt-4.1-mini

   fallback_providers: []
   ```

   Catatan pengalaman:
   - `fallback_model` efektif sebagai jalur cadangan saat model utama gagal/limit.
   - Jika runtime tertentu tidak trigger fallback saat `fallback_providers` kosong, isi provider fallback eksplisit sesuai dokumentasi runtime yang dipakai.

3. Paksa gaya jawaban hemat token lewat channel prompt Telegram (per allowlisted user atau global channel prompt):
   - Jawaban maksimal 3–5 bullet singkat.
   - Hindari paragraf panjang kecuali diminta.
   - Jika ambigu, tanya 1 klarifikasi singkat.

4. Restart gateway profil:

   ```bash
   systemctl --user restart hermes-gateway-<profile>.service
   systemctl --user status hermes-gateway-<profile>.service --no-pager
   ```

5. Jika diminta berlaku ke banyak bot/profil, terapkan perubahan yang sama ke setiap `config.yaml` profil target (mis. `node-b`, `olo`, `mvp`, `plus`) lalu restart service masing-masing.
   - Jangan asumsikan satu profil otomatis mewarisi profil lain.
   - Verifikasi tiap file setelah edit (`fallback_model` + `max_turns`) sebelum restart.
   - Pastikan nama unit systemd benar dengan discovery dulu:

   ```bash
   systemctl --user list-units 'hermes-gateway*' --no-pager
   ```

   Catatan pengalaman: profil bernama `hermes-support` bisa berjalan di unit default `hermes-gateway.service` (bukan `hermes-gateway-hermes-support.service`). Jika restart unit yang salah, akan muncul `Unit ... not found` dan profil terkait tidak ikut ter-restart.

## Verifikasi pasca deploy
1. Pastikan service aktif:

   ```bash
   systemctl --user is-active hermes-gateway-<profile>.service
   ```

2. Pantau log rate-limit/fallback:

   ```bash
   journalctl --user -u hermes-gateway-<profile>.service -n 200 --no-pager
   ```

3. Uji chat nyata setelah deploy (penting):
   - Kirim beberapa prompt beruntun dari user allowlist.
   - Konfirmasi bot tetap membalas konsisten/ringkas.
   - Jika masih diam/timeout, cek log lagi untuk 429 berulang atau error provider fallback.

## Pitfalls
- Jangan set nilai enum display yang invalid (mis. `display.tool_progress: none`) karena bisa membuat startup gagal (`status=75/TEMPFAIL`).
- Uji 429 sulit dipaksa on-demand; validasi terbaik adalah monitoring log saat traffic real.
- Fallback model harus benar-benar tersedia pada provider aktif; jika tidak, fallback akan gagal diam-diam sebagai error lanjutan di log.
- Pada `openai-codex` dengan akun ChatGPT/Codex, `gpt-4.1-mini` dapat gagal sebagai fallback (pernah muncul error unsupported/BadRequest). Jika log menunjukkan fallback `gpt-4.1-mini via openai-codex` gagal, hapus `fallback_model` dari profile atau ganti ke model Codex yang benar-benar didukung, lalu restart gateway.
- Saat memperbaiki auth Codex (`HTTP 401 token_invalidated`), hapus credential Codex lama yang invalid dari `hermes auth list` setelah menambah credential baru. Jika credential lama masih menjadi aktif (`←`), service bisa tetap 401 walau re-auth sudah berhasil.
- Pada environment dengan approval gate, restart service bisa diblokir dengan pesan `BLOCKED: User denied. Do NOT retry.`. Saat ini terjadi:
  1) minta approval eksplisit user untuk aksi restart, atau
  2) minta user jalankan restart manual lalu kirim output `is-active` untuk verifikasi.

## Rollback cepat
- Kembalikan `max_turns` ke nilai sebelumnya.
- Hapus/ubah `fallback_model` ke konfigurasi valid lama.
- Restart service profil dan cek status/log lagi.
