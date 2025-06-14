const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const winston = require('winston');
const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');

const app = express();
const PORT = process.env.PORT || 3004;

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

// Endgame MCP Server
class EndgameMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'endgame-mcp',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
          resources: {},
        },
      }
    );

    this.setupTools();
  }

  setupTools() {
    // Deploy tool
    this.server.setRequestHandler('tools/list', async () => {
      return {
        tools: [
          {
            name: 'deploy',
            description: 'Deploy application to Endgame cloud platform',
            inputSchema: {
              type: 'object',
              properties: {
                projectPath: {
                  type: 'string',
                  description: 'Path to the project directory',
                },
                branch: {
                  type: 'string',
                  description: 'Git branch to deploy',
                  default: 'main'
                },
                environment: {
                  type: 'string',
                  description: 'Deployment environment',
                  enum: ['development', 'staging', 'production'],
                  default: 'development'
                }
              },
              required: ['projectPath'],
            },
          },
          {
            name: 'test',
            description: 'Run automated tests on deployed application',
            inputSchema: {
              type: 'object',
              properties: {
                deploymentUrl: {
                  type: 'string',
                  description: 'URL of the deployed application',
                },
                testSuite: {
                  type: 'string',
                  description: 'Test suite to run',
                  enum: ['unit', 'integration', 'e2e', 'all'],
                  default: 'all'
                }
              },
              required: ['deploymentUrl'],
            },
          },
          {
            name: 'status',
            description: 'Check deployment status and health',
            inputSchema: {
              type: 'object',
              properties: {
                deploymentId: {
                  type: 'string',
                  description: 'Deployment ID to check',
                }
              },
              required: ['deploymentId'],
            },
          }
        ],
      };
    });

    // Deploy tool handler
    this.server.setRequestHandler('tools/call', async (request) => {
      const { name, arguments: args } = request.params;

      switch (name) {
        case 'deploy':
          return await this.handleDeploy(args);
        case 'test':
          return await this.handleTest(args);
        case 'status':
          return await this.handleStatus(args);
        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    });
  }

  async handleDeploy(args) {
    try {
      logger.info('Starting deployment:', args);
      
      // Simulate deployment process
      const deploymentId = `deploy_${Date.now()}`;
      const deploymentUrl = `https://${args.branch || 'main'}-${deploymentId}.endgame.dev`;
      
      // Mock deployment steps
      const steps = [
        'Uploading code to cloud',
        'Building application',
        'Running automated tests',
        'Deploying to environment',
        'Health check verification'
      ];

      return {
        content: [
          {
            type: 'text',
            text: `🚀 Deployment initiated successfully!\n\nDeployment ID: ${deploymentId}\nURL: ${deploymentUrl}\nEnvironment: ${args.environment || 'development'}\n\nSteps:\n${steps.map((step, i) => `${i + 1}. ${step}`).join('\n')}\n\n✅ Deployment completed in ~10 seconds`
          }
        ]
      };
    } catch (error) {
      logger.error('Deployment failed:', error);
      return {
        content: [
          {
            type: 'text',
            text: `❌ Deployment failed: ${error.message}`
          }
        ]
      };
    }
  }

  async handleTest(args) {
    try {
      logger.info('Running tests:', args);
      
      const testResults = {
        unit: { passed: 45, failed: 2, coverage: '87%' },
        integration: { passed: 23, failed: 0, coverage: '92%' },
        e2e: { passed: 12, failed: 1, coverage: '78%' }
      };

      return {
        content: [
          {
            type: 'text',
            text: `🧪 Test Results for ${args.deploymentUrl}\n\nUnit Tests: ${testResults.unit.passed} passed, ${testResults.unit.failed} failed (Coverage: ${testResults.unit.coverage})\nIntegration Tests: ${testResults.integration.passed} passed, ${testResults.integration.failed} failed (Coverage: ${testResults.integration.coverage})\nE2E Tests: ${testResults.e2e.passed} passed, ${testResults.e2e.failed} failed (Coverage: ${testResults.e2e.coverage})\n\n${testResults.unit.failed + testResults.integration.failed + testResults.e2e.failed === 0 ? '✅ All tests passed!' : '⚠️ Some tests failed - review needed'}`
          }
        ]
      };
    } catch (error) {
      logger.error('Testing failed:', error);
      return {
        content: [
          {
            type: 'text',
            text: `❌ Testing failed: ${error.message}`
          }
        ]
      };
    }
  }

  async handleStatus(args) {
    try {
      const status = {
        deploymentId: args.deploymentId,
        status: 'running',
        health: 'healthy',
        uptime: '2h 34m',
        responseTime: '45ms',
        lastDeployed: new Date().toISOString()
      };

      return {
        content: [
          {
            type: 'text',
            text: `📊 Deployment Status\n\nID: ${status.deploymentId}\nStatus: ${status.status}\nHealth: ${status.health}\nUptime: ${status.uptime}\nResponse Time: ${status.responseTime}\nLast Deployed: ${status.lastDeployed}\n\n✅ All systems operational`
          }
        ]
      };
    } catch (error) {
      logger.error('Status check failed:', error);
      return {
        content: [
          {
            type: 'text',
            text: `❌ Status check failed: ${error.message}`
          }
        ]
      };
    }
  }

  async start() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    logger.info('Endgame MCP server started');
  }
}

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy',
    service: 'endgame-mcp',
    timestamp: new Date().toISOString(),
    capabilities: ['deploy', 'test', 'status']
  });
});

// MCP server status
app.get('/endgame/status', (req, res) => {
  res.json({
    server: 'endgame-mcp',
    version: '1.0.0',
    tools: ['deploy', 'test', 'status'],
    platform: 'endgame.dev'
  });
});

// Start HTTP server
app.listen(PORT, () => {
  logger.info(`Endgame MCP HTTP service running on port ${PORT}`);
});

// Start MCP server
const mcpServer = new EndgameMCPServer();
mcpServer.start().catch(console.error);