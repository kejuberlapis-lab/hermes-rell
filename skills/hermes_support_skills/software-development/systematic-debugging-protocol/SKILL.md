---
name: systematic-debugging-protocol
description: Use when debugging code. 4-phase root cause diagnosis.
---

# Systematic 4-Phase Debugging Protocol

Standar operasional penanganan bug dan error sistematis untuk AI Tech Worker.

### 4 Fase Diagnosis Root Cause:
1. **Fase 1 - Observasi & Reproduksi Masalah:**
   - Dilarang menebak penyebab error sebelum membaca pesan error dan file log asli secara lengkap.
   - Periksa status proses, kode exit, dan traceback secara menyeluruh.

2. **Fase 2 - Isolasi Sumber Error (Root Cause Isolation):**
   - Periksa file konfigurasi terkait, tipe data input, dan dependensi pustaka.
   - Bedah baris kode yang memicu eksepsi menggunakan pembacaan file terarah.

3. **Fase 3 - Solusi Bedah Presisi (Surgical Fix):**
   - Terapkan perbaikan pada titik akar masalah, bukan hanya membungkus dengan try-catch kosong.
   - Jaga agar perubahan tidak merusak modul lain yang bergantung padanya.

4. **Fase 4 - Verifikasi Eksekusi Nyata:**
   - Jalankan ulang script atau restart service.
   - Uji dengan request nyata untuk memastikan status 200 OK dan fungsionalitas berjalan normal.
