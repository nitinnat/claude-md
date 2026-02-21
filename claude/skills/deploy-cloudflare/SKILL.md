---
name: deploy-cloudflare
description: Deploy a FastAPI + React (Vite) app publicly via Cloudflare Tunnel with optional Google OAuth. Use when the user says "deploy this", "set up Cloudflare Tunnel", "make this app public", "add a start script", or "I want to access this from outside my laptop". Detects Google OAuth from the codebase and includes auth setup steps only when needed.
---

# Deploy via Cloudflare Tunnel

**Announce:** "Using deploy-cloudflare skill to set up public deployment."

## What This Skill Does

Walks through deploying a local FastAPI + React (Vite) app publicly via Cloudflare Tunnel. Handles automated steps (generating `start.sh`, `stop.sh`, `.cloudflared.yml`) and outputs a numbered manual steps checklist for the Cloudflare dashboard and optionally Google Cloud Console.

## Prerequisites Check

Before doing anything else, run:

```bash
which cloudflared || echo "MISSING: brew install cloudflared"
which poetry || echo "MISSING: install via https://python-poetry.org"
node --version || echo "MISSING: install Node.js"
```

If any are missing, tell the user what to install and stop. Do not proceed until all three are present.

---

## Phase 1: Inspect the Project

Read these files to understand the project. Do not ask the user for info that can be determined from the code.

| What to read | What to extract |
|---|---|
| `pyproject.toml` | `[tool.poetry].name` → **app_name** (lowercase, hyphens) |
| `api/main.py` | Does `StaticFiles` appear? → **frontend_mode**: `static` or `devserver` |
| `api/routers/auth.py` (if exists) OR grep `AuthGate` in `frontend/src/` | → **auth_detected**: true/false |
| `frontend/package.json` | Confirm Vite/React, get dev port (default `5173`) → **frontend_port** |
| `.env` | Any existing `DASHBOARD_*` vars or `TUNNEL_ID` → skip re-adding these |
| `start.sh` (if exists) | Extract existing port → **api_port** (default `8000`) |

After reading, determine:
- **api_port**: `8000` unless found elsewhere
- **frontend_mode**: `static` if `StaticFiles` is mounted in `main.py`, otherwise `devserver`
- **auth_detected**: `true` if `api/routers/auth.py` exists or `AuthGate` is found in frontend

---

## Phase 2: Ask the User

Ask the following in a **single message** (not one-by-one):

```
I've inspected the project. Here's what I found:

  App name:       <app_name>
  API port:       <api_port>
  Frontend mode:  <static (served by FastAPI) | devserver on port <frontend_port>>
  Auth detected:  <yes | no>

I need a couple of details to generate your deployment files:

1. What subdomain should this run on? (e.g., myapp.nitinnataraj.com)
   [If auth detected] 2. What email address should be allowed to log in?
```

Wait for the user's answers before generating any files.

---

## Phase 3: Generate Files

Generate all files below. Replace **every** `{{PLACEHOLDER}}` with actual values — do NOT leave any placeholders in the output.

---

### `start.sh`

```bash
#!/bin/bash
set -e
cd "$(dirname "$0")"

# Load env vars safely
if [ -f .env ]; then set -a; source .env; set +a; fi

echo "[{{APP_NAME}}] starting backend..."
poetry run uvicorn api.main:app \
  --port {{API_PORT}} \
  --host 127.0.0.1 \
  --proxy-headers \
  --forwarded-allow-ips=127.0.0.1 \
  > /tmp/{{APP_NAME}}-backend.log 2>&1 &
echo $! > /tmp/{{APP_NAME}}-backend.pid

# INCLUDE THIS BLOCK ONLY IF frontend_mode == devserver
echo "[{{APP_NAME}}] starting frontend dev server..."
cd frontend && npm run dev > /tmp/{{APP_NAME}}-frontend.log 2>&1 &
echo $! > /tmp/{{APP_NAME}}-frontend.pid
cd ..
# END devserver block

# INCLUDE THIS BLOCK ONLY IF frontend_mode == static
echo "[{{APP_NAME}}] building frontend..."
cd frontend && npm run build && cd ..
# END static block

echo "[{{APP_NAME}}] starting tunnel..."
cloudflared tunnel --config .cloudflared.yml run {{APP_NAME}} \
  > /tmp/{{APP_NAME}}-tunnel.log 2>&1 &
echo $! > /tmp/{{APP_NAME}}-tunnel.pid

echo "[{{APP_NAME}}] live at https://{{SUBDOMAIN}}"
```

Make the file executable: `chmod +x start.sh`

---

### `stop.sh`

```bash
#!/bin/bash
cd "$(dirname "$0")"

stop_pid() {
  local f="/tmp/$1.pid"
  [ -f "$f" ] && kill "$(cat "$f")" 2>/dev/null && rm "$f" && echo "stopped $1"
}

stop_pid {{APP_NAME}}-tunnel
stop_pid {{APP_NAME}}-backend
# INCLUDE IF devserver mode:
stop_pid {{APP_NAME}}-frontend

echo "[{{APP_NAME}}] stopped"
```

Make the file executable: `chmod +x stop.sh`

---

### `.cloudflared.yml` (in project root)

