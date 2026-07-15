# Pattern

RAG Access Control and Provenance filters candidate chunks by authorization
before answer synthesis and carries source evidence into the final answer.

Flow:

1. Preserve the original user query and task scope.
2. Check tenant, role, domain, lifecycle, and confidentiality before context.
3. Revalidate cached chunks and exclude deleted or unloaded sources.
4. Rank only authorized candidates.
5. Label retrieved content as evidence, not authority.
6. Require citations that point to retrieved source ids and versions.
7. Validate answer citations.
8. Return no authorized source instead of hallucinating when retrieval is empty.

This pattern works with Prompt Injection containment and Tool Privilege Broker.
An authorized document can still be poisoned; retrieval authorization decides
who may see it, not whether its text can issue instructions.
