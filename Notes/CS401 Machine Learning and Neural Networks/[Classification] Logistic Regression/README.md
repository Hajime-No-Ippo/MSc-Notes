# [Classification] Logistic Regression Implementations — CS401

From-scratch implementation of Logistic Regression, matching the lecture notes.

## Files

| File | Language | Method | Description |
|---|---|---|---|
| `logistic_regression.py` | Python | Gradient Descent | Sigmoid + log loss, from scratch, no ML libraries |

## Code

```python
"""
Logistic Regression with Gradient Descent — CS401
From scratch, no ML libraries.
"""

import math

# ---- Training Data ----
# Hours studied → Passed (1) / Failed (0)
X = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5]
Y = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

n = len(X)

# Standardise features so gradient descent converges cleanly
mean = sum(X) / n
std = (sum((x - mean) ** 2 for x in X) / n) ** 0.5
Xs = [(x - mean) / std for x in X]


# ---- Hypothesis (sigmoid) ----
def predict_proba(xs, theta0, theta1):
    """h(x) = 1 / (1 + e^-(theta0 + theta1*x))"""
    z = theta0 + theta1 * xs
    return 1.0 / (1.0 + math.exp(-z))


def predict(xs, theta0, theta1, threshold=0.5):
    """Class 1 if h(x) >= 0.5, else 0"""
    return 1 if predict_proba(xs, theta0, theta1) >= threshold else 0


# ---- Loss Function (log loss / cross-entropy) ----
def compute_loss(theta0, theta1):
    """J = -(1/n) * sum(y*log(h) + (1-y)*log(1-h))"""
    total = 0.0
    for i in range(n):
        h = predict_proba(Xs[i], theta0, theta1)
        h = min(max(h, 1e-9), 1 - 1e-9)  # avoid log(0)
        total += Y[i] * math.log(h) + (1 - Y[i]) * math.log(1 - h)
    return -total / n


# ---- Gradient Descent ----
def gradient_descent(lr=0.1, iterations=1000):
    theta0 = 0  # bias
    theta1 = 0  # weight

    for iteration in range(iterations):
        grad0 = 0  # dJ/dtheta0
        grad1 = 0  # dJ/dtheta1

        for i in range(n):
            h = predict_proba(Xs[i], theta0, theta1)
            error = h - Y[i]
            grad0 += error            # derivative w.r.t. theta0
            grad1 += error * Xs[i]    # derivative w.r.t. theta1

        grad0 /= n
        grad1 /= n

        theta0 -= lr * grad0
        theta1 -= lr * grad1

        if iteration % 200 == 0:
            loss = compute_loss(theta0, theta1)
            print(f"Iter {iteration:4d} | Loss: {loss:>8.4f} | theta0: {theta0:.4f} | theta1: {theta1:.4f}")

    return theta0, theta1


# ---- Main ----
if __name__ == "__main__":
    print("=" * 60)
    print("Logistic Regression — Gradient Descent")
    print("=" * 60)
    print(f"Training data: {n} examples")
    print(f"X (hours studied): {X}")
    print(f"Y (passed):        {Y}")
    print()

    theta0, theta1 = gradient_descent(lr=0.1, iterations=2000)

    print()
    print("=" * 60)
    print(f"Result: h(x) = 1 / (1 + e^-({theta0:.3f} + {theta1:.3f} * x))")
    print(f"Final loss: {compute_loss(theta0, theta1):.4f}")
    print("=" * 60)

    # Predictions
    print()
    print("Predictions:")
    print(f"{'Hours':>6} | {'Actual':>6} | {'P(pass)':>7} | {'Predicted':>9}")
    print("-" * 38)
    correct = 0
    for x_val, y_val in zip(X, Y):
        p = predict_proba((x_val - mean) / std, theta0, theta1)
        y_pred = predict((x_val - mean) / std, theta0, theta1)
        correct += y_pred == y_val
        print(f"{x_val:>6} | {y_val:>6} | {p:>7.3f} | {y_pred:>9}")

    print()
    print(f"Training accuracy: {correct}/{n} = {correct / n:.0%}")

    # Predict new value
    print()
    new_hours = 3.2
    p = predict_proba((new_hours - mean) / std, theta0, theta1)
    print(f"New prediction: {new_hours} hours studied → P(pass) = {p:.3f} → {'PASS' if p >= 0.5 else 'FAIL'}")
```
## What's Inside

- **Hypothesis**: h(x) = 1 / (1 + e^-(θ₀ + θ₁x))  (sigmoid)
- **Loss**: Log loss J = -(1/n) Σ [y·log(h) + (1-y)·log(1-h)]
- **Gradient Descent**: θⱼ := θⱼ - α · ∂J/∂θⱼ
- **Prediction**: P(pass) ≥ 0.5 → class 1, else class 0
- Features are standardised first so GD converges cleanly

## Training Data

Hours studied → Pass (1) / Fail (0):

| Hours studied | 1 | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 | 4.5 | 5 | 5.5 |
|---|---|---|---|---|---|---|---|---|---|---|
| Passed | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |

Decision lands between 3 and 3.5 hours — try `3.2` in the "new prediction" line to see a ~0.44 probability (right on the boundary).
