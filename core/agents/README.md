# Agents

The agents directory manages all agent registrations and configurations in the Manas system.

## Agent Registry

The main configuration file is `agents.yaml` which defines:
- Agent identities and capabilities
- Communication protocols
- Discovery settings
- Priority and startup configurations

## Agent Types

### System Agents
- Core Infrastructure Specialist
- Memory Architecture Specialist  
- Project Migration Specialist
- Knowledge Consolidation Specialist
- Infrastructure & Protocols Specialist

### Custom Agents
Custom agents can be registered by adding entries to agents.yaml with:
- Unique ID
- Capabilities list
- Configuration parameters

## Agent Lifecycle

1. **Registration**: Agents register via agents.yaml
2. **Discovery**: Automatic discovery based on capabilities
3. **Communication**: Via context broker using MCP protocol
4. **Health Monitoring**: Orchestrator monitors agent health
5. **Scaling**: Dynamic scaling based on load

## Development

To create a new agent:
1. Define agent in agents.yaml
2. Implement agent logic following the Agent interface
3. Register capabilities and endpoints
4. Deploy and monitor via orchestrator