---
name: architectural-floorplan-drafting
description: "Use when drafting floor plans. Generates SVG & CAD layouts."
---

# Architectural Floorplan & CAD Drafting Skill

Comprehensive skill for designing architectural layouts, spatial zoning, building floor plans, exporting production-ready 2D CAD drawings (.DXF), high-resolution visual blueprints (.SVG / .PNG), and editing authentic Detail Engineering Design (DED) documents with multimedia/MEE annotations.

---

## 📐 1. Architectural Standards & Design Rules

### A. Indonesian & International Residential & Commercial Dimensions
* **Dinding (Walls):**
  * Dinding Utama (Bata/Bata Ringan/Hebel): Tebal 15 cm (0.15 m)
  * Dinding Partisi (Drywall/Gypsum): Tebal 10 cm (0.10 m)
  * Kolom Praktis (Columns): 15x15 cm setiap jarak maks 3.0–3.5 meter
* **Pintu (Doors) & Bukaan (*Door Swing*):**
  * Pintu Utama: Lebar 90 cm – 100 cm, Tinggi 210 cm
  * Pintu Kamar Tidur: Lebar 80 cm – 90 cm, Tinggi 210 cm
  * Pintu Kamar Mandi/Toilet: Lebar 70 cm – 80 cm, Tinggi 200 cm
  * Busur ayun pintu (*door swing arc*) wajib 90° menunjukkan arah bukaan ke dalam ruangan.
* **Jendela (Windows):**
  * Jendela Kamar/Ruang Tamu: Lebar 60–80 cm per daun, ambang 80–100 cm dari lantai
  * Ventilasi/Bovenlicht Kamar Mandi: Lebar 50–60 cm, Tinggi 40 cm
* **Ruang Standar Ergonomis (Minimal Dimensions):**
  * Kamar Tidur Utama (Master Bedroom): Min. 3.0 m x 4.0 m
  * Kamar Tidur Anak/Standar: Min. 2.7 m x 3.0 m
  * Kamar Mandi / Toilet: Min. 1.5 m x 1.5 m (shower + WC)
  * Dapur & Dining: Min. 2.5 m x 3.0 m
  * Living Room / Ruang Keluarga: Min. 3.0 m x 4.0 m
  * Carport (1 Mobil): Min. 3.0 m x 5.0 m
  * Selasar / Koridor: Min. Lebar 1.0 m – 1.2 m

---

## 🏛️ 2. Official DED Blueprint Editing & Multimedia Overlay Protocol

When editing an official DED floor plan or blueprint image (adding Interactive Flat Panels, Audio Visual, Smart Classroom, MEE tags):
1. **Never Redraw from Scratch unless requested:** Always use the authentic high-resolution DED document/PDF page as the base image to preserve the official Title Block (Kop Gambar), official consultant & client data, grid dimensions, and room numbers 100% intact.
2. **Classroom Display Wall Mounting Rule (Anti-Glare & Ergonomics):**
   * In classrooms and laboratories, display screens (IFP / Smart Boards / Whiteboards) must be mounted on the **front wall facing the central corridor/selasar** (e.g. South wall for North-wing rooms, North wall for South-wing rooms), **NEVER** on side dividing walls.
   * *Why:* This positions the teacher and display at the entrance front, directs student view toward the corridor, and allows natural light from exterior facade windows to enter from the sides/rear without causing screen glare (*anti-glare*).
3. **Standard Color Coding & Tagging:**
   * **Red Tags (`IFP 75" + SL dll`):** Used for standard classroom/lab interactive display units. Include numbered sequential prefixes (`1.`, `2.`, `3.`, etc.).
   * **Blue Tags (`IFP 86" + CRS + SL dll`):** Used for Smart Classrooms & Large Interactive Lecture halls.
   * **Physical Wall Display Symbol:** Solid black box on the designated front wall with glowing active screen bar and leader line to the tag box.
4. **Physical Device Evidence Insertion (*Eviden Bentuk Perangkat*):**
   * Place the high-res photo/render of the actual hardware (e.g. Interactive Flat Panel UI, camera, smart board) as a framed card in the **clean outer margin** (outside the building perimeter), so it never covers walls, corridors, or room labels.
5. **Visual Verification Audit:** Always verify with `vision_analyze` to ensure zero collision, crystal-clear typography, and perfect visual hierarchy before delivering to the user.

---

## 🎨 3. Layer & Styling Conventions

When generating DXF / CAD files:
* `WALLS` (Color: White / Index 7, Lineweight 0.35mm): Boundary and internal structural walls.
* `DOORS` (Color: Cyan / Index 4, Lineweight 0.18mm): Door frame and 90-degree swing arc.
* `WINDOWS` (Color: Green / Index 3, Lineweight 0.18mm): Window sills and glass double lines.
* `DIMENSIONS` (Color: Red / Index 1, Lineweight 0.13mm): Dimension lines, ticks, and text in meters/cm.
* `ROOM_LABELS` (Color: Yellow / Index 2): Room names, area sizes (e.g. `KAMAR UTAMA ±0.00 (3.50 x 4.00 m)`).
* `FURNITURE` (Color: 8 / Light Gray): Bed, sofa, table, kitchen sink, sanitary fixtures.

---

## ⚡ 4. Python Automation Engine

### Method 1: Exporting Native AutoCAD (.DXF) with `ezdxf`

```python
import ezdxf
from ezdxf import units

def create_floorplan_dxf(filename="denah_bangunan.dxf"):
    doc = ezdxf.new("R2010", setup=True)
    doc.units = units.M  # Unit: Meters
    msp = doc.modelspace()

    # Define standard architectural layers
    doc.layers.add(name="WALLS", color=7)
    doc.layers.add(name="DOORS", color=4)
    doc.layers.add(name="WINDOWS", color=3)
    doc.layers.add(name="DIMENSIONS", color=1)
    doc.layers.add(name="ROOM_LABELS", color=2)

    # Example: Room boundary
    msp.add_lwpolyline([(0, 0), (4.0, 0), (4.0, 5.0), (0, 5.0), (0, 0)], dxfattribs={"layer": "WALLS"})

    # Room Label
    msp.add_text("RUANG KELUARGA\n4.00 x 5.00 m", dxfattribs={"layer": "ROOM_LABELS", "height": 0.25}).set_placement((1.0, 2.5))

    doc.saveas(filename)
    return filename
```

### Method 2: Exporting Vector SVG Blueprints with `svgwrite`
* Generate SVG with crisp grid, clean room fills, wall thickness, door swing arcs, dimensions, and north arrow.
