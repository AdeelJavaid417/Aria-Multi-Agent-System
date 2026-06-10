"""
Intelligent Conditional Router
"""
from typing import Dict, Any, List
from routing.classifier import task_classifier
from utils.logger import logger

class ConditionalRouter:
    """Route tasks to appropriate agents"""
    
    AGENT_SEQUENCE = {
        "research": ["research"],
        "creative": ["creative"],
        "technical": ["technical"],
        "research_to_creative": ["research", "creative"],
        "research_to_technical": ["research", "technical"],
        "full_pipeline": ["research", "creative", "technical"],
        "general": ["creative"]
    }
    
    def __init__(self):
        self.routing_history = []
    
    def route(self, task: str) -> Dict[str, Any]:
        """
        Route task to appropriate agents
        """
        logger.info("🔀 Routing task through intelligent router...")
        
        # Classify task
        classification = task_classifier.classify(task)
        primary_agent = classification["primary_agent"]
        secondary_agents = classification.get("secondary_agents", [])
        
        # Determine routing sequence
        routing_sequence = self._determine_sequence(
            primary_agent,
            secondary_agents,
            task
        )
        
        logger.info(f"📍 Routing sequence: {' → '.join(routing_sequence)}")
        
        routing_result = {
            "task": task,
            "classification": classification,
            "routing_sequence": routing_sequence,
            "execution_order": self._optimize_sequence(routing_sequence),
            "fallback_agents": self._get_fallback_agents(primary_agent)
        }
        
        self.routing_history.append(routing_result)
        
        return routing_result
    
    def _determine_sequence(self, primary: str, secondary: List[str], 
                          task: str) -> List[str]:
        """
        Determine optimal agent sequence
        """
        # Check for common patterns
        task_lower = task.lower()
        
        if "search" in task_lower or "research" in task_lower:
            if "write" in task_lower or "create" in task_lower:
                return ["research", "creative"]
            elif "code" in task_lower or "optimize" in task_lower:
                return ["research", "technical"]
        
        if "write" in task_lower or "create" in task_lower:
            if "based on" in task_lower or "using" in task_lower:
                return ["research", "creative"]
            return ["creative"]
        
        if "code" in task_lower or "optimize" in task_lower or "debug" in task_lower:
            return ["technical"]
        
        # Default to primary agent
        return [primary] if primary != "general" else ["creative"]
    
    def _optimize_sequence(self, sequence: List[str]) -> List[str]:
        """
        Optimize agent execution order
        """
        # Research agents should always come before others
        if "research" in sequence and len(sequence) > 1:
            optimized = ["research"]
            optimized.extend([a for a in sequence if a != "research"])
            return optimized
        
        return sequence
    
    def _get_fallback_agents(self, primary_agent: str) -> List[str]:
        """
        Get fallback agents if primary fails
        """
        fallback_map = {
            "research": ["general", "creative"],
            "creative": ["general", "research"],
            "technical": ["research", "creative"],
            "general": ["creative"]
        }
        
        return fallback_map.get(primary_agent, ["general"])
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """
        Get routing statistics
        """
        agent_counts = {}
        for routing in self.routing_history:
            for agent in routing["routing_sequence"]:
                agent_counts[agent] = agent_counts.get(agent, 0) + 1
        
        return {
            "total_routings": len(self.routing_history),
            "agent_usage": agent_counts,
            "most_used_agent": max(agent_counts, key=agent_counts.get) if agent_counts else None
        }

# Global router instance
conditional_router = ConditionalRouter()