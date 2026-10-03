---
name: academic-proposal-standards-v5
description: Use when verifying academic citations and proposals.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Academic, Citations, Thesis, Skripsi, Verification, Typography, OpenAccess, Audit]
    related_skills: [academic-proposal-workflow, grounded-citations, anti-hallucination]
---

# Academic Proposal Standards & Citation Verification

Use this skill when verifying scientific citations, auditing literature accessibility, drafting academic research proposals, ensuring bidirectional text-bibliography synchronization, and formatting Indonesian academic prose (EYD/PUEBI).

## 1. Zero-Hallucination Literature & Citation Gates

1. **Active Accessibility & Direct Download Gate**:
   - Before citing any scientific paper, verify that the paper is 100% accessible and downloadable without paywalls or login barriers.
   - For Indonesian papers: use SINTA 1–4, Garuda, or university OJS repositories with direct, unblocked PDF URLs.
   - For international literature: avoid commercial paywalled textbooks (e.g., Wiley, Elsevier, Springer books without open PDF access) for standard methodology (e.g. Black Box Testing); replace them with verified Open Access journal papers with direct PDF downloads.
   - For foundational international papers (e.g. ByteTrack, YOLOv8): verify Gold Open Access status (MDPI, PeerJ, IEEE Access open) or direct open preprint PDFs (e.g. arXiv.org).
   - Never cite a paper based on metadata or title keywords alone without inspecting the actual document content (e.g. using `curl` + `pdftotext`) to prevent topic/domain mismatches.
2. **5-Year Recency & 15+ Reference Quantity Gate**:
   - All primary citations, baseline models, and comparative methods must be published within the last 5 years (current year minus 5).
   - Proposals must maintain at least 15 verified references in the bibliography (recommended 17–25+).
3. **1:1 Bidirectional Citation-Bibliography Audit Gate**:
   - Every reference in the bibliography (Daftar Pustaka) must be explicitly cited in the body text.
   - Every citation in the body text must have a corresponding entry in the bibliography.
   - Before executing batch modifications or deletions of unused references, audit the entire file and present the planned additions/removals clearly for user review and approval.
4. **Exact Grounding & Verbatim Attribution**:
   - When explaining citations to students or advisors, provide:
     - Exact verbatim excerpt from the paper's abstract or findings.
     - Faithful Indonesian translation.
     - Direct, clickable download URL / DOI.
     - Clear distinction between direct author quotes and secondary synthesis.

## 2. Indonesian Academic Typography & Template Integrity (PUEBI/EYD)

1. **Foreign & Technical Terms Italicization**:
   - Every foreign term, English technical concept (e.g., *Point of Sale*, *workforce management*, *dwell time*, *rush hour*, *cycle time*, *phantom occupancy*, *rule base*, *deep learning*, *multi-object tracking*), and Latin phrase (*et al.*) must be strictly formatted in *italic*.
2. **Preserving University Word Templates (`.docx`)**:
   - When filling institutional templates, never delete, overwrite, or alter existing instruction prompts, rubric guidelines, or header formatting.
   - Insert drafted text directly below the instruction blocks using standard academic typography (Times New Roman 12pt, 1.15 line spacing, justified alignment).
3. **Drafting & Verification Workflow**:
   - Conduct drafting, citation checking, and review paragraph-by-paragraph in Markdown (`.md`) / chat first before compiling and writing into the final `.docx` artifact.
