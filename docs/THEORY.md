# Formal Models, Derivations and Validation Evidence

This document gives the formal-language details used in the five case studies. `ε` denotes the empty string. A PDA configuration is written as `(state, unread input, stack)` with the stack top shown at the right.

## Case Study 1 — Arithmetic expression validation

### Target language

Let identifiers be `id`, numeric tokens be `num`, and operators be `+`, `-`, `*`, `/`. The language consists of syntactically valid infix expressions with balanced parentheses. Whitespace is ignored by the lexer.

### CFG

The compact precedence grammar is:

```text
E -> E + T | E - T | T
T -> T * F | T / F | F
F -> ( E ) | id | num
```

`E` handles addition/subtraction, `T` handles multiplication/division, and `F` handles atomic operands or parenthesised expressions. Since `T` is below `E`, multiplication/division bind more tightly. Left recursion makes operators at the same level left-associative.

For a predictive parser, eliminate left recursion:

```text
E  -> T E'
E' -> + T E' | - T E' | ε
T  -> F T'
T' -> * F T' | / F T' | ε
F  -> ( E ) | id | num
```

### Derivation

For `id + id * id`, a leftmost derivation is:

```text
E => E + T
  => T + T
  => F + T
  => id + T
  => id + T * F
  => id + F * F
  => id + id * F
  => id + id * id
```

The parse groups the expression as `id + (id * id)`.

### Ambiguity and correction

The tempting grammar `E -> E+E | E*E | (E) | id` is ambiguous. For `id+id*id`, it permits both `(id+id)*id` and `id+(id*id)`. These groupings can produce different values. The precedence grammar above removes the ambiguity by separating expression, term and factor levels.

### PDA model

A general CFG can be converted to an NPDA that accepts by empty stack. Use one state `q`, bottom marker `Z0`, and stack symbols consisting of grammar non-terminals and terminals. Initially push the start symbol `E` above `Z0`. For a production `A -> X1...Xk`, nondeterministically replace `A` on top of the stack with the RHS in reverse push order so `X1` becomes the next stack top. If the stack top is a terminal equal to the next input token, consume the input and pop that terminal. Accept when input is exhausted and only `Z0` remains (then pop `Z0`).

This generic CFG-to-PDA construction is nondeterministic. The left-recursion-free grammar has an LL(1) predictive parser; the implementation uses recursive-descent functions with lookahead, which is deterministic for this grammar.

### Examples

| Input | Result | Reason |
|---|---|---|
| `a+b*c` | Accept | Valid operands and operator order |
| `(x+12)/y` | Accept | Parenthesised subexpression |
| `a+*b` | Reject | Two operators without an operand between |
| `(x+2` | Reject | Missing closing parenthesis |

---

## Case Study 2 — Programming-language syntax checker

### Target language

A small statement language with one or more statements. A statement is either a declaration `let id = Expr` or an assignment `id = Expr`. Statements are separated by semicolons. Expressions use identifiers, numbers, parentheses and the four arithmetic operators. A trailing semicolon is not allowed.

### CFG

```text
Program  -> StmtList
StmtList -> Stmt ; StmtList | Stmt
Stmt     -> let id = Expr | id = Expr
Expr     -> Term ExprTail
ExprTail -> + Term ExprTail | - Term ExprTail | ε
Term     -> Factor TermTail
TermTail -> * Factor TermTail | / Factor TermTail | ε
Factor   -> ( Expr ) | id | num
```

This grammar is suitable for predictive parsing: the optional tails encode repetition without left recursion. `let` is a reserved keyword and is not accepted as an identifier in the declaration position.

### Derivation

For `let x = 3 + y * 2`:

```text
Program => StmtList => Stmt
=> let id = Expr
=> let x = Term ExprTail
=> let x = Factor ExprTail
=> let x = num ExprTail
=> let x = 3 + Term ExprTail
=> let x = 3 + Factor TermTail ExprTail
=> let x = 3 + id * Factor TermTail ExprTail
=> let x = 3 + y * num
=> let x = 3 + y * 2
```

### PDA / parser stack

A predictive parser can be viewed as a deterministic pushdown machine. Its finite control tracks the current parser routine/lookahead token; its stack stores grammar symbols and pending parser work. For each non-terminal, the parser selects a production using the next token. A terminal must match the next input token and is then consumed. The parser accepts only when the start production has completed and the input is at EOF.

Example stack idea (top at left):

```text
Initial:  [Program, EOF]
Expand:   [StmtList, EOF]
Select:   [Stmt, EOF]
Match:    let, id, =, Expr, EOF
...
Accept:   [EOF] with EOF lookahead
```

### Examples

| Input | Result | Reason |
|---|---|---|
| `let total = price * 2` | Accept | Valid declaration |
| `x=3; y=x+4` | Accept | Two valid statements |
| `let = 3` | Reject | Identifier missing |
| `x=; y=2` | Reject | Expression missing |
| `x=1;` | Reject | Trailing separator requires another statement |

