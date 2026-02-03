# Browser Navigation Challenge Bot

Three agents that solve all 30 levels of the browser challenge:

| Agent | How it works | Cost |
|-------|--------------|------|
| **Auto** | Pure automation - decrypts session codes | $0 |
| **Haiku** | Claude Haiku + exploit fallback | ~$0.04/run |
| **Sonnet** | Claude Sonnet + exploit fallback | ~$0.15/run |

## Setup

```bash
git clone https://github.com/mitchhall16/figure-agent.git
cd figure-agent
pip install -r requirements.txt
playwright install chromium
```

**For LLM agents (Haiku/Sonnet):** Copy the example env file and add your API key:

```bash
cp .env.example .env
# Edit .env and replace "your-key-here" with your Anthropic API key
```

## Run

```bash
# Auto agent (no API key needed)
python3 agent-auto.py

# Haiku agent (requires API key)
python3 agent-haiku.py

# Sonnet agent (requires API key)
python3 agent-sonnet.py

# Run multiple times
python3 run_multiple.py auto 5      # 5 auto runs
python3 run_multiple.py haiku 3     # 3 haiku runs

# Compare all three agents
python3 compare.py
```

## View Results

```bash
# Command line summary
python3 view_results.py

# Web dashboard (just open the file - no server needed!)
open dashboard.html
```

## Files

| File | Description |
|------|-------------|
| `agent-auto.py` | Pure automation agent ($0) |
| `agent-haiku.py` | Haiku LLM agent |
| `agent-sonnet.py` | Sonnet LLM agent |
| `run_multiple.py` | Run any agent N times |
| `compare.py` | Run all 3 agents and compare |
| `view_results.py` | CLI results summary |
| `dashboard.html` | Web dashboard |
| `results.json` | All run history (auto-created) |
