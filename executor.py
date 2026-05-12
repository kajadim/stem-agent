from registry import ToolRegistry
from architect import AgentPlan
from pydantic import BaseModel

class ExecutionResult(BaseModel):
    tool_name: str
    success: bool
    findings: list[dict]
    error: str | None = None
    cost_used: float

class ExecutorOutput(BaseModel):
    plan: AgentPlan
    results: list[ExecutionResult]
    total_cost: float
    total_findings: int
    failed_tools: list[str]

class Executor:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry
    
    def run(self, plan: AgentPlan, code: str) -> ExecutorOutput:
        results = []
        failed_tools = []

        for tool_name in plan.selected_tools:
            print(f"  Running {tool_name}...")
            
            tool = self.registry.get_tool(tool_name)
            
            if tool is None:
                failed_tools.append(tool_name)
                results.append(ExecutionResult(
                    tool_name=tool_name,
                    success=False,
                    findings=[],
                    error=f"Tool '{tool_name}' not found in registry",
                    cost_used=0.0
                ))
                continue

            try:
                raw = tool.execute(code=code)
                results.append(ExecutionResult(
                    tool_name=tool_name,
                    success=raw["success"],
                    findings=raw.get("findings", []),
                    error=raw.get("error"),
                    cost_used=raw.get("cost_used", 0.0)
                ))
            except Exception as e:
                failed_tools.append(tool_name)
                results.append(ExecutionResult(
                    tool_name=tool_name,
                    success=False,
                    findings=[],
                    error=f"Unexpected error: {str(e)}",
                    cost_used=0.0
                ))

        total_cost = sum(r.cost_used for r in results)
        total_findings = sum(len(r.findings) for r in results)

        return ExecutorOutput(
            plan=plan,
            results=results,
            total_cost=total_cost,
            total_findings=total_findings,
            failed_tools=failed_tools
        )