---
title: Pengumpulan & Pengolahan Data
author: 124230117_Stefano Garrent Khristiawan
date: 2026-09-29
status: Aktif
tags:
  - skripsi
  - data
  - preprocessing
  - dataset
---

# 📈 Pengumpulan & Pra-pengolahan Data (Data Pipeline)

Kembali ke [[MOC - Skripsi]] | Terkait: [[BAB 3 - Metodologi Penelitian]] | [[Analisis & Hasil Pengujian]]

---

## 🗄️ 1. Profil & Metadata Dataset

- **Nama Dataset:** *Nama Dataset (misal: XAU/USD Tick Dataset / Heart Disease UCI / dsb.)*
- **Sumber / URL Asal:** *Kaggle / Repositori Kampus / Pengambilan Mandiri*
- **Format File Asal:** `.csv` / `.json` / `.parquet` / `.sqlite` / Citra `.png`
- **Jumlah Total Data Mentah:** $N = ...$ baris / file
- **Jumlah Fitur/Kolom:** $M = ...$ atribut

---

## 🧹 2. Log Pipeline Pra-pengolahan Data (Preprocessing)

```
[Data Mentah (Raw)]
         │
         ▼
[1. Pengecekan Missing Value] ────► Hapus baris / Imputasi Mean/Median
         │
         ▼
[2. Deteksi & Penanganan Outlier] ► Metode IQR / Z-Score Capping
         │
         ▼
[3. Encoding Fitur Kategorikal] ──► One-Hot Encoding / Label Encoding
         │
         ▼
[4. Normalisasi / Standarisasi] ──► MinMaxScaler [0, 1] / StandardScaler
         │
         ▼
[5. Pembagian Dataset (Split)] ───► Train (70%), Val (15%), Test (15%)
```

---

## 📊 3. Ringkasan Data Sebelum vs. Sesudah Cleaning

| Metrik Data | Kondisi Mentah (Raw) | Kondisi Bersih (Cleaned) | Keterangan Tindakan |
| :--- | :---: | :---: | :--- |
| **Total Baris Data** | 10,000 | 9,650 | 350 baris duplikat/rusak dihapus |
| **Missing Values** | 215 sel | 0 sel | Imputasi menggunakan median kelas |
| **Jumlah Outlier Ekstrem** | 142 data | 0 data | Di-trimming dengan threshold $3\sigma$ |
| **Distribusi Kelas** | Minoritas 10% : Mayoritas 90% | Seimbang (50% : 50%) | Penerapan SMOTE / Random Under-sampling |

---

## 💾 4. Lokasi Penyimpanan File Data
- **Raw Data Path:** `/home/ubuntu/.../data/raw/`
- **Processed Data Path:** `/home/ubuntu/.../data/processed/`
- **Final Train/Test Split:** `/home/ubuntu/.../data/splits/`
