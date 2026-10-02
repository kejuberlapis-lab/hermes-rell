#!/bin/bash
set -e

BACKUP_DIR="/home/ubuntu/hermes_vps_backup"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S WIB")

echo "=========================================="
echo "Starting Hermes VPS Master Backup: $TIMESTAMP"
echo "=========================================="

mkdir -p "$BACKUP_DIR/vaults"
mkdir -p "$BACKUP_DIR/projects/lamar_coffee"
mkdir -p "$BACKUP_DIR/projects/hris"
mkdir -p "$BACKUP_DIR/projects/scripts"
mkdir -p "$BACKUP_DIR/skills"

# 1. Sync Obsidian Vaults (Excluding nested .git and huge files)
echo "📦 Syncing Obsidian Vaults..."
rsync -av --delete \
  --exclude=".git" \
  --exclude=".trash" \
  --exclude="*.zip" \
  --exclude="*.csv" \
  /home/ubuntu/ObsidianVault/ "$BACKUP_DIR/vaults/"

# 2. Sync Lamar Coffee Website
echo "☕ Syncing Lamar Coffee Website..."
rsync -av --delete \
  --exclude=".git" \
  /home/ubuntu/lamar_coffee_website/ "$BACKUP_DIR/projects/lamar_coffee/"

# 3. Sync HRIS Core Code (Excluding venv, uploads, .env)
echo "🏢 Syncing HRIS Mitsindo Code..."
rsync -av --delete \
  --exclude="venv" \
  --exclude=".env" \
  --exclude="__pycache__" \
  --exclude="static/uploads" \
  --exclude="*.db" \
  /home/ubuntu/hris/ "$BACKUP_DIR/projects/hris/"

# 4. Sync Standalone Automation Scripts
echo "⚙️ Syncing Core Scripts..."
mkdir -p "$BACKUP_DIR/projects/scripts"
cp -f /home/ubuntu/*.py "$BACKUP_DIR/projects/scripts/" 2>/dev/null || true

# 5. Sync Hermes Custom Skills
echo "🧠 Syncing Custom Skills..."
rsync -av --delete \
  --exclude="__pycache__" \
  /home/ubuntu/.hermes/profiles/profil-admin-mvp/skills/ "$BACKUP_DIR/skills/"

# 6. Git Commit & Push
cd "$BACKUP_DIR"

if [ ! -d ".git" ]; then
    echo "🔧 Initializing git repository..."
    git init -b main
    git config user.name "Hermes Agent"
    git config user.email "hermes@mitsindo.co.id"
    git config core.sshCommand "ssh -i /home/ubuntu/.ssh/id_ed25519_skripsi -o StrictHostKeyChecking=accept-new"
    git remote add origin git@github.com:StefanoGarrent/hermes-vps-backup.git 2>/dev/null || true
fi

git add -A
if git diff --staged --quiet; then
    echo "✓ No new changes to commit. Everything is up-to-date!"
else
    git commit -m "Hermes VPS Master Backup — $TIMESTAMP"
    echo "✓ Committed successfully!"
fi

echo "🚀 Pushing to GitHub (origin main)..."
if git push -u origin main; then
    echo "🎉 BACKUP SUCCESSFUL TO GITHUB!"
else
    echo "⚠️ Push failed: Make sure the repo 'StefanoGarrent/hermes-vps-backup' is created on GitHub and has write access for the deploy key."
fi
