# Style Guide — Agent Harness Cookbook Articles

## Voice

- **Technical and direct.** Write for engineers who build systems, not executives who approve budgets.
- **Opinionated.** State what works and what doesn't. "Use this when X. Do not use this when Y."
- **Honest about limits.** Every article states what it proves and what it does not prove. No overclaiming.
- **No hype.** No "revolutionary," "game-changing," "cutting-edge." The code speaks.

## Structure

Every article follows this template:

```
export const metadata = {
  title: "...",
  description: "One sentence.",
  keywords: ["agent harness", "...", "..."]
}

# Title

Opening paragraph: what problem this solves, in 2-3 sentences. Include a brief scope note: "This is one of a starting set of harness patterns."

## Playground

Link to repo. List source files.

## Flow

Mermaid diagram showing the control flow.

## Code

Working code example with assert statements. Show the happy path, then show a failure/denial case.

## What Is Enforced

Bullet list of controls this pattern checks.

## Verification Scenarios

How to run tests. List what the tests prove.

"What this proves:" — one sentence.
"What this does not prove:" — one sentence.

## When to Use It

2-3 sentences. When to apply, when not to.

## References

2-4 external sources. Use inline links. Prefer arxiv, OWASP, NIST, named researchers.

## See Also

Cross-links to related patterns in the series.

Tags at bottom: `tag1` `tag2` `tag3`
```

## Formatting Rules

- **MDX format** with metadata export at top for online publishing
- **Mermaid diagrams** for flows — keep them under 15 nodes
- **Code blocks** use Python unless the pattern is language-agnostic
- **Assert statements** in code examples — the reader should be able to run them
- **No screenshots** — everything is text/code/diagram
- **Cross-references** use relative paths: `./06-prompt-injection-and-goal-hijack.mdx`
- **Reference links** use inline format: `[name](url)`

## Naming Conventions

- Article files: `##-slug-name.mdx` (e.g., `01-tool-privilege-broker.mdx`)
- Draft files: `##-slug-name.md` (plain markdown until ready for MDX conversion)
- Slugs match the pattern directory name in the cookbook repo

## Length

- Target 600-900 words per article
- Code examples: 20-40 lines each (2 examples per article typical)
- Mermaid diagrams: 8-15 nodes

## What Not to Do

- Don't write tutorials ("Step 1: Install Python")
- Don't explain what an LLM is
- Don't add disclaimers about AI safety in general — be specific about this pattern's risks
- Don't use "we" — use "the broker checks," "the harness enforces," direct statements
- Don't pad with filler paragraphs between sections

---

## Canonical Source and Backlink Strategy

**allsrc.dev is the canonical source for all content.** Every article is published on allsrc.dev first. All cross-posted versions point back to allsrc.dev via canonical URLs. This ensures:
- Search engines credit allsrc.dev as the authoritative source
- Link equity from cross-posts flows back to allsrc.dev
- No duplicate content risk across platforms

### Publishing Workflow

1. **Publish on allsrc.dev first** — this is the canonical version
2. **Wait 24-48 hours** for Google to index the original
3. **Cross-post to platforms** using their import/canonical features
4. **Add backlinks** within the article body where natural (see below)

### Backlink Placement (In Every Article)

Weave allsrc.dev links naturally into the content. Don't force them — they should add value:

- **Opening or closing:** "This is part of the [Agent Harness Cookbook series](https://allsrc.dev/series/agent-harness-cookbook)."
- **Code references:** "Full source and tests: [allsrc.dev/agent-harness-cookbook](https://allsrc.dev/agent-harness-cookbook)"
- **Cross-pattern links:** "See [Prompt Injection Defense](https://allsrc.dev/articles/06-prompt-injection) for the containment layer."
- **Author byline:** Link author name to allsrc.dev profile/about page

Target **2-3 backlinks to allsrc.dev per article** — enough for SEO, not so many it feels spammy.

---

## Platform-Specific Adaptations

The canonical MDX article on allsrc.dev is the **master copy**. Each platform gets an adapted version. The agent should produce both the master and platform variants when drafting.

### allsrc.dev (Canonical — MDX)

- Full article with all sections, Mermaid diagrams, code blocks
- MDX metadata export at top
- This is the version of record

### Dev.to

- **Format:** Markdown with YAML front matter
- **Canonical URL:** Always set to the allsrc.dev URL
- **Tags:** Up to 4 tags (e.g., `agentai`, `security`, `python`, `architecture`)
- **Adaptation:** Keep the full article largely intact — Dev.to readers expect depth
- **Mermaid:** Supported natively, keep as-is
- **Code blocks:** Supported, keep as-is
- **Footer:** Add "Originally published on [allsrc.dev](https://allsrc.dev/articles/...)"

```yaml
---
title: "Tool Privilege Broker"
published: true
description: "Enterprise action governance at the agent tool-call boundary."
tags: agentai, security, python, architecture
canonical_url: https://allsrc.dev/articles/01-tool-privilege-broker
cover_image: (optional)
---
```

