---
name: deployer
description: Deploy applications to Cloud Run (backend) and Cloudflare Pages (frontend) via git push to main
enabled: true
---

# Deployer Skill

Deploy any application that follows the Cloud Run + Cloudflare Pages architecture. Handles both first-time setup and ongoing deployments.

## When to Use This Skill

Use when the user wants to:
- Deploy an application (backend, frontend, or both)
- Set up deployment infrastructure for a new project
- Check deployment status or troubleshoot a failed deploy
- Update deployment configuration (CORS, env vars, etc.)

## Project Configuration

Every deployable project must have a `deploy.json` at its root. If one doesn't exist, guide the user through creating it.

### deploy.json Schema

```json
{
  "project_name": "my-app",
  "gcp": {
    "project_id": "my-gcp-project-123",
    "region": "us-central1",
    "service_name": "my-app-backend"
  },
  "cloudflare": {
    "pages_project": "my-app-frontend",
    "pages_url": "https://my-app.pages.dev",
    "custom_domain": ""
  },
  "github": {
    "owner": "username",
    "repo": "my-app",
    "main_branch": "main"
  },
  "backend": {
    "source_dir": "./backend",
    "env_vars": ["GOOGLE_API_KEY", "TAVILY_API_KEY", "CACHE_TTL_DAYS"],
    "cors_env_var": "CORS_ORIGINS",
    "health_endpoint": "/health"
  },
  "frontend": {
    "source_dir": "./frontend",
    "build_command": "npm run build",
    "build_output": "dist",
    "api_url_env_var": "VITE_API_URL"
  }
}
```

---

## Output Format: Manual Action Blocks

Whenever the skill encounters a step that **cannot be automated** by the agent, it MUST output a clearly formatted manual action block to the user. Use this exact format:

```
------------------------------
MANUAL ACTION REQUIRED
------------------------------
What: <one-line summary>
Where: <URL or location, e.g. "Cloudflare Dashboard > Workers & Pages">
Steps:
  1. <step>
  2. <step>
  3. <step>
Why: <brief reason this can't be automated>
Verify: <how to confirm it's done, e.g. a CLI command the agent can run>
------------------------------
```

Always wait for the user to confirm they've completed a manual action before proceeding to the next step.

---

## Workflow: First-Time Setup (`/deployer setup`)

When the user needs to set up deployment infrastructure for the first time, walk through these steps in order.

### Step 1: Create deploy.json [AUTOMATED]

Ask the user for:
- GCP project ID
- Desired Cloud Run region (default: `us-central1`)
- Cloud Run service name
- GitHub owner/repo
- Backend source directory (default: `./backend`)
- Frontend source directory (default: `./frontend`)
- Required environment variable names (just the names, not values)
- Frontend build command (default: `npm run build`)

Create `deploy.json` at the project root.

### Step 2: Verify Prerequisites [MANUAL CHECK]

Before proceeding, verify and inform the user about prerequisites they must have in place:

```
------------------------------
MANUAL ACTION REQUIRED — Prerequisites
------------------------------
What: Ensure GCP and Cloudflare accounts are ready
Where: Google Cloud Console + Cloudflare Dashboard

Verify these are done:
  1. GCP project exists with billing enabled
     - Go to: https://console.cloud.google.com/billing
     - Select project: <PROJECT_ID>
     - Confirm billing account is linked

  2. gcloud CLI is installed and authenticated
     - Run: gcloud auth login (if not already done)
     - Run: gcloud config set project <PROJECT_ID>

  3. Cloudflare account exists and is connected to GitHub
     - Go to: https://dash.cloudflare.com
     - Verify your GitHub account is linked under Settings > Connections

  4. gh CLI is authenticated
     - Run: gh auth status
     - If not authenticated: gh auth login

Why: These are account-level configurations that require browser-based auth flows.
Verify: Agent will run `gcloud config get-value project` and `gh auth status`
------------------------------
```

### Step 3: Enable GCP APIs [AUTOMATED]

```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com --project <PROJECT_ID>
```

### Step 4: Initial Cloud Run Deploy [AUTOMATED with user input]

Ask the user for actual values of each env var listed in `deploy.json.backend.env_vars`. Never log or echo these values.

