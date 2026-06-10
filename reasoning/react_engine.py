"""
ReAct (Reasoning + Acting) Engine
"""
from typing import Dict, Any, List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from utils.logger import logger
from config import settings
import re

class ReActEngine:
    """ReAct pattern implementation"""
    
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=0.3
        )
        self.max_iterations = 5
    
    def solve(self, task: str, tools_available: List[str]) -> Dict[str, Any]:
        """
        Solve task using ReAct pattern
        """
        logger.info("🔄 Starting ReAct reasoning...")
        
        iterations = []
        current_state = ""
        
        for i in range(self.max_iterations):
            logger.info(f"  Iteration {i+1}/{self.max_iterations}")
            
            # Generate thought and action
            response = self._get_thought_and_action(
                task,
                tools_available,
                current_state
            )
            
            thought = response.get("thought", "")
            action = response.get("action", "")
            action_input = response.get("action_input", "")
            
            logger.info(f"  💭 Thought: {thought[:100]}...")
            logger.info(f"  ⚡ Action: {action}")
            
            # Simulate observation
            observation = self._simulate_action(action, action_input)
            
            logger.info(f"  👁️  Observation: {observation[:100]}...")
            
            iteration = {
                "thought": thought,
                "action": action,
                "action_input": action_input,
                "observation": observation
            }
            iterations.append(iteration)
            current_state += f"\n{thought}\n{observation}"
            
            # Check if we have a final answer
            if "final answer" in response.get("action", "").lower():
                break
        
        return {
            "task": task,
            "iterations": iterations,
            "final_answer": iterations[-1]["observation"] if iterations else "No solution found",
            "num_iterations": len(iterations)
        }
    
    def _get_thought_and_action(self, task: str, tools: List[str], 
                               state: str) -> Dict[str, str]:
        """Get thought and action from LLM"""
        
        tools_str = ", ".join(tools) if tools else "none"
        
        prompt = f"""Solve this task using the following format:

Thought: Think about what to do
Action: Choose from {{{tools_str}}} or "final answer"
Action Input: The input for the action

Task: {task}
{f'Previous Progress: {state}' if state else ''}

Now respond in the exact format above."""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        text = response.content
        
        return {
            "thought": self._extract_section(text, "Thought"),
            "action": self._extract_section(text, "Action"),
            "action_input": self._extract_section(text, "Action Input")
        }
    
    def _simulate_action(self, action: str, action_input: str) -> str:
        """Simulate executing an action"""
        return f"Executed {action} with input '{action_input}'. Result: Success"
    
    def _extract_section(self, text: str, section: str) -> str:
        """Extract a section from text"""
        pattern = f"{section}:(.+?)(?=\n[A-Z]|$)"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""

# Global ReAct engine instance
react_engine = ReActEngine()