# Browser Navigation Challenge Bot

Solves all 30 levels in ~30 seconds. No AI calls - $0 cost per run.

## Setup

```bash
git clone https://github.com/mitchhall16/browser-challenge-bot.git
cd browser-challenge-bot
pip install playwright
playwright install chromium
```

## Run the Bot

```bash
# Single run
python agent.py

# Multiple runs (e.g., 10 times)
python run_multiple.py 10
```

## View Dashboard

```bash
python start_dashboard.py
```

This opens the dashboard in your browser. All runs are saved to `runs.json` and displayed automatically.

- Chart shows run times with timestamps
- Filter by version (v1, v2, v3)
- Click any run to see step-by-step breakdown

## Files

| File | What it does |
|------|--------------|
| `agent.py` | The bot - completes all 30 levels |
| `run_multiple.py` | Run the bot N times |
| `start_dashboard.py` | Open the dashboard |
| `dashboard.html` | Results visualization |
| `runs.json` | Your run history (auto-created) |
