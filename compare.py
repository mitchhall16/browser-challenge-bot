#!/usr/bin/env python3
"""
Compare all three agents side by side.
Runs each agent once and displays comparison.
"""

import subprocess
import json
import sys
import time

AGENTS = [
    ("AUTO (pure automation)", "agent-auto.py"),
    ("HAIKU (LLM + fallback)", "agent-haiku.py"),
    ("SONNET (LLM + fallback)", "agent-sonnet.py"),
]

def run_agent(name, script):
    """Run an agent and return results"""
    print(f"\n{'='*60}")
    print(f"RUNNING: {name}")
    print(f"{'='*60}\n")

    start = time.time()
    result = subprocess.run([sys.executable, script], capture_output=False)
    duration = time.time() - start

    return {"name": name, "script": script, "exit_code": result.returncode, "wall_time": duration}

def load_results():
    """Load results.json"""
    try:
        with open("results.json") as f:
            return json.load(f)
    except:
        return []

def main():
    print("="*60)
    print("BROWSER CHALLENGE - AGENT COMPARISON")
    print("="*60)

    # Get initial count
    initial_results = load_results()
    initial_count = len(initial_results)

    # Run all agents
    for name, script in AGENTS:
        run_agent(name, script)

    # Load updated results
    results = load_results()
    new_results = results[initial_count:]

    # Print comparison
    print("\n" + "="*70)
    print("COMPARISON RESULTS")
    print("="*70)
    print(f"{'Agent':<30} {'Time':>10} {'Steps':>10} {'LLM':>8} {'Cost':>10}")
    print("-"*70)

    for r in new_results:
        agent = r.get("agent", "unknown").upper()
        name = f"{agent}"
        if r.get("model"):
            name = f"{agent} ({r['model'].split('-')[1]})"

        duration = r.get("duration_seconds", 0)
        steps = f"{r.get('steps_completed', 0)}/30"
        llm_solved = r.get("solve_breakdown", {}).get("llm_solved", 0)
        cost = r.get("token_usage", {}).get("cost_usd", 0) if r.get("token_usage") else 0

        print(f"{name:<30} {duration:>9.2f}s {steps:>10} {llm_solved:>8} ${cost:>9.4f}")

    print("-"*70)

    # LLM breakdown
    print("\nLLM vs EXPLOIT BREAKDOWN:")
    for r in new_results:
        agent = r.get("agent", "unknown").upper()
        sb = r.get("solve_breakdown", {})
        llm = sb.get("llm_solved", 0)
        exploit = sb.get("exploit_fallback", 0)
        print(f"  {agent:<12}: LLM={llm}, Exploit={exploit}")

    print(f"\nAll results saved to: results.json")
    print(f"View dashboard: open dashboard.html")

if __name__ == "__main__":
    main()
