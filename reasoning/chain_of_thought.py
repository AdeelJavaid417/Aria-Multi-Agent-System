"""
Chain of Thought Reasoning Engine
"""
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from utils.logger import logger
from config import settings
import json

class ChainOfThoughtReasoner:
    """Chain of Thought reasoning engine"""
    
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=0.3
        )
    
    def think_through(self, problem: str, context: str = "") -> Dict[str, Any]:
        """
        Think through a problem step by step
        """
        logger.info("🧠 Engaging Chain of Thought reasoning...")
        
        prompt = f"""Think through this problem step-by-step.

Problem: {problem}
{f'Context: {context}' if context else ''}

Break this down into logical steps:
1. What is the core question?
2. What information do I need?
3. What assumptions am I making?
4. What are the key considerations?
5. What is my conclusion?

Provide detailed reasoning for each step."""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        reasoning_text = response.content
        steps = self._parse_reasoning(reasoning_text)
        
        return {
            "problem": problem,
            "reasoning": reasoning_text,
            "steps": steps,
            "conclusion": self._extract_conclusion(reasoning_text)
        }
    
    def verify_solution(self, problem: str, solution: str) -> Dict[str, Any]:
        """
        Verify a proposed solution
        """
        logger.info("✓ Verifying solution...")
        
        prompt = f"""Verify this solution to the problem.

Problem: {problem}
Proposed Solution: {solution}

Check:
1. Does it address the core problem?
2. Are there any logical flaws?
3. Are there edge cases not considered?
4. Is the reasoning sound?
5. What improvements could be made?

Provide a detailed verification report."""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        return {
            "problem": problem,
            "solution": solution,
            "verification": response.content,
            "is_valid": "valid" in response.content.lower() or "correct" in response.content.lower()
        }
    
    def _parse_reasoning(self, text: str) -> List[str]:
        """Parse reasoning into steps"""
        lines = text.split('\n')
        steps = [line.strip() for line in lines if line.strip()]
        return steps
    
    def _extract_conclusion(self, text: str) -> str:
        """Extract conclusion from reasoning"""
        lines = text.split('\n')
        # Find line with conclusion keyword
        for i, line in enumerate(lines):
            if 'conclusion' in line.lower():
                return '\n'.join(lines[i:i+2])
        return text[-200:]  # Return last 200 chars if no conclusion found

# Global reasoner instance
cot_reasoner = ChainOfThoughtReasoner()