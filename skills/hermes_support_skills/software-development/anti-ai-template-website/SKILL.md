---
name: anti-ai-template-website
description: Anti-AI template rules untuk website design.
---

# Anti-AI Template Website Design

## Kapan Dipakai
- User minta redesign website dan komplain "terlihat kayak template AI"
- User minta website company profile / contractor / engineering
- User minta website dengan Bootstrap 5

## AI Template Tells yang HARUS Dihindari

### 6. Mobile Spacing Overdo
❌ Section padding `5rem 0` (80px) tanpa media query → terlalu banyak space kosong di mobile
✅ WAJIB tambah media query: mobile ≤768px → `padding: 2.5rem 0`, tablet ≤992px → `padding: 3.5rem 0`

### 1. Multi-Color Text di Headline
❌ `Kontraktor <span style="color:yellow">Mekanikal</span> & <span style="color:yellow">Elektrikal</span>`
✅ `Kontraktor Mekanikal & Elektrikal` (seragam warnanya)

### 2. Glassmorphism Nav Overdo
❌ `backdrop-filter: blur(20px); background: rgba(255,255,255,0.1);`
✅ Transparent navbar → solid on scroll

### 3. 3 Equal Cards
❌ 3 `col-md-4` cards identik
✅ Bento grid atau asymmetric layout

### 4. AI Purple/Blue Gradient
❌ `linear-gradient(135deg, #667eea, #764ba2)`
✅ Solid color atau foto asli

### 5. Fade-in Semua Elemen
❌ Animasi smooth di setiap elemen
✅ Animasi yang motivated

### 7. Low Contrast Dark Mode & Missing Glyph Tells
❌ Teks muted/abu-abu gelap (`#8b949e`, `text-muted`) pada card gelap (`#161b22`, `#0b0f17`) sehingga tulisan menyatu/tidak terbaca
✅ WAJIB high-contrast typography di dark theme: background `#0b0f17` / `#131a26` memakai text `#ffffff` (utama) dan `#cbd5e1` / `#94a3b8` (sub-label/subtle).
❌ Menggunakan emoji mentah (`🔥`, `🟢`, `🔴`, `🟡`) untuk status badge di server yang menyebabkan rendering kotak hilang (*tofu box* `⯐`)
✅ Gunakan icon library resmi (Bootstrap Icons `bi-fire`, `bi-check-circle-fill`, `bi-lightning-charge-fill`, dll.) dipadu badge semi-transparan dengan border outline kontras.

### 8. Long Scroll & Truncated Scorecard Numbers (Compact Workspace UX)
❌ Membuat halaman dashboard vertikal panjang yang memerlukan scroll ke bawah berulang kali.
✅ Gunakan **Nav Tab Filter** modular (*Performance Overview, AI Audit, Campaign Matrix, Leads CRM*) sehingga seluruh ringkasan KPI dan chart muat dalam 1 layar penuh (*single viewport*).
❌ Membiarkan teks mata uang besar terpotong elipsis (`Rp 17.21...`) atau membungkus baris secara tidak simetris pada scorecard sempit.
✅ Format angka besar secara ringkas (`Rp 17.21 Jt` / `Rp 73.54 Jt` / `1.42 M`) dengan `white-space: nowrap` dan sematkan nominal lengkap pada atribut `title` (hover tooltip). Sub-label di bawah kartu wajib menggunakan warna kontras terang (`#cbd5e1` / `#94a3b8`).

### 9. Inline JavaScript HTML Template String Collisions
❌ Menyematkan tanda petik satu mentah (`\'`) di dalam inline handler HTML template string JavaScript Node.js/Python (e.g. `onclick="handler(\'${id}\')"`), yang berisiko memecah parsing browser dan memicu `SyntaxError` tersembunyi sehingga `fetchState()`/render loop macet total.
✅ Gunakan entitas HTML baku (`&quot;`) untuk membungkus string argumen dalam inline handler: `onclick="handler(&quot;${id}&quot;)"` atau gunakan `addEventListener` terpisah.

### 10. Multi-Slot Dynamic Telemetry (Zero Empty State Flash)
❌ Membiarkan container data dinamis berkedip kosong saat render awal sebelum JavaScript fetching selesai.
✅ Pre-render card telemetri / status default langsung dari sisi server pada HTML awal agar klien langsung melihat data live tanpa menunggu script selesai dieksekusi.

