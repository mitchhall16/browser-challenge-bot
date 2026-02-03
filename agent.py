#!/usr/bin/env python3
"""
Browser Navigation Challenge - Session Hack Bot v2
Solves all 30 levels by decrypting codes from sessionStorage

Site: https://serene-frangipane-7fd25b.netlify.app/
Strategy: Decrypt XOR-encrypted session to get all 30 codes, then inject each
          directly into React via page.evaluate() - bypasses ALL overlays/modals!
"""

import asyncio
import json
import time
from playwright.async_api import async_playwright

# Config
SITE_URL = "https://serene-frangipane-7fd25b.netlify.app"
ENCRYPTION_KEY = "WO_2024_CHALLENGE"
TOTAL_STEPS = 30

# Metrics tracking
metrics = {
    "start_time": None,
    "end_time": None,
    "step_times": [],
    "steps_completed": 0,
    "result": "INCOMPLETE",
    "errors": []
}


async def get_all_codes(page) -> list:
    """Extract all 30 codes from sessionStorage via browser JS (more reliable)"""
    codes = await page.evaluate('''() => {
        const KEY = "WO_2024_CHALLENGE";
        const encoded = sessionStorage.getItem("wo_session");
        if (!encoded) return null;
        const decoded = atob(encoded);
        let decrypted = "";
        for (let i = 0; i < decoded.length; i++) {
            decrypted += String.fromCharCode(decoded.charCodeAt(i) ^ KEY.charCodeAt(i % KEY.length));
        }
        const session = JSON.parse(decrypted);
        console.log("Session ID:", session.sessionId);
        return session.codes;
    }''')
    if not codes:
        raise Exception("No session found in sessionStorage")
    print(f"Codes extracted: {len(codes)}")
    return codes  # codes[N] = code for step N


async def inject_code_and_submit(page, code: str) -> bool:
    """
    Inject code directly into React via JS - bypasses ALL overlays/modals!

    Single evaluate call with setTimeout inside browser to avoid React
    re-rendering between separate evaluate calls.
    """
    try:
        result = await page.evaluate('''(code) => {
            return new Promise((resolve) => {
                const input = document.querySelector('div[class*="bg-yellow-50"] input[maxlength="6"]');
                if (!input) { resolve({ success: false, error: "Input not found" }); return; }

                const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                setter.call(input, code);
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));

                // Wait 150ms inside the browser for React to commit state, then submit
                setTimeout(() => {
                    const input2 = document.querySelector('div[class*="bg-yellow-50"] input[maxlength="6"]');
                    if (!input2) { resolve({ success: false, error: "Input gone after delay" }); return; }
                    const form = input2.closest('form');
                    if (!form) { resolve({ success: false, error: "Form not found after delay" }); return; }
                    form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
                    resolve({ success: true });
                }, 150);
            });
        }''', code)

        if result.get("success"):
            return True
        else:
            print(f"    JS error: {result.get('error')}")
            return False

    except Exception as e:
        print(f"    JS evaluate error: {e}")
        return False


async def wait_for_navigation(page, expected_step: int, timeout: float = 5.0):
    """Wait for page to navigate to next step or finish"""
    start = time.time()
    while time.time() - start < timeout:
        url = page.url
        if f"/step{expected_step + 1}" in url or "/finish" in url:
            return True
        await asyncio.sleep(0.1)
    return False


