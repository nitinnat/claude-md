# Gemini Image Generation API Reference

## Overview

The `gemini-2.5-flash-image` model generates images via the `generate_content` API.

## Basic Usage

```python
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="A futuristic city at sunset",
)

for part in response.parts:
    if part.inline_data:
        image = part.as_image()
        image.save("output.png")
```

## Response Structure

The response contains `parts`, each potentially having:
- `inline_data`: Binary image data (use `.as_image()` to get PIL Image)
- `text`: Text content (if model also returns text)

## Error Handling

- **No inline_data in parts**: Prompt blocked by safety filters
- **Invalid API key**: Check GOOGLE_API_KEY
- **Rate limiting**: Implement exponential backoff

## Limitations

- Subject to content safety policies
- Rate limits apply based on API tier
