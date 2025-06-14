#!/usr/bin/env python3
"""
LangFlow MCP Agent Launcher
Orchestrates the entire Cross-Agent Memory Intelligence System
"""

import asyncio
import subprocess
import json
import yaml
import os
import signal
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
import time
import psutil

# Import local components
sys.path.append('/Users/josephhillin/workspace/mcp-central')
from langflow.memory_mcp_bridge import LangFlowMCPBridge
from raycast_config_registry import RaycastConfigRegistry
from team.team_memory_manager import TeamMemoryManager

class CrossAgentMemoryOrchestrator:
    def __init__(self):
        self.base_path = "/Users/josephhillin/workspace/mcp-central"
        self.running_processes = {}
        self.health_checks = {}
        self.startup_sequence = []
        
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{self.base_path}/orchestrator.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('MemoryOrchestrator')
        
        # Initialize components
        self.registry = RaycastConfigRegistry()
        self.langflow_bridge = LangFlowMCPBridge()
        
        # Load configuration
        self.load_orchestrator_config()
    
    def load_orchestrator_config(self):
        """Load orchestrator configuration"""
        config_path = f"{self.base_path}/orchestrator-config.yaml"
        
        default_config = {
            "startup_sequence": [
                {"service": "docker", "wait_seconds": 5},
                {"service": "langflow", "wait_seconds": 10},
                {"service": "memory_graph_api", "wait_seconds": 3},
                {"service": "temporal_processor", "wait_seconds": 3},
                {"service": "audit_system", "wait_seconds": 2},
                {"service": "raycast_sync", "wait_seconds": 2}
            ],
            "health_check_interval": 30,
            "auto_restart": True,
            "resource_profile": "balanced",
            "services": {
                "docker": {
                    "enabled": True,
                    "compose_file": f"{self.base_path}/docker-compose.yaml",
                    "profile": "balanced"
                },
                "langflow": {
                    "enabled": True,
                    "host": "localhost",
                    "port": 7860,
                    "auto_deploy_flows": True
                },
                "memory_graph_api": {
                    "enabled": True,
                    "port": 8767,
                    "script": f"{self.base_path}/graph/memory-graph-service.py"
                },
                "temporal_processor": {
                    "enabled": True,
                    "schedule": "*/5 * * * *",  # Every 5 minutes
                    "script": f"{self.base_path}/agents/temporal-engine/temporal-processor.py"
                }
            }
        }
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = default_config
            with open(config_path, 'w') as f:
                yaml.dump(default_config, f, indent=2)
    
    async def start_system(self, resource_profile: str = None):
        """Start the entire Cross-Agent Memory Intelligence System"""
        profile = resource_profile or self.config.get("resource_profile", "balanced")
        
        self.logger.info(f"🚀 Starting Cross-Agent Memory Intelligence System with profile: {profile}")
        
        try:
            # 1. Apply resource profile
            await self.apply_resource_profile(profile)
            
            # 2. Start services in sequence
            for step in self.config["startup_sequence"]:
                service_name = step["service"]
                wait_time = step.get("wait_seconds", 3)
                
                self.logger.info(f"Starting {service_name}...")
                
                if service_name == "docker":
                    await self.start_docker_services(profile)
                elif service_name == "langflow":
                    await self.start_langflow()
                elif service_name == "memory_graph_api":
                    await self.start_memory_graph_api()
                elif service_name == "temporal_processor":
                    await self.start_temporal_processor()
                elif service_name == "audit_system":
                    await self.start_audit_system()
                elif service_name == "raycast_sync":
                    await self.sync_raycast_configs()
                
                self.logger.info(f"✅ {service_name} started, waiting {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            
            # 3. Initialize LangFlow-MCP bridge
            await self.langflow_bridge.initialize_flows()
            
            # 4. Start health monitoring
            asyncio.create_task(self.health_monitor_loop())
            
            self.logger.info("🎉 Cross-Agent Memory Intelligence System fully operational!")
            
            return {
                "success": True,
                "services_started": len(self.running_processes),
                "resource_profile": profile,
                "startup_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ System startup failed: {e}")
            await self.shutdown_system()
            raise
    
    async def apply_resource_profile(self, profile: str):
        """Apply Docker resource profile"""
        profiles_file = f"{self.base_path}/docker-configs/resource-profiles.yaml"
        
        if os.path.exists(profiles_file):
            # Create Docker Compose file with profile
            await self.generate_docker_compose(profile)
            self.logger.info(f"Applied resource profile: {profile}")
    
    async def generate_docker_compose(self, profile: str):
        """Generate Docker Compose file based on resource profile"""
        profiles_file = f"{self.base_path}/docker-configs/resource-profiles.yaml"
        
        with open(profiles_file, 'r') as f:
            profiles_config = yaml.safe_load(f)
        
        profile_config = profiles_config["profiles"][profile]
        
        docker_compose = {
            "version": "3.8",
            "services": {
                "postgres": {
                    "image": "postgres:15",
                    "environment": {
                        "POSTGRES_DB": "openmemory",
                        "POSTGRES_USER": "memory_user",
                        "POSTGRES_PASSWORD": "memory_pass"
                    },
                    "ports": ["5432:5432"],
                    "deploy": {
                        "resources": {
                            "limits": {
                                "memory": profile_config["services"]["postgres"]["memory"],
                                "cpus": str(profile_config["services"]["postgres"]["cpu"])
                            }
                        }
                    },
                    "volumes": ["postgres_data:/var/lib/postgresql/data"]
                },
                "qdrant": {
                    "image": "qdrant/qdrant:latest",
                    "ports": ["6333:6333", "6334:6334"],
                    "deploy": {
                        "resources": {
                            "limits": {
                                "memory": profile_config["services"]["qdrant"]["memory"],
                                "cpus": str(profile_config["services"]["qdrant"]["cpu"])
                            }
                        }
                    },
                    "volumes": ["qdrant_data:/qdrant/storage"]
                }
            },
            "volumes": {
                "postgres_data": {},
                "qdrant_data": {}
            }
        }
        
        compose_file = f"{self.base_path}/docker-compose.yaml"
        with open(compose_file, 'w') as f:
            yaml.dump(docker_compose, f, indent=2)
    
    async def start_docker_services(self, profile: str):
        """Start Docker services"""
        compose_file = f"{self.base_path}/docker-compose.yaml"
        
        if os.path.exists(compose_file):
            cmd = ["docker-compose", "-f", compose_file, "up", "-d"]
            process = await asyncio.create_subprocess_exec(
                *cmd, 
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                self.running_processes["docker"] = process.pid
                self.logger.info("Docker services started successfully")
            else:
                raise Exception(f"Docker startup failed: {stderr.decode()}")
    
    async def start_langflow(self):
        """Start LangFlow server"""
        cmd = ["langflow", "run", "--host", "0.0.0.0", "--port", "7860"]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        self.running_processes["langflow"] = process.pid
        
        # Wait for LangFlow to be ready
        await self.wait_for_service("http://localhost:7860/health", timeout=60)
    
    async def start_memory_graph_api(self):
        """Start memory graph API service"""
        script_path = f"{self.base_path}/graph/memory-graph-service.py"
        
        cmd = ["python3", script_path, "--api-mode", "--port", "8767"]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        self.running_processes["memory_graph_api"] = process.pid
    
    async def start_temporal_processor(self):
        """Start temporal processor as background service"""
        script_path = f"{self.base_path}/agents/temporal-engine/temporal-processor.py"
        
        cmd = ["python3", script_path, "--daemon"]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        self.running_processes["temporal_processor"] = process.pid
    
    async def start_audit_system(self):
        """Initialize audit system"""
        # Audit system runs as library, just verify it's accessible
        script_path = f"{self.base_path}/security/audit-system.py"
        
        cmd = ["python3", "-c", f"import sys; sys.path.append('{self.base_path}'); from security.audit_system import MemoryAuditSystem; print('Audit system ready')"]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        await process.communicate()
    
    async def sync_raycast_configs(self):
        """Sync configurations to Raycast"""
        sync_result = self.registry.sync_to_raycast()
        
        if sync_result["success"]:
            self.logger.info(f"Raycast sync completed: {sync_result['synced_extensions']}")
        else:
            self.logger.error(f"Raycast sync failed: {sync_result['errors']}")
    
    async def wait_for_service(self, url: str, timeout: int = 30):
        """Wait for a service to become available"""
        import aiohttp
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            return True
            except:
                pass
            
            await asyncio.sleep(2)
        
        raise Exception(f"Service at {url} not available within {timeout} seconds")
    
    async def health_monitor_loop(self):
        """Monitor system health and restart services if needed"""
        while True:
            try:
                await self.perform_health_checks()
                await asyncio.sleep(self.config.get("health_check_interval", 30))
            except Exception as e:
                self.logger.error(f"Health check error: {e}")
                await asyncio.sleep(10)
    
    async def perform_health_checks(self):
        """Perform health checks on all services"""
        health_status = {}
        
        for service_name, pid in self.running_processes.items():
            if psutil.pid_exists(pid):
                health_status[service_name] = "running"
            else:
                health_status[service_name] = "stopped"
                self.logger.warning(f"Service {service_name} stopped unexpectedly")
                
                if self.config.get("auto_restart"):
                    await self.restart_service(service_name)
        
        self.health_checks = {
            "timestamp": datetime.now().isoformat(),
            "services": health_status
        }
    
    async def restart_service(self, service_name: str):
        """Restart a specific service"""
        self.logger.info(f"Restarting service: {service_name}")
        
        # Remove from running processes
        if service_name in self.running_processes:
            del self.running_processes[service_name]
        
        # Restart based on service type
        if service_name == "langflow":
            await self.start_langflow()
        elif service_name == "memory_graph_api":
            await self.start_memory_graph_api()
        elif service_name == "temporal_processor":
            await self.start_temporal_processor()
    
    async def shutdown_system(self):
        """Gracefully shutdown the entire system"""
        self.logger.info("🛑 Shutting down Cross-Agent Memory Intelligence System...")
        
        # Stop all running processes
        for service_name, pid in self.running_processes.items():
            try:
                if psutil.pid_exists(pid):
                    process = psutil.Process(pid)
                    process.terminate()
                    self.logger.info(f"Stopped {service_name} (PID: {pid})")
            except Exception as e:
                self.logger.error(f"Error stopping {service_name}: {e}")
        
        # Stop Docker services
        compose_file = f"{self.base_path}/docker-compose.yaml"
        if os.path.exists(compose_file):
            cmd = ["docker-compose", "-f", compose_file, "down"]
            subprocess.run(cmd)
        
        self.logger.info("✅ System shutdown complete")

async def main():
    orchestrator = CrossAgentMemoryOrchestrator()
    
    # Handle shutdown signals
    def signal_handler(sig, frame):
        asyncio.create_task(orchestrator.shutdown_system())
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start system
        result = await orchestrator.start_system()
        print(json.dumps(result, indent=2))
        
        # Keep running
        while True:
            await asyncio.sleep(60)
            
    except KeyboardInterrupt:
        await orchestrator.shutdown_system()

if __name__ == "__main__":
    asyncio.run(main())
