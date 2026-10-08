---
tags: [cs401, machine-learning, classification, regularization, lecture-notes]
module: CS401
topic: "Machine Learning — Classification & Regularization"
date: 2026-10-08
next: "[[]]"
prev: "[[2026-09-28 - Neural Networks & Perceptron]]"
---

# Machine Learning — Classification & Regularization

> [!info] Lecture 3a — 2026-10-08
> CS401 Machine Learning and Neural Networks · Dr. Cathy Ennis
> Source: `3a Classification.pdf`

**Overview**

- Classification vs logistic regression
- Cost functions & log loss
- Gradient descent + training
- Overfitting & regularisation
- Links to neural networks

---

## 1. Supervised Learning — Prediction

Given data points $\{x^{(1)}, \dots, x^{(m)}\}$ with outcomes $\{y^{(1)}, \dots, y^{(m)}\}$, build a model that learns to predict $y$ from $x$.

| | **Regression** | **Classification** |
|---|---|---|
| Outcome | Continuous | Class |
| Examples | Linear Regression, Multiple Linear Regression | Logistic Regression, SVM, Naïve Bayes |
| Uses | House price, stock price | Cancer prediction, customer churn |

### Discriminative vs Generative

| | **Discriminative** | **Generative** |
|---|---|---|
| Goal | Directly estimate $P(y \mid x)$ | Estimate $P(x \mid y)$, then deduce $P(y \mid x)$ |
| What's learned | Decision boundary | Probability distributions of the data |
| Examples | Regression, SVM | GDA, Naïve Bayes |

---

## 2. Classification

> [!abstract] Definition
> **Class = category.** The output variable can take on only one of a small number of values.

```
Is this email spam?            Yes / No
Is this transaction fraudulent? Yes / No
Is the tumour malignant?        Yes / No
```

Linear regression is **not** a good algorithm for classification problems.

### Types of Classification

| Type | Labels | Condition | Example |
|---|---|---|---|
| **Binary** | $y \in \{0,1\}$ | Negative class / Positive class · False/True · Absence/Presence (not bad / good) | Spam or not |
| **Multi-class** | $y \in \{0,1,2,3,\dots\}$ | Each instance belongs to **only one** class | Digit recognition |
| **Multi-label** | zero or more labels | Labels **not mutually exclusive** | Tagging images with multiple objects |

### Common Classification Algorithms

| Category | Algorithms |
|---|---|
| **Linear models** | Logistic Regression · Linear Discriminant Analysis (LDA) |
| **Instance-based** | k-Nearest Neighbors (kNN) |
| **Tree-based** | Decision Trees · Random Forest · Gradient Boosted Trees (XGBoost, LightGBM, CatBoost) |
| **Probabilistic / other** | Support Vector Machines (SVM) · Neural Networks / Deep Learning |

---

## 3. Why Not Linear Regression?

Trying to predict Yes(1)/No(0) from tumour size with a straight line:

```
      Yes - 1     x  x  x  x
 Malignant?
      No - 0     o  o  o
                  Tumour Size
```

With $\hat y = h_\theta(x) = \theta^T x$ and thresholding at 0.5:

$$\text{if } h_\theta(x) < 0.5,\ \hat y = 0 \qquad \text{if } h_\theta(x) \ge 0.5,\ \hat y = 1$$

**Problems:** a few far-outlier points drag the line around, moving the 0.5 crossing point — so the decision boundary is unstable. **Logistic regression is better than linear regression for this.**

---

## 4. Logistic Regression

> [!note] Despite the name
> Logistic regression is a **classification** algorithm, not a regression algorithm.

It models the **probability** that a given input $x$ belongs to a particular class.

### Logistic / Sigmoid Function

Maps any real input to $[0, 1]$:

$$h_\theta(x) = g(\theta^T x) = \frac{1}{1 + e^{-(\theta^T x)}} \qquad \text{where } g(z) = \frac{1}{1 + e^{-z}}$$

Remember $\theta^T x = \sum_{i=0}^{d} \theta_i x_i$ (with $x_0 = 1$).

**Properties:**

