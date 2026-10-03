# Mitsindo Visual Pratama - Company Profile Redesign

## Project Info
- **Company**: PT Mitsindo Visual Pratama (AV Integrator, est. 2005)
- **Stack**: Bootstrap 5.3 CDN + Custom CSS + Swiper.js + Boxicons + Inter font
- **Color**: Navy #0a1628 (primary), Orange #e85d04 (CTA)
- **URL**: http://43.134.179.61:8081
- **Original site**: mitsindo.co.id (all subpages 404, only homepage worked)

## File Structure
```
mitsindo-redesign/
├── index.html          (24.5KB) — Homepage
├── tentang.html        (15.4KB) — About Us
├── produk.html         (15.0KB) — Products & Services (6 categories)
├── portofolio.html     (11.2KB) — Portfolio (8 projects + filter)
├── kontak.html         (11.1KB) — Contact (form + office info)
├── css/style.css       (25.9KB) — Custom styles + responsive
├── js/main.js          (4.5KB)  — Navbar, Swiper, filter, counters
└── images/
```

## Key Lessons
1. **Mobile spacing**: Original CSS had `padding: 5rem 0` on all sections with NO media queries. User complained "bnyak space kosong". Fixed by adding responsive padding: mobile=2.5rem, tablet=3.5rem, desktop=5rem.
2. **Port conflict**: Port 8080 was occupied by topengdwimakmur. Used 8081 instead.
3. **Subagent delegation**: Built 5 pages + CSS + JS via single `delegate_task`. Subagent wrote all files in ~9 minutes. Post-delegation manual CSS patch needed for mobile spacing.
4. **Original site issues**: All subpage links (tentang.html, produk.html, etc.) returned 404. Company effectively had a single-page site masquerading as multi-page.

## Design Pattern
- Sticky navbar with scroll shadow
- Dark navy hero with orange CTA buttons
- Product cards with hover effects
- Swiper.js carousel for portfolio
- Accordion FAQ
- WhatsApp floating button
- 4-column dark footer
