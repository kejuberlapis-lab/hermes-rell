---
name: search-engine-indexing-and-geo
description: Use when setting SEO. Implements IndexNow, GSC, & GEO.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [seo, indexnow, google-search-console, geo, llms-txt, sitemap]
---

# Production Search Engine Indexing & GEO Standards

Standard operating procedure for deploying instant multi-search engine indexing (Google, Bing, Yandex), structured data for AI search crawlers (GEO), and ownership verification without security triggers.

## When to Use

- When launching or updating web domains, SaaS landing pages, or multi-page websites.
- When configuring Google Search Console (GSC) verification, IndexNow protocol, or XML sitemaps.
- When authoring AI crawler manifests (`llms.txt`) and Rich JSON-LD schemas.

## Step-by-Step Procedure

1. **Deterministic XML Sitemap & Robots.txt:**
   - Generate a valid XML sitemap (`/sitemap.xml`) with correct namespace `http://www.sitemaps.org/schemas/sitemap/0.9`, priority rankings (`1.0` homepage, `0.9` pricing/skills, `0.8` subpages), and `lastmod` dates.
   - Configure `/robots.txt` allowing all legitimate user agents (`User-agent: *`, `Allow: /`) and pointing explicitly to `Sitemap: https://<domain>/sitemap.xml`.

2. **IndexNow Instant Multi-Engine Submission:**
   - Generate a unique 32-character hexadecimal key.
   - Serve the raw key as plain text at `/<key>.txt`.
   - Post a JSON payload (`host`, `key`, `keyLocation`, `urlList`) to `https://api.indexnow.org/indexnow` with header `Content-Type: application/json; charset=utf-8`. Expect `HTTP 202 Accepted`.

3. **Generative Engine Optimization (GEO) Manifest (`llms.txt`):**
   - Serve a structured Markdown file at `/llms.txt` defining the service entity, official bot handles, full division capabilities, pricing tiers, and canonical route mappings.
   - Ensure the definition is concise, unambiguous, and quantitative so LLM retrieval agents (ChatGPT Search, Perplexity, Gemini) extract facts accurately.

4. **Multi-Entity JSON-LD Schema (`@graph`):**
   - Inject structured JSON-LD in `<head>` combining `SoftwareApplication` (offers, pricing, ratings), `Organization` (brand logo, social handles), and `FAQPage` (high-intent Q&A for featured snippets).

5. **Google Search Console Ownership Verification:**
   - Serve the exact static verification file (e.g. `/google<hash>.html`) returning `google-site-verification: google<hash>.html` with `Content-Type: text/html`.
   - Simultaneously inject `<meta name="google-site-verification" content="google<hash>">` into the homepage `<head>` as a dual verification fail-safe.

## Critical Pitfalls

- **Wildcard Verification Soft-404 / Cloaking Trigger:** Never create catch-all dynamic routes (e.g., `/google{id}.html` returning 200 for any random string). Google automated security probes test random fake filenames; returning 200 for nonexistent verification files causes GSC to reject verification with a false-positive "site appears to have been hacked" security alert. Always return strict HTTP 404 for nonexistent verification routes.
- **Initial Sitemap Pending Queue Delay:** Brand new sitemap submissions in GSC temporarily display "Tidak dapat mengambil peta situs" / "Jenis: Tidak diketahui" while queued before Googlebot completes its first crawler run. If `curl` confirms HTTP 200 XML with valid syntax, do not repeatedly re-submit.
- **Staggered Container Alignment on Sibling Sections:** Do not mix mismatched container widths (e.g., `max-w-6xl` banner stacked against `max-w-5xl` grid). Maintain uniform container boundaries and consistent margins (`mt-12 mb-16`) across sibling sections.
