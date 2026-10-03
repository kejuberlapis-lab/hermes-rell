# Evidence BW run (2026-09) — image-type & layout corrections

Session where the user repeatedly corrected the evidence extraction. Record of the
clarifications so a future run starts correct instead of rediscovering them.

## The 2-evidence definition (user-confirmed)
Each site's one-page "Eviden Bandwidth" PDF contains EXACTLY 2 evidence images,
stacked vertically (portrait):
1. **BANDWIDTH** (top) — from image column **7, 8, or (fallback) 0**. Content is
   EITHER a traffic-throughput graph OR a GPON CLI config screenshot, varying per
   site/sheet. Do not assume which.
2. **TRAFFIC** (bottom) — from image column **15**. This is a **topology /
   koneksi-path diagram** (RAN→METRO→OLT→ODC→ODP→site), NOT a traffic line-graph
   despite the "TRAFFIC" label. User explicitly chose: "Trafik = topologi (col15),
   bandwidth = CLI/graph (col7/8/0)".

## Column image-type variance observed (do NOT hardcode)
| Site  | col 7/8  | col 15 |
|-------|----------|--------|
| BTM350| traffic graph | topology |
| PBR530| CLI config   | topology |
| UJT074| traffic graph | topology |

So col 7/8 is NOT consistently a graph — sometimes CLI config. col 15 is
consistently the topology diagram. ALWAYS `vision_analyze` one image per column
to confirm that run's mapping.

## Missteps user flagged this session (avoid repeating)
- **"kamu masih belum paham"** — first attempt mapped images by their OWN anchor row,
  missing that images sit in rows BELOW their site's ID. Fix: nearest site-ID row
  strictly ABOVE the anchor row.
- **"kamu salah lagi hanya ada 2 eviden nya yaitu traffic dan bandwidth"** — first
  layout included all 3–5 images per site (template + CLI + BW + TRAFFIC). Fix:
  keep exactly BW(7/8/0) + TRAFFIC(15), drop everything else.
- **"trafik = topologi yg skrg gue sebut traffic"** — don't label the topology
  diagram as a line-graph; the user's "traffic" evidence IS the topology image.
- Column preference for BANDWIDTH: 7 → 8 → 0. Prefer col 7/8; use col 0 (CLI)
  only as fallback for sites with no 7/8.
- Site qualifies only if it has BOTH a BW image and a TRAFFIC(15) image. Sites
  with only one are SKIPPED and reported.

## Reference numbers from this run
- Evidence sheet dedup site count: 77 uniques in col A.
- QC-match sites with both BW+TRAFFIC images: 36 (out of 41 QC-matching sites).
- Skipped (missing one of the 2 evid): BTM168, COJ089, PAD659, PAD661, PAY014.
- Deliverable: `Evid_BW_Final_36.zip` (36 PDFs, A4 portrait, 2 images each).
