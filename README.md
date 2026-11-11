
# Case Study-Based Analysis and Design Using PDA and CFG

**Course:** 21CSC301T Formal Language and Automata  
**Assessment:** CLA-2, Assessment Task 3  
**Student:** K Neeraj (RA2411026050023)  
**Programme:** B.Tech AIML 'A', III Year  
**Faculty:** Dr. C. Gunasundari  
**Institution:** SRM IST Tiruchirappalli  
**Language:** Python 3.10+  
**Project type:** Academic case-study implementation

This project models five practical input-validation problems using formal languages. It provides target-language definitions, CFG productions, PDA designs, derivations/stack traces, accepted and rejected examples, ambiguity/determinism discussions, executable validators and automated tests.

## 1. Objectives

- Define each target language precisely before designing its grammar or automaton.
- Express context-free languages using standard CFG notation.
- Explain PDA states, stack symbols and transition behaviour.
- Show why finite automata cannot recognise the non-regular examples in this project.
- Identify ambiguity and revise grammars where needed.
- Test both valid and invalid strings using a small Python implementation.

## 2. Project structure

```text
PDA-CFG-Case-Studies/
├── README.md
├── requirements.txt
├── .gitignore
├── pda_cfg/
│   ├── __init__.py
│   ├── grammar.py
│   ├── validators.py
│   ├── cases.py
│   └── cli.py
├── tests/
│   └── test_validators.py
└── docs/
    └── THEORY.md
```

## 3. Installation and execution

Python 3.10 or later is recommended.

```bash
cd PDA-CFG-Case-Studies

python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

# Run all case studies
python -m pda_cfg.cli all

# Run individual case studies
python -m pda_cfg.cli expr
python -m pda_cfg.cli program
python -m pda_cfg.cli brackets
python -m pda_cfg.cli palindrome
python -m pda_cfg.cli password

# Run automated tests
python -m pytest -q
```

The validators use only the Python standard library. Pytest is needed only for the test suite.

## 4. Case-study summary

| # | Case study | Formal model | Determinism / memory |
|---|---|---|---|
| 1 | Arithmetic expression validation | Unambiguous precedence CFG; CFG-to-PDA construction | Predictive parser |
| 2 | Programming-language syntax checker | CFG for a small assignment language | Predictive parsing |
| 3 | Balanced parentheses/brackets | CFG and stack-matching PDA | Deterministic PDA |
| 4 | Palindrome checker | CFG for palindromes over {a,b} | NPDA midpoint guess |
| 5 | Password pattern validation | Regular expression / finite automaton | DFA is sufficient |

## 5. Why finite automata are insufficient for the context-free cases

A finite automaton has only a fixed finite number of states and cannot store an unbounded number of opening brackets or remember an arbitrarily long first half of a palindrome.

The language `{ (ⁿ )ⁿ : n ≥ 0 }` is non-regular by the pumping lemma. Pumping a portion of the opening brackets changes their count without changing the closing brackets. Therefore, the resulting string is not balanced.

Likewise, `{aⁿ b aⁿ : n ≥ 0}` is a non-regular subset of the palindrome language. A PDA solves these problems using an unbounded stack.

Arithmetic expressions with arbitrarily nested parentheses also require nesting memory. In contrast, the password policy in Case Study 5 is regular and can be recognised by a DFA.

## 6. Implementation notes and scope

- Arithmetic parser: recognises identifiers, decimal/integer numbers, +, -, *, / and parentheses. It checks syntax, not numeric evaluation.
- Programming checker: recognises `let name = expression` or `name = expression`, with statements separated by semicolons.
- Bracket validator: ignores non-bracket characters to demonstrate stack matching.
- Palindrome checker: uses direct reversal as an executable recogniser. Its theoretical PDA design is described in `docs/THEORY.md`.
- Password validator: demonstrates an illustrative regular password policy, not a security-strength score.

## 7. Expected result

Running `python -m pda_cfg.cli all` prints each target language, example strings and acceptance results.

Running `python -m pytest -q` executes positive and negative tests for all five validators.

## 8. Conclusion

CFGs describe recursive syntax, while PDAs recognise context-free languages by using a stack.

These models are useful for nested expressions, programming-language fragments, balanced delimiters and palindrome structures.

Not every validation problem needs a PDA: a finite-state model is sufficient for regular password-pattern constraints. Choosing the simplest suitable formal model is an important part of language design.
