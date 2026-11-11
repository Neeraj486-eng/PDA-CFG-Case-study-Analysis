"""Executable recognisers for the five formal-language case studies."""
import re

TOKEN_RE = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|([A-Za-z_][A-Za-z0-9_]*)|(.))")

class ParseError(ValueError):
    pass

class TokenStream:
    def __init__(self, text):
        self.tokens = []
        pos = 0
        while pos < len(text):
            if not text[pos:].strip():
                break
            match = TOKEN_RE.match(text, pos)
            if not match:
                raise ParseError(f"Unexpected input at position {pos}")
            number, ident, symbol = match.groups()
            if number:
                self.tokens.append(("num", number))
            elif ident:
                self.tokens.append(("let" if ident == "let" else "id", ident))
            elif symbol in "+-*/()=;":
                self.tokens.append((symbol, symbol))
            elif symbol.isspace():
                pass
            else:
                raise ParseError(f"Invalid character {symbol!r}")
            pos = match.end()
        self.tokens.append(("EOF", "EOF"))
        self.index = 0

    def peek(self): return self.tokens[self.index][0]
    def take(self, kind=None):
        token = self.tokens[self.index]
        if kind is not None and token[0] != kind:
            raise ParseError(f"Expected {kind}, found {token[1]!r}")
        self.index += 1
        return token


def validate_arithmetic(source):
    """Recognise expressions with +,-,*,/, parentheses, identifiers and numbers."""
    ts = TokenStream(source)
    def factor():
        if ts.peek() in ("num", "id"):
            ts.take()
        elif ts.peek() == "(":
            ts.take("("); expression(); ts.take(")")
        else:
            raise ParseError("Expected a number, identifier, or parenthesised expression")
    def term():
        factor()
        while ts.peek() in ("*", "/"):
            ts.take(); factor()
    def expression():
        term()
        while ts.peek() in ("+", "-"):
            ts.take(); term()
    expression()
    if ts.peek() != "EOF":
        raise ParseError(f"Unexpected token {ts.take()[1]!r}")
    return True


def validate_program(source):
    """Recognise a tiny language: let x = expr; x = expr; (one or more statements)."""
    ts = TokenStream(source)
    def factor():
        if ts.peek() in ("num", "id"):
            ts.take()
        elif ts.peek() == "(":
            ts.take("("); expression(); ts.take(")")
        else:
            raise ParseError("Expected identifier, number, or '('")
    def term():
        factor()
        while ts.peek() in ("*", "/"):
            ts.take(); factor()
    def expression():
        term()
        while ts.peek() in ("+", "-"):
            ts.take(); term()
    def statement():
        if ts.peek() == "let": ts.take("let")
        ts.take("id"); ts.take("="); expression()
    statement()
    while ts.peek() == ";":
        ts.take(";")
        if ts.peek() == "EOF":
            raise ParseError("A statement is required after ';'")
        statement()
    if ts.peek() != "EOF":
        raise ParseError(f"Unexpected token {ts.take()[1]!r}")
    return True


def validate_brackets(source, trace=False):
    """DPDA-style stack matcher. Non-bracket characters are ignored."""
    pairs = {")": "(", "]": "[", "}": "{"}
    opening = set(pairs.values())
    stack, moves = ["Z0"], []
    for char in source:
        if char in opening:
            stack.append(char)
            moves.append(f"read {char}: push {char}; stack={stack}")
        elif char in pairs:
            if len(stack) == 1 or stack[-1] != pairs[char]:
                moves.append(f"read {char}: reject (top does not match)")
                return (False, moves) if trace else False
            stack.pop()
            moves.append(f"read {char}: pop {pairs[char]}; stack={stack}")
    accepted = stack == ["Z0"]
    moves.append("accept" if accepted else f"reject: unclosed openings {stack[1:]}")
    return (accepted, moves) if trace else accepted


def validate_palindrome(source, alphabet="ab"):
    """Recognise even/odd palindromes over {a,b}; mirrors the CFG non-deterministic PDA."""
    if any(ch not in alphabet for ch in source):
        return False
    return source == source[::-1]


def validate_marked_palindrome(source, marker="#"):
    """Deterministic PDA language {w#w^R}; marker identifies the midpoint."""
    if source.count(marker) != 1:
        return False
    left, right = source.split(marker)
    return left == right[::-1]


def validate_password(source):
    """Example regular policy: >=8 chars, uppercase, lowercase, digit, symbol; no whitespace."""
    return (len(source) >= 8 and re.search(r"[A-Z]", source) is not None
            and re.search(r"[a-z]", source) is not None
            and re.search(r"\d", source) is not None
            and re.search(r"[^A-Za-z0-9\s]", source) is not None
            and re.search(r"\s", source) is None)
