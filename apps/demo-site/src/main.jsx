import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  AlertTriangle,
  BookOpen,
  CheckCircle2,
  ClipboardCheck,
  FileJson,
  Gauge,
  GitBranch,
  Lock,
  Play,
  ShieldCheck,
  Workflow,
  XCircle,
} from "lucide-react";
import "./styles.css";

const API_BASE = "http://localhost:8000";

const patternCatalog = [
  { id: "01", key: "01-tool-privilege-broker", name: "Tool Privilege Broker", detail: "Tool calls are checked against role, tenant, resource, action, and environment policy." },
  { id: "02", key: "02-hitl-approval-gate", name: "HITL Approval Gate", detail: "Risky actions pause with an approval request bound to the exact action hash." },
  { id: "03", key: "03-decision-trace-and-audit", name: "Decision Trace and Audit", detail: "Every important decision is recorded for review and evaluation." },
  { id: "04", key: "04-cost-and-tool-budgeting", name: "Cost and Tool Budgeting", detail: "Model, token, and tool-call limits stop runaway execution." },
  { id: "05", key: "05-redaction-boundary", name: "Redaction Boundary", detail: "Sensitive values are removed before results leave the harness boundary." },
  { id: "06", key: "06-prompt-injection-and-goal-hijack", name: "Prompt Injection and Goal Hijack", detail: "Untrusted instructions in inputs, logs, or retrieved content are downgraded." },
  { id: "07", key: "07-rag-access-control-and-provenance", name: "RAG Access Control and Provenance", detail: "Retrieved content is authorized and tracked by source." },
  { id: "08", key: "08-memory-isolation", name: "Memory Isolation", detail: "Memory stays scoped to the right tenant, user, task, and agent." },
  { id: "09", key: "09-sandboxed-execution", name: "Sandboxed Execution", detail: "Generated code runs under execution policy instead of on the host directly." },
  { id: "10", key: "10-agent-evaluations", name: "Agent Evaluations", detail: "The trajectory is checked, not only the final answer." },
  { id: "11", key: "11-ci-cd-evaluation-gates", name: "CI/CD Evaluation Gates", detail: "Regression checks block unsafe harness changes." },
  { id: "12", key: "12-agent-lifecycle-profile", name: "Agent Lifecycle Profile", detail: "Agent identity and lifecycle metadata constrain runtime behavior." },
];

const defaultRequest =
  "Orders are not being processed after the latest release. Investigate the likely cause and recommend next steps.";

const runSteps = [
  {
    title: "1. Your text becomes the incident task",
    detail: "The API receives this request as the user goal. The harness also scans it for prompt-injection style instructions.",
  },
  {
    title: "2. A mock model classifies intent",
    detail: "The demo uses a deterministic mock model, not a real LLM, so the run is repeatable locally.",
  },
  {
    title: "3. The agent asks for evidence",
    detail: "The harness evaluates each proposed tool call before returning mock logs, metrics, and release events.",
  },
  {
    title: "4. Untrusted evidence is cleaned",
    detail: "The logs intentionally contain a malicious instruction. The harness records it and removes the unsafe action text.",
  },
  {
    title: "5. Risky remediation pauses",
    detail: "If remediation is enabled, production restart is not executed. The harness returns an approval request with an action hash.",
  },
  {
    title: "6. The run is evaluated",
    detail: "The final answer is less important than the trajectory: policy decisions, budget, redaction, approval, and trace events.",
  },
];

function shortHash(value) {
  if (!value) return "none";
  return `${String(value).slice(0, 10)}...`;
}

function getEvents(run, eventType) {
  return run?.audit?.filter((event) => event.event_type === eventType) ?? [];
}

function statusTone(status) {
  if (["passed", "allow", "approved", "complete", "completed", "ok"].includes(status)) return "good";
  if (["approval_required", "waiting_for_approval", "detected", "warning"].includes(status)) return "warn";
  if (["deny", "denied", "failed", "error"].includes(status)) return "bad";
  return "idle";
}

