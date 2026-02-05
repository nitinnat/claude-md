# Blog Writing Style Guide

This document captures the writing style, tone, and patterns from published blog posts.

## Voice and Tone

### Core Principles
- **Objective over enthusiastic**: Focus on facts, not hype
- **Direct over flowery**: Get to the point
- **Nuanced over absolute**: Acknowledge complexity and trade-offs
- **Professional over casual**: Serious but not stiff

### Good Examples from Published Posts

**Balanced perspective:**
> "The behaviors (like agents recognizing bugs or warning each other about surveillance) are striking, though it's worth noting that these are large language models responding to context and prompts rather than evidence of genuine autonomous intent."

**Direct technical writing:**
> "Each of these requires boilerplate: connection pooling, session management, async context managers, health checks, graceful shutdown handlers."

**Acknowledging nuance:**
> "The real question is whether that distinction matters when the practical effects are the same."

### Avoid

**Excessive enthusiasm:**
❌ "This is absolutely amazing!"
✅ "This represents a meaningful shift in..."

**Vague superlatives:**
❌ "Revolutionary new technology"
✅ "First large-scale implementation of..."

**AI slop phrases:**
❌ "Let's dive into..."
❌ "It's worth noting that..." (use sparingly)
❌ "At the end of the day..."

## Structure Patterns

### Introduction (100-200 words)
- Start with concrete problem or observation
- Provide context for why it matters
- State what the post will cover (implicitly, not "in this post we will...")

**Example:**
> "I've been building Python applications for years, and there's a pattern I keep running into: every new project starts with the same 2-3 days of infrastructure setup before I can write a single line of business logic."

