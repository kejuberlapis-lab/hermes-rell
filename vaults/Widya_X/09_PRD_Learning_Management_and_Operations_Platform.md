# 📑 09. Product Requirement Document (PRD): Widya.X Unified Learning & Operations Management Platform (Widya.X OS)

---

## 📌 1. Executive Summary & Product Vision

### 1.1 Judul Produk
**Widya.X OS (Unified LMS, ERP & Marketing Operations Platform)**

### 1.2 Visi Platform
Membangun satu sistem platform terpadu (*Single Source of Truth*) berbasis web & mobile-responsive yang mengintegrasikan seluruh operasional lembaga les **Widya.X**—mulai dari manajemen multi-cabang (2 cabang awal), manajemen siswa, monitoring pengajaran guru/instruktur, kurikulum & LMS 4 pilar (Robotik, AI, AI Agentic, Drone), hingga otomatisasi *digital marketing lead capture* dan integrasi WhatsApp Gateway.

### 1.3 Penanggung Jawab Utama
* **Product Owner & Executive Overseer:** Andi Saputra *(Operational Manager)*
* **Target Pengguna:**
  1. **Operational Manager / Super Admin:** Akses kontrol penuh multi-cabang, finansial, lead marketing, dan evaluasi guru.
  2. **Branch Admin / Front Office (Cabang 1 & Cabang 2):** Registrasi siswa, billing kasir/QRIS, jadwal kelas, dan customer service.
  3. **Guru / Instruktur (Mentor):** Presensi digital, jurnal kelas, upload progress belajar siswa, dan panduan silabus.
  4. **Siswa & Orang Tua (Student/Parent Portal):** Jadwal sesi, modul & video materi, portofolio proyek robotik/drone, dan laporan rapor digital.

---

## 🏗️ 2. Arsitektur Multi-Peran & Hirarki Akses (Role-Based Access Control)

```text
┌────────────────────────────────────────────────────────────────────────┐
│             WIDYA.X UNIFIED CLOUD ENGINE (FastAPI / PostgreSQL)        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
    ┌───────────────────────┬───────┴───────────────┬────────────────────────┐
    ▼                       ▼                       ▼                        ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ SUPER ADMIN      │ │ BRANCH ADMIN     │ │ INSTRUKTUR /     │ │ STUDENT & PARENT │
│ (Operational Mgr)│ │ (Cabang A & B)   │ │ MENTOR LAB       │ │ PORTAL (PWA)     │
├──────────────────┤ ├──────────────────┤ ├──────────────────┤ ├──────────────────┤
│ • Lintas 2 Cabang│ • Siswa Cabang     │ • Presensi Kelas   │ • Portofolio Siswa │
│ • Analytics P&L  │ • Kasir & Tagihan  │ • Jurnal Belajar   │ • Modul & Challenge│
│ • Lead Marketing │ • Jadwal Ruang Lab │ • Nilai Rapor Siswa│ • Rapor Digital    │
│ • Mutasi Inventar│ • CRM Orang Tua    │ • Unduh Modul/Code │ • Invoices & QRIS  │
└──────────────────┘ └──────────────────┘ └──────────────────┘ └──────────────────┘
```

---

## 🧩 3. Rincian Modul Fungsional Platform

### 🏢 MODUL 1: MULTI-BRANCH & OPERATIONAL MANAGEMENT (2 CABANG)
* **Pilihan Switcher Cabang:** Super Admin dapat berpindah (*toggle switch*) antara **Cabang 1 (Pusat)** dan **Cabang 2 (Satelit)** atau melihat agregasi data konsolidasian (*All Branches*).
* **Manajemen Ruang & Jadwal Lab:** 
  * Penjadwalan penggunaan Lab Robotika, Lab Komputasi AI, dan Arena Jaring Drone per cabang untuk mencegah jadwal tabrakan (*schedule collision detector*).
* **Inventarisasi Hardware Lintas Cabang:** 
  * Pelacakan status unit (Robot Yanshee, Drone Kit, Mikrokontroler, FPV Goggles) dengan status: *Tersedia, Sedang Digunakan, Dalam Perbaikan, Rusak*.
  * Fitur Transfer Antar-Cabang (*Internal Stock Movement*).

---

### 🎓 MODUL 2: STUDENT MANAGEMENT & ACADEMIC LIFECYCLE
* **Database Profil Siswa:** Biodata siswa, kontak darurat orang tua, asal sekolah, level program (Junior, Intermediate, Advanced).
* **Smart Attendance (Presensi Digital):** 
  * Scan barcode/QR ID Card siswa atau centang cepat oleh instruktur kelas.
  * Otomatis memotong sisa kuota sesi belajar paket bulanan.
* **Student Portfolio Hub:**
  * Wadah digital tempat siswa mengunggah foto, video, dan link kode GitHub/proyek robotik/drone yang berhasil mereka rakit.
* **E-Report Card (Rapor Digital 3 Bulanan):**
  * Penilaian 5 dimensi: *Logika/Problem Solving, Keterampilan Hardware, Kreativitas, Resiliensi Troubleshooting, & Komunikasi*.
  * Cetak PDF resmi ber-QR Code verifikasi keaslian.

---

