---
marp: true
theme: default
paginate: true
---

<!--
AI-Assisted Coding: Boosting Development Productivity
Presentation for engineering teams
Can be split into two 30-minute sessions at the marker indicated
-->

# AI-Assisted Coding
## Boosting Development Productivity with GitHub Copilot

**From Chaos to System: A Practical Workflow**

---

# The Problem

Most developers using AI coding assistants face these issues:

- 🔄 **Repeating yourself** - Re-explaining preferences every session
- 🐠 **Goldfish memory** - AI forgets context after 30 minutes
- 🎲 **Inconsistent results** - Sometimes great, sometimes terrible
- ⚠️ **Security risks** - Hardcoded credentials, SQL injection
- 📉 **Wasted time** - Fixing AI-generated bugs

**We need a systematic approach, not a magic wand.**

---

# What This Presentation Covers

1. The Foundation: `copilot-instructions.md`
2. Specialized Agents for Different Roles
3. Reusable Prompts for Common Tasks
4. Security Best Practices
5. Managing Token Limits with Implementation Logs
6. Complete Workflow: Planning to Production
7. Working Across Multiple Repositories

---

# Part 1: The Foundation

## copilot-instructions.md

Your AI's "onboarding document" that persists across **all sessions**

**Location**: `.github/copilot-instructions.md` in your repository

**What it does**: Automatically loaded by GitHub Copilot as context for every chat

---

# What Goes in copilot-instructions.md?

## 1. Project Overview
```markdown
## Project Overview
This repository contains a real-time data processing pipeline
for customer analytics. Processes 10M+ events daily through
Kafka, Spark, and BigQuery.
```

**Why**: AI needs domain context to suggest relevant solutions

---

# What Goes in copilot-instructions.md?

## 2. Tech Stack
```markdown
## Tech Stack
- **Primary Language**: Python 3.11+
- **Data Processing**: Apache Spark 3.4, PySpark
- **Cloud Platform**: GCP
- **Container Orchestration**: Kubernetes 1.28+
- **Testing**: pytest
```

**Why**: Prevents AI from suggesting deprecated libraries or wrong versions

---

# What Goes in copilot-instructions.md?

## 3. Code Style and Standards

```markdown
### Python Code Style
- Follow PEP 8 style guide
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use `black` for code formatting

### Documentation
- Public functions MUST have docstrings
- Use Google-style docstrings
- Do NOT add docstrings to simple getters/setters
```

**Be opinionated!** Say "use type hints" not "prefer type hints"

---

# What Goes in copilot-instructions.md?

## 4. Domain-Specific Best Practices

```markdown
## PySpark Best Practices
- Avoid `.collect()` on large DataFrames
- Use DataFrame API over RDD API
- Partition DataFrames before joins
- Cache only when reused multiple times

## Kubernetes Deployment
- Always specify resource limits and requests
- Include liveness and readiness probes
- Use ConfigMaps for config, Secrets for sensitive data
```

**Why**: Captures tribal knowledge new team members learn over months

---

# What Goes in copilot-instructions.md?

## 5. Security Guidelines

```markdown
## Security Guidelines - NON-NEGOTIABLE
- NEVER hardcode credentials or API keys
- Use Secret Manager for sensitive configuration
- Validate and sanitize all external inputs
- Use least-privilege IAM roles
- Enable audit logging for data access
```

**Why**: Security is non-negotiable, enforce it systematically

---

# What Goes in copilot-instructions.md?

## 6. File Organization

```markdown
## File Organization
.
├── src/
│   ├── pipelines/      # Data pipeline implementations
│   ├── transforms/     # Data transformation logic
│   └── utils/          # Shared utilities
├── tests/
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
└── k8s/                # Kubernetes manifests
```

**Why**: AI knows where to create files

---

# Updating copilot-instructions.md

Treat it as a **living document**. Update when:

