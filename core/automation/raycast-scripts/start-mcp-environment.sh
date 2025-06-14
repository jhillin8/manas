#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Start MCP Environment
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 🚀
# @raycast.description Start OpenMemory MCP and all required services

MCP_HOME="/Users/josephhillin/workspace/mcp-central"

echo "🚀 Starting MCP Environment..."
echo "=============================="

# Load environment variables
if [ -f "$MCP_HOME/.env.master" ]; then
    source "$MCP_HOME/.env.master"
    echo "✅ Loaded environment configuration"
else
    echo "❌ Environment file not found"
    exit 1
fi

# Check Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker not running. Starting Docker Desktop..."
    open -a "Docker Desktop"
    sleep 30
fi

# Start OpenMemory if directory exists
OPENMEMORY_DIR="/Users/josephhillin/workspace/mem0/openmemory"
if [ -d "$OPENMEMORY_DIR" ]; then
    cd "$OPENMEMORY_DIR"
    echo "🔄 Starting OpenMemory services..."
    make up && make ui &
    
    echo "🎉 MCP Started!"
    echo "📊 Dashboard: http://localhost:3000"
    echo "🔗 MCP Server: http://localhost:8765"
else
    echo "❌ OpenMemory not found. Please install first."
fi
