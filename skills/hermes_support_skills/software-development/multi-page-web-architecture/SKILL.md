---
name: multi-page-web-architecture
description: "Use when building full multi-page websites and web apps."
version: 1.1.0
author: Hermes AI
license: MIT
metadata:
  hermes:
    tags: [web, architecture, multi-page, routing, state-persistence, localstorage, cart, tailwind, hospitality, ecommerce, segmented-nav, anti-cache]
    related_skills: [anti-slop-web-design, popular-web-designs, claude-design, ai-agent-product-and-pricing-strategy]
---

# Multi-Page Web Architecture & State Persistence Guide

## When to Use
Use this skill whenever building, expanding, or converting web applications and brand websites from single landing pages into **comprehensive Multi-Page Web Architectures** (e.g. hospitality, specialty roasteries, F&B, agencies, SaaS marketing portals).

---

## 🏛️ Core Multi-Page Architecture Blueprint

When a client or user requests a **Website** (distinct from a single landing page), deliver a modular multi-page system with standardized file structures:

| File | Page Name & Scope | Mandatory Interactive Features |
|---|---|---|
| **`index.html`** | **Home / Brand Overview** | Hero spread, signature highlights, atmospheric ambient audio player, quick CTA. |
| **`menu.html` / `catalog.html`** | **Full Catalog / Menu** | Real-time search filter, category tabs, dietary tags, quick-add (`+ Pesan`), customizer modal (`⚙️ Custom`). |
| **`beans.html` / `shop.html`** | **Specialty E-Commerce / Roastery** | Multi-attribute product cards (Origin, MDPL, SCA score), package weight selectors (200g/500g/1kg with dynamic pricing), grind size selector, subscription tiers. |
| **`about.html` / `story.html`** | **Philosophy & Provenance** | Founder/brand journey, ethical sourcing policies, machinery specs (Probat/Giesen), master artisan profiles. |
| **`space.html` / `amenities.html`** | **Spatial Sanctuary & Facilities** | Zonal breakdown (Slow Bar, Quiet Work Loft, Garden Courtyard, VIP Room), WiFi speeds, outlet accessibility, noise policies. |
| **`reservation.html` / `booking.html`** | **Direct Booking Engine** | Instant date/time picker, guest count, seating zone selection, VIP minimum spend calculation, automated WhatsApp reservation pre-formatting. |
| **`journal.html` / `guides.html`** | **Editorial Journal & Guides** | Technical recipes (V60 ratios, temperature limits), extraction chemistry, weekly newsletter subscription box. |
| **`contact.html` / `locator.html`** | **Store Locator & B2B Supply** | Interactive maps preview, public transit instructions (MRT/Bus), operating hours, customer FAQ, B2B wholesale beans sample form. |
| **`skills.html` / `capabilities.html`** | **SaaS Technical Skills Directory** | Interactive real-time search, category filter pills, concrete input/output examples, latency SLA tags (<30s), direct bot CTA buttons. |
| **`pricing.html` / `plans.html`** | **SaaS Pricing & Checkout** | Subscription tiering cards, token value economics, live Dynamic QRIS modal checkout with instant settlement timer. |
| **`case-studies.html` / `results.html`** | **Verified Technical Proof** | Real-world problem breakdown (FastAPI bug fix, anti-bot scraping, Nginx SSL), before/after code, and verified completion durations. |
| **`docs.html` / `manual.html`** | **Bot Documentation & Guides** | Prompting best practices, Telegram bot slash commands (/start, /saldo, /status, /paket), and file attachment formatting. |
| **`enterprise.html` / `umkm.html` / `personal.html`** | **Target Audience Segment Portals** | Dedicated solution deep-dives for corporate teams, SMEs, and solo developers with tailored workflows and ROI calculations. |

---

## 🧭 Precision Segmented Dock Navigation & Mobile Responsiveness

When building multi-page headers with 6–10 navigation items, avoid dumping a flat, cluttered list of text links across the navbar. Apply the **Precision Segmented Dock Architecture**:

1. **Three-Cluster Segmented Dock (Desktop/Tablet-L):**
   - Encapsulate center navigation within a floating pill container (`rounded-full bg-obsidian-900/90 hairline-border p-1 shadow-inner`).
   - Group links into 3 functional clusters separated by subtle vertical hairline dividers (`w-[1px] h-4 bg-white/10 mx-1.5`):
     - **Cluster 1 (Core Navigation):** `Beranda`, `Katalog Skill`, `Pricing`, `Tutorial`.
     - **Cluster 2 (Audience Segments):** `Enterprise`, `UMKM`, `Personal` (each paired with an icon).
     - **Cluster 3 (Help & Support):** `Contact & Help`.
   - Active pages receive a translucent highlighted pill background (`bg-white/[0.08] text-emerald-400 font-semibold border border-emerald-500/30`).

