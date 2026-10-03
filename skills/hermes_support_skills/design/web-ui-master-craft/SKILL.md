---
name: web-ui-master-craft
description: Use when building web UI. Enforces anti-slop rules.
---

# Web UI Master Craft & Precision Quality Gate

Protokol komprehensif untuk rekayasa antarmuka web modern, bebas dari klise AI Slop, teruji pada berbagai resolusi viewport, dan siap produksi.

## 1. Disiplin Palet Warna & Anti-Carnival UI
- **Larangan Palet Pelangi:** Dilarang memberi warna pastel acak pada setiap kartu/seksi (kartu 1 pink, kartu 2 biru, kartu 3 hijau, dst.). Ini adalah *tell* AI slop nomor satu.
- **Tipografi Monokrom:** Judul wajib `text-slate-900`, teks deskripsi `text-slate-600`.
- **Wadah Ikon Terpadu:** Seluruh wadah ikon dalam satu seksi wajib menggunakan gaya seragam (`bg-slate-100 border border-slate-200 text-slate-800` atau aksen tunggal brand `bg-blue-50 text-blue-600`).
- **Terminal / Prompt Box Developer-Grade:** Gunakan satu gaya terminal gelap berwibawa (`bg-slate-900 text-slate-100 font-mono text-[11px] p-3 rounded-xl`) dengan aksen emerald (`text-emerald-400 font-bold > Prompt:`).

## 2. Golden Rules Geometri & Alignment
- **Tombol Ikon Bundar:** Wajib dimensi pasti `w-10 h-10 rounded-full shrink-0 flex items-center justify-center`. Badge notifikasi wajib `absolute -top-1.5 -right-1.5` dan diberi kelas `hidden` saat 0.
- **Penyelarasan Brand Block:** Teks brand dan logo wajib sejajar rata atas (`items-start pt-0.5`). Tinggi total teks dilarang melebihi tinggi logo (`leading-none` & margin rapat).
- **Anti-Clipping Navbar:** Tombol aksi navbar wajib `whitespace-nowrap shrink-0` agar tidak pernah terpotong di layar mengecil.

## 3. Ekstraksi Logo & Alpha Masking
- **Anti-Silhouette Degradation:** Saat menghapus background putih pada logo, gunakan *smooth linear alpha ramp* berbasis intensitas. Dilarang mengubah semua piksel non-transparan menjadi putih polos karena akan merusak detail internal gambar.
- **Dual Asset Separation:** Siapkan ikon simbolik murni untuk navbar/favicon (`tech_worker_icon.png`) dan logo penuh untuk preview OpenGraph (`tech_worker_logo.png`).

## 4. Konfigurasi Server & Anti-Cache Invalidation
- **Nginx Cache Bypass:** Pada Nginx reverse proxy, wajib pasang header anti-cache agar browser klien tidak tertinggal cache lama:
  ```nginx
  add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0" always;
  add_header Pragma "no-cache" always;
  add_header Expires "0" always;
  ```
- **HTTP HEAD Route Support:** Backend FastAPI/Flask untuk static web wajib mendukung `methods=["GET", "HEAD"]` agar diagnostik `curl -I` dan uptime monitor tidak menghasilkan error 405.

## 5. Kepadatan Jarak (Compact Density)
- Batas maksimal padding seksi: `py-8 sm:py-12` (32px–48px). Hindari `py-20`/`py-24`/`py-32`.
- Grid gap: `gap-4 sm:gap-6`. Header height: `min-h-[72px] sm:min-h-[78px] py-2`.
