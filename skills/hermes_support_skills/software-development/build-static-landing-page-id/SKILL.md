---
name: build-static-landing-page-id
description: "Bangun cepat website landing page statis berbahasa Indonesia untuk bisnis lokal (contoh: tempat les), lengkap dengan CTA dan form WhatsApp."
version: 1.1.0
author: Hermes Agent
license: MIT
---

# Build Static Landing Page (Indonesia)

## Kapan dipakai
- User minta “buat website” tanpa spesifikasi teknis detail.
- Butuh hasil cepat, siap dipreview, mudah diubah.
- User minta company profile profesional/enterprise dan butuh iterasi cepat dari feedback visual.

## Langkah
1. Buat folder proyek baru (mis. `/root/website-tempat-les`).
2. Tulis satu file `index.html` yang sudah mencakup:
   - Hero + value proposition
   - Navigasi anchor section
   - Program/layanan
   - Keunggulan
   - Pricing cards
   - Kontak + form
   - Script submit ke WhatsApp (`wa.me`)
3. Gunakan CSS internal untuk mempercepat (single file delivery).
4. Verifikasi halaman dengan `browser_navigate file:///.../index.html` dan cek elemen penting di snapshot.
5. Jika user minta screenshot, ambil dengan `browser_vision` lalu kirim `MEDIA:/path/screenshot.png`.
6. Jika user minta link online cepat:
   - Jalankan server lokal: `python3 -m http.server 8080` (workdir folder website).
   - **Jangan bergantung pada tunnel ephemeral** sebagai hasil akhir (localtunnel/localhost.run kadang tidak mengeluarkan URL atau tidak stabil di environment tertentu).
   - Gunakan hosting gratis yang stabil untuk link publik final: Netlify, Vercel, atau GitHub Pages.
7. Serahkan path file + daftar bagian yang perlu diganti (nomor WA, alamat, harga, brand) + opsi deploy gratis yang direkomendasikan.

## Pitfalls
- Encoding pesan WhatsApp: gunakan `encodeURIComponent` untuk field teks.
- Jangan lupa placeholder nomor WA admin (format internasional tanpa +).
- Pastikan mobile responsive (`@media`).
- Untuk request “tampil seperti perusahaan besar”, hindari hasil awal yang terlalu sederhana (single-column basic). Mulai dari hierarchy enterprise: hero kuat, trust indicators, services grid, portfolio grid, process/timeline, CTA block.
- Jika user meminta “tiru/samakan konten website lain”, jangan salin mentah teks/gambar. Gunakan struktur + positioning yang setara, tapi copywriting dan aset harus original/berizin.
- Saat user tidak puas visual (“terlihat pemula”), lakukan redesign menyeluruh (v2/v3) dan jelaskan perbedaan konkrit per iterasi (typography, spacing, component hierarchy, information architecture), bukan tweak kecil.
- Untuk SEO final, jangan berhenti di homepage: tambahkan halaman layanan terpisah + sitemap/robots/schema agar siap indexing setelah deploy domain final.
- Saat user minta "clone" website lain, jangan salin mentah teks/gambar berhak cipta; tiru struktur/flow dan tulis konten original setara.
- Pastikan mobile responsive (`@media`).

## Checklist selesai
- Halaman bisa dibuka lokal
- Struktur section lengkap
- Tombol CTA ada
- Form pendaftaran ada
- Nomor WA mudah diganti
