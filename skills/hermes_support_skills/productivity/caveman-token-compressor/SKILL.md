---
name: caveman-token-compressor
description: Use when optimizing context. Compresses LLM communication.
---

# Caveman Context & Token Compressor

Protokol kompresi komunikasi LLM dan agent untuk memangkas konsumsi token hingga 40-60% saat menjalankan tugas-tugas coding dan eksekusi multi-step.

## Aturan Kompresi
1. **Eliminasi Basa-Basi:** Hapus kalimat pengantar, penutup retoris, dan permintaan maaf yang tidak perlu.
2. **Keyword-Dense Formatting:** Sajikan fakta teknis, status keluaran terminal, dan rencana aksi dalam bentuk poin terstruktur padat sinyal.
3. **Diff/Delta Reporting:** Laporkan hanya perubahan atau baris penting yang berubah, bukan keseluruhan file yang tidak disentuh.
