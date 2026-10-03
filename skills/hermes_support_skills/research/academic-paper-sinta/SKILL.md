---
name: academic-paper-sinta
description: "Write SINTA 4 journal papers in Bahasa Indonesia with DOCX output."
version: 2.0.0
author: Hermes Agent
---

# Academic Paper Writer — SINTA 4 Journals

Write complete, publication-ready academic papers for SINTA-indexed journals in Bahasa Indonesia.

## When to Use
User asks to write a journal paper for Indonesian academic journals. Triggers: "tulis paper", "buat jurnal", "SINTA", "artikel ilmiah", "IMRAD", "paper penelitian".

## Paper Structure (IMRAD)
1. **Judul & Abstrak** — Bilingual (ID+EN), 150-250 kata, 3-5 keywords
2. **Pendahuluan** — Latar belakang, state of the art, novelty, rumusan masalah, tujuan, manfaat
3. **Tinjauan Pustaka** — Teori, framework, penelitian terdahulu, research gap
4. **Metode** — Pendekatan, populasi/sampel, instrumen, analisis data
5. **Hasil & Pembahasan** — Tabel/grafik placeholder, analisis mendalam
6. **Kesimpulan & Saran** — Ringkasan, implikasi, keterbatasan
7. **Daftar Pustaka** — APA 7th, 15-20 referensi (campuran Indonesia + internasional)

## Output Format
1. **Markdown** — Save as `[Title].md` in Obsidian vault `Riset/` folder, update MOC
2. **DOCX** — Generate via python-docx with academic formatting (see DOCX Formatting below)
3. Always provide BOTH outputs when possible

## DOCX Formatting (python-docx)
```python
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
# Page setup
for section in doc.sections:
    section.top_margin = Cm(3)
    section.bottom_margin = Cm(3)
    section.left_margin = Cm(3)
    section.right_margin = Cm(2.5)

# Default style
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.paragraph_format.line_spacing = Pt(20)
style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

# Heading sizes: Level 1 = 14pt, Level 2 = 12pt
# Table style: 'Light Grid Accent 1', cell text 10pt, centered
# References: hanging indent (left_indent=1.27cm, first_line_indent=-1.27cm)
```

## Reference Strategy
- **Minimum 15-20 references** (more than basic 10-15 requirement)
- **Mix Indonesian + International**: ~40% Indonesian journals (SINTA-indexed), ~60% international
- **Indonesian references**: Use web_search with "jurnal Indonesia SINTA [topic] 2023 2024"
- **International references**: Use web_search with "[topic] research journal 2023 2024"
- **Always verify references exist** via web_search — never fabricate
- **Cite Indonesian references** to show local relevance and increase SINTA acceptance chance

## Sample Size Flexibility
- **Large sample (30+)**: Use quasi-experimental with control group, uji-t, ANOVA
- **Small sample (8-15)**: Use pre-experimental (one-group pretest-posttest), N-Gain, descriptive statistics
- **Very small (<8)**: Use qualitative case study or mixed methods
- Always justify sample size choice in methodology

## Language Rules
- Bahasa Indonesia formal (PUEBI/EYD), no contractions
- "Peneliti" not "kami"
- English terms in parentheses on first use if no standard Indonesian equivalent
- No informal Indonesian. No slang, no contractions.

## Quality Checklist
- [ ] Abstract bilingual, 150-250 words
- [ ] Research gap explicit in introduction
- [ ] Method replicable (sample, instrument, analysis)
- [ ] Results in tables with statistical tests
- [ ] Discussion links to prior literature (both ID and INTL)
- [ ] 15+ real references (use web_search, never fabricate)
- [ ] Mix of Indonesian and international references
- [ ] DOCX output with proper academic formatting

## Obsidian Output
- Save as `[Title].md` in `Riset/` folder
- Tags: `#riset` `#sinta4`
- Update MOC with link
- Wikilinks for related notes

## Pitfalls
- **Never fabricate references.** Search with web_search for real papers.
- **Never skip research gap.** SINTA reviewers require explicit novelty.
- **Mark placeholder data** (location, sample, results) clearly for user to fill.
- **No informal Indonesian.** No slang, no contractions.
- **Small samples need different stats.** Don't use uji-t with N<30 per group.
- **Indonesian references increase acceptance.** Always include 3-5+ Indonesian journal citations.
- **DOCX requires python-docx.** Install with `pip install python-docx` in venv (PEP 668 compliant).
- **User may provide their own prompt template.** Use it as the structure guide, not just the skill default.
