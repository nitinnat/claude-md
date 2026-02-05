# Sample Code for IDE Demonstrations

Use these code examples during your presentation to demonstrate Copilot agents and prompts.

---

## Demo 1: @python-coder Agent

### Task to Show
```
@python-coder Write a function to validate customer email addresses.
Include type hints, error handling, logging, and support for both
standard emails and + addressing.
```

### Expected Output (What They'll See)

```python
import logging
import re
from typing import Tuple

logger = logging.getLogger(__name__)

def validate_email(email: str) -> Tuple[bool, str]:
    """Validate customer email address format.

    Supports standard email format and + addressing.

    Args:
        email: Email address to validate

    Returns:
        Tuple of (is_valid, error_message)

    Raises:
        ValueError: If email is None or empty

    Example:
        >>> is_valid, msg = validate_email("user@example.com")
        >>> print(is_valid)
        True
    """
    logger.info(f"[validate_email] Starting validation for email: {email[:10]}...")

    if not email:
        logger.warning("[validate_email] Email is empty")
        raise ValueError("Email cannot be empty")

    # Standard email regex pattern
    email_pattern = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    try:
        if re.match(email_pattern, email.lower()):
            logger.info("[validate_email] Email validation successful")
            return True, ""
        else:
            error_msg = "Email format is invalid"
            logger.warning(f"[validate_email] {error_msg}")
            return False, error_msg
    except Exception as e:
        logger.error(f"[validate_email] Validation failed: {str(e)}", exc_info=True)
        raise
```

### What to Point Out
- ✅ Type hints on input and output
- ✅ Comprehensive docstring with example
- ✅ Specific exception types
- ✅ Logging at entry/exit and errors
- ✅ Email masking in logs for security
- ✅ Follows project standards immediately

---

## Demo 2: @python-tester Agent

### Task to Show
```
@python-tester Generate unit tests for the validate_email function.
Include happy path, edge cases, invalid formats, and error conditions.
Use pytest parametrization.
```

### Expected Output

```python
import pytest
from app.validators import validate_email, ValidationError

class TestValidateEmail:
    """Tests for validate_email function."""

    @pytest.mark.parametrize("email,expected", [
        ("user@example.com", True),
        ("john.doe+tag@company.co.uk", True),
        ("test_123@sub.domain.com", True),
        ("user+tag@domain.com", True),
    ])
    def test_validate_email_with_valid_formats(self, email, expected):
        is_valid, _ = validate_email(email)
        assert is_valid == expected

    @pytest.mark.parametrize("email", [
        "invalid.email",
        "user@",
        "@example.com",
        "user @example.com",
        "user@.com",
        "",
        "user@domain",
    ])
    def test_validate_email_with_invalid_formats(self, email):
        if email == "":
            with pytest.raises(ValueError):
                validate_email(email)
        else:
            is_valid, error_msg = validate_email(email)
            assert is_valid is False
            assert len(error_msg) > 0

    def test_validate_email_with_none_raises_error(self):
        with pytest.raises(ValueError, match="Email cannot be empty"):
            validate_email(None)

    def test_validate_email_is_case_insensitive(self):
        is_valid_lower, _ = validate_email("user@example.com")
        is_valid_upper, _ = validate_email("USER@EXAMPLE.COM")
        assert is_valid_lower == is_valid_upper == True

    def test_validate_email_with_special_chars_at_position(self):
        # Test + addressing in local part
        is_valid, _ = validate_email("user+filter+tag@example.com")
        assert is_valid is True
```

### What to Point Out
- ✅ Parametrized tests for multiple scenarios
- ✅ Descriptive test names
- ✅ AAA pattern (Arrange-Act-Assert)
- ✅ Edge cases covered
- ✅ Error conditions tested
- ✅ Fixtures for setup
- ✅ All done automatically

---

## Demo 3: /generate-unit-tests Prompt

### Setup
```python
# In your editor, have this simple function:

def calculate_discount(price: float, discount_percent: int) -> float:
    """Calculate discounted price.

    Args:
        price: Original price
        discount_percent: Discount percentage (0-100)

    Returns:
        Final price after discount
    """
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")

    return price * (1 - discount_percent / 100)
```

### Demo Steps
1. Select all the code
2. Open Copilot Chat
3. Type `/generate-unit-tests`
4. Show generated tests

