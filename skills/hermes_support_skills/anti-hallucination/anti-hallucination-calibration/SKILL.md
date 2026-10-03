---
name: anti-hallucination-calibration
description: Use when making factual claims. Catches fabrication loops.
---

# Calibrated Anti-Hallucination & Fabrication Guard

Sistem kalibrasi internal untuk mendeteksi dan mencegah 4 pola halusinasi utama sebelum jawaban diserahkan ke user.

## 4 Pola Halusinasi yang Dicegah
1. **Fabrikasi (Fabrication):** Mengklaim file, fungsi, path, API endpoint, atau paper ada tanpa ada bukti `read_file`/`search_files`/`curl` di sesi ini.
2. **Ingatan Basi (Stale Recall):** Mengasumsikan data memori masa lalu sebagai fakta saat ini tanpa mengecek kondisi live sistem.
3. **Drift Parafrase Output Tool:** Merangkum output terminal/database secara longgar sehingga mengubah angka atau arti aslinya.
4. **Kepercayaan Diri Tanpa Bukti (Unhedged Confidence):** Memberikan pernyataan pasti atas hal yang belum diuji secara teknis.

## Checklist Hening Sebelum Mengirim Jawaban (Silent Pre-Flight Gate)
- Apakah saya menyebut nama file/fungsi yang belum saya baca di sesi ini? $\rightarrow$ *Jalankan tool terlebih dahulu.*
- Apakah saya menyebut status server/service aktif tanpa `curl` atau `systemctl status`? $\rightarrow$ *Verifikasi dulu.*
- Apakah saya menyatakan scraping selesai tanpa menghitung baris file fisik di disk? $\rightarrow$ *Cek file fisik dulu.*
