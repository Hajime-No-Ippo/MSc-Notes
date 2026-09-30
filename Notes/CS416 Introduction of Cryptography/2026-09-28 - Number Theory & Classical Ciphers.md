---
tags: [cs416, cryptography, lecture-notes]
module: CS416
topic: "Number Theory & Classical Ciphers"
date: 2026-09-28
next: "[[]]"
prev: "[[2026-09-24 - Introduction to Cryptography]]"
---

# Number Theory & Classical Ciphers

> [!info] Lecture 2 — 2026-09-28
> CS416 Cryptography · Lecturer: Tom Dowling (tom.dowling@mu.ie)

---

## Chinese Remainder Theorem (CRT)

> [!abstract] Number Theory Aside
> CRT solves systems of simultaneous congruences.

### Problem Statement

Given a system of congruences:

$$x \equiv a_1 \pmod{m_1}$$
$$x \equiv a_2 \pmod{m_2}$$
$$\vdots$$
$$x \equiv a_n \pmod{m_n}$$

Where $m_1, m_2, \ldots, m_n$ are **pairwise coprime** (gcd of any pair = 1).

### Solution

$$x = \sum_{i=1}^{n} a_i M_i N_i \pmod{M}$$

Where:

| Symbol | Definition |
|---|---|
| $M$ | $m_1 \cdot m_2 \cdots m_n$ (product of all moduli) |
| $M_i$ | $M / m_i$ (product of all moduli except $m_i$) |
| $N_i$ | $M_i^{-1} \bmod m_i$ (modular inverse of $M_i$ mod $m_i$) |

### Worked Example

> [!example] Simple CRT
> Solve: $x \equiv 3 \pmod{5}$, $x \equiv 4 \pmod{7}$
>
> 1. $M = 5 \times 7 = 35$
> 2. $M_1 = 35/5 = 7$, $M_2 = 35/7 = 5$
> 3. $N_1 = 7^{-1} \bmod 5 = 3$ (since $7 \times 3 = 21 \equiv 1 \pmod{5}$)
> 4. $N_2 = 5^{-1} \bmod 7 = 3$ (since $5 \times 3 = 15 \equiv 1 \pmod{7}$)
> 5. $x = (3 \times 7 \times 3 + 4 \times 5 \times 3) \bmod 35 = (63 + 60) \bmod 35 = 123 \bmod 35 = \mathbf{18}$

### 中國剩餘定理詳解（孫子算經）

> [!note] 中文筆記
> 要分清楚「**題目給的**」和「**自己算出來的**」兩類數字。

#### 題目給的：$a_i$ 和 $m_i$

這組數字 $x \equiv 2 \pmod{3},\ x \equiv 3 \pmod{5},\ x \equiv 2 \pmod{7}$ 不是隨機亂挑的——它就是《孫子算經》裡的原題：

> 「有物不知其數，三三數之剩二，五五數之剩三，七七數之剩二，問物幾何？」

翻成白話：有一堆東西不知道數量，三個三個數剩 2 個，五個五個數剩 3 個，七個七個數剩 2 個，問總共多少個？答案 23。

所以在實際問題中，**題目會用兩種方式提供數字**：

1. **白話描述**：「除以 3 餘 2、除以 5 餘 3、除以 7 餘 2」→ 你自己翻譯成同餘式
2. **直接給同餘式**：$x \equiv a_i \pmod{m_i}$，給你一串 $a_i$（餘數）和 $m_i$（模數）

題目給的數字只有兩組：**餘數 $a_i$ 和 模數 $m_i$，而且要滿足一個條件：模數兩兩互質（3、5、7 都是質數，天然符合）。

#### 自己算出來的：$M$、$M_i$、$N_i$、$x$

題目不會給這些，是機械性算出來的：

| 量 | 算法 | 這題的值 |
|---|---|---|
| $M$ | 所有模數相乘 | $3 \times 5 \times 7 = 105$ |
| $M_i$ | $M$ 除以 $m_i$ | 35、21、15 |
| $N_i$ | 解 $M_i N_i \equiv 1 \pmod{m_i}$ | 2、1、1 |
| $x$ | 代入公式再 mod M | 23 |

#### 古人口訣

> 三人同行七十稀（$2 \times 70$），五樹梅花廿一枝（$3 \times 21$），
> 七子團圓正半月（$2 \times 15$），除百零五便得知。

算出 $140 + 63 + 30 = 233$，減掉 105 得 23。這裡的 70、21、15 其實就是 $M_i N_i$，口訣等於把反元素都幫你背好了。

#### 實務應用

- **考試/課本**：直接給你同餘式系統，或包裝成應用題（「一個數除以…餘…」）
- **密碼學/工程**：例如 RSA 解密加速、秘密分享、雜湊產生，會直接指定幾個互質的模數（常用質數），程式用擴展歐幾里得算法自動求 $N_i$，整個過程不需要人手算

**簡單說：給的是「餘數」和「模數」，其餘全是套公式的機械計算。**

### Cryptographic Applications

| Application | Description |
|---|---|
| **Key Recovery Mechanism (KRM)** | Split a key into shares using CRT; recover by solving the system |
| **Subliminal Channel** | Hidden communication channel embedded within CRT-based schemes |

---

## Decoding: Converting Numbers to Text

