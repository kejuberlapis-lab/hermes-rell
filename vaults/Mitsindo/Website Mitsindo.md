# Website Mitsindo (mitsindo.co.id) - Technical & Maintenance Notes

## 🌐 Overview
Dokumentasi teknis, arsitektur, dan pemeliharaan website resmi **PT Mitsindo Visual Pratama** (`https://mitsindo.co.id/`).

- **Domain Utama:** https://mitsindo.co.id/
- **Hosting / cPanel:** `bausasran.idweb.host:2083` (User: `mitsindo`)
- **Web Server:** LiteSpeed Web Server
- **HRIS Subdomain:** https://hris.mitsindo.co.id/
- **Backend Architecture:** Standalone Python FastAPI Application on cPanel Hosting (`/home/mitsindo/hris.mitsindo.co.id`) via CloudLinux Python 3.11 Runtime + LiteSpeed Fast Gateway.
- **Portofolio Galeri:** Multi-Category Interactive Grid (15 Proyek Riil dengan Default 6 Card + Load More Expansion).

---

## 🌐 Subdomain Terdaftar & Status Operasional

1. **`hris.mitsindo.co.id`**
   - **Document Root:** `/hris.mitsindo.co.id`
   - **Status:** **`ONLINE & LIVE 🟢 (HTTP 200 OK)`**
   - **Fungsi:** Enterprise HRIS Portal PT Mitsindo Visual Pratama (SPPD, Absensi, Cuti, Overtime, Payroll, KPI).
   - **URL Akses:** https://hris.mitsindo.co.id/

2. **`monitor.mitsindo.co.id`**
   - **Document Root:** `/monitor.mitsindo.co.id`
   - **Status:** `AKTIF 🟢`

3. **`sap.mitsindo.co.id`**
   - **Document Root:** `/sap.mitsindo.co.id`
   - **Status:** `Laravel System (Under Maintenance)`

---

## 🛠️ Riwayat Audit & Deployment

### 1. Pembaruan Hero Banner & Multi-Category Portfolio (28 September 2026)
- **Hero Banner 2K:** Banner Belyst *"Professionally Yours"* di-upscale ke Ultra HD `2560 x 1064 px` menggunakan Lanczos + Unsharp filtering.
- **Posisi Tombol CTA:** Tombol "Konsultasi Gratis" dan "Lihat Solusi" diposisikan presisi di lantai pantulan kaca showroom dengan ukuran modern yang pas.
- **Portofolio 15 Proyek Riil:** 15 foto instalasi nyata (Mahkamah Konstitusi RI, Telkom University, Command Center, PIP Makassar, Re.juve, BNPT, dll.) diintegrasikan ke dalam Grid Galeri Multi-Kategori.
- **Sistem Load More:** Default menampilkan 6 proyek teratas dengan tombol *Lihat Lebih Banyak (9 Proyek Lainnya)* untuk menjaga kecepatan loading dan kerapian layout.
- **Pembersihan Header:** Badge *"Studi Kasus & Instalasi"* dihilangkan sesuai arahan agar judul lebih rapi dan elegan.

### 2. Penambahan & Sinkronisasi HRIS Online (24 September 2026)
- Subdomain `hris.mitsindo.co.id` berhasil dibuat melalui cPanel UAPI.
- Dikonfigurasi arsitektur **High-Performance Full-Pass Reverse Proxy** di cPanel `/hris.mitsindo.co.id/index.php` yang meneruskan seluruh request secara transparan ke FastAPI core engine di VPS.
- Seluruh endpoint API, Session JWT, Dokumentasi Swagger (`/docs`), dan antarmuka login/dashboard telah aktif live via HTTPS.

---
*Buku Pembahasan Lengkap: `00_BUKU_PEMBAHASAN_MITSINDO.md`*  
*Last Updated: September 28, 2026 | Maintained by: Hermes AI Agent*
