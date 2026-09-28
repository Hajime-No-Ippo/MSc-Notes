---
tags: [cs401, machine-learning, lecture-notes]
module: CS401
topic: "Machine Learning — Linear Models"
date: 2026-09-28
next: "2026-09-28 - Gradient Descent"
prev: "2026-09-21 - Foundations"
---

# Machine Learning — Linear Models

> [!info] Lecture — 2026-09-26
> CS401 Machine Learning and Neural Networks

## The Prediction Problem

Given a dataset of (input, output) pairs, learn a function that maps new inputs to outputs.

| Symbol | Meaning |
|---|---|
| x⁽ⁱ⁾ | Input (feature) of i-th training example |
| y⁽ⁱ⁾ | Output (label) of i-th training example |
| D | Training set: {(x⁽ⁱ⁾, y⁽ⁱ⁾); i = 1,...,n} |
| X, Y | Input and output spaces (here both ℝ) |

**Goal**: Learn a function h: X → Y (called the **hypothesis**)

## Linear Hypothesis

The simplest model — a straight line:

$$h_\theta(x) = \theta_0 + \theta_1 x$$

| Parameter | Name | Role |
|---|---|---|
| θ₀ | Bias / intercept | Where the line crosses the y-axis |
| θ₁ | Weight / slope | How steep the line is |

**Example** — three different hypotheses:

```
h(x) = 1.5 + 0x        h(x) = 0 + 0.5x        h(x) = 1 + 0.5x

   y │ ────────           y │     ╱              y │     ╱
     │                        │   ╱                  │   ╱
     │                        │ ╱                    │ ╱
  ───┼──── x              ───┼──── x            ───┼──── x
     │                        │                      │
     
θ₀=1.5, θ₁=0            θ₀=0, θ₁=0.5          θ₀=1, θ₁=0.5
(horizontal line)        (through origin)       (starts at y=1)
```

The model is **linear** in the parameters θ₀, θ₁. Adjusting these changes the line.

## Loss Function — How Wrong Are We?

To pick the best θ₀, θ₁, we need a measure of error. The **loss function** tells us how far our predictions are from reality.

### Mean Squared Error (MSE)

$$J(\theta_0, \theta_1) = \frac{1}{n} \sum_{i=1}^{n} \left( h_\theta(x^{(i)}) - y^{(i)} \right)^2$$

- **Squared** penalises large errors more than small ones
- **Average** over all n examples gives a single number
- **Goal**: find θ₀, θ₁ that **minimise** J

### Normal Equation (closed-form solution)

For linear regression, there's an exact formula — no iteration needed:

$$\theta = (X^T X)^{-1} X^T y$$

| Pros | Cons |
|---|---|
| One-step, no hyperparameters | O(n³) matrix inversion |
| Exact solution | Doesn't scale to millions of features |
| — | Only works for linear regression |

When the Normal Equation is too expensive or the model isn't linear, we use **Gradient Descent** instead.

## From Linear Models to Neural Networks

A single linear unit is a **neuron**. Stack many, add a non-linearity, and you get a neural network — the topic of the next lecture.

---

> [!tip] Next lecture
> Gradient Descent — how to find the best θ by iterative optimisation.
