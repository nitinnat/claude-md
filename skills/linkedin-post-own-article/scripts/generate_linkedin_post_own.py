#!/usr/bin/env python3
"""
Generate authentic LinkedIn posts from your own published articles.

Uses webpage-to-markdown to extract article content, then generates three different
variations of genuine, conversational LinkedIn posts tailored to sharing your own work.

Usage:
    python generate_linkedin_post_own.py URL
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)

try:
    from google import genai
except ImportError:
    print("Error: google-genai not installed. Run: pip install google-genai")
    sys.exit(1)


def load_api_key() -> str:
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent.parent.parent

    for env_path in [project_root / ".env", Path.cwd() / ".env"]:
        if env_path.exists():
            load_dotenv(env_path)
            break

    return os.environ.get("GOOGLE_API_KEY", "")


def convert_webpage_to_markdown(url: str, output_dir: Path) -> Path:
    script_path = Path(__file__).parent.parent.parent / "webpage-to-markdown" / "scripts" / "convert_webpage.py"

    if not script_path.exists():
        raise FileNotFoundError(f"webpage-to-markdown script not found at {script_path}")

    print("Converting webpage to markdown...")
    result = subprocess.run(
        ["python3", str(script_path), url, "--output-dir", str(output_dir)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"webpage-to-markdown failed: {result.stderr}")

    article_path = output_dir / "article.md"
    if not article_path.exists():
        raise FileNotFoundError(f"article.md not created at {article_path}")

    return article_path


def analyze_article(article_content: str) -> dict:
    lines = article_content.split("\n")
    word_count = len(article_content.split())

    # Extract title
    title = ""
    for line in lines[:5]:
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            break

    # Detect topic type by keywords
    content_lower = article_content.lower()
    is_technical = any(word in content_lower for word in [
        "algorithm", "model", "ml", "ai", "machine learning", "deep learning",
        "neural", "reinforcement learning", "api", "code", "python", "database",
        "system", "architecture", "technical", "engineering"
    ])

    is_business = any(word in content_lower for word in [
        "business", "strategy", "market", "revenue", "growth", "sales",
        "customer", "product", "company", "enterprise", "roi"
    ])

    topic_type = "technical" if is_technical else (
        "business" if is_business else "general"
    )

    # Recommend post length
    if word_count < 500:
        recommended_length = "short (2-3 paragraphs)"
    elif word_count < 1500:
        recommended_length = "medium (3-5 paragraphs)"
    else:
        recommended_length = "long (5-7 paragraphs with detailed insights)"

    # Extract numbers and key statistics
    numbers = re.findall(r'\b(\d+(?:%|x|\\s*(?:billion|million|thousand|percent))?)\b', article_content)
    numbers = list(set(numbers))[:3]

    # Extract sentences with key insights
    key_insights = []
    sentences = re.split(r'[.!?]+', article_content)
    for sentence in sentences[:10]:
        if any(word in sentence.lower() for word in ["algorithm", "model", "solution", "approach"]):
            key_insights.append(sentence.strip())
    key_insights = key_insights[:2]

    return {
        "title": title,
        "word_count": word_count,
        "topic_type": topic_type,
        "recommended_length": recommended_length,
        "key_numbers": numbers,
        "key_insights": key_insights,
        "is_technical": is_technical
    }


def generate_linkedin_post_variation(variation: int, article_analysis: dict, article_content: str, original_url: str, api_key: str) -> str:
    """Generate a specific variation of the LinkedIn post for your own article."""

    # Prepare article excerpt
    article_excerpt = article_content[:3000] if len(article_content) > 3000 else article_content

    # Build topic guidance
    topic_guidance = ""
    if article_analysis["is_technical"]:
        topic_guidance = "This is a technical article. Maintain technical accuracy but keep it accessible to non-specialists."
    else:
        topic_guidance = "Focus on relatable insights and broader implications for your audience."

    # Different prompts for each variation
    variation_prompts = {
        1: f"""You are writing a LinkedIn post to share an article you wrote and published. Write in a genuine, conversational
tone as if you're sharing insights with professional peers over coffee.

Variation 1: Start with what inspired or motivated you to tackle this topic. Lead with the "why."

Article Title: {article_analysis['title']}

Article Content (excerpt):
{article_excerpt}

Article URL: {original_url}

Topic Type: {article_analysis['topic_type']}
{topic_guidance}

Guidelines - What TO do:
- Write in natural paragraphs (not bullet points or lists)
- Be conversational, not corporate or dramatic
- Lead with what inspired or motivated you to explore this topic
- Mix practical insights with broader implications
- Include specific examples/data when they add value
- Recommended length: {article_analysis['recommended_length']}
- End with the article URL on its own line
- Use first person naturally ("I explored", "I wanted to understand", "I built", "I realized")
- Let readers know this is your own work without being salesy

Guidelines - What NOT to do:
- NO emojis of any kind
- NO em-dashes (use regular dashes or write around them)
- NO clickbait openings
- NO dramatic one-liners for effect
- NO "Here's why:", "Here's how:", "Here's the story:" setups
- NO bullet points with emoji markers
- NO explicit self-promotion or requests to follow/share
- NO manufactured suspense or breathless tone
- NO listicle format
- NO ending with CTAs about sharing or following

Write the LinkedIn post now (start writing directly, no preamble):""",

        2: f"""You are writing a LinkedIn post to share an article you wrote and published. Write in a genuine, conversational
tone as if you're sharing insights with professional peers over coffee.

