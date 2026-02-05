# Presenter's Guide: AI-Assisted Coding Demo

Complete guide for running the demonstration with all materials.

---

## Before the Presentation

### Setup (30 minutes before)

1. **Test everything**
   - [ ] VSCode open with demo project
   - [ ] GitHub Copilot Chat working
   - [ ] All sample code ready in editor tabs
   - [ ] Presentation loaded (AI-Assisted-Coding-Demo-Presentation.md)
   - [ ] DEMO-SAMPLE-CODE.md open for reference
   - [ ] Monitor/dual screen setup working

2. **Prepare your demo project**
   ```bash
   mkdir demo-copilot-project
   cd demo-copilot-project
   mkdir .github/copilot/{agents,prompts}
   cp ../copilot-instructions.md .github/
   code .
   ```

3. **Pre-populate sample code**
   - validator.py with email validation example
   - pricing.py with calculate_discount example
   - Any other examples from DEMO-SAMPLE-CODE.md

4. **Verify Copilot Chat**
   - Open Copilot Chat (Cmd+Shift+I)
   - Test a simple prompt to ensure connection works
   - Close chat, ready to go

---

## During the Presentation

### Overall Flow

```
Total Time: 60 minutes

5 min  - Opening + Problem (Slides)
5 min  - Foundation concept (Slides)
5 min  - IDE Demo: Show copilot-instructions.md
10 min - Agents concept (Slides)
15 min - IDE Demos: 3 agents × 5 min
10 min - Prompts concept (Slides)
10 min - IDE Demos: 2 prompts × 5 min
5 min  - Security (Slides)
5 min  - IDE Demo: /security-review
5 min  - Workflow (Slides)
10 min - IDE Demo: Complete workflow
3 min  - Context/Log (Slides)
5 min  - Multi-repo (Slides)
5 min  - Getting started (Slides)
7 min  - Q&A
```

---

## Detailed Section Guide

### Section 1: Opening (5 min)

**Slide:** The Problem

**What to say:**
- "How many of you use Copilot?"
- "Hands up if you've re-explained your coding standards to Copilot multiple times?"
- "Or noticed it forgets what you told it 30 minutes ago?"
- "That's the 'Goldfish Problem' - and today we're going to fix it"

**Transition:**
- "The solution isn't a bigger AI. It's systematic structure."
- "Let me show you how."

---

### Section 2: Foundation (5 min)

**Slide:** Part 1 - The Foundation

**What to say:**
- "Start with one file: copilot-instructions.md"
- "This is your AI's onboarding document"
- "You put it in .github/ and it automatically loads for every Copilot chat"
- "It contains: your project overview, tech stack, coding standards, security rules"

**Key insight:**
- "Instead of re-explaining everything, the AI reads your onboarding"
- "First chat feels like continuing from yesterday"

**Transition:** "Let me show you what this looks like..."

---

### Section 3: IDE Demo - copilot-instructions.md (5 min)

**In IDE:**

1. Show folder structure
   ```
   .github/
   └── copilot-instructions.md
   ```

2. Open the file
   - Scroll through sections:
     - Project Overview (2 sec)
     - Tech Stack (2 sec)
     - Code Standards (3 sec)
     - Security Rules (2 sec)

3. Point out key elements:
   - "Notice it's very specific - 'use type hints for ALL functions'"
   - "Not 'prefer type hints' - we're being directive"
   - "This is how you teach the AI your standards"

4. Close file

**Back to presentation**

---

### Section 4: Agents Concept (10 min)

**Slide:** Part 2 - Specialized Agents

**What to say:**
- "Different tasks need different expertise"
- "You wouldn't ask a code reviewer to plan architecture"
- "You wouldn't ask a tester to write production code"
- "So we create specialized agents"

**Agents available:**
- Go through each agent, 2 sentences each:
  - @python-coder - Write production code
  - @python-tester - Generate test suites
  - @kubernetes-expert - Create K8s configs
  - @task-planner - Plan implementations
  - @code-reviewer - Review for issues
  - @readme-generator - Create docs
  - @pr-description-generator - Write PRs

