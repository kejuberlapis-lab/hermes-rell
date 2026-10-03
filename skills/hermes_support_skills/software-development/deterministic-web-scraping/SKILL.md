---
name: deterministic-web-scraping
description: Use when scraping web data. Enforces deterministic proof.
---

# Deterministic Zero-Hallucination Web Scraping & Data Extraction

Standar operasional mutlak untuk scraping, ekstraksi data web, dan crawling tanpa risiko halusinasi. Melarang keras pembuatan data sintetis/palsu dan mewajibkan bukti audit fisik.

## 6 Protokol Anti-Halusinasi Scraping
1. **Larang Keras Data Sintetis:** Jika ekstraksi gagal (403, 429, Cloudflare, selector kosong), wajib lapor gagal secara jujur. Dilarang mengarang baris tiruan.
2. **Raw Response Dump:** Simpan payload mentah (HTML/JSON) ke file disk sebelum proses parsing dilakukan.
3. **Deterministic Parser:** Gunakan Playwright, BeautifulSoup, atau lxml berbasis DOM selector nyata.
4. **Provenance Metadata:** Setiap baris data wajib memiliki metadata asal (`_source_url`, `_scraped_at`, `_dom_selector`).
5. **Zero-Result Alert:** Jika jumlah baris yang ditemukan adalah 0, lempar status `FAILED: 0 MATCHED`, jangan isi dengan data tebakan.
6. **Physical Verification Gate:** Tampilkan bukti eksekusi riil (jumlah baris `wc -l`, sampel 3 baris teratas `head`, dan path file fisik).
