# Browser Navigation Challenge Bot

Solves all 30 levels in ~30 seconds. No AI calls - $0 cost.

## Setup

```bash
pip install playwright
playwright install chromium
```

## Run

```bash
# Single run
python agent.py

# Multiple runs (e.g., 10 times)
python run_multiple.py 10
```

## View Results

Open `dashboard.html` in your browser. All runs are saved to `runs.json` and the dashboard auto-loads them.

Just refresh the dashboard to see new runs.

## Files

- `agent.py` - The bot
- `run_multiple.py` - Run bot N times
- `dashboard.html` - Results dashboard
- `runs.json` - All your runs (auto-created)
