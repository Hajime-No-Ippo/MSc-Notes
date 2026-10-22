---
tags: [cs357, lab, coq, rocq, proofs, lecture-notes]
module: CS357
topic: "Lab 1 — Rocq (Coq) Proof Scripts"
date: 2026-10-07
next: "[[2026-10-21 - Lab 2 Rocq - Conjunction, Disjunction & Negation]]"
prev: "[[2026-10-01 - Lab 1 Logic & Propositional Translation]]"
---

# Lab 1 — Rocq (Coq) Proof Scripts

> [!info] CS357 Lab 1 (Rocq part) — 2026-10-01 / completed 2026-10-07
> Proving implication lemmas in Rocq (Coq) using **intro** and **apply**.
> Lab page: <https://classicwuhao.github.io/rocq/lab1.html>
> Submission: `25251621.txt` (all seven scripts, `.v` files concatenated) in `~/Downloads/lab1_rocq/`

---

## The Two Tactics

| Tactic | What it does |
|---|---|
| `intro` | Turns a goal `A -> B` into subgoal `B`, adding `A` as a hypothesis |
| `apply H` | Uses hypothesis `H : A -> B` to prove goal `B` by *changing the goal to A* |
| `exact H` | Closes the goal because `H` is *exactly* what is needed |

The asymmetry is the whole point:

- **`intro`** works **backwards from the goal** — it *destroys* the implication in the goal and *introduces* the premise.
- **`apply`** works **forwards from a hypothesis** — it *consumes* a hypothesis and *weakens* the goal to that hypothesis's premise.

You only ever move in one direction: the goal gets simpler until it matches a hypothesis.

---

## Worked Example

$$\texttt{Lemma example1: } (A \to B) \to (B \to C) \to (A \to C)$$

| Step | Tactic | Goal after | Hypotheses |
|---|---|---|---|
| 0 | — | `(A→B) → (B→C) → A→C` | — |
| 1 | `intro H` | `(B→C) → A→C` | `H : A→B` |
| 2 | `intro H0` | `A → C` | `H : A→B`, `H0 : B→C` |
| 3 | `intro H1` | `C` | `H : A→B`, `H0 : B→C`, `H1 : A` |
| 4 | `apply H0` | `B` | goal `C` needs `B` |
| 5 | `apply H` | `A` | goal `B` needs `A` |
| 6 | `exact H1` | ✅ closed | `H1 : A` matches |

```coq
Parameter A B C: Prop.

Lemma example1: (A->B) -> (B->C) -> (A->C).
Proof.
  intro H.
  intro H0.
  intro H1.
  apply H0.
  apply H.
  exact H1.
Qed.
```

> [!tip] `intros` shorthand
> A chain of `intro`s can be replaced with a single `intros`, which introduces *everything* in the goal at once. That is what the submitted proofs below mostly use.
>
> Auto-naming kicks in: first hypothesis is `H`, then `H0`, `H1`, … — so when you write `apply H1` you must know *which* position that is.

> [!note] Prose vs. proof
> `apply` reads in English as: "to prove the goal, it suffices to prove ___". Write the paper proof first, then each "it suffices to prove" becomes an `apply`.

---

## The Seven Lemmas

### q1 — Reflexivity

$$A \rightarrow A$$

```coq
Parameter A: Prop.
Lemma q1 : A -> A.
Proof.
  intros.
  exact H.
Qed.
```

`intros` assumes `A` as `H`. Goal is now `A`, which is literally `H`, so `exact H` closes it. This is the identity/assumption rule.

---

### q2 — Weakening (ignore a hypothesis)

$$A \rightarrow (B \rightarrow A)$$

```coq
Parameter A B: Prop.
Lemma q2: A->(B->A).
Proof.
  intro.
  intros.
  exact H.
Qed.
```

Assume `A` (→ `H`), assume `B` (→ `H0`), then return `H`. Note `H0 : B` is **never used** — logic lets you ignore anything you were given.

---

### q3 — Feed two premises into one function

$$(A \to B \to C) \to B \to A \to C$$

```coq
Parameter A B C: Prop.
Lemma q3: (A->B->C)->B->A->C.
Proof.
  intro.
  intro.
  intro.
  apply H.
  - apply H1.
  - apply H0.
Qed.
```

After three `intro`s: `H : A→B→C`, `H0 : B`, `H1 : A`, goal `C`.

`apply H` needs `A` first, then `B` — so it emits **two subgoals in that order**, closed with bullets:

| Bullet | Goal | Closed by | Why |
|---|---|---|---|
| `-` | `A` | `apply H1` | `H1 : A` |
| `-` | `B` | `apply H0` | `H0 : B` |

> [!warning] Subgoal order
> The bullets follow the **order of the premises in the hypothesis**, left to right — *not* the order you introduced them. Here `H1 : A` comes first because `H : A→B→C` lists `A` first, even though `H0` (from `B`) was created before `H1`.

---

### q4 — Use the same hypothesis twice

$$(A \to A \to B) \to A \to B$$

