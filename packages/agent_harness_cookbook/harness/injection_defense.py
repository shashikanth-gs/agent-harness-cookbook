from __future__ import annotations

import base64
import binascii
import re
import secrets
import string
from dataclasses import dataclass, field
from typing import Callable, Literal


ContentRole = Literal["authority", "task_intent", "evidence", "observation", "context", "delegated_instruction"]


@dataclass
class DefenseDecision:
    is_safe: bool
    reason: str
    confidence: float


@dataclass(frozen=True)
class InjectionScanResult:
    cleaned_text: str
    findings: list[str]
    decoded_findings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SourceClassification:
    source: str
    trust_level: str
    content_role: ContentRole
    requires_citation: bool


INJECTION_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("instruction_override", re.compile(r"\b(ignore|disregard|forget|override)\b.+\b(instruction|policy|previous|prior|rules)\b", re.I)),
    ("secret_exfiltration", re.compile(r"\b(print|reveal|send|dump|exfiltrate)\b.+\b(secret|token|api key|credential|env)\b", re.I)),
    ("unsafe_prod_action", re.compile(r"\b(restart|rollback|delete|disable)\b.+\b(prod|production|payment-service|validation)\b", re.I)),
    ("policy_bypass", re.compile(r"\b(skip|bypass|disable)\b.+\b(approval|policy|validation|guardrail)\b", re.I)),
]


def classify_source(source: str) -> SourceClassification:
    if source in {"system", "policy", "platform_policy"}:
        return SourceClassification(source, "trusted", "authority", False)
    if source == "user":
        return SourceClassification(source, "user", "task_intent", False)
    if source in {"retrieved_document", "openapi_description", "confluence_page", "runbook"}:
        return SourceClassification(source, "untrusted", "evidence", True)
    if source in {"tool_result", "log_search", "metrics_lookup", "release_events", "ticket", "log_line"}:
        return SourceClassification(source, "untrusted", "observation", True)
    if source in {"agent_message", "subagent_message"}:
        return SourceClassification(source, "delegated", "delegated_instruction", True)
    return SourceClassification(source, "untrusted", "context", True)


def scan_for_injection(text: str) -> InjectionScanResult:
    findings = [name for name, pattern in INJECTION_PATTERNS if pattern.search(text)]
    decoded_findings: list[str] = []
    for token in re.findall(r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{16,}={0,2}(?![A-Za-z0-9+/])", text):
        try:
            decoded = base64.b64decode(token, validate=True).decode("utf-8")
        except (binascii.Error, UnicodeDecodeError, ValueError):
            continue
        decoded_findings.extend(f"decoded:{name}" for name, pattern in INJECTION_PATTERNS if pattern.search(decoded))

    cleaned = text
    if findings or decoded_findings:
        cleaned = re.sub(
            r"\b(ignore|disregard|forget|override)\b[^.\n]*\b(instruction|policy|previous|prior|rules)\b[^.\n]*[.]?",
            "[REMOVED_UNTRUSTED_INSTRUCTION]",
            cleaned,
            flags=re.I,
        )
        cleaned = re.sub(
            r"\b(restart|rollback|delete|disable)\b[^.\n]*(prod|production|payment-service|validation)[^.\n]*[.]?",
            "[REMOVED_UNTRUSTED_ACTION]",
            cleaned,
            flags=re.I,
        )

    return InjectionScanResult(cleaned, findings, decoded_findings)


class InstructionBoundary:
    """
    Implements randomized XML boundaries to prevent instruction spoofing in LLM prompts.
    """
    def __init__(self, tag_prefix: str = "instr") -> None:
        self._tag_prefix = tag_prefix
        self._current_tag = self._generate_secure_tag()

    def _generate_secure_tag(self) -> str:
        """Generates a random alphanumeric suffix to prevent tag prediction."""
        suffix = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        return f"{self._tag_prefix}_{suffix}"

    def get_boundary_tag(self) -> str:
        return self._current_tag

    def wrap_instruction(self, instruction: str) -> str:
        tag = self.get_boundary_tag()
        return f"<{tag}>\n{instruction}\n</{tag}>"

    def wrap_untrusted_data(self, data: str) -> str:
        """Wraps untrusted data in a separate tag to clearly demarcate it from instructions."""
        tag = f"{self._current_tag}_data"
        return f"<{tag}>\n{data}\n</{tag}>"

class SemanticAuditor:
    """
    Uses a secondary, smaller LLM or a deterministic heuristic to audit inputs 
    for prompt injection or goal hijacking before processing.
    """
    def __init__(self, auditing_llm_callback: Callable[[str], str] | None = None) -> None:
        # auditing_llm_callback should take the prompt and return 'SAFE' or 'UNSAFE: <reason>'
        self.auditor = auditing_llm_callback

    def check_input(self, user_input: str) -> DefenseDecision:
        # Deterministic checks first
        suspicious_phrases = [
            "ignore previous instructions", 
            "system override", 
            "forget all rules", 
            "you are now", 
            "output the system prompt"
        ]
        
        lower_input = user_input.lower()
        for phrase in suspicious_phrases:
            if phrase in lower_input:
                return DefenseDecision(
                    is_safe=False,
                    reason=f"Detected deterministic injection heuristic: '{phrase}'",
                    confidence=1.0
                )

        # Semantic check using a secondary LLM if provided
        if self.auditor:
            try:
                result = self.auditor(user_input)
                if result.startswith("UNSAFE"):
                    return DefenseDecision(
                        is_safe=False,
                        reason=result.removeprefix("UNSAFE: ").strip(),
                        confidence=0.9
                    )
            except Exception as e:
                # Fail open or closed depending on enterprise posture. We choose closed for safety.
                return DefenseDecision(
                    is_safe=False,
                    reason=f"Auditor model failed to respond: {str(e)}",
                    confidence=1.0
                )
                
        return DefenseDecision(is_safe=True, reason="Input passed semantic and heuristic checks.", confidence=0.8)

class TaskShield:
    """
    Evaluates whether a proposed agent tool call aligns with the original goal.
    """
    def __init__(self, original_goal: str) -> None:
        self.original_goal = original_goal

    def verify_tool_alignment(self, tool_name: str, arguments: dict, justification: str) -> DefenseDecision:
        # In a real enterprise system, this might use an LLM or an allowed-actions graph.
        # Here we do a basic semantic alignment check (mocked).
        if "exfiltrate" in tool_name.lower() or "delete" in tool_name.lower() and "delete" not in self.original_goal.lower():
            return DefenseDecision(
                is_safe=False,
                reason="Tool proposed is a destructive action not aligned with the read-only goal.",
                confidence=0.95
            )
            
        return DefenseDecision(
            is_safe=True,
            reason="Tool invocation aligns with original task scope.",
            confidence=0.7
        )
