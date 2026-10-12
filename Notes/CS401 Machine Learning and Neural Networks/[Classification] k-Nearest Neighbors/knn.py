"""
k-Nearest Neighbors (kNN) — CS401
From scratch, no ML libraries.
Instance-based learning: no training phase, prediction = majority vote of k closest points.
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

# Standardise features so distance is scale-independent
means = [sum(p[i] for p in POINTS) / n for i in range(2)]
stds = [(sum((p[i] - means[i]) ** 2 for p in POINTS) / n) ** 0.5 for i in range(2)]
POINTS_S = [((p[0] - means[0]) / stds[0], (p[1] - means[1]) / stds[1]) for p in POINTS]


# ---- Distance ----
def distance(a, b):
    """Euclidean distance sqrt(sum((a_i - b_i)^2))"""
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


# ---- Prediction: majority vote of the k closest training points ----
def knn_predict(x, k=3, exclude_index=None):
    xs = ((x[0] - means[0]) / stds[0], (x[1] - means[1]) / stds[1])
    dists = []
    for i, p in enumerate(POINTS_S):
        if i == exclude_index:
            continue
        dists.append((distance(xs, p), LABELS[i]))
    dists.sort(key=lambda t: t[0])
    votes = [label for _, label in dists[:k]]
    return 1 if sum(votes) * 2 > k else 0, dists[:k]


# ---- Main ----
if __name__ == "__main__":
    print("=" * 60)
    print("k-Nearest Neighbors (k = 3, Euclidean distance)")
    print("=" * 60)
    print(f"Training data: {n} examples")
    print()

    # Leave-one-out evaluation (a point never votes for itself)
    print("Leave-one-out evaluation:")
    print(f"{'Hours':>6} | {'Slept':>6} | {'Actual':>6} | {'Predicted':>9} | Nearest 3 (dist, label)")
    print("-" * 78)
    correct = 0
    for i, (pt, label) in enumerate(zip(POINTS, LABELS)):
        y_pred, neighbours = knn_predict(pt, k=3, exclude_index=i)
        correct += y_pred == label
        nbrs = ", ".join(f"({d:.2f}, {y})" for d, y in neighbours)
        print(f"{pt[0]:>6} | {pt[1]:>6} | {label:>6} | {y_pred:>9} | {nbrs}")

    print()
    print(f"LOO accuracy: {correct}/{n} = {correct / n:.0%}")

    # Predict new value
    print()
    new_point = (4.5, 6.0)
    y_pred, neighbours = knn_predict(new_point, k=3)
    nbrs = ", ".join(f"({d:.2f}, {y})" for d, y in neighbours)
    print(f"New prediction: {new_point[0]} hours studied, {new_point[1]} hours slept")
    print(f"  3 nearest: {nbrs} → {'PASS' if y_pred else 'FAIL'}")
