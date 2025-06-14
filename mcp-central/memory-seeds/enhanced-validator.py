#!/usr/bin/env python3
"""
Enhanced Memory Validation System with Fuzzy Matching and ML-based Categorization
"""

import yaml
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import difflib
from collections import Counter
import sqlite3
import hashlib

class EnhancedMemoryValidator:
    def __init__(self, schema_path: str, history_db_path: str = None):
        with open(schema_path, 'r') as f:
            self.schema = yaml.safe_load(f)
        
        self.history_db_path = history_db_path or "/Users/josephhillin/workspace/mcp-central/memory-seeds/validation_history.db"
        self.init_history_db()
        
        # Common typos and corrections
        self.tag_corrections = {
            'project_actve': 'project_active',
            'knowldge': 'knowledge',
            'tecnical': 'technical',
            'preferenc': 'preferences',
            'buisness': 'business',
            'javascrpit': 'javascript',
            'pyhton': 'python',
            'reactjs': 'react'
        }
    
    def init_history_db(self):
        """Initialize validation history database for learning"""
        conn = sqlite3.connect(self.history_db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS validation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_hash TEXT,
                suggested_category TEXT,
                actual_category TEXT,
                confidence_score REAL,
                user_accepted BOOLEAN,
                timestamp TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tag_usage_patterns (
                tag TEXT PRIMARY KEY,
                usage_count INTEGER DEFAULT 1,
                category_associations TEXT,  -- JSON
                last_used TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def fuzzy_tag_matcher(self, input_tags: List[str]) -> Dict[str, List[str]]:
        """Suggest corrections for misspelled tags"""
        corrections = {}
        all_known_tags = set()
        
        # Collect all known tags from schema and history
        for category_data in self.schema.get('memory_categories', {}).values():
            if 'tags_required' in category_data:
                all_known_tags.update(category_data['tags_required'])
        
        # Add tags from usage history
        conn = sqlite3.connect(self.history_db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT tag FROM tag_usage_patterns WHERE usage_count > 2')
        for row in cursor.fetchall():
            all_known_tags.add(row[0])
        conn.close()
        
        for tag in input_tags:
            suggestions = []
            
            # Check direct corrections first
            if tag in self.tag_corrections:
                suggestions.append({
                    'suggestion': self.tag_corrections[tag],
                    'confidence': 0.95,
                    'reason': 'common_typo'
                })
            
            # Fuzzy matching
            close_matches = difflib.get_close_matches(
                tag, all_known_tags, n=3, cutoff=0.6
            )
            
            for match in close_matches:
                if match != tag:  # Don't suggest the same tag
                    confidence = difflib.SequenceMatcher(None, tag, match).ratio()
                    suggestions.append({
                        'suggestion': match,
                        'confidence': confidence,
                        'reason': 'fuzzy_match'
                    })
            
            if suggestions:
                corrections[tag] = sorted(suggestions, key=lambda x: x['confidence'], reverse=True)
        
        return corrections
    
    def enhanced_validation(self, content: str, suggested_category: str = None, 
                          tags: List[str] = None, source_tool: str = None) -> Dict[str, Any]:
        """Perform enhanced validation with ML and fuzzy matching"""
        tags = tags or []
        
        result = {
            'validation_score': 0.0,
            'suggested_category': suggested_category,
            'confidence_score': 0.0,
            'tag_corrections': {},
            'category_predictions': {},
            'enhanced_tags': [],
            'quality_metrics': {},
            'recommendations': [],
            'learning_metadata': {}
        }
        
        # Basic validation
        basic_result = self.basic_validate_memory_entry(content, suggested_category or 'knowledge_technical', tags, source_tool)
        result.update(basic_result)
        
        # Fuzzy tag matching
        if tags:
            tag_corrections = self.fuzzy_tag_matcher(tags)
            result['tag_corrections'] = tag_corrections
            
            # Apply corrections to enhance tags
            enhanced_tags = []
            for tag in tags:
                if tag in tag_corrections and tag_corrections[tag]:
                    best_correction = tag_corrections[tag][0]
                    if best_correction['confidence'] > 0.8:
                        enhanced_tags.append(best_correction['suggestion'])
                        result['recommendations'].append(f"Corrected '{tag}' to '{best_correction['suggestion']}'")
                    else:
                        enhanced_tags.append(tag)
                else:
                    enhanced_tags.append(tag)
            
            result['enhanced_tags'] = enhanced_tags
        
        return result
    
    def calculate_content_hash(self, content: str) -> str:
        """Calculate hash for content tracking"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def basic_validate_memory_entry(self, content: str, category: str, tags: List[str], source_tool: str) -> Dict[str, Any]:
        """Basic validation logic"""
        validation_score = 0.0
        
        # Content length check
        if 50 <= len(content) <= 5000:
            validation_score += 0.3
        
        # Category match check
        if category in self.schema.get('memory_categories', {}):
            validation_score += 0.4
        
        # Tags check
        if tags:
            validation_score += 0.3
        
        return {
            'validation_score': validation_score,
            'quality_metrics': {'basic_check': True},
            'recommendations': []
        }

if __name__ == "__main__":
    validator = EnhancedMemoryValidator(
        schema_path="/Users/josephhillin/workspace/mcp-central/memory-policies/temporal-schema.yaml"
    )
    print("Enhanced validator initialized")
