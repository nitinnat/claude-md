---
name: add-google-auth
description: Add Google OAuth authentication to an existing FastAPI + React project. Use when the user says "add auth", "add login", "protect this app", "add Google OAuth", or "I want only me to be able to access this". Adds session-based auth gated to a single allowed email. Detects what already exists and only adds what's missing.
---

# Add Google OAuth Authentication

**Announce:** "Using add-google-auth skill to add Google OAuth to this project."

## What This Skill Adds

- FastAPI: `SessionMiddleware`, `api/settings.py`, `api/deps.py`, `api/routers/auth.py`
- React: `AuthGate.jsx`, `Login.jsx`, `App.jsx` wrapping, `api.js` auth methods
- `.env` vars with `DASHBOARD_` prefix (matches EmailCollie convention)
- Manual steps for Google Cloud Console setup

All env vars use the `DASHBOARD_` prefix (`DASHBOARD_GOOGLE_CLIENT_ID`, etc.).

---

## Phase 1: Detect What Exists

Read the following files and note what is already present. **Skip generating any file or section that already exists.**

| File | What to check |
|---|---|
| `api/main.py` | `SessionMiddleware` imported/added? `require_auth` imported? `auth.router` mounted? |
| `api/settings.py` | `DashboardSettings` class exists? |
| `api/deps.py` | `require_auth` function exists? |
| `api/routers/auth.py` | Exists at all? |
| `frontend/src/AuthGate.jsx` | Exists? |
| `frontend/src/views/Login.jsx` | Exists? |
| `frontend/src/App.jsx` | Wrapped with `<AuthGate>`? |
| `frontend/src/api.js` | Has `api.auth.me` and `api.auth.logout`? |
| `.env` | Has `DASHBOARD_GOOGLE_CLIENT_ID`? |
| `pyproject.toml` | Has `google-auth-oauthlib`, `pydantic-settings`? |

After scanning, tell the user: "Found: [list what exists]. Will add: [list what's missing]."

---

## Phase 2: Ask the User

Ask in a single message:

```
To set up auth, I need one detail:

1. What's the app name? (shown on the login page, e.g., "EmailCollie")
2. What email should be allowed to log in? (e.g., you@gmail.com)
3. What's the public URL this will be accessed from?
   - Local dev only: http://localhost:8000
   - Cloudflare Tunnel: https://myapp.yourdomain.com
```

---

## Phase 3: Generate Files

Generate all files below, filling in `{{PLACEHOLDERS}}` with actual values. Skip any file that already fully exists.

---

### `api/settings.py`

```python
import secrets
from pathlib import Path

from pydantic_settings import BaseSettings


class DashboardSettings(BaseSettings):
    model_config = {"env_prefix": "DASHBOARD_"}

    auth_enabled: bool = True
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = ""
    allowed_email: str = ""
    session_secret: str = ""
    session_ttl_seconds: int = 86400
    https_only: bool = False
    cors_origins: str = "http://localhost:5173"

    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    def ensure_session_secret(self) -> str:
        if self.session_secret:
            return self.session_secret
        secret_file = Path(".session_secret")
        if secret_file.exists():
            self.session_secret = secret_file.read_text().strip()
            return self.session_secret
        generated = secrets.token_urlsafe(48)
        secret_file.write_text(generated)
        self.session_secret = generated
        return self.session_secret


settings = DashboardSettings()
```

---

### `api/deps.py`

```python
import time

from fastapi import HTTPException, Request, status

from api.settings import settings


def require_auth(request: Request) -> dict:
    if not settings.auth_enabled:
        return {"email": "disabled"}

    user = request.session.get("user")
    expires_at = request.session.get("expires_at")
    if not user or not expires_at:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    if time.time() > float(expires_at):
        request.session.clear()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired"
        )

    return user
```

---

### `api/routers/auth.py`

