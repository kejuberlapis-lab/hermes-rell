---
title: Instrumen Penelitian
author: 124230117_Stefano Garrent Khristiawan
date: 2026-09-29
status: Aktif
tags:
  - skripsi
  - metodologi
  - instrumen
  - pengujian
---

# 🛠️ Instrumen & Parameter Penelitian

Kembali ke [[MOC - Skripsi]] | Terkait: [[BAB 3 - Metodologi Penelitian]]

---

## 💻 1. Spesifikasi Perangkat & Environment

### Hardware Environment
- **Processor (CPU):** *misal: AMD Ryzen 7 / Intel Core i7 / VPS Ubuntu Server*
- **Akselerator (GPU):** *misal: NVIDIA RTX 3060 12GB / CUDA v12.2*
- **RAM:** *misal: 16 GB DDR4*
- **Storage:** *misal: SSD NVMe 512 GB*

### Software Stack & Tools
- **Operating System:** Linux Ubuntu 24.04 LTS / Windows 11
- **Interpreter / Compiler:** Python 3.11 / Node.js 20 / PHP 8.2
- **IDE / Editor:** VS Code / JupyterLab / Obsidian
- **Version Control:** Git & GitHub

---

## 📦 2. Libraries & Dependency Packages

```yaml
# Daftar library utama yang digunakan
packages:
  - name: numpy
    version: "1.26.4"
    purpose: "Kalkulasi matriks dan array numerik"
  - name: pandas
    version: "2.2.2"
    purpose: "Manipulasi data tabular dan analisis statistik"
  - name: scikit-learn
    version: "1.4.2"
    purpose: "Preprocessing, model baseline, dan metrik evaluasi"
  - name: torch / tensorflow
    version: "2.3.0"
    purpose: "Training arsitektur neural network"
  - name: matplotlib / seaborn
    version: "3.8.4"
    purpose: "Visualisasi grafik dan matriks hasil"
```

---

## ⚙️ 3. Konfigurasi Hyperparameter & Setup Pengujian

| Nama Parameter | Rentang Nilai yang Diuji | Nilai Optimal (Hasil Tuning) | Alasan Pemilihan |
| :--- | :---: | :---: | :--- |
| **Learning Rate** | `[0.0001, 0.001, 0.01]` | `0.001` | Konvergensi stabil tanpa osilasi |
| **Batch Size** | `[16, 32, 64, 128]` | `32` | Keseimbangan VRAM & generalisasi |
| **Epoch** | `[50, 100, 200]` | `100` | Early stopping diaktifkan (patience 10) |
| **Optimizer** | `Adam, AdamW, SGD` | `AdamW` | Mengurangi bobot overfitting (*weight decay*) |
| **K-Fold CV** | `k = 5, k = 10` | `k = 5` | Validasi silang data training |

---

## 📋 4. Instrumen Pengumpulan Data Non-Sistem (Kuesioner / Pengujian Ahli)

*(Jika penelitian melibatkan validasi ahli / user acceptance test seperti SUS/TAM)*
- **Model Instrumen:** System Usability Scale (SUS) / Technology Acceptance Model (TAM)
- **Skala Pengukuran:** Skala Likert 1–5 (Sangat Tidak Setuju s.d. Sangat Setuju)
- **Target Responden:** $N = 30$ Responden ahli / pengguna
- **Uji Validitas:** Pearson Product Moment ($r_{\text{hitung}} > r_{\text{tabel}}$)
- **Uji Reliabilitas:** Cronbach's Alpha ($\alpha > 0.70$)
