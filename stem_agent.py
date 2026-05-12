from registry import ToolRegistry
from architect import Architect, AgentPlan
from executor import Executor, ExecutorOutput
from evaluator import Evaluator, EvaluationResult
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

class AgentState(BaseModel):
    task_description: str
    attempts: list[dict] = []
    final_output: ExecutorOutput | None = None
    final_evaluation: EvaluationResult | None = None
    total_cost: float = 0.0

class StemAgent:
    def __init__(self, max_attempts: int = 3):
        self.registry = ToolRegistry()
        self.architect = Architect(self.registry)
        self.executor = Executor(self.registry)
        self.evaluator = Evaluator(threshold=8.0)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.max_attempts = max_attempts

    def research_domain(self, task_class: str) -> str:
        print(f"Researching domain: {task_class}")
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"""You are an expert software engineer.
            Explain how '{task_class}' tasks are typically approached.
            What techniques, tools, and workflows are commonly used?
            Be concise and practical.
            Respond in 3-5 sentences."""}],
            temperature=0.3
        )
        research = response.choices[0].message.content
        print(f"Research: {research}\n")
        return research

    def _build_retry_prompt(self, state: AgentState) -> str:
        last_attempt = state.attempts[-1]
        return f"""Previous analysis attempt failed to meet quality threshold.

        Original task: {state.task_description}
        Previous tools used: {last_attempt['tools_used']}
        Previous score: {last_attempt['score']}
        Evaluator feedback: {last_attempt['reasoning']}
        Suggestions: {last_attempt['suggestions']}

        Based on this feedback, create an improved execution plan.
        Use different tools or a different approach than before.

        Available tools:
        {json.dumps(self.registry.get_all_metadata(), indent=2)}

        Respond ONLY with JSON, no markdown:
        {{
            "task_type": "what kind of task this is",
            "selected_tools": ["tool_name1", "tool_name2"],
            "workflow_pattern": "sequential or parallel or iterative",
            "reasoning": "why you chose these tools this time",
            "estimated_total_cost": 0.0,
            "confidence_score": 0.0
        }}"""

    def run(self, task_class: str, code: str) -> AgentState:
        state = AgentState(task_description=task_class)

        # FAZA 1: Research
        research = self.research_domain(task_class)
        enriched_task = f"{task_class}\n\nContext: {research}"

        attempt_num = 0

        while attempt_num < self.max_attempts:
            attempt_num += 1
            print(f" Attempt {attempt_num}/{self.max_attempts}")

            # FAZA 2: Architect pravi plan
            if attempt_num == 1:
                plan = self.architect.create_plan(enriched_task)
            else:
                print(" Re-differentiating based on feedback...")
                prompt = self._build_retry_prompt(state)
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                plan_data = json.loads(response.choices[0].message.content)
                plan = AgentPlan(**plan_data)

            print(f"  Plan: {plan.selected_tools} | {plan.workflow_pattern}")

            # FAZA 3: Executor izvrsava
            output = self.executor.run(plan, code)
            state.total_cost += output.total_cost

            # FAZA 4: Evaluator ocenjuje
            evaluation = self.evaluator.evaluate(output)
            print(f"📊 Score: {evaluation.score}/10 | Needs retry: {evaluation.needs_retry}")

            # Belezimo pokusaj
            state.attempts.append({
                "attempt": attempt_num,
                "tools_used": plan.selected_tools,
                "score": evaluation.score,
                "reasoning": evaluation.reasoning,
                "suggestions": evaluation.suggestions,
                "total_findings": output.total_findings
            })

            state.final_output = output
            state.final_evaluation = evaluation

            # FAZA 5: Da li je dovoljno dobro?
            if not evaluation.needs_retry:
                print(f"Agent satisfied with results after {attempt_num} attempt(s)")
                break
            else:
                print(f"Score below threshold, re-differentiating...\n")

        return state