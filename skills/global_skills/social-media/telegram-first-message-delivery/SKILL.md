---
name: telegram-first-message-delivery
description: Mengirim pesan pertama ke beberapa Telegram ID lintas profile bot Hermes, termasuk diagnosa error 'chat not found' dan verifikasi allowlist.
version: 1.0.0
author: Hermes
created_by: agent
---

# Telegram First Message Delivery

## Kapan dipakai
- Sir meminta kirim sapaan/pesan awal ke ID Telegram baru.
- Ada lebih dari satu bot/profile.
- Perlu validasi kenapa kirim gagal walau ID tampak sudah terdaftar.

## Langkah kerja
1. Identifikasi profile bot target: `~/.hermes/profiles/<nama-profile>/`.
2. Verifikasi allowlist user per profile dari `.env` tanpa menampilkan nilainya mentah.
3. Ambil token bot hanya untuk eksekusi internal; jangan tampilkan token.
4. Pastikan user pernah start bot. Jika belum, Telegram API bisa mengembalikan `chat not found`.
5. Kirim pesan hanya jika sir memberi instruksi eksplisit untuk target tersebut.
6. Catat hasil aman: sukses/gagal, profile, alasan umum, tanpa token/secret.

## Larangan
- Jangan kirim DM ke ID Telegram mana pun tanpa instruksi eksplisit sir.
- Jangan menampilkan token bot, full allowlist, atau data pribadi yang tidak perlu.
