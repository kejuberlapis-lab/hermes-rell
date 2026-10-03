---
name: indonesian-academic-paper
description: "Create Indonesian SINTA journal papers in DOCX IEEE format."
version: 1.1.0
tags: [academic, journal, SINTA, IEEE, DOCX, Indonesia]
related_skills: [docx, xlsx, obsidian]
---

# Indonesian Academic Paper (Jurnal Ilmiah)

Create publication-ready Indonesian journal papers in DOCX format following IEEE numbered reference style, matching the format of published SINTA-indexed journals.

## When to Use

Trigger phrases: "buat jurnal", "tulis paper", "artikel ilmiah", "SINTA 4", "journal paper", "makalah penelitian", "daftar pustaka", "riset dosen"

## Format Rules (CRITICAL — User Corrected Multiple Times)

### Title
- UPPERCASE, bold, centered, 14pt Times New Roman
- Pattern: "Implementasi Metode XXX pada YYY untuk Menunjang ZZZ"

### Abstract (Bilingual)
```
Abstrak: [Indonesian abstract, 150-250 kata]
Kata kunci: [italic, 3-5 keywords]

Abstract: [English abstract, same content]
Keywords: [italic, 3-5 keywords]
```

### Sections (Numbered)
1. **PENDAHULUAN** — Background + literature integration (NO separate "Tinjauan Pustaka" section)
2. **METODE** — Research design, subjects, instruments, procedure (MUST be detailed enough)
3. **HASIL DAN PEMBAHASAN** — Combined results + discussion
4. **KESIMPULAN** — Concise conclusions + suggestions

### References — IEEE Numbered Style
```
[1] A. Author, "Title," Journal, vol. X, no. Y, pp. Z–W, Year, doi: xxx.
[2] B. Author, "Title," Conference, pp. X–Y, Year.
```
NOT APA author-date format.

### Tables — BLACK AND WHITE ONLY
- Single border (`#000000`)
- No color fills, no gradients
- Header: bold, center
- Data: center, 10pt
- User explicitly flagged colorful tables as "terlihat pakai AI"

### Font and Layout
- Times New Roman 12pt everywhere
- Line spacing: Pt(20) or 1.5
- Margins: 3cm top/bottom/left, 2.5cm right
- Alignment: Justify

## User Preferences (IMPORTANT)

1. **"kurangi rumus"** — This is for dosen presenting results, NOT thesis/skripsi. Minimize formulas. Show results, not derivations.
2. **"terlihat pakai AI"** — Avoid: colorful tables, excessive formatting, overly perfect structure. Match published journal examples exactly.
3. **Bahasa Indonesia** — Write in formal academic Indonesian (PUEBI/EYD).
4. **Campuran referensi** — Mix Indonesian + international journals. User specifically wants Indonesian journal citations.
5. **Sesuaikan dengan contoh** — When user provides a published journal as reference, match its format EXACTLY.
6. **Sekolah/lokasi** — User may specify real institutions (e.g., NJIS). Use them as-is.
7. **Sampel kecil OK** — User may have 8-10 students. Use pre-eksperimen design, not quasi-eksperimen.
8. **Metode harus jelas** — User's colleague said "jurnal kamu tidak ada metode yang jelas". Methodology section MUST include: research design justification, sampling technique details, instrument development process, validity/reliability, step-by-step procedure, analysis techniques.
9. **Journal ≠ Skripsi** — Journal articles present findings concisely. No heavy formulas, no lengthy literature reviews. Keep it focused and practical.

## Pitfalls

- **DO NOT** use `Light Grid Accent 1` or any colored table style
- **DO NOT** write formulas like Aiken's V calculation — just state the result
- **DO NOT** use APA author-date in-text citations — use [1], [2]
- **DO NOT** make the paper thesis-length — journal articles are 8-12 pages
- **DO NOT** separate literature review into its own section
- **DO** match the format of any published journal example the user provides
- **DO** use real institution names the user specifies
- **DO** mix Indonesian + international references (user wants both)
- **DO** make methodology detailed enough (justify design, explain sampling, describe instruments)
- **DO** keep formulas minimal — state results, not derivations