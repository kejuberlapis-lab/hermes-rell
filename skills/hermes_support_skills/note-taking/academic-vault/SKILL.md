---
name: academic-vault
description: Structure and sync academic thesis vaults in Obsidian.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Vault, Academic, Skripsi, Thesis, GitSync]
    related_skills: [obsidian]
---

# Academic & Thesis Vault Management

Use this skill when scaffolding, organizing, and synchronizing academic research or thesis (skripsi/thesis/dissertation) vaults in Obsidian with headless agent support.

## 1. Six-Module Vault Architecture (MOC Pattern)

Structure academic vaults into six core functional modules:
1. `00_Dashboard/`: 
   - `MOC - [Topic].md`: Master Map of Content with YAML frontmatter, thesis metadata, target milestones, and wiki-links.
   - `Logbook Bimbingan.md`: Cumulative advisor consultation logs with action items.
   - `Timeline & Milestones.md`: Progress bar and target completion dates.
2. `01_Proposal_dan_Draft/`: 
   - Standard chapters (`BAB 1 - Pendahuluan.md` through `BAB 5 - Kesimpulan dan Saran.md`).
   - Use inverted pyramid for introduction and explicit 1:1 mapping between Bab 1 objectives and Bab 5 conclusions.
3. `02_Studi_Literatur/`:
   - `Matriks Literatur & Research Gap.md`: SOTA comparison table (authors, methods, datasets, metrics, limitations, novelty).
   - `Daftar Jurnal & Paper.md`: Categorized repository (Q1/Q2/Sinta).
   - `Catatan_Paper/Template Review Jurnal.md`: Single-paper critique template.
4. `03_Data_dan_Metodologi/`:
   - `Instrumen Penelitian.md`: Hardware, software stack, hyperparameter tuning tables.
   - `Pengumpulan & Pengolahan Data.md`: Cleaning, outlier handling, and train/val/test splits.
   - `Analisis & Hasil Pengujian.md`: Confusion matrices, metrics comparison, and statistical hypothesis tests.
5. `04_Bimbingan_dan_Revisi/`:
   - Per-advisor directive logs (`Masukan Dosen Pembimbing 1.md`, `Masukan Dosen Pembimbing 2.md`).
   - `Checklist Revisi Pasca Seminar.md`: Before/after page-numbered revision audit trail.
6. `05_Sidang_dan_Kelulusan/`:
   - `Daftar Pertanyaan Kritis Penguji.md`: Question bank with structured response frameworks.
   - `Outline Slide Presentasi.md`: 12-slide high-impact defense structure (10–15 min).
   - Preparation checklists for Sempro and Defense.

## 2. Two-Way Headless Git Synchronization Setup

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
