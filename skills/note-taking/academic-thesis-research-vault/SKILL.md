---
name: academic-thesis-research-vault
description: Use when managing thesis vaults. Guides vault & Git sync.
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Thesis, Skripsi, Research, Git-Sync, Academic, Pra-TA, Citations]
    related_skills: [obsidian, research-paper-writing, grounded-citations]
---

# Academic Thesis & Research Vault

Use this skill when designing, organizing, drafting, reviewing citations, or synchronizing an academic thesis (*skripsi*, *tesis*, *disertasi*), pre-thesis proposals (*Pra-TA / Seminar Proposal*), or scientific research vaults in Obsidian.

---

## 1. Vault Architecture Standard (Modular 7-Tier Architecture)

When scaffolding or maintaining an academic vault, enforce this directory hierarchy:

```text
<VaultRoot>/
├── 00_Dashboard/
│   ├── MOC - Skripsi.md                  # Master Map of Content, student/advisor metadata, milestones
│   ├── Timeline & Milestones.md          # Deadlines, phased execution roadmap, progress bar
│   └── Logbook Bimbingan.md              # Formal supervision logbook & action items
├── 00_Pra_TA/                            # Pre-Thesis Registration & Topic Proposal Stage
│   ├── Dokumen_Pra_TA.md                 # Interactive proposal draft (PTA.01 / Form Pengajuan)
│   └── [Template_Asli].docx              # Official faculty template document (.docx / .pdf)
├── 01_Proposal_dan_Draft/
│   ├── BAB 1 - Pendahuluan.md            # Inverted pyramid intro, problem statement, research gap
│   ├── BAB 2 - Tinjauan Pustaka...md     # State of the art, theoretical foundations, conceptual framework
│   ├── BAB 3 - Metodologi Penelitian.md  # ISO flowchart, dataset split, metrics, statistical tests
│   ├── BAB 4 - Hasil dan Pembahasan.md   # Objective results vs in-depth discussion & benchmarking
│   └── BAB 5 - Kesimpulan dan Saran.md   # 1:1 mapping with problem statements and future work
├── 02_Studi_Literatur/
│   ├── Matriks Literatur & Research Gap.md # Comparison matrix (methods, datasets, metrics, gap)
│   ├── Daftar Jurnal & Paper.md          # Repositories partitioned by Tier/Quartile/Sinta (min 15 papers)
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

1. **Strict 5-Year Citation Recency Rule ($\le 5$ Years):**
   - All primary research papers, state-of-the-art comparisons, and methodological tools must be published within the **last 5 years** (current year $- 5$ to current year, e.g., 2021–2026 for a 2026 thesis).
   - Seminal classical theories (e.g., Zadeh 1965, Mamdani 1975) must be complemented or replaced by recent indexed peer-reviewed journal articles demonstrating contemporary adaptation.

2. **Pre-Thesis / Pra-TA Phase (PTA.01):**
   - Anchor problem statements objectively in the business/domain phenomena rather than framing the development of software/applications as the primary problem. The software/system acts solely as the evaluation testbed.
   - Enforce a minimum of 15 authentic, verified references indexed in Scopus (Q1–Q4) or Sinta (S1–S3).

3. **Chapter 1 (Pendahuluan):**
   - Apply the *Inverted Pyramid* structure: Macro (global context) $\rightarrow$ Meso (domain problems) $\rightarrow$ Micro (empirical research gap) $\rightarrow$ Proposed Solution & Novelty.
   - Problem statements must be measurable and map 1:1 to research objectives and Chapter 5 conclusions.

4. **Chapter 2 (Tinjauan Pustaka & SOTA):**
   - Synthesize comparisons using the SOTA matrix to clearly highlight the *Research Gap* (methodological, empirical, or performance gap) and formulate a distinct *Novelty Statement*.

5. **Methodology Citation Grounding:**
   - Every single step in the research methodology (computer vision algorithms, decision support / fuzzy inference systems, software development lifecycles like Prototyping, testing strategies like Black Box, and error metrics like MAPE) must be explicitly grounded in recent literature citations in the text.

6. **Chapter 4 (Hasil vs. Pembahasan):**
   - Strictly separate *Hasil* (raw and processed data, metric tables, ROC curves, loss graphs) from *Pembahasan* (scientific interpretation explaining *why* the metrics behaved as observed, factor ablation, and benchmark comparisons with prior literature).

7. **Turnitin & Paraphrasing Protocol:**
   - Enforce multi-source synthesis and active-to-passive or clause restructuring.
   - Maintain target similarity score $< 20\%$ with direct quotes excluded.

---

## 3. In-Depth Citation Breakdown Protocol

When the user asks to inspect, audit, or understand the citations used in their draft:
1. Provide full bibliographic metadata: Authors, Title, Journal/Conference, Year, Indexing (Scopus Q1/Q2/Sinta), and DOI/URL.
2. Summarize the core findings and scientific contribution of the paper.
3. Present the **verbatim original English excerpt** alongside an accurate Indonesian translation.
4. Detail exactly how the citation anchors the thesis argument (e.g., establishing problem urgency, identifying research gap, or justifying methodology choices).
5. Present this breakdown in the conversation chat without mutating the underlying report files unless requested.

---

## 4. Obsidian Git Sync & Multi-Device Workflow

When configuring automated two-way synchronization between client machines (Windows/macOS) and remote agents/servers:

### Headless Agent SSH Authentication (Deploy Key Pattern)
For private user repositories where the headless agent cannot enter passwords/tokens interactively:
1. Generate an unpassphrased ED25519 key on the server:
   ```bash
   ssh-keygen -t ed25519 -C "hermes-skripsi-vault" -f ~/.ssh/id_ed25519_skripsi -N ""
   ```
2. Guide the user to add the public key (`cat ~/.ssh/id_ed25519_skripsi.pub`) to their GitHub repository under **Settings $\rightarrow$ Deploy Keys** with **"Allow write access"** checked.
3. Configure Git to use this identity:
   ```bash
   git config core.sshCommand "ssh -i ~/.ssh/id_ed25519_skripsi -o StrictHostKeyChecking=accept-new"
   git remote set-url origin git@github.com:<username>/<repo>.git
   ```

### Plugin & Command Conventions on Client
- Use the official community plugin: **`Obsidian Git`** (by Vinzent03).
- Primary execution command in Command Palette (`Ctrl + P`): **`Git: Commit-and-sync`** (do not look for outdated single-purpose commands like `Git: Create backup`).
- Recommended Hotkey: Bind `Git: Commit-and-sync` to `Ctrl + Alt + S` or `Ctrl + Shift + S`.

### Interval Configuration Rules
- **Vault backup interval:** Set to **3 to 5 minutes** (sweet spot). Avoid 1-minute intervals to prevent excessive commit history noise and notification distraction while maintaining near real-time durability.
- **Auto pull on startup:** Always enable (ON) to automatically ingest upstream modifications made by the AI agent on server side before editing.

---

## 5. Pitfalls & Lessons

- **Resolve initial merge conflicts cleanly:** When merging client-initialized vaults with server scaffolds, use `git merge origin/main --allow-unrelated-histories` and resolve any conflicting baseline templates using `git checkout --ours` or `--theirs` before continuing automated sync.
- **Never create monolithic unlinked markdown files:** Always link concepts using Obsidian Wikilinks `[[File Name]]` so graph analysis and cross-chapter referencing function properly.
- **Never promise local client edits directly without Git remote sync:** Changes made on the remote agent server only appear on the user's local Obsidian client once pulled via Git sync or re-downloaded. Always clarify the synchronization bridge (GitHub Private Repo) to prevent user confusion.
