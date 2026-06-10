"""
Technical Agent - Analyzes and optimizes code
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from prompts import TECHNICAL_SYSTEM_PROMPT, CODE_VALIDATION_PROMPT
from tools.code_tools import code_executor, code_analyzer
from utils.logger import logger

class TechnicalAgent(BaseAgent):
    """Specialized agent for technical tasks"""
    
    def __init__(self):
        """Initialize Technical Agent"""
        super().__init__(
            name="Technical Agent",
            description="Specialized in code analysis, optimization, and technical problem-solving",
            system_prompt=TECHNICAL_SYSTEM_PROMPT
        )
    
    def execute(self, task: str, context: str = "") -> Dict[str, Any]:
        """
        Execute technical task
        
        Args:
            task: Technical task description
            context: Additional context
        
        Returns:
            Technical analysis result
        """
        logger.info(f"💻 {self.name} executing: {task}")
        
        try:
            # Step 1: Analyze the problem
            reasoning = self.think(task, context)
            
            # Step 2: Identify the issue
            analysis = self._analyze_problem(task)
            
            # Step 3: Propose solutions
            solutions = self._propose_solutions(task, analysis)
            
            # Step 4: Validate solutions
            validation = self._validate_solutions(solutions)
            
            # Step 5: Save to memory
            self.save_to_memory(
                key=f"technical_{task[:30]}",
                content=validation.get("best_solution", ""),
                metadata={
                    "type": "technical",
                    "task": task,
                    "solutions_count": len(solutions)
                }
            )
            
            # Record execution
            self.record_execution(
                task=task,
                result=validation.get("best_solution", ""),
                success=True,
                tool_calls=self.tool_calls_count
            )
            
            return {
                "status": "success",
                "task": task,
                "reasoning": reasoning,
                "analysis": analysis,
                "solutions": solutions,
                "validation": validation,
                "execution_time": self.last_execution_time
            }
        
        except Exception as e:
            logger.error(f"❌ Technical agent error: {e}")
            self.record_execution(task=task, result=str(e), success=False)
            
            return {
                "status": "error",
                "error": str(e),
                "task": task
            }
    
    def _analyze_problem(self, task: str) -> str:
        """Analyze the technical problem"""
        logger.info("🔍 Analyzing problem...")
        
        prompt = f"""Analyze this problem comprehensively:

Problem: {task}

Provide a structured analysis with:
1. Problem Statement - Clear restatement of the issue
2. Root Cause Analysis - Why this is happening
3. Impact Assessment - What effects this has
4. Affected Components - What systems/parts are involved
5. Complexity Level - Easy/Medium/Hard assessment

Format your response clearly with each section labeled."""
        
        analysis = self.invoke_llm(prompt)
        return analysis if analysis else "Analysis processing..."
    
    def _propose_solutions(self, task: str, analysis: str) -> List[str]:
        """Propose solutions"""
        logger.info("💡 Proposing solutions...")
        
        prompt = f"""Based on this analysis, propose multiple solutions:

Problem: {task}

Analysis:
{analysis}

Propose at least 3 solutions ranked by effectiveness:
1. Solution 1 with pros/cons
2. Solution 2 with pros/cons
3. Solution 3 with pros/cons

Include implementation complexity and time estimate."""
        
        response = self.invoke_llm(prompt)
        
        # Parse solutions - filter out empty lines and numbering
        solutions = []
        for line in response.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Remove common numbering patterns
                if line[0].isdigit() and ('. ' in line or ': ' in line):
                    line = line.split('. ', 1)[-1] if '. ' in line else line.split(': ', 1)[-1]
                if line:
                    solutions.append(line)
        
        # Return solutions or a default message
        return solutions if solutions else ["Analysis in progress - solution details available in analysis section"]
    
    def _validate_solutions(self, solutions: List[str]) -> Dict[str, Any]:
        """Validate proposed solutions"""
        logger.info("✓ Validating solutions...")
        
        validation_results = []
        
        solutions_to_validate = solutions[:3] if solutions else []
        
        for i, solution in enumerate(solutions_to_validate, 1):
            prompt = f"""Validate this solution:

