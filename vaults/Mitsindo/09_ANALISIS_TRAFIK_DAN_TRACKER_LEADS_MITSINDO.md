# 📈 ANALISIS TRAFIK WEBSITE & PELACAK LEADS WHATSAPP MITSINDO
**PT Mitsindo Visual Pratama (MVP)**  
*Dokumentasi Resmi Analisis Pengunjung, Sistem Server-Side Lead Tracker, dan Dashboard Interaktif*

---

## 📌 Ringkasan Eksekutif
Sistem ini dirancang untuk memantau performa trafik pengunjung website `mitsindo.co.id` serta melacak setiap interaksi calon klien yang mengeklik tombol konsultasi WhatsApp menuju nomor Hotline Resmi Mitsindo (**`0811-9255-476`**).

---

## 1. 🌐 Analisis Trafik Pengunjung Website (September 2026)

### A. Data Log Server Mentah (*Raw Hits*) vs Pengunjung Manusia Asli (*Cleaned Traffic*):
* **Catatan Log Server (*Raw Hits*):** Mencatat ~4.076 requests (termasuk file CSS, JS, gambar hero, dan bot crawler).
* **Pengunjung Manusia Asli (*Cleaned Human Pageviews*):** **`2.144 Kunjungan / Bulan`** (setelah bot dan scanner disaring).
* **Perangkat Unik (*Unique Human IPs*):** **`1.094 Pengunjung Unik / Bulan`**.
* **Rata-rata Kunjungan Harian:** **`65 – 100 kunjungan per hari kerja`**.

### B. Karakteristik & Tren Pengunjung:
1. **Dominasi Perangkat B2B (Desktop PC/Laptop):** **`66.6%`** pengunjung mengakses dari komputer kantor/instansi saat jam kerja.
2. **Pengunjung Smartphone (Mobile):** **`33.4%`** pengunjung mengakses via ponsel (direct link/WhatsApp/Instagram).
3. **Pola Siklus Harian (*Day-over-Day*):**
   * ⚡ **Awal Pekan (Senin):** Rebound tajam naik lebih dari **+100%** saat jam kantor dimulai.
   * 🔥 **Hari Paling Ramai:** Rabu & Kamis (Puncak aktivitas pencarian pengadaan AV).
   * 📉 **Akhir Pekan (Sabtu & Minggu):** Trafik turun alami karena libur kantor.
4. **Tren Mingguan:** Mengalami tren kenaikan konsisten sebesar **`+29.0%`** di akhir bulan September.

---

## 2. 🎯 Sistem Pelacak Leads WhatsApp (*Server-Side Lead Tracker*)

### A. Mengapa Diperlukan Tracker Khusus?
Tautan WhatsApp (`https://wa.me/628119255476`) adalah tautan keluar (*outbound link*). Log server web biasa tidak dapat mencatat klik keluar secara otomatis. Oleh karena itu, dibangun sistem tracker berbasis **`navigator.sendBeacon`** yang mengirimkan event klik secara instan ke server tanpa memperlambat loading browser.

### B. Arsitektur Teknis Sistem:
* **Backend Endpoint:** `https://mitsindo.co.id/api/track-lead.php`
* **Penyimpanan Log:** `public_html/api/leads_data.jsonl` (Dilindungi `.htaccess` dari akses download publik).
* **Frontend Listener:** Terintegrasi pada `/js/main.js?v=20260929` dan `/js/tracker.js` di seluruh halaman website (Homepage, Produk, dan 10 Artikel Blog).
* **Metode Pengiriman:** Asynchronous `navigator.sendBeacon` (fallback: `fetch keepalive`).

### C. 4 Parameter Data yang Direkam Otomatis:
1. ⏰ **Waktu & Jam (WIB):** Tanggal dan waktu klik presisi sesuai Waktu Indonesia Barat.
2. 🔘 **Nama & Posisi Tombol (*CTA Location*):**
   * *Floating Button WA (Pojok Kanan Bawah)*
   * *Hero Banner CTA ("KONSULTASI GRATIS")*
   * *Blog Article CTA Box (Di Bawah Artikel Solusi)*
   * *Product Page / Contact Card CTA*
