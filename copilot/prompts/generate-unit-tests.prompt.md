# Generate Unit Tests

Generate comprehensive unit tests for the selected code using pytest.

## Test Requirements

1. **Coverage**: Test happy path, edge cases, and error conditions
2. **Independence**: Each test should be independent and isolated
3. **Clarity**: Use descriptive test names that explain what is being tested
4. **AAA Pattern**: Structure tests as Arrange-Act-Assert
5. **Fixtures**: Use pytest fixtures for common setup
6. **Parametrize**: Use `@pytest.mark.parametrize` for testing multiple scenarios

## Test Naming Convention

Format: `test_<function>_<scenario>_<expected_result>`

Examples:
- `test_calculate_discount_with_valid_coupon_returns_discounted_price`
- `test_process_payment_with_insufficient_funds_raises_error`
- `test_parse_date_with_invalid_format_returns_none`

## Test Structure Template

```python
import pytest
from unittest.mock import Mock, patch
from mymodule import function_to_test

@pytest.fixture
def sample_data():
    """Provide sample test data."""
    return {"key": "value"}

@pytest.fixture
def mock_database():
    """Provide mocked database client."""
    return Mock()

class TestFunctionName:
    """Tests for function_name."""

    def test_function_with_valid_input_returns_expected_output(self, sample_data):
        # Arrange
        expected = "expected_value"

        # Act
        result = function_to_test(sample_data)

        # Assert
        assert result == expected

    @pytest.mark.parametrize("input_val,expected", [
        (0, 0),
        (5, 25),
        (10, 100),
        (-3, 9),
    ])
    def test_function_with_various_inputs_returns_correct_values(
        self, input_val, expected
    ):
        # Arrange & Act
        result = function_to_test(input_val)

        # Assert
        assert result == expected

    def test_function_with_invalid_input_raises_value_error(self):
        # Arrange
        invalid_input = None

        # Act & Assert
        with pytest.raises(ValueError, match="Input cannot be None"):
            function_to_test(invalid_input)

    @patch('mymodule.external_api')
    def test_function_with_mocked_dependency_calls_api_correctly(
        self, mock_api, mock_database
    ):
        # Arrange
        mock_api.get.return_value = {"data": "value"}

        # Act
        result = function_to_test(database=mock_database)

        # Assert
        mock_api.get.assert_called_once_with("/endpoint")
        assert result == {"data": "value"}
```

## Coverage Goals

For the selected code, generate tests covering:

1. **Happy Path**: Normal execution with valid inputs
2. **Edge Cases**:
   - Empty inputs (empty list, empty string, None)
   - Boundary values (0, negative numbers, very large numbers)
   - Single element vs multiple elements
3. **Error Cases**:
   - Invalid input types
   - Missing required parameters
   - Exceptions from dependencies
4. **Mocking**:
   - External API calls
   - Database operations
   - File I/O
   - Time-dependent behavior

Please generate comprehensive unit tests for the selected code.
