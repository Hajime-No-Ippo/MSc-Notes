---
tags: [cs357, lab, logic, lecture-notes]
module: CS357
topic: "Lab 1 — Logic & Propositional Translation"
date: 2026-10-01
next: "[[]]"
prev: "[[2026-09-28 - Natural Deduction]]"
---

# Lab 1 — Logic & Propositional Translation

> [!info] CS357 Lab 1 — 2026-10-01
> Translating English statements into propositional and predicate logic.

---

## Exercise A — Propositional Logic

Translate each English statement using propositional variables and logical connectives.

### A1. Conditional with Conjunction

> "If the demand has remained constant and prices have been increased, then turnover must have decreased."

**Translation:**

| Variable | Meaning |
|---|---|
| $C$ | The demand has remained constant |
| $I$ | Prices have been increased |
| $T$ | Turnover has decreased |

$$\boxed{(C \land I) \rightarrow T}$$

> [!note] Structure
> "If P and Q, then R" → $(P \land Q) \rightarrow R$

---

### A2. Biconditional

> "The sum of two numbers is even if and only if either both numbers are even or both numbers are odd."

**Translation:**

| Variable | Meaning |
|---|---|
| $S$ | The sum of two numbers is even |
| $E$ | Both numbers are even |
| $O$ | Both numbers are odd |

$$\boxed{S \leftrightarrow (E \lor O)}$$

> [!note] Structure
> "P if and only if (Q or R)" → $P \leftrightarrow (Q \lor R)$

---

### A3. Nested Conditional

> "If $y$ is an integer then $z$ is not real, provided that $x$ is a rational number."

**Translation:**

| Variable | Meaning |
|---|---|
| $X$ | $x$ is a rational number |
| $Y$ | $y$ is an integer |
| $Z$ | $z$ is not real |

$$\boxed{X \rightarrow (Y \rightarrow Z)}$$

> [!note] Structure
> "Provided that P, if Q then R" → $P \rightarrow (Q \rightarrow R)$
> Note: $X$ is the **antecedent** (the condition that enables the implication).

---

## Exercise B — Predicate Logic (First-Order Logic)

Translate each English statement using predicates and quantifiers.

### B1. Universal — Every cat washes itself

$$\boxed{\forall x : \text{Cat}(x) \rightarrow \text{Washes}(x, x)}$$

> [!note] "Every P is Q" → $\forall x: P(x) \rightarrow Q(x)$

---

### B2. Universal — All dogs are mortal, Fido is mortal

> "If all dogs are mortal, Fido is mortal."

$$\boxed{(\forall x : \text{Dog}(x) \rightarrow \text{Mortal}(x)) \rightarrow \text{Mortal}(\text{Fido})}$$

> [!note] This is a **meta-level implication**: the universal statement implies a specific instance.

---

### B3. Negated Universal — Not every scorpion is lethal

$$\boxed{\neg (\forall x : \text{Scorpion}(x) \rightarrow \text{Lethal}(x))}$$

> [!tip] Equivalent forms:
> - $\neg \forall x: P(x) \rightarrow Q(x)$
> - $\exists x: P(x) \land \neg Q(x)$ (there exists a scorpion that is not lethal)

---

### B4. Universal with Negation — Every scorpion is non-lethal

$$\boxed{\forall x : \text{Scorpion}(x) \rightarrow \neg \text{Lethal}(x)}$$

> [!warning] Subtle difference from B3:
> - **B3**: "Not every scorpion is lethal" = some scorpions might not be lethal
> - **B4**: "Every scorpion is non-lethal" = no scorpion is lethal

---

### B5. Existential — At least one satellite orbits Mars

> [!warning] Correction
> The original answer used $\forall$, but "at least one" requires $\exists$.

$$\boxed{\exists x : \text{Satellite}(x) \land \text{Orbits}(x, \text{Mars})}$$

---

### B6. Existential with Conjunction — There is a planet larger than Neptune but cooler than it

$$\boxed{\exists x : \text{Planet}(x) \land \text{LargerThan}(x, \text{Neptune}) \land \text{CoolerThan}(x, \text{Neptune})}$$

---

### B7. Universal-Existential — Every village has at least one church

$$\boxed{\forall x : \text{Village}(x) \rightarrow \exists y : \text{Church}(y) \land \text{HasA}(x, y)}$$

> [!note] Structure
> "Every P has at least one Q" → $\forall x: P(x) \rightarrow \exists y: Q(y) \land R(x, y)$
> The quantifier order matters: $\forall x \exists y \neq \exists y \forall x$

---

## Summary Table

| # | English | Logic |
|---|---|---|
| A1 | If C and I then T | $(C \land I) \rightarrow T$ |
| A2 | S iff E or O | $S \leftrightarrow (E \lor O)$ |
| A3 | If Y then Z, provided X | $X \rightarrow (Y \rightarrow Z)$ |
| B1 | Every cat washes itself | $\forall x: \text{Cat}(x) \rightarrow \text{Washes}(x,x)$ |
| B2 | All dogs mortal → Fido mortal | $(\forall x: \text{Dog}(x) \rightarrow \text{Mortal}(x)) \rightarrow \text{Mortal}(\text{Fido})$ |
| B3 | Not every scorpion lethal | $\neg(\forall x: \text{Scorpion}(x) \rightarrow \text{Lethal}(x))$ |
| B4 | Every scorpion non-lethal | $\forall x: \text{Scorpion}(x) \rightarrow \neg\text{Lethal}(x)$ |
| B5 | At least one satellite orbits Mars | $\exists x: \text{Satellite}(x) \land \text{Orbits}(x,\text{Mars})$ |
| B6 | Planet > Neptune & cooler | $\exists x: \text{Planet}(x) \land \text{Larger}(x,\text{Neptune}) \land \text{Cooler}(x,\text{Neptune})$ |
| B7 | Every village has a church | $\forall x: \text{Village}(x) \rightarrow \exists y: \text{Church}(y) \land \text{HasA}(x,y)$ |

---

## Key Patterns

```
English                          → Logic
─────────────────────────────────────────────────
"Every P is Q"                   → ∀x: P(x) → Q(x)
"Some P is Q"                    → ∃x: P(x) ∧ Q(x)
"Not every P is Q"               → ¬∀x: P(x) → Q(x)
"No P is Q"                      → ∀x: P(x) → ¬Q(x)
"If P then Q"                    → P → Q
"P if and only if Q"             → P ↔ Q
"P and Q"                        → P ∧ Q
"P or Q"                         → P ∨ Q
"Not P"                          → ¬P
```