This case is a syntax checker only. Real programming languages have additional lexical, type, scope and semantic rules.

---

## Case Study 3 — Balanced parentheses and brackets

### Target language

`L` contains all properly nested strings over `(`, `)`, `[`, `]`, `{`, `}`. Every closer must match the most recent unmatched opener. The empty string is included.

### CFG

```text
S -> B S | ε
B -> ( S ) | [ S ] | { S } | () | [] | {}
```

`S` is a sequence of balanced blocks; `B` is one balanced block. This right-recursive list grammar gives a unique sequence decomposition. A simpler grammar such as `S -> SS | (S) | [] | ... | ε` is ambiguous because a sequence like `()()()` can be grouped in more than one way using `SS`.

### PDA

A deterministic PDA uses states `q` (scanning) and `qf` (accepting), with stack-bottom symbol `Z0` and stack symbols `(`, `[`, `{`.

- On `(`, `[`, or `{`, push that symbol.
- On `)`, `]`, or `}`, pop only if the stack top is its matching opener; otherwise reject.
- At end of input, accept if the stack contains only `Z0`.

This is deterministic: the next action is fixed by the current input symbol and stack top. It needs no midpoint guess.

### Stack trace

For input `([])`, with the stack top shown at the right:

| Step | Input read | Stack after move |
|---|---|---|
| 0 | — | `Z0` |
| 1 | `(` | `Z0 (` |
| 2 | `[` | `Z0 ( [` |
| 3 | `]` | `Z0 (` |
| 4 | `)` | `Z0` |
| 5 | end | Accept |

For `([)]`, reading `)` finds `[` on top. The closer does not match, so the PDA rejects immediately. For `((`, the input ends with two unmatched openers, so it rejects.

### Why DFA is insufficient

The machine must remember an unbounded number of unmatched opening delimiters. The one-type sublanguage `{ (ⁿ )ⁿ : n ≥ 0 }` is non-regular by the pumping lemma, so no finite automaton can recognise all balanced strings.

---

## Case Study 4 — Palindrome checker

### Target language

`L = { w in {a,b}* : w = w^R }`, where `w^R` is the reverse of `w`. Both odd- and even-length palindromes and `ε` are included.

### CFG

```text
S -> a S a | b S b | a | b | ε
```

The outer symbols of a palindrome must match. Removing them leaves a smaller palindrome, so the grammar captures the language. This grammar is unambiguous: for a non-empty string, its first and last symbols determine the outer production; the centre is eventually `a`, `b`, or `ε`.

### PDA models

For the unmarked language, an NPDA pushes symbols while reading the first half, nondeterministically guesses the midpoint (using an ε-transition), then compares the remaining input by popping matching symbols. The midpoint is not marked in the input, so the PDA must guess it. The unmarked palindrome language is not deterministic context-free in general.

For the marked language `L# = { w#w^R : w in {a,b}* }`, the centre marker makes the split explicit. A DPDA pushes each `a` or `b` before `#`, then after `#` pops one symbol for each matching input character. It accepts when the marker has been read, the input ends and the stack returns to `Z0`.

### Example

For `abba`, an NPDA can push `a`, `b`, guess the midpoint, then pop `b`, `a`. For `ab#ba`, the deterministic marked machine pushes `a,b`, reads `#`, then matches `b,a` while popping. `ab` is rejected because its reverse is `ba`, not `ab`.

### Why DFA is insufficient

A palindrome recogniser must compare arbitrarily distant symbols. The language `{aⁿ b aⁿ : n ≥ 0}` is a non-regular subset of this language; the pumping lemma shows that a finite automaton cannot remember an arbitrary number of initial `a` symbols for later comparison.

---

## Case Study 5 — Password pattern validation

### Target language

For this demonstration, a valid string must:

1. contain at least 8 characters;
2. contain at least one uppercase English letter;
3. contain at least one lowercase English letter;
4. contain at least one decimal digit;
5. contain at least one non-alphanumeric, non-whitespace symbol; and
6. contain no whitespace.

This policy is an example of a regular language. It is not intended to measure real-world password strength.

### Regular-expression description

```text
^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[^A-Za-z0-9\\s])[A-Za-z0-9\\S]{8,}$
```

The executable implementation uses equivalent explicit checks. The look-ahead notation is a convenient regex specification; the policy can also be implemented by a DFA whose finite state records which required character categories have appeared and a length counter capped at 8. The DFA also has a rejecting sink state for whitespace or disallowed input.

### CFG-style specification

A simple grammar-style description is:

```text
Password -> Upper Lower Digit Tail
Tail     -> Char Tail | ε
```

This is a schematic constraint description, not a complete ordinary CFG for the policy: the three required categories may occur in any order and at any position, and the minimum length must also be enforced. The DFA is the clearest exact model for this regular policy.

### Determinism and examples

The DFA updates a finite set of flags: `seenUpper`, `seenLower`, `seenDigit`, `seenSymbol`, plus a length state `0..8+`. It accepts at end-of-input only when all flags are true and the length state is `8+`. No stack is needed.

