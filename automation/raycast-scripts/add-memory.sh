#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Add Memory to MCP
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 🧠
# @raycast.description Quick add memory entry to OpenMemory MCP
# @raycast.argument1 { "type": "text", "placeholder": "Memory content" }
# @raycast.argument2 { "type": "dropdown", "placeholder": "Category", "data": [{"title": "Active Project", "value": "project_active"}, {"title": "Technical Knowledge", "value": "knowledge_technical"}, {"title": "Coding Preference", "value": "preferences_coding"}] }

MEMORY_CONTENT="$1"
CATEGORY="${2:-knowledge_technical}"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
MEMORY_FILE="/Users/josephhillin/workspace/mcp-central/memory-seeds/pending_memories.jsonl"

echo "🧠 Adding Memory to MCP..."
echo "=========================="

if [ -z "$MEMORY_CONTENT" ]; then
    echo "❌ Memory content is required"
    exit 1
fi

# Save to pending file
echo "{\"timestamp\": \"$TIMESTAMP\", \"category\": \"$CATEGORY\", \"content\": \"$MEMORY_CONTENT\", \"source\": \"raycast\", \"status\": \"pending\"}" >> "$MEMORY_FILE"

echo "✅ Memory added successfully!"
echo "📁 Category: $CATEGORY"
echo "📝 Content: $MEMORY_CONTENT"
echo "🕒 Timestamp: $TIMESTAMP"
echo ""
echo "💡 Memory will be processed when MCP server is running"
