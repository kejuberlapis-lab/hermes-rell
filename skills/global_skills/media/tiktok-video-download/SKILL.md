---
name: tiktok-video-download
description: Use when you need to download TikTok videos (with or without watermark) from terminal safely and quickly.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [tiktok, video, downloader, yt-dlp, media]
    related_skills: [youtube-content, gif-search]
---

# TikTok Video Download

## Overview
Skill ini dipakai untuk mengunduh video TikTok via terminal menggunakan `yt-dlp`, termasuk opsi memilih kualitas, output filename, dan mode audio-only jika diperlukan.

Lihat juga catatan kasus nyata: `references/youtube-shorts-antibot-and-cookie-format.md` dan `references/youtube-403-after-cookies.md`.

## When to Use
- Saat user memberi URL video TikTok dan minta file videonya.
- Saat butuh arsip konten TikTok untuk analisis/editing.
- Saat perlu mode cepat (default command) tanpa setup rumit.

Jangan gunakan skill ini untuk:
- Mengakses konten privat tanpa izin.
- Melanggar hak cipta atau ToS platform.

## Prerequisites
1. Pastikan `yt-dlp` terpasang.
2. Pastikan `ffmpeg` terpasang untuk merge format tertentu.

Cek cepat:
```bash
yt-dlp --version
ffmpeg -version
```

Install (Ubuntu/Debian):
```bash
python3 -m pip install -U yt-dlp
sudo apt-get update && sudo apt-get install -y ffmpeg
```

## Core Commands

Unduh video default:
```bash
yt-dlp "<TIKTOK_URL>"
```

Unduh kualitas terbaik + nama file rapi:
```bash
yt-dlp -f "bv*+ba/b" -o "%(uploader)s-%(id)s.%(ext)s" "<TIKTOK_URL>"
```

Unduh tanpa metadata berlebih (lebih bersih):
```bash
yt-dlp --no-write-info-json --no-write-thumbnail "<TIKTOK_URL>"
```

Audio-only (mp3):
```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 "<TIKTOK_URL>"
```

Simpan ke folder tertentu:
```bash
yt-dlp -P "~/Downloads/tiktok" "<TIKTOK_URL>"
```

## Batch Download
Dari file daftar URL (`urls.txt`):
```bash
yt-dlp -a urls.txt -P "~/Downloads/tiktok"
```

## YouTube Shorts Support (Fallback Workflow)
Walau skill ini fokus TikTok, dalam praktik chat downloader sering menerima link YouTube Shorts juga. Gunakan urutan fallback berikut agar stabil:

1. Coba unduh normal via `yt-dlp`.
2. Jika muncul proteksi YouTube seperti `Sign in to confirm you’re not a bot`, lanjut pakai cookies.
3. Jika cookies gagal/invalid, minta user kirim **file** `cookies.txt` (bukan paste isi chat).
4. Jika masih gagal, fallback ke API downloader pihak ketiga (jika tersedia) atau browser automation.

Contoh command Shorts + cookies:
```bash
yt-dlp --cookies "<PATH_COOKIES_TXT>" -f "bv*+ba/b" "<YOUTUBE_SHORTS_URL>"
```

## Cookie Handling Rules (Penting)
- `yt-dlp` mengharuskan format Netscape yang valid (tab-separated fields).
- Cookies yang dipaste sebagai plain text chat sering rusak separator-nya dan ditolak (`invalid length`).
- Selalu minta user **upload file cookies.txt langsung** dari export browser extension (mis. Get cookies.txt LOCALLY).
- Simpan cookie file dengan permission ketat (`chmod 600`).

Lihat detail sesi & contoh troubleshooting di: `references/youtube-shorts-auth-and-fallback.md`.

## YouTube Shorts Fallback (tanpa cookies user sebagai default)
Jika URL adalah YouTube Shorts dan `yt-dlp` gagal dengan error anti-bot (mis. `Sign in to confirm you’re not a bot`), gunakan urutan fallback berikut:

