---
tags: [cs357, lab, coq, rocq, proofs, lecture-notes]
module: CS357
topic: "Lab 2 — Rocq: Conjunction, Disjunction & Negation"
date: 2026-10-21
next: "[[]]"
prev: "[[2026-10-07 - Lab 1 Rocq Proofs]]"
---

# Lab 2 — Rocq: Conjunction, Disjunction & Negation

> [!info] CS357 Lab 2 (Rocq) — 2026-10-21
> Proving lemmas built from **∧**, **∨** and **¬** in Rocq (Coq), using the introduction and elimination rules for conjunction and disjunction.
> Lab page: <https://classicwuhao.github.io/rocq/lab2.html>
> Companion script: `lab2_rocq.v` (same folder)

Lab 1 only ever used `intro` and `apply` on **implications**. This lab adds the tactics that come with the other connectives:

| Connective | Introduction rule | Elimination rule |
|---|---|---|
| $A \land B$ | `split` — goal becomes two subgoals $A$ and $B$ | `destruct H` / `elim H` — turns hypothesis $H : A \land B$ into **two** hypotheses |
| $A \lor B$ | `left` / `right` — goal becomes $A$ (resp. $B$) | `destruct H` / `elim H` — turns hypothesis $H : A \lor B$ into **two subgoals** |
| $\neg A$ | `red` — goal becomes $A \to \bot$ | `intro` — assumes $A$, goal becomes $\bot$ |

---

## The Tactic Toolbox

