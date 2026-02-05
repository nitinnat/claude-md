---
name: linkedin-post-generator
description: Generate authentic, conversational LinkedIn posts from webpage content. Uses webpage-to-markdown to extract article, then crafts genuine posts without emojis or AI tells. Use when users want to share articles on LinkedIn, create thought leadership content, or transform long-form content into engaging social posts.
---

# LinkedIn Post Generator

Generate authentic LinkedIn posts from any webpage. The skill extracts clean article content using webpage-to-markdown, analyzes the topic, and crafts a genuine post that sounds like a real person sharing insights—not AI-generated or disingenuous.

## Prerequisites

- `GOOGLE_API_KEY` in .env file (for content analysis and post generation via Gemini)
- Python packages: `google-genai`, `python-dotenv`
- webpage-to-markdown skill (must be installed in skills/ directory)

## Quick Start

```bash
python3 skills/linkedin-post-generator/scripts/generate_linkedin_post.py "https://example.com/article"
```

The script will:
1. Convert the webpage to markdown using webpage-to-markdown
2. Analyze the content to determine topic type and key insights
3. Generate three different authentic LinkedIn post variations
4. Save all variations to `linkedin-post-variation-1.md`, `linkedin-post-variation-2.md`, and `linkedin-post-variation-3.md`
5. Print all three variations to stdout so you can choose the one you prefer

## Usage

```bash
python3 scripts/generate_linkedin_post.py URL
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| URL | Yes | The webpage URL to convert and analyze |

### Examples

Generate post from tech blog:
```bash
python3 scripts/generate_linkedin_post.py "https://techblog.example.com/machine-learning-article"
```

Generate post from business article:
```bash
python3 scripts/generate_linkedin_post.py "https://news.example.com/startup-strategy"
```

## How It Works

1. **Extract Article** - Calls webpage-to-markdown to fetch and clean the article
2. **Analyze Content** - Determines topic type (technical, business, general), word count, and key insights
3. **Generate Three Variations** - Uses Gemini 2.0 Flash to craft three different authentic posts:
   - **Variation 1: Personal Reaction** - Leads with what caught your attention
   - **Variation 2: Problem-Solution** - Focuses on problem being solved
   - **Variation 3: Key Insight** - Focuses on the central takeaway
4. **Enforce Authenticity** - All variations avoid AI tells: emojis, em-dashes, clickbait, drama, self-promotion
5. **Save Output** - Writes all three variations alongside `article.md` in the output folder

## Output Structure

```
webpage_20260104_143022/
├── article.md                       # Original article from webpage-to-markdown
├── linkedin-post-variation-1.md     # Personal Reaction approach
├── linkedin-post-variation-2.md     # Problem-Solution approach
├── linkedin-post-variation-3.md     # Key Insight approach
└── assets/                          # Images from webpage-to-markdown
    └── ...
```

All three variations are ready to copy-paste into LinkedIn. Choose the one that resonates most with your voice and the article's focus.

## Post Quality Guidelines

### What Makes an Authentic Post

- **Genuine voice**: Sounds like a peer sharing insights, not a marketer
- **Value-first**: Leads with what readers learn, not self-promotion
- **Specific**: Uses real numbers, quotes, and examples
- **Conversational**: Natural paragraphs, contractions, no corporate speak
- **No AI tells**: Zero emojis, no em-dashes, no clickbait, no drama

### Tone by Topic

- **Technical articles**: Maintain accuracy but stay accessible. Explain why it matters.
- **Business articles**: Focus on practical implications and relatable insights
- **General interest**: Share what surprised you and why it's interesting

### Things the Post Will NOT Have

- Emojis (none, not decorative ones, not rockets or pointing fingers)
- Em-dashes (replaced with regular dashes or rewritten)
- Clickbait openings ("X just solved Y's biggest problem")
- Dramatic one-liners for effect
- "Here's why:", "Here's how:", "Here's the story:" setups
- Bullet points with emoji markers
- Requests to follow, share, or comment
- Manufactured suspense or breathless tone
- Listicle format
- Self-promotion

## Error Handling

- **No GOOGLE_API_KEY**: Script exits with clear error message
- **webpage-to-markdown not found**: Script exits with path guidance
- **Failed article conversion**: Error reported from webpage-to-markdown
- **Failed post generation**: Logs error and exits cleanly

## References

- See [references/post_examples.md](references/post_examples.md) for good vs bad post examples
- See [references/writing_guidelines.md](references/writing_guidelines.md) for detailed writing best practices
