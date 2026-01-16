from __future__ import annotations

import re
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple


Token = Tuple[str, str]  # (type, lexeme)


@dataclass
class Grammar:
    start: str
    productions: Dict[str, List[List[str]]]


class Lexer:
    def __init__(self) -> None:
        self.lexicon = {
            "CONJ": {
                "and",
                "but",
                "or",
                "so",
                "mais",
                "et",
                "donc",
                "alors",
                "puis",
                "parce",
            },
            "DET": {
                "the",
                "a",
                "an",
                "your",
                "my",
                "this",
                "that",
                "un",
                "une",
                "le",
                "la",
                "les",
                "des",
                "du",
                "ce",
                "cette",
                "ces",
                "mon",
                "ma",
                "mes",
                "ton",
                "ta",
                "tes",
                "notre",
                "votre",
            },
            "PRON": {
                "i",
                "you",
                "we",
                "me",
                "he",
                "she",
                "they",
                "je",
                "tu",
                "il",
                "elle",
                "on",
                "nous",
                "vous",
                "moi",
                "toi",
                "lui",
                "leur",
                "ça",
                "c'est",
                "j'ai",
                "j'suis",
            },
            "NEG": {"no", "not", "pas", "jamais", "plus"},
            "AUX": {"don", "ai", "as", "a", "avons", "avez", "ont", "est", "suis"},
            "VERB": {
                # English / Pidgin
                "drop",
                "send",
                "dey",
                "fit",
                "carry",
                "go",
                "pass",
                "make",
                "get",
                "try",
                "cut",
                "charge",
                "reduce",
                "give",
                "be",
                "start",
                "come",
                "turn",
                "slip",
                "remain",
                "increase",
                "add",
                "keep",
                "dodge",
                "finish",
                "beat",
                "spoil",
                "na",
                "sabi",
                "want",
                "need",
                "wait",
                "hurry",
                "pay",
                # French (common in franc-anglais)
                "suis",
                "est",
                "faire",
                "fais",
                "donner",
                "donne",
                "envoyer",
                "envoie",
                "aller",
                "vais",
                "venir",
                "viens",
                "peux",
                "peut",
                "faut",
                "chercher",
                "cherche",
                "regarder",
                "regarde",
                "aider",
                "aide",
                "descendre",
                "descends",
                "monter",
                "monte",
                "pose",
            },
            "PREP": {
                "for",
                "to",
                "since",
                "like",
                "in",
                "on",
                "at",
                "from",
                "dans",
                "sur",
                "chez",
                "avec",
                "sans",
                "pour",
                "depuis",
                "vers",
                "à",
                "au",
                "aux",
                "de",
                "du",
                "des",
            },
            "ADVWORD": {
                "small",
                "quick",
                "today",
                "again",
                "last-last",
                "too",
                "much",
                "ready",
                "combien",
                "scarce",
                "long",
                "hmmm",
                "garrr",
                "ekiee",
                "ah",
                "wanda",
                "wah",
                "non",
                "hein",
                "eh",
                "abeg",
                "oya",
                "svp",
                "stp",
                "vite",
                "maintenant",
                "déjà",
                "encore",
                "seulement",
                "trop",
                "urgent",
                "calm",
                # Local greetings/expressions
                "mbolo",
                "jaaraama",
                "jam",
                "tan",
            },
            "NOUN": {
                "chef",
                "chauffeur",
                "moto-guy",
                "bendskin",
                "nlongkak",
                "carrefour",
                "ngousso",
                "melen",
                "data",
                "network",
                "assignment",
                "connexion",
                "zero-zero",
                "morning",
                "eneo",
                "light",
                "phone",
                "quartier",
                "current",
                "yesterday",
                "frigo",
                "mami",
                "price",
                "pikin",
                "bro",
                "traffic",
                "behind",
                "ahead",
                "front",
                "rain",
                "road",
                "route",
                "problem",
                "river",
                "hostel",
                "mud",
                "shoe",
                "water",
                "yaounde",
                "fuel",
                "essence",
                "queue",
                "station",
                "taxi",
                "man",
                "fare",
                "aunty",
                "beignet",
                "beans",
                "piment",
                "boss",
                "helmet",
                "police",
                "checkpoint",
                "id",
                "noise",
                "class",
                "lecturer",
                "time",
                "effort",
                "enerve",
                "ictu",
                "moodle",
                "devoir",
                "monnaie",
                "change",
                "prière",
                "couvre-feu",
            },
            "GREET": {
                "mbolo",
                "molo",
                "jaaraama",
                "jam",
                "tan",
            },
            "REQ_WORD": {
                "please",
                "svp",
                "stp",
                "s'il",
                "sil",
            },
            "FUL_WORD": {
                "mi",
                "miɗo",
                "yidi",
                "yahugo",
                "heɓi",
                "ɗum",
                "yahii",
                "suudu",
                "waawi",
                "waɗi",
                "ndeenee",
                "yahi",
                "wondi",
                "ndiyam",
            },
            "EWO_WORD": {
                "mee",
                "ndzii",
                "mia",
                "ekolo",
                "abui",
                "ndap",
                "nyol",
                "nkukuma",
                "yaoundé",
            },
        }

    def tokenize(self, sentence: str) -> List[Token]:
        cleaned = (
            sentence.lower()
            .replace("’", "'")
            .replace("+", " ")
            .replace(",", " ")
            .replace("?", " ")
            .replace("!", " ")
            .replace(";", " ")
            .replace(".", " ")
        )

        # Unicode-friendly tokenization: supports accents and many African-language letters.
        word = r"[^\W\d_]+(?:-[^\W\d_]+)*(?:'[^\W\d_]+)?"
        numword = r"\d+[^\W_]*"
        words = re.findall(fr"{word}|{numword}", cleaned, flags=re.UNICODE)

        tokens: List[Token] = [(self._classify(w), w) for w in words]
        tokens = self._collapse_conjunctions(tokens)
        tokens.append(("$", "$"))
        return tokens

    def _classify(self, word: str) -> str:
        if re.fullmatch(r"\d+[^\W_]*", word, flags=re.UNICODE):
            return "NUM"

        for token_type, vocab in self.lexicon.items():
            if word in vocab:
                return token_type

        return "NOUN"

    @staticmethod
    def _collapse_conjunctions(tokens: List[Token]) -> List[Token]:
        collapsed: List[Token] = []
        for token in tokens:
            if collapsed and token[0] == "CONJ" and collapsed[-1][0] == "CONJ":
                continue
            collapsed.append(token)

        if collapsed and collapsed[0][0] == "CONJ":
            collapsed = collapsed[1:]
        if collapsed and collapsed[-1][0] == "CONJ":
            collapsed = collapsed[:-1]
        return collapsed


