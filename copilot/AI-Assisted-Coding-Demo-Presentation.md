---
marp: true
theme: default
paginate: true
footer: "AI-Assisted Coding with GitHub Copilot | Demo Presentation"
---

<!--
Demo-Focused Presentation
Switch between slides and IDE for live demonstrations
Minimal text - just talking points
Each section: Explain concept → Demo in IDE → Move to next section
-->

# AI-Assisted Coding
## A Practical Demo

**Using GitHub Copilot Systematically**

---

# The Problem

- 🔄 Re-explaining standards every session
- 🐠 AI forgets context after 30 minutes
- 🎲 Inconsistent, unpredictable results
- ⚠️ Security risks from unclear guidance
- 📉 Token limits destroy continuity

**Root cause: Treating AI like magic instead of a team member**

---

# The Solution

Treat AI like a new engineer:

1. **Onboarding** - Clear written instructions
2. **Specialization** - Different roles for different tasks
3. **Reusable processes** - Encoded patterns
4. **Continuity** - Session-to-session memory

---

![Copilot architecture showing instructions at top, agents in middle, prompts at bottom](/assets/copilot_architecture.png)

---

# Part 1: The Foundation

![Impact of clear instructions showing difference between chaos and organization](/assets/instructions_impact.png)

---

## copilot-instructions.md

```
.github/
└── copilot-instructions.md
```

**What it does:**
- Automatically loads every Copilot chat
- Explains your project, tech stack, standards
- Enforces security, code style, best practices
- Provides context immediately

**Result:** First chat feels like continuing from yesterday

---

# Demo: Show copilot-instructions.md in IDE

**Show in IDE:**
1. Open `.github/copilot-instructions.md` in editor
2. Show the file structure
3. Highlight key sections:
   - Project overview
   - Tech stack
   - Code standards
   - Security guidelines
   - File organization

**Then:** Ask Copilot to write code without vs with instructions loaded

---

# What Goes in copilot-instructions.md

## Must Include:
- **Project overview** - What does this repo do?
- **Tech stack** - Languages, frameworks, tools
- **Code style** - PEP 8, type hints, docstrings
- **Domain practices** - PySpark, Kubernetes, etc.
- **Security rules** - Non-negotiable constraints
- **File organization** - Where things go

---

# copilot-instructions.md Template

```markdown
## Project Overview
Real-time data pipeline. 10M+ events/day via Kafka, Spark, BigQuery.

## Tech Stack
- Python 3.11+, PySpark 3.4
- GCP, BigQuery, Cloud Storage
- Kubernetes 1.28+, pytest

## Code Standards
- PEP 8, type hints required
- Google-style docstrings
- Specific exceptions, no bare except
- 100 char line limit, black formatting

## PySpark Best Practices
- No .collect() on large DataFrames
- Partition before joins
- Cache only when reused

## Kubernetes
- Always specify resource limits
- Include health probes
- Use ConfigMaps, Secrets

## Security - NON-NEGOTIABLE
- NEVER hardcode credentials
- ALWAYS validate inputs
- Use environment variables
```

---

# Key Principle: Be Explicit

❌ "Prefer type hints"
✅ "Use type hints for ALL function signatures"

❌ "Good error handling"
✅ "Use specific exception types, never bare except"

**Directives work better than suggestions**

---

# Part 2: Specialized Agents

## Why Agents?

Different tasks, different expertise:
- Writing code ≠ Testing code
- Planning ≠ Implementing
- Coding ≠ Reviewing
- Implementing ≠ Documenting

---

# Available Agents

1. **@python-coder** - Write production Python code
2. **@python-tester** - Generate pytest test suites
3. **@kubernetes-expert** - Create K8s manifests
4. **@task-planner** - Plan implementations
5. **@code-reviewer** - Review for issues
6. **@readme-generator** - Create documentation
7. **@pr-description-generator** - Write PR descriptions

---

# Demo: @python-coder Agent

**In Copilot Chat, type:**
```
@python-coder Write a function to validate customer emails.
Include type hints, error handling, and logging.
```

