#!/bin/bash
set -e

BACKUP_DIR="/home/ubuntu/hermes_vps_backup"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S WIB")
SSH_KEY="/home/ubuntu/.ssh/id_ed25519_vps_backup"
REPO_URL="git@github.com:kejuberlapis-lab/hermes-rell.git"
PROFILE_DIR="/home/ubuntu/.hermes/profiles/profil-admin-mvp"

echo "=========================================================="
echo "Starting Hermes VPS Comprehensive Backup: $TIMESTAMP"
echo "Target Repo: $REPO_URL"
echo "=========================================================="

mkdir -p "$BACKUP_DIR/vaults"
mkdir -p "$BACKUP_DIR/projects/lamar_coffee"
mkdir -p "$BACKUP_DIR/projects/hris"
mkdir -p "$BACKUP_DIR/projects/scripts"
mkdir -p "$BACKUP_DIR/hermes_core/memories"
mkdir -p "$BACKUP_DIR/hermes_core/config"
mkdir -p "$BACKUP_DIR/skills/profile_skills"
mkdir -p "$BACKUP_DIR/skills/global_skills"
mkdir -p "$BACKUP_DIR/system_configs/systemd"
mkdir -p "$BACKUP_DIR/system_configs/nginx"

# 1. Backup Memories, Rules, Soul & Personas
echo "📝 Backing up Hermes Memories, Core Rules & Personas..."
cp -f "$PROFILE_DIR/memories/MEMORY.md" "$BACKUP_DIR/hermes_core/memories/" 2>/dev/null || true
cp -f "$PROFILE_DIR/memories/USER.md" "$BACKUP_DIR/hermes_core/memories/" 2>/dev/null || true
cp -f "$PROFILE_DIR/SOUL.md" "$BACKUP_DIR/hermes_core/memories/" 2>/dev/null || true
cp -f "$PROFILE_DIR/channel_directory.json" "$BACKUP_DIR/hermes_core/config/" 2>/dev/null || true
cp -f "$PROFILE_DIR/.skills_prompt_snapshot.json" "$BACKUP_DIR/hermes_core/config/" 2>/dev/null || true

# Sanitize & copy config.yaml (remove raw secrets if present)
if [ -f "$PROFILE_DIR/config.yaml" ]; then
    sed -E 's/(token|key|secret|password): *("[^"]+"|[^\n]+)/\1: "[REDACTED]"/gi' "$PROFILE_DIR/config.yaml" > "$BACKUP_DIR/hermes_core/config/config.sanitized.yaml"
fi

# 2. Backup All Obsidian Vaults (Full Markdown & Docs)
echo "📦 Backing up All Obsidian Vaults & Markdown Docs..."
rsync -av --delete \
  --exclude=".git" \
  --exclude=".trash" \
  --exclude="*.zip" \
  --exclude="*.csv" \
  /home/ubuntu/ObsidianVault/ "$BACKUP_DIR/vaults/"

# Copy any root markdown files
find /home/ubuntu/ -maxdepth 1 -name "*.md" -exec cp -f {} "$BACKUP_DIR/" \; 2>/dev/null || true

# 3. Backup Skills (Profile Skills + Global Skills Library)
echo "🧠 Backing up Profile Skills & Full Global Skills Library..."
rsync -av --delete \
  --exclude="__pycache__" \
  --exclude=".git" \
  "$PROFILE_DIR/skills/" "$BACKUP_DIR/skills/profile_skills/"

rsync -av --delete \
  --exclude="__pycache__" \
  --exclude=".git" \
  --exclude=".archive" \
  /home/ubuntu/.hermes/skills/ "$BACKUP_DIR/skills/global_skills/"

# 4. Generate Master Skills Catalog & Index
echo "📋 Generating Master Skills Catalog (SKILLS_CATALOG.md)..."
cat << 'EOF' > "$BACKUP_DIR/SKILLS_CATALOG.md"
# 🧠 Katalog & Daftar Lengkap Skill Hermes AI Agent

Dokumen ini berisi daftar seluruh skill operasional, workflow otomasi, dan pustaka kemampuan yang terpasang pada sistem Hermes.

## 📂 1. Profile Custom Skills (`skills/profile_skills/`)
Daftar skill spesifik yang disesuaikan untuk workflow VPS, trading, otomasi web anti-bot, DED arsitektur, dan pengembangan web:
- **anti-hallucination-gates**: Enforces execution proof gates and deterministic verification.
- **architectural-floorplan-drafting**: Generates & edits official CAD & SVG architectural layouts.
- **automated-trading-systems**: MQL4/MQL5 EA design, backtesting, and MT5 deployment.
- **cad-and-3d-modeling**: 3D & CAD geometry modeling (DXF, OBJ, Shapely, Trimesh).
- **claude-design**: High-end HTML/CSS design artifact synthesis (Anti-Slop AI standards).
- **enterprise-workflow-and-role-governance**: Multi-server DB, role hierarchy, attendance rules.
- **hallucination-guard**: Execution-based verification guardrail with 14 check items.
- **market-backtesting**: Deterministic 20-year XAU backtesting & tick analysis.
- **multi-page-web-architecture**: Full multi-page web application architecture.
- **production-environment-operations**: Live service, VPS XRDP, and database administration.
- **stealth-browser-automation**: SeleniumBase UC mode, JA3/TLS evasion, Cloudflare Turnstile bypass.
- **telegram-mini-app-automation**: Automated tap, batch claiming & Web3 node compounding.

