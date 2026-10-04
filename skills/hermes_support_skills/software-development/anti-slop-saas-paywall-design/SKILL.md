---
name: anti-slop-saas-paywall-design
description: "Use when designing Anti-Slop SaaS paywalls & QRIS modals."
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [anti-slop, saas, landing-page, qris, paywall, tailwind, ui-ux, dark-mode, executive-dashboard, timezone-wib, video-walkthrough]
---

# Anti-Slop SaaS Landing Page & Paywall Checkout Design

A class-level operational guide and standard for designing high-craft, developer-grade SaaS landing pages, Pay-to-Unlock subscription tiers, Dynamic QRIS checkout interfaces, Executive Monitoring Dashboards, and automated video walkthroughs without falling into generic AI design clichés (*"AI slop"*).

## When to Use

- When building or redesigning landing pages for AI agents, developer tools, SaaS platforms, or autonomous virtual workers.
- When implementing Paywall flows, subscription tiering, and dynamic QRIS payment checkout modals.
- When designing executive monitoring dashboards with live SQLite, QRIS transaction logs, and Nginx traffic telemetry.
- When generating end-to-end video tutorial walkthroughs for Telegram bot and SaaS onboarding.
- When eliminating AI template clichés: purple/blue gradient bloat, 3 identical icon-topper boxes, floating unaligned modals, and em-dash punctuation tells.

## Core Anti-Slop Archetypes & Rules

1. **Surface & Palette Commitment (Developer / Tech SaaS):**
   - **Background Canvas:** Dark Obsidian (`#06080F` / `#0B0F19`) or Crisp High-Contrast Light (`#F8FAFC`). Never default to generic indigo/purple mesh gradients.
   - **Texture & Layering:** Subtle technical dot-grid canvas (`radial-gradient(rgba(255, 255, 255, 0.07) 1px, transparent 1px)`) with hairline borders (`1px solid rgba(255, 255, 255, 0.08)`).
   - **Single High-Contrast Accent:** Restrain to one saturated accent (e.g. Crisp Emerald Mint `#10B981` / `#34D399` or Electric Blue).

2. **Micro-Commitment Paywall & Quota Guard (Rp 1.000 vs "Free Trial"):**
   - **Eliminate Generic "Free Trial" Framing:** Replace "Free Trial (Rp0)" with a nominal micro-commitment tier (e.g. **Rp 1.000 / sekali coba** for 8 Command Tokens). Thoroughly sweep all secondary pages, hero badges, and docs to remove the word "Gratis" entirely.
   - **Proof-Driven Copywriting:** Title the entry tier with an action-driven hook: *"Lihat Bagaimana Virtual Tech Worker Bekerja"* or *"Tiket Uji Kerja"*.
   - **Punchy CTA:** Use high-converting direct calls-to-action: *"👉 Scan QRIS Rp 1.000 & Buktikan Sendiri"*.
   - **Quota Limit & Smart Upsell (Max 2x per User):** Enforce a strict backend rule limiting trial purchases to **maximum 2 paid trials per Telegram/user ID**. If a user attempts a 3rd purchase, return an HTTP 400 with an informative message and trigger a client-side confirmation dialog offering instant transition to the **Starter tier (Rp 99.000 / 50 Tokens)**.

3. **Timezone-Aware Telemetry Formatting (WIB / UTC+7):**
   - In executive dashboards and audit logs, never display raw UTC timestamps (`2026-10-03T14:30:00`).
   - Automatically convert server timestamps to local business time (**Asia/Jakarta, UTC+7**) using the standard format: `YYYY-MM-DD HH:MM:SS WIB` (e.g., `2026-10-03 21:30:00 WIB`).
   - Label column headers explicitly with `(WIB)` to guarantee unambiguous stakeholder reporting.

4. **Precision Segmented Dock Navbar (3-Point Symmetry):**
   - Avoid long, crowded, unaligned single-row text links. Group navigation into a centered floating capsule dock (`p-1 rounded-full bg-obsidian-900 hairline-border shadow-inner`):
     - **Left Group (Core):** `Beranda` · `Katalog Skill` · `Pricing` · `Tutorial`.
     - **Precision Hairline Dividers:** Vertical `1px` lines (`w-[1px] h-4 bg-white/10 mx-1.5`) between functional groups.
     - **Center Group (Segments & Solutions):** Thematic icon pills (`Enterprise`, `UMKM`, `Personal Use`).
     - **Right Group (Support):** `Contact & Help`.
   - **Mobile Dual-Nav:** Pair desktop docks with an always-visible horizontal scrollable pill bar (`lg:hidden overflow-x-auto`) plus a collapsible dropdown drawer to prevent links from disappearing on mobile screens.

5. **Promo Pricing & Strikethrough Visual Hierarchy:**
   - **Inline Strikethrough:** Place strikethrough original prices (e.g. `~~Rp150k~~`) inline immediately beside the active promo price (e.g. `Rp99k`) rather than stacking them vertically. This preserves horizontal baseline alignment across all pricing tier cards.
   - **Strikethrough Contrast:** Render strikethrough text in bold (`font-extrabold`) with an explicit crimson/red strike line (`text-decoration-color: #ef4444; text-decoration-thickness: 3px`) to ensure the discount is visually unmistakable.

