# CS401 — Machine Learning & Neural Networks

> [!note] Complete Course Notes
> Consolidated summary from all CS401 lectures.

---

## Lecture Overview

| # | Date | Topic | Link |
|---|---|---|---|
| 1 | 2026-09-21 | Foundations | `[[2026-09-21 - Foundations]]` |
| 2 | 2026-09-28 | Linear Models | `[[2026-09-28 - Linear Models]]` |
| 3 | 2026-09-28 | Gradient Descent | `[[2026-09-28 - Gradient Descent]]` |
| 4 | 2026-09-28 | Neural Networks & Perceptron | `[[2026-09-28 - Neural Networks & Perceptron]]` |

---

## 1. Foundations

### What is ML?

- **Machine Learning** is a subset of AI
- Hierarchy: **AI → ML → Neural Networks**
- ML learns patterns from data

### Core Pipeline

```
┌─────────┐      ┌──────────────┐      ┌─────────────────┐
│  DATA   │ ───▶ │ ML Algorithm │ ───▶ │ Prediction Model│
└─────────┘      └──────────────┘      └─────────────────┘
```

### Learning Types

| Type | Labels? | Tasks | Example |
|---|---|---|---|
| **Supervised** | ✅ Yes | Classification, Regression | Predict house price from area |
| **Unsupervised** | ❌ No | Clustering, Dimensionality reduction | Customer segmentation |
| **Reinforcement** | Reward-based | Policy learning | Game playing, robotics |

### RL Agent-Environment Loop

```
┌─────────┐    Action (A₁)    ┌─────────────┐
│  Agent  │ ───────────────▶  │ Environment │
└─────────┘                    └─────────────┘
     ▲                              │
     │        State (S₁)            │
     └──────────────────────────────┘
                    ▲
                    │  Reward (R)
```

### Key References

- **Andrew Ng** — prominent ML educator
- **Tom Mitchell** — *Machine Learning* (textbook)
- **Donald Hebb** (1949) — Hebbian learning, foundational to neural networks

---

## 2. Linear Models

### Hypothesis

$$h(x) = \theta_0 + \theta_1 x$$

- $\theta_0$ — bias/intercept
- $\theta_1$ — slope/weight

### Loss Function (MSE)

$$J(\theta_0, \theta_1) = \frac{1}{n} \sum_{i=1}^{n} (h(x_i) - y_i)^2$$

### Training Data (House Prices)

| Area (m²) | 50 | 60 | 70 | 80 | 90 | 100 | 110 | 120 | 130 | 140 |
|---|---|---|---|---|---|---|---|---|---|---|
| Price (€k) | 150 | 180 | 210 | 240 | 270 | 300 | 330 | 360 | 390 | 420 |

---

## 3. Gradient Descent

### Update Rule

$$\theta_j := \theta_j - \alpha \frac{\partial J(\theta)}{\partial \theta_j}$$

- $\alpha$ — learning rate (step size)

### Comparison

| Variant | Data Used | Speed | Convergence |
|---|---|---|---|
| **Batch GD** | All n samples | Slow | Smooth, stable |
| **SGD** | 1 sample | Fast | Noisy, may oscillate |
| **Mini-Batch** | B samples (e.g., 32) | Balanced | Good compromise |

---

## 4. Neural Networks & Perceptron

### Single Neuron

```
Input → [Weighted Sum + Bias] → Activation → Output
         w₁x₁ + w₂x₂ + b         σ(z)
```

### Activation Function (Sigmoid)

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

### Perceptron Learning Rule

$$w_j := w_j + \alpha (y - \hat{y}) x_j$$

### AND Gate Example

| x₁ | x₂ | y (AND) |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

After training: $w_1 = 1, w_2 = 1, b = -1.5$

---

## 5. Implementations

### Files

| File | Method | Location |
|---|---|---|
| `linear_regression.py` | Gradient Descent (from scratch) | `Linear Regression/` |
| `LinearRegression.java` | Gradient Descent (from scratch) | `Linear Regression/` |
| `normal_equation.py` | Normal Equation (NumPy) | `Linear Regression/` |
| `Foundation.ipynb` | Interactive notebook | `Linear Regression/` |

### Normal Equation (Closed-form)

$$\theta = (X^T X)^{-1} X^T y$$

---

## 6. Key Formulas Cheat Sheet

| Concept | Formula |
|---|---|
| Hypothesis | $h(x) = \theta_0 + \theta_1 x$ |
| MSE Loss | $J(\theta) = \frac{1}{n} \sum (h(x_i) - y_i)^2$ |
| GD Update | $\theta_j := \theta_j - \alpha \frac{\partial J}{\partial \theta_j}$ |
| Normal Equation | $\theta = (X^T X)^{-1} X^T y$ |
| Sigmoid | $\sigma(z) = \frac{1}{1 + e^{-z}}$ |
| Perceptron Update | $w_j := w_j + \alpha (y - \hat{y}) x_j$ |

---

## 7. Related Fields

| Field | Relevance |
|---|---|
| Statistics | Probability, distributions, inference |
| Dynamic Programming | Optimisation, sequence problems |
| Data Mining | Pattern discovery in large datasets |