### 11. High-Contrast Light Theme & Typography Standards
❌ Teks muted, abu-abu tipis, atau font yang samar di atas background putih/abu-abu yang menyebabkan user kesulitan membaca data.
✅ Gunakan palet **High-Contrast Clean Light**:
  - Headings/Judul: Deep Charcoal (`#111827`)
  - Body/Data Angka: Dark Slate (`#374151`)
  - Sub-label/Muted: Neutral Slate (`#6b7280`)
  - Card & Container: `#ffffff` dengan border `#e5e7eb`
  - Chart Theme: Selalu eksplisit set `theme: { mode: 'light' }` pada ApexCharts/Chart.js dengan axis label kontras `#6b7280`.

### 12. Document & Print Layout Standards (Zero Horizontal Scroll & High Contrast Print)
❌ Dokumen / tabel cetak (SPPD, Invoice, Slip Gaji) memiliki scroll horizontal kiri-kanan pada layar desktop/mobile, garis tabel abu-abu samar yang hilang saat diprint, atau watermark stempel yang terlalu besar sehingga menutupi tanda tangan.
✅ WAJIB terapkan:
  - **Zero Horizontal Scroll**: Set `overflow-x: hidden !important; max-width: 100vw;` secara global dan gunakan container berbatas (`max-width: 820px; width: 100%`) agar konten hanya di-scroll vertikal (atas-bawah).
  - **Crisp Black Print Tables**: Garis border tabel dokumen/invoice wajib hitam pekat (`border: 1px solid #000; border-collapse: collapse;`) dengan `border: 1.5px solid #000` pada kontainer terluar dan `@media print` penegasan warna hitam 100% ink.
  - **Proportional Stamp Watermarks**: Watermark approval digital dibuat ringkas (`font-size: 7pt`, padding `2px 8px`, border `1.5px solid #16a34a`, background transparan `rgba(240,253,244,0.75)`, rotasi `-7deg`) sehingga proporsional dan tidak menenggelamkan teks/nama pejabat penandatangan.

## Architecture Guide: Digital Marketing & Social Media Agency App
Referensi lengkap repositori open-source GitHub terkemuka (Hootsuite/Buffer open-source alternatives, campaign manager, ad hubs) tersedia di: [digital-marketing-agency-apps-guide.md](references/digital-marketing-agency-apps-guide.md).
- **Multi-Client Isolation**: Workspace dengan sidebar switcher per brand klien.
- **Real Scraping**: Gunakan `yt-dlp` + `BeautifulSoup` untuk ekstraksi data konten real-time tanpa data mockup/palsu.

## Pattern Premium untuk Corporate

### Transparent Navbar
```html
<header class="site-header" id="siteHeader">
  <nav class="navbar navbar-expand-lg transparent-nav">
    <div class="container">
      <a class="navbar-brand" href="#">
        <img src="images/logo.svg" alt="Brand" style="height:40px">
        <span class="brand-name">Brand Name</span>
      </a>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav mx-auto">
          <li class="nav-item"><a class="nav-link" href="#section">MENU</a></li>
        </ul>
        <a href="#contact" class="btn-pill-cta">HUBUNGI KAMI</a>
      </div>
    </div>
  </nav>
</header>
```

### Scroll Effect
```javascript
window.addEventListener('scroll', function() {
    var header = document.getElementById('siteHeader');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});
```

```css
.transparent-nav { background: transparent; transition: all 0.3s ease; }
.site-header.scrolled .transparent-nav { background: var(--primary); box-shadow: 0 4px 30px rgba(0,0,0,0.15); }
```

## Download Gambar dari Website Lain
Referensi project sebelumnya: [topengdwimakmur](references/topengdwimakmur-project.md), [mitsindo](references/mitsindo-project.md)
```bash
mkdir -p images
curl -sO https://example.com/logo.svg
curl -sO https://example.com/hero.webp
curl -sO https://example.com/dealer-logo.png
```

### Cara Ambil Semua Gambar dari Website
1. `browser_navigate` ke website sumber
2. `browser_get_images` → dapat semua URL gambar
3. `browser_console` untuk background images:
   ```javascript
   document.querySelectorAll('[style*="background"]').forEach(el => {
       const bg = el.style.backgroundImage;
       if (bg && bg !== 'none') console.log(bg);
   });
   ```
