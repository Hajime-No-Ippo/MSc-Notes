"""
Normal Equation for Linear Regression — CS401
Closed-form solution: theta = (X^T X)^(-1) X^T y
"""
import numpy as np

# Training data
X = np.array([50, 60, 70, 80, 90, 100, 110, 120, 130, 140], dtype=float)
Y = np.array([150, 180, 210, 240, 270, 300, 330, 360, 390, 420], dtype=float)

# Add bias column (column of 1s)
X_b = np.column_stack([np.ones(len(X)), X])

# Normal Equation: theta = (X^T X)^(-1) X^T y
theta = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ Y

print("=" * 60)
print("Linear Regression — Normal Equation (closed-form)")
print("=" * 60)
print(f"theta0 (bias): {theta[0]:.4f}")
print(f"theta1 (slope): {theta[1]:.6f}")
print(f"Result: h(x) = {theta[0]:.2f} + {theta[1]:.4f} * x")
print()

# Predictions
print(f"{'Area (m²)':>10} | {'Actual (€k)':>12} | {'Predicted (€k)':>14}")
print("-" * 42)
for x_val, y_val in zip(X, Y):
    y_pred = theta[0] + theta[1] * x_val
    print(f"{x_val:>10.0f} | {y_val:>12.0f} | {y_pred:>14.2f}")

print()
new_area = 150
predicted_price = theta[0] + theta[1] * new_area
print(f"New prediction: {new_area} m² → {predicted_price:.2f} €k")
