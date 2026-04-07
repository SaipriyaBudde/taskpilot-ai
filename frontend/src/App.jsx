import { useState } from "react";
import {
  Sparkles,
  Clock3,
  Zap,
  AlertTriangle,
  Briefcase,
  CheckCircle2,
  ArrowRightCircle,
  Brain,
} from "lucide-react";
import "./App.css";

export default function App() {
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleGenerate = async () => {
    if (!userInput.trim()) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_input: userInput,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch AI plan.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Something went wrong while building your plan.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const badgeClass = (value) => {
    const lower = value?.toLowerCase();
    if (lower === "high" || lower === "urgent") return "badge red";
    if (lower === "medium") return "badge yellow";
    if (lower === "low") return "badge green";
    return "badge";
  };

  return (
    <div className="app-shell">
      <div className="background-glow bg1" />
      <div className="background-glow bg2" />

      <main className="container">
        <section className="hero-card">
          <div className="hero-top">
            <div>
              <p className="eyebrow">AI EXECUTION INTELLIGENCE</p>
              <h1>TaskPilot AI</h1>
              <p className="hero-sub">
                Turn messy thoughts into a clear, execution-ready plan.
              </p>
            </div>

            <div className="hero-icon-wrap">
              <Sparkles size={34} />
            </div>
          </div>

          <div className="input-box">
            <textarea
              placeholder="Example: I have a deadline tomorrow, pending office work, groceries to buy, and I need to prepare for an interview."
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
            />

            <button onClick={handleGenerate} disabled={loading}>
              {loading ? "Building your plan..." : "Build My Plan"}
            </button>
          </div>

          {error && <p className="error-text">{error}</p>}
        </section>

        {!result && !loading && (
          <section className="section-block">
            <div className="section-header">
              <h3>Your plan will appear here</h3>
              <p>
                Describe what’s on your mind, and TaskPilot AI will organize it
                into clear priorities and next steps.
              </p>
            </div>
          </section>
        )}

        {loading && (
          <section className="section-block">
            <div className="section-header">
              <h3>Building your plan...</h3>
              <p>
                Prioritizing what matters, sequencing your tasks, and mapping
                your next best moves.
              </p>
            </div>
          </section>
        )}

        {result && (
          <>
          <section className="summary-banner">
            <div className="summary-icon">
              <Brain size={24} />
            </div>
            <div>
              <p className="section-label">TODAY’S EXECUTION STRATEGY</p>
              <h2>{result.summary}</h2>
              <p className="strategy-subtext">{result.visual}</p>
            </div>
          </section>

            <section className="section-block">
              <div className="section-header">
                <h3>Start Here</h3>
                <p>Your best first move right now.</p>
              </div>

              <div className="task-card">
                <h4>{result.tasks?.[0]?.task}</h4>
                <p className="task-reason">
                  Begin with this first — it carries the highest execution value
                  and helps reduce mental overload fastest.
                </p>
              </div>
            </section>

            <section className="section-block">
              <div className="section-header">
                <h3>Today’s Non-Negotiables</h3>
                <p>If you complete these, your day still moves forward.</p>
              </div>

              <div className="task-grid">
                {result.tasks?.slice(0, 3).map((task, index) => (
                  <div className="task-card" key={index}>
                    <div className="task-card-top">
                      <h4>{task.task}</h4>
                      <div className="badge-row">
                        <span className={badgeClass(task.priority)}>
                          {task.priority}
                        </span>
                      </div>
                    </div>
                    <p className="task-reason">{task.reason}</p>
                  </div>
                ))}
              </div>
            </section>

            <section className="section-block">
              <div className="section-header">
                <h3>Execution Priorities</h3>
                <p>What needs your attention first — and why it matters.</p>
              </div>

              <div className="task-grid">
                {result.tasks?.map((task, index) => (
                  <div className="task-card" key={index}>
                    <div className="task-card-top">
                      <h4>{task.task}</h4>
                      <div className="badge-row">
                        <span className={badgeClass(task.priority)}>
                          {task.priority}
                        </span>
                        <span className={badgeClass(task.urgency)}>
                          {task.urgency}
                        </span>
                      </div>
                    </div>

                    <p className="task-reason">{task.reason}</p>

                    <div className="meta-grid">
                      <div className="meta-pill">
                        <Clock3 size={16} />
                        <span>{task.estimated_duration}</span>
                      </div>

                      <div className="meta-pill">
                        <Zap size={16} />
                        <span>{task.energy_level} Energy</span>
                      </div>

                      <div className="meta-pill">
                        <ArrowRightCircle size={16} />
                        <span>{task.best_time}</span>
                      </div>

                      <div className="meta-pill">
                        <Briefcase size={16} />
                        <span>{task.impact} Impact</span>
                      </div>

                      <div className="meta-pill">
                        <AlertTriangle size={16} />
                        <span>{task.deadline_risk} Risk</span>
                      </div>

                      <div className="meta-pill">
                        <CheckCircle2 size={16} />
                        <span>
                          {task.can_delegate ? "Delegatable" : "Do It Yourself"}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            <section className="section-block">
              <div className="section-header">
                <h3>Suggested Execution Plan</h3>
                <p>An ideal flow for completing your tasks with less overwhelm.</p>
                <p className="timeline-note">
                  Adjust based on your current time — this is an optimized flow,
                  not a fixed schedule.
                </p>
              </div>

              <div className="timeline">
                {result.schedule?.map((item, index) => (
                  <div className="timeline-item" key={index}>
                    <div className="timeline-dot" />
                    <div className="timeline-time">
                      {item.start_time} — {item.end_time}
                    </div>
                    <div className="timeline-card">
                      <h4>{item.task}</h4>
                      <p>{item.focus}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>

          </>
        )}
      </main>
    </div>
  );
}