### Medium

- **Import:** Use Medium's "Import Story" feature — paste the allsrc.dev URL and Medium auto-sets the canonical tag
- **Adaptation:** Remove Mermaid diagrams (not supported) — replace with a text description or an image export of the diagram. Remove MDX metadata.
- **Code blocks:** Supported via Medium's code formatting (use gists for long blocks)
- **Length:** Same as canonical — Medium rewards depth (6-8 min read is the sweet spot)
- **Tags:** Up to 5 tags
- **Footer:** "Read the full series with working code at [allsrc.dev](https://allsrc.dev/series/agent-harness-cookbook)"

### LinkedIn

LinkedIn gets **two versions** per article — a short post and optionally a full article.

**LinkedIn Post (primary — higher reach):**
- **Length:** 1,300-1,900 characters for best engagement
- **Hook:** First 140 characters decide if anyone reads the rest. Lead with the insight, not the announcement. No "Excited to share..." — start with the problem or a surprising fact.
- **Structure:** Hook → 3-4 short paragraphs → key takeaway → link to allsrc.dev
- **Format:** Short paragraphs (1-2 sentences each), line breaks between them, sparing use of bold for emphasis
- **Link:** One link to the full article on allsrc.dev at the end (LinkedIn suppresses reach for posts with links, so some prefer putting the link in the first comment instead)
- **No code blocks** — LinkedIn doesn't render them. Use plain text for short snippets.

```
The real question isn't "can the agent call this tool?"

It's: who is asking, which tenant, which environment,
does the action match the task, is there budget left,
and does approval bind to this exact action?

That's 9 checks before a tool call executes.
Most agent frameworks check zero of them.

The Tool Privilege Broker makes all 9 executable
— the model does not authorize itself.

Full pattern with working code:
https://allsrc.dev/articles/01-tool-privilege-broker
```

**LinkedIn Article (optional — lower reach, higher depth):**
- **Length:** 800-1,200 words
- **Format:** Subheadings, bullet points, short paragraphs — no walls of text
- **No canonical tag support** — use "Originally published on [allsrc.dev](...)" at the top
- **Images:** Add 1-2 images (diagram exports) to break up text
- **CTA:** End with a call to follow or visit allsrc.dev for the series

### Hashnode

- **Format:** Markdown with YAML front matter
- **Canonical URL:** Set to allsrc.dev URL
- **Custom domain:** If allsrc.dev is hosted on Hashnode, it becomes the canonical source directly
- **Tags:** Up to 5
- **Mermaid:** Supported natively
- **Full article:** No adaptation needed beyond front matter

```yaml
---
title: "Tool Privilege Broker"
subtitle: "Enterprise action governance at the agent tool-call boundary."
slug: 01-tool-privilege-broker
canonical: https://allsrc.dev/articles/01-tool-privilege-broker
tags: agent-ai, security, python, enterprise
---
```

### Substack

- **Format:** Rich text editor (paste from markdown, manually format)
- **Canonical:** No native canonical tag support — add "Originally published on [allsrc.dev](...)" prominently
- **Adaptation:** Remove Mermaid (not supported). Code blocks are basic — keep them short. Substack favors narrative over reference-style writing, so add a brief narrative intro before the technical content.
- **Length:** 1,000-1,500 words (Substack readers expect email-length, not reference docs)
- **CTA:** "Subscribe for the full series" + link to allsrc.dev

### X / Twitter

- **Format:** Thread (5-8 tweets) or single post with link
- **Hook tweet:** Bold claim or surprising stat in under 280 characters
- **Thread structure:** Problem → What most people do wrong → What the pattern does → 1 code snippet as image → Link to allsrc.dev
- **Always link** to the full allsrc.dev article in the last tweet

---

## Platform Priority

When time is limited, prioritize in this order:

1. **allsrc.dev** — always first, always canonical
2. **Dev.to** — highest technical reach, native canonical support, lowest adaptation effort
3. **LinkedIn post** — professional visibility, drives traffic
4. **Medium** — broad reach, good canonical import
5. **Hashnode** — strong SEO, developer audience
6. **Substack** — if building an email list
7. **X thread** — for amplification

---

## Agent Drafting Instructions

When creating content for a specific platform, the agent should:

1. Draft the **canonical allsrc.dev version first** (full MDX article)
2. Generate **platform-specific variants** in separate files:
   - `drafts/##-slug.md` — canonical version
   - `drafts/##-slug.devto.md` — Dev.to front matter + adapted body
   - `drafts/##-slug.linkedin.md` — Short post + optional article
   - `drafts/##-slug.medium.md` — Medium-adapted (no Mermaid, no MDX)
3. All variants must include **backlinks to allsrc.dev**
4. Update `CONTENT_PLAN.md` status to `in-progress`
