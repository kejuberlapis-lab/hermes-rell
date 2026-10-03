# Vault: AI Tech Worker (All-in-One Virtual Tech SaaS)

## 📌 Gambaran Umum Proyek
**AI Tech Worker** adalah produk SaaS berbasis Telegram AI Agent yang mengotomatisasi pekerjaan teknis end-to-end (Software Engineering, DevOps, Data Analyst, Web/App Scraping, Admin Operations). 

Berbeda dengan chatbot pasif (ChatGPT/Gemini), AI Tech Worker bertindak sebagai **pekerja virtual otonom** yang mampu mengeksekusi aksi nyata di server, terminal, browser stealth, database, dan repositori kode.

---

## 🗂️ Struktur Dokumen Vault

| Dokumen | Topik & Cakupan |
| :--- | :--- |
| [[01_Arsitektur_Sistem_dan_Paywall_QRIS]] | Blueprint arsitektur middleware, validasi pembayaran, dan flow gateway |
| [[02_Skema_Paket_Pricing_dan_Kuota_Token]] | Struktur harga (Starter, Advance, Pro), kuota task, dan mekanisme 8-token trial |
| [[03_Spesifikasi_API_Payment_Gateway_QRIS]] | Integrasi dynamic QRIS (Tripay, Pakasir, Duitku, Midtrans) & payload webhook |
| [[04_Implementasi_Middleware_dan_Webhook_FastAPI]] | Kode backend Python FastAPI, database SQLite/PostgreSQL, dan router callback |
| [[05_Konfigurasi_Bot_Telegram_dan_Hermes_Profile]] | Setup profil Hermes, isolasi environment, dan system prompt multi-jobdesk |
| [[06_Integrasi_End_to_End_Website_Telegram_dan_Lifecycle_Transaksi]] | Mekanisme Deep-Link website-to-bot, binding transaksi, aktivasi trial Rp 1k, dan webhook |

---

## 🚀 Fitur Utama & Value Proposition
1. **Pay-to-Unlock / Auto-QRIS Gateway:** User menekan `/start` -> jika belum berlangganan, bot langsung menyajikan pilihan paket dan QRIS dinamis.
2. **Instant Auto-Activation:** Pembayaran terkonfirmasi via webhook dalam hitungan detik, saldo token/task langsung masuk, dan bot siap dipakai.
3. **8-Token Free Trial:** Setiap user baru mendapatkan 8 token uji coba untuk menyelesaikan 1 tugas penuh dan mencoba jobdesk kedua.
4. **Proactive & Autonomous:** Deteksi error otomatis, perbaikan mandiri (*self-healing*), dan pelaporan hasil kerja terverifikasi.
5. **Multi-Jobdesk Capability:** 
   - **DevOps:** Setup VPS, Docker, SSL/Nginx, Systemd, CI/CD, Cron.
   - **Full-Stack:** Debugging kode, API backend, frontend fix, database querying.
   - **Data & Ops:** Web scraping, data entry, Google Sheets automation, PDF extraction.

---
*Dibuat & Disinkronkan: Oktober 2026 | Ekosistem Hermes AI Agent*