- ✅ **After code review** - Reviewers flag the same issue repeatedly
- ✅ **After incidents** - Bug revealed a missed pattern
- ✅ **Adopting new tech** - Add best practices immediately
- ✅ **After onboarding** - Explaining same thing to new devs

**Small, focused updates** - Like git commits, not monolithic changes

---

# Demo: copilot-instructions.md

**Without instructions:**
```
User: Write a function to validate email addresses
AI: [Generates function without type hints, no docstring,
     no input validation, bare except clause]
```

**With instructions:**
```
User: Write a function to validate email addresses
AI: [Generates function with type hints, Google-style docstring,
     proper validation, specific exception types, logging]
```

The difference: **Explicit standards** encode your preferences

---

# Part 2: Specialized Agents

## Problem: Not All Coding Tasks Are the Same

- Writing production code ≠ Reviewing code
- Planning a feature ≠ Implementing it
- Writing tests ≠ Writing documentation

**Solution**: Custom agents with specialized roles and expertise

---

# What Are Custom Agents?

**Definition**: Specialized AI personas configured for specific roles

**Location**: `.github/copilot/agents/<agent-name>.agent.md`

**Invocation**: `@agent-name` in Copilot Chat

**Benefits**:
- Consistent behavior for specific tasks
- Role-specific expertise and constraints
- Reusable across projects

---

# Agent: Python Coder (@python-coder)

**Role**: Write production-quality Python code

```markdown
# Python Coder Agent

Expert Python developer specializing in data engineering,
PySpark, and cloud-native applications.

## Code Standards
- Follow PEP 8, use type hints
- Comprehensive docstrings (Google style)
- Proper error handling (specific exceptions)
- Testable, modular code

## Constraints
- Do NOT use deprecated features
- Do NOT use `.collect()` on large DataFrames
- Do NOT hardcode configuration
```

---

# Using Python Coder Agent

**Usage**:
```
@python-coder Implement a PySpark function that validates
customer records against a schema, logs validation errors,
and writes valid records to BigQuery.
```

**Result**:
- Type-hinted function
- Error handling with specific exceptions
- Logging at appropriate points
- Configuration via environment variables
- No hardcoded values

---

# Agent: Python Tester (@python-tester)

**Role**: Write comprehensive pytest tests

```markdown
# Python Tester Agent

Expert in pytest, mocking, and test-driven development.

## Testing Standards
- Descriptive names: `test_<function>_<scenario>_<expected>`
- Arrange-Act-Assert (AAA) pattern
- Pytest fixtures for setup
- Parametrize for multiple scenarios
- Mock external services and I/O

## Coverage Goals
- Happy path, edge cases, error conditions
```

---

# Using Python Tester Agent

**Usage**:
```
@python-tester Generate unit tests for the customer
validation function, including edge cases for invalid
schemas and malformed records.
```

**Result**:
- Comprehensive test suite with fixtures
- Parametrized tests for multiple scenarios
- Mocked external dependencies
- Tests for happy path, edge cases, and errors

---

# Agent: Kubernetes Expert (@kubernetes-expert)

**Role**: Create production-grade K8s configurations

```markdown
# Kubernetes Expert Agent

Kubernetes expert for GKE deployments.

## Standards
- Always specify resource limits and requests
- Include liveness and readiness probes
- Use namespaces for environment isolation
- ConfigMaps for config, Secrets for sensitive data
- Security contexts (non-root, read-only filesystem)
```

---

# Agent: Task Planner (@task-planner)

**Role**: Create detailed implementation plans

```markdown
# Task Planner Agent

Technical architect who creates actionable implementation plans.

## Planning Process
1. Understand: Clarify requirements and constraints
2. Analyze: Identify affected components
3. Design: Propose technical approach
4. Break Down: Create step-by-step plan
5. Validate: Check for edge cases and risks
```

**Use at the start of complex features** before writing code

---

# Agent: Code Reviewer (@code-reviewer)

**Role**: Review code for issues and improvements

