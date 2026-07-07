import os
from pathlib import Path

docs = {
    "06-prompt-injection-and-goal-hijack": {
        "title": "Prompt Injection & Goal Hijack",
        "spec": "Implements a dynamic `InstructionBoundary` using randomized XML tags to prevent spoofing, alongside a `SemanticAuditor` for upfront adversarial classification and a `TaskShield` for runtime alignment."
    },
    "07-rag-access-control-and-provenance": {
        "title": "RAG Access Control & Provenance",
        "spec": "Implements a `RetrievalAuthorizer` to enforce Relationship-Based Access Control (ReBAC) dynamically during RAG lookups. Includes a `ProvenanceTracker` to sign retrieved chunks and verify citations against hallucination."
    },
    "08-memory-isolation": {
        "title": "Memory Isolation",
        "spec": "Provides a `NamespaceMemoryManager` mimicking secure Redis behavior. Implements tiered memory (Working vs Episodic) with strict namespace isolation and TTL purging managed via a `TenantContextGateway`."
    },
    "09-sandboxed-execution": {
        "title": "Sandboxed Execution",
        "spec": "Implements a `ContainerRuntime` mock demonstrating robust sandbox execution limits, including egress network allow-listing (simulating EACCES), CPU tick constraints, and graceful handling of segfaults or timeouts."
    },
    "10-agent-evaluations": {
        "title": "Agent Evaluations",
        "spec": "Introduces a `TrajectoryScorer` shifting from outcome-based to trajectory-based evaluation. Combines LLM-as-a-judge for plan adherence with deterministic checks for tool efficiency and dangerous argument detection."
    },
    "11-ci-cd-evaluation-gates": {
        "title": "CI/CD Evaluation Gates",
        "spec": "Implements an `EvaluationGate` utilizing Welch's t-test (simulated) to detect statistically significant regressions in agent behavior against a golden dataset baseline, actively blocking poor deployments."
    },
    "12-agent-lifecycle-profile": {
        "title": "Agent Lifecycle Profile",
        "spec": "Implements an `AgentManifest` acting as a secure identity passport for the agent. Binds operational limits (budgets, execution bounds) with a cryptographic signature verified by a `LifecycleManager` to prevent runtime tampering."
    }
}

base_path = Path("/Users/skgs/Views/my-open-souce-projects/agent-harness/patterns")

for pattern_dir, content in docs.items():
    dir_path = base_path / pattern_dir
    if not dir_path.exists():
        continue
        
    spec_path = dir_path / "implementation-spec.md"
    article_path = dir_path / "article.md"
    
    spec_content = f"# {content['title']} - Implementation Specification\\n\\n## Overview\\n{content['spec']}\\n\\n## Components\\nSee `example.py` for concrete integration."
    
    article_content = f"# {content['title']}\\n\\nEnterprise agents require robust safeguards. This pattern demonstrates:\\n- {content['spec']}\\n\\nExplore the implementation specification and example for a deep dive."
    
    spec_path.write_text(spec_content)
    article_path.write_text(article_content)

print("Docs generated.")
