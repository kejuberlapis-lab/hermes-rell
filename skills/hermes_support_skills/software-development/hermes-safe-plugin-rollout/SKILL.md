---
name: hermes-safe-plugin-rollout
description: Rollout plugin Hermes secara selektif, aman, dan hemat biaya; prioritaskan tool tanpa API, gunakan venv untuk dependency Python, dan verifikasi config fallback provider secara end-to-end.
triggers:
  - User minta instal/aktifkan plugin Hermes
  - User minta setup hemat biaya (OpenRouter fallback, model free/cheap)
  - User ingin integrasi bertahap, bukan instal semua
---

# Hermes Safe Plugin Rollout

## Tujuan
Menjalankan integrasi plugin Hermes yang **selektif**, **aman**, dan **terverifikasi**, terutama saat user ingin memprioritaskan tool tanpa API dan fallback provider hemat biaya.

## Alur Eksekusi (Class Workflow)
1. **Tetapkan scope & safety gate**
   - Konfirmasi fokus: plugin mana yang benar-benar dibutuhkan untuk use-case saat ini.
   - Hindari aktivasi borongan; jalankan bertahap per prioritas.
   - Untuk aksi berisiko (write/delete/commit/push), minta approval eksplisit.

2. **Aktivasi plugin inti per prioritas**
   - Prioritaskan plugin no-API lebih dulu (contoh: web/ddgs).
   - Aktifkan plugin observability/provider hanya saat ada use-case nyata.

3. **Tangani dependency Python dengan benar**
   - Jika install global gagal karena managed environment (PEP 668), **jangan paksa system Python**.
   - Pasang dependency di virtualenv proyek/agent lalu validasi import/runtime.

4. **Konfigurasi fallback provider hemat biaya**
   - Set fallback provider (mis. OpenRouter) dan model default yang sesuai budget.
   - Simpan secret di `.env`, bukan hardcode di config/repo.

5. **Verifikasi end-to-end**
   - Jalankan validasi config yang benar (`check`/`show`, bukan asumsi subcommand lain).
   - Pastikan env var terdeteksi, provider kebaca, dan model fallback terset.

6. **Dokumentasikan guardrail komunitas**
   - Jika pasang skill komunitas, tambahkan safety gate lokal (read-only by default, aksi write harus approved).

## Pitfalls yang Harus Dihindari
- Menginstal semua plugin sekaligus tanpa prioritas use-case.
- Menganggap backend search juga bisa extract konten URL tanpa verifikasi backend capability.
- Menyimpan/menampilkan kredensial di chat/log.
- Memakai command verifikasi yang tidak didukung CLI (cek help/subcommand resmi dulu).

## Checklist Verifikasi
- Plugin target aktif sesuai scope.
- Dependency runtime terpasang di environment yang benar (venv bila perlu).
- `OPENROUTER_API_KEY` (atau provider lain) terbaca oleh `config check`.
- Fallback provider dan default model tampil di `config show`.
- Tidak ada kredensial sensitif terekspos di output final.

## Referensi
- `references/openrouter-fallback-and-no-api-first.md` — ringkasan pola integrasi, urutan prioritas, dan guardrail dari kasus nyata.
