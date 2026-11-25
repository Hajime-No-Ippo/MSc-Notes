---
tags: [cs401, machine-learning, cnn, cifar-10, assignment, lecture-notes]
module: CS401
topic: "Machine Learning — CA2 CNN Implementation & Evaluation"
date: 2026-11-25
next: "[[]]"
prev: "[[2026-10-12 - Evaluation Measures]]"
---

# Machine Learning — CA2 CNN Implementation & Evaluation

> [!info] Continuous Assessment 2 — due 2026-12-06 23:59
> CS401 Machine Learning and Neural Networks · Dr. Cathy Ennis
> Source: `CS401 CA2.pdf` + `CA_CNN_template.ipynb` (template) · `Week 7 CNN MNIST-Start.ipynb` (class lab reference)
> Worth **10%** of final mark, graded out of **100**. Submit **one** Jupyter notebook (`.ipynb`).

**Overview**

- Implement, train, and evaluate a **Convolutional Neural Network** for object classification on **CIFAR-10**, then run experiments to build intuition for how architecture and training choices affect performance.
- **Task 1** (40 pts): a standard working CNN.
- **Task 2** (60 pts): 4 experiments of your choice + a mandatory conv-layer visualisation.
- Both **code** and **written interpretation** are required — code without explanation, or explanation without working code, cannot get full marks on any task.

---

## 1. Dataset & Environment

| Item | Detail |
|---|---|
| Dataset | **CIFAR-10** (from its official webpage) |
| Resource fallback | May use only the first training batch `data_batch_1` |
| Size | 60,000 32×32 RGB images, 10 classes |
| Framework | TensorFlow/Keras or PyTorch (your choice) |

---

## 2. Submission Rules

- Use the provided template `CA_CNN_template.ipynb`; keep every tagged header `[CNN-...]` as written.
- Add code + explanation under each header; extra cells allowed, but don't move content between sections.
- Name, student ID, and programme code go in the title cell.
- The notebook must run **top-to-bottom** with no external files or filename changes; run it before submitting so output cells are complete (incomplete outputs may forfeit marks).
- Interpretation answers are capped at the stated word limit — a cohesive, specific answer beats a long, vague one (the limit is a cap, not a target).

---

## 3. Task 1 — Implement a Standard CNN (40 pts)

| Tag | Task | Pts | Word cap |
|---|---|---|---|
| `[CNN-T1a]` | **Data Load + Prep** — load CIFAR-10, explain the features, prepare data (format, normalisation) | 8 | — |
| `[CNN-T1b]` | **Propose Architecture** — propose a CNN architecture appropriate for CIFAR-10 (justified by data examination + class material) | 8 | — |
| `[CNN-T1c]` | **Train and Test** — define & fit the CNN, justifying initial training decisions (learning rate, optimiser, split) | 8 | 75 words |
| `[CNN-T1d]` | **Explaining Results** — plot training & validation loss; interpret | 16 | 150 words |

---

## 4. Task 2 — Experimentation (60 pts)

Pick **any 4 of the 6** experiments (10 pts each). Say clearly which 4 you're doing — don't attempt all 6 (extra ones aren't marked).

| Tag | Experiment | Word cap |
|---|---|---|
| `[CNN-T2a]` | **Convolutional Layers** — change the number of conv layers (e.g. double) | 75 |
| `[CNN-T2b]` | **Kernel Size** — change the kernel size | 75 |
| `[CNN-T2c]` | **Learning Rate** — try two alternative LRs | 75 |
| `[CNN-T2d]` | **Activation Function** — alternative (ReLU, Tanh) | 75 |
| `[CNN-T2e]` | **Optimiser** — alternative optimiser | 75 |
| `[CNN-T2f]` | **Batch Size** — try 4, 32, 256 | 75 |

### Always required (regardless of the 4 picked)

| Tag | Task | Pts | Word cap |
|---|---|---|---|
| `[CNN-T2g]` | **Visualisation of Convolutional Layers** — visualise & explain the output of each conv layer for a sample test image, each channel as a grayscale image | 20 | 150 |

---

## 5. Rubric Summary

| Section | Points |
|---|---|
| T1a Data load + prep | 8 |
| T1b Propose architecture | 8 |
| T1c Train & test | 8 |
| T1d Explain results | 16 |
| T2a–T2f (4 × 10) | 40 |
| T2g Conv-layer visualisation | 20 |
| **Total** | **100** |

---

## 6. Checklist

- [ ] Fill name / student ID / programme code in the title cell
- [ ] `[CNN-T1a]` load CIFAR-10 + normalise + explain features
- [ ] `[CNN-T1b]` propose architecture
- [ ] `[CNN-T1c]` train & test (justify LR / optimiser / split, ≤75 words)
- [ ] `[CNN-T1d]` plot train vs validation loss (≤150 words)
- [ ] Choose 4 of the 6 experiments, state them clearly
- [ ] `[CNN-T2g]` conv-layer channel visualisation (≤150 words)
- [ ] Run notebook top-to-bottom, outputs rendered
- [ ] Submit single `.ipynb` by 6 Dec 23:59

> [!tip] Next lecture
> Fill in the `next` field in frontmatter once the next notes arrive.
