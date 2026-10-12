---
tags: [cs401, machine-learning, evaluation, metrics, lecture-notes]
module: CS401
topic: "Machine Learning — Evaluation Measures"
date: 2026-10-12
next: "[[]]"
prev: "[[2026-10-08 - Classification & Regularization]]"
---

# Machine Learning — Evaluation Measures

> [!info] Lecture 4 — 2026-10-12
> CS401 Machine Learning and Neural Networks · Dr. Cathy Ennis
> Source: `4 Evaluation Measures.pdf`

**Overview**

- Goals of evaluation & model skill
- The hold-out test set & cross-validation
- Classification measures: confusion matrix, accuracy, precision, recall, F1
- ROC & Precision-Recall curves
- Designing experiments (and pitfalls)

---

## 1. Why Evaluation Matters

> [!example] The N-rays cautionary tale
> In 1903 Prosper-René Blondlot "discovered" N-rays while attempting to polarise x-rays. Many tried to replicate; some failed. Physicist Robert W. Wood visited the lab, **secretly removed/swapped elements of the apparatus — yet N-rays were still "observed"**. He published in *Nature* calling them a subjective phenomenon.
>
> **Lesson:** evaluation experiments must be designed to give an *accurate* estimate of how a model performs when deployed. **The data used to evaluate must not be the same as the data used to train.**

**Evaluation measures answer:** How are we doing? Is System A better than System B? Which model suits this task?

- A measure of how (in)accurate a system is on a task.
- **Error/accuracy is often *not* the best measure** — the appropriate measure helps select the best algorithm.
- **Model skill** = once the measures are chosen, the ML approach that *maximises* them is the best.

---

## 2. What is "Best" Performance?

No model is perfect — some fraction of predictions will be wrong, and **the way it is wrong matters**.

| Context | What matters |
|---|---|
| Medical diagnosis | High accuracy; **a sick person must never be misdiagnosed as healthy** (misses unforgivable) |
| Advertising response | Only needs to be *slightly better than random* to be profitable |

Other considerations beyond accuracy:

- How **quickly** the model predicts.
- How **easy** predictions are for human analysts to understand.
- How **easy** it is to retrain so the model doesn't go stale.

---

## 3. Cross-Validation

> [!abstract] Definition
> Cross-validation checks how a model performs on **unseen data**: split data into parts, train on some, test on the rest, repeat, and **average the results**. Main purpose: **prevent overfitting** — ensure the model generalises, not just memorises.

**Ways to split train/test:**

| Method | Description |
|---|---|
| **Hold-out** | Single split, e.g. 50% train / 50% test |
| **K-Fold CV** | Data split into $k$ folds; train on $k-1$, test on the remaining, repeat for every fold, average |
| **Leave-One-Out (LOO)** | Train on the whole dataset, test on a single left-out point; **iterate over every point** |
| **Stratified CV** | For multi-class: each fold keeps the same **class proportions** as the full dataset |

> [!warning] Peeking
> Test data must be **unseen** during training. A model tested on data it has already seen performs suspiciously well — that's "peeking", and it tells you nothing about generalisation.

---

## 4. The Confusion Matrix

For 2-class (binary) problems you pick one class to be **positive**, the other **negative**.

```
                  All Testing Instances
                 Predict Positive?
                 Yes      No
 Really    Yes |  TP     FN    |
 Positive?   No |  FP     TN    |
```

- **TP** — True Positive: predicted +, really +
- **TN** — True Negative: predicted -, really -
- **FP** — False Positive: predicted +, really - (false alarm)
- **FN** — False Negative: predicted -, really + (miss)

> [!tip] We want a **large diagonal (TP, TN)** with **small off-diagonal (FP, FN)**.

---

## 5. Accuracy & Classification Error

$$Accuracy = \frac{Correct}{Total} = \frac{TP + TN}{TP + TN + FP + FN}$$

$$Classification\ error = \frac{Errors}{Total} = \frac{FP + FN}{TP + TN + FP + FN} = 1 - Accuracy$$

> [!warning] Accuracy is misleading on imbalanced data
> A dataset that is 90% class A / 10% class B: a model that **always predicts A hits 90% accuracy** but never identifies any B. Accuracy gives a false sense of success (a "False Positive sense of high accuracy").

---

## 6. Precision & Recall

$$Precision = \frac{TP}{TP + FP}$$

> "How many of the *positives we predicted* are actually positive."
> Used when **false positives are costly** (e.g. diagnosing a disease that isn't there).

$$Recall = Sensitivity = True\ Positive\ Rate = \frac{TP}{TP + FN}$$

> "How many of the *actual positives* we caught."
> Used when **missing a positive (false negative) is costly** (e.g. disease detection).

---

## 7. F1 Score & Log Loss

$$F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}$$

- Harmonic mean of precision & recall; balances both into a single number in $[0,1]$.

$$LogLoss = -\frac{1}{N} \sum_{i=1}^{N}\sum_{j=1}^{M} y_{ij} \cdot \log(p_{ij})$$

