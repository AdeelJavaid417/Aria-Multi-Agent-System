"""
Performance metrics tracking
"""
import time
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from config import settings

class MetricsCollector:
    """Collect and store performance metrics"""
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "total_execution_time": 0.0,
            "average_execution_time": 0.0,
            "tool_calls": 0,
            "total_tokens": 0,
            "agent_executions": {}
        }
        self.session_start = datetime.now()
    
    def start_timer(self) -> float:
        """Start execution timer"""
        return time.time()
    
    def end_timer(self, start_time: float) -> float:
        """End execution timer and return elapsed time"""
        return time.time() - start_time
    
    def record_task(self, task_name: str, execution_time: float, 
                   success: bool = True, tokens: int = 0) -> None:
        """Record task metrics"""
        self.metrics["total_tasks"] += 1
        
        if success:
            self.metrics["successful_tasks"] += 1
        else:
            self.metrics["failed_tasks"] += 1
        
        self.metrics["total_execution_time"] += execution_time
        self.metrics["average_execution_time"] = (
            self.metrics["total_execution_time"] / self.metrics["total_tasks"]
        )
        self.metrics["total_tokens"] += tokens
    
    def record_agent_execution(self, agent_name: str, execution_time: float, 
                              tool_calls: int = 0) -> None:
        """Record agent execution metrics"""
        if agent_name not in self.metrics["agent_executions"]:
            self.metrics["agent_executions"][agent_name] = {
                "calls": 0,
                "total_time": 0.0,
                "average_time": 0.0,
                "tool_calls": 0
            }
        
        agent_metrics = self.metrics["agent_executions"][agent_name]
        agent_metrics["calls"] += 1
        agent_metrics["total_time"] += execution_time
        agent_metrics["average_time"] = agent_metrics["total_time"] / agent_metrics["calls"]
        agent_metrics["tool_calls"] += tool_calls
        
        self.metrics["tool_calls"] += tool_calls
    
    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        session_duration = (datetime.now() - self.session_start).total_seconds()
        
        return {
            "session_duration_seconds": round(session_duration, 2),
            "total_tasks": self.metrics["total_tasks"],
            "successful_tasks": self.metrics["successful_tasks"],
            "failed_tasks": self.metrics["failed_tasks"],
            "success_rate": f"{(self.metrics['successful_tasks'] / self.metrics['total_tasks'] * 100) if self.metrics['total_tasks'] > 0 else 0:.1f}%",
            "average_execution_time": f"{self.metrics['average_execution_time']:.2f}s",
            "total_tool_calls": self.metrics["tool_calls"],
            "total_tokens_used": self.metrics["total_tokens"],
            "agent_breakdown": self.metrics["agent_executions"]
        }
    
    def save_metrics(self, filename: Optional[str] = None) -> None:
        """Save metrics to file"""
        if filename is None:
            filename = f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = settings.data_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(self.get_summary(), f, indent=2)

# Global metrics instance
metrics_collector = MetricsCollector()