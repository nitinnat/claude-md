# Jina Reader API

## Overview
Jina Reader converts any URL to clean markdown by prepending `https://r.jina.ai/` to the target URL.

## How It Works
1. Headless Chrome browser fetches the webpage
2. Mozilla Readability extracts main content (removes headers, footers, navigation)
3. Turndown converts HTML to markdown
4. Returns clean, LLM-friendly markdown

## Usage
```
https://r.jina.ai/{your-url}
```

## Capabilities
- Bypasses many paywalls via reader-mode extraction
- Handles dynamic JavaScript-rendered content
- Processes PDFs (extracts text via PDF.js)
- Supports most major news sites and blogs
- Free tier with no authentication required

## Limitations
- Complex interactive pages may lose functionality
- Some paywalls require authentication (not bypassed)
- Very long pages may be truncated
- Images are returned as URLs (not downloaded)
- Rate limits may apply for heavy usage

## Response Format
Returns raw markdown text. Common elements:
- `# Title` - Main headline
- `![alt](url)` - Images with original URLs
- Standard markdown formatting (bold, italic, lists, code)

## Error Handling
- 404: Page not found
- 503: Service temporarily unavailable
- Timeout: Complex pages may take >30 seconds

## Alternatives
If Jina fails:
1. Try `https://archive.is/{url}` for cached versions
2. Use browser automation (Playwright) for authenticated sessions
3. Fall back to raw HTML fetch with BeautifulSoup parsing
