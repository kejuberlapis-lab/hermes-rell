---
name: academic-proposal-workflow-v2
description: Draft research proposals and sync thesis vaults in Obsidian.
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Academic, Skripsi, Pra-TA, Thesis, Proposal, Obsidian, GitSync, Citations, OpenAccess]
    related_skills: [obsidian, docx, grounded-citations, academic-document-formatting]
---

# Academic Proposal & Thesis Vault Workflow

Use this skill when scaffolding, drafting, reviewing, and synchronizing academic research proposals (e.g., Pra-TA / Sempro) and thesis vaults in Obsidian with headless agent support.

## 1. Seven-Module Vault Architecture (MOC Pattern)

Structure academic vaults into seven core functional modules:
1. `00_Dashboard/`: 
   - `MOC - [Topic].md`: Master Map of Content with YAML frontmatter, thesis metadata, target milestones, and wiki-links.
   - `Logbook Bimbingan.md`: Cumulative advisor consultation logs with action items.
   - `Timeline & Milestones.md`: Progress bar and target completion dates.
2. `00_Pra_TA/`:
   - Official university pre-thesis registration forms (e.g., `Dokumen_Pra_TA_[Name].md` & `.docx`).
   - Short synopsis, research gap, objectives, and initial verified 15+ references.
3. `01_Proposal_dan_Draft/`: 
   - Standard chapters (`BAB 1 - Pendahuluan.md` through `BAB 5 - Kesimpulan dan Saran.md`).
   - Use inverted pyramid for introduction and explicit 1:1:1 mapping between Bab 1 problem statements, objectives, and Bab 5 conclusions.
4. `02_Studi_Literatur/`:
   - `Matriks Literatur & Research Gap.md`: SOTA comparison table (authors, methods, datasets, metrics, limitations, novelty).
   - `Daftar Jurnal & Paper.md`: Categorized repository (Q1/Q2/Sinta).
   - `Catatan_Paper/Template Review Jurnal.md`: Single-paper critique template.
5. `03_Data_dan_Metodologi/`:
   - `Instrumen Penelitian.md`: Hardware, software stack, hyperparameter tuning tables.
   - `Pengumpulan & Pengolahan Data.md`: Cleaning, outlier handling, and train/val/test splits.
   - `Analisis & Hasil Pengujian.md`: Confusion matrices, metrics comparison, and statistical hypothesis tests.
6. `04_Bimbingan_dan_Revisi/`:
   - Per-advisor directive logs (`Masukan Dosen Pembimbing 1.md`, `Masukan Dosen Pembimbing 2.md`).
   - `Checklist Revisi Pasca Seminar.md`: Before/after page-numbered revision audit trail.
7. `05_Sidang_dan_Kelulusan/`:
   - `Daftar Pertanyaan Kritis Penguji.md`: Question bank with structured response frameworks.
   - `Outline Slide Presentasi.md`: 12-slide high-impact defense structure (10–15 min).
   - Preparation checklists for Sempro and Defense.

## 2. Academic Rigor & Citation Standards

1. **5-Year Recency & 15+ Reference Floor**:
   - Ensure primary literature, benchmark algorithms, and comparative studies fall strictly within the last 5 years (current year minus 5).
   - Proposals must maintain at least 15 verified references in the bibliography (18–25 recommended).
2. **100% Verified Open Access & Indonesian Journal Priority**:
   - Prioritize Indonesian accredited journals (SINTA 1–4, Garuda, Neliti, university OJS) and Gold Open Access international publishers (IEEE Access, MDPI, PeerJ, arXiv) that allow immediate, free PDF downloads without institutional login.
   - **Full-Text PDF Inspection Gate**: Never cite based on search snippets, aggregator metadata, or DOI alone. Always download or inspect the full text to verify that the authors, title, and findings match the exact domain of the study (preventing mismatches such as vehicle scheduling cited as barista tracking).
   - If a paywalled paper is encountered, immediately replace it with an accessible open-access equivalent or provide the official open preprint (e.g. arXiv PDF).
3. **Authentic In-Text Grounding & Verbatim Quoting**:
   - When presenting literature to the user in chat:
     - Provide the exact verbatim text from the paper's abstract or findings.
     - Provide a faithful Indonesian translation.
     - Provide the active, clickable direct download URL.
     - Explicitly distinguish between literal quotes and secondary synthesis.
4. **Iterative Markdown-First Drafting Flow**:
   - Always draft and update paragraph-by-paragraph in the vault's `.md` file first.
   - Commit and push to Git after each paragraph so the user can review, click links, and verify the text in Obsidian before proceeding to the next paragraph or compiling to Word.
5. **1:1:1 Alignment Triad**:
   - Every **Rumusan Masalah** ($Q_i$) must map directly to a single **Tujuan Penelitian** ($T_i$) and an explicit **Metrik Pengujian** ($M_i$) in Metodologi (e.g., Computer Vision $\rightarrow$ mAP/FPS; Decision Support/Fuzzy $\rightarrow$ MAPE; Software $\rightarrow$ Black Box).

## 3. Two-Way Headless Git Synchronization Setup

When syncing between a user's local Obsidian (Windows/macOS) and headless server:
1. **Private Repository**: Enforce private repositories on GitHub/GitLab to protect unpublished academic work.
2. **SSH Deploy Key Authentication**:
   - Never solicit GitHub passwords or personal access tokens in chat.
   - Generate an isolated key: `ssh-keygen -t ed25519 -C "hermes-vault" -f ~/.ssh/id_ed25519_vault -N ""`.
   - Set repo config: `git config core.sshCommand "ssh -i ~/.ssh/id_ed25519_vault -o StrictHostKeyChecking=accept-new"`.
   - Direct user to repo Deploy Keys settings (`https://github.com/<user>/<repo>/settings/keys`) to add the public key with **Allow write access**.
3. **Client-Side Obsidian Git Plugin (Vinzent03)**:
   - Primary sync command: `Git: Commit-and-sync` (executes stage, commit, push, pull concurrently).
   - Setting `Vault backup interval (minutes)` to 3–5 minutes handles automated background sync.
4. **Dual Markdown & Word (`.docx`) Mirroring**:
   - Maintain both the interactive Markdown note in the vault and a compiled clean `.docx` file (Times New Roman 12pt, 1-inch margins, signature tables). Both are committed to Git so the user receives ready-to-print artifacts upon pulling.
   - Clean temporary Word lock files (`~$*.docx`) before staging to avoid Git conflicts.