```bash
gcloud run deploy <SERVICE_NAME> \
  --source <BACKEND_SOURCE_DIR> \
  --region <REGION> \
  --project <PROJECT_ID> \
  --allow-unauthenticated \
  --set-env-vars KEY1=val1,KEY2=val2,...
```

Capture and display the service URL. Save it to `deploy.json` for later use.

### Step 5: OIDC Setup [AUTOMATED]

Check if `scripts/setup-oidc.sh` exists. If not, create it by generating the script from `deploy.json` values using this template structure:

```bash
#!/usr/bin/env bash
set -euo pipefail
PROJECT_ID="<from deploy.json>"
OWNER="<from deploy.json>"
REPO="<from deploy.json>"
POOL_ID="github-pool"
PROVIDER_ID="github-provider"
SA_NAME="github-cloud-run"
# ... (pool creation, provider creation, SA creation, IAM bindings)
```

Run the script and capture the output values for `GCP_WIF_PROVIDER` and `GCP_WIF_SERVICE_ACCOUNT`.

### Step 6: GitHub Actions Workflow [AUTOMATED]

Check if `.github/workflows/cloud-run-deploy.yml` exists. If not, create it using values from `deploy.json`:

- Trigger on pushes to `main_branch`
- Use OIDC authentication (no JSON keys)
- Deploy from `backend.source_dir`
- Set all `backend.env_vars` from GitHub secrets
- Include `CORS_ORIGINS` from secrets

### Step 7: GitHub Secrets [MIXED — try automated, fall back to manual]

First, attempt to set secrets via `gh`:

```bash
gh secret set GCP_WIF_PROVIDER --body "<value>" --repo <owner>/<repo>
gh secret set GCP_WIF_SERVICE_ACCOUNT --body "<value>" --repo <owner>/<repo>
```

For env var secrets, ask the user for each value and set via `gh secret set`.

If `gh secret set` fails (e.g., insufficient permissions), output:

```
------------------------------
MANUAL ACTION REQUIRED — GitHub Secrets
------------------------------
What: Add deployment secrets to your GitHub repository
Where: https://github.com/<owner>/<repo>/settings/secrets/actions

Add these secrets:
  1. GCP_WIF_PROVIDER
     Value: <value from OIDC setup output>

  2. GCP_WIF_SERVICE_ACCOUNT
     Value: <value from OIDC setup output>

  3. GOOGLE_API_KEY
     Value: <your API key>

  4. TAVILY_API_KEY (if applicable)
     Value: <your API key>

  5. CORS_ORIGINS
     Value: ["https://<your-pages-domain>"]
     Note: Set this after Cloudflare Pages is configured (Step 8).
           Use the pages.dev URL initially, update later if you add a custom domain.

  (Add one secret for each env var listed in deploy.json backend.env_vars)

Why: gh CLI may lack permissions to set secrets, or values are sensitive
     and should be entered directly in the browser.
Verify: Agent will run `gh secret list --repo <owner>/<repo>` to confirm
        secrets exist (values are not shown, only names).
------------------------------
```

After user confirms, verify:
```bash
gh secret list --repo <owner>/<repo>
```

### Step 8: Cloudflare Pages Setup [MANUAL]

This step cannot be automated — Cloudflare Pages must be set up via their dashboard.

```
------------------------------
MANUAL ACTION REQUIRED — Cloudflare Pages
------------------------------
What: Create a Cloudflare Pages project for your frontend
Where: https://dash.cloudflare.com > Workers & Pages > Create application > Pages

Steps:
  1. Click "Connect to Git" and select the repository: <owner>/<repo>

  2. Configure the build settings:
     - Production branch: <main_branch>
     - Root directory (advanced): <frontend.source_dir>   (e.g., "frontend")
     - Build command: <frontend.build_command>            (e.g., "npm run build")
     - Build output directory: <frontend.build_output>    (e.g., "dist")

  3. Add environment variable:
     - Variable name: <frontend.api_url_env_var>          (e.g., "VITE_API_URL")
     - Value: <Cloud Run URL from Step 4>

  4. Click "Save and Deploy"

  5. (Recommended) Disable preview deployments to avoid building on every PR:
     - Go to: Settings > Builds & Deployments
     - Set "Preview deployments" to "None"

  6. Note the pages.dev URL assigned to your project
     (e.g., https://my-app.pages.dev)

  7. (Optional) Set up a custom domain:
     - Go to: Custom Domains tab
     - Add your subdomain (e.g., app.yourdomain.com)
     - Your domain must be managed by Cloudflare DNS

Why: Cloudflare Pages project creation requires their dashboard UI.
     There is no CLI or API for the initial import-from-Git setup.
Verify: Tell the agent your pages.dev URL and it will update deploy.json
        and configure CORS on Cloud Run.
------------------------------
```

