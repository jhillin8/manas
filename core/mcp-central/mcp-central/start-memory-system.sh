#!/bin/bash
"""
Cross-Agent Memory Intelligence System - Universal Startup Script
One script to rule them all - handles installation, configuration, and startup
"""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
MCP_CENTRAL_DIR="/Users/josephhillin/workspace/mcp-central"
PYTHON_EXEC="python3"
VENV_DIR="$MCP_CENTRAL_DIR/.venv"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}$1${NC}"
}

# Check if running as executable script
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    SCRIPT_MODE="bash"
else
    SCRIPT_MODE="python"
fi

print_header "🧠 Cross-Agent Memory Intelligence System"
print_header "========================================="

# Check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_warning "Docker not found - some features may be limited"
    fi
    
    # Check Node.js (for LangFlow)
    if ! command -v node &> /dev/null; then
        print_warning "Node.js not found - LangFlow may not work properly"
    fi
    
    print_success "System requirements check complete"
}

# Setup Python virtual environment
setup_venv() {
    print_status "Setting up Python virtual environment..."
    
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR"
        print_success "Created virtual environment at $VENV_DIR"
    fi
    
    source "$VENV_DIR/bin/activate"
    
    # Install required packages
    pip install --upgrade pip
    pip install -r "$MCP_CENTRAL_DIR/requirements.txt" 2>/dev/null || {
        print_status "Installing core dependencies..."
        pip install asyncio aiohttp networkx sqlite3 psutil pyyaml
        pip install langflow qdrant-client openai anthropic
    }
    
    print_success "Virtual environment ready"
}

# Install OpenMemory MCP if not present
install_openmemory() {
    print_status "Checking OpenMemory MCP installation..."
    
    if [ ! -d "/Users/josephhillin/.mem0" ]; then
        print_status "Installing OpenMemory MCP..."
        pip install mem0ai
        print_success "OpenMemory MCP installed"
    else
        print_success "OpenMemory MCP already installed"
    fi
}

# Run integration tests
run_tests() {
    print_status "Running integration tests..."
    
    cd "$MCP_CENTRAL_DIR"
    python3 integration-tests.py
    
    if [ $? -eq 0 ]; then
        print_success "All integration tests passed!"
    else
        print_warning "Some integration tests failed - system may have issues"
    fi
}

# Start the orchestrator
start_orchestrator() {
    print_status "Starting Cross-Agent Memory Intelligence System..."
    
    cd "$MCP_CENTRAL_DIR"
    python3 orchestrator.py &
    ORCHESTRATOR_PID=$!
    
    echo $ORCHESTRATOR_PID > "$MCP_CENTRAL_DIR/.orchestrator.pid"
    print_success "Orchestrator started with PID: $ORCHESTRATOR_PID"
}

# Stop the system
stop_system() {
    print_status "Stopping Cross-Agent Memory Intelligence System..."
    
    if [ -f "$MCP_CENTRAL_DIR/.orchestrator.pid" ]; then
        PID=$(cat "$MCP_CENTRAL_DIR/.orchestrator.pid")
        if kill -0 $PID 2>/dev/null; then
            kill $PID
            print_success "Orchestrator stopped"
        fi
        rm -f "$MCP_CENTRAL_DIR/.orchestrator.pid"
    fi
    
    # Stop Docker services
    if [ -f "$MCP_CENTRAL_DIR/docker-compose.yaml" ]; then
        docker-compose -f "$MCP_CENTRAL_DIR/docker-compose.yaml" down
        print_success "Docker services stopped"
    fi
}

# Check system status
check_status() {
    print_status "Checking system status..."
    
    # Check orchestrator
    if [ -f "$MCP_CENTRAL_DIR/.orchestrator.pid" ]; then
        PID=$(cat "$MCP_CENTRAL_DIR/.orchestrator.pid")
        if kill -0 $PID 2>/dev/null; then
            print_success "Orchestrator running (PID: $PID)"
        else
            print_warning "Orchestrator PID file exists but process not running"
        fi
    else
        print_warning "Orchestrator not running"
    fi
    
    # Check Docker services
    if command -v docker &> /dev/null; then
        if docker ps | grep -q "postgres\|qdrant"; then
            print_success "Docker services running"
        else
            print_warning "Docker services not running"
        fi
    fi
    
    # Check LangFlow
    if curl -s http://localhost:7860/health &> /dev/null; then
        print_success "LangFlow running"
    else
        print_warning "LangFlow not responding"
    fi
}

# Sync Raycast configurations
sync_raycast() {
    print_status "Syncing Raycast configurations..."
    
    cd "$MCP_CENTRAL_DIR"
    python3 -c "
from raycast_config_registry import RaycastConfigRegistry
registry = RaycastConfigRegistry()
discovered = registry.auto_discover_components()
sync_result = registry.sync_to_raycast()
print(f'Discovered: {discovered}')
print(f'Sync result: {sync_result}')
"
    
    print_success "Raycast configurations synced"
}

# Show usage information
show_usage() {
    echo ""
    print_header "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  install     - Install and setup the system"
    echo "  start       - Start the system"
    echo "  stop        - Stop the system" 
    echo "  restart     - Restart the system"
    echo "  status      - Check system status"
    echo "  test        - Run integration tests"
    echo "  sync        - Sync Raycast configurations"
    echo "  cli         - Open interactive CLI"
    echo "  help        - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 install   # First time setup"
    echo "  $0 start     # Start all services"
    echo "  $0 cli add --content 'My memory' --category knowledge_technical"
    echo ""
}

# Interactive CLI mode
interactive_cli() {
    print_status "Starting interactive CLI mode..."
    print_status "Type 'help' for commands, 'exit' to quit"
    
    cd "$MCP_CENTRAL_DIR"
    
    while true; do
        echo -n -e "${CYAN}memory-cli>${NC} "
        read -r input
        
        if [ "$input" = "exit" ] || [ "$input" = "quit" ]; then
            break
        elif [ "$input" = "help" ]; then
            python3 bin/memory-cli.py --help
        elif [ -n "$input" ]; then
            python3 bin/memory-cli.py $input
        fi
    done
}

# Main script logic
case "${1:-help}" in
    "install")
        check_requirements
        setup_venv
        install_openmemory
        run_tests
        print_success "Installation complete!"
        print_status "Run '$0 start' to start the system"
        ;;
    
    "start")
        check_requirements
        setup_venv
        start_orchestrator
        sleep 5
        sync_raycast
        check_status
        print_success "System started successfully!"
        print_status "System logs: tail -f $MCP_CENTRAL_DIR/orchestrator.log"
        ;;
    
    "stop")
        stop_system
        print_success "System stopped"
        ;;
    
    "restart")
        stop_system
        sleep 2
        setup_venv
        start_orchestrator
        sleep 5
        check_status
        print_success "System restarted"
        ;;
    
    "status")
        check_status
        ;;
    
    "test")
        setup_venv
        run_tests
        ;;
    
    "sync")
        setup_venv
        sync_raycast
        ;;
    
    "cli")
        setup_venv
        if [ -z "$2" ]; then
            interactive_cli
        else
            # Pass remaining arguments to CLI
            shift
            cd "$MCP_CENTRAL_DIR"
            python3 bin/memory-cli.py "$@"
        fi
        ;;
    
    "help"|"--help"|"-h")
        show_usage
        ;;
    
    *)
        print_error "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac
