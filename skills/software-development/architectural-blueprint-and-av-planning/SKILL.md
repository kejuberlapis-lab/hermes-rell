---
name: architectural-blueprint-and-av-planning
description: "Use when analyzing DED drawings or editing CAD floor plans."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [architecture, blueprints, ded, mee, floor-plans, smart-classroom, ifp, crs, audio-visual, boq, drawing-annotations, cad-overlay]
---

# Architectural Blueprint Analysis, Audio-Visual Systems Planning, & Drawing Annotations

A class-level operational guide for reading, interpreting, auditing, and directly annotating architectural engineering blueprints (DED / Detail Engineering Design & MEE drawings), decoding structural grids and elevation marks, transcribing handwritten markup, generating high-resolution (300 DPI) CAD-style graphical overlays with verified AV equipment (IFP 75", IFP 86", CRS), and compiling floor-by-floor BOQs.

## When to Use

- When analyzing architectural and MEE floor plan blueprints for educational campuses, corporate offices, government buildings, or hospital facilities.
- When transcribing and mapping room designations, room numbers, and handwritten pen/pencil annotations across multi-floor drawings.
- When requested to **edit, annotate, or generate visual floor plan images** (*edit gambar denah*) with crisp CAD-style device symbols, room numbers, and equipment badges.
- When categorizing and quantifying Interactive Flat Panel (IFP) displays (e.g. IFP 75", IFP 86") and Classroom Recording Systems (CRS / Smart Classrooms).
- When synthesizing grand master equipment schedules, room counts, and infrastructure requirements (power, network, conduit) from multi-page CAD/PDF drawings.
- When distinguishing between functional academic/office spaces and non-functional structural/utility levels (e.g. roof plant floors, lift motor rooms, attic voids).

## Procedure

1. **Title Block & Engineering Metadata Decoding:**
   - Extract primary project identity from the right-hand or bottom title block (*Kop Gambar*):
     - Project Owner / Institution, Project Name (*Nama Pekerjaan: Pembuatan DED / Review DED*), Location, Budget Year (*Tahun Anggaran*), Lead Consultant / Planner (*Konsultan Perencana*), Sheet Code (*MEE / ARS / STR*), Sheet Number & Total Sheet Count (e.g. *MEE / 4 / 153*), and Drawing Scale (e.g. *1:250*).
   - Record the main floor peil/elevation level (e.g. `+9.200`, `+13.400`, `+17.600`, `+21.800`, `+26.100`) to confirm vertical zoning.

2. **Structural Grid & Coordinate Orientation:**
   - Map horizontal axes (typically Letters: `Grid A – S`) and vertical axes (typically Numbers: `Grid 1 – 8`).
   - Calculate total building footprint dimensions from modular spans (e.g. $72.000\text{ mm} \times 33.000\text{ mm}$).
   - Divide analysis systematically into directional quadrants:
     - **North Wing / Top Bar:** Grid 1–3 (West-to-East traversal).
     - **Central Circulation Core / Atrium:** Grid 3–6 (Selasar, Voids, Lavatories, Lift/Stairwell Cores, Panel Rooms).
     - **South Wing / Bottom Bar:** Grid 6–8 (West-to-East traversal).

3. **Handwritten Annotation & Equipment Transcription Protocol:**
   - Systematically inspect each room enclosure for both printed CAD text and handwritten/pencil markup:
     - **Standard Classrooms vs Smart / Large Classrooms:** Identify standard 64m² modular classrooms versus double-span/large rooms.
     - **Room Indexing / Numbering:** Capture sequential Arabic numbers (`1` to `11`) and Roman numerals (`I` to `IV`) assigned to specific room types.
     - **IFP Display Sizing:**
       - **IFP 75" (75 Inch):** Standard academic classrooms and engineering laboratories (e.g. Chemical / Industrial / Process Labs).
       - **IFP 86" (86 Inch):** Computer labs, computational centers, and large-capacity lecture halls.
       - **IFP 86" + CRS (Classroom Recording System):** Smart hybrid lecture classrooms equipped with tracking cameras, ceiling microphone arrays, audio DSPs, and lecture capture encoders.
     - **Laboratory Safety & Utility Markers:** Log special safety fixtures (e.g. `AREA SAFETY SHOWER`, `R. LABORAN`, Fume Hoods) adjacent to chemical/industrial practical labs.

