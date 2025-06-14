const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const winston = require('winston');

const app = express();
const PORT = process.env.PORT || 8080;

// Configure logger
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console()
  ]
});

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    service: 'orchestrator',
    timestamp: new Date().toISOString(),
    environment: process.env.MANAS_ENV || 'development'
  });
});

// Service registry endpoint
app.get('/services', (req, res) => {
  res.json({
    services: [
      { name: 'orchestrator', status: 'running', port: 8080 },
      { name: 'context-broker', status: 'pending', port: 8081 },
      { name: 'router', status: 'pending', port: 8082 },
      { name: 'memory-service', status: 'pending', port: 8083 }
    ]
  });
});

// Metrics endpoint
app.get('/metrics', (req, res) => {
  res.json({
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    cpu: process.cpuUsage()
  });
});

app.listen(PORT, () => {
  logger.info(`Orchestrator service running on port ${PORT}`);
});