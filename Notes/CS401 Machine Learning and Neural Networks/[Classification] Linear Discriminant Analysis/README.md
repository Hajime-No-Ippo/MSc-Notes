# [Classification] Linear Discriminant Analysis Implementations — CS401

From-scratch implementation of (binary) LDA, matching the lecture notes.

## Files

| File                              | Language | Method      | Description                                              |
| --------------------------------- | -------- | ----------- | -------------------------------------------------------- |
| `linear_discriminant_analysis.py` | Python   | Closed-form | Pooled covariance inverse, from scratch, no ML libraries |
|                                   |          |             |                                                          |

## Code

```python
"""
Linear Discriminant Analysis (LDA) — CS401
From scratch, no ML libraries.
Closed-form: w = S^-1 (mu1 - mu0), b = -0.5 w^T (mu0 + mu1)
"""

# Training data: (Hours studied, Hours slept) → Passed (1) / Failed (0)
DATA = [
    (1.0, 5.0, 0),
    (1.5, 6.0, 0),
    (2.0, 5.0, 0),
    (2.5, 4.0, 0),
    (3.0, 5.0, 0),
    (4.0, 5.0, 1),
    (5.0, 6.0, 1),
    (6.0, 5.0, 1),
    (6.5, 7.0, 1),
    (7.0, 6.0, 1),
]

X = [d[:2] for d in DATA]
Y = [d[2] for d in DATA]

X0 = [x for x, y in zip(X, Y) if y == 0]
X1 = [x for x, y in zip(X, Y) if y == 1]
n0, n1 = len(X0), len(X1)


def mean(rows, j):
    """Class/feature mean"""
    return sum(r[j] for r in rows) / len(rows)


def covariance(rows, mu):
    """Sample covariance matrix of one class (ddof=1)"""
    m = len(rows)
    c00 = sum((r[0] - mu[0]) ** 2 for r in rows) / (m - 1)
    c01 = sum((r[0] - mu[0]) * (r[1] - mu[1]) for r in rows) / (m - 1)
    c11 = sum((r[1] - mu[1]) ** 2 for r in rows) / (m - 1)
    return [[c00, c01], [c01, c11]]


def inverse2(m):
    """Inverse of a 2x2 matrix: (1/det) * [[d, -b], [-c, a]]"""
    det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    return [[m[1][1] / det, -m[0][1] / det],
            [-m[1][0] / det, m[0][0] / det]]


def matvec(m, v):
    return [m[0][0] * v[0] + m[0][1] * v[1],
            m[1][0] * v[0] + m[1][1] * v[1]]


# Class means
mu0 = [mean(X0, 0), mean(X0, 1)]
mu1 = [mean(X1, 0), mean(X1, 1)]

# Pooled (within-class) covariance
C0, C1 = covariance(X0, mu0), covariance(X1, mu1)
S = [[((n0 - 1) * C0[i][j] + (n1 - 1) * C1[i][j]) / (n0 + n1 - 2) for j in range(2)]
     for i in range(2)]

# LDA projection: w = S^-1 (mu1 - mu0), decision at class-mean midpoint
w = matvec(inverse2(S), [mu1[0] - mu0[0], mu1[1] - mu0[1]])
b = -0.5 * (w[0] * (mu1[0] + mu0[0]) + w[1] * (mu1[1] + mu0[1]))


def decision(x):
    """w.x + b — positive → class 1 (pass)"""
    return w[0] * x[0] + w[1] * x[1] + b


def predict(x):
    return 1 if decision(x) > 0 else 0


print("=" * 60)
print("Linear Discriminant Analysis (closed-form)")
print("=" * 60)
print(f"mu0 (fail): [{mu0[0]:.3f}, {mu0[1]:.3f}]   mu1 (pass): [{mu1[0]:.3f}, {mu1[1]:.3f}]")
print(f"S (pooled): [[{S[0][0]:.3f}, {S[0][1]:.3f}], [{S[1][0]:.3f}, {S[1][1]:.3f}]]")
print(f"w: [{w[0]:.4f}, {w[1]:.4f}]   b: {b:.4f}")
print(f"Result: h(x) = sign({w[0]:.4f}*x1 + {w[1]:.4f}*x2 + {b:.4f})")
print()

# Predictions
print(f"{'Hours studied':>13} | {'Hours slept':>11} | {'Actual':>6} | {'Score':>7} | {'Predicted':>9}")
print("-" * 60)
correct = 0
for xi, yi in zip(X, Y):
    y_pred = predict(xi)
    correct += y_pred == yi
    print(f"{xi[0]:>13.1f} | {xi[1]:>11.1f} | {yi:>6} | {decision(xi):>7.3f} | {y_pred:>9}")

print()
print(f"Training accuracy: {correct}/{len(X)} = {correct / len(X):.0%}")

# Predict new value
print()
new_point = (4.5, 6.0)
print(f"New prediction: {new_point[0]} hours studied, {new_point[1]} hours slept "
      f"→ score {decision(new_point):.3f} → {'PASS' if predict(new_point) else 'FAIL'}")
```
## What's Inside

- **Class means**: μ₀ = mean(fail), μ₁ = mean(pass)
- **Pooled covariance**: S = ((n₀-1)C₀ + (n₁-1)C₁) / (n₀+n₁-2)
- **Projection**: w = S⁻¹(μ₁ - μ₀)
- **Decision threshold**: b = -½ wᵀ(μ₀ + μ₁) → midpoint between the projected class means
- **Prediction**: sign(w·x + b) > 0 → class 1 (pass)
- 2×2 matrix inverse done by hand — the closed-form analogue of the Normal Equation

## Training Data

(Hours studied, Hours slept) → Pass (1) / Fail (0):

| Hours studied | 1 | 1.5 | 2 | 2.5 | 3 | 4 | 5 | 6 | 6.5 | 7 |
|---|---|---|---|---|---|---|---|---|---|---|
| Hours slept | 5 | 6 | 5 | 4 | 5 | 5 | 6 | 5 | 7 | 6 |
| Passed | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |

No iteration needed — one matrix inverse gives the answer directly.
