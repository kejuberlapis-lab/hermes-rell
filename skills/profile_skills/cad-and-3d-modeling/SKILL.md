---
name: cad-and-3d-modeling
version: "1.0.0"
author: "Hermes Agent"
license: "MIT"
description: "Use when modeling CAD & 3D. Generates DXF, OBJ, & 3D assets."
---

# CAD and 3D Modeling Skill

Use this skill when generating 3D architectural meshes, building wireframes, CAD models (.OBJ, .STL, .DXF), or converting 2D floor plans to 3D spatial models.

## When to Use
- Generating 3D floor plan models from 2D room layouts.
- Exporting Wavefront (.OBJ) or STL files for Blender, SketchUp, AutoCAD, or 3D viewer tools.
- Calculating building floor area, room volumes, and structural geometries.

## Tools & Libraries
- `trimesh` & `shapely`: Extruding 2D polygon floor plans into 3D walls, slabs, windows, and roof planes.
- `ezdxf`: Native AutoCAD DXF vector generation.