| $z$ | $g(z)$ |
|---|---|
| $z = 100$ | $\approx 1$ |
| $z = 0$ | $0.5$ |
| $z = -100$ | $\approx 0$ |

- S-shaped curve, always $0 < g(z) < 1$
- **Predict class 0** if $h_\theta(x) < 0.5$
- **Predict class 1** if $h_\theta(x) \ge 0.5$

**Probabilities:**

$$P(y = 1 \mid x; \theta) = h_\theta(x) \qquad\qquad P(y = 0 \mid x; \theta) = 1 - h_\theta(x)$$

---

## 5. Decision Boundaries

### Linear

$$h_\theta(x) = g(\theta_0 + \theta_1x_1 + \theta_2x_2), \qquad \theta = \begin{bmatrix}-3\\1\\1\end{bmatrix}$$

```
 x2
  3 │
  2 │        y = 1
  1 │   ● ●
    └──────────── x1
        1   2   3
       y = 0
        Decision boundary
```

- Predict $y=1$ if $-3 + x_1 + x_2 \ge 0$, i.e. $x_1 + x_2 \ge 3$
- Predict $y=0$ if $x_1 + x_2 < 3$

### Non-Linear

Adding polynomial features lets the boundary curve:

$$h_\theta(x) = g(\theta_0 + \theta_1x_1 + \theta_2x_2 + \theta_3x_1^2 + \theta_4x_2^2 + \dots)$$

With $\theta = [-1, 0, 0, 1, 1]^T$: predict $y=1$ if $x_1^2 + x_2^2 \ge 1$ — a **circle** of radius 1.

---

## 6. Cost Function for Logistic Regression

The MSE cost does **not** work here:

$$J(\theta) = \frac{1}{2m}\sum_i \left(h_\theta(x^{(i)}) - y^{(i)}\right)^2$$

> [!warning] Why MSE fails
> 1. Because of the nature of decision boundaries, MSE is not a good option — lots of **local minima**.
> 2. Substituting the **sigmoid** into the MSE cost function makes it **non-convex** (the non-linearity of the sigmoid gives a non-convex shape).

$$J(\theta) = \frac{1}{2m}\sum_{i=1}^{m}\left(\frac{1}{1+e^{-(\theta^Tx^{(i)})}} - y^{(i)}\right)^2 \quad \leftarrow \text{non-convex, many local minima}$$

**We need a different cost function.**

### Logistic Loss — Cross Entropy

$$\ln \sigma = \ln\frac{1}{1+e^{-z}}$$

$$L(h_\theta(x), y) = \begin{cases} -\log h_\theta(x) & \text{if } y = 1 \\[4pt] -\log\big(1 - h_\theta(x)\big) & \text{if } y = 0 \end{cases}$$

| Symbol | Meaning |
|---|---|
| $m$ | number of training examples |
| $y^{(i)}$ | true class label for example $i$ (0 or 1) |
| $h_\theta(x^{(i)})$ | predicted probability for example $i$ |
| $\theta$ | model parameters |

### Intuition

| If $y = 1$ | If $y = 0$ |
|---|---|
| Cost $= 0$ when the predicted value is 1 | Cost $= 0$ when the predicted value is 0 |
| As $h_\theta(x)$ deviates from 1 → 0, cost increases **exponentially** and tends to infinity | As $h_\theta(x)$ deviates from 0 → 1, cost increases **exponentially** and tends to infinity |

### Simplified Loss Function

Because $y^{(i)}$ is only ever 0 or 1, the two cases collapse into one expression:

$$L(h_\theta(x^{(i)}), y^{(i)}) = -y^{(i)}\log h_\theta(x^{(i)}) - (1-y^{(i)})\log\big(1-h_\theta(x^{(i)})\big)$$

- If $y^{(i)} = 1$: second term is $0 \times \log(\cdot) = 0$, leaving $-\log h_\theta$
- If $y^{(i)} = 0$: first term is $0$, leaving $-\log(1-h_\theta)$

### Simplified Cost Function

