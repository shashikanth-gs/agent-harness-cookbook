# Article Scheduling Workspace

This directory is the content planning and drafting workspace for allsrc.dev articles.

## What This Is

A VCS-controlled workspace where an AI agent (Claude Code, Codex, or any agent that reads project instructions) can:
- Understand the overall content intent and series context
- See what's published, in-progress, and planned
- Draft the next article when asked
- Summarize daily status on demand

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
3. Read any related published articles in `articles/` for continuity
4. Draft the **canonical allsrc.dev version first** into `drafts/<##>-<slug>.md`
5. Generate **platform-specific variants** as needed:
   - `drafts/<##>-<slug>.devto.md` — Dev.to with YAML front matter and canonical URL
   - `drafts/<##>-<slug>.linkedin.md` — Short post (1,300-1,900 chars) with hook
   - `drafts/<##>-<slug>.medium.md` — No Mermaid, no MDX metadata
6. All variants must include **2-3 backlinks to allsrc.dev**
7. Update the tracker status to `in-progress`

When the draft is approved, the user moves it to `articles/` and updates status to `published`.

## Canonical Source

**allsrc.dev is the canonical source for all content.** Publish there first, wait for indexing, then cross-post with canonical URLs pointing back. See `STYLE_GUIDE.md` for platform-specific formatting and canonical link setup.

## Key Files

| File | Purpose |
|------|---------|
| `CONTENT_PLAN.md` | Master tracker — series intent, article table, references |
| `STYLE_GUIDE.md` | Tone, structure, formatting rules for all articles |
| `articles/` | Published/final articles |
| `drafts/` | Work-in-progress drafts |

## Repository Context

The code and patterns referenced in these articles live in the `agent-harness-cookbook` repo:
https://github.com/shashikanth-gs/agent-harness-cookbook

When drafting, the agent should cross-reference that repo for accurate code examples, pattern details, and architecture descriptions.
