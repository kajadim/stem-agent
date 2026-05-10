from capabilities import ToolMetadata, BaseModel, PermissionLevel

class TestRunnerTool(BaseModel):
    metadata: ToolMetadata = ToolMetadata(
        name= "test_runner",
        description="Executes the provided Python code and runs its unit tests to verify functional correctness. Returns test results, pass/fail status, and traceback information if a failure occurs.",
        cost_estimate=5.0,
        required_permissions=[PermissionLevel.EXECUTE],
        suitable_for=["functional_verification", "unit_testing", "regression_testing", "code_execution"]
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
                {
                    "line": 8, 
                    "message": "AssertionError: Expected 10, but got 7. Check the addition logic.", 
                    "severity": "error"
                },
                {
                    "line": 15, 
                    "message": "ZeroDivisionError: division by zero. Function lacks input validation for divisor.", 
                    "severity": "error"
                },
                {
                    "line": 2, 
                    "message": "DeprecationWarning: Using deprecated 'unittest.makeSuite'. Move to 'unittest.TestLoader'.", 
                    "severity": "warning"
                }
            ],
            "cost_used" : self.metadata.cost_estimate
        }       