const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const winston = require('winston');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3003;

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

// Pearl MCP remote connection manager
class PearlMCPManager {
  constructor() {
    this.connections = new Map();
    this.isConnected = false;
    this.apiKey = process.env.PEARL_API_KEY;
  }

  async startRemoteConnection() {
    try {
      if (!this.apiKey) {
        throw new Error('PEARL_API_KEY environment variable is required');
      }

      // Start mcp-remote connection to Pearl API
      const mcpRemote = spawn('mcp-remote', [
        'sse',
        'https://mcp.pearl.com/sse',
        '--header', `X-API-KEY: ${this.apiKey}`
      ], {
        stdio: ['pipe', 'pipe', 'pipe'],
        env: { ...process.env }
      });

      mcpRemote.stdout.on('data', (data) => {
        logger.info('Pearl MCP output:', data.toString());
      });

      mcpRemote.stderr.on('data', (data) => {
        logger.error('Pearl MCP error:', data.toString());
      });

      mcpRemote.on('close', (code) => {
        logger.info(`Pearl MCP process exited with code ${code}`);
        this.isConnected = false;
      });

      this.mcpProcess = mcpRemote;
      this.isConnected = true;
      
      logger.info('Pearl MCP remote connection started successfully');
      return true;
    } catch (error) {
      logger.error('Failed to start Pearl MCP connection:', error);
      return false;
    }
  }

  getStatus() {
    return {
      connected: this.isConnected,
      hasApiKey: !!this.apiKey,
      connections: this.connections.size,
      pearlEndpoint: 'https://mcp.pearl.com/sse'
    };
  }

  async stopConnection() {
    if (this.mcpProcess) {
      this.mcpProcess.kill();
      this.isConnected = false;
    }
  }
}

const pearlManager = new PearlMCPManager();

// Health check endpoint
app.get('/health', (req, res) => {
  const status = pearlManager.getStatus();
  res.json({ 
    status: status.connected ? 'healthy' : 'disconnected',
    service: 'pearl-mcp',
    timestamp: new Date().toISOString(),
    pearl: status
  });
});

// Pearl MCP status endpoint
app.get('/pearl/status', (req, res) => {
  res.json(pearlManager.getStatus());
});

// Start Pearl connection endpoint
app.post('/pearl/connect', async (req, res) => {
  try {
    const success = await pearlManager.startRemoteConnection();
    res.json({ 
      success,
      message: success ? 'Pearl MCP connection started' : 'Failed to start connection'
    });
  } catch (error) {
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
});

// Stop Pearl connection endpoint
app.post('/pearl/disconnect', async (req, res) => {
  try {
    await pearlManager.stopConnection();
    res.json({ 
      success: true,
      message: 'Pearl MCP connection stopped'
    });
  } catch (error) {
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  logger.info('Received SIGTERM, shutting down gracefully');
  await pearlManager.stopConnection();
  process.exit(0);
});

process.on('SIGINT', async () => {
  logger.info('Received SIGINT, shutting down gracefully');
  await pearlManager.stopConnection();
  process.exit(0);
});

app.listen(PORT, async () => {
  logger.info(`Pearl MCP service running on port ${PORT}`);
  
  // Auto-start Pearl connection if API key is available
  if (process.env.PEARL_AUTO_CONNECT === 'true') {
    await pearlManager.startRemoteConnection();
  }
});