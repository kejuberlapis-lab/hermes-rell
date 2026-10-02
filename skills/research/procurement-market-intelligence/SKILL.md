---
name: procurement-market-intelligence
description: "Extract public procurement, vendor, and pricing data."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: research
    tags: [procurement, inaproc, lkpp, e-katalog, tkdn, vendor-scraping, pricing-matrix, market-research]
    related_skills: [blocked-page-recovery, xlsx, grounded-citations]
---

# Procurement Market Intelligence & Vendor Data Mining

A class-level operational skill for researching, scraping, and compiling structured vendor directories, product catalogs, price benchmarks, and regulatory compliance records from public procurement portals (e.g. INAPROC, LKPP E-Katalog, LPSE) and national manufacturing registries (e.g. TKDN / P3DN).

## When to Use

- When building competitive intelligence or vendor lists for B2B/B2G hardware, AV systems, IT infrastructure, or government tenders.
- When extracting catalog items, pricing tiers, and vendor contact info from protected public procurement platforms.
- When compiling and structuring multi-region/provincial supplier databases across all 514 Kabupaten/Kota into styled `.xlsx` workbooks and `.csv` datasets.
- When resolving access blocks on governmental e-procurement platforms where direct scraping triggers Cloudflare/WAF bot interstitials.
- When processing multi-page saved HTML batches or user-uploaded ZIP archives containing hundreds of catalog search results.
- When auditing the validity and provenance of public procurement data models and guaranteeing zero duplicate records for stakeholders.

## Procedure

1. **Access Strategy & WAF Bypass Ladder:**
   - **Direct API Check:** Check if the platform provides an Open Data API (e.g. `data.inaproc.id/api/v1/...`). Verify if public bearer tokens or IP whitelisting are required.
   - **SERP Indexing Pivot:** When portals enforce strict Cloudflare WAF blocks (`403 Forbidden` / "Akses Ditolak") on automated scrapers, pivot to search engine indices:
     ```
     site:<portal-domain> "<product keyword>" "<region/province>"
     site:katalog.inaproc.id "<brand>" OR "<product>"
     ```
   - **Regulatory Mirror Registries:** E-procurement platforms require statutory compliance certificates. Query public regulatory registries (e.g. Ministry of Industry TKDN/P3DN databases, certification bodies) to reconstruct full vendor legal entities, factory locations, brand ownerships, and certified local content percentages without hitting protected catalog endpoints.

2. **Complete 514 Regency/City Territorial Taxonomy:**
   - When generating nationwide procurement market intelligence for Indonesia, map all **514 Kabupaten & Kota across all 38 Provinces** (416 Kabupaten + 98 Kota) systematically from Aceh to Papua Barat Daya.
   - Separate national principal Tier-1 distributors (concentrated in Jakarta, Surabaya, Bandung, Medan, Makassar) from local regional dealers and micro-enterprises (UMKM / CV daerah) who execute local LPSE tenders and DAK Fisik school deliveries.

3. **Data Model, Multi-Category Aggregation & Grand Master Architecture:**
   - When extracting multi-page catalog datasets across multiple related domains/categories (e.g. IFP, Video Wall, LED Videotron):
     - **Category-Level Workbooks (Dual-Sheet):**
       - **Sheet 1:** Category-specific Unique Vendors (1 row = 1 unique company, zero duplicates).
       - **Sheet 2:** Category-specific Granular Product SKU Listings (all variants, screen sizes, pixel pitches).
     - **Grand Master Multi-Sector Workbook (Tri-Category / Multi-Sheet):**
       - **Sheet 1 (Grand Master Vendors):** Consolidates all unique vendors across all sectors into a single master registry (e.g. 839 unique vendors across IFP, Video Wall, Videotron). Columns: `No`, `Nama Vendor / CV / PT`, `Provinsi`, `Kabupaten / Kota`, `Kategori Produk yang Dijual` (comma-separated), `Brand Utama`, `Total Listing`, `Listing IFP`, `Listing Video Wall`, `Listing Videotron`, `Tautan Toko Resmi INAPROC`.
       - **Sheets 2, 3, 4:** Category-specific granular SKU listing sheets with color-coded headers (Emerald for IFP, Navy for Video Wall, Indigo for Videotron).
     - **Focused Vendor & Active Category Mapping View:** When stakeholders require a simplified, executive view stripped of granular SKU noise:
       - Format 1 row per unique vendor with structured active category strings: `Interactive Flat Panel (N) • Video Wall (N) • Videotron (N)`.
       - Include: `No`, `Nama Vendor / CV / PT`, `Kategori Produk yang Tayang di INAPROC`, `Provinsi`, `Kabupaten / Kota`, `Total Produk`, and direct clickable `Tautan Toko INAPROC` (`https://katalog.inaproc.id/<merchant-slug>`). Ensure zero duplicates across all rows.

