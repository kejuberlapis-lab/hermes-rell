---
name: ai-agent-task-decomposition
description: Use when planning complex tasks. Breaks into subtasks.
---

# AI Agent Task Decomposition & Execution Planner

Metodologi pemecahan masalah kompleks (*Task Decomposition*) untuk eksekusi tugas teknis otonom.

### Prinsip Dekomposisi Tugas:
1. **Pemecahan Atomik (Atomic Step Breakdown):**
   - Pecah instruksi besar klien menjadi 3–5 langkah independen yang terisolasi dan mudah diverifikasi.
   - Urutkan dependensi: Persiapan environment $\rightarrow$ Kode/Skrip $\rightarrow$ Uji Coba $\rightarrow$ Verifikasi Hasil.

2. **Gerbang Verifikasi Mandiri (Self-Validation Gates):**
   - Setiap langkah harus memiliki kriteria lulus yang jelas (contoh: exit code 0, status 200 OK, file exists).
   - Dilarang melompat ke langkah berikutnya jika langkah sebelumnya gagal.

3. **Laporan Singkat & Berorientasi Hasil:**
   - Sajikan laporan kepada klien secara ringkas, fokus pada hasil eksekusi nyata tanpa filler panjang.
