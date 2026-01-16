# Yaoundé Slang Language Analyzer

## Brief description

This mini-project builds a lexer and LL(1) parser for informal Yaoundé speech (code-mixed slang and everyday expressions). It tokenizes sentences, checks whether they fit a small CFG, and outputs lexical statistics plus LL(1) artifacts (FIRST/FOLLOW and parsing table).

## How to run

1. Ensure you have Python 3.9+ installed.
2. Edit the input sentences in data/sentences.txt (optional).
3. Run the analyzer from the src folder:
   python analyzer.py --mode franglais
   or
   python analyzer.py --mode pidgin

### Outputs

- data/token_frequencies.txt: token and lexeme frequencies
- data/ll1_artifacts.txt: grammar, FIRST/FOLLOW sets, LL(1) table
- Console output: ACCEPT/REJECT per sentence
