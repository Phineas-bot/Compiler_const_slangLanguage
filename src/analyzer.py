
from __future__ import annotations

import re
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple


Token = Tuple[str, str]


@dataclass
class Grammar:
    start: str
    productions: Dict[str, List[List[str]]]


class Lexer:
    """
    Refined Lexer with ADJ category and corrected VERB/AUX classifications.
    """
    
    def __init__(self) -> None:
        self.lexicon = {
            "CONJ": {
                "but", "and", "mais", "et", "or", "ou", "while", "because", "quoique"
            },
            
            "DET": {
                "the", "your", "my", "this", "that", "our", "a", "an",
                "un", "une", "ce", "cette", "le", "la", "les", "des", 
                "mon", "ma", "mes", "l", "au", "aux", "du", "de",
                "d", "ton", "ta", "tes", "son", "sa", "ses", "some", "any"
            },
            
            "PRON": {
                "i", "you", "we", "me", "he", "she", "they", "us", "your",
                "je", "tu", "il", "elle", "on", "nous",
                "c'est", "dem", "c", "j", "him", "her", "it", "them", "who", "what", "qui"
            },
            
            "NEG": {
                "no", "not", "non", "ne", "n", "never", "dont"
            },
            
            "AUX": {
                # Auxiliary verbs that strictly support another verb (Don, Fit, Go)
                "don", "fit", "go", 
                # French Auxiliaries
                "va", "vais", "ont", "est", "suis", "sont", "ai", "as", "av", "a",
                "wan", "bin"
            },
            
            "VERB": {
                # Full verbs including those that act as Copula/Existential
                "drop", "carry", "go", "pass", "come", "waka", "rush", "fall",
                "slip", "ferme", "take", "dodge", "send", "make", "get", "try", 
                "cut", "charge", "reduce", "give", "start", "turn", "remain", 
                "increase", "add", "keep", "finish", "beat", "spoil", "show", 
                "wait", "open", "print", "copy", "kill", "work", "say", "talk", 
                "happen", "crack", "change", "clash", "wire", "die", "chop", 
                "manage", "control", "wanda", "wonder", "check", "look", "tell", 
                "call", "need", "want", "like", "stay", "run", "enter", "leave", 
                "reach", "wash", "buy", "sell", "increase", "print",
                
                # Copula/Existential Pidgin Verbs (Moved from AUX to VERB to fix "Traffic dey")
                "dey", "be", "na",
                
                # Mixed Verbs
                "fit", # Can be aux or main verb "It fit"
                "suis", "est", "sont", "ont", "ai", "as", "av", "a", # French copulas
                "enerve", "confuse" # Used as verbs "Je suis enerve" (I am annoyed) or "Je m'enerve"
            },
            
            "PREP": {
                "for", "to", "since", "like", "at", "after", "in", "on",
                "with", "from", "de", "a", "dans", "sur", "avec", "devant", 
                "depuis", "pour", "chez", "au", "aux", "du", "d", "by", "about",
                "inside", "outside", "behind", "front", "near", "sans"
            },
            
            "ADJ": {
                "small", "big", "long", "short", "fast", "quick", "slow",
                "good", "bad", "hot", "cold", "sweet", "bitter", "better",
                "scarce", "ready", "true", "full", "open", "high", "low",
                "fine", "okay", "serious", "wrong", "right", "hard", "soft",
                "black", "white", "red", "young", "old", "new", "last",
                "franglais", "pidgin", "french", "english", "pale", "tired",
                "enerve", "confuse" # Can be adjectives
            },

            "ADVWORD": {
                "small-small", "nayo-nayo", "fast-fast", "well-well",
                "vite", "tot", "today", "yesterday", "tomorrow", "morning", 
                "again", "deja", "bientot", "trop", "encore", "just", "even",
                "combien", "wetin", "quand", "comment", "hmmm", "garrr", "ekiee", 
                "ah", "wah", "hein", "o", "nor", "la", "là", "comme", "now", "here", "there"
            },
            
            "NOUN": {
                # People
                "chef", "moto-guy", "mami", "pikin", "bro", "man", "aunty",
                "boss", "boy", "prof", "lecturer", "student", "babana",
                "boh", "students", "fools", "police", "thieves", "security",
                
                # Places
                "nlongkak", "carrefour", "quartier", "yaounde", "station",
                "hostel", "campus", "melen", "bastos", "universite", "ngola", 
                "checkpoint", "gate", "classe", "class", "cyber", "place",
                
                # Objects/Abstract
                "data", "network", "assignment", "connexion", "zero-zero",
                "eneo", "light", "phone", "current", "frigo", "price",
                "traffic", "rain", "road", "problem", "river", "mud",
                "shoe", "shoes", "water", "fuel", "queue", "taxi", "fare",
                "beignet", "beans", "piment", "helmet", "id",
                "noise", "time", "effort", "vie", "cours", "deadline",
                "am", "zero", "okada", "carte", "ac", "heat", "life",
                "sufferhead", "force", "td", "machine", "potopoto",
                "transport", "distance", "exam", "notes", "faim", "war",
                "entry", "screen", "timetable", "courses", "yamo", "lecture",
                "book", "bag", "food", "hand", "money", "cash", "change",
                "effort", "head", "body", "eye", "leg", "mouth", "shoes",
                "gate", "thieves", "example", "way", "thing"
            },
        }

    def tokenize(self, sentence: str) -> List[Token]:
        # Replace punctuation with spaces
        cleaned = (
            sentence.lower()
            .replace("'", "'")
            .replace("à", "a").replace("é", "e").replace("è", "e")
            .replace("ê", "e").replace("ô", "o")
            .replace(",", " ").replace("?", " ").replace("!", " ")
            .replace(";", " ").replace(".", " ").replace(":", " ")
            .replace("+", " ")
        )

        words = re.findall(r"[a-z]+(?:-[a-z]+)*(?:'[a-z]+)?|\d+[a-z]*", cleaned)
        tokens: List[Token] = []

        for word in words:
            token_type = self._classify(word)
            tokens.append((token_type, word))

        tokens = self._collapse_conjunctions(tokens)
        tokens.append(("$", "$"))
        return tokens

    def _classify(self, word: str) -> str:
        if re.fullmatch(r"\d+[a-z]*", word):
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

    def parse(self, tokens: List[Token], debug: bool = False) -> bool:
        stack: List[str] = ["$", self.grammar.start]
        index = 0
        
        while stack:
            top = stack.pop()
            current_type = tokens[index][0]
            current_lexeme = tokens[index][1]

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
                        first[nt].update(first[symbol] - {"ε"})
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


