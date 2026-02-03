#!/usr/bin/env python3
"""Run an agent multiple times and collect all results."""

import subprocess
import sys

AGENTS = {
    "auto": "agent-auto.py",
    "haiku": "agent-haiku.py",
    "sonnet": "agent-sonnet.py"
}

def main():
    # Parse arguments
    agent = "auto"
    count = 5

    args = sys.argv[1:]
    for arg in args:
        if arg in AGENTS:
            agent = arg
        elif arg.isdigit():
            count = int(arg)

    script = AGENTS[agent]
    print(f"Running {agent} agent ({script}) {count} times...\n")

    for i in range(count):
        print(f"\n{'='*60}")
        print(f"RUN {i+1}/{count} - {agent.upper()}")
        print(f"{'='*60}")
        subprocess.run([sys.executable, script])

    print(f"\n{'='*60}")
    print(f"DONE! Completed {count} runs with {agent} agent.")
    print(f"Results saved to results.json")
    print(f"Open dashboard.html to see all results.")
    print(f"{'='*60}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print("Usage: python3 run_multiple.py [agent] [count]")
        print("  agent: auto, haiku, or sonnet (default: auto)")
        print("  count: number of runs (default: 5)")
        print("\nExamples:")
        print("  python3 run_multiple.py          # 5 auto runs")
        print("  python3 run_multiple.py haiku 3  # 3 haiku runs")
        print("  python3 run_multiple.py 10       # 10 auto runs")
    else:
        main()