function summarizePayload(payload) {
  if (!payload) return "";
  if (payload.tool && payload.decision) return `${payload.tool}: ${payload.decision}`;
  if (payload.reason) return payload.reason;
  if (payload.findings?.length) return payload.findings.join(", ");
  if (payload.status) return payload.status;
  if (payload.usage) return `usage ${JSON.stringify(payload.usage)}`;
  return JSON.stringify(payload).slice(0, 140);
}

function buildControlChecks(run) {
  const evaluation = run?.evaluation ?? {};
  const remediation = run?.result?.remediation;
  const remediationStatus = remediation?.status ?? (run ? "not_requested" : "not_run");
  const policyEvents = getEvents(run, "policy.decided");

  return [
    {
      label: "Input and source guard",
      icon: ShieldCheck,
      status: run ? (evaluation.detected_injection ? "detected" : "checked") : "not_run",
      detail: run
        ? evaluation.detected_injection
          ? "Injection-like text was detected and treated as untrusted content."
          : "No injection finding was emitted in this run."
        : "Waiting for a run.",
    },
    {
      label: "Tool privilege broker",
      icon: Lock,
      status: run ? (policyEvents.length ? "passed" : "not_seen") : "not_run",
      detail: run
        ? `${policyEvents.length} policy decision${policyEvents.length === 1 ? "" : "s"} recorded.`
        : "Waiting for tool decisions.",
    },
    {
      label: "Budget guard",
      icon: Gauge,
      status: run ? (evaluation.budget_recorded ? "passed" : "not_seen") : "not_run",
      detail: run?.budget
        ? `${run.budget.usage.model_calls} model calls, ${run.budget.usage.tool_calls} tool calls, ${run.budget.usage.tokens} tokens.`
        : "Waiting for budget usage.",
    },
    {
      label: "Redaction boundary",
      icon: ClipboardCheck,
      status: run ? (evaluation.secret_leak_absent ? "passed" : "failed") : "not_run",
      detail: run
        ? evaluation.secret_leak_absent
          ? "Known sensitive values are absent from the returned run."
          : "A sensitive value was found in the returned run."
        : "Waiting for output.",
    },
    {
      label: "Approval gate",
      icon: AlertTriangle,
      status: remediationStatus,
      detail:
        remediationStatus === "approval_required"
          ? `Pending ${remediation.request?.required_approver_role ?? "human"} approval. Action ${shortHash(remediation.action_hash)}.`
          : remediationStatus === "approved"
            ? `Approved and revalidated. Action ${shortHash(remediation.action_hash)}.`
            : run
              ? "No remediation approval was requested."
              : "Enable remediation to exercise the gate.",
    },
    {
      label: "Trajectory evaluation",
      icon: GitBranch,
      status: run ? (evaluation.passed ? "passed" : "failed") : "not_run",
      detail: run
        ? evaluation.passed
          ? `${evaluation.event_count ?? run.audit?.length ?? 0} events passed deterministic checks.`
          : "One or more trajectory checks failed."
        : "Waiting for evaluation.",
    },
  ];
}

function StatusPill({ status }) {
  return <span className={`pill ${statusTone(status)}`}>{String(status).replaceAll("_", " ")}</span>;
}

function ControlRow({ check }) {
  const Icon = check.icon;
  return (
    <div className="controlRow">
      <Icon size={18} aria-hidden="true" />
      <div>
        <div className="rowTitle">
          <span>{check.label}</span>
          <StatusPill status={check.status} />
        </div>
        <p>{check.detail}</p>
      </div>
    </div>
  );
}

