#!/bin/bash
set -e

BACKUP_DIR="/home/ubuntu/hermes_vps_backup"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S WIB")
SSH_KEY="/home/ubuntu/.ssh/id_ed25519_vps_backup"
REPO_URL="git@github.com:kejuberlapis-lab/hermes-rell.git"

echo "=========================================="
echo "Starting Hermes VPS Master Backup: $TIMESTAMP"
echo "Target Repo: $REPO_URL"
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
fi

git config user.name "Hermes Agent"
git config user.email "kejuberlapis@gmail.com"
git config core.sshCommand "ssh -i $SSH_KEY -o StrictHostKeyChecking=accept-new"

# Set remote origin
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"

git add -A
if git diff --staged --quiet; then
    echo "✓ No new changes to commit. Everything is up-to-date!"
else
    git commit -m "Hermes VPS Master Backup — $TIMESTAMP"
    echo "✓ Committed successfully!"
fi

echo "🚀 Pushing to GitHub: $REPO_URL (branch main)..."
if git push -u origin main; then
    echo "🎉 BACKUP MASTER BERHASIL KE GITHUB: $REPO_URL!"
else
    echo "⚠️ Push failed: Pastikan Deploy Key sudah ditambahkan ke repo dengan write access."
fi
