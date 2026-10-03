---
name: secret-sanitization-guard
description: Use when handling secrets. Prevents key & token leaks.
---

# Secret Sanitization & Sensitive Data Masking Guard

Protokol keamanan mutlak pencegahan kebocoran kredensial, token, dan data rahasia.

### Standar Sanitasi Data Rahasia:
1. **Zero-Leakage Policy:**
   - Dilarang keras menampilkan API Key, Secret Token, Private Key, DB Password, atau Master PIN di chat atau file repositori publik.
   - Wajib gunakan placeholder masking seperti `[REDACTED]` atau `sk-***`.

2. **Isolasi File Lingkungan (.env):**
   - Semua variabel rahasia wajib disimpan di file `.env` dengan permission `chmod 600`.
   - File `.env` wajib dimasukkan ke `.gitignore` dan script backup wajib menyaring isi file kredensial sebelum di-push.

3. **Penyaringan Output Terminal & Log:**
   - Periksa output curl, log gateway, atau print database agar tidak memuat header autentikasi secara telanjang.
