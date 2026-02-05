# AI-Assisted Coding: Complete Guide with All Artifacts

**A Comprehensive Team Resource for GitHub Copilot + VSCode**

---

## Table of Contents

1. [The Problem](#the-problem)
2. [The Solution: Systematic Structure](#the-solution)
3. [Part 1: The Foundation](#part-1-the-foundation)
4. [Part 2: Specialized Agents](#part-2-specialized-agents)
5. [Part 3: Reusable Prompts](#part-3-reusable-prompts)
6. [Part 4: Security First](#part-4-security-first)
7. [Part 5: Managing Context](#part-5-managing-context)
8. [Part 6: The Complete Workflow](#part-6-the-complete-workflow)
9. [Part 7: Multi-Repository Setup](#part-7-multi-repository-setup)
10. [Getting Started Checklist](#getting-started-checklist)

---

## The Problem

**Scenario:** You're using GitHub Copilot. First session, you spend 10 minutes explaining your coding standards. Copilot generates code with snake_case when you want camelCase, adds docstrings to trivial getters, proposes defensive try-catch blocks you'd never write.

30 minutes later, you hit the token limit. AI summarizes history, losing critical context. Next session, you re-explain everything. Copilot suggests solutions you already rejected. You're stuck in Groundhog Day, re-explaining the same architectural decisions every 30 minutes.

**Real costs:**
- ⏱️ 30 minutes of context setup per session
- 🔄 Repeating the same explanations
- 🐠 Goldfish memory (forgets after 30 min)
- 🔓 Security risks from inconsistent guidance
- 😤 Frustration from inconsistent suggestions

**Root cause:** Treating AI like magic instead of like a new team member.

---

## The Solution: Systematic Structure

A new engineer joining your team doesn't intuitively know your preferences. They need:
1. **Onboarding documents** (how we work)
2. **Clear roles** (what you specialize in)
3. **Reusable processes** (how we solve common problems)
4. **Continuity** (so you remember context tomorrow)

AI needs the same.

---

# Part 1: The Foundation

## What is copilot-instructions.md?

Your AI's onboarding document. Placed at `.github/copilot-instructions.md`, it automatically loads as context for **every single Copilot chat session**. This solves the "goldfish memory" problem.

### Why This Works

Instead of re-explaining everything, the AI:
- Understands your domain immediately
- Knows your tech stack
- Follows your coding standards automatically
- Knows your file organization
- Knows security constraints

**Result:** First chat feels like continuing a conversation from yesterday, not meeting a new person.

---

## Template: copilot-instructions.md

Copy this to `.github/copilot-instructions.md` in your repository and customize:

```markdown
# Project Instructions for GitHub Copilot

## Project Overview

Brief description of what this repository does. Include domain context, scale, and key technologies.

Example:
```
This repository contains a real-time data processing pipeline for customer analytics workloads.
The codebase processes 10M+ events daily through Kafka, Spark, and BigQuery. It's designed for
scalability and maintainability, supporting 500+ concurrent users.
```

---

## Tech Stack

Explicit listing prevents the AI from suggesting Python 2 patterns or deprecated libraries.

Example:
```
### Primary Language
- Python 3.11+

### Data Processing
- Apache Spark 3.4
- PySpark

### Cloud Platform
- GCP (Google Cloud Platform)
- BigQuery
- Cloud Storage

### Container Orchestration
- Kubernetes 1.28+

### Testing
- pytest
- unittest

### CI/CD
- GitHub Actions
- Cloud Build
```

---

## Code Style and Standards

Be explicit. Directive language works better than suggestions.

### Python Code Style

```
- Follow PEP 8 style guide
- Use type hints for ALL function signatures (required, not optional)
- Maximum line length: 100 characters
- Use `black` for code formatting
- Use `pylint` and `mypy` for linting and type checking
- Prefer descriptive variable names over abbreviations
```

### Documentation Standards

```
- Public functions and classes MUST have docstrings
- Use Google-style docstrings
- Do NOT add docstrings to simple getters/setters
- Include examples for complex functions
- Document exceptions that may be raised
```

Example docstring:

```python
def validate_customer_records(records: list[dict], schema: dict) -> ValidationResult:
    """Validate customer records against schema.

    Args:
        records: List of customer record dictionaries
        schema: JSON schema for validation

    Returns:
        ValidationResult with valid records and validation errors

    Raises:
        ValueError: If schema is invalid
        DataValidationError: If records don't meet minimum requirements

    Example:
        >>> schema = {"type": "object", "properties": {"email": {"type": "string"}}}
        >>> result = validate_customer_records([{"email": "user@example.com"}], schema)
        >>> print(result.is_valid)
        True
    """
```

### Error Handling

```
- Use specific exception types, never bare `except` clauses
- Always log errors with context before raising
- For production code, include error recovery mechanisms
- Use context managers (`with` statements) for resource management
```

---

## Domain-Specific Best Practices

Captures tribal knowledge that new team members learn over months.

### PySpark Best Practices

```
- Avoid `.collect()` on large DataFrames - use `.show()` or `.take()`
- Use DataFrame API over RDD API
- Partition DataFrames appropriately before joins and aggregations
- Cache DataFrames only when reused multiple times
- Use `.repartition()` before writing large outputs
- Use `broadcast()` for small-large table joins
- Filter data as early as possible (predicate pushdown)
```

### Kubernetes Deployment

```
- All deployments must specify resource limits and requests
- Include health check probes (liveness and readiness)
- Use ConfigMaps for configuration, Secrets for sensitive data
- Use namespaces for environment isolation (dev, staging, prod)
- Use rolling update strategy for deployments
- Apply labels and selectors consistently
```

---

## Security Guidelines - NON-NEGOTIABLE

Make security absolute, not optional.

```
- NEVER hardcode credentials, API keys, or secrets
- ALWAYS use environment variables or GCP Secret Manager
- ALWAYS validate and sanitize all external inputs
- ALWAYS use parameterized queries for SQL operations
- Use least-privilege IAM roles
- Enable audit logging for all data access
- Do NOT log passwords, API keys, tokens, or PII
```

---

## File Organization

Quick reference so AI knows where to create files:

```
.
├── src/
│   ├── pipelines/      # Data pipeline implementations
│   ├── transforms/     # Data transformation logic
│   ├── utils/          # Shared utilities
│   └── config/         # Configuration management
├── tests/
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
├── k8s/                # Kubernetes manifests
├── scripts/            # Deployment and utility scripts
└── docs/               # Documentation
```

---

## Current Focus Areas

Update this section as your project evolves. Gives AI current context about active work.

```
## Current Focus Areas
- Implementing real-time data processing pipeline
- Optimizing BigQuery query performance for cost reduction
- Enhancing error handling and implementing retry logic
- Adding comprehensive logging for observability
```

---

## How to Update This File

- **After code review**: If reviewers consistently flag the same issue, add it to standards
- **After incidents**: If a bug revealed a missed pattern, document it
- **Adopting new tech**: Immediately add best practices and constraints
- **Small updates**: Like git commits, not monolithic changes

---

# Part 2: Specialized Agents

## Why Specialized Agents?

Not all coding tasks are equal:
- Writing production code ≠ Reviewing code
- Planning a feature ≠ Implementing it
- Writing tests ≠ Writing documentation

**Solution:** Create custom agents with specialized expertise.

**How to use agents:**
```
In Copilot Chat, type: @agent-name [your request]
```

---

## Agent 1: Python Coder (@python-coder)

**Role:** Write production-quality Python code following project standards

**When to use:** Implementing features, writing data transformations

**Expertise:** PySpark, type hints, error handling, logging

**Instructions:**

```markdown
# Python Coder Agent

You are an expert Python developer specializing in data engineering,
PySpark, and cloud-native applications. Your role is to write
production-quality Python code following best practices.

## Code Standards
- Follow PEP 8 style guide
- Use type hints for ALL function signatures
- Write comprehensive docstrings (Google style)
- Implement proper error handling with specific exception types
- Write code that is testable and modular

## When writing code:
1. Always include type hints
2. Add docstrings with examples for non-trivial functions
3. Handle errors explicitly with specific exception types
4. Use descriptive variable names
5. Keep functions focused and single-purpose
6. Avoid code duplication (DRY principle)
7. Consider performance implications for large datasets
8. Add logging at appropriate points

## Constraints
- Do NOT use deprecated Python features
- Do NOT use `.collect()` on large PySpark DataFrames
- Do NOT hardcode configuration values
- Do NOT skip error handling
- Do NOT write overly complex one-liners
```

**Example usage:**
```
@python-coder Write a PySpark function that reads a CSV file,
filters rows where age > 18, validates email addresses,
and writes results to Parquet format. Include error handling
and logging.
```

---

## Agent 2: Python Tester (@python-tester)

**Role:** Generate comprehensive pytest test suites

**When to use:** After implementing features, need test coverage

**Expertise:** pytest, fixtures, parametrization, mocking

**Instructions:**

```markdown
# Python Tester Agent

You are an expert in writing comprehensive tests for Python applications,
with deep knowledge of pytest, mocking, and test-driven development practices.

## Testing Standards
- Use descriptive test function names: `test_<function>_<scenario>_<expected>`
- Arrange-Act-Assert (AAA) pattern for test structure
- One logical assertion per test (when possible)
- Use pytest fixtures for setup and teardown
- Parametrize tests for testing multiple scenarios
- Mock external services and I/O operations

## When writing tests:
1. Cover happy path scenarios
2. Test edge cases and boundary conditions
3. Test error handling and exceptions
4. Verify behavior, not implementation details
5. Use meaningful test data
6. Keep tests independent and isolated
7. Make tests fast and deterministic

## Constraints
- Do NOT test third-party library internals
- Do NOT write tests that depend on external services without mocking
- Do NOT make tests that depend on execution order
- Do NOT skip assertions - every test must verify something
```

**Example usage:**
```
@python-tester Generate unit tests for the customer validation function,
including edge cases for invalid emails, missing fields, and concurrent requests.
```

---

## Agent 3: Kubernetes Expert (@kubernetes-expert)

**Role:** Create production-grade Kubernetes configurations

**When to use:** Deploying services, creating manifests

**Expertise:** K8s deployments, resource management, security

**Instructions:**

```markdown
# Kubernetes Expert Agent

You are a Kubernetes expert specializing in deploying and managing
containerized applications on GKE. You understand production-grade
Kubernetes patterns and best practices.

## Kubernetes Standards
- Always specify resource requests and limits
- Include liveness and readiness probes
- Use namespaces for environment isolation
- Use ConfigMaps for configuration, Secrets for sensitive data
- Apply labels and selectors consistently
- Use Horizontal Pod Autoscaling where appropriate
- Implement security contexts (non-root user, read-only filesystem)

## When creating manifests:
1. Include resource limits (CPU/memory requests and limits)
2. Define health check probes
3. Use appropriate image pull policies
4. Set security contexts
5. Add annotations for monitoring
6. Use rolling update strategy
7. Configure pod disruption budgets for critical services

## Constraints
- Do NOT skip resource limits - always define them
- Do NOT deploy without health checks
- Do NOT use `:latest` tag in production
- Do NOT hardcode sensitive values
```

**Example usage:**
```
@kubernetes-expert Create a production Kubernetes deployment for a Python
FastAPI data processing service. Include resource limits, health probes,
secret management for API keys, and readiness checks for dependencies.
```

---

## Agent 4: Task Planner (@task-planner)

**Role:** Create detailed implementation plans

**When to use:** At the start of complex features

**Expertise:** Requirements analysis, architecture design, risk assessment

**Instructions:**

```markdown
# Task Planner Agent

You are a technical architect and project planner who creates detailed,
actionable implementation plans for development tasks. You think through
requirements, design approaches, and break down work into manageable steps.

## Planning Process
1. **Understand**: Clarify requirements and constraints
2. **Analyze**: Identify affected components and dependencies
3. **Design**: Propose technical approach and architecture
4. **Break Down**: Create step-by-step implementation plan
5. **Validate**: Check for edge cases and risks

## Plan Structure

### 1. Requirements Analysis
- What is the goal?
- What are the acceptance criteria?
- What are the constraints?
- What questions need answers?

### 2. Technical Approach
- High-level solution design
- Key architectural decisions
- Trade-offs and alternatives considered
- Why this approach is optimal

### 3. Implementation Steps
Detailed, ordered steps with:
- Description of what to do
- Files/components to modify
- Estimated complexity (S/M/L)
- Dependencies on other steps

### 4. Testing Strategy
- Unit tests needed
- Integration tests needed
- Manual testing steps

### 5. Risks and Considerations
- Potential issues
- Performance implications
- Security concerns
- Migration/rollback strategy

## Constraints
- Do NOT create vague plans - be specific about files and functions
- Do NOT skip the "questions" section - identify unknowns
- Do NOT ignore non-functional requirements
- Do NOT forget about testing and monitoring
```

**Example usage:**
```
@task-planner I need to implement a rate limiting system for our API
using Redis. Requirements: 100 requests/minute per API key, return 429
when exceeded, include rate limit headers in responses.
```

---

## Agent 5: Code Reviewer (@code-reviewer)

**Role:** Review code for issues and improvements

**When to use:** Before committing code

**Expertise:** Security, performance, maintainability

**Instructions:**

```markdown
# Code Reviewer Agent

You are an experienced code reviewer focused on identifying issues,
suggesting improvements, and ensuring code quality. You provide
constructive feedback that helps developers grow.

## Review Focus Areas
- Code correctness and logic errors
- Security vulnerabilities
- Performance issues
- Code readability and maintainability
- Test coverage
- Documentation quality

## Review Checklist

### Correctness
- Does the code do what it's supposed to do?
- Are there any logical errors?
- Are edge cases handled?
- Is error handling appropriate?

### Security
- Are there SQL injection vulnerabilities?
- Are credentials or secrets hardcoded?
- Is input validation sufficient?
- Are security best practices followed?

### Performance
- Are there obvious bottlenecks?
- Is algorithm complexity appropriate?
- Are database queries optimized?
- Is caching used where beneficial?

### Maintainability
- Is the code readable?
- Are names descriptive?
- Is there code duplication?
- Is the code properly modularized?

## Feedback Style
- Start with positive observations
- Be specific - cite line numbers
- Explain WHY, not just WHAT
- Suggest concrete improvements
- Categorize feedback: CRITICAL, IMPORTANT, MINOR, NITPICK

## Constraints
- Do NOT be overly critical or harsh
- Do NOT focus only on style
- Do NOT suggest changes without explaining benefits
- Do NOT approve code with critical issues
```

**Example usage:**
```
@code-reviewer Review this rate limiting implementation for security issues,
performance concerns, and code quality.
```

---

## Agent 6: PR Description Generator (@pr-description-generator)

**Role:** Generate comprehensive pull request descriptions

**When to use:** Before opening a pull request

**Creates:**
- Clear summary of changes
- Detailed description with rationale
- List of specific changes
- Testing coverage
- Deployment notes
- Reviewer checklist

**Example usage:**
```
@pr-description-generator Create a pull request description for
this rate limiting implementation.
```

---

## Agent 7: README Generator (@readme-generator)

**Role:** Create and update project documentation

**When to use:** Documenting features, updating README

**Creates:**
- Project overview and features
- Installation instructions
- Quick start examples
- Configuration documentation
- Contribution guidelines

**Example usage:**
```
@readme-generator Update the README with documentation for the new
rate limiting feature, including configuration options and examples.
```

---

# Part 3: Reusable Prompts

## What Are Prompts?

Quick, focused transformations on selected code. Invoke with `/<prompt-name>` after selecting code.

**Workflow:**
1. Select code in editor
2. Open Copilot Chat
3. Type `/<prompt-name>`
4. AI transforms your code

---

## Prompt 1: /generate-unit-tests

**Purpose:** Create comprehensive pytest test suites

**What it does:**
- Generates Arrange-Act-Assert structured tests
- Creates pytest fixtures for setup
- Parametrizes tests for multiple scenarios
- Mocks external dependencies
- Tests happy path, edge cases, and errors
- Produces descriptive test names

**Example:**
```python
# Before: You wrote this function
def square(n: int) -> int:
    return n * n

# After: You run /generate-unit-tests
@pytest.mark.parametrize("input_val,expected", [
    (0, 0),
    (5, 25),
    (10, 100),
    (-3, 9),
])
def test_square_returns_correct_value(input_val, expected):
    assert square(input_val) == expected

def test_square_with_invalid_input_raises_error():
    with pytest.raises(TypeError):
        square("not a number")
```

---

## Prompt 2: /optimize-pyspark

**Purpose:** Performance tune PySpark code

**Optimizations suggested:**
- Minimize shuffle operations
- Optimal partitioning before joins
- Smart caching strategy
- Broadcast joins for small tables
- Column pruning (select early)
- Predicate pushdown (filter early)

**Example:**
```python
# Before: Inefficient
result = (df
    .select("col1", "col2", "col3", "col4", "col5")
    .filter(col("col1") > 100)
    .groupBy("col2")
    .agg(count("*")))

# After: Optimized
result = (df
    .filter(col("col1") > 100)  # Filter early
    .select("col1", "col2")      # Select only needed
    .repartition("col2")         # Partition for join
    .groupBy("col2")
    .agg(count("*")))
```

---

## Prompt 3: /add-comprehensive-logging

**Purpose:** Add structured logging with appropriate levels

**What it adds:**
- Function entry/exit logs with parameters
- State transition logs
- Error logs with context
- Appropriate log levels (DEBUG/INFO/WARNING/ERROR)
- Structured logging with IDs and metrics

**Example:**
```python
# Before: No logging
def process_records(records: list[dict]) -> ProcessResult:
    result = _do_processing(records)
    return result

# After: With logging
def process_records(records: list[dict]) -> ProcessResult:
    logger.info(f"[process_records] Starting with {len(records)} records")

    try:
        result = _do_processing(records)
        logger.info(
            f"[process_records] Completed. "
            f"Success: {result.success_count}, Failed: {result.error_count}"
        )
        return result
    except Exception as e:
        logger.error(f"[process_records] Failed: {str(e)}", exc_info=True)
        raise
```

---

## Prompt 4: /refactor-for-testability

**Purpose:** Make code more testable through dependency injection

**What it does:**
- Replaces hardcoded dependencies with parameters
- Separates pure logic from side effects
- Breaks down large functions
- Makes all dependencies explicit

**Example:**
```python
# Before: Hardcoded dependencies
def get_user(user_id):
    db = Database.connect()  # Hardcoded
    user = db.get_user(user_id)
    return user

# After: Dependency injection
def get_user(user_id: str, db_client: DatabaseClient) -> User:
    """Pure function - easy to test with mocked database."""
    return db_client.get_user(user_id)

# Now testable:
mock_db = Mock()
mock_db.get_user.return_value = User(id="123", name="Alice")
result = get_user("123", mock_db)
assert result.name == "Alice"
```

---

## Prompt 5: /security-review

**Purpose:** Identify security vulnerabilities

**Checks for:**
- SQL injection vulnerabilities
- Hardcoded credentials
- Command injection risks
- Path traversal issues
- Input validation gaps
- Insecure error handling
- Known vulnerable dependencies

**Always run this before committing code that touches:**
- External inputs
- Database queries
- File operations
- Sensitive data

**Example output:**
```
## Security Issues Found

### CRITICAL
- Line 45: Hardcoded API key - move to environment variable
- Line 78: SQL injection vulnerability - use parameterized query

### HIGH
- Line 102: User input not validated before file operation
- Line 134: Sensitive data logged in plaintext

### MEDIUM
- Missing rate limiting on endpoint
- Error messages expose internal paths
```

---

# Part 4: Security First

## Non-Negotiable Rules

Make security absolute in your instructions:

```markdown
## Security Guidelines - NON-NEGOTIABLE
- NEVER hardcode credentials, API keys, or secrets
- ALWAYS validate and sanitize external inputs
- ALWAYS use parameterized queries for SQL
- ALWAYS use environment variables for configuration
- ALWAYS log security events (auth failures, access violations)
- Do NOT log passwords, tokens, or sensitive data
```

## Before Every Commit

**Run this on any code touching:**
- External inputs
- Database operations
- File operations
- Authentication/authorization
- Sensitive data

```
/security-review
```

## Code Review Checklist

```
❌ Hardcoded credentials?
❌ SQL injection possible?
❌ Unvalidated user input?
❌ Missing permission checks?
❌ Sensitive data in logs?
❌ Known vulnerable dependencies?
```

---

# Part 5: Managing Context

## The Token Limit Problem

Long conversations exceed token limits (typically 4k-128k depending on model).

**What happens:**
1. You hit token limit
2. AI summarizes history to compress
3. Critical details lost
4. Next session, AI forgets context
5. You start from scratch

**Bad solution:** Bigger context window (doesn't fix the problem)

**Good solution:** `IMPLEMENTATION_LOG.md`

---

## Implementation Log

Maintain a running log in your project:

```
project/
├── .github/copilot-instructions.md
├── IMPLEMENTATION_LOG.md          ← Add this
├── src/
└── tests/
```

**What to track:**

```markdown
# Implementation Log: [Feature Name]

## [Date]: Planning Phase
**Objective**: What are we building?
**Requirements**: Acceptance criteria
**Technical Approach**: How we'll build it
**Key Decisions**: Important choices made

## [Date]: Implementation
**Completed**: What was done
**Files Modified**: Which files changed
**Code Locations**: Key code locations
**Issues Found**: Bugs discovered and fixed

## [Date]: Testing
**Test Coverage**: What was tested
**Issues Found**: Bugs and their fixes
**Performance**: Metrics and observations

## Next Steps
What needs to be done next
```

**Example:**

```markdown
# Implementation Log: Rate Limiting Feature

## 2026-02-01: Planning Phase
**Objective**: Add Redis-backed rate limiting to API

**Requirements**:
- 100 requests/minute per API key
- Return 429 when limit exceeded
- Include headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset

**Technical Approach**:
- Redis sliding window algorithm
- FastAPI middleware architecture
- Configuration via environment variables
- Graceful degradation if Redis unavailable

**Key Decisions**:
- Chose sliding window over fixed window to prevent burst traffic
- Decided to fail open (allow requests) if Redis down
- Using separate Redis instance from session cache

## 2026-02-02: Implementation
**Completed**:
- Created RateLimiter class in `src/middleware/rate_limiter.py`
- Implemented sliding window algorithm with Redis INCR + EXPIRE
- Added middleware to FastAPI app
- Configured limits per endpoint via `rate_limits.yaml`

**Code Locations**:
- Rate limiter logic: `src/middleware/rate_limiter.py:15-78`
- Middleware registration: `src/app.py:45-52`

**Files Modified**:
- `src/middleware/rate_limiter.py` (new)
- `src/app.py` (added middleware)
- `config/rate_limits.yaml` (new)

## 2026-02-03: Testing
**Test Coverage**:
- Unit tests for rate limiter logic (100% coverage)
- Integration tests with real Redis
- Load tests with 1000 concurrent requests

**Issues Found**:
- Off-by-one error in window calculation (fixed)
- Race condition in concurrent requests (fixed with Lua script)

**Performance**:
- Added ~1-2ms latency per request (Redis roundtrip)
- Tested at 10k req/s - no degradation

## Next Steps
- Update API documentation
- Create monitoring dashboard
- Deploy to staging for validation
```

---

## When You Hit Token Limits

Start a new session:

```
Read the IMPLEMENTATION_LOG.md and continue from where we left off.

We completed planning, implementation, and testing.
Next we need to create the monitoring dashboard and update documentation.
```

**Result:** AI has full context without needing entire conversation history.

---

# Part 6: The Complete Workflow

## Step-by-Step: Building a Feature

### Phase 1: Planning

```
@task-planner Implement rate limiting for our API using Redis.
Requirements: 100 requests/minute per API key, return 429 when exceeded,
include rate limit info in response headers.
```

**Output:** Detailed plan with requirements analysis, technical approach, step-by-step tasks, testing strategy, and risks.

**Your action:** Review the plan, answer clarification questions, refine approach.

---

### Phase 2: Implementation

```
@python-coder Implement the rate limiter according to the plan.
Use Redis with sliding window algorithm. Include type hints,
error handling, and logging.
```

**Output:** Production-ready code with type hints, error handling, logging, and config management.

---

### Phase 3: Testing

Select the implemented code, then:

```
/generate-unit-tests
```

**Output:** Comprehensive pytest suite with fixtures, parametrization, mocking, and edge cases.

**Your action:** Review tests, run them, fix any issues.

---

### Phase 4: Optimization

For PySpark code:
```
/optimize-pyspark
```

For general code:
```
/refactor-for-testability
```

---

### Phase 5: Logging & Observability

```
/add-comprehensive-logging
```

**Output:** Structured logging at function entry/exit, state transitions, and errors.

---

### Phase 6: Security Review

```
/security-review
```

**Output:** Identified vulnerabilities with severity levels and fix recommendations.

**Your action:** Address CRITICAL and IMPORTANT issues before proceeding.

---

### Phase 7: Code Review

```
@code-reviewer Review this implementation for issues,
security vulnerabilities, and improvements.
```

**Output:** Categorized feedback (CRITICAL, IMPORTANT, MINOR, NITPICK).

---

### Phase 8: Documentation

```
@readme-generator Update the README with documentation
for the rate limiting feature, including configuration
options and usage examples.
```

---

### Phase 9: Pull Request

```
@pr-description-generator Create a comprehensive PR description
for this rate limiting implementation.
```

**Output:** Complete PR description with summary, changes list, testing coverage, and deployment notes.

---

## The Story

**Why this workflow works:**

1. **Planning** forces thinking before coding
2. **Implementation** from clear plan reduces back-and-forth
3. **Testing** ensures quality immediately
4. **Optimization** happens after working code
5. **Security review** prevents vulnerabilities
6. **Code review** catches issues
7. **Documentation** is fresh and accurate
8. **PR description** is clear and comprehensive

Each step builds on the previous, creating confidence and quality.

---

# Part 7: Multi-Repository Setup

## The Problem

Teams work across multiple repositories:
- Backend (Python/FastAPI)
- Frontend (React/TypeScript)
- Infrastructure (Kubernetes/Terraform)

Each needs slightly different standards, but share core principles.

## The Solution

Place shared configuration in **workspace parent directory**:

```
workspace/
├── .github/
│   ├── copilot-instructions.md      ← Shared
│   └── copilot/
│       ├── agents/                   ← Shared
│       └── prompts/                  ← Shared
├── backend/                          ← Python repo
├── frontend/                         ← React repo
└── infrastructure/                   ← Terraform repo
```

VSCode **automatically loads from parent directories**. Each repo gets shared config + inherits agents/prompts.

---

## Shared copilot-instructions.md

```markdown
# Multi-Repository Workspace

## Overview

This workspace contains three repositories:
- **backend**: Python FastAPI data processing service
- **frontend**: React TypeScript user interface
- **infrastructure**: Kubernetes and Terraform configurations

**IMPORTANT**: When working on code, only modify files in the relevant
repository. Do not make changes outside the current repository directory.

---

## Shared Principles

All repositories follow:
- Clear, explicit code standards
- Type hints and docstrings
- Comprehensive error handling
- Security-first approach
- Automated testing requirements

---

## Backend (Python) Standards

### Tech Stack
- Python 3.11+, FastAPI, SQLAlchemy
- PostgreSQL, Redis
- pytest for testing
- Docker for containerization

### Code Standards
- PEP 8, type hints required
- Google-style docstrings
- Async/await for I/O operations
- Error handling with specific exceptions

### Testing
- Unit tests for all business logic
- Integration tests for API endpoints
- Minimum 80% coverage

---

## Frontend (React) Standards

### Tech Stack
- React 18+, TypeScript
- TailwindCSS for styling
- Jest for testing
- Webpack for bundling

### Code Standards
- TypeScript strict mode
- Functional components with hooks
- Prop validation with TypeScript
- ESLint configuration

### Testing
- Jest unit tests
- React Testing Library for components
- E2E tests with Playwright

---

## Infrastructure Standards

### Tech Stack
- Kubernetes 1.28+
- Terraform for IaC
- GCP as cloud provider

### Standards
- Resource limits always specified
- Health probes required
- Security contexts enforced
- Gitops workflow for deployments

---

## Security (All Repos)

- NEVER hardcode credentials
- Always use environment variables/secret managers
- Validate all external inputs
- Use parameterized queries
- Enable audit logging

```

---

## Per-Repository Customization

Each repo can have its own `.github/copilot-instructions.md` that **overrides** the shared version:

```
workspace/.github/copilot-instructions.md          ← Shared (base config)
backend/.github/copilot-instructions.md           ← Backend-specific (overrides)
frontend/.github/copilot-instructions.md          ← Frontend-specific (overrides)
infrastructure/.github/copilot-instructions.md    ← Infrastructure-specific (overrides)
```

---

# Getting Started Checklist

## Week 1: Setup

- [ ] Create `.github/` directory in your repository
- [ ] Copy `copilot-instructions.md` to `.github/copilot-instructions.md`
- [ ] Customize with your project details:
  - Project overview
  - Tech stack
  - Code standards
  - File organization
  - Current focus areas
- [ ] Create `.github/copilot/agents/` directory
- [ ] Create `.github/copilot/prompts/` directory

## Week 1: Add Agents

- [ ] Copy `python-coder.agent.md` to `.github/copilot/agents/`
- [ ] Copy `python-tester.agent.md` to `.github/copilot/agents/`
- [ ] Copy `code-reviewer.agent.md` to `.github/copilot/agents/`
- [ ] Add other agents as needed for your team

## Week 1: Add Prompts

- [ ] Copy `/generate-unit-tests.prompt.md` to `.github/copilot/prompts/`
- [ ] Copy `/security-review.prompt.md` to `.github/copilot/prompts/`
- [ ] Copy `/add-comprehensive-logging.prompt.md` to `.github/copilot/prompts/`
- [ ] Add other prompts as needed

## Week 2: Try It Out

- [ ] Reload VSCode window
- [ ] Test an agent: `@python-coder write a function to validate email`
- [ ] Test a prompt: Select code, then `/generate-unit-tests`
- [ ] Review generated code carefully

## Week 2: Team Training

- [ ] Share this guide with your team
- [ ] Demo the workflow on a small task
- [ ] Explain the story: why each step matters
- [ ] Address questions

## Ongoing: Iterate

- [ ] Update `copilot-instructions.md` based on feedback
- [ ] Create custom agents for team-specific needs
- [ ] Create prompts for your common patterns
- [ ] Track lessons learned in implementation logs

---

## Key Principles

1. **Be Explicit** - Directives work better than suggestions
2. **Role Specialization** - Different agents for different tasks
3. **Reusable Patterns** - Prompts encode common transformations
4. **Security First** - Always run `/security-review`
5. **Continuous Learning** - Update instructions as you learn
6. **Context Continuity** - Implementation logs preserve knowledge

---

## The Bottom Line

Treating AI systematically—with clear onboarding, specialized roles, reusable processes, and structured continuity—transforms it from an inconsistent tool into a reliable coding partner.

The breakthrough isn't about bigger AI. It's about explicit guidance, just like onboarding any new team member.

---

## Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [5 Tips for Better Custom Instructions](https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/)
- [Custom Agents in VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [GitHub Awesome Copilot](https://github.com/github/awesome-copilot)

---

**Document Version:** 1.0
**Created:** February 2026
**Last Updated:** February 2026

Share this document with your team and customize as needed.
