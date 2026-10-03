---
name: virtual-tech-worker-suite
description: "Use when deploying AI sales, CRM, CAPI, or agent flows."
---

# Virtual Tech Worker Commercial Suite

Protokol operasional komprehensif untuk mengoperasikan 5 pilar modul bisnis enterprise: AI Sales & Order Automation, Marketing & Campaign Tools, Omnichannel CRM & Ticketing, Custom AI Agent Builder, dan Open API Integrations.

---

## 1. Modul Penjualan & Otomatisasi Pesanan (AI Sales & Order Automation)

### A. Pengecekan Ongkir & Kurir Otomatis (Multi-Courier Engine)
- **Cakupan Kurir:** JNE, J&T, SiCepat, AnterAja, Ninja, POS Indonesia, ID Express, Lion Parcel, Gosend/GrabExpress.
- **Logika Eksekusi:**
  1. Ekstrak entitas alamat: Kecamatan, Kota/Kabupaten, Kode Pos, Berat barang (gram), Dimensi (PxLxT).
  2. Hitung berat volumetrik: `(P x L x T) / 6000` (dibulatkan ke atas).
  3. Query tarif API pengiriman (RajaOngkir / Biteship / internal courier gateway).
  4. Sajikan pilihan terstruktur dalam chat: Layanan Regular, Next Day, Kargo, dan Instant lengkap dengan estimasi tiba (ETD).

### B. Pembayaran Instant via QR (Dynamic QRIS & Payment Link)
- **Integrasi Gateway:** BuatQris Open API, Midtrans, Xendit, Doku.
- **Standar Output:**
  - QRIS Dinamis (string payload QRIS berstandar EMVCo / PNG image).
  - Tautan Pembayaran (Payment URL) dengan masa kadaluwarsa (TTL 15-60 menit).
  - Validasi nominal otomatis (termasuk biaya admin / kode unik bila diperlukan).
  - Webhook callback listener dengan verifikasi signature HMAC-SHA256.

### C. Manajemen Stok & Produk (Knowledge Base & Multi-Varian)
- **Struktur Katalog:**
  ```json
  {
    "sku": "PROD-001",
    "name": "Virtual Tech Worker Starter",
    "variants": [
      {"id": "V1", "name": "Bulanan", "price": 99000, "stock": 999},
      {"id": "V2", "name": "Tahunan", "price": 990000, "stock": 999}
    ],
    "description": "Akses 10 divisi bisnis via Telegram",
    "is_active": true
  }
  ```
- **Aturan Reservasi:** Kunci stok sementara selama 30 menit saat QRIS dibuat; batalkan kunci jika kadaluwarsa.

---

## 2. Marketing & Campaign Tools

### A. Targeted Broadcast Marketing (Segmented Blast Berizin)
- **Segmentasi Pelanggan (RFM Matrix):**
  - *Champions:* Transaksi sering & nominal tinggi -> Penawaran VIP & Akses Awal.
  - *Potential Loyalists:* Baru repeat order -> Paket Membership / Upgrade Tier.
  - *At-Risk / Dormant:* Tidak aktif >30 hari -> Voucher Re-engagement & Promo Spesial.
- **Kepatuhan Saluran:** Gunakan template WhatsApp Business API resmi berstatus Approved atau Bot Telegram broadcast dengan rate limiting (maksimal 20-30 pesan/detik).

### B. AI Automated Follow-Up (Abandoned Cart Recovery)
- **Rhythm & Cadence Follow-Up:**
  1. *Follow-Up 1 (15 Menit Pasca-Checkout):* Pengingat ramah + bantuan kendala transfer.
  2. *Follow-Up 2 (2 Jam Pasca-Checkout):* Informasi batas reservasi stok + kemudahan bayar QRIS.
  3. *Follow-Up 3 (24 Jam Pasca-Checkout):* Penawaran bonus / free trial konsultasi sebelum tagihan ditutup.
- **Tone of Voice:** Solutif, santun, tidak agresif/spammy.

