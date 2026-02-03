# Browser Navigation Challenge Bot

Three agents that solve all 30 levels of the browser challenge.

![Dashboard Screenshot](dashboard-screenshot.png)

| Agent | How it works | Cost |
|-------|--------------|------|
| **Automation** | No AI - decrypts session codes directly | $0 |
| **Haiku** | Claude Haiku vision + fallback | ~$0.04/run |
| **Sonnet** | Claude Sonnet vision + fallback | ~$0.15/run |

## Setup

```bash
git clone https://github.com/mitchhall16/browser-challenge-bot.git
cd browser-challenge-bot
pip install -r requirements.txt
playwright install chromium
```

**For Haiku/Sonnet:** Add your Anthropic API key:

```bash
cp .env.example .env
# Edit .env and add your key
```

## Run

```bash
# No AI (free)
python3 agent-auto.py

# With AI (requires API key)
python3 agent-haiku.py
python3 agent-sonnet.py
```

**Benchmark one agent:**
```bash
python3 run_multiple.py auto 5     # Run automation 5 times
python3 run_multiple.py haiku 3    # Run haiku 3 times
```

**Compare all agents:**
```bash
python3 compare.py                 # Runs all 3 once, shows comparison
```

## View Results

```bash
python3 view_results.py            # CLI summary
open dashboard.html                # Visual dashboard
```

## What This Proves

When a task has a clear beginning and end, you don't always need AI. This challenge has 30 defined steps with predictable logic — perfect for automation. Reverse engineering took a few hours but produced a solution that runs in ~29 seconds, forever, for free.

That said, AI shines when you give it a strong foundation to work from. Haiku and Sonnet both performed way better with the cheat sheet baked in than they would have going in blind. The takeaway isn't that AI is useless — it's that building a solid understanding of the problem first makes everything better, whether you're automating or prompting.

My thought process was: dissect the problem first, automate what you can, then bring in AI with guardrails and a failsafe. Solutions-based, scalable, and always looking for the most efficient path.

## Findings

**Step 30 is unsolvable by design.** validateCode(30) checks for a 31st code that doesn't exist in the session (only 1-30). Nobody's beating that level legitimately. The bot patches sessionStorage to add a 31st entry so the app's own React Router navigates to /finish naturally.

**The blocking modals have predictable answers.** Every modal's correct radio button follows a simple formula based on the step number. No AI needed to figure that out.

**All three versions (v1, v2, v3) are identical.** Same encryption, same logic, same everything. One bot handles all of them.

## About Me

Based in Livermore, CA. Started using Claude on January 3rd of this year and haven't stopped building since — I won't go to sleep until the project's done.

Some recent projects: bought a $30 drone off Amazon and got it streaming video and controlled entirely from my computer. Doesn't fly very well but the fact that I can do that is still insanely cool. This challenge was the same kind of fun — couldn't put it down until it was cracked.

[LinkedIn](https://www.linkedin.com/in/mitchellphall)
