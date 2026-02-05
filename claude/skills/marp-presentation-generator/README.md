# Marp Presentation Generator

AI-powered presentation generation using Marp (Markdown Presentation Ecosystem) and Google Gemini.

## Prerequisites

- `GOOGLE_API_KEY` set in `.env` file
- `google-genai` Python package installed

## Quick Start

Generate a presentation:

```bash
python3 skills/marp-presentation-generator/scripts/generate_presentation.py "AI in Healthcare" --export pdf
```

## Features

- AI-generated content using Google Gemini
- Professional slide layouts
- Multiple themes (default, gaia, uncover)
- Export to PDF, PPTX, or HTML
- Customizable number of slides
- Supports outlines and topics

## Installation

Marp CLI is already installed globally. If you need to reinstall:

```bash
npm install -g @marp-team/marp-cli
```

Install the Python dependency:

```bash
pip install google-genai
```

## Examples

### Basic presentation
```bash
python3 skills/marp-presentation-generator/scripts/generate_presentation.py "Introduction to Machine Learning"
```

### Custom theme and export
```bash
python3 skills/marp-presentation-generator/scripts/generate_presentation.py \
  "Quarterly Business Review" \
  --theme gaia \
  --export pdf \
  --slides 15
```

### From outline
```bash
python3 skills/marp-presentation-generator/scripts/generate_presentation.py "
1. Introduction to Cloud Computing
2. Types of Cloud Services (IaaS, PaaS, SaaS)
3. Benefits and Challenges
4. Real-world Case Studies
5. Future Trends and Predictions
" --title "Cloud Computing 101"
```

## Output

Files are saved to the `presentations/` directory:
- Markdown source: `presentations/<slug>.md`
- Exports: `presentations/<slug>.[pdf|pptx|html]`

## Manual Export

If you need to manually export or customize:

```bash
# Export to PDF
marp presentations/my-presentation.md -o presentations/my-presentation.pdf

# Export with custom theme
marp presentations/my-presentation.md --theme gaia -o output.pdf

# Export to PowerPoint
marp presentations/my-presentation.md -o output.pptx

# Export to HTML
marp presentations/my-presentation.md -o output.html
```

## Tips

- Keep presentations focused (8-15 slides is ideal)
- Use the `gaia` theme for tech/modern presentations
- Use the `default` theme for business/professional presentations
- The AI generates well-structured content, but you can edit the markdown afterward
- Combine with `gemini-image-generator` skill to add custom images
