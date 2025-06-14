FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install --only=production

# Copy source code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S manas -u 1001

# Set permissions
RUN chown -R manas:nodejs /app
USER manas

EXPOSE 8080

CMD ["node", "server.js"]