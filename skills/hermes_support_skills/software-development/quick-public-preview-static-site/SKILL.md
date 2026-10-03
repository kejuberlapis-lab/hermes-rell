---
name: quick-public-preview-static-site
description: "Publikasikan cepat website statis lokal ke URL publik sementara (tanpa deploy permanen), dengan fallback tunnel dan verifikasi browser."
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Quick Public Preview for Static Site

## Kapan dipakai
- User ingin "cek online sekarang" tanpa setup akun hosting dulu.
- Hanya butuh link preview sementara untuk review tampilan.

## Prasyarat
- File website statis sudah ada (mis. `index.html`).
- `python3` dan `ssh` tersedia.

## Langkah eksekusi
1. Jalankan server lokal folder website:
   - `python3 -m http.server 8080` (background, workdir project).
2. Coba tunnel utama (opsional):
   - `npx localtunnel --port 8080` atau Pinggy via SSH.
3. Jika URL tidak keluar / gagal, gunakan fallback paling praktis:
   - `ssh -o StrictHostKeyChecking=no -R 80:localhost:8080 serveo.net`
4. Ambil URL publik dari output baris:
   - `Forwarding HTTP traffic from https://<subdomain>.serveousercontent.com`
5. Verifikasi URL dengan browser tool:
   - Buka URL, jika muncul halaman "Serveo Browser Warning", klik **Continue to Site**.
   - Pastikan halaman target (hero, CTA, section utama) tampil.
6. Kirim link ke user dengan catatan ini preview sementara.

## Pitfalls & temuan lapangan
- Localtunnel bisa gagal dengan error `connection refused: localtunnel.me:<port>` walau sempat mencetak URL; jika ini terjadi, ganti ke Pinggy.
- Untuk Pinggy, gunakan SSH port 443: `ssh -p 443 -R0:localhost:8080 qr@a.pinggy.io`.
- Jika output URL Pinggy tidak muncul di mode background biasa, jalankan proses tunnel dengan PTY agar banner + URL terbaca.
- Serveo bisa tidak stabil/expired; jika URL lama memberi 502, restart tunnel dan pakai URL baru.
- Link preview bersifat sementara dan bisa berubah/expired.

## Verifikasi minimum
- Link publik terbuka dari browser eksternal.
- Validasi cepat via CLI sebelum kirim ke user:
  - `curl -I -L <public_url>` harus `200 OK`.
  - `curl -s <public_url> | head` menampilkan HTML halaman target (cek `<title>`/konten hero).
- Setelah klik warning page (jika ada), website asli tampil.
- Server lokal dan tunnel process status = running saat link dibagikan.

## Troubleshooting saat user bilang "tidak bisa akses"
1. Jangan langsung asumsi server mati; cek dulu URL aktif dengan `curl -I -L`.
2. Jika endpoint sebenarnya `200 OK` tapi user tetap lihat halaman lama/error:
   - minta buka link di incognito, atau
   - hard refresh (`Ctrl+F5`).
3. Jika ada beberapa tunnel URL yang sempat dibagikan, selalu kirim ulang **satu URL terbaru** dan tegaskan untuk tidak memakai link lama.
4. Bila tetap gagal, restart tunnel dan bagikan URL baru lalu verifikasi ulang via `curl`.

## Kapan lanjut ke deploy permanen
Jika user butuh link stabil/brandable, lanjutkan ke:
- Netlify (`*.netlify.app`), atau
- Vercel (`*.vercel.app`).