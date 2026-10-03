# Telkom QC 63-site run — 2026-08-30

Working run details from the first full execution of `telkom-qc-certificate`.

## Source data
- Excel site list `Buat QC.xlsx` → 69 sites, col D=Site ID, E=Site Name, G=SOW (FIRO/FIMO/REDEPLOY/RELOKASI), H=Integration Date ("TGL OA"). Sheet name `Sheet2`.
- Monitoring images: `Archive.zip` → 64 PNG of "Daily Performance Monitoring" reports, naming pattern `QC_Performance_Report_<SITE>_<YYYY-MM-DD>_to_<YYYY-MM-DD>.png`. 64 images / 63 unique (BTM520 had two date ranges 25-27 and 25-28).
- Extract zip to /tmp: `unzip -o` (skip `__MACOSX/` dir which holds stray `._` metadata files).

## File naming inconsistency (critical)
Monitoring PNG filenames had unpredictable date ranges. Some sites monitored in **July** (e.g. NTJ040, PAD381, PAD659, PAD664 = `2026-07-30_to_2026-08-01`), others late August. The dashboard `ls QC_Performance_Report_*.png` listing vs actual glob differed. **Always resolve the true path first**: `python3 -c "import glob; print(glob.glob(f'*{SITE}*'))"` before vision_analyze. Guessing wrong path → `media file not found` (+ tool-loop warnings).

## Sheet cleanup
- 6 excel sites had NO monitoring image: BTM856, PAD384, PAY126, PBR997, TBK019, TPJ005. Their sheets still showed stale template (dates `25-May-26`, D19 `0.0083`). User: delete → cleared D18:F20 (NOT removed sheets; kept sheet but emptied data cells).
- Final data-bearing count: 63 sheets (69 − 6 no-data). Template TBH077 excluded from exports.

## PDF export
- Initial naive convert gave 420 pages (6 pages/sheet because no page setup). After setting A4 landscape fitToPage → exactly 70 pages (70 sheets).
- Split per sheet with pymupdf, mapped sheet index → page index (openpyxl sheet order == PDF page order).
- Exported only the 63 data-bearing sheets → 63 files `QC_<SITE>.pdf`.
- Zipped `QC_PDF_63_Site.zip` (2.69 MB) using `zipfile` (CLI `zip` not installed).

## User preference notes
- KPI values display format `0.00` (2 decimals) — set via number_format on D19:F20.
- J20 (avg latency) = numeric `round(avg,2)`, replacing `=AVERAGE(D20:F20)` formula (openpyxl won't calc formulas).
- J19 status ALWAYS 'Clear' regardless of spike; N19 'Pass' to match (initial auto-set had fail on spikes — user corrected to always Clear/Pass).
- User work style: "pelan pelan dan teliti" — process in batches, verify each batch, report only SPIKE sites.
- User rescoped SPIKE detection: wanted J19 = Clear for all (don't flag spikes in final doc), even though some packet loss exceeded 0.1% threshold.

## Spike sites found (data note; final J19 set to Clear anyway)
BGS019(0.47), BLS063(2.38), BTM366(0.11), BTM506(0.017), BTM934(3.44), COJ053(0.17), COJ089(2.78), DAK100(0.49), NTJ040(1.41), NTJ041(0.20), PAD666(0.036), PAY014(2.78), PBR534(0.049), PKR031(0.066), PNN041(2.42), RGT504(0.059), TMP002(2.51), TPJ010(1.21), UJT043(0.89), UJT060(0.15). Worst = BTM934 & PAY014 & PNN041 (>2%).
