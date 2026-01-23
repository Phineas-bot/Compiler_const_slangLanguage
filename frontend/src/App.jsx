import { useEffect, useMemo, useState } from "react";

const examples = [
  "Le trafic est très dense ce matin.",
  "Mee ndzii Yaoundé.",
  "S'il vous plaît, réduisez le prix.",
  "I will pay the fare now.",
  "Jam tan."
];

export default function App() {
  const [sentence, setSentence] = useState(examples[0]);
  const [sampleIndex, setSampleIndex] = useState(0);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  const canSubmit = sentence.trim().length > 0;

  useEffect(() => {
    const stored = window.localStorage.getItem("yaounde-theme");
    if (stored === "dark") {
      setDarkMode(true);
    }
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle("theme-dark", darkMode);
    window.localStorage.setItem("yaounde-theme", darkMode ? "dark" : "light");
  }, [darkMode]);

  const statusText = useMemo(() => {
    if (!result) return "Waiting";
    return result.ok ? "Accepted" : "Rejected";
  }, [result]);

  const parsedOutput = useMemo(() => {
    if (!result) return "Run analysis to see parser output.";
    if (result.ok) return "Sentence accepted by the LL(1) grammar.";
    if (!result.diagnostic) return "Rejected with no diagnostics.";
    return `Error at position ${result.diagnostic.position}\nExpected: ${result.diagnostic.expected.join(", ")}\nActual: ${result.diagnostic.actual}`;
  }, [result]);

  const currentToken = useMemo(() => {
    if (!result?.tokens?.length) return "--";
    const first = result.tokens[0];
    return first[1] ?? first[0] ?? "--";
  }, [result]);

  const stackPreview = useMemo(() => {
    if (!result?.stack?.length) return "Stack preview not available.";
    const latest = result.stack[result.stack.length - 1] || [];
    if (!latest.length) return "(empty stack)";
    return latest.slice().reverse().join("\n");
  }, [result]);

  const actionPreview = useMemo(() => {
    if (!result?.actions?.length) return "No actions yet.";
    return result.actions.slice(-8).join("\n");
  }, [result]);


  async function runCheck({ tokens = true, explain = true } = {}) {
    if (!canSubmit) return;
    setLoading(true);
    try {
      const res = await fetch("/api/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sentence, explain, tokens })
      });
      const data = await res.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  }

  function handleLoadSample() {
    const nextIndex = (sampleIndex + 1) % examples.length;
    setSampleIndex(nextIndex);
    setSentence(examples[nextIndex]);
    setResult(null);
  }

  function handleClear() {
    setSentence("");
    setResult(null);
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="flag">🇨🇲</div>
          <div>
            <h1>Yaoundé Urban Language Analyzer</h1>
            <p>Compiler Frontend</p>
          </div>
        </div>
        <div className="window-actions">
          <span className="dot" />
          <span className="dot" />
          <span className="dot" />
          <div
            className={`menu ${menuOpen ? "open" : ""}`}
            onBlur={(e) => {
              if (!e.currentTarget.contains(e.relatedTarget)) {
                setMenuOpen(false);
              }
            }}
          >
            <button
              className="menu-button"
              type="button"
              aria-label="Theme menu"
              aria-expanded={menuOpen}
              onClick={() => setMenuOpen((open) => !open)}
            >
              ☰
            </button>
            <div className="menu-panel" role="menu">
              <label className="menu-item">
                <input
                  type="checkbox"
                  checked={darkMode}
                  onChange={(e) => setDarkMode(e.target.checked)}
                />
                Dark mode
              </label>
            </div>
          </div>
        </div>
      </header>

      <main className="workspace">
        <section className="panel">
          <div className="panel-title">
            <span className="panel-icon">📄</span>
            <h2>Lexical Analysis</h2>
          </div>
          <div className="panel-body">
            <button className="btn" type="button" onClick={handleLoadSample}>
              Load Sentence
            </button>

            <div className="table">
              <div className="table-header">
                <span>Token</span>
                <span>Type</span>
              </div>
              <div className="table-body">
                {result?.tokens?.length ? (
                  result.tokens.map((token, index) => (
                    <div className="table-row" key={`${token[0]}-${index}`}>
                      <span>{token[1]}</span>
                      <span>{token[0]}</span>
                    </div>
                  ))
                ) : (
                  <div className="table-row empty">
                    <span>—</span>
                    <span>—</span>
                  </div>
                )}
              </div>
            </div>

            <div className="panel-actions">
              <button
                className="btn primary"
                type="button"
                disabled={!canSubmit || loading}
                onClick={() => runCheck({ tokens: true, explain: false })}
              >
                {loading ? "Analyzing..." : "Analyze Tokens"}
              </button>
              <button
                className="btn"
                type="button"
                disabled={!canSubmit || loading}
                onClick={() => runCheck({ tokens: true, explain: true })}
              >
                Token Summary
              </button>
            </div>
          </div>
        </section>

        <section className="panel">
          <div className="panel-title">
            <span className="panel-icon">🧩</span>
            <h2>Syntactic Analysis</h2>
          </div>
          <div className="panel-body">
            <div className="output">
              <p className="output-title">Parsed Output:</p>
              <pre>{parsedOutput}</pre>
            </div>
            <div className="panel-actions">
              <button
                className="btn success"
                type="button"
                disabled={!canSubmit || loading}
                onClick={() => runCheck({ tokens: true, explain: true })}
              >
                Parse Sentence
              </button>
              <button
                className="btn"
                type="button"
                disabled={!canSubmit || loading}
                onClick={() => runCheck({ tokens: true, explain: true })}
              >
                Syntax Tree
              </button>
            </div>
            <div className={`status-pill ${result?.ok ? "ok" : result ? "bad" : ""}`}>
              Result: <span>{statusText}</span>
            </div>
          </div>
        </section>
      </main>

      <section className="sentence-panel">
        <div className="sentence-title">Sentence Input</div>
        <div className="sentence-controls">
          <input
            type="text"
            value={sentence}
            onChange={(e) => setSentence(e.target.value)}
            placeholder="Type a Yaoundé expression..."
          />
          <button className="btn" type="button" onClick={handleClear}>
            Clear
          </button>
          <button className="btn danger" type="button" onClick={handleClear}>
            Exit
          </button>
        </div>
      </section>

      <section className="bottom-row">
        <div className="panel small">
          <div className="panel-title">
            <h3>Parsing Actions</h3>
          </div>
          <div className="panel-body">
            <pre className="mini-output">{actionPreview}</pre>
          </div>
        </div>
        <div className="panel small">
          <div className="panel-title">
            <h3>Parse Stack</h3>
          </div>
          <div className="panel-body">
            <pre className="mini-output">{stackPreview}</pre>
          </div>
        </div>
        <div className="panel small">
          <div className="panel-title">
            <h3>Current Token</h3>
          </div>
          <div className="panel-body">
            <div className="token-pill">{currentToken}</div>
          </div>
        </div>
      </section>

    </div>
  );
}
