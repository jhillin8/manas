FROM node:18-alpine

WORKDIR /app

# Install global dependencies
RUN npm install -g mcp-remote@latest

# Install local dependencies
COPY package*.json ./
RUN npm install

# Copy application files
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S pearl
RUN adduser -S manas -u 1001 -G pearl

# Create necessary directories
RUN mkdir -p /data /config && chown -R manas:pearl /data /config /app

# Switch to non-root user
USER manas

EXPOSE 3003

# Health check script
COPY healthcheck.js /app/healthcheck.js

# Start the Pearl MCP proxy service
CMD ["node", "server.js"]