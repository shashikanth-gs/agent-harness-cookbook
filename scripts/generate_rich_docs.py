import os
from pathlib import Path
from litellm import completion

PROMPT = """
You are an expert technical writer and enterprise AI architect.
Below is the source code for a specific Enterprise AI Agent Harness pattern.
You are given the pure Python harness implementation, the pure Python usage example, and the LangGraph integration example.

Your task is to write the contents for a specific markdown file. 
Keep it highly professional, technical, and publish-ready. Use Markdown formatting.

Context Files:
{files_content}

---
Write the content for: {doc_type}

Instructions for doc_type:
- README.md: A high-level overview of the pattern, what problem it solves in enterprise AI, and how to run the examples. (Max 300 words).
- article.md: A thought-leadership style article explaining WHY this pattern is necessary for production, the risks of not having it, and how the harness acts as an operating system around the agent. (Max 600 words).
- implementation-spec.md: Deeply technical specification. Detail the classes used, the architecture, and explicitly explain how the pure Python implementation differs from the LangGraph integration (e.g., how the harness wraps LangGraph nodes). (Max 800 words).

Output ONLY the markdown content. Do not include markdown code block wrappers (```markdown) around the entire output.
"""

def read_file_safe(path: Path) -> str:
    if path.exists():
        return path.read_text()
    return ""

def main():
    base_path = Path("/Users/skgs/Views/my-open-souce-projects/agent-harness")
    patterns_dir = base_path / "patterns"
    harness_dir = base_path / "packages" / "agent_harness_cookbook" / "harness"
    
    # Mapping of pattern directory to its core harness module file
    pattern_to_module = {
        "01-tool-privilege-broker": "privilege_broker.py",
        "02-hitl-approval-gate": "approvals.py",
        "03-decision-trace-and-audit": "audit.py",
        "04-cost-and-tool-budgeting": "budgets.py",
        "05-redaction-boundary": "redaction.py",
        "06-prompt-injection-and-goal-hijack": "injection_defense.py",
        "07-rag-access-control-and-provenance": "rag_governance.py",
        "08-memory-isolation": "memory_isolation.py",
        "09-sandboxed-execution": "sandbox.py",
        "10-agent-evaluations": "evaluations.py",
        "11-ci-cd-evaluation-gates": "cicd.py",
        "12-agent-lifecycle-profile": "lifecycle.py",
    }
    
    doc_types = ["README.md", "article.md", "implementation-spec.md"]
    model_name = os.environ.get("DOCS_MODEL", "gpt-4o")
    
    for p_dir in sorted(os.listdir(patterns_dir)):
        full_p_dir = patterns_dir / p_dir
        if not full_p_dir.is_dir() or p_dir not in pattern_to_module:
            continue
            
        print(f"Processing {p_dir}...")
        
        # Gather context
        module_file = harness_dir / pattern_to_module[p_dir]
        module_content = read_file_safe(module_file)
        
        # Find the python files in the pattern dir
        inner_dir = list(full_p_dir.glob("pattern_*"))
        if not inner_dir:
            continue
        inner_dir = inner_dir[0]
        
        example_content = read_file_safe(inner_dir / "example.py")
        langgraph_content = read_file_safe(inner_dir / "langgraph_example.py")
        
        files_context = (
            f"--- {module_file.name} ---\\n{module_content}\\n\\n"
            f"--- example.py ---\\n{example_content}\\n\\n"
            f"--- langgraph_example.py ---\\n{langgraph_content}\\n"
        )
        
        for doc in doc_types:
            print(f"  Generating {doc}...")
            prompt = PROMPT.format(files_content=files_context, doc_type=doc)
            
            try:
                response = completion(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                output = response.choices[0].message.content
                if output.startswith("```markdown"):
                    output = output[11:]
                if output.startswith("```"):
                    output = output[3:]
                if output.endswith("```"):
                    output = output[:-3]
                    
                (full_p_dir / doc).write_text(output.strip() + "\\n")
            except Exception as e:
                print(f"  Failed to generate {doc}: {e}")

if __name__ == "__main__":
    main()
