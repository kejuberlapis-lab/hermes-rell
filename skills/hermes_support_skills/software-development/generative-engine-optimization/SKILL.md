---
name: generative-engine-optimization
description: Optimize web content for AI search and LLM citations.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [geo, ai-search, chatgpt-search, gemini-citations, perplexity, rag, seo, google-search-console]
---

# Generative Engine Optimization (GEO) & AI Citation Architecture

A class-level guide for authoring, structuring, and auditing web content to maximize discovery, retrieval, and direct citation by AI search engines (ChatGPT Search, Google Gemini, Perplexity AI, Microsoft Copilot) and search crawlers via Retrieval-Augmented Generation (RAG).

## When to Use

- When writing or editing commercial solution pages, product descriptions, or educational blog posts intended to serve as authoritative reference sources for AI search queries.
- When structuring technical comparison matrices, product specifications, or enterprise buying guides.
- When configuring technical SEO assets (`sitemap.xml`, `robots.txt`, `llms.txt`, IndexNow) and search console verification.

## Procedure

1. **Direct Answer Architecture (The 3-Sentence Rule):**
   - Place an immediate, definitive synthesis answering the primary query or product category within the first 2–3 sentences.
   - Avoid generic preamble ("In today's fast-paced digital era..."); start directly with definitions, operational thresholds, and core distinguishing parameters.

2. **Factual & Technical Parameter Tables:**
   - Always format specifications into Markdown/HTML tables (`<table>` or Markdown pipe tables).
   - Label columns and rows unambiguously so zero-shot LLM table parsers can quote exact figures without confusion.

3. **Conversational Problem-Oriented Headings (H2 / H3):**
   - Frame subheadings as natural-language questions enterprise procurement managers and buyers ask (e.g. *"Berapa Jarak Pandang Ideal untuk Videotron P2.5 Indoor?"*).
   - Follow each heading with a concrete calculation formula, rule of thumb, or verified standard.

4. **DOM Cleanliness & Unobstructed Content Rendering:**
   - Ensure all body text, specification tables, and FAQ cards are immediately present in the DOM with default `opacity: 1`.
   - Never gate textual content behind fragile JavaScript scroll animations that render invisible to headless web scrapers.

5. **The `llms.txt` & AI Crawl Manifest Standard:**
   - Host a clean, structured Markdown manifest at `/llms.txt` outlining brand definitions, core capabilities, subscription tiers, and canonical URLs for fast ingestion by LLM crawlers (ChatGPT, Perplexity, Claude, Gemini).

6. **IndexNow & Instant Multi-Engine Notification:**
   - Deploy a 32-character key at `/{key}.txt` and post an IndexNow JSON payload (`host`, `key`, `keyLocation`, `urlList`) to `https://api.indexnow.org/indexnow` to bypass crawl lag and trigger near-instant discovery on Bing, Yandex, and partner networks.

7. **Rich JSON-LD Multi-Type Schema (`@graph`):**
   - Inject structured JSON-LD data combining `SoftwareApplication` (pricing, ratings), `Organization` (brand identity, official bot links), and `FAQPage` (featured snippets).

8. **Google Search Console Verification Setup:**
   - Deploy the specific static HTML verification file (e.g. `google[hash].html`) returning exact verification text.
   - Also add `<meta name="google-site-verification" content="...">` in `<head>` for dual verification.

## Pitfalls

- **Wildcard Verification Soft-404 / Cloaking Trigger:** Never implement dynamic catch-all routes (e.g. `/google{id}.html` returning 200 for any random ID). Google's automated security scanners test random non-existent verification filenames; returning 200 for fake files triggers false-positive "Site appears to have been hacked" warnings. Only serve the exact verification file and return strict HTTP 404 for random non-existent files.
- **Initial Sitemap Pending Queue Delay:** On freshly submitted sitemaps, Google Search Console UI temporarily displays "Tidak dapat mengambil peta situs" / "Jenis: Tidak diketahui" before the Googlebot crawler completes its first scheduled fetch pass. Do not treat this queue latency as a server failure if `curl` confirms a valid HTTP 200 XML response.
- **Vague Fluff Copy:** Using purely emotional marketing adjectives without concrete numbers prevents AI models from identifying the page as an authoritative technical reference.
