---
name: pr-creator
description: Creates a GitHub pull request with a concise description
enabled: true
---

# PR Creator Skill

When the user asks to create a PR, follow these steps:

1. **Check git status** to see what's staged
2. **Create a commit** with a brief, clear message (no AI attribution)
3. **Push to remote** branch
4. **Create PR** using gh CLI with:
   - Brief title (under 70 characters)
   - Concise description with bullet points of key changes
   - No mention of AI/Claude/automation
   - No emojis

## Commit Message Format
```
Brief title describing the change

Bullet points of key changes:
- Change 1
- Change 2
- Change 3
```

## PR Description Format
```
Brief paragraph describing what this PR does.

Key changes:
- Change 1
- Change 2
- Change 3
```

Keep it professional and concise. Focus on what changed and why.
