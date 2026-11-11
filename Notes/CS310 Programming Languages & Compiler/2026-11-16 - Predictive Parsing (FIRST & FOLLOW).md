---
tags: [cs310, programming-languages, compiler, syntax-analysis, predictive-parsing, ll1, first-follow, lecture-notes]
module: CS310
topic: "Predictive Parsing: FIRST & FOLLOW"
date: 2026-11-16
next: "[[]]"
prev: "[[2026-11-09 - Left Recursion & Left Factoring]]"
---

# Predictive Parsing: FIRST & FOLLOW

> [!info] Lecture — 2026-11-16
> CS310 Programming Languages & Compilers — Week 8, Syntax Analysis (Transition Diagrams for Predictive Parsers, FIRST and FOLLOW)
> Lecturer: Edgar Galván López · Source: `week_8_l1.pdf`

**Overview**

- **LL(1)** grammars = left-to-right scan, leftmost derivation, **1** token of lookahead — parseable without backtracking.
- A **transition diagram** can be drawn for a parser, just like for the lexical analyser.
- Predictive parsing tables are filled using two functions: **FIRST** and **FOLLOW**.

---

## 1. Predictive Parsers / LL(1) Grammars

> [!important] Definition
> An **LL(1)** grammar: **L**eft-to-right input, **L**eftmost derivation, **1** symbol of lookahead.

By carefully writing a grammar (eliminating left recursion + left factoring), we often get a grammar parseable by a recursive-descent parser with **no backtracking**.

Given the current input token $\alpha$ and a nonterminal $A$ to expand, we must **deterministically** pick one of $A \to \alpha_1 \mid \alpha_2 \mid \dots \mid \alpha_n$.

> [!example]
> $$
> \begin{aligned}
> stmt &\to \textbf{if}\ expr\ \textbf{then}\ stmt\ \textbf{else}\ stmt \\
>       &\mid \textbf{while}\ expr\ \textbf{do}\ stmt \\
>       &\mid \textbf{begin}\ stmt\_list\ \textbf{end}
> \end{aligned}
> $$
> The keywords `if`, `while`, `begin` each uniquely identify the alternative to choose.

---

## 2. Transition Diagrams for Predictive Parsers

To build the transition diagram of a predictive parser from a grammar, first **eliminate left recursion** and **left factor**. Then, for each nonterminal $A$:

1. Create an **initial** and a **final** (return) state.
2. For each production $A \to X_1 X_2 \dots X_n$, create a path from initial to final state with edges labelled $X_1 X_2 \dots X_n$. If $A \to \varepsilon$, the path is an edge labelled $\varepsilon$.

> [!example]
> $$
> \begin{aligned}
> E &\to TE' \\
> E' &\to +TE' \mid \varepsilon
> \end{aligned}
> $$
> - $E$: initial →(T)→(E′)→ final.
> - $E'$: initial →(+ T E′)→ final, and initial →(ε)→ final.

---

## 3. Computation of FIRST

> [!note] FIRST($X$)
> The set of terminals that can **begin** a string derived from $X$ (plus $\varepsilon$ if $X$ derives $\varepsilon$).

Rules for a symbol $X$:
1. If $X$ is a **terminal**, $\text{FIRST}(X) = \{X\}$.
2. If $X \to \varepsilon$ is a production, add $\varepsilon$ to $\text{FIRST}(X)$.
3. If $X$ is nonterminal with $X \to Y_1 Y_2 \dots Y_k$: add $a$ to $\text{FIRST}(X)$ if $a \in \text{FIRST}(Y_i)$ and $\varepsilon \in \text{FIRST}(Y_1), \dots, \text{FIRST}(Y_{i-1})$ (i.e. $Y_1\dots Y_{i-1} \Rightarrow^* \varepsilon$). If $\varepsilon \in \text{FIRST}(Y_j)$ for **all** $j = 1..k$, add $\varepsilon$ to $\text{FIRST}(X)$.

---

## 4. Computation of FOLLOW

> [!note] FOLLOW($A$)
> The set of terminals that can appear **immediately to the right** of $A$ in some sentential form.

Rules for nonterminals $A$:
1. Place $\$$ (the input right-end marker) in $\text{FOLLOW}(S)$, where $S$ is the start symbol.
2. If there is a production $A \to \alpha B \beta$, put everything in $\text{FIRST}(\beta)$ **except $\varepsilon$** into $\text{FOLLOW}(B)$.
3. If there is a production $A \to \alpha B$ (or $A \to \alpha B \beta$ where $\text{FIRST}(\beta)$ contains $\varepsilon$), put **everything in $\text{FOLLOW}(A)$** into $\text{FOLLOW}(B)$.

---

## 5. Summary

```mermaid
graph LR
    G[Grammar] --> L[Eliminate left recursion]
    L --> F[Left factor]
    F --> LL[LL(1) grammar]
    LL --> TD[Transition diagram]
    LL --> FF[FIRST & FOLLOW]
    FF --> T[Predictive parsing table]
```

| Concept | Meaning |
|---|---|
| LL(1) | left-to-right, leftmost, 1 lookahead |
| FIRST($X$) | terminals that begin strings from $X$ |
| FOLLOW($A$) | terminals that can follow $A$ |
| $\$$ | end-of-input marker |

> [!tip] Next lecture
> FIRST and FOLLOW fill the **predictive parsing table**, which drives the non-recursive predictive parser — the LL(1) parser implementation.