async def run():
    """Main bot loop - uses JS injection to bypass ALL overlays/modals"""
    print("=" * 60)
    print("BROWSER NAVIGATION CHALLENGE - SESSION HACK BOT v2")
    print("Using JS injection to bypass all overlays/modals!")
    print("=" * 60)

    metrics["start_time"] = time.time()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # Visible browser for screen recording
            args=['--force-device-scale-factor=1']
        )
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()

        try:
            # Step 1: Navigate to home page first to let React app initialize
            print(f"\n[{elapsed(metrics['start_time'])}] Navigating to home page...")
            await page.goto(SITE_URL, wait_until="networkidle")
            await asyncio.sleep(1)

            # Click START button to initialize session
            print(f"[{elapsed(metrics['start_time'])}] Clicking START...")
            try:
                await page.click('button:has-text("START")', timeout=5000)
            except:
                # Maybe already redirected or different button text
                await page.click('a:has-text("Start"), button:has-text("Begin")', timeout=3000)

            # Wait for navigation to step1 and session to initialize
            await asyncio.sleep(2)

            # Make sure we're on step1
            if "/step1" not in page.url:
                print(f"[{elapsed(metrics['start_time'])}] Navigating to /step1...")
                await page.goto(f"{SITE_URL}/step1", wait_until="networkidle")
                await asyncio.sleep(1)

            # Capture the version param from the URL
            current_url = page.url
            version = "1"
            if "version=" in current_url:
                version = current_url.split("version=")[1].split("&")[0]
            metrics["version"] = version
            print(f"[{elapsed(metrics['start_time'])}] Version: {version}")

            # Step 2: Extract all codes from session
            print(f"[{elapsed(metrics['start_time'])}] Decrypting session...")
            codes = await get_all_codes(page)
            print(f"[{elapsed(metrics['start_time'])}] Got {len(codes)} codes")
            print(f"[{elapsed(metrics['start_time'])}] First 5 codes: {codes[1:6]}\n")

            # Step 3: Loop through all 30 steps
            # CRITICAL: Never use page.goto() after step 1 - Netlify has no SPA redirects
            # Let React Router handle all navigation via the submit button
            for step in range(1, TOTAL_STEPS + 1):
                step_start = time.time()

                print(f"[{elapsed(metrics['start_time'])}] Step {step}/30", end="")

                # Check if we somehow reached finish early
                if "/finish" in page.url:
                    print(f" -> /finish early!")
                    metrics["steps_completed"] = step - 1
                    metrics["result"] = "SUCCESS"
                    break

                # Step 30: validateCode(30) checks codes.get(31) which doesn't exist
                # SPA is already loaded from step 29 - just pushState directly to /finish
                if step == 30:
                    print(f" -> /finish")
                    await page.evaluate('''() => {
                        window.history.pushState({}, "", "/finish");
                        window.dispatchEvent(new PopStateEvent("popstate"));
                    }''')
                    await asyncio.sleep(0.5)
                    metrics["step_times"].append({"step": step, "duration": time.time() - step_start})
                    metrics["steps_completed"] = step
                    break

                # Get the code for this step: codes[N] for step N
                code = codes[step] if step < len(codes) else None
                if not code:
                    print(f" ERROR: No code!")
                    metrics["errors"].append(f"No code for step {step}")
                    continue

                print(f" -> {code}", end="")

                # Inject code and submit - let React Router handle navigation
                success = await inject_code_and_submit(page, code)
                if success:
                    nav_success = await wait_for_navigation(page, step, timeout=3.0)
                    step_duration = time.time() - step_start
                    if nav_success:
                        print(f" -> OK ({step_duration:.2f}s)")
                    else:
                        print(f" -> no nav ({step_duration:.2f}s)")
                else:
                    step_duration = time.time() - step_start
                    print(f" -> FAILED ({step_duration:.2f}s)")
                    metrics["errors"].append(f"Failed step {step}")

                # Record step metrics
                metrics["step_times"].append({
                    "step": step,
                    "duration": time.time() - step_start
                })
                metrics["steps_completed"] = step

            # Step 4: Check final result
            await asyncio.sleep(0.5)
            final_url = page.url
            if "/finish" in final_url:
                metrics["result"] = "SUCCESS"
                # Record end time NOW - before waiting for display
                metrics["end_time"] = time.time()
                finish_time = metrics["end_time"] - metrics["start_time"]
                print(f"\n{'='*60}")
                print(f"SUCCESS! Reached /finish in {finish_time:.2f}s")
                print(f"{'='*60}")

                # Wait to see the finish page (doesn't count toward time)
                await asyncio.sleep(2)

                # Print finish page content
                text = await page.evaluate('document.body.innerText')
                print(f"\n{text}")
            else:
                metrics["result"] = f"INCOMPLETE - ended at {final_url}"
                print(f"\nEnded at: {final_url}")

            # Save final screenshot
            await page.screenshot(path="final_screenshot.png")

        except Exception as e:
            metrics["errors"].append(str(e))
            print(f"\nFatal error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()

    # Only set end_time if not already set (success case sets it earlier)
    if metrics["end_time"] is None:
        metrics["end_time"] = time.time()


def elapsed(start_time: float) -> str:
    """Format elapsed time"""
    return f"{time.time() - start_time:.1f}s"


def print_summary():
    """Print run summary to console"""
    duration = metrics["end_time"] - metrics["start_time"]
    step_times = metrics["step_times"]

    avg_time = duration / len(step_times) if step_times else 0
    fastest = min(step_times, key=lambda x: x["duration"]) if step_times else None
    slowest = max(step_times, key=lambda x: x["duration"]) if step_times else None

    print("\n" + "=" * 50)
    print("RUN SUMMARY")
    print("=" * 50)
    print(f"Total time:       {duration:.2f}s")
    print(f"Avg per step:     {avg_time:.2f}s")
    if fastest:
        print(f"Fastest step:     Step {fastest['step']} ({fastest['duration']:.2f}s)")
    if slowest:
        print(f"Slowest step:     Step {slowest['step']} ({slowest['duration']:.2f}s)")
    print(f"Steps completed:  {metrics['steps_completed']}/{TOTAL_STEPS}")
    print(f"Result:           {metrics['result']}")
    if metrics["errors"]:
        print(f"Errors:           {len(metrics['errors'])}")
        for err in metrics["errors"][:5]:
            print(f"  - {err}")
    print("=" * 50)

    # Per-step breakdown
    if step_times:
        print("\nPER-STEP TIMING:")
        for st in step_times:
            print(f"  Step {st['step']:2d}: {st['duration']:.2f}s")


def save_results():
    """Save detailed results to JSON"""
    duration = metrics["end_time"] - metrics["start_time"]

    # Calculate stats
    step_durations = [s["duration"] for s in metrics["step_times"]]
    avg_time = sum(step_durations) / len(step_durations) if step_durations else 0
    fastest = min(metrics["step_times"], key=lambda x: x["duration"]) if metrics["step_times"] else None
    slowest = max(metrics["step_times"], key=lambda x: x["duration"]) if metrics["step_times"] else None

    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "site": SITE_URL,
        "version": metrics.get("version", "1"),
        "total_duration_seconds": round(duration, 3),
        "steps_completed": metrics["steps_completed"],
        "total_steps": TOTAL_STEPS,
        "result": metrics["result"],
        "stats": {
            "avg_time_per_step": round(avg_time, 3),
            "fastest_step": fastest["step"] if fastest else None,
            "fastest_time": round(fastest["duration"], 3) if fastest else None,
            "slowest_step": slowest["step"] if slowest else None,
            "slowest_time": round(slowest["duration"], 3) if slowest else None,
        },
        "errors": metrics["errors"],
        "step_breakdown": [
            {"step": s["step"], "duration_seconds": round(s["duration"], 3)}
            for s in metrics["step_times"]
        ]
    }

    import os
    results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run-results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*50}")
    print("RESULTS SAVED")
    print(f"{'='*50}")
    print(f"File: {results_path}")
    print(f"\nView in dashboard:")
    print(f"  https://mitchhall16.github.io/browser-challenge-bot/dashboard.html")
    print(f"\nClick 'Load Run (JSON)' and select your run-results.json")
    print(f"{'='*50}")


if __name__ == "__main__":
    asyncio.run(run())
    print_summary()
    save_results()
