---
name: multi-page-web-architecture
description: "Use when building full multi-page websites and web apps."
version: 1.0.0
author: Hermes AI
license: MIT
metadata:
  hermes:
    tags: [web, architecture, multi-page, routing, state-persistence, localstorage, cart, tailwind, hospitality, ecommerce]
    related_skills: [anti-slop-web-design, popular-web-designs, claude-design]
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
* **Always verify sub-page HTTP 200 response codes**: Run automated curl or headless browser tests against all sub-page URLs (`/menu.html`, `/beans.html`, `/space.html`, etc.) to guarantee zero broken links.
* **Deploy both dedicated port and Nginx default root**: Sync web assets to `/var/www/html/` and the application working directory so clients can preview via dedicated ports (e.g. `:8085`) and standard HTTP root (`/`).
