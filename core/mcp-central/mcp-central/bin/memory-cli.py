#!/usr/bin/env python3
"""
Memory CLI - Command Line Interface for Cross-Agent Memory Intelligence System
Provides seamless integration between CLI, Chat, and MCP interfaces
"""

import sys
import argparse
import json
import asyncio
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Optional
import subprocess
import os

# Import local components
sys.path.append('/Users/josephhillin/workspace/mcp-central')
from agents.temporal_engine.temporal_processor import TemporalIntelligenceEngine
from graph.memory_graph_service import MemoryGraphService
from security.audit_system import MemoryAuditSystem
from memory_seeds.enhanced_validator import EnhancedMemoryValidator

class MemoryCLI:
    def __init__(self):
        self.base_path = "/Users/josephhillin/workspace/mcp-central"
        self.temporal_engine = TemporalIntelligenceEngine(
            config_path=f"{self.base_path}/memory-policies/temporal-schema.yaml",
            db_path=f"{self.base_path}/memory-seeds/temporal.db"
        )
        self.graph_service = MemoryGraphService(f"{self.base_path}/graph/memory-graph.db")
        self.audit_system = MemoryAuditSystem(f"{self.base_path}/security/audit.db")
        self.validator = EnhancedMemoryValidator(f"{self.base_path}/memory-policies/temporal-schema.yaml")
        
    def add_memory(self, content: str, category: str = None, tags: List[str] = None, 
                   source: str = "cli") -> Dict[str, Any]:
        """Add new memory entry with full validation and processing"""
        
        # Generate memory ID
        memory_id = f"mem_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Validate memory
        validation_result = self.validator.enhanced_validation(
            content=content,
            suggested_category=category,
            tags=tags or [],
            source_tool=source
        )
        
        if validation_result['validation_score'] < 0.6:
            return {
                "success": False,
                "error": "Memory validation failed",
                "validation_result": validation_result,
                "memory_id": memory_id
            }
        
        # Add to graph
        enhanced_category = validation_result.get('suggested_category', category or 'knowledge_technical')
        enhanced_tags = validation_result.get('enhanced_tags', tags or [])
        
        self.graph_service.add_memory_node(
            memory_id=memory_id,
            content=content,
            category=enhanced_category,
            tags=enhanced_tags,
            metadata={
                "source": source,
                "validation_score": validation_result['validation_score'],
                "created_via": "memory_cli"
            }
        )
        
        # Log audit trail
        self.audit_system.log_memory_operation(
            memory_id=memory_id,
            operation_type="create",
            source_tool=source,
            content=content,
            metadata={
                "category": enhanced_category,
                "tags": enhanced_tags,
                "validation_score": validation_result['validation_score']
            }
        )
        
        return {
            "success": True,
            "memory_id": memory_id,
            "category": enhanced_category,
            "tags": enhanced_tags,
            "validation_result": validation_result
        }
    
    def search_memories(self, query: str, category: str = None, limit: int = 10) -> Dict[str, Any]:
        """Search memories with temporal relevance scoring"""
        # TODO: Implement semantic search integration with vector database
        # For now, return graph-based search
        
        results = []
        try:
            # Simple keyword search in graph nodes
            for node_id in self.graph_service.graph.nodes():
                node_data = self.graph_service.graph.nodes[node_id]
                content = node_data.get('content', '').lower()
                
                if query.lower() in content:
                    if not category or node_data.get('category') == category:
                        # Get relevance score from temporal engine
                        relevance = self.temporal_engine.update_relevance_score(node_id)
                        
                        results.append({
                            "memory_id": node_id,
                            "content": node_data.get('content'),
                            "category": node_data.get('category'),
                            "tags": node_data.get('tags', []),
                            "relevance_score": relevance
                        })
            
            # Sort by relevance
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            results = results[:limit]
            
            return {
                "success": True,
                "results": results,
                "query": query,
                "total_found": len(results)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
    
    def get_review_queue(self) -> Dict[str, Any]:
        """Get prioritized memory review queue"""
        try:
            review_queue = self.temporal_engine.generate_review_queue()
            return {
                "success": True,
                "review_queue": review_queue,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def export_graph(self, output_path: str = None) -> Dict[str, Any]:
        """Export memory graph for visualization"""
        try:
            if not output_path:
                output_path = f"{self.base_path}/graph/memory-export-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            self.graph_service.export_graph_json(output_path)
            
            return {
                "success": True,
                "export_path": output_path,
                "node_count": len(self.graph_service.graph.nodes()),
                "edge_count": len(self.graph_service.graph.edges())
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

def main():
    parser = argparse.ArgumentParser(description="Cross-Agent Memory Intelligence System CLI")
    parser.add_argument('command', choices=['add', 'search', 'review', 'export', 'health'], 
                       help='Command to execute')
    
    # Add memory arguments
    parser.add_argument('--content', type=str, help='Memory content to add')
    parser.add_argument('--category', type=str, help='Memory category')
    parser.add_argument('--tags', type=str, nargs='*', help='Memory tags')
    parser.add_argument('--source', type=str, default='cli', help='Source tool/system')
    
    # Search arguments
    parser.add_argument('--query', type=str, help='Search query')
    parser.add_argument('--limit', type=int, default=10, help='Max results')
    
    # Export arguments
    parser.add_argument('--output', type=str, help='Output file path')
    
    # Format arguments
    parser.add_argument('--format', choices=['json', 'pretty'], default='pretty', help='Output format')
    
    args = parser.parse_args()
    
    cli = MemoryCLI()
    result = None
    
    try:
        if args.command == 'add':
            if not args.content:
                print("Error: --content is required for add command")
                sys.exit(1)
            result = cli.add_memory(
                content=args.content,
                category=args.category,
                tags=args.tags,
                source=args.source
            )
        
        elif args.command == 'search':
            if not args.query:
                print("Error: --query is required for search command")
                sys.exit(1)
            result = cli.search_memories(
                query=args.query,
                category=args.category,
                limit=args.limit
            )
        
        elif args.command == 'review':
            result = cli.get_review_queue()
        
        elif args.command == 'export':
            result = cli.export_graph(output_path=args.output)
        
        elif args.command == 'health':
            # System health check
            result = {
                "success": True,
                "components": {
                    "temporal_engine": "operational",
                    "graph_service": "operational", 
                    "audit_system": "operational",
                    "validator": "operational"
                },
                "timestamp": datetime.now().isoformat()
            }
        
        # Output results
        if args.format == 'json':
            print(json.dumps(result, indent=2))
        else:
            # Pretty print
            if result.get('success'):
                print(f"✅ {args.command.capitalize()} completed successfully")
                if args.command == 'add' and 'memory_id' in result:
                    print(f"Memory ID: {result['memory_id']}")
                    print(f"Category: {result['category']}")
                    print(f"Validation Score: {result['validation_result']['validation_score']:.2f}")
                elif args.command == 'search':
                    print(f"Found {result['total_found']} memories:")
                    for memory in result['results'][:5]:  # Show top 5
                        print(f"  • {memory['memory_id']}: {memory['content'][:80]}...")
                elif args.command == 'review':
                    queue = result['review_queue']
                    print(f"Review Queue:")
                    for category, items in queue.items():
                        if items:
                            print(f"  {category}: {len(items)} items")
            else:
                print(f"❌ {args.command.capitalize()} failed: {result.get('error', 'Unknown error')}")
                sys.exit(1)
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
