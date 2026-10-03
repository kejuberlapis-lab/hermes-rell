---
name: academic-thesis-vault
description: Use when managing thesis vaults. Guides vault & Git sync.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Thesis, Skripsi, Research, Git-Sync, Academic]
    related_skills: [obsidian, research-paper-writing]
---

# Academic Thesis & Research Vault

Use this skill when designing, organizing, drafting, or synchronizing an academic thesis (*skripsi*, *tesis*, *disertasi*) or scientific research vault in Obsidian.

---

## 1. Vault Architecture Standard (Modular 6-Tier Architecture)

When scaffolding or maintaining an academic vault, enforce this directory hierarchy:

```text
<VaultRoot>/
├── 00_Dashboard/
│   ├── MOC - Skripsi.md                  # Master Map of Content, student/advisor metadata, milestones
│   ├── Timeline & Milestones.md          # Deadlines, phased execution roadmap, progress bar
│   └── Logbook Bimbingan.md              # Formal supervision logbook & action items
├── 01_Proposal_dan_Draft/
│   ├── BAB 1 - Pendahuluan.md            # Inverted pyramid intro, problem statement, research gap
│   ├── BAB 2 - Tinjauan Pustaka...md     # State of the art, theoretical foundations, conceptual framework
│   ├── BAB 3 - Metodologi Penelitian.md  # ISO flowchart, dataset split, metrics, statistical tests
│   ├── BAB 4 - Hasil dan Pembahasan.md   # Objective results vs in-depth discussion & benchmarking
│   └── BAB 5 - Kesimpulan dan Saran.md   # 1:1 mapping with problem statements and future work
├── 02_Studi_Literatur/
│   ├── Matriks Literatur & Research Gap.md # Comparison matrix (methods, datasets, metrics, gap)
│   ├── Daftar Jurnal & Paper.md          # Repositories partitioned by Tier/Quartile/Sinta
│   └── Catatan_Paper/                    # Per-paper critical appraisal notes
├── 03_Data_dan_Metodologi/
│   ├── Instrumen Penelitian.md           # Hardware/software stack, libraries, hyperparameters
│   ├── Pengumpulan & Pengolahan Data.md  # Preprocessing logs, cleaning, transformation pipelines
│   └── Analisis & Hasil Pengujian.md     # Experiment runs, confusion matrices, hypothesis testing
├── 04_Bimbingan_dan_Revisi/
│   ├── Masukan Dosen Pembimbing 1.md     # Substantive & methodological advisory log
│   ├── Masukan Dosen Pembimbing 2.md     # Technical & formatting advisory log
│   └── Checklist Revisi Pasca Seminar.md # "Before vs. After" page-by-page revision tracking matrix
├── 05_Sidang_dan_Kelulusan/
│   ├── Persiapan Seminar Proposal.md     # Proposal defense dossier checklist
│   ├── Persiapan Sidang Skripsi.md       # Final defense yudisium prerequisites & system demo
│   ├── Daftar Pertanyaan Kritis Penguji.md # Examiner Q&A bank with structured response frameworks
│   └── Outline Slide Presentasi.md       # 10-12 slide defense deck structure (10-15 min)
└── 99_Templates_dan_Panduan/
    ├── Panduan Format Sitasi (APA & IEEE).md
    ├── Panduan Anti-Plagiarisme & Parafrase.md # Academic paraphrasing rules for Turnitin < 20%
    ├── Template Catatan Literatur.md
    └── Template Draft Bab.md
```

---

## 2. Core Scientific Writing & Drafting Rules

1. **Chapter 1 (Pendahuluan):**
   - Apply the *Inverted Pyramid* structure: Macro (global context) $\rightarrow$ Meso (domain problems) $\rightarrow$ Micro (empirical research gap) $\rightarrow$ Proposed Solution.
   - Problem statements must be measurable and map 1:1 to research objectives and Chapter 5 conclusions.

2. **Chapter 2 (Tinjauan Pustaka & SOTA):**
   - Never write isolated summaries of papers sequentially. Synthesize comparisons using the SOTA matrix to clearly highlight the *Research Gap* (methodological, empirical, or performance gap) and define a distinct *Novelty Statement*.

3. **Chapter 4 (Hasil vs. Pembahasan):**
   - Strictly separate *Hasil* (raw and processed data, metric tables, ROC curves, loss graphs) from *Pembahasan* (scientific interpretation explaining *why* the metrics behaved as observed, factor ablation, and benchmark comparisons with prior literature).

4. **Turnitin & Paraphrasing Protocol:**
   - Enforce multi-source synthesis and active-to-passive or clause restructuring.
   - Maintain target similarity score $< 20\%$ with direct quotes excluded.

---

## 3. Obsidian Git Sync & Multi-Device Workflow

When configuring automated two-way synchronization between client machines (Windows/macOS) and remote agents/servers:

### Plugin & Command Conventions
- Use the official community plugin: **`Obsidian Git`** (by Vinzent03).
- Primary execution command in Command Palette (`Ctrl + P`): **`Git: Commit-and-sync`** (do not look for outdated single-purpose commands).
- Recommended Hotkey: Bind `Git: Commit-and-sync` to `Ctrl + Alt + S` or `Ctrl + Shift + S`.

### Interval Configuration Rules
- **Vault backup interval:** Set to **3 to 5 minutes** (sweet spot). Avoid 1-minute intervals to prevent excessive commit history noise and notification distraction while maintaining near real-time durability.
- **Auto pull on startup:** Always enable (ON) to automatically ingest upstream modifications made by the AI agent on server side before editing.
- **Git Repo Init Sequence on Local:**
  ```bash
  git init
  git remote add origin <private_repo_url>
  git branch -M main
  git add .
  git commit -m "Initialize thesis vault"
  git push -u origin main
  ```

---

## 4. Pitfalls & Lessons

- **Never create monolithic unlinked markdown files:** Always link concepts using Obsidian Wikilinks `[[File Name]]` so graph analysis and cross-chapter referencing function properly.
- **Never promise local client edits directly without Git remote sync:** Changes made on the remote agent server only appear on the user's local Obsidian client once pulled via Git sync or re-downloaded. Always clarify the synchronization bridge (GitHub Private Repo) to prevent user confusion.
