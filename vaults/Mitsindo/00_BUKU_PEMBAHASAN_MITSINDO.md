# 📘 BUKU PEMBAHASAN & CATATAN OPERASIONAL MITSINDO
**PT Mitsindo Visual Pratama (MVP)**  
*Dokumentasi Resmi Integrasi Sistem, Website, Server, HRIS, Database Vendor, & Analitik*

---

## 📑 Daftar Isi Buku Pembahasan
1. [🏢 Identitas Perusahaan & Kontak Resmi](#1-identitas-perusahaan--kontak-resmi)
2. [🌐 Infrastruktur & Akses Web Hosting](#2-infrastruktur--akses-web-hosting)
3. [🖼️ Konfigurasi Hero Banner & Desain Visual](#3-konfigurasi-hero-banner--desain-visual)
4. [📂 Master Portofolio Proyek Terpasang (15 Proyek)](#4-master-portofolio-proyek-terpasang-15-proyek)
5. [⚙️ Standar Operasional Pemeliharaan & Cache-Buster](#5-standar-operasional-pemeliharaan--cache-buster)
6. [🏢 Ekosistem Subdomain (HRIS & Sistem Internal)](#6-ekosistem-subdomain-hris--sistem-internal)
7. [📰 Artikel & Blog Solution (SEO & Yoast Standard)](#7-artikel--blog-solution-seo--yoast-standard)
8. [📊 Database Master Scraping Audio Visual Se-Indonesia (INAPROC LKPP v6)](#8-database-master-scraping-audio-visual-se-indonesia-inaproc-lkpp-v6)
9. [📱 Perancangan Sistem Chatbot & Otomasi WhatsApp Bisnis Mitsindo](#9-perancangan-sistem-chatbot--otomasi-whatsapp-bisnis-mitsindo)
10. [📈 Analisis Trafik Website & Pelacak Leads WhatsApp (Server-Side Tracker)](#10-analisis-trafik-website--pelacak-leads-whatsapp-server-side-tracker)
11. [📜 Log Riwayat Pembaruan & Deployment](#11-log-riwayat-pembaruan--deployment)

---

## 1. 🏢 Identitas Perusahaan & Kontak Resmi
* **Nama Perusahaan:** PT Mitsindo Visual Pratama (MVP)
* **Tahun Berdiri:** 2005 (20+ Tahun Pengalaman di Industri AV)
* **Spesialisasi:** Audio Visual System Integrator (Design & Build)
* **Brand Resmi:** **BELYST** (*"Professionally Yours"*)
* **Kontak Resmi & Fast Response:**
  * **WhatsApp Official:** `08119255476` (`https://wa.me/628119255476`)
  * **Telepon Kantor:** `+6221 668 0223`, `668 2033` (Fax: `+6221 668 5110`)
  * **Email:** `sales@mitsindo.co.id`
  * **Instagram:** `@belyst.co.id` & `@mitsindo.education`
  * **Alamat:** Rukan Puri Delta Mas Blok I No.46-47, Jl. Bandengan Selatan No.43, Jakarta 14450
* **Produk Inti:**
  * Video Wall & Controllers (Bezel-less, NOC & Command Center)
  * LED Videotron Indoor & Outdoor
  * Interactive Flat Panel (IFP 4K untuk Meeting & Training)
  * Smart Control System & Extender / Switcher
  * Smart Film Screen & Robotics AI Education

---

## 2. 🌐 Infrastruktur & Akses Web Hosting
* **Domain Utama:** `https://mitsindo.co.id/`
* **Server Web:** LiteSpeed Web Server
* **Hosting Hostname:** `bausasran.idweb.host` (Port FTP: 21 / cPanel: 2083)
* **User cPanel / FTP:** `mitsindo`
* **Root Direktori Produksi:** `public_html/`
* **File Struktur Utama:**
  * `public_html/index.html` (Markup utama, cache-buster parameter)
  * `public_html/css/style.css` (Stylesheet global)
  * `public_html/js/main.js` (Script interaksi UI, carousel, & WhatsApp lead tracker)
  * `public_html/api/track-lead.php` (Backend API pencatat klik WA)
  * `public_html/api/dashboard.php` (Dashboard live laporan klik WA)
  * `public_html/images/` (Aset gambar hero, portofolio, logo, icon)
  * `public_html/blog/` (Direktori 10 artikel SEO)

---

## 3. 🖼️ Konfigurasi Hero Banner & Desain Visual
* **Ukuran Master Kanvas:** `2400 x 1000 px` (Rasio `2.4 : 1`)
* **Resolusi Produksi:** `2560 x 1064 px` (Ultra HD 2K Sharp Lanczos)
* **File Asset:** `public_html/images/hero.png`
* **Zona Desain:**
  * 75% Atas (`0 - 750px`): Zona Konten Visual (Logo Belyst, Teks Keunggulan, Display Hardware, Robot).
  * 25% Bawah (`750 - 1000px`): Zona Aman Lantai Bersih untuk penempatan tombol CTA dan pita *running text*.
* **Tombol CTA (*Call-to-Action*):**
  * `Konsultasi Gratis` & `Lihat Solusi`
  * Posisi: Presisi di area lantai pantulan kaca showroom (clean space).
  * Ukuran: Ramping, modern (`font-size: 0.92rem`, `padding: 9px 24px`, `border-radius: 30px`).

---

## 4. 📂 Master Portofolio Proyek Terpasang (15 Proyek)
Website menggunakan sistem **Multi-Category Gallery Grid (Default 6 item + Load More Expand)** dengan 15 proyek riil:

### Kategori A: 🏛️ Lembaga Negara & Pemerintahan (4 Proyek)
1. **Ruang Sidang Utama Mahkamah Konstitusi RI** (`portfolio-mahkamah-konstitusi.jpg`)
2. **Executive VVIP Teleconference Lembaga Negara** (`portfolio-executive-meeting.jpg`)
3. **Exhibition & Museum Display Panel BNPT RI** (`portfolio-museum-bnpt.jpg`)
4. **Layanan Publik & Smart City Pemkot Makassar** (`portfolio-pelayanan-publik-makassar.jpg`)

### Kategori B: 🖥️ Command Center & NOC (2 Proyek)
5. **Command Center Video Wall & NOC System** (`portfolio-command-center.jpg`)
6. *(Termasuk Makassar Smart City Command Room)*

### Kategori C: 📢 LED Videotron & Panggung (4 Proyek)
7. **Auditorium LED Video Wall Telkom University** (`portfolio-telkom-university.jpg`)
8. **Outdoor LED Videotron Gerbang PIP Makassar** (`portfolio-pip-makassar.jpg`)
9. **Curved Giant Outdoor Videotron Plaza Landmark** (`portfolio-curved-outdoor-led.jpg`)
10. **Grand Ballroom & Event Stage 100 Tahun RS** (`portfolio-event-hall-led.jpg`)

### Kategori D: 🏢 Corporate & Smart Room (4 Proyek)
11. **Smart Boardroom & Video Conference Enterprise** (`portfolio-boardroom-vcon.jpg`)
12. **Interactive Flat Panel (IFP) Training Room** (`portfolio-ifp-training-room.jpg`)
13. **Vertical Pillar Digital Signage PT Aisin Indonesia** (`portfolio-pillar-signage-aisin.jpg`)
14. **Corporate Lobby Integrated Display** (`portfolio-corporate-lobby.jpg`)

### Kategori E: 🛍️ Commercial & Retail (1 Proyek)
15. **Retail Commercial Digital Menu Board Re.juve** (`portfolio-retail-rejuve.jpg`)

---

## 5. ⚙️ Standar Operasional Pemeliharaan & Cache-Buster
Karena server LiteSpeed menerapkan header `Cache-Control: public, max-age=604800` (7 hari cache):
1. **Aturan Cache-Busting:** Setiap perubahan file CSS, JS, atau gambar pada `public_html/` WAJIB menaikkan query parameter versi pada `index.html` (contoh: `style.css?v=XX`, `main.js?v=XX`, dan `hero.png?v=XX`).
2. **Hard Refresh Browser:** Jika Chrome masih menyimpan cache lama, tekan `Ctrl + F5` (Windows) atau `Cmd + Shift + R` (Mac).
3. **Backup SOP:** Sebelum melakukan replace file master, simpan salinan backup dengan format tanggal (contoh: `hero_backup_YYYYMMDD.png`).

---

## 6. 🏢 Ekosistem Subdomain (HRIS & Sistem Internal)
1. **`hris.mitsindo.co.id`**
   * **Status:** `ONLINE 🟢`
   * **Fungsi:** Enterprise HRIS Portal PT Mitsindo Visual Pratama (SPPD, Absensi, Cuti, Overtime, Payroll, KPI).
   * **Runtime:** CloudLinux Python 3.11 + FastAPI Engine.
2. **`monitor.mitsindo.co.id`**
   * **Status:** `AKTIF 🟢`
3. **`sap.mitsindo.co.id`**
   * **Status:** `Laravel System (Under Maintenance)`

---

## 7. 📰 Artikel & Blog Solution (SEO & Yoast Standard)
1. **Perbedaan Utama Videotron Indoor dan Outdoor: Mana yang Anda Butuhkan?**
   * **URL:** `https://mitsindo.co.id/blog/perbedaan-videotron-indoor-dan-outdoor.html`
2. **Strategi Penempatan Videotron: Outdoor untuk Awareness, Indoor untuk Engagement**
   * **URL:** `https://mitsindo.co.id/blog/strategi-penempatan-videotron-indoor-outdoor.html`
3. **Apa itu Digital Signage? Panduan Lengkap, Cara Kerja, dan Manfaatnya**
   * **URL:** `https://mitsindo.co.id/blog/apa-itu-digital-signage-panduan-lengkap.html`
4. **Digital Signage vs Smart TV Biasa: Mana yang Lebih Bagus untuk Bisnis?**
   * **URL:** `https://mitsindo.co.id/blog/digital-signage-vs-smart-tv-untuk-bisnis.html`
5. **Revolusi Pendidikan: Mengapa Sekolah Harus Beralih ke Interactive Flat Panel (IFP)?**
   * **URL:** `https://mitsindo.co.id/blog/revolusi-pendidikan-interactive-flat-panel-sekolah.html`
6. **Transformasi Ruang Rapat: Tingkatkan Produktivitas Bisnis dengan Interactive Flat Panel**
   * **URL:** `https://mitsindo.co.id/blog/transformasi-ruang-rapat-bisnis-interactive-flat-panel.html`

---

## 8. 📊 Database Master Scraping Audio Visual Se-Indonesia (INAPROC LKPP v6)
* **🌟 GRAND MASTER DATABASE 3 SEKTOR (4 Sheets):**
  * File Master Excel: `/home/ubuntu/GRAND_MASTER_DATABASE_AV_INAPROC_ALL_SECTOR.xlsx` (**2.094 Produk & 839 Vendor Unik Gabungan**)
  * File CSV Vendor Gabungan: `/home/ubuntu/GRAND_MASTER_VENDOR_AV_INAPROC_ALL_SECTOR.csv`
* **1. Master Interactive Flat Panel (IFP - 20 Halaman):**
  * File Excel (.xlsx): `/home/ubuntu/DATABASE_SCRAP_IFP_INAPROC_MASTER.xlsx` (**725 Produk Riil & 312 Vendor Unik**)
  * Dokumentasi Vault: `[[DATABASE_VENDOR_AV_INAPROC_725.md]]`
* **2. Master Video Wall System (20 Halaman):**
  * File Excel (.xlsx): `/home/ubuntu/DATABASE_SCRAP_VIDEOWALL_INAPROC_MASTER.xlsx` (**714 Produk Riil & 337 Vendor Unik**)
  * Dokumentasi Vault: `[[DATABASE_VENDOR_VIDEOWALL_INAPROC_714.md]]`
* **3. Master LED Videotron Indoor & Outdoor (20 Halaman):**
  * File Excel (.xlsx): `/home/ubuntu/DATABASE_SCRAP_VIDEOTRON_INAPROC_MASTER.xlsx` (**655 Produk Riil & 370 Vendor Unik**)
  * Dokumentasi Vault: `[[DATABASE_VENDOR_VIDEOTRON_INAPROC_655.md]]`
* **4. File Khusus Daftar 839 Vendor & Kategori Tayang (Clean 1 Row/Vendor):**
  * File Excel (.xlsx): `/home/ubuntu/DAFTAR_VENDOR_DAN_KATEGORI_PRODUK_INAPROC.xlsx`
  * File CSV: `/home/ubuntu/DAFTAR_VENDOR_DAN_KATEGORI_PRODUK_INAPROC.csv`
* **Status Validasi:** **100% Valid & Zero Duplicates** hasil scraping langsung dari E-Katalog LKPP v6 (`katalog.inaproc.id`).

---

## 9. 📱 Perancangan Sistem Chatbot & Otomasi WhatsApp Bisnis Mitsindo
* **Nomor Resmi:** `08119255476` (`https://wa.me/628119255476`)
* **Dokumentasi Khusus & Roadmap:** `[[PERANCANGAN_CHATBOT_WA_MITSINDO.md]]`
* **Pilar Layanan Utama (Pintasan Pesan Cepat):**
  1. `/1`: Interactive Flat Panel (IFP) Belyst 4K TKDN (Edukasi & Ruang Rapat)
  2. `/2`: LED Videotron Indoor & Outdoor P1.2–P10
  3. `/3`: Video Wall & Command Center System Bezel 0.88–3.5mm
  4. `/4`: Robotic AI for Education (STEM, Lab AI, Training Guru)
  5. `/5`: Format Permintaan Penawaran Resmi & Tim Sales

---

## 10. 📈 Mitsindo Unified Analytics & Leads Command Center (All-in-One Dashboard)
* **Status Engine:** **AKTIF & LIVE (100% Real-Time, Terintegrasi Penuh + Executive Business Insights)**
* **Link Master Dashboard Resmi (Satu-satunya):** 
  * 👉 `https://mitsindo.co.id/api/dashboard.php?key=mitsindo2026`
* **Fitur Baru: Panel Rangkuman Laporan & Insight Eksekutif (Bahasa Umum & Owner-Friendly):**
  1. 💡 **Rangkuman Laporan & Insight Bisnis:** Menerjemahkan angka teknis ke bahasa bisnis yang mudah dipahami owner (kualitas pengunjung, rata-rata durasi baca, produk paling diminati, dominasi perangkat, dan konversi kontak WhatsApp).
  2. 🚀 **Rekomendasi Strategis yang Perlu Ditingkatkan:** 4 panduan aksi nyata untuk meningkatkan omset dan jumlah leads (Iklan Meta Ads/Google Ads, SOP balas WA <5 menit, penambahan foto/video studi kasus, dan pemanfaatan sertifikasi TKDN/E-Katalog LKPP).
  3. 📊 **6 Kartu Eksekutif KPI Utama:** Pengunjung Unik, Pageviews, Durasi Baca, Bounce Rate, Total Leads WhatsApp, dan Conversion Rate %.
  4. 📈 **Grafik Korelasi Trafik & Leads Harian + Segmentasi Perangkat.**
  5. 💬 **Tabel Log WhatsApp Leads, Top Pages & Live Recent Sessions.**

---

## 11. 🚀 Optimasi SEO Yoast Standard & Keyword Targeting
* **Status Implementasi:** **100% SELESAI & LIVE DI SELURUH 22 HALAMAN**
* **Cakupan Halaman:**
  * **Homepage (`index.html`):** Focus Keyphrase `Audio Visual Integrator Jakarta & Indonesia`.
  * **Halaman Produk & Layanan (4 Halaman Core):** `product-led.html` (Jual LED Videotron Indoor & Outdoor), `product-videowall.html` (Video Wall Command Center & Processors), `product-ifp.html` (Interactive Flat Panel 4K TKDN Belyst), `product-integration.html` (System Integration AV Enterprise).
  * **Halaman Pendukung (4 Halaman):** `blog.html`, `pricing.html`, `case-studies.html`, `comparison.html`, `landing.html`.
  * **10 Artikel Blog & Edukasi:** Focus keyphrase, meta description 150-160 karakter, breadcrumb & article JSON-LD schema, open graph 1200x630, twitter summary large image card.
* **Fitur Yoast SEO Standard yang Diaktifkan:**
  1. 🏷️ **Optimasi Judul (Title Tag):** 50–60 karakter dengan kata kunci komersial di depan.
  2. 📝 **Meta Description (Yoast Standard):** 145–160 karakter dengan focus keyphrase + CTA Hotline WhatsApp `0811-9255-476`.
  3. 🤖 **Robots Directives Modern:** `index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1` (membuka peluang fitur Google Discover & Rich Snippets).
  4. 🌐 **Canonical URL:** Mencegah isu duplikasi konten di seluruh halaman web.
  5. 📱 **Open Graph & Twitter Cards:** Thumbnail preview 1200x630px otomatis muncul saat link dibagikan ke WhatsApp, LinkedIn, Facebook, dan X/Twitter.
  6. 🗺️ **Sitemap XML & Robots.txt Master:** `https://mitsindo.co.id/sitemap.xml` diperbarui memuat 20 URL lengkap dengan prioritas indeks dan timestamp `2026-09-30`.

---

## 12. 🔗 Official Link-in-Bio Micro-Site (Pengganti Lynk.id / Linktree)
* **Status Implementasi:** **100% LIVE & TERINTEGRASI DI DOMAIN RESMI**
* **URL Akses Resmi:**
  * 👉 **`https://mitsindo.co.id/link`** (atau `https://mitsindo.co.id/bio`)
* **Keunggulan Menggunakan Link Mandiri vs Lynk.id:**
  1. 👑 **Branding Profesional:** Menggunakan domain resmi perusahaan `mitsindo.co.id/link` (bukan domain pihak ketiga `lynk.id/mitsindo`), meningkatkan *trust* dan kredibilitas instansi & klien korporat.
  2. 💸 **100% Gratis & Bebas Watermark:** Tidak ada biaya langganan bulanan atau watermark iklan pihak ketiga.
  3. ⚡ **Terhubung Langsung ke Lead Tracker & Web Analytics:** Setiap klik tombol WhatsApp dan kunjungan produk di bio link langsung tercatat real-time di Dashboard Eksekutif Mitsindo (`dashboard.php`).
  4. 🎨 **Desain Khusus Mobile & High-Converting:** Dilengkapi profil verified badge 🔵, 7 ikon sosmed cepat, 9 kartu link interaktif (WA Hotline Sales respon cepat, Videotron, Video Wall, IFP TKDN, System Integration, Portofolio, Blog Edukasi, Maps Showroom), serta card ajakan booking Showroom Belyst.

---

## 13. 📜 Log Riwayat Pembaruan & Deployment
* **2026-09-29:**
  * Implementasi & Deployment **Server-Side WhatsApp Lead Tracker** (`/api/track-lead.php`, `/api/dashboard.php`, `/js/tracker.js`, dan integrasi `/js/main.js`).
  * Perbaikan path script `/js/main.js?v=20260929` pada seluruh 10 artikel blog agar tracking berjalan seragam.
  * Penyelesaian scraping masif **3 Sektor Audio Visual E-Katalog LKPP v6 (INAPROC)** menghasilkan **Grand Master Database 2.094 Produk & 839 Vendor Unik**.
  * Pembuatan file khusus ringkas **Daftar 839 Vendor & Kategori Tayang**.
  * Audit mendalam log web server LiteSpeed cPanel September 2026 dan pembuatan Dashboard Trafik Pengunjung & Leads.
* **2026-09-28:**
  * Penerbitan **6 artikel pilar SEO** di halaman Solution (Blog) dengan standar Yoast & Schema.org.
  * Sinkronisasi seluruh footer sosial media `@belyst.co.id` dan `@mitsindo.education`.
  * Redesign galeri portofolio menjadi **Multi-Category Interactive Grid (15 Proyek Riil)** dengan tombol *Load More*.
  * Deployment Hero Banner Belyst Ultra HD 2K Lanczos dan penyelarasan posisi tombol CTA.
* **2026-09-24:**
  * Setup subdomain `hris.mitsindo.co.id` (FastAPI Python 3.11 engine).

---
*Buku ini disimpan di Vault Khusus: `/home/ubuntu/ObsidianVault/Mitsindo/`*  
*Tersinkronisasi secara otomatis pada Memory Hermes.*
