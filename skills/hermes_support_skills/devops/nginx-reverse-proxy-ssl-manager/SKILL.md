---
name: nginx-reverse-proxy-ssl-manager
description: Use when setting Nginx & SSL. Configures proxy & HTTPS.
---

# Nginx Reverse Proxy & Automated SSL Manager

Standar konfigurasi Web Server Nginx reverse proxy dan Certbot SSL Let's Encrypt.

### Prosedur Konfigurasi & Pemeliharaan:
1. **Virtual Host & Reverse Proxy:**
   - Arahkan domain publik ke port lokal backend (misal port 8088 atau 8085) dengan header proxy standar (Host, X-Real-IP, X-Forwarded-For, X-Forwarded-Proto).
   - Konfigurasikan client_max_body_size yang memadai untuk upload file.

2. **Sertifikat SSL Let's Encrypt Otomatis:**
   - Pasang SSL via Certbot dengan auto-redirect HTTP ke HTTPS 301 permanen.
   - Pastikan konfigurasi perpanjangan otomatis (cron/certbot.timer) aktif.

3. **Proteksi Cache Dinamis:**
   - Tambahkan header no-cache (Cache-Control: no-store, no-cache, must-revalidate) pada aplikasi dinamis untuk mencegah browser menyajikan data usang.
   - Selalu uji sintaks dengan `nginx -t` sebelum melakukan reload service.
