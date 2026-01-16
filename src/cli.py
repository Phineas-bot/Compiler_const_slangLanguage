from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, Optional

from analyzer import (  # noqa: E402
    Lexer,
    LL1Parser,
    build_grammar,
    parse_sentence,
    write_ll1_artifacts,
)


def _load_sentences(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def _print_result(result: dict, sentence: str) -> None:
    verdict = "ACCEPT" if result["ok"] else "REJECT"
    print(f"{verdict}: {sentence}")
    if not result["ok"] and result.get("diagnostic"):
        diag = result["diagnostic"]
        expected = ", ".join(sorted(diag.get("expected", [])))
        actual = diag.get("actual", "")
        position = diag.get("position")
        print(f"  at token {position}: {actual}")
        if expected:
            print(f"  expected: {expected}")


def cmd_check(sentence: str, explain: bool) -> None:
    result = parse_sentence(sentence, explain=explain)
    _print_result(result, sentence)


def cmd_tokens(sentence: str) -> None:
    tokens = Lexer().tokenize(sentence)
    print(tokens)


def cmd_file(path: Path, explain: bool) -> None:
    for sentence in _load_sentences(path):
        result = parse_sentence(sentence, explain=explain)
        _print_result(result, sentence)


def cmd_artifacts(output: Optional[Path]) -> None:
    parser = LL1Parser(build_grammar())
    if output is None:
        write_ll1_artifacts(parser)
        print("Updated data/ll1_artifacts.txt")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8") as handle:
            handle.write("GRAMMAR\n")
            for nt, rules in parser.grammar.productions.items():
                rhs = [" ".join(rule) for rule in rules]
                handle.write(f"{nt} -> {' | '.join(rhs)}\n")

            handle.write("\nFIRST SETS\n")
            for nt in parser.grammar.productions:
                values = ", ".join(sorted(parser.first[nt]))
                handle.write(f"FIRST({nt}) = {{ {values} }}\n")

            handle.write("\nFOLLOW SETS\n")
            for nt in parser.grammar.productions:
                values = ", ".join(sorted(parser.follow[nt]))
                handle.write(f"FOLLOW({nt}) = {{ {values} }}\n")

            handle.write("\nLL(1) PARSING TABLE\n")
            for (nt, terminal), rule in sorted(parser.table.items()):
                handle.write(f"M[{nt}, {terminal}] = {' '.join(rule)}\n")
        print(f"Wrote {output}")


def cmd_repl(explain: bool) -> None:
    print("Yaoundé Slang Frontend REPL")
    print("Type a sentence and press Enter (blank or 'exit' to quit).")
    try:
        while True:
            line = input("> ").strip()
            if not line or line.lower() in {"exit", "quit"}:
                break
            result = parse_sentence(line, explain=explain)
            _print_result(result, line)
    except (EOFError, KeyboardInterrupt):
        print("\nbye")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Yaoundé Slang compiler frontend")
    parser.add_argument("--explain", action="store_true", help="show diagnostics when rejecting")

    subs = parser.add_subparsers(dest="command", required=True)

    check = subs.add_parser("check", help="check a single sentence")
    check.add_argument("sentence")

    tokens = subs.add_parser("tokens", help="print token stream for a sentence")
    tokens.add_argument("sentence")

    file_cmd = subs.add_parser("file", help="check all sentences from a file")
    file_cmd.add_argument("path", type=Path)

    repl = subs.add_parser("repl", help="interactive prompt")

    artifacts = subs.add_parser("artifacts", help="write LL(1) artifacts")
    artifacts.add_argument("--out", type=Path, default=None)

    return parser


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.command == "check":
        cmd_check(args.sentence, explain=args.explain)
    elif args.command == "tokens":
        cmd_tokens(args.sentence)
    elif args.command == "file":
        cmd_file(args.path, explain=args.explain)
    elif args.command == "repl":
        cmd_repl(explain=args.explain)
    elif args.command == "artifacts":
        cmd_artifacts(args.out)
    else:
        parser.print_help()
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
