# Core Infrastructure

The core directory contains the fundamental components of the Manas system architecture.

## Directory Structure

- **mcp-central/**: Central MCP (Model Context Protocol) implementation and management
- **orchestrator/**: System orchestration and service coordination
- **agents/**: Agent registry and management system
- **context-broker/**: Context management and message brokering
- **router/**: Request routing and load balancing

## Key Components

### MCP Central
Manages all MCP server connections and protocol implementations. This was migrated from the root mcp-central directory.

### Orchestrator
Coordinates services, manages lifecycles, and handles system-wide operations.

### Agents
Contains the agent registry (agents.yaml) and manages agent lifecycle, discovery, and communication.

### Context Broker
Manages context passing between agents and services, handles state management.

### Router
Routes requests between services and manages load distribution.

## Configuration

The main configuration files are:
- `agents/agents.yaml`: Agent registry configuration
- `orchestrator/config.yaml`: Orchestration settings
- `mcp-central/servers.json`: MCP server configurations

## Getting Started

1. Ensure all services are properly configured
2. Start the orchestrator: `cd orchestrator && ./start.sh`
3. Agents will auto-register based on agents.yaml configuration
4. Monitor system health via the orchestrator dashboard