Variation 2: Focus on the problem you were solving or the gap you were addressing. Lead with the challenge.

Article Title: {article_analysis['title']}

Article Content (excerpt):
{article_excerpt}

Article URL: {original_url}

Topic Type: {article_analysis['topic_type']}
{topic_guidance}

Guidelines - What TO do:
- Write in natural paragraphs (not bullet points or lists)
- Be conversational, not corporate or dramatic
- Lead with the problem/challenge you addressed
- Explain your approach and why it matters
- Include specific examples/data when they add value
- Recommended length: {article_analysis['recommended_length']}
- End with the article URL on its own line
- Use first person naturally ("I ran into", "I built", "I explored", "I tackled")
- Let readers know this is your own work naturally

Guidelines - What NOT to do:
- NO emojis of any kind
- NO em-dashes (use regular dashes or write around them)
- NO clickbait openings
- NO dramatic one-liners for effect
- NO "Here's why:", "Here's how:", "Here's the story:" setups
- NO bullet points with emoji markers
- NO explicit self-promotion or requests to follow/share
- NO manufactured suspense or breathless tone
- NO listicle format
- NO ending with CTAs about sharing or following

Write the LinkedIn post now (start writing directly, no preamble):""",

        3: f"""You are writing a LinkedIn post to share an article you wrote and published. Write in a genuine, conversational
tone as if you're sharing insights with professional peers over coffee.

Variation 3: Focus on the key insight or discovery from your work. Lead with the insight.

Article Title: {article_analysis['title']}

Article Content (excerpt):
{article_excerpt}

Article URL: {original_url}

Topic Type: {article_analysis['topic_type']}
{topic_guidance}

Guidelines - What TO do:
- Write in natural paragraphs (not bullet points or lists)
- Be conversational, not corporate or dramatic
- Lead with the central insight or discovery you made
- Explain why this insight matters to others
- Connect to practical implications
- Include specific examples/data when they add value
- Recommended length: {article_analysis['recommended_length']}
- End with the article URL on its own line
- Use first person naturally ("I discovered", "I realized", "What I learned", "I found")
- Let readers know this is your own work without over-emphasizing it

Guidelines - What NOT to do:
- NO emojis of any kind
- NO em-dashes (use regular dashes or write around them)
- NO clickbait openings
- NO dramatic one-liners for effect
- NO "Here's why:", "Here's how:", "Here's the story:" setups
- NO bullet points with emoji markers
- NO explicit self-promotion or requests to follow/share
- NO manufactured suspense or breathless tone
- NO listicle format
- NO ending with CTAs about sharing or following

Write the LinkedIn post now (start writing directly, no preamble):"""
    }

    prompt = variation_prompts[variation]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    post_content = response.text.strip()

    # Ensure URL is on its own line at the end
    if original_url not in post_content:
        post_content = f"{post_content}\n\n{original_url}"
    elif not post_content.endswith(original_url):
        post_content = post_content.replace(original_url, "").strip()
        post_content = f"{post_content}\n\n{original_url}"

    return post_content


def main():
    parser = argparse.ArgumentParser(description="Generate LinkedIn posts from your own article")
    parser.add_argument("url", help="URL of the article you wrote")
    args = parser.parse_args()

    api_key = load_api_key()
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file")
        sys.exit(1)

    # Create temporary output directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        try:
            # Convert webpage to markdown
            article_path = convert_webpage_to_markdown(args.url, temp_dir_path)
            article_content = article_path.read_text()

            # Analyze article
            article_analysis = analyze_article(article_content)
            print(f"Article analyzed: {article_analysis['word_count']} words, {article_analysis['topic_type']} topic")

            # Generate three LinkedIn post variations
            print("Generating three LinkedIn post variations...")
            variations = {}
            for i in range(1, 4):
                print(f"  Generating variation {i}...")
                variations[f"variation_{i}"] = generate_linkedin_post_variation(i, article_analysis, article_content, args.url, api_key)

            # Save all variations to separate files
            for i in range(1, 4):
                post_path = temp_dir_path / f"linkedin-post-variation-{i}.md"
                post_path.write_text(variations[f"variation_{i}"])

            # Also copy article.md to output
            article_output = temp_dir_path / "article.md"
            if article_output.exists() and article_path != article_output:
                article_output.write_text(article_content)

            # Move entire directory to current working directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = Path.cwd() / f"webpage_{timestamp}"
            output_dir.mkdir(exist_ok=True)

            # Copy files from temp to output
            for file in temp_dir_path.glob("*"):
                if file.is_file():
                    (output_dir / file.name).write_text(file.read_text())
                elif file.is_dir():
                    import shutil
                    shutil.copytree(file, output_dir / file.name, dirs_exist_ok=True)

            # Print all variations to stdout
            for i in range(1, 4):
                print("\n" + "="*80)
                print(f"VARIATION {i}: {['Inspiration & Motivation', 'Problem & Solution', 'Key Insight'][i-1]}")
                print("="*80)
                print(variations[f"variation_{i}"])

            print("\n" + "="*80)
            print(f"All variations saved to: {output_dir}")
            print(f"Files:")
            print(f"  - linkedin-post-variation-1.md (Inspiration & Motivation)")
            print(f"  - linkedin-post-variation-2.md (Problem & Solution)")
            print(f"  - linkedin-post-variation-3.md (Key Insight)")
            print(f"  - article.md (Original article)")
            print(f"  - assets/ (Images)")
            print("="*80)

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
