---
name: thesis-vault-workflow
description: Use when building thesis vaults. Manages sync and citations.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Vault, Academic, Skripsi, Thesis, GitSync, Pra-TA]
    related_skills: [obsidian, academic-vault]
---

# Thesis Vault & Academic Proposal Workflow

Use this skill when scaffolding, organizing, writing, and synchronizing academic research or thesis (skripsi/thesis/dissertation) vaults in Obsidian with headless agent support.

## 1. Vault Lifecycle & Pre-Thesis (Pra-TA / PTA.01)

Structure academic vaults into core functional modules:
1. `00_Dashboard/`: Master MOC (`MOC - [Topic].md`), cumulative logbooks, timeline milestones.
2. `00_Pra_TA/`: Official university pre-thesis forms (e.g. `PTA.01 Pendaftaran Pra-Tugas Akhir`). Store both interactive `.md` and compiled ready-to-submit `.docx` via `python-docx`.
3. `01_Proposal_dan_Draft/`: Standard chapters (Bab 1 through Bab 5).
4. `02_Studi_Literatur/`: SOTA matrix comparison table, categorized repository, paper review templates.
5. `03_Data_dan_Metodologi/`: Hardware/software stack, data pipeline, and experimental evaluation logs.
6. `04_Bimbingan_dan_Revisi/`: Per-advisor directives and before/after revision tables.
7. `05_Sidang_dan_Kelulusan/`: Question banks, presentation outlines, defense checklists.

## 2. Headless 2-Way Git Synchronization

When syncing between user's local Obsidian (Windows/macOS) and headless server:
1. **Private Repository**: Enforce private repositories on GitHub/GitLab.
2. **SSH Deploy Key**:
   - Generate key: `ssh-keygen -t ed25519 -C "hermes-vault" -f ~/.ssh/id_ed25519_vault -N ""`.
   - Set repo config: `git config core.sshCommand "ssh -i ~/.ssh/id_ed25519_vault -o StrictHostKeyChecking=accept-new"`.
   - Add public key to repo Deploy Keys with **Allow write access**.
3. **Obsidian Git Plugin (Vinzent03)**:
   - Primary command: `Git: Commit-and-sync` (stages, commits, pushes, and pulls).
   - Set `Vault backup interval (minutes)` to 3–5 minutes.

## 3. Academic Writing & Citation Quality Standards

- **Inverted Pyramid Background**: Macro phenomenon -> Meso industry pain points -> Micro research gap -> Proposed solution novelty.
- **Strict Citation Accessibility & Verification**:
  - All cited publications MUST be 100% Open Access and freely downloadable (no paywalled papers; prioritize SINTA/Garuda-indexed Indonesian journals or Gold Open Access like MDPI/IEEE Access/arXiv).
  - Every citation must be verified with active, working URLs and exact verbatim quotes from the actual paper.
- **Drafting & Review Protocol**:
  - Always update and format the interactive `.md` version in the vault first for user inspection and verification before altering binary `.docx` documents.
  - When editing official `.docx` university templates: preserve all original template instruction paragraphs intact, append the draft paragraphs below the instructions, and format all foreign/English terms (e.g. *workforce management*, *shift*, *labor cost*, *et al.*) in *italics*.
- **DOCX Synchronization**: Compile clean ready-to-submit `.docx` via `python-docx` alongside the template document.
