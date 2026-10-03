---
name: saas-web-architecture-and-paywall
description: "Use when building SaaS web portals and QRIS paywalls."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [saas, architecture, paywall, qris, anti-slop, multi-page, dark-mode, fastapi, terminal-simulator]
---

# Commercial SaaS Web Architecture, Paywall & Dynamic Showcase Guide

A class-level operational standard for designing, structuring, and deploying commercial developer-grade SaaS websites, multi-page customer funnels, Dynamic QRIS payment gateways, and live action showcases.

## When to Use

- When building or refactoring a SaaS marketing portal or AI agent platform into a comprehensive **Multi-Page Web Architecture** (distinct from a single landing page).
- When integrating dynamic payment paywalls (e.g. BuatQris Open API, token quotas, webhook callbacks).
- When designing developer-grade, Anti-Slop user interfaces with dark studio palettes, hairline borders, and live rotating CLI execution showcases.
- When creating customer segmentation funnels (`Enterprise`, `UMKM/SME`, `Personal/Developer`).

---

## 🏛️ Core SaaS Multi-Page Architecture Blueprint

Deliver a modular multi-page system with standardized file structures and unified navigation:

| Route | Page Scope | Mandatory Interactive Components |
|---|---|---|
| **`/` (`index.html`)** | **Platform Overview & Hero** | Asymmetric hero, dynamic auto-cycling CLI terminal simulator (5 diverse task scenarios), 3-step execution pipeline, verified SLA metrics. |
| **`/skills` (`skills.html`)** | **Technical Skills Catalog** | Real-time search filter, category tabs (*Fullstack, DevOps, Scraping, Automation, Database, Security*), concrete input/output specs, latency tags (<30s), direct bot CTA. |
| **`/pricing` (`pricing.html`)** | **Pricing & QRIS Paywall** | Subscription tiering cards (Free Trial, Starter, Advance, Pro), value economics breakdown, interactive Dynamic QRIS modal checkout with real-time settlement countdown. |
| **`/docs` (`docs.html`)** | **Bot Tutorial & Reference** | Step-by-step Telegram prompt formatting, file/error log attachment guidelines, token management commands (`/saldo`, `/status`, `/paket`). |
| **`/enterprise` (`enterprise.html`)** | **Enterprise Solutions** | Dedicated private VPS sandbox, Zero-Data Retention policy, custom private SOP skills, 99.9% SLA, contact CTA. |
| **`/umkm` (`umkm.html`)** | **SME & Local Business** | 24/7 Google Sheets auto-sync, price monitoring, auto-responder dispatch, instant PDF invoice generator. |
| **`/personal` (`personal.html`)** | **Solo Dev & Productivity** | 8-token free trial onboarding, midnight bug fixing, zero-hassle VPS deployment, dataset scraping. |
| **`/contact` (`contact.html`)** | **Contact & Help Center** | WhatsApp enterprise consultation link, Telegram bot support channel, automated inquiry form, QRIS payment help desk. |

---

## 🎨 Anti-Slop Visual & Copy Standards

1. **Surface & Palette Commitment:**
   - **Canvas:** Dark Obsidian (`#06080F` / `#0B0F19` / `#101626`) with subtle dot-grid background (`radial-gradient(rgba(255, 255, 255, 0.07) 1px, transparent 1px)`).
   - **Borders & Accents:** Hairline borders (`1px solid rgba(255,255,255,0.08)`) with a single crisp accent (e.g. Electric Mint `#10B981` / `#34D399`).
   - **Typography:** *Plus Jakarta Sans* for clean UI + *JetBrains Mono* for telemetry, code, and pricing data.

2. **White-Labeling & Engine Confidentiality:**
   - **Zero AI Engine Leaks:** Never expose underlying LLM foundation model names or providers (OpenAI, Claude, Gemini, DeepSeek, Hermes) in customer-facing UI or copy.
   - **Proprietary Branding:** Present all capabilities as an in-house *"Autonomous Virtual Technical Worker"* or *"Autonomous Execution Pipeline"*.

3. **Dynamic Rotating Live CLI Terminal Showcase:**
   - Instead of static screenshots, build an interactive simulated terminal in the Hero section that auto-cycles every 6-8 seconds across 5 realistic technical domains:
     1. *#1 Fullstack Bug Fix & CORS/Deadlock Resolution*
     2. *#2 DevOps, Docker Container Orchestration & SSL Certbot*
     3. *#3 Stealth Anti-Bot Web Scraping (Cloudflare Turnstile Bypass)*
     4. *#4 Database SQL Query Tuning & B-Tree Index Optimization*
     5. *#5 Background Cronjobs & 24/7 Google Sheets Sync*
   - Provide clickable task tab selectors, progress bar timers, typing/step logs, and verified latency timestamps.

4. **Studio Precision QRIS Checkout Modal:**
   - Render QR code inside a solid white rounded card for instant mobile camera recognition.
   - Show banking/e-wallet logos (BCA, Mandiri, GoPay, Dana, OVO, ShopeePay).
   - Highlight the exact total amount including unique 3-digit verification code (`amount_uniq`).
   - Support click-outside backdrop dismissal and explicit close buttons.

---

## ⚙️ Backend & Routing Best Practices (FastAPI)

1. **Custom `/docs` Route Collision:**
   - FastAPI intercepts `/docs` by default for Swagger UI. When serving custom HTML documentation at `/docs`, disable Swagger docs during app instantiation:
     ```python
     app = FastAPI(title="SaaS Platform", docs_url=None, redoc_url=None)
```
2. **Explicit Multi-Path Handlers:**
   - Chaining multiple decorators on one function (e.g. `@app.get("/skills")` and `@app.get("/skills.html")`) only registers the last decorator in FastAPI. Create separate handler functions for clean route aliasing.
3. **Port Lifecycle Management:**
   - When restarting daemons via systemd, kill lingering orphaned processes (`fuser -k <port>/tcp`) to prevent `[Errno 98] address already in use` bind failures.
