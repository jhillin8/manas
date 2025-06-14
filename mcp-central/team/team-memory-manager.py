#!/usr/bin/env python3
"""
Team-Mode Memory Sharing System
Enables secure multi-user memory sharing with access controls and collaboration features
"""

import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
import uuid
from enum import Enum
import os

class AccessLevel(Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    OWNER = "owner"

class ShareScope(Enum):
    PERSONAL = "personal"
    TEAM = "team"
    ORGANIZATION = "organization"
    PUBLIC = "public"

class TeamMemoryManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_team_db()
    
    def init_team_db(self):
        """Initialize team memory sharing database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Teams table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                team_id TEXT PRIMARY KEY,
                team_name TEXT NOT NULL,
                description TEXT,
                created_by TEXT,
                created_timestamp TEXT,
                settings TEXT  -- JSON
            )
        ''')
        
        # Team members
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id TEXT,
                user_id TEXT,
                access_level TEXT,
                joined_timestamp TEXT,
                invited_by TEXT,
                FOREIGN KEY (team_id) REFERENCES teams (team_id)
            )
        ''')
        
        # Memory sharing permissions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_sharing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id TEXT,
                owner_user_id TEXT,
                share_scope TEXT,
                team_id TEXT,
                access_level TEXT,
                shared_timestamp TEXT,
                expires_timestamp TEXT,
                settings TEXT  -- JSON
            )
        ''')
        
        # Team memory access log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_access_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id TEXT,
                user_id TEXT,
                team_id TEXT,
                action TEXT,  -- view, edit, share, unshare
                timestamp TEXT,
                metadata TEXT  -- JSON
            )
        ''')
        
        # Memory collaboration
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_collaboration (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id TEXT,
                user_id TEXT,
                team_id TEXT,
                contribution_type TEXT,  -- annotation, enhancement, tag_addition
                content TEXT,
                timestamp TEXT,
                metadata TEXT  -- JSON
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_team(self, team_name: str, description: str, created_by: str,
                   settings: Dict = None) -> str:
        """Create a new team"""
        team_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO teams (team_id, team_name, description, created_by, created_timestamp, settings)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            team_id, team_name, description, created_by,
            datetime.now().isoformat(),
            json.dumps(settings or {})
        ))
        
        # Add creator as owner
        cursor.execute('''
            INSERT INTO team_members (team_id, user_id, access_level, joined_timestamp, invited_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (team_id, created_by, AccessLevel.OWNER.value, datetime.now().isoformat(), created_by))
        
        conn.commit()
        conn.close()
        
        return team_id
    
    def add_team_member(self, team_id: str, user_id: str, access_level: AccessLevel,
                       invited_by: str) -> bool:
        """Add member to team"""
        # Check if inviter has admin/owner permissions
        if not self.has_permission(invited_by, team_id, AccessLevel.ADMIN):
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO team_members 
            (team_id, user_id, access_level, joined_timestamp, invited_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (team_id, user_id, access_level.value, datetime.now().isoformat(), invited_by))
        
        conn.commit()
        conn.close()
        
        return True
    
    def share_memory(self, memory_id: str, owner_user_id: str, share_scope: ShareScope,
                    team_id: str = None, access_level: AccessLevel = AccessLevel.READ,
                    expires_hours: int = None) -> Dict[str, Any]:
        """Share memory with team or make public"""
        
        # Validate team membership if sharing with team
        if share_scope == ShareScope.TEAM and team_id:
            if not self.is_team_member(owner_user_id, team_id):
                return {"success": False, "error": "Not a team member"}
        
        expires_timestamp = None
        if expires_hours:
            expires_timestamp = (datetime.now() + timedelta(hours=expires_hours)).isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO memory_sharing 
            (memory_id, owner_user_id, share_scope, team_id, access_level, 
             shared_timestamp, expires_timestamp, settings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory_id, owner_user_id, share_scope.value, team_id,
            access_level.value, datetime.now().isoformat(),
            expires_timestamp, json.dumps({})
        ))
        
        conn.commit()
        conn.close()
        
        # Log sharing action
        self.log_team_access(memory_id, owner_user_id, team_id, "share")
        
        return {
            "success": True,
            "memory_id": memory_id,
            "share_scope": share_scope.value,
            "access_level": access_level.value,
            "expires_timestamp": expires_timestamp
        }
    
    def get_accessible_memories(self, user_id: str, team_id: str = None) -> List[Dict]:
        """Get memories accessible to user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        accessible_memories = []
        
        # Personal memories (owned by user)
        cursor.execute('''
            SELECT memory_id, share_scope, access_level, shared_timestamp
            FROM memory_sharing 
            WHERE owner_user_id = ?
        ''', (user_id,))
        
        for row in cursor.fetchall():
            accessible_memories.append({
                "memory_id": row[0],
                "access_type": "owner",
                "share_scope": row[1],
                "access_level": "owner",
                "shared_timestamp": row[3]
            })
        
        # Team memories (if user is team member)
        if team_id and self.is_team_member(user_id, team_id):
            cursor.execute('''
                SELECT ms.memory_id, ms.share_scope, ms.access_level, ms.shared_timestamp,
                       ms.owner_user_id
                FROM memory_sharing ms
                WHERE ms.team_id = ? AND ms.share_scope = 'team'
                AND (ms.expires_timestamp IS NULL OR ms.expires_timestamp > ?)
            ''', (team_id, datetime.now().isoformat()))
            
            for row in cursor.fetchall():
                if row[4] != user_id:  # Don't duplicate owned memories
                    accessible_memories.append({
                        "memory_id": row[0],
                        "access_type": "team_shared",
                        "share_scope": row[1],
                        "access_level": row[2],
                        "shared_timestamp": row[3],
                        "owner": row[4]
                    })
        
        # Public memories
        cursor.execute('''
            SELECT memory_id, share_scope, access_level, shared_timestamp, owner_user_id
            FROM memory_sharing 
            WHERE share_scope = 'public'
            AND (expires_timestamp IS NULL OR expires_timestamp > ?)
        ''', (datetime.now().isoformat(),))
        
        for row in cursor.fetchall():
            if row[4] != user_id:  # Don't duplicate owned memories
                accessible_memories.append({
                    "memory_id": row[0],
                    "access_type": "public",
                    "share_scope": row[1],
                    "access_level": row[2],
                    "shared_timestamp": row[3],
                    "owner": row[4]
                })
        
        conn.close()
        return accessible_memories
    
    def can_access_memory(self, user_id: str, memory_id: str, 
                         required_level: AccessLevel = AccessLevel.READ) -> bool:
        """Check if user can access memory with required permission level"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if user owns the memory
        cursor.execute('''
            SELECT 1 FROM memory_sharing 
            WHERE memory_id = ? AND owner_user_id = ?
        ''', (memory_id, user_id))
        
        if cursor.fetchone():
            conn.close()
            return True
        
        # Check team access
        cursor.execute('''
            SELECT ms.access_level, ms.team_id
            FROM memory_sharing ms
            WHERE ms.memory_id = ? 
            AND ms.share_scope IN ('team', 'public')
            AND (ms.expires_timestamp IS NULL OR ms.expires_timestamp > ?)
        ''', (memory_id, datetime.now().isoformat()))
        
        for row in cursor.fetchall():
            access_level_str, team_id = row
            
            # For team memories, check membership
            if team_id and not self.is_team_member(user_id, team_id):
                continue
            
            # Check access level hierarchy
            access_level = AccessLevel(access_level_str)
            if self.access_level_sufficient(access_level, required_level):
                conn.close()
                return True
        
        conn.close()
        return False
    
    def access_level_sufficient(self, granted: AccessLevel, required: AccessLevel) -> bool:
        """Check if granted access level is sufficient for required level"""
        hierarchy = {
            AccessLevel.READ: 1,
            AccessLevel.WRITE: 2,
            AccessLevel.ADMIN: 3,
            AccessLevel.OWNER: 4
        }
        return hierarchy[granted] >= hierarchy[required]
    
    def is_team_member(self, user_id: str, team_id: str) -> bool:
        """Check if user is a team member"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 1 FROM team_members 
            WHERE user_id = ? AND team_id = ?
        ''', (user_id, team_id))
        
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    
    def has_permission(self, user_id: str, team_id: str, required_level: AccessLevel) -> bool:
        """Check if user has required permission level in team"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT access_level FROM team_members 
            WHERE user_id = ? AND team_id = ?
        ''', (user_id, team_id))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return False
        
        user_level = AccessLevel(result[0])
        return self.access_level_sufficient(user_level, required_level)
    
    def log_team_access(self, memory_id: str, user_id: str, team_id: str = None,
                       action: str = "view", metadata: Dict = None):
        """Log team memory access"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO team_access_log 
            (memory_id, user_id, team_id, action, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            memory_id, user_id, team_id, action,
            datetime.now().isoformat(),
            json.dumps(metadata or {})
        ))
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    # Test team memory system
    team_manager = TeamMemoryManager("/Users/josephhillin/workspace/mcp-central/team/team-memory.db")
    
    # Create test team
    team_id = team_manager.create_team(
        team_name="AI Development Team",
        description="Team for AI/ML development projects",
        created_by="josephhillin"
    )
    
    print(f"Created team: {team_id}")
    
    # Test memory sharing
    share_result = team_manager.share_memory(
        memory_id="test_memory_001",
        owner_user_id="josephhillin",
        share_scope=ShareScope.TEAM,
        team_id=team_id,
        access_level=AccessLevel.READ
    )
    
    print(f"Share result: {share_result}")