```markdown
# Code Reviewer Agent

Reviews code for correctness, security, performance,
maintainability, and test coverage.

## Feedback Categories
- CRITICAL: Security issues, logic errors
- IMPORTANT: Performance, maintainability
- MINOR: Style, missing edge cases
- NITPICK: Suggestions, not requirements
```

---

# Agent: PR Description Generator

**Role**: Create comprehensive pull request descriptions

```markdown
# PR Description Generator

Creates clear, informative PR descriptions.

## Structure
1. Summary (1-2 sentences)
2. Type of Change (feature/bugfix/refactor)
3. Detailed Description (problem, solution, trade-offs)
4. Changes Made (bulleted list)
5. Testing Done
6. Deployment Notes
```

---

# Agent: README Generator

**Role**: Create and update project documentation

Generates:
- Project overview and features
- Installation instructions
- Quick start guides
- Configuration documentation
- Usage examples
- Contributing guidelines

---

# Summary: Available Agents

| Agent | Role | Use When |
|-------|------|----------|
| `@python-coder` | Write production code | Implementing features |
| `@python-tester` | Generate tests | Need test coverage |
| `@kubernetes-expert` | K8s configs | Deploying services |
| `@task-planner` | Create plans | Starting complex work |
| `@code-reviewer` | Review code | Before commits |
| `@pr-description-generator` | PR descriptions | Opening pull requests |
| `@readme-generator` | Documentation | Updating docs |

---

<!-- SESSION 1 ENDS HERE (30 minutes) -->
<!-- SESSION 2 STARTS HERE -->

# Part 3: Reusable Prompts

## Problem: Common Code Transformations

- Refactoring for testability
- Optimizing PySpark code
- Adding logging
- Generating tests
- Security reviews

**Solution**: Custom prompts - quick, focused templates

---

# What Are Custom Prompts?

**Definition**: Reusable templates for common transformations

**Location**: `.github/copilot/prompts/<prompt-name>.prompt.md`

**Invocation**: `/<prompt-name>` in Copilot Chat

**Workflow**:
1. Select code in editor
2. Run `/<prompt-name>` in chat
3. AI transforms selected code

---

# Prompt: Refactor for Testability

**Command**: `/refactor-for-testability`

**What it does**:
- Dependency injection (replace hardcoded dependencies)
- Separate pure logic from side effects
- Break down large functions
- Make all dependencies explicit

**Example**:
```python
# Before: Hardcoded database connection
def get_user(user_id):
    db = Database.connect()
    return db.query(f"SELECT * FROM users WHERE id = {user_id}")

# After: Dependency injection, parameterized query
def get_user(user_id: str, db_client: DatabaseClient) -> User:
    return db_client.get_user(user_id)
```

---

# Prompt: Optimize PySpark

**Command**: `/optimize-pyspark`

**Optimizations**:
- Minimize shuffle operations
- Optimal partitioning before joins
- Broadcast joins for small tables
- Column pruning (select early)
- Predicate pushdown (filter early)
- Smart caching strategy

**Example**:
```python
# Before
df.select(*).filter(condition).groupBy(key)

# After
df.filter(condition).select(needed_cols).repartition(key).groupBy(key)
```

---

# Prompt: Add Comprehensive Logging

**Command**: `/add-comprehensive-logging`

**Adds**:
- Function entry/exit logs with parameters
- State transition logs
- Error logs with context
- Appropriate log levels (DEBUG/INFO/WARNING/ERROR)
- Structured logging with IDs and metrics

**Example**:
```python
logger.info(f"[process_records] Starting processing {len(records)} records")
# ... processing ...
logger.info(f"[process_records] Completed. Success: {success_count}, Failed: {fail_count}")
```

---

# Prompt: Generate Unit Tests

**Command**: `/generate-unit-tests`

**Generates**:
- Pytest test suite with fixtures
- Parametrized tests for multiple scenarios
- Mocked external dependencies
- Tests for happy path, edge cases, errors
- Descriptive test names

