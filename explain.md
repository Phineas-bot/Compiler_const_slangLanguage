Project Explanation: Yaoundé Slang Language Analyzer

1) Purpose and Scope
This project is a teaching‑style compiler frontend for Yaoundé urban slang (a code‑mixed blend of French, English, and Pidgin). It focuses on:
- Lexical analysis (tokenization of slang expressions).
- Syntactic analysis (LL(1) parsing against a CFG).
- Diagnostic feedback for invalid sentences.
- Dual access: a CLI for terminal use and a GUI for interactive exploration.

It is not a full compiler (no semantic analysis or code generation). Instead, it demonstrates core parsing concepts in a domain that is culturally relevant and linguistically rich.

2) Architecture at a Glance
Input sentence → Lexer → Token stream → LL(1) Parser → ACCEPT/REJECT + Diagnostics

Key modules:
- src/analyzer.py: core logic (lexicon, grammar, parser, artifacts).
- src/api.py: FastAPI wrapper around analyzer for the web UI.
- src/cli.py: CLI entry point.
- frontend/: React + Vite interface.

3) Lexical Analysis (Lexer)
The lexer maps raw words into token categories. These tokens represent the grammar’s terminals.

How it works:
- A lexicon dictionary defines sets of words per category (e.g., NOUN, VERB, PRON, DET, PREP, ADVWORD).
- Input sentences are normalized (lowercase, punctuation handling) and split.
- Each word is matched to a token category; unknown words may be tagged or treated as errors depending on the grammar rules.

Example:
Input: "boss drop me for carrefour"
Tokens: [(SLANG, boss), (VERB, drop), (PRON, me), (PREP, for), (NOUN, carrefour)]

Why it matters:
- The parser only understands tokens, not raw text.
- Lexicon updates directly expand the language recognized by the system.

4) Grammar Definition (CFG)
The grammar is encoded as a context‑free grammar (CFG) with a start symbol and production rules.

Example concept (simplified):
S → STATEMENT
STATEMENT → SLANG_PHRASE | VERB_PHRASE | NOUN_PHRASE
SLANG_PHRASE → SLANG VERB_PHRASE
VERB_PHRASE → VERB NOUN_PHRASE
NOUN_PHRASE → PRON | NOUN | DET NOUN | NOUN PREP NOUN

Each rule defines valid structures for the slang expressions. The real grammar in analyzer.py is richer and tailored to common Yaoundé phrases.

5) FIRST/FOLLOW Sets and LL(1) Table
The parser computes:
- FIRST(X): all terminals that can start strings derived from symbol X.
- FOLLOW(X): all terminals that can appear immediately after X in a valid derivation.

These sets are then used to build the LL(1) parsing table M[NonTerminal, Terminal]. This table drives a predictive parser that always knows which production to apply next.

6) LL(1) Parsing Process
The parser uses a stack and the token stream:
- Initialize stack with "$" and the start symbol.
- Look at the top of the stack and the current input token.
- If top is a terminal and matches the current token, consume it.
- If top is a non‑terminal, consult the LL(1) table to expand it.
- If no valid rule exists, parsing fails with a diagnostic.

Outputs:
- ok: true/false (ACCEPT/REJECT)
- diagnostic (if reject):
	- position: token index
	- actual: token encountered
	- expected: list of valid tokens at that point
- actions/stack (for UI panels): snapshots of parsing steps and stack state

7) Diagnostics and Artifacts
Diagnostics are designed to help the learner understand why a sentence fails:
- They report the exact token index.
- They show what was expected vs. what appeared.

Artifacts are exported to data/ll1_artifacts.txt. This file includes:
- The grammar rules.
- FIRST and FOLLOW sets.
- The LL(1) parsing table.

8) Backend API (FastAPI)
The backend exposes analyzer functionality to the frontend.

Endpoints:
- GET /api/health
	Returns status for quick health checks.
- POST /api/check
	Request: { sentence, explain, tokens }
	Response:
	- ok: parsing verdict
	- diagnostic: error details when rejected
	- tokens: token list when requested
	- actions: list of parse actions
	- stack: list of stack snapshots

The backend does not persist data; it processes requests on demand.

9) Frontend UI (React + Vite)
The interface mimics a desktop‑style language tool. It includes:
- Lexical Analysis: shows token/lexeme table.
- Syntactic Analysis: parsed output and acceptance status.
- Sentence Input: text input bar for raw input.
- Parsing Actions: latest parser action history.
- Parse Stack: current stack snapshot.

Theme support:
- Light/dark mode toggling via a small top‑right menu.
- The theme is stored in localStorage and applied on load.

10) CLI Workflow
The CLI mirrors the backend behavior but in terminal form:
- check: validate a single sentence
- tokens: show the token stream
- file: validate sentences in bulk from a file
- repl: interactive prompt
- artifacts: regenerate parsing artifacts

11) Data Files
- data/sentences.txt: example sentences to test the parser.
- data/token_frequencies.txt: lexical statistics output.
- data/ll1_artifacts.txt: FIRST/FOLLOW sets and parsing table.

12) How to Extend the Project
Lexicon expansion:
- Add new slang terms or code‑mixed variants in the lexicon inside analyzer.py.

Grammar expansion:
- Add production rules for new phrase patterns.
- Regenerate artifacts to ensure LL(1) compatibility.

Frontend enhancement:
- Add visual parse tree rendering.
- Add step‑by‑step parser replay.
- Improve token visualization (color‑coding by category).

13) Limitations (Current)
- Unknown words outside the lexicon may be rejected.
- Grammar is intentionally small and not exhaustive for real conversational slang.
- No semantic validation (meaning or intent is not checked).

Summary
This project is a compact, educational compiler frontend that demonstrates how a lexer and LL(1) parser can be applied to a culturally rich, code‑mixed language domain. It is ideal for learning parsing concepts, experimenting with grammar design, and building interactive language tooling.
