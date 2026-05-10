from capabilities.linter import LinterTool
from capabilities.code_analyzer import CodeAnalyzerTool
from capabilities.test_runner import TestRunnerTool
from capabilities import BaseTool

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}
        self._register_defaults()
    
    def _register_defaults(self):
        default_tools = [
            LinterTool(),
            CodeAnalyzerTool(),
            TestRunnerTool()
        ]
        for tool in default_tools:
            self._tools[tool.metadata.name] = tool
    
    def get_tool(self, name: str) -> BaseTool | None:
        return self._tools.get(name)
    
    def get_all_metadata(self) -> list[dict]:
        return [
            {
                "name": tool.metadata.name,
                "description": tool.metadata.description,
                "cost_estimate": tool.metadata.cost_estimate,
                "required_permissions": [p.value for p in tool.metadata.required_permissions],
                "suitable_for": tool.metadata.suitable_for
            }
            for tool in self._tools.values()
        ]
    
    def get_tools_for_task(self, task_type: str) -> list[BaseTool]:
        return [
            tool for tool in self._tools.values()
            if task_type in tool.metadata.suitable_for
        ]