---
name: gemini-image-generator
description: Generate images using Google Gemini's Imagen model. Use when users request image creation, visual content generation, or ask to create pictures/graphics. Requires GOOGLE_API_KEY in .env file.
---

# Gemini Image Generator

Generate images using Google's Gemini API with the gemini-3-pro-image-preview model.

## Prerequisites

- `GOOGLE_API_KEY` must be set in the `.env` file
- The `google-genai` Python package must be installed

## Quick Start

When the user requests an image:

1. Run the generation script with the user's prompt
2. Images are saved to `generated_images/` in the project root
3. Return the file path to the user

## Usage

Execute the script at `scripts/generate_image.py`:

```bash
python3 .claude/skills/gemini-image-generator/scripts/generate_image.py "A detailed description of the image"
```

### Parameters

The script accepts:
- **prompt** (required): Detailed description of the image to generate
- **--output-dir**: Custom output directory (default: `generated_images/`)
- **--filename**: Custom filename without extension (default: timestamp-based)

### Examples

```bash
# Basic usage
python3 .claude/skills/gemini-image-generator/scripts/generate_image.py "A serene mountain landscape at sunset"

# Custom output location
python3 .claude/skills/gemini-image-generator/scripts/generate_image.py "A futuristic cityscape" --output-dir ./my_images

# Custom filename
python3 .claude/skills/gemini-image-generator/scripts/generate_image.py "A red sports car" --filename sports_car
```

## Prompt Guidelines

For best results, prioritize **technical accuracy and informational value** over pure aesthetics:

1. **Be factual and specific**: Focus on conveying information clearly rather than artistic flair
2. **Use diagram-style prompts**: For technical content, describe layouts, labels, arrows, and data flow
3. **Specify format**: Flowchart, architecture diagram, comparison chart, infographic, etc.
4. **Include text labels**: Specify what text should appear in the image
5. **Keep backgrounds clean**: White or light backgrounds for diagrams and technical illustrations

### Good Prompt Examples for Technical Content

- "A clean architecture diagram on white background showing three horizontal layers: 'Frontend' with React icon at top, 'Backend' with Python/FastAPI in middle, 'Database' with PostgreSQL and Redis icons at bottom. Arrows showing data flow between layers. Flat design, blue and gray colors."
- "A comparison infographic with two columns: left column labeled 'Before' showing 5 manual steps in red boxes, right column labeled 'After' showing single automated step in green. Clean professional style."
- "A workflow diagram showing 4 connected boxes from left to right: 'Input' -> 'Processing' -> 'Validation' -> 'Output'. Each box contains a small icon and label. Horizontal layout, minimal style, white background."

### Aesthetic Prompts (use sparingly)

- "A photorealistic image of a golden retriever puppy playing in autumn leaves, warm afternoon lighting"
- "An oil painting style landscape of rolling hills with a small cottage, dramatic cloudy sky"

## Output

- Images are saved as PNG files
- Default location: `generated_images/` in project root
- Filename format: `gemini_<timestamp>.png` or custom name
- The script prints the full path of the saved image

## Error Handling

The script will display clear error messages for:
- Missing API key
- Invalid prompts (safety filters)
- Network issues
- File system errors
