const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const winston = require('winston');

const app = express();
const PORT = process.env.PORT || 8081;

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

// Context storage
let contextStore = {};

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    service: 'context-broker',
    timestamp: new Date().toISOString(),
    mode: process.env.BROKER_MODE || 'standalone'
  });
});

// Context endpoints
app.get('/context/:agent', (req, res) => {
  const agentId = req.params.agent;
  res.json(contextStore[agentId] || {});
});

app.post('/context/:agent', (req, res) => {
  const agentId = req.params.agent;
  contextStore[agentId] = { ...contextStore[agentId], ...req.body };
  res.json({ success: true, agentId });
});

app.get('/contexts', (req, res) => {
  res.json(contextStore);
});

app.listen(PORT, () => {
  logger.info(`Context broker service running on port ${PORT}`);
});