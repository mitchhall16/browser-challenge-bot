# Browser Navigation Challenge Bot

Automated bot that solves all 30 levels of the browser navigation challenge in ~30 seconds.

**No AI/LLM calls at runtime - pure browser automation. $0 cost per run.**

## Quick Start

```bash
# Install dependencies
pip install playwright
playwright install chromium

# Run the bot
python agent.py

# View your runs
# Open dashboard.html in your browser
```

## How It Works

The challenge site stores all 30 codes in sessionStorage with weak XOR encryption. The bot:

1. Navigates to the site and clicks START
2. Decrypts all 30 codes from sessionStorage using the known key
3. Injects each code directly into React via JavaScript (bypasses all overlays/modals)
4. Completes all 30 steps in ~30 seconds

## Files

| File | Description |
|------|-------------|
| `agent.py` | The bot - run this |
| `dashboard.html` | Run history visualization - open in browser |
| `run-results.json` | Output from each run (auto-generated) |

## Dashboard

After running the bot:

1. Open `dashboard.html` in your browser
2. Click **"Load Latest Run"** button to import your run
3. Your runs are saved in browser localStorage, so they persist

**Dashboard features:**
- Total runs, success rate, avg time, best time
- Chart showing run times over time
- Filter by version (v1, v2, v3)
- Expandable details showing per-step timing

## Expected Output

```
============================================================
BROWSER NAVIGATION CHALLENGE - SESSION HACK BOT v2
============================================================
[2.7s] Navigating to home page...
[4.7s] Clicking START...
[6.8s] Version: 3
[6.8s] Decrypting session...
[6.9s] Got 30 codes

[6.9s] Step 1/30 -> 6C2KVM -> OK (0.77s)
[7.6s] Step 2/30 -> 2W9AYZ -> OK (0.76s)
...
[29.0s] Step 30/30 -> /finish

============================================================
SUCCESS! Reached /finish in 30.04s
============================================================
```

## Troubleshooting

**"No session found in sessionStorage"**
- Make sure you let the START button click complete before the session is read

**Browser doesn't open**
- Run `playwright install chromium` to install the browser

**Steps failing after step 14**
- This shouldn't happen with the current code, but if it does, the bot targets the correct input in the yellow submission box
