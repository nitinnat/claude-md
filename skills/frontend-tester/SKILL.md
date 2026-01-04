---
name: frontend-tester
description: Test frontend applications using Playwright. Use when users want to test web UI, verify frontend requirements, check UI behavior, run browser automation tests, or validate that a web application works correctly. Supports screenshot capture, element interaction, and assertion-based testing.
---

# Frontend Tester

Test frontend applications using Playwright browser automation.

## Prerequisites

- Python 3.8+
- Playwright installed: `pip install playwright && playwright install`

## Quick Start

When the user wants to test frontend requirements:

1. Understand the requirements to test
2. Run the test script with appropriate parameters
3. Review results and screenshots

## Usage

Execute the script at `scripts/run_test.py`:

```bash
python3 .claude/skills/frontend-tester/scripts/run_test.py --url "http://localhost:3000" --test-file tests.json
```

### Parameters

- **--url** (required): Base URL of the application to test
- **--test-file**: JSON file containing test definitions
- **--screenshot-dir**: Directory for screenshots (default: `test_screenshots/`)
- **--headless**: Run in headless mode (default: true)
- **--browser**: Browser to use: chromium, firefox, webkit (default: chromium)

### Test File Format

Create a JSON file defining tests:

```json
{
  "tests": [
    {
      "name": "Homepage loads correctly",
      "steps": [
        {"action": "goto", "url": "/"},
        {"action": "screenshot", "name": "homepage"},
        {"action": "assert_visible", "selector": "h1"},
        {"action": "assert_text", "selector": "h1", "text": "Welcome"}
      ]
    },
    {
      "name": "Login form works",
      "steps": [
        {"action": "goto", "url": "/login"},
        {"action": "fill", "selector": "#email", "value": "test@example.com"},
        {"action": "fill", "selector": "#password", "value": "password123"},
        {"action": "click", "selector": "button[type=submit]"},
        {"action": "wait_for_url", "url": "/dashboard"},
        {"action": "screenshot", "name": "dashboard"}
      ]
    }
  ]
}
```

### Available Actions

| Action | Parameters | Description |
|--------|------------|-------------|
| `goto` | `url` | Navigate to URL (relative or absolute) |
| `click` | `selector` | Click an element |
| `fill` | `selector`, `value` | Fill an input field |
| `type` | `selector`, `value` | Type text with key events |
| `press` | `key` | Press a keyboard key |
| `screenshot` | `name` | Capture screenshot |
| `wait` | `ms` | Wait for milliseconds |
| `wait_for_selector` | `selector`, `state` (optional) | Wait for element |
| `wait_for_url` | `url` | Wait for navigation |
| `assert_visible` | `selector` | Assert element is visible |
| `assert_hidden` | `selector` | Assert element is hidden |
| `assert_text` | `selector`, `text` | Assert element contains text |
| `assert_value` | `selector`, `value` | Assert input has value |
| `assert_url` | `url` | Assert current URL matches |
| `hover` | `selector` | Hover over element |
| `select` | `selector`, `value` | Select dropdown option |
| `check` | `selector` | Check a checkbox |
| `uncheck` | `selector` | Uncheck a checkbox |

### Interactive Mode

For quick one-off tests without a test file:

```bash
python3 .claude/skills/frontend-tester/scripts/run_test.py --url "http://localhost:3000" --interactive
```

In interactive mode, pass actions as JSON:

```bash
python3 .claude/skills/frontend-tester/scripts/run_test.py \
  --url "http://localhost:3000" \
  --actions '[{"action": "goto", "url": "/"}, {"action": "screenshot", "name": "home"}]'
```

## Example Workflows

### Verify a button click updates the UI

```json
{
  "tests": [{
    "name": "Counter increments",
    "steps": [
      {"action": "goto", "url": "/"},
      {"action": "assert_text", "selector": "#count", "text": "0"},
      {"action": "click", "selector": "#increment"},
      {"action": "assert_text", "selector": "#count", "text": "1"},
      {"action": "screenshot", "name": "counter_incremented"}
    ]
  }]
}
```

### Test form validation

```json
{
  "tests": [{
    "name": "Email validation shows error",
    "steps": [
      {"action": "goto", "url": "/signup"},
      {"action": "fill", "selector": "#email", "value": "invalid-email"},
      {"action": "click", "selector": "button[type=submit]"},
      {"action": "assert_visible", "selector": ".error-message"},
      {"action": "assert_text", "selector": ".error-message", "text": "valid email"}
    ]
  }]
}
```

### Test responsive layout

```json
{
  "tests": [{
    "name": "Mobile menu appears on small screens",
    "viewport": {"width": 375, "height": 667},
    "steps": [
      {"action": "goto", "url": "/"},
      {"action": "assert_visible", "selector": ".mobile-menu-button"},
      {"action": "assert_hidden", "selector": ".desktop-nav"},
      {"action": "screenshot", "name": "mobile_layout"}
    ]
  }]
}
```

## Output

- Test results printed to stdout with pass/fail status
- Screenshots saved to `test_screenshots/` (or custom directory)
- Exit code 0 on all tests passing, 1 on any failure
