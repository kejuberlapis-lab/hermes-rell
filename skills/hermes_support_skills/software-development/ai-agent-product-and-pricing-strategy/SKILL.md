---
name: ai-agent-product-and-pricing-strategy
description: "Use when designing AI agent SaaS tiers, pricing, and UX."
version: 1.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [saas, ai-agents, pricing-strategy, product-management, free-trial, unit-economics, telegram-bots, pitch-deck, light-theme, qris-paywall, gateway, multi-page, terminal-simulator]
---

# AI Agent SaaS Product Strategy, Tiering Architecture, & Unit Economics

A class-level operational guide for packaging autonomous AI agents into commercial SaaS products, designing high-converting Free Trial loops, formulating 3-tier value-based pricing ladders, mapping skill capabilities across tiers, implementing dynamic QRIS auto-paywall middleware, white-labeling proprietary autonomous architectures, and building high-converting multi-page web portals.

## When to Use

- When structuring commercial SaaS subscription packages and message quotas for autonomous AI agents or Telegram-based virtual workers.
- When formulating Free Trial token limits and conversion paywalls that balance user trust with zero-risk API cost (COGS) burn rate.
- When implementing automated Dynamic QRIS paywalls, Telegram `/start` gatekeepers, and webhook settlement callbacks for instant user activation.
- When designing multi-page SaaS web portals and interactive skills catalogs that serve as the primary customer conversion hub.
- When enforcing proprietary engine white-labeling (shielding internal LLM models and framework names from client-facing assets).
- When building interactive live execution terminal simulators that cycle through real-world work scenarios to prove technical competence.
- When calculating unit economics, API token cost margins (~75%–80% gross profit), and monthly recurring revenue (MRR) projections.
- When generating executive pitch decks (16:9 PDF/PPTX) and high-contrast, Clean Light Theme visual comparison tables.

## Procedure

1. **Proprietary Engine White-Labeling & Confidentiality (Zero Model Leak):**
   - In all client-facing surfaces (website, landing pages, pitch decks, Telegram bot menus, system prompt responses), **strictly conceal internal LLM models** (GPT, Claude, Gemini, DeepSeek, etc.) and underlying orchestration frameworks.
   - Market the product purely as a **Proprietary Autonomous Execution Engine & Real-Time Action Pipeline**.
   - Frame the technology as custom enterprise-grade architecture capable of deterministic tool execution, self-healing, and end-to-end task completion.

2. **The 8-Token Free Trial Rule (Completion & Taste Principle):**
   - Never set trial quotas too low (e.g. 3–5 tokens), which risks cutting off the user mid-task and creating paywall frustration.
   - Never set trial quotas too high (e.g. 20 tokens), which cannibalizes 40% of the entry tier and allows users to finish entire monthly workloads without paying.
   - Enforce the **8-Token Golden Ratio**:
     - **Tokens 1–5 (Task 1 Tuntas 100%):** Delivers a fully completed, verified artifact (Excel file, fixed code, or ad copy), establishing deep trust and reciprocity.
     - **Tokens 6–8 (Taste 2nd Jobdesk):** Allows the user to test a completely different job skill (e.g. pivoting from web coding to financial analysis or copywriting), proving the "All-in-One" tagline.
     - **Token 8 Closure (Paywall Hook):** Displays a celebratory completion notice and a direct call to action to unlock 50 new task quotas for the entry price.

3. **Multi-Page Web Portal as Primary Customer Magnet:**
   - Commercial SaaS conversions require an authoritative multi-page architecture rather than a single scroller:
     - **`/` (Home / Overview):** Hero value proposition, live terminal/console simulation, 3-step pipeline, and instant Telegram CTA.
     - **`/skills` (Interactive Capabilities Catalog):** Searchable and filterable directory of technical skills with concrete input/output examples, deliverable specs, and estimated latencies (<30s).
     - **`/pricing` (Pricing & Dynamic QRIS):** 3-tier matrix, token economics calculator, and real-time QRIS modal checkout.
     - **`/case-studies` (Verified Real-World Proof):** Before/after technical breakdown of real problem resolutions (bug fix, scraping, DevOps).
     - **`/docs` (User Manual & Commands):** Telegram prompt guidelines, file upload formats, and `/saldo` / `/status` token management.
     - **`/enterprise`, `/umkm`, `/personal` (Target Audience Solution Pages):** Dedicated landing pages with tailored ROI, concrete workflows, and custom callouts.
     - **`/about` (Sandbox Security & Privacy):** Zero-trust session isolation, credential masking, and 99.9% uptime SLA.

4. **Dynamic Rotating Live Execution Terminal Simulator:**
   - Replace passive static screenshots with an interactive, auto-cycling terminal simulator (5+ task scenarios: backend bug fix, Nginx Docker SSL, anti-bot web scraping, SQL tuning, and background cronjob sync).
   - Display real prompt syntax (`[@user]`), step-by-step terminal execution logs, and verified completion timestamps (<30s). Provide interactive task selector tabs and auto-cycle progress bars to maximize engagement.