```python
import os
import secrets
import time
from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException, Request
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from starlette.responses import RedirectResponse

from api.settings import settings

router = APIRouter()

_SCOPES = ["openid", "email", "profile"]


def _client_config() -> dict:
    if not (settings.google_client_id and settings.google_client_secret):
        raise HTTPException(status_code=500, detail="OAuth credentials not configured")
    return {
        "web": {
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [settings.google_redirect_uri],
        }
    }


def _safe_next(path: str | None) -> str:
    if not path:
        return "/"
    parsed = urlparse(path)
    if parsed.scheme or parsed.netloc:
        origin = f"{parsed.scheme}://{parsed.netloc}"
        if origin in settings.cors_origin_list():
            return path
        return "/"
    return parsed.path or "/"


@router.get("/login")
def login(request: Request, next: str | None = None):
    if not settings.auth_enabled:
        return {"message": "auth disabled"}

    if request.url.hostname in {"localhost", "127.0.0.1"}:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

    config = _client_config()
    flow = Flow.from_client_config(config, scopes=_SCOPES)
    flow.redirect_uri = settings.google_redirect_uri
    request.session["redirect_uri"] = settings.google_redirect_uri
    request.session["next"] = _safe_next(next)

    state = secrets.token_urlsafe(32)
    _, returned_state = flow.authorization_url(
        state=state, access_type="online", prompt="select_account"
    )
    request.session["oauth_state"] = returned_state

    authorization_url, _ = flow.authorization_url(
        state=returned_state, access_type="online", prompt="select_account"
    )
    return RedirectResponse(authorization_url)


@router.get("/callback")
def callback(request: Request):
    if not settings.auth_enabled:
        return {"message": "auth disabled"}

    if request.url.hostname in {"localhost", "127.0.0.1"}:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

    state = request.session.get("oauth_state")
    if not state:
        raise HTTPException(status_code=400, detail="Missing OAuth state")

    config = _client_config()
    flow = Flow.from_client_config(config, scopes=_SCOPES, state=state)
    redirect_uri = request.session.get("redirect_uri") or settings.google_redirect_uri
    flow.redirect_uri = redirect_uri

    authorization_response = str(request.url)
    # Reverse proxy (e.g. Cloudflare Tunnel) terminates TLS; rewrite scheme if needed.
    if authorization_response.startswith("http://") and redirect_uri.startswith("https://"):
        authorization_response = "https://" + authorization_response[len("http://"):]

    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    id_token_value = getattr(credentials, "id_token", None)
    if not id_token_value:
        raise HTTPException(status_code=400, detail="Missing id_token")

    info = id_token.verify_oauth2_token(
        id_token_value,
        google_requests.Request(),
        config["web"]["client_id"],
    )

    email = (info.get("email") or "").lower()
    allowed = settings.allowed_email.lower()
    if allowed and email != allowed:
        request.session.clear()
        raise HTTPException(status_code=403, detail="Email not authorized")

    request.session["user"] = {
        "email": email,
        "name": info.get("name", ""),
        "picture": info.get("picture", ""),
        "sub": info.get("sub", ""),
    }
    request.session["expires_at"] = time.time() + settings.session_ttl_seconds

    next_path = request.session.pop("next", "/")
    request.session.pop("oauth_state", None)
    return RedirectResponse(next_path or "/")


@router.get("/me")
def me(request: Request):
    if not settings.auth_enabled:
        return {"email": "disabled"}
    user = request.session.get("user")
    expires_at = request.session.get("expires_at")
    if not user or not expires_at or time.time() > float(expires_at):
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"ok": True}
```

---

### `api/main.py` — edits needed

Make these additions to the existing `main.py`. Do not remove anything that exists.

**Add imports** (merge with existing imports):
```python
from fastapi import Depends
from starlette.middleware.sessions import SessionMiddleware
from api.deps import require_auth
from api.settings import settings
from api.routers import auth  # add to existing router imports
```

**Add middleware** (before any `app.include_router` calls):
```python
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.ensure_session_secret(),
    same_site="lax",
    https_only=settings.https_only,
    max_age=settings.session_ttl_seconds,
)
```

