# Code style
- Avoid the following "AI Slop" patterns
    - Extra comments that a competent senior engineer wouldn’t add or is inconsistent with the rest of the codebase. This includes docstrings - if it's very obvious what a function, class or file does to a senior engineer, then do not add a docstring. Reserve docstrings for crucial information that is not really obvious by looking at the code. Avoid adding Args and Returns information in the docstrings.
    - Avoid extra defensive checks or try/catch blocks that are abnormal for that area of the codebase.
    - Avoid casting a variable to a different type to get around type issues (or other similar patterns).
    - Variables that are only used a single time right after declaration, prefer inlining the RHS.
    - Style or formatting that is inconsistent with the file.
    - Excessive emojis or emoticons unless it's in a README.md file. Do not add emojis in PR descriptions.
- Utilize software engineering principles like SOLID, DRY, KISS, YAGNI and others to write clean, solid and concise code. Think about whether the code you are adding adheres to coding style of the existing code in the repository
- Avoid adding copious amounts of code, and lean towards conciseness unless it cannot be helped.


# Debugging Issues
- When trying to debug an issue, do the following:
    1. Understand the issue from the ground up, and internalize it. We are not interested in workarounds, simplifications, or hacky patches.
    2. Lay out a plan for how you'll debug the issue.
    3. If you're running around in circles, stop and revise your plan.
    4. Prefer running small, constrained tests to validate the fixes rather than entire test suites, if it can be helped.
- Add comprehensive logging at critical points in the code to trace execution flow
  - Log function entry/exit with key parameters
  - Log intermediate results and state transitions
  - Use consistent prefixes like `[FUNCTION_NAME]` for easy grepping
  - Include relevant context: IDs, counts, sizes, status values


# Pull Request Descriptions
- Do not add emojis and emoticons in PR descriptions.
- Provide a small paragraph describing the entire change, and explain the individual changes below that in concise bullet points.
- Do not add "Created by Claude Code" or anything similar in the PR description.

# General Instructions
- You are allowed to write a maximum of 3 documents (md files) per session, UNLESS the user explicitly asks you to write a 4th or 5th document.
- For EVERY new project, you MUST create and maintain an IMPLEMENTATION_LOG.md file where you preserve a concise, chronological, running log of everything you have planned, implemented, debugged and tested in this project. The document should be written and updated in such a way that a senior engineer should just be able to glance at it and understand whatever has been done in this project until now. This file will also be used by future, new Claude sessions to obtain the required context to take over from where the previous session left off.

# Environment preferences
For any new environment, here are my preferences:
- I prefer poetry plus pyproject.toml for python package dependency management
- For UI, I prefer React with TailwindCSS unless something else makes better sense for the problem at hand

# Docker & Containerization
- ALL operations should be performed inside Docker containers - do NOT run anything outside of Docker unless explicitly requested
- Use `docker exec <container>` for all backend operations (alembic, poetry, python)
- Use `docker-compose` for orchestrating services
- When dependencies are added to package.json or pyproject.toml:
  - For backend: Rebuild container OR run `docker exec backend poetry install`
  - For frontend: Rebuild container OR run `docker exec frontend npm install`, then restart
- Service hostnames in containerized environments:
  - Use Docker service names (e.g., `postgres`, `redis`, `ollama`) NOT `localhost`
  - Only use `localhost` when connecting FROM the host machine TO containers

# Python/FastAPI Best Practices

## Async Database Operations (SQLAlchemy)
- **CRITICAL:** Never access lazy-loaded relationships outside async context
- Use `selectinload()` to eagerly load relationships when they'll be accessed later
- When creating new objects, avoid accessing relationships unless they're explicitly loaded
- Check conditions before accessing relationships: `if obj_id and obj.relationship:`
- For raw SQL with asyncpg:
  - With SQLAlchemy `text()`: Use positional parameters (`$1, $2`) with tuple/list arguments
  - When mixing with ORM operations: Use raw asyncpg connection via `session.connection()` to avoid parameter binding conflicts
  - Access asyncpg Record objects with dict-like syntax: `row["column"]` not `row.column`
  - SQLAlchemy session.execute() with text() and tuples will fail - use raw connection or dict parameters

## Database Migrations (Alembic)
- Always run migrations inside Docker: `docker exec backend poetry run alembic upgrade head`
- When adding models, import them in `alembic/env.py` for auto-detection
- Create migration: `docker exec backend poetry run alembic revision --autogenerate -m "description"`

## Error Handling
- Understand the root cause deeply before fixing - no workarounds or hacky patches
- For async/greenlet errors: Check if operations are in proper async context
- For connection errors: Verify Docker network hostnames are used, not localhost
- Test fixes with minimal, targeted tests before full integration
- When debugging transaction errors: Look for the ORIGINAL error before the transaction failure
  - Transaction errors like "InFailedSQLTransactionError" are symptoms, not root causes
  - Search logs for errors immediately preceding the transaction failure
  - The actual SQL error usually appears 5-20 lines before the transaction abort message

## Dependencies
- When resolving conflicts: Update to compatible versions across the entire dependency tree
- Use `poetry lock` to lock without upgrading everything
- Check for version compatibility between related packages (e.g., langchain, langgraph, langchain-openai)

# Testing & Validation
- Before claiming something works, actually test it end-to-end
- Don't just restart services and assume they're working - verify with actual requests
- Use curl or similar tools to validate API endpoints after changes
- Check Docker logs when things fail: `docker logs <container> --tail 50`
- For async issues, check the full stack trace to find the exact line causing problems
- When Python code changes don't take effect after container restart:
  - Use `docker-compose stop <service> && docker-compose start <service>` for clean restart
  - Verify changes are in container: `docker exec <container> cat /path/to/file.py | grep "pattern"`

## Data Validation
- Handle invalid data (NaN, infinity, null) explicitly before it reaches validation layers
- Use `math.isnan()` for NaN checks rather than equality comparisons
- For vector/embedding operations: Validate embeddings are non-zero before performing similarity calculations
