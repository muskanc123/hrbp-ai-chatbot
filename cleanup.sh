#!/bin/bash

# Git Cleanup Script for HRBP AI Chatbot
# This script removes unnecessary files before pushing to Git

echo "🧹 Cleaning up unnecessary files..."

# Navigate to project directory
cd "$(dirname "$0")"

# Delete media files
echo "Deleting media files..."
rm -f "My HRBP Agent Experience.mp4"
rm -f "My HRBP Agent Screenshot 1.jpeg"
rm -f "image.png"
rm -f "image copy.png"

# Delete optional documentation
echo "Deleting redundant documentation..."
rm -f "UI_REDESIGN.md"
rm -f "QUICKSTART.md"

echo "✅ Cleanup complete!"
echo ""
echo "Files deleted:"
echo "  - My HRBP Agent Experience.mp4 (24MB)"
echo "  - My HRBP Agent Screenshot 1.jpeg"
echo "  - image.png"
echo "  - image copy.png"
echo "  - UI_REDESIGN.md"
echo "  - QUICKSTART.md"
echo ""
echo "📦 Repository is now ready for Git!"
echo ""
echo "Next steps:"
echo "1. git init"
echo "2. git add ."
echo "3. git commit -m 'Initial commit: HRBP AI Chatbot'"
echo "4. Create GitHub repo and push"
