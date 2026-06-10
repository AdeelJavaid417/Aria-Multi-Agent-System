"""
Metadata Database using SQLite
"""
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional
from config import settings
from utils.logger import logger

class MetadataDatabase:
    """SQLite database for metadata"""
    
    def __init__(self):
        self.db_path = settings.metrics_db_path
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Task history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_history (
                id INTEGER PRIMARY KEY,
                task_description TEXT,
                routing_sequence TEXT,
                execution_time REAL,
                status TEXT,
                created_at TIMESTAMP,
                result TEXT
            )
        """)
        
        # Agent execution table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_executions (
                id INTEGER PRIMARY KEY,
                task_id INTEGER,
                agent_name TEXT,
                execution_time REAL,
                tool_calls INTEGER,
                status TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY(task_id) REFERENCES task_history(id)
            )
        """)
        
        # Memory references table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_references (
                id INTEGER PRIMARY KEY,
                task_id INTEGER,
                memory_key TEXT,
                relevance_score REAL,
                accessed_at TIMESTAMP,
                FOREIGN KEY(task_id) REFERENCES task_history(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_task(self, task: str, routing: List[str], 
                 execution_time: float, status: str, result: str = "") -> int:
        """Save task to history"""
        logger.info(f"📝 Recording task: {task[:50]}...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO task_history 
            (task_description, routing_sequence, execution_time, status, created_at, result)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (task, ",".join(routing), execution_time, status, datetime.now(), result))
        
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return task_id
    
    def save_agent_execution(self, task_id: int, agent_name: str, 
                           execution_time: float, tool_calls: int, status: str) -> None:
        """Save agent execution details"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO agent_executions
            (task_id, agent_name, execution_time, tool_calls, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (task_id, agent_name, execution_time, tool_calls, status, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_task_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent task history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM task_history
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(zip([d[0] for d in cursor.description], row)) for row in rows]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get counts
        cursor.execute("SELECT COUNT(*) FROM task_history")
        total_tasks = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM agent_executions")
        total_executions = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(execution_time) FROM task_history")
        total_time = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "total_tasks": total_tasks,
            "total_agent_executions": total_executions,
            "total_execution_time": round(total_time, 2),
            "db_path": str(self.db_path)
        }

# Global metadata DB instance
metadata_db = MetadataDatabase()