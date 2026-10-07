---
tags: [cs416, cryptography, lecture-notes]
module: CS416
topic: "Affine Cipher, Digraphs & Zero-Knowledge Protocol"
date: 2026-10-07
next: "[[]]"
prev: "[[2026-09-28 - Number Theory & Classical Ciphers]]"
---

# Affine Cipher, Digraphs & Zero-Knowledge Protocol

> [!info] Lecture 3 — 2026-10-07
> CS416 Cryptography · Lecturer: Tom Dowling (tom.dowling@mu.ie)
> Source: `s1_3.pdf` (slides 130–169, Section 1)

---

## 0. Number Equivalents (Encoding)

> [!abstract] The number equivalent of a character
> A mapping from the alphabet in question to the integers.

| Encoding | Maps to |
|---|---|
| `A–Z` | `0–25` |
| `A–Z !"£$%^&*()0–9` | `0–44` |
| ASCII characters | ASCII values |
| `a–z` | `97–122` |

> [!note] Two steps, two different $n$
> **Encoding** takes characters → numbers. **Encryption** operates on those number equivalents. The alphabet size used for encoding and the $N$ used for encryption can be *different* — see [[#3. Encoding ≠ Encryption]].

---

## 1. Affine Cipher

An attempt to improve on the shift cipher. Uses **two keys**, $a$ and $b$.

### Encryption

Let $P$ be the number equivalent of a plaintext character, $n$ the alphabet size ($n = 26$ for A–Z only):

$$\boxed{E_{a,b}(P) = (a \cdot P + b) \bmod n} \qquad a, b \in [0, n-1]$$

### Example — $E_{3,11}(\text{HELLO}) = \text{GXSSB}$

| Letter | $P$ | $3P + 11$ | $\bmod 26$ | Cipher |
|---|---|---|---|---|
| H | 7 | 32 | 6 | **G** |
| E | 4 | 23 | 23 | **X** |
| L | 11 | 44 | 18 | **S** |
| L | 11 | 44 | 18 | **S** |
| O | 14 | 53 | 1 | **B** |

### Decryption

Must be able to compute the **inverse of a modulo $n$** (see Appendix A below):

$$P = D_{a,b}(E_{a,b}(P)) = \left(a^{-1} \cdot E_{a,b}(P) - a^{-1} \cdot b\right) \bmod n$$

### Example — $D_{3,11}(\text{GXSSB}) = \text{HELLO}$

| Step | Computation | Result |
|---|---|---|
| Take first cipher letter | G | 6 |
| Modular inverse | $3^{-1} \bmod 26$ | 9 |
| Multiply the offset | $a^{-1} \cdot b = 9 \cdot 11 = 99 \bmod 26$ | 21 |
| Decrypt | $9 \cdot 6 - 21 = 33 \bmod 26$ | 7 |
| Decode | 7 | **H** |

---

### Full Worked Example — Encrypt and Decrypt "VERIFY"

> [!example] The setup
> Plaintext: **VERIFY** · Keys: $a = 5$, $b = 8$ · Alphabet: $n = 26$ (A–Z → 0–25)
>
> Check the key is legal: $\gcd(5, 26) = 1$ ✓ (if $\gcd \neq 1$ there is no inverse and the cipher is not decryptable)

#### Step 1 — Encode: letters → numbers

| Letter | V | E | R | I | F | Y |
|---|---|---|---|---|---|---|
| Value | 21 | 4 | 17 | 8 | 5 | 24 |

#### Step 2 — Encrypt: $C = (a \cdot P + b) \bmod n$

| $P$ | $5P$ | $5P + 8$ | $\bmod 26$ | Letter |
|---|---|---|---|---|
| 21 | 105 | 113 | $113 - 104 = 9$ | **J** |
| 4 | 20 | 28 | $28 - 26 = 2$ | **C** |
| 17 | 85 | 93 | $93 - 78 = 15$ | **P** |
| 8 | 40 | 48 | $48 - 26 = 22$ | **W** |
| 5 | 25 | 33 | $33 - 26 = 7$ | **H** |
| 24 | 120 | 128 | $128 - 104 = 24$ | **Y** |

$$\boxed{E_{5,8}(\text{VERIFY}) = \textbf{JCPWHY}}$$

#### Step 3 — Recover the inverse $a^{-1} \bmod 26$ (Extended Euclid)

$$26 = (5)(5) + 1 \;\Longrightarrow\; 1 = 26 - 5 \times 5 \;\Longrightarrow\; -5 \times 5 \equiv 1 \pmod{26}$$

$$a^{-1} = -5 \bmod 26 = \mathbf{21} \qquad \textit{check: } 5 \times 21 = 105 = 4 \times 26 + 1 \equiv 1 \ ✓$$

Also precompute the constant: $a^{-1} \cdot b = 21 \times 8 = 168 \bmod 26 = \mathbf{12}$

#### Step 4 — Decrypt: $P = (a^{-1} \cdot C - a^{-1}b) \bmod n$

i.e. $P = (21 \cdot C - 12) \bmod 26$

| Cipher letter | $C$ | $21C$ | $21C - 12$ | $\bmod 26$ | Letter |
|---|---|---|---|---|---|
| J | 9 | 189 | 177 | $177 - 156 = 21$ | **V** |
| C | 2 | 42 | 30 | $30 - 26 = 4$ | **E** |
| P | 15 | 315 | 303 | $303 - 286 = 17$ | **R** |
| W | 22 | 462 | 450 | $450 - 442 = 8$ | **I** |
| H | 7 | 147 | 135 | $135 - 130 = 5$ | **F** |
| Y | 24 | 504 | 492 | $492 - 468 = 24$ | **Y** |

$$D_{5,8}(\text{JCPWHY}) = \textbf{VERIFY} \quad \checkmark$$

> [!tip] The mental shortcut
> Encrypt: multiply by $a$, add $b$, reduce mod 26.
> Decrypt: multiply by $a^{-1}$, subtract $a^{-1}b$, reduce mod 26.
> The *only* hard part is finding $a^{-1}$ — and that's just Appendix A.

---

### Key Space & Strength

| | |
|---|---|
| Nominal key space | $n^2$ (choices of $a$ × choices of $b$) |
| Real constraint | $a$ must satisfy $(a, n) = 1$, otherwise $a^{-1}$ doesn't exist |
| For $n = 26$ | $\varphi(26) = 12$ valid values of $a$, × 26 values of $b$ = **312** keys, vs $26^2 = 676$ |

> [!warning] Slides say "311 choices as opposed to 676"
> The correct count is $\varphi(26) \times 26 = 12 \times 26 = \mathbf{312}$. Treat the 311 on the slide as an off-by-one.

- **Still better than the shift cipher** (shift has only 25/26 usable keys)
- **But still mono-alphabetic** → vulnerable to frequency analysis

### Attacks

| Attack                           | Requirement         | Notes                                                                                                                                           |
| -------------------------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Brute force, ciphertext-only** | $n$, $a$, $b$       | Try values until the plaintext "makes sense". Easily programmed. Use $(a,n)=1$ to shorten the search. More graceful treatment in *Garrett* p37. |
| **Chosen plaintext**             | 2 chosen characters | Two chosen plaintext characters are enough to discover the keys — *Garrett* p14.                                                                |

---

## 2. Strengthening Affine: Digraphs

**Idea:** apply the affine transformation to *pairs* of characters instead of single characters.

- Take characters in groups of two → alphabet size grows to $n^2$
- Key space consequently grows to approximately $n^4$
- Can extend upwards (but there are limitations and cribs…)

### Constructing digraphs

The 1–1 encoding of a pair:

$$(x, y) \;\xrightarrow{\;1\text{-}1\;}\; P = x \cdot n + y \;\in\; [0,\, n^2-1]$$

### Encryption / Decryption over $\mathbb{Z}_{n^2}$

$$E_{a,b}(P) = (a \cdot P + b) \bmod n^2, \qquad a, b \in [0,\, n^2-1]$$

$$P = D_{a,b}(E_{a,b}(P)) = \left(a^{-1} \cdot E_{a,b}(P) - a^{-1} \cdot b\right) \bmod n^2$$

> [!important] Note it's $a^{-1} \bmod n^2$
> The inverse is now taken **mod $n^2$**, not mod $n$. The exponent "squares" along with the modulus.

### Worked example — encryption

$a = 159$, $b = 580$, $n = 26$, digraph $(x,y) = \text{NO}$

$$P = x \cdot n + y = 13 \cdot 26 + 14 = 352$$

$$E_{159,580}(352) = (159 \cdot 352 + 580) \bmod 676 = 440$$

$$440 = 16 \cdot 26 + 24 \;\longrightarrow\; \textbf{QY}$$

### Worked example — decryption (the "do it yourself" exercise)

Decrypt $\textbf{QY} \rightarrow \textbf{NO}$:

| Step | Computation | Result |
|---|---|---|
| Encode ciphertext | $\text{QY} \rightarrow 16\cdot26 + 24$ | $C = 440$ |
| Find inverse | $159^{-1} \bmod 676$ (Appendix A) | $a^{-1} = 659$ |
| Multiply the offset | $659 \cdot 580 \bmod 676$ | $a^{-1}b = 280$ |
| Decrypt | $(659 \cdot 440 - 280) \bmod 676 = 289680 \bmod 676$ | $P = 352$ |
| Decode | $\lfloor 352/26 \rfloor = 13 \rightarrow \text{N}$, $352 \bmod 26 = 14 \rightarrow \text{O}$ | **NO** |

*(Not worked on the slide — computed here to check the exercise.)*

---

### The Digraph Crib

> [!danger] There IS a crib — the cipher is not stronger than it looks
> - The **second letter of the ciphertext depends only on the second letter of the plaintext**
> - A frequency analysis of the **even-numbered letters of the ciphertext** gives information on $a$ and $b$

**Why it holds** (the slide says "show this!"):

Let $C = X \cdot n + Y$, so the second ciphertext letter is $Y = C \bmod n$. Then

$$C \bmod n = (a \cdot P + b) \bmod n = \big(a(x \cdot n + y) + b\big) \bmod n = (a \cdot y + b) \bmod n$$

The $x \cdot n$ term vanishes mod $n$, so $Y$ depends on $y$ alone. Stripping the odd letters leaves a plain single-character affine cipher over $\mathbb{Z}_n$ — broken with two samples.

---

## 3. Encoding ≠ Encryption

> [!tip] Take note of the difference
> - **Encoding** takes characters to numbers
> - **Encryption** encrypts the resulting number equivalents

### Digraph encryption to numbers, not characters

For a digraph affine cipher the encryption modulus can be **different** from the encoding modulus.

| Stage | Modulus | Purpose |
|---|---|---|
| Characters → numbers | $n = 256$ (ASCII) | Encoding |
| The actual encryption | any $N$ (can be $> 256$) | Selected key |

**The scheme:**

1. $(x, y) \rightarrow$ number equivalents $X, Y$ **using ASCII**
2. Select $N$ for encryption (can be $> 256$)
3. $P = X \cdot N + Y$
4. $C = (aP + b) \bmod N^2$
5. $P = a^{-1}(C - b) \bmod N^2$
6. $P = X \cdot N + Y$
7. $x = $ ASCII decoding of $X$, $\;y = $ ASCII decoding of $Y$

> [!warning] Which $n$ when converting back?
> To go from the number $x$ back to a character you must use the **encoding** $n$ (i.e. ASCII), **not** the encryption $N$. Decrypt with the key and $N$ to recover $P$, then split into $X, Y$, then decode with ASCII.

---

## 4. Exercises (Lab Work)

1. **Write a specification** for a digraph Affine cipher
2. **Write a Perl/Java program** to implement the digraph Affine cipher
3. **Cryptanalyse** the ciphertext below, given these clues:
   - The output represents the number equivalent of each digraph of ciphertext
   - The alphabet $n = 256$
   - Take a couple of numbers and apply the decryption process, varying $a$ and $b$
   - No need to calculate inverses: $a^{-1}$ is just a number in $[0, n^2-1]$
4. **Write a cracker program** — brute force ciphertext-only attack on a digraph affine cipher
   - Assume the ciphertext is a colon-separated list of numbers representing the number equivalents of the ciphertext digraphs
   - e.g. `3456:5678:45:34567:678` etc.

### The Ciphertext

```
38344:1300:19716:3584:57344:25288:32629:43453:40761:40192:41100:
54103:19377:47876:17117:622:18021:48441:24949:13056:5041:17269:
20281:40192:58591:19965:12398:56832
17096:52041:19377:32629:19490:13076:63232:55459:50572:51363:
53760:35438:16213:55346:12624:42097
```

---

## 5. Usefulness of Classical Ciphers — A Secure ZK Protocol

A secure cryptographic protocol **built from classical ciphers**.

### The Objective: Zero-Knowledge (ZK)

> [!abstract] Goal
> To allow **verification of a key without letting the verifier know the key** — secure login.
> You should not have to show your key in order to login to a page/process. This prevents the verifier from seeing and subsequently using your key to access a resource.

### Set up

**1. Select a classical cipher** — e.g. the shift cipher.

**2. Select a function $f(z)$ over $\mathbb{Z}_n$ that is:**

| Property | Meaning |
|---|---|
| **One-way** | Given $f(z)$ it's really difficult to get $z$ |
| **Homomorphic** | Given $z_1, z_2$: $\;f(z_1 + z_2) = f(z_1) \cdot f(z_2)$ |

**3. Select a protocol** — the Zero-Knowledge protocol, with two actors:

| Actor | Role |
|---|---|
| **Prover** | Wants to *prove ownership* of the key without revealing it |
| **Verifier** | Wants to *verify* the prover knows the key |

> A prover shows a verifier that they know $z$ by sending $f(z)$ without revealing $z$.

### Initialisation (Registration)

- **Prover input:** $z < n$ (the prover's **secret**)
- **Prover sends to verifier:** $X = f(z)$

```
     z                X = f(z)
     P ──────────────────────► V
```

---

### The Game — repeated $m$ times

$$\mathbb{Z}_n^* = \{a \mid 0 < a < n,\ (a,n) = 1\}$$

| Round | Prover | Verifier |
|---|---|---|
| **Commit** | picks $k \in \mathbb{Z}_n^*$, computes $\text{Commit} = f(k)$ | receives Commit |
| **Challenge** | receives Challenge | picks Challenge = $0$ or $1$ |
| **Response** | $\text{Response} = \begin{cases} k & \text{if Challenge} = 0 \\ k + z \bmod n & \text{if Challenge} = 1 \end{cases}$ | receives Response |
| **Decision** | — | checks $f(\text{Response}) \begin{cases} = \text{Commit} & \text{if Challenge} = 0 \\ = \text{Commit} \cdot X & \text{if Challenge} = 1 \end{cases}$ |

- **Reject** if there is an error; **Accept after $m$ times**.
- The $k + z$ branch is **the homomorphic bit**: $f(k+z) = f(k)\cdot f(z) = \text{Commit} \cdot X$.

### Analysis — "perfect" security

- The verifier gets **no information about $z$** except what they can glean from $X = f(z)$ at the start
- Since $k$ can be any number in $\mathbb{Z}_n^*$, **the key size is as large as the message size** → ciphertext leaks no information about plaintext → **information-theoretically secure**
- **$k$ must only be used once** — repeated use of $k$ will reveal $z$

### Question: why not send 1 back all the time?

> [!note] Slide poses this as a discussion question
> *"Surely the cheater will be found out as they don't know $z$?"*

A cheater who doesn't know $z$ can always prepare for **one** of the two challenges (they can pick $k$ and answer Challenge 0 correctly with $k$), but they **cannot** compute $k + z \bmod n$ for Challenge 1. So a fixed/guessed response fails on one of the two branches → caught with probability $\tfrac12$ per round. Repeating $m$ independent rounds drives the cheating probability down to $2^{-m}$ — which is exactly why the protocol is run $m$ times.

---

### General Guidelines for Secure Use

> [!important] Two general conditions
> 1. The **key space should be at least as big as the message space**
> 2. **Keys should not be repeated**

- Weaker ciphers **can** form part of a secure system if they are "built in" properly
- Security faults are littered with the opposite approach — **WEP!**

### Practical implications

| | |
|---|---|
| Large data | Problem: a huge key space would be required |
| Small data | Fine — **nonces**, **session keys** |
| Constant key changes | Cause real problems in practice: **key distribution** |

---

## Appendix A — Computing $a^{-1} \bmod n$

### Problem

Compute $a^{-1} \bmod n$ — i.e. find $x$ with $a \cdot x \equiv 1 \pmod n$.

### Method: Extended Euclidean Algorithm

Worked example — **find $365^{-1} \bmod 10007$**.

**Step 1 — Euclid's algorithm (repeated division):**

| Division | Quotient | Remainder |
|---|---|---|
| $10007 = (27)(365) + 152$ | 27 | 152 |
| $365 = (2)(152) + 61$ | 2 | 61 |
| $152 = (2)(61) + 30$ | 2 | 30 |
| $61 = (2)(30) + 1$ | 2 | **1** |

Stop when the remainder is 1 (that guarantees $\gcd = 1$, so the inverse exists).

**Step 2 — back-substitute to express 1 as a combination:**

$$1 = 61 - 2(30)$$
$$= 61 - 2\big(152 - (2)(61)\big) = (5)(61) - 2(152)$$
$$= (5)\big(365 - (2)(152)\big) - 2(152) = (5)(365) - 12(152)$$
$$= (5)(365) - 12\big(10007 - (27)(365)\big)$$
$$1 = (329)(365) - 12(10007)$$

**Step 3 — read off the inverse:**

Mod 10007 the $-12(10007)$ term vanishes, so $329 \cdot 365 \equiv 1$:

$$\boxed{365^{-1} \bmod 10007 = 329}$$

> [!tip] Check
> $329 \times 365 = 120085 = 12 \times 10007 + 1 \equiv 1 \pmod{10007}$ ✓

---

## Summary

```
Number Equivalents          Affine Cipher
(A-Z→0-25, ASCII)                 │
        │                    E(P) = (aP + b) mod n
        ▼                          │
   Encoding                 needs a⁻¹ mod n  ──► Appendix A
 (chars → numbers)                │
                           ┌──────┴──────┐
                           ▼             ▼
                        Single        Digraphs
                       (n = 26)     (mod n²)
                           │             │
                           └──────┬──────┘
                                  ▼
                       still mono-alphabetic
                       + DIGRAPH CRIB (even letters)
                                  │
                                  ▼
              ZK Protocol: prove you know the key
              without revealing it (one-way + homomorphic f)
                                  │
                                  ▼
              Guidelines: keyspace ≥ message space,
              never reuse keys  ──► WEP's failure
```

---

> [!tip] Next lecture
> Fill in the `next` field in frontmatter once the next notes arrive.

## Related

- [[2026-09-28 - Number Theory & Classical Ciphers]]
- [[2026-09-24 - Introduction to Cryptography]]
