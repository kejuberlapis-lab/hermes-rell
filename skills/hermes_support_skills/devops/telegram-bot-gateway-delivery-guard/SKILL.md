---
name: telegram-bot-gateway-delivery-guard
description: "Use when sending Telegram bot notifications from backends."
---

# Telegram Bot Gateway Delivery & Dashboard Integration Guard

Protokol teknis untuk mengintegrasikan pengiriman pesan/notifikasi/OTP dari backend web ke Telegram, serta konsolidasi identitas pengguna pada dashboard operasional.

---

## 1. Telegram API Delivery Constraints & Pitfalls

### A. The "Chat Not Found" Constraint (400 Bad Request)
- **Mekanisme:** Telegram Bot API secara ketat melarang bot mengirim pesan pertama (`sendMessage`) ke user ID mana pun sebelum user tersebut membuka bot dan menekan tombol `/start` secara eksplisit.
- **Dampak:** Upaya pengiriman OTP atau notifikasi tagihan dari web backend ke ID Telegram baru akan gagal total dengan error:
  `{"ok": false, "error_code": 400, "description": "Bad Request: chat not found"}`.
- **Aturan Implementasi (Enforced Guard):**
  1. **Direct Deep Link Fallback:** Jika pengiriman gagal/status belum terhubung, selalu sediakan tombol atau tautan langsung `https://t.me/<bot_username>?start=auth` agar user dapat menginisiasi chat dalam 1 klik.
  2. **Alternative Instant Auth:** Selalu sediakan bypass sekunder (misal: Master Security PIN atau Web Password) agar pengguna tidak terblokir saat membutuhkan akses cepat.
  3. **Explicit Error Translation:** Tangkap HTTP 400 dari Telegram API dan ubah menjadi pesan panduan yang jelas (*"Akun belum mengklik /start di bot @..."*) daripada menampilkan error teknis mentah.

---

## 2. Multi-Profile Identity & Metric Consolidation

### A. Enriching User Data Across Gateways
Ketika membangun dashboard pemantauan operasional yang terhubung dengan bot Telegram:
1. **Query Database Billing/SaaS:** Ambil daftar `telegram_id`, status kuota, dan transaksi.
2. **Cross-Reference Gateway Directory:** Baca `channel_directory.json` dari profil Telegram bot untuk memetakan nama akun asli (`display_name` / `username`) pengguna.
3. **Session State Analytics:** Periksa `state.db` pada tabel `sessions` untuk menghitung volume pesan nyata (`message_count`) dan stempel waktu aktivitas terakhir (`last_seen`).

---

## 3. Dashboard Usability & Friction Governance

### A. Friction vs Security Decision Gate
- **Internal / Executive Dashboard:** Jika pemilik bisnis menghendaki visibilitas instan tanpa hambatan interaktif, hilangkan form login/modal OTP dan sajikan ringkasan data langsung (*Zero-Friction Access*).
- **Public Multi-Tenant Portal:** Terapkan isolasi sesi bertanda tangan HMAC-SHA256 dengan batas kedaluwarsa 24 jam.
