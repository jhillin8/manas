#!/usr/bin/env python3
"""
LangFlow-as-MCP Bridge Service
Exposes LangFlow memory workflows as MCP-compatible tools
"""

import json
import asyncio
import aiohttp
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

class LangFlowMCPBridge:
    def __init__(self, langflow_host: str = "localhost", langflow_port: int = 7860):
        self.langflow_base_url = f"http://{langflow_host}:{langflow_port}"
        self.memory_steward_flow_id = None
        self.running_sessions = {}
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    async def initialize_flows(self):
        """Initialize LangFlow workflows for memory operations"""
        try:
            # Deploy Memory Steward flow
            steward_flow_path = "/Users/josephhillin/workspace/mcp-central/agents/memory-steward/memory-steward-flow.json"
            with open(steward_flow_path, 'r') as f:
                flow_data = json.load(f)
            
            self.memory_steward_flow_id = await self.deploy_flow("memory-steward", flow_data)
            self.logger.info(f"Memory Steward flow deployed with ID: {self.memory_steward_flow_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize flows: {e}")
            raise
    
    async def deploy_flow(self, flow_name: str, flow_data: Dict) -> str:
        """Deploy a flow to LangFlow"""
        async with aiohttp.ClientSession() as session:
            deploy_url = f"{self.langflow_base_url}/api/v1/flows"
            
            payload = {
                "name": flow_name,
                "data": flow_data,
                "auto_start": True
            }
            
            async with session.post(deploy_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("flow_id")
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to deploy flow {flow_name}: {error_text}")
    
    async def validate_memory_via_steward(self, content: str, suggested_category: str = None,
                                         tags: List[str] = None) -> Dict[str, Any]:
        """Use Memory Steward flow to validate memory entry"""
        if not self.memory_steward_flow_id:
            raise Exception("Memory Steward flow not initialized")
        
        async with aiohttp.ClientSession() as session:
            run_url = f"{self.langflow_base_url}/api/v1/flows/{self.memory_steward_flow_id}/run"
            
            payload = {
                "inputs": {
                    "content": content,
                    "suggested_category": suggested_category,
                    "tags": tags or []
                },
                "stream": False
            }
            
            async with session.post(run_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return self.parse_validation_result(result)
                else:
                    error_text = await response.text()
                    raise Exception(f"Validation failed: {error_text}")
    
    def parse_validation_result(self, langflow_result: Dict) -> Dict[str, Any]:
        """Parse LangFlow validation result into standardized format"""
        # Extract validation metrics from LangFlow output
        outputs = langflow_result.get("outputs", {})
        
        return {
            "validation_score": outputs.get("validation_score", 0.0),
            "suggested_category": outputs.get("suggested_category"),
            "quality_metrics": outputs.get("quality_metrics", {}),
            "recommendations": outputs.get("recommendations", []),
            "enhanced_tags": outputs.get("enhanced_tags", []),
            "processing_time": outputs.get("processing_time", 0),
            "confidence": outputs.get("confidence", 0.0)
        }
    
    # MCP Tool Interface Methods
    async def mcp_validate_memory(self, content: str, category: str = None, tags: List[str] = None) -> Dict:
        """MCP-compatible memory validation tool"""
        try:
            result = await self.validate_memory_via_steward(content, category, tags)
            return {
                "success": True,
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def mcp_enhance_memory(self, content: str, context: str = None) -> Dict:
        """MCP-compatible memory enhancement tool"""
        # Enhanced memory processing via LangFlow
        try:
            # Future: implement memory enhancement flow
            return {
                "success": True,
                "enhanced_content": content,  # Placeholder
                "extracted_metadata": {},
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def mcp_memory_health_check(self) -> Dict:
        """MCP-compatible health check for memory system"""
        try:
            # Check LangFlow connectivity
            async with aiohttp.ClientSession() as session:
                health_url = f"{self.langflow_base_url}/health"
                async with session.get(health_url) as response:
                    langflow_healthy = response.status == 200
            
            return {
                "success": True,
                "langflow_connected": langflow_healthy,
                "memory_steward_ready": self.memory_steward_flow_id is not None,
                "active_sessions": len(self.running_sessions),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

if __name__ == "__main__":
    bridge = LangFlowMCPBridge()
    
    async def test_bridge():
        await bridge.initialize_flows()
        
        # Test validation
        test_result = await bridge.mcp_validate_memory(
            content="How to implement async/await in Python for better performance",
            category="knowledge_technical",
            tags=["python", "async", "performance"]
        )
        
        print(json.dumps(test_result, indent=2))
    
    asyncio.run(test_bridge())