### Expected Tests Generated
```python
import pytest
from app.pricing import calculate_discount

class TestCalculateDiscount:
    """Tests for calculate_discount function."""

    @pytest.mark.parametrize("price,discount,expected", [
        (100, 0, 100),
        (100, 50, 50),
        (100, 100, 0),
        (75.50, 20, 60.4),
    ])
    def test_calculate_discount_with_valid_inputs(self, price, discount, expected):
        result = calculate_discount(price, discount)
        assert pytest.approx(result) == expected

    def test_calculate_discount_with_zero_price(self):
        result = calculate_discount(0, 50)
        assert result == 0

    def test_calculate_discount_with_negative_discount_raises_error(self):
        with pytest.raises(ValueError, match="Discount must be between"):
            calculate_discount(100, -10)

    def test_calculate_discount_with_discount_over_100_raises_error(self):
        with pytest.raises(ValueError, match="Discount must be between"):
            calculate_discount(100, 150)

    def test_calculate_discount_with_float_price(self):
        result = calculate_discount(99.99, 10)
        assert pytest.approx(result) == 89.991
```

---

## Demo 4: /security-review Prompt

### Vulnerable Code to Show
```python
# Show this code and run /security-review on it

def get_user_data(user_id):
    import sqlite3

    # WARNING: SQL Injection vulnerability!
    query = f"SELECT * FROM users WHERE id = {user_id}"

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(query)

    # WARNING: Hardcoded credentials
    api_key = "sk-1234567890abcdef"
    headers = {"Authorization": f"Bearer {api_key}"}

    # WARNING: Logging sensitive data
    logger.info(f"User data retrieved: {cursor.fetchone()}")

    return cursor.fetchone()
```

### Demo Steps
1. Show code in editor
2. Select all
3. Open Copilot Chat
4. Type `/security-review`
5. Show identified vulnerabilities

### Expected Output
```
## Security Issues Found

### CRITICAL
- **SQL Injection** (Line 8): Direct string interpolation in query
  Fix: Use parameterized queries

- **Hardcoded Credentials** (Line 12): API key in source code
  Fix: Move to environment variable

### HIGH
- **PII in Logs** (Line 17): User data logged without redaction
  Fix: Only log user_id, not full user object

### MEDIUM
- **Missing Input Validation** (Line 3): user_id not validated before use
  Fix: Validate user_id type and range
```

---

## Demo 5: @code-reviewer Agent

### Code to Review
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

### Demo Steps
1. Select code
2. Open Copilot Chat
3. Type `@code-reviewer Review this code`
4. Show feedback

### Expected Feedback
```
## Code Review

### CRITICAL
- **Bare except clause** (Line 6): Never use bare except
  Impact: Catches system exceptions you don't want
  Fix: except KeyError: (be specific)

### IMPORTANT
- **Missing type hints** (Line 1): All functions need type hints
  Impact: IDE can't provide autocomplete, errors unclear
  Fix: def process_orders(orders_data: list[dict]) -> float:

- **Unclear variable names** (Line 2): 'total' could be 'total_amount'
  Impact: Reduces code clarity

- **No logging** (Line 7): Silent failures make debugging hard
  Impact: Can't track what went wrong in production
  Fix: logger.warning(f"Invalid order: {order}")

- **No docstring** (Line 1): Functions must have docstrings
  Impact: Team doesn't know what this does
  Fix: Add docstring with Args, Returns, Raises

### MINOR
- **Inefficient loop** (Line 4): Use sum() instead
  Better: return sum(o['amount'] for o in orders_data if 'amount' in o)
```

---

## Demo 6: @task-planner Agent

### Task to Show
```
@task-planner Create a plan for implementing rate limiting on our API.

Requirements:
- 100 requests per minute per API key
- Return 429 Too Many Requests when exceeded
- Include rate limit headers in responses
- Log rate limit violations
```