def build_grammar(mode: str = "pidgin") -> Grammar:
    base_productions = {
        "ADV": [["ADVWORD", "ADV_TAIL"]],
        "ADV_TAIL": [["ADVWORD", "ADV_TAIL"], ["ε"]],
        "PP": [["PREP", "NP"]],
    }
    
    if mode == "pidgin":
        pidgin_productions = {
            "S": [["CLAUSE", "S_TAIL"]],
            # KEY FIX: Allow CLAUSES to follow CLAUSES without CONJ (Run-on sentences)
            "S_TAIL": [
                ["CONJ", "CLAUSE", "S_TAIL"], 
                ["CLAUSE", "S_TAIL"],  
                ["ε"]
            ],
            
            "CLAUSE": [
                ["VOCATIVE", "CLAUSE"],
                ["CORE"]
            ],
            "VOCATIVE": [["NOUN"], ["DET", "NOUN"]], 
            
            "CORE": [
                ["VP"],                 
                ["NP", "CORE_TAIL"],   
                ["ADV"],                
                ["PP"]
            ],
            "CORE_TAIL": [
                ["VP"],
                ["ADV", "CORE_TAIL"],
                ["PP", "CORE_TAIL"],
                ["ε"]
            ],
            
            "NP": [
                ["DET", "NP_HEAD"], 
                ["NEG", "NP_HEAD"],
                ["NP_HEAD"]
            ],
            "NP_HEAD": [
                ["ADJ", "NP_TAIL"],
                ["NOUN", "NP_TAIL"], 
                ["PRON"], 
                ["NUM"]
            ],
            "NP_TAIL": [
                ["NOUN", "NP_TAIL"],
                ["ADJ", "NP_TAIL"],
                ["PP", "NP_TAIL"],
                ["ε"]
            ],
            
            "VP": [
                ["NEG", "AUX", "VP_TAIL"],
                ["NEG", "VERB", "VP_TAIL"],
                ["AUX", "VERB", "VP_TAIL"],
                ["VERB", "VP_TAIL"]          # "Dey" as main verb
            ],
            "VP_TAIL": [
                ["VERB", "VP_TAIL"],
                ["NP", "VP_TAIL"],
                ["PP", "VP_TAIL"],
                ["ADV", "VP_TAIL"],
                ["ε"]
            ],
        }
        productions = {**base_productions, **pidgin_productions}
    
    elif mode == "franglais":
        franglais_productions = {
            "S": [["CLAUSE", "S_TAIL"]],
            "S_TAIL": [
                ["CONJ", "CLAUSE", "S_TAIL"], 
                ["CLAUSE", "S_TAIL"], 
                ["ε"]
            ],
            
            "CLAUSE": [
                ["VOCATIVE", "CLAUSE"],
                ["INTJ", "CORE"],
                ["CORE"]
            ],
            "INTJ": [["ADVWORD"]],
            "VOCATIVE": [["NOUN"], ["DET", "NOUN"]],
            
            "CORE": [
                ["VP"],
                ["NP", "CORE_TAIL"],
                ["ADV"],
                ["PP"]
            ],
            "CORE_TAIL": [
                ["VP"],
                ["ADV", "CORE_TAIL"],
                ["PP", "CORE_TAIL"],
                ["ε"]
            ],
            
            "NP": [
                ["DET", "NP_HEAD"],
                ["NEG", "NP_HEAD"],
                ["PRON", "NP_TAIL"],
                ["NP_HEAD"]
            ],
            "NP_HEAD": [
                ["ADJ", "NP_TAIL"],
                ["NOUN", "NP_TAIL"],
                ["NUM"]
            ],
            "NP_TAIL": [
                ["NOUN", "NP_TAIL"],
                ["ADJ", "NP_TAIL"],
                ["PP", "NP_TAIL"],
                ["ε"]
            ],
            
            "VP": [
                ["NEG", "AUX", "VP_TAIL"],
                ["NEG", "VERB", "VP_TAIL"],
                ["PRON", "VERB", "VP_TAIL"], 
                ["AUX", "VERB", "VP_TAIL"],
                ["VERB", "VP_TAIL"]
            ],
            "VP_TAIL": [
                ["VERB", "VP_TAIL"],
                ["NP", "VP_TAIL"],
                ["PP", "VP_TAIL"],
                ["ADV", "VP_TAIL"],
                ["ε"]
            ],
        }
        productions = {**base_productions, **franglais_productions}
    
    else:
        raise ValueError(f"Unknown mode: {mode}")
    
    return Grammar(start="S", productions=productions)


