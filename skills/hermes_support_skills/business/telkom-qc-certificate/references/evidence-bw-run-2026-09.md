# Evidence run — 2026-09 (BAUT Area 1)

Concrete run specifics for PHASE 4b/5/6 of `telkom-qc-certificate`.

## Input
- `Need Evidences BAUT Area 1.xlsx`, sheet `Evident bw` = **LAST sheet** (index 2). 77 unique site IDs in col A. Also has `BW` header at col index 2 and `TRAFFIC` at col index 10.
- Anchor mode: **`oneCellAnchor`** only — `twoCellAnchor` returned 0 anchors. 222 anchors total.
- Column histogram (dump before filtering): `{0: 81, 8: 24, 7: 54, 15: 59, 6: 1, 14: 3}`.
  - col 0 = CLI/template (GPON config — **skip**)
  - col 6/7/8 = bandwidth (7/8 primary; col 8 = BW variant)
  - col 14/15 = traffic (15 primary)
  - Keep col 7/8 → BW and col 15 → TRAFFIC.
- Embed resolution: `a:blip` attribute `r:embed` = `{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed`; scan `el.iter()` for it. `xml.etree.ElementTree` with namespaces: must register `a` namespace or `find('.//a:blip')` fails with KeyError.

## Mapping rule (the correction the user enforced)
Image anchors sit **rows below** their site's col-A ID row. Map via **nearest site-ID row ≤ anchor row** (binary/bisect over sorted site rows, take last ≤). Never use the anchor row's own col-A value.

## Outputs & counts
- 41 QC sites had evidence images (from 77 unique sheet IDs ∩ 63 QC).
- After requiring BOTH BW+TRAFFIC and filtering to QC set: **35 sites** → `Eviden_BW_<SITE>.pdf` (A4 portrait, 2 images, BANDWIDTH top, TRAFFIC bottom, red labels, centered).
- **6 QC sites SKIPPED** (no complete pair in sheet; reported to user):
  `BTM168, COJ089, PAD659, PAD661, PAY014, SWL005`
- Zip: `Evid_BW_2Gambar_35_Site.zip` (4.57 MB).

## Pitfalls hit
- `zip` CLI absent (`exit 127`) → build zips with Python `zipfile` (`ZIP_DEFLATED`).
- PIL `paste` needs **int** coords — cast `int()` on scaled boxes or you get `TypeError: 'float' object`.
- `openpyxl.load_workbook(data_only=True)` returns `None` for formula cells that were never recalculated — compute AVERAGE manually from inputs before rounding (J20 was `=AVERAGE(D20:F20)`).
- "Bulatkan J20" meant **round the VALUE to 2 decimals** (replace formula), NOT the display number format. Bytes-wise both were applied this session; confirm intent with user each time.
- Sheet names containing `&` (e.g. `"Evid BW per Site"`) must be `shlex.quote`d in shell or use Python-only paths.
- Vision-verify a sampled subset (2–3 sites) of every generated PDF batch, not just trust counters.