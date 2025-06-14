# Memory System

The memory system provides multi-modal, temporal memory management for the Manas architecture.

## Directory Structure

- **active/**: Currently active memories with fast access
- **archive/**: Compressed historical memories
- **policies/**: Temporal policies and governance rules  
- **seeds/**: Memory initialization templates
- **graph/**: Graph-based memory relationships
- **vision/**: Visual memory storage and embeddings
- **audio/**: Audio memory transcripts and embeddings
- **code/**: Code understanding and pattern memory
- **timeline/**: Temporal memory organization

## Memory Types

### Episodic Memory
Short-term memories of specific events and experiences with temporal context.

### Semantic Memory
Long-term conceptual knowledge, facts, and relationships.

### Procedural Memory
Knowledge of how to perform tasks and procedures.

### Multi-Modal Memory
Memories that span multiple modalities (vision, audio, code).

## Key Features

- **Temporal Policies**: Automatic archival and cleanup based on age and access patterns
- **Multi-Modal Support**: Native support for text, vision, audio, and code
- **Graph Relationships**: Memory items connected in a knowledge graph
- **Memory Seeds**: Templates for consistent memory initialization
- **Compression**: Progressive compression for archived memories
- **Privacy Controls**: Built-in anonymization and redaction

## Configuration

Key configuration files:
- `policies/temporal-policies.yaml`: Retention and archival rules
- `seeds/memory-seeds.yaml`: Memory initialization templates
- `graph/config.yaml`: Graph database configuration

## Integration

The memory system integrates with:
- **Agents**: For memory storage and retrieval
- **Context Broker**: For memory-aware context passing
- **Vector Databases**: For similarity search
- **Graph Databases**: For relationship queries

## Usage

1. Initialize memories using seed templates
2. Store in active memory for fast access
3. Automatic archival based on policies
4. Query via graph or vector search
5. Restore from archive on access