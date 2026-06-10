"""
Base Tool Definitions
"""
from typing import Any, Callable, Dict, Optional
from pydantic import BaseModel, Field

class ToolDefinition(BaseModel):
    """Definition of a tool"""
    name: str
    description: str
    func: Callable
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True

class ToolRegistry:
    """Registry for managing tools"""
    
    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
    
    def register_tool(self, definition: ToolDefinition) -> None:
        """Register a tool"""
        self.tools[definition.name] = definition
    
    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """Get tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> list[str]:
        """List all available tools"""
        return list(self.tools.keys())
    
    def execute_tool(self, name: str, **kwargs) -> Any:
        """Execute a tool"""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool {name} not found")
        return tool.func(**kwargs)

# Global tool registry
tool_registry = ToolRegistry()

# Tool Definitions
class WebSearchInput(BaseModel):
    query: str
    max_results: int = Field(default=10, description="Maximum results to return")

class CalculateInput(BaseModel):
    expression: str = Field(description="Mathematical expression to evaluate")

class ExecuteCodeInput(BaseModel):
    code: str = Field(description="Python code to execute")
    timeout: int = Field(default=30, description="Execution timeout in seconds")

class FetchDataInput(BaseModel):
    url: str = Field(description="API endpoint URL")
    params: Dict[str, Any] = Field(default_factory=dict, description="Query parameters")

class SendNotificationInput(BaseModel):
    title: str = Field(description="Notification title")
    message: str = Field(description="Notification message")
    notify_type: str = Field(default="info", description="Type: info, warning, error")