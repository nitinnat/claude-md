# Presentation Setup Guide

This guide explains how to convert the Marp markdown presentation to PowerPoint format.

## Converting to PowerPoint

The presentation is written in Marp format (`AI-Assisted-Coding-Presentation.md`), which can be converted to PPTX using Marp CLI.

### Option 1: Using Marp CLI (Recommended)

1. **Install Marp CLI**:
   ```bash
   npm install -g @marp-team/marp-cli
   ```

2. **Convert to PowerPoint**:
   ```bash
   cd copilot/
   marp AI-Assisted-Coding-Presentation.md --pptx
   ```

   This creates `AI-Assisted-Coding-Presentation.pptx` in the same directory.

3. **With custom output name**:
   ```bash
   marp AI-Assisted-Coding-Presentation.md --pptx -o "My-Presentation.pptx"
   ```

### Option 2: Using Marp VS Code Extension

1. **Install Extension**:
   - Open VS Code
   - Search for "Marp for VS Code" in Extensions
   - Install the extension

2. **Convert**:
   - Open `AI-Assisted-Coding-Presentation.md` in VS Code
   - Click the Marp icon in the editor toolbar
   - Select "Export Slide Deck..."
   - Choose "PowerPoint (.pptx)"

### Option 3: Using Marp Web (No Installation)

1. Go to https://web.marp.app/
2. Copy the contents of `AI-Assisted-Coding-Presentation.md`
3. Paste into the editor
4. Click "Export" → "PowerPoint (.pptx)"

## Presentation Structure

The presentation is designed for **two 30-minute sessions**:

### Session 1 (Slides 1-35, ~30 minutes)
- Introduction and problem statement
- Foundation: copilot-instructions.md
- Part 2: Specialized Agents
- Covers theory and setup

**Split marker**: Look for the comment `<!-- SESSION 1 ENDS HERE -->`

### Session 2 (Slides 36-70, ~30 minutes)
- Part 3: Reusable Prompts
- Part 4: Security Best Practices
- Part 5: Managing Token Limits
- Part 6: Complete Workflow
- Part 7: Multi-Repository Setup
- Covers practical application and workflows

## Customization

Before presenting, customize:

1. **Contact Information** (last slide):
   - Update `[Your contact information]`
   - Add links to your blog, GitHub, etc.

2. **Branding** (optional):
   - Add company logo by editing theme settings
   - Modify color scheme in the frontmatter

3. **Examples** (optional):
   - Replace generic examples with your team's actual use cases
   - Add screenshots from your projects

## Tips for Presenting

### Session 1 Tips:
- **Start with the problem**: Most developers relate to AI inconsistency
- **Demo copilot-instructions.md**: Show before/after with real Copilot
- **Keep it interactive**: Ask attendees about their AI experiences
- **Emphasize "be opinionated"**: This is the key insight for instructions

### Session 2 Tips:
- **Live demo the workflow**: Use a simple feature as example
- **Show real code**: More impactful than slides
- **Security section is critical**: Don't rush this
- **End with actionable steps**: The getting started checklist

### Live Demo Suggestions:

1. **Demo copilot-instructions.md** (Session 1):
   - Show Copilot generating code without instructions (messy)
   - Add copilot-instructions.md with clear standards
   - Show same prompt now producing clean, standardized code

2. **Demo custom agent** (Session 1):
   - Show `@python-coder` generating a simple function
   - Compare to generic Copilot response
   - Highlight how it follows project conventions

3. **Demo complete workflow** (Session 2):
   - Pick a small feature (e.g., "add input validation to a function")
   - Walk through: plan → implement → test → review → security
   - Show how each agent/prompt builds on the previous step

4. **Demo implementation log** (Session 2):
   - Show a real IMPLEMENTATION_LOG.md from your project
   - Demonstrate starting new session with log as context
   - Show how it maintains continuity

## Additional Resources to Share

After the presentation, share with attendees:

1. **Blog Post**: `content/posts/ai-assisted-coding-workflow.md`
   - Complete written guide with all details
   - Links to resources and further reading

2. **Copilot Folder**: `copilot/` directory contents
   - Sample copilot-instructions.md
   - All custom agents
   - All custom prompts
   - README with setup instructions

3. **Getting Started Checklist**:
   ```markdown
   - [ ] Create .github/copilot-instructions.md
   - [ ] Add project overview and tech stack
   - [ ] Define code standards and security guidelines
   - [ ] Copy 2-3 agents relevant to your work
   - [ ] Copy 2-3 prompts you'll use frequently
   - [ ] Try the workflow on a small task
   - [ ] Share with your team and iterate
   ```

## Troubleshooting

### Marp CLI Installation Issues

**On macOS**:
```bash
# If npm global install fails, try using npx
npx @marp-team/marp-cli@latest AI-Assisted-Coding-Presentation.md --pptx
```

**On Windows**:
```powershell
# Use PowerShell as administrator
npm install -g @marp-team/marp-cli
```

**Alternative - Use Docker**:
```bash
docker run --rm -v $PWD:/home/marp/app/ marpteam/marp-cli AI-Assisted-Coding-Presentation.md --pptx
```

### Presentation Not Rendering Correctly

- **Images missing**: Ensure you've generated the diagrams first
- **Formatting issues**: Check that all code blocks are properly closed
- **Slides too long**: Marp auto-adjusts, but you can add `<!-- fit -->` to shrink text

### Converting to PDF Instead

```bash
marp AI-Assisted-Coding-Presentation.md --pdf
```

## Questions and Feedback

After the presentation, collect feedback:
- What resonated most?
- What needs more explanation?
- What real-world challenges do attendees face?
- What additional agents/prompts would be useful?

Use this feedback to refine the artifacts and create team-specific versions.
