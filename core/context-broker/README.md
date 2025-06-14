# Context Broker

The Context Broker manages context passing and state synchronization across the Manas system.

## Core Functions

- **Context Management**: Maintains and distributes context between agents
- **Message Brokering**: Handles inter-agent communication
- **State Synchronization**: Ensures consistent state across services
- **Event Distribution**: Publishes and subscribes to system events

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Agents    │────▶│   Context   │────▶│   Router    │
└─────────────┘     │   Broker    │     └─────────────┘
                    └─────────────┘
                           │
                    ┌─────────────┐
                    │ State Store │
                    └─────────────┘
```

## Message Protocol

Uses MCP (Model Context Protocol) for communication with:
- Request/Response patterns
- Pub/Sub for events
- State synchronization messages

## Configuration

- `broker.yaml`: Main configuration
- `topics.yaml`: Topic definitions
- `security.yaml`: Authentication and authorization

## API

- WebSocket endpoint for real-time communication
- REST API for context queries
- gRPC for high-performance agent communication

## Integration Points

- Orchestrator: Service registration and health
- Agents: Message routing and context sharing
- Router: Load balancing and failover
- State Store: Persistent context storage