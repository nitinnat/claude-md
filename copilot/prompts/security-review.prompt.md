# Security Review

Perform a security review of the selected code and identify potential vulnerabilities.

## Security Checklist

### 1. Input Validation
- [ ] All external inputs are validated
- [ ] SQL injection prevention (parameterized queries)
- [ ] Command injection prevention
- [ ] Path traversal prevention
- [ ] XSS prevention (if web application)

### 2. Authentication & Authorization
- [ ] Authentication properly implemented
- [ ] Authorization checks in place
- [ ] No hardcoded credentials
- [ ] Secure password storage (hashing + salt)
- [ ] Session management secure

### 3. Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] Sensitive data encrypted in transit (HTTPS/TLS)
- [ ] No logging of sensitive information
- [ ] PII handled according to regulations

### 4. Error Handling
- [ ] Errors don't expose sensitive information
- [ ] Stack traces not exposed to users
- [ ] Proper exception handling

### 5. Dependencies
- [ ] Dependencies are up to date
- [ ] No known vulnerabilities in dependencies
- [ ] Minimal dependencies (reduce attack surface)

## Common Vulnerabilities to Check

### SQL Injection
```python
# ❌ VULNERABLE
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)

# ✅ SAFE - Parameterized query
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))
```

### Command Injection
```python
# ❌ VULNERABLE
os.system(f"ping {user_input}")

# ✅ SAFE - Use list arguments
subprocess.run(["ping", user_input], check=True)
```

### Path Traversal
```python
# ❌ VULNERABLE
file_path = f"/var/data/{user_provided_filename}"
with open(file_path) as f:
    content = f.read()

# ✅ SAFE - Validate and sanitize
import os
base_dir = "/var/data"
safe_path = os.path.normpath(os.path.join(base_dir, user_provided_filename))
if not safe_path.startswith(base_dir):
    raise ValueError("Invalid file path")
with open(safe_path) as f:
    content = f.read()
```

### Hardcoded Secrets
```python
# ❌ VULNERABLE
API_KEY = "sk-1234567890abcdef"
db_password = "super_secret_password"

# ✅ SAFE - Use environment variables or secret management
import os
API_KEY = os.environ.get("API_KEY")
db_password = secret_manager.get_secret("db_password")
```

### Insecure Deserialization
```python
# ❌ VULNERABLE - pickle can execute arbitrary code
import pickle
data = pickle.loads(untrusted_input)

# ✅ SAFE - Use JSON for untrusted data
import json
data = json.loads(untrusted_input)
```

### Insufficient Logging & Monitoring
```python
# ❌ INSUFFICIENT
try:
    perform_sensitive_operation()
except Exception:
    pass  # Silent failure

# ✅ PROPER
import logging
logger = logging.getLogger(__name__)

try:
    perform_sensitive_operation()
    logger.info("Sensitive operation completed", extra={"user_id": user_id})
except Exception as e:
    logger.error(
        f"Sensitive operation failed: {str(e)}",
        extra={"user_id": user_id},
        exc_info=True
    )
    raise
```

## Review Output Format

```markdown
## Security Issues Found

### Critical
- [CRITICAL] Hardcoded API key in line 45
- [CRITICAL] SQL injection vulnerability in line 78

### High
- [HIGH] User input not validated before file operation (line 102)
- [HIGH] Sensitive data logged in plaintext (line 134)

### Medium
- [MEDIUM] Missing rate limiting on API endpoint
- [MEDIUM] Error messages expose internal paths

### Low
- [LOW] Dependency 'requests' is outdated (security patches available)

## Recommendations

1. **Immediate Actions** (Critical/High):
   - Move API key to environment variable
   - Use parameterized SQL queries
   - Add input validation for file paths
   - Remove sensitive data from logs

2. **Follow-up Actions** (Medium/Low):
   - Implement rate limiting
   - Sanitize error messages
   - Update dependencies
```

Please perform a security review of the selected code and report any vulnerabilities.
