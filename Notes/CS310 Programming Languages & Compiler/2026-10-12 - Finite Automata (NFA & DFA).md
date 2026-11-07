---
tags: [cs310, programming-languages, compiler, finite-automata, nfa, dfa, lecture-notes]
module: CS310
topic: "Finite Automata: NFA & DFA"
date: 2026-10-12
next: "[[2026-10-19 - Thompson's Construction & Subset Construction]]"
prev: "[[2026-10-05 - Regular Expressions]]"
---

# Finite Automata: NFA & DFA

> [!info] Lecture — 2026-10-12
> CS310 Programming Languages & Compiler — Week 3, Lectures 1 & 2
> Lecturer: Edgar Galván López · Source: `2026_CS310_Notes.pdf`

## NFA vs DFA

A **finite automaton** is a recogniser for a regular language — a machine that reads an input string left to right and answers *accept* or *reject*.

| | DFA | NFA |
|---|---|---|
| Next state | exactly **one** per symbol | a **set** of states (possibly none) |
| ε-transitions | not allowed | allowed |
| Deterministic? | yes | no — several paths may exist |

**Acceptance**: an NFA **accepts** an input iff there **exists at least one** path from the start state to an accepting state that consumes the entire string. A DFA accepts iff the single path ends in an accepting state.

## NFA for `(a|b)*abb`

**Transition graph** — state `0` loops on `a`/`b` (the `(a|b)*` part); on an `a` it may also move to `1`, beginning the `abb` suffix:

```
       a                b
   ┌───────┐        ┌───────┐
   │   ┌───┴──┐     │  ┌────┴───┐
   ▼   ▼      │     ▼  ▼        │
  (0)──a,b──▶(1)──b──▶(2)──b──▶((3))
 start                     accept
```

**Transition table** (the `ε` column is empty — this NFA has no ε-transitions):

| State | `a` | `b` | `ε` |
|---|---|---|---|
| 0 (start) | {0, 1} | {0} | — |
| 1 | — | {2} | — |
| 2 | — | {3} | — |
| 3 (accept) | — | — | — |

> [!example] Accepting `aabb`
> $0 \xrightarrow{a} 0 \xrightarrow{a} 1 \xrightarrow{b} 2 \xrightarrow{b} 3$ — ends in the accepting state `3`, so **accepted**. A string like `aab` reaches `2` but runs out of input before `3` → **rejected** (the slides contrast an accepting trace with a non-accepting one).

## NFA for `L(aa* | bb*)`

$L(aa^* \mid bb^*) = \{a^n \mid n \ge 1\} \cup \{b^m \mid m \ge 1\}$ — one-or-more `a`s, **or** one-or-more `b`s. The NFA splits into two branches via ε-transitions:

```
            ε        a
     ┌───────────▶ (s1) ──▶ (s2) ──a──▶ (s2)  ──▶ ((accept))
     │
(start)
     │            b
     └───────────▶ (s3) ──▶ (s4) ──b──▶ (s4)  ──▶ ((accept))
            ε
```

- Branch 1 recognises $a^n$ ($n \ge 1$): consume one `a`, then loop on `a`.
- Branch 2 recognises $b^m$ ($m \ge 1$): consume one `b`, then loop on `b`.
- The ε-transitions mean the machine *non-deterministically* guesses which branch applies.

## DFA for `(a|b)*abb`

The **deterministic** equivalent (each state has exactly one transition per symbol):

```
       a            a            b            b
   ┌───────┐   ┌────────┐   ┌────────┐   ┌────────┐
   ▼       │   ▼        │   ▼        │   ▼        │
  (A) ──a──▶ (B) ──a──▶ (B) ──b──▶ (C) ──b──▶ ((D))
   ▲  b               │  b        │  a        │
   └──────────────────┴───────────┴───────────┘
```

| State | `a` | `b` |
|---|---|---|
| A (start) | B | A |
| B | B | C |
| C | B | D |
| D (accept) | B | A |

> [!tip] NFA → DFA
> DFAs are easy to implement (a table + a pointer), NFAs are easy to *construct* from regular expressions. The **subset construction** (next lecture, [[2026-10-19 - Thompson's Construction & Subset Construction]]) turns the latter into the former automatically.

---

> [!tip] Next lecture
> See how a regular expression is turned into an NFA (Thompson's construction) and then into a DFA (subset construction).