2. **Mobile Horizontal Quick-Pill Sub-Header:**
   - On screens <1024px, provide a dedicated sub-header strip (`overflow-x-auto flex items-center gap-1.5 px-3 py-2 bg-obsidian-950/90 hairline-border`) allowing smooth finger-swiping across all navigation pills without breaking layout.
   - Design right-side CTA buttons with responsive text (`<span class="hidden sm:inline">Buka </span><span>Telegram</span>`) and hide non-essential badges on screens <640px to ensure zero text truncation on narrow viewports (360px–390px).

3. **Anti-Cache Middleware for Dynamic Web Frameworks:**
   - In FastAPI, Express, or Nginx serving static multi-page assets, explicitly set `Cache-Control: no-cache, no-store, must-revalidate, max-age=0`, `Pragma: no-cache`, and `Expires: 0` headers. This prevents mobile browsers from serving stale cached HTML files during live development iterations.

---

## 🎨 Brand Asset & Logo Header Integration Standards

1. **Tightly-Cropped Assets First:**
   - Always crop transparent deadspace margins (`PIL.Image.crop(bbox)`) from extracted PNG brand logos before embedding. Transparent margins make standard CSS heights (`h-14`, `h-16`) render the visible artwork at half its intended size.
2. **No Artificial Wrapper Boxes on Organic Emblems:**
   - Do not wrap curved, arched, or organic logo badges in generic square bordered box containers (`p-1 rounded-xl bg-sand border`). Let the transparent emblem sit organically directly on the canvas.
3. **Top-Flush Brand Typography Alignment:**
   - When pairing a logo emblem with a vertical 3-line brand block (Title, Sub-brand/Category, Tagline):
     - Container must use `items-start pt-0.5` so the top of the title text sits flush with the apex/top boundary of the logo emblem.
     - Constrain the total combined vertical height of all text lines (`total_text_height <= logo_height`) using `leading-none` and tight margins (`mt-1`, `mt-1.5`) so the bottom tagline finishes neatly inside the logo's bottom boundary without protruding.

---

## 📐 High-Density Compact Spacing Standards

Avoid excessive vertical padding (`py-20`, `py-24` / 80-96px) in editorial and brand websites that forces users into endless empty scrolling. Apply compact, high-density editorial spacing:
- **Navbar / Header:** `py-2 min-h-[76px]` (with top utility bar `py-1.5`).
- **Hero Spread:** `pt-5 pb-8` (with `space-y-4` and `pt-4` for metrics/CTAs).
- **Content Sections:** `py-8 sm:py-10` with `pb-4 border-b` section headers and `pt-5` grid spacing.
- **Product / Feature Grids:** `gap-x-8 gap-y-4` to keep cards dense and readable without empty deadspace.
- **Footer:** `py-6 sm:py-8` with `pb-5 border-b` bottom grid.

---

## 🔄 Cross-Page State Persistence Workflow (`shared.js`)

To ensure a seamless user experience without server-side database overhead, synchronize application state across all pages via `localStorage`:

1. **Persistent Cart & Drawer**:
   * Store items in `localStorage.getItem('lamar_cart')`.
   * Keep cart badge counts and drawer previews synchronized across all sub-pages upon `DOMContentLoaded`.
   * Automatically calculate subtotal, restaurant tax (PB1 10%), and formatted Grand Total in real time.

2. **Persistent Ambient Audio & Controls**:
   * Save user audio toggle preferences to `sessionStorage` or `localStorage` to avoid jarring restarts on page navigation.

3. **Direct WhatsApp Checkout Dispatch**:
   * Pre-format item options (temperature, dairy choice, sugar level, grind size, extra shots) directly into standard WhatsApp URL encoding (`https://wa.me/<number>?text=...`).

---

## ⚡ Imperative Architectural Pitfalls

* **Never confuse a landing page with a complete website**: If the user requests a website for a business or brand, providing only a single-page scroller fails the requirement — always build dedicated interconnected sub-pages.
* **Never dump flat unstructured link lists across a multi-page header**: Flat rows of 7+ links look cluttered and unaligned; always use grouped segmented docks with hairline dividers.
* **Always verify sub-page HTTP 200 response codes**: Run automated curl or headless browser tests against all sub-page URLs (`/menu.html`, `/beans.html`, `/space.html`, etc.) to guarantee zero broken links.
* **Deploy both dedicated port and Nginx default root**: Sync web assets to `/var/www/html/` and the application working directory so clients can preview via dedicated ports (e.g. `:8085`) and standard HTTP root (`/`).