### Step 9: CORS Configuration [AUTOMATED]

Once the user provides the Cloudflare Pages URL:

1. Update `deploy.json` with the `cloudflare.pages_url` value.
2. Update Cloud Run CORS:

```bash
gcloud run services update <SERVICE_NAME> \
  --region <REGION> \
  --project <PROJECT_ID> \
  --update-env-vars CORS_ORIGINS='["https://<pages-domain>"]'
```

3. If GitHub secrets were set via `gh`, also update the `CORS_ORIGINS` secret:
```bash
gh secret set CORS_ORIGINS --body '["https://<pages-domain>"]' --repo <owner>/<repo>
```

4. If secrets were set manually, output:

```
------------------------------
MANUAL ACTION REQUIRED — Update CORS Secret
------------------------------
What: Update the CORS_ORIGINS GitHub secret with your Pages URL
Where: https://github.com/<owner>/<repo>/settings/secrets/actions

Update this secret:
  CORS_ORIGINS
  New value: ["https://<pages-domain>"]

  If you also have a custom domain, include both:
  ["https://<pages-domain>", "https://<custom-domain>"]

Why: GitHub Actions needs this secret to set CORS correctly on every deploy.
Verify: Agent will run `gh secret list --repo <owner>/<repo>`
------------------------------
```

### Step 10: Setup Complete — Summary

Print a final summary:

```
Setup complete for: <project_name>

Backend:  <Cloud Run URL>     (Cloud Run, <region>)
Frontend: <Pages URL>         (Cloudflare Pages)
Deploys:  Push to <main_branch> triggers both

Files created:
  - deploy.json                              (project config)
  - scripts/setup-oidc.sh                    (OIDC bootstrap, already run)
  - .github/workflows/cloud-run-deploy.yml   (CI/CD pipeline)

To deploy in the future, run: /deployer
```

---

## Workflow: Deploy (`/deployer` or `/deployer deploy`)

This is the standard deployment flow. It deploys by merging to main and pushing, which triggers GitHub Actions (backend) and Cloudflare Pages (frontend) automatically.

### Pre-flight Checks

1. **Read `deploy.json`** from the project root. If missing, ask if the user wants to run setup.

2. **Check git status:**
   ```bash
   git status
   git log --oneline -5
   ```
   - Warn if there are uncommitted changes
   - Show current branch name

3. **Verify remote is up to date:**
   ```bash
   git fetch origin
   git log --oneline origin/<main_branch>..HEAD
   ```
   Show what commits will be deployed.

4. **Run build verification** (if applicable):
   - Backend: Check if Dockerfile or build config exists
   - Frontend: Run `npm run build` in `frontend.source_dir` to catch errors before pushing

### Deploy Steps

1. **Confirm with the user** — show a summary:
   ```
   Deploying: <project_name>
   Branch: <current_branch> -> <main_branch>
   Commits: <N> new commits
   Backend: Cloud Run (<service_name> in <region>)
   Frontend: Cloudflare Pages (<pages_project>)

   Proceed?
   ```

2. **Push current branch to remote** (if not already pushed):
   ```bash
   git push origin <current_branch>
   ```

3. **Merge to main:**
   ```bash
   git checkout <main_branch>
   git pull origin <main_branch>
   git merge <current_branch>
   git push origin <main_branch>
   ```

4. **Switch back to the working branch:**
   ```bash
   git checkout <current_branch>
   ```

5. **Monitor deployment status:**
   - GitHub Actions: `gh run list --limit 1 --repo <owner>/<repo>`
   - Wait and check: `gh run watch <run_id> --repo <owner>/<repo>`

### Post-Deploy Verification

