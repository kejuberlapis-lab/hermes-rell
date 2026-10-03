---
name: telkom-qc-certificate
description: Fill Telkom QC certificate sheets, extract bandwidth/traffic evidence from xlsx, compose one-page evidence PDFs, reconcile against QC site list.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Telkom 4G Site QC Certificate — full pipeline

Two-phase workflow in `/home/ubuntu/Format QC - cleaned.xlsx` (also mirrored in Obsidian note `ObsidianVault/Telkom/Telkom - SOP Generate QC Sheets.md`).

## Files
- **Workbook:** `/home/ubuntu/Format QC - cleaned.xlsx`, sheet `TBH077` = pristine template (never modify). Each site = one sheet named by Site ID.
- **Excel source:** `Buat QC.xlsx` (site list: `Sheet2`, col D=Site ID, E=Site Name, G=SOW, H=TGL OA).
- **Monitoring images:** per-site `.png` "Daily Performance Monitoring" reports (often zipped).

## PHASE 1 — Create sheet per site (from excel site list)
Only 4 cells changed per site:

| Cell | Field | Source col |
|---|---|---|
| B5 | Site Name | E |
| B7 | Site ID | D |
| G7 | Integration Date | H |
| L7 | Type of Work (SOW) | G |

Static: E5=SUMBAGTENG, G5=4G, KPI/checklist/ttd rows 12–48 unchanged. Delete old sheet before regenerate (`del wb[name]`). Strip whitespace in Site ID (becomes sheet title). Spot-check B5/B7/G7/L7 afterwards.

## PHASE 2 — Fill KPI Transport table (rows 16–20) from monitoring images
Per sheet, only these cells change from monitoring data:

| Cell | Content |
|---|---|
| D18/E18/F18 | monitoring dates (first 3 days) — MUST be consecutive (+1 day each), `DD-MMM-YY` fmt |
| D19/E19/F19 | L2 Packet Loss (max/worst per day) |
| D20/E20/F20 | L3 Latency (max/worst per day) |
| J19 | 'Clear' (user requirement: ALWAYS 'Clear', even if data spiked) |
| N19 | 'Pass' (keep consistent with J19='Clear') |
| N20 | 'Pass' |
| J20 | average of D20:F20 ROUNDED to 2 decimals (replace `=AVERAGE` formula with numeric literal) |

Formatting: D19:F20 number_format `0.00` (2 decimals).

### Reading monitoring images
- Use `vision_analyze` on each PNG, ask for: site ID, first 3 dates with exact date + Average Packet Loss + Average Latency + Status Packet Loss, max PL per day.
- **Filenames are inconsistent** (date ranges vary — some July `2026-07-30_to_2026-08-01`, some 23–26, etc.). ALWAYS verify the real filename via glob before vision_analyze: `glob.glob(f'*{SITE}*')`. Guessing the path causes "media file not found".
- Max-per-day when multiple rows per date (network reports repeat dates with different sectors).

## PHASE 3 — Export each sheet to one-page PDF
LibreOffice must be installed (`sudo apt-get install -y libreoffice-calc`).

1. Set page setup per sheet for A4 landscape fit-to-page:
```python
from openpyxl.worksheet.properties import PageSetupProperties
ws.page_setup.orientation='landscape'
ws.page_setup.paperSize=9  # A4
ws.page_setup.fitToWidth=1
ws.page_setup.fitToHeight=1
ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
```
2. Convert whole workbook: `soffice --headless --convert-to pdf --outdir OUT "Format QC - cleaned.xlsx"` → 1 PDF page per sheet (verify page count == sheet count).
3. Split into per-sheet files with `pymupdf`: iterate sheets, map sheet index → page index (same order), `new.insert_pdf(doc, from_page=i, to_page=i)`, save `QC_<SITEID>.pdf`.
4. Zip result: `QC_PDF_<N>_Site.zip`, name files by basename only (`zipfile`, `-j` equivalent via `z.write(f, os.path.basename(f))`).

**Only export sheets that have data** (D18 filled). Empty template sheets (TBH077, sites without monitoring images) must be EXCLUDED.

