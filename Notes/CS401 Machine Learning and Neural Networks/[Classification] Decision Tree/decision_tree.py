"""
Decision Tree (CART, Gini impurity) — CS401
From scratch, no ML libraries.
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

FEATURE_NAMES = ["hours studied", "hours slept"]
X = [d[:2] for d in DATA]
Y = [d[2] for d in DATA]


# ---- Gini Impurity ----
def gini(labels):
    """Gini = 1 - (p1^2 + p0^2); 0 = pure node"""
    if not labels:
        return 0.0
    p1 = sum(labels) / len(labels)
    return 1.0 - (p1 ** 2 + (1 - p1) ** 2)


# ---- Best Split (CART) ----
def best_split(Xs, ys):
    """Try every feature × every midpoint threshold, keep lowest weighted Gini."""
    best = None
    best_score = 1.0
    for feat in range(len(FEATURE_NAMES)):
        values = sorted({x[feat] for x in Xs})
        for i in range(len(values) - 1):
            thr = (values[i] + values[i + 1]) / 2
            left = [ys[j] for j in range(len(Xs)) if Xs[j][feat] <= thr]
            right = [ys[j] for j in range(len(Xs)) if Xs[j][feat] > thr]
            if not left or not right:
                continue
            score = (len(left) * gini(left) + len(right) * gini(right)) / len(Xs)
            if score < best_score:
                best_score = score
                best = (feat, thr)
    return best, best_score


# ---- Tree Building ----
def build_tree(Xs, ys, depth=0):
    """Leaf when pure or no split improves impurity."""
    if len(set(ys)) == 1 or not Xs:
        return {"leaf": ys[0]}
    split, score = best_split(Xs, ys)
    if split is None or score >= gini(ys):
        return {"leaf": max(set(ys), key=ys.count)}

    feat, thr = split
    left_idx = [j for j in range(len(Xs)) if Xs[j][feat] <= thr]
    right_idx = [j for j in range(len(Xs)) if Xs[j][feat] > thr]
    return {
        "feature": feat,
        "threshold": thr,
        "left": build_tree([Xs[j] for j in left_idx], [ys[j] for j in left_idx], depth + 1),
        "right": build_tree([Xs[j] for j in right_idx], [ys[j] for j in right_idx], depth + 1),
    }


def predict_one(tree, x):
    while "leaf" not in tree:
        tree = tree["left"] if x[tree["feature"]] <= tree["threshold"] else tree["right"]
    return tree["leaf"]


def print_tree(tree, indent=""):
    if "leaf" in tree:
        print(f"{indent}→ class {tree['leaf']}")
        return
    feat = FEATURE_NAMES[tree["feature"]]
    print(f"{indent}{feat} <= {tree['threshold']:.2f} ?")
    print_tree(tree["left"], indent + "    yes: ")
    print_tree(tree["right"], indent + "    no:  ")


# ---- Main ----
if __name__ == "__main__":
    print("=" * 60)
    print("Decision Tree — CART with Gini impurity")
    print("=" * 60)
    print(f"Training data: {len(X)} examples")
    print()

    tree = build_tree(X, Y)
    print("Tree structure:")
    print_tree(tree)
    print()

    # Predictions
    print(f"{'Hours':>6} | {'Slept':>6} | {'Actual':>6} | {'Predicted':>9}")
    print("-" * 38)
    correct = 0
    for xi, yi in zip(X, Y):
        y_pred = predict_one(tree, xi)
        correct += y_pred == yi
        print(f"{xi[0]:>6} | {xi[1]:>6} | {yi:>6} | {y_pred:>9}")

    print()
    print(f"Training accuracy: {correct}/{len(X)} = {correct / len(X):.0%}")

    # Predict new value
    print()
    new_point = (4.5, 6.0)
    print(f"New prediction: {new_point[0]} hours studied, {new_point[1]} hours slept "
          f"→ {'PASS' if predict_one(tree, new_point) else 'FAIL'}")