class LL1Parser:
    def __init__(self, grammar: Grammar) -> None:
        self.grammar = grammar
        self.first = self._compute_first_sets()
        self.follow = self._compute_follow_sets()
        self.table = self._build_parse_table()

    def parse(self, tokens: List[Token]) -> bool:
        stack: List[str] = ["$", self.grammar.start]
        index = 0

        while stack:
            top = stack.pop()
            current_type = tokens[index][0]

            if top == "$":
                return current_type == "$"

            if self._is_terminal(top):
                if top == current_type:
                    index += 1
                    continue
                return False

            production = self.table.get((top, current_type))
            if production is None:
                return False

            for symbol in reversed(production):
                if symbol != "ε":
                    stack.append(symbol)

        return False

    def _is_terminal(self, symbol: str) -> bool:
        return symbol not in self.grammar.productions

    def _compute_first_sets(self) -> Dict[str, Set[str]]:
        first: Dict[str, Set[str]] = {nt: set() for nt in self.grammar.productions}

        changed = True
        while changed:
            changed = False
            for nt, rules in self.grammar.productions.items():
                for rule in rules:
                    nullable = True
                    for symbol in rule:
                        if self._is_terminal(symbol):
                            if symbol not in first[nt]:
                                first[nt].add(symbol)
                                changed = True
                            nullable = False
                            break
                        before = len(first[nt])
                        first[nt].update(first[symbol] - {"ε"})
                        if len(first[nt]) != before:
                            changed = True
                        if "ε" not in first[symbol]:
                            nullable = False
                            break
                    if nullable:
                        if "ε" not in first[nt]:
                            first[nt].add("ε")
                            changed = True

        return first

    def _compute_follow_sets(self) -> Dict[str, Set[str]]:
        follow: Dict[str, Set[str]] = {nt: set() for nt in self.grammar.productions}
        follow[self.grammar.start].add("$")

        changed = True
        while changed:
            changed = False
            for nt, rules in self.grammar.productions.items():
                for rule in rules:
                    trailer = follow[nt].copy()
                    for symbol in reversed(rule):
                        if not self._is_terminal(symbol):
                            before = len(follow[symbol])
                            follow[symbol].update(trailer)
                            if len(follow[symbol]) != before:
                                changed = True
                            if "ε" in self.first[symbol]:
                                trailer = trailer | (self.first[symbol] - {"ε"})
                            else:
                                trailer = self.first[symbol].copy()
                        else:
                            trailer = {symbol}

        return follow

    def _build_parse_table(self) -> Dict[Tuple[str, str], List[str]]:
        table: Dict[Tuple[str, str], List[str]] = {}

        for nt, rules in self.grammar.productions.items():
            for rule in rules:
                first_set = self._first_of_sequence(rule)
                for terminal in first_set - {"ε"}:
                    table[(nt, terminal)] = rule
                if "ε" in first_set:
                    for terminal in self.follow[nt]:
                        table[(nt, terminal)] = rule

        return table

    def _first_of_sequence(self, symbols: List[str]) -> Set[str]:
        result: Set[str] = set()
        for symbol in symbols:
            if self._is_terminal(symbol):
                result.add(symbol)
                return result
            result.update(self.first[symbol] - {"ε"})
            if "ε" not in self.first[symbol]:
                return result
        result.add("ε")
        return result