**Key point:**
- "Usage is simple: @agent-name [your request]"
- "The agent knows your standards from copilot-instructions.md"
- "So it generates code that fits your project immediately"

**Transition:** "Let's see this in action..."

---

### Section 5: IDE Demos - Agents (15 min, 5 min each)

#### Demo 1: @python-coder (5 min)

1. Show slide "Demo: @python-coder Agent"
2. Switch to IDE
3. Open Copilot Chat
4. Type:
   ```
   @python-coder Write a function to validate customer email addresses.
   Include type hints, error handling, logging, and support for
   both standard emails and + addressing.
   ```
5. Show the generated code
6. Point out:
   - Type hints ✅
   - Docstring with example ✅
   - Error handling ✅
   - Logging ✅
   - Security (email masking) ✅
7. Back to presentation

**What to say:**
- "Notice the code follows our standards immediately"
- "Type hints, docstring, error handling, logging"
- "No explanation needed - the agent knows what good looks like"

#### Demo 2: @python-tester (5 min)

1. Show slide "Demo: @python-tester Agent"
2. In IDE, show the validate_email function (already there)
3. Open Copilot Chat
4. Type:
   ```
   @python-tester Generate unit tests for the validate_email function.
   Include edge cases, parametrization, and mocked dependencies.
   ```
5. Show generated tests
6. Point out:
   - Parametrized tests ✅
   - Edge cases ✅
   - Descriptive names ✅
   - Fixtures ✅
7. Back to presentation

#### Demo 3: @code-reviewer (5 min)

1. Show slide "Demo: @code-reviewer Agent"
2. In IDE, paste vulnerable code from DEMO-SAMPLE-CODE.md:
   ```python
   def process_orders(orders_data):
       total = 0
       for order in orders_data:
           try:
               amount = order['amount']
           except:
               print("Error in order")
               continue
           total = total + amount
       return total
   ```
3. Select code, open Copilot Chat
4. Type:
   ```
   @code-reviewer Review this code for issues, security, and improvements.
   ```
5. Show feedback
6. Point out:
   - CRITICAL issues flagged ✅
   - Specific line references ✅
   - Concrete suggestions ✅
7. Back to presentation

