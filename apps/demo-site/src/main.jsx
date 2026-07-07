import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { BookOpen, ClipboardCheck, Gauge, GitBranch, ShieldCheck } from "lucide-react";
import "./styles.css";

const patterns = [
  "Tool Privilege Broker",
  "HITL Approval Gate",
  "Decision Trace and Audit",
  "Cost and Tool Budgeting",
  "Redaction Boundary",
  "Prompt Injection and Goal Hijack",
  "RAG Access Control and Provenance",
  "Memory Isolation",
  "Sandboxed Execution",
  "Agent Evaluations",
  "CI/CD Evaluation Gates",
  "Agent Lifecycle Profile",
];

function App() {
  const [request, setRequest] = useState(
    "Orders are not being processed after the latest release. Investigate the likely cause and recommend next steps."
  );
  const [requestRemediation, setRequestRemediation] = useState(false);
  const [demo, setDemo] = useState(null);
  const [catalog, setCatalog] = useState(null);
  const [loading, setLoading] = useState(false);
  const [catalogLoading, setCatalogLoading] = useState(false);

  async function runDemo() {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/demos/service-incident-investigation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ request, request_remediation: requestRemediation }),
      });
      setDemo(await response.json());
    } finally {
      setLoading(false);
    }
  }

  async function runCatalog() {
    setCatalogLoading(true);
    try {
      const response = await fetch("http://localhost:8000/patterns/run-all");
      setCatalog(await response.json());
    } finally {
      setCatalogLoading(false);
    }
  }

  return (
    <main>
      <section className="hero">
        <div>
          <p className="eyebrow">Open-source engineering reference</p>
          <h1>Agent Harness Cookbook</h1>
          <p className="lede">
            A practical reference for designing enterprise-grade agent harnesses.
            It is not a framework. It is a cookbook of patterns, examples,
            implementation specs, and prompts.
          </p>
        </div>
        <div className="heroPanel" aria-label="Capability summary">
          <div><ShieldCheck size={20} /> bounded tools</div>
          <div><ClipboardCheck size={20} /> approval gates</div>
          <div><GitBranch size={20} /> decision trace</div>
          <div><Gauge size={20} /> budget controls</div>
        </div>
      </section>

      <section className="band">
        <div className="sectionHeader">
          <h2>Capability Map</h2>
          <button onClick={runCatalog} disabled={catalogLoading}>
            {catalogLoading ? "Running..." : "Run All Patterns"}
          </button>
        </div>
        <div className="grid">
          {patterns.map((pattern) => (
            <article className="pattern" key={pattern}>
              <BookOpen size={18} />
              <span>{pattern}</span>
            </article>
          ))}
        </div>
        {catalog && (
          <div className="catalogResult">
            <h3>Pattern Catalogue Result</h3>
            <pre>{JSON.stringify(catalog, null, 2)}</pre>
          </div>
        )}
      </section>

      <section className="band demo">
        <div>
          <h2>Service Incident Investigation</h2>
          <p>
            A generic local demo that combines tool policy, trace, audit,
            budgets, redaction, and approval for risky remediation.
          </p>
        </div>
        <label>
          Request
          <textarea value={request} onChange={(event) => setRequest(event.target.value)} />
        </label>
        <label className="check">
          <input
            type="checkbox"
            checked={requestRemediation}
            onChange={(event) => setRequestRemediation(event.target.checked)}
          />
          Include a remediation request
        </label>
        <button onClick={runDemo} disabled={loading}>
          {loading ? "Running..." : "Run Demo"}
        </button>
        {demo && (
          <div className="results">
            <div>
              <h3>Outcome</h3>
              <p>{demo.result.summary}</p>
              <p><strong>Confidence:</strong> {demo.result.confidence}</p>
              <p><strong>Runbook:</strong> {demo.result.recommended_runbook}</p>
              {demo.result.remediation && (
                <p><strong>Remediation:</strong> {demo.result.remediation.status}</p>
              )}
            </div>
            <div>
              <h3>Budget</h3>
              <pre>{JSON.stringify(demo.budget, null, 2)}</pre>
            </div>
            <div>
              <h3>Trace</h3>
              <pre>{JSON.stringify(demo.trace.steps.slice(0, 6), null, 2)}</pre>
            </div>
          </div>
        )}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
