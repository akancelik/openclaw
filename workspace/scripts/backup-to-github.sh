#!/bin/bash
# Daily backup script for OpenClaw to GitHub (excludes secrets)

# Configuration
BACKUP_DIR="/data/.openclaw-backup"
WORK_TREE="/data/.openclaw-backup"

# Create backup directory if not exists
mkdir -p /data/.openclaw-backup

# Initialize git repo if not exists
if [ ! -d "$GIT_DIR" ]; then
    cd /data/.openclaw-backup || exit 1
    git init
    git config user.name "Neo"
    git config user.email "neo@openclaw.local"
else
    cd /data/.openclaw-backup || exit 1
fi

# Sync files (exclude secrets!)
rsync -av --delete \
    --exclude='node_modules' \
    --exclude='.git' \
    --exclude='*.log' \
    --exclude='session-*' \
    --exclude='*.lock' \
    --exclude='openclaw.json' \
    --exclude='openclaw.json.*' \
    --exclude='agents/main/agent/auth-profiles.json' \
    --exclude='agents/main/sessions/*.jsonl' \
    --exclude='workspace/client_secret.json' \
    --exclude='workspace/.clawhub' \
    --exclude='browser/' \
    --exclude='identity/' \
    --exclude='credentials/' \
    --exclude='telegram/' \
    --exclude='media/' \
    /data/.openclaw/ /data/.openclaw-backup/

# Add all files
git add -A

# Commit with timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
git commit -m "Backup: $TIMESTAMP" || exit 0

# Push to GitHub (using token from remote)
git push origin master

echo "Backup completed: $TIMESTAMP"
