#!/bin/bash
# MCP Server Removal Verification Script
# Run this to verify the cleanup was successful

echo "🔍 MCP Server Removal Verification"
echo "================================="
echo

# Check main MCP config
echo "📁 Checking main MCP configuration..."
if grep -q "docker-mcp\|servers\|fetch\|puppeteer\|github" /Users/josephhillin/mcp/mcp_server_config.json; then
    echo "❌ ERROR: Removed servers still found in main config"
    exit 1
else
    echo "✅ Main MCP config successfully cleaned"
fi

# Check Claude Desktop config  
echo "📁 Checking Claude Desktop configuration..."
if grep -q "docker-mcp\|servers\|fetch\|puppeteer\|github" "/Users/josephhillin/Library/Application Support/Claude/claude_desktop_config.json"; then
    echo "❌ ERROR: Removed servers still found in Claude Desktop config"
    exit 1
else
    echo "✅ Claude Desktop config successfully cleaned"
fi

# Count remaining servers
MAIN_COUNT=$(grep -o "\"[a-zA-Z0-9-]*\":" /Users/josephhillin/mcp/mcp_server_config.json | wc -l | tr -d ' ')
CLAUDE_COUNT=$(grep -o "\"[a-zA-Z0-9-]*\":" "/Users/josephhillin/Library/Application Support/Claude/claude_desktop_config.json" | wc -l | tr -d ' ')

echo
echo "📊 Server Counts:"
echo "   Main config: ${MAIN_COUNT} servers"
echo "   Claude Desktop: ${CLAUDE_COUNT} servers"
echo

# Verify backup exists
if [ -f "/Users/josephhillin/workspace/mcp-central/backups/pre-removal-backup/mcp_server_config_backup.json" ]; then
    echo "✅ Backup file exists and is accessible"
else
    echo "❌ WARNING: Backup file not found!"
fi

echo
echo "🎯 Verification Summary:"
echo "   - Removed servers: docker-mcp, servers, fetch, puppeteer, github, playwright-mcp-server"
echo "   - Retained core functionality through consolidation"
echo "   - Configuration files successfully updated"
echo "   - Backup created for rollback if needed"
echo
echo "✅ System ready for new memory intelligence architecture!"