### C. Atribusi Iklan & CAPI Integration (Meta Ads / Google Ads)
- **Server-Side Event Tracking:**
  - `Lead` -> Saat prospek pertama kali berinteraksi dan memberikan kontak.
  - `InitiateCheckout` -> Saat QRIS / Invoice digenerasikan.
  - `Purchase` -> Saat webhook pembayaran terverifikasi sukses.
- **Parameter Wajib:** Event ID, Timestamp, Value, Currency (`IDR`), Hashed User Data (SHA256 email/phone).

---

## 3. Modul Manajemen Hubungan Pelanggan (Omnichannel CRM & Ticketing)

### A. Kanban & Pipeline Management
- **Stage Alur Penjualan:**
  `[New Lead]` -> `[Needs Assessment]` -> `[Quotation Sent]` -> `[Payment Pending]` -> `[Closed Won / Active]` -> `[Retention]`
- **Auto-Transition Hook:** Perubahan stage terjadi otomatis berbasis trigger aksi pelanggan (misal: generate invoice otomatis memindahkan kartu ke `Payment Pending`).

### B. Ticketing System & Cross-Division Escalation
- **Struktur Tiket:**
  - `Ticket_ID`: Format `TICK-YYYYMMDD-XXXX`
  - `Severity`: `P1 (Critical/Payment Block)`, `P2 (Feature Bug)`, `P3 (General Inquiry)`
  - `Assigned_Team`: `Tech`, `Finance`, `Legal`, `Operations`
  - `SLA Target`: P1 (<15 menit), P2 (<2 jam), P3 (<24 jam).

### C. Auto-Assignment & Human Handoff Protocol
- **Trigger Eskalasi ke Agen Manusia:**
  1. Pelanggan mengetik *"Bicara dengan admin"*, *"Komplain"*, *"Refund"*.
  2. AI mendeteksi sentimen negatif/marah secara berturut-turut.
  3. Kebutuhan kustomisasi kontrak hukum di luar template baku.
- **Handoff Action:** AI mem-pause respon otomatis pada thread tersebut, mengirim notifikasi rangkuman percakapan (Executive Summary) ke admin grup internal, dan menandai status `Assigned to Human`.

---

## 4. Custom AI Agent Builder & Visual Flow Designer

### A. AI Multi-Agent Specialists
- **Agen Sales Closer:** Fokus pada identifikasi kebutuhan, rekomendasi paket, dan konversi QRIS.
- **Agen Technical Support:** Mengakses knowledge base teknis, dokumentasi API, dan troubleshooting error.
- **Agen Billing & Finance:** Rekonsiliasi mutasi, penerbitan invoice PDF, dan bukti potong pajak.

### B. Visual Flow State Machine Logic
- Mengoperasikan percakapan berbasis state machine deterministik:
  `State 0 (Greeting)` -> `State 1 (Pilih Layanan)` -> `State 2 (Input Data)` -> `State 3 (Konfirmasi & Bayar)` -> `State 4 (Aktivasi)`.

### C. Penjadwalan Operasional AI (Shift & After-Hours)
- Mode Jam Kerja (08.00 - 17.00 WIB): AI mendampingi agen manusia (*Copilot mode*).
- Mode Luar Jam Kerja / Hari Libur (17.00 - 08.00 WIB): AI beroperasi penuh secara mandiri (*Autonomous mode*), memproses order dan reservasi 24/7.

---

## 5. Fitur Integrasi (Open API & Third-Party Apps)

### A. RESTful Open API & Webhook Specifications
- Format Pertukaran: JSON murni (UTF-8).
- Otentikasi: Bearer Token JWT / API Key Header `X-API-Key`.
- Webhook Payload Security: Signature Header `X-Signature: HMAC_SHA256(payload, secret)`.

### B. Database & ERP Synchronization
- Dukungan database relasional (PostgreSQL, MySQL, SQLite) dan ERP (Odoo, Accurate, SAP).
- Sinkronisasi mutasi transaksi, update status pesanan, dan pembaruan master data barang secara terjadwal / real-time.

### C. E-Commerce Marketplace Sync
- Mengintegrasikan data pesanan dan resi pengiriman dari marketplace utama ke dalam satu dashboard konsolidasi.
