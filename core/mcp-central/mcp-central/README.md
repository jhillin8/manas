# Cross-Agent Memory Intelligence System

A comprehensive, multi-agent memory management system that provides intelligent memory storage, retrieval, and collaboration across AI tools and human workflows.

## 🧠 System Overview

The Cross-Agent Memory Intelligence System unifies memory management across multiple AI agents, tools, and human interfaces. It provides:

- **Agent-Orchestrated Memory Lifecycle** - Automated memory validation, categorization, and maintenance
- **Temporal Intelligence Layer** - Time-aware memory relevance and decay modeling  
- **Graph View & Relationship Intelligence** - Visual memory relationships and semantic connections
- **Zero Trust Security** - Complete audit trails and rollback capabilities
- **Team Collaboration** - Secure multi-user memory sharing with access controls
- **Universal Integration** - Works with Raycast, CLI, MCP servers, and LangFlow

## 🚀 Quick Start

### Installation

```bash
# Clone and setup the system
cd /Users/josephhillin/workspace/mcp-central
./start-memory-system.sh install
```

### Starting the System

```bash
# Start all services with balanced resource profile
./start-memory-system.sh start

# Check system status
./start-memory-system.sh status
```

### Using the CLI

```bash
# Add a memory
./start-memory-system.sh cli add --content "How to implement async/await in Python" --category knowledge_technical --tags python async performance

# Search memories
./start-memory-system.sh cli search --query "Python async" --limit 5

# View review queue
./start-memory-system.sh cli review

# Export memory graph
./start-memory-system.sh cli export --output memory-graph.json
```

### Interactive CLI Mode

```bash
./start-memory-system.sh cli
memory-cli> add --content "My memory" --category knowledge_technical
memory-cli> search --query "memory"
memory-cli> exit
```

## 📁 System Architecture

```
mcp-central/
├── agents/                     # AI agents and processors
│   ├── memory-steward/        # Memory lifecycle management
│   └── temporal-engine/       # Time-aware intelligence
├── graph/                     # Memory relationship management
├── security/                  # Audit and security systems
├── team/                      # Multi-user collaboration
├── langflow/                  # LangFlow-MCP integration
├── docker-configs/            # Resource profiles and containers
├── memory-policies/           # Schemas and validation rules
├── memory-seeds/              # Enhanced validation and history
├── bin/                       # CLI and utility scripts
└── orchestrator.py           # System orchestration
```

## 🔧 Core Components

### 1. Memory Steward Agent
Manages the complete memory lifecycle:
- **Validation**: Schema compliance and quality assessment
- **Enhancement**: Tag normalization and relationship extraction  
- **Lifecycle**: Relevance decay modeling and archival recommendations

**Configuration**: `agents/memory-steward/config.yaml`

### 2. Temporal Intelligence Engine
Provides time-aware memory management:
- **Access Tracking**: Records when and how memories are accessed
- **Relevance Scoring**: Dynamic relevance based on usage patterns
- **Decay Modeling**: Configurable staleness factors and half-life calculations
- **Review Queues**: Identifies forgotten gems and trending memories

**Script**: `agents/temporal-engine/temporal-processor.py`

### 3. Graph Relationship Service  
Manages memory connections and visualizations:
- **Relationship Mapping**: Semantic connections between memories
- **Graph Visualization**: D3.js compatible exports
- **Related Memory Discovery**: Multi-hop relationship traversal
- **Visual Analytics**: Memory clusters and influence mapping

**Service**: `graph/memory-graph-service.py`

### 4. Security & Audit System
Provides zero-trust security with complete auditability:
- **Operation Logging**: Every memory operation is logged
- **Content Hashing**: Integrity verification for all memories
- **Suspicious Activity Detection**: Automated threat detection
- **Rollback Capabilities**: Complete history and recovery

**System**: `security/audit-system.py`

