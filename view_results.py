#!/usr/bin/env python3
"""View results summary from the command line or web dashboard."""

import json
import sys
import re

def load_results():
    try:
        with open("results.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def print_results(agent_filter=None):
    results = load_results()

    if not results:
        print("No results found. Run an agent first:")
        print("  python3 agent-auto.py    # No API key needed")
        print("  python3 agent-haiku.py   # Requires ANTHROPIC_API_KEY")
        print("  python3 agent-sonnet.py  # Requires ANTHROPIC_API_KEY")
        return

    if agent_filter:
        results = [r for r in results if r.get("agent") == agent_filter]

    print(f"\nRESULTS SUMMARY ({len(results)} runs)")
    print("=" * 80)
    print(f"{'Agent':<10} {'Time':>8} {'Steps':>8} {'LLM':>6} {'Exploit':>8} {'Cost':>10} {'Timestamp'}")
    print("-" * 80)

    for r in reversed(results[-20:]):
        agent = r.get("agent", "?").upper()
        duration = r.get("duration_seconds", 0)
        steps = r.get("steps_completed", 0)
        sb = r.get("solve_breakdown", {})
        llm = sb.get("llm_solved", 0)
        exploit = sb.get("exploit_fallback", 0)
        cost = r.get("token_usage", {}).get("cost_usd", 0) if r.get("token_usage") else 0
        ts = r.get("timestamp", "")
        status = "OK" if r.get("result") == "SUCCESS" else "FAIL"
        print(f"{agent:<10} {duration:>7.1f}s {steps:>5}/30 {llm:>6} {exploit:>8} ${cost:>9.4f} {ts} {status}")

    print("-" * 80)

    # Totals by agent
    print("\nTOTALS BY AGENT:")
    agents_data = {}
    for r in results:
        agent = r.get("agent", "unknown")
        if agent not in agents_data:
            agents_data[agent] = {"count": 0, "total_time": 0, "total_cost": 0, "success": 0}
        agents_data[agent]["count"] += 1
        agents_data[agent]["total_time"] += r.get("duration_seconds", 0)
        if r.get("token_usage"):
            agents_data[agent]["total_cost"] += r["token_usage"].get("cost_usd", 0)
        if r.get("result") == "SUCCESS":
            agents_data[agent]["success"] += 1

    for agent in ["auto", "haiku", "sonnet"]:
        if agent in agents_data:
            d = agents_data[agent]
            avg_time = d["total_time"] / d["count"] if d["count"] else 0
            success_rate = (d["success"] / d["count"] * 100) if d["count"] else 0
            print(f"  {agent.upper():<8}: {d['count']:>3} runs, avg {avg_time:>6.1f}s, ${d['total_cost']:>7.4f} total, {success_rate:>5.1f}% success")

def open_dashboard():
    """Sync results into dashboard.html and open in browser."""
    import webbrowser
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_path = os.path.join(script_dir, "results.json")
    dashboard_path = os.path.join(script_dir, "dashboard.html")

    if not os.path.exists(dashboard_path):
        print("dashboard.html not found")
        return

    # Load results and embed into dashboard
    runs = load_results()
    if runs:
        with open(dashboard_path, "r") as f:
            html = f.read()
        embedded_script = f'<script id="embedded-data">const EMBEDDED_RESULTS = {json.dumps(runs)};</script>'
        html = re.sub(
            r'<!-- EMBEDDED_DATA_START -->.*?<!-- EMBEDDED_DATA_END -->',
            f'<!-- EMBEDDED_DATA_START -->\n    {embedded_script}\n    <!-- EMBEDDED_DATA_END -->',
            html,
            flags=re.DOTALL
        )
        with open(dashboard_path, "w") as f:
            f.write(html)
        print(f"Synced {len(runs)} runs to dashboard")

    webbrowser.open(f"file://{dashboard_path}")
    print(f"Opened: file://{dashboard_path}")

def main():
    args = sys.argv[1:]

    if "-h" in args or "--help" in args:
        print("Usage: python3 view_results.py [options]")
        print("\nOptions:")
        print("  --web         Open dashboard.html in browser")
        print("  auto/haiku/sonnet   Filter by agent type")
        print("\nExamples:")
        print("  python3 view_results.py         # CLI summary")
        print("  python3 view_results.py --web   # Open dashboard")
        print("  python3 view_results.py haiku   # Filter by agent")
        return

    if "--web" in args:
        open_dashboard()
    else:
        agent_filter = None
        for arg in args:
            if arg in ("auto", "haiku", "sonnet"):
                agent_filter = arg
        print_results(agent_filter)

if __name__ == "__main__":
    main()
