from __future__ import annotations

import secrets
import string
from dataclasses import dataclass
from typing import Callable, Literal

@dataclass
class DefenseDecision:
    is_safe: bool
    reason: str
    confidence: float

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
