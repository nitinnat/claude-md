# GitHub Copilot Configuration for Data Engineering Projects

This directory contains custom configurations, agents, and prompts to enhance your GitHub Copilot experience in VSCode for data engineering, Python, PySpark, and Kubernetes development.

## Contents

- **copilot-instructions.md** - Repository-wide instructions that Copilot uses as context
- **agents/** - Custom AI agents with specialized personas
- **prompts/** - Reusable prompt templates for common tasks
- **examples/** - Example usage patterns

## Setup in VSCode

### 1. Place copilot-instructions.md

For **repository-level** instructions (shared with your team):
```
your-project/
├── .github/
│   └── copilot-instructions.md  ← Copy copilot-instructions.md here
```

For **workspace-level** instructions (across multiple repos):
```
your-workspace/
├── .github/
│   └── copilot-instructions.md
├── repo1/
├── repo2/
└── repo3/
```

For **user-level** instructions (personal, across all projects):
- Open VSCode Settings (Cmd/Ctrl + ,)
- Search for "Copilot Instructions"
- Add your instructions in the "GitHub > Copilot: Chat: Instruction File" setting

### 2. Using Custom Agents

Custom agents are specialized AI personas that follow specific roles and behaviors.

**To use an agent:**

1. Copy the agent file to `.github/copilot/agents/` in your repository:
   ```bash
   mkdir -p .github/copilot/agents
   cp copilot/agents/python-coder.agent.md .github/copilot/agents/
   ```

2. In VSCode Copilot Chat, invoke the agent with `@`:
   ```
   @python-coder implement a function to validate email addresses
   ```

**Available Agents:**
- `@python-coder` - Expert Python developer for data engineering
- `@python-tester` - Specialist in writing comprehensive pytest tests
- `@kubernetes-expert` - K8s deployment and configuration expert
- `@code-reviewer` - Code review and quality assessment
- `@task-planner` - Creates detailed implementation plans
- `@readme-generator` - Generates comprehensive documentation
- `@pr-description-generator` - Creates detailed PR descriptions

### 3. Using Custom Prompts

Custom prompts are reusable templates for common coding tasks.

**To use a prompt:**

1. Copy prompt files to `.github/copilot/prompts/` in your repository:
   ```bash
   mkdir -p .github/copilot/prompts
   cp copilot/prompts/*.prompt.md .github/copilot/prompts/
   ```

2. In VSCode Copilot Chat, invoke with `/`:
   ```
   # Select code first, then:
   /refactor-for-testability

   # Or:
   /optimize-pyspark
   ```

**Available Prompts:**
- `/refactor-for-testability` - Refactor code to be more testable
- `/optimize-pyspark` - Optimize PySpark code for performance
- `/add-comprehensive-logging` - Add appropriate logging
- `/generate-unit-tests` - Generate pytest unit tests
- `/security-review` - Perform security vulnerability review

## Usage Examples

### Example 1: Write Code with Python Coder Agent

```
@python-coder Write a PySpark function that reads a CSV file,
filters rows where age > 18, and writes the result to Parquet.
Include error handling and logging.
```

The agent will generate code following the project's standards defined in `copilot-instructions.md`.

### Example 2: Generate Tests for Existing Code

1. Select your function code in the editor
2. Open Copilot Chat
3. Type: `/generate-unit-tests`

The prompt will generate comprehensive pytest tests with fixtures, parametrization, and mocking.

### Example 3: Plan a Complex Feature

```
@task-planner I need to implement a data validation pipeline
that checks incoming data against a schema, logs validation errors,
and stores valid records in BigQuery. The pipeline should handle
millions of records daily.
```

The planner will create a detailed implementation plan with steps, file changes, and testing strategy.

### Example 4: Optimize PySpark Code

1. Select your PySpark code
2. Run: `/optimize-pyspark`
3. Review suggested optimizations (partitioning, caching, broadcast joins, etc.)

### Example 5: Code Review

1. Select the code you want reviewed
2. Use: `@code-reviewer Review this code for issues, security vulnerabilities, and improvements`
3. Get structured feedback with categories: CRITICAL, IMPORTANT, MINOR

## Workflow: Using Copilot for End-to-End Development

### 1. Planning Phase

```
@task-planner Implement rate limiting for our API using Redis.
Requirements: 100 requests/minute per API key, return 429 when exceeded.
```

Review the generated plan, ask clarifying questions if needed.

### 2. Implementation Phase

```
@python-coder Implement the rate limiter according to the plan.
Use Redis with sliding window algorithm.
```

### 3. Testing Phase

Select the implemented code, then:
```
/generate-unit-tests
```

Review and refine the generated tests.

### 4. Optimization Phase

```
/add-comprehensive-logging
```

Or for PySpark code:
```
/optimize-pyspark
```

### 5. Review Phase

```
@code-reviewer Review this implementation
```

And:
```
/security-review
```

### 6. Documentation Phase

```
@readme-generator Update the README with documentation
for the new rate limiting feature
```

### 7. PR Creation

```
@pr-description-generator Create a PR description for
the rate limiting implementation
```

## Working Across Multiple Repositories

If you work on multiple related repositories, place shared configuration in a parent directory:

```
workspace/
├── .github/
│   ├── copilot-instructions.md  ← Shared instructions
│   └── copilot/
│       ├── agents/               ← Shared agents
│       └── prompts/              ← Shared prompts
├── backend/                      ← Python/FastAPI repo
├── frontend/                     ← React repo
└── infrastructure/               ← Terraform/K8s repo
```

In your copilot-instructions.md, add:
```markdown
# Multi-Repository Workspace

This workspace contains multiple repositories:
- backend: Python FastAPI application
- frontend: React TypeScript application
- infrastructure: Kubernetes and Terraform configs

When working on code, only modify files in the relevant repository.
Do not make changes outside the current repository directory.
```

## Tips for Effective Use

1. **Be Specific**: The more context you provide, the better the results
2. **Iterate**: Refine prompts based on initial outputs
3. **Combine Approaches**: Use agents for complex tasks, prompts for quick transformations
4. **Update Instructions**: Keep `copilot-instructions.md` current as your project evolves
5. **Security First**: Always run `/security-review` before committing sensitive code
6. **Test Coverage**: Use `/generate-unit-tests` to maintain high test coverage
7. **Document as You Go**: Use `@readme-generator` to keep docs updated

## Security Best Practices

When using Copilot with these configurations:

- Never commit hardcoded secrets or credentials
- Always use environment variables for sensitive config
- Run security reviews on generated code
- Validate and sanitize all external inputs
- Use least-privilege IAM roles
- Enable audit logging for production deployments

## Customization

You can customize these files for your specific needs:

1. **Edit copilot-instructions.md** to match your project structure and standards
2. **Modify agents** to adjust expertise areas and constraints
3. **Create new prompts** for your team's common tasks
4. **Add examples** specific to your domain

## Troubleshooting

**Agent not working:**
- Ensure the .agent.md file is in `.github/copilot/agents/`
- Check that the file name matches the agent invocation (e.g., `python-coder.agent.md` → `@python-coder`)
- Restart VSCode

**Prompt not found:**
- Verify prompt file is in `.github/copilot/prompts/`
- Check file has `.prompt.md` extension
- Reload VSCode window

**Instructions not being followed:**
- Ensure `copilot-instructions.md` is in `.github/` directory
- Check file is named exactly `copilot-instructions.md`
- The file should be in the repository root's `.github/` folder

## Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Custom Instructions Guide](https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/)
- [Custom Agents in VSCode](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [Awesome Copilot Examples](https://github.com/github/awesome-copilot)
