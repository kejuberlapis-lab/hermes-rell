---
name: sinta4-journal-writing
description: Write academic papers for Indonesian SINTA 4 journals. DOCX with IEEE refs.
triggers:
  - "buat jurnal"
  - "tulis paper"
  - "artikel ilmiah"
  - "sinta 4"
  - "journal writing"
category: writing
---

# SINTA 4 Journal Writing

> Write publication-ready academic papers for Indonesian SINTA 4 journals.

## Format Requirements (CRITICAL)

### Document Style
- Font: Times New Roman 12pt
- Margins: 3cm top/bottom, 3cm left, 2.5cm right
- Line spacing: Pt(20) / 1.5
- Alignment: Justify

### Structure (IEEE Style)
1. **Judul** — UPPERCASE, bold, centered
2. **Abstrak** — "Abstrak:" (bold) + teks (Indonesian)
3. **Kata kunci** — italic, 3-5 keywords
4. **Abstract** — "Abstract:" (bold italic) + teks (English)
5. **Keywords** — italic
6. **1. PENDAHULUAN** — Literature review integrated, NOT separate section
7. **2. METODE** — Methods (deskriptif, no heavy formulas)
8. **3. HASIL DAN PEMBAHASAN** — Combined results + discussion
9. **4. KESIMPULAN** — Brief conclusions
10. **DAFTAR PUSTAKA** — IEEE numbered format [1], [2], [3]

### Tables (CRITICAL)
- **BLACK AND WHITE ONLY** — no colored headers, no colored rows
- Border: single, black (#000000), size 4
- Header: bold, centered
- Data: centered, normal weight

### Writing Style
- **NO AI-LIKE PATTERNS** — vary sentence length, use natural academic Indonesian
- **Reduce formulas** — journal papers present results, not thesis methodology
- **Mixed references** — Indonesian + International journals
- **PUEBI/EYD** — formal academic Indonesian

### Reference Format (IEEE)
```
[1] A. Author, "Title of article," Journal Name, vol. X, no. Y, pp. XX-XX, Year, doi: xxx.
[2] B. Author, Book Title, Xth ed. Publisher, Year.
```

## Workflow

1. **Get topic from user** — title, research focus, sample size
2. **Search references** — mix Indonesian (SINTA) + international journals
3. **Write in markdown** — following structure above
4. **Convert to DOCX** — using python-docx with exact formatting
5. **Send via MEDIA:** — deliver file to user

## DOCX Generation (Python)

```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# Setup document
doc = Document()
for section in doc.sections:
    section.top_margin = Cm(3)
    section.bottom_margin = Cm(3)
    section.left_margin = Cm(3)
    section.right_margin = Cm(2.5)

# Style
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.paragraph_format.line_spacing = Pt(20)
style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

# Black-white table function
def tbl_bw(headers, rows):
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Add black borders
    tbl = t._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')
    borders = OxmlElement('w:tblBorders')
    for bn in ['top','left','bottom','right','insideH','insideV']:
        b = OxmlElement(f'w:{bn}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '4')
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), '000000')
        borders.append(b)
    tblPr.append(borders)
    # Header row
    for i, hd in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = hd
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in c.paragraphs[0].runs:
            r.bold = True
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
    # Data rows
    for ri, row in enumerate(rows):
        for ci, v in enumerate(row):
            c = t.rows[ri+1].cells[ci]
            c.text = str(v)
            for p in c.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)
    doc.add_paragraph()
```

## Common Corrections

1. **Tables colored** → Must be black-white only
2. **Too many formulas** → Reduce, present results not methodology
3. **AI-like writing** → Vary sentence structure, use natural flow
4. **APA references** → Change to IEEE numbered [1], [2]
5. **Separate lit review** → Integrate into Pendahuluan
6. **Title format** → "Implementasi metodr xxx pada xxx untuk menunjang xxx"