### 5. Team Memory Manager
Enables secure multi-user collaboration:
- **Access Controls**: Granular permission management (read/write/admin/owner)
- **Share Scopes**: Personal, team, organization, and public sharing
- **Collaboration Tracking**: Team contributions and annotations
- **Temporal Access Policies**: Time-limited sharing with expiration

**Manager**: `team/team-memory-manager.py`

## 🔌 Integrations

### LangFlow Integration
- **MCP Bridge**: Exposes LangFlow workflows as MCP-compatible tools
- **Flow Orchestration**: Automated deployment and management of memory flows
- **Validation Workflows**: Complex memory processing pipelines

**Bridge**: `langflow/memory-mcp-bridge.py`

### Raycast Integration
- **Unified Commands**: All memory operations available in Raycast
- **Auto-Discovery**: Automatic detection and registration of MCP servers
- **Configuration Sync**: Centralized config management for all extensions

**Registry**: `raycast-config-registry.py`

### CLI Integration
- **Full Feature Access**: Complete memory system access via command line
- **Scripting Support**: Automation-friendly interface
- **Interactive Mode**: Real-time memory management shell

**CLI**: `bin/memory-cli.py`

## ⚙️ Resource Profiles

The system supports three resource profiles for different usage scenarios:

### Low Power
- **Memory**: 2GB limit
- **CPU**: 1.0 core
- **Use Case**: Battery-saving for mobile work

### Balanced (Default)
- **Memory**: 4GB limit  
- **CPU**: 2.0 cores
- **Use Case**: Standard development work

### High Performance
- **Memory**: 8GB limit
- **CPU**: 4.0 cores
- **Use Case**: Intensive AI workloads

**Configuration**: `docker-configs/resource-profiles.yaml`

## 🛠️ Commands Reference

### System Management
```bash
./start-memory-system.sh install    # First-time setup
./start-memory-system.sh start      # Start all services
./start-memory-system.sh stop       # Stop all services  
./start-memory-system.sh restart    # Restart the system
./start-memory-system.sh status     # Check system health
./start-memory-system.sh test       # Run integration tests
./start-memory-system.sh sync       # Sync Raycast configs
```

### Memory Operations
```bash
# Add memories
./start-memory-system.sh cli add --content "Content" --category "knowledge_technical" --tags tag1 tag2

# Search memories  
./start-memory-system.sh cli search --query "search term" --category "knowledge_technical" --limit 10

# Review queue
./start-memory-system.sh cli review

# Export graph
./start-memory-system.sh cli export --output graph.json

# Health check
./start-memory-system.sh cli health
```

## 📊 Memory Categories

The system supports structured memory categorization:

### Project Active
- **Retention**: 90 days
- **Decay Rate**: Fast (30-day half-life)  
- **Tags**: project_name, technology_stack, status
- **Use**: Current project work and active tasks

### Project Research
- **Retention**: 180 days
- **Decay Rate**: Medium (60-day half-life)
- **Tags**: research_topic, technology, priority
- **Use**: Research and evaluation work

### Knowledge Technical  
- **Retention**: Permanent
- **Decay Rate**: Very slow (365-day half-life)
- **Tags**: technology, use_case, complexity, source
- **Use**: Technical solutions and implementation knowledge

### Knowledge Business
- **Retention**: Permanent
- **Decay Rate**: Slow (270-day half-life)  
- **Tags**: industry, insight_type, confidence_level
- **Use**: Business insights and strategic knowledge

### Preferences Coding
- **Retention**: 365 days
- **Decay Rate**: Slow (180-day half-life)
- **Tags**: language, framework, pattern_type  
- **Use**: Coding preferences and style guidelines

## 🔍 Testing

### Integration Tests
```bash
./start-memory-system.sh test
```

Tests include:
- Component initialization
- Memory validation workflows
- Graph operations and relationships
- Temporal intelligence calculations
- Security and audit logging
- Team collaboration features
- LangFlow integration
- End-to-end workflows