1. **Check Cloud Run service:**
   ```bash
   gcloud run services describe <SERVICE_NAME> --region <REGION> --project <PROJECT_ID> --format="value(status.url)"
   ```
   If `backend.health_endpoint` is set, curl it:
   ```bash
   curl -s -o /dev/null -w "%{http_code}" <SERVICE_URL><health_endpoint>
   ```

2. **Check GitHub Actions result:**
   ```bash
   gh run list --limit 1 --repo <owner>/<repo>
   ```

3. **Report deployment result** to the user with:
   - Backend URL and health check status
   - Frontend URL
   - GitHub Actions run status
   - Any errors from the deploy logs

4. **If GitHub Actions failed**, automatically pull the failed logs:
   ```bash
   gh run view <run_id> --repo <owner>/<repo> --log-failed
   ```
   Analyze the error and suggest fixes (see Troubleshooting section).

5. **Frontend verification — manual check reminder:**

   ```
   ------------------------------
   MANUAL VERIFICATION — Frontend
   ------------------------------
   What: Verify the frontend deployed correctly on Cloudflare Pages
   Where: <pages_url>

   Checks:
     1. Open <pages_url> in your browser
     2. Verify the page loads without errors
     3. Open browser DevTools > Console — check for errors
     4. Test a core user flow (e.g., search for a word, submit a form)
     5. Verify API calls reach the backend (Network tab)

   If something is wrong:
     - Check Cloudflare Pages build log:
       https://dash.cloudflare.com > Workers & Pages > <pages_project> > Deployments
     - Common issue: VITE_API_URL not set or pointing to wrong backend URL
     - Common issue: CORS errors — tell the agent and it will fix Cloud Run CORS

   Note: Cloudflare Pages typically deploys within 1-2 minutes of the push.
         If you don't see changes yet, wait and refresh.
   ------------------------------
   ```

---

## Workflow: Status Check (`/deployer status`)

Quick check on current deployment state:

```bash
# Latest GitHub Actions runs
gh run list --limit 3 --repo <owner>/<repo>

# Cloud Run service status
gcloud run services describe <SERVICE_NAME> --region <REGION> --project <PROJECT_ID> --format="table(status.url, status.conditions)"

# Recent Cloud Run revisions
gcloud run revisions list --service <SERVICE_NAME> --region <REGION> --project <PROJECT_ID> --limit 3
```

Then output:

```
------------------------------
MANUAL CHECK — Cloudflare Pages Status
------------------------------
What: Check latest Cloudflare Pages deployment status
Where: https://dash.cloudflare.com > Workers & Pages > <pages_project> > Deployments

The agent cannot query Cloudflare Pages deployment status via CLI.
Check the dashboard to see:
  - Latest deployment status (success/failed)
  - Build duration
  - Any build errors

Why: Cloudflare Pages API requires an API token not configured in this setup.
     The Wrangler CLI supports `wrangler pages deployment list` but requires
     additional auth configuration.
------------------------------
```

---

## Workflow: Update Config (`/deployer config`)

For updating deployment configuration:

### Update CORS [AUTOMATED]
```bash
gcloud run services update <SERVICE_NAME> \
  --region <REGION> \
  --project <PROJECT_ID> \
  --update-env-vars CORS_ORIGINS='["https://new-domain"]'
```

Also remind the user:

```
------------------------------
MANUAL ACTION REQUIRED — Update CORS GitHub Secret
------------------------------
What: Update the CORS_ORIGINS secret so future deploys preserve the new value
Where: https://github.com/<owner>/<repo>/settings/secrets/actions

Update: CORS_ORIGINS = ["https://new-domain"]

Why: If this secret isn't updated, the next GitHub Actions deploy will
     overwrite CORS_ORIGINS with the old value from secrets.
Verify: Agent will run `gh secret list` to confirm the secret exists.
------------------------------
```

### Update Environment Variables [AUTOMATED]
```bash
gcloud run services update <SERVICE_NAME> \
  --region <REGION> \
  --project <PROJECT_ID> \
  --update-env-vars KEY=new_value
```

If the env var is also a GitHub secret, remind the user to update it there too (same manual action block pattern).

### Update Custom Domain [MANUAL]

