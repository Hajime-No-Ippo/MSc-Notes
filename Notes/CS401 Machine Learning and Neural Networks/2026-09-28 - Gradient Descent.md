---
tags: [cs401, machine-learning, lecture-notes]
module: CS401
topic: "Machine Learning — Gradient Descent"
date: 2026-09-28
next: "2026-09-28 - Neural Networks & Perceptron"
prev: "2026-09-28 - Linear Models"
---

# Machine Learning — Gradient Descent

> [!info] Lecture — 2026-09-27
> CS401 Machine Learning and Neural Networks

## The Problem

We have a loss function J(θ) we want to minimise. The Normal Equation only works for linear regression. **Gradient Descent** is a general-purpose optimisation algorithm that works for any differentiable function.

## Core Idea

Start with random θ, then repeatedly take a step in the direction that **most reduces** the loss:

$$\theta_j := \theta_j - \alpha \frac{\partial J(\theta)}{\partial \theta_j}$$

| Symbol | Meaning |
|---|---|
| θⱼ | The j-th parameter being updated |
| α | **Learning rate** — how big each step is |
| ∂J/∂θⱼ | Partial derivative — which direction reduces loss |

**Intuition**: The gradient points **uphill**. Subtracting it moves **downhill** toward the minimum.

## Learning Rate α

The most important hyperparameter in gradient descent.

```
        J(θ)
        │
        │  ╲                         α too large
        │   ╲   ╱╲                  ─────────────
        │    ╲╱    ╲╱              Overshoots the minimum,
        │              ╲╱╲         bounces around, diverges
        │                  ╲
        └──────────────────── θ
        
        J(θ)
        │
        │  ╲
        │   ╲                       α just right
        │    ╲                     ─────────────
        │     ╲                   Converges smoothly
        │      ●                  to the minimum
        └──────────────────── θ
        
        J(θ)
        │
        │  ╲
        │   ╲                       α too small
        │    ·                     ─────────────
        │     ·                    Takes forever,
        │      ·                   tiny steps
        └──────────────────── θ
```

| α | Effect |
|---|---|
| Too large | Overshoots, may diverge (J increases) |
| Too small | Converges very slowly |
| Just right | Converges efficiently |

## Three Variants of Gradient Descent

The difference: **how many examples** you use to compute the gradient before updating.

### Batch Gradient Descent

- Uses **all n** training examples per update
- Gradient is accurate but expensive
- Smooth convergence (like walking steadily downhill)

```
  ┌──────────────────┐
  │  All n examples   │
  │  compute gradient │
  │  → update θ       │
  └──────────────────┘
  Repeated for each iteration
```

**Pros**: Stable, guaranteed to converge (for convex)
**Cons**: Slow on large datasets, needs all data in memory

### Stochastic Gradient Descent (SGD)

- Uses **1 random example** per update
- Gradient is noisy but cheap
- Bounces around the minimum (like a drunk walk downhill)

```
  ┌──────────────────┐
  │  1 random example │
  │  compute gradient │
  │  → update θ       │
  └──────────────────┘
  Repeated n times per epoch
```

**Pros**: Fast, can escape local minima (noise helps)
**Cons**: Noisy convergence, never fully settles

### Mini-Batch Gradient Descent

- Uses **a small batch** (e.g., 32, 64, 128 examples) per update
- Best of both worlds — most common in practice

```
  ┌──────────────────┐
  │  k random examples│
  │  compute gradient │
  │  → update θ       │
  └──────────────────┘
  Repeated n/k times per epoch
```

**Pros**: Efficient, GPU-friendly, balances stability and speed
**Cons**: One more hyperparameter (batch size)

### Comparison

```
    Batch GD          Stochastic GD        Mini-Batch GD
    
    smooth curve      noisy zigzag         moderate noise
    
    ╲                 ╱╲  ╱╲               ╲╱╲
     ╲               ╱  ╲╱  ╲╱╲            ╲╱╲╱
      ╲             ╱         ╲╱            ╲╱
       ╲           ╱                       
        ●         
```

## Gradient Descent as a Family

| Variant | Batch Size | Use Case |
|---|---|---|
| Batch GD | n (all data) | Small datasets, convex problems |
| SGD | 1 | Online learning, very large data |
| Mini-Batch GD | k (typically 32–256) | **Default choice** for deep learning |

> [!note] Terminology
> "Batch GD" uses the full dataset. "Mini-Batch GD" with batch_size=32 is just called "SGD" in most ML libraries (PyTorch, TensorFlow). The terms overlap.

## Recap — Linear Regression + GD

```
1. Choose hypothesis:  h_θ(x) = θ₀ + θ₁x
2. Define loss:        J(θ) = MSE
3. Optimise:           Repeat until convergence:
                         θⱼ := θⱼ - α · ∂J/∂θⱼ
4. Result:             Best-fit line
```

---

> [!tip] Next lecture
> Neural Networks & Perceptron — from linear models to multi-layer networks.
