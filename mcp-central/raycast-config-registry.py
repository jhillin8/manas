#!/usr/bin/env python3
"""
Central Raycast Config Registry
Manages unified configuration for all MCP servers and memory tools in Raycast
"""

import json
import os
import yaml
from datetime import datetime
from typing import Dict, List, Any, Optional
import shutil
import glob

class RaycastConfigRegistry:
    def __init__(self):
        self.raycast_config_dir = "/Users/josephhillin/.config/raycast"
        self.extensions_dir = f"{self.raycast_config_dir}/extensions"
        self.mcp_central_dir = "/Users/josephhillin/workspace/mcp-central"
        self.registry_file = f"{self.mcp_central_dir}/raycast-config-registry.json"
        
        self.load_registry()
    
    def load_registry(self):
        """Load existing registry or create new one"""
        if os.path.exists(self.registry_file):
            with open(self.registry_file, 'r') as f:
                self.registry = json.load(f)
        else:
            self.registry = {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "mcp_servers": {},
                "memory_tools": {},
                "resource_profiles": {},
                "extension_mapping": {}
            }
    
    def save_registry(self):
        """Save registry to file"""
        self.registry["last_updated"] = datetime.now().isoformat()
        with open(self.registry_file, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def register_mcp_server(self, server_name: str, config: Dict[str, Any]):
        """Register an MCP server configuration"""
        self.registry["mcp_servers"][server_name] = {
            "config": config,
            "registered_timestamp": datetime.now().isoformat(),
            "status": "active",
            "health_endpoint": config.get("health_endpoint"),
            "dependencies": config.get("dependencies", [])
        }
        self.save_registry()
    
    def register_memory_tool(self, tool_name: str, tool_config: Dict[str, Any]):
        """Register a memory tool configuration"""
        self.registry["memory_tools"][tool_name] = {
            "config": tool_config,
            "registered_timestamp": datetime.now().isoformat(),
            "raycast_command": tool_config.get("raycast_command"),
            "cli_command": tool_config.get("cli_command"),
            "mcp_integration": tool_config.get("mcp_integration", False)
        }
        self.save_registry()
    
    def register_resource_profile(self, profile_name: str, profile_config: Dict[str, Any]):
        """Register a resource profile configuration"""
        self.registry["resource_profiles"][profile_name] = {
            "config": profile_config,
            "registered_timestamp": datetime.now().isoformat(),
            "docker_compose_path": profile_config.get("docker_compose_path"),
            "auto_switch_rules": profile_config.get("auto_switch_rules", {})
        }
        self.save_registry()
    
    def sync_to_raycast(self) -> Dict[str, Any]:
        """Sync all configurations to Raycast extensions"""
        results = {
            "success": True,
            "synced_extensions": [],
            "errors": []
        }
        
        try:
            # Sync MCP servers to Raycast MCP extension
            mcp_extension_path = self.find_mcp_extension()
            if mcp_extension_path:
                mcp_config = self.generate_mcp_raycast_config()
                config_file = f"{mcp_extension_path}/mcp-servers.json"
                with open(config_file, 'w') as f:
                    json.dump(mcp_config, f, indent=2)
                results["synced_extensions"].append("mcp-manager")
            
            # Sync memory tools to memory extension
            memory_extension_path = self.find_memory_extension()
            if memory_extension_path:
                memory_config = self.generate_memory_raycast_config()
                config_file = f"{memory_extension_path}/memory-tools.json"
                with open(config_file, 'w') as f:
                    json.dump(memory_config, f, indent=2)
                results["synced_extensions"].append("memory-manager")
            
            # Create unified Raycast commands file
            self.create_unified_commands_file()
            results["synced_extensions"].append("unified-commands")
            
        except Exception as e:
            results["success"] = False
            results["errors"].append(str(e))
        
        return results
    
    def find_mcp_extension(self) -> Optional[str]:
        """Find MCP extension directory in Raycast"""
        # Look for MCP-related extensions
        pattern = f"{self.extensions_dir}/*/manage-mcp-servers.js"
        matches = glob.glob(pattern)
        
        if matches:
            return os.path.dirname(matches[0])
        return None
    
    def find_memory_extension(self) -> Optional[str]:
        """Find memory extension directory in Raycast"""
        # Look for memory-related extensions
        pattern = f"{self.extensions_dir}/*/view-memory.js"
        matches = glob.glob(pattern)
        
        if matches:
            return os.path.dirname(matches[0])
        return None
    
    def generate_mcp_raycast_config(self) -> Dict[str, Any]:
        """Generate Raycast-compatible MCP configuration"""
        config = {
            "servers": {},
            "profiles": {},
            "last_sync": datetime.now().isoformat()
        }
        
        for server_name, server_data in self.registry["mcp_servers"].items():
            config["servers"][server_name] = {
                "command": server_data["config"].get("command"),
                "args": server_data["config"].get("args", []),
                "env": server_data["config"].get("env", {}),
                "health_endpoint": server_data.get("health_endpoint"),
                "auto_start": server_data["config"].get("auto_start", True)
            }
        
        for profile_name, profile_data in self.registry["resource_profiles"].items():
            config["profiles"][profile_name] = profile_data["config"]
        
        return config
    
    def generate_memory_raycast_config(self) -> Dict[str, Any]:
        """Generate Raycast-compatible memory tools configuration"""
        config = {
            "tools": {},
            "cli_path": f"{self.mcp_central_dir}/bin/memory-cli.py",
            "shortcuts": {},
            "last_sync": datetime.now().isoformat()
        }
        
        for tool_name, tool_data in self.registry["memory_tools"].items():
            config["tools"][tool_name] = {
                "title": tool_data["config"].get("title", tool_name.title()),
                "description": tool_data["config"].get("description", ""),
                "command": tool_data.get("cli_command"),
                "raycast_command": tool_data.get("raycast_command"),
                "icon": tool_data["config"].get("icon", "🧠"),
                "keywords": tool_data["config"].get("keywords", [])
            }
        
        # Add default shortcuts
        config["shortcuts"] = {
            "add_memory": "cmd+shift+m",
            "search_memory": "cmd+shift+s",
            "review_queue": "cmd+shift+r",
            "export_graph": "cmd+shift+e"
        }
        
        return config
    
    def create_unified_commands_file(self):
        """Create unified commands file for all memory operations"""
        commands = {
            "memory_cli": {
                "path": f"{self.mcp_central_dir}/bin/memory-cli.py",
                "description": "Command-line interface for memory operations"
            },
            "memory_health": {
                "command": "python3 -c \"from langflow.memory_mcp_bridge import LangFlowMCPBridge; import asyncio; asyncio.run(LangFlowMCPBridge().mcp_memory_health_check())\"",
                "description": "Check memory system health"
            },
            "sync_raycast": {
                "command": f"python3 {self.mcp_central_dir}/raycast-config-sync.py",
                "description": "Sync configurations to Raycast"
            }
        }
        
        commands_file = f"{self.mcp_central_dir}/unified-commands.json"
        with open(commands_file, 'w') as f:
            json.dump(commands, f, indent=2)
    
    def auto_discover_components(self) -> Dict[str, Any]:
        """Auto-discover memory system components and register them"""
        discovered = {
            "mcp_servers": 0,
            "memory_tools": 0,
            "resource_profiles": 0
        }
        
        # Discover MCP servers
        mcp_config_file = "/Users/josephhillin/mcp/mcp_server_config.json"
        if os.path.exists(mcp_config_file):
            with open(mcp_config_file, 'r') as f:
                mcp_config = json.load(f)
                for server_name, server_config in mcp_config.get("mcpServers", {}).items():
                    self.register_mcp_server(server_name, server_config)
                    discovered["mcp_servers"] += 1
        
        # Discover memory tools
        memory_tools = [
            {
                "name": "memory_cli", 
                "title": "Memory CLI",
                "description": "Command-line memory management",
                "cli_command": f"python3 {self.mcp_central_dir}/bin/memory-cli.py",
                "raycast_command": "memory-cli",
                "icon": "🧠",
                "keywords": ["memory", "cli", "add", "search"]
            },
            {
                "name": "memory_graph",
                "title": "Memory Graph Viewer", 
                "description": "Visualize memory relationships",
                "cli_command": f"python3 {self.mcp_central_dir}/graph/memory-graph-service.py",
                "raycast_command": "memory-graph",
                "icon": "🕸️",
                "keywords": ["memory", "graph", "relationships", "visualize"]
            },
            {
                "name": "memory_review",
                "title": "Memory Review Queue",
                "description": "Review forgotten and trending memories",
                "cli_command": f"python3 {self.mcp_central_dir}/bin/memory-cli.py review",
                "raycast_command": "memory-review",
                "icon": "📋",
                "keywords": ["memory", "review", "forgotten", "trending"]
            }
        ]
        
        for tool in memory_tools:
            self.register_memory_tool(tool["name"], tool)
            discovered["memory_tools"] += 1
        
        # Discover resource profiles
        profiles_file = f"{self.mcp_central_dir}/docker-configs/resource-profiles.yaml"
        if os.path.exists(profiles_file):
            with open(profiles_file, 'r') as f:
                profiles_config = yaml.safe_load(f)
                for profile_name, profile_config in profiles_config.get("profiles", {}).items():
                    self.register_resource_profile(profile_name, profile_config)
                    discovered["resource_profiles"] += 1
        
        return discovered

if __name__ == "__main__":
    registry = RaycastConfigRegistry()
    
    # Auto-discover components
    discovered = registry.auto_discover_components()
    print(f"Auto-discovered components: {discovered}")
    
    # Sync to Raycast
    sync_result = registry.sync_to_raycast()
    print(f"Raycast sync result: {sync_result}")
    
    print(f"Registry saved to: {registry.registry_file}")