> [!example] Decoding a Number to Letters
> Given a numeric value $P$, decode it to a 3-letter string using base-26 encoding.
>
> **Given:** $P = 1 \times 26^2 + 8 \times 26 + 17 = 861$
>
> **Step 1:** Extract the first letter:
> $$x = \lfloor P / 26^2 \rfloor = \lfloor 861 / 676 \rfloor = 1 \rightarrow \textbf{B}$$
>
> **Step 2:** Extract the last letter:
> $$z = P \bmod 26 = 861 \bmod 26 = 17 \rightarrow \textbf{R}$$
>
> **Step 3:** Extract the middle letter:
> $$Y = \frac{P - 1 \times 26^2 - 17}{26} = \frac{861 - 676 - 17}{26} = \frac{168}{26} = 8 \rightarrow \textbf{I}$$
>
> **Result:** $P = 861 \rightarrow \textbf{BIR}$ (Biometric Identity Record)

### Encoding Formula

For a 3-letter word $(L_1, L_2, L_3)$ where each letter is a number 0–25:

$$P = L_1 \times 26^2 + L_2 \times 26 + L_3$$

---

## Classic Ciphers

> [!note] Historical Ciphers
> These are the foundations of cryptographic thinking, though insecure by modern standards.

### Substitution Ciphers

Each letter is replaced by another letter according to a fixed mapping.

```
Plaintext:  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
Ciphertext: D E F G H I J K L M N O P Q R S T U V W X Y Z A B C
```

- **Caesar Cipher** — shift by a fixed number (e.g., shift 3: A→D, B→E)
- **ROT13** — special case of Caesar with shift 13

### Transposition Ciphers

Letters are rearranged according to a fixed pattern.

```
Plaintext:  HELLO WORLD
Ciphertext: HLOOL WRLDE  (reading columns)
```

### One-Time Pad

> [!tip] Theoretically Unbreakable
> - Key is truly random, at least as long as the message
> - Key is used only once
> - Key is kept perfectly secret
>
> **XOR encryption:** $C = P \oplus K$, $P = C \oplus K$

---

## Quadratic Residues (QR) & Legendre Symbol

### Definitions

> [!abstract] Quadratic Residue
> A number $a$ is a **quadratic residue mod n** if there exists some $x$ such that:
> $$x^2 \equiv a \pmod{n}$$
> If no such $x$ exists, $a$ is a **quadratic non-residue (QNR)**.

### Legendre Symbol

For prime $p$ and integer $a$:

$$\left(\frac{a}{p}\right) = \begin{cases} +1 & \text{if } a \text{ is a QR mod } p \\ -1 & \text{if } a \text{ is a QNR mod } p \\ 0 & \text{if } a \equiv 0 \pmod{p} \end{cases}$$

**Key property:**

$$\left(\frac{a}{p}\right) \equiv a^{(p-1)/2} \pmod{p}$$

### QR for Composite Moduli (n = p·q)

> [!important] Jacobi Symbol Extension
> For $n = p \cdot q$ (product of two primes):
>
> $$\left(\frac{a}{n}\right) = \left(\frac{a}{p}\right) \cdot \left(\frac{a}{q}\right)$$
>
> $a$ is a **QR mod n** if and only if **both** $\left(\frac{a}{p}\right) = +1$ **and** $\left(\frac{a}{q}\right) = +1$.

---

## QR Bleed Attack

> [!warning] QR Bleed — E-Voting Vulnerability
> If an encryption scheme **preserves quadratic residuosity**, an attacker can determine the plaintext without decrypting.

### The Attack

Given:
- Encryption scheme where **QR is invariant** (QR encrypts to QR, QNR encrypts to QNR)
- $n = 35 = 5 \times 7$
- Plaintext mapping: **Yes → 8**, **No → 9**
- Ciphertext: $C = 22$

**Question:** Was the plaintext Yes or No?

### Solution

**Step 1:** Compute Jacobi symbol for the ciphertext:

$$\left(\frac{22}{35}\right) = \left(\frac{22}{5}\right) \cdot \left(\frac{22}{7}\right)$$

**Step 2:** Evaluate each Legendre symbol:

| Component | Calculation | Result |
|---|---|---|
| $\left(\frac{22}{5}\right)$ | $22^2 \bmod 5 = 4$ | $-1$ (QNR) |
| $\left(\frac{22}{7}\right)$ | $22^3 \bmod 7 = 1$ | $+1$ (QR) |

**Step 3:** Combine:

$$\left(\frac{22}{35}\right) = (-1)(+1) = -1 \implies \textbf{QNR}$$

**Step 4:** Check the plaintext values:

| Plaintext | Jacobi Symbol | Type |
|---|---|---|
| 8 (Yes) | $(8/35) = (8/5)(8/7) = (-1)(+1) = -1$ | QNR |
| 9 (No) | $(9/35) = (9/5)(9/7) = (+1)(+1) = +1$ | QR |

**Conclusion:** Since $C = 22$ is QNR, and QR is preserved by encryption, the plaintext must also be QNR. Therefore:

$$\boxed{\text{Plaintext} = \textbf{YES}}$$

> [!danger] Critical Insight
> **We did not have to decrypt!** By checking whether the ciphertext is QR or QNR, we can determine information about the plaintext — a devastating attack on e-voting systems.

### Consequences for E-Voting

- An encrypted vote (Yes/No) leaks information via its quadratic residuosity
- Anyone who knows the public key $(n)$ can check if $C$ is QR or QNR
- This violates **semantic security** (ciphertext should reveal nothing about plaintext)

---

## Summary

```
Chinese Remainder Theorem          Classic Ciphers
         │                              │
    Solve systems                 Historical methods
    of congruences               (substitution, transposition)
         │                              │
         ▼                              ▼
    Key Recovery                 Foundation of
    Mechanism (KRM)              modern cryptography
         │                              │
         └──────────┬───────────────────┘
                    ▼
           Number Theory is the
           backbone of cryptography
```

---

> [!tip] Next lecture
> Fill in the `next` field in frontmatter once the next notes arrive.