```yaml
tunnel: TUNNEL_ID_PLACEHOLDER
credentials-file: /Users/{{USERNAME}}/.cloudflared/TUNNEL_ID_PLACEHOLDER.json

ingress:
  - hostname: {{SUBDOMAIN}}
    service: http://localhost:{{API_PORT}}
  # INCLUDE IF devserver mode:
  - hostname: {{SUBDOMAIN}}
    service: http://localhost:{{FRONTEND_PORT}}
  - service: http_status:404
```

**IMPORTANT:** `TUNNEL_ID_PLACEHOLDER` and `{{USERNAME}}` must be filled in AFTER the user creates the tunnel (Manual Step 1). Tell the user to run `cloudflared tunnel list` and paste the tunnel UUID so you can update this file.

Get `{{USERNAME}}` by running: `whoami`

---

### `.env` additions

Append to `.env` (do NOT overwrite existing content, skip any vars already present):

```bash
# [INCLUDE IF auth_detected == true]
DASHBOARD_AUTH_ENABLED=true
DASHBOARD_GOOGLE_CLIENT_ID=         # fill in after Manual Step 2
DASHBOARD_GOOGLE_CLIENT_SECRET=     # fill in after Manual Step 2
DASHBOARD_GOOGLE_REDIRECT_URI=https://{{SUBDOMAIN}}/api/auth/callback
DASHBOARD_ALLOWED_EMAIL={{ALLOWED_EMAIL}}
DASHBOARD_HTTPS_ONLY=true
# [END auth block]
```

If auth was not detected, do not add any auth vars.

---

### `.gitignore` additions

Append these lines if not already present:

```
.cloudflared.yml
client_secret_*.json
*.pem
```

`.cloudflared.yml` contains the path to your tunnel credentials file — never commit it.

---

## Phase 4: Output Manual Steps

After generating all files, output the checklist below. Fill in all values — no placeholders. Print it inside a clearly separated block so the user can refer to it.

---

```
══════════════════════════════════════════════════════
MANUAL STEPS — complete in order before running ./start.sh
══════════════════════════════════════════════════════

[ ] STEP 1: Create the Cloudflare Tunnel (~5 min)
────────────────────────────────────────────────────
Run these commands in your terminal:

  cloudflared tunnel login
  (opens browser — pick your domain: nitinnataraj.com)

  cloudflared tunnel create {{APP_NAME}}
  cloudflared tunnel route dns {{APP_NAME}} {{SUBDOMAIN}}

  cloudflared tunnel list
  (copy the UUID next to {{APP_NAME}} — you'll need it below)

Once you have the UUID, paste it here so I can update .cloudflared.yml.

──────────────────────────────────────────────────────
[ ] STEP 2: Google OAuth Setup (~10 min)   ← SKIP IF NO AUTH
──────────────────────────────────────────────────────
URL: https://console.cloud.google.com/apis/credentials

2a. OAuth consent screen (if not already done):
    APIs & Services → OAuth consent screen
    User Type: External → fill App name: {{APP_NAME}} → Save & Continue

2b. Create OAuth client:
    + Create Credentials → OAuth client ID
    Application type: Web application
    Name: {{APP_NAME}}
    Authorized redirect URIs: https://{{SUBDOMAIN}}/api/auth/callback
    → Create

2c. Copy Client ID and Client Secret into .env:
    DASHBOARD_GOOGLE_CLIENT_ID=<paste here>
    DASHBOARD_GOOGLE_CLIENT_SECRET=<paste here>

──────────────────────────────────────────────────────
[ ] STEP 3: Update .cloudflared.yml with tunnel ID
──────────────────────────────────────────────────────
After pasting the tunnel UUID from Step 1, I'll update .cloudflared.yml.
Verify it looks correct:
  cat .cloudflared.yml

──────────────────────────────────────────────────────
[ ] STEP 4: Start the app
──────────────────────────────────────────────────────
  ./start.sh

Verify it's live: https://{{SUBDOMAIN}}

Check logs if something looks wrong:
  tail -f /tmp/{{APP_NAME}}-backend.log
  tail -f /tmp/{{APP_NAME}}-tunnel.log

══════════════════════════════════════════════════════
```

---

## Phase 5: Tunnel ID Follow-up

After the user pastes the tunnel UUID from Step 1:

1. Run `whoami` to get the username if not already known
2. Update `.cloudflared.yml` — replace `TUNNEL_ID_PLACEHOLDER` in both the `tunnel:` field and the `credentials-file:` path
3. Tell the user: "`.cloudflared.yml` is ready. Complete Step 2 (auth) if needed, then run `./start.sh`."

---

## Troubleshooting Notes

Include these if the user hits issues after `./start.sh`:

- **Tunnel not found / DNS not resolving**: DNS propagation can take 30–60s. Wait and retry.
- **OAuth `redirect_uri_mismatch`**: The redirect URI in `.env` must exactly match what's in Google Cloud Console. Check for `http://` vs `https://` mismatch.
- **OAuth `invalid_grant`**: Restart the backend (`./stop.sh && ./start.sh`) — stale process may be loading old env vars.
- **Frontend not loading (static mode)**: Run `cd frontend && npm run build` manually and check for errors. Then restart.
- **Frontend not loading (devserver mode)**: Check `/tmp/{{APP_NAME}}-frontend.log` — likely a missing `node_modules/` (`cd frontend && npm install`).
- **`--forwarded-allow-ips` warning**: Must be `127.0.0.1` (not `*`) since cloudflared connects from localhost. If you change the bind host, update this flag to match.
