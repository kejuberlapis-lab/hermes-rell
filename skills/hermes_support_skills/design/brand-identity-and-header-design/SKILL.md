---
name: brand-identity-and-header-design
description: "Use when extracting brand logos, assets, and headers."
version: 1.0.0
author: Hermes AI
license: MIT
metadata:
  hermes:
    tags: [branding, logo, typography, header, navigation, anti-slop, crop-alpha, scope-isolation]
    related_skills: [anti-slop-web-design, brand-extract, design-taste-frontend]
---

# Brand Identity, Asset Hygiene, and Header Design

## When to Use
Use this skill whenever extracting brand identity assets from social links/Linktree, integrating logos into websites, designing responsive header navigations, and maintaining strict multi-project scope boundaries.

---

## 1. Logo Asset Hygiene & Alpha Deadspace Cropping

When harvesting logo images from external platforms (Linktree, Instagram, social media profile pictures):
* **Crop Transparent Padding First**: Profile pictures (e.g., 1080x1080 PNGs) frequently contain 40%–60% empty transparent margins. Direct application of CSS `h-14` or `h-16` will scale the empty whitespace rather than the artwork, rendering the logo unreadably small (~30px).
* **Deterministic Bounding Box**: Always crop the image tightly around non-zero alpha pixels before referencing it:
  ```python
  from PIL import Image
  img = Image.open("assets/logo_raw.png")
  bbox = img.getbbox() # (left, top, right, bottom)
  cropped = img.crop(bbox)
  cropped.save("assets/logo.png")
  ```
* **No Artificial Border Boxes**: Never encase transparent custom-shaped or arched logo emblems inside arbitrary generic rounded border containers (`<div class="border rounded-xl">`). Let the emblem sit cleanly and transparently directly on the canvas.
* **Dual-Tone Inversion**: Always produce and verify two high-contrast assets:
  1. `logo.png` (Brand color tone for light backgrounds/headers).
  2. `logo_light.png` (Inverted crisp linen/white `#F6F4EB` for dark footers and contrast cards).

---

## 2. 3-Tier Vertical Brand Typography Hierarchy

When pairing logo marks with brand text in headers and footers, enforce this proportional 3-tier vertical hierarchy:

```html
<a href="index.html" class="flex items-center gap-3.5 group py-1 shrink-0">
  <!-- 1. Pure Cropped Emblem Logo -->
  <img src="assets/logo.png" alt="Brand Logo" class="h-14 sm:h-16 w-auto object-contain transition-transform group-hover:scale-105" />
  
  <!-- 2. Balanced 3-Tier Typography Block -->
  <div class="flex flex-col justify-center">
    <!-- Primary Brand (Bold, Solid, Tight Leading) -->
    <span class="font-serif text-2xl sm:text-3xl font-bold tracking-tight text-espresso group-hover:text-primary transition-colors leading-none">
      BRAND NAME
    </span>
    <!-- Sub-Brand / Category (Italic, Medium Weight, Distinct Accent) -->
    <span class="font-serif italic text-sm font-medium text-primary tracking-wide leading-tight mt-1">
      Category & Specialty
    </span>
    <!-- Micro Tagline Anchor (Monospace, Uppercase, Wide Tracking) -->
    <span class="text-[9px] font-mono tracking-[0.18em] text-espresso/50 uppercase mt-0.5">
      Authentic Tagline • Location / Descriptor
    </span>
  </div>
</a>
```

---

## 3. Horizontal Navigation Standards & Action Layout

* **Uniform Spacing & Baseline**: Group menu links with balanced spacing (`gap-7`), clean monospaced uppercase typography (`text-[12px] uppercase tracking-wider`), and active-page underline indicators (`after:bg-primary after:h-[2px] after:bottom-0`).
* **Utility Top-Bar**: Reserve the top bar for authentic operational facts (real branch locations, daily opening hours, live batch notices).
* **Right Action Cluster**: Group secondary utilities (ambient audio, search, cart bag) and anchor with a prominent pill-shaped Primary CTA button (`Book a Table` / `Order Now`).

---

## 4. Strict Vault & Multi-Project Scope Isolation

* **Absolute Project Boundaries**: Every project, client vault, and workspace must remain strictly isolated.
* **No Cross-Pollination**: Never transfer, reuse, or leak personal emails, SSH keys, notification contacts, or credentials from one vault/client workspace into another.
* **Clean Fallbacks**: When executing administrative automation tools (e.g. Certbot SSL), use explicit non-interactive flags (`--register-unsafely-without-email`) unless the user explicitly provides a designated email address for that specific domain.

---

## ⚡ Imperative Pitfalls

* **Crop logo alpha deadspace before tuning CSS dimensions** — uncropped transparent padding tricks the eye into thinking CSS sizing is defective.
* **Never add decorative border boxes around organic arched emblems** — box wrappers add visual noise and clash with bespoke logo geometry.
* **Keep brand text line-height tight (`leading-none`)** — default line heights add excessive vertical gaps between brand title, category, and tagline.
* **Do not pull emails or configurations across vault boundaries** — treat each project ecosystem as completely self-contained.
