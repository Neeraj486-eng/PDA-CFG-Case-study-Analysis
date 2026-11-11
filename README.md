# Case Study-Based Analysis and Design Using PDA and CFG

**Course:** Formal Languages and Automata (FLA)  
**Project type:** Academic case-study implementation  
**Language:** Python 3.10+  
**Student:** K Neeraj (RA) — edit this line if your department requires the full register number.

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
│   ├── grammar.py       # CFG production definitions
│   ├── validators.py    # executable recognisers / parsers
│   ├── cases.py         # language descriptions and sample strings
│   └── cli.py           # command-line interface
├── tests/
│   └── test_validators.py
└── docs/
    └── THEORY.md        # detailed models, derivations and analysis
```

## 3. Installation and execution

Python 3.10 or later is recommended.

```bash
# 1. Move into the project directory
cd PDA-CFG-Case-Studies

# 2. (Optional) create and activate a virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# 3. Install the test dependency
pip install -r requirements.txt

# 4. Run every case study
python -m pda_cfg.cli all

# 5. Run one case study
python -m pda_cfg.cli expr
python -m pda_cfg.cli program
python -m pda_cfg.cli brackets
python -m pda_cfg.cli palindrome
python -m pda_cfg.cli password

# 6. Run the automated tests
python -m pytest -q
```

The validators themselves use only the Python standard library. `pytest` is needed only for the test suite.

## 4. Case-study summary

| # | Case study | Formal model | Determinism / memory |
|---|---|---|---|
| 1 | Arithmetic expression validation | Unambiguous precedence CFG; CFG-to-PDA construction | General CFG-to-PDA is an NPDA; the implemented predictive parser is deterministic for this grammar |
| 2 | Programming-language syntax checker | CFG for a small assignment language | Predictive parsing with one-token lookahead; parser maintains a call/parse stack |
| 3 | Balanced parentheses/brackets | CFG and stack-matching PDA | DPDA; stack remembers unmatched opening brackets |
| 4 | Palindrome checker | CFG for palindromes over `{a,b}` | Unmarked language needs an NPDA midpoint guess; marked form `{w#w^R}` is deterministic |
| 5 | Password pattern validation | Regular expression / finite automaton | DFA is sufficient; a PDA is not required |

## 5. Why finite automata are insufficient for the context-free cases

A finite automaton has only a fixed finite number of states and cannot store an unbounded number of opening brackets or remember an arbitrarily long first half of a palindrome. The language `{ (ⁿ )ⁿ : n ≥ 0 }` is non-regular by the pumping lemma: for pumping length `p`, the first `p` symbols of `(ⁿ )ⁿ` are all `(`; pumping a non-empty part of that prefix changes the number of opening brackets without changing the closing part. The pumped string is not balanced. Therefore balanced brackets are not regular.

Likewise, `{aⁿ b aⁿ : n ≥ 0}` is a non-regular subset of the palindrome language, so the full palindrome language cannot be regular. A PDA solves this by using an unbounded stack. Arithmetic expressions with arbitrarily nested parentheses also require unbounded nesting memory. In contrast, the password policy in Case Study 5 is regular and can be recognised by a DFA.

## 6. Implementation notes and scope

- The arithmetic parser recognises identifiers, decimal/integer number tokens, `+ - * /`, and parentheses. It checks syntax, not division-by-zero or numeric evaluation.
- The programming checker recognises a deliberately small language: `let name = expression` or `name = expression`, with multiple statements separated by semicolons. It is not a complete Python/C compiler and does not perform type checking or name resolution.
- The bracket validator ignores non-bracket characters to demonstrate stack matching. A production compiler would first tokenize input so brackets inside strings/comments are not treated as syntax.
- The palindrome checker uses direct reversal as an executable recogniser. The theoretical PDA design is described in `docs/THEORY.md`.
- The password rule is an illustrative regular policy, not a security-strength score or a recommendation to reuse passwords.

## 7. Expected result

Running `python -m pda_cfg.cli all` prints each target language, example strings and acceptance results. Running `python -m pytest -q` runs positive and negative tests for all five validators.

## 8. Conclusion

CFGs describe recursive syntax, while PDAs recognise context-free languages by using a stack. These models are useful for nested expressions, programming-language fragments, balanced delimiters and palindrome structures. Not every validation problem needs a PDA: a finite-state model is sufficient for regular password-pattern constraints. Choosing the simplest suitable formal model is an important part of language design.

---

**Reference for project structure and topic coverage:** [FLA-Task3-PDA-CFG-Case-Studies](https://github.com/Vaishakkr/FLA-Task3-PDA-CFG-Case-Studies). This repository is an independently written implementation and explanation, not a copy of the reference repository.
