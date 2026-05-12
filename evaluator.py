from executor import ExecutorOutput
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

class EvaluationResult(BaseModel):
    score: float  # 1.0 - 10.0
    reasoning: str
    needs_retry: bool
    suggestions: list[str]  

class Evaluator:
    def __init__(self, threshold: float = 7.0):
        self.threshold = threshold
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def evaluate(self, output: ExecutorOutput) -> EvaluationResult:
        prompt = self._build_prompt(output)
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        
        raw = response.choices[0].message.content
        data = json.loads(raw)
        result = EvaluationResult(**data)
        result.needs_retry = result.score < self.threshold
        return result
    
    def _build_prompt(self, output: ExecutorOutput) -> str:
        findings_summary = []
        for result in output.results:
            findings_summary.append({
                "tool": result.tool_name,
                "success": result.success,
                "findings_count": len(result.findings),
                "errors": [f for f in result.findings if f["severity"] == "error"],
                "warnings": [f for f in result.findings if f["severity"] == "warning"]
            })

        return f"""You are a Code Quality Evaluator. Analyze these results and score the analysis quality.
                Task: {output.plan.task_type}
                Tools used: {output.plan.selected_tools}
                Total findings: {output.total_findings}
                Failed tools: {output.failed_tools}

                Results per tool:
                {json.dumps(findings_summary, indent=2)}

                Score the quality of this analysis from 1-10 where:
                - 10: Perfect, comprehensive analysis with clear actionable findings
                - 7: Good analysis, covers main issues
                - 4: Partial analysis, missing important issues  
                - 1: Failed or useless analysis

                Respond ONLY with JSON, no markdown:
                {{
                    "score": 8.5,
                    "reasoning": "why you gave this score",
                    "needs_retry": false,
                    "suggestions": ["what could be improved"]
                }}"""