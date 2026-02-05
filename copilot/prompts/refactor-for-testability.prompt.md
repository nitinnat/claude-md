# Refactor for Testability

Analyze the selected code and refactor it to make it more testable. Focus on:

1. **Dependency Injection**: Replace hardcoded dependencies with injectable parameters
2. **Pure Functions**: Separate pure logic from side effects (I/O, external calls)
3. **Single Responsibility**: Break down large functions into smaller, focused units
4. **Remove Hidden Dependencies**: Make all dependencies explicit

## Example

**Before**:
```python
def process_user_data(user_id):
    db = Database.connect()  # Hard dependency
    user = db.get_user(user_id)
    api_result = requests.get(f"https://api.example.com/user/{user_id}")  # HTTP call
    processed = complex_transformation(user, api_result.json())
    db.save(processed)
    return processed
```

**After**:
```python
def process_user_data(
    user_id: str,
    db_client: DatabaseClient,
    api_client: APIClient
) -> ProcessedUser:
    """Process user data with injected dependencies."""
    user = db_client.get_user(user_id)
    api_data = api_client.fetch_user_data(user_id)
    return transform_user_data(user, api_data)

def transform_user_data(user: User, api_data: dict) -> ProcessedUser:
    """Pure function - easy to test."""
    # Transformation logic here
    pass
```

Now the code can be tested with mocked dependencies and the transformation logic can be unit tested in isolation.

Please refactor the selected code following these principles.