function App() {
  const [request, setRequest] = useState(defaultRequest);
  const [requestRemediation, setRequestRemediation] = useState(true);
  const [workflow, setWorkflow] = useState("python");
  const [demo, setDemo] = useState(null);
  const [catalog, setCatalog] = useState(null);
  const [loading, setLoading] = useState(false);
  const [catalogLoading, setCatalogLoading] = useState(false);
  const [error, setError] = useState("");
  const [catalogError, setCatalogError] = useState("");

  const controlChecks = useMemo(() => buildControlChecks(demo), [demo]);
  const timeline = demo?.audit?.slice(0, 14) ?? [];
  const policyEvents = getEvents(demo, "policy.decided");
  const toolResults = getEvents(demo, "tool.result.classified");
  const catalogPatternCount = catalog ? Object.keys(catalog).filter((key) => key !== "audit").length : 0;

  async function runDemo() {
    setLoading(true);
    setError("");
    try {
      const endpoint =
        workflow === "langgraph"
          ? `${API_BASE}/demos/service-incident-investigation/langgraph`
          : `${API_BASE}/demos/service-incident-investigation`;
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ request, request_remediation: requestRemediation }),
      });
      if (!response.ok) throw new Error(`API returned ${response.status}`);
      setDemo(await response.json());
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Demo run failed");
    } finally {
      setLoading(false);
    }
  }

  async function runCatalog() {
    setCatalogLoading(true);
    setCatalogError("");
    try {
      const response = await fetch(`${API_BASE}/patterns/run-all`);
      if (!response.ok) throw new Error(`API returned ${response.status}`);
      setCatalog(await response.json());
    } catch (caught) {
      setCatalogError(caught instanceof Error ? caught.message : "Pattern catalog failed");
    } finally {
      setCatalogLoading(false);
    }
  }

  return (
    <main className="appShell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Local harness run explorer</p>
          <h1>Agent Harness Cookbook</h1>
        </div>
        <div className="topbarMeta">
          <span>API {API_BASE}</span>
          <span>Mock tools</span>
        </div>
      </header>

      <section className="runSurface">
        <aside className="scenarioPanel">
          <div className="sectionTitle">
            <Workflow size={18} />
            <h2>Try an Incident Request</h2>
          </div>
          <p className="muted">
            Type an incident request and run a local simulation. The result is not a real production action;
            it shows which harness controls fire while the agent investigates.
          </p>

          <label>
            Incident request
            <textarea value={request} onChange={(event) => setRequest(event.target.value)} />
          </label>

          <div className="fieldGroup">
            <span className="fieldLabel">Runtime</span>
            <div className="segmented" aria-label="Workflow runtime">
              <button type="button" className={workflow === "python" ? "active" : ""} onClick={() => setWorkflow("python")}>
                Python
              </button>
              <button type="button" className={workflow === "langgraph" ? "active" : ""} onClick={() => setWorkflow("langgraph")}>
                LangGraph
              </button>
            </div>
          </div>

          <label className="check">
            <input
              type="checkbox"
              checked={requestRemediation}
              onChange={(event) => setRequestRemediation(event.target.checked)}
            />
            Also ask the agent to remediate production
          </label>

          <button type="button" className="primaryButton" onClick={runDemo} disabled={loading}>
            <Play size={17} />
            {loading ? "Running simulation" : "Run simulation"}
          </button>

          {error && <div className="notice bad"><XCircle size={18} /> {error}</div>}
        </aside>

        <section className="controlPanel" aria-label="Harness control status">
          <div className="sectionTitle">
            <ClipboardCheck size={18} />
            <h2>What Happens After Click</h2>
          </div>
          <ol className="runSteps">
            {runSteps.map((step) => (
              <li key={step.title}>
                <strong>{step.title}</strong>
                <p>{step.detail}</p>
              </li>
            ))}
          </ol>
        </section>
      </section>

      <section className="controlPanel fullWidth" aria-label="Harness control status">
          <div className="sectionTitle">
            <ShieldCheck size={18} />
            <h2>Controls Observed In This Run</h2>
          </div>
          <div className="controlList">
            {controlChecks.map((check) => (
              <ControlRow check={check} key={check.label} />
            ))}
          </div>
      </section>

      <section className="outcomeGrid">
        <section className="panel">
          <div className="sectionTitle">
            <CheckCircle2 size={18} />
            <h2>Agent Answer</h2>
          </div>
          {demo ? (
            <>
              <div className="outcomeHeader">
                <StatusPill status={demo.result.status ?? "completed"} />
                {demo.result.workflow && <span className="muted">Workflow: {demo.result.workflow}</span>}
              </div>
              <p className="summaryText">{demo.result.summary}</p>
              <dl className="keyValues">
                <div>
                  <dt>Confidence</dt>
                  <dd>{demo.result.confidence ?? "n/a"}</dd>
                </div>
                <div>
                  <dt>Evidence refs</dt>
                  <dd>{demo.result.evidence_refs?.join(", ") || "none"}</dd>
                </div>
                <div>
                  <dt>Runbook</dt>
                  <dd>{demo.result.recommended_runbook ?? "n/a"}</dd>
                </div>
                <div>
                  <dt>Remediation</dt>
                  <dd>{demo.result.remediation?.status?.replaceAll("_", " ") ?? "not requested"}</dd>
                </div>
              </dl>
            </>
          ) : (
            <p className="emptyState">No incident run yet.</p>
          )}
        </section>

        <section className="panel">
          <div className="sectionTitle">
            <Lock size={18} />
            <h2>Tool Decisions</h2>
          </div>
          {policyEvents.length ? (
            <div className="decisionList">
              {policyEvents.map((event) => (
                <div className="decisionRow" key={event.event_id}>
                  <span>{event.payload.tool}</span>
                  <StatusPill status={event.payload.decision} />
                  <small>{event.payload.reason}</small>
                </div>
              ))}
            </div>
          ) : (
            <p className="emptyState">No policy decisions recorded yet.</p>
          )}
        </section>

        <section className="panel">
          <div className="sectionTitle">
            <Gauge size={18} />
            <h2>Run Budget</h2>
          </div>
          {demo ? (
            <dl className="metricGrid">
              <div>
                <dt>Model calls</dt>
                <dd>{demo.budget.usage.model_calls}</dd>
              </div>
              <div>
                <dt>Tool calls</dt>
                <dd>{demo.budget.usage.tool_calls}</dd>
              </div>
              <div>
                <dt>Tokens</dt>
                <dd>{demo.budget.usage.tokens}</dd>
              </div>
              <div>
                <dt>Retries</dt>
                <dd>{demo.budget.usage.retries}</dd>
              </div>
            </dl>
          ) : (
            <p className="emptyState">Budget appears after a run.</p>
          )}
        </section>
      </section>

      <section className="timelinePanel">
        <div className="sectionTitle">
          <GitBranch size={18} />
          <h2>Run Timeline</h2>
        </div>
        {timeline.length ? (
          <ol className="timeline">
            {timeline.map((event) => (
              <li key={event.event_id}>
                <span>{event.event_type}</span>
                <small>{event.actor}</small>
                <p>{summarizePayload(event.payload)}</p>
              </li>
            ))}
          </ol>
        ) : (
          <p className="emptyState">Trace and audit events appear here after a run.</p>
        )}
      </section>

      <section className="patternSection">
        <div className="sectionHeader">
          <div className="sectionTitle">
            <BookOpen size={18} />
            <h2>Pattern Coverage</h2>
          </div>
          <button type="button" className="secondaryButton" onClick={runCatalog} disabled={catalogLoading}>
            {catalogLoading ? "Running catalog" : "Run catalog"}
          </button>
        </div>

        {catalogError && <div className="notice bad"><XCircle size={18} /> {catalogError}</div>}
        {catalog && (
          <div className="notice good">
            <CheckCircle2 size={18} /> {catalogPatternCount} pattern demos returned results.
          </div>
        )}

        <div className="patternGrid">
          {patternCatalog.map(({ id, key, name, detail }) => {
            const result = catalog?.[key];
            const passed = result?.passed ?? result?.valid ?? result?.citation_valid ?? result?.goal_preserved;
            return (
              <article className="patternTile" key={id}>
                <div className="patternNumber">{id}</div>
                <div>
                  <h3>{name}</h3>
                  <p>{detail}</p>
                  {catalog && <StatusPill status={passed === false ? "failed" : "ok"} />}
                </div>
              </article>
            );
          })}
        </div>
      </section>

      <section className="rawSection">
        <details>
          <summary><FileJson size={17} /> Raw run JSON</summary>
          <pre>{demo ? JSON.stringify({ result: demo.result, budget: demo.budget, evaluation: demo.evaluation, toolResults }, null, 2) : "Run an incident to inspect raw output."}</pre>
        </details>
        <details>
          <summary><FileJson size={17} /> Raw catalog JSON</summary>
          <pre>{catalog ? JSON.stringify(catalog, null, 2) : "Run the catalog to inspect raw output."}</pre>
        </details>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
