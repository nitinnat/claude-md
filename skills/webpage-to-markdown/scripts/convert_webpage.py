#!/usr/bin/env python3
"""
Convert webpage to markdown with local images and multi-level summaries.

Usage:
    python convert_webpage.py URL [--output-dir DIR]
"""

import argparse
import hashlib
import mimetypes
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Error: requests not installed. Run: pip install requests")
    sys.exit(1)

try:
    from google import genai
    from google.genai import types
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


def fetch_webpage(url: str) -> str:
    jina_url = f"https://r.jina.ai/{url}"
    print("Fetching webpage via Jina Reader...")

    response = requests.get(jina_url, timeout=60, headers={
        "User-Agent": "Mozilla/5.0 (compatible; WebpageToMarkdown/1.0)"
    })
    response.raise_for_status()

    print(f"Fetched {len(response.text)} characters")
    return response.text


def download_image(url: str, assets_dir: Path) -> str | None:
    if url.startswith("data:"):
        return None

    try:
        response = requests.get(url, timeout=30, headers={
            "User-Agent": "Mozilla/5.0 (compatible; WebpageToMarkdown/1.0)"
        })
        response.raise_for_status()

        content_hash = hashlib.md5(response.content).hexdigest()[:12]
        content_type = response.headers.get("Content-Type", "image/jpeg").split(";")[0]
        ext = mimetypes.guess_extension(content_type) or ".jpg"
        if ext == ".jpe":
            ext = ".jpg"

        filename = f"{content_hash}{ext}"
        filepath = assets_dir / filename

        if not filepath.exists():
            filepath.write_bytes(response.content)
            print(f"Downloaded: {filename}")

        return f"assets/{filename}"
    except Exception as e:
        print(f"Warning: Failed to download {url[:60]}...: {e}")
        return None


def analyze_image(image_path: Path, client: genai.Client, context: str) -> str:
    try:
        image_bytes = image_path.read_bytes()
        media_type = mimetypes.guess_type(str(image_path))[0] or "image/jpeg"

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=media_type),
                f"Describe this image concisely (1-2 sentences) in the context of an article about: {context[:200]}"
            ]
        )

        return response.text
    except Exception as e:
        print(f"Warning: Failed to analyze image {image_path.name}: {e}")
        return ""


def process_markdown_images(markdown: str, assets_dir: Path, client: genai.Client | None) -> str:
    title_match = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
    context = title_match.group(1) if title_match else "this article"

    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    processed_urls = {}

    def replace_image(match):
        alt_text = match.group(1)
        url = match.group(2)

        if url.startswith(".") or url.startswith("assets/"):
            return match.group(0)

        if url in processed_urls:
            local_path, description = processed_urls[url]
        else:
            local_path = download_image(url, assets_dir)
            if not local_path:
                return match.group(0)

            full_path = assets_dir.parent / local_path
            description = analyze_image(full_path, client, context) if client else ""
            processed_urls[url] = (local_path, description)

        if description:
            return f"![{alt_text}]({local_path})\n\n*{description}*\n"
        return f"![{alt_text}]({local_path})\n"

    return re.sub(pattern, replace_image, markdown)


def generate_summary(article_content: str, client: genai.Client) -> str:
    print("Generating summaries...")

    prompt = f"""Analyze this article and create a Summary section with three subsections.

Write each summary as a concise paragraph (2-4 sentences):

1. **ELI5** - Explain like I'm 5 years old. Use simple words, analogies, and relatable examples.
2. **High School** - Explain for a high school student. Clear and educational with some technical terms.
3. **College Graduate** - Explain for someone with a degree in the relevant field. Use proper terminology and nuanced analysis.

Format as:

## Summary

### ELI5
[paragraph]

### High School
[paragraph]

### College Graduate
[paragraph]

Article:
{article_content[:15000]}"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text


def main():
    parser = argparse.ArgumentParser(description="Convert webpage to markdown with images and summaries")
    parser.add_argument("url", help="URL of the webpage to convert")
    parser.add_argument("--output-dir", help="Output directory name (default: auto-generated timestamp)")
    args = parser.parse_args()

    api_key = load_api_key()
    client = None

    if not api_key:
        print("Warning: GOOGLE_API_KEY not found. Images won't be analyzed and summaries won't be generated.")
    else:
        client = genai.Client(api_key=api_key)

    try:
        markdown = fetch_webpage(args.url)
    except requests.RequestException as e:
        print(f"Error: Failed to fetch webpage: {e}")
        sys.exit(1)

    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(f"webpage_{timestamp}")

    output_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(exist_ok=True)

    print("Processing images...")
    processed_markdown = process_markdown_images(markdown, assets_dir, client)

    if client:
        try:
            summary = generate_summary(processed_markdown, client)
            processed_markdown = f"{processed_markdown}\n\n---\n\n{summary}"
        except Exception as e:
            print(f"Warning: Failed to generate summary: {e}")

    article_path = output_dir / "article.md"
    article_path.write_text(processed_markdown)

    if not any(assets_dir.iterdir()):
        assets_dir.rmdir()
        print("No images downloaded - removed empty assets folder")

    print(f"\nSuccess! Article saved to: {article_path.resolve()}")


if __name__ == "__main__":
    main()
