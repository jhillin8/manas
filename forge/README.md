# Forge

The Forge is where all projects are created, developed, and managed within the Manas system.

## Directory Structure

- **active/**: Currently active projects in development or production
- **experiments/**: Experimental projects and proof-of-concepts
- **templates/**: Project templates and scaffolding
- **archived/**: Completed or deprecated projects

## Project Lifecycle

### 1. Creation
New projects start from templates in `templates/` and are created in either `active/` or `experiments/`.

### 2. Development
Active development happens in `active/` with full integration to Manas services.

### 3. Experimentation
Quick prototypes and tests go in `experiments/` with relaxed constraints.

### 4. Archival
Completed or deprecated projects move to `archived/` with metadata preserved.

## Project Types

- **Web Applications**: Full-stack web applications
- **CLI Tools**: Command-line utilities and tools
- **Libraries**: Reusable code libraries
- **Services**: Microservices and APIs
- **Experiments**: Proof-of-concepts and prototypes

## Active Projects

Current projects in active development:
- target-spectrum
- rcr
- instagram-analyzer
- brooksie
- binary
- pola
- surface-tension
- westsidebis
- marypip

## Templates

Available project templates:
- `project-template.yaml`: Standard project configuration template

## Integration

Projects in the Forge can integrate with:
- **MCP Servers**: For enhanced capabilities
- **Agents**: For autonomous operations
- **Memory System**: For persistent knowledge
- **Core Services**: For infrastructure support

## Creating a New Project

1. Copy a template from `templates/`
2. Fill in project details
3. Create project directory in `active/` or `experiments/`
4. Initialize with template structure
5. Configure integrations

## Best Practices

- Use semantic versioning
- Maintain comprehensive documentation
- Write tests for all functionality
- Use Docker for consistent environments
- Configure monitoring from the start
- Regular commits with clear messages