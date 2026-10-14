---
tags: [cs401, machine-learning, lecture-notes]
module: CS401
topic: "Machine Learning — Neural Networks & Perceptron"
date: 2026-09-28
next: "[[2026-10-08 - Classification & Regularization]]"
prev: "[[2026-09-28 - Gradient Descent]]"
---

# Machine Learning — Neural Networks & Perceptron

> [!info] Lecture — 2026-09-28
> CS401 Machine Learning and Neural Networks

## From Linear Models to Neural Networks

A linear model h(x) = θ₀ + θ₁x can only draw straight lines. To learn complex patterns, we need **non-linearity**. The trick: combine many linear units with a non-linear activation function.

## The Single Neuron

```
  x₁ ──w₁──╲
             ╲
  x₂ ──w₂───( Σ + b )──σ── y
             ╱
  x₃ ──w₃──╱
```

$$y = \sigma(z) = \sigma\left(\sum_i w_i x_i + b\right)$$

| Component | Name | Role |
|---|---|---|
| xᵢ | Input features | What the neuron sees |
| wᵢ | Weights | Importance of each input |
| b | Bias | Shift the activation threshold |
| Σ | Weighted sum | z = Σwᵢxᵢ + b |
| σ | Activation function | Introduces non-linearity |

## Sigmoid Activation

The classic activation function:

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

```
  σ(z)
   1 │          ╭────────
     │        ╱
 0.5 │──────╱───────────
     │     ╱
   0 │────╯
     └──────────────── z
        -5    0    5
```

**Properties**:
- Output is always between 0 and 1 (interpretable as probability)
- Smooth, differentiable everywhere
- Large negative z → σ ≈ 0, Large positive z → σ ≈ 1

## Neuron as Logic Gate — AND

A single neuron can learn the **AND gate**:

| x₁ | x₂ | x₁ AND x₂ |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

**Solution**: w₁ = 0.5, w₂ = 0.5, b = -0.7

```
x₁  x₂  │  z = 0.5x₁ + 0.5x₂ - 0.7  │  σ(z)  │  Output
─────────┼─────────────────────────────┼────────┼──────────
 0    0  │  -0.7                        │  0.33  │  0
 0    1  │  -0.2                        │  0.45  │  0
 1    0  │  -0.2                        │  0.45  │  0
 1    1  │   0.3                        │  0.57  │  1
```

> [!note] Threshold
> With sigmoid, σ(0) = 0.5. The neuron outputs 1 when z > 0, i.e., σ(z) > 0.5.

## The Perceptron — Learning Algorithm

The perceptron is the simplest neural network: a single neuron with a step function (not sigmoid). It learns by trial and error.

### Perceptron Learning Rule

After each prediction, update the weights:

$$w_i := w_i + \eta \cdot (y - \hat{y}) \cdot x_i$$

| Symbol | Meaning |
|---|---|
| η | Learning rate |
| y | True label |
| ŷ | Predicted label (0 or 1) |
| (y - ŷ) | Error signal: 0 if correct, ±1 if wrong |

**Logic**:
- If y = 1, ŷ = 0 (under-predicted) → **increase** weights
- If y = 0, ŷ = 1 (over-predicted) → **decrease** weights
- If y = ŷ (correct) → **no change**

### Worked Example — AND Gate

Training data: (0,0)→0, (0,1)→0, (1,0)→0, (1,1)→1

**Iteration 1** (starting: w₁=0, w₂=0, b=0, η=0.5):

| x₁  | x₂  | y   | z    | ŷ   | Error | Update                                  |
| --- | --- | --- | ---- | --- | ----- | --------------------------------------- |
| 0   | 0   | 0   | 0    | 1   | -1    | w₁=w₁+0.5·(-1)·0=0, b=0+0.5·(-1)·1=-0.5 |
| 0   | 1   | 0   | -0.5 | 0   | 0     | no change                               |
| 1   | 0   | 0   | -0.5 | 0   | 0     | no change                               |
| 1   | 1   | 1   | 0.5  | 1   | 0     | no change                               |

After iteration 1: w₁=0, w₂=0, b=-0.5

**Iteration 2**:

| x₁  | x₂  | y   | z    | ŷ   | Error | Update    |
| --- | --- | --- | ---- | --- | ----- | --------- |
| 0   | 0   | 0   | -0.5 | 0   | 0     | no change |
| 0   | 1   | 0   | -0.5 | 0   | 0     | no change |
| 1   | 0   | 0   | -0.5 | 0   | 0     | no change |
| 1   | 1   | 1   | 0.5  | 1   | 0     | no change |

All correct — **converged!** Final: w₁=0, w₂=0, b=-0.5

> [!warning] Convergence
> The perceptron **converges** if the data is **linearly separable** (a straight line can separate classes). For non-linearly separable data (like XOR), the perceptron will never converge.

## Perceptron vs Sigmoid Neuron

| Feature        | Perceptron                      | Sigmoid Neuron                    |
| -------------- | ------------------------------- | --------------------------------- |
| Output         | 0 or 1 (hard step)              | 0 to 1 (smooth)                   |
| Learning rule  | w += η(y-ŷ)x                    | Gradient descent                  |
| Can learn XOR? | No                              | Yes (with hidden layers)          |
| Guarantee      | Converges if linearly separable | Minimises loss (may be local min) |

## Key Insight

> [!important] From One Neuron to Many
> A single neuron can only learn **linearly separable** patterns. To learn complex functions (like image recognition), we stack many neurons into **layers** → **neural networks**.

```
  Input Layer    Hidden Layers    Output Layer
  
   x₁ ─────╲     ╱─────╲
             ╲──╱   ╲───╲
   x₂ ──────╲╱──────────╲─── y₁
             ╱╲   ╱─────╱
   x₃ ─────╱  ╲╱   ╱──╱
                ╲──╱
```

Each hidden layer learns increasingly abstract features from the previous layer's output.

---

> [!tip] Next lecture
> Fill in the `next` field in frontmatter once the next notes arrive.