def analyze_sentences(sentences: List[str], mode: str, debug: bool = False) -> None:
    lexer = Lexer()
    parser = LL1Parser(build_grammar(mode))

    print(f"\n{'='*70}")
    print(f"PARSING RESULTS - {mode.upper()} MODE")
    print(f"{'='*70}\n")

    accept_count = 0
    reject_count = 0

    for sentence in sentences:
        tokens = lexer.tokenize(sentence)
        ok = parser.parse(tokens, debug=debug)
        
        verdict = "ACCEPT" if ok else "REJECT"
        if ok:
            accept_count += 1
        else:
            reject_count += 1
        print(f"{verdict}: {sentence.strip()}")
    
    print(f"\n{'='*70}")
    print(f"Summary: {accept_count} ACCEPTED, {reject_count} REJECTED")
    print(f"{'='*70}")


def write_token_frequencies(sentences: List[str], output_suffix: str = "") -> None:
    lexer = Lexer()
    type_counts: Dict[str, int] = {}
    lexeme_counts: Dict[str, int] = {}

    for sentence in sentences:
        for token_type, lexeme in lexer.tokenize(sentence):
            if token_type == "$": continue
            type_counts[token_type] = type_counts.get(token_type, 0) + 1
            lexeme_counts[lexeme] = lexeme_counts.get(lexeme, 0) + 1

    filename = f"token_frequencies{output_suffix}.txt"
    output_path = Path(__file__).resolve().parent.parent / "data" / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("TOKEN TYPE FREQUENCIES\n")
        handle.write("=" * 50 + "\n")
        for k, v in sorted(type_counts.items()):
            handle.write(f"{k}: {v}\n")
        handle.write("\nLEXEME FREQUENCIES\n")
        for k, v in sorted(lexeme_counts.items()):
            handle.write(f"{k}: {v}\n")
    
    print(f"✓ Token frequencies written to: {filename}")