4. **Direct Floor Plan Image Annotation & Graphical Overlay Engine:**
   - When the deliverable requires an annotated drawing image (*bukan dashboard, melainkan edit gambar denah*):
     - **High-Resolution Vector Rasterization:** Render base vector PDF pages at **300 DPI** minimum ($4960 \times 3508\text{ px}$ for standard architectural sheets) via PyMuPDF to preserve crisp CAD line weights.
     - **Strict Horizontal & Vertical Alignment:** Fix baseline Y-coordinates across each row of classrooms (e.g. `TOP_IFP_Y = 1260`, `BOT_IFP_Y = 2020`) so that badges and symbols form a mathematically straight architectural line across the floor plan.
     - **Display Screen & Camera Device Symbols:** Draw distinct vector device symbols on interior mounting walls:
       - *IFP 75":* Dual-bezel cyan display rectangle (`#0284c7` fill, `#38bdf8` outline) with horizontal reflection line.
       - *IFP 86" + CRS:* Purple display rectangle (`#7c3aed` fill, `#c084fc` outline) accompanied by a dedicated tracking camera turret icon on the mounting flank.
     - **Anti-Collision Clearance:** Place badge cards with dedicated margins (at least 15px) away from original printed CAD text (`RG. KELAS + 13.400`) to avoid visual overlap.
     - **Standardized Nomenclature:** Enforce uniform badge wording across all sheets (e.g. always `IFP 86" + CRS`, never inverted as `CRS + IFP 86"`).
     - **Non-Obstructing Floating Legend Panel:** Render a structured recap box in an open corner (e.g. top right margin) bordered with title header, device count pills, and clear color coding, ensuring it never overlaps CAD dimension strings or title blocks.

5. **Multi-Floor Room Schedule & BOQ Compilation:**
   - Tabulate room-by-room records with explicit columns: `No`, `Lantai`, `Posisi Grid Kolom`, `Nama Ruang (Cetak)`, `Nomor Urut Tangan`, `Kategori IFP / CRS`, `Elevasi`, and `Keterangan Fasilitas`.
   - Distinguish utility/plant floors (e.g. Lantai 06 / Roof Level: *Ruang Mesin Lift +26.100*, bordes tangga servis, dak atap AC VRV) where instructional AV equipment is not applicable ($0\text{ unit}$), but emergency PA horns, lift intercoms, and CCTV are required.
   - Generate a Grand Total Summary Table consolidating all equipment types across all floor levels.

6. **Technical Infrastructure Requirements per Smart Room:**
   - **Power (Arus Kuat):** Dedicated grounded surge-protected AC outlets located at 120–150cm AFFL (Above Finished Floor Level) behind the display bracket.
   - **Data (Arus Lemah):** Dual Cat6 RJ45 data drops for IFP interactive features and camera streaming.
   - **Audio-Visual Interconnect:** Embedded wall conduit for HDMI 2.0/2.1, USB-B Touch out, and USB-C pass-through to the lecturer's podium.

## Pitfalls

- **Delivering Abstract Dashboards when Image Overlays are Requested:** When users ask to edit floor plans (*edit gambar*), generating only an HTML/CSS dashboard table fails their visual requirement; always produce high-resolution, annotated architectural drawing image files with device badges placed directly on the floor plans.
- **Inconsistent Alignment Across CAD Rows:** Positioning badges with variable manual offsets produces an amateur, jagged appearance; enforce strict, calculated Y-coordinate baselines for entire rows.
- **Overlapping Original CAD Dimension Strings:** Placing legend panels or rekap boxes over grid bubbles or dimensional extension lines destroys engineering readability; position floating legends exclusively in clear margin zones.
- **Inverted Equipment Nomenclature:** Mixing `IFP 86" + CRS` with `CRS + IFP 86"` across different rooms on the same drawing creates confusion in procurement tenders; maintain 100% uniform string formatting.
- **Low-DPI Base Rasterization:** Exporting PDF floor plans at standard 72 DPI blurs CAD text and thin hatch lines upon zoom; always rasterize at 300 DPI ($>4000\text{ px}$ width).
- **Confusing Architectural Scale with Print Dimensions:** Reading millimeter grid spans directly without verifying drawing scale (e.g. 1:250) leads to erroneous square-footage and cable-run length calculations.
- **Overlooking Non-Instructional Roof / MEP Plant Floors:** Assuming every numbered floor plan contains classrooms leads to false equipment allocations on utility-only levels (e.g. elevator machine rooms or roof decks).
- **Ignoring Handwritten Pen/Pencil Overrides:** In review DED workflows, printed CAD labels often show generic `RG. KELAS` while handwritten annotations specify crucial upgrades (`IFP 86" + CRS` or room renumbering); always prioritize verified markups over baseline stubs.
