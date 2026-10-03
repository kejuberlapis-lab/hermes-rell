---
name: ai-artwork-recolor-and-brand-asset-pipeline
description: "Use when recoloring AI artwork or extracting ChatGPT media."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [ai-artwork, logo-recolor, duotone, chatgpt-extraction, brand-identity, anti-slop, color-grading]
    related_skills: [brand-asset-optimization-and-integration, anti-slop-web-design, anti-slop-saas-paywall-design]
---

# AI Artwork Extraction, Duotone Color-Grading & Brand Pipeline

A class-level operational protocol for extracting master high-resolution generated media from external platforms (e.g. ChatGPT share links), applying non-destructive 1–2 solid color duotone grading to eliminate generic AI multi-color/purple-pink gradients without distorting original character geometry, and generating production-ready branding assets.

## When to Use

- When downloading/extracting generated images, logos, or concept artwork from ChatGPT shared conversations (`https://chatgpt.com/s/...`).
- When a user asks to simplify an AI logo/illustration into "1 or 2 solid colors" to remove the synthetic AI look ("Ubah warnanya saja, gambarnya tidak usah").
- When presenting curated brand color explorations across multiple corporate/tech archetypes.
- When generating high-contrast dark mode and transparent assets from master artwork.

## Procedure

1. **Extracting Master Media from ChatGPT Share Links:**
   - **Target Data Source:** In modern ChatGPT share pages, full-resolution artwork is serialized inside React Router stream controller payloads.
   - **Extraction Logic:**
     - Fetch the page HTML and extract the unescaped payload from `window.__reactRouterContext.streamController.enqueue(...)`.
     - Extract the raw backend estuary storage URL matching:
       `https://chatgpt.com/backend-api/estuary/public_content/enc/[A-Za-z0-9+/=_-]+`
     - Download the asset using desktop browser headers (`User-Agent: Mozilla/5.0...`, `Referer: https://chatgpt.com/`) to capture the full-resolution uncompressed master PNG (e.g. 1536×1024) rather than degraded low-res previews.

2. **Non-Destructive 1–2 Color Duotone Grading:**
   - **Core Rule:** Never redraw, replace, or convert the illustration into flat line-art when the user only asked to change the color palette. Retain 100% of the authentic curves, facial expressions, and lighting contours.
   - **Luminance-Driven Duotone Script:**
     ```python
     import numpy as np
     from PIL import Image

     def create_duotone_artwork(input_path: str, output_path: str, dark_hex: str, mid_hex: str, bg_hex="#ffffff"):
         def hex2rgb(h):
             h = h.lstrip("#")
             return [int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)]

         img = Image.open(input_path).convert("RGB")
         w, h = img.size
         arr = np.array(img, dtype=np.float32) / 255.0
         luma = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]

         c_dark = np.array(hex2rgb(dark_hex), dtype=np.float32)
         c_mid = np.array(hex2rgb(mid_hex), dtype=np.float32)
         c_bg = np.array(hex2rgb(bg_hex), dtype=np.float32)

         out = np.zeros_like(arr)
         for y in range(h):
             for x in range(w):
                 v = luma[y, x]
                 if v >= 0.97:
                     out[y, x] = c_bg
                 elif v < 0.45:
                     t = v / 0.45
                     out[y, x] = (1 - t) * c_dark + t * c_mid
                 else:
                     t = (v - 0.45) / 0.52
                     out[y, x] = (1 - t) * c_mid + t * c_bg

         res = Image.fromarray(np.clip(out * 255.0, 0, 255).astype(np.uint8))
         res.save(output_path, quality=95)
     ```

3. **Curated 1–2 Color Brand Archetypes:**
   - **Corporate & Trust:** Royal Tech Blue (`#1D4ED8`) & Slate Navy (`#0F172A`).
   - **Timeless Minimalist:** Architectural Monochrome Solid Black (`#090A0F`) & Charcoal (`#334155`).
   - **Modern SaaS:** Electric Cobalt (`#2563EB`) & Slate Cyan (`#0284C7`).
   - **Nordic Clean Tech:** Nordic Teal (`#0D9488`) & Deep Carbon (`#0F172A`).
   - **Fintech & Precision:** Emerald Green (`#059669`) & Charcoal (`#1E293B`).
   - **Humanized Assistant:** Warm Amber (`#D97706`) & Espresso (`#1C1917`).
   - **High-Velocity Execution:** Crimson Ruby (`#E11D48`) & Noir Slate (`#0F172A`).
   - **VIP & Enterprise:** Executive Gold (`#CA8A04`) & Pitch Black (`#090A0F`).

4. **Multi-Option Comparison Board Generation:**
   - Always present color exploration options on a clean light board (1380px wide HTML template rendered via Playwright at 2x Retina scale) displaying side-by-side cards with hex swatches, title, and brand character descriptions.

## Pitfalls

- **Redrawing Artwork on Color Requests:** Replacing an original illustration with vector wireframes when the user asked for color changes loses original facial expressions and artistic fidelity; use pixel-level color re-grading instead.
- **Scraping Thumbnail Artifacts:** Extracting `og:image` from ChatGPT shares yields a low-res cropped 512px preview. Always locate and download the raw estuary storage endpoint.
- **Retaining Synthetic Multi-Color Slop:** Leaving random purple, pink, and cyan highlights on an AI logo makes it look instantly generated; consolidating into a disciplined 2-color palette creates human-crafted brand authority.
