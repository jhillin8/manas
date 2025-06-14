#!/usr/bin/env python3
"""
Memory Audit and Zero Trust Security System
Tracks all memory operations and enables rollback capabilities
"""

import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

class MemoryAuditSystem:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_audit_db()
        self.setup_logging()
    
    def setup_logging(self):
        """Setup audit logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/Users/josephhillin/workspace/mcp-central/security/audit.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def init_audit_db(self):
        """Initialize audit trail database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id TEXT,
                operation_type TEXT,  -- create, read, update, delete
                operation_timestamp TEXT,
                source_tool TEXT,
                source_user TEXT,
                source_ip TEXT,
                content_hash TEXT,
                previous_content_hash TEXT,
                change_summary TEXT,
                metadata TEXT  -- JSON
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id TEXT,
                snapshot_timestamp TEXT,
                content_hash TEXT,
                content TEXT,
                metadata TEXT,  -- JSON
                snapshot_type TEXT  -- manual, automatic, pre_delete
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_timestamp TEXT,
                event_type TEXT,  -- suspicious_access, failed_validation, unauthorized_change
                severity TEXT,    -- low, medium, high, critical
                source_tool TEXT,
                source_user TEXT,
                description TEXT,
                memory_id TEXT,
                metadata TEXT  -- JSON
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def calculate_content_hash(self, content: str) -> str:
        """Calculate SHA-256 hash of content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def log_memory_operation(self, memory_id: str, operation_type: str,
                           source_tool: str, content: str = None,
                           previous_content: str = None, metadata: Dict = None):
        """Log memory operation to audit trail"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        content_hash = self.calculate_content_hash(content) if content else None
        previous_hash = self.calculate_content_hash(previous_content) if previous_content else None
        
        # Generate change summary
        change_summary = self.generate_change_summary(content, previous_content)
        
        cursor.execute('''
            INSERT INTO memory_audit_log 
            (memory_id, operation_type, operation_timestamp, source_tool, source_user,
             content_hash, previous_content_hash, change_summary, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory_id, operation_type, datetime.now().isoformat(),
            source_tool, "josephhillin",  # Current user
            content_hash, previous_hash, change_summary,
            json.dumps(metadata or {})
        ))
        
        conn.commit()
        conn.close()
        
        # Log to file
        self.logger.info(f"Memory operation: {operation_type} on {memory_id} by {source_tool}")
        
        # Check for suspicious activity
        self.detect_suspicious_activity(memory_id, operation_type, source_tool)
    
    def detect_suspicious_activity(self, memory_id: str, operation_type: str, source_tool: str):
        """Detect suspicious memory access patterns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check for rapid modifications
        five_minutes_ago = (datetime.now() - timedelta(minutes=5)).isoformat()
        cursor.execute('''
            SELECT COUNT(*) FROM memory_audit_log 
            WHERE memory_id = ? AND operation_type = 'update' 
            AND operation_timestamp > ?
        ''', (memory_id, five_minutes_ago))
        
        recent_updates = cursor.fetchone()[0]
        
        if recent_updates > 5:
            self.log_security_event(
                event_type="rapid_modifications",
                severity="medium",
                source_tool=source_tool,
                description=f"Memory {memory_id} modified {recent_updates} times in 5 minutes",
                memory_id=memory_id
            )
        
        conn.close()
    
    def log_security_event(self, event_type: str, severity: str, source_tool: str,
                          description: str, memory_id: str = None, metadata: Dict = None):
        """Log security event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO security_events 
            (event_timestamp, event_type, severity, source_tool, source_user,
             description, memory_id, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(), event_type, severity,
            source_tool, "josephhillin", description, memory_id,
            json.dumps(metadata or {})
        ))
        
        conn.commit()
        conn.close()
        
        self.logger.warning(f"Security event: {event_type} - {description}")
    
    def generate_change_summary(self, new_content: str, old_content: str) -> str:
        """Generate summary of changes between content versions"""
        if not old_content:
            return "Initial content creation"
        
        if not new_content:
            return "Content deleted"
        
        # Simple change detection
        new_words = set(new_content.split())
        old_words = set(old_content.split())
        
        added_words = new_words - old_words
        removed_words = old_words - new_words
        
        changes = []
        if added_words:
            changes.append(f"Added: {len(added_words)} words")
        if removed_words:
            changes.append(f"Removed: {len(removed_words)} words")
        
        if not changes:
            return "Minor modifications"
        
        return ", ".join(changes)

if __name__ == "__main__":
    audit_system = MemoryAuditSystem("/Users/josephhillin/workspace/mcp-central/security/audit.db")
    print("Audit system initialized")
