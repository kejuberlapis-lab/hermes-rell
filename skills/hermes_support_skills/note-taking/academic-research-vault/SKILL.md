---
name: academic-research-vault
description: Use when building thesis vaults. Syncs Git and drafts.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Thesis, Skripsi, Research, Git-Sync, Academic]
    related_skills: [obsidian, docx]
---

# Academic Research & Thesis Vault

Use this skill when designing, scaffolding, drafting, or synchronizing an academic thesis (*skripsi*, *tesis*, *disertasi*), pre-thesis (*Pra-TA*), or scientific research vault in Obsidian.

---

## 1. Modular 7-Tier Vault Architecture

When scaffolding or maintaining an academic vault in Obsidian, enforce this directory structure:

```text
<VaultRoot>/
├── 00_Dashboard/
│   ├── MOC - Skripsi.md                  # Master Map of Content, student/advisor metadata, milestones
│   ├── Timeline & Milestones.md          # Deadlines, phased execution roadmap, progress bar
│   └── Logbook Bimbingan.md              # Formal supervision logbook & action items
├── 00_Pra_TA/                            # Pre-thesis stage (PTA.01 registration, title defense)
│   ├── Dokumen_Pra_TA_<Name>.md          # Interactive markdown workspace for title & proposal registration
│   └── Pra-TA_<Name>_<NIM>.docx          # Formatted, submission-ready DOCX for advisor approval
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

## 2. Scientific Writing, Citations, & Literature Recency Gate

1. **Strict 5-Year Literature Recency Gate:**
   - In academic proposals (*Pra-TA*, *Sempro*, *Skripsi*), all core references and state-of-the-art matrix citations must strictly originate from the **last 5 years** ($\le 5$ years back from current year).
   - In-text citations must back up every empirical claim in *Latar Belakang*, each methodology phase (e.g. YOLO, tracking, fuzzy inference, software development method), and evaluation metrics (e.g. mAP, MAPE, Black Box Testing).

2. **Chapter 1 (Pendahuluan):**
   - Apply the *Inverted Pyramid* structure: Macro (global context) $\rightarrow$ Meso (domain problems) $\rightarrow$ Micro (empirical research gap) $\rightarrow$ Proposed Solution.
   - Problem statements must be measurable and map 1:1 to research objectives and Chapter 5 conclusions. Building an application/testbed is a vehicle, not the core research problem.

3. **Chapter 2 (Tinjauan Pustaka & SOTA):**
   - Never write isolated summaries of papers sequentially. Synthesize comparisons using the SOTA matrix to clearly highlight the *Research Gap* (methodological, empirical, or performance gap) and define a distinct *Novelty Statement*.

4. **Chapter 4 (Hasil vs. Pembahasan):**
   - Strictly separate *Hasil* (raw and processed data, metric tables, ROC curves, loss graphs) from *Pembahasan* (scientific interpretation explaining *why* the metrics behaved as observed, factor ablation, and benchmark comparisons with prior literature).

5. **Turnitin & Paraphrasing Protocol:**
   - Enforce multi-source synthesis and active-to-passive or clause restructuring. Maintain target similarity score $< 20\%$ with direct quotes excluded.

---

## 3. Obsidian Git Sync & Multi-Device Workflow

When configuring automated two-way synchronization between client machines (Windows/macOS) and remote agents/servers:

### Plugin & Command Conventions
- Use the official community plugin: **`Obsidian Git`** (by Vinzent03).
- Primary execution command in Command Palette (`Ctrl + P`): **`Git: Commit-and-sync`** (replaces legacy single commands).
- Recommended Hotkey: Bind `Git: Commit-and-sync` to `Ctrl + Alt + S` or `Ctrl + Shift + S`.

### Interval Configuration Rules
- **Vault backup interval:** Set to **3 to 5 minutes** (optimal sweet spot). Avoid 1-minute intervals to prevent excessive commit history noise and notification distraction while maintaining near real-time durability.
- **Auto pull on startup:** Always enable (ON) to automatically ingest upstream modifications made by the AI agent on server side before editing.

### Agent SSH Deploy Key Setup (Headless Authentication)
For private repositories without requiring user personal access tokens:
1. Generate an Ed25519 deploy key:
   ```bash
   ssh-keygen -t ed25519 -C "hermes-skripsi-vault" -f ~/.ssh/id_ed25519_skripsi -N ""
   ```
2. Have the user add the public key (`~/.ssh/id_ed25519_skripsi.pub`) to GitHub Repo $\rightarrow$ Settings $\rightarrow$ Deploy Keys with **Write Access** enabled.
3. Configure Git's SSH command:
   ```bash
   git config core.sshCommand "ssh -i ~/.ssh/id_ed25519_skripsi -o StrictHostKeyChecking=accept-new"
   git remote set-url origin git@github.com:<username>/<repo>.git
   ```

### Divergence Resolution
When local Obsidian Git auto-backups (`vault backup: YYYY-MM-DD HH:MM:SS`) cause non-fast-forward divergence on the server:
- Always run `git pull --rebase origin main` before pushing agent-generated commits.

---

## 4. Pitfalls & Lessons

- **Never create monolithic unlinked markdown files:** Always link concepts using Obsidian Wikilinks `[[File Name]]` so graph analysis and cross-chapter referencing function properly.
- **Never promise local client edits directly without Git remote sync:** Changes made on the remote agent server only appear on the user's local Obsidian client once pulled via Git sync or re-downloaded. Always clarify the synchronization bridge (GitHub Private Repo) to prevent user confusion.
- **Generate formatted DOCX alongside Markdown:** When academic submission forms (e.g. *PTA.01*) require signatures, compile a cleanly styled `.docx` (Times New Roman 12, 1.15 line spacing, 1-inch margins) matching the markdown version so the user can immediately submit to advisors.