**Example**:
```python
@pytest.mark.parametrize("input_val,expected", [(0, 0), (5, 25), (10, 100)])
def test_square_function_returns_correct_value(input_val, expected):
    assert square(input_val) == expected
```

---

# Prompt: Security Review

**Command**: `/security-review`

**Checks**:
- SQL injection vulnerabilities
- Command injection risks
- Path traversal issues
- Hardcoded credentials
- Input validation gaps
- Insecure error handling

**Run before every commit** that touches external inputs or sensitive data

---

# Summary: Available Prompts

| Prompt | Purpose | When to Use |
|--------|---------|-------------|
| `/refactor-for-testability` | Make code testable | Legacy code, before testing |
| `/optimize-pyspark` | Performance tuning | PySpark transformations |
| `/add-comprehensive-logging` | Add structured logs | Production code |
| `/generate-unit-tests` | Create test suite | After implementation |
| `/security-review` | Find vulnerabilities | Before commits |

---

# Part 4: Security Best Practices

## AI Can Introduce Security Risks

Common issues:
- Hardcoded credentials
- SQL injection
- Missing input validation
- Excessive logging of sensitive data
- Vulnerable dependencies

**Solution**: Systematic security checks

---

# Security Practice 1: Never Trust Generated Code

**Always review for**:
- ❌ Hardcoded secrets or credentials
- ❌ SQL injection vulnerabilities
- ❌ Command injection risks
- ❌ Missing input validation
- ❌ Excessive permissions

**Always run** `/security-review` before committing

---

# Security Practice 2: Explicit Constraints

**In copilot-instructions.md**:

```markdown
## Security Guidelines - NON-NEGOTIABLE
- NEVER hardcode credentials, API keys, or secrets
- ALWAYS validate and sanitize external inputs
- ALWAYS use parameterized queries for SQL
- ALWAYS use environment variables for config
- ALWAYS log security events (auth failures)
```

Make security rules explicit and absolute

---

# Security Practice 3: Sanitize Prompts

**Bad**:
```
"Fix this query: SELECT * FROM users WHERE api_key = 'sk-1234567890abcdef'"
```

**Good**:
```
"Fix this query: SELECT * FROM users WHERE api_key = '<API_KEY>'"
```

Replace real secrets with placeholders in prompts

---

# Security Practice 4: Review Dependencies

When AI suggests adding dependencies:

- ✅ Check for known vulnerabilities (Snyk, Dependabot)
- ✅ Verify package is actively maintained
- ✅ Review package's dependencies
- ✅ Use pinned versions, not `latest`

**Example**:
```python
# Bad
requests  # Unspecified version

# Good
requests==2.31.0  # Pinned, verified version
```

---

# Security Practice 5: Logging Guidelines

```markdown
## Logging Guidelines
- Do NOT log passwords, API keys, tokens
- Do NOT log PII unless required
- Redact sensitive fields:
  logger.info(f"User {user_id[:8]}... logged in")
```

AI may suggest logging sensitive data - explicitly forbid it

---

# Part 5: Managing Token Limits

## The Token Limit Problem

- Long conversations exceed context windows
- AI starts forgetting earlier context
- Quality degrades as history is compressed
- Repeats questions already answered

**Bigger context windows don't solve this**
You need **structured continuity**

---

# Solution: Implementation Logs

**Concept**: Maintain a running log of what you've built

**File**: `IMPLEMENTATION_LOG.md` in project root

**Purpose**: Provides context for new sessions without full conversation history

**When to use**: Multi-day features, complex projects, when hitting token limits

---

# Implementation Log Structure

```markdown
# Implementation Log: [Feature Name]

## [Date]: Planning Phase
**Objective**: [What are we building]
**Requirements**: [Acceptance criteria]
**Technical Approach**: [How we'll build it]
**Key Decisions**: [Important choices made]

## [Date]: Implementation
**Completed**: [What was done]
**Files Modified**: [Which files changed]
**Code Locations**: [Key code locations]

## [Date]: Testing
**Test Coverage**: [What was tested]
**Issues Found**: [Bugs discovered and fixed]

## Next Steps
[What needs to be done next]
```