### Expected Plan Output
```
## Implementation Plan: Rate Limiting

### Requirements Analysis
**Goal**: Prevent API abuse while maintaining service availability

**Acceptance Criteria**:
- ✅ Enforce 100 req/min per API key
- ✅ Return 429 status code when exceeded
- ✅ Include rate limit headers in all responses
- ✅ Log violations for monitoring

**Clarifying Questions**:
1. Should limits differ by user tier (free/premium)?
2. Should we use sliding window or fixed window?
3. Is in-memory sufficient or do we need Redis?

### Technical Approach
**Solution**: Redis-backed rate limiting with sliding window

**Why this approach**:
- Sliding window prevents burst traffic at boundaries
- Redis allows distributed deployments
- Fast O(1) operations
- Easy to adjust limits per endpoint

**Alternatives Considered**:
- In-memory: Simpler but doesn't work across instances
- Fixed window: Easier but allows bursts at boundaries

### Implementation Steps

#### Step 1: Create RateLimiter class (MEDIUM)
File: `src/middleware/rate_limiter.py`
- Implement sliding window algorithm
- Use Redis INCR and EXPIRE operations
- Handle Redis connection failures gracefully

#### Step 2: Add FastAPI middleware (SMALL)
File: `src/app.py`
- Register RateLimiter middleware
- Configure limits per endpoint
- Add rate limit headers to responses

#### Step 3: Configuration (SMALL)
File: `config/rate_limits.yaml`
- Define per-endpoint limits
- Set Redis connection parameters
- Configure logging

#### Step 4: Testing (MEDIUM)
- Unit tests for rate limiter logic
- Integration tests with Redis
- Load tests for concurrent requests

### Testing Strategy
- Unit: Test rate limiter with mocked Redis
- Integration: Test with real Redis
- Load: Test with 1000 concurrent requests

### Risks & Mitigations
- Redis unavailable → Fail open (allow requests)
- Clock skew → Use server time only
- Memory issues → Clean up expired keys
```

---

## Demo 7: Complete Workflow (Optional 10-min demo)

If you want to show the entire workflow, use this task:

```
@task-planner Create a plan for adding email notification to customer records.

Requirements:
- Send email when customer creates account
- Include verification link
- Handle email bounce errors
- Log all notification attempts
```

Then follow through:
1. Plan → Show the plan
2. Implement → `@python-coder implement notification service`
3. Test → Select code, `/generate-unit-tests`
4. Review → `@code-reviewer review this`
5. Security → `/security-review`
6. Logging → `/add-comprehensive-logging`

---

## Setup for Your Demo Repository

Create this structure to demo against:

```
your-project/
├── .github/
│   └── copilot-instructions.md
├── src/
│   ├── __init__.py
│   ├── validators.py              # Paste validate_email here
│   ├── pricing.py                 # Paste calculate_discount here
│   └── app.py
├── tests/
│   ├── test_validators.py         # Paste unit tests here
│   └── test_pricing.py
└── requirements.txt
```

---

## Tips for Smooth Demos

1. **Have code ready** - Paste examples from this file to save time
2. **Show file structure** - Briefly show .github/copilot-instructions.md is in place
3. **Explain before demo** - Tell them what prompt you're about to run
4. **Pause for questions** - After each demo, ask if they understand
5. **Show the full output** - Don't rush through - let them see what's generated
6. **Point out details** - Highlight type hints, error handling, logging, etc.

---

## Transition Between Slides and IDE

**Pattern for each demo:**

1. **Slide**: Show what you're about to do (the concept)
2. **Explain**: Talk about why this matters
3. **IDE**: Show the actual code/demo
4. **Point out**: What's good about the output
5. **Back to slide**: Move to next section

**Example**:
- Slide: "Python Coder Agent - writes production code"
- Talk: "Notice how it includes type hints, docstrings, logging, error handling"
- IDE: Paste example code, show Copilot output
- Point: "Look at the docstring with examples, the logging strategy, the error handling"
- Next: "Any questions? Let's look at testing..."

---

## Demo Timing

- **Intro**: 5 min
- **Part 1 (instructions)**: 5 min
- **Part 2 (agents)**: 15 min (3-5 agents × 3-5 min each)
- **Part 3 (prompts)**: 10 min (2-3 prompts × 4-5 min each)
- **Part 4 (security)**: 5 min
- **Part 5 (workflow)**: 10 min (show end-to-end)
- **Part 6 (context)**: 3 min
- **Part 7 (multi-repo)**: 2 min
- **Q&A**: 5 min

**Total: ~60 minutes for complete demo**

---

## What to Have Open

During presentation:

1. **VS Code with demo project** - Ready to switch to
2. **GitHub Copilot Chat** - Open and ready
3. **Sample files** - All examples in editor tabs
4. **Presentation slides** - This file in another monitor/window

Alt+Tab smoothly between slides and IDE for best effect.