If `CORSMiddleware` is already present, update its `allow_origins` to use `settings.cors_origin_list()`.

**Mount auth router** (no auth dependency — this must be unprotected):
```python
app.include_router(auth.router, prefix="/api/auth")
```

**Add `Depends(require_auth)` to all other existing routers:**
```python
# For every existing app.include_router(...) call that is NOT auth, add:
app.include_router(
    existing_router.router,
    prefix="/api/existing",
    dependencies=[Depends(require_auth)],
)
```

---

### `frontend/src/AuthGate.jsx`

```jsx
import { useEffect, useState } from 'react'
import { api } from './api'
import Login from './views/Login'

export default function AuthGate({ children }) {
  const [loading, setLoading] = useState(true)
  const [user, setUser] = useState(null)

  useEffect(() => {
    api.auth.me()
      .then((u) => { setUser(u); setLoading(false) })
      .catch(() => { setUser(null); setLoading(false) })
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-sm text-gray-400">Checking session…</p>
      </div>
    )
  }

  if (!user || user.detail || !user.email || user.email === 'disabled') {
    if (user?.email === 'disabled') return children
    return <Login />
  }

  return children
}
```

---

### `frontend/src/views/Login.jsx`

```jsx
export default function Login() {
  const login = () => {
    const next = window.location.origin + window.location.pathname + window.location.search
    const isDev = window.location.port === '5173'
    const apiBase = isDev
      ? `${window.location.protocol}//${window.location.hostname}:8000`
      : ''
    window.location.href = `${apiBase}/api/auth/login?next=${encodeURIComponent(next)}`
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="p-8 max-w-sm w-full border rounded-lg">
        <h2 className="text-2xl font-bold mb-2">{{APP_NAME}}</h2>
        <p className="text-sm text-gray-500 mb-6">Sign in with Google to continue.</p>
        <button
          onClick={login}
          className="w-full px-4 py-2 border rounded text-sm hover:bg-gray-50 transition-colors"
        >
          Continue with Google
        </button>
      </div>
    </div>
  )
}
```

NOTE: The login page styling above is minimal and intentionally unstyled. If the project uses Tailwind with a custom theme (dark mode, custom CSS vars, etc.), adapt the classNames to match the project's existing style. Check `frontend/src/App.jsx` and other views for the theme conventions.

---

### `frontend/src/App.jsx` — edit needed

Wrap the root JSX content with `<AuthGate>`:

```jsx
// Add import at top:
import AuthGate from './AuthGate'

// Wrap your root return:
return (
  <AuthGate>
    {/* existing app content */}
  </AuthGate>
)
```

If the app uses `BrowserRouter`, `AuthGate` should go inside it so routing still works during the loading/login states.

---

### `frontend/src/api.js` — additions

Add an `auth` section. If `api.js` uses a structured object (`const api = { ... }`), merge this in:

```js
auth: {
  me: () => fetch('/api/auth/me', { credentials: 'include' }).then((r) => r.json()),
  logout: () => fetch('/api/auth/logout', { method: 'POST', credentials: 'include' }).then((r) => r.json()),
},
```

If the project uses axios or another HTTP client, adapt the calls to match the existing pattern in `api.js`.

---

### Python dependencies

Run:
```bash
poetry add google-auth-oauthlib google-auth pydantic-settings
```

`starlette` (for `SessionMiddleware`) is already a FastAPI dependency — no separate install needed.

---

### `.env` additions

Append to `.env` (skip vars that already exist):

```bash
# Google OAuth
DASHBOARD_AUTH_ENABLED=true
DASHBOARD_GOOGLE_CLIENT_ID=          # fill in after manual steps
DASHBOARD_GOOGLE_CLIENT_SECRET=      # fill in after manual steps
DASHBOARD_GOOGLE_REDIRECT_URI={{REDIRECT_URI}}
DASHBOARD_ALLOWED_EMAIL={{ALLOWED_EMAIL}}
DASHBOARD_HTTPS_ONLY={{true if public URL is https, false if localhost}}
DASHBOARD_CORS_ORIGINS=http://localhost:5173
```

Where `{{REDIRECT_URI}}` is:
- Local dev: `http://localhost:8000/api/auth/callback`
- Cloudflare Tunnel: `https://{{SUBDOMAIN}}/api/auth/callback`