### Manual Testing
```bash
# Test memory addition
./start-memory-system.sh cli add --content "Test memory for validation" --category knowledge_technical

# Test search functionality  
./start-memory-system.sh cli search --query "validation"

# Test review queue
./start-memory-system.sh cli review
```

## 📝 Configuration Files

### Main Configuration
- **Orchestrator**: `orchestrator-config.yaml` - System-wide settings
- **Resource Profiles**: `docker-configs/resource-profiles.yaml` - Performance tuning
- **Memory Schema**: `memory-policies/temporal-schema.yaml` - Memory structure and policies

### Agent Configuration
- **Memory Steward**: `agents/memory-steward/config.yaml` - Lifecycle management
- **Temporal Engine**: `memory-policies/temporal-schema.yaml` - Time intelligence

### Integration Configuration  
- **Raycast Registry**: `raycast-config-registry.json` - Extension management
- **MCP Bridge**: `langflow/memory-mcp-bridge.py` - LangFlow integration

## 🔧 Troubleshooting

### System Won't Start
```bash
# Check system status
./start-memory-system.sh status

# Check logs
tail -f /Users/josephhillin/workspace/mcp-central/orchestrator.log

# Restart system
./start-memory-system.sh restart
```

### Docker Issues
```bash
# Check Docker services
docker ps

# Restart Docker services
docker-compose -f docker-compose.yaml restart
```

### LangFlow Connection Issues
```bash
# Check LangFlow status
curl http://localhost:7860/health

# Restart LangFlow manually
langflow run --host 0.0.0.0 --port 7860
```

### Memory Validation Failures
```bash
# Test validator directly
cd /Users/josephhillin/workspace/mcp-central
python3 memory-seeds/enhanced-validator.py
```

## 🔐 Security Features

- **Zero Trust Architecture**: Every operation is logged and verified
- **Content Integrity**: SHA-256 hashing for all memory content
- **Access Control**: Granular permissions for team collaboration
- **Audit Trail**: Complete history with rollback capabilities
- **Suspicious Activity Detection**: Automated threat monitoring

## 🚀 Performance Optimization

- **Resource Profiles**: Optimized configurations for different use cases
- **Intelligent Caching**: Temporal relevance-based memory prioritization
- **Background Processing**: Asynchronous operation for responsiveness
- **Database Optimization**: Efficient indexing and query patterns

## 🤝 Team Collaboration

- **Multi-User Support**: Secure sharing with access controls
- **Team Workspaces**: Isolated collaboration environments  
- **Contribution Tracking**: Attribution and collaboration history
- **Access Policies**: Flexible permission management

## 📈 Future Enhancements

- **Advanced ML Models**: Enhanced categorization and relationship detection
- **Real-time Collaboration**: Live editing and synchronization
- **Mobile Integration**: iOS/Android companion apps
- **Advanced Analytics**: Usage patterns and optimization recommendations
- **API Ecosystem**: Third-party integrations and extensions

## 📚 Related Documentation

- [Memory Schema Reference](memory-policies/temporal-schema.yaml)
- [API Documentation](docs/api-reference.md)
- [Development Guide](docs/development.md)
- [Deployment Guide](docs/deployment.md)

## 🔗 Integration Endpoints

- **LangFlow**: http://localhost:7860
- **Memory Graph API**: http://localhost:8767
- **Audit API**: http://localhost:8769
- **PostgreSQL**: localhost:5432
- **Qdrant Vector DB**: http://localhost:6333

## 💡 Tips & Best Practices

1. **Memory Quality**: Include specific, actionable content in memories
2. **Tagging Strategy**: Use consistent, hierarchical tag structures
3. **Regular Reviews**: Use the review queue to maintain memory relevance
4. **Team Sharing**: Establish clear sharing policies and access controls
5. **Performance Tuning**: Choose appropriate resource profiles for your workload

---

Built with ❤️ for seamless cross-agent memory intelligence.
