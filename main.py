from registry import ToolRegistry
from architect import Architect

registry = ToolRegistry()

print("=== ALL TOOLS ===")
for tool in registry.get_all_metadata():
    print(f"\n{tool['name']}")
    print(f"  Description: {tool['description'][:50]}...")
    print(f"  Cost: {tool['cost_estimate']}")
    print(f"  Permissions: {tool['required_permissions']}")

print("\n=== TOOLS FOR 'bug_detection' ===")
for tool in registry.get_tools_for_task("bug_detection"):
    print(f"  - {tool.metadata.name}")


architect = Architect(registry)
plan = architect.create_plan("I need to check this Python code for bugs and style issues")

print("\n=== ARCHITECT PLAN ===")
print(f"Task type: {plan.task_type}")
print(f"Selected tools: {plan.selected_tools}")
print(f"Workflow: {plan.workflow_pattern}")
print(f"Reasoning: {plan.reasoning}")
print(f"Estimated cost: {plan.estimated_total_cost}")
print(f"Confidence: {plan.confidence_score}")