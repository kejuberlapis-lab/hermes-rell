# MiniMax-M3 Upstream Breakage (Jun 2026)

## Kronologi
- **Tanggal:** 11 Juni 2026
- **Model:** `minimax/MiniMax-M3` via 9Router (custom provider, localhost:20128/v1)
- **Error:** HTTP 500: `{"type":"error","error":{"type":"api_error","message":"unknown error, 999 (1000)"}}`

## Ciri
- Service gateway tetap `active (running)` — tidak crash
- Semua retries (3x) gagal dengan error yang sama
- Tidak ada perubahan konfigurasi — model tiba-tiba berhenti bekerja
- Model masih muncul di daftar `/v1/models` 9Router, tapi API MiniMax backend menolak

## Dampak
- Semua 5 profile Telegram (hermes-support, mvp, node-b, olo, plus) + default terkena
- Bot merespon di Telegram? Ya, tapi gagal generate jawaban → timeout → user lihat bot tidak membalas

## Fix
Rollback ke `minimax/MiniMax-M2.7` — model ini masih tersedia dan berfungsi normal.

## Model MiniMax yang masih berfungsi (via 9Router VPS-Zeus)
- `minimax/MiniMax-M2.7` ✅
- `minimax/MiniMax-M2.5` ✅
- `minimax/MiniMax-M2.1` ✅

## Lesson
- Jangan percaya memory yang bilang "profile sudah update" — **selalu audit langsung** config files di VPS
- Model yang muncul di `/v1/models` belum tentu bisa dipakai — selalu test dengan request minimal
- HTTP 500 dari upstream (bukan 401/403/404) = model breakage, bukan config issue
- Rollback model harus ke SEMUA profile, bukan cuma yang dilaporkan error
- Update memory IMMEDIATELY setelah fix selesai