6. **Telegram Trust-Building Architecture:**
   - When deploying Telegram-first SaaS tools, include an explicit trust-building section addressing enterprise friction:
     - **Privacy & Isolation:** Highlight enterprise encryption and segregated database storage.
     - **Zero-Overhead:** 1-click start without software installation or RAM consumption.
     - **Lossless Document Exchange:** Full support for large native `.xlsx`, `.docx`, and PDF files without image compression.
     - **Seamless Multi-Device Continuity:** Synchronous access from mobile to desktop web without session drops.

7. **Dynamic Multi-Task Terminal Showcase (Auto-Cycle):**
   - Avoid static, single-prompt mockups. Build an auto-cycling interactive terminal simulator (cycling every 6-8 seconds) covering diverse real-world workloads (e.g. API debugging, Nginx Docker SSL, anti-bot web scraping, SQL index tuning, background cronjobs).
   - Include interactive tab selector buttons (`#1`, `#2`, `#3`), progress bars, simulated user handles (`[@growth_analyst]`), step-by-step action logs, and verified completion timestamps (`<30s latency`).

8. **Executive Admin Dashboard & Frictionless Telemetry:**
   - **Clean Light Monitoring:** Slate-50 canvas (`#f8fafc`), clean white cards with hairline borders (`#e2e8f0`), and high-contrast typography (*Plus Jakarta Sans*).
   - **Frictionless Direct Access:** Keep internal executive monitoring dashboards open and directly viewable (`/dashboard`) without unnecessary modal/OTP/PIN auth gates when the stakeholder prioritizes instant access.
   - **Real Telegram User Detection:** Cross-reference SQLite database users with Telegram gateway channel directories (`channel_directory.json`) and session state databases (`state.db`) to detect and display real Telegram names (e.g. `Andi Saputra`, `Iskandar`), message volume, and token balances.

9. **High-Fidelity Automated Video Tutorial Walkthroughs:**
   - When delivering user onboarding walkthroughs, build an interactive 1920x1080 HTML/CSS/JS stage simulating each phase:
     1. *Scene 1: Web Navigation & Pricing Selection (Rp 1.000 QRIS / Bot link)*
     2. *Scene 2: Telegram Bot Welcome & `/start` activation*
     3. *Scene 3: Real multi-divisional prompt input & Multi-Agent reasoning status*
     4. *Scene 4: Deliverable output (Excel formula, legal clause) & live token deduction*
     5. *Scene 5: Outro & official channels*
   - Record headlessly via Playwright (`record_video_dir`, `record_video_size={"width": 1920, "height": 1080}`) and transcode with FFmpeg to H.264 MP4 (`-c:v libx264 -pix_fmt yuv420p -movflags +faststart -r 30`) for native Telegram media playback.

10. **Bespoke Typography & Zero Em-Dash Discipline:**
    - **Font Stack:** Clean geometric UI Sans (*Plus Jakarta Sans* / *Geist*) paired with precision Monospace (*JetBrains Mono*) for telemetry, code, transaction IDs, and currency amounts.
    - **Zero Em-Dash (`—`) Rule:** Never use `—` in headlines, subheads, feature badges, or button labels. Use standard hyphens (`-`), colons, commas, or line breaks instead.

11. **Studio Precision QRIS Checkout Modal:**
    - **Modal Backdrop:** Deep dark backdrop blur (`bg-black/80 backdrop-blur-md`) with perfect viewport centering (`flex items-center justify-center`).
    - **Scanning Optimization:** Dynamic QR code must sit inside a crisp, high-contrast white rounded card with clear banking/e-wallet badges (BCA, Mandiri, GoPay, Dana, OVO, ShopeePay).
    - **Nominal Transparency:** Highlight the exact total amount including unique 3-digit verification code (`amount_uniq`).
    - **Dismissal & Telemetry:** Support click-outside backdrop dismissal and an explicit close button (`window.onclick`), plus direct action dispatch to the Telegram bot or support channel.

## Pitfalls

- **Allowing Infinite Micro-Commitment Purchases:** Neglecting a trial purchase count limit allows users to repeatedly buy Rp 1.000 passes (8 tokens each) rather than converting to the higher-margin Starter/Advance tiers.
- **Unconverted UTC Timestamps in Dashboards:** Presenting raw UTC timestamps without adding $+7\text{ hours}$ (for WIB) confuses stakeholders and causes false discrepancy reports.
- **Uncentered Modal Popups:** Forgetting `flex items-center justify-center` on fixed modal wrappers causes popups to render awkwardly pinned to the top on tall viewports.
- **Sending JSON to Form-Encoded Gateways:** Sending JSON bodies to payment gateways (like BuatQris) that require `application/x-www-form-urlencoded` triggers 502/400 errors.
- **Stale Browser Caches on Rapid Iteration:** Forgetting to inject `Cache-Control: no-cache, no-store, must-revalidate, max-age=0` in backend response headers causes mobile and desktop browsers to serve stale HTML/CSS layouts even after server updates.
- **Mobile Viewport Navigation Blindspots:** Hiding top navigation links behind `hidden lg:flex` without a persistent horizontal scrollable pill dock or collapsible drawer leaves mobile users unable to reach sub-pages.
- **Exposing Internal Engine Names:** Leaking model names or underlying runtime frameworks in marketing copy diminishes perceived proprietary value and undermines brand positioning. Always present the platform as an autonomous proprietary agent.
- **Unsolicited Screenshot Artifacts in Chat:** Attaching `MEDIA:<path>` image screenshots in chat when the user did not explicitly ask for visual verification creates conversational clutter and wastes user bandwidth. Keep responses text-first unless images are requested.
