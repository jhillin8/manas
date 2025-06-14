#!/bin/bash
# Workflow automation: Setup development session with memory context

PROJECT_PATH="$1"
if [ -z "$PROJECT_PATH" ]; then
    echo "Usage: $0 <project-path>"
    exit 1
fi

PROJECT_NAME=$(basename "$PROJECT_PATH")
echo "🚀 Starting development session for $PROJECT_NAME"

# Inject project context into memory (when OpenMemory is available)
if [ -f "$PROJECT_PATH/.mcp-context" ]; then
    echo "📝 Loading project context..."
    # curl -s -X POST "http://localhost:8000/memories" -H "Content-Type: application/json" -d "..." >/dev/null
fi

# Open in Cursor with context
cursor "$PROJECT_PATH"

# Start any necessary services
if [ -f "$PROJECT_PATH/docker-compose.yml" ]; then
    echo "🐳 Starting Docker services..."
    cd "$PROJECT_PATH" && docker-compose up -d
fi

echo "✅ Development environment ready for $PROJECT_NAME"
