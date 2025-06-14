# Use the official MindsDB Docker image as base
FROM mindsdb/mindsdb:latest

# Expose default MindsDB port
EXPOSE 47334

# Create data directory for persistence
VOLUME ["/opt/mindsdb/var"]

# Configure MindsDB for MCP integration
ENV MINDSDB_CONFIG_PATH=/opt/mindsdb/config.json
ENV MINDSDB_STORAGE_DIR=/opt/mindsdb/var

# Copy MindsDB configuration
COPY config.json /opt/mindsdb/config.json

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:47334/api/status || exit 1

# Start MindsDB with MCP server enabled
CMD ["python", "-m", "mindsdb", "--api", "http", "--verbose"]