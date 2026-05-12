from registry import ToolRegistry
from pydantic import BaseModel
from dotenv import load_dotenv
import json
import os
from openai import OpenAI

load_dotenv()

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
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
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

    def _llm_call(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    
    def create_plan(self, task_description: str) -> AgentPlan:
        prompt = self._build_prompt(task_description)
        response = self._llm_call(prompt)
        
        try:
            plan_data = json.loads(response)
            return AgentPlan(**plan_data)
        except Exception as e:
            raise ValueError(f"Architect failed to create valid plan: {e}")