**Show:**
- Clean, typed function
- Proper error handling
- Structured logging
- Follows project standards automatically

---

# Demo: @python-tester Agent

**In Copilot Chat, type:**
```
@python-tester Generate unit tests for the email validation function.
Include edge cases, parametrization, and mocked dependencies.
```

**Show:**
- Comprehensive test suite
- Fixtures for setup
- Parametrized tests
- Proper mocking

---

# Demo: @task-planner Agent

**In Copilot Chat, type:**
```
@task-planner Create a plan for adding rate limiting to our API.
Requirements: 100 req/min per API key, return 429 when exceeded.
```

**Show:**
- Requirements analysis
- Technical approach
- Step-by-step implementation
- Testing strategy
- Risk assessment

---

# Demo: @code-reviewer Agent

**In Copilot Chat, type:**
```
@code-reviewer Review this function for issues, security, and performance.
```

**Then paste/select code**

**Show:**
- Categorized feedback (CRITICAL, IMPORTANT, MINOR)
- Specific line references
- Concrete suggestions

---

# Part 3: Reusable Prompts

## What Are Prompts?

Quick transformations on selected code.

![How to use prompts: select code, open chat, type prompt](/assets/demo_workflow_steps.png)

---

# Prompt 1: /generate-unit-tests

Select your function code, then:
```
/generate-unit-tests
```

**Shows:**
- AAA pattern (Arrange-Act-Assert)
- Pytest fixtures
- Parametrized tests
- Edge cases
- Mock dependencies

---

# Demo: /generate-unit-tests

**In IDE:**
1. Select the `validate_email()` function
2. Open Copilot Chat
3. Type `/generate-unit-tests`
4. Show generated test suite

---

# Prompt 2: /optimize-pyspark

Select PySpark code, then:
```
/optimize-pyspark
```

**Suggests:**
- Partitioning strategies
- Caching optimization
- Broadcast joins
- Column pruning
- Filter placement

---

# Prompt 3: /add-comprehensive-logging

Select code, then:
```
/add-comprehensive-logging
```

**Adds:**
- Function entry/exit logs
- State transition logs
- Error context logging
- Appropriate log levels

---

# Prompt 4: /security-review

Select code, then:
```
/security-review
```

**Checks for:**
- SQL injection
- Hardcoded credentials
- Input validation gaps
- Permission issues
- Vulnerable dependencies

**Always run before committing**

---

# Prompt 5: /refactor-for-testability

Select code, then:
```
/refactor-for-testability
```

**Improves:**
- Dependency injection
- Pure vs impure separation
- Function granularity
- Explicit dependencies

---

# Demo: /security-review

**In IDE:**
1. Select the database query function
2. Open Copilot Chat
3. Type `/security-review`
4. Show vulnerability detection

---

# Part 4: Security First

## Non-Negotiable Rules

```
NEVER hardcode credentials
ALWAYS validate inputs
ALWAYS use parameterized queries
ALWAYS use environment variables
```

---

# Security in Practice

**Before every commit:**

```
/security-review
```

**Check for:**
- ❌ Hardcoded secrets
- ❌ SQL injection
- ❌ Missing validation
- ❌ Exposed errors
- ❌ PII in logs

---

# Demo: Security Vulnerability

**In IDE:**
1. Show a vulnerable query (SQL injection)
2. Run `/security-review`
3. Show detected vulnerability
4. Show recommended fix

---

# Part 5: Complete Workflow

## From Idea to Production

---

![Complete AI-assisted coding workflow showing 7 phases in circular flow](/assets/ai_coding_workflow.png)

---

# Workflow Phase 1: Planning

```
@task-planner Implement rate limiting for our API.
Requirements: 100 req/min per API key, return 429 when exceeded.
```

**Output:** Implementation plan

---

# Workflow Phase 2: Implementation

```
@python-coder Implement the rate limiter.
Use Redis sliding window. Include type hints, error handling, logging.
```

**Output:** Production-ready code

---

# Workflow Phase 3: Testing

**Select code, then:**
```
/generate-unit-tests
```

**Output:** Comprehensive test suite

---

# Workflow Phase 4: Optimization

