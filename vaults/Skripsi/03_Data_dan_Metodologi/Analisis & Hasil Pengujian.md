---
title: Analisis & Hasil Pengujian
author: 124230117_Stefano Garrent Khristiawan
date: 2026-09-29
status: Aktif
tags:
  - skripsi
  - eksperimen
  - hasil-uji
  - evaluasi
---

# 📉 Log Analisis & Hasil Pengujian Eksperimen

Kembali ke [[MOC - Skripsi]] | Terkait: [[BAB 4 - Hasil dan Pembahasan]] | [[Instrumen Penelitian]]

---

## 🧪 1. Log Eksperimen & Iterasi Model

| Run ID | Konfigurasi Model / Fitur | Akurasi | Precision | Recall | F1-Score | Catatan / Temuan |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| `EXP-01` | Baseline Model (Default) | 78.4% | 76.2% | 79.1% | 77.6% | Model underfitting pada kelas minoritas |
| `EXP-02` | + Normalisasi Standar | 82.1% | 80.5% | 83.0% | 81.7% | Konvergensi loss jauh lebih cepat |
| `EXP-03` | + Hyperparameter Tuning LR 0.001 | 87.6% | 86.8% | 88.1% | 87.4% | Akurasi meningkat signifikan |
| `EXP-04` | + Metode Usulan Lengkap | **92.3%** | **91.8%** | **92.5%** | **92.2%** | **Model Terbaik (Best Checkpoint)** |

---

## 📊 2. Detail Confusion Matrix (Best Model `EXP-04`)

| | Prediksi Positif (1) | Prediksi Negatif (0) |
| :--- | :---: | :---: |
| **Aktual Positif (1)** | **TP = 462** | FN = 38 |
| **Aktual Negatif (0)** | FP = 41 | **TN = 459** |

- **Total Sampel Uji:** $N_{\text{test}} = 1,000$ sampel
- **True Positive Rate (Sensitivity):** $92.4\%$
- **True Negative Rate (Specificity):** $91.8\%$
- **False Alarm Rate:** $8.2\%$

---

## 📈 3. Uji Signifikansi Statistik (Hypothesis Testing)

- **Jenis Uji:** Paired Student's t-test (antara Baseline vs. Metode Usulan)
- **Taraf Signifikansi ($\alpha$):** 0.05 (Confidence Level 95%)
- **Hasil Nilai t-Hitung:** $t = 4.821$
- **Hasil p-value:** $p = 0.00028 \ll 0.05$
- **Kesimpulan Statistik:** Peningkatan performa signifikan secara statistik (bukan karena kebetulan / fluktuasi acak).

---

## 🖼️ 4. Visualisasi & Grafik yang Disiapkan untuk Bab 4
- [ ] Grafik Perbandingan Loss & Akurasi Training vs. Validation per Epoch
- [ ] Heatmap Confusion Matrix
- [ ] Kurva ROC (Receiver Operating Characteristic) & Nilai AUC
- [ ] Bar Chart Komparasi Metrik terhadap Baseline dan SOTA Peneliti Terdahulu
