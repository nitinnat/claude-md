---
name: webpage-to-markdown
description: Convert webpages to clean markdown with local images and multi-level summaries. Bypasses paywalls using Jina Reader. Use when users want to save articles, convert web content to markdown, archive webpages with images, or need offline access to web articles. Outputs folder with article.md and assets/ directory.
---

# Webpage to Markdown

Convert any webpage to clean markdown with locally downloaded images, AI-generated image descriptions, and three-level summaries (ELI5, High School, College Graduate).

## Prerequisites

- `GOOGLE_API_KEY` in .env file (for image analysis and summary generation via Gemini)
- Python packages: `requests`, `google-genai`, `python-dotenv`

## Quick Start

```bash
python3 .claude/skills/webpage-to-markdown/scripts/convert_webpage.py "https://example.com/article"
```

## Usage

```bash
python3 scripts/convert_webpage.py URL [--output-dir DIR]
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| url | Yes | The webpage URL to convert |
| --output-dir | No | Custom output directory (default: `webpage_YYYYMMDD_HHMMSS/`) |

### Examples

Convert article to current directory:
```bash
python3 scripts/convert_webpage.py "https://techblog.example.com/machine-learning-intro"
```

Convert to specific folder:
```bash
python3 scripts/convert_webpage.py "https://news.site.com/article" --output-dir my-article
```

## How It Works

1. **Fetch via Jina Reader** - Prepends `https://r.jina.ai/` to bypass paywalls and get clean markdown
2. **Download Images** - Saves all images locally with content-hash naming (prevents duplicates)
3. **Analyze Images** - Gemini 2.0 Flash describes each image contextually (1-2 sentences)
4. **Generate Summary** - Gemini 2.0 Flash creates three-level summary section
5. **Save Output** - Writes article.md with local image paths and descriptions

## Output Structure

```
webpage_20260104_143022/
├── article.md
└── assets/
    ├── 3a8f9b2c1d4e.jpg
    ├── 7f2a1c8d9e0b.png
    └── ...
```

The article.md contains:
- Original article content with images replaced by local paths
- Image descriptions in italics below each image
- Summary section at the end with ELI5, High School, and College Graduate explanations

## Error Handling

- **No GOOGLE_API_KEY**: Runs without image analysis or summaries
- **Failed image download**: Logs warning, keeps original URL
- **Failed image analysis**: Skips description for that image
- **Failed summary generation**: Article saved without summary section

## References

- See [references/jina_api.md](references/jina_api.md) for Jina Reader technical details
- See [references/summary_guidelines.md](references/summary_guidelines.md) for summary quality guidelines
