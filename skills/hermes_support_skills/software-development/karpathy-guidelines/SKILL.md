---
name: karpathy-guidelines
description: Use when coding and refactoring. Enforces minimal scope.
---

# Karpathy-Inspired Coding & Refactoring Guidelines

Standar coding ala Andrej Karpathy untuk menulis, mereview, dan merefaktor kode secara efisien, presisi, dan terukur.

## 4 Aturan Emas
1. **Asumsi Eksplisit:** Nyatakan semua asumsi di awal; jangan menebak perilaku sistem secara implisit.
2. **Surgical Minimal Scope:** Ubah hanya kode yang benar-benar wajib diubah. Dilarang merefaktor area sekitar tanpa instruksi.
3. **Kriteria Sukses Terukur:** Tentukan kriteria sukses deterministik (test pass, status code 200, output valid) sebelum mengeksekusi.
4. **No Speculative Abstraction:** Tulis kode sesederhana mungkin. Jangan membuat fungsi pembungkus abstrak sebelum ada kebutuhan nyata (YAGNI).