3. 📄 **Halaman Asal (*Source Page*):** URL & Judul halaman spesifik tempat calon klien berada saat mengklik.
4. 📱 **Perangkat & Jaringan Pengunjung:** Deteksi device (Windows PC, Mac, Android, iPhone) dan IP address.

---

## 3. 📊 Dashboard Master Analytics & Leads Terpadu (All-in-One Command Center)

### A. Akses Dashboard Resmi (Satu-Satunya):
* **URL Master Dashboard:** 👉 `https://mitsindo.co.id/api/dashboard.php?key=mitsindo2026`
* **Keamanan:** Dilindungi parameter rahasia `?key=mitsindo2026` dan proteksi database `.htaccess`.
* **Catatan Server:** Seluruh file redundan/testing lama telah dihapus bersih dari server cPanel untuk menjaga performa server tetap maksimal, ringan, dan cepat.

### B. 5 Metrik Utama yang Ditampilkan Secara Presisi:
1. 👥 **Total Visitors / Unique Users:** Jumlah orang unik yang berkunjung.
2. 📄 **Total Pageviews:** Jumlah akumulatif halaman yang dibuka.
3. ⏱️ **Average Session Duration:** Rata-rata lama waktu pengunjung membaca halaman (detik/menit).
4. 📉 **Bounce Rate:** Persentase pentalan (kunjungan < 10 detik tanpa interaksi vs engaged > 10 detik).
5. 🟢 **Real-Time Active Users:** Jumlah pengunjung yang sedang online di website Mitsindo detik ini (detak heartbeat 3 menit).

### C. Tabel & Visualisasi yang Tersedia:
* **Grafik Tren Harian:** Pageviews & Visitors Day-by-Day.
* **Grafik Segmentasi Device:** Proporsi Desktop PC vs Mobile Smartphone.
* **Tabel Top Pages & Reading Duration:** Mengetahui artikel dan produk mana yang paling lama dibaca.
* **Tabel Live Recent Sessions:** Memantau ID sesi, halaman yang dibuka, durasi aktif, dan status interaksi pengunjung secara real-time.

---

## 4. 💡 Pemahaman Metrik: Klik Tombol vs Pesan Terkirim

| Parameter | Definisi | Lokasi Pencatatan |
|---|---|---|
| **Klik Tombol WhatsApp (*Click Intent*)** | Pengunjung menekan tombol WA di website untuk membuka chat. | ✅ **Tercatat Real-Time di Dashboard Server Kita** |
| **Pesan Terkirim (*Sent Message*)** | Pengguna menekan tombol "Kirim / Send" di dalam aplikasi WhatsApp. | 🔒 **Hanya Terlihat di Aplikasi WhatsApp HP Admin** |

* **Estimasi Rasio Konversi:** Rata-rata industri mencatat **70% – 85%** dari orang yang mengeklik tombol WA akan lanjut mengirim pesan ke admin.
* **Fungsi Dashboard:** Menjadi indikator akurat untuk mengukur daya tarik halaman artikel, promosi banner, dan performa tim marketing dalam memancing minat prospek.

---

## 5. 📁 File & Aset Terkait di Server Hermes
* **Screenshot Dashboard Pelacak Klik Live:** `/home/ubuntu/MITSINDO_LIVE_WHATSAPP_CLICKS_DASHBOARD.png`
* **Screenshot Dashboard Analitik Bulanan:** `/home/ubuntu/MITSINDO_MONTHLY_LEADS_DASHBOARD_SEP2026.png`
* **File Master Laporan Excel (.xlsx):** `/home/ubuntu/LAPORAN_BULANAN_LEADS_WHATSAPP_MITSINDO_SEP2026.xlsx`
* **File Dashboard HTML Interaktif:** `/home/ubuntu/mitsindo_monthly_leads_dashboard.html` & `/home/ubuntu/mitsindo_traffic_dashboard.html`
* **Buku Induk Master Mitsindo:** `[[00_BUKU_PEMBAHASAN_MITSINDO.md]]`