4. **Source Transparency & Data Integrity Disclosure (Strict Anti-Hallucination):**
   - **Never Fabricate or Synthesize Fictitious Entities:** When requested for large-scale geographic supplier directories (e.g., covering 514 regencies), NEVER invent templated or synthetic company names (e.g. `CV <Kota> Media Visual`) to satisfy coverage quotas. An agent must only output 100% verified legal entities that possess real digital footprints, official store slugs, or government certification records. If live coverage is limited by access controls, explicitly state the verified sample count rather than extrapolating dummy records.
   - **Client-Side Extraction Options for Gated Portals:** When portals enforce Cloudflare WAF/session auth, offer practical in-session tools:
     - **Saved HTML Parsing (`Ctrl+S`) & Batch ZIP Ingestion:** Parse single or batch `.zip` archives containing multi-page saved HTML files using BeautifulSoup to extract merchant slugs (`/merchant-slug/product-slug`), product titles, locations, prices, and TKDN metrics.
     - **In-Browser Auto-Crawler:** Provide a client-side JavaScript snippet for the user's authenticated DevTools Console / Bookmarklet that loops through search pagination (`fetch('/search?keyword=...&page=N')`) with `DOMParser`, polite delays (500–800ms), live floating progress UI, and direct CSV blob download.
     - **Console Self-XSS Clearance:** Instruct users to manually type `allow pasting` in DevTools Console if browser paste protection blocks script execution.
     - Developer API Bearer token integration.
   - Always classify and disclose data provenance to users:
     - **Verified Primary Entities:** Principal manufacturers, primary TKDN certificate holders, and official national E-Katalog catalog stores.
     - Provide concrete, verifiable public verification paths:
       - Portal LPSE: `http://lpse.[namakabupaten]kab.go.id` (Cari Paket Lelang / Pengadaan Langsung).
       - E-Katalog LKPP: `https://e-katalog.lkpp.go.id/` (Etalase Peralatan IT & Komoditas DAK Fisik).
       - Toko Daring LKPP: Mitra Bela Pengadaan (Mbizmarket, PaDi UMKM, KlikMRO).

5. **Document & Identity Card Image Enhancement for Procurement/Tender Verifications:**
   - When processing low-resolution tender submissions, tax IDs (NPWP), or director identity cards (KTP):
     - Upscale 4X with high-order Lanczos interpolation.
     - Apply weak deblocking / subtle bilateral smoothing before unsharp masking to prevent amplifying JPEG ringing and noise.
     - Generate both full enhanced views and high-contrast text-optimized crops.
     - Accompany visual deliverables with a complete, structured text transcription of all identity and registration fields for error-free verification.

6. **Structured Multi-Format Spreadsheet & Report Generation:**
   - **CSV Export:** Generate standardized UTF-8 encoded `.csv` for CRM, database seeding, and programmatic imports.
   - **Styled Excel (.xlsx) Generation:** Build formatted Excel workbooks using Python `openpyxl` with:
     - Dark navy headers (`#1F4E79`) with white bold text.
     - Zebra striping (`#F2F5F9`) on alternate data rows.
     - Center alignment on status and scale columns; left alignment with text-wrapping on multiline descriptions.
     - Explicit column widths and top freeze pane (`ws.freeze_panes = "A5"`) on header rows.
   - **Markdown Knowledge Base Sync:** Export a companion Markdown summary to the workspace/Obsidian vault for persistent reference.

## Pitfalls

- **Conflating Total SKU Listings with Unique Vendor Counts:** Presenting a multi-product catalog table (e.g. 725 product SKUs) as "725 vendors" causes severe confusion when users search for duplicates; always structure output with a dedicated single-row-per-vendor sheet (e.g. 312 unique vendors) alongside the granular SKU listing.
- **Omitting Local UMKM Suppliers in Procurement Bidding Analysis:** Focusing only on national Tier-1 principals overlooks the 40%+ statutory budget allocation for local micro/small enterprises (UMKM / CV daerah) who execute the actual purchasing and installation on regional government projects.
- **Unverified Reseller Entities vs Primary TKDN Holders:** Confusing secondary sub-distributors with primary TKDN certificate holders; always verify the primary manufacturer or exclusive import license holder in official certification databases.
- **Relying Solely on Direct HTTP GET on WAF-Gated Portals:** Direct scraping of government catalog URLs frequently returns Cloudflare 403 blocks; failing to fall back to search engine cache/SERP indices or regulatory registries halts data gathering prematurely.
- **Conflating Area Pricing with Unit Pricing:** Mixing up per-square-meter (`/m²`) pricing on modular LED Videotron with fixed-unit display pricing on Interactive Flat Panels or Video Wall screens corrupts financial estimates.
- **Unadjusted Regional Pricing:** Comparing Jakarta ex-factory prices with remote regional tenders (e.g. Papua, Maluku) without factoring in shipping, heavy structural rigging, and on-site engineering leads to inaccurate price benchmarking.
- **Failing to Disclose Synthetic Network Mapping vs Live Scraped Data:** Presenting regional distribution network mappings as live realtime-scraped server databases damages credibility; always state data provenance, primary verified cores, and verification steps clearly.
- **Synthesizing Fictitious Company Names to Meet Scale Quotas:** Generating placeholder company names (e.g., `CV <City> Media Visual`) when large-scale data cannot be scraped directly produces hallucinated records that fail verification; keep directories strictly limited to verified entities with verifiable URLs/handles.
- **Unsharp Masking Compressed Documents Without Pre-Smoothing:** Applying strong sharpening filters directly to low-resolution JPEG/document scans amplifies compression ringing and noise artifacts around text; always apply subtle deblocking/bilateral smoothing before sharpening and pair with manual text transcription.
