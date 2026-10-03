---
name: anti-slop-saas-paywall-design
description: "Use when designing Anti-Slop SaaS paywalls & QRIS modals."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [anti-slop, saas, landing-page, qris, paywall, tailwind, ui-ux, dark-mode, executive-dashboard]
---

# Anti-Slop SaaS Landing Page & Paywall Checkout Design

A class-level operational guide and standard for designing high-craft, developer-grade SaaS landing pages, Pay-to-Unlock subscription tiers, Dynamic QRIS checkout interfaces, and Executive Monitoring Dashboards without falling into generic AI design clichés (*"AI slop"*).

## When to Use

- When building or redesigning landing pages for AI agents, developer tools, SaaS platforms, or autonomous virtual workers.
- When implementing Paywall flows, subscription tiering, and dynamic QRIS payment checkout modals.
- When designing executive monitoring dashboards with live SQLite, QRIS transaction logs, and Nginx traffic telemetry.
- When eliminating AI template clichés: purple/blue gradient bloat, 3 identical icon-topper boxes, floating unaligned modals, and em-dash punctuation tells.

## Core Anti-Slop Archetypes & Rules

1. **Surface & Palette Commitment (Developer / Tech SaaS):**
   - **Background Canvas:** Dark Obsidian (`#06080F` / `#0B0F19`) or Crisp High-Contrast Light (`#F8FAFC`). Never default to generic indigo/purple mesh gradients.
   - **Texture & Layering:** Subtle technical dot-grid canvas (`radial-gradient(rgba(255, 255, 255, 0.07) 1px, transparent 1px)`) with hairline borders (`1px solid rgba(255, 255, 255, 0.08)`).
   - **Single High-Contrast Accent:** Restrain to one saturated accent (e.g. Crisp Emerald Mint `#10B981` / `#34D399` or Electric Blue).

2. **Precision Segmented Dock Navbar (3-Point Symmetry):**
   - Avoid long, crowded, unaligned single-row text links. Group navigation into a centered floating capsule dock (`p-1 rounded-full bg-obsidian-900 hairline-border shadow-inner`):
     - **Left Group (Core):** `Beranda` · `Katalog Skill` · `Pricing` · `Tutorial`.
     - **Precision Hairline Dividers:** Vertical `1px` lines (`w-[1px] h-4 bg-white/10 mx-1.5`) between functional groups.
     - **Center Group (Segments & Solutions):** Thematic icon pills (`Enterprise`, `UMKM`, `Personal Use`).
     - **Right Group (Support):** `Contact & Help`.
   - **Mobile Dual-Nav:** Pair desktop docks with an always-visible horizontal scrollable pill bar (`lg:hidden overflow-x-auto`) plus a collapsible dropdown drawer to prevent links from disappearing on mobile screens.

3. **Promo Pricing & Strikethrough Visual Hierarchy:**
   - **Inline Strikethrough:** Place strikethrough original prices (e.g. `~~Rp150k~~`) inline immediately beside the active promo price (e.g. `Rp99k`) rather than stacking them vertically. This preserves horizontal baseline alignment across all pricing tier cards.
   - **Strikethrough Contrast:** Render strikethrough text in bold (`font-extrabold`) with an explicit crimson/red strike line (`text-decoration-color: #ef4444; text-decoration-thickness: 3px`) to ensure the discount is visually unmistakable.

4. **Telegram Trust-Building Architecture:**
   - When deploying Telegram-first SaaS tools, include an explicit trust-building section addressing enterprise friction:
     - **Privacy & Isolation:** Highlight enterprise encryption and segregated database storage.
     - **Zero-Overhead:** 1-click start without software installation or RAM consumption.
     - **Lossless Document Exchange:** Full support for large native `.xlsx`, `.docx`, and PDF files without image compression.
     - **Seamless Multi-Device Continuity:** Synchronous access from mobile to desktop web without session drops.

5. **Dynamic Multi-Task Terminal Showcase (Auto-Cycle):**
   - Avoid static, single-prompt mockups. Build an auto-cycling interactive terminal simulator (cycling every 6-8 seconds) covering diverse real-world workloads (e.g. API debugging, Nginx Docker SSL, anti-bot web scraping, SQL index tuning, background cronjobs).
   - Include interactive tab selector buttons (`#1`, `#2`, `#3`), progress bars, simulated user handles (`[@growth_analyst]`), step-by-step action logs, and verified completion timestamps (`<30s latency`).