---

# Implementation Log Example

```markdown
# Implementation Log: Rate Limiting Feature

## 2026-02-01: Planning Phase
**Objective**: Add Redis-backed rate limiting to API
**Requirements**: 100 req/min per API key, return 429 when exceeded
**Technical Approach**: Redis sliding window algorithm
**Key Decisions**: Chose sliding over fixed window, fail open if Redis down

## 2026-02-02: Implementation
**Completed**: RateLimiter class, FastAPI middleware
**Files Modified**:
- `src/middleware/rate_limiter.py` (new)
- `src/app.py` (added middleware)
**Code Locations**: Rate limiter logic at `src/middleware/rate_limiter.py:15-78`

## 2026-02-03: Testing
**Test Coverage**: Unit, integration, load tests (1000 concurrent)
**Issues Found**: Off-by-one error (fixed), race condition (fixed with Lua)

## Next Steps: Create monitoring dashboard
```

---

# Using Implementation Logs

**Starting a new session**:
```
Read the IMPLEMENTATION_LOG.md and continue from where we left off.
We need to create the monitoring dashboard next.
```

**AI has full context** without needing the entire conversation history

**Benefits**:
- Consistent context across sessions
- No information loss from summarization
- Other team members can pick up where you left off

---

# Part 6: Complete Workflow

## Planning → Implementation → Review → Deploy

Let's walk through a complete feature using all the tools

**Example Feature**: Implement rate limiting for an API

---

# Workflow Phase 1: Planning

```
@task-planner Implement rate limiting for our API using Redis.
Requirements: 100 requests/minute per API key, return 429 when
exceeded, include rate limit info in response headers.
```

**Planner Output**:
- Requirements analysis with clarification questions
- Technical approach (Redis sliding window)
- Step-by-step implementation tasks
- Testing strategy
- Risks and considerations

**Review, answer questions, refine approach**

---

# Workflow Phase 2: Implementation

```
@python-coder Implement the rate limiter according to the plan.
Use Redis with sliding window algorithm. Include type hints,
error handling, and logging.
```

**Coder Output**:
- RateLimiter class with dependency injection
- Type-hinted function signatures
- Proper error handling
- Structured logging
- Environment variable configuration

---

# Workflow Phase 3: Testing

**Select the implemented code**, then:
```
/generate-unit-tests
```

**AI Generates**:
- Pytest fixtures for setup
- Parametrized tests for multiple scenarios
- Mocked Redis dependencies
- Tests for happy path, edge cases, errors
- Integration tests

**Review and run the tests**

---

# Workflow Phase 4: Optimization

**For PySpark code**:
```
/optimize-pyspark
```

**For general code**:
```
/refactor-for-testability
```

**AI suggests specific improvements** with before/after examples

---

# Workflow Phase 5: Logging

```
/add-comprehensive-logging
```

**AI adds**:
- Function entry/exit logs
- State transition logs
- Error logs with context
- Appropriate log levels

---

# Workflow Phase 6: Review

```
@code-reviewer Review this implementation for issues,
security vulnerabilities, and improvements.
```

**Reviewer provides categorized feedback**:
- **CRITICAL**: Security issues, logic errors
- **IMPORTANT**: Performance, maintainability
- **MINOR**: Style, missing edge cases

**Then run**:
```
/security-review
```

**Address critical and important items**

---

# Workflow Phase 7: Documentation

```
@readme-generator Update the README with documentation
for the rate limiting feature, including configuration
options and usage examples.
```

**AI generates**:
- Feature description
- Configuration options table
- Usage examples with code
- Deployment notes

---

# Workflow Phase 8: Pull Request

```
@pr-description-generator Create a PR description for
the rate limiting implementation.
```

**AI creates**:
- Clear summary of changes
- Detailed description with rationale
- List of specific changes
- Testing coverage
- Deployment notes
- Reviewer checklist

