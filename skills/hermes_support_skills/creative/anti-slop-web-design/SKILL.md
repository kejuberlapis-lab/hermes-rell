---
name: anti-slop-web-design
description: "Use when designing web UIs to eliminate AI slop tropes."
version: 1.0.0
author: Hermes AI
license: MIT
metadata:
  hermes:
    tags: [design, web, ui, editorial, anti-slop, tailwind, aesthetic]
    related_skills: [claude-design, popular-web-designs, design-md]
---

# Anti-Slop Web & UI Design Guide

## When to Use
Use this skill whenever designing, reviewing, or refactoring landing pages, brand websites, customer portals, or dashboards to eliminate generic AI design artifacts (*"AI slop"*) and deliver authentic, human-grade, tactile web experiences.

---

## 🚫 The 11 AI Slop Tells & How to Replace Them

| # | AI Slop Tell | Why It Fails | Anti-Slop Replacement |
|---|---|---|---|
| 1 | **Tech Gradient Mania** | Electric indigo/purple gradients look like cookie-cutter crypto/SaaS. | **Earthy / Organic Canvas**: Warm linen (`#F8F5EE`), deep roasted espresso (`#140F0D`), terracotta clay, or architectural monochrome. |
| 2 | **Rainbow Pastel / Carnival UI** | Assigning random pastel colors (pink, sky, green, amber, red, purple) to every single box and text label. | **Disciplined Monochrome & Single Accent**: Strict dark neutral headings (`text-slate-900`), muted body (`text-slate-600`), and a single cohesive brand accent color. |
| 3 | **Unearned Glassmorphism** | Blur and semi-transparent cards pasted everywhere without real depth. | **Tactile Physical Layers**: Subtle `dot-grid` canvas textures, hairline borders (`1px solid rgba(...)`), and grounded cards. |
| 4 | **Default Font Pairings** | Raw Inter / Roboto everywhere feels sterile and machine-generated. | **Bespoke Editorial Typography**: High-contrast Serif headlines (*Cormorant Garamond, Playfair Display*) + clean human geometric Sans body (*Plus Jakarta Sans*) + Mono metadata (*Space Grotesk / JetBrains Mono*). |
| 5 | **Icon-Topper Clichés** | Placing a rounded colored icon above every single heading. | **Clean Structural Hierarchy**: Use scale, weight, uppercase micro-labels, and whitespace instead of boxy icons. |
| 6 | **Equal-Weight Feature Grids** | 3 or 4 identical boxes with an icon + title + filler sentence. | **Asymmetric Editorial Spreads**: Prioritize the hero signature lot, highlight an authentic artifact, and vary column widths (7/5 or 8/4 grid). |
| 7 | **Generic Stock Fluff** | Unsplash search #1 hero images and abstract 3D spheres. | **Grounded Subject Photography**: Editorial close-ups of ingredients, brewing rituals, physical packaging, and human space. |
| 8 | **Decorative AI Buzzwords** | Vague labels like *"Seamless Synergy," "Next-Gen," "Revolutionary."* | **Concrete Specifications**: Real quantitative metrics, specific feature outcomes, and clear operational details. |
| 9 | **Floating Ghost Forms** | Forms that submit to nothing or display synthetic alert modals. | **Direct-Action Dispatch**: Form actions that pre-format messages directly to WhatsApp, email, or live backend APIs with instant feedback. |
| 10 | **Fake Dashboard Metrics** | Gratuitous counters without context. | **Transparent Metrics**: Real operational facts (roasting days, operating hours, direct-trade sourcing). |
| 11 | **Disconnected Action Controls** | Buttons that look clickable but fail under automation testing. | **Full Interactive Wiring**: Wire customizer modals, steppers `[-] qty [+]`, subtotal/PB1 tax calculations, and floating toast feedback. |

---

## 🛠️ Step-by-Step Anti-Slop Production Workflow

### 1. Palette & Surface Archetype Commitment
* Commit to the brand's authentic nature before writing code:
  * **Specialty Coffee / Hospitality**: Warm linen, raw sand, charcoal, ochre amber, dark roast.
  * **High-End Luxury / Fine Dining**: High-contrast black/bone, gold foil accents, bespoke serifs.
  * **Enterprise / FinTech**: Crisp high-density light themes, subtle grey borders, dark slate ink.

### 2. Crafting the Texture & Editorial Grid
* Add tactile micro-textures via CSS:
  ```css
  .bg-paper {
    background-color: #F8F5EE;
    background-image: radial-gradient(#E3DDD2 0.75px, transparent 0.75px);
    background-size: 24px 24px;
  }
  ```
* Use asymmetric editorial magazine layout with volume numbers, issue stamps, and hairline dividers.

### 3. Interactive Components & Visual Mockups
* Every menu or product list must include:
  * Rounded-square (*squircle*) product thumbnail mockup.
  * Category badge, price in clean typography, and detailed notes.
  * Two distinct action triggers: **Quick Add (`+ Pesan`)** and **Customizer Trigger (`⚙️ Custom`)**.
* Provide tactile user feedback (Toast notification pop-up on add to cart).

### 4. Verification Gate via Headless Browser
* Verify all interactive controls using browser automation tools:
  * Test category filtering without full page reloads.
  * Test quantity increment/decrement math and tax recalculations.
  * Test modal open/close transitions and form validation.
  * Ensure selector uniqueness (avoid generic `button:has-text("+")` locator collisions).

---

## ⚡ Imperative Anti-Slop Pitfalls

* **Avoid generic icon selectors in Playwright/Patchright tests**: Lucide JS replaces `<i data-lucide="...">` with `<svg class="lucide...">`, making `button:has(i[data-lucide])` fail after hydration — target `button[onclick="..."]` or explicit aria/title attributes.
* **Never ship decorative-only customizer buttons**: If an item offers kustomisasi (e.g. Milk: Oat/Almond, Temp: Hot/Ice), provide an interactive modal that reflects those choices in the cart payload and WhatsApp dispatch message.
