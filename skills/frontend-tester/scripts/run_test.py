#!/usr/bin/env python3
"""
Run Playwright tests for frontend applications.

Usage:
    python run_test.py --url URL --test-file FILE
    python run_test.py --url URL --actions '[...]'
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, expect
except ImportError:
    print("Error: playwright not installed. Run: pip install playwright && playwright install")
    sys.exit(1)


def run_action(page, action: dict, base_url: str, screenshot_dir: Path) -> bool:
    act = action["action"]

    if act == "goto":
        url = action["url"]
        if url.startswith("/"):
            url = base_url.rstrip("/") + url
        page.goto(url)
    elif act == "click":
        page.locator(action["selector"]).click()
    elif act == "fill":
        page.locator(action["selector"]).fill(action["value"])
    elif act == "type":
        page.locator(action["selector"]).type(action["value"])
    elif act == "press":
        page.keyboard.press(action["key"])
    elif act == "screenshot":
        path = screenshot_dir / f"{action['name']}.png"
        page.screenshot(path=str(path))
        print(f"  Screenshot saved: {path}")
    elif act == "wait":
        page.wait_for_timeout(action["ms"])
    elif act == "wait_for_selector":
        state = action.get("state", "visible")
        page.locator(action["selector"]).wait_for(state=state)
    elif act == "wait_for_url":
        url = action["url"]
        if url.startswith("/"):
            url = base_url.rstrip("/") + url
        page.wait_for_url(url)
    elif act == "assert_visible":
        expect(page.locator(action["selector"])).to_be_visible()
    elif act == "assert_hidden":
        expect(page.locator(action["selector"])).to_be_hidden()
    elif act == "assert_text":
        expect(page.locator(action["selector"])).to_contain_text(action["text"])
    elif act == "assert_value":
        expect(page.locator(action["selector"])).to_have_value(action["value"])
    elif act == "assert_url":
        url = action["url"]
        if url.startswith("/"):
            url = base_url.rstrip("/") + url
        expect(page).to_have_url(url)
    elif act == "hover":
        page.locator(action["selector"]).hover()
    elif act == "select":
        page.locator(action["selector"]).select_option(action["value"])
    elif act == "check":
        page.locator(action["selector"]).check()
    elif act == "uncheck":
        page.locator(action["selector"]).uncheck()
    else:
        print(f"  Unknown action: {act}")
        return False

    return True


def run_test(playwright, test: dict, base_url: str, screenshot_dir: Path, browser_type: str, headless: bool) -> bool:
    name = test.get("name", "Unnamed test")
    steps = test.get("steps", [])
    viewport = test.get("viewport")

    print(f"\nRunning: {name}")

    browser_launcher = getattr(playwright, browser_type)
    browser = browser_launcher.launch(headless=headless)

    context_options = {}
    if viewport:
        context_options["viewport"] = viewport

    context = browser.new_context(**context_options)
    page = context.new_page()

    try:
        for i, step in enumerate(steps):
            action_name = step.get("action", "unknown")
            print(f"  Step {i+1}: {action_name}")
            run_action(page, step, base_url, screenshot_dir)
        print(f"  PASSED")
        return True
    except Exception as e:
        print(f"  FAILED: {e}")
        error_path = screenshot_dir / f"error_{datetime.now().strftime('%H%M%S')}.png"
        page.screenshot(path=str(error_path))
        print(f"  Error screenshot: {error_path}")
        return False
    finally:
        browser.close()


def main():
    parser = argparse.ArgumentParser(description="Run Playwright frontend tests")
    parser.add_argument("--url", required=True, help="Base URL of the application")
    parser.add_argument("--test-file", help="JSON file containing test definitions")
    parser.add_argument("--actions", help="JSON string of actions for quick test")
    parser.add_argument("--screenshot-dir", default="test_screenshots", help="Screenshot directory")
    parser.add_argument("--headless", action="store_true", default=True, help="Run headless")
    parser.add_argument("--no-headless", action="store_false", dest="headless", help="Show browser")
    parser.add_argument("--browser", default="chromium", choices=["chromium", "firefox", "webkit"])

    args = parser.parse_args()

    screenshot_dir = Path(args.screenshot_dir)
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    tests = []

    if args.test_file:
        with open(args.test_file) as f:
            data = json.load(f)
            tests = data.get("tests", [data] if "steps" in data else [])
    elif args.actions:
        tests = [{"name": "Quick test", "steps": json.loads(args.actions)}]
    else:
        print("Error: Provide --test-file or --actions")
        sys.exit(1)

    print(f"Testing: {args.url}")
    print(f"Browser: {args.browser} (headless={args.headless})")
    print(f"Tests to run: {len(tests)}")

    passed = 0
    failed = 0

    with sync_playwright() as playwright:
        for test in tests:
            if run_test(playwright, test, args.url, screenshot_dir, args.browser, args.headless):
                passed += 1
            else:
                failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