6. **Executive Admin Dashboard (Clean Light Monitoring):**
   - **Visual Standards:** Slate-50 canvas (`#f8fafc`), clean white cards with hairline borders (`#e2e8f0`), and high-contrast typography (*Plus Jakarta Sans*).
   - **Realtime Telemetry:** 4 KPI summary cards (Total Users, Free Trials, Total QRIS Invoices, Nginx Traffic), interactive Chart.js visualizations (Donut tier breakdown, Bar transaction pipeline), and searchable SQLite data tables.

7. **Proprietary SaaS Branding & Engine Confidentiality:**
   - Never expose third-party AI model names, underlying engines, or internal prompts in client-facing UI copy. Brand all capabilities under the platform's proprietary autonomous agent infrastructure.

8. **Bespoke Typography & Zero Em-Dash Discipline:**
   - **Font Stack:** Clean geometric UI Sans (*Plus Jakarta Sans* / *Geist*) paired with precision Monospace (*JetBrains Mono*) for telemetry, code, transaction IDs, and currency amounts.
   - **Zero Em-Dash (`—`) Rule:** Never use `—` in headlines, subheads, feature badges, or button labels. Use standard hyphens (`-`), colons, commas, or line breaks instead.

9. **Studio Precision QRIS Checkout Modal:**
   - **Modal Backdrop:** Deep dark backdrop blur (`bg-black/80 backdrop-blur-md`) with perfect viewport centering (`flex items-center justify-center`).
   - **Scanning Optimization:** Dynamic QR code must sit inside a crisp, high-contrast white rounded card with clear banking/e-wallet badges (BCA, Mandiri, GoPay, Dana, OVO, ShopeePay).
   - **Nominal Transparency:** Highlight the exact total amount including unique 3-digit verification code (`amount_uniq`).
   - **Dismissal & Telemetry:** Support click-outside backdrop dismissal and an explicit close button (`window.onclick`), plus direct action dispatch to the Telegram bot or support channel.

## Procedure

1. **Structure Layout & Containers:**
   - Create semantic sections: Sticky Navbar $\rightarrow$ Asymmetric Hero + Live CLI $\rightarrow$ Core Capabilities Grid (asymmetric/bento) $\rightarrow$ Subscription Matrix $\rightarrow$ Dynamic QRIS Checkout Modal $\rightarrow$ Trust Builder $\rightarrow$ FAQ $\rightarrow$ Minimalist Footer $\rightarrow$ Executive Dashboard (`/dashboard`).

2. **Wiring Interactive Paywall & QRIS Actions:**
   - Connect pricing tier CTA buttons directly to backend API (`POST /api/payment/create-qris`).
   - Ensure tactile button feedback on active state:
     ```css
     .btn-tactile:active {
       transform: translateY(1px) scale(0.99);
     }
     ```

3. **Verification via Browser Automation:**
   - Verify modal open/close states, dashboard telemetry endpoints (`GET /api/admin/metrics`), and inspect rendered layouts using `browser_vision` to confirm contrast, typography hierarchy, and absence of template artifacts.

## Pitfalls

- **Uncentered Modal Popups:** Forgetting `flex items-center justify-center` on fixed modal wrappers causes popups to render awkwardly pinned to the top on tall viewports.
- **Missing Click-Outside Handler:** Modals lacking `window.onclick` backdrop dismissal frustrate users on desktop and mobile clients.
- **Obscuring QR Codes in Dark Themes:** Inverting QR colors or placing QR codes on dark transparent backgrounds prevents camera barcode scanners from reading the payload. Always render QR codes on solid white backgrounds.
- **Stale Browser Caches on Rapid Iteration:** Forgetting to inject `Cache-Control: no-cache, no-store, must-revalidate, max-age=0` in backend response headers causes mobile and desktop browsers to serve stale HTML/CSS layouts even after server updates.
- **Mobile Viewport Navigation Blindspots:** Hiding top navigation links behind `hidden lg:flex` without a persistent horizontal scrollable pill dock or collapsible drawer leaves mobile users unable to reach sub-pages.
- **Exposing Internal Engine Names:** Leaking model names or underlying runtime frameworks in marketing copy diminishes perceived proprietary value and undermines brand positioning. Always present the platform as an autonomous proprietary agent.
- **Unsolicited Screenshot Artifacts in Chat:** Attaching `MEDIA:<path>` image screenshots in chat when the user did not explicitly ask for visual verification creates conversational clutter and wastes user bandwidth. Keep responses text-first unless images are requested.