## 🌐 2. Global Skills Library (`skills/global_skills/`)
Pustaka skill bawaan meliputi:
- **autonomous-ai-agents**: `claude-code`, `codex`, `antigravity`, `merge-reconciler`, `computer-use`.
- **creative**: `anti-slop-web-design`, `architecture-diagram`, `excalidraw`, `manim-video`, `p5js`, `popular-web-designs`.
- **github**: `github-auth`, `github-code-review`, `github-issue-to-pr`, `github-pr-workflow`, `github-repo-management`.
- **mlops & inference**: `serving-llms-vllm`, `llama-cpp`, `evaluating-llms-harness`, `weights-and-biases`.
- **productivity**: `google-workspace`, `docx`, `pdf`, `powerpoint`, `xlsx`, `airtable`, `notion`.
- **research**: `grounded-citations`, `academic-proposal-standards`, `arxiv`, `competitor-news-monitor`.
- **social-media & web**: `xurl`, `blocked-page-recovery`, `stealth-browser-automation`.

---
*Generated automatically during Hermes Master Backup.*
EOF

# 5. Generate Master Rules & Settings Manifest
echo "📜 Generating Rules & Settings Manifest (RULES_AND_SETTINGS.md)..."
cat << 'EOF' > "$BACKUP_DIR/RULES_AND_SETTINGS.md"
# 🛡️ Manifest Pengaturan, Rule Inti, & Konfigurasi Sistem Hermes

## 👑 1. Persona & Identitas
- **Nama:** Hermes AI Agent.
- **Sapaan User:** `sir`.
- **Bahasa:** Bahasa Indonesia secara natural (kecuali sir meminta bahasa lain).
- **Filosofi Ekosistem:** 1 Otak, 1 Proses, 1 Tempat (Lokal, VPS-Zeus, dan Telegram adalah satu kesatuan tersinkron).

## 🔒 2. Protokol Keamanan & Whitelist Telegram
- **Whitelist Akses Telegram (Hanya 4 Akun Resmi):**
  1. Andi Saputra (ID: `661471478`, Owner)
  2. Avrell (ID: `5955713269`, Admin)
  3. Sedni (ID: `856579127`, Admin)
  4. Admin (ID: `728903007`, Admin)
- Seluruh ID di luar daftar di atas diblokir total.
- Tidak pernah membocorkan kredensial, token rahasia, atau data sensitif.

## 🎓 3. Isolasi Akun & Scope
- **Akun GitHub `StefanoGarrent`:** HANYA KHUSUS untuk scope Skripsi (`skripsi-vault.git`).
- Proyek lain (Mitsindo, Lamar Coffee, XAU Trading, VPS Backup, Bot Airdrop) wajib diisolasi penuh di repositori/kunci terpisah.

## ⚙️ 4. Infrastruktur & Port Aktif di VPS
- **Port 80:** Nginx Web Server (`/var/www/html/`)
- **Port 8082:** HRIS Mitsindo (`hris.service` - FastAPI Backend)
- **Port 8085:** Lamar Coffee Multi-Page Website (`lamar-coffee.service`)
- **Port 3389:** XRDP Remote Desktop (Wine 10.0 & MetaTrader 5 - 24/7 Nonstop)

---
*Generated automatically during Hermes Master Backup.*
EOF

# 6. Backup Projects
echo "💻 Syncing Projects..."
rsync -av --delete \
  --exclude=".git" \
  /home/ubuntu/lamar_coffee_website/ "$BACKUP_DIR/projects/lamar_coffee/"

rsync -av --delete \
  --exclude="venv" \
  --exclude=".env" \
  --exclude="__pycache__" \
  --exclude="static/uploads" \
  --exclude="*.db" \
  /home/ubuntu/hris/ "$BACKUP_DIR/projects/hris/"

cp -f /home/ubuntu/*.py "$BACKUP_DIR/projects/scripts/" 2>/dev/null || true

# 7. Backup System Configurations
echo "⚙️ Syncing System Service Configs..."
cp -f /etc/systemd/system/lamar-coffee.service "$BACKUP_DIR/system_configs/systemd/" 2>/dev/null || true
cp -f /etc/systemd/system/hris.service "$BACKUP_DIR/system_configs/systemd/" 2>/dev/null || true
cp -rf /etc/nginx/sites-available "$BACKUP_DIR/system_configs/nginx/" 2>/dev/null || true

# 8. Git Commit & Push
cd "$BACKUP_DIR"

if [ ! -d ".git" ]; then
    git init -b main
fi

git config user.name "Hermes Agent"
git config user.email "kejuberlapis@gmail.com"
git config core.sshCommand "ssh -i $SSH_KEY -o StrictHostKeyChecking=accept-new"

git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"

git add -A
if git diff --staged --quiet; then
    echo "✓ No new changes to commit."
else
    git commit -m "Hermes Full Comprehensive Backup: Rules, Settings, Skills Catalog & MD Files — $TIMESTAMP"
    echo "✓ Committed successfully!"
fi

echo "🚀 Pushing Full Backup to GitHub: $REPO_URL..."
git push -u origin main

echo "=========================================================="
echo "🎉 SEMUA RULE, PENGATURAN, MD, & DAFTAR SKILL TELAH TERSINKRON!"
echo "=========================================================="
