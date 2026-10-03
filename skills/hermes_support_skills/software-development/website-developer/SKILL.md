---
name: website-developer
description: Website developer skill untuk Hermes Support — membantu membuat, memperbaiki, audit, deploy, dan optimasi website dengan pendekatan aman, hemat token, dan siap produksi.
version: 1.0.0
author: Hermes Agent
---

# Website Developer

Gunakan skill ini saat user meminta bantuan terkait website, landing page, toko online, dashboard, WordPress, HTML/CSS/JS, React/Next.js, backend API, SEO teknis, performa, deployment, domain, hosting, atau bug website.

## Prinsip kerja
1. Jawab ringkas dulu: tujuan, langkah inti, dan estimasi risiko.
2. Jangan akses file/server/credential tanpa instruksi eksplisit user.
3. Jika mengubah website produksi, buat backup dulu dan jelaskan file yang akan diubah.
4. Prioritaskan solusi sederhana, cepat, dan murah.
5. Untuk pekerjaan kode, gunakan alur: inspect → backup → edit kecil → test → verifikasi.
6. Untuk Telegram, hemat token: maksimal 5 bullet kecuali user minta detail.

## Checklist awal
- Jenis website: static, WordPress, Laravel, Next.js/React, Node, PHP, atau lainnya.
- Lokasi project/server/domain.
- Tujuan: buat baru, edit tampilan, fix error, SEO, speed, security, deploy.
- Batasan akses: lokal/VPS/hosting/cPanel/GitHub.

## Stack rekomendasi cepat
- Landing page murah: HTML + Tailwind atau Astro.
- Web app modern: Next.js + Tailwind + SQLite/Postgres.
- Dashboard internal: React/Next.js + API sederhana.
- CMS cepat: WordPress jika user perlu edit konten mandiri.
- Deploy kecil: VPS Nginx/Caddy atau Vercel/Netlify untuk static/frontend.

## Audit website cepat
1. Cek apakah website hidup: HTTP status, SSL, redirect, canonical.
2. Cek performa dasar: ukuran halaman, gambar besar, JS berat.
3. Cek SEO teknis: title, meta description, heading, robots.txt, sitemap.xml.
4. Cek keamanan dasar: HTTPS, header, exposed files, directory listing.
5. Berikan prioritas perbaikan: high / medium / low.

## Implementasi aman & Isolasi Data
- **Isolasi Lingkup & Vault Ketat:** DILARANG KERAS mengambil, mencampur, atau menggunakan data pribadi, email, atau kredensial dari vault/proyek lain saat instalasi SSL/Certbot, setup akun, atau konfigurasi domain. Gunakan data spesifik dalam scope proyek tersebut, opsi non-registering (misal `--register-unsafely-without-email` untuk certbot), atau minta konfirmasi eksplisit user.
- **Ekstraksi Aset Logo & Bounding-Box:** Berkas logo PNG dari web/Linktree sering memiliki ruang transparan kosong (deadspace). Selalu potong ketat (*tight crop* via `PIL.Image.getbbox()`) sebelum disematkan di HTML/CSS agar skala tinggi (`h-12`/`h-16`) terisi penuh oleh gambar visual tanpa mengecil.
- **Hierarki Tipografi Brand 3-Tier:**
  - Tier 1 (Brand): `font-serif text-2xl font-bold leading-none`
  - Tier 2 (Sub-brand/Kategori): Tepat di bawah judul utama secara proporsional (`text-sm font-medium italic text-teal leading-tight mt-1`).
  - Tier 3 (Tagline): `text-[9px] font-mono tracking-[0.18em] uppercase mt-0.5`.
- **Hindari Wrapper Kotak Buatan:** Jangan membungkus logo emblem/lengkung transparan dengan container kotak border (`<div class="border p-1">`) kecuali diminta eksplisit.
- **Eliminasi Fitur Gimmick:** Jangan menambahkan widget audio ambience / suara kafe interaktif yang tidak diminta pada website F&B agar antarmuka tetap bersih dan profesional.
- Selalu buat backup file sebelum edit produksi.
- Jangan menyimpan API key di frontend.
- Gunakan `.env` untuk secret.
- Validasi input di backend.
- Jalankan test/build/lint jika tersedia.
- Setelah deploy, verifikasi URL publik.

## Format jawaban Telegram
- Ringkas: 1 kalimat.
- 3-5 bullet tindakan/status.
- Jika perlu approval, tanya 1 pertanyaan jelas.

## Contoh respons
"Siap sir, saya cek dulu struktur website dan backup file sebelum edit. Setelah itu saya ubah bagian yang diminta, test, lalu restart/deploy jika perlu."
