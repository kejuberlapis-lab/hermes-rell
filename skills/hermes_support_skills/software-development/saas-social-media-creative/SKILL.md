---
name: saas-social-media-creative
description: "Use when creating SaaS social media graphics or UI mockups."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [social-media, instagram-story, reels, ui-mockup, checklist-card, cekat-ai-style, safe-zones, conversion-design]
    related_skills: [anti-slop-web-design, poster-hero, social-media-sage, brand-asset-optimization-and-integration]
---

# SaaS Social Media Creative & UI Mockup Protocol

A class-level operational guide for designing high-converting, scroll-stopping social media graphics and vertical 9:16 assets (Instagram Stories, Reels covers, TikTok promos) for SaaS products and AI services using the proven **Interactive UI Checklist Mockup** design paradigm (e.g. Cekat.AI style).

## When to Use

- When creating vertical promotional banners or share graphics for SaaS products, AI workers, or Telegram bots (1080×1920 px, 9:16 aspect ratio).
- When the user asks for high-impact social media creatives that look like real software interfaces rather than generic typography posters.
- When referencing top-performing tech social media ads (e.g. Cekat.AI, Superhuman, Linear-style mobile promos).
- When designing multi-feature product walkthroughs in a single vertical frame.

## Core Architectural Structure (The UI Checklist Paradigm)

1. **Rich Solid Tech Canvas (Background):**
   - Use deep, authoritative brand gradients: Radial Tech Blue (`#0066EE` to `#002D80`), Dark Slate (`#060913` to `#0F172A`), or Royal Navy.
   - Layer with subtle texture: geometric arabesque grid, isometric matrix (`opacity: 0.7`), or contextual seasonal/ambient lighting.

2. **Top Header & Brand Lockup:**
   - Place a floating pill containing the official logo, brand name, and platform badge (e.g. `TELEGRAM` / `WEB`).
   - Add a concise value-hook tagline with keyword highlighting (e.g. *"Operasional Bisnis Otomatis Beres 24/7"* with golden-yellow accent `#FFD600`).

3. **Central Interactive UI Card (The Hero Component):**
   - **Container:** Pure white card (`#FFFFFF`), extra-rounded corners (`border-radius: 34px - 36px`), deep realistic SaaS elevation shadow (`box-shadow: 0 25px 60px -10px rgba(0, 15, 60, 0.45)`).
   - **Header Band:** Vivid gradient banner (e.g. Electric Cyan-to-Blue `#0077FF` to `#00B4D8`) with spark icon, bold list title (*"Business Operational Checklist"*), and an `● ALL ACTIVE` emerald status badge.
   - **Row Structure (5–6 Key Jobdesks/Features):**
     - **Col 1 (Icon):** Rounded duotone pastel icon container (48×48 px, 14px radius, soft background tint).
     - **Col 2 (Content):** Bold feature title (17px bold `#0F172A`) + solution-oriented microcopy with bolded key benefits.
     - **Col 3 (State):** Realistic iOS-style toggle switch in active `ON` state (vibrant blue `#0077FF` or emerald `#10B981` with white checkmark knob).

4. **Integrated Offer & Price Strip:**
   - Semi-transparent frosted glass card (`rgba(255,255,255,0.12)`, `backdrop-filter: blur(20px)`).
   - Prominent strikethrough promo price (`~~Rp150k~~` in bold red `#FCA5A5`) next to active price (`Rp99.000/bln` in white 32px 900-weight) + golden ticket badge (`🎁 COBA GRATIS - 8 Token Langsung Aktif`).

5. **Bottom Action Dock:**
   - Floating white action card displaying the clean custom domain (`techworker.my.id`) and a high-contrast primary action button (`Coba di Telegram ✈`).

## Instagram Story Safe-Zone Strict Gates

- **Top Safe-Zone:** Always enforce at least **100px–110px top padding** to prevent the IG profile avatar, handle, and story progress bars from obscuring the header.
- **Bottom Safe-Zone:** Always enforce at least **120px–130px bottom padding** to ensure bottom CTA cards and domain links are never occluded by the Instagram "Send Message" reply input or share sheet.
- **Side Padding:** Maintain at least **50px horizontal padding** against curved phone screen corners.

## Playwright Render Template

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True)
    page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    page.goto(f"file://{html_path}")
    page.wait_for_timeout(1000)
    page.screenshot(path=output_png_path, full_page=True)
    browser.close()
```

## Pitfalls

- **Placing CTA in the Bottom 100px:** Instagram overlays a permanent interactive message box across the bottom 100px; interactive buttons placed there cannot be tapped or read cleanly.
- **Using Flat Generic Text Posters for SaaS Ads:** Text-only bullet points fail to communicate software capability; presenting solutions as an active UI mockup with toggle switches creates immediate product tangibility.
- **Cluttered Font Hierarchies:** Mixing more than 2 font families destroys professional polish; pair Plus Jakarta Sans (UI & headings) with JetBrains Mono (badges & status pills).
