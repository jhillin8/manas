#!/bin/bash
# Edge Cleanup Script - Remove development bloat and temp files

echo "🧹 Starting edge cleanup..."

# Clean Downloads folder of old installers  
echo "Cleaning Downloads..."
find ~/Downloads -name "*.dmg" -mtime +7 -delete 2>/dev/null
find ~/Downloads -name "*.zip" -mtime +14 -delete 2>/dev/null

# Clean development caches
echo "Cleaning development caches..."
npm cache clean --force 2>/dev/null || true

# Remove .DS_Store files from workspace areas
echo "Removing .DS_Store clutter..."  
find ~/workspace ~/code ~/Documents -name ".DS_Store" -delete 2>/dev/null

# Clean Docker if running
if docker info >/dev/null 2>&1; then
    echo "Cleaning Docker..."
    docker system prune -f >/dev/null 2>&1 || true
fi

echo "✅ Edge cleanup complete!"
