#!/bin/bash
# Meta-Agent Startup Script (location-agnostic)
# Quick commands to manage the Meta-Agent monitoring system

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

show_help() {
    echo "🤖 Meta-Agent Control Panel"
    echo "=========================="
    echo "start    - Start monitoring daemon"
    echo "stop     - Stop monitoring daemon" 
    echo "status   - Check current status"
    echo "analyze  - Run single analysis cycle"
    echo "logs     - Show recent logs"
    echo "reset    - Reset monitoring state"
    echo "install  - Install dependencies"
    echo ""
}

start_monitoring() {
    echo "🚀 Starting Meta-Agent Monitor..."
    # Check if already running
    if pgrep -f "meta_agent_monitor.py" > /dev/null; then
        echo "⚠️  Meta-Agent is already running!"
        echo "Use './meta_agent.sh stop' to stop it first"
        return 1
    fi
    # Start in background
    nohup python3 "$SCRIPT_DIR/meta_agent_monitor.py" > "$SCRIPT_DIR/../logs/meta_agent.log" 2>&1 &
    echo $! > "$SCRIPT_DIR/../logs/meta_agent.pid"
    echo "✅ Meta-Agent Monitor started (PID: $(cat $SCRIPT_DIR/../logs/meta_agent.pid))"
    echo "📋 Logs: tail -f ../logs/meta_agent.log"
    echo "⛔ Stop: ./meta_agent.sh stop"
}

stop_monitoring() {
    echo "⛔ Stopping Meta-Agent Monitor..."
    if [ -f "$SCRIPT_DIR/../logs/meta_agent.pid" ]; then
        PID=$(cat "$SCRIPT_DIR/../logs/meta_agent.pid")
        if kill "$PID" 2>/dev/null; then
            echo "✅ Meta-Agent stopped (PID: $PID)"
        else
            echo "⚠️  Process $PID not found, cleaning up..."
        fi
        rm -f "$SCRIPT_DIR/../logs/meta_agent.pid"
    else
        pkill -f "meta_agent_monitor.py" && echo "✅ Meta-Agent stopped" || echo "⚠️  No running Meta-Agent found"
    fi
}

check_status() {
    echo "📊 Meta-Agent Status"
    echo "==================="
    if pgrep -f "meta_agent_monitor.py" > /dev/null; then
        PID=$(pgrep -f "meta_agent_monitor.py")
        echo "Status: 🟢 RUNNING (PID: $PID)"
        if [ -f "$SCRIPT_DIR/../logs/meta_agent_state.json" ]; then
            echo "Last Analysis: $(python3 -c "import json; data=json.load(open('$SCRIPT_DIR/../logs/meta_agent_state.json')); print(data.get('last_optimization', 'Never'))")"
            echo "Monitored Files: $(python3 -c "import json; data=json.load(open('$SCRIPT_DIR/../logs/meta_agent_state.json')); print(len(data.get('file_hashes', {})))")"
        fi
    else
        echo "Status: 🔴 STOPPED"
    fi
    echo ""
    if [ -f "$SCRIPT_DIR/../logs/meta_agent.log" ]; then
        echo "Recent Activity:"
        tail -5 "$SCRIPT_DIR/../logs/meta_agent.log" | sed 's/^/  /'
    fi
}

run_analysis() {
    echo "⚡ Running single analysis cycle..."
    python3 "$SCRIPT_DIR/meta_agent_monitor.py" --once
    if [ -f "$SCRIPT_DIR/../docs/meta_agent_prompt.md" ]; then
        echo ""
        echo "📋 Generated optimization prompt:"
        echo "   File: ../docs/meta_agent_prompt.md"
        echo "   Open in Claude Code for AI-driven optimization"
    fi
}

show_logs() {
    if [ -f "$SCRIPT_DIR/../logs/meta_agent.log" ]; then
        echo "📋 Meta-Agent Logs (last 20 lines):"
        echo "===================================="
        tail -20 "$SCRIPT_DIR/../logs/meta_agent.log"
    else
        echo "📋 No logs found. Start monitoring first."
    fi
}

reset_state() {
    echo "🔄 Resetting Meta-Agent state..."
    stop_monitoring
    rm -f "$SCRIPT_DIR/../logs/meta_agent_state.json"
    rm -f "$SCRIPT_DIR/../logs/meta_agent.log"  
    rm -f "$SCRIPT_DIR/../docs/meta_agent_prompt.md"
    echo "✅ State reset complete"
}

install_deps() {
    echo "📦 Installing Meta-Agent dependencies..."
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 not found. Please install Python 3.8+"
        return 1
    fi
    echo "✅ Python 3 found: $(python3 --version)"
    echo "✅ Meta-Agent ready to run"
    echo "🧪 Testing configuration..."
    python3 -c "import sys; sys.path.insert(0, '$SCRIPT_DIR'); from meta_agent_config import MetaAgentConfig; print('✅ Configuration OK')"
}

case "${1:-help}" in
    "start")    start_monitoring ;;
    "stop")     stop_monitoring ;;
    "status")   check_status ;;
    "analyze")  run_analysis ;;
    "logs")     show_logs ;;
    "reset")    reset_state ;;
    "install")  install_deps ;;
    "help"|*)   show_help ;;
esac
