---
name: hermes-telegram-profile-operations
description: "Operasional Hermes multi-profile untuk bot Telegram: sinkronisasi tools lintas platform, hard reset sesi, restart gateway stabil, fallback provider, dan verifikasi cepat saat bot tidak merespons."
version: 1.0.0
author: Hermes
created_by: agent
---

# Hermes Telegram Profile Operations

## Kapan dipakai
- Bot Telegram tidak membalas, lambat, timeout, atau conflict polling.
- Perlu sinkronisasi perilaku profile lokal/server/Telegram agar tool tidak hilang di satu platform.
- Perlu hard reset cepat tanpa mengubah arsitektur besar.
- Perlu cek gateway setelah perubahan tools/skills.

## Tujuan
1. Pulihkan bot agar online dan membalas lagi.
2. Jaga keamanan: aksi sensitif tetap owner-only, chat umum tetap aman.
3. Kurangi false diagnosis akibat status CLI yang ambigu.

## Prosedur standar
1. Validasi proses gateway nyata, jangan hanya percaya satu output status:
   - `ps -ef | grep hermes`
   - `systemctl --user status hermes-gateway*`
2. Cek log gateway:
   - conflict `getUpdates` berarti ada proses lain memakai token yang sama.
   - auth/forbidden/token error jangan tampilkan token.
   - `Agent error` setelah inbound Telegram berarti polling sudah masuk, tapi agent/runtime gagal memproses jawaban.
3. Jika ada `getUpdates` conflict:
   - tentukan satu runner utama (biasanya VPS always-on untuk Telegram).
   - stop gateway di runner duplikat dulu, baru restart runner utama.
   - tunggu dan cek log setelah restart; conflict lama di log historis tidak sama dengan conflict baru.
4. Cek config profile:
   - toolsets untuk Telegram.
   - memory aktif.
   - approvals sesuai policy.
   - auxiliary/compression model valid untuk Hermes.
5. Jika log menunjukkan `Auxiliary compression model ... context window ... below the minimum 64,000`:
   - backup `config.yaml` profile.
   - ganti `auxiliary.compression.model` ke model 64K+ context atau set `auxiliary.compression.context_length` hanya jika deteksi salah.
   - jangan mengubah API key/token/provider secret.
6. Restart gateway hanya untuk profile yang benar.
7. Verifikasi channel discovery atau pesan test jika tersedia.
8. Untuk test Telegram aman:
   - boleh kirim pesan test ke chat yang sudah eksplisit diinstruksikan/terlibat oleh sir.
   - muat token dari `.env` tanpa mencetak nilainya.
   - verifikasi `sendMessage ok=True`, lalu cek log inbound/response/sending response.

## Referensi
- `references/telegram-gateway-recovery-vps-primary.md`: pola recovery saat lokal dan VPS rebutan polling, plus fix auxiliary compression 8K.

## Guardrail
- Jangan kirim DM Telegram tanpa instruksi eksplisit sir.
- Jangan ubah provider/model/token tanpa izin jelas.
- Jangan menampilkan isi `.env` mentah.
- Jangan simpan password/token yang diberikan user ke memory atau log; perlakukan sebagai `[REDACTED]` setelah dipakai.
- Jika command stop/restart gateway diblokir oleh approval/security tool, berhenti total: jangan retry, jangan akali via systemctl/kill/SSH/command lain, dan minta sir menjalankan/approve manual sebelum lanjut.

## Pitfall: Telegram polling conflict + approval block
Saat conflict `getUpdates` muncul, solusi umumnya adalah memastikan hanya satu runner memakai token tersebut. Namun penghentian runner adalah aksi operasional sensitif. Urutan aman:
1. Jelaskan bahwa satu token Telegram hanya boleh dipolling oleh satu gateway.
2. Minta/konfirmasi runner utama: VPS always-on atau lokal/WSL.
3. Jika sudah ada instruksi eksplisit, jalankan stop/restart hanya pada runner yang disepakati.
4. Jika tool approval memblokir command, jangan mencoba outcome yang sama lewat command berbeda. Beri command manual kepada sir dan tunggu hasilnya.
5. Setelah runner conflict selesai, baru verifikasi gateway log dan lakukan test Telegram.
