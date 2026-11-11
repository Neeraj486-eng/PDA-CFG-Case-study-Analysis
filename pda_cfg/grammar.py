"""Small CFG utilities used by the case-study demonstrations."""
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass(frozen=True)
class Grammar:
    start: str
    productions: Dict[str, Tuple[Tuple[str, ...], ...]]

    def describe(self) -> str:
        lines = []
        for lhs, alternatives in self.productions.items():
            rhs = [" ".join(p) if p else "ε" for p in alternatives]
            lines.append(f"{lhs} -> " + " | ".join(rhs))
        return "\n".join(lines)

BALANCED_GRAMMAR = Grammar("S", {
    "S": (("B", "S"), ()),
    "B": (("(", "S", ")"), ("[", "S", "]"), ("{", "S", "}"), ("(", ")"), ("[", "]"), ("{", "}"),),
})

ARITHMETIC_GRAMMAR = Grammar("E", {
    "E": (("E", "+", "T"), ("E", "-", "T"), ("T",)),
    "T": (("T", "*", "F"), ("T", "/", "F"), ("F",)),
    "F": (("(", "E", ")"), ("id",), ("num",)),
})

PROGRAM_GRAMMAR = Grammar("Program", {
    "Program": (("StmtList",),),
    "StmtList": (("Stmt", ";", "StmtList"), ("Stmt",)),
    "Stmt": (("let", "id", "=", "Expr"), ("id", "=", "Expr")),
    "Expr": (("Term", "ExprTail"),),
    "ExprTail": (("+", "Term", "ExprTail"), ("-", "Term", "ExprTail"), ()),
    "Term": (("Factor", "TermTail"),),
    "TermTail": (("*", "Factor", "TermTail"), ("/", "Factor", "TermTail"), ()),
    "Factor": (("(", "Expr", ")"), ("id",), ("num",)),
})

PALINDROME_GRAMMAR = Grammar("S", {
    "S": (("a", "S", "a"), ("b", "S", "b"), ("a",), ("b",), ()),
})

PASSWORD_GRAMMAR = Grammar("Password", {
    "Password": (("Upper", "Lower", "Digit", "Tail"),),
    "Tail": (("Char", "Tail"), ()),
})