```coq
Parameter A B : Prop.
Lemma q4: (A->A->B)->A->B.
Proof.
  intros.
  apply H.
  - apply H0.
  - apply H0.
Qed.
```

`H` needs `A` twice. Both subgoals are discharged by the *same* `H0 : A` — hypotheses can be reused any number of times (structural logic / no linear resources here).

---

### q5 — A redundant premise (weakening)

$$(A \to B) \to A \to A \to B$$

```coq
Parameter A B: Prop.

Lemma q5: (A->B)->A->A->B.
Proof.
  intros.
  apply H.
  apply H0.
Qed.
```

The third argument `A` is **completely unnecessary** — this proves `(A→B)→A→B` and just carries an extra `A` along for free. Proof is a single `apply H` → goal `A`, discharged by `apply H0`.

Useful reminder: lemmas can be *stronger than needed*; a proof only has to use what it needs.

---

### q6 — A chain of implications

$$(A \to B) \to (A \to C) \to (B \to C \to D) \to A \to D$$

```coq
Parameter A B C D: Prop.

Lemma q6: (A->B)->(A->C)->(B->C->D)->A->D.
Proof.
  intros.
  apply H1.
  - apply H. apply H2.
  - apply H0. apply H2.
Qed.
```

Hypotheses after `intros`: `H : A→B`, `H0 : A→C`, `H1 : B→C→D`, `H2 : A`, goal `D`.

- `apply H1` → need `B` and `C`.
- `B` comes from `H2` through `H`; `C` comes from `H2` through `H0`.
- `H2 : A` is the **single source** feeding all three branches — the "diamond" shape of the proof.

Tactics can be put on one line (`. ` is a separator) when a chain is obvious: `apply H. apply H2.`

---

### q7 — The tricky one

$$((((A \to B) \to A) \to A) \to B) \to B$$

```coq
Parameter A B: Prop.
Lemma q7: ((((A->B)->A)->A)->B)->B.
Proof.
  intros.
  apply H.
  intros.
  apply H0.
  intros.
  apply H.
  intro.
  apply H1.
Qed.
```

Trace it (hypotheses auto-name `H`, `H0`, `H1`, …):

| Tactic | New goal | Why |
|---|---|---|
| `intros` | goal `B`, `H : (((A→B)→A)→A)→B` | outermost assumption |
| `apply H` | `((A→B)→A)→A` | to get `B` I need `A`'s wrapper |
| `intros` | goal `A`, `H0 : (A→B)→A` | |
| `apply H0` | `A→B` | to get `A` I need `A→B` |
| `intros` | goal `B`, `H1 : A` | assume `A` |
| `apply H` | `((A→B)→A)→A` | reuse the **original** `H` |
| `intro` | goal `A`, `H2 : A→B` | assume `A→B` |
| `apply H1` | `A` ✅ | `H1 : A` matches |

Two things make this one hard:

1. **`H` is reused** — the outer hypothesis is used twice (steps 1 and 6), not just consumed once.
2. **The nesting is deep**, so you must count parens carefully when reading the goal.

---

## Summary Table

| # | Lemma | Key idea | Tactics used |
|---|---|---|---|
| q1 | `A → A` | identity | `intros`, `exact` |
| q2 | `A → (B → A)` | ignore `B` | `intro`/`intros`, `exact` |
| q3 | `(A→B→C) → B → A → C` | two premises, bullet order | `intro`×3, `apply`, `-` |
| q4 | `(A→A→B) → A → B` | reuse a hypothesis | `intros`, `apply`, `-`×2 |
| q5 | `(A→B) → A → A → B` | redundant premise | `intros`, `apply` |
| q6 | 4-premise chain | one source feeds all | `intros`, `apply` + one-liners |
| q7 | deeply nested | reuse `H` twice | `intros`, `apply`, `intro` |

---

## Checklist & Gotchas

- [x] Every script starts with `Parameter ... : Prop.` so the propositions are arbitrary
- [x] Every script ends with `Qed.`
- [x] All seven lemmas proved — `q1.v` … `q7.v` → concatenated into `25251621.txt`
- [x] Demonstrator shown for grading

> [!warning] Common mistakes
> - **Bullet order ≠ introduction order.** Bullets follow the premises as written in the hypothesis (see q3).
> - **Forgetting a bullet.** If `apply` creates 2+ subgoals, you must close them all with `-` (or finish each inline like q6).
> - **`exact` vs `apply`.** `exact H` needs the goal to match `H` *exactly*; `apply H` matches the goal against `H`'s *conclusion* and replaces it with `H`'s premises.
> - **Unused hypotheses are fine.** q2 and q5 prove it — logic is not linear.

> [!tip] Verify locally
> Load the file in Rocq (Coq) and inspect the generated proof term:
> ```coq
> Print q1.
> Print q7.
> ```
> Useful for seeing that the proof script really is a term of the stated type.

---

## Related

- [[2026-10-01 - Lab 1 Logic & Propositional Translation]] — Exercises A & B (English → logic)
- [[2026-09-28 - Natural Deduction]] — the underlying rules these tactics implement

---

> [!tip] Next lecture
> Fill in the `next` field in frontmatter once the next notes arrive.
