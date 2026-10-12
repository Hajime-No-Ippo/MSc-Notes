# [Classification] Support Vector Machine Implementations — CS401

From-scratch implementation of a linear soft-margin SVM, matching the lecture notes.

## Files

| File | Language | Method | Description |
|---|---|---|---|
| `svm.py` | Python | Hinge-loss subgradient descent | Linear soft margin, from scratch, no ML libraries |

## Code

```python
"""
Linear Support Vector Machine (soft margin) — CS401
From scratch, no ML libraries.
Minimises 0.5*||w||^2 + C * sum(max(0, 1 - y*(w.x + b))) by full-batch subgradient descent.
"""

# ---- Training Data ----
# (Hours studied, Hours slept) → Passed (+1) / Failed (-1)
DATA = [
    (1.0, 5.0, -1),
    (1.5, 6.0, -1),
    (2.0, 5.0, -1),
    (2.5, 4.0, -1),
    (3.0, 5.0, -1),
    (4.0, 5.0, +1),
    (5.0, 6.0, +1),
    (6.0, 5.0, +1),
    (6.5, 7.0, +1),
    (7.0, 6.0, +1),
]

n = len(DATA)
POINTS = [(d[0], d[1]) for d in DATA]
LABELS = [d[2] for d in DATA]

# Standardise features so the margin is scale-independent
means = [sum(p[i] for p in POINTS) / n for i in range(2)]
stds = [(sum((p[i] - means[i]) ** 2 for p in POINTS) / n) ** 0.5 for i in range(2)]
POINTS_S = [((p[0] - means[0]) / stds[0], (p[1] - means[1]) / stds[1]) for p in POINTS]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


# ---- Training: subgradient of hinge-loss objective ----
def train_svm(C=1.0, lr=0.05, iterations=2000):
    w = [0.0, 0.0]
    b = 0.0

    for iteration in range(iterations):
        grad_w = [w[0], w[1]]          # d/dw of 0.5*||w||^2
        grad_b = 0.0                   # bias is not regularised
        hinge_count = 0

        for xi, yi in zip(POINTS_S, LABELS):
            margin = yi * (dot(w, xi) + b)
            if margin < 1:             # hinge loss active → support vector candidate
                hinge_count += 1
                grad_w[0] -= C * yi * xi[0]
                grad_w[1] -= C * yi * xi[1]
                grad_b -= C * yi

        w[0] -= lr * grad_w[0] / n
        w[1] -= lr * grad_w[1] / n
        b -= lr * grad_b / n

        if iteration % 400 == 0:
            print(f"Iter {iteration:4d} | hinge violations: {hinge_count:2d} | "
                  f"w: [{w[0]:+.4f}, {w[1]:+.4f}] | b: {b:+.4f}")

    return w, b


def decision(w, b, x):
    """w.x + b — positive → class +1 (pass)"""
    xs = ((x[0] - means[0]) / stds[0], (x[1] - means[1]) / stds[1])
    return dot(w, xs) + b


def predict(w, b, x):
    return 1 if decision(w, b, x) > 0 else 0


# ---- Main ----
if __name__ == "__main__":
    print("=" * 60)
    print("Linear SVM — soft margin, subgradient descent")
    print("=" * 60)
    print(f"Training data: {n} examples (+1 pass / -1 fail)")
    print()

    w, b = train_svm(C=1.0, lr=0.05, iterations=2000)

    print()
    print("=" * 60)
    print(f"Result: h(x) = sign({w[0]:.4f}*x1 + {w[1]:.4f}*x2 + {b:.4f})")
    print("=" * 60)

    # Predictions
    print()
    print(f"{'Hours':>6} | {'Slept':>6} | {'Actual':>6} | {'Margin':>7} | {'Predicted':>9}")
    print("-" * 46)
    correct = 0
    support = []
    for xi, yi in zip(POINTS, LABELS):
        y_pred = predict(w, b, xi)
        m = decision(w, b, xi)
        correct += (1 if y_pred else -1) == yi
        if abs(m) < 0.5:
            support.append(xi)
        print(f"{xi[0]:>6} | {xi[1]:>6} | {yi:>+6} | {m:>7.3f} | {y_pred:>9}")

    print()
    print(f"Training accuracy: {correct}/{n} = {correct / n:.0%}")
    print(f"Points near the margin (|margin| < 0.5): {support}")

    # Predict new value
    print()
    new_point = (4.5, 6.0)
    print(f"New prediction: {new_point[0]} hours studied, {new_point[1]} hours slept "
          f"→ margin {decision(w, b, new_point):.3f} → {'PASS' if predict(w, b, new_point) else 'FAIL'}")
```
## What's Inside

- **Objective**: minimise ½‖w‖² + C · Σ max(0, 1 - y(w·x + b))
- **Hinge loss**: penalty only when a point violates the margin (y(w·x+b) < 1)
- **Optimisation**: full-batch subgradient descent, bias excluded from regularisation
- **Prediction**: sign(w·x + b) > 0 → class 1 (pass)
- **Support-vector candidates**: points with |margin| < 0.5 — here (3.0, 5.0) and (4.0, 5.0), the two points hugging the boundary
- Labels are ±1 (SVM convention), features standardised so the margin is scale-independent

## Training Data

(Hours studied, Hours slept) → Pass (+1) / Fail (-1):

| Hours studied | 1 | 1.5 | 2 | 2.5 | 3 | 4 | 5 | 6 | 6.5 | 7 |
|---|---|---|---|---|---|---|---|---|---|---|
| Hours slept | 5 | 6 | 5 | 4 | 5 | 5 | 6 | 5 | 7 | 6 |
| Passed | -1 | -1 | -1 | -1 | -1 | +1 | +1 | +1 | +1 | +1 |

Try `C=10.0` — a harder margin penalises violations more and pushes the support vectors closer to the line.
