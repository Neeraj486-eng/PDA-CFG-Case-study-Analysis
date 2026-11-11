"""Case-study metadata and sample accepted/rejected inputs."""
CASES = {
    "expr": {
        "title": "Arithmetic expression validation",
        "target": "Well-formed infix expressions over identifiers/numbers, + - * / and parentheses.",
        "accepted": ["a+b*c", "(x+12)/y", "42", "a*(b-c)"],
        "rejected": ["a+*b", "(x+2", "a b", "+a"],
    },
    "program": {
        "title": "Programming-language syntax checker",
        "target": "One or more let declarations or assignments, separated by semicolons; RHS is an arithmetic expression.",
        "accepted": ["let total = price * 2", "x=3; y=x+4", "let avg=(a+b)/2"],
        "rejected": ["let = 3", "x 3", "x=; y=2", "x=1;"],
    },
    "brackets": {
        "title": "Balanced brackets",
        "target": "All strings over (), [], {} in which every opening bracket is closed by the same type in LIFO order; other characters are ignored by this demo.",
        "accepted": ["()", "([]{})", "f(a[2], {b})"],
        "rejected": ["(", ")(", "([)]", "{[}"],
    },
    "palindrome": {
        "title": "Palindrome checker",
        "target": "All palindromes over alphabet {a,b}, including epsilon; the unmarked language needs a nondeterministic midpoint guess.",
        "accepted": ["", "a", "abba", "baab", "babab"],
        "rejected": ["ab", "aab", "abb"],
    },
    "password": {
        "title": "Password pattern validation",
        "target": "Strings of length at least 8 with >=1 uppercase, >=1 lowercase, >=1 digit and >=1 non-alphanumeric non-whitespace symbol; no spaces.",
        "accepted": ["Formal123!", "Pda_Cfg9", "Study#2026"],
        "rejected": ["password", "PASSWORD1!", "Pass123", "Pass word9!"],
    },
}
