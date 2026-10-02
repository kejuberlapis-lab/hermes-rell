---
name: static-site-seo-and-analytics-v2
description: "Deploy static SEO, Yoast standards, and unified analytics."
version: 1.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [seo, yoast, static-sites, analytics, json-ld, sitemap, meta-tags, mobile-ux, copywriting, executive-insights, link-in-bio]
---

# Static Site SEO, Yoast Standard Optimization, & Unified Web Analytics

A class-level operational guide for implementing comprehensive on-page SEO, Yoast-standard metadata, Schema.org JSON-LD structured data, XML sitemaps, robots crawler directives, mobile-first product page UI/copywriting, official domain Link-in-Bio micro-sites, and self-hosted unified web analytics command centers with executive business insights across multi-page static websites.

## When to Use

- When optimizing static HTML websites (e.g., cPanel/LiteSpeed, Nginx, GitHub Pages, Netlify) for search engine discovery, keyword rankings, and AI search citations (GEO - Generative Engine Optimization).
- When applying Yoast SEO standards (title tag formulas, calibrated meta descriptions, OpenGraph, Twitter Cards, robots directives) across multi-page portfolios and blogs.
- When formatting commercial product/solution/service pages to ensure immaculate mobile readability and elimination of dense, unstyled text blocks.
- When creating an official-domain Link-in-Bio micro-site (e.g., `/link/` or `/bio/`) to replace third-party link aggregators (Lynk.id, Linktree) with zero watermarks and native analytics.
- When generating or synchronizing comprehensive `sitemap.xml` and `robots.txt` architectures.
- When building or maintaining self-hosted SQLite/PHP web analytics engines (Unique Visitors, Pageviews, Average Session Duration, Bounce Rate, Real-Time Active Users) and outbound lead tracking (WhatsApp, phone, email CTAs).
- When consolidating fragmented analytics into a single unified executive dashboard with clean light-theme styling and plain-language business insights for business owners and executives.

## Procedure

1. **Yoast-Standard Metadata Calibration:**
   - **Title Tag Formula (50–60 Chars):** Position high-intent commercial or informational keywords at the beginning, followed by a brand separator:
     `[High-Intent Focus Keyphrase] | [Brand / Region]`
     *(Strictly avoid exceeding 60 characters to prevent Google SERP ellipsis truncation).*
   - **Meta Description (145–160 Chars):** Draft active, compelling descriptions containing the exact target focus keyphrase, core value proposition, and a clear Call to Action (e.g. hotline phone/WhatsApp number).
   - **Modern Robots Directives:** Include `<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">` on all public pages to unlock Google Discover large card previews and rich SERP snippets.
   - **Canonical Tag Hardcoding:** Add `<link rel="canonical" href="https://domain.com/exact-page.html">` to prevent split ranking caused by query parameters, tracking tags, or duplicate index routes.

2. **OpenGraph & Twitter Card Social Stack:**
   - **OpenGraph Tags:** Set `og:locale` (`id_ID` or target locale), `og:type` (`website`, `article`, `product`, or `service`), `og:title`, `og:description`, `og:url`, `og:site_name`, `og:image` (1200x630px high-resolution banner), `og:image:width`, and `og:image:height`.
   - **Twitter Cards:** Deploy `twitter:card` (`summary_large_image`), `twitter:title`, `twitter:description`, `twitter:image`, and `twitter:site`.

3. **Schema.org JSON-LD Structured Data:**
   - **Organization & LocalBusiness:** On root landing/homepages, deploy structured schemas with official business names, alternate names, logo image object, geo-coordinates (`latitude`/`longitude`), operating hours, address, `contactPoint` phone numbers, and `sameAs` social media links.
   - **Product & Service:** On commercial offering pages, deploy `Product` or `Service` schemas with brand, category, offers, provider, and area served.
   - **BreadcrumbList & Article:** On blog and educational articles, inject `BreadcrumbList` navigation and `Article` / `BlogPosting` schemas with author, publisher, `datePublished`, and `dateModified`.

4. **Official Domain Link-in-Bio Micro-Site Architecture:**
   - **Replace Third-Party Aggregators (Lynk.id / Linktree):** Deploy a self-hosted, mobile-first micro-page at `/link/index.html` (and `/bio/index.html`) under the company's official domain.
   - **Design & Conversion Elements:**
     - Centered brand avatar with official verified checkmark badge (`🔵`).
     - Horizontal quick-action social media icon bar (WhatsApp, Instagram, LinkedIn, YouTube, Email, Maps).
     - Glowing, high-visibility primary WhatsApp sales hotline CTA button with response-time SLA badge (e.g. "RESPON CEPAT < 5 MENIT").
     - Stack of styled interactive product/service link cards with clean category icons.
     - Direct showroom / consultation booking highlight card.
   - **Native Lead & Traffic Tracking:** Link all buttons with `data-cta-location="bio_link_..."` attributes so every click automatically records to the master SQLite lead tracking database.

