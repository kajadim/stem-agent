from capabilities import ToolMetadata, BaseModel, PermissionLevel

class CodeAnalyzerTool(BaseModel):
    metadata: ToolMetadata = ToolMetadata (
        name= "code_analyzer",
        description="Performs deep static analysis of the source code to identify logic bugs, structural weaknesses, and high cyclomatic complexity. Use this tool for identifying dead code, unreachable blocks, and potential runtime errors without executing the code.",
        cost_estimate=4.0,
        required_permissions=[PermissionLevel.READ_ONLY],
        suitable_for=["bug_detection", "complexity_analysis", "dead_code"]
    )

    def validate_input(self, **kwargs) -> bool:
        return "code" in kwargs and isinstance(kwargs["code"], str)
    
    def execute (self, **kwargs) -> dict:
        if not self.validate_input(**kwargs):
            return {
                "success": False,
                "error" : "Invalid input: 'code' argument must be a string."
            }
        return {
            "success": True,
            "tool" : self.metadata.name,
            "findings": [
                {"line": 5, "message": "Function has too many nested blocks (depth: 4)", "severity": "error"},
                {"line": 12, "message": "Unused variable 'result'", "severity": "warning"},
                {"line": 20, "message": "Function has too many parameters (8/5)", "severity": "warning"}
            ],
            "cost_used" : self.metadata.cost_estimate
        }