4. Download semua ke folder `images/`
5. Update HTML pakai path relatif: `images/filename.ext`

## Bootstrap 5 CDN
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
```

### Color Scheme Contractor
```css
:root { --primary: #1a3c5e; --accent: #f0a500; --dark: #1a1a2e; --light: #f8f9fa; }
```

## Serving via Public IP
```bash
cd /path/to/website && python3 -m http.server 8081 &
```
Akses: `http://PUBLIC_IP:8081`
Matikan: `kill $(lsof -t -i:8081)`
⚠️ Port 8080 sudah terpakai (topengdwimakmur). Selalu cek `lsof -ti:PORT` dulu.

## Project Deployment & Rollback Safety
- **Selalu backup full folder** dengan timestamp (e.g. `cp -r project project_backup_$(date +%Y%m%d_%H%M%S)`) sebelum melakukan extract, overwrite, atau refactoring UI/UX.
- Jika user meminta **"rollback"**, kembalikan folder secara atomik (gunakan folder temporary / rename) dan restart service daemon terkait (FastAPI / Uvicorn / http.server).
- **Google Drive Direct Download**: Gunakan library `gdown` (`gdown.download(url, quiet=False)`) ke direktori tujuan jika user memberikan link sharing Google Drive.

## User Preference
- Langsung eksekusi, jangan banyak tanya
- "jangan bantah" = langsung kerjakan
- "pelan-pelan dan teliti" / "jangan buru-buru" = lakukan audit mendalam, verifikasi cPanel/live server secara bertahap, dan konfirmasi sebelum mengubah file produksi
- "tes" = cek status dan kabarkan
- **Tema Desain Default (Light Theme)**: User sangat tidak menyukai *Dark Theme* untuk dashboard/workspace/web. Selalu prioritaskan **Clean Light Professional Theme** (Background `#f8fafc`, Card/Sidebar `#ffffff`, Tipografi High-Contrast `#0f172a` & `#334155`, Border Soft `#e2e8f0`, ApexCharts `theme: light`) kecuali jika diminta secara eksplisit.
- Pada dashboard scraping/analisis media sosial, wajib menggunakan data asli yang diekstrak murni tanpa angka mockup/sintetis. Jika metrik asli = 0, wajib laporkan 0. Form input link wajib mendukung direct execution pada penekanan tombol `Enter`.
- **Digital Marketer Workspace App Design**: Saat membuat dashboard agency digital marketing, jangan buat tampilan generik 1-halaman statis. Bangun sebagai aplikasi workspace dengan **Sidebar Client Switcher** dinamis (klik ganti klien) yang mengisolasi data KPI, chart trajektori, matriks kampanye aktif, leads CRM, dan modul AI audit link konten per klien.

## Live cPanel / Hosting Deployment Pitfalls
- **Backup Sebelum Edit**: Selalu buat backup file server (`.backup_YYYYMMDD`) sebelum menimpa file live.
- **Hindari Stray Syntax**: Periksa `<head>` dari karakter nyasar (seperti `>`) yang dapat memecah parsing browser dan mendorong tag `<meta>` ke dalam `<body>`.
- **FTP Clean Editing**: Saat mengupload via FTP, pastikan mode PASV aktif, verifikasi data dengan `RETR` atau curl live URL, dan sinkronkan `sitemap.xml` serta `.htaccess` bila ada file testing/dummy yang dihapus.

## Documentation Tips
- Buat PRD/BRD/FRD/TRD yang SPESIFIK sama project, jangan generic
- Sebutkan: nama section, konten aktual, gambar yang dipakai
- Jangan melebar ke hal-hal di luar project

## Checklist
- [ ] Tidak ada multi-color text di headline
- [ ] Tidak ada glassmorphism overdo
- [ ] Tidak ada 3 equal cards
- [ ] Tidak ada AI purple/blue gradient
- [ ] Navbar clean (transparent/solid)
- [ ] Gambar asli terdownload dari website sumber
- [ ] Mobile responsive
- [ ] **Mobile spacing sudah dikurangi** (media query padding ≤768px)
- [ ] Server bisa diakses via public IP
- [ ] **Port sudah dicek tidak konflik** (`lsof -ti:PORT`)
- [ ] Dokumen spesifik sama project
