# PDA state diagrams (Mermaid)

These are conceptual state diagrams; stack actions are written on transitions as `input, stack-top → replacement`.

## Balanced brackets DPDA

```mermaid
stateDiagram-v2
    [*] --> q_scan
    q_scan --> q_scan: opening bracket / push it
    q_scan --> q_scan: matching closer / pop opener
    q_scan --> q_accept: EOF and stack = Z0
    q_scan --> q_reject: mismatched closer
    q_scan --> q_reject: EOF with opener remaining
    q_accept --> [*]
```

## Marked palindrome DPDA for `w#w^R`

```mermaid
stateDiagram-v2
    [*] --> q_push
    q_push --> q_push: a or b / push symbol
    q_push --> q_pop: # / keep Z0 and switch phase
    q_pop --> q_pop: matching symbol / pop
    q_pop --> q_reject: mismatch or extra input
    q_pop --> q_accept: EOF and stack = Z0
    q_accept --> [*]
```

## CFG-to-PDA construction (arithmetic expressions)

```mermaid
stateDiagram-v2
    [*] --> q
    q --> q: expand nonterminal using a CFG production
    q --> q: match terminal with next input token and pop
    q --> q_accept: EOF and only bottom marker remains
    q --> q_reject: no production or terminal mismatch
    q_accept --> [*]
```

## Password DFA state information

The password DFA can be represented as a finite collection of product states rather than a pushdown automaton. Each state stores `(length_bucket, seen_upper, seen_lower, seen_digit, seen_symbol)`. Whitespace leads to a rejecting sink. The accepting states have `length_bucket=8+` and all four flags set to true.
