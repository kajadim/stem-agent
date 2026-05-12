from capabilities import ToolMetadata, BaseTool, PermissionLevel

import subprocess
import tempfile
import json
import os

class TestRunnerTool(BaseTool):
    metadata: ToolMetadata = ToolMetadata(
        name= "test_runner",
        description="Executes the provided Python code and runs its unit tests to verify functional correctness. Returns test results, pass/fail status, and traceback information if a failure occurs.",
        cost_estimate=5.0,
        required_permissions=[PermissionLevel.EXECUTE],
        suitable_for=["functional_verification", "unit_testing", "regression_testing", "code_execution"]
    )

    def validate_input(self, **kwargs) -> bool:
        return "code" in kwargs and isinstance(kwargs["code"], str)
    
    def execute(self, **kwargs) -> dict:
        if not self.validate_input(**kwargs):
            return {"success": False, "error": "Invalid input"}

        code = kwargs["code"]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            tmp_path = f.name

        try:
            result = subprocess.run(
                ["pytest", tmp_path, "--tb=short", "-q"],
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout + result.stderr
            passed = output.count(" passed")
            failed = output.count(" failed")
            findings = []

            if failed > 0:
                findings.append({
                    "line": 0,
                    "message": f"{failed} test(s) failed: {output[:300]}",
                    "severity": "error"
                })
            if passed > 0:
                findings.append({
                    "line": 0,
                    "message": f"{passed} test(s) passed",
                    "severity": "info"
                })

        except Exception as e:
            findings = [{"line": 0, "message": str(e), "severity": "error"}]
        finally:
            os.unlink(tmp_path)

        return {
            "success": True,
            "tool": self.metadata.name,
            "findings": findings,
            "cost_used": self.metadata.cost_estimate
        }