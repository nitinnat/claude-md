#!/usr/bin/env python3
"""
Generate images using Google Gemini's image generation model.

Usage:
    python generate_image.py "prompt" [--output-dir DIR] [--filename NAME]
"""

import argparse
import os
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
    project_root = script_dir.parent.parent.parent.parent

    env_paths = [project_root / ".env", Path.cwd() / ".env"]
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            break

    return os.environ.get("GOOGLE_API_KEY", "")


def generate_image(prompt: str, output_dir: str = "generated_images", filename: str | None = None) -> str:
    """
    Generate an image using Gemini's image generation model.

    Returns the path to the saved image.
    """
    api_key = load_api_key()
    if not api_key or api_key == "your-google-api-key":
        print("Error: GOOGLE_API_KEY not configured in .env file")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if filename:
        image_filename = f"{filename}.png"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"gemini_{timestamp}.png"

    full_path = output_path / image_filename

    print(f"Generating image for prompt: {prompt[:100]}...")

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=prompt,
    )

    image_saved = False
    if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                image = part.as_image()
                image.save(str(full_path))
                image_saved = True
                break

    if not image_saved:
        if hasattr(response, "text") and response.text:
            print(f"Model response: {response.text}")
        print("Error: No image was generated. The prompt may have been blocked by safety filters.")
        sys.exit(1)

    print(f"Image saved to: {full_path.resolve()}")
    return str(full_path.resolve())


def main():
    parser = argparse.ArgumentParser(description="Generate images using Gemini")
    parser.add_argument("prompt", help="Description of the image to generate")
    parser.add_argument("--output-dir", default="generated_images", help="Output directory (default: generated_images)")
    parser.add_argument("--filename", help="Custom filename without extension (default: timestamp-based)")

    args = parser.parse_args()

    generate_image(args.prompt, args.output_dir, args.filename)


if __name__ == "__main__":
    main()