5. **Mobile-First Product & Service Page UI Standards:**
   - **Eliminate Dense Raw Bullet Lists:** Never leave raw `<ul><li>✓...</li></ul>` checkmark lists where titles and long descriptive sentences collapse into unstyled text walls on mobile screens.
   - **Convert to Modern Structured Highlight Cards:**
     - A 4px solid left accent border (`border-left: 4px solid #2563eb;`).
     - Thematic circular icon badge (`32x32px`, `background: rgba(37,99,235,0.1)`, centered vector icon).
     - Bold title (`font-weight: 700; color: #0f172a; margin-bottom: 3px;`).
     - Muted, comfortable line-height description (`font-size: 0.85rem; color: #64748b; line-height: 1.5;`).
   - **Workflow & Process Steps:** Transform complex multi-step delivery workflows into numbered step cards with distinctive icons, bold titles, and clear phase deliverables.
   - **Mobile Specification & Matrix Tables:** Wrap multi-column technical comparison and solution matrix tables in responsive containers with `-webkit-overflow-scrolling: touch; overflow-x: auto;` and a clear touch-swipe prompt for smartphone users.

6. **Unified Web Analytics & Executive Business Insights:**
   - **Telemetry Collection:** Deploy lightweight client-side JavaScript (`/js/analytics.js`) injected in `<head>` with cache-busting query strings (`?v=YYYYMMDD_N`).
   - **Multi-Transport Fallback:** Capture data via `navigator.sendBeacon` -> `fetch({keepalive: true})` -> `new Image().src = ...` to ensure zero data loss on mobile browsers, iOS Safari, and in-app webviews.
   - **Executive Command Center Layout (Clean Light Theme Standard):** Default to a clean, bright, white-themed interface (`#ffffff` cards, `#f8fafc` background, high-contrast dark text `#0f172a`) which is significantly more approachable and comfortable for business owners and executives compared to dark mode.
   - **Dashboard Components:**
     1. **Top 6 KPI Summary Cards:** Unique Visitors, Pageviews, Average Duration, Bounce Rate, WhatsApp Leads, Conversion Rate.
     2. **Executive Insights Panel (Plain Business Language):** Translate technical metrics into plain-language conclusions (visitor intent quality, engagement duration, top-demanded products, device dominance, lead conversion performance).
     3. **Visual Trend Charts:** Daily visitor/lead correlation line chart and device breakdown donut chart.
     4. **Real-Time Data Feeds:** WhatsApp Leads Intent log, Top Pages & Reading Duration ranking, and Live active visitor session feed.
   - **Server Clutter Purge:** Delete obsolete testing scripts (`probe.php`, `report.php`, secondary dashboard files) from the server to maintain speed, security, and clarity.

## Pitfalls

- **Third-Party Bio Link Leakage:** Relying on third-party linktree/lynk.id services bleeds domain authority, exposes users to third-party ads/watermarks, and disconnects click events from internal CRM tracking. Host the bio-link directly on the brand's root domain.
- **Dark Mode Alienation on Executive Dashboards:** Dark UI themes often feel technical and unapproachable to non-technical business owners; always use clean, bright light themes with clear card shadows and high contrast for executive presentations.
- **Unsolicited Recommendation Clutter:** Overloading executive dashboards with unsolicited strategic advice panels dilutes focus; keep dashboards focused on plain-language insights on actual performance data unless recommendations are explicitly requested.
- **Dense Unformatted Mobile Text Walls:** Leaving plain text bullet points without card containers or visual separation causes high mobile bounce rates; convert all key features, components, and workflows into structured highlight cards.
- **Copy-Paste Template Drift & Foreign Tokens:** Reusing HTML page templates across different product categories without a line-by-line rewrite risks leaking mismatched hardware specs or foreign language fragments.
- **Fragile JS Scroll Animation Opacity Blockers:** Applying `.slide-up` classes with CSS `opacity: 0` without robust IntersectionObserver initialization hides entire page sections on mobile browsers or when scripts fail.
- **Title Tag Character Overflow:** Exceeding 60 characters causes Google search results to truncate the brand name or primary commercial keywords with ellipses (`...`).
- **Relative Script Paths in Subdirectories:** Using `<script src="js/analytics.js">` in nested directories like `/blog/*.html` leads to HTTP 404 errors; always use root-relative paths (`/js/analytics.js?v=...`).
