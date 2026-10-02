---
title: Daftar Pertanyaan Kritis Penguji Sidang
author: 124230117_Stefano Garrent Khristiawan
date: 2026-09-29
status: Aktif
tags:
  - skripsi
  - sidang
  - tanya-jawab
  - penguji
  - kisi-kisi
---

# ❓ Bank Pertanyaan Kritis Dewan Penguji & Strategi Menjawab

Kembali ke [[MOC - Skripsi]] | Terkait: [[Persiapan Sidang Skripsi (Pendadaran)]]

---

## 🎯 1. Pertanyaan Seputar Topik & Urgensi (Bab 1)

### Q1: "Mengapa Anda memilih topik dan judul penelitian ini? Apa urgensinya?"
- 💡 **Framework Jawaban:** Jelaskan masalah riil di lapangan didukung data angka, lalu sebutkan kelemahan solusi yang ada saat ini, dan bagaimana skripsi Anda menawarkan solusi yang lebih baik/efisien.
- 🗣️ **Contoh Respon:** *"Berdasarkan data [X], permasalahan [Y] menyebabkan inefisiensi sebesar [Z%]. Penelitian terdahulu oleh [Peneliti A] telah mencoba menyelesaikan ini dengan [Metode A], namun masih memiliki kelemahan pada aspek [Kelemahan]. Oleh karena itu, penelitian ini urgen untuk dilakukan guna..."*

### Q2: "Apa kontribusi original (Novelty) dari penelitian Anda?"
- 💡 **Framework Jawaban:** Rujuk langsung ke [[Matriks Literatur & Research Gap]]. Bedakan antara kontribusi metode, modifikasi arsitektur, atau studi kasus baru yang belum pernah diteliti dengan parameter tersebut.

---

## 🔬 2. Pertanyaan Seputar Teori & Metode (Bab 2 & 3)

### Q3: "Kenapa Anda memilih Metode A daripada Metode B atau C?"
- 💡 **Framework Jawaban:** Jangan menjawab "karena lebih mudah" atau "karena disarankan pembimbing"! Jawab dengan alasan komparasi teoritis dan karakteristik data.
- 🗣️ **Contoh Respon:** *"Metode B memang populer, namun berdasarkan karakteristik data kami yang [non-linear / high-dimensional], Metode A terbukti lebih unggul dalam [kecepatan konvergensi / pencegahan overfitting], sebagaimana dibuktikan juga oleh riset [Nama Peneliti, 2024]."*

### Q4: "Bagaimana Anda memastikan data Anda valid dan tidak bias?"
- 💡 **Framework Jawaban:** Jelaskan tahapan pra-pengolahan di [[Pengumpulan & Pengolahan Data]] (misal: normalisasi, stratified k-fold cross validation, penanganan class imbalance, dan penghapusan data bocor/data leakage).

---

## 📊 3. Pertanyaan Seputar Hasil & Analisis (Bab 4 & 5)

### Q5: "Mengapa akurasi/performa metode Anda bisa meningkat? Di mana titik penentu perbaikannya?"
- 💡 **Framework Jawaban:** Rujuk ke hasil eksperimen ablation study atau analisis parameter di Bab 4. Tunjukkan modul mana yang paling berkontribusi terhadap kenaikan metrik.

### Q6: "Jika dataset atau skenario diubah dengan data ekstrem baru, apakah sistem Anda masih dapat bekerja dengan baik?"
- 💡 **Framework Jawaban:** Akui keterbatasan penelitian secara jujur (*honest limitation*), jelaskan domain batasan masalah di Bab 1, dan arahkan jawaban ke saran pengembangan riset di masa depan (Bab 5).
- 🗣️ **Contoh Respon:** *"Sesuai dengan batasan masalah pada sub-bab 1.2, model ini dioptimalkan untuk rentang karakteristik [X]. Pada skenario data di luar distribusi tersebut, performa berpotensi mengalami penurunan. Oleh karena itu, kami telah mencantumkan adaptasi domain sebagai saran riset lanjutan pada Bab 5."*
