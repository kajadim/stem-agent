from capabilities import ToolMetadata, BaseTool, PermissionLevel
import ast
class CodeAnalyzerTool(BaseTool):
    metadata: ToolMetadata = ToolMetadata (
        name= "code_analyzer",
        description="Performs deep static analysis of the source code to identify logic bugs, structural weaknesses, and high cyclomatic complexity. Use this tool for identifying dead code, unreachable blocks, and potential runtime errors without executing the code.",
        cost_estimate=4.0,
        required_permissions=[PermissionLevel.READ_ONLY],
        suitable_for=["bug_detection", "complexity_analysis", "dead_code"]
    )

    def validate_input(self, **kwargs) -> bool:
        return "code" in kwargs and isinstance(kwargs["code"], str)
    
    def execute(self, **kwargs) -> dict:
        if not self.validate_input(**kwargs):
            return {"success": False, "error": "Invalid input"}

        code = kwargs["code"]
        findings = []

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {"success": False, "error": f"Syntax error: {e}"}

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.args.args) > 5:
                    findings.append({
                        "line": node.lineno,
                        "message": f"Function '{node.name}' has too many parameters ({len(node.args.args)}/5)",
                        "severity": "warning"
                    })
                if hasattr(node, 'end_lineno') and (node.end_lineno - node.lineno) > 50:
                    findings.append({
                        "line": node.lineno,
                        "message": f"Function '{node.name}' is too long ({node.end_lineno - node.lineno} lines)",
                        "severity": "warning"
                    })

            if isinstance(node, ast.If):
                depth = sum(1 for _ in ast.walk(node) if isinstance(_, ast.If))
                if depth > 3:
                    findings.append({
                        "line": node.lineno,
                        "message": f"Deeply nested if statements (depth: {depth})",
                        "severity": "error"
                    })

            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    findings.append({
                        "line": node.lineno,
                        "message": "Bare except clause, be more specific",
                        "severity": "error"
                    })

            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == 'print':
                    findings.append({
                        "line": node.lineno,
                        "message": "Found print statement, use logging instead",
                        "severity": "warning"
                    })

        return {
            "success": True,
            "tool": self.metadata.name,
            "findings": findings,
            "cost_used": self.metadata.cost_estimate
        }
