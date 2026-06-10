"""
LangGraph Workflow - Orchestrate agents in a graph
"""
from typing import Dict, Any, List, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from utils.logger import logger
from routing import conditional_router, task_classifier
from agents import ResearchAgent, CreativeAgent, TechnicalAgent
from utils.formatter import formatter
import time

class WorkflowState(TypedDict):
    """Workflow state definition"""
    task: str
    task_classification: Dict[str, Any]
    routing_sequence: List[str]
    messages: Annotated[list, add_messages]
    context: str
    results: Dict[str, Any]
    execution_metadata: Dict[str, Any]

class ARIAWorkflow:
    """ARIA Multi-Agent Workflow"""
    
    def __init__(self):
        """Initialize workflow"""
        # Initialize agents
        self.research_agent = ResearchAgent()
        self.creative_agent = CreativeAgent()
        self.technical_agent = TechnicalAgent()
        
        self.agents_map = {
            "research": self.research_agent,
            "creative": self.creative_agent,
            "technical": self.technical_agent
        }
        
        # Build graph
        self.graph = self._build_graph()
        self.app = self.graph.compile()
        
        logger.info("✅ ARIA Workflow initialized")
    
    def _build_graph(self) -> StateGraph:
        """Build the workflow graph"""
        logger.info("🏗️  Building workflow graph...")
        
        graph = StateGraph(WorkflowState)
        
        # Add nodes
        graph.add_node("classify_task", self._classify_task_node)
        graph.add_node("route_task", self._route_task_node)
        graph.add_node("research", self._research_agent_node)
        graph.add_node("creative", self._creative_agent_node)
        graph.add_node("technical", self._technical_agent_node)
        graph.add_node("synthesize", self._synthesize_node)
        
        # Add edges
        graph.add_edge(START, "classify_task")
        graph.add_edge("classify_task", "route_task")
        graph.add_conditional_edges(
            "route_task",
            self._route_agents,
            {
                "research": "research",
                "creative": "creative",
                "technical": "technical",
                "synthesize": "synthesize",
                "end": END
            }
        )
        
        # Agent to synthesis
        graph.add_edge("research", "synthesize")
        graph.add_edge("creative", "synthesize")
        graph.add_edge("technical", "synthesize")
        graph.add_edge("synthesize", END)
        
        logger.info("✅ Workflow graph built successfully")
        return graph
    
    def _classify_task_node(self, state: WorkflowState) -> WorkflowState:
        """Classify task"""
        logger.info("📋 Classifying task...")
        
        classification = task_classifier.classify(state["task"])
        state["task_classification"] = classification
        
        formatter.print_info(
            f"Task classified as: {classification['primary_agent']} "
            f"(confidence: {classification['confidence']})"
        )
        
        return state
    
    def _route_task_node(self, state: WorkflowState) -> WorkflowState:
        """Route task to agents"""
        logger.info("🔀 Routing task...")
        
        routing = conditional_router.route(state["task"])
        state["routing_sequence"] = routing["routing_sequence"]
        
        formatter.print_info(f"Routing sequence: {' → '.join(routing['routing_sequence'])}")
        
        return state
    
    def _route_agents(self, state: WorkflowState) -> str:
        """Determine which agent to execute next"""
        routing_sequence = state.get("routing_sequence", [])
        executed_agents = list(state.get("results", {}).keys())
        
        for agent in routing_sequence:
            if agent not in executed_agents:
                return agent
        
        # All agents executed, time to synthesize
        return "synthesize"
    
    def _research_agent_node(self, state: WorkflowState) -> WorkflowState:
        """Execute research agent"""
        logger.info("📚 Executing Research Agent...")
        
        start_time = time.time()
        result = self.research_agent.execute(state["task"], state.get("context", ""))
        execution_time = time.time() - start_time
        
        if "results" not in state:
            state["results"] = {}
        
        state["results"]["research"] = result
        state["execution_metadata"] = {
            "last_agent": "research",
            "execution_time": execution_time
        }
        
        # Save context for next agents
        if result.get("synthesis"):
            state["context"] = result["synthesis"]
        
        formatter.print_success(f"Research complete in {execution_time:.2f}s")
        
        return state
    
    def _creative_agent_node(self, state: WorkflowState) -> WorkflowState:
        """Execute creative agent"""
        logger.info("✍️ Executing Creative Agent...")
        
        start_time = time.time()
        result = self.creative_agent.execute(state["task"], state.get("context", ""))
        execution_time = time.time() - start_time
        
        if "results" not in state:
            state["results"] = {}
        
        state["results"]["creative"] = result
        state["execution_metadata"] = {
            "last_agent": "creative",
            "execution_time": execution_time
        }
        
        state["context"] = result.get("enhanced_output", result.get("creative_output", ""))
        
        formatter.print_success(f"Creative execution complete in {execution_time:.2f}s")
        
        return state
    
    def _technical_agent_node(self, state: WorkflowState) -> WorkflowState:
        """Execute technical agent"""
        logger.info("💻 Executing Technical Agent...")
        
        start_time = time.time()
        result = self.technical_agent.execute(state["task"], state.get("context", ""))
        execution_time = time.time() - start_time
        
        if "results" not in state:
            state["results"] = {}
        
        state["results"]["technical"] = result
        state["execution_metadata"] = {
            "last_agent": "technical",
            "execution_time": execution_time
        }
        
        formatter.print_success(f"Technical execution complete in {execution_time:.2f}s")
        
        return state
    
    def _synthesize_node(self, state: WorkflowState) -> WorkflowState:
        """Synthesize results from all agents"""
        logger.info("🔗 Synthesizing results...")
        
        results = state.get("results", {})
        
        # Compile final output
        final_output = self._compile_results(results)
        state["results"]["final_output"] = final_output
        
        return state
    
    def _compile_results(self, results: Dict[str, Any]) -> str:
        """Compile results into final output"""
        compilation = []
        
        if "research" in results and results["research"].get("status") == "success":
            synthesis = results['research'].get('synthesis', '')
            if synthesis:
                compilation.append(f"## Research Findings\n{synthesis}")
        
        if "creative" in results and results["creative"].get("status") == "success":
            output = results['creative'].get('enhanced_output', '')
            if output:
                compilation.append(f"## Creative Output\n{output}")
        
        if "technical" in results and results["technical"].get("status") == "success":
            technical_result = results['technical']
            analysis = technical_result.get('analysis', '')
            validation = technical_result.get('validation', {})
            best_solution = validation.get('best_solution', '')
            all_solutions = validation.get('all_solutions', [])
            
            # Start with analysis if available
            if analysis:
                compilation.append(f"## Problem Analysis\n{analysis}")
            
            # Add recommended solution
            if best_solution:
                compilation.append(f"## Recommended Solution\n{best_solution}")
            
            # Add alternative solutions
            if all_solutions and len(all_solutions) > 1:
                other_solutions = all_solutions[1:]
                alternatives_text = "\n".join(f"**Option {i}:** {sol}" for i, sol in enumerate(other_solutions, 2))
                compilation.append(f"## Alternative Solutions\n{alternatives_text}")
        
        final_text = "\n\n".join(compilation)
        
        # If no results found, return a helpful message
        if not final_text:
            return "Processing your request... Solution details will appear shortly."
        
        return final_text
    
    def execute(self, task: str, context: str = "") -> Dict[str, Any]:
        """
        Execute workflow
        
        Args:
            task: Task description
            context: Additional context
        
        Returns:
            Workflow execution result
        """
        logger.info(f"🚀 Starting ARIA workflow: {task}")
        
        initial_state: WorkflowState = {
            "task": task,
            "task_classification": {},
            "routing_sequence": [],
            "messages": [],
            "context": context,
            "results": {},
            "execution_metadata": {}
        }
        
        try:
            final_state = self.app.invoke(initial_state)
            
            logger.info("✅ Workflow completed successfully")
            
            return {
                "status": "success",
                "task": task,
                "classification": final_state.get("task_classification", {}),
                "routing": final_state.get("routing_sequence", []),
                "results": final_state.get("results", {}),
                "final_output": final_state.get("results", {}).get("final_output", "")
            }
        
        except Exception as e:
            logger.error(f"❌ Workflow failed: {e}")
            
            return {
                "status": "error",
                "task": task,
                "error": str(e)
            }
    
    def get_workflow_info(self) -> Dict[str, Any]:
        """Get workflow information"""
        return {
            "workflow_name": "ARIA",
            "available_agents": list(self.agents_map.keys()),
            "total_agents": len(self.agents_map),
            "agents_status": {
                name: agent.get_status()
                for name, agent in self.agents_map.items()
            }
        }