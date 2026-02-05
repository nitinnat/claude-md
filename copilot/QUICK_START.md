# Quick Start Guide

Get up and running with AI-Assisted Coding in 5 minutes.

## For Presenters

### Step 1: Convert Presentation to PowerPoint

```bash
# Install Marp CLI (one time)
npm install -g @marp-team/marp-cli

# Convert to PPTX
cd copilot/
marp AI-Assisted-Coding-Presentation.md --pptx
```

**Alternative**: Use Marp VS Code extension or https://web.marp.app/

### Step 2: Review Content

- **Session 1**: Slides 1-35 (copilot-instructions.md + agents)
- **Session 2**: Slides 36-70 (prompts + workflow + security)
- Split marker in presentation: `<!-- SESSION 1 ENDS HERE -->`

### Step 3: Customize

Edit the presentation to add:
- Your contact info (last slide)
- Your team's specific examples
- Your company logo (optional)

### Step 4: Prepare Demos

Choose 1-2 live demos from PRESENTATION_SETUP.md:
- Demo copilot-instructions.md (before/after)
- Demo custom agent (@python-coder)
- Demo complete workflow on simple feature

### Step 5: Share Artifacts

After presenting, share with attendees:
- Blog post link (once published)
- Entire `copilot/` folder (ZIP it)
- Getting started checklist

## For Developers

### Step 1: Setup in Your Repository

```bash
# Create directory structure
mkdir -p .github/copilot/{agents,prompts}

# Copy instructions template
cp copilot/copilot-instructions.md .github/copilot-instructions.md

# Customize for your project
# Edit .github/copilot-instructions.md with your:
# - Project description
# - Tech stack
# - Code standards
# - File organization
```

### Step 2: Add Agents (Pick 2-3 to Start)

```bash
# Essential agents for most teams
cp copilot/agents/python-coder.agent.md .github/copilot/agents/
cp copilot/agents/python-tester.agent.md .github/copilot/agents/
cp copilot/agents/code-reviewer.agent.md .github/copilot/agents/
```

### Step 3: Add Prompts (Pick 2-3 to Start)

```bash
# Most useful prompts
cp copilot/prompts/generate-unit-tests.prompt.md .github/copilot/prompts/
cp copilot/prompts/security-review.prompt.md .github/copilot/prompts/
cp copilot/prompts/add-comprehensive-logging.prompt.md .github/copilot/prompts/
```

### Step 4: Try It Out

In VSCode Copilot Chat:

```
# Use an agent
@python-coder Write a function to validate email addresses

# Use a prompt (select code first)
/generate-unit-tests
```

### Step 5: Iterate

- Update copilot-instructions.md based on code review feedback
- Create custom agents for your team's specific needs
- Share your configurations with the team

## For Multi-Repository Teams

```bash
# Create workspace structure
workspace/
├── .github/                    # Shared config
│   ├── copilot-instructions.md
│   └── copilot/
│       ├── agents/
│       └── prompts/
├── backend/                    # Python repo
├── frontend/                   # React repo
└── infrastructure/             # K8s repo
```

VSCode automatically loads configurations from parent directories.

## Troubleshooting

**Agents not working?**
- Check file is in `.github/copilot/agents/`
- File name should be `<agent-name>.agent.md`
- Restart VSCode

**Prompts not found?**
- Check file is in `.github/copilot/prompts/`
- File extension must be `.prompt.md`
- Reload VSCode window

**Instructions not followed?**
- File must be exactly `.github/copilot-instructions.md`
- In repository root's `.github/` folder
- Reload VSCode

## Resources

- **Complete Guide**: See `content/posts/ai-assisted-coding-workflow.md`
- **Setup Guide**: See `copilot/README.md`
- **Presentation Guide**: See `copilot/PRESENTATION_SETUP.md`
- **All Artifacts**: See `copilot/ARTIFACTS_SUMMARY.md`

## Getting Help

1. Read the full blog post for detailed explanations
2. Check README.md for setup instructions
3. Review example agents and prompts
4. Start small and iterate

**Key Insight**: Be explicit. AI needs direct instructions, not suggestions.
