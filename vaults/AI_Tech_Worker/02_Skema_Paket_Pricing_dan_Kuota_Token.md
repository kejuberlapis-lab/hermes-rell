# 02 - Skema Paket, Pricing & Kuota Token

## 1. Struktur Tiering Harga (Subscription & Pay-per-Task)

| Paket | Harga (IDR) | Alokasi Kuota | Target Pengguna | Fitur Utama |
| :--- | :--- | :--- | :--- | :--- |
| **Free Trial** | **Rp 0** | **8 Token** | Pengguna Baru | 1 Tugas penuh selesai + Uji coba 1 jobdesk tambahan. |
| **Starter** | **Rp 100.000** | **50 Tasks** | Freelancer / Solo Dev | Eksekusi script, bug fix ringan, DevOps dasar, scraping. |
| **Advance** | **Rp 249.000** | **150 Tasks** | Startup / Agensi Kecil | Multi-file coding, setup server lengkap, database ops, prioritas antrian. |
| **Pro Enterprise** | **Rp 499.000** | **350 Tasks** | Bisnis / Tim Teknis Aktif | Full autonomous pipeline, browser stealth unblock, integrasi API custom, 24/7 background worker. |

---

## 2. Mekanisme Perhitungan Token (Token Consumption Logic)

1. **Definisi 1 Task Standar (1 Token):**
   - 1 siklus pengerjaan instruksi yang menghasilkan artefak kerja riil (misal: "Install Docker dan Nginx di VPS saya", "Perbaiki bug CORS di FastAPI ini", "Ambil 100 data tabel dari URL X").
   - Termasuk auto-retry dan perbaikan jika kode menghasilkan error syntax.

2. **Konsumsi Multi-Token (Heavy Pipeline):**
   - **Tugas Ringan / Q&A Teknis:** 1 Token
   - **Eksekusi Full-Stack / Multi-File Refactor (3+ file):** 2 Token
   - **Deep Autonomous Research / Heavy Scraping + Anti-Bot:** 3 Token

3. **Proteksi Anti-Pemborosan (Fair Use Policy):**
   - Jika AI gagal menyelesaikan tugas karena kesalahan internal sistem, token **di-refund otomatis** ke saldo user.
   - User dapat memeriksa saldo kapan saja dengan perintah `/saldo` atau `/status`.

---

## 3. Strategi Konversi dari 8-Token Free Trial
- **Desain Trial 8 Token:**
  - Token 1–4: Digunakan untuk menyelesaikan 1 tugas nyata pertama user hingga tuntas (bukti kapabilitas kerja nyata, bukan sekadar chat).
  - Token 5–8: Digunakan untuk memancing user mencoba jobdesk kedua (misal dari perbaikan kode lanjut ke otomatisasi server).
- **Trigging Paywall:**
  - Saat sisa token = 1, bot memberikan notifikasi lembut (*soft nudge*).
  - Saat sisa token = 0, bot menampilkan preview hasil yang belum selesai dan menyajikan QRIS untuk melanjutkan.
