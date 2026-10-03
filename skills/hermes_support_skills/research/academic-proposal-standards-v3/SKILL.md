---
name: academic-proposal-standards-v3
description: Use when verifying academic citations and proposals.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Academic, Citations, Thesis, Skripsi, Verification, Typography, OpenAccess]
    related_skills: [academic-proposal-workflow, grounded-citations, anti-hallucination]
---

# Academic Proposal Standards & Citation Verification

Use this skill when verifying scientific citations, auditing literature accessibility, drafting academic research proposals, and formatting Indonesian academic prose (EYD/PUEBI).

## 1. Zero-Hallucination Literature & Citation Gates

1. **Active Accessibility & Direct Download Gate**:
   - Before citing any scientific paper, verify that the paper is accessible and downloadable without paywalls.
   - For Indonesian papers: use SINTA 1–4, Garuda, or university OJS repositories with direct PDF URLs.
   - For international papers: verify Gold Open Access status (MDPI, IEEE Access, PeerJ) or provide direct open preprint PDF links (e.g., arXiv.org).
   - Never cite a paper based on metadata alone without inspecting the actual document content to avoid domain/topic mismatches (e.g. airport vehicle scheduling vs cafe barista tracking).
2. **5-Year Recency & 15+ Reference Quantity Gate**:
   - All primary citations, baseline models, and comparative methods must be published within the last 5 years (current year minus 5).
   - Proposals must maintain at least 15 verified references (recommended 18–25).
3. **Exact Grounding & Verbatim Attribution**:
   - When explaining citations to students or advisors, provide:
     - Exact verbatim excerpt from the paper's abstract or findings.
     - Faithful Indonesian translation.
     - Direct, clickable download URL / DOI.
     - Clear distinction between direct author quotes and secondary synthesis.

## 2. Indonesian Academic Typography & Template Integrity (PUEBI/EYD)

1. **Foreign & Technical Terms Italicization**:
   - Every foreign term, English technical concept (e.g., *Point of Sale*, *workforce management*, *dwell time*, *rush hour*, *cycle time*, *phantom occupancy*, *rule base*, *deep learning*), and Latin phrase (*et al.*) must be strictly formatted in *italic*.
2. **Preserving University Word Templates (`.docx`)**:
   - When filling institutional templates, never delete, overwrite, or alter existing instruction prompts, rubric guidelines, or header formatting.
   - Insert drafted text directly below the instruction blocks using standard academic typography (Times New Roman 12pt, 1.15 line spacing, justified alignment).
3. **Drafting & Verification Workflow**:
   - Conduct drafting, citation checking, and review paragraph-by-paragraph in Markdown / chat first before compiling and writing into the final `.docx` artifact.
