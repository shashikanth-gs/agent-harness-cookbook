# What This Does Not Solve

- It does not execute tools safely by itself.
- It does not replace sandboxing for code execution.
- It does not decide whether a human approval was wise.
- It does not guarantee policy completeness.
- It does not discover every over-privileged tool automatically.
- It does not protect tools called outside the broker.

Residual risk remains when tool metadata is wrong, tenant labels are stale,
approval UI hides important evidence, or downstream systems expose side effects
that the broker does not model.
