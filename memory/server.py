from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Manas Memory Service", version="1.0.0")

# Memory storage (in-memory for now)
memory_store = {}

class Memory(BaseModel):
    id: str
    content: str
    type: str = "text"
    metadata: Dict = {}
    timestamp: Optional[str] = None

class MemoryQuery(BaseModel):
    query: str
    type: Optional[str] = None
    limit: int = 10

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "memory-service",
        "backend": os.getenv("MEMORY_BACKEND", "in-memory"),
        "vector_db": os.getenv("VECTOR_DB_URL", "not configured"),
        "graph_db": os.getenv("GRAPH_DB_URL", "not configured")
    }

@app.post("/memories")
async def create_memory(memory: Memory):
    memory_store[memory.id] = memory.dict()
    logger.info(f"Created memory: {memory.id}")
    return {"success": True, "id": memory.id}

@app.get("/memories/{memory_id}")
async def get_memory(memory_id: str):
    if memory_id not in memory_store:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory_store[memory_id]

@app.get("/memories")
async def list_memories():
    return list(memory_store.values())

@app.post("/memories/search")
async def search_memories(query: MemoryQuery):
    # Simple text search for now
    results = []
    search_term = query.query.lower()
    
    for memory in memory_store.values():
        if search_term in memory["content"].lower():
            results.append(memory)
            if len(results) >= query.limit:
                break
    
    return {"results": results, "total": len(results)}

@app.delete("/memories/{memory_id}")
async def delete_memory(memory_id: str):
    if memory_id not in memory_store:
        raise HTTPException(status_code=404, detail="Memory not found")
    del memory_store[memory_id]
    return {"success": True}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8083))
    uvicorn.run(app, host="0.0.0.0", port=port)