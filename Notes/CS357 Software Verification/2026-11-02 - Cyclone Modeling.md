---
tags: [cs357, software-verification, cyclone, model-checking, lecture-notes]
module: CS357
topic: "Software Verification — Cyclone Modeling"
date: 2026-11-02
next: "[[]]"
prev: "[[2026-10-21 - Lab 2 Rocq - Conjunction, Disjunction & Negation]]"
---

# Software Verification — Cyclone Modeling

> [!info] Lecture — 2026-11-02
> CS357 Software Verification — Cyclone: Verifying Programs, Building Models
> Source: `CS357_Program_Verification.pdf`

## What is Cyclone?

Cyclone is a **model-checking** tool: you model a program as a **state machine (graph)**, then write **assertions** and **invariants** that Cyclone tries to satisfy or break.

Two core skills:

1. How to write **assertions** and **invariants**.
2. How to build an **appropriate model** for program verification.

---

## Data Types

Cyclone currently supports 6 data types:

| # | Type | Kind |
|---|---|---|
| 0 | `int` | primitive |
| 1 | `real` | primitive |
| 2 | `bool` | primitive |
| 3 | `enum` | special — a list of predefined constants |
| 4 | `record` | complex — an object |
| 5 | `BV` (bit-vector) | complex |

### int / real / bool

Same as Java's `int` / `float` / `boolean`.

```java
int x = 10;
real r = 1.20394;
bool b = true;
```

### enum

Predefines a list of constant values:

```java
enum {Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday} Days;
Days = #Saturday;
```

### record

A complex type; **only primitive and enum types are allowed** as fields.

```java
record Point {
    real x = 0;
    real y = 0;
    real z = 0;
};
Point.x = 1.0;
Point.y = 1.0;
Point.z = 1.0;
```

### Bit vector (bv)

Complex data structures can be encoded into bit vectors. Each has a **fixed size** and can be displayed as **binary**, **decimal**, or **hex-decimal**.

```java
bv[4]  map1 = 0b1111;   // binary
bv[8]  map2 = 0b10001;
bv[16] map3 = 0xffff;   // hex
```

---

## Constants

A constant is a predefined value that cannot change during computation.

> [!warning] Restriction
> A constant can currently only be applied to **primitive** data types.

```java
const real PI = 3.1415926;

// the following is ILLEGAL — records cannot be const
const record Point {
    real x;
    real y;
};
```

---

## Functions

```java
function name : return_type ([arg_name:type]*) {
    (expression)*
    return expression;
}
```

Rules:

- A function must be declared **before** nodes; it lives in the variable section.
- The name must be **unique**.
- It **must return** a value.
- It **cannot** be used with a `where` clause.
- It is **non-recursive**.
- It works over `int`, `bool`, `real` only (complex data unsupported).

```java
function add : int (x:int, y:int) {
    return x + y;
}

function increment : int (x:int) {
    return add(x, 1);
}
```

> [!note] Standard operators
> See the Cyclone tutorial: `https://classicwuhao.github.io/cyclone_tutorial/chapter3/tutorial-c3-2.html`

### The `one` function

Says **exactly one** condition in a list must hold. Return type is `bool`.

```java
one (x>0, x>1, x>2);                 // exactly one of these is true
one (x>0, one (y>0, y>x, y<z));      // can nest
one (x+y==0, y<0, y>=x);             // ILLEGAL expression
```

---

## Variables

In the current version, **all variables are graph scope** — visible to:

- every well-defined node and edge,
- `where` clauses,
- invariants,
- `assert` statements.

---

## Modeling with Graphs

A Cyclone spec is a `graph` with **nodes** (states) and **edges** (transitions).

```java
graph Example {
    int counter = 0;
    normal start final node S {
        counter++;
    }
    edge { S -> S }
    goal {
        assert (counter >= 3);
        check for 3
    }
}
```

- `normal` modifier is required when a node contains **computational instructions**.
- `start` = entry point; `final` = terminating state.
- `check for 3` = "find me a length-3 path" that makes `counter >= 3` → the path `S -> S -> S -> S` (counter = 4).

---

## Assertions

`assert` states the **properties** to be checked. It can only appear in the `goal` section. Cyclone compiles each assert into a set of **content conditions**; if a spec satisfies the properties, it finds a satisfying path.

Two optional operators:

- `always` — property holds **along the whole path** (EG in CTL).
- `some` — property holds **somewhere** along the path (EF in CTL).

And `in` restricts a property to a **subset of states**:

- `in (S)` — the property always holds **only in state S**.

### Four forms (property φ)

| Form | Meaning |
|---|---|
| `assert (φ);` | φ holds in the **last** state |
| `assert (φ) in (S);` | φ holds **only in S** |
| `assert some (φ);` | φ holds **sometime** |
| `assert always (φ);` | φ holds **at all times** |

