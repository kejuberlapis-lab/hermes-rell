---
name: academic-proposal-standards
description: Verify open-access citations and draft academic proposals.
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Academic, Citations, OpenAccess, SINTA, Verification, Skripsi, Pra-TA]
    related_skills: [academic-proposal-workflow, grounded-citations, academic-document-formatting]
---

# Academic Citation Verification & Open-Access Standards

Use this skill when gathering, auditing, verifying, or synthesizing academic citations for research proposals, theses (skripsi/tesis), and scholarly publications.

## 1. 100% Open Access & Direct Verification Protocol

1. **Direct Download Requirement**:
   - Every cited reference MUST be accessible and downloadable directly without payment barriers, subscription walls (e.g. Elsevier/ScienceDirect paid, Springer non-OA), or institutional logins.
   - If an international publication is paywalled, immediately substitute it with a reputable Indonesian national accredited journal (SINTA 1–4, Garuda, institutional OJS repositories) or a Gold Open Access / open preprint equivalent (arXiv direct PDF).
2. **Direct Verification Before Citing**:
   - Download the PDF or access the full HTML text directly before incorporating the reference into the draft.
   - Verify that the direct PDF link or article viewer works without authentication. Never cite a paywalled link that the user cannot click and read.

## 2. Verbatim Grounding & Quote Extraction

1. **Strict Verbatim vs. Paraphrase Distinction**:
   - When presenting quotes to the user, extract the authentic verbatim sentence directly from the paper's PDF (using text extraction tools) rather than inventing approximate summaries.
   - If citing research findings as a synthesis/paraphrase rather than a verbatim quote, explicitly state that it is a synthesis of the study's empirical results.
2. **Standard Citation Presentation in Chat**:
   When presenting or explaining references to the user:
   - **Identity:** Full author list, year, paper title, journal name, volume/issue, and page numbers.
   - **Direct URL:** Hyperlink to the open article landing page and direct PDF download link.
   - **Verbatim Quote:** Exact original sentence(s) in quotation marks.
   - **Indonesian Translation:** Faithful academic translation if the original text is in a foreign language.
   - **Thesis Role:** Precise explanation of which problem statement, objective, or methodology layer the reference defends.

## 3. Interactive Markdown-First Review Flow

1. **Markdown Review First**:
   - Update the interactive Markdown document (`Dokumen_Pra_TA_[Name].md`) with embedded hyperlinks first. This allows the user to review, click links, and audit literature on laptop/mobile before compiling Word `.docx` files.
2. **Iterative Section-by-Section Validation**:
   - Proceed paragraph by paragraph when revising background or literature, confirming user satisfaction with each source before advancing to subsequent sections.
