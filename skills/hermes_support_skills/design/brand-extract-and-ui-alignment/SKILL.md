---
name: brand-extract-and-ui-alignment
description: Extract brand assets and apply cleanly to web UIs.
triggers:
  - "extract logo and color"
  - "brand extraction"
  - "apply brand from linktree"
  - "align website branding"
---

# Brand Extract & UI Alignment

Instructions for extracting brand assets from live sites, social profiles (Linktree, Instagram), or reference URLs and embedding them cleanly into frontend layouts.

## 1. Asset Extraction & Logo Pre-processing

When extracting raster/PNG logos from web sources (Linktree profile images, social avatars, favicon packages):

### Bounding-Box Tight Cropping (Mandatory)
- **Pitfall:** Extracted PNG avatars and social profile pictures often carry 30%–60% empty transparent margins around the mark. If embedded directly with CSS constraints like `h-14` (56px), the visible artwork is scaled down to ~25px, appearing tiny and unreadable.
- **Rule:** Always crop transparent padding tightly using bounding box detection before deploying to assets:
```python
from PIL import Image

img = Image.open("assets/raw_logo.png")
bbox = img.getbbox()
if bbox:
    cropped = img.crop(bbox)
    cropped.save("assets/brand_logo.png")
```

### Dual Light/Dark Variants
- Provide both a primary version (for light backgrounds/headers) and a light/inverted version (`brand_logo_light.png` in `#FAF9F5` or `#FFFFFF`) for dark footers and dark cards.

## 2. Safe CSS Sizing & Anti-Blowout Guards

- **Pitfall:** Using non-standard Tailwind classes (e.g., `h-13` instead of `h-12` or `h-14`) causes Tailwind to emit no CSS rule, resulting in the image unconstraining to its natural 1000px+ intrinsic resolution and blowing out the entire header.
- **Rule:** Always use standard Tailwind classes (`h-12`, `h-14`, `h-16`) or explicit bracket notation (`h-[56px]`), and ALWAYS pair with an inline style fallback guard:
```html
<img src="assets/brand_logo.png" alt="Brand Logo" 
     class="h-14 w-auto max-h-14 shrink-0 object-contain" 
     style="height: 56px; width: auto;" />
```

## 3. Brand Typography Hierarchy
- When structuring multi-tier brand header locks:
  1. **Primary Name:** `font-serif text-2xl font-bold tracking-tight text-espresso leading-none`
  2. **Subtitle/Category:** `font-serif italic text-sm font-medium text-teal leading-tight mt-1` (placed directly beneath primary name)
  3. **Tagline:** `font-mono text-[9px] tracking-[0.18em] text-espresso/50 uppercase mt-0.5`
- Keep vertical height of the text block strictly proportional to the adjacent logo mark (50px–60px total).

## 4. Spacing & Whitespace Rhythm
- Avoid oversized section padding (`py-24`, `py-20`, `space-y-20`) in luxury editorial sites unless explicitly requested.
- Maintain compact rhythm:
  - Header: `py-2 min-h-[76px]`
  - Hero: `pt-5 pb-8`
  - Content Sections: `py-8 sm:py-10`
  - Footer: `py-6 sm:py-8`