**For PySpark:**
```
/optimize-pyspark
```

**For general code:**
```
/refactor-for-testability
```

---

# Workflow Phase 5: Logging

```
/add-comprehensive-logging
```

**Output:** Structured logging at all critical points

---

# Workflow Phase 6: Security

```
/security-review
```

**Output:** Identified vulnerabilities

---

# Workflow Phase 7: Code Review

```
@code-reviewer Review this implementation.
```

**Output:** Categorized feedback

---

# Complete Workflow Demo

**In IDE:**
1. Show entire workflow on a small feature
2. Each step in sequence
3. Show how each builds on previous
4. Final result: Production-ready, tested, secure code

---

# Part 6: Handling Context

## The Token Limit Problem

Long projects lose context:
- Conversations exceed limits
- AI summarizes history
- Details lost
- Next session: start over

**Solution: IMPLEMENTATION_LOG.md**

---

![Implementation log workflow showing phases from planning through next steps](/assets/implementation_log_workflow.png)

---

# IMPLEMENTATION_LOG.md

```
project/
├── .github/copilot-instructions.md
├── IMPLEMENTATION_LOG.md          ← Add this
├── src/
└── tests/
```

**Tracks:**
- Planning decisions
- Implementation status
- Code locations
- Issues found and fixed
- What's next

---

# Using the Log

When starting new session:

```
Read IMPLEMENTATION_LOG.md and continue from where we left off.
We completed planning, implementation, and testing.
Next: create monitoring dashboard.
```

**Result:** Full context without conversation history

---

# Part 7: Multi-Repository Teams

## Shared Workspace Setup

```
workspace/
├── .github/
│   ├── copilot-instructions.md    ← Shared
│   └── copilot/
│       ├── agents/                ← Shared
│       └── prompts/               ← Shared
├── backend/                       ← Python
├── frontend/                      ← React
└── infrastructure/                ← K8s
```

VSCode loads from parent directories automatically.

---

# Shared vs Repository-Specific

**Shared (workspace/.github/):**
- Core principles
- Security guidelines
- General agents & prompts

**Repository-specific (.github/):**
- Tech stack details
- File organization
- Language-specific standards

---

# Getting Started

## Week 1:

- [ ] Create `.github/copilot-instructions.md`
- [ ] Copy agents to `.github/copilot/agents/`
- [ ] Copy prompts to `.github/copilot/prompts/`
- [ ] Customize for your project
- [ ] Reload VSCode

## Week 2:

- [ ] Test agents and prompts
- [ ] Train team
- [ ] Iterate based on feedback

---

# Key Takeaway

Not about bigger AI.

**About systematic structure:**
- Clear onboarding (instructions)
- Role specialization (agents)
- Reusable patterns (prompts)
- Context continuity (logs)

---

# Demo Summary

**What we showed:**

1. ✅ copilot-instructions.md foundation
2. ✅ @python-coder agent generating code
3. ✅ @python-tester generating tests
4. ✅ /generate-unit-tests prompt
5. ✅ /security-review finding vulnerabilities
6. ✅ Complete workflow end-to-end
7. ✅ IMPLEMENTATION_LOG for continuity

---

# Next Steps

1. **Copy the complete guide** - AI-ASSISTED-CODING-COMPLETE-GUIDE.md
2. **Set up your repo** - Follow getting started checklist
3. **Start small** - Try one agent, one prompt
4. **Iterate** - Update instructions as you learn
5. **Scale** - Share with team, create custom agents/prompts

---

# Resources

- **Complete Guide**: AI-ASSISTED-CODING-COMPLETE-GUIDE.md
- **GitHub Copilot Docs**: https://docs.github.com/en/copilot
- **Custom Agents**: https://code.visualstudio.com/docs/copilot/customization/custom-agents
- **Awesome Copilot**: https://github.com/github/awesome-copilot

---

# Questions?

**Key Insight:**
Treat AI like a team member. Give it clear onboarding, assign specialized roles, create reusable processes, maintain context.

That's it. That's the entire system.

---

# Thank You

Let's build better software faster.

---
