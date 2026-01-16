import { useMemo, useState } from "react";

const examples = [
  "Le trafic est très dense ce matin.",
  "Mee ndzii Yaoundé.",
  "S'il vous plaît, réduisez le prix.",
  "I will pay the fare now.",
  "Jam tan."
];

export default function App() {
  const [sentence, setSentence] = useState(examples[0]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showTokens, setShowTokens] = useState(true);
  const [showExplain, setShowExplain] = useState(true);

  const canSubmit = sentence.trim().length > 0;

  const statusClass = useMemo(() => {
    if (!result) return "status";
    return result.ok ? "status ok" : "status bad";
  }, [result]);

  async function handleCheck(e) {
    e.preventDefault();
    if (!canSubmit) return;
    setLoading(true);
    try {
      const res = await fetch("/api/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sentence, explain: showExplain, tokens: showTokens })
      });
      const data = await res.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  }

  function handleExample(example) {
    setSentence(example);
    setResult(null);
  }

  return (
    <div className="page">
      <header className="hero">
        <div>
          <p className="eyebrow">Compiler Frontend</p>
          <h1>Yaoundé Slang Language Analyzer</h1>
          <p className="subtitle">
            Paste a sentence, run the compiler front-end, and get ACCEPT/REJECT with diagnostics.
          </p>
        </div>
        <div className="card tips">
          <h3>Examples</h3>
          <div className="chips">
            {examples.map((example) => (
              <button key={example} type="button" onClick={() => handleExample(example)}>
                {example}
              </button>
            ))}
          </div>
        </div>
      </header>

      <main className="content">
        <form className="card" onSubmit={handleCheck}>
          <label className="label" htmlFor="sentence">
            Sentence
          </label>
          <textarea
            id="sentence"
            value={sentence}
            onChange={(e) => setSentence(e.target.value)}
            rows={4}
            placeholder="Type a Yaoundé expression..."
          />
          <div className="options">
            <label>
              <input
                type="checkbox"
                checked={showTokens}
                onChange={(e) => setShowTokens(e.target.checked)}
              />
              Show tokens
            </label>
            <label>
              <input
                type="checkbox"
                checked={showExplain}
                onChange={(e) => setShowExplain(e.target.checked)}
              />
              Show diagnostics
            </label>
          </div>
          <button type="submit" disabled={!canSubmit || loading}>
            {loading ? "Checking..." : "Check sentence"}
          </button>
        </form>

        <section className="card result">
          <div className={statusClass}>
            {result ? (result.ok ? "ACCEPT" : "REJECT") : "Waiting for input"}
          </div>
          {result && result.tokens && (
            <div className="block">
              <h4>Tokens</h4>
              <pre>{JSON.stringify(result.tokens, null, 2)}</pre>
            </div>
          )}
          {result && result.diagnostic && (
            <div className="block">
              <h4>Diagnostics</h4>
              <pre>{JSON.stringify(result.diagnostic, null, 2)}</pre>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