```java
assert (light==#Green && gate==#Open);                    // last state
assert (light==#Green && gate==#Open) in (S);             // only in S
assert some (light==#Green && gate==#Open);               // sometime
assert always (light==#Green && gate==#Open);             // always
```

---

## Path & Content Conditions

Use **path conditions** (the route through the graph) together with **content conditions** (variable values) for powerful checks.

```java
goal {
    assert (c == 3);
    enumerate for 5 condition (D) reach (R, I, D)
}
```

- `enumerate for 5` → find **all** paths of length 5 that make `c == 3`.
- `condition (D)` → instruction D must be used **at least once** (path condition).
- `reach (R, I, D)` → restrict which nodes the path may pass through.

> [!tip] `check` vs `enumerate`
> `check` finds **one** satisfying path; `enumerate` finds **all** of them.

---

## Initial States

A **start state** is not the same as an **initial state**.

```
initial   start          final/terminating
 state    state                state
  R        S0      S1          S2
```

- **Initial state** — a state that happens *before* a start state.
- **Start state** — the entry point of the graph/state machine.
- **Final/terminating state** — where the user wants computation to stop.

To refer to a variable's value in its **initial state**, use the `initial` keyword:

```java
graph Example {
    int counter;
    normal start final node S { counter++; }
    edge { S -> S }
    goal {
        assert initial(counter) < 0;   // counter before entering S
        assert counter >= 2;           // counter in the FINAL state
        check for 3
    }
}
```

If **no initial value** is given, Cyclone picks an appropriate one to satisfy the goal:

```java
graph Example {
    int counter;                       // no initial value
    normal start final node S { counter++; }
    edge { S -> S }
    goal {
        assert counter >= 2;           // final state
        check for 3
    }
}
```

---

## Conditional Transitions & Non-determinism

A **conditional transition** only fires when its condition is true — use a `where` clause.

```java
edge { Select -> Coke where coin <= 3; }
edge { Select -> Beer }    // coin > 3 implied
```

### Non-determinism

Multiple conditional transitions can be simultaneously satisfied:

```
coin = 6,  transitions: coin>=3, coin>=4, coin>=5 → Coke, Beer, Coffee?
```

- With `check`, Cyclone picks the **first satisfied condition** — which one depends on the **compiler** (transitions stored in a **red-black tree**) and the **underlying solver**.
- With `enumerate`, **every** satisfied transition is selected, so all branches are covered.

```java
goal {
    enumerate for 1 reach (Coke, Beer, Coffee)
}
// 1. Select -> Coke
// 2. Select -> Beer
// 3. Select -> Coffee
```

> [!tip] Covering all transitions
> If you want to test/cover **every** satisfied transition, use `enumerate`.

---

## Invariants

A **(graph) invariant** specifies properties that must hold across **all transitions**.

- If a spec contains at least one invariant, Cyclone searches for a **counter-example** that breaks it.
- Use `in` to scope the invariant to a **subset of transitions**.

```java
normal state S {
    invariant Positive { x >= 0; }
    x = x - a;
    ...
    x = (y - x) * 2;
}
```

> [!warning] Timing
> An invariant must hold **for each transition** (i.e. after leaving a node/state). It **may not hold during** the computation inside the state — e.g. `x >= 0` holds *after* `x = (y-x)*2`, but may be false in between.

### Two forms (property φ = "gate open & light green")

```java
// everywhere
invariant Property {
    light == #Green &&
    gate  == #Open;
}

// only in RaiseGate transitions
invariant Property {
    light == #Green &&
    gate  == #Open;
} in (RaiseGate)
```

### Loop invariants vs Graph invariants

A **loop invariant** holds at the top of every iteration (between the precondition and postcondition); a **graph invariant** is the model-level analogue, holding after every transition.

---

## Verifying Programs

### A sequential program (swap)

```java
t = x;
x = y;
y = t;
```

- Precondition (γ): `x = A ∧ y = B`
- Postcondition (φ): `x = B ∧ y = A`

### An if-else

```java
a = x + 1;
if (a - 1 == 0) { y = 1; }
else            { y = a; }
```

- Precondition (γ): `true`
- Postcondition (φ): `y = x + 1`

### A loop

```java
i = 0;
z = 0;
while (i != y) {
    i = i + 1;
    z = z + x;
}
```

- Precondition (γ): `true`
- Postcondition (φ): `z = x * y`

---

## Summary

| Concept | Cyclone keyword |
|---|---|
| Model | `graph`, `node` (state), `edge` (transition) |
| Property to satisfy | `assert`, `assert some`, `assert always`, `in` |
| One/all satisfying paths | `check` / `enumerate` |
| Always-hold property | `invariant` (with optional `in`) |
| Pre-state value | `initial(...)` |
| Conditional transition | `edge ... where ...` |
| Exactly-one condition | `one(...)` |

> [!tip] Next lecture
> —
