---
name: brand-asset-optimization-and-integration
description: "Use when cropping, optimizing, and integrating brand logos."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [brand-assets, logo-optimization, alpha-crop, dual-contrast, web-design, tailwind, linktree-extraction]
    related_skills: [web-asset-deployment-and-caching, brand-extract, anti-slop-web-design]
---

# Brand Asset Optimization, Alpha Cropping & Dual-Contrast Integration

A standardized operational protocol for extracting brand assets from external platforms (Linktree, social media, CDN avatars), eliminating transparent deadspace via tight alpha bounding box cropping, generating dual-contrast variants (light vs. dark UI surfaces), and integrating proportional branding across multi-page web architectures.

## When to Use

- When integrating brand logos, wordmarks, or icons extracted from external profiles (Linktree, Instagram, Twitter/X, CDN uploads) into web applications.
- When brand logos appear disproportionately small or unreadable despite specifying large CSS height classes (e.g. `h-14`, `h-16`).
- When logos must be rendered across differing background luminosities (light headers, dark footers, colored hero banners).
- When configuring brand color palettes (primary brand tone, deep base, accent highlights) derived from authentic reference sources.

## Procedure

1. **Brand Extraction from Linktree / Social Hubs:**
   - Query the target profile and extract the raw avatar/logo URL, brand bio/tagline, theme color tokens, and authentic branch/location deep-links (e.g. Google Maps URLs).
   - Download the raw master image to `assets/<brand>_logo_raw.png`.

2. **Automated Alpha Bounding Box Cropping (Deadspace Elimination):**
   - **Mechanism:** External avatar/profile uploads commonly feature square canvases (e.g. 1080x1080) with 40%–60% transparent empty padding above and below the actual artwork. Constraining raw images via CSS (`height: 4rem`) scales the entire empty canvas, shrinking the visible artwork to half size (~30px).
   - **Execution Script:** Run an automated tight-bounding box crop using Pillow:
     ```python
     from PIL import Image

     def crop_brand_logo(input_path: str, output_path: str):
         img = Image.open(input_path).convert("RGBA")
         bbox = img.getbbox()  # Extracts exact non-zero alpha boundaries
         if bbox:
             cropped = img.crop(bbox)
             cropped.save(output_path, "PNG")
             print(f"Cropped {input_path} from {img.size} to {cropped.size}")
     ```

3. **Dual-Contrast Asset Generation:**
   - **Primary Variant (`<brand>_logo.png`):** Retains original brand chromatic values for light surfaces (Header Navbar, product cards, checkout drawers).
   - **Light / Linen Inverted Variant (`<brand>_logo_light.png`):** Preserves original alpha channel contours while replacing non-transparent RGB values with high-contrast light tones (`#F6F4EB` or `#FFFFFF`):
     ```python
     def generate_light_variant(input_path: str, output_path: str, target_rgb=(246, 244, 235)):
         img = Image.open(input_path).convert("RGBA")
         r_tgt, g_tgt, b_tgt = target_rgb
         new_pixels = [
             (r_tgt, g_tgt, b_tgt, a) if a > 0 else (0, 0, 0, 0)
             for r, g, b, a in img.get_flattened_data()
         ]
         out = Image.new("RGBA", img.size)
         out.putdata(new_pixels)
         out.save(output_path, "PNG")
     ```

4. **Multi-Page Navbar & Footer Integration:**
   - **Header Navbar:** Place `<img src="assets/<brand>_logo.png" class="h-12 sm:h-14 w-auto object-contain">` inside a subtle background container/capsule (`p-1 rounded-xl bg-sand/80 border border-borderWarm/80`) paired with bold brand typography and tagline. Ensure the navbar container height (`min-h-[88px]`) provides generous breathing room.
   - **Footer Brand:** Use `<img src="assets/<brand>_logo_light.png" class="h-11 sm:h-12 w-auto object-contain">` against dark backgrounds to guarantee crisp legibility.
   - **Batch Template Update:** Enumerate and patch all HTML templates simultaneously using automated regex passes rather than editing single pages manually.

## Pitfalls

- **Uncropped Avatar Deadspace:** Relying on raw 1080x1080 avatar PNGs directly in HTML headers results in tiny, unreadable logos because the browser allocates half the specified height to transparent padding. Always crop to `img.getbbox()` before styling.
- **Single Dark Mark on Dark Footers:** Using a dark-colored logo asset on both light navbars and dark footers causes the footer mark to blend into the background and disappear; always deploy a secondary light/white silhouette variant.
- **Unconstrained Brand Image Heights:** Omitting explicit CSS height constraints (`h-12`, `h-14`, `max-height`) on high-resolution master logos allows raw 800px+ assets to expand to gigantic sizes when stylesheets fail to load.
- **Cross-Scope Asset Contamination:** Borrowing logos, icons, or color palettes from unrelated client/project folders breaches scope isolation; derive assets strictly from the designated project sources.