1. **Retry extractor ringan**
```bash
yt-dlp --extractor-args "youtube:player_client=web" "<YOUTUBE_SHORTS_URL>"
```
2. **Jika masih gagal, jangan looping terlalu lama**: eskalasi ke **API downloader pihak ketiga** (RapidAPI/Apify) agar pengalaman user tetap cepat.
3. **Minta kredensial API secara eksplisit**:
   - `X-RapidAPI-Key` / token provider
   - endpoint + method + contoh response
4. **Set ekspektasi user**: tanpa cookies/proxy, Shorts bisa diblokir di server tertentu.

## Cookie Handling Rules (penting)
Untuk kasus YouTube yang perlu autentikasi:
- **Wajib minta file `cookies.txt` sebagai file attachment**, bukan paste isi cookie di chat.
- Paste teks sering merusak format Netscape (tab-separated) dan memicu error parsing seperti `invalid length`.
- Simpan permission ketat (`chmod 600`) sebelum dipakai.

## Common Pitfalls
1. **HTTP 403 / blocked**
   - Coba update `yt-dlp` ke versi terbaru.
   - Jika platform YouTube mengembalikan "Sign in to confirm you’re not a bot", gunakan opsi legal: cookies login, proxy resmi, atau API provider pihak ketiga.
2. **Format tidak bisa di-merge**
   - Pastikan `ffmpeg` terinstall.
3. **Nama file aneh/terpotong**
   - Gunakan template output `-o` yang eksplisit.
4. **Video private/removed**
   - URL tidak valid lagi atau butuh autentikasi; tidak selalu bisa diunduh.
5. **Cookies tidak terbaca oleh yt-dlp**
   - Pastikan file cookies dalam format Netscape TAB-separated.
   - Jangan copy-paste isi cookies ke chat lalu simpan manual jika separator berubah; kirim/gunakan file `cookies.txt` asli hasil export extension browser.
6. **YouTube tetap 403 meski `--cookies` sudah dipakai**
   - Ini biasanya berarti cookies *terbaca* tapi sesi tidak cukup valid untuk origin/IP server saat ini.
   - Sinyal umum: error berubah dari `Sign in to confirm you’re not a bot` menjadi `HTTP Error 403: Forbidden`.
   - Tindakan: minta export cookies **fresh** saat user sedang login aktif, sertakan cookies `youtube.com` + `google.com` bila extension mendukung, lalu retry.

## Provider Fallback (Legal)
Jika unduhan langsung gagal karena anti-bot, lakukan fallback berurutan:
1. `yt-dlp` direct dengan user-agent browser normal.
2. `yt-dlp --cookies <cookies.txt>` (cookies legal milik user).
3. API provider pihak ketiga (RapidAPI/Apify) untuk endpoint download.

Detail checklist ada di `references/provider-fallback-checklist.md`.

## Telegram Chat Downloader Response Pattern
Saat dipakai sebagai asisten chat downloader (user kirim link lalu minta file):
1. Jalankan unduhan **langsung** (jangan minta klarifikasi jika URL sudah valid).
2. Jika sukses, kirim file/video path yang bisa langsung dikirim ke chat.
3. Jika gagal karena YouTube anti-bot, laporkan **error persisnya** (mis. `Sign in to confirm you’re not a bot`) dan minta satu artifact paling relevan berikutnya:
   - file `cookies.txt` valid (Netscape), atau
   - endpoint API provider + API key.
4. Hindari jawaban generik; selalu sertakan langkah next-action paling kecil agar user bisa lanjut cepat.

## Verification Checklist
- [ ] URL platform valid (TikTok/Shorts/Reels/Facebook/X).
- [ ] `yt-dlp --version` dan `ffmpeg -version` berjalan.
- [ ] Untuk YouTube yang terproteksi: fallback cookies/API provider dijalankan sesuai urutan.
- [ ] File output muncul di folder target.
- [ ] File output bisa diputar normal sebelum dikirim ke user.