---

# Part 7: Working Across Multiple Repositories

## Multi-Repo Workspaces

Many teams work on:
- Backend (Python/FastAPI)
- Frontend (React/TypeScript)
- Infrastructure (Kubernetes/Terraform)

**Solution**: Shared configuration in parent directory

---

# Multi-Repo Structure

```
workspace/
├── .github/
│   ├── copilot-instructions.md  ← Shared instructions
│   └── copilot/
│       ├── agents/               ← Shared agents
│       └── prompts/              ← Shared prompts
├── backend/                      ← Python repo
├── frontend/                     ← React repo
└── infrastructure/               ← K8s/Terraform repo
```

**VSCode automatically loads from parent directories**

---

# Shared copilot-instructions.md

```markdown
# Multi-Repository Workspace

This workspace contains:
- backend: Python FastAPI application
- frontend: React TypeScript application
- infrastructure: Kubernetes and Terraform configs

**IMPORTANT**: When working on code, only modify files
in the relevant repository. Do not make changes outside
the current repository directory.

## Backend Standards
[Python/FastAPI specific standards]

## Frontend Standards
[React/TypeScript specific standards]

## Infrastructure Standards
[K8s/Terraform specific standards]
```

---

# Best Practices Summary

1. **Be Explicit** - Direct instructions work better than implicit expectations
2. **Specialize Agents** - Different roles for different tasks
3. **Review Everything** - Never blindly accept AI-generated code
4. **Iterate** - Use feedback to refine output
5. **Document** - Keep implementation logs for complex projects
6. **Security First** - Always run security reviews
7. **Update Instructions** - Keep copilot-instructions.md current

---

# Measuring Impact

**Time Savings**:
- Feature implementation: ~30-40% faster
- Time to first prototype: ~50% faster
- Code review cycles: ~20% faster

**Quality Improvements**:
- Test coverage: 70% → 85%+
- Security findings: 35% reduction
- Documentation: Significantly improved

**Note**: Subjective measurements, not controlled experiments

---

# What Works

✅ **Explicit instructions** over implicit expectations
✅ **Role specialization** (different agents for different tasks)
✅ **Iterative refinement** with clear feedback
✅ **Implementation logs** for multi-day projects
✅ **Combining approaches** (agents for complex, prompts for quick)

---

# What Doesn't Work

❌ **Vague requests** ("make this better")
❌ **Blind acceptance** (always review AI output)
❌ **Over-engineering** (not everything needs AI)
❌ **Ignoring context limits** (start fresh with logs)
❌ **Treating AI as infallible** (you still need expertise)

---

# Getting Started Checklist

- [ ] Create `.github/copilot-instructions.md` in your repo
- [ ] Add project overview, tech stack, code standards
- [ ] Create custom agents for your common tasks
- [ ] Create custom prompts for transformations
- [ ] Add security guidelines to instructions
- [ ] Train your team on the workflow
- [ ] Start small - one project, iterate and improve
- [ ] Share and refine configurations across team

---

# Resources

**Official Documentation**:
- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [Custom Instructions Guide](https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/)
- [Custom Agents in VSCode](https://code.visualstudio.com/docs/copilot/customization/custom-agents)

**Community**:
- [Awesome Copilot](https://github.com/github/awesome-copilot)
- Copilot Prompting Guide 2025

**All artifacts from this presentation** available in the `copilot/` directory

---

# Questions?

**Key Takeaway**:
AI coding assistants are tools that amplify expertise when used systematically.

Treat them like new team members:
- Provide clear onboarding (instructions)
- Assign specialized roles (agents)
- Create reusable processes (prompts)
- Maintain continuity (implementation logs)

**Start experimenting today!**

---

# Thank You!

**Contact**: [Your contact information]

**Resources**:
- Blog post: [Link to your blog]
- Copilot configurations: [Link to copilot folder]
- Implementation examples: [Link to examples]

**Let's build better software faster!**
