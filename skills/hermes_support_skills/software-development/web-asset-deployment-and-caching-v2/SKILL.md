---
name: web-asset-deployment-and-caching-v2
description: "Use when deploying web assets or managing client caches."
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [static-assets, deployment, caching, web-performance, cpanel, carousel, image-optimization, super-resolution]
    related_skills: [production-environment-operations-v2, systematic-debugging, reverify]
---

# Web Asset Deployment, Carousel Synchronization, & Client Cache Management

A standardized class-level operational guide for preparing high-resolution web media assets, super-resolution denoising and upscaling, synchronizing carousels and galleries, translating visual user feedback into CSS adjustments, and managing client-side cache divergence across shared hosting and CDN environments.

## When to Use

- When replacing or optimizing website banners, heroes, logos, or gallery/portfolio media assets.
- When deploying changes to static sites hosted on cPanel/LiteSpeed, Nginx, or shared hosting via FTP/SFTP/APIs.
- When upscaling and cleaning low-resolution or compressed images (e.g. from chat apps) into crisp 2K/4K Retina-ready assets.
- When resolving duplicate text/button overlays when graphics have CTA buttons pre-baked into the image.
- When synchronizing multi-element galleries or carousels (e.g., Swiper, Lightbox) where thumbnails and full-size links must align.
- When translating annotated user feedback (drawn lines/boxes on screenshots) into precise CSS spatial offsets.
- When diagnosing client cache discrepancies where users report seeing old styles despite successful server deployment.
- When implementing server-side outbound lead tracking (WhatsApp, tel, email) or a self-hosted Web Analytics Engine.

## Procedure

1. **Asset Optimization, Super-Resolution & DPI Upscaling:**
   - **Multi-Pass Super-Resolution & Denoising Pipeline:** When source photos sent via chat apps suffer from 1280px caps and JPEG compression artifacts, upscale to 2560px for Retina/4K displays using a 3-stage PIL pipeline:
     ```python
     from PIL import Image, ImageFilter, ImageEnhance

     im = Image.open(input_path).convert("RGB")
     # 1. 2x Super-sampling with Lanczos
     target_w = 2560
     target_h = int(im.size[1] * (target_w / im.size[0]))
     im_2x = im.resize((target_w, target_h), Image.Resampling.LANCZOS)

     # 2. Edge-preserving smoothing on flat background areas
     im_smooth = im_2x.filter(ImageFilter.SMOOTH_MORE)
     edges = im_2x.filter(ImageFilter.FIND_EDGES).convert('L')
     edges_thresh = edges.point(lambda p: 255 if p > 30 else 0).filter(ImageFilter.GaussianBlur(1))
     im_clean = Image.composite(im_2x, im_smooth, edges_thresh)

     # 3. Multi-band unsharp mask + micro-contrast
     im_crisp = im_clean.filter(ImageFilter.UnsharpMask(radius=1.8, percent=190, threshold=1))
     im_crisp = im_crisp.filter(ImageFilter.UnsharpMask(radius=3.5, percent=90, threshold=2))
     im_final = ImageEnhance.Contrast(im_crisp).enhance(1.08)
     im_final = ImageEnhance.Sharpness(im_final).enhance(1.15)
     im_final.save(output_path, "PNG", quality=100)
     ```

2. **Hero Banner Button Overlay & Anti-Ghosting Alignment:**
   - **Detecting Pre-Baked Graphic Text:** When inserting hero images that already contain visually rendered buttons (e.g., "KONSULTASI GRATIS", "LIHAT SOLUSI") in the raster file, inspect the overlying HTML structure.
   - **Transparent Hotspot Overlays:** Rather than rendering visible HTML text that will misalign or create a double-vision ghosting glitch over the raster buttons, style the HTML overlay buttons as invisible click targets:
     ```html
     <div class="hero-ui-container">
       <a class="btn-primary hero-btn" href="#contact" style="opacity: 0; cursor: pointer;">Konsultasi Gratis</a>
       <a class="btn-white hero-btn" href="#services" style="opacity: 0; cursor: pointer;">Lihat Solusi</a>
     </div>
     ```
     This keeps keyboard/mouse accessibility and navigation routing 100% functional while ensuring the visual banner displays with zero duplicate-text artifacts.

3. **Visual Feedback & Annotated Screenshot Translation:**
   - **Coordinate Extraction:** When users provide screenshots with drawn lines, boxes, or arrows, inspect the image with `vision_analyze` to extract spatial bounds and calculate pixel distance from neighboring UI elements.
   - **Local Staging Verification:** Spin up a temporary local HTTP server (`python3 -m http.server 8899`) and evaluate the layout with headless browser tools (`browser_navigate`, `browser_vision`) before pushing changes to production.
   - **Responsive Hierarchy:** Adjust padding, font sizes, and container gaps across all breakpoints (`@media (max-width: 1024px)` and `@media (max-width: 480px)`), not just desktop.