### 👨‍🏫 MODUL 3: INSTRUCTOR & TEACHING GOVERNANCE
* **Jadwal & Penugasan Mentor:** Kalender jadwal mengajar mentor per cabang lengkap dengan informasi jumlah siswa hadir.
* **Jurnal Mengajar Harian (*Teaching Log*):** 
  * Mentor wajib mengisi materi yang diajarkan, kendala teknis lab, dan catatan khusus per anak sebelum sesi dapat ditutup (*lock session*).
* **Evaluasi & KPI Guru:** Rating kepuasan orang tua, kedisiplinan jam hadir, dan keaktifan mendokumentasikan karya siswa.
* **Kalkulator Fee Mengajar (Automated Payroll):** Menghitung otomatis akumulasi honor mengajar mentor berdasarkan jumlah sesi reguler, private, atau workshop yang telah diselesaikan.

---

### 📚 MODUL 4: CONTENT MANAGEMENT & 4-PILLAR LMS
* **Repositori Silabus Terstruktur:**
  * **Pilar 1 (Robotics):** Modul PDF, skema wiring Fritzing, contoh program `.ino`/MicroPython, YanAPI Python.
  * **Pilar 2 (AI):** Jupyter Notebook tutorial, dataset gambar OpenCV, script YOLOv8.
  * **Pilar 3 (AI Agentic):** Workflow JSON, template prompt system, script function calling Hermes.
  * **Pilar 4 (Drone):** Diagram wiring flight controller, panduan Betaflight CLI, peta misi Mission Planner.
* **Weekly Hands-on Challenge:** Fitur misi tantangan mingguan berhadiah poin/badge gamifikasi bagi siswa yang berhasil menyelesaikan studi kasus khusus.

---

### 📢 MODUL 5: DIGITAL MARKETING & LEAD FUNNEL DASHBOARD
* **Lead Capture CRM:** Menampung data calon siswa yang mendaftar dari formulir web, link iklan IG/TikTok, dan roadshow sekolah.
* **Kanban Board Prospek:**
  * Kolom: `Lead Masuk` $\rightarrow$ `Dihubungi Admin` $\rightarrow$ `Jadwal Free Trial` $\rightarrow$ `Hadir Trial` $\rightarrow$ `Closing / Siswa Resmi` $\rightarrow$ `Lost / Batal`.
* **WhatsApp Automation Engine (Fonnte / Gateway API):**
  * Auto-send pesan sambutan & konfirmasi jadwal *Free Trial Class*.
  * Auto-reminder H-1 jadwal kelas reguler ke orang tua.
  * Push notifikasi tagihan SPP bulanan via WhatsApp lengkap dengan link Dynamic QRIS.
* **Campaign Attribution Analytics:** Melacak sumber pendaftaran siswa terbanyak (apakah dari Instagram Ads, TikTok, Roadshow Sekolah, atau Referral Rekan).

---

### 💳 MODUL 6: BILLING, PAYMENT GATEWAY & FINANCIAL REPORTS
* **Tagihan Otomatis SPP:** Sistem meng-generate invoice berkala setiap tanggal 25 untuk pembayaran bulan berikutnya.
* **Dynamic QRIS & VA Integration:** Pembayaran instan melalui QRIS nasional (BCA, Mandiri, BRI, GoPay, OVO, ShopeePay) dengan verifikasi otomatis webhook 24/7.
* **Laporan Finansial Cabang:** Laporan Arus Kas Masuk/Keluar, Laporan Profit/Loss per Cabang, dan Ringkasan Omzet Konsolidasian untuk Operational Manager.

---

## 🛠️ 4. Spesifikasi Teknis & Stack Rekomendasi

| Komponen Arsitektur | Teknologi Terpilih | Alasan Pemilihan |
| :--- | :--- | :--- |
| **Backend API** | **FastAPI (Python 3.11+)** | Sangat cepat, hemat memori RAM VPS, integrasi mudah ke AI Agent & script otomasi. |
| **Frontend UI Dashboard** | **Tailwind CSS + Alpine.js / Vue 3** | Tampilan modern *Clean Light & Dark Mode*, responsif mobile di HP orang tua & admin. |
| **Database Engine** | **PostgreSQL / SQLite Production** | Integritas data relasional multi-cabang yang kokoh dan ACID compliant. |
| **Penyimpanan Aset Media** | Local SSD Fast Storage / S3 Bucket | Menyimpan video demo siswa, foto presensi, dan modul PDF silabus. |
| **Notifikasi Gateway** | WhatsApp Gateway API + Webhook | Saluran komunikasi nomor 1 paling efektif untuk orang tua di Indonesia. |
| **Keamanan & Autentikasi** | JWT Auth, Role Guard, HTTPS Let's Encrypt | Mengisolasi data privat siswa dan rekap keuangan lembaga. |

---

## ⏱️ 5. Timeline Rencana Pengembangan (Phase 1 s.d. Phase 3)

* **Phase 1 (Minggu 1 - 3): Core Foundation & Multi-Branch CRM**
  * Setup database, manajemen 2 cabang, data master siswa, guru, dan jadwal kelas.
* **Phase 2 (Minggu 4 - 6): LMS 4 Pilar & WhatsApp Automation**
  * Upload silabus modul materi, presensi digital, rapor berkala, dan integrasi broadcast WA.
* **Phase 3 (Minggu 7 - 8): Billing QRIS & Marketing Analytics**
  * Integrasi pembayaran QRIS otomatis, dashboard metrik lead marketing, dan pengujian menyeluruh (UAT).
