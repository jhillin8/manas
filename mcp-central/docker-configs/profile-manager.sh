#!/bin/bash

# Docker Resource Profile Manager for OpenMemory MCP

PROFILES_DIR="/Users/josephhillin/workspace/mcp-central/docker-configs"
CURRENT_PROFILE_FILE="$PROFILES_DIR/.current_profile"
OPENMEMORY_DIR="/Users/josephhillin/workspace/mem0/openmemory"

show_usage() {
    echo "🐳 Docker Resource Profile Manager"
    echo "=================================="
    echo ""
    echo "Usage: $0 [COMMAND] [PROFILE]"
    echo ""
    echo "Commands:"
    echo "  list                List available profiles"
    echo "  current            Show current active profile"
    echo "  switch [PROFILE]   Switch to specified profile"
    echo "  auto               Enable automatic profile switching"
    echo "  status             Show resource usage and recommendations"
    echo ""
    echo "Profiles:"
    echo "  low_power          Battery-saving configuration"
    echo "  balanced           Standard development setup"
    echo "  high_performance   Maximum performance configuration"
}

get_current_profile() {
    if [ -f "$CURRENT_PROFILE_FILE" ]; then
        cat "$CURRENT_PROFILE_FILE"
    else
        echo "balanced"  # default
    fi
}

switch_profile() {
    local target_profile="$1"
    
    if [ -z "$target_profile" ]; then
        echo "❌ Profile name required"
        show_usage
        exit 1
    fi
    
    echo "🔄 Switching to profile: $target_profile"
    echo "==============================="
    echo "$target_profile" > "$CURRENT_PROFILE_FILE"
    echo "✅ Profile switched to $target_profile"
}

show_status() {
    echo "📊 Docker Resource Status"
    echo "========================="
    
    current_profile=$(get_current_profile)
    echo "🏷️  Current profile: $current_profile"
    echo ""
    
    # Show basic system info
    echo "💻 System Resources:"
    if command -v free &> /dev/null; then
        echo "Memory: $(free -h | grep Mem | awk '{print $3 "/" $2}')"
    fi
    
    # Battery status (macOS)
    if command -v pmset &> /dev/null; then
        battery_level=$(pmset -g batt | grep -Eo "\d+%" | head -1)
        echo "🔋 Battery: $battery_level"
    fi
}

# Main command handling
case "$1" in
    "list")
        echo "📋 Available Docker Resource Profiles:"
        echo "======================================"
        echo "• low_power          - Battery-saving configuration"
        echo "• balanced           - Standard development setup"  
        echo "• high_performance   - Maximum performance configuration"
        ;;
    "current")
        echo "Current profile: $(get_current_profile)"
        ;;
    "switch")
        switch_profile "$2"
        ;;
    "status")
        show_status
        ;;
    *)
        show_usage
        ;;
esac
