FROM node:18-alpine AS builder

WORKDIR /app

# Install git and build dependencies
RUN apk add --no-cache git

# Clone Pipedream repository and navigate to MCP directory
RUN git clone https://github.com/PipedreamHQ/pipedream.git .
WORKDIR /app/modelcontextprotocol

# Install dependencies
RUN npm install

FROM node:18-alpine

WORKDIR /app

# Install runtime dependencies
RUN apk add --no-cache ca-certificates

# Copy built application
COPY --from=builder /app/modelcontextprotocol .

# Create non-root user
RUN addgroup -g 1001 -S pipedream
RUN adduser -S manas -u 1001 -G pipedream

# Create data directory
RUN mkdir -p /data && chown -R manas:pipedream /data /app

# Switch to non-root user
USER manas

EXPOSE 3002

# Start the Pipedream MCP server
CMD ["node", "src/index.js"]