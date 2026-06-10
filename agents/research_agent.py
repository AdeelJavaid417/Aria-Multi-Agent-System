"""
Research Agent - Gathers and analyzes information
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from prompts import RESEARCH_SYSTEM_PROMPT, RESEARCH_REASONING_PROMPT
from tools.web_tools import tavily_search, data_fetch
from utils.logger import logger
from reasoning import cot_reasoner
import json

class ResearchAgent(BaseAgent):
    """Specialized agent for research tasks"""
    
    def __init__(self):
        """Initialize Research Agent"""
        super().__init__(
            name="Research Agent",
            description="Specialized in gathering, analyzing, and synthesizing information",
            system_prompt=RESEARCH_SYSTEM_PROMPT
        )
    
    def execute(self, task: str, context: str = "") -> Dict[str, Any]:
        """
        Execute research task
        
        Args:
            task: Research task description
            context: Additional context
        
        Returns:
            Research findings
        """
        logger.info(f"🔬 {self.name} executing: {task}")
        
        try:
            # Step 1: Think through the research
            reasoning = self.think(task, context)
            
            # Step 2: Conduct research using tools
            findings = self._conduct_research(task)
            
            # Step 3: Synthesize findings
            synthesis = self._synthesize_findings(task, findings)
            
            # Step 4: Save to memory
            self.save_to_memory(
                key=f"research_{task[:30]}",
                content=synthesis,
                metadata={
                    "type": "research",
                    "task": task,
                    "findings_count": len(findings.get("results", []))
                }
            )
            
            # Record execution
            self.record_execution(
                task=task,
                result=synthesis,
                success=True,
                tool_calls=self.tool_calls_count
            )
            
            return {
                "status": "success",
                "task": task,
                "reasoning": reasoning,
                "findings": findings,
                "synthesis": synthesis,
                "execution_time": self.last_execution_time
            }
        
        except Exception as e:
            logger.error(f"❌ Research agent error: {e}")
            self.record_execution(task=task, result=str(e), success=False)
            
            return {
                "status": "error",
                "error": str(e),
                "task": task
            }
    
    def _conduct_research(self, task: str) -> Dict[str, Any]:
        """Conduct research using available tools"""
        logger.info("📚 Conducting research...")
        
        # Use Tavily search
        search_results = tavily_search.search(task, max_results=5)
        self.tool_calls_count += 1
        
        if search_results["status"] == "error":
            logger.warning("⚠️  Tavily search failed, returning empty results")
            return {
                "status": "partial",
                "results": [],
                "sources": []
            }
        
        return {
            "status": "success",
            "results": search_results.get("results", []),
            "raw_response": search_results.get("raw_response", ""),
            "results_count": search_results.get("results_count", 0)
        }
    
    def _synthesize_findings(self, task: str, findings: Dict[str, Any]) -> str:
        """Synthesize research findings into insights"""
        logger.info("🔗 Synthesizing findings...")
        
        if not findings["results"]:
            return "No findings available for synthesis"
        
        # Create synthesis prompt
        results_text = "\n".join([
            f"- {str(result)[:200]}" 
            for result in findings["results"][:5]
        ])
        
        prompt = f"""Based on this research data, provide a comprehensive synthesis:

Task: {task}

Research Results:
{results_text}

Please provide:
1. Executive Summary
2. Key Findings (3-5 main points)
3. Important Insights
4. Recommendations
5. Sources Summary"""
        
        synthesis = self.invoke_llm(prompt)
        return synthesis
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get available tools"""
        return [
            {
                "name": "web_search",
                "description": "Search the web using Tavily",
                "function": tavily_search.search
            },
            {
                "name": "fetch_data",
                "description": "Fetch data from API endpoint",
                "function": data_fetch.fetch
            }
        ]
    
    def deep_research(self, topic: str, aspects: List[str]) -> Dict[str, Any]:
        """
        Conduct deep research on multiple aspects of a topic
        
        Args:
            topic: Main research topic
            aspects: Specific aspects to research
        
        Returns:
            Comprehensive research results
        """
        logger.info(f"🔬 Conducting deep research on: {topic}")
        
        all_findings = {}
        
        for aspect in aspects:
            research_query = f"{topic}: {aspect}"
            findings = self._conduct_research(research_query)
            all_findings[aspect] = findings
        
        return {
            "topic": topic,
            "aspects_researched": len(aspects),
            "findings_by_aspect": all_findings
        }
    
    def verify_information(self, claim: str) -> Dict[str, Any]:
        """
        Verify a claim through research
        
        Args:
            claim: Claim to verify
        
        Returns:
            Verification results
        """
        logger.info(f"✓ Verifying claim: {claim}")
        
        # Search for supporting evidence
        findings = self._conduct_research(f"verify: {claim}")
        
        # Use COT to analyze
        verification = cot_reasoner.verify_solution(
            problem="Is this claim accurate?",
            solution=claim
        )
        
        return {
            "claim": claim,
            "research_findings": findings,
            "verification_analysis": verification
        }