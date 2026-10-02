---
title: BAB 3 - Metodologi Penelitian
author: 124230117_Stefano Garrent Khristiawan
date: 2026-09-29
status: Draft
tags:
  - skripsi
  - naskah
  - bab3
  - metodologi
---

# BAB 3. METODOLOGI PENELITIAN

Kembali ke [[MOC - Skripsi]] | Sebelumnya: [[BAB 2 - Tinjauan Pustaka & Landasan Teori]] | Lanjut ke [[BAB 4 - Hasil dan Pembahasan]]
Terkait: [[Instrumen Penelitian]] | [[Pengumpulan & Pengolahan Data]] | [[Analisis & Hasil Pengujian]]

---

## 3.1 Diagram Alur Penelitian (Research Flowchart)

```
[Mulai]
   │
   ▼
[Identifikasi Masalah & Studi Literatur] ──► [[Matriks Literatur & Research Gap]]
   │
   ▼
[Pengumpulan Data / Dataset] ──────────────► [[Pengumpulan & Pengolahan Data]]
   │
   ▼
[Pra-pengolahan Data (Preprocessing)]
   │
   ▼
[Perancangan & Implementasi Metode] ───────► [[Instrumen Penelitian]]
   │
   ▼
[Pengujian & Eksperimen] ──────────────────► [[Analisis & Hasil Pengujian]]
   │
   ▼
[Evaluasi & Validasi Hasil]
   │
   ▼
[Penarikan Kesimpulan & Laporan] ──────────► [[BAB 5 - Kesimpulan dan Saran]]
   │
   ▼
[Selesai]
```

---

## 3.2 Waktu, Tempat, dan Subjek/Objek Penelitian

- **Waktu Penelitian:** *Bulan Tahun – Bulan Tahun*
- **Lokasi / Lingkungan Penelitian:** *Laboratorium / Instansi / Cloud Server*
- **Subjek / Objek Riset:** *Dataset / Sistem / Pengguna Target*

---

## 3.3 Bahan dan Alat Penelitian (Instrumen)

### 3.3.1 Perangkat Keras (Hardware)
- Processor: ...
- RAM: ...
- GPU: ...
- Storage: ...

### 3.3.2 Perangkat Lunak (Software & Library)
- Sistem Operasi: Linux Ubuntu / Windows
- Bahasa Pemrograman: Python / PHP / JS / C++
- Framework & Library: PyTorch / TensorFlow / Pandas / Scikit-Learn
- Tool Riset & Catatan: Obsidian / LaTeX / Zotero

---

## 3.4 Metode Pengumpulan dan Karakteristik Data

- **Sumber Data:** Primer (kuesioner, pengukuran langsung) / Sekunder (Kaggle, UCI ML Repository, data internal perusahaan).
- **Jumlah Data / Sampel:** Total $N = ...$ baris/sampel.
- **Fitur / Atribut:** Daftar variabel independen ($X$) dan variabel dependen ($y$).

---

## 3.5 Tahapan Pra-pengolahan Data (Preprocessing)
1. **Data Cleaning:** Penanganan *missing values*, deduplikasi data.
2. **Outlier Filtering:** Metode IQR / Z-Score / Isolation Forest.
3. **Data Transformation:** Normalisasi Min-Max / Standard Scaler.
4. **Data Splitting:** Pembagian Train (70%), Validation (15%), Test (15%) atau $k$-Fold Cross Validation ($k=5 / 10$).

---

## 3.6 Perancangan dan Implementasi Metode

*(Jelaskan skema arsitektur model, algoritma, atau sistem yang dibangun)*
- Diagram Arsitektur Sistem
- Konfigurasi Hyperparameter (Learning rate, batch size, epoch, optimizer)
- Prosedur Pelatihan (*Training Procedure*)

---

## 3.7 Metode Evaluasi dan Pengujian Performa

Pengujian dilakukan untuk mengukur efektivitas metode yang diusulkan dengan menggunakan metrik:

1. **Akurasi (Accuracy):**
   $$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$
2. **Presisi (Precision) & Recall:**
   $$\text{Precision} = \frac{TP}{TP + FP}, \quad \text{Recall} = \frac{TP}{TP + FN}$$
3. **F1-Score:**
   $$\text{F1} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$
4. **Uji Validasi Statistik:** *Paired t-test* dengan tingkat signifikansi $\alpha = 0.05$.
