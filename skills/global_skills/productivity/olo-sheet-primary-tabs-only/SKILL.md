---
name: olo-sheet-primary-tabs-only
description: "Aturan kerja berulang untuk spreadsheet OLO; hanya gunakan tab OLO, NEW OLO RECSI, NO BAUT, dan DATA BAUT OLO sebagai sumber data utama."
version: 1.0.0
author: Hermes Agent
license: MIT
---

# OLO Sheet — Primary Tabs Only

## Trigger
Gunakan skill ini setiap kali user meminta pencarian, validasi, ringkasan, atau pengolahan data pada spreadsheet OLO berikut:

- `https://docs.google.com/spreadsheets/d/1Lk86Lv_D2mFNgtAOyZWFEB4EL_0aTOf7-TR91n7aCqA/`

## Aturan Wajib
1. Jadikan spreadsheet di atas sebagai **sumber utama pekerjaan**.
2. **Hanya** gunakan tab berikut untuk baca/cari/olah data:
   - `OLO`
   - `NEW OLO RECSI`
   - `NO BAUT`
   - `DATA BAUT OLO`
3. **Jangan gunakan tab lain** untuk pencarian atau pengolahan data, kecuali user memberi izin eksplisit.
4. Jika data tidak ditemukan pada 4 tab utama, laporkan: "tidak ditemukan pada tab utama".

## Prosedur Kerja Standar
1. Konfirmasi konteks permintaan user (misalnya nomor order, SID, site, BAUT, dll).
2. Cari data berurutan di 4 tab utama.
3. Kembalikan hasil dengan format ringkas:
   - tab sumber
   - nomor baris
   - field penting (No Order/SID/BAUT/dll sesuai permintaan)
4. Jika diminta detail, tampilkan satu baris lengkap berdasarkan header kolom tab sumber.

## Pitfalls
- Nama tab bisa mirip dengan tab lain (mis. OLO vs OLO RECSI). Tetap batasi ke 4 tab utama yang ditetapkan.
- Jangan melakukan cross-check ke tab non-utama tanpa instruksi eksplisit.

## Verifikasi
- Sebelum kirim jawaban, pastikan setiap hasil mencantumkan salah satu dari 4 tab utama.
- Jika ada referensi dari tab lain, ulangi query hanya pada tab utama.
