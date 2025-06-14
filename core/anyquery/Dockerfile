FROM golang:1.24-alpine AS builder

WORKDIR /app

# Install git and build dependencies
RUN apk add --no-cache git gcc musl-dev sqlite-dev

# Clone and build anyquery
RUN git clone https://github.com/julien040/anyquery.git .
RUN go mod download
RUN CGO_ENABLED=1 go build -ldflags="-s -w" -o anyquery ./cmd/anyquery

FROM alpine:latest

# Install runtime dependencies
RUN apk add --no-cache ca-certificates sqlite

# Create non-root user
RUN addgroup -g 1001 -S anyquery
RUN adduser -S manas -u 1001 -G anyquery

WORKDIR /app

# Copy binary
COPY --from=builder /app/anyquery /usr/local/bin/anyquery

# Create data directory
RUN mkdir -p /data && chown -R manas:anyquery /data

# Switch to non-root user
USER manas

EXPOSE 8102

# Start anyquery server
CMD ["anyquery", "server", "--host", "0.0.0.0", "--port", "8102", "--data-dir", "/data"]