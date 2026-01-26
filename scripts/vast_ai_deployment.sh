#!/bin/bash
set -e  # exit on error

# -----------------------------
# Repo location
# -----------------------------
REPO_DIR="/workspace/repo"

# -----------------------------
# Pull latest repo to get deployment.sh and app
# -----------------------------
if [ -d "$REPO_DIR/.git" ]; then
    echo "Updating existing repo..."
    cd "$REPO_DIR"
    git reset --hard
    git clean -fd
    git pull
else
    echo "Cloning repo..."
    git clone "$GITHUB_REPO" "$REPO_DIR"
fi

# -----------------------------
# Run deployment script
# -----------------------------
bash "$REPO_DIR/deployment.sh"

echo "Startup complete."
