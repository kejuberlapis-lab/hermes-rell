---
name: maintenance-fallback-notification
description: Fallback notifikasi standar saat auth gagal atau callback API tidak merespons.
version: 1.0.0
author: Hermes
created_by: agent
---

# Maintenance Fallback Notification

## Trigger
Gunakan aturan ini untuk semua bot saat terjadi:
1. Auth gagal: token invalid/expired, unauthorized, forbidden.
2. Callback/API timeout atau tidak merespons.
3. Error gateway sementara yang menghambat request utama.

## Aksi standar
Ganti pesan error teknis ke notifikasi user-friendly berikut:

```text
Sedang maintenance. Silakan coba beberapa saat lagi.
```

## Aturan implementasi
- Berlaku lintas bot/global policy.
- Jangan tampilkan detail internal, stack trace, endpoint, credential hint, token, atau secret ke user.
- Tetap catat error detail di log internal untuk debugging.
- Jika memungkinkan, retry internal 1-3x sebelum menampilkan notifikasi.
- Untuk issue berulang, laporkan ringkas ke sir dan minta approval sebelum perubahan besar.