5. **Value-Based 3-Tier Pricing Ladder (Starter, Advance, PRO):**
   - Structure tiers with clear step-up incentives and asymmetric value:
     - **🟢 Tier 1: STARTER (Rp 100.000 / 50 Tasks | ~Rp 2.000/task):**
       - *Role:* Low-friction entry gate for students, solo developers, and freelancers.
       - *Scope:* Daily coding bug fixes, basic spreadsheet cleansing (<300 rows), legal/HR drafts (SPK/MoU), basic Nginx/VPS setup.
       - *Gross Margin:* ~80% (API COGS ~Rp 20.000).
     - **🔵 Tier 2: ADVANCE — BEST VALUE (Rp 249.000 / 150 Tasks | ~Rp 1.660/task | Save 17%):**
       - *Role:* Primary revenue driver (Cash Cow) for marketers, SMEs, and digital agencies. 3x quota for 2.5x price.
       - *Scope:* Starter skills + multi-file architecture refactor, full cloud VPS & database ops, bank mutation PDF parsing, priority task queue.
       - *Gross Margin:* ~76% (API COGS ~Rp 60.000).
     - **🟣 Tier 3: PRO — ENTERPRISE (Rp 499.000 / 350 Tasks | ~Rp 1.425/task | Save 29%):**
       - *Role:* High-ticket enterprise tier for corporate offices, software houses, and heavy-duty operators.
       - *Scope:* All Advance skills + massive stealth anti-bot web scraping, dedicated 24/7 background cronjob daemons, custom skill builders, and VIP priority.
       - *Gross Margin:* ~73% (API COGS ~Rp 135.000).

6. **Dynamic QRIS Auto-Paywall & Telegram Gatekeeper Middleware:**
   - **Pre-Flight Inbound Gatekeeper:**
     - On `/start` or message arrival, query database (`telegram_id`, `tier`, `remaining_tasks`, `trial_used`).
     - If `remaining_tasks > 0` or `trial_used < 8`, forward the prompt to the AI agent execution engine.
     - If quota is exhausted or zero, intercept the message *before* invoking LLM tools, and render the interactive tier selector with one-click payment buttons.
   - **On-Demand Dynamic QRIS Generation:**
     - User selects tier -> Backend calls payment gateway API (BuatQris Open API via single action `application/x-www-form-urlencoded`) with `amount`, `action=api_create_qris`, and credentials.
     - Return raw QR URL (`qr_url` PNG) or render QR code image directly to Telegram chat with countdown timer (e.g., 15 minutes) and total amount (including unique nominal code `total_amount`).
   - **Webhook Settlement & Instant Activation:**
     - Payment Gateway calls `/api/payment/webhook` on VPS.
     - Middleware verifies HMAC-SHA256 signature / Merchant Secret (`X-BuatQris-Signature` using raw body digest) to block forged settlement requests.
     - Atomically increment user's task balance in database, log invoice/transaction ID (with idempotency guard), and push instant success notification to user's Telegram chat with new balance and `/menu` prompt.

## Pitfalls

- **Exposing Underlying LLM Model Names:** Revealing model names (e.g. OpenAI/Anthropic/Google) in promotional copy commoditizes the product and encourages users to bypass your SaaS and use the raw models directly; always maintain proprietary branding.
- **Direct LLM Invocations Without Pre-Flight Middleware:** Routing Telegram `/start` or chat messages directly to the LLM agent without a deterministic database gatekeeper burns API tokens on non-paying users.
- **Insecure Webhook Endpoints Without Signature Verification:** Processing payment callbacks without validating HMAC-SHA256 signature or merchant secret allows malicious actors to forge fake settlement requests and claim free token quotas.
- **Overwhelming Mainstream Users with Multi-Agent Jargon:** Marketing multi-agent technical orchestration to non-technical business owners causes confusion and hesitation; sell the outcome as a single, ultra-capable virtual team member.
- **Under-Provisioning Free Trial Quotas (<5 Tasks):** Stopping trial users before their first real task is 100% finished generates resentment rather than conversion; ensure at least 1 complex task finishes completely before triggering the paywall.
- **Over-Provisioning Free Trial Quotas (>15 Tasks):** Giving too many free tasks allows users to finish their entire one-off project for free and creates vulnerability to multi-account abuse.
- **Single-Page Landing Pages for Complex Technical SaaS:** Relying solely on a one-page scroller without a dedicated skills catalog, documentation, and security proof creates trust friction for technical buyers.
- **Static Passive Terminal Previews:** Using static screenshots rather than an animated, rotating multi-task execution terminal fails to showcase breadth across coding, DevOps, data scraping, and automations.
