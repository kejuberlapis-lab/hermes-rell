---
title: BAB 4 - Hasil dan Pembahasan
author: 124230117_Stefano Garrent Khristiawan
date: 2026-09-29
status: Draft
tags:
  - skripsi
  - naskah
  - bab4
  - hasil
  - pembahasan
---

# BAB 4. HASIL DAN PEMBAHASAN

Kembali ke [[MOC - Skripsi]] | Sebelumnya: [[BAB 3 - Metodologi Penelitian]] | Lanjut ke [[BAB 5 - Kesimpulan dan Saran]]
Terkait: [[Analisis & Hasil Pengujian]]

---

> [!warning] **Aturan Emas Bab 4**
> **Hasil ≠ Pembahasan!**
> - **Hasil (4.1 & 4.2):** Menyajikan data mentah/olahan, grafik, angka metrik secara objektif tanpa opini.
> - **Pembahasan (4.3):** Memberikan interpretasi ilmiah mendalam: **MENGAPA** hasilnya seperti itu? Apa faktor penyebabnya? Bagaimana perbandingannya dengan teori di Bab 2 dan riset peneliti terdahulu?

---

## 4.1 Hasil Eksperimen dan Pengujian

### 4.1.1 Hasil Pra-pengolahan Data
- Distribusi data sebelum dan sesudah cleaning.
- Dampak penanganan outlier dan normalisasi fitur.

### 4.1.2 Hasil Kinerja Model / Sistem
Tabel ringkasan metrik performa pengujian:

| Skenario Pengujian | Akurasi (%) | Presisi (%) | Recall (%) | F1-Score (%) | Waktu Komputasi (detik) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Model Standar)** | 78.40 | 76.20 | 79.10 | 77.62 | 12.4 s |
| **Skenario 1 (Uji Parameter A)** | 83.15 | 81.50 | 84.00 | 82.73 | 14.2 s |
| **Skenario 2 (Uji Parameter B)** | 87.60 | 86.80 | 88.10 | 87.44 | 16.8 s |
| **Metode Usulan (Optimasi Penuh)** | **92.30** | **91.80** | **92.50** | **92.15** | **18.5 s** |

### 4.1.3 Analisis Confusion Matrix & Kurva Konvergensi
*(Sertakan grafik loss/akurasi selama training dan visualisasi confusion matrix)*

---

## 4.2 Pembahasan Mendalam (Discussion)

### 4.2.1 Analisis Pengaruh Variabel & Parameter
- Analisis bagaimana perubahan parameter mempengaruhi metrik performa.
- Mengapa model usulan mampu meningkatkan performa hingga *X%*.
- Pembahasan mengenai titik jenuh / overfitting jika ada.

### 4.2.2 Perbandingan dengan Penelitian Terdahulu (Benchmarking)
Perbandingan kinerja metode yang diusulkan dengan penelitian sebelumnya:

| Peneliti | Metode | Dataset | Metrik Utama |
| :--- | :--- | :--- | :--- |
| *Riset A (2024)* | Metode X | Dataset Standar | Akurasi 86.2% |
| *Riset B (2025)* | Metode Y | Dataset Standar | Akurasi 89.0% |
| **Penelitian Ini (2026)** | **Metode Usulan** | **Dataset Standar** | **Akurasi 92.3%** |

### 4.2.3 Pembuktian Hipotesis
- Hasil uji statistik menunjukkan nilai $p\text{-value} = 0.002 < 0.05$, sehingga $H_0$ ditolak dan $H_1$ diterima.
- Terbukti secara signifikan bahwa metode usulan memberikan peningkatan performa nyata.

---

## 4.3 Implikasi Penelitian

- **Implikasi Teoretis:** Memperkuat teori mengenai integrasi metode ...
- **Implikasi Praktis:** Dapat diterapkan langsung pada sistem operasional untuk menghemat biaya / waktu ...

---

## 4.4 Keterbatasan Penelitian (Research Limitations)

1. Pengujian dibatasi pada rentang data / parameter tertentu ...
2. Komputasi membutuhkan resource GPU minimum ...
