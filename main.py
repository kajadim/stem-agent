from stem_agent import StemAgent

with open("tests/sample_code/bad_code.py", "r") as f:
    test_code = f.read()

agent = StemAgent(max_attempts=3)
state = agent.run("Code Quality Assurance", test_code)

print("\n" + "="*50)
print("FINAL REPORT")
print("="*50)
print(f"Total attempts: {len(state.attempts)}")
print(f"Total cost: {state.total_cost}")
print(f"Final score: {state.final_evaluation.score}/10")

print("\nAttempt history:")
for attempt in state.attempts:
    print(f"  Attempt {attempt['attempt']}: score={attempt['score']} | tools={attempt['tools_used']} | findings={attempt['total_findings']}")

print("\nFinal findings:")
for result in state.final_output.results:
    print(f"\n--- {result.tool_name.upper()} ---")
    for finding in result.findings:
        print(f"  Line {finding['line']}: [{finding['severity']}] {finding['message']}")