4. **Gallery, Multi-Category Filter Grid & "Load More" Synchronization:**
   - **Dual Target Alignment:** In interactive galleries, ensure both the thumbnail `<img src="...">` and modal zoom anchor `<a href="...">` point to the new asset.
   - **Multi-Category Grid & Progressive Disclosure:** When managing 10+ project assets, replace single-row carousels with a responsive multi-category filter grid (category pill tabs with item counters). Set an initial display limit (e.g. 6 items) paired with an interactive `[Lihat Lebih Banyak (N Proyek Lainnya) ↓]` expand/collapse toggle to maintain fast page load and avoid visual clutter.
   - **Filter State Synchronization:** When switching category tabs, reset expansion state and dynamically hide the "Load More" button if the filtered count is within the initial display limit.
   - **Metadata & Accessibility:** Set descriptive `alt` text and `data-title` attributes to preserve SEO value and lightbox captions.

5. **Remote Deployment & Transport Reliability:**
   - **Session Isolation & Retry Wrapping on Shared Hosts:** Do not hold a single FTP connection open across prolonged processing; wrap FTP upload blocks in retry loops with explicit connection timeouts (e.g. 25-35s) and passive mode (`set_pasv(True)`) to prevent socket timeouts on cPanel/LiteSpeed hosts.
   - **Pre-Deploy Snapshot:** Retain the previous version on the server (`asset_bak_<timestamp>.<ext>`) before overwriting.

6. **Global Multi-Page CTA, Contact, Social Media & Maps Synchronization:**
   - **Cross-Page Endpoint Scanning:** When updating official contact channels (e.g., WhatsApp number, emergency telephone, email, Instagram/social handles), do not update only `index.html`. Enumerate and patch all landing and product detail pages (`product-*.html`, `case-studies.html`, `pricing.html`, `landing.html`) using regex matching.
   - **Interactive Google Maps Universal Links:** Wrap physical address blocks and titles with universal Google Maps search URLs: `https://www.google.com/maps/search/?api=1&query=<Encoded+Company+Name+Full+Address>` with `target="_blank" rel="noopener noreferrer"`.
   - **Brand Logo Dimension Guardrails:** Always enforce explicit `height`/`max-height` (e.g. `35-42px`) and `object-fit: contain` on brand logos in global CSS (`.logo img`, `.footer-brand img`) as well as inline fallbacks.

7. **Cache Invalidation & Client Cache Diagnosis:**
   - **Cache-Buster Escalation:** Append query-string version tags (`hero.png?v=N+1`, `style.css?v=N+1`) across all HTML files to break through 7-day LiteSpeed/CDN cache headers.
   - **Server State vs Browser Cache:** When users report seeing outdated layouts, verify server response headers via `curl -sI` and take a clean headless browser snapshot.
   - **Actionable User Recovery Guidance:** Explain Chrome/Safari disk cache behavior and provide immediate platform-specific shortcuts (`Ctrl + F5` or `Cmd + Shift + R` on desktop; Incognito tab on mobile).

8. **Post-Deployment Verification & Rendering Diagnostics:**
   - Query the production URL directly, verify `HTTP 200` with expected `Content-Length`, and inspect the rendered page visually using browser screenshot verification before closing the task.
   - Verify that dynamic filter tabs, "Load More" button clicks, and lightbox modals trigger properly without JavaScript console errors.

## Pitfalls

- **Duplicate Button Text Overlay Ghosting:** Overriding a hero banner graphic with pre-baked visual CTA text while retaining opaque HTML `<a class="btn">` overlays causes text duplication and slight misalignment; set the overlying HTML links to `opacity: 0; cursor: pointer;` to keep clickability without visual clutter.
- **Pixelation from Direct Upscaling without Edge Filtering:** Upscaling compressed 1280px JPEG uploads to 2560px via nearest-neighbor or raw bilinear scaling magnifies block noise; always use Lanczos interpolation with edge-preserving smoothing and unsharp masking.
- **Mobile Disk Cache on Injected Analytics Scripts:** Relying on existing bundled footer scripts (`main.js?v=old`) or bottom-of-page script tags causes returning mobile visitors to load cached versions; inject standalone `<script src="/js/analytics.js?v=YYYYMMDD_N"></script>` directly into `<head>` with an incremented cache-buster query string.
- **Relative Script Path Resolution in Subdirectory Pages:** Using relative script paths like `<script src="js/main.js">` inside nested pages (e.g. `/blog/*.html`) causes the browser to request `/blog/js/main.js` (resulting in HTTP 404); always use root-relative paths (`/js/main.js?v=...`).
- **Escaped Quotation Marks in Programmatic Replacements:** Escaping double quotes inside replacement strings during automated regex passes injects literal quotes into HTML attributes (`href="\"https...\""`), breaking external navigations.
- **Unconstrained Brand Logo in Shared Footers:** Referencing high-resolution master logos without `.footer-brand img { height: 38px; }` CSS constraints results in oversized logos dominating the layout on standalone subpages.
- **Animation Opacity Lock (`.slide-up` with `opacity: 0`):** Adding animation classes that rely on scroll-triggered `IntersectionObserver` to newly injected grid containers causes them to remain invisible if the trigger does not fire; enforce `opacity: 1 !important; visibility: visible !important;` on dynamically filtered grids.
- **Stale Contact Links Across Subpages:** Updating the primary homepage WhatsApp button while forgetting secondary product pages leaves dead or wrong numbers on high-intent conversion funnels; always batch-update all HTML templates via automated script.
- **FTP Timeout on Shared Hosting:** Leaving FTP sessions open between image processing steps causes silent disconnects; connect right before transfer and close immediately.
