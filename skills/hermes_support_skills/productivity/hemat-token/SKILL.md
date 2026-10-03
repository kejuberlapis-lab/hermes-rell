---
name: hemat-token
description: Strategi praktis untuk menghemat token saat memakai Hermes tanpa mengurangi kualitas hasil.
version: 1.0.0
author: Hermes
---

# hemat-token

Gunakan skill ini saat pengguna ingin biaya lebih hemat, konteks lebih panjang, dan respons tetap efektif.

## Tujuan
- Menurunkan konsumsi token input/output.
- Menjaga hasil tetap akurat dan actionable.
- Mengurangi konteks berulang yang tidak perlu.

## Langkah Setup Cepat
1. Pilih model lebih ekonomis sebagai default:
   - `hermes model` lalu pilih model murah/efficient.
2. Aktifkan kompresi konteks:
   - `hermes config set compression.enabled true`
   - `hermes config set compression.threshold 0.50`
   - `hermes config set compression.target_ratio 0.20`
3. Batasi verbosity jawaban (ringkas, poin-poin).
4. Gunakan mode kerja terarah:
   - Satu prompt = satu tujuan jelas.
   - Hindari multi-topik dalam satu pesan panjang.
5. Hindari tool call berulang yang tidak perlu:
   - Cache hasil penting dalam ringkasan singkat.
6. Gunakan `/compress` saat percakapan mulai panjang.

## Pola Prompt Hemat Token
- Format efektif:
  - Tujuan: ...
  - Konteks minimum: ...
  - Output yang diminta: ...
  - Batasan: ringkas, maksimal N poin.

Contoh:
```text
Tujuan: debug error login API.
Konteks minimum: stack trace + potongan endpoint auth saja.
Output: 3 kemungkinan akar masalah + langkah perbaikan.
Batasan: maksimal 120 kata.
```

## Kebiasaan yang Menghemat Banyak Token
- Kirim hanya bagian error/log yang relevan, bukan seluruh file.
- Minta output terstruktur (checklist/tabel singkat).
- Hindari mengulang instruksi global di setiap pesan.
- Untuk iterasi coding, minta diff kecil per langkah.

## Verifikasi
- Cek penggunaan token via `/usage`.
- Bandingkan sebelum/sesudah 3 percakapan.
- Jika kualitas turun, naikkan detail hanya di langkah kritis.

## Pitfalls
- Terlalu ringkas bisa hilangkan konteks penting.
- Kompresi agresif dapat membuang detail edge-case.
- Model terlalu murah mungkin butuh iterasi tambahan.
