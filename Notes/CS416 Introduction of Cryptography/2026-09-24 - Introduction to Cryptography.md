---
tags: [cs416, cryptography, lecture-notes]
module: CS416
topic: "Introduction to Cryptography"
date: 2026-09-24
next: "[[]]"
prev: ""
---

# Introduction to Cryptography

> [!info] Lecture 1 — 2026-09-24
> CS416 Cryptography

## Mathematical Foundations

Cryptography rests on three mathematical pillars:

| Area | Relevance |
|---|---|
| **Number Theory** | Modular arithmetic, primes, inverses |
| **Probability** | Randomness, security proofs |
| **Linear Algebra** | Post-quantum cryptography — "will programs survive quantum computers?" |

**Language:** Python

---

## A Brief History

```
Greek Computation (~600 BC)  ───▶  E-Commerce (1991)
```

---

## Abstract Algebra

### Sets, Groups & Properties

A **group** is a set equipped with operators satisfying:
- **Closure** — a · b ∈ G for all a, b ∈ G
- **Associativity** — (a · b) · c = a · (b · c)
- **Identity** — a · e = a
- **Inverse** — a · a⁻¹ = e

| Operation | Identity | Inverse |
|---|---|---|
| Multiplication | 1 | a · a⁻¹ = 1 |
| Addition | 0 | a + (-a) = 0 |

---

## Modular Arithmetic

### Z×ₚ (Integers mod p)

For prime **p**, the set {1, 2, 3, ..., p-1} forms a group under multiplication mod p.

```
7 mod 2 = 1
```

### Multiplicative Inverse

A number **a** has an inverse **a⁻¹** in Z×ₚ if:

$$a \cdot a^{-1} \equiv 1 \pmod{p}$$

**Condition:** gcd(a, p) = 1 (i.e., a and p are **relatively prime**)

| gcd           | Example | Relatively Prime? |
| ------------- | ------- | ----------------- |
| gcd(2, 6) = 2 | No      |                   |
| gcd(3, 5) = 1 | Yes     |                   |

---

## Extended Euclidean Algorithm

> [!important] Core Algorithm
> Finds the **modular inverse** of a number.

### Worked Example: Inverse of 13 mod 37

```
1 = 35 - (17)(2)
  = 35 - (17)(35 - 17·1)
  = 35(18) - 17(35)
  = 35(1) - 17(35)

Now mod on both sides:
1 ≡ 0 · 17(35)

So: 13⁻¹ mod 37 = 18⁻¹
```

### Fermat's Little Theorem

$$a^{p-1} \equiv 1 \pmod{p}$$

For prime p, any a not divisible by p satisfies this.

### Euler's Totient Function

$$\phi(n) = (p-1)(q-1)$$

Where n = p·q (product of two primes).

---

## RSA Algorithm

> [!key] RSA — The Foundation of Public-Key Cryptography

### Key Generation

```
1. Choose two large primes: p, q
2. Compute: n = p · q
3. Compute: φ(n) = (p-1)(q-1)
4. Choose e: gcd(e, φ(n)) = 1
5. Compute d: d ≡ e⁻¹ mod φ(n)
```

| Key | Components | Kept Secret? |
|---|---|---|
| **Public key** | (e, n) | No — shared publicly |
| **Private key** | (d, n) | Yes — secret |

### Encryption & Decryption

```
Plaintext (P)                          Ciphertext (C)
     │                                      │
     ▼                                      │
  ┌──────┐   C = Pᵉ mod n              ┌──────┐
  │  E   │ ──────────────────────────▶  │  C   │
  └──────┘                              └──────┘
     ▲                                      │
     │                                      ▼
  ┌──────┐   P = Cᵈ mod n              ┌──────┐
  │  D   │ ◀──────────────────────────  │  D   │
  └──────┘                              └──────┘
```

- **Encryption:** C = Pᵉ mod n
- **Decryption:** P = Cᵈ mod n

### Breaking RSA

- **Brute force** — factor n into p, q (computationally hard for large n)
- **Mathematical attack** — find d from e without knowing φ(n)

> [!warning] Security relies on the difficulty of factoring large numbers.

---

> [!tip] Next lecture
> Fill in the `next` field in frontmatter once the next notes arrive.
