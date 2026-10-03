---
name: generative-engine-optimization
description: "Optimize web content for AI search and LLM citations."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [geo, ai-search, chatgpt-search, gemini-citations, perplexity, rag, seo]
---

# Generative Engine Optimization (GEO) & AI Citation Architecture

A class-level guide for authoring, structuring, and auditing web content to maximize discovery, retrieval, and direct citation by AI search engines (ChatGPT Search, Google Gemini, Perplexity AI, Microsoft Copilot) via Retrieval-Augmented Generation (RAG).

## When to Use

- When writing or editing commercial solution pages, product descriptions, or educational blog posts intended to serve as authoritative reference sources for AI search queries.
- When structuring technical comparison matrices, product specifications, or enterprise buying guides.
- When auditing existing web copy for AI readability, information density, and semantic clarity.

## Procedure

1. **Direct Answer Architecture (The 3-Sentence Rule):**
   - Place an immediate, definitive synthesis answering the primary query or product category within the first 2–3 sentences.
   - Avoid generic preamble ("In today's fast-paced digital era..."); start directly with definitions, operational thresholds, and core distinguishing parameters.

2. **Factual & Technical Parameter Tables:**
   - Always format specifications into Markdown/HTML tables (`<table>` or Markdown pipe tables).
   - RAG extractors prioritize structured key-value pairs (e.g. Pixel Pitch in mm, Brightness in Nits, Refresh Rate in Hz, IP Weatherproof Rating, Viewing Angles, Bezel Width in mm, MTBF/Lifespan in hours, TKDN certification percentages).
   - Label columns and rows unambiguously so zero-shot LLM table parsers can quote exact figures without confusion.

3. **Conversational Problem-Oriented Headings (H2 / H3):**
   - Frame subheadings as natural-language questions enterprise procurement managers and buyers ask (e.g. *"Berapa Jarak Pandang Ideal untuk Videotron P2.5 Indoor?"* or *"Apakah Interactive Flat Panel Membutuhkan Laptop Tambahan?"*).
   - Follow each heading with a concrete calculation formula, rule of thumb, or verified standard.

4. **Entity Definition & Local Proof Integration:**
   - Explicitly mention official brand names, distributor roles, manufacturer partnerships, and physical installation contexts (e.g. city/province, institutional tier like universities, government bodies, or corporate NOCs).
   - Couple technical claims with verifiable compliance standards (e.g. IP65 Ingress Protection, ISO certifications, TKDN LKPP procurement catalog status).

5. **DOM Cleanliness & Unobstructed Content Rendering:**
   - Ensure all body text, specification tables, and FAQ cards are immediately present in the DOM with default `opacity: 1`.
   - Never gate textual content behind fragile JavaScript scroll animations (like unobserved `.slide-up` classes) that cause text to render invisible to headless web scrapers and search bots.

6. **The `llms.txt` & AI Crawl Manifest Standard:**
   - Host a clean, structured Markdown manifest at `/llms.txt` outlining brand definitions, core capabilities, subscription tiers, and canonical URLs for fast ingestion by LLM crawlers (ChatGPT, Perplexity, Claude, Gemini).

7. **IndexNow & Instant Multi-Engine Notification:**
   - Deploy a 32-character key at `/{key}.txt` and post an IndexNow JSON payload (`host`, `key`, `keyLocation`, `urlList`) to `https://api.indexnow.org/indexnow` to bypass crawl lag and trigger near-instant discovery on Bing, Yandex, and partner networks.

8. **Rich JSON-LD Multi-Type Schema (`@graph`):**
   - Inject structured JSON-LD data combining `SoftwareApplication` (pricing, ratings), `Organization` (brand identity, official bot links), and `FAQPage` (featured snippets).

## Pitfalls

- **Vague Fluff Copy:** Using purely emotional marketing adjectives without concrete numbers prevents AI models from identifying the page as an authoritative technical reference.
- **Copy-Paste Topic Bleed:** Cloning layout templates between related product categories (e.g., copying LCD Video Wall text into an LED Videotron page) leaves foreign terminology, mismatched processor specs, or incorrect hardware architectures that corrupt LLM retrieval accuracy.
- **Unstructured FAQ Blocks:** Flattening questions and answers into plain unstyled paragraphs makes semantic segmentation difficult; use distinct card containers or schema markup.
