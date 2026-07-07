# Implementation Spec

Implement a structured trace object with a stable trace id and ordered steps.
Every step must have a name, timestamp, and redacted payload. The trace must not
store private chain-of-thought.