## PITFALLS
- `zip` CLI not installed → use python `zipfile`.
- Page count 420 (6/sheet) before fit-to-page if page setup missing → set fitToPage first.
- openpyxl does NOT recalculate formulas: `data_only=True` gives None for `=AVERAGE(...)`. Compute avg from D20:F20 manually, write rounded literal.
- After changing any cell formatting/value, must regenerate PDF + re-zip (PDF does not auto-update).
- `J20` raw = `=AVERAGE(D20:F20)`; user asked to round to 2 decimals → replace with numeric `round(avg,2)`. Latency often <0.005 → shows 0.00.
- If a site sheet shows stale template data (dates `25-May-26`, D19 `0.0083`) and there's no monitoring image for it — CLEAR D18:F20 (user: delete, don't keep template).
- **NEVER assume image type from column index alone.** Always dump col histogram + `vision_analyze` one image per col to identify type. Column semantics vary by sheet/workbook — what is "traffic graph" in one run may be "CLI config" in another. The user WILL notice if you include wrong images and WILL require you to redo all PDFs.
- **Exactly 2 images per evidence PDF, not 3, not 5.** User was explicit: each site gets BANDWIDTH (col 7/8/0) + TRAFFIC (col 15 = topology diagram). Extra images (templates, CLI col-0 when col-7/8 exists) must be DISCARDED, not composited.
- Excel embedded images use `<xdr:oneCellAnchor>` (NOT `<xdr:twoCellAnchor>`). If `findall('...twoCellAnchor')` returns 0 anchors, try `oneCellAnchor` immediately — don't waste time debugging namespace issues.

## PHASE 4 — Bandwidth-evidence one-page PDF per site
User produces "eviden bandwidth" one-page PDFs per site. **CRITICAL: each site has exactly 2 evidence images — TRAFFIC + BANDWIDTH. Discard everything else (GPON CLI config/anchor col-0 images, templates, duplicates).**

Two sources:

### 4a. Direct screenshots (2 files: GPON CLI + traffic graph)
1. **GPON CLI config** — `ont-lineprofile`, `dba-profile`, `service-port show` (DBA fixed BW, e.g. `1024000 kbps` ≈ 1 Gbps, all ports `up`).
2. **Traffic graph** — PRTG-style `TSEL.<SITE> - Traffic - Ethernet 1/1` 24h line chart (out peak/avg/current bps + total GB).

### 4b. Extract from excel sheet (typical: "Evident bw" is the LAST sheet, images anchor there)
Images in the sheet are stored as **`oneCellAnchor`** (NOT `twoCellAnchor`!) in `xl/drawings/drawingN.xml`. To fetch:
- `unzip -q source.xlsx` to /tmp; images live in `xl/media/image*.png`; anchor→image mapping via `xl/drawings/_rels/drawingN.xml.rels` (`rId` → `../media/...`).
- Parse anchors: `ET.parse(...).findall('.//xdr:oneCellAnchor', ns)` with `ns={'xdr':'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing'}`; read `from/row` + `from/col`; resolve image via the `r:embed` attribute on the `a:blip` element (`embed = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed'`).
- **Column semantics — VERIFY each run before mapping** (dump `col` histogram first, then `vision_analyze` ONE image per column to identify its type — do not assume from a prior run):
  - col 7/8 = BANDWIDTH evidence (content varies: a traffic-throughput graph OR a GPON CLI config screenshot, per sheet/site)
  - col 15 = TRAFFIC evidence = **topology / koneksi-path diagram** (RAN→METRO→OLT→ODC→ODP→site) — it is NOT a traffic graph despite the label
  - col 0 = GPON CLI config — also valid BANDWIDTH evidence; use as FALLBACK for sites lacking cols 7/8 (preference order 7 → 8 → 0)
