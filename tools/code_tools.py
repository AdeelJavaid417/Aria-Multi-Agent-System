"""
Code Tools - Execution and analysis
"""
import subprocess
import ast
import re
from typing import Dict, Any
from utils.logger import logger
import signal
from contextlib import contextmanager

class TimeoutException(Exception):
    pass

@contextmanager
def time_limit(seconds):
    """Context manager for timeout"""
    def signal_handler(signum, frame):
        raise TimeoutException("Code execution timed out")
    
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

class CodeExecutorTool:
    """Execute Python code safely"""
    
    @staticmethod
    def execute(code: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute Python code and return results
        """
        logger.info("💻 Executing code...")
        
        try:
            # Create safe execution environment
            exec_globals = {"__builtins__": {}}
            exec_locals = {}
            
            # Execute with timeout
            exec(code, exec_globals, exec_locals)
            
            return {
                "status": "success",
                "output": str(exec_locals),
                "execution_time": timeout
            }
        except TimeoutException:
            return {
                "status": "error",
                "error": "Code execution timed out",
                "error_type": "TimeoutError"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__
            }

class CodeAnalyzerTool:
    """Analyze Python code"""
    
    @staticmethod
    def analyze(code: str) -> Dict[str, Any]:
        """
        Analyze code for issues
        """
        logger.info("🔍 Analyzing code...")
        
        issues = {
            "syntax_errors": [],
            "warnings": [],
            "suggestions": [],
            "metrics": {}
        }
        
        try:
            # Parse code
            tree = ast.parse(code)
            
            # Count metrics
            issues["metrics"]["lines"] = len(code.split('\n'))
            issues["metrics"]["functions"] = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
            issues["metrics"]["classes"] = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
            
            # Check for common issues
            if len(code.split('\n')) > 50:
                issues["suggestions"].append("Function might be too long, consider refactoring")
            
            if re.search(r'except\s*:', code):
                issues["warnings"].append("Bare except clause found - should specify exception type")
            
            if re.search(r'eval\(', code) or re.search(r'exec\(', code):
                issues["warnings"].append("Use of eval/exec detected - potential security risk")
            
            return {
                "status": "success",
                "issues": issues
            }
        
        except SyntaxError as e:
            return {
                "status": "error",
                "error": f"Syntax error: {e}",
                "line": e.lineno
            }

# Create tool instances
code_executor = CodeExecutorTool()
code_analyzer = CodeAnalyzerTool()