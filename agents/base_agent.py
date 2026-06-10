"""
Base Agent Class - Abstract base for all agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time
from datetime import datetime
from utils.logger import logger
from utils.metrics import metrics_collector
from memory import vector_store, metadata_db
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from config import settings

class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name: str, description: str, system_prompt: str):
        """
        Initialize agent
        
        Args:
            name: Agent name
            description: Agent description
            system_prompt: System prompt for the agent
        """
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        
        # Initialize LLM
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=0.7
        )
        
        # Message history
        self.messages: List[BaseMessage] = []
        
        # Execution tracking
        self.last_execution_time = 0.0
        self.execution_count = 0
        self.tool_calls_count = 0
        
        logger.info(f"✅ Agent initialized: {self.name}")
    
    @abstractmethod
    def execute(self, task: str, context: str = "") -> Dict[str, Any]:
        """
        Execute agent task
        
        Args:
            task: Task description
            context: Additional context
        
        Returns:
            Execution result
        """
        pass
    
    @abstractmethod
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get available tools for this agent"""
        pass
    
    def think(self, problem: str, context: str = "") -> str:
        """
        Agent thinks through a problem step-by-step
        
        Args:
            problem: Problem to think about
            context: Additional context
        
        Returns:
            Reasoning output
        """
        logger.info(f"🧠 {self.name} thinking about: {problem[:50]}...")
        
        prompt = f"""You are {self.name}.
{self.system_prompt}

Think step-by-step about this problem:
{problem}

{f'Context: {context}' if context else ''}

Provide detailed reasoning before taking action."""
        
        response = self.llm.invoke([
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ])
        
        reasoning = response.content
        self.messages.append(HumanMessage(content=problem))
        self.messages.append(response)
        
        return reasoning
    
    def invoke_llm(self, prompt: str, use_history: bool = True) -> str:
        """
        Invoke LLM with prompt
        
        Args:
            prompt: User prompt
            use_history: Use message history
        
        Returns:
            LLM response
        """
        messages = []
        
        # Add system prompt
        messages.append(SystemMessage(content=self.system_prompt))
        
        # Add history if enabled
        if use_history and self.messages:
            messages.extend(self.messages[-5:])  # Last 5 messages
        
        # Add current prompt
        messages.append(HumanMessage(content=prompt))
        
        response = self.llm.invoke(messages)
        
        # Update history
        self.messages.append(HumanMessage(content=prompt))
        self.messages.append(response)
        
        return response.content
    
    def save_to_memory(self, key: str, content: str, 
                      metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Save information to memory
        
        Args:
            key: Memory key
            content: Content to save
            metadata: Additional metadata
        """
        if settings.enable_memory:
            vector_store.save_memory(key, content, metadata or {})
            logger.info(f"💾 Saved to memory: {key}")
    
    def retrieve_from_memory(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve information from memory
        
        Args:
            query: Search query
            top_k: Number of results
        
        Returns:
            Retrieved memories
        """
        if settings.enable_memory:
            results = vector_store.retrieve_memory(query, top_k)
            logger.info(f"🔍 Retrieved {len(results)} memories")
            return results
        return []
    
    def record_execution(self, task: str, result: str, 
                        success: bool = True, tool_calls: int = 0) -> int:
        """
        Record execution in metadata database
        
        Args:
            task: Task description
            result: Result/output
            success: Execution status
            tool_calls: Number of tool calls
        
        Returns:
            Task ID for tracking
        """
        task_id = metadata_db.save_task(
            task=task,
            routing=[self.name],
            execution_time=self.last_execution_time,
            status="success" if success else "failed",
            result=result
        )
        
        metadata_db.save_agent_execution(
            task_id=task_id,
            agent_name=self.name,
            execution_time=self.last_execution_time,
            tool_calls=tool_calls,
            status="success" if success else "failed"
        )
        
        return task_id
    
    def track_execution(self, func):
        """Decorator to track execution metrics"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                self.last_execution_time = time.time() - start_time
                self.execution_count += 1
                
                metrics_collector.record_agent_execution(
                    agent_name=self.name,
                    execution_time=self.last_execution_time,
                    tool_calls=self.tool_calls_count
                )
                
                logger.info(f"✅ {self.name} execution completed in {self.last_execution_time:.2f}s")
                return result
            
            except Exception as e:
                self.last_execution_time = time.time() - start_time
                logger.error(f"❌ {self.name} execution failed: {e}")
                raise
        
        return wrapper
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "name": self.name,
            "description": self.description,
            "execution_count": self.execution_count,
            "last_execution_time": f"{self.last_execution_time:.2f}s",
            "total_tool_calls": self.tool_calls_count,
            "message_history_length": len(self.messages)
        }
    
    def reset(self) -> None:
        """Reset agent state"""
        self.messages = []
        self.tool_calls_count = 0
        logger.info(f"🔄 {self.name} reset")