#!/bin/bash

# Git setup and push script for Beauty Haircut Generator
set -e

echo "=========================================="
echo "📦 Beauty Haircut — Git Setup & Push"
echo "=========================================="
cd "$(dirname "$0")"

git init
git add README.md backend.py start.sh package.json frontend/ requirements.txt .gitignore 2>/dev/null || true
git commit -m "Initial commit: Beauty Haircut Generator with Qwen Image 2.1"
git branch -M main
git remote add origin https://github.com/magzumAlmat/beautyHaircut.git 2>/dev/null || echo "Remote already exists or failed (maybe auth needed)"
git push -u origin main

echo ""
echo "✅ Git setup complete!"