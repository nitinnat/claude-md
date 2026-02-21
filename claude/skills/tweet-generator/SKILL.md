---
name: tweet-generator
description: Generate authentic project introduction tweets by analyzing the current repo, finding accounts to tag, and applying engagement patterns from builders like Karpathy, DHH, and Boris Cherny
enabled: true
---

# Tweet Generator Skill

Generate genuine, personal tweets to introduce a project you've built. Analyzes the current repo for context, finds relevant accounts to tag via web search, and produces 3 tweet variations.

## Process

### Step 1: Analyze the Repository

Read these files (whichever exist) to understand the project:

1. **README.md** — project description, purpose, features
2. **package.json** / **pyproject.toml** / **Cargo.toml** / **go.mod** — tech stack and dependencies
3. **IMPLEMENTATION_LOG.md** / **CHANGELOG.md** — what was built, recent changes
4. **deploy.json** — if deployed, get the live URL
5. Scan `src/` or `app/` top-level structure to understand scope

Extract:
- **What it does** (one sentence, specific)
- **What problem or gap motivated it** (why it exists)
- **One interesting technical detail** (architecture choice, constraint, surprising number)
- **Tech stack** (major frameworks/libraries only)
- **Live URL / Repo URL** (from git remote or deploy config)

### Step 2: Find Accounts to Tag

Tagging is the single biggest organic reach lever. When you tag @CloudflareDev and they RT you, their 500K+ followers see your project. This step is not optional — it's the difference between 200 impressions and 20,000.

**Run these searches** (use Exa MCP `web_search_exa` if available, otherwise WebSearch):

#### A. Framework & Library Accounts
For each major dependency in the tech stack, search:
- `"<framework name>" official X Twitter account`
- `<framework name> site:x.com` (look at the verified/official result)

Common ones to know (verify these are current via search):
- React → `@reactjs`
- Next.js → `@nextjs`
- Vue → `@vuejs`
- Svelte → `@svaboreltejs`
- Tailwind CSS → `@tailwindcss`
- Framer Motion → `@framermotion`
- Vite → `@vaborite_js`

#### B. Platform & Infrastructure Accounts
These are high-value tags — platform accounts actively retweet builders deploying on their infrastructure:
- Cloudflare → `@CloudflareDev` (very active in RTing builders)
- Vercel → `@vercel`
- Google Cloud → `@googlecloud`
- Firebase → `@Firebase`
- AWS → `@awscloud`
- Supabase → `@supabase` (extremely active in RTing)
- Railway → `@Railway` (actively RTs)
- Fly.io → `@flydotio`

#### C. AI/API Provider Accounts
If the project uses an AI API or notable service:
- Google Gemini → `@GoogleAI` or `@GoogleDeepMind`
- OpenAI → `@OpenAI`
- Anthropic → `@AnthropicAI`
- Replicate → `@replicate`

#### D. Developer Community Accounts
Search for accounts that curate/amplify projects in the relevant space:
- `"best developer Twitter accounts that retweet projects" <technology>`
- `"<technology> community" site:x.com`

Examples:
- `@buildwithtech` / `@IndieHackers` — for indie projects
- `@JavaScriptDaily` / `@typescript` — for JS/TS projects
- `@PythonHub` / `@realpython` — for Python projects

#### E. DevRel / Developer Advocate Accounts
Search: `"<framework> developer advocate" site:x.com`

These are individuals whose job is to amplify community projects. They RT builders more than official accounts do. Find 1-2 relevant DevRel people for the main framework used. Only tag them if they have a pattern of engaging with community projects (check their recent tweets via search).

**After searching, compile a ranked tag list:**

| Account | Why tag them | RT likelihood |
|---------|-------------|---------------|
| @CloudflareDev | Deployed on CF Pages, they RT builders weekly | High |
| @reactjs | Built with React, huge audience | Medium (high volume, selective) |
| @GoogleAI | Uses Gemini API | Medium |

**Tagging rules:**
- Include 2-3 tags per tweet, woven naturally or at the end
- Vary which accounts you tag across the 3 variations
- Prioritize accounts with a known pattern of RTing builders (platforms > frameworks > AI providers)
- Never tag more than 1 individual person per tweet

### Step 3: Generate 3 Variations

Each variation should take a genuinely different angle — not the same content reshuffled. Draw from the voice patterns below. **Each variation should tag different accounts** to give the user options for which audience to target.

### Step 4: Present to User

```
---
1 — [N] chars
---
[tweet text]

---
2 — [N] chars
---
[tweet text]

---
3 — [N] chars
---
[tweet text]

---
Accounts found:
  @account1 — [why, RT likelihood]
  @account2 — [why, RT likelihood]
  @account3 — [why, RT likelihood]
  @account4 — [why, RT likelihood]

Suggested media: [what screenshot/gif/video to attach and why]
Timing: [when to post based on target audience timezone]
```

---

## Engagement Strategy

Tagging is the main reach amplifier, but these additional tactics compound on it:

### Media is Mandatory
Tweets with images get ~150% more retweets. Don't just suggest media — actually create it using the available skills.

