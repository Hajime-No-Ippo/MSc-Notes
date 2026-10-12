"""
Linear Regression with Gradient Descent — CS401
From scratch, no ML libraries.
"""

import random

# ---- Training Data ----
# Living area (m²) → Price (€k)
X = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140]
Y = [150, 180, 210, 240, 270, 300, 330, 360, 390, 420]

n = len(X)


# ---- Hypothesis ----
def predict(x, theta0, theta1):
    """h(x) = theta0 + theta1 * x"""
    return theta0 + theta1 * x


# ---- Loss Function (MSE) ----
def compute_loss(theta0, theta1):
    """J(theta0, theta1) = (1/n) * sum((h(x_i) - y_i)^2)"""
    total = 0
    for i in range(n):
        y_pred = predict(X[i], theta0, theta1)
        total += (y_pred - Y[i]) ** 2
    return total / n


# ---- Evaluation Metrics ----
def mae(theta0, theta1):
    """Mean Absolute Error = (1/n) * sum(|h(x_i) - y_i|)"""
    total = 0
    for i in range(n):
        total += abs(predict(X[i], theta0, theta1) - Y[i])
    return total / n


def rmse(theta0, theta1):
    """Root Mean Squared Error = sqrt((1/n) * sum((h(x_i) - y_i)^2))"""
    return compute_loss(theta0, theta1) ** 0.5


# ---- Gradient Descent ----
def gradient_descent(lr=0.00001, iterations=1000):
    theta0 = 0  # bias
    theta1 = 0  # weight

    for iteration in range(iterations):
        # Compute gradients
        grad0 = 0  # dJ/dtheta0
        grad1 = 0  # dJ/dtheta1

        for i in range(n):
            y_pred = predict(X[i], theta0, theta1)
            error = y_pred - Y[i]
            grad0 += error          # derivative w.r.t. theta0
            grad1 += error * X[i]   # derivative w.r.t. theta1

        grad0 /= n
        grad1 /= n

        # Update parameters
        theta0 -= lr * grad0
        theta1 -= lr * grad1

        # Print progress every 200 iterations
        if iteration % 200 == 0:
            loss = compute_loss(theta0, theta1)
            print(f"Iter {iteration:4d} | Loss: {loss:>10.2f} | theta0: {theta0:.4f} | theta1: {theta1:.6f}")

    return theta0, theta1


# ---- Main ----
if __name__ == "__main__":
    print("=" * 60)
    print("Linear Regression — Gradient Descent")
    print("=" * 60)
    print(f"Training data: {n} examples")
    print(f"X (area m²): {X}")
    print(f"Y (price €k): {Y}")
    print()

    theta0, theta1 = gradient_descent(lr=0.00001, iterations=2000)

    print()
    print("=" * 60)
    print(f"Result: h(x) = {theta0:.2f} + {theta1:.4f} * x")
    print(f"Final loss (MSE):  {compute_loss(theta0, theta1):.2f}")
    print(f"MAE:  {mae(theta0, theta1):.4f}")
    print(f"RMSE: {rmse(theta0, theta1):.4f}")
    print("=" * 60)

    # Predictions
    print()
    print("Predictions:")
    print(f"{'Area (m²)':>10} | {'Actual (€k)':>12} | {'Predicted (€k)':>14}")
    print("-" * 42)
    for x_val, y_val in zip(X, Y):
        y_pred = predict(x_val, theta0, theta1)
        print(f"{x_val:>10} | {y_val:>12} | {y_pred:>14.2f}")

    # Predict new value
    print()
    new_area = 150
    predicted_price = predict(new_area, theta0, theta1)
    print(f"New prediction: {new_area} m² → {predicted_price:.2f} €k")
