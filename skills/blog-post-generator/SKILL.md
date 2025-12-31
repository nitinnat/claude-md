---
name: blog-post-generator
description: Generate illustrated blog posts with AI-generated images. Use when users request blog post creation, article writing, or content with images. Outputs markdown with inline images.
---

# Blog Post Generator

Generate blog posts with AI-generated images. Claude writes the content, and uses the `gemini-image-generator` skill to create relevant images.

## Workflow

When the user requests a blog post:

1. Create a directory for the blog: `generated_images/blog_<topic_slug>/`
2. Write the blog content in markdown
3. For each section that needs an image:
   - Create a detailed image prompt describing the visual
   - Use the `gemini-image-generator` skill to generate the image
   - Embed the image in the markdown using relative paths
4. Save the final markdown file and return the path

## Blog Structure

Generate posts with this structure:

```markdown
# [Title]

[Introduction paragraph - hook the reader]

## [Section 1 Heading]

[Content - 2-3 paragraphs]

![Section 1 visual](image_1.png)

## [Section 2 Heading]

[Content - 2-3 paragraphs]

## [Section 3 Heading]

[Content - 2-3 paragraphs]

![Section 3 visual](image_2.png)

## Conclusion

[Wrap up and call-to-action]
```

## Image Generation

Use the `gemini-image-generator` skill for images:

```bash
python3 .claude/skills/gemini-image-generator/scripts/generate_image.py "detailed image prompt" --output-dir generated_images/blog_<slug> --filename image_1
```

### Image Prompt Guidelines

- Be specific about style: photorealistic, illustration, diagram, etc.
- Include colors, lighting, and composition details
- Describe the mood and atmosphere
- Match the tone of the blog content

Example prompts:
- "A photorealistic image of solar panels on a modern rooftop at sunset, golden hour lighting, clean energy concept"
- "A minimalist flat illustration of a developer at a standing desk with multiple monitors, soft blue and white color scheme"

## Output

- Save markdown to: `generated_images/blog_<slug>/<title-slug>.md`
- Save images to: `generated_images/blog_<slug>/image_N.png`
- Use relative paths in markdown so the blog is portable
- Return the full path to the markdown file when done
