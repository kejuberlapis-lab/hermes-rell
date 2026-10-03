---
name: vps-linux-server-hardening
description: Use when securing Linux VPS. Sets UFW, SSH, & fail2ban.
---

# Production Linux VPS Hardening & Security Standard

Prosedur pengamanan server Linux VPS Ubuntu/Debian untuk layanan komersial.

### Protokol Keamanan Server:
1. **Manajemen Port & Firewall (UFW):**
   - Hanya buka port yang benar-benar aktif digunakan publik (Port 80 HTTP, Port 443 HTTPS, Port SSH).
   - Blokir akses publik ke port database internal (PostgreSQL 5432, MySQL 3306, Redis 6379) dan arahkan via localhost/Unix socket.

2. **Pengamanan SSH & Akses Remote:**
   - Wajib gunakan autentikasi kunci SSH (ed25519/RSA-4096) dan nonaktifkan login root langsung via password publik jika sudah ada sudo user.
   - Pasang perlindungan brute-force seperti fail2ban untuk membatasi percobaan login berulang.

3. **Isolasi Service & Hak Akses:**
   - Jalankan daemon aplikasi web dengan user non-root atau environment terisolasi.
   - Kunci permission file kredensial (.env) ke mode 600 (chmod 600 .env).
