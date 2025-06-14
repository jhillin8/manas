# MANAS System Documentation

## Overview

Manas is an autonomous AI system built on a distributed agent architecture with multi-modal memory, knowledge synthesis, and emergent intelligence capabilities.

## Directory Structure

```
manas/
├── core/                    # Core infrastructure components & MCP servers
│   ├── mcp-central/        # MCP server management
│   ├── awesome-mcp-servers/# MCP servers collection
│   ├── automation/        # Automation scripts
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
│   ├── knowledge-base/  # Migrated knowledge base
│   └── meta/           # Meta-knowledge
│
├── forge/                # Project workspace
│   ├── active/         # Active projects
│   ├── experiments/    # Experiments
│   ├── templates/      # Project templates
│   └── archived/       # Archived projects (including old projects/)
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

### MCP Server Ecosystem
Comprehensive Model Context Protocol integration:

**Anyquery**: Universal SQL interface for data access
- Query 40+ data sources via SQL
- MCP-enabled for LLM integration
- Plugin ecosystem for extensibility
- SQLite-compatible interface

**MetaMCP**: Unified MCP server management
- Centralized management for all MCP servers
- Multi-workspace context isolation
- Tool-level toggle functionality
- Prevents context pollution

**MindsDB**: AI/ML query engine
- SQL-based ML model integration
- Federated querying across data sources
- Built-in AI agents and knowledge bases
- MCP server for AI interactions

**Pipedream**: Workflow automation platform
- OAuth and credential management for 2,500+ apps
- Dynamic API request routing
- Workflow automation integration
- MCP-enabled third-party service access

**Pearl**: Human expert collaboration platform
- Transforms AI agents into collaborative systems
- Real-time human assistance integration
- Remote MCP server infrastructure
- Tool discovery and invocation capabilities

**Endgame**: AI agent deployment platform
- Rapid cloud deployment in ~10 seconds
- Automated testing and self-healing
- Unlimited simultaneous branch deployments
- Full-stack Node.js application support

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
- Anyquery: http://localhost:8102/health
- MetaMCP: http://localhost:3001/health
- MindsDB: http://localhost:47334/api/status
- Pipedream: http://localhost:3002/health
- Pearl: http://localhost:3003/health
- Endgame: http://localhost:3004/health

## API Reference

### Core APIs
- Orchestrator API: Port 8080
- Context Broker API: Port 8081
- Router API: Port 8082
- Memory API: Port 8083

### MCP Server APIs
- Anyquery: Port 8102 (SQL query engine)
- MetaMCP: Port 3001 (Unified MCP management)
- MindsDB: Port 47334/47335/47336 (AI/ML query engine)
- Pipedream: Port 3002 (Workflow automation)
- Pearl: Port 3003 (Human expert collaboration)
- Endgame: Port 3004 (AI agent deployment)

### Protocol Endpoints
- MCP: WebSocket/HTTP/gRPC
- A2A: gRPC/NATS/Kafka
- REST: HTTP with JSON
- SQL: Anyquery unified data access
- ML: MindsDB AI/ML operations
- Workflow: Pipedream automation

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