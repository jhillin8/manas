# Orchestrator

The Orchestrator is the central coordination service for the Manas system.

## Responsibilities

- Service lifecycle management
- Health monitoring and recovery
- Resource allocation
- Event coordination
- System-wide state management

## Architecture

The orchestrator follows a microservices pattern with:
- Service registry
- Health checker
- Event bus
- State store
- API gateway

## Configuration

Configuration is managed through `config.yaml` with sections for:
- Service definitions
- Health check intervals
- Resource limits
- Scaling policies

## API Endpoints

- `GET /health` - System health status
- `GET /services` - List registered services
- `POST /services/{id}/restart` - Restart a service
- `GET /metrics` - System metrics

## Integration

The orchestrator integrates with:
- Agent registry for agent management
- Context broker for state synchronization
- Router for request distribution
- MCP Central for protocol handling