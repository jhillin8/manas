#!/usr/bin/env python3
"""
Memory Relationship Graph Service
Manages memory relationships and provides graph visualization
"""

import json
import sqlite3
from typing import Dict, List, Any, Optional
import networkx as nx
from datetime import datetime

class MemoryGraphService:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.graph = nx.DiGraph()
        self.init_graph_db()
        self.load_graph()
    
    def init_graph_db(self):
        """Initialize graph database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_nodes (
                memory_id TEXT PRIMARY KEY,
                content TEXT,
                category TEXT,
                tags TEXT,  -- JSON array
                created_timestamp TEXT,
                metadata TEXT  -- JSON object
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_memory_id TEXT,
                target_memory_id TEXT,
                relationship_type TEXT,
                confidence REAL,
                context TEXT,
                created_timestamp TEXT,
                FOREIGN KEY (source_memory_id) REFERENCES memory_nodes (memory_id),
                FOREIGN KEY (target_memory_id) REFERENCES memory_nodes (memory_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_memory_node(self, memory_id: str, content: str, category: str, 
                       tags: List[str], metadata: Dict = None):
        """Add memory node to graph"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO memory_nodes 
            (memory_id, content, category, tags, created_timestamp, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            memory_id, content, category, 
            json.dumps(tags), 
            datetime.now().isoformat(),
            json.dumps(metadata or {})
        ))
        
        conn.commit()
        conn.close()
        
        # Add to NetworkX graph
        self.graph.add_node(memory_id, 
                           content=content,
                           category=category,
                           tags=tags,
                           metadata=metadata or {})
    
    def add_relationship(self, source_id: str, target_id: str, 
                        relationship_type: str, confidence: float = 1.0,
                        context: str = ""):
        """Add relationship between memories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO memory_relationships 
            (source_memory_id, target_memory_id, relationship_type, confidence, context, created_timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (source_id, target_id, relationship_type, confidence, context, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        # Add to NetworkX graph
        self.graph.add_edge(source_id, target_id,
                           relationship_type=relationship_type,
                           confidence=confidence,
                           context=context)
    
    def load_graph(self):
        """Load graph from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Load nodes
        cursor.execute('SELECT * FROM memory_nodes')
        for row in cursor.fetchall():
            memory_id, content, category, tags, created_timestamp, metadata = row
            self.graph.add_node(memory_id,
                               content=content,
                               category=category,
                               tags=json.loads(tags) if tags else [],
                               created_timestamp=created_timestamp,
                               metadata=json.loads(metadata) if metadata else {})
        
        # Load edges
        cursor.execute('SELECT * FROM memory_relationships')
        for row in cursor.fetchall():
            _, source_id, target_id, rel_type, confidence, context, created_timestamp = row
            self.graph.add_edge(source_id, target_id,
                               relationship_type=rel_type,
                               confidence=confidence,
                               context=context,
                               created_timestamp=created_timestamp)
        
        conn.close()
    
    def find_related_memories(self, memory_id: str, max_depth: int = 2, 
                             min_confidence: float = 0.5) -> Dict:
        """Find memories related to given memory"""
        if memory_id not in self.graph:
            return {'related': [], 'graph_data': None}
        
        # BFS to find related nodes
        related_nodes = []
        visited = set()
        queue = [(memory_id, 0)]
        
        while queue:
            current_id, depth = queue.pop(0)
            
            if current_id in visited or depth > max_depth:
                continue
            
            visited.add(current_id)
            
            # Get neighbors
            for neighbor in self.graph.neighbors(current_id):
                edge_data = self.graph[current_id][neighbor]
                confidence = edge_data.get('confidence', 1.0)
                
                if confidence >= min_confidence:
                    related_nodes.append({
                        'memory_id': neighbor,
                        'relationship_type': edge_data.get('relationship_type'),
                        'confidence': confidence,
                        'depth': depth + 1,
                        'context': edge_data.get('context', '')
                    })
                    
                    if depth + 1 <= max_depth:
                        queue.append((neighbor, depth + 1))
        
        # Generate subgraph for visualization
        subgraph_nodes = [memory_id] + [r['memory_id'] for r in related_nodes]
        subgraph = self.graph.subgraph(subgraph_nodes)
        
        return {
            'related': related_nodes,
            'graph_data': self.networkx_to_d3(subgraph)
        }
    
    def networkx_to_d3(self, graph) -> Dict:
        """Convert NetworkX graph to D3.js format"""
        nodes = []
        links = []
        
        for node_id in graph.nodes():
            node_data = graph.nodes[node_id]
            nodes.append({
                'id': node_id,
                'category': node_data.get('category', 'unknown'),
                'content': node_data.get('content', '')[:100] + '...',
                'tags': node_data.get('tags', []),
                'group': self.get_category_group(node_data.get('category', 'unknown'))
            })
        
        for source, target in graph.edges():
            edge_data = graph[source][target]
            links.append({
                'source': source,
                'target': target,
                'relationship_type': edge_data.get('relationship_type', 'related_to'),
                'confidence': edge_data.get('confidence', 1.0),
                'context': edge_data.get('context', '')
            })
        
        return {'nodes': nodes, 'links': links}
    
    def get_category_group(self, category: str) -> int:
        """Map memory categories to visualization groups"""
        category_groups = {
            'project_active': 1,
            'project_research': 2,
            'preferences_coding': 3,
            'preferences_business': 4,
            'knowledge_technical': 5,
            'knowledge_business': 6
        }
        return category_groups.get(category, 0)
    
    def export_graph_json(self, file_path: str):
        """Export entire graph as JSON for external visualization"""
        graph_data = self.networkx_to_d3(self.graph)
        with open(file_path, 'w') as f:
            json.dump(graph_data, f, indent=2)

if __name__ == "__main__":
    graph_service = MemoryGraphService("/Users/josephhillin/workspace/mcp-central/graph/memory-graph.db")
    
    # Example usage
    related = graph_service.find_related_memories("example_memory_id")
    print(json.dumps(related, indent=2))
