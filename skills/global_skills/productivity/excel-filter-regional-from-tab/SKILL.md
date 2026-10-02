---
name: excel-filter-regional-from-tab
description: Memisahkan data regional tertentu dari tab Excel (.xlsx) lokal, termasuk saat nama tab yang diminta tidak persis sama.
---

# Kapan dipakai
- User minta memisahkan/filter data regional dari file Excel lokal.
- Nama tab di instruksi user tidak persis sama dengan nama sheet aktual (contoh: user sebut `newlink`, sheet yang ada `NL 2025`).

# Langkah
1. **Validasi sheet yang tersedia**
   - Baca workbook dan tampilkan semua `sheetnames`.
   - Cocokkan nama tab user secara fleksibel (alias/kemiripan), lalu konfirmasi asumsi di output jika tidak persis sama.

2. **Gunakan interpreter Python sistem**
   - Pakai `/usr/bin/python3` untuk otomasi Excel lokal.
   - Jika `openpyxl` belum ada, install `python3-openpyxl` via apt.
   - Hindari asumsi `python3` default punya library data science.

3. **Deteksi kolom filter dari header**
   - Ambil header baris 1.
   - Cari kolom regional (contoh umum: `TSEL REG`).

4. **Filter regional target**
   - Untuk regional numerik seperti `10`, gunakan `str(value).strip().startswith('10')` agar match format seperti `10. Sumbagteng`.

5. **Output hasil dalam 2 opsi (disarankan)**
   - Opsi A: file baru berisi hanya hasil filter (single sheet).
   - Opsi B: duplikat workbook asli + sheet tambahan hasil filter (mis. `Regional 10 Newlink`).

6. **Verifikasi hasil**
   - Pastikan jumlah baris hasil filter (tanpa header) sesuai.
   - Cek file output benar-benar tersimpan di path cache/documents.

# Pitfalls
- `pandas`/`openpyxl` sering tidak ada di env default agent.
- Nama tab user sering shorthand; jangan langsung gagal jika tab literal tidak ditemukan.
- Jangan lupa pisahkan hitung `rows_with_header` vs `data_rows`.
- Proses simpan workbook besar bisa lama; jika timeout terjadi, cek apakah file sebenarnya sudah tersimpan sebelum retry penuh.

# Contoh snippet inti
```python
import openpyxl
wb = openpyxl.load_workbook(src)
ws = wb['NL 2025']
headers = [ws.cell(1,c).value for c in range(1, ws.max_column+1)]
col_reg = headers.index('TSEL REG') + 1

new = wb.create_sheet('Regional 10 Newlink')
for c in range(1, ws.max_column+1):
    new.cell(1,c,ws.cell(1,c).value)

rr = 2
for r in range(2, ws.max_row+1):
    v = ws.cell(r,col_reg).value
    if v is not None and str(v).strip().startswith('10'):
        for c in range(1, ws.max_column+1):
            new.cell(rr,c,ws.cell(r,c).value)
        rr += 1

wb.save(out)
print('data_rows', rr-2)
```