- **Map image → site by nearest site-ID row ABOVE the anchor row** (site IDs live in col A; images sit in rows below their site's ID, not on the same row). Never read the anchor row as the site row.
- **Site IDs REPEAT down col A** (multiple evidence blocks per site = re-runs/different days). For each site keep the images from the LAST block (max anchor row per column), not the first.
- A site qualifies only if it has BOTH a BW (7/8/0) and a TRAFFIC (15) image; skip & report the rest.

Combine the 2 chosen images into one **A4 PORTRAIT PDF, exactly 2 images stacked VERTICALLY top→bottom, centered, uniform same layout for every site** (user explicitly rejects landscape/side-by-side/multi-image mashups):
```python
from PIL import Image, ImageDraw, ImageFont
import pymupdf
bw = Image.open(bw_path).convert('RGB'); tf = Image.open(tf_path).convert('RGB')
imgs = [bw, tf]
W, H = 794, 1123         # A4 PORTRAIT @96dpi
MARGIN, GAP = 30, 18; HEADER_H = 60; LABEL_H = 36
f_bold = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
avail_w = W - 2*MARGIN
avail_h = H - 2*MARGIN - HEADER_H - LABEL_H*2 - GAP
s = min(avail_w/max(im.width for im in imgs), avail_h/sum(im.height for im in imgs)); s = min(s, 1.6)
sc = [im.resize((int(im.width*s), int(im.height*s)), Image.LANCZOS) for im in imgs]
c = Image.new('RGB',(W,H),'white'); d = ImageDraw.Draw(c)
d.text((MARGIN,14), f'Eviden Bandwidth - {SITE}', font=f_bold, fill=(15,15,15))
y = MARGIN + HEADER_H
for im, lab in zip(sc, ['BANDWIDTH','TRAFFIC']):
    lw = d.textlength(lab, font=f_bold); d.text(((W-lw)//2, y), lab, font=f_bold, fill=(200,30,30))
    y += LABEL_H
    c.paste(im, ((W-im.width)//2, y)); y += im.height + GAP
c.save('/tmp/evid.png')
doc = pymupdf.open(); pg = doc.new_page(width=595, height=842)  # A4 PORTRAIT pts
pg.insert_image(pg.rect, filename='/tmp/evid.png'); doc.save(f'Eviden_BW_{SITE}.pdf')
```
Verify with `vision_analyze` on `get_pixmap(dpi=70)`: confirm EXACTLY 2 labeled sections (BANDWIDTH top, TRAFFIC bottom), fully visible, no crop/overlap. Layout must be uniform across ALL sites.

## PHASE 5 — Reconcile evidence sheet against QC site list
Given an excel with an "Evident bw" sheet (typically the LAST sheet) whose col A lists Site IDs:
1. **Read QC site set** = the existing data-bearing sheets of the QC workbook (63 in the reference run — check actual count each time; distinguishes real sheets from the pristine template sheet `TBH077`).
2. **Extract evidence site set** — dedupe col A of the evidence sheet (strip whitespace; drop header rows that happen to look like IDs, e.g. a duplicate ID on a merged/header row).
3. **Match** = intersection; **SKIP** = QC − evidence (and evidence − QC). Return three-way result and **report to user exactly which sites are SKIPPED** — never silently drop them.
4. **Filter to QC-match sites only**, then require BOTH a BW and a TRAFFIC image (PHASE 4b) — sites with only one image are SKIPped too and reported.

## PHASE 6 — Archive & deliver zips
- 63 QC PDFs → `QC_PDF_63_Site.zip` (named `QC_<SITEID>.pdf`).
- Bandwidth evidence PDFs → `Evid_BW_2Gambar_<N>_Site.zip` (named `Eviden_BW_<SITEID>.pdf`).
- Deliver each as `MEDIA:/abs/path.zip`. After edits, regenerate PDFs then regenerate the zip so formats propagate.

## Verification checklist
- 1 page/sheet (pages == non-empty sheet count).
- Dates strictly consecutive.
- Only data-bearing sheets in final PDF/zip.
- Evidence PDF: **exactly 1 page, exactly 2 labeled images stacked vertically (BANDWIDTH top, TRAFFIC bottom), uniform layout across all sites** — no landscape, no side-by-side, no third image.

## Reference
See `references/telkom-qc-session-2026-08-30.md` for the 63-site run specifics (spike sites, file layout).