---
name: academic-document-formatting
description: Use when formatting academic documents and DOCX/MD files.
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Academic, Formatting, PUEBI, EYD, Typography, DOCX, Skripsi, Pra-TA]
    related_skills: [docx, academic-proposal-workflow, academic-proposal-standards]
---

# Academic Document & Template Formatting

Use this skill when drafting, updating, styling, or compiling academic documents (skripsi, tesis, pra-TA proposals, journal manuscripts) in Markdown and Microsoft Word (.docx).

---

## 1. Indonesian Academic Typography Rules (PUEBI / EYD)

When composing academic text in Indonesian:

### Mandatory Italicization (*Huruf Miring*)
- **Foreign Terms:** All non-Indonesian words (English technical terms, industry terminology, foreign phrases) MUST be formatted in *italics*.
  - Examples: *workforce management*, *coffee shop*, *dwell time*, *shift*, *labor cost*, *throughput*, *understaffing*, *overstaffing*, *rush hour*, *cycle time*, *phantom occupancy*, *machine learning*, *deep learning*, *bounding box*, *anchor-free*, *Point of Sale*, *real-time*, *rule base*, *fuzzy inference system*, *people counting*.
- **Latin Scholarly Abbreviations:** Always italicize Latin academic notations.
  - Examples: *et al.*, *ibid.*, *op. cit.*, *ad hoc*, *de facto*.
- **Standardized Loanwords (Regular / Non-Italic):** Words already absorbed into KBBI must remain in standard regular font.
  - Examples: sistem, analisis, variabel, algoritma, kafe, manajer, operasional, metode, fungsi, komputer.

---

## 2. University Template Preservation Protocol

When populating official administrative templates (e.g. Form PTA.01, Proposal Pengajuan Judul, Form Bimbingan):

1. **Preserve Guidance & Instructions:**
   - Never overwrite, truncate, or delete original instruction paragraphs provided by the department or faculty.
   - Insert candidate content directly underneath each corresponding instruction block (Enter/Paragraph Break).
2. **Sequential Drafting & Formatting Protocol:**
   - Position cursor / insertion point at the end of the preceding instruction block.
   - Insert text cleanly.
   - Programmatically tokenize and apply *italic* formatting to all foreign terms and Latin citations (*et al.*) while maintaining regular font for Indonesian terms.
3. **Standard Academic Paragraph Formatting:**
   - **Font:** Times New Roman, 12 pt.
   - **Line Spacing:** 1.15 lines.
   - **Paragraph Spacing:** 6 pt after (or 6 pt before/after).
   - **Alignment:** Justified (*Rata Kanan-Kiri*).
   - **Margins:** 1.0 inch (2.54 cm) on all sides (Top, Bottom, Left, Right).

---

## 3. Interactive Markdown-First Workflow

1. **Edit Markdown First:**
   - Always update the `.md` file in the Obsidian vault first so the user can easily read, click links, and review content.
2. **Compile to Word After Confirmation:**
   - Once the Markdown draft is reviewed, compile or insert into the target `.docx` file using `python-docx` with proper run-level typography.

---

## 4. Multi-Device Git Synchronization Hygiene

- **Word Lock File Exclusion:** Microsoft Word automatically generates hidden temporary lock files (`~$<filename>.docx`) when opened on Windows/macOS.
- **Rule:** Always verify and clean temporary lock files before staging and committing to Git:
  ```bash
  rm -f "path/to/~$*.docx"
  git add -u
  git commit -m "style: apply academic formatting and typography"
  git push origin main
  ```
