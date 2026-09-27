---
tags: [cs401, ml, neural-networks, lecture-notes]
module: CS401
topic: "ML & Neural Networks — Foundations"
date: 2026-09-21
next: "[[]]"
prev: ""
---

# ML & Neural Networks — Foundations

> [!info] Lecture 1 — 2026-09-21
> CS401 Machine Learning and Neural Networks

## What is ML?

- **Machine Learning** is a subset of [[AI]] (Artificial Intelligence)
- Hierarchy: **AI → ML → Neural Networks**
- ML → branch of AI that learns patterns from data

```mermaid
graph TD
    A[AI] --> B[ML]
    B --> C[Neural Networks]
    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#bfb,stroke:#333
```

## Core Pipeline

```mermaid
graph LR
    D[(DATA)] --> A[ML Algorithm]
    A --> P[Prediction Model]
    style D fill:#ff9,stroke:#333
    style A fill:#f9f,stroke:#333
    style P fill:#9f9,stroke:#333
```

```
┌─────────┐      ┌──────────────┐      ┌─────────────────┐
│  DATA   │ ───▶ │ ML Algorithm │ ───▶ │ Prediction Model│
└─────────┘      └──────────────┘      └─────────────────┘
```

## Key References

- **Andrew Ng** — prominent ML educator
- **Tom Mitchell** — *Machine Learning* (textbook)
- **Jugal Kalita** — *ML Learning Theory and Practice*

## ML Tasks

- Data exploration
- Data summary / description

## History

- **1949** — Donald Hebb (*Hebbian learning* — foundational to neural networks)

## Input–Output Framework

```mermaid
graph LR
    I[Input] --> M[ML]
    M --> O[Output]
    M -.-> U[Unsupervised / Semi / RL]
    style I fill:#ff9,stroke:#333
    style M fill:#f9f,stroke:#333
    style O fill:#9f9,stroke:#333
```

Learning types:
- **Unsupervised** — no labels
- **Semi-supervised** — partial labels
- **Reinforcement Learning (RL)** — reward-based

### Statistics ↔ ML relationship

```
 ┌───────────┐     ┌───────────┐
 │Statistics │◄───►│    ML     │
 └───────────┘     └───────────┘
       ▲                 ▲
       └────────┬────────┘
          Dynamic Programming
```

## Related Fields

| Field | Relevance to ML |
|---|---|
| Statistics | Probability, distributions, inference |
| Dynamic Programming | Optimisation, sequence problems |
| State Transmission | Modelling state changes |
| Data Mining | Pattern discovery in large datasets |

## Application Example

- ML on tracking health conditions

## Supervised vs Unsupervised Learning

### Supervised Learning

- Uses **labelled** data: features (x) → target (y)
- Tasks: classification, regression
- Example: predicting outcomes from known input-output pairs

```
  y│    ×  ×
   │  ×
   │        ○  ○
   │      ○
   └──────────── x
   (known labels guide the model)
```

### Unsupervised Learning

- Uses **unlabelled** data
- Tasks: clustering, dimensionality reduction
- Example: **customer segmentation** (grouping similar customers)

```
  y│   (○○)    (××)
   │   (○○)    (××)
   │
   └──────────── x
   (no labels — algorithm finds clusters)
```

## Reinforcement Learning (RL)

```mermaid
graph LR
    A[Agent] -->|Action A₁| E[Environment]
    E -->|State S₁| A
    E -->|Reward R| A
    style A fill:#f9f,stroke:#333
    style E fill:#ff9,stroke:#333
```

```
        ┌─────────┐    Action (A₁)    ┌─────────────┐
        │  Agent  │ ───────────────▶  │ Environment │
        └─────────┘                    └─────────────┘
             ▲                              │
             │        State (S₁)            │
             └──────────────────────────────┘
                        ▲
                        │  Reward (R)
```

- Agent takes actions in an environment
- Receives **reward** signals
- Learns a policy to maximise cumulative reward

---

> [!tip] Next lecture
> Fill in the `next` field in frontmatter once the next notes arrive.
