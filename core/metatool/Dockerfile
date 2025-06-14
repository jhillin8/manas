FROM node:18-alpine AS builder

WORKDIR /app

# Clone the repository
RUN apk add --no-cache git
RUN git clone https://github.com/metatool-ai/metatool-app.git .

# Install dependencies and build
RUN npm install
RUN npm run build

FROM node:18-alpine

WORKDIR /app

# Install runtime dependencies
RUN apk add --no-cache ca-certificates

# Copy built application
COPY --from=builder /app .

# Create non-root user
RUN addgroup -g 1001 -S metatool
RUN adduser -S manas -u 1001 -G metatool

# Create necessary directories
RUN mkdir -p /data /config && chown -R manas:metatool /data /config /app

# Switch to non-root user
USER manas

EXPOSE 3001

# Start the application
CMD ["npm", "start"]