| Tactic | Applies to | What it does |
|---|---|---|
| `intro` | goal $A \to B$ | assume $A$ as a hypothesis, goal becomes $B$ |
| `intros` | any number of arrows | introduce everything at once (auto-names `H`, `H0`, `H1`, …) |
| `apply H` | hypothesis $H : A \to B$ | goal $B$ becomes goal $A$ (uses $H$'s conclusion) |
| `exact H` | hypothesis $H : A$ | closes a goal that is literally $A$ |
| `split` | goal $A \land B$ | goal becomes **two** subgoals: $A$, $B$ |
| `left` | goal $A \lor B$ | goal becomes $A$ |
| `right` | goal $A \lor B$ | goal becomes $B$ |
| `destruct H` | hypothesis of an **inductive** type (∧, ∨, False, ∃, ℕ, …) | case analysis: one branch per constructor |
| `elim H` | same | the elimination-rule form; `elim H` + `intros` ≡ `destruct H as [H0 H1]` |
| `red` | goal $\neg A$ | "reduce": unfolds $\neg$ into its constructive definition $A \to \bot$ |
| `contradiction` | context containing $\bot$ (or $A$ together with $\neg A$) | closes the goal |
| `exfalso` | any goal | changes the goal to $\bot$ (ex falso quodlibet) |

> [!note] `destruct` = elimination
> `destruct` takes a term whose type is an **inductive type** (a conjunction, disjunction, `False`, an existential, a natural number, …) and does case analysis on it, splitting according to the constructors of its type. In logic terms it *is* the elimination rule for that connective.
>
> The difference between the two shapes of hypothesis:
> - **Conjunction** $H : A \land B$ → `destruct H` creates **two new hypotheses** ($H_0 : A$, $H_1 : B$).
> - **Disjunction** $H : A \lor B$ → `destruct H` creates **two new subgoals**, each with $H$ replaced by one of $A$ or $B$.

---

## The Lecture Example

$$\texttt{Lemma example: } A \land B \to B \land A$$

```coq
Parameter A B : Prop.
Lemma example : A /\ B -> B /\ A.
Proof.
  intro H.
  destruct H as [H0 H1].
  split.
  exact H1.
  exact H0.
Qed.
```

| Step | Tactic | Goal after | Hypotheses |
|---|---|---|---|
| 0 | — | $A \land B \to B \land A$ | — |
| 1 | `intro H` | $B \land A$ | `H : A ∧ B` |
| 2 | `destruct H as [H0 H1]` | $B \land A$ | `H0 : A`, `H1 : B` |
| 3 | `split` | $B$, $A$ | `H0 : A`, `H1 : B` |
| 4 | `exact H1` | $A$ | ✓ closes first subgoal |
| 5 | `exact H0` | ✅ closed | ✓ |

The `elim` spelling is equivalent:

```coq
Proof.
  intro H.
  elim H.
  intros.
  split.
  exact H1.
  exact H0.
Qed.
```

`elim H` + `intros` ≡ `destruct H as [H0 H1]` — `elim` does the case analysis, `intros` then introduces the components of the conjunctive hypothesis (which is where the auto-names `H0`/`H1` come from).

---

## Part 1 — Conjunction & Disjunction

### q1 — Associativity of ∧

$$((A \land B) \land C) \to (A \land (B \land C))$$

```coq
Parameter A B C : Prop.
Lemma q1: ((A /\ B) /\ C) -> (A /\ (B /\ C)).
Proof.
  intros H.
  destruct H as [[H0 H1] H2].
  split.
  - exact H0.
  - split.
    + exact H1.
    + exact H2.
Qed.
```

Note the **nested** destruct pattern `as [[H0 H1] H2]`: the outer conjunction `(A ∧ B) ∧ C` is destroyed first, giving the inner pair `(A ∧ B)` and the lone `C`; then the inner pair is destroyed too, giving `H0 : A`, `H1 : B`.

> [!tip] `destruct H as [...]` vs. two `destruct`s
> The pattern form is just shorthand: `destruct H as [[H0 H1] H2]` ≡ `destruct H as [H01 H2]. destruct H01 as [H0 H1].`

---

### q2 — Curry-Howard for ∧

$$((A \land B) \to C) \to (A \to (B \to C))$$

```coq
Lemma q2: ((A /\ B) -> C) -> (A -> (B -> C)).
Proof.
  intros H HA HB.
  apply H.
  split.
  - exact HA.
  - exact HB.
Qed.
```

Reading it backwards (this is the point of Curry–Howard): a function that consumes a **pair** `(A, B)` is used by handing it a pair. `apply H` demands `A ∧ B`; `split` builds that pair from `HA : A` and `HB : B`.

| Step | Tactic | Goal after | Hypotheses |
|---|---|---|---|
| 1 | `intros H HA HB` | $C$ | `H : A∧B→C`, `HA : A`, `HB : B` |
| 2 | `apply H` | $A \land B$ | ↑ |
| 3 | `split` | $A$, $B$ | ↑ |
| 4 | `exact HA` | $B$ | ✓ |
| 5 | `exact HB` | ✅ closed | ✓ |

---

### q3 — Associativity of ∨

$$((A \lor B) \lor C) \to (A \lor (B \lor C))$$

```coq
Lemma q3: ((A \/ B) \/ C) -> (A \/ (B \/ C)).
Proof.
  intros H.
  destruct H as [H0 | H2].
  - destruct H0 as [HA | HB].
    + left. exact HA.
    + right. left. exact HB.
  - right. right. exact H2.
Qed.
```

This is the shape to watch: `destruct` on a **disjunction** hypothesis produces **two subgoals**, so the proof body is nested:

```
destruct H as [H0 | H2].        -- 2 branches
  branch 1 (H0 : A \/ B):  destruct H0 as [HA | HB].   -- 2 more branches
      HA : A   ->  left.  exact HA.
      HB : B   ->  right. left. exact HB.
  branch 2 (H2 : C):  right. right. exact H2.
```

> [!note] `right` twice for right-nesting
> The target is $A \lor (B \lor C)$, so the *outer* `∨` is on the right → `right`, and then the inner $B \lor C$ also goes on the right → `right` again. Two `right`s, then the payload.

---

### q4 — Elimination through a disjunction

$$((A \lor B) \to C) \to (A \to (B \to C))$$

```coq
Lemma q4: ((A \/ B) -> C) -> (A -> (B -> C)).
Proof.
  intros H HA HB.
  apply H.
  left. exact HA.
Qed.
```

`apply H` demands $A \lor B$; the **introduction** rule for ∨ (`left`) discharges it using `HA : A`. `HB : B` is never used — legal, and a direct echo of Lab 1's q2/q5 (weakening: extra hypotheses may be ignored).

---

## Part 2 — Negation

### The two ways to handle $\neg$

Rocq's logic is **constructive**, so $\neg A$ is *defined* as $A \to \bot$:

$$\neg A \;\equiv\; A \to \bot$$

> [!tip] `red` = "reduce"
> Whenever the goal is a negation, `red` replaces it with its constructive definition, so that after `intros` you get **a new assumption** and a goal of **`False`**.
>
> ```coq
> Goal ~A.   red.   intros.   -- assumption: A,  goal: False
> ```
>
> In practice `intro`/`intros` already performs this unfolding for you, so `red` is mostly there to make the move **explicit** in the script.

### q5 — Cases of a disjunction with a negation

$$(\neg A \lor B) \to (A \to B)$$

```coq
Lemma q5: (~A \/ B) -> (A -> B).
Proof.
  intros H HA.
  destruct H as [H0 | H1].
  - exfalso. apply H0. exact HA.
  - exact H1.
Qed.
```

| Branch | Hypothesis | Goal $B$ | How it closes |
|---|---|---|---|
| 1 | `H0 : ¬A` | `$B$` | `exfalso` → goal `False`; `apply H0` → goal `A`; `exact HA` ✅ |
| 2 | `H1 : B` | `$B$` | `exact H1` ✅ |

Branch 1 is a genuine contradiction: we assumed $A$ and also have $\neg A$, so $\bot$ follows and $\bot$ eliminates anything (`exfalso`).

> [!tip] `contradiction`
> When the context already contains a contradiction, the `contradiction` tactic closes the goal on its own — so branch 1 could also be written as `contradiction.` instead of `exfalso. apply H0. exact HA.`

---

### q6 — Contrapositive

$$(A \to B) \to (\neg B \to \neg A)$$

```coq
Lemma q6: (A -> B) -> (~B -> ~A).
Proof.
  intros H HB.
  red. intro HA.
  apply HB. apply H. exact HA.
Qed.
```

| Step | Tactic | Goal after | Hypotheses |
|---|---|---|---|
| 1 | `intros H HB` | $\neg A$ | `H : A→B`, `HB : ¬B` |
| 2 | `red` | $A \to \bot$ | ↑ |
| 3 | `intro HA` | $\bot$ | `HA : A` |
| 4 | `apply HB` | $B$ | ✓ goal $\bot$ reduces to needing $B$ |
| 5 | `apply H` | $A$ | ✓ goal $B$ reduces to needing $A$ |
| 6 | `exact HA` | ✅ closed | ✓ |

The chain reads: *assume $A$; then $B$ holds (by `H`); but $\neg B$ was assumed — contradiction.* This is the classical contrapositive, and it is fully constructive.

---

### q7 — No contradiction from a conjunction

$$\neg(A \land \neg A)$$

```coq
Lemma q7: ~(A /\ ~A).
Proof.
  red. intros H.
  destruct H as [H0 H1].
  apply H1. exact H0.
Qed.
```

`red` turns the goal into $(A \land \neg A) \to \bot$; `intros H` assumes the pair; `destruct H` splits it into `H0 : A` and `H1 : ¬A`; then `apply H1` demands an `A` and `exact H0` supplies it → $\bot$.

> [!warning] The point of the lemma
> $A \land \neg A$ is unsatisfiable, so $\neg(A \land \neg A)$ holds. Note this is **not** LEM: it says nothing about whether $A$ or $\neg A$ holds, only that they cannot both hold.

---

## Part 3 — LEM and the De Morgan Laws

### Law of the Excluded Middle (LEM)

$$\text{LEM}: \forall P : \text{Prop},\; P \lor \neg P$$

Rocq is constructive, so LEM is **not** available for free — it is an extra assumption you must declare explicitly:

```coq
Axiom LEM: forall P: Prop, P \/ ~P.        -- global, applies to every file
Hypothesis LEM: forall P: Prop, P \/ ~P.   -- local to the current section/lemma
```

> [!warning] `Axiom` vs `Hypothesis`
> - `Hypothesis LEM` introduces the assumption **as a hypothesis** — the lemma is proved *from* it, and it stays in the context.
> - `Axiom LEM` declares LEM as a **global axiom** of the development. It is consistent with Rocq's core (Rocq simply does not know whether it is inhabited), but anything you prove with it is only "proved" *relative to* LEM, and you can no longer claim the result is constructive.
>
> For a graded lab, `Hypothesis LEM` is the honest and least invasive choice — exactly what the lab sheet suggests.

Once LEM is available you can always reason by case analysis:

```coq
destruct (LEM E) as [HE | HE].   -- splits the proof into the case E and the case ¬E
```

---

### q8 — ¬ distributes over ∨ (constructive)

$$\neg(E \lor F) \to (\neg E \land \neg F)$$

```coq
Parameter E F : Prop.
Hypothesis LEM: forall P: Prop, P \/ ~P.

Lemma q8: ~(E \/ F) -> (~E /\ ~F).
Proof.
  intros H.
  split.
  - intro HE. apply H. left. exact HE.
  - intro HF. apply H. right. exact HF.
Qed.
```

No LEM needed here: the introduction rule for ∧ (`split`) gives two goals $\neg E$ and $\neg F$; each is closed by assuming the negation and using `H` on the matching side of the disjunction.

---

### q9 — ¬ of a ∨ (constructive)

$$(\neg E \land \neg F) \to \neg(E \lor F)$$

```coq
Lemma q9: (~E /\ ~F) -> ~(E \/ F).
Proof.
  intros H.
  destruct H as [HE HF].
  intros H0.
  destruct H0 as [HE0 | HF0].
  - apply HE. exact HE0.
  - apply HF. exact HF0.
Qed.
```

Case analysis on the *disjunction* in the goal's premise: either $E$ (contradicts `HE`) or $F$ (contradicts `HF`).

---

### q10 — ∨ of negations implies ¬ of conjunction (constructive)

$$(\neg E \lor \neg F) \to \neg(E \land F)$$

```coq
Lemma q10: (~E \/ ~F) -> ~(E /\ F).
Proof.
  intros H.
  destruct H as [HE | HF].
  - intros H0. destruct H0 as [HE0 HF0]. apply HE. exact HE0.
  - intros H0. destruct H0 as [HE0 HF0]. apply HF. exact HF0.
Qed.
```

Here `destruct` on the disjunction gives **two subgoals** (each keeping the goal $\neg(E \land F)$); in each branch we assume the pair and pull the contradiction out of the relevant component.

---

### q11 — The one that needs LEM

$$\neg(E \land F) \to (\neg E \lor \neg F)$$

```coq
Lemma q11: ~(E /\ F) -> (~E \/ ~F).
Proof.
  intros H.
  destruct (LEM E) as [HE | HE].
  - right. intro HF. apply H. split. exact HE. exact HF.
  - left. exact HE.
Qed.
```

**This is the lemma the lab sheet warns about.** Its proof needs to produce a *disjunction* $\neg E \lor \neg F$, but intuitionistically there is no way to decide *which* of the two negations holds from $\neg(E \land F)$ alone. So we lean on LEM to split into the two cases:

| Case | From LEM | Then |
|---|---|---|
| 1 | `HE : E` | we must show $\neg F$; assume `HF : F` and contradict `H : ¬(E ∧ F)` by exhibiting `E ∧ F` |
| 2 | `HE : ¬E` | `left. exact HE.` ✅ |

| Step | Tactic | Goal after | Hypotheses |
|---|---|---|---|
| 1 | `intros H` | $\neg E \lor \neg F$ | `H : ¬(E∧F)` |
| 2 | `destruct (LEM E) as [HE\|HE]` | two subgoals | branch 1: `HE : E`; branch 2: `HE : ¬E` |
| 3a | `right. intro HF.` | $\bot$ | `HF : F` |
| 4a | `apply H. split.` | $E$, $F$ | ✓ goal $\bot$ reduces to needing `E ∧ F` |
| 5a | `exact HE. exact HF.` | ✅ | ✓ |
| 3b | `left. exact HE.` | ✅ | ✓ |

> [!warning] Not constructively provable
> q11 is classically valid but has **no** intuitionistic proof. This is the crisp demonstration that Rocq's default logic is constructive: if you try to prove q11 without LEM you will stall. (Formally, q11 for all $E, F$ is equivalent to LEM up to the usual double-negation bookkeeping.)

---

## Summary Table

| # | Lemma | Shape | Tactic used | LEM needed? |
|---|---|---|---|---|
| q1 | $((A \land B) \land C) \to (A \land (B \land C))$ | associativity of ∧ | `destruct H as [[H0 H1] H2]`, `split` | no |
| q2 | $((A \land B) \to C) \to (A \to (B \to C))$ | pair as argument | `apply H`, `split` | no |
| q3 | $((A \lor B) \lor C) \to (A \lor (B \lor C))$ | associativity of ∨ | nested `destruct`, `left`/`right` | no |
| q4 | $((A \lor B) \to C) \to (A \to (B \to C))$ | introduction of ∨ | `apply H`, `left` | no |
| q5 | $(\neg A \lor B) \to (A \to B)$ | cases with a contradiction | `destruct`, `exfalso` | no |
| q6 | $(A \to B) \to (\neg B \to \neg A)$ | contrapositive | `red`, `intro`, `apply` | no |
| q7 | $\neg(A \land \neg A)$ | no self-contradiction | `red`, `destruct`, `apply` | no |
| q8 | $\neg(E \lor F) \to (\neg E \land \neg F)$ | De Morgan (∨ side) | `split`, `intro` | no |
| q9 | $(\neg E \land \neg F) \to \neg(E \lor F)$ | De Morgan (∨ side, reverse) | `destruct` | no |
| q10 | $(\neg E \lor \neg F) \to \neg(E \land F)$ | De Morgan (∧ side) | `destruct` on ∨ | no |
| q11 | $\neg(E \land F) \to (\neg E \lor \neg F)$ | De Morgan (∧ side, reverse) | `destruct (LEM E)` | **yes** |

---

## The De Morgan Picture

```
¬(E ∨ F)  ↔  ¬E ∧ ¬F        (both directions constructive — q8, q9)
¬(E ∧ F)  ↔  ¬E ∨ ¬F        (¬E ∨ ¬F → ¬(E∧F) constructive — q10)
                             (¬(E∧F) → ¬E ∨ ¬F  needs LEM — q11)
```

```
        ¬(E ∨ F)                    ¬(E ∧ F)
       ─────────                    ─────────
       proof: q8  ◄──── constructive ────►  proof: q10
       proof: q9  ◄──── constructive ────►  proof: q11
                                               (needs LEM)
```

---

## Gotchas

- [ ] **`split` creates *two* goals.** If you `split` and then only close one, Rocq reports a remaining goal.
- [ ] **`destruct` on a conjunction → hypotheses; on a disjunction → *subgoals*.** This asymmetry is the single most common source of confusion (and of bullet-count errors).
- [ ] **Bullet nesting must match the case tree.** q3 has *three* leaves (two from the inner `destruct`, one from the outer), so it needs `- / +` and `-` at the right depths.
- [ ] **`red` only fires when the negation is at the head of the goal.** In q6 you must `intro HB` *first*, then `red` the remaining `¬A`. A `red` before that does nothing.
- [ ] **Unused hypotheses are fine.** q4 never uses `HB`.
- [ ] **`left`/`right` are *introduction* rules; `destruct` is the *elimination* rule.** If the disjunction is in the *goal*, use `left`/`right`; if it is in a *hypothesis*, use `destruct`.
- [ ] **`destruct (LEM E)` yields two goals, not two hypotheses** — the second branch carries `¬E`, the first carries `E`.

> [!tip] Verify locally
> ```coq
> Print q11.       -- inspect the generated proof term
> ```
> With LEM as an `Axiom`, `Print q11` will show `q11` depending on `LEM` — a good visual reminder that the proof is only as strong as your assumptions.

---

## Grading (per the lab sheet)

- [x] Show the proof scripts to the demonstrators.
- [x] Submit the `.v` file on Moodle before leaving the lab.

---

## Related

- [[2026-10-07 - Lab 1 Rocq Proofs]] — `intro` / `apply` on implications
- [[2026-10-01 - Lab 1 Logic & Propositional Translation]] — English → propositional/predicate logic
- [[2026-09-28 - Natural Deduction]] — the inference rules these tactics implement

---

> [!tip] Next lecture
> Fill in the `next` field in frontmatter once the next notes arrive.
