# MANAS System Documentation

## Overview

Manas is an autonomous AI system built on a distributed agent architecture with multi-modal memory, knowledge synthesis, and emergent intelligence capabilities.

## Directory Structure

```
manas/
├── core/                    # Core infrastructure components
│   ├── mcp-central/        # MCP server management (migrated)
│   ├── orchestrator/       # Service orchestration
│   ├── agents/            # Agent registry and management
│   ├── context-broker/    # Context distribution
│   └── router/           # Request routing
│
├── memory/                 # Multi-modal memory system
│   ├── active/           # Active memories
│   ├── archive/          # Archived memories
│   ├── policies/         # Temporal policies
│   ├── seeds/           # Memory templates
│   ├── graph/           # Graph relationships
│   ├── vision/          # Visual memories
│   ├── audio/           # Audio memories
│   ├── code/            # Code memories
│   └── timeline/        # Temporal organization
│
├── wisdom/                # Knowledge consolidation
│   ├── patterns/        # Discovered patterns
│   ├── insights/        # Generated insights
│   ├── research/        # Research findings
│   ├── documentation/   # System docs
│   └── meta/           # Meta-knowledge
│
├── forge/                # Project workspace
│   ├── active/         # Active projects
│   ├── experiments/    # Experiments
│   ├── templates/      # Project templates
│   └── archived/       # Archived projects
│
├── cascade/             # Information processing
│   ├── incoming/       # Raw input
│   ├── synthesis/      # Knowledge synthesis
│   ├── emergence/      # Emergent patterns
│   └── automation/     # Automated workflows
│
├── infrastructure/      # Deployment and operations
│   ├── docker/        # Container configs
│   ├── environments/  # Environment configs
│   ├── security/      # Security policies
│   ├── monitoring/    # Monitoring setup
│   └── observability/ # Logs and traces
│
├── protocols/          # Communication protocols
│   ├── mcp/          # Model Context Protocol
│   ├── a2a/          # Agent-to-Agent
│   ├── acp/          # Agent Control
│   ├── anp/          # Agent Negotiation
│   └── adapters/     # Protocol adapters
│
├── automation/        # Automation scripts
└── claude/           # Claude-specific configs
```

## Quick Start

### 1. Start Infrastructure
```bash
cd infrastructure/docker
docker-compose up -d
```

### 2. Initialize Core Services
```bash
cd core/orchestrator
./start.sh
```

### 3. Verify Health
```bash
curl http://localhost:8080/health
```

## Core Components

### Orchestrator
Central coordination service managing:
- Service lifecycle
- Health monitoring
- Resource allocation
- Event coordination

### Context Broker
Manages context distribution:
- Inter-agent communication
- State synchronization
- Event pub/sub
- Message routing

### Agent Registry
Manages autonomous agents:
- Agent discovery
- Capability registration
- Lifecycle management
- Communication protocols

### Memory System
Multi-modal temporal memory:
- Active/archive separation
- Policy-based retention
- Graph relationships
- Multi-modal support

### Wisdom System
Knowledge synthesis and insights:
- Pattern recognition
- Insight generation
- Research integration
- Living documentation

## Development

### Creating a New Agent
1. Define in `core/agents/agents.yaml`
2. Implement agent interface
3. Register capabilities
4. Deploy via orchestrator

### Adding a Project
1. Use template from `forge/templates/`
2. Create in `forge/active/`
3. Configure integrations
4. Build and deploy

### Storing Knowledge
1. Create memory with appropriate type
2. Apply temporal policies
3. Extract patterns to wisdom
4. Document insights

## Configuration

### Environment Variables
- `MANAS_ENV`: Environment (dev/staging/prod)
- `LOG_LEVEL`: Logging level
- Service-specific vars in docker-compose

### Key Configuration Files
- `core/agents/agents.yaml`: Agent registry
- `memory/policies/temporal-policies.yaml`: Memory policies
- `infrastructure/docker/docker-compose.yaml`: Service definitions
- `protocols/*/protocol-spec.yaml`: Protocol specifications

## Monitoring

### Dashboards
- Grafana: http://localhost:3000
- Jaeger: http://localhost:16686
- Prometheus: http://localhost:9091

### Health Endpoints
- Orchestrator: http://localhost:8080/health
- Context Broker: http://localhost:8081/health
- Router: http://localhost:8082/health
- Memory Service: http://localhost:8083/health

## API Reference

### Core APIs
- Orchestrator API: Port 8080
- Context Broker API: Port 8081
- Router API: Port 8082
- Memory API: Port 8083

### Protocol Endpoints
- MCP: WebSocket/HTTP/gRPC
- A2A: gRPC/NATS/Kafka
- REST: HTTP with JSON

## Security

### Authentication
- Service-to-service: mTLS
- External: API keys/OAuth2
- Admin: Strong passwords + MFA

### Network Security
- TLS for external communication
- Network isolation
- Firewall rules
- Rate limiting

## Troubleshooting

### Common Issues
1. Service won't start: Check logs
2. Connection errors: Verify network
3. Memory issues: Check limits
4. Performance: Review metrics

### Debug Commands
```bash
# View logs
docker-compose logs <service>

# Check service status
docker-compose ps

# Enter container
docker exec -it <container> /bin/sh

# View metrics
curl http://localhost:8080/metrics
```

## Contributing

### Code Standards
- Follow language-specific guidelines
- Write comprehensive tests
- Document all changes
- Update relevant configs

### Submission Process
1. Create feature branch
2. Implement changes
3. Run tests
4. Update documentation
5. Submit pull request

## Migration Notes

### Recent Changes (Directory Reorganization)
- `mcp-central/` → `core/mcp-central/`
- `projects/active/*` → `forge/active/*`
- `knowledge-base/*` → `wisdom/patterns/*`
- `Cascade/research` → `cascade/synthesis/research`

### Deprecated Paths
- `/projects` (use `/forge`)
- `/knowledge-base` (use `/wisdom`)

## Version History

- v1.0.0: Initial Manas architecture
- v2.0.0: Directory reorganization
- Current: v2.0.0

## Support

For issues or questions:
1. Check documentation in `/wisdom/documentation/`
2. Review logs and metrics
3. Consult runbooks
4. Contact system administrators