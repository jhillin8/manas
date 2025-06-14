# Router

The Router component handles request routing, load balancing, and traffic management for the Manas system.

## Features

- **Intelligent Routing**: Routes requests based on agent capabilities
- **Load Balancing**: Distributes load across available agents
- **Circuit Breaking**: Prevents cascading failures
- **Request Retry**: Automatic retry with exponential backoff
- **Rate Limiting**: Protects system from overload

## Routing Strategies

1. **Capability-Based**: Routes to agents based on required capabilities
2. **Round-Robin**: Distributes requests evenly
3. **Least-Connections**: Routes to least busy agent
4. **Priority-Based**: Considers agent priority levels
5. **Geographic**: Routes based on proximity (future)

## Configuration

```yaml
router:
  strategies:
    default: capability-based
    fallback: round-robin
  
  circuit_breaker:
    threshold: 5
    timeout: 30s
  
  rate_limiting:
    requests_per_second: 100
    burst_size: 200
```

## Monitoring

- Request metrics and latencies
- Success/failure rates
- Circuit breaker status
- Agent availability

## Integration

- **Context Broker**: Receives routing context
- **Agents**: Forwards requests to appropriate agents
- **Orchestrator**: Gets service health information
- **Monitoring**: Exports metrics for observability

## API

- `POST /route` - Route a request
- `GET /routes` - List active routes
- `GET /metrics` - Router metrics
- `PUT /config` - Update routing configuration