**For web apps and UI projects — use `/screenshot-capture`:**
- Invoke the `screenshot-capture` skill to capture the app in its most visually interesting state
- Capture the core feature in action, not the landing page or empty state
- If the app has multiple compelling views, capture 2-3 for the main tweet and self-replies
- Specify the exact URL and viewport size (desktop 1280x800 for best tweet image ratio)

**For projects that need conceptual visuals — use `/gemini-image-generator`:**
- If the project is a CLI tool, library, or backend service with no visual UI, use the `gemini-image-generator` skill to generate a compelling visual
- Good prompts: architecture diagrams, workflow visualizations, before/after comparisons, conceptual illustrations of what the tool does
- Keep the style clean and technical — not flashy marketing graphics
- Use this for self-reply images too (e.g., a visual architecture breakdown for "how it works" replies)

**For projects with a UI AND a conceptual angle — use both:**
- Main tweet: screenshot of the app via `/screenshot-capture`
- Self-reply: architecture or workflow visual via `/gemini-image-generator`

**Media priority by project type:**
| Project Type | Main Tweet Media | Self-Reply Media |
|---|---|---|
| Web app | Screenshot via `/screenshot-capture` | Second state screenshot or architecture via `/gemini-image-generator` |
| CLI tool | Terminal recording/GIF (manual) | Workflow diagram via `/gemini-image-generator` |
| Library/package | Usage code snippet screenshot | Architecture visual via `/gemini-image-generator` |
| API/backend | Generated architecture diagram via `/gemini-image-generator` | Request/response example screenshot |
| Game/interactive | Screenshot via `/screenshot-capture` | Second screenshot of a funny/interesting result |

### Timing
- **Weekdays 8-10 AM** in the user's timezone for morning scrollers
- **Weekdays 6-9 PM** for evening engagement
- **Avoid weekends** for developer/tech audience unless it's a casual project
- If targeting a specific account for RT (e.g., @CloudflareDev), check when they're most active via search

### First 30 Minutes Matter
The X algorithm weighs early engagement heavily. Advise the user:
- Reply to your own tweet with a technical detail, screenshot, or "how it works" follow-up — this seeds the reply thread
- If anyone replies in the first 30 min, respond immediately — replies boost algorithmic ranking
- Don't post and disappear

### Self-Reply Thread Strategy
Suggest 1-2 self-replies the user can post immediately after the main tweet:
- **Reply 1**: The technical "how it works" — use `/gemini-image-generator` to create an architecture diagram or workflow visual to attach
- **Reply 2**: A second view of the project — use `/screenshot-capture` to grab a different state/feature, or `/gemini-image-generator` for a conceptual visual
This turns a single tweet into a mini-thread without the cringe "Thread 🧵" opener.

### Position for Quote Tweets
Write the tweet so it's easy for others to quote-tweet with their own take. Tweets that state something specific and opinionated get more QTs than generic descriptions. A claim about the state of existing tools, a surprising technical constraint, or a strong opinion about how something should work — these invite reactions.

---

## Voice: A Person, Not a Product Page

This is someone sharing something they personally built. It should sound like a real human being — first person, warm, direct. The tweet is coming from a person, not a brand. "I built this" is not bragging — it's just being real.

### The Core Principles

**It's personal.** Use "I" freely. "I built", "I've been working on", "I wanted", "I couldn't find." This is your work — own it naturally. Removing the personal voice doesn't make you humble, it makes you sound like a press release.

**Invite people in.** "Here's", "go try it", "check it out", "give it a spin" — these are generous, not desperate. You're sharing something you made and inviting people to experience it. That's a normal human thing to do. DHH does it constantly: "Rails 8 is out so here's a brand new demo showing it off."

**Be specific about what's interesting.** Don't describe the project generically. Pick the one detail that would make another builder go "oh, that's cool." A concrete number, a surprising constraint, a technical choice that reveals something about how it works.

**Honest without being self-deprecating.** Karpathy says "it is by no means finished, tuned or optimized" — that's honest confidence, not false modesty. "Still rough around the edges but it works" is fine. "It's not much but..." is not — that's fishing for reassurance.

### What Actually Works (From Studying Real Builders)

**Karpathy's style:** Teacher who shares what he built as a way to explain something. Opens with what the thing *is* using precise details. Uses `~` for casual precision ("~8,000 lines", "~4 hours"). States limitations openly. Doesn't hype.

**DHH's style:** Punchy, declarative, opinionated. "Here's" is his power word. Ships arguments, not just software — every project is a stance on how something should work. Uses exclamation marks with genuine (not marketing) energy. "I crammed a lot into this one!"

**Boris Cherny's style:** Practitioner sharing his process. Leads with personal context. Proves value with concrete numbers ("259 PRs — 497 commits, 40k lines added"). Gives you actionable instructions: "Try it: [command]". Credits community and tools.

### The Three Angles

When generating variations, pick three that fit the project:

**The Gap** — You wanted something, couldn't find it, so you built it. Personal motivation first, then the project.

**The Demo** — "Here's what I built" / "Here's [thing] in action." Direct, generous, paired with media. The tweet frames the visual.

