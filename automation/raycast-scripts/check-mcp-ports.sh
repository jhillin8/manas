#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Check MCP Ports
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 🔍
# @raycast.description Check if MCP required ports are available

echo "🔍 Checking MCP Required Ports..."
echo "================================="

# Array of ports to check
ports=(3000 8765 5432 6333)

for port in "${ports[@]}"; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "❌ Port $port is OCCUPIED"
        echo "   Process: $(lsof -Pi :$port -sTCP:LISTEN | tail -n +2)"
    else
        echo "✅ Port $port is AVAILABLE"
    fi
done

echo ""
echo "📋 Port Usage:"
echo "  3000 - OpenMemory Dashboard"
echo "  8765 - OpenMemory MCP Server"
echo "  5432 - PostgreSQL Database"
echo "  6333 - Qdrant Vector Database"
echo ""

if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1 || \
   lsof -Pi :8765 -sTCP:LISTEN -t >/dev/null 2>&1 || \
   lsof -Pi :5432 -sTCP:LISTEN -t >/dev/null 2>&1 || \
   lsof -Pi :6333 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Some ports are occupied. You may need to stop conflicting services."
    echo "💡 Use 'sudo lsof -ti:PORT | xargs sudo kill' to free a port"
else
    echo "🎉 All MCP ports are available! Ready for installation."
fi
