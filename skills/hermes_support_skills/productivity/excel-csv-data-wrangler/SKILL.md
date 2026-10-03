---
name: excel-csv-data-wrangler
description: Use when processing tabular data. Cleans CSV & Excel.
---

# Production Excel & CSV Data Wrangling Standard

Standar pembersihan, pengolahan, kalkulasi, dan automasi data tabular (CSV, Excel `.xlsx`).

### Standar Pengolahan Data:
1. **Pembersihan Data (Data Cleaning):**
   - Tangani missing values (`NULL`, `NaN`, whitespace kosong) secara eksplisit.
   - Standardisasi format tanggal (ISO 8601: `YYYY-MM-DD`), penulisan nomor telepon, dan kapitalisasi teks.

2. **Kalkulasi & Validasi Tipe Data:**
   - Konversi tipe data numerik dan mata uang ke integer/float sebelum kalkulasi matematika.
   - Validasi integritas baris data terhadap total ringkasan untuk mencegah kesalahan kalkulasi.

3. **Ekspor & Kompatibilitas:**
   - Ekspor CSV dengan encoding `utf-8-sig` (agar karakter Indonesia/khusus terbaca sempurna di Microsoft Excel).
   - Simpan hasil output ke path absolut yang terverifikasi.
