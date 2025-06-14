const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const winston = require('winston');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 8082;

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

// Service registry
const services = {
  orchestrator: 'http://orchestrator:8080',
  'context-broker': 'http://context-broker:8081',
  'memory-service': 'http://memory-service:8083'
};

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    service: 'router',
    timestamp: new Date().toISOString(),
    strategy: process.env.ROUTING_STRATEGY || 'round-robin'
  });
});

// Route requests to services
app.use('/api/:service/*', async (req, res) => {
  const serviceName = req.params.service;
  const serviceUrl = services[serviceName];
  
  if (!serviceUrl) {
    return res.status(404).json({ error: 'Service not found' });
  }
  
  try {
    const response = await axios({
      method: req.method,
      url: `${serviceUrl}${req.originalUrl.replace(`/api/${serviceName}`, '')}`,
      data: req.body,
      headers: req.headers
    });
    
    res.status(response.status).json(response.data);
  } catch (error) {
    logger.error(`Routing error: ${error.message}`);
    res.status(500).json({ error: 'Service unavailable' });
  }
});

app.listen(PORT, () => {
  logger.info(`Router service running on port ${PORT}`);
});