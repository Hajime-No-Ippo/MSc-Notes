# Linear Regression Implementations — CS401

From-scratch implementations of Linear Regression, matching the lecture notes.

## Files

| File | Language | Method | Description |
|---|---|---|---|
| `linear_regression.py` | Python | Gradient Descent | From scratch, no ML libraries |
| `LinearRegression.java` | Java | Gradient Descent | From scratch, no ML libraries |
| `normal_equation.py` | Python | Normal Equation | Closed-form solution using NumPy |

## Running

```bash
# Python
python linear_regression.py
python normal_equation.py

# Java
javac LinearRegression.java && java LinearRegression
```

## What's Inside

- **Hypothesis**: h(x) = θ₀ + θ₁x
- **Loss**: Mean Squared Error J(θ) = (1/n) Σ(h(xᵢ) - yᵢ)²
- **Gradient Descent**: θⱼ := θⱼ - α · ∂J/∂θⱼ
- **Normal Equation**: θ = (XᵀX)⁻¹Xᵀy

## Training Data

Living area (m²) → Price (€k):

| Area | 50 | 60 | 70 | 80 | 90 | 100 | 110 | 120 | 130 | 140 |
|---|---|---|---|---|---|---|---|---|---|---|
| Price | 150 | 180 | 210 | 240 | 270 | 300 | 330 | 360 | 390 | 420 |
