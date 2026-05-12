from stem_agent import StemAgent

def run_benchmark():
    with open("tests/sample_code/bad_code.py", "r") as f:
        bad_code = f.read()
    
    with open("tests/sample_code/benchmark_cases.py", "r") as f:
        benchmark_code = f.read()

    with open("tests/sample_code/good_code.py", "r") as f:
        good_code = f.read()

    test_cases = [
        ("Good code", good_code),
        ("Bad code", bad_code),
        ("Benchmark cases", benchmark_code),
    ]

    print("=" * 60)
    print("BENCHMARK RESULTS")
    print("=" * 60)

    for name, code in test_cases:
        print(f"\n>>> Testing: {name}")
        agent = StemAgent(max_attempts=2)
        state = agent.run("Code Quality Assurance", code)
        
        errors = sum(
            1 for r in state.final_output.results
            for f in r.findings
            if f["severity"] == "error"
        )
        warnings = sum(
            1 for r in state.final_output.results
            for f in r.findings
            if f["severity"] == "warning"
        )

        print(f"  Attempts: {len(state.attempts)}")
        print(f"  Total findings: {state.final_output.total_findings}")
        print(f"  Errors: {errors} | Warnings: {warnings}")
        print(f"  Final score: {state.final_evaluation.score}/10")
        print(f"  Total cost: {state.total_cost}")

if __name__ == "__main__":
    run_benchmark()