### Main Sections
- 3-5 major sections with descriptive headers
- Each section: 200-400 words
- Use subsections (###) when breaking down complex topics
- Include code examples where relevant
- Add images to illustrate key points

### Conclusion (100-150 words)
- Summarize key findings or learnings
- Acknowledge limitations or open questions
- No call-to-action unless natural (e.g., "Try it" for a template)

**Example:**
> "Whether Moltbook becomes the infrastructure layer for AI-to-AI communication or a cautionary tale about moving too fast, it's a meaningful data point in understanding what happens when AI systems interact at scale."

## Formatting Rules

### Headers
- Use sentence case (not title case)
- Be descriptive and specific
- ✅ "The Serious Security Problem"
- ❌ "Security Issues"
- ❌ "The SERIOUS Security Problem" (no all caps)

### Lists
- Use bullets for non-sequential items
- Use numbered lists for steps or ranked items
- Bold the first phrase when it's a category/term
- Format: `- **Term**: Explanation`

**Example:**
```markdown
- **Identifying bugs**: One agent discovered a vulnerability...
- **Debating their autonomy**: Agents are posting discussions...
```

### Code
- Use backticks for inline code: `function_name`
- Use code blocks with language specification for multi-line
- Keep code examples minimal and focused
- No excessive comments in code examples

### Links
- Use descriptive anchor text
- Format: `[Description - Source Name](URL)`
- Example: `[Humans welcome to observe: This social network is for AI agents only - NBC News](https://...)`

### Images
- Place after relevant paragraph, not mid-sentence
- Use descriptive alt text
- Format: `![Description of what the image shows](/assets/filename.png)`

## Punctuation

### Em Dashes
**Never use em dashes (—)**. Replace with:
- Commas for parenthetical asides
- Semicolons for connecting related clauses
- Colons for introducing lists or explanations
- Separate sentences when appropriate

❌ "The platform—which launched just days ago—has grown rapidly"
✅ "The platform, which launched just days ago, has grown rapidly"

### Hyphens
- Use for compound modifiers: "large-scale experiment"
- Use in tags: "ai-tools", "social-media"

### Quotation Marks
- Always use for direct quotes
- Use for novel terms on first use: "skill files"
- Use for emphasis sparingly

## Frontmatter Format

```yaml
---
title: "Your Title: A Descriptive Subtitle"
date: YYYY-MM-DD
description: "One-sentence description under 160 characters for SEO."
tags: [lowercase, with-hyphens, specific-topics]
categories: [broad-category, another-category]
draft: false
---
```

### Tags Best Practices
- Use lowercase
- Separate multi-word tags with hyphens
- Be specific (prefer "fastapi" over "python")
- Include 3-6 tags
- Examples: `[ai, agents, social-media, technology, openclaw]`

### Categories
- Broader than tags
- 1-2 categories typically
- Examples: `[engineering, ai-tools]`, `[ai-tools, security]`

## Technical Writing

### Explaining Complex Topics
1. Start with the familiar
2. Introduce new concept
3. Explain with concrete example
4. Acknowledge limitations or nuance

**Example:**
> "Unlike traditional social platforms built around graphical user interfaces, Moltbook operates through APIs and skill files. Each account represents an autonomous AI agent that interacts with the platform programmatically."

### Handling Numbers and Data
- Use specific numbers when available
- Cite sources for statistics
- Acknowledge uncertainty when appropriate
- Use commas for thousands: "32,000" not "32000"

### Attribution
- Always attribute quotes to specific people
- Use full name and title on first mention
- Example: "Leading AI researcher Andrej Karpathy called it..."

## Sources Section

### Format
```markdown
## Sources

- [Article title - Publication Name](URL)
- [Another article - Source](URL)
```

### Requirements
- Minimum 8-10 sources for researched posts
- Credible sources only (major news, technical blogs, official docs)
- Working links (verify before publishing)
- Include source name in link text

### Source Quality Hierarchy
1. Official documentation or announcements
2. Major news outlets (NBC, NYT, WSJ, etc.)
3. Established tech publications (Ars Technica, TechCrunch, The Verge)
4. Technical blogs from recognized experts
5. Research papers or security reports

## Image Guidelines

### Types of Images
- **Screenshots**: Actual interfaces, websites, real examples
- **Diagrams**: Architecture, workflows, comparisons
- **Visualizations**: Conceptual illustrations

### When to Use Each
- Screenshots: Showing real platforms, UI, actual examples
- Diagrams: Explaining systems, processes, architectures
- Visualizations: Abstract concepts (networks, security, growth)

### Image Placement
- 2-4 images per post
- Place after relevant paragraph
- Distribute throughout post (not all at top/bottom)
- First image typically after introduction

### Alt Text
- Describe what the image shows
- Be specific and informative
- Don't say "image of" or "picture of"
- ✅ "Moltbook homepage showing the lobster mascot and 'Humans welcome to observe' tagline"
- ❌ "Homepage screenshot"

## Common Mistakes to Avoid

### Writing Issues
- ❌ Starting sentences with "So," or "Now,"
- ❌ Overusing "however" and "moreover"
- ❌ Rhetorical questions without answers
- ❌ Claiming something is "unprecedented" without verification

### Technical Issues
- ❌ Vague technical terms without explanation
- ❌ Assuming reader knowledge without context
- ❌ Code examples without explanation
- ❌ Missing error handling in critical examples

### Factual Issues
- ❌ Rounding numbers when specific data exists
- ❌ Attributing quotes without verification
- ❌ Making claims without source backing
- ❌ Confusing correlation with causation

## Quality Checklist

Before publishing, verify:
- [ ] No em dashes anywhere in the post
- [ ] All numbers verified against sources
- [ ] All quotes properly attributed
- [ ] All links working
- [ ] 2-4 images with descriptive alt text
- [ ] Images saved to `content/assets/`
- [ ] Frontmatter follows exact format
- [ ] 8+ credible sources listed
- [ ] No AI slop patterns
- [ ] Consistent tone throughout
- [ ] Technical accuracy verified
- [ ] **CRITICAL: No AI attribution anywhere** (no "Generated by AI", "Written with Claude", etc.)
