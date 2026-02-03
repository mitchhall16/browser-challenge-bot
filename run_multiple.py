#!/usr/bin/env python3
"""Run the bot multiple times and collect all results."""

import subprocess
import sys

def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print(f"Running bot {count} times...\n")

    for i in range(count):
        print(f"\n{'='*60}")
        print(f"RUN {i+1}/{count}")
        print(f"{'='*60}")
        subprocess.run([sys.executable, "agent.py"])

    print(f"\n{'='*60}")
    print(f"DONE! Completed {count} runs.")
    print(f"Open dashboard.html to see all results.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