{solution}

Check for:
1. Logical correctness
2. Edge cases
3. Performance implications
4. Security concerns
5. Maintainability

Provide a brief validation summary."""
            
            result = self.invoke_llm(prompt)
            validation_results.append({
                "solution_number": i,
                "validation": result,
                "is_recommended": i == 1
            })
        
        # Create comprehensive best solution text
        best_solution_text = ""
        if solutions_to_validate:
            best_solution_text = solutions_to_validate[0]
            if validation_results:
                best_solution_text += f"\n\n### Validation:\n{validation_results[0].get('validation', '')}"
        
        return {
            "best_solution": best_solution_text,
            "all_solutions": solutions_to_validate,
            "validation_results": validation_results
        }
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get available tools"""
        return [
            {
                "name": "execute_code",
                "description": "Execute Python code safely",
                "function": code_executor.execute
            },
            {
                "name": "analyze_code",
                "description": "Analyze code for issues",
                "function": code_analyzer.analyze
            }
        ]
    
    def debug_code(self, code: str, error_message: str = "") -> Dict[str, Any]:
        """
        Debug code
        
        Args:
            code: Code to debug
            error_message: Error message from execution
        
        Returns:
            Debug analysis and fix
        """
        logger.info("🐛 Debugging code...")
        
        # Analyze the code
        analysis = code_analyzer.analyze(code)
        self.tool_calls_count += 1
        
        # Execute to see error
        if not error_message:
            execution = code_executor.execute(code)
            self.tool_calls_count += 1
            error_message = execution.get("error", "")
        
        # Get debugging advice
        prompt = f"""Debug this code and provide fixes:

Code:
{code}

Error: {error_message}

Analysis Results:
{str(analysis)}

Provide:
1. Root cause of the error
2. Detailed fix explanation
3. Corrected code
4. Prevention tips
5. Best practices"""
        
        debug_advice = self.invoke_llm(prompt)
        
        return {
            "original_code": code,
            "error": error_message,
            "code_analysis": analysis,
            "debug_advice": debug_advice
        }
    
    def optimize_code(self, code: str) -> Dict[str, Any]:
        """
        Optimize code
        
        Args:
            code: Code to optimize
        
        Returns:
            Optimized code and explanation
        """
        logger.info("⚡ Optimizing code...")
        
        # Analyze code
        analysis = code_analyzer.analyze(code)
        self.tool_calls_count += 1
        
        # Get optimization suggestions
        prompt = f"""Optimize this code for performance and readability:

Original Code:
{code}

Current Analysis:
{str(analysis)}

Provide:
1. Performance bottlenecks identified
2. Optimization opportunities
3. Optimized code with comments
4. Performance improvements
5. Readability enhancements"""
        
        optimization = self.invoke_llm(prompt)
        
        return {
            "original_code": code,
            "analysis": analysis,
            "optimization_suggestions": optimization
        }
    
    def code_review(self, code: str) -> Dict[str, Any]:
        """
        Perform code review
        
        Args:
            code: Code to review
        
        Returns:
            Code review feedback
        """
        logger.info("📋 Reviewing code...")
        
        # Analyze code
        analysis = code_analyzer.analyze(code)
        self.tool_calls_count += 1
        
        prompt = f"""Perform a comprehensive code review:

Code:
{code}

Analysis:
{str(analysis)}

Review for:
1. Code quality
2. Best practices
3. Security issues
4. Performance concerns
5. Readability and maintainability
6. Testing considerations

Provide specific feedback and recommendations."""
        
        review = self.invoke_llm(prompt)
        
        return {
            "code": code,
            "analysis": analysis,
            "review_feedback": review
        }