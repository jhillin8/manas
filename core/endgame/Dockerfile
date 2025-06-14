FROM node:18-alpine

WORKDIR /app

# Install global dependencies for MCP
RUN npm install -g @modelcontextprotocol/sdk

# Install local dependencies
COPY package*.json ./
RUN npm install

# Copy application files
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S endgame
RUN adduser -S manas -u 1001 -G endgame

# Create necessary directories
RUN mkdir -p /data /config && chown -R manas:endgame /data /config /app

# Switch to non-root user
USER manas

EXPOSE 3004

# Start the Endgame MCP service
CMD ["node", "server.js"]