def write_ll1_artifacts(parser: LL1Parser, output_suffix: str = "") -> None:
    filename = f"ll1_artifacts{output_suffix}.txt"
    output_path = Path(__file__).resolve().parent.parent / "data" / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("CONTEXT-FREE GRAMMAR\n")
        handle.write("=" * 70 + "\n")
        for nt, rules in parser.grammar.productions.items():
            rhs = [" ".join(rule) for rule in rules]
            handle.write(f"{nt} -> {' | '.join(rhs)}\n")

        handle.write("\nFIRST SETS\n")
        handle.write("=" * 70 + "\n")
        for nt in sorted(parser.grammar.productions):
            handle.write(f"FIRST({nt}) = {{ {', '.join(sorted(parser.first[nt]))} }}\n")

        handle.write("\nFOLLOW SETS\n")
        handle.write("=" * 70 + "\n")
        for nt in sorted(parser.grammar.productions):
            handle.write(f"FOLLOW({nt}) = {{ {', '.join(sorted(parser.follow[nt]))} }}\n")

        handle.write("\nLL(1) PARSING TABLE\n")
        handle.write("=" * 70 + "\n")
        for (nt, term), rule in sorted(parser.table.items()):
            if rule != ["ε"]:
                handle.write(f"M[{nt}, {term}] = {' '.join(rule)}\n")
    
    print(f"✓ LL(1) artifacts written to: {filename}")


def process_mode(mode: str, data_dir: Path, debug: bool = False) -> None:
    try:
        if mode == "pidgin":
            path = data_dir / "sentences.txt"
            if not path.exists(): raise FileNotFoundError(path)
            with path.open("r", encoding="utf-8") as f:
                sentences = [l.strip() for l in f if l.strip()]
            analyze_sentences(sentences, "pidgin", debug)
            write_token_frequencies(sentences)
            write_ll1_artifacts(LL1Parser(build_grammar("pidgin")))
            
        elif mode == "franglais":
            path = data_dir / "franglais_sentences.txt"
            if not path.exists(): raise FileNotFoundError(path)
            with path.open("r", encoding="utf-8") as f:
                sentences = [l.strip() for l in f if l.strip()]
            analyze_sentences(sentences, "franglais", debug)
            write_token_frequencies(sentences, "_franglais")
            write_ll1_artifacts(LL1Parser(build_grammar("franglais")), "_franglais")
            
        elif mode == "both":
            for m in ["pidgin", "franglais"]:
                p = data_dir / (f"sentences.txt" if m == "pidgin" else f"franglais_sentences.txt")
                if p.exists():
                    with p.open("r", encoding="utf-8") as f:
                        s = [l.strip() for l in f if l.strip()]
                    analyze_sentences(s, m, debug)
                    suf = "" if m == "pidgin" else "_franglais"
                    write_token_frequencies(s, suf)
                    write_ll1_artifacts(LL1Parser(build_grammar(m)), suf)

    except Exception as e:
        print(f"Error: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Urban Slang Analyzer")
    parser.add_argument("--mode", choices=["pidgin", "franglais", "both"], default="pidgin")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir.parent / "data"
    process_mode(args.mode, data_dir, args.debug)


if __name__ == "__main__":
    main()

