from capabilities import BaseTool, ToolMetadata, PermissionLevel

class LinterTool(BaseTool):
    metadata: ToolMetadata = ToolMetadata(
        name="linter",
        description="Analyzes Python code to find stylistic errors and potential issues using pylint.",
        cost_estimate=2.0,
        required_permissions=[PermissionLevel.READ_ONLY],
        suitable_for=["code_quality", "style_check", "basic_analysis"]
    )
    
    def validate_input(self, **kwargs) -> bool:
        return "code" in kwargs and isinstance(kwargs["code"], str)
    
    def execute(self, **kwargs) -> dict:
        if not self.validate_input(**kwargs):
            return {
                "success": False, 
                "error": "Invalid input: 'code' argument must be a string."}
        
        code = kwargs["code"]
        
        return {
            "success": True,
            "tool": self.metadata.name,
            "findings": [
                {
                    "line": 1, 
                    "message": "Mock: missing docstring", 
                    "severity": "warning"
                }
            ],
            "cost_used": self.metadata.cost_estimate
        }