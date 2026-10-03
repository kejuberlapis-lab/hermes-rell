# 01 - Arsitektur Sistem & Paywall QRIS Dinamis

## 1. Diagram Alur Kerja (End-to-End Flow)

```
+-------------------------------------------------------------------------------+
|                                  PENGGUNA                                     |
|                            (Telegram App Client)                              |
+-------------------------------------------------------------------------------+
       │                                                         ▲
       │ 1. Kirim /start atau prompt perintah                   │ 6. Notifikasi Sukses
       │                                                         │    & Akses Terbuka
       ▼                                                         │
+-------------------------------------------------------------------------------+
|                        TELEGRAM GATEWAY / MIDDLEWARE                          |
|                       (FastAPI Service di Port 8086)                          |
+-------------------------------------------------------------------------------+
       │                                                         ▲
       │ 2. Cek Kuota & Status Langganan di Database             │ 5. Webhook
       │                                                         │    Callback Valid
       ▼                                                         │
+-----------------------+                         +-----------------------------+
|    DATABASE KUOTA     |                         |       PAYMENT GATEWAY       |
| (SQLite / PostgreSQL) |                         |  (Tripay / Pakasir / Mid)   |
+-----------------------+                         +-----------------------------+
       │                                                         ▲
       ├────── Kuota > 0 ──────► [Eksekusi Hermes AI Agent]     │
       │                         (Menjalankan task teknis)       │
       │                                                         │
       └────── Kuota == 0 ─────► [Generate Dynamic QRIS] ────────┘
                                 3. Request QR Code Unik
                                 4. Kirim Gambar QRIS + Timer ke User
```

---

## 2. Tahapan Transaksi & Validasi Akses

### Tahap A: Pengguna Baru (Onboarding & 8-Token Free Trial)
1. User menekan `/start`.
2. Middleware memeriksa apakah `telegram_id` sudah ada di database.
3. Jika belum pernah terdaftar:
   - Akun dibuat otomatis dengan status `TRIAL`.
   - Diberikan saldo **8 Token Trial**.
   - Bot mengirim pesan sambutan interaktif dan panduan eksekusi task pertama.

### Tahap B: Pengguna Habis Kuota (Paywall Intercept)
1. User mengirimkan prompt saat saldo token = 0.
2. Middleware mencegat (*intercept*) pesan sebelum sampai ke Hermes LLM Engine.
3. Bot membalas dengan pesan ringkas berisi:
   - Peringatan kuota habis.
   - Pilihan menu paket tombol inline: `[Starter - 50 Task]` `[Advance - 150 Task]` `[Pro - 350 Task]`.

### Tahap C: Pembayaran QRIS Dinamis
1. User menekan salah satu tombol paket.
2. Middleware memanggil API Payment Gateway untuk membuat transaksi QRIS dinamis:
   - Nominal sesuai paket + kode unik (jika gateway non-otomatis) atau dynamic payload QRIS string.
   - Expired timer: 15 menit.
3. Gateway mengembalikan QR image URL / raw QR string.
4. Bot mengirim gambar QRIS langsung ke chat Telegram user beserta detail tagihan.

### Tahap D: Verifikasi Webhook & Pembukaan Akses
1. User scan dan bayar melalui mobile banking / e-wallet (BCA, Mandiri, GoPay, Dana, OVO, ShopeePay, dll).
2. Server Payment Gateway mengirim HTTP POST Webhook ke endpoint VPS: `https://api.domain.com/api/payment/webhook`.
3. Middleware memverifikasi HMAC Signature / Secret Key untuk memastikan keaslian data.
4. Saldo token/task user diperbarui di database (`saldo += task_paket`).
5. Bot otomatis mengirim pesan ke Telegram:
   > *"✅ **Pembayaran Berhasil Dikonfirmasi!** Paket [Nama Paket] aktif. Anda memiliki [N] task. Silakan kirimkan instruksi teknis Anda sekarang!"*

---

## 3. Matriks Keamanan & Anti-Fraud
- **Signature Verification:** Setiap request webhook wajib divalidasi menggunakan HMAC SHA256 dengan secret key gateway.
- **Idempotency Key:** Mencegah dobel top-up jika webhook terpanggil lebih dari 1 kali untuk invoice yang sama.
- **Expired Order Lock:** Transaksi yang melewati batas waktu 15 menit otomatis berstatus `EXPIRED` dan tidak dapat diaktifkan.
- **Session Isolation:** Workspace setiap user di VPS terisolasi sehingga tidak ada tumpang tindih data atau perintah antar-pengguna.
