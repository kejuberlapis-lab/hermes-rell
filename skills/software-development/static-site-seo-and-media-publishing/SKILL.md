---
name: static-site-seo-and-media-publishing
description: "Use when publishing SEO blog articles and media pipelines."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [seo, yoast, static-sites, analytics, json-ld, sitemap, meta-tags, mobile-ux, copywriting, blog-publishing, media-pipeline, lanczos, light-theme]
---

# Static Site SEO, Media Enhancement, & End-to-End Blog Publishing Pipeline

A class-level operational guide for converting raw visual assets into high-definition 16:9 banners, authoring Yoast-standard & GEO-optimized educational and commercial articles, synchronizing multi-page blog indexes and XML sitemaps, deploying live via FTP to cPanel/LiteSpeed servers, and maintaining unified web analytics across static websites.

## When to Use

- When transforming raw photos or user attachments into web-optimized 16:9 HD banners (Lanczos upscale + unsharp mask) and publishing full-featured SEO/GEO blog posts.
- When applying Yoast SEO standards (title tag formulas, calibrated meta descriptions, OpenGraph, Twitter Cards, robots directives) across multi-page static websites and blogs.
- When generating, updating, and synchronizing `blog.html` grid cards and `sitemap.xml` canonical URL entries.
- When writing GEO (Generative Engine Optimization) content with direct key-takeaway answer blocks, structured feature cards, and comparative matrix tables.
- When deploying static files directly to production hosting (cPanel/FTP) and verifying live rendering via headless browser inspection.

## Procedure

1. **Visual Asset Optimization & 16:9 Banner Generation:**
   - Take raw source images (e.g. photos of workshops, hardware, installations).
   - Use ffmpeg Lanczos filter + unsharp masking to upscale and enhance clarity:
     `ffmpeg -y -i input.jpg -vf "scale=2560:1440:flags=lanczos,unsharp=5:5:0.8:5:5:0.0" output_hd.png`
   - Optimize down to standard high-resolution 16:9 web banner (`1200 x 675 px`) for fast web loading and crisp mobile display.
   - Upload asset directly to `public_html/images/`.

2. **Yoast-Standard Metadata & Social Stack Calibration:**
   - **Title Tag Formula (50–60 Chars):** `[High-Intent Keyphrase] - [Brand / Segment]`
   - **Meta Description (145–160 Chars):** High-intent value summary with action-driven vocabulary.
   - **Modern Robots Directive:** `<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">`
   - **Canonical Tag:** `<link rel="canonical" href="https://domain.com/blog/article-slug.html">`
   - **OpenGraph & Twitter Cards:** Full metadata stack referencing the 1200x675px banner.

3. **Schema.org JSON-LD Structured Data Injection:**
   - Inject `BreadcrumbList` navigation schema (Beranda -> Solution/Blog -> Article Title).
   - Inject `Article` / `BlogPosting` schema with headline, description, author organization, publisher logo, `datePublished`, and `dateModified`.

4. **GEO-Optimized Article Architecture:**
   - **Hero Header:** Topic badge, bold H1 headline, author, publication date, and reading time.
   - **Direct Answer Callout Box ("Jawaban Cepat / Key Takeaway"):** Positioned immediately below the featured banner to maximize AI search snippet extraction (ChatGPT Search, Google Gemini, Perplexity).
   - **Structured 4-Pillar Benefit Cards:** Clean UI cards with distinct icons, bold headers, and concise descriptions.
   - **Comparative Analysis Table:** Structured `<table>` contrasting conventional/passive methods against active technological solutions.
   - **Hardware Cross-Linking:** Natural contextual links to related core products (e.g. Interactive Flat Panels or Video Walls).
   - **High-Converting WhatsApp CTA Banner:** Pulsating WhatsApp consultation button with pre-filled message intent.

5. **Multi-Page Index & Sitemap Synchronization:**
   - **Blog Index Update (`public_html/blog.html`):** Insert the new article card into the featured grid with category badge, formatted date, excerpt, and "Baca Selengkapnya" link.
   - **Sitemap XML Update (`public_html/sitemap.xml`):** Append the new `<url>` entry with priority `0.85` and current `<lastmod>YYYY-MM-DD</lastmod>`.

6. **Production Deployment & Browser Verification:**
   - Deploy all updated files (`.png`, article `.html`, `blog.html`, `sitemap.xml`) via FTP to `public_html/`.
   - Perform live headless browser navigation to the published article URL and blog index to verify DOM integrity, CSS styling, and visual rendering.

## Pitfalls

- **Publishing Articles Without Updating Blog Index or Sitemap:** Creating an isolated HTML file under `/blog/` without adding its preview card to `blog.html` and its URL to `sitemap.xml` leaves the content orphaned and undiscoverable.
- **Unoptimized Raw Image Uploads:** Uploading uncompressed or low-resolution raw images creates slow page load times and blurry hero previews on high-DPI displays; always run Lanczos upscale + unsharp filter and resize to standard 16:9 (`1200x675px`).
- **Relative Script Paths in Subdirectories:** Using `<script src="js/analytics.js">` in nested directories like `/blog/*.html` leads to HTTP 404 errors; always use root-relative paths (`/js/analytics.js?v=...`).
- **Dense Unformatted Mobile Text Walls:** Leaving plain text bullet points without card containers or visual separation causes high mobile bounce rates; convert all key features into structured highlight cards.