**Timing tips:**
- Show output immediately (don't wait)
- Scroll through the full response
- Point out 2-3 key insights per demo
- Keep moving to stay on schedule

---

### Section 6: Prompts Concept (10 min)

**Slide:** Part 3 - Reusable Prompts

**What to say:**
- "For quick transformations, we have prompts"
- "Select code → Open Chat → Type /<prompt-name>"
- "These are templates for common tasks"

**Available prompts:**
- `/generate-unit-tests` - Create test suites
- `/optimize-pyspark` - Performance tuning
- `/add-comprehensive-logging` - Add logging
- `/refactor-for-testability` - Dependency injection
- `/security-review` - Find vulnerabilities

**Key point:**
- "Prompts are faster than agents for focused tasks"
- "But they do the same thing: transform code to your standards"

---

### Section 7: IDE Demos - Prompts (10 min, 5 min each)

#### Demo 1: /generate-unit-tests (5 min)

1. Show slide "Prompt 1: /generate-unit-tests"
2. In IDE, paste calculate_discount function
3. Select the entire function
4. Open Copilot Chat
5. Type: `/generate-unit-tests`
6. Show output
7. Point out:
   - Parametrized tests ✅
   - Edge cases ✅
   - Error conditions ✅
8. Back to presentation

#### Demo 2: /security-review (5 min)

1. Show slide "Prompt 5: /security-review"
2. In IDE, paste vulnerable code (SQL injection + hardcoded credentials)
3. Select all
4. Open Copilot Chat
5. Type: `/security-review`
6. Show output
7. Point out:
   - CRITICAL issues ✅
   - IMPORTANT issues ✅
   - Concrete fixes ✅
8. Back to presentation

**What to say:**
- "Always run this before committing code"
- "Catches issues that code review might miss"

---

### Section 8: Security (5 min)

**Slide:** Part 4 - Security First

**What to say:**
- "Security isn't optional"
- "It's in your copilot-instructions.md as non-negotiable rules"
- "Before every commit: /security-review"

**Rules to emphasize:**
- Never hardcode credentials
- Always validate inputs
- Always use parameterized queries
- Always use environment variables

---

### Section 9: Complete Workflow (10 min, IDE demo)

**Slide:** Part 5 - Complete Workflow

**What to say:**
- "Now let's see everything together"
- "From idea to production in a systematic way"

**In IDE: Show the workflow (quick version)**

1. Task Planner (1 min)
   ```
   @task-planner Create a plan for adding email validation to signup form.
   Requirements: validate format, check for disposable emails, send verification.
   ```
   - Show it generates a plan

2. Python Coder (1 min)
   ```
   @python-coder Implement email validation based on the plan.
   ```
   - Show generated code

3. Test Generation (1 min)
   - Select code, `/generate-unit-tests`
   - Show tests

4. Logging (1 min)
   - Select code, `/add-comprehensive-logging`
   - Show logging added

5. Security (1 min)
   - Select code, `/security-review`
   - Show no issues

6. Code Review (1 min)
   - `@code-reviewer Review this implementation`
   - Show feedback

7. Documentation (1 min)
   ```
   @readme-generator Update docs for email validation feature
   ```
   - Show docs generated

**What to say:**
- "Each step builds on the previous"
- "From plan to production-ready code"
- "All following our standards automatically"

---

### Section 10: Context Management (3 min)

**Slide:** Part 5 - Managing Context

**What to say:**
- "Long projects exceed token limits"
- "Solution: IMPLEMENTATION_LOG.md"
- "Tracks what you've done, decisions made, code locations"
- "Next session: read the log, continue where you left off"

**No IDE demo needed - concept is simple**

---

### Section 11: Multi-Repository (5 min)

**Slide:** Part 7 - Multi-Repository Teams

**What to say:**
- "If you work across multiple repos..."
- "...put shared config in workspace parent directory"
- "Each repo inherits shared standards"
- "Can override for repo-specific needs"

**Structure to show:**
```
workspace/
├── .github/                    ← Shared
│   ├── copilot-instructions.md
│   └── copilot/
│       ├── agents/
│       └── prompts/
├── backend/                    ← Inherits shared
├── frontend/                   ← Inherits shared
└── infrastructure/             ← Inherits shared
```

---

### Section 12: Getting Started (5 min)

**Slide:** Getting Started Checklist

**What to say:**
- "Ready to try this?"
- "Week 1: Set up your repo"
- "Week 2: Try it on a small task"
- "Iterate: Update instructions as you learn"

**Call to action:**
- "I'm sharing all materials with you"
- "Complete guide, sample code, templates"
- "Questions?"

---

### Section 13: Q&A (7 min)

**Common questions to prepare for:**

Q: "Does this work with other LLMs?"
A: "Copilot in VSCode specifically, but principles apply to others"

Q: "How often do you update instructions?"
A: "After code reviews catch patterns, after incidents, when adopting new tech"

Q: "What if Copilot doesn't follow the instructions?"
A: "Be more explicit, give examples, test with different wording"

Q: "How long to see productivity improvement?"
A: "Week 1: learning curve, Week 2-3: noticeable improvement, Month 1: significant"

Q: "Does this replace code review?"
A: "No, it enhances it - Copilot follows your standards, humans verify logic"

---

## Materials Checklist

### Files You Have

- ✅ `AI-Assisted-Coding-Demo-Presentation.md` - Slides (minimal text, demo-focused)
- ✅ `DEMO-SAMPLE-CODE.md` - All code examples for IDE
- ✅ `AI-ASSISTED-CODING-COMPLETE-GUIDE.md` - Full reference guide for team
- ✅ `copilot-instructions.md` - Template they can customize
- ✅ Agents directory with 7 agent files
- ✅ Prompts directory with 5 prompt files
- ✅ Generated diagrams:
  - `copilot_architecture.png`
  - `ai_coding_workflow.png`
  - `instructions_impact.png`
  - `demo_workflow_steps.png`
  - `before_after_comparison.png`
  - `implementation_log_workflow.png`

### What to Share After Presentation

1. **Presentation file** (converted to PPTX)
2. **Complete guide** (AI-ASSISTED-CODING-COMPLETE-GUIDE.md)
3. **Getting started checklist**
4. **All artifacts** (ZIP the copilot folder)

---

## Tips for Smooth Delivery

### General Tips

1. **Practice transitions** - Switching between slides and IDE should be smooth
2. **Speak slowly** - You're introducing new concepts, let them sink in
3. **Use Alt+Tab** - Switch between presentations and IDE smoothly
4. **Pause for questions** - After each major section
5. **Point at screen** - When showing code, highlight the important bits

### IDE Tips

1. **Have code ready** - Don't type during demo, have it pre-pasted
2. **Use zoom** - Make text large (Cmd/Ctrl + +)
3. **Clear Copilot chat** - Between demos, clear chat for fresh start
4. **Show full output** - Scroll to show complete response
5. **Take your time** - Let output load, let people read

### Pacing Tips

- **Don't rush** - You have 60 minutes, use them
- **One thing at a time** - Show one agent/prompt at a time
- **Explain before showing** - Set context before IDE demo
- **Point out details** - "See the type hints? See the docstring?"
- **Build momentum** - Each demo gets faster as people understand

### If Something Goes Wrong

- **Copilot times out**: Refresh chat, try again
- **Code won't paste**: Type it manually (keep it short)
- **Wrong output**: Show it anyway, explain why it's different
- **Technical issue**: Have backup explanation ready

---

## Timing Breakdown

```
Section 1 (Opening + Problem):        5 min
Section 2 (Foundation concept):       5 min
Section 3 (IDE: instructions):        5 min
─────────────────────────────────────────
  Subtotal:                           15 min

Section 4 (Agents concept):          10 min
Section 5 (IDE: 3 agents):           15 min
─────────────────────────────────────────
  Subtotal:                           25 min

Section 6 (Prompts concept):         10 min
Section 7 (IDE: 2 prompts):          10 min
─────────────────────────────────────────
  Subtotal:                           20 min

Section 8 (Security):                 5 min
Section 9 (Workflow):                10 min
Section 10 (Context):                 3 min
Section 11 (Multi-repo):              5 min
Section 12 (Getting started):         5 min
─────────────────────────────────────────
  Subtotal:                           28 min

Q&A:                                  7 min
─────────────────────────────────────────

TOTAL:                               60 min
```

If running short on time, trim:
- Section 5: Show 2 agents instead of 3 (save 5 min)
- Section 9: Show simplified workflow (save 3 min)

If running long, extend:
- Q&A (audience can ask more)
- Expand one demo they find interesting

---

## Post-Presentation Follow-up

### In the Meeting

- Show getting started checklist
- Offer to answer setup questions
- Share the artifacts

### After the Meeting

1. **Email materials** (within 24 hours)
   - Presentation (PPTX)
   - Complete guide
   - All artifacts (ZIP copilot folder)
   - Setup instructions

2. **Follow-up support**
   - Offer to review their copilot-instructions.md
   - Help with first setup
   - Answer questions on Slack/email

3. **Track adoption**
   - Check in after week 1
   - Gather feedback
   - Iterate on materials based on questions

---

## Success Metrics

After the presentation:
- [ ] Team sets up copilot-instructions.md
- [ ] Team tries 2-3 agents/prompts
- [ ] Team reports improved code quality
- [ ] Team updates instructions based on patterns
- [ ] Team creates custom agents for their needs

---

**Good luck with your presentation!**

Remember: You're teaching a systematic approach to AI-assisted coding. The goal isn't to make people AI experts - it's to show them how structure, specialization, and continuity make AI a reliable coding partner.
