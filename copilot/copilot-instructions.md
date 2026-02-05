# Project Instructions for GitHub Copilot

## Project Overview
This repository contains [brief description of your project - e.g., a data processing pipeline for analytics workloads]. The codebase is designed for scalability and maintainability, with a focus on clean code principles.

## Tech Stack
- **Primary Language**: Python 3.11+
- **Data Processing**: Apache Spark, PySpark
- **Cloud Platform**: GCP (Google Cloud Platform)
- **Container Orchestration**: Kubernetes
- **Data Storage**: BigQuery, Cloud Storage
- **Testing**: pytest, unittest
- **CI/CD**: GitHub Actions, Cloud Build

## Code Style and Standards

### Python Code Style
- Follow PEP 8 style guide
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use `black` for code formatting
- Use `pylint` and `mypy` for linting and type checking
- Prefer descriptive variable names over abbreviations

### Example:
```python
def process_customer_records(
    input_path: str,
    output_path: str,
    batch_size: int = 1000
) -> dict[str, Any]:
    """Process customer records from input to output location."""
    # Implementation
    pass
```

### Documentation
- All public functions and classes MUST have docstrings
- Use Google-style docstrings
- Include examples for complex functions
- Document exceptions that may be raised

### Example:
```python
def transform_data(df: DataFrame, config: dict) -> DataFrame:
    """Transform input DataFrame according to configuration.

    Args:
        df: Input PySpark DataFrame
        config: Transformation configuration dictionary

    Returns:
        Transformed DataFrame with applied rules

    Raises:
        ValueError: If config is missing required fields
        DataValidationError: If input data doesn't meet schema requirements

    Example:
        >>> config = {"remove_nulls": True, "dedupe": True}
        >>> result_df = transform_data(input_df, config)
    """
    pass
```

### Error Handling
- Use specific exception types, not bare `except` clauses
- Always log errors with context before raising or re-raising
- For production code, include error recovery mechanisms
- Use context managers (`with` statements) for resource management

### Testing
- Write unit tests for all business logic
- Use pytest fixtures for test setup
- Aim for >80% code coverage
- Name test functions descriptively: `test_<function>_<scenario>_<expected_result>`
- Use parametrize for testing multiple scenarios

### Example:
```python
@pytest.mark.parametrize("input_value,expected", [
    (10, 100),
    (5, 25),
    (0, 0),
])
def test_square_function_returns_correct_value(input_value, expected):
    assert square(input_value) == expected
```

## PySpark Best Practices
- Avoid `.collect()` on large DataFrames - use `.show()` or `.take()`
- Use DataFrame API over RDD API
- Partition DataFrames appropriately before joins
- Cache DataFrames only when reused multiple times
- Use `.repartition()` before writing large outputs

## Kubernetes Deployment
- All deployments must specify resource limits and requests
- Use ConfigMaps for configuration, Secrets for sensitive data
- Include health check probes (liveness and readiness)
- Use namespaces for environment isolation (dev, staging, prod)

## Security Guidelines
- NEVER hardcode credentials or API keys
- Use GCP Secret Manager for sensitive configuration
- Validate and sanitize all external inputs
- Use least-privilege IAM roles
- Enable audit logging for all data access

## File Organization
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

## Common Commands

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v --cov=src

# Format code
black src/ tests/

# Type check
mypy src/

# Lint
pylint src/
```

### Deployment
```bash
# Build Docker image
docker build -t <image-name>:latest .

# Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml

# Check pod status
kubectl get pods -n <namespace>
```

## Important Notes
- Always run tests before committing code
- Use feature branches and pull requests for all changes
- Update documentation when adding new features
- Run `black` and `mypy` before pushing code
- Never commit directly to `main` branch

## Current Focus Areas
[Update this section as the project evolves]
- Implementing real-time data processing pipeline
- Optimizing BigQuery query performance
- Enhancing error handling and retry logic
