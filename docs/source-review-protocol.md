# Source Review Protocol

Before implementing or materially changing any pattern, framework mapping, demo,
or topic in this repo, do a current-source review.

## Required Before Implementation

1. Read current official docs for any named framework, protocol, model platform,
   or standard involved in the topic.
2. Prefer primary sources:
   - official framework docs,
   - official protocol specifications,
   - standards bodies,
   - government or recognized security guidance,
   - official project repositories when docs are incomplete.
3. Record the reviewed sources in the pattern's `source-review.md`.
4. Capture design consequences, not just links.
5. If a source is outdated, deprecated, or in maintenance mode, call that out.
6. Keep implementation local-first unless the source review proves an external
   dependency is necessary for the demo.

## What to Look For

- current framework capabilities,
- changed APIs or runtime assumptions,
- security updates,
- observability conventions,
- human-in-the-loop and checkpointing support,
- MCP/tool authorization guidance,
- RAG provenance guidance,
- evaluation and CI practices,
- deprecation or maintenance status.

## Implementation Rule

Do not start a new pattern implementation from model memory alone. Start from a
short, current-source summary and keep the reference implementation adaptable to
multiple runtimes.
