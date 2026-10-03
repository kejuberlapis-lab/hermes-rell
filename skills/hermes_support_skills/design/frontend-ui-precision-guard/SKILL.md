---
name: frontend-ui-precision-guard
description: Use when polishing web UI. Enforces strict layout gates.
---

# Frontend UI Precision Guard & Quality Gate

Protokol ketat dan checklist kualitas desain antarmuka web untuk memastikan UI selalu rapi, proporsional, bebas bug visual, dan tidak mengalami regresi berulang.

## 1. Golden Rules Tata Letak & Geometri

### A. Geometri Tombol Ikon & Badge Keranjang
- **Wajib Dimensi Eksplisit:** Setiap tombol ikon bundar (Cart, Search, Menu) WAJIB memiliki ukuran pasti: `w-10 h-10 rounded-full shrink-0 flex items-center justify-center`. Dilarang hanya mengandalkan `p-2.5` tanpa lebar/tinggi.
- **Badge Mengambang Bebas Alur:** Badge angka/notifikasi WAJIB berposisi `absolute -top-1.5 -right-1.5 min-w-[20px] h-5 px-1 rounded-full`. Saat bernilai 0 atau kosong, WAJIB menggunakan kelas `hidden`. Dilarang membiarkan badge jatuh ke dalam alur dokumen normal (`inline`/`block`) yang merusak bentuk tombol.

### B. Penyelarasan Brand Block (Logo + Teks)
- **Top Flush Alignment:** Teks brand dan logo wajib sejajar rata atas (`items-start pt-0.5`).
- **Batasan Tinggi Teks:** Tinggi total blok teks (Judul + Sub-brand + Tagline) DILARANG melebihi tinggi gambar logo. Gunakan `leading-none` dan margin rapat (`mt-0.5` / `mt-1`) agar teks selalu berada rapi di dalam batas vertikal logo.

### C. Proteksi Anti-Clipping Tombol Header
- Semua tombol aksi pada navbar (CTA "Book a Table", Login, dll.) WAJIB memiliki kelas `whitespace-nowrap shrink-0` agar tidak pernah terpotong atau terdesak keluar layar saat ukuran browser mengecil.

---

## 2. Standar Kepadatan Jarak (Anti-Loose Spacing)

| Komponen | Batas Maksimal Jarak | Hindari |
| :--- | :--- | :--- |
| **Section Padding** | `py-8 sm:py-12` (32px – 48px) | `py-20`, `py-24`, `py-32` (80px–128px) |
| **Hero Bottom Padding** | `pb-8 sm:pb-12` (32px – 48px) | `pb-24`, `pb-32` |
| **Grid Gaps** | `gap-4 sm:gap-6` (16px – 24px) | `gap-12`, `gap-16` |
| **Header Height** | `min-h-[72px] sm:min-h-[78px] py-2` | `min-h-[96px]`, `py-4+` |
| **Footer Padding** | `py-6 sm:py-8` | `py-16`, `py-20` |

---

## 3. Larangan Kelas Non-Standar (Zero Guessing Classes)
- **Dilarang Menebak Kelas Tailwind:** Jangan pernah menulis kelas yang tidak ada di standar Tailwind CSS (seperti `h-13`, `py-18`, `gap-14`).
- **Safety Fallback:** Jika butuh ukuran kustom di luar kelipatan 4, selalu gunakan arbitrary value eksplisit `h-[56px]` atau sertakan inline style `style="height: 56px; width: auto;"` untuk mencegah gambar meledak ke ukuran aslinya.

---

## 4. Pre-Delivery Quality Checklist (Wajib Cek Sebelum Selesai)
1. **Apakah logo dan teks sejajar rata atas dan tingginya proporsional?**
2. **Apakah seluruh tombol bulat memiliki dimensi terkunci (`w-10 h-10`) dan badge-nya mengambang di pojok tanpa merusak bentuk tombol?**
3. **Apakah ada tombol atau teks di navbar yang terpotong di tepi kanan?**
4. **Apakah ada ruang kosong (whitespace) yang terlalu renggang di atas/bawah seksi?**
5. **Apakah JavaScript pengubah badge/UI mempertahankan posisi `absolute`?**
