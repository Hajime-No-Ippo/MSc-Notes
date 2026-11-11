---
tags: [cs310, programming-languages, compiler, syntax-analysis, left-recursion, left-factoring, top-down-parsing, lecture-notes]
module: CS310
topic: "Left Recursion & Left Factoring"
date: 2026-11-09
next: "[[2026-11-16 - Predictive Parsing (FIRST & FOLLOW)]]"
prev: "[[2026-11-02 - Syntax Analysis & Grammar]]"
---

# Left Recursion & Left Factoring

> [!info] Lecture — 2026-11-09
> CS310 Programming Languages & Compilers — Week 7, Syntax Analysis (Left Recursion, Left Factoring, Top-Down Parsing)
> Lecturer: Edgar Galván López · Source: `week_7_l1.pdf`, `week_7_l2.pdf`

**Overview**

- A **regular expression** can always be rewritten as an equivalent **grammar**.
- Ambiguity (e.g. the **dangling-else**) can be removed by restructuring the grammar.
- **Left recursion** breaks top-down parsers — it must be eliminated.
- **Left factoring** defers a choice between two alternatives until enough input is seen (needed for predictive parsing).
- **Recursive-descent parsing** is the top-down approach, with **backtracking** as a fallback.

---

## 1. Regular Expressions vs Context-Free Grammars

Every RE can be expressed as a grammar. Example: the RE $(a|b)^*abb$ becomes:

$$
\begin{aligned}
A_0 &\to aA_0 \mid bA_0 \mid aA_1 \\
A_1 &\to bA_2 \\
A_2 &\to bA_3 \\
A_3 &\to \varepsilon
\end{aligned}
$$

(Each state of the NFA becomes a nonterminal; a move on a symbol becomes a production.)

---

## 2. Eliminating Ambiguity — The Dangling-Else

```
stmt → if expr then stmt
     | if expr then stmt else stmt
     | other
```

This is ambiguous: `if E1 then if E2 then S1 else S2` has two parse trees. Rewrite:

```
stmt          → matched_stmt | unmatched_stmt
matched_stmt  → if expr then matched_stmt else matched_stmt | other
unmatched_stmt → if expr then stmt
               | if expr then matched_stmt else unmatched_stmt
```

This forces each `else` to bind to the nearest unmatched `if`.

---

## 3. Left Recursion

> [!important] Definition
> A grammar is **left recursive** if a nonterminal $A$ has a derivation $A \Rightarrow^+ A\alpha$ for some string $\alpha$. **Top-down parsers cannot handle left-recursive grammars.**

Example: $E \to E + E$ expands forever — $E \Rightarrow E+E \Rightarrow E+E+E \Rightarrow \dots$

### Eliminating immediate left recursion

Transform $A \to A\alpha \mid \beta$ into:

$$
A \to \beta A' \qquad A' \to \alpha A' \mid \varepsilon
$$

**General rule** — group $A \to A\alpha_1 \mid A\alpha_2 \mid \dots \mid A\alpha_m \mid \beta_1 \mid \dots \mid \beta_n$ (no $\beta_i$ begins with $A$), then:

$$
\begin{aligned}
A &\to \beta_1 A' \mid \beta_2 A' \mid \dots \mid \beta_n A' \\
A' &\to \alpha_1 A' \mid \alpha_2 A' \mid \dots \mid \alpha_m A' \mid \varepsilon
\end{aligned}
$$

> [!example] Classic expression grammar
> $$
> \begin{aligned}
> E &\to E + T \mid T &\Rightarrow\quad E &\to T E',\ E' \to +TE' \mid \varepsilon \\
> T &\to T * F \mid F &\Rightarrow\quad T &\to F T',\ T' \to *FT' \mid \varepsilon \\
> F &\to (E) \mid id && (\text{no left recursion})
> \end{aligned}
> $$

### Eliminating multi-step (non-immediate) left recursion

Immediate elimination does **not** remove left recursion involving two or more derivation steps:

```
S → Aa | b
A → Ac | Sd | ε
```

$S$ is left-recursive because $S \Rightarrow Aa \Rightarrow Sda$, yet it is not *immediate*. First substitute $S$ into $A$, then eliminate the immediate recursion that appears:

$$
A \to Ac \mid Aad \mid bd \mid \varepsilon
$$

then:

$$
\begin{aligned}
S &\to Aa \mid b \\
A &\to bdA' \mid A' \\
A' &\to cA' \mid adA' \mid \varepsilon
\end{aligned}
$$

---

## 4. Left Factoring

> [!note] Motivation
> When two alternatives share a common prefix $\alpha$ ($A \to \alpha\beta_1 \mid \alpha\beta_2$), the parser can't decide which to expand until it has seen past $\alpha$. Left factoring **defers** that decision.

Transform $A \to \alpha\beta_1 \mid \alpha\beta_2$ into:

$$
A \to \alpha A' \qquad A' \to \beta_1 \mid \beta_2
$$

> [!example] Dangling-else abstracted
> $$
> S \to iEtS \mid iEtSeS \mid a \;\Rightarrow\; S \to iEtSS' \mid a,\quad S' \to eS \mid \varepsilon
> $$

---

## 5. Top-Down Parsing (Recursive Descent)

- Top-down parsing = finding a **leftmost derivation**, equivalently building the parse tree from the **root**, creating nodes in **preorder**.
- **Recursive-descent** parser = a set of (mutually) recursive procedures, one per nonterminal.

> [!warning] Backtracking
> General recursive descent may need **backtracking** — repeatedly re-scanning the input — which **dramatically slows** parsing. It is rarely needed for programming-language constructs if the grammar is well written (LL(1)).

> [!example] Backtracking
> $$
> S \to cAd,\quad A \to ab \mid a,\quad w = cad
> $$
> Parsing $cad$: try $A \to ab$ (fails at second char), backtrack and try $A \to a$ (succeeds).

---

## 6. Summary

| Transformation | Purpose |
|---|---|
| Eliminate left recursion | Top-down parsers loop forever on $A \Rightarrow^+ A\alpha$ |
| Left factoring | Defer choice so predictive parsing can decide on one lookahead |
| Rewrite dangling-else | Remove ambiguity (bind `else` to nearest `if`) |

> [!tip] Next lecture
> With left recursion gone and grammar left-factored, we can build **predictive parsers** using **FIRST & FOLLOW** — **[[2026-11-16 - Predictive Parsing (FIRST & FOLLOW)]]**.
