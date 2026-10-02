# Telkom — SOP Generate Sheet QC Certificate

> Cara generate 1 sheet QC per site ID di `Format QC.xlsx` dari data excel "need push".
> Skill penting: `note-taking/obsidian`, library `openpyxl`.

## 1. File yang Dibutuhkan
- **Template:** `Format QC - cleaned.xlsx` (ada sheet `TBH077` = template asli, JANGAN diubah)
- **Data:** excel site list (mis. `Buat QC.xlsx`) dengan kolom:
  - `Actual Site ID` → kolom D
  - `Actual Site Name` → kolom E
  - `SOW` → kolom G
  - `TGL OA` → kolom H
  - (baris 1 = header, data mulai baris 2)

## 2. Rule Yang Diubah Per Site (HANYA 4 INI)
| Cell | Field | Sumber Kolom |
|---|---|---|
| B5 | Site Name | Actual Site Name (E) |
| B7 | Site ID | Actual Site ID (D) |
| G7 | Integration Date | TGL OA (H) |
| L7 | Type of Work | SOW (G) |

## 3. Yang STATIS (tidak pernah diubah)
- E5 Sales Cluster = SUMBAGTENG
- G5 Band = 4G
- E6 NE Type = kosong
- B8 Problem / B9 Justification / B10 Escalation = kosong
- KPI table, checklist QC, blok ttd (baris 12–48) = ikut template

## 4. Prosedur (openpyxl)
```python
import openpyxl
qc = '/home/ubuntu/Format QC - cleaned.xlsx'
wb = openpyxl.load_workbook(qc)
tpl = wb['TBH077']
# src = sheet data site
for r in range(2, src.max_row+1):
    sid = src.cell(row=r, column=4).value   # D
    if sid:
        ws = wb.copy_worksheet(tpl)
        ws.title = str(sid).strip()
        ws['B5'] = src.cell(row=r, column=5).value  # name
        ws['B7']  = str(sid).strip()
        ws['G7']  = src.cell(row=r, column=8).value # tgl
        ws['L7']  = src.cell(row=r, column=7).value # sow
wb.save(qc)
```

## 5. Verifikasi Wajib
- Jumlah sheet = 1 template + jumlah site
- Spot check per sheet: B5/B7/G7/L7 cocok dgn excel
- TBH077 tidak berubah
- Semua sheet maxrow = 49 (template utuh)

## 6. Pitfall
- Hapus dulu sheet salah sebelum regenerate (`del wb[nama]`)
- Strip spasi di Site ID sebelum jadi judul sheet
- Judul sheet = Site ID (mis. `LSK054`)
- Kalau excel data beda layout, cek dulu kolom header-nya — jangan asumsikan
- Simpan file sebelum verifikasi (buka ulang untuk cek)

## 7. Format Angka KPI
- Nilai PL/Latency (D19:F20) → number_format `0.00` (2 desimal, tampilan saja, nilai asli utuh)

## 8. Pengisian KPI dari Gambar Monitoring (Daily Performance)
- Sumber: screenshot `QC_Performance_Report_<SITEID>_<tgl>_to_<tgl>.png` (lipat zip)
- Baca tiap gambar: site ID + nilai per tanggal (avg, dan pakai MAX packet loss per hari)
- Cell yang diisi: **D18:F18** (tanggal), **D19:F19** (PL), **D20:F20** (Latency), **J19/N19** (status PL), **N20** (status Latency)
- D17/E17, K19, M19, K20, M20 = statis (tidak diubah)
- Tanggal **wajib berurutan** (+1 hari), format `DD-MMM-YY`
- Status: **selalu tulis `Clear`** di J19 dan **`Pass`** di N19/N20, termasuk site yang monitoring-nya spike (nilai tetap diisi sesuai report)
- Nilai yang spike: isi nilai asli (mis. 3.44), status tetap Clear/Pass

## 9. Export PDF per Sheet
- Install: `sudo apt-get install -y libreoffice-calc`
- Set tiap sheet: landscape A4, fit 1 halaman (`fitToWidth=1, fitToHeight=1`)
- Konversi: `soffice --headless --convert-to pdf --outdir <dir> "Format QC - cleaned.xlsx"` → 1 sheet = 1 halaman PDF
- Split per sheet pake pymupdf → `QC_<SITEID>.pdf`
- Hanya buat PDF untuk sheet yang **terisi data** (D18 tidak kosong)
- Zip semua: `QC_PDF_63_Site.zip`

## 10. Cek Konsistensi (setelah isi)
- Sheet terisi = 63, yang kosong template JANGAN dibuat PDF
- Cek: semua sheet D18 terisi → jumlah PDF = jumlah sheet terisi

## Riwayat
- 2026-08-30: 69 site dari `Buat QC.xlsx` (SOW: FIRO/FIMO/REDEPLOY/RELOKASI)
- 2026-08-30: Isi KPI 63 site dari zip gambar monitoring (batch 5 gambar/putaran)
- 2026-08-30: J20 = rata-rata Latency dibulatkan 2 desimal (nilai, bukan rumus)
- 2026-08-30: Export 63 PDF per site + zip `QC_PDF_63_Site.zip`
