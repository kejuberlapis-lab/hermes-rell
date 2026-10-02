---
name: web-asset-deployment-and-caching
description: "Use when deploying web assets or managing client caches."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [static-assets, deployment, caching, web-performance, cpanel, carousel, image-optimization]
    related_skills: [production-environment-operations-v2, systematic-debugging, reverify]
---

# Web Asset Deployment, Carousel Synchronization, & Client Cache Management

A standardized class-level operational guide for preparing high-resolution web media assets, synchronizing carousels and galleries, translating visual user feedback into CSS adjustments, and managing client-side cache divergence across shared hosting and CDN environments.

## When to Use

- When replacing or optimizing website banners, heroes, logos, or gallery/portfolio media assets.
- When deploying changes to static sites hosted on cPanel/LiteSpeed, Nginx, or shared hosting via FTP/SFTP/APIs.
- When synchronizing multi-element galleries or carousels (e.g., Swiper, Lightbox) where thumbnails and full-size links must align.
- When translating annotated user feedback (drawn lines/boxes on screenshots) into precise CSS spatial offsets.
- When diagnosing client cache discrepancies where users report seeing old styles despite successful server deployment.
- When implementing server-side outbound lead tracking (WhatsApp, tel, email) or a self-hosted Web Analytics Engine (Unique Visitors, Pageviews, Time on Page, Bounce Rate, Real-Time Active Users).

## Procedure

1. **Asset Optimization & DPI Upscaling:**
   - **Aspect Ratio Standardization:** Crop or scale incoming images to uniform canvas dimensions (e.g. `2400x1000` / `2560x1080` for hero banners; `1200x675` 16:9 for portfolio cards).
   - **Quality Enhancement for Compressed Uploads:** Source photos sent via chat apps often suffer from 1280px caps and compression. Apply Lanczos interpolation with unsharp masking:
     ```bash
     ffmpeg -y -i input.jpg -vf "scale=2560:1080:flags=lanczos,unsharp=5:5:1.0:5:5:0.0" -q:v 2 output.jpg
     ```
   - Request uncompressed master files sent as "File / Document" when maximum fidelity is required.

2. **Visual Feedback & Annotated Screenshot Translation:**
   - **Coordinate Extraction:** When users provide screenshots with drawn lines, boxes, or arrows, inspect the image with `vision_analyze` to extract spatial bounds and calculate pixel distance from neighboring UI elements.
   - **Local Staging Verification:** Spin up a temporary local HTTP server (`python3 -m http.server 8899`) and evaluate the layout with headless browser tools (`browser_navigate`, `browser_vision`) before pushing changes to production.
   - **Responsive Hierarchy:** Adjust padding, font sizes, and container gaps across all breakpoints (`@media (max-width: 1024px)` and `@media (max-width: 480px)`), not just desktop.

3. **Gallery, Multi-Category Filter Grid & "Load More" Synchronization:**
   - **Dual Target Alignment:** In interactive galleries, ensure both the thumbnail `<img src="...">` and modal zoom anchor `<a href="...">` point to the new asset.
   - **Multi-Category Grid & Progressive Disclosure:** When managing 10+ project assets, replace single-row carousels with a responsive multi-category filter grid (category pill tabs with item counters). Set an initial display limit (e.g. 6 items) paired with an interactive `[Lihat Lebih Banyak (N Proyek Lainnya) ↓]` expand/collapse toggle to maintain fast page load and avoid visual clutter.
   - **Filter State Synchronization:** When switching category tabs, reset expansion state and dynamically hide the "Load More" button if the filtered count is within the initial display limit.
   - **Metadata & Accessibility:** Set descriptive `alt` text and `data-title` attributes to preserve SEO value and lightbox captions.

4. **Remote Deployment & Transport Reliability:**
   - **Session Isolation & Retry Wrapping on Shared Hosts:** Do not hold a single FTP connection open across prolonged processing; wrap FTP upload blocks in retry loops with explicit connection timeouts (e.g. 25-35s) and passive mode (`set_pasv(True)`) to prevent socket timeouts on cPanel/LiteSpeed hosts.
   - **Pre-Deploy Snapshot:** Retain the previous version on the server (`asset_bak_<timestamp>.<ext>`) before overwriting.

