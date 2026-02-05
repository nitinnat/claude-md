---
name: linkedin-post-own-article
description: Generate authentic LinkedIn posts to promote your own published articles. Uses webpage-to-markdown to extract content, then creates three distinct post variations tailored to sharing your work. Use when you want to share articles you've written on LinkedIn with authentic voice and different angles.
---

# LinkedIn Post for Own Article

Generate authentic LinkedIn posts specifically designed to promote your own published articles. The skill extracts clean article content and crafts genuine posts that sound like you sharing your own work—not someone promoting it for you.

## Prerequisites

- `GOOGLE_API_KEY` in .env file (for content analysis and post generation via Gemini)
- Python packages: `google-genai`, `python-dotenv`
- webpage-to-markdown skill (must be installed in skills/ directory)

## Quick Start

```bash
python3 skills/linkedin-post-own-article/scripts/generate_linkedin_post_own.py "https://yoursite.com/article"
```

The script will:
1. Convert the webpage to markdown using webpage-to-markdown
2. Analyze the content to determine topic type and key insights
3. Generate three different LinkedIn post variations tailored to your work
4. Save all variations to `linkedin-post-variation-1.md`, `linkedin-post-variation-2.md`, and `linkedin-post-variation-3.md`
5. Print all three variations to stdout so you can choose the one you prefer

## Usage

```bash
python3 scripts/generate_linkedin_post_own.py URL
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| URL | Yes | The URL of your published article |

### Examples

Share a technical article you wrote:
```bash
python3 scripts/generate_linkedin_post_own.py "https://yoursite.com/articles/machine-learning-guide"
```

Share a business/startup article:
```bash
python3 scripts/generate_linkedin_post_own.py "https://yoursite.com/posts/product-strategy"
```

## How It Works

1. **Extract Article** - Calls webpage-to-markdown to fetch and clean your article
2. **Analyze Content** - Determines topic type (technical, business, general), word count, and key insights
3. **Generate Three Variations** - Uses Gemini 2.0 Flash to craft three different posts, each highlighting different angles:
   - **Variation 1: Inspiration & Motivation** - Leads with what inspired you to write this
   - **Variation 2: Problem & Solution** - Focuses on the problem/gap you addressed
   - **Variation 3: Key Insight** - Focuses on the key discovery or takeaway
4. **Enforce Authenticity** - All variations sound like you sharing your own work: no emojis, em-dashes, clickbait, or artificial drama
5. **Save Output** - Writes all three variations alongside `article.md` in the output folder

## Output Structure

```
webpage_20260104_143022/
├── article.md                       # Your article from webpage-to-markdown
├── linkedin-post-variation-1.md     # Inspiration & Motivation approach
├── linkedin-post-variation-2.md     # Problem & Solution approach
├── linkedin-post-variation-3.md     # Key Insight approach
└── assets/                          # Images from webpage-to-markdown
    └── ...
```

All three variations are ready to copy-paste into LinkedIn. Choose the one that best represents your voice and the article's focus.

## Post Quality Guidelines

### What Makes an Authentic Post About Your Own Work

- **Your voice**: Sounds like you explaining your work to a peer
- **Genuine motivation**: Explains why you wrote/built this
- **Value-first**: Leads with insights and value, not "check out my article"
- **Specific**: Uses real numbers, examples from your work
- **Conversational**: Natural paragraphs, contractions, no corporate speak
- **No AI tells**: Zero emojis, no em-dashes, no clickbait, no drama

### Tone by Topic

- **Technical articles**: Explain the problem you solved and why it matters
- **Business articles**: Focus on the challenge you addressed and practical implications
- **General interest**: Share what inspired you to explore this and what you discovered

### Things the Post Will NOT Have

- Emojis
- Em-dashes (replaced with regular dashes or rewritten)
- Clickbait openings
- Dramatic one-liners
- "Here's why:", "Here's how:", "Here's the story:" setups
- Bullet points with emoji markers
- Requests to follow, share, or comment
- Manufactured suspense or breathless tone
- Listicle format

## Error Handling

- **No GOOGLE_API_KEY**: Script exits with clear error message
- **webpage-to-markdown not found**: Script exits with path guidance
- **Failed article conversion**: Error reported from webpage-to-markdown
- **Failed post generation**: Logs error and exits cleanly

## References

- See [references/post_examples.md](references/post_examples.md) for examples of good vs bad posts about your own work
- See [references/writing_guidelines.md](references/writing_guidelines.md) for best practices when sharing your own articles
