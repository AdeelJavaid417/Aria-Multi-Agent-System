"""
Task Classification Engine
"""
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from utils.logger import logger
from config import settings
import json

class TaskClassifier:
    """Classify tasks to determine routing"""
    
    AGENT_TYPES = {
        "research": "Research Agent - Gathers and analyzes information",
        "creative": "Creative Agent - Generates creative content",
        "technical": "Technical Agent - Analyzes and optimizes code",
        "general": "General Agent - Handles general queries"
    }
    
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=0.3
        )
    
    def classify(self, task: str) -> Dict[str, Any]:
        """
        Classify a task into categories
        """
        logger.info("🎯 Classifying task...")
        
        agent_descriptions = "\n".join(
            f"- {key}: {value}" 
            for key, value in self.AGENT_TYPES.items()
        )
        
        prompt = f"""Classify this task into one of these agent types:
{agent_descriptions}

Task: {task}

Respond with ONLY valid JSON in this format:
{{
    "primary_agent": "one of: research, creative, technical, general",
    "secondary_agents": ["list of other relevant agents"],
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}}"""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        try:
            # Parse JSON response
            result = json.loads(response.content)
            logger.info(f"✓ Classification: {result['primary_agent']} (confidence: {result['confidence']})")
            return result
        except json.JSONDecodeError:
            logger.warning("Failed to parse classification, using default")
            return {
                "primary_agent": "general",
                "secondary_agents": [],
                "confidence": 0.5,
                "reasoning": "Default classification due to parsing error"
            }
    
    def classify_complexity(self, task: str) -> Dict[str, Any]:
        """
        Classify task complexity level
        """
        logger.info("📊 Assessing task complexity...")
        
        prompt = f"""Assess the complexity of this task:

Task: {task}

Rate complexity as: simple (1), moderate (2), complex (3), very_complex (4)

Also identify:
- Required skills
- Estimated difficulty
- Key challenges

Respond with JSON:
{{
    "complexity_level": 1-4,
    "required_skills": ["skill1", "skill2"],
    "estimated_difficulty": "easy/moderate/hard",
    "key_challenges": ["challenge1", "challenge2"]
}}"""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {
                "complexity_level": 2,
                "required_skills": ["general"],
                "estimated_difficulty": "moderate",
                "key_challenges": []
            }

# Global classifier instance
task_classifier = TaskClassifier()