```
------------------------------
MANUAL ACTION REQUIRED — Custom Domain
------------------------------
What: Add or update a custom domain for your Cloudflare Pages site
Where: https://dash.cloudflare.com > Workers & Pages > <pages_project> > Custom Domains

Steps:
  1. Click "Set up a custom domain"
  2. Enter your subdomain (e.g., app.yourdomain.com)
  3. Cloudflare will auto-configure DNS if the domain is in your Cloudflare account
  4. Wait for SSL certificate provisioning (usually < 5 minutes)
  5. Tell the agent your new custom domain URL

After this, the agent will:
  - Update deploy.json with the custom domain
  - Update Cloud Run CORS to include the new domain
  - Remind you to update the CORS_ORIGINS GitHub secret

Why: Custom domain setup requires Cloudflare dashboard DNS verification.
------------------------------
```

---

## Troubleshooting

When a deploy fails, check these in order:

### GitHub Actions Failed [AUTOMATED diagnosis]
```bash
gh run view <run_id> --repo <owner>/<repo> --log-failed
```

Common causes and fixes:

| Error | Cause | Fix |
|-------|-------|-----|
| `PERMISSION_DENIED` | Missing IAM roles on OIDC service account | Add missing roles (see IAM Roles below) |
| `OIDC invalid_target` | Wrong `GCP_WIF_PROVIDER` secret value | Verify with `gcloud iam workload-identity-pools providers list` |
| `Build failed` | Dockerfile or dependency issue | Check build log, fix code, redeploy |
| `serviceusage.services.use` | Missing `serviceUsageConsumer` role | Add `roles/serviceusage.serviceUsageConsumer` |

**Required IAM roles for the OIDC service account:**
- `roles/run.admin`
- `roles/iam.serviceAccountUser`
- `roles/cloudbuild.builds.editor`
- `roles/artifactregistry.writer`
- `roles/storage.admin`
- `roles/serviceusage.serviceUsageConsumer` (if needed)

### Cloud Run Startup Fails
- **PORT mismatch**: App must bind to `$PORT` (default 8080), not a hardcoded port. Check the Dockerfile CMD.
- **Missing env vars**: Deploy overwrote env vars without including all required ones. Verify with:
  ```bash
  gcloud run services describe <SERVICE_NAME> --region <REGION> --project <PROJECT_ID> --format="yaml(spec.template.spec.containers[0].env)"
  ```

### Cloudflare Pages Failed [MANUAL]

```
------------------------------
MANUAL ACTION REQUIRED — Cloudflare Pages Build Failed
------------------------------
What: Check and fix the Cloudflare Pages build error
Where: https://dash.cloudflare.com > Workers & Pages > <pages_project> > Deployments

Common causes:
  1. TypeScript errors — run `npm run build` locally first to catch these
  2. Missing VITE_API_URL env var — add it in Pages > Settings > Environment Variables
  3. Wrong root directory — should be "<frontend.source_dir>"
  4. Wrong build command — should be "<frontend.build_command>"
  5. Node.js version mismatch — set NODE_VERSION env var in Pages settings

Steps:
  1. Click on the failed deployment to see the build log
  2. Scroll to the error in the log
  3. Fix the issue locally and push again, OR update Pages settings

Why: Cloudflare Pages build logs are only accessible via their dashboard.
Verify: Tell the agent the error message and it will help diagnose.
------------------------------
```

### CORS Broken After Deploy
- Deploy command must include `CORS_ORIGINS` every time or it gets wiped
- Verify current CORS:
  ```bash
  gcloud run services describe <SERVICE_NAME> --region <REGION> --project <PROJECT_ID> --format="yaml(spec.template.spec.containers[0].env)"
  ```
- Fix:
  ```bash
  gcloud run services update <SERVICE_NAME> --region <REGION> --project <PROJECT_ID> --update-env-vars CORS_ORIGINS='["https://<pages-domain>"]'
  ```

---

## Important Notes

- **Never deploy with uncommitted changes** — always commit first
- **Always verify the build locally** before pushing to main
- **CORS_ORIGINS must be included in every deploy** or it gets wiped
- **Frontend deploys automatically** when Cloudflare Pages detects a push to main
- **Backend deploys via GitHub Actions** triggered by push to main
- Do not store secrets in `deploy.json` — only non-sensitive configuration
- Always wait for user confirmation before proceeding past a MANUAL ACTION block