def build_grammar() -> Grammar:
    productions = {
        "S": [["CLAUSE", "S_TAIL"], ["GREETING"], ["REQUEST"], ["LANG_SENT"]],
        "S_TAIL": [["CONJ", "CLAUSE", "S_TAIL"], ["ε"]],
        "CLAUSE": [["CORE"]],
        "CORE": [["NP", "CORE_TAIL"], ["VP"], ["ADV"]],
        "CORE_TAIL": [["VP"], ["ADV", "CORE_TAIL"], ["PP", "CORE_TAIL"], ["ε"]],
        "NP": [["DET", "NP_HEAD"], ["NEG", "NP_HEAD"], ["NP_HEAD"]],
        "NP_HEAD": [["NOUN", "NP_TAIL"], ["PRON"], ["NUM"]],
        "NP_TAIL": [["NOUN", "NP_TAIL"], ["ε"]],
        "VP": [["NEG", "VERB", "VP_TAIL"], ["AUX", "VERB", "VP_TAIL"], ["VERB", "VP_TAIL"]],
        "VP_TAIL": [
            ["VERB", "VP_TAIL"],
            ["NP", "VP_TAIL"],
            ["PP", "VP_TAIL"],
            ["ADV", "VP_TAIL"],
            ["ε"],
        ],
        "PP": [["PREP", "NP"]],
        "ADV": [["ADVWORD", "ADV_TAIL"]],
        "ADV_TAIL": [["ADVWORD", "ADV_TAIL"], ["ε"]],
        "GREETING": [["GREET", "GREET_TAIL"]],
        "GREET_TAIL": [["GREET", "GREET_TAIL"], ["ε"]],
        "REQUEST": [["REQ_WORD", "REQUEST_BODY"]],
        "REQUEST_BODY": [["CORE"], ["LANG_SENT"], ["GREETING"], ["ε"]],
        "LANG_SENT": [["FUL_WORD", "FUL_TAIL"], ["EWO_WORD", "EWO_TAIL"]],
        "FUL_TAIL": [["FUL_WORD", "FUL_TAIL"], ["ε"]],
        "EWO_TAIL": [["EWO_WORD", "EWO_TAIL"], ["ε"]],
    }
    return Grammar(start="S", productions=productions)


def analyze_sentences(sentences: List[str]) -> None:
    lexer = Lexer()
    parser = LL1Parser(build_grammar())

    for sentence in sentences:
        tokens = lexer.tokenize(sentence)
        ok = parser.parse(tokens)
        verdict = "ACCEPT" if ok else "REJECT"
        print(f"{verdict}: {sentence.strip()}")


def write_token_frequencies(sentences: List[str]) -> None:
    lexer = Lexer()
    type_counts: Dict[str, int] = {}
    lexeme_counts: Dict[str, int] = {}

    for sentence in sentences:
        for token_type, lexeme in lexer.tokenize(sentence):
            if token_type == "$":
                continue
            type_counts[token_type] = type_counts.get(token_type, 0) + 1
            lexeme_counts[lexeme] = lexeme_counts.get(lexeme, 0) + 1

    output_path = Path(__file__).resolve().parent.parent / "data" / "token_frequencies.txt"
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("TOKEN TYPE FREQUENCIES\n")
        for token_type, count in sorted(type_counts.items(), key=lambda item: (-item[1], item[0])):
            handle.write(f"{token_type}: {count}\n")

        handle.write("\nLEXEME FREQUENCIES\n")
        for lexeme, count in sorted(lexeme_counts.items(), key=lambda item: (-item[1], item[0])):
            handle.write(f"{lexeme}: {count}\n")


def write_ll1_artifacts(parser: LL1Parser) -> None:
    output_path = Path(__file__).resolve().parent.parent / "data" / "ll1_artifacts.txt"
    with output_path.open("w", encoding="utf-8") as handle:
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


def main() -> None:
    input_path = Path(__file__).resolve().parent.parent / "data" / "sentences.txt"
    with input_path.open("r", encoding="utf-8") as handle:
        sentences = [line.strip() for line in handle if line.strip()]

    analyze_sentences(sentences)
    write_token_frequencies(sentences)
    write_ll1_artifacts(LL1Parser(build_grammar()))


if __name__ == "__main__":
    main()
