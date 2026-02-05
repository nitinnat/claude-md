#!/usr/bin/env python3
"""
Generate Marp presentations using AI.

Usage:
    python generate_presentation.py "topic" [options]
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv package not installed. Run: pip install python-dotenv")
    sys.exit(1)

try:
    from google import genai
except ImportError:
    print("Error: google-genai package not installed. Run: pip install google-genai")
    sys.exit(1)


def load_api_key() -> str:
    """Load GOOGLE_API_KEY from .env file."""
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent.parent.parent

    env_paths = [project_root / ".env", Path.cwd() / ".env"]
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            break

    return os.environ.get("GOOGLE_API_KEY", "")


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text[:50]


def generate_presentation_content(
    topic: str, title: str | None, theme: str, num_slides: int, api_key: str
) -> tuple[str, str]:
    """
    Generate presentation content using Gemini.

    Returns (markdown_content, extracted_title)
    """
    client = genai.Client(api_key=api_key)

    prompt = f"""Generate a professional presentation about: {topic}

Requirements:
- Create {num_slides} slides (including title and conclusion)
- Use Marp markdown syntax
- Theme: {theme}
- Include proper formatting with headers, bullet points, and structure
- Make slides visually balanced (3-5 points per slide max)
- Include section breaks between major topics
- Add a title slide, agenda, content slides, and conclusion
- Keep text concise and impactful
{f"- Use this title: {title}" if title else "- Create an engaging title"}

Format using Marp syntax:
- Start with frontmatter (marp: true, theme, paginate, etc.)
- Use `---` to separate slides
- Use `<!-- _class: lead -->` for title and section slides
- Keep content clear and professional

Generate the complete presentation markdown now."""

    print("Generating presentation content...")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    content = response.text

    if title:
        extracted_title = title
    else:
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        extracted_title = title_match.group(1) if title_match else "Presentation"

    return content, extracted_title


def save_presentation(
    content: str, output_dir: str, filename: str | None, title: str
) -> Path:
    """Save presentation markdown file."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not filename:
        filename = slugify(title)

    md_path = output_path / f"{filename}.md"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Markdown saved to: {md_path.resolve()}")
    return md_path


def export_presentation(md_path: Path, export_format: str, theme: str) -> Path | None:
    """Export presentation using Marp CLI."""
    if export_format == "none":
        return None

    output_path = md_path.with_suffix(f".{export_format}")

    marp_available = subprocess.run(
        ["which", "marp"], capture_output=True
    ).returncode == 0

    if marp_available:
        marp_cmd = ["marp"]
    else:
        marp_cmd = ["npx", "@marp-team/marp-cli@latest"]

    if theme != "default":
        marp_cmd.extend(["--theme", theme])

    marp_cmd.extend([str(md_path), "-o", str(output_path), "--allow-local-files"])

    print(f"Exporting to {export_format.upper()}...")

    try:
        result = subprocess.run(
            marp_cmd,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Exported to: {output_path.resolve()}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Warning: Export failed. {e.stderr}")
        print("You can manually export using:")
        print(f"  marp {md_path} -o {output_path}")
        return None
    except FileNotFoundError:
        print("Warning: marp not found. Install it with: npm install -g @marp-team/marp-cli")
        print(f"Or manually export using: marp {md_path} -o {output_path}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate Marp presentations using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("topic", help="Presentation topic or outline")
    parser.add_argument("--title", help="Custom presentation title")
    parser.add_argument(
        "--output-dir", default="presentations", help="Output directory (default: presentations)"
    )
    parser.add_argument(
        "--filename", help="Custom filename without extension (default: slug of title)"
    )
    parser.add_argument(
        "--theme",
        choices=["default", "gaia", "uncover"],
        default="default",
        help="Marp theme (default: default)"
    )
    parser.add_argument(
        "--export",
        choices=["pdf", "pptx", "html", "none"],
        default="none",
        help="Export format (default: none)"
    )
    parser.add_argument(
        "--slides",
        type=int,
        default=10,
        help="Number of slides to generate (default: 10)"
    )

    args = parser.parse_args()

    api_key = load_api_key()
    if not api_key:
        print("Error: GOOGLE_API_KEY not configured in .env file")
        sys.exit(1)

    content, extracted_title = generate_presentation_content(
        args.topic, args.title, args.theme, args.slides, api_key
    )

    md_path = save_presentation(
        content, args.output_dir, args.filename, extracted_title
    )

    if args.export != "none":
        export_presentation(md_path, args.export, args.theme)

    print("\nPresentation generated successfully!")
    print(f"Markdown: {md_path.resolve()}")


if __name__ == "__main__":
    main()
