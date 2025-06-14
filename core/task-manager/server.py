from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Literal
import uvicorn
import os
import logging
import json
import sqlite3
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Manas Task Management Service", version="1.0.0")

# Task models
class Task(BaseModel):
    id: str
    content: str
    status: Literal["pending", "in_progress", "completed", "blocked"] = "pending"
    priority: Literal["low", "medium", "high", "critical"] = "medium"
    assignee: Optional[str] = None
    tags: List[str] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    due_date: Optional[str] = None
    dependencies: List[str] = []

class TaskList(BaseModel):
    name: str
    description: Optional[str] = None
    tasks: List[Task] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class TaskUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[Literal["pending", "in_progress", "completed", "blocked"]] = None
    priority: Optional[Literal["low", "medium", "high", "critical"]] = None
    assignee: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[str] = None
    dependencies: Optional[List[str]] = None

# Database setup
DATABASE_PATH = os.getenv("DATABASE_PATH", "/data/tasks.db")

def init_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'medium',
            assignee TEXT,
            tags TEXT,
            created_at TEXT,
            updated_at TEXT,
            due_date TEXT,
            dependencies TEXT
        )
    """)
    
    # Create task_lists table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_lists (
            name TEXT PRIMARY KEY,
            description TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_database()

class TaskManager:
    def __init__(self):
        self.db_path = DATABASE_PATH
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def create_task(self, task: Task) -> Task:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        task.created_at = now
        task.updated_at = now
        
        cursor.execute("""
            INSERT INTO tasks (id, content, status, priority, assignee, tags, 
                             created_at, updated_at, due_date, dependencies)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task.id, task.content, task.status, task.priority, task.assignee,
            json.dumps(task.tags), task.created_at, task.updated_at,
            task.due_date, json.dumps(task.dependencies)
        ))
        
        conn.commit()
        conn.close()
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return Task(
            id=row[0],
            content=row[1],
            status=row[2],
            priority=row[3],
            assignee=row[4],
            tags=json.loads(row[5]) if row[5] else [],
            created_at=row[6],
            updated_at=row[7],
            due_date=row[8],
            dependencies=json.loads(row[9]) if row[9] else []
        )
    
    def update_task(self, task_id: str, update: TaskUpdate) -> Optional[Task]:
        task = self.get_task(task_id)
        if not task:
            return None
        
        # Update fields
        if update.content is not None:
            task.content = update.content
        if update.status is not None:
            task.status = update.status
        if update.priority is not None:
            task.priority = update.priority
        if update.assignee is not None:
            task.assignee = update.assignee
        if update.tags is not None:
            task.tags = update.tags
        if update.due_date is not None:
            task.due_date = update.due_date
        if update.dependencies is not None:
            task.dependencies = update.dependencies
        
        task.updated_at = datetime.now().isoformat()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE tasks SET content = ?, status = ?, priority = ?, assignee = ?,
                           tags = ?, updated_at = ?, due_date = ?, dependencies = ?
            WHERE id = ?
        """, (
            task.content, task.status, task.priority, task.assignee,
            json.dumps(task.tags), task.updated_at, task.due_date,
            json.dumps(task.dependencies), task_id
        ))
        
        conn.commit()
        conn.close()
        return task
    
    def list_tasks(self, status: Optional[str] = None, assignee: Optional[str] = None) -> List[Task]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM tasks"
        params = []
        
        conditions = []
        if status:
            conditions.append("status = ?")
            params.append(status)
        if assignee:
            conditions.append("assignee = ?")
            params.append(assignee)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        tasks = []
        for row in rows:
            tasks.append(Task(
                id=row[0],
                content=row[1],
                status=row[2],
                priority=row[3],
                assignee=row[4],
                tags=json.loads(row[5]) if row[5] else [],
                created_at=row[6],
                updated_at=row[7],
                due_date=row[8],
                dependencies=json.loads(row[9]) if row[9] else []
            ))
        
        return tasks

task_manager = TaskManager()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "task-manager",
        "database": DATABASE_PATH,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    logger.info(f"Creating task: {task.id}")
    return task_manager.create_task(task)

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, update: TaskUpdate):
    task = task_manager.update_task(task_id, update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"Updated task: {task_id}")
    return task

@app.get("/tasks", response_model=List[Task])
async def list_tasks(status: Optional[str] = None, assignee: Optional[str] = None):
    return task_manager.list_tasks(status=status, assignee=assignee)

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    conn = task_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    
    conn.commit()
    conn.close()
    logger.info(f"Deleted task: {task_id}")
    return {"success": True, "message": f"Task {task_id} deleted"}

@app.get("/stats")
async def get_task_stats():
    tasks = task_manager.list_tasks()
    
    stats = {
        "total": len(tasks),
        "by_status": {},
        "by_priority": {},
        "by_assignee": {}
    }
    
    for task in tasks:
        # Count by status
        stats["by_status"][task.status] = stats["by_status"].get(task.status, 0) + 1
        
        # Count by priority
        stats["by_priority"][task.priority] = stats["by_priority"].get(task.priority, 0) + 1
        
        # Count by assignee
        assignee = task.assignee or "unassigned"
        stats["by_assignee"][assignee] = stats["by_assignee"].get(assignee, 0) + 1
    
    return stats

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8104))
    uvicorn.run(app, host="0.0.0.0", port=port)