# Infrastructure

The infrastructure directory contains all deployment, monitoring, and operational configurations for the Manas system.

## Directory Structure

- **docker/**: Docker and Docker Compose configurations
- **environments/**: Environment-specific configurations
- **security/**: Security policies and certificates
- **monitoring/**: Monitoring and observability setup
- **observability/**: Logging, tracing, and metrics

## Quick Start

### Local Development
```bash
cd docker
docker-compose up -d
```

### Production Deployment
```bash
cd docker
docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d
```

## Services Overview

### Core Infrastructure
- **NATS**: Message broker for async communication
- **Redis**: Cache and session storage
- **Qdrant**: Vector database for embeddings
- **Neo4j**: Graph database for relationships

### Monitoring Stack
- **Prometheus**: Metrics collection
- **Grafana**: Visualization and dashboards
- **Jaeger**: Distributed tracing
- **Alertmanager**: Alert routing and management

## Configuration

### Environment Variables
Each service can be configured via environment variables:
- `MANAS_ENV`: Environment (development, staging, production)
- `LOG_LEVEL`: Logging verbosity (debug, info, warn, error)
- Service-specific variables in docker-compose.yaml

### Volumes
Persistent data is stored in named volumes:
- `orchestrator-data`: Orchestrator state
- `memory-data`: Memory system data
- `*-data`: Service-specific data

### Networks
All services communicate on the `manas-network` (172.28.0.0/16).

## Security

### TLS/SSL
- All external endpoints use TLS
- Internal communication uses mTLS where supported
- Certificates managed in `security/certs/`

### Authentication
- Service-to-service: mTLS certificates
- External access: API keys or OAuth2
- Admin access: Strong passwords with MFA

### Network Policies
- Ingress restricted to necessary ports
- Egress controlled via firewall rules
- Internal network isolated from external

## Monitoring

### Metrics
Access Grafana at http://localhost:3000
- Default credentials: admin/manas-admin
- Pre-configured dashboards for all services

### Logs
Centralized logging via:
- Fluentd/Fluent Bit for collection
- Elasticsearch for storage
- Kibana for analysis

### Tracing
Jaeger UI at http://localhost:16686
- Distributed request tracing
- Performance bottleneck analysis
- Error tracking

### Alerts
Configured alerts include:
- Service health checks
- Resource utilization
- Error rate thresholds
- SLA violations

## Scaling

### Horizontal Scaling
Services that support horizontal scaling:
- Router (stateless)
- Agents (with coordination)
- Memory service (with sharding)

### Vertical Scaling
Resource limits configured in:
- `docker/resources.yaml`
- Kubernetes manifests
- Cloud provider configs

## Backup and Recovery

### Backup Strategy
- Daily snapshots of persistent volumes
- Continuous replication for critical data
- Off-site backup storage

### Disaster Recovery
- RTO: 4 hours
- RPO: 1 hour
- Automated failover for critical services

## Maintenance

### Updates
1. Test updates in staging environment
2. Perform rolling updates
3. Monitor health during deployment
4. Rollback if issues detected

### Health Checks
All services expose `/health` endpoints:
- Liveness: Service is running
- Readiness: Service can handle requests
- Startup: Service initialization complete

## Troubleshooting

### Common Issues
1. **Service won't start**: Check logs with `docker-compose logs <service>`
2. **Connection refused**: Verify network connectivity
3. **High memory usage**: Check for memory leaks
4. **Slow performance**: Review metrics and traces

### Debug Mode
Enable debug logging:
```bash
LOG_LEVEL=debug docker-compose up
```

### Support
- Check service logs
- Review monitoring dashboards
- Consult runbooks in `docs/operations/`