$$\boxed{J(\theta) = -\frac{1}{m}\sum_{i=1}^{m}\Big[y^{(i)}\log\big(h_\theta(x^{(i)})\big) + \big(1-y^{(i)}\big)\log\big(1-h_\theta(x^{(i)})\big)\Big]}$$

> [!tip] Why this one
> Derived from **maximum likelihood estimation** in statistics — gives a **convex** loss function with a **single global minimum**.

---

## 7. Gradient Descent + Training

### Training Logistic Regression

1. Find a good choice for parameters $\theta$ (or $w, b$)
2. Then for a new input $x$ compute
   $$g(\theta^T x) = \frac{1}{1+e^{-(\theta^T x)}}$$
3. The model makes a prediction / estimates $P(y = 1 \mid x; \theta)$

Minimise the cost function with gradient descent, as before.

### The Update Rule

$$\theta_j := \theta_j - \alpha\,\frac{\partial}{\partial \theta_j}J(\theta)$$

$$\text{Repeat}\ \begin{cases} \theta_j := \theta_j - \alpha\,\frac{1}{m}\sum_{i=1}^{m}\big(h_\theta(x^{(i)}) - y^{(i)}\big)x_j^{(i)} \end{cases} \quad \text{simultaneous updates}$$

> [!note] Looks like linear regression…
> The update rule has the same shape, but the $h_\theta(x^{(i)})$ **function is different** — here $h_\theta(x) = \dfrac{1}{1+e^{-\theta^Tx}}$.

### Same concepts as linear regression

- Monitor gradient descent — **learning curve**
- **Vectorized** implementation
- **Feature scaling**

---

## 8. Overfitting + Regularization

### Underfitting vs Overfitting

```
   Overfit            Generalisation          Underfit
 High Variance                            High Bias
```

### Bias and Variance

Two key sources of error that impact performance and generalisation.

| | **Bias** | **Variance** |
|---|---|---|
| Cause | Model is **too simple** and doesn't learn enough detail | Model learns **too much**, including random noise/outliers |
| Effect | Underfitting — poor on **both** training and test data | Poor generalisation — good on training, poor on test |
| Speed | Easier to train | |
| Example | Linear regression applied to data with a non-linear relationship | |

### Addressing Underfitting

1. Increase model complexity
2. Increase the number of features — feature engineering
3. Remove noise from the data
4. Increase the number of **epochs** or the duration of training

> [!note] Epoch
> One complete pass through the entire training dataset, where every sample is passed through the model and parameters are updated based on the calculated error. Training requires multiple epochs so the model improves iteratively.

### Addressing Overfitting

1. **Collect more training data** — improves generalisation
2. **Reduce model complexity**
   - Fewer features (feature selection) — can use intuition to pick the most relevant
   - Disadvantage: useful features could be lost
3. **Regularization** — shrink the value of parameters $\theta$ for features $x$
   - Gentler than setting them to zero
   - Keeps all features but prevents them having an overly large effect
   - Generally not for $\theta_0$, though it should make little difference

---

## 9. Regularization

### The Idea

Add the features you want to penalise to the cost function, weighted by a **large magnitude**. The model is penalised by having a large cost function if those parameters are large — so it is forced to make them small.

```
  Price                              Price
   │                                  │        ╱
   │      ╱                          │      ╱
   │    ╱                            │    ╱
   │  ╱                              │  ╱
   └────────── Size of house         └────────── Size of house
   θ0 + θ1x + θ2x²                   θ0 + θ1x + θ2x² + θ3x³ + θ4x⁴

                                      If we penalise θ3, θ4 the model
                                      is forced to make them small
```

Example with an explicit penalty:

$$\frac{1}{2m}\sum_{i=1}^{m}\big(h_\theta(x^{(i)}) - y^{(i)}\big)^2 + 1000*\theta_3^2 + 1000*\theta_4^2$$

### The Regularized Cost Function

If you have a larger model with $n$ features ($>100$), you can't select which to penalise, so penalise **all of them apart from the bias coefficient** ($b$ or $\theta_0$):

$$\boxed{J(\theta) = \frac{1}{2m}\sum_{i=1}^{m}\big(h_\theta(x^{(i)}) - y^{(i)}\big)^2 + \frac{\lambda}{2m}\sum_{j=1}^{n}\theta_j^2}$$

