---
name: marp-presentation-generator
description: Create professional PowerPoint-style presentations using Marp. Generates markdown-based slides that can be exported to PDF, PPTX, or HTML. Use when users request presentations, slide decks, or visual presentations.
---

# Marp Presentation Generator

Generate professional presentations using Marp (Markdown Presentation Ecosystem). Write slides in markdown and export to PDF, PPTX, or HTML.

## Prerequisites

- `GOOGLE_API_KEY` must be set in the `.env` file
- `google-genai` Python package must be installed
- Marp CLI is required for exporting presentations (already installed globally)

To check if Marp CLI is installed:

```bash
marp --version
```

## Quick Start

When the user requests a presentation:

1. Run the generation script with the topic/outline
2. The script creates a Marp markdown file
3. Optionally export to PDF, PPTX, or HTML using Marp CLI
4. Return the file paths to the user

## Usage

Execute the script at `scripts/generate_presentation.py`:

```bash
python3 .claude/skills/marp-presentation-generator/scripts/generate_presentation.py "Topic or outline" [options]
```

### Parameters

- **topic** (required): Presentation topic or outline (can be multi-line)
- **--title**: Custom presentation title (default: derived from topic)
- **--output-dir**: Output directory (default: `presentations/`)
- **--filename**: Custom filename without extension (default: slug of title)
- **--theme**: Marp theme (default, gaia, uncover) (default: default)
- **--export**: Export format (pdf, pptx, html, none) (default: none)
- **--slides**: Number of slides to generate (default: 8-12)

### Examples

```bash
# Basic usage - generates markdown only
python3 .claude/skills/marp-presentation-generator/scripts/generate_presentation.py "AI in Healthcare"

# With custom settings and PDF export
python3 .claude/skills/marp-presentation-generator/scripts/generate_presentation.py "Quarterly Business Review" --theme gaia --export pdf --slides 15

# From outline
python3 .claude/skills/marp-presentation-generator/scripts/generate_presentation.py "
1. Introduction to Cloud Computing
2. Types of Cloud Services
3. Benefits and Challenges
4. Case Studies
5. Future Trends
" --title "Cloud Computing Overview"
```

## Marp Syntax

The generated markdown uses Marp syntax:

```markdown
---
marp: true
theme: default
paginate: true
header: 'Presentation Title'
footer: 'Your Name | Date'
---

<!-- _class: lead -->
# Main Title
## Subtitle

---

# Slide Title

- Bullet point 1
- Bullet point 2
- Bullet point 3

---

<!-- _class: lead -->
# Section Break
## New Section

---

# Two Column Layout

<div class="columns">
<div>

**Left Column**
- Point 1
- Point 2

</div>
<div>

**Right Column**
- Point 3
- Point 4

</div>
</div>
```

## Slide Structure Guidelines

Effective presentations follow this structure:

1. **Title Slide**: Title, subtitle, author, date
2. **Agenda/Overview**: What will be covered
3. **Content Slides**: Main content (3-5 points per slide max)
4. **Section Breaks**: Mark major transitions
5. **Conclusion**: Summary and call-to-action
6. **Thank You/Q&A**: Final slide

## Content Guidelines

- **One idea per slide**: Don't overcrowd
- **Use bullet points**: Max 5-7 per slide
- **Visual hierarchy**: Use headers and emphasis
- **Consistent formatting**: Maintain style throughout
- **Speaker notes**: Add presenter notes when needed

## Themes

Marp includes built-in themes:

- **default**: Clean, professional, good for business
- **gaia**: Modern, colorful, good for tech talks
- **uncover**: Minimalist, centered text, good for impact

## Exporting Presentations

After generating the markdown, export using Marp CLI:

```bash
# Export to PDF
marp presentation.md -o presentation.pdf

# Export to PowerPoint
marp presentation.md -o presentation.pptx

# Export to HTML
marp presentation.md -o presentation.html

# With custom theme
marp presentation.md --theme gaia -o presentation.pdf

# Allow local files (for images)
marp presentation.md --allow-local-files -o presentation.pdf
```

## Adding Images

Include images in slides:

```markdown
# Slide with Image

![width:600px](path/to/image.png)

Or with caption:

![bg right:40%](image.png)
Content on the left, image background on right
```

You can use the `gemini-image-generator` skill to create images for slides.

## Advanced Features

### Background Images
```markdown
<!-- _backgroundColor: #123 -->
<!-- _backgroundImage: url('image.jpg') -->
```

### Split Layouts
```markdown
![bg left:40%](image.png)
Content appears on the right side
```

### Speaker Notes
```markdown
<!--
These are speaker notes that won't appear on slides
but can be viewed in presenter mode
-->
```

## Output

- Markdown saved to: `presentations/<filename>.md`
- Exports saved to: `presentations/<filename>.[pdf|pptx|html]`
- The script prints all generated file paths

## Tips

1. Keep slides simple and visual
2. Use section breaks to organize content
3. Include images to illustrate concepts
4. Test the exported format before presenting
5. Use speaker notes for detailed talking points
