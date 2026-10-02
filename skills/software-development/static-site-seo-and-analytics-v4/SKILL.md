---
name: static-site-seo-and-analytics-v4
description: "Deploy static SEO, Yoast, bio links, and analytics."
version: 1.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [seo, yoast, static-sites, analytics, json-ld, sitemap, meta-tags, mobile-ux, copywriting, executive-insights, link-in-bio, light-theme]
---

# Static Site SEO, Yoast Standard Optimization, & Unified Web Analytics

A class-level operational guide for implementing comprehensive on-page SEO, Yoast-standard metadata, Schema.org JSON-LD structured data, XML sitemaps, robots crawler directives, mobile-first product page UI/copywriting, native domain Link-in-Bio micro-sites, and self-hosted unified web analytics command centers with executive business insights across multi-page static websites.

## When to Use

- When optimizing static HTML websites (e.g., cPanel/LiteSpeed, Nginx, GitHub Pages, Netlify) for search engine discovery, keyword rankings, and AI search citations (GEO - Generative Engine Optimization).
- When applying Yoast SEO standards (title tag formulas, calibrated meta descriptions, OpenGraph, Twitter Cards, robots directives) across multi-page portfolios and blogs.
- When formatting commercial product/solution/service pages to ensure immaculate mobile readability and elimination of dense, unstyled text blocks.
- When generating or synchronizing comprehensive `sitemap.xml` and `robots.txt` architectures.
- When creating self-hosted, on-domain Link-in-Bio micro-sites (`/link` or `/bio`) to replace third-party link aggregators (Lynk.id, Linktree) with zero watermark, enterprise branding, and native lead tracking.
- When building or maintaining self-hosted SQLite/PHP web analytics engines (Unique Visitors, Pageviews, Average Session Duration, Bounce Rate, Real-Time Active Users) and outbound lead tracking (WhatsApp, phone, email CTAs).
- When consolidating fragmented analytics into a single unified executive dashboard (Clean Light Theme) with plain-language business insights for business owners and executives.

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

4. **Sitemap.xml & Robots.txt Architecture:**
   - **Sitemap Generation:** Enumerate all canonical URLs in `sitemap.xml` with appropriate priority tiers (`1.0` for Homepage, `0.9` for Core Products/Services, `0.85` for Articles, `0.8` for Secondary Landing/Pricing), appropriate `<changefreq>`, and current `<lastmod>YYYY-MM-DD</lastmod>`.
   - **Robots.txt Crawler Rules:** Configure `robots.txt` allowing major crawlers (`Googlebot`, `Bingbot`, `Applebot`, `YandexBot`), disallowing internal directories (`/api/`, `/tmp/`, `/cgi-bin/`), and explicitly declaring the sitemap URL (`Sitemap: https://domain.com/sitemap.xml`).

5. **Mobile-First Product & Service Page UI Standards:**
   - **Eliminate Dense Raw Bullet Lists:** Never leave raw `<ul><li>✓...</li></ul>` checkmark lists where titles and long descriptive sentences collapse into unstyled text walls on mobile screens.
   - **Convert to Modern Structured Highlight Cards:**
     - A 4px solid left accent border (`border-left: 4px solid #2563eb;`).
     - Thematic circular icon badge (`32x32px`, `background: rgba(37,99,235,0.1)`, centered vector icon).
     - Bold title (`font-weight: 700; color: #0f172a; margin-bottom: 3px;`).
     - Muted, comfortable line-height description (`font-size: 0.85rem; color: #64748b; line-height: 1.5;`).
   - **Workflow & Process Steps:** Transform complex multi-step delivery workflows into numbered step cards with distinctive icons, bold titles, and clear phase deliverables.
   - **Mobile Specification & Matrix Tables:** Wrap multi-column technical comparison and solution matrix tables in responsive containers with `-webkit-overflow-scrolling: touch; overflow-x: auto;` and a clear touch-swipe prompt for smartphone users.

6. **Self-Hosted Link-in-Bio Micro-Site Architecture (`/link` & `/bio`):**
   - **Enterprise Branding:** Host link landing pages on the brand's primary domain (`domain.com/link` and `domain.com/bio`) instead of 3rd party services (Lynk.id, Linktree) to boost B2B institutional trust and eliminate 3rd-party ads/watermarks.
   - **Core Visual Modules:**
     - Centered circular avatar with verified badge checkmark (`🔵`).
     - Horizontal row of quick social media icon links (WhatsApp, Instagram, LinkedIn, YouTube, Email, Tel).
     - High-converting pulsating WhatsApp Hotline button with "Fast Response" badge.
     - Product/service action cards with vector icons, bold titles, and subtitles.
     - Interactive physical office/showroom location banner linked to Google Maps.
   - **Native Lead Tracking:** Embed the site's analytics and WhatsApp click tracker directly into all bio buttons.

7. **Unified Web Analytics & Executive Business Insights (Clean Light Theme):**
   - **Telemetry Collection:** Deploy lightweight client-side JavaScript (`/js/analytics.js`) injected in `<head>` with cache-busting query strings (`?v=YYYYMMDD_N`).
   - **Multi-Transport Fallback:** Capture data via `navigator.sendBeacon` -> `fetch({keepalive: true})` -> `new Image().src = ...` to ensure zero data loss on mobile browsers, iOS Safari, and in-app webviews.
   - **Theme & Visual Standards (Clean Light Theme):** Use bright off-white and pure white backgrounds (`#f8fafc`, `#ffffff`) with crisp card borders (`#e2e8f0`), high-contrast dark text (`#0f172a`, `#334155`), and colored accent sidebars for executive readability.
   - **Executive Insights Panel (Plain Business Language):** Position a full-width summary box directly below KPI cards translating technical numbers into plain-language business insights (visitor quality/intent, engagement duration, top-demanded offerings, device usage, WhatsApp conversion efficiency). Keep strategic recommendation panels optional and uncluttered unless explicitly requested by the stakeholder.
   - **Server Clutter Purge:** Delete obsolete test scripts (`probe.php`, `report.php`, redundant dashboard files) from the server when consolidating into a unified dashboard endpoint.

## Pitfalls

- **Dense Unformatted Mobile Text Walls:** Leaving plain text bullet points without card containers or visual separation causes high mobile bounce rates; convert all key features, components, and workflows into structured highlight cards.
- **Copy-Paste Template Drift & Foreign Tokens:** Reusing HTML page templates across different product categories without a line-by-line rewrite risks leaking mismatched hardware specs or foreign language fragments.
- **Fragile JS Scroll Animation Opacity Blockers:** Applying `.slide-up` classes with CSS `opacity: 0` without robust IntersectionObserver initialization hides entire page sections on mobile browsers.
- **Title Tag Character Overflow:** Exceeding 60 characters causes Google search results to truncate the brand name or primary commercial keywords with ellipses (`...`).
- **Dark Mode vs Executive Readability:** Overly dark executive dashboards reduce readability in brightly lit executive environments; default to Clean Light Theme with high-contrast text and clean card shadows.
- **Third-Party Link-in-Bio Dependencies:** Using 3rd-party link trees dilutes brand authority for B2B enterprises and introduces external tracking/captcha friction; deploy self-hosted `/link` pages on the official domain.
- **Technical-Only Dashboards Without Executive Summary:** Showing only raw numbers and bounce rates alienates business owners; always pair technical data with a plain-language executive summary.
- **Relative Script Paths in Subdirectories:** Using `<script src="js/analytics.js">` in nested directories like `/blog/*.html` leads to HTTP 404 errors; always use root-relative paths (`/js/analytics.js?v=...`).
