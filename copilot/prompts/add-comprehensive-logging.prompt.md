# Add Comprehensive Logging

Add appropriate logging to the selected code following these guidelines:

## Logging Principles

1. **Log at Function Entry/Exit**: For critical functions, log when they start and complete
2. **Log Important State Changes**: Track state transitions and significant events
3. **Include Context**: Add relevant IDs, counts, timestamps to log messages
4. **Use Appropriate Levels**:
   - `DEBUG`: Detailed diagnostic information
   - `INFO`: General informational messages (normal operation)
   - `WARNING`: Unexpected but handled situations
   - `ERROR`: Error events that might still allow the application to continue
   - `CRITICAL`: Serious errors causing the application to abort

## Logging Patterns

### Function Entry/Exit
```python
import logging

logger = logging.getLogger(__name__)

def process_records(records: list[dict]) -> ProcessResult:
    logger.info(f"[process_records] Starting processing {len(records)} records")

    try:
        result = _do_processing(records)
        logger.info(
            f"[process_records] Completed successfully. "
            f"Processed: {result.success_count}, Failed: {result.error_count}"
        )
        return result
    except Exception as e:
        logger.error(f"[process_records] Processing failed: {str(e)}", exc_info=True)
        raise
```

### State Transitions
```python
def deploy_model(model_id: str, environment: str):
    logger.info(f"[deploy_model] Deploying model {model_id} to {environment}")

    logger.debug(f"[deploy_model] Validating model {model_id}")
    validate_model(model_id)

    logger.info(f"[deploy_model] Building container for model {model_id}")
    container = build_container(model_id)

    logger.info(f"[deploy_model] Pushing container {container.id} to registry")
    push_to_registry(container)

    logger.info(f"[deploy_model] Deploying to {environment}")
    deployment = create_deployment(container, environment)

    logger.info(
        f"[deploy_model] Model {model_id} successfully deployed "
        f"to {environment} as {deployment.url}"
    )
```

### Error Handling with Context
```python
def fetch_user_data(user_id: str) -> UserData:
    try:
        logger.debug(f"[fetch_user_data] Fetching data for user {user_id}")
        data = api.get_user(user_id)
        logger.debug(f"[fetch_user_data] Successfully fetched {len(data)} fields")
        return data
    except APIError as e:
        logger.error(
            f"[fetch_user_data] API error fetching user {user_id}: "
            f"status={e.status_code}, message={e.message}"
        )
        raise
    except TimeoutError as e:
        logger.warning(
            f"[fetch_user_data] Timeout fetching user {user_id}, "
            f"will retry with fallback"
        )
        return fetch_from_cache(user_id)
```

## What to Log

✅ **Do Log**:
- Function entry with key parameters
- Completion with results/metrics
- State changes
- External API calls (with sanitized params)
- Errors with full context
- Performance metrics for critical paths

❌ **Don't Log**:
- Passwords, API keys, tokens
- Personal identifiable information (PII) unless necessary and approved
- Excessive debug info in tight loops (causes performance issues)
- Complete request/response bodies (log relevant fields instead)

Please add appropriate logging to the selected code.