5. **Global Multi-Page CTA, Contact, Social Media & Maps Synchronization:**
   - **Cross-Page Endpoint Scanning:** When updating official contact channels (e.g., WhatsApp number, emergency telephone, email, Instagram/social handles), do not update only `index.html`. Enumerate and patch all landing and product detail pages (`product-*.html`, `case-studies.html`, `pricing.html`, `landing.html`) using regex matching (`https?://wa\.me/\d+`, `api\.whatsapp\.com/send\?phone=\d+`, `tel:\+?\d+`, `instagram\.com/[^"]+`) to maintain consistent communication channels across the entire conversion funnel.
   - **Interactive Google Maps Universal Links:** Wrap physical address blocks and titles with universal Google Maps search URLs: `https://www.google.com/maps/search/?api=1&query=<Encoded+Company+Name+Full+Address>` with `target="_blank" rel="noopener noreferrer"`. This provides seamless app deep-linking across iOS Maps, Android Google Maps, and desktop browsers without API key friction.
   - **Structured Data (Schema.org / JSON-LD):** Keep `sameAs` social media arrays and `contactPoint` entries in `<script type="application/ld+json">` synchronized with visual contact cards and footer links.
   - **Brand Logo Dimension Guardrails:** Always enforce explicit `height`/`max-height` (e.g. `35-42px`) and `object-fit: contain` on brand logos in global CSS (`.logo img`, `.footer-brand img`) as well as inline fallbacks. High-resolution master assets (500px+) without explicit constraints will expand to native gigantic sizes when shared templates or new article subpages lack specialized container classes.

6. **Content Publishing & Yoast SEO Static Site Pipeline:**
   - **Google Docs Asset & Text Extraction:** When publishing articles from Google Docs links, extract structured text and embedded images programmatically via `/export?format=zip` (for images) and `/export?format=txt` (for raw text) to avoid manual copy-paste formatting loss.
   - **Semantic Image-Article Topic Verification:** When extracting multiple related articles simultaneously (e.g., educational classroom vs corporate meeting room), inspect image visual features with `vision_analyze` prior to linking to ensure headers match article context (e.g. students/teacher vs business executives).
   - **Yoast SEO & On-Page Hierarchy:** Structure article pages with a primary Focus Keyphrase in `<title>`, URL slug, `<meta name="description">` (150–160 chars), `<h1>`, introductory paragraph, and `<h2>`/`<h3>` headings. Use styled responsive tables for complex specification comparisons.
   - **Rich Snippets & Social Meta:** Inject `Article` and `BreadcrumbList` JSON-LD schemas alongside OpenGraph (`og:image`, `og:title`) and Twitter Card tags.
   - **Catalog & Sitemap Synchronization:** Update the blog catalog index (`blog.html`) with the new headline/grid cards and register new canonical URLs in `sitemap.xml` with updated `<lastmod>YYYY-MM-DD</lastmod>` timestamps.

7. **Cache Invalidation & Client Cache Diagnosis:**
   - **Cache-Buster Escalation:** Append query-string version tags (`hero.png?v=N+1`, `style.css?v=N+1`) across all HTML files to break through 7-day LiteSpeed/CDN cache headers.
   - **Server State vs Browser Cache:** When users report seeing outdated layouts, verify server response headers via `curl -sI` and take a clean headless browser snapshot.
   - **Actionable User Recovery Guidance:** Explain Chrome/Safari disk cache behavior and provide immediate platform-specific shortcuts:
     - Desktop: Hard refresh (`Ctrl + F5` or `Cmd + Shift + R`).
     - Mobile: Open in a New Incognito / Private Tab, or clear cached images in browser settings.

8. **Post-Deployment Verification & Rendering Diagnostics:**
   - Query the production URL directly, verify `HTTP 200` with expected `Content-Length`, and inspect the rendered page visually using browser screenshot verification before closing the task.
   - Verify that dynamic filter tabs, "Load More" button clicks, and lightbox modals trigger properly without JavaScript console errors.
   - Verify interactive DOM links: check `element.href` in browser console to ensure external URLs are well-formed and do not contain leading escaped quotation marks (`%22https...`).

