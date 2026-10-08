# Random Forest Implementations — CS401

From-scratch implementation of a Random Forest, matching the lecture notes.

## Files

| File | Language | Method | Description |
|---|---|---|---|
| `random_forest.py` | Python | Bagging (5 trees) | Bootstrap samples + random feature subsets, from scratch, no ML libraries |

## Code

```python
"""
Random Forest (bagged decision trees) — CS401
From scratch, no ML libraries.
Each tree trains on a bootstrap sample; each split sees a random feature subset.
"""

import random

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
N_FEATURES = len(FEATURE_NAMES)
random.seed(42)


# ---- Gini Impurity ----
def gini(labels):
    if not labels:
        return 0.0
    p1 = sum(labels) / len(labels)
    return 1.0 - (p1 ** 2 + (1 - p1) ** 2)


# ---- Best Split over a random feature subset (sqrt(N_FEATURES) = 1) ----
def best_split(Xs, ys, candidate_feats):
    best = None
    best_score = 1.0
    for feat in candidate_feats:
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


# ---- Tree Building (random feature subset at every split) ----
def build_tree(Xs, ys):
    if len(set(ys)) == 1 or not Xs:
        return {"leaf": ys[0]}

    k = max(1, int(N_FEATURES ** 0.5))  # sqrt(p) features per split
    candidate_feats = random.sample(range(N_FEATURES), k)
    split, score = best_split(Xs, ys, candidate_feats)
    if split is None or score >= gini(ys):
        return {"leaf": max(set(ys), key=ys.count)}

    feat, thr = split
    left_idx = [j for j in range(len(Xs)) if Xs[j][feat] <= thr]
    right_idx = [j for j in range(len(Xs)) if Xs[j][feat] > thr]
    return {
        "feature": feat,
        "threshold": thr,
        "left": build_tree([Xs[j] for j in left_idx], [ys[j] for j in left_idx]),
        "right": build_tree([Xs[j] for j in right_idx], [ys[j] for j in right_idx]),
    }


def predict_one(tree, x):
    while "leaf" not in tree:
        tree = tree["left"] if x[tree["feature"]] <= tree["threshold"] else tree["right"]
    return tree["leaf"]


# ---- Forest: bootstrap aggregating (bagging) ----
def build_forest(n_trees=5):
    forest = []
    n = len(X)
    for t in range(n_trees):
        # Bootstrap sample: n draws with replacement
        idx = [random.randrange(n) for _ in range(n)]
        forest.append(build_tree([X[i] for i in idx], [Y[i] for i in idx]))
    return forest


def forest_predict(forest, x):
    votes = [predict_one(tree, x) for tree in forest]
    return 1 if sum(votes) * 2 > len(votes) else 0, votes


# ---- Main ----
if __name__ == "__main__":
    N_TREES = 5

    print("=" * 60)
    print(f"Random Forest — {N_TREES} bagged CART trees")
    print("=" * 60)
    print(f"Training data: {len(X)} examples, bootstrap samples, sqrt(p) features/split")
    print()

    forest = build_forest(N_TREES)

    print(f"{'Hours':>6} | {'Slept':>6} | {'Actual':>6} | {'Votes (tree 1..N)':>18} | {'Predicted':>9}")
    print("-" * 66)
    correct = 0
    for xi, yi in zip(X, Y):
        y_pred, votes = forest_predict(forest, xi)
        correct += y_pred == yi
        print(f"{xi[0]:>6} | {xi[1]:>6} | {yi:>6} | {str(votes):>18} | {y_pred:>9}")

    print()
    print(f"Training accuracy: {correct}/{len(X)} = {correct / len(X):.0%}")

    # Predict new value
    print()
    new_point = (4.5, 6.0)
    y_pred, votes = forest_predict(forest, new_point)
    print(f"New prediction: {new_point[0]} hours studied, {new_point[1]} hours slept")
    print(f"  votes: {votes} → {'PASS' if y_pred else 'FAIL'}")
```
## What's Inside

- **Bootstrap**: each tree trains on n draws *with replacement* from the data
- **Feature randomisation**: only √p features are considered at each split (p = 2 here)
- **Vote**: forest prediction = majority vote over the 5 trees
- **Individual trees disagree** near the boundary (see the Votes column) — the majority vote fixes it → 10/10
- Seeded `random.seed(42)` so results are reproducible

## Training Data

(Hours studied, Hours slept) → Pass (1) / Fail (0):

| Hours studied | 1 | 1.5 | 2 | 2.5 | 3 | 4 | 5 | 6 | 6.5 | 7 |
|---|---|---|---|---|---|---|---|---|---|---|
| Hours slept | 5 | 6 | 5 | 4 | 5 | 5 | 6 | 5 | 7 | 6 |
| Passed | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |

Try raising `N_TREES` to see the vote settle down, or compare with `Decision Tree/`.