| Symbol | Meaning |
|---|---|
| $m$ | number of examples / data points |
| $n$ | number of features (predictor variables) — the sum starts at $j=1$, skipping $\theta_0$ |
| $h_\theta(x^{(i)})$ | predicted target value for the $i$-th example |
| $y^{(i)}$ | actual target value for the $i$-th example |
| $\theta_j^2$ | coefficients of the features |
| $\lambda$ | **regularization parameter** — controls the strength of regularization |

### Choosing $\lambda$

| $\lambda$ | Result |
|---|---|
| Too big | Horizontal line at $\theta_0$ → **underfit** |
| Too small | **overfitting** |
| Just right | Balanced model that generalises |

> [!important] Choosing the right value for $\lambda$ is important.

### Regularized Linear Regression — Gradient Descent

$$\text{Repeat until convergence } \begin{cases} \theta_0 := \theta_0 - \alpha\,\dfrac{1}{m}\displaystyle\sum_{i=1}^{m}\big(h_\theta(x^{(i)}) - y^{(i)}\big)x_0^{(i)} \\[10pt] \theta_j := \theta_j - \alpha\left(\dfrac{1}{m}\displaystyle\sum_{i=1}^{m}\big(h_\theta(x^{(i)}) - y^{(i)}\big)x_j^{(i)} + \dfrac{\lambda}{m}\theta_j\right) \quad j \ge 1 \end{cases}$$

simultaneous updates · remember $x_0^{(i)} = 1$

> The $\theta_0$ update is **not** regularized; every other $\theta_j$ picks up the extra $+\dfrac{\lambda}{m}\theta_j$ term, which shrinks it toward 0 each step.

### Regularized Logistic Regression — Gradient Descent

$$\text{Repeat until convergence } \begin{cases} \theta_0 := \theta_0 - \alpha\,\dfrac{1}{m}\displaystyle\sum_{i=1}^{m}\big(h_\theta(x^{(i)}) - y^{(i)}\big)x_0^{(i)} \\[10pt] \theta_j := \theta_j - \alpha\left(\dfrac{1}{m}\displaystyle\sum_{i=1}^{m}\big(h_\theta(x^{(i)}) - y^{(i)}\big)x_j^{(i)} + \dfrac{\lambda}{m}\theta_j\right) \quad j \ge 1 \end{cases}$$

simultaneous updates · remember $x_0^{(i)} = 1$

> [!note] Same as linear regression
> Looks similar to linear regression, **but** $h_\theta(x^{(i)}) = \dfrac{1}{1+e^{-\theta^Tx}}$.

---

## 10. Links to Neural Networks

In the coming weeks the course moves to neural networks, which reuse everything covered here:

- **Gradient descent**
- **Cost functions**
- **Sigmoid functions**

---

## Summary

```
Regression ──(continuous)──► predict a number
     │
 Supervised prediction
     │
Classification ─(class)───► predict a category
     │
     ├─ binary / multi-class / multi-label
     ├─ linear regression fails → Logistic Regression
     │      └─ sigmoid maps to [0,1] → probability
     ├─ MSE non-convex → Log Loss / Cross Entropy (convex, MLE)
     ├─ Gradient Descent trains θ (same shape as linear, new h)
     │
 Overfitting/Underfitting
     ├─ bias    → too simple   → underfit
     ├─ variance→ learns noise → overfit
     └─ Regularization: + (λ/2m)Σθⱼ²  (all but θ0)
            ├─ λ too big → underfit
            ├─ λ too small → overfit
            └─ GD updates gain + (λ/m)θⱼ
     │
     ▼
 Neural Networks (reuse GD, cost functions, sigmoid)
```

---

## Related

- [[2026-09-28 - Linear Models]]
- [[2026-09-28 - Gradient Descent]]
- [[2026-09-28 - Neural Networks & Perceptron]]
- [[2026-09-21 - Foundations]]

---

> [!tip] Next lecture
> Fill in the `next` field in frontmatter once the next notes arrive.