- Measures **uncertainty** of the predictions; penalises low probabilities assigned to correct classes. Works for multi-class.

---

## 8. Misses and False Alarms

$$False\ Alarm\ Rate = False\ Positive\ Rate\ (FPR) = \frac{FP}{FP + TN}$$

- % of **negatives** misclassified as positives.

$$Miss\ Rate = False\ Negative\ Rate\ (FNR) = \frac{FN}{TP + FN}$$

- % of **positives** misclassified as negatives. Note $Recall = 1 - Miss\ Rate$ (they share denominator $TP + FN$).

> [!danger] Meaningless to report only one of these
> Predict *everything* positive → 100% recall but huge false-alarm rate. Predict *everything* negative → 0% false alarms but catch nothing.
> **Always report a pair:** Recall/Precision, Miss/FA rate, or TP/FP rate.

---

## 9. Thresholds & ROC Curves

**Thresholds:** many algorithms output a *confidence* $f(x)$, then a threshold $t$ decides:

- Naïve Bayes: spam if $P(spam|x) > 0.5$
- Linear / Logistic / SVM: $w^Tx > 0$
- Decision tree: $p \ge 0.75$

> [!note] Misleading comparison
> "System A: TP 50%, FP 20% — System B: TP 100%, FP 60% — which is better?" A and B could be the **same system at different thresholds**. Threshold-agnostic curves (ROC/PR) fix this.

### The ROC Curve

**Receiver Operating Characteristic:** TPR vs FPR across **all thresholds** (plots the two rates in §8):

$$TPR = \frac{TP}{TP + FN} \qquad FPR = \frac{FP}{FP + TN}$$

**Worked example — 12 test points** (8 positive, 4 negative) ranked by $f(x)$, threshold $t$ swept left→right:

| $t$ position | TPR | FPR |
|---|---|---|
| Very left ($t=0$) | $8/8 = 1.0$ | $4/4 = 1.0$ |
| Raising $t$ past 1 negative | $8/8 = 1.0$ | $3/4 = 0.75$ |
| $t$ past all negatives | $8/8 = 1.0$ | $0/4 = 0$ |
| Then past each positive | $7/8,\ 3/8,\ \dots,\ 0$ | $0$ |

- **Ideal classifier** ROC: an L — straight up the TPR axis then right (TPR=1 with FPR=0), AUC = 1.
- **Chance classification** = the diagonal (AUC = 0.5).
- **Realistic** curve sits between; **AUC** (area under curve, 0–1) summarises it as one number.

**Benefits of ROC (from lecture):**

1. **Threshold independence** — shows performance at *all* thresholds, not one arbitrary $t$.
2. **Model comparison** — closer to the top-left corner = better; AUC gives a single comparable number.
3. **Handles class imbalance** — based on TPR/FPR, not accuracy (which lies on imbalanced data).
4. **Comprehensive** — reveals strengths/weaknesses across thresholds (steep start = good detection, few false alarms).
5. **Visual intuition** for trade-offs in medical diagnosis / fraud detection.

---

## 10. Precision-Recall (PR) Curves

Alternative threshold-independent view: **Precision (y) vs Recall (x)**. Recall here = TPR from the ROC curve.

**Worked example, same 12 points:**

| TP | FP | Recall $TP/(TP+FN)$ | Precision $TP/(TP+FP)$ |
|---|---|---|---|
| 8 | 4 | 1.0 | $8/12 = 0.67$ |
| 8 | 3 | 1.0 | $8/11 = 0.73$ |
| 8 | 0 | 1.0 | $8/8 = 1.0$ |
| 7 | 0 | $7/8 = .875$ | $7/7 = 1.0$ |
| 3 | 0 | $3/8 = .375$ | $3/3 = 1.0$ |
| 0 | 0 | $0/8 = 0$ | $0/0 =$ **Undefined*** |

- Ideal PR curve hugs the top-right; realistic ones drop off at high recall.
- **Average Precision (AP)** = area under the PR curve (the PR equivalent of AUC), compressing it to one number.

> [!tip] ROC vs PR — when to use which
> - ROC can look **overly optimistic** when negatives vastly outnumber positives: FPR's denominator $(TN+FP)$ is dominated by the huge negative class, so FPR stays low even when FP is large.
> - PR has **no such blind spot**: Precision's denominator $(TP+FP)$ only involves *predicted* positives, so it's sensitive to false alarms relative to true detections.
> - **Rule of thumb:** balanced classes → ROC is fine; **rare positive class** (fraud detection, disease screening, spam) → PR gives a more honest picture.
> - Both are threshold-independent; both compress to a single number (AUC vs AP).

---

## 11. Further Reading

- Datacamp: ["Understanding Logistic Regression in Python"](https://www.datacamp.com/tutorial/understanding-logistic-regression-python) — the lecture's binary classification example.

---

> [!tip] Next lecture
> Fill in the `next` field in frontmatter once the next notes arrive.