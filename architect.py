from registry import ToolRegistry
from pydantic import BaseModel
import json

class AgentPlan(BaseModel):
    task_type: str
    selected_tools: list[str]
    workflow_pattern: str  # "sequential", "parallel", "iterative"
    reasoning: str
    estimated_total_cost: float
    confidence_score: float  # 0.0 - 1.0

class Architect:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry
    
    def _build_prompt(self, task_description: str) -> str:
        available_tools = self.registry.get_all_metadata()
        
        return f"""You are an AI Architect. Your job is to analyze a task and create an execution plan.

                Available tools:
                {json.dumps(available_tools, indent=2)}

                Task: {task_description}

                Respond ONLY with a JSON object in this exact format:
                {{
                    "task_type": "what kind of task this is",
                    "selected_tools": ["tool_name1", "tool_name2"],
                    "workflow_pattern": "sequential or parallel or iterative",
                    "reasoning": "why you chose these tools",
                    "estimated_total_cost": 0.0,
                    "confidence_score": 0.0
                }}"""

    def _mock_llm_call(self, prompt: str) -> str:
        return json.dumps({
            "task_type": "code_quality",
            "selected_tools": ["linter", "code_analyzer"],
            "workflow_pattern": "sequential",
            "reasoning": "For code quality analysis, we first lint for style issues, then do deep analysis for bugs.",
            "estimated_total_cost": 6.0,
            "confidence_score": 0.85
        })
    
    def create_plan(self, task_description: str) -> AgentPlan:
        prompt = self._build_prompt(task_description)
        response = self._mock_llm_call(prompt)
        
        try:
            plan_data = json.loads(response)
            return AgentPlan(**plan_data)
        except Exception as e:
            raise ValueError(f"Architect failed to create valid plan: {e}")