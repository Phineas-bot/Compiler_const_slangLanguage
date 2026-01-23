# Yaoundé Slang Language Analyzer

## Brief description
This mini-project builds a lexer and LL(1) parser for informal Yaoundé speech (code-mixed slang and everyday expressions). It tokenizes sentences, checks whether they fit a small CFG, and outputs lexical statistics plus LL(1) artifacts (FIRST/FOLLOW and parsing table).

## How to run
1. Ensure you have Python 3.9+ installed.
2. Edit the input sentences in data/sentences.txt (optional).
3. Run the analyzer from the src folder:
   python analyzer.py

## Compiler frontend (CLI)
Run the CLI from the src folder:
python cli.py <command> [options]

Commands:
- check "sentence..."      Check a single sentence (ACCEPT/REJECT)
- tokens "sentence..."     Show the token stream for a sentence
- file data/sentences.txt  Check all sentences from a file
- repl                     Interactive prompt (type sentences and get results)
- artifacts                Regenerate LL(1) artifacts

Examples:
- python cli.py check "Le trafic est très dense ce matin."
- python cli.py repl
- python cli.py file ..\data\sentences.txt
- python cli.py tokens "Mbolo mia"
- python cli.py artifacts

Tip: add --explain to show diagnostics for rejected sentences.

## Web GUI (React + FastAPI)
Backend (FastAPI):
1. Install dependencies:
   pip install -r requirements.txt
2. Run the API from the src folder:
   uvicorn api:app --reload --port 8000

Frontend (React + Vite):
1. In a new terminal:
   cd frontend
   npm install
   npm run dev

Then open http://localhost:5173 in your browser.

### Outputs
- data/token_frequencies.txt: token and lexeme frequencies
- data/ll1_artifacts.txt: grammar, FIRST/FOLLOW sets, LL(1) table
- Console output: ACCEPT/REJECT per sentence
