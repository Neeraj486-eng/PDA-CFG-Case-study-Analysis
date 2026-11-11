import argparse
from .cases import CASES
from .validators import (validate_arithmetic, validate_program, validate_brackets,
                         validate_palindrome, validate_marked_palindrome, validate_password)

CHECKERS = {"expr": validate_arithmetic, "program": validate_program,
            "brackets": validate_brackets, "palindrome": validate_palindrome,
            "password": validate_password}

def run_case(name):
    case = CASES[name]
    print(f"\n## {case['title']}\nTarget language: {case['target']}")
    checker = CHECKERS[name]
    for label in ("accepted", "rejected"):
        print(f"{label.title()} examples:")
        for sample in case[label]:
            try: result = checker(sample)
            except ValueError: result = False
            print(f"  {sample!r:24} -> {'ACCEPT' if result else 'REJECT'}")
    if name == "brackets":
        _, moves = validate_brackets("([])", trace=True)
        print("Stack trace for '([])':")
        for move in moves: print("  " + move)
    if name == "palindrome":
        print("Marked deterministic example 'ab#ba':", "ACCEPT" if validate_marked_palindrome("ab#ba") else "REJECT")

def main():
    parser = argparse.ArgumentParser(description="PDA and CFG case-study demonstrator")
    parser.add_argument("case", choices=["all", *CASES], nargs="?", default="all")
    args = parser.parse_args()
    names = CASES if args.case == "all" else [args.case]
    for name in names: run_case(name)

if __name__ == "__main__": main()
