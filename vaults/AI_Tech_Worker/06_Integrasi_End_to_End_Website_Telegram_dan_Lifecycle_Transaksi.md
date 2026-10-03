# 06. Integrasi End-to-End Website, Telegram Gateway, dan Lifecycle Transaksi

Dokumen ini menjelaskan arsitektur integrasi lintas antarmuka antara Website Multi-Page SaaS (`http://43.134.179.61:8088/`), Bot Telegram (`@Olo_SBT_bot`), Payment Gateway BuatQris, dan Database Billing `tech_worker_billing.db`.

---

## 🏗️ 1. Arsitektur Komunikasi & Alur Data

```
+-------------------------------------------------------------------------------+
|                               1. WEBSITE FRONTEND                             |
|  - Katalog Skill (/skills), Pricing (/pricing), Solusi (Enterprise/UMKM)     |
|  - Modal Dynamic QRIS BuatQris (Auto Code Unik)                              |
|  - Deep-Link: https://t.me/Olo_SBT_bot?start=trx_<TRANSACTION_ID>             |
+---------------------------------------+---------------------------------------+
                                        | (Klik Hubungkan ke Telegram)
                                        v
+-------------------------------------------------------------------------------+
|                             2. TELEGRAM GATEWAY                               |
|  - Profil: `profil-admin-mvp` (Bot @Olo_SBT_bot)                              |
|  - Menerima Inbound Event: `/start trx_<ID>` atau `/start` biasa             |
|  - Bridge Gateway: `gateway/ai_tech_worker_bridge.py`                          |
+---------------------------------------+---------------------------------------+
                                        | (Cek & Bind User ke Transaksi)
                                        v
+-------------------------------------------------------------------------------+
|                             3. BACKEND & BILLING DB                           |
|  - Database SQLite: `tech_worker_billing.db` (Tabel `users`, `transactions`)  |
|  - FastAPI Service di port `8088` (`ai-tech-worker.service`)                  |
|  - CLI Helper: `cli_billing.py`                                               |
+---------------------------------------+---------------------------------------+
                                        ^
                                        | (Callback Webhook HMAC-SHA256)
+---------------------------------------+---------------------------------------+
|                             4. BUATQRIS OPEN API                              |
|  - Endpoint Webhook: `http://43.134.179.61:8088/api/payment/webhook`          |
|  - Validasi Signature: `X-BuatQris-Signature` (whsec_...)                     |
|  - Auto-Settlement & Unlock Kuota Task (+8, +50, +150, +350)                 |
+-------------------------------------------------------------------------------+
```

---

## 🔗 2. Mekanisme Deep-Linking Website $\rightarrow$ Telegram

Ketika pengunjung memilih paket di website:
1. **Generate Invoice:** Frontend memanggil `POST /api/payment/create-qris` dengan pilihan tier (`STARTER`, `ADVANCE`, `PRO`, atau `TRIAL`).
2. **Penerbitan QRIS:** API BuatQris mengembalikan `transaction_id` (contoh: `5SYK-2625-10Y8-0392`), `total_amount` (contoh: `Rp 249.918`), dan `qr_url`.
3. **Deep-Link URL Injection:** Tombol *"Hubungkan & Buka Bot Telegram"* pada modal QRIS secara dinamis dipasangi tautan:
   ```
   https://t.me/Olo_SBT_bot?start=trx_5SYK-2625-10Y8-0392
   ```
4. **Binding Transaksi:** Saat Telegram terbuka dan user menekan Start, gateway membaca parameter `trx_5SYK-2625-10Y8-0392`, lalu memperbarui kolom `telegram_id` pada record transaksi di database agar terikat resmi ke ID Telegram user tersebut.

---

## 💳 3. Lifecycle Pembayaran & Skenario User

### Skenario A: User Klik Hubungkan ke Telegram Terlebih Dahulu, Lalu Bayar
1. User klik *"Hubungkan & Buka Bot Telegram"*.
2. Telegram menampilkan rincian pesanan berstatus `⏳ Menunggu Pembayaran` beserta gambar QRIS dan nominal pas.
3. User melakukan transfer via m-Banking/e-Wallet.
4. BuatQris mengirim webhook callback ke `/api/payment/webhook`.
5. Server memvalidasi signature HMAC-SHA256, menambahkan kuota task, dan mengirimkan pesan notifikasi sukses ke Telegram user:
   ```markdown
   🎉 *PEMBAYARAN QRIS TERVERIFIKASI!* 🚀

   • Paket: ADVANCE
   • Kuota Masuk: +150 Tasks
   • Total Sisa Kuota: 150 Tasks

   AI Tech Worker Anda sudah aktif dan siap mengeksekusi instruksi tugas sekarang! 🚀
   ```

### Skenario B: User Bayar di Web DULU, Baru Buka Telegram (*Post-Payment Claim*)
1. User langsung scan dan bayar QRIS di layar laptop/web tanpa membuka Telegram terlebih dahulu.
2. Webhook masuk ke server dan menandai status transaksi sebagai `success`.
3. Ketika user kemudian mengklik *"Hubungkan & Buka Bot Telegram"*, bot menerima `/start trx_<ID>`.
4. Sistem gateway mendeteksi bahwa transaksi ini sudah berstatus `success`, dan seketika itu juga **mencairkan dan menambahkan kuota task ke akun Telegram user**.

---

## 🎟️ 4. Mekanisme Aktivasi Free Trial (Rp 1.000)

Untuk mencegah spam dan memverifikasi identitas pengguna baru:
1. User baru yang menekan `/start` polos di Telegram otomatis dibuatkan QRIS Aktivasi Trial (Rp 1.000 + 3 digit kode unik).
2. Bot mengirim pesan sambutan berformat:
   ```markdown
   🎉 *SELAMAT DATANG DI AI TECH WORKER!* 🚀

   Saya adalah asisten dan pekerja teknologi virtual mandiri Anda untuk Coding Fullstack, DevOps VPS, Data Scraping, dan Otomasi Bisnis.

   🎟️ *AKTIVASI FREE TRIAL (8 TASKS)*
   Untuk memverifikasi akun Anda dan mengaktifkan kuota 8 tugas percobaan gratis:

   • Nominal Aktivasi: *Rp 1,079* (Wajib pas 3 digit kode unik)
   • Kuota Didapat: *8 Tasks Eksekusi Nyata*
   • ID Tagihan: `3RHV-26X2-10V8-032P`
   • Masa Berlaku: `2026-10-03 10:57:38`

   💡 *Langkah Pembayaran:*
   1. Scan QRIS di atas via *BCA Mobile, Livin Mandiri, GoPay, Dana, OVO, atau ShopeePay*.
   2. Pastikan nominal transfer tepat *Rp 1079*.
   3. Begitu transfer berhasil, sistem webhook otomatis membuka kuota 8 task Anda dalam hitungan detik!

   🌐 Website Resmi: http://43.134.179.61:8088/
   ```
3. Begitu transfer Rp 1.0xx masuk, webhook memvalidasi dan mengaktifkan **8 Token Tasks**.

---

## ⚡ 5. Konsumsi Kuota Token (Deduct Engine)

1. **Pengecekan Pra-Eksekusi:** Sebelum menjalankan tugas (Fullstack, DevOps, Scraping), agen memeriksa saldo kuota user via database.
2. **Eksekusi Tugas:** Agen menyelesaikan perintah teknis sampai tuntas dan terverifikasi.
3. **Pemotongan Saldo:** Script `cli_billing.py deduct --telegram-id <ID> --count 1` dijalankan untuk mengurangi 1 kuota.
4. **Pelaporan Saldo:** Sisa saldo dilampirkan pada laporan hasil tugas di Telegram (`📊 Sisa kuota Anda: N Tasks`).
5. **Paywall Terkunci:** Jika saldo = 0, agen secara otomatis menyajikan pilihan paket top up dan tautan web `/pricing`.

---

## 🛡️ 6. Keamanan & Konfigurasi Server

- **No-Cache Middleware:** FastAPI menyematkan header `Cache-Control: no-cache, no-store, must-revalidate` pada seluruh route web agar perubahan UI/harga selalu termuat instan di browser user.
- **Isolasi Kredensial:** Seluruh secret key (`BUATQRIS_SECRET_TOKEN`, `BUATQRIS_SIGNING_SECRET`, `TELEGRAM_BOT_TOKEN`) tersimpan di `/home/ubuntu/ai_tech_worker/.env` berizin `600`.
- **Systemd Management:** Service backend berjalan stabil 24/7 di bawah unit `ai-tech-worker.service` pada port `8088`.
