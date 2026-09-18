# Article Scheduling Workspace

This directory is the **self-contained** content planning and drafting workspace for allsrc.dev articles. Everything an agent needs to understand the series, read past work, and draft the next article is here — no external repo checkout required.

## What This Is

A VCS-controlled workspace where an AI agent (Claude Code, Codex, or any agent that reads project instructions) can:
- Understand the overall content intent and series context
- Read all previously published articles for voice, continuity, and cross-references
- Read the background context (threat model, architecture, reference landscape)
- See what's published, in-progress, and planned
- Draft the next article with platform-specific variants when asked
- Summarize daily status on demand

## Directory Structure

```
FINAL/
├── CLAUDE.md              ← You are here. Agent instructions.
├── CONTENT_PLAN.md        ← Master tracker: intent, article table, references, backlog
├── STYLE_GUIDE.md         ← Voice, article template, platform adaptations, canonical/backlink strategy
├── .gitignore
├── articles/              ← Published/final articles (MDX canonical versions)
│   ├── 00-introduction.mdx
│   ├── 01-tool-privilege-broker.mdx
│   ├── ...
│   └── 12-agent-lifecycle-profile.mdx
├── drafts/                ← Work-in-progress drafts and platform variants
│   ├── 13-identity-propagation.md          (canonical draft)
│   ├── 13-identity-propagation.devto.md    (Dev.to variant)
│   ├── 13-identity-propagation.linkedin.md (LinkedIn post)
│   └── 13-identity-propagation.medium.md   (Medium variant)
└── context/               ← Background docs for series continuity
    ├── 00-what-is-an-agent-harness.md
    ├── 03-enterprise-agent-threat-model.md
    ├── 05-authority-vs-context.md
    ├── reference-architecture.md
    ├── source-landscape.md
    ├── use-case-scenarios.md
    ├── what-this-cookbook-does-not-cover.md
    └── identity-and-principal-propagation.md
```

## Daily Workflow

The user will ask: **"What's pending for today?"**
The agent should:
1. Read `CONTENT_PLAN.md` for the tracker table
2. Find the next article with status `planned` or `in-progress`
3. Summarize what's ready to work on, any blockers, and dependencies
4. When asked, draft content into `drafts/<##>-<slug>.md`

When the user says **"Create content for [topic]"**, the agent should:
1. Read `CONTENT_PLAN.md` for context, intent, and references
2. Read `STYLE_GUIDE.md` for tone, structure, formatting rules, and **platform-specific adaptation guidance**
3. Read related published articles in `articles/` for voice continuity and cross-references
4. Read relevant background in `context/` for technical accuracy
5. Draft the **canonical allsrc.dev version first** into `drafts/<##>-<slug>.md`
6. Generate **platform-specific variants** as needed:
   - `drafts/<##>-<slug>.devto.md` — Dev.to with YAML front matter and canonical URL
   - `drafts/<##>-<slug>.linkedin.md` — Short post (1,300-1,900 chars) with hook
   - `drafts/<##>-<slug>.medium.md` — No Mermaid, no MDX metadata
7. All variants must include **2-3 backlinks to allsrc.dev**
8. Update the tracker status to `in-progress`

When the draft is approved, the user moves it to `articles/` and updates status to `published`.

## Canonical Source

**allsrc.dev is the canonical source for all content.** Publish there first, wait for indexing, then cross-post with canonical URLs pointing back. See `STYLE_GUIDE.md` for platform-specific formatting, canonical link setup, and backlink placement rules.

## Key Files — What to Read and When

| File | When to Read | Purpose |
|------|-------------|---------|
| `CONTENT_PLAN.md` | Every session | Master tracker — series intent, article table, reference library, backlog |
| `STYLE_GUIDE.md` | Before any drafting | Voice, article template, platform adaptations, canonical/backlink strategy |
| `articles/*.mdx` | When drafting (read related ones) | Published articles — voice reference, cross-link targets, continuity |
| `context/*.md` | When drafting (read relevant ones) | Background: architecture, threat model, authority hierarchy, scenarios |
| `drafts/` | When resuming work | In-progress drafts and platform variants |

## Source Code Repository

The working code and patterns referenced in these articles live in the `agent-harness-cookbook` repo:
https://github.com/shashikanth-gs/agent-harness-cookbook

When drafting, the agent should cross-reference that repo for accurate code examples, pattern details, and architecture descriptions. The `context/` directory here contains the key docs from that repo, but the repo has the full source code, tests, fixtures, and demos.

## Keeping This Directory Current

When new articles are published or context docs are updated in the source repo:
- Copy the final MDX to `articles/`
- Update any changed context docs in `context/`
- Update `CONTENT_PLAN.md` status from `in-progress` → `published`

This directory is the agent's single source of truth. If it's not here, the agent doesn't know about it.