9. **Server Access Logs, Outbound Lead Tracking & Self-Hosted Web Analytics:**
   - **Log Acquisition via FTP/SSH:** Pull archived web server access logs from shared cPanel/LiteSpeed hosts (`logs/<domain>-ssl_log-<Month>-<Year>.gz` and `logs/<domain>-<Month>-<Year>.gz`). Always enforce passive mode (`ftp.set_pasv(True)`) and explicit 30s timeouts to prevent socket hangs during multi-megabyte compressed transfers.
   - **Bot vs Human Traffic Filtering:** Filter search engine bots, crawlers, and vulnerability scanners (`googlebot`, `bingbot`, `ahrefs`, `semrush`, `petalbot`, `yandex`, `uptime`, `chatgpt`, `claudebot`) by User-Agent inspection to isolate authentic human visitor sessions.
   - **Day-of-Week Seasonality Analysis:** In B2B and institutional procurement domains, traffic follows a distinct weekly pattern: sharp Monday rebound (+100%+ DoD), midweek peak (Wednesday–Thursday), and significant weekend contraction (-40% to -50%). Evaluate growth across 7-day moving averages and Week-over-Week (WoW) baselines rather than isolated single-day fluctuations.
   - **Self-Hosted Web Analytics Engine (GA4 Style):**
     - Track 5 core metrics: (1) Unique Visitors via persistent `localStorage` Visitor ID, (2) Pageviews via initial `pageview` event, (3) Average Session Duration via 10–15s heartbeat pings and `visibilitychange`/`beforeunload` events, (4) Bounce Rate (< 10s single pageview = bounce, >= 10s or multi-page = engaged), (5) Real-Time Active Users (sessions pinged in last 180s).
     - Store telemetry in a local SQLite database in WAL mode (`PRAGMA journal_mode = WAL;`) for high concurrency and zero external dependencies. Protect the database file from direct browser downloads via `.htaccess` (`<FilesMatch "\.(db|db-wal|db-shm|jsonl)$"> Deny from all </FilesMatch>`).
     - **Multi-Transport Client Fallback:** Implement a 3-tier delivery mechanism in the tracking script: `navigator.sendBeacon` -> `window.fetch({keepalive: true})` -> `new Image().src = '/api/analytics.php?...'`. This ensures 100% telemetry capture across strict mobile operating systems, iOS Safari, and in-app webviews (WhatsApp/Instagram/Telegram).
     - **Early `<head>` Injection for Instant Capture:** Inject the analytics script (`<script src="/js/analytics.js?v=YYYYMMDD_N"></script>`) directly in `<head>` across all templates rather than at the bottom of the body. This guarantees immediate execution upon DOM start and breaks through aggressive 7-day mobile browser disk caching.
   - **Server-Side Outbound Lead Tracking (WhatsApp & External CTAs):** Standard web servers do not record outbound link clicks (`href="https://wa.me/..."`). Implement an asynchronous server-side beacon endpoint (`/api/track-lead.php`) paired with client-side event delegation:
     - Use `navigator.sendBeacon('/api/track-lead.php', JSON.stringify(payload))` with fallback to `fetch(..., {keepalive: true})` to record timestamp, CTA position, source page, device type, and target URL without delaying app launch.
     - Always use absolute root-relative script paths (`<script src="/js/main.js?v=YYYYMMDD"></script>`) across all templates so nested subdirectory pages (`/blog/*.html`) resolve the tracking script reliably.
     - When delivering dashboards or monthly reports for newly deployed trackers before real visitor data accumulates, state the true live count honestly (e.g. 0 records) and clearly label any format mockups as `[CONTOH FORMAT / SIMULASI]` to prevent confusion with encrypted chat logs on private phones.

## Pitfalls

