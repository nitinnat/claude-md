# Screenshot Capture Skill

Capture screenshots of web pages and social media posts for blog illustrations.

## Prerequisites

- Node.js and npm installed
- Playwright browsers installed (`npx playwright install`)

## Quick Start

When the user needs screenshots of social media posts, tweets, or web pages:

1. Run the screenshot script with the URL
2. Images are saved to `public/assets/screenshots/`
3. Return the file path to reference in blog posts

## Usage

Execute the script at `scripts/screenshot.js`:

```bash
node .claude/skills/screenshot-capture/scripts/screenshot.js <URL> [--output filename] [--selector CSS_SELECTOR] [--full-page]
```

### Parameters

- **URL** (required): The web page or post to capture
- **--output**: Custom filename without extension (default: timestamp-based)
- **--selector**: CSS selector to capture a specific element instead of full viewport
- **--full-page**: Capture the entire scrollable page

### Examples

```bash
# Capture a tweet
node .claude/skills/screenshot-capture/scripts/screenshot.js "https://twitter.com/user/status/123456" --output moltbook_tweet

# Capture specific element
node .claude/skills/screenshot-capture/scripts/screenshot.js "https://example.com" --selector ".post-content"

# Full page screenshot
node .claude/skills/screenshot-capture/scripts/screenshot.js "https://example.com" --full-page
```

## Output

- Images are saved as PNG files
- Default location: `public/assets/screenshots/` in project root
- Filename format: `<custom-name>.png` or `screenshot_<timestamp>.png`

## Tips for Social Media

- For Twitter/X: Use the direct tweet URL
- For Reddit: Use the post permalink
- For embedded content: Use `--selector` to capture just the relevant element
- Screenshots include a timestamp in metadata

## Error Handling

The script will display clear error messages for:
- Invalid URLs
- Network issues
- Element not found (when using --selector)
- Browser launch failures
