#!/bin/bash
set -e

# ============================================================
# Rekanan Carousel - Deploy Script
#
# Usage: ./scripts/deploy.sh
# 
# Pipeline:
#   1. Generate carousel HTML (uses OUTPUT_FILE set in generate_carousel.py)
#   2. Commit to local git
#   3. Push to GitHub (triggers Cloudflare Pages auto-deploy)
#
# IMPORTANT:
#   - On dev1 (this server), generator outputs: carousel_dev.html
#   - On dev2 (prod server), change line 18 in generate_carousel.py
#     to output: carousel_prod.html
# ============================================================

PROJECT_DIR="/home/dev/rekanan-carousel"

cd "$PROJECT_DIR"

echo "=========================================="
echo "🚀 Deploying Carousel"
echo "=========================================="

# Step 1: Generate HTML
echo "[1/4] Generating carousel HTML..."
python3 scripts/generate_carousel.py

# Step 2: Check if git repo is initialized
if [ ! -d ".git" ]; then
    echo "[WARN] Git repository not initialized. Please run:"
    echo "       git init"
    echo "       git remote add origin <YOUR_GITHUB_REPO_URL>"
    exit 1
fi

# Step 3: Commit
echo "[2/4] Committing changes..."
git add outputs/
git add scripts/generate_carousel.py
git add .gitignore 2>/dev/null || true

# Only commit if there are staged changes
if git diff --cached --quiet; then
    echo "       No changes to commit."
else
    git commit -m "auto: update carousel $(date '+%Y-%m-%d %H:%M')"
    echo "       Committed."
fi

# Step 4: Push
echo "[3/4] Pushing to GitHub..."
git push origin main
echo "       Pushed."

echo "[4/4] ✅ Deploy complete!"
echo ""
echo "Cloudflare Pages will auto-deploy in ~30 seconds."
echo "Check your Cloudflare dashboard for the build status."
echo ""

exit 0
