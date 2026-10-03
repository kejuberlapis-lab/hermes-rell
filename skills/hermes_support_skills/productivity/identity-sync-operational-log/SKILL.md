---
name: identity-sync-operational-log
description: Sinkronisasi perubahan identitas agent ke log operasional lokal dan verifikasi akses VPS.
version: 1.0.0
author: Hermes
created_by: agent
---

# Identity Sync Operational Log

## Kapan dipakai
- Saat user meminta update identitas, SOUL, peraturan, persona, atau sinkron lokal/VPS/Telegram.
- Saat perlu mencatat perubahan kebijakan/persona penting ke log Markdown.

## Langkah
1. Load konteks skill/aturan yang relevan.
2. Discovery file log/identity markdown yang sudah ada.
3. Jika tidak ada, gunakan path standar: `~/.hermes/ops-logs/operational-log.md` atau profile terkait.
4. Cek waktu aktual dengan `date -u` untuk timestamp log.
5. Verifikasi data lokal dulu: file ada, hash/isi sesuai.
6. Jika perlu sinkron VPS, cek akses SSH dan path Hermes target.
7. Jangan tampilkan token, API key, password, secret, private key, atau isi credential.
8. Untuk sinkronisasi skills antar profile/host, jangan gunakan `rsync --delete` pada root skills luas dengan pola include/exclude karena bisa mencoba menghapus direktori skill lain. Pakai allowlist tanpa delete, atau targetkan direktori skill spesifik satu per satu.
9. Catat hanya ringkasan aman: perubahan apa, path file, hash/verifikasi, status sukses/pending.

## Format log singkat
```md
## YYYY-MM-DD HH:MM UTC — Identity/Policy Sync
- Scope:
- Local:
- VPS/Telegram:
- Verification:
- Notes:
```