- **Mobile Disk Cache on Injected Analytics Scripts:** Relying on existing bundled footer scripts (`main.js?v=old`) or bottom-of-page script tags causes returning mobile visitors (iOS/Android) to load cached versions lacking newly added tracking hooks; inject standalone `<script src="/js/analytics.js?v=YYYYMMDD_N"></script>` directly into `<head>` with an incremented cache-buster query string.
- **Click Intent vs Sent Message Attribution:** Assuming website click counters equal confirmed chats received on mobile; website trackers only record outbound clicks (intent), while WhatsApp's encrypted sandbox prevents web servers from verifying whether the message was actually sent (industry average conversion is 70%–85%).
- **Simulated/Mockup Data Misrepresentation in Production Reports:** Presenting simulated benchmark data as real production leads without explicit "[SIMULASI FORMAT]" labeling confuses users regarding whether data originates from their live encrypted apps (e.g. WhatsApp on mobile) vs newly deployed web server event trackers; always report live counts accurately and label format mockups explicitly.
- **Relative Script Path Resolution in Subdirectory Pages:** Using relative script paths like `<script src="js/main.js">` inside nested pages (e.g. `/blog/*.html`) causes the browser to request `/blog/js/main.js` (resulting in HTTP 404), silently disabling tracking, mobile menus, and interactive scripts; always use root-relative paths (`/js/main.js?v=...`).
- **Outbound Link Blindspot in Standard Server Logs:** Assuming standard Apache/LiteSpeed web server access logs track WhatsApp or phone inquiries; external link clicks leave the origin server immediately and require client-side `sendBeacon` event dispatch to be recorded.
- **Raw Server Log vs Real Human Traffic Confusion:** Quoting gross hit numbers or uncleaned server access logs as "visitor counts" creates massive false positives because single pageviews download 10+ static assets and automated AI/crawler bots generate 30%–50% of background hits; always filter bots and isolate unique HTML document requests.
- **Semantic Image-Article Topic Inversion in Multimodal Publishing:** When extracting and publishing multiple related articles simultaneously from a shared document (e.g., educational classroom vs corporate meeting room), failing to inspect image visual features with `vision_analyze` causes header images to be accidentally swapped between articles.
- **Escaped Quotation Marks in Programmatic Replacements:** Escaping double quotes inside replacement strings during automated regex passes (e.g. `r'href=\"https://...\"'`) injects literal quotes into HTML attributes (`href="\"https...\""`). Browsers interpret this as a relative URL (`https://site.com/%22https...%22`), silently breaking external navigations (Instagram, WhatsApp, external Maps).
- **Unconstrained Brand Logo in Shared Footers:** Referencing high-resolution master logos (`images/logo.png`) in footer or header blocks without global `.footer-brand img { height: 38px; }` CSS constraints results in oversized logos dominating the layout on standalone subpages.
- **Animation Opacity Lock (`.slide-up` with `opacity: 0`):** Adding animation classes that rely on scroll-triggered `IntersectionObserver` to newly injected grid containers causes them to remain invisible (`opacity: 0`) if the trigger does not fire; explicitly enforce `opacity: 1 !important; visibility: visible !important;` on dynamically filtered grids.
- **Native `loading="lazy"` on Hidden/Expandable Items:** Leaving native `loading="lazy"` on cards hidden behind a "Load More" toggle causes images to remain blank placeholders when revealed; use eager loading or programmatic trigger on expansion.
- **Stale Contact Links Across Subpages:** Updating the primary homepage WhatsApp button while forgetting secondary product pages leaves dead or wrong numbers on high-intent conversion funnels; always batch-update all HTML templates via automated script.
- **Gallery Zoom Mismatch:** Updating `<img src>` while leaving `<a href>` on old filenames causes the expanded Lightbox view to display outdated images.
- **Client Cache False-Positive Failure:** Assuming a deployment script failed because the user still sees old styles; verify server-side HTTP headers first before touching production code.
- **FTP Timeout on Shared Hosting:** Leaving FTP sessions open between image processing steps or uploading multiple un-retried assets causes silent disconnects and broken uploads; connect right before transfer and close immediately.
- **Breakpoint Neglect:** Increasing button padding or text size on desktop without scaling down tablet/mobile CSS rules causes mobile UI overflow.
- **Unverified Spatial Guessing:** Adjusting CSS margins by trial-and-error instead of measuring coordinate deltas from user-annotated screenshots wastes round-trips.
