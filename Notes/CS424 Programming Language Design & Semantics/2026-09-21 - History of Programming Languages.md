---
tags: [cs424, programming-languages, semantics, lecture-notes]
module: CS424
topic: "History of Programming Languages & FORTRAN"
date: 2026-09-21
next: "[[]]"
prev: ""
---

# History of Programming Languages & FORTRAN

> [!info] Lecture 1 — 2026-09-21
> CS424 Programming Language Design & Semantics

## What Makes a Good Language?

The role of three factors in language design:

1. **Motivating applications** — what problems does the language solve?
2. **Program execution** — how is code compiled/interpreted?
3. **Theoretical foundations** — type systems, formal semantics

Also covered: **Language standardization**

> [!note] Reference
> [History of Programming Languages — Wikipedia](https://en.wikipedia.org/wiki/History_of_programming_languages)

---

## FORTRAN — FORmula TRANslator (1957)

### Timeline

| Version | Year | Key Change |
|---|---|---|
| FORTRAN I | 1957 | First high-level language |
| FORTRAN 66 | 1966 | Standardized; `GOTO`, `DO` loops |
| FORTRAN 77 | 1977 | Modern control structures (`if-then-else`) |
| FORTRAN 2008 | 2008 | Concurrency support |

### Why FORTRAN Still Matters

- Remains the main language for **scientific computing**
- Easier for a compiler to optimize than C

### FORTRAN Features

- **Main + subprograms** — each compiled separately
- **Static storage allocation** — no stack, no recursion
- **Memory** — arranged as linear array

### Key Constructs

| FORTRAN 66 | FORTRAN 77 | FORTRAN 2008 |
|---|---|---|
| `GOTO` statement | `if-then-else` blocks | Concurrency support |
| `DO` loops | | |

---

## FORTRAN Code Example

```fortran
PROGRAM MAIN
    PARAMETER (MAXSIZ=99)
    REAL A(MAXSIZ)
    READ (5, 100, END=999) K
    FORMAT(I5)
    IF ((K.LE.0) .OR. (K.GT.MAXSIZ)) STOP
    READ *, (A(I), I=1, K)
    PRINT *, (A(I), I=1, K)
    PRINT *, 'SUM=', SUM(A,K)
    GO TO 10
    PRINT *, "All Done"
    STOP
END

C SUMMATION SUBPROGRAM
    FUNCTION SUM(V,N)
        REAL V(N)
        SUM = 0.0
        DO 20 I = 1, N
            SUM = SUM + V(I)
        CONTINUE
        RETURN
    END
```

### Key Observations

- `FORMAT` for I/O specification
- `DO` loop with label-based iteration
- Subprograms compiled separately
- Static memory allocation

---

## Data Formats & Memory

### EQUIVALENCE & COMMON

```fortran
EQUIVALENCE
COMMON
```

- **EQUIVALENCE** — share memory between variables
- **COMMON** — shared memory blocks between subprograms

### Parameters

| Concept | Description |
|---|---|
| **Actual parameters** | Values passed to function calls |
| **Formal parameters** | Variables declared in function definition |

---

## LISP — Contributions & Syntax

### Key Features

| Feature | Description |
|---|---|
| **Prefix notation** | Operations written before operands |
| **Atoms & Cells** | Basic data building blocks |
| **Dynamically typed** | Types determined at runtime |
| **Boolean** | `T` (true), `NIL` (false) |

### LISP Code Example

```lisp
(defvar x 1)
(defun g(z) (+ x z))
(defun f(y)
    (+ (g y)
        (let
            ((x y))
            (g x)
        )
    )
)
(f (+ x 1))
```

### Key Observations

- Parenthesized prefix notation: `(+ x y)`
- `defvar` — define variable
- `defun` — define function
- `let` — local binding
- Dynamic scoping (default in early LISP)

---

## Scope & Binding

| Type | Description |
|---|---|
| **Static scope** | Variable bound at compile time (lexical) |
| **Dynamic scope** | Variable bound at runtime (call stack) |

> [!note]
> Modern languages use **static (lexical) scope** by default.
> LISP originally used **dynamic scope**, later added lexical scoping.

---

> [!tip] Next lecture
> Fill in the `next` field in frontmatter once the next notes arrive.
