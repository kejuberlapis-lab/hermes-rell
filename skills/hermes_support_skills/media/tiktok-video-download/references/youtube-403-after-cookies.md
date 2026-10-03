# YouTube Shorts: 403 after valid cookies (session note)

## Symptom progression
1. Tanpa cookies: `Sign in to confirm you’re not a bot`.
2. Dengan cookies file Netscape valid: error berubah jadi `HTTP Error 403: Forbidden`.

## Interpretation
Perubahan error ini biasanya berarti `--cookies` sudah terbaca, tetapi sesi login tidak cukup valid untuk konteks server saat ini (IP/origin/expiry/domain scope).

## Fast operator response
- Jelaskan bahwa progress terjadi (anti-bot challenge terlewati, tapi akses video data tetap ditolak 403).
- Minta export ulang `cookies.txt` yang fresh saat user sedang login aktif.
- Jika memungkinkan, minta export yang mencakup `youtube.com` dan `google.com`.
- Jangan minta user paste cookies di chat; wajib kirim file asli hasil export.

## Safety note
Jangan pernah memantulkan isi cookie/token ke chat. Perlakukan sebagai kredensial sensitif.
