# [Classification] Perceptron Implementations — CS401

From-scratch implementation of the Perceptron Learning Algorithm, matching the lecture notes.

## Files

| File | Language | Method | Description |
|---|---|---|---|
| `perceptron.py` | Python | Perceptron rule | Step neuron, updates only on mistakes, from scratch, no ML libraries |

## Code

```python
"""
Perceptron Learning Algorithm — CS401
From scratch, no ML libraries.
Matches the lecture: linear neuron with step activation, weights update only on misclassification.
"""

# ---- Training Data ----
# (Hours studied, Hours slept) → Passed (1) / Failed (0)
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

n = len(DATA)
POINTS = [(d[0], d[1]) for d in DATA]
LABELS = [d[2] for d in DATA]

# Standardise features so the learning rate behaves consistently
means = [sum(p[i] for p in POINTS) / n for i in range(2)]
stds = [(sum((p[i] - means[i]) ** 2 for p in POINTS) / n) ** 0.5 for i in range(2)]
POINTS_S = [((p[0] - means[0]) / stds[0], (p[1] - means[1]) / stds[1]) for p in POINTS]


# ---- Neuron: step activation ----
def neuron(x, w, b):
    """output = 1 if w.x + b >= 0 else 0"""
    z = w[0] * x[0] + w[1] * x[1] + b
    return 1 if z >= 0 else 0


# ---- Perceptron Learning Rule ----
def train_perceptron(lr=0.1, epochs=50):
    w = [0.0, 0.0]
    b = 0.0

    for epoch in range(epochs):
        errors = 0
        for x, y in zip(POINTS_S, LABELS):
            y_pred = neuron(x, w, b)
            if y_pred != y:  # update ONLY on mistake
                errors += 1
                w[0] += lr * (y - y_pred) * x[0]
                w[1] += lr * (y - y_pred) * x[1]
                b += lr * (y - y_pred)
        if epoch % 10 == 0 or errors == 0:
            print(f"Epoch {epoch:3d} | errors: {errors} | w: [{w[0]:+.4f}, {w[1]:+.4f}] | b: {b:+.4f}")
        if errors == 0:
            print(f"Converged at epoch {epoch} — zero training errors")
            break

    return w, b


# ---- Logic gates (lecture: "Neuron as Logic Gate") ----
def train_gate(name, inputs, targets, lr=1.0, epochs=20):
    w = [0.0, 0.0]
    b = 0.0
    errors = epochs
    for _ in range(epochs):
        errors = 0
        for x, y in zip(inputs, targets):
            z = 1 if w[0] * x[0] + w[1] * x[1] + b >= 0 else 0
            if z != y:
                errors += 1
                w[0] += lr * (y - z) * x[0]
                w[1] += lr * (y - z) * x[1]
                b += lr * (y - z)
        if errors == 0:
            break
    hits = sum(
        (1 if w[0] * x1 + w[1] * x2 + b >= 0 else 0) == y
        for (x1, x2), y in zip(inputs, targets)
    )
    print(f"{name}: w = [{w[0]:+.1f}, {w[1]:+.1f}], b = {b:+.1f} → "
          f"{hits}/{len(targets)} correct")
    return errors


# ---- Main ----
if __name__ == "__main__":
    print("=" * 60)
    print("Perceptron Learning Algorithm")
    print("=" * 60)
    print(f"Training data: {n} examples")
    print()

    w, b = train_perceptron(lr=0.1, epochs=50)

    print()
    print("=" * 60)
    print(f"Result: h(x) = step({w[0]:.4f}*x1 + {w[1]:.4f}*x2 + {b:.4f})")
    print("=" * 60)

    # Predictions
    print()
    print(f"{'Hours':>6} | {'Slept':>6} | {'Actual':>6} | {'z = w.x+b':>9} | {'Predicted':>9}")
    print("-" * 50)
    correct = 0
    for xi, yi in zip(POINTS, LABELS):
        xs = ((xi[0] - means[0]) / stds[0], (xi[1] - means[1]) / stds[1])
        z = w[0] * xs[0] + w[1] * xs[1] + b
        y_pred = neuron(xs, w, b)
        correct += y_pred == yi
        print(f"{xi[0]:>6} | {xi[1]:>6} | {yi:>6} | {z:>+9.3f} | {y_pred:>9}")

    print()
    print(f"Training accuracy: {correct}/{n} = {correct / n:.0%}")

    # Predict new value
    print()
    new_point = (4.5, 6.0)
    xs = ((new_point[0] - means[0]) / stds[0], (new_point[1] - means[1]) / stds[1])
    print(f"New prediction: {new_point[0]} hours studied, {new_point[1]} hours slept "
          f"→ {'PASS' if neuron(xs, w, b) else 'FAIL'}")

    # Logic gates — can a single neuron learn them?
    print()
    print("Logic gates (single neuron):")
    train_gate("AND", [(0, 0), (0, 1), (1, 0), (1, 1)], [0, 0, 0, 1])
    train_gate("OR ", [(0, 0), (0, 1), (1, 0), (1, 1)], [0, 1, 1, 1])
    xor_errors = train_gate("XOR", [(0, 0), (0, 1), (1, 0), (1, 1)], [0, 1, 1, 0])
    if xor_errors:
        print("XOR: NOT linearly separable — a single neuron can never learn it (→ need hidden layers)")
```
## What's Inside

- **Neuron**: output = step(w·x + b) → 1 if z ≥ 0, else 0 (the lecture's step activation)
- **Learning rule**: on a mistake only, w := w + η(y - ŷ)x and b := b + η(y - ŷ)
- Converges in **1 epoch** on this linearly separable data
- **Logic-gate demo** (lecture: "Neuron as Logic Gate"):
  - AND → 4/4 correct
  - OR → 4/4 correct
  - XOR → stuck at 2/4 — **not linearly separable**, a single neuron can never learn it (the motivation for hidden layers)
- Features standardised so η = 0.1 behaves consistently

## Training Data

(Hours studied, Hours slept) → Pass (1) / Fail (0):

| Hours studied | 1 | 1.5 | 2 | 2.5 | 3 | 4 | 5 | 6 | 6.5 | 7 |
|---|---|---|---|---|---|---|---|---|---|---|
| Hours slept | 5 | 6 | 5 | 4 | 5 | 5 | 6 | 5 | 7 | 6 |
| Passed | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |

Compare with `Support Vector Machines/` — both learn a linear boundary, but the SVM maximises the margin instead of stopping at the first error-free one.
