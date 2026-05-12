from capabilities import BaseTool, ToolMetadata, PermissionLevel

import subprocess
import tempfile
import json
import os

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
            return {"success": False, "error": "Invalid input"}

        code = kwargs["code"]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            tmp_path = f.name

        try:
            result = subprocess.run(
                ["pylint", tmp_path, "--output-format=json"],
                capture_output=True,
                text=True,
                timeout=30
            )

            raw = json.loads(result.stdout) if result.stdout else []
            findings = [
                {
                    "line": item["line"],
                    "message": item["message"],
                    "severity": "error" if item["type"] in ["error", "fatal"] else "warning"
                }
                for item in raw
            ]
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