**The Interesting Detail** — Lead with the one technical or design choice that makes this project different. Then zoom out to what the whole thing is.

**The Argument** — The project embodies an opinion. Something about existing tools bothered you or you think things should work differently. The project is your answer.

**The Build Story** — What you did, how long it took, what you used. Conversational, like telling a friend over coffee.

### What to Avoid

- "Excited to announce/share/release" — corporate language
- Emoji bullet points (🔥📈🚀💡✅) or emoji as decoration
- Feature lists formatted like a product page
- Superlatives: "game-changing", "revolutionary", "incredible"
- "Like and RT" / "Follow for more" / explicit engagement begging
- Self-deprecation as a shield ("it's nothing special but...")
- Comparing to competitors ("like X but better")
- Hashtag spam — 0-1 max, only if genuinely relevant
- Third-person voice or passive descriptions — this is YOU sharing YOUR thing

---

## Examples

Each example shows a different project type. Notice the tone stays consistent — personal, specific, inviting — but the content adapts to what's interesting about each project.

### Example 1: CLI Tool (The Gap angle)

```
I got mass frustrated with grepping through CloudWatch logs across
~40 Lambda functions to trace a single request.

So I built a CLI that takes a correlation ID and stitches together
the full request path across services — timing, errors, payloads,
all in one terminal view.

It's ~1,200 lines of Go. Try it: pip install traceweave

[link] @awscloud
```
Tags @awscloud — they RT builders who solve real AWS pain points.

### Example 2: Web App (The Demo angle)

```
Here's a thing I built over the last few weeks — an app that
generates custom meal plans from whatever's already in your fridge.

Snap a photo of your fridge, it identifies ingredients via
@GoogleAI Gemini Vision, then builds a week of recipes around what
you actually have. No grocery list needed.

Go give it a try:

[link]
```
Tags @GoogleAI — creative use of their Vision API, high RT likelihood.

### Example 3: Open Source Library (The Interesting Detail angle)

```
I needed a date picker in @svaboreltejs that didn't pull in 200KB of
dependencies. Couldn't find one under 5KB that handled timezones.

So I wrote one. ~3KB gzipped, zero dependencies, handles IANA
timezones natively. Took more effort than expected to get DST
transitions right.

npm install svelte-datepick — check it out:

[link]
```
Tags @sveltejs — they actively RT community packages.

### Example 4: Side Project / Fun App (The Build Story angle)

```
Spent my weekend building a multiplayer drawing game where the
prompt is generated by AI based on the previous round's drawings.

It gets unhinged fast. By round 4 someone was trying to draw
"a melancholic octopus conducting an orchestra in zero gravity."

Built with @nextjs + WebSockets, deployed on @vercel. Go play
with friends:

[link]
```
Tags @nextjs + @vercel — fun project that shows off their platform well, both RT builders.

### Example 5: Developer Tool (The Argument angle)

```
Most API documentation is either auto-generated garbage or a
hand-maintained wiki that's 6 months out of date. There's no
middle ground.

I built a tool that generates docs from your actual route handlers
— reads the types, extracts validation rules, hits the endpoints
to get real response shapes. Docs that can't drift from the code.

Works with Express and Fastify so far. Here's the repo:

[link] @CloudflareDev
```
Tags @CloudflareDev — if deployed on their platform. The opinionated opening invites QTs from people who've felt the same pain.

### Why These Work

- **Personal throughout**: "I built", "I needed", "I got frustrated", "I spent my weekend"
- **Inviting**: "try it", "go give it a try", "go play with friends", "check it out", "here's the repo"
- **Specific details**: ~1,200 lines of Go, ~3KB gzipped, 40 Lambda functions, round 4, 6 months out of date
- **Honest**: "took more effort than expected", "still rough", "works with Express and Fastify so far"
- **Tags earn reach**: each targets a different platform/framework audience
- **Opinionated where it fits**: "auto-generated garbage", "no middle ground" — invites QTs
- **Varied project types**: CLI, web app, library, game, dev tool — proves the skill generalizes

### Suggested Self-Replies

Generate 1-2 project-specific self-replies. For each, create the accompanying media using the appropriate skill.

**CLI/Library**: "Here's what the output looks like" + terminal screenshot. Or: "Here's the architecture" + use `/gemini-image-generator` to create a clean workflow/architecture diagram.

**Web App**: Use `/screenshot-capture` to grab a second view showing a different feature/state. Or: "Here's how it works under the hood" + use `/gemini-image-generator` to create a data flow or pipeline visual.

**Fun/Game Project**: Use `/screenshot-capture` to grab a funny or interesting result state. Or: "Best [results] so far: [list]."

**Dev Tool**: Use `/gemini-image-generator` to create a before/after visual comparison. Or: use `/screenshot-capture` to grab the tool's output for a real-world example.

---

## Edge Cases

- **No README or docs**: Ask the user to describe the project in 2-3 sentences.
- **No clear tech stack files**: Ask the user what they built it with.
- **Not deployed yet**: Use the repo link. "Still early but here it is" works fine.
- **Monorepo**: Ask the user which project/feature to tweet about.
