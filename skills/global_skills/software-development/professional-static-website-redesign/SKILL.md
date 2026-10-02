---
name: professional-static-website-redesign
description: Redesign website company profile statis agar terlihat profesional (enterprise-grade), konsisten antar halaman, SEO-ready, lalu paketkan ZIP siap upload.
---

# Professional Static Website Redesign (Company Profile)

Gunakan skill ini saat user meminta tampilan website statis terlihat lebih profesional/modern, bukan style "belajar", dan ingin hasil siap deploy.

## Kapan Dipakai
- User minta redesign UI/UX website company profile.
- Website berupa HTML/CSS statis multi-page.
- User ingin output cepat: file ZIP siap upload + opsi preview gratis.

## Workflow
1. **Discovery cepat & baseline file**
   - Identifikasi struktur situs: `index.html`, halaman internal, `styles.css`, `robots.txt`, `sitemap.xml`.
   - Catat halaman mana yang sudah diubah vs belum diubah.

2. **Ambil referensi desain yang relevan**
   - Gunakan referensi enterprise sejenis (mis. clean fintech/corporate design system).
   - Fokus pada: hierarchy tipografi, spacing, CTA, card consistency, header/nav, section rhythm.

3. **Redesign sistematis (bukan tambal sulam)**
   - Tulis ulang/rapikan `styles.css` sebagai design system mini:
     - token warna, font scale, spacing scale, container width, button variants, card style.
   - Terapkan konsisten ke semua halaman, bukan homepage saja.
   - Pastikan komponen inti seragam: navbar, footer, hero/heading blocks, card/list blocks.

4. **Jaga SEO on-page tetap aman**
   - Per halaman: `title`, `meta description`, `canonical`, struktur heading (`H1` tunggal), OG tags minimal.
   - Pastikan `robots.txt` dan `sitemap.xml` tetap valid setelah perubahan URL/struktur.

5. **Verifikasi hasil sebelum kirim**
   - Jika ada warning seperti file berubah sejak read terakhir, baca ulang file sebelum overwrite berikutnya.
   - Cek cepat konsistensi antar halaman (desktop/mobile basic).

6. **Paket deliverable**
   - Buat ZIP versi baru (gunakan nama versi, jangan overwrite file lama):
     - contoh: `project-site-v2-professional.zip`
   - Laporkan path file final untuk dikirim sebagai media.

7. **Berikan opsi preview gratis**
   - Rekomendasikan jalur tercepat: Netlify Drop.
   - Opsi tambahan: Cloudflare Pages, GitHub Pages.

## Pitfalls yang Pernah Terjadi
- **Hanya homepage yang diperbaiki** → hasil terasa tidak konsisten/profesional.
- **Overwrite konflik** saat file berubah sejak pembacaan terakhir → harus re-read sebelum edit lanjutan.
- **Konflik sibling writer/subagent** (warning file dimodifikasi pihak lain) → hentikan patch lanjutan, `read_file` ulang lalu rewrite final satu sumber kebenaran.
- **ZIP lama terkirim ulang** → gunakan nama ZIP baru yang jelas versinya.

## Upgrade Bootstrap 5 (V4)
Gunakan saat user minta "lanjutkan" setelah redesign dasar:
1. Tambahkan Bootstrap Icons CDN di semua halaman untuk visual yang lebih enterprise.
2. Tambahkan micro-interaction ringan (IntersectionObserver + class `.reveal/.show`) alih-alih animasi berat.
3. Tambahkan halaman `portfolio.html` sebagai social proof dan hubungkan di navbar semua halaman.
4. Pastikan CTA tetap konsisten (`Konsultasi`, `Kontak`) dan hierarchy heading tetap 1x H1 per halaman.
5. Re-package sebagai ZIP versi baru (contoh: `-v4-bootstrap5-animated.zip`) sebelum dikirim.

## Pengiriman ke Chat
- Jika user minta "kirim file ke chat ini", balas dengan format media path langsung:
  - `MEDIA:/absolute/path/file.zip`
- Jangan hanya kirim path teks biasa ketika user secara eksplisit meminta file dikirim.

## Checklist Selesai
- [ ] Semua halaman utama sudah mengikuti visual system yang sama.
- [ ] SEO dasar per halaman terisi.
- [ ] ZIP baru berhasil dibuat dan ukurannya masuk akal.
- [ ] User menerima file final + opsi preview cepat.