---

### `.gitignore` additions

Append if not already present:
```
.session_secret
client_secret_*.json
```

---

## Phase 4: Output Manual Steps

After generating all files, output this checklist clearly:

```
══════════════════════════════════════════════════════
MANUAL STEPS — complete before testing auth
══════════════════════════════════════════════════════

[ ] STEP 1: Create Google OAuth credentials (~10 min)
────────────────────────────────────────────────────
URL: https://console.cloud.google.com/apis/credentials

1a. OAuth consent screen (first time only):
    APIs & Services → OAuth consent screen
    User Type: External
    App name: {{APP_NAME}}
    Support email: {{ALLOWED_EMAIL}}
    Developer email: {{ALLOWED_EMAIL}}
    → Save & Continue (skip optional fields)
    → Back to Dashboard

1b. Create OAuth client ID:
    + Create Credentials → OAuth client ID
    Application type: Web application
    Name: {{APP_NAME}}

    Authorized redirect URIs — add ALL that apply:
      http://localhost:8000/api/auth/callback     ← local dev
      {{PUBLIC_REDIRECT_URI}}                     ← production (if applicable)

    → Create
    → Copy Client ID and Client Secret

1c. Paste into .env:
    DASHBOARD_GOOGLE_CLIENT_ID=<paste Client ID>
    DASHBOARD_GOOGLE_CLIENT_SECRET=<paste Client Secret>

──────────────────────────────────────────────────────
[ ] STEP 2: Verify .env is complete
──────────────────────────────────────────────────────
All of these must be filled in:

  DASHBOARD_GOOGLE_CLIENT_ID=      ← not empty
  DASHBOARD_GOOGLE_CLIENT_SECRET=  ← not empty
  DASHBOARD_GOOGLE_REDIRECT_URI=   ← matches what you entered in step 1b
  DASHBOARD_ALLOWED_EMAIL=         ← your Google account email
  DASHBOARD_AUTH_ENABLED=true

──────────────────────────────────────────────────────
[ ] STEP 3: Test locally
──────────────────────────────────────────────────────
  poetry run uvicorn api.main:app --reload --port 8000

  Open http://localhost:5173 (or wherever your frontend runs)
  → Should redirect to Google login
  → After signing in, should return to the app

Check logs if it fails:
  - "redirect_uri_mismatch": the URI in .env doesn't match Google Console — fix typos
  - "invalid_grant": restart the server (stale process with old env)
  - 403 "Email not authorized": DASHBOARD_ALLOWED_EMAIL doesn't match your Google account

══════════════════════════════════════════════════════
```

---

## Troubleshooting

Include these only if the user hits issues:

- **`redirect_uri_mismatch`**: The exact URI in `DASHBOARD_GOOGLE_REDIRECT_URI` must appear in the "Authorized redirect URIs" list in Google Cloud Console. Check for trailing slashes, `http` vs `https`, and port numbers.
- **`invalid_grant`**: Usually means the server loaded stale env vars. Restart it.
- **Session cookie not persisting across requests**: Check that `credentials: 'include'` is on all `fetch` calls in `api.js`, and that `CORSMiddleware` has `allow_credentials=True` and the correct origin.
- **AuthGate stuck on "Checking session…"**: The `/api/auth/me` request is failing — open browser devtools, check the Network tab for the actual error.
- **Behind Cloudflare Tunnel / reverse proxy**: Set `DASHBOARD_HTTPS_ONLY=true`. The `http://` → `https://` scheme rewrite in `auth.py` handles Cloudflare's TLS termination automatically.
- **`OAUTHLIB_RELAX_TOKEN_SCOPE` warning in logs**: Harmless — this suppresses a scope-mismatch warning that appears when Google returns slightly different scopes than requested.
