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
