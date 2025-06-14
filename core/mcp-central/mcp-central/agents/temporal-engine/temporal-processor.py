#!/usr/bin/env python3
"""
Temporal Intelligence Engine for OpenMemory MCP
Manages time-aware memory relevance, decay, and surfacing
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import math
import os

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("Warning: PyYAML not available, using JSON fallback")

class TemporalIntelligenceEngine:
    def __init__(self, config_path: str = None, db_path: str = ":memory:"):
        # Default configuration if YAML not available or config file missing
        self.config = {
            "temporal_intelligence": {
                "access_tracking": {
                    "last_accessed": "timestamp",
                    "access_frequency": "number"
                },
                "relevance_modeling": {
                    "staleness_factor": "0.0-1.0",
                    "decay_rate": "medium",
                    "half_life_days": 60
                }
            },
            "memory_categories": {
                "knowledge_technical": {
                    "retention_days": -1,
                    "temporal_config": {
                        "decay_rate": "slow",
                        "half_life_days": 365,
                        "staleness_threshold": 180
                    }
                }
            }
        }
        
        # Load config if available
        if config_path and os.path.exists(config_path) and YAML_AVAILABLE:
            try:
                with open(config_path, 'r') as f:
                    loaded_config = yaml.safe_load(f)
                    if loaded_config:
                        self.config.update(loaded_config)
            except Exception as e:
                print(f"Warning: Could not load config from {config_path}: {e}")
        
        self.db_path = db_path
        self.init_temporal_db()
    
    def init_temporal_db(self):
        """Initialize temporal tracking database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_temporal_data (
                memory_id TEXT PRIMARY KEY,
                created_timestamp TEXT,
                last_accessed TEXT,
                access_count INTEGER DEFAULT 0,
                access_frequency REAL DEFAULT 0.0,
                staleness_factor REAL DEFAULT 0.0,
                relevance_score REAL DEFAULT 1.0,
                decay_rate TEXT,
                half_life_days INTEGER,
                next_review_date TEXT,
                temporal_tags TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id TEXT,
                access_timestamp TEXT,
                access_context TEXT,
                tool_source TEXT,
                query_type TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_memory_access(self, memory_id: str, context: str, 
                           tool_source: str, query_type: str = "retrieval"):
        """Record memory access and update temporal metadata"""
        # Ensure tables exist
        self.init_temporal_db()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        # Log access
        cursor.execute('''
            INSERT INTO access_log (memory_id, access_timestamp, access_context, tool_source, query_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (memory_id, now, context, tool_source, query_type))
        
        # Initialize or update temporal data
        cursor.execute('''
            INSERT OR IGNORE INTO memory_temporal_data 
            (memory_id, created_timestamp, last_accessed, access_count, decay_rate, half_life_days)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (memory_id, now, now, 0, "medium", 60))
        
        # Update temporal data
        cursor.execute('''
            UPDATE memory_temporal_data 
            SET last_accessed = ?, access_count = access_count + 1
            WHERE memory_id = ?
        ''', (now, memory_id))
        
        conn.commit()
        conn.close()
        
        # Recalculate relevance score
        return self.update_relevance_score(memory_id)
    
    def calculate_staleness_factor(self, memory_id: str) -> float:
        """Calculate how stale a memory has become"""
        # Ensure tables exist
        self.init_temporal_db()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT last_accessed, decay_rate, half_life_days 
            FROM memory_temporal_data 
            WHERE memory_id = ?
        ''', (memory_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result or not result[0]:
            return 0.0
        
        last_accessed, decay_rate, half_life_days = result
        
        # Calculate time since last access
        try:
            last_access_dt = datetime.fromisoformat(last_accessed)
            days_since_access = (datetime.now() - last_access_dt).days
        except:
            return 0.0
        
        # Apply decay function based on rate
        if decay_rate == "fast":
            staleness = 1 - math.exp(-days_since_access / (half_life_days * 0.5))
        elif decay_rate == "medium":
            staleness = 1 - math.exp(-days_since_access / half_life_days)
        elif decay_rate == "slow":
            staleness = 1 - math.exp(-days_since_access / (half_life_days * 1.5))
        else:  # very_slow
            staleness = 1 - math.exp(-days_since_access / (half_life_days * 2))
        
        return min(staleness, 1.0)
    
    def update_relevance_score(self, memory_id: str) -> float:
        """Update relevance score based on access patterns and staleness"""
        # Ensure tables exist
        self.init_temporal_db()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get access frequency (last 30 days)
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        cursor.execute('''
            SELECT COUNT(*) FROM access_log 
            WHERE memory_id = ? AND access_timestamp > ?
        ''', (memory_id, thirty_days_ago))
        
        result = cursor.fetchone()
        recent_access_count = result[0] if result else 0
        
        # Calculate staleness
        staleness = self.calculate_staleness_factor(memory_id)
        
        # Base relevance (inverse of staleness)
        base_relevance = 1.0 - staleness
        
        # Frequency boost
        frequency_boost = min(recent_access_count * 0.1, 0.5)
        
        # Calculate final relevance score
        relevance_score = min(base_relevance + frequency_boost, 1.0)
        
        # Update database
        cursor.execute('''
            UPDATE memory_temporal_data 
            SET staleness_factor = ?, relevance_score = ?
            WHERE memory_id = ?
        ''', (staleness, relevance_score, memory_id))
        
        conn.commit()
        conn.close()
        
        return relevance_score
    
    def get_forgotten_gems(self, limit: int = 10) -> List[Dict]:
        """Identify valuable memories that haven't been accessed recently"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT memory_id, staleness_factor, access_count, last_accessed
            FROM memory_temporal_data
            WHERE staleness_factor > 0.6 
            AND access_count > 5
            AND last_accessed < date('now', '-30 days')
            ORDER BY access_count DESC, staleness_factor DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        forgotten_gems = []
        for row in results:
            forgotten_gems.append({
                'memory_id': row[0],
                'staleness_factor': row[1],
                'historical_access_count': row[2],
                'last_accessed': row[3],
                'reason': 'Previously valuable but forgotten'
            })
        
        return forgotten_gems
    
    def generate_review_queue(self) -> Dict[str, List]:
        """Generate prioritized review queue for memory maintenance"""
        review_queue = {
            'forgotten_gems': self.get_forgotten_gems(5),
            'expiring_soon': [],  # Placeholder
            'trending_up': [],    # Placeholder
            'context_relevant': []  # Placeholder
        }
        
        return review_queue

if __name__ == "__main__":
    import tempfile
    
    # Use a temporary file instead of in-memory for testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        engine = TemporalIntelligenceEngine(db_path=tmp.name)
    
    # Test basic functionality
    engine.record_memory_access("test_memory", "test_context", "test_tool")
    staleness = engine.calculate_staleness_factor("test_memory")
    relevance = engine.update_relevance_score("test_memory")
    
    print(f"Staleness: {staleness}, Relevance: {relevance}")
    print("Temporal engine test completed successfully")