| Input | Result | Reason |
|---|---|---|
| `Formal123!` | Accept | All categories and length satisfied |
| `Pda_Cfg9` | Accept | Upper/lower/digit/symbol present |
| `password` | Reject | No uppercase, digit or symbol |
| `Pass123` | Reject | Fewer than 8 characters and no symbol |
| `Pass word9!` | Reject | Whitespace is disallowed |

### Why a PDA is unnecessary

The policy needs only a finite number of category flags and a length counter capped at the threshold. That information can be encoded in a finite number of DFA states. A PDA could recognise the same language, but its stack would add unnecessary power and complexity.

---

## Overall comparison

| Language | Needs unbounded stack? | Best model in this project |
|---|---:|---|
| Arithmetic expressions with nested parentheses | Yes, for arbitrary nesting | CFG / PDA; deterministic predictive parser for the chosen grammar |
| Small programming syntax | Yes, for nested expression structure | CFG / predictive pushdown parser |
| Balanced brackets | Yes | DPDA |
| Unmarked palindromes | Yes; nondeterministic midpoint selection | CFG / NPDA |
| Marked palindromes `w#w^R` | Yes | DPDA |
| Password pattern | No | DFA / regular expression |

## Final conclusion

The case studies show that CFGs and PDAs model recursive and nested structures that finite automata cannot handle. The stack provides unbounded memory for matching delimiters, parsing nested expressions and comparing palindrome halves. Ambiguous grammars must be revised when multiple parse trees produce different interpretations. Password-pattern validation is included as a contrast: its constraints are regular, so a DFA is sufficient and a PDA is unnecessary.

## Additional failed-processing examples and explicit control states

### Arithmetic: failed parse of `a+*b`

Using the LL(1) grammar, the parser expands `E -> T E'`, `T -> F T'`, and `F -> id`, then matches `a`. The next token is `+`, so `T' -> ε` and `E' -> + T E'` are selected. The parser now expects a `T`, whose `F` must begin with `(`, `id`, or `num`. The actual next token is `*`; no production can start with `*`, so the parser rejects. It does not silently skip the operator.

The generic CFG-to-PDA uses control state `q`; its stack alphabet is `{Z0} ∪ N ∪ Σ`, where `N` is the set of grammar non-terminals and `Σ` the token terminals. Its transition types are (1) production expansion, (2) matching-terminal consumption, and (3) final bottom-marker removal. A mismatch has no valid transition and rejects.

### Programming syntax: failed parse of `x=;`

The parser reads `id` (`x`) and `=`, then calls the expression parser. A factor must begin with `id`, `num`, or `(`. The next token is `;`, so there is no valid factor production and the parser rejects. The semicolon cannot stand in for a missing expression.

The predictive pushdown parser has a start/control state `q_parse`, an accepting state `q_accept`, and a rejecting outcome when no table entry or terminal match exists. Its stack alphabet contains `Z0`, grammar symbols (`Program`, `StmtList`, `Stmt`, `Expr`, `Term`, `Factor`, tail symbols) and terminals (`let`, `id`, `num`, `=`, arithmetic operators, parentheses, `;`). The stack expands non-terminals according to the next token and matches terminals in order.

### Balanced brackets: failed stack move for `([)]`

After reading `(` then `[`, the stack is `Z0 ( [`. The next input is `)`, but the top is `[`. Since `)` can pop only `(`, no transition is defined and the DPDA rejects immediately. Its states are `q_scan` and `q_accept`; the stack alphabet is `{Z0, (, [, {}`. A mismatched closer transitions to rejection (or has no transition). End-of-input moves to `q_accept` only when `Z0` is the sole stack symbol.

### Palindrome: failed comparison for `ab#bb`

The marked DPDA pushes `a`, then `b`, and reads `#` to switch from `q_push` to `q_pop`. The first symbol after the marker is `b`, which matches and pops `b`. The next symbol is `b`, but the stack top is `a`; the comparison fails and the machine rejects. Its states are `q_push` (before `#`), `q_pop` (after `#`), `q_accept`, and an implicit rejecting state. Its stack alphabet is `{Z0, a, b}`. For the unmarked palindrome language, an NPDA additionally has an ε-transition choice to switch from pushing to popping at a guessed midpoint; that guess is what makes it nondeterministic.

### Password: failed DFA condition for `password`

A DFA can track the tuple `(length_bucket, U, L, D, S)`, where `length_bucket` is one of `0,1,...,7,8+` and each Boolean records whether uppercase, lowercase, digit and symbol categories have appeared. The conceptual states are all reachable tuples plus a rejecting sink. On each character, update the length bucket and the relevant category flag. Whitespace goes to the sink. At end-of-input, accept only if the length bucket is `8+` and all four flags are true. The input `password` reaches a state with `L=true` but `U=false`, `D=false`, and `S=false`, so it is rejected. The state set is finite; no stack symbols are required.
