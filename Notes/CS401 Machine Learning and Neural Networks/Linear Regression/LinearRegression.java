/**
 * Linear Regression with Gradient Descent — CS401
 * From scratch, no ML libraries.
 */
public class LinearRegression {

    // Training data: Living area (m²) → Price (€k)
    static double[] X = {50, 60, 70, 80, 90, 100, 110, 120, 130, 140};
    static double[] Y = {150, 180, 210, 240, 270, 300, 330, 360, 390, 420};
    static int n = X.length;

    /** h(x) = theta0 + theta1 * x */
    static double predict(double x, double theta0, double theta1) {
        return theta0 + theta1 * x;
    }

    /** J(theta0, theta1) = (1/n) * sum((h(x_i) - y_i)^2) */
    static double computeLoss(double theta0, double theta1) {
        double total = 0;
        for (int i = 0; i < n; i++) {
            double yPred = predict(X[i], theta0, theta1);
            total += Math.pow(yPred - Y[i], 2);
        }
        return total / n;
    }

    /** Gradient Descent */
    static double[] gradientDescent(double lr, int iterations) {
        double theta0 = 0;
        double theta1 = 0;

        for (int iter = 0; iter < iterations; iter++) {
            double grad0 = 0;
            double grad1 = 0;

            for (int i = 0; i < n; i++) {
                double yPred = predict(X[i], theta0, theta1);
                double error = yPred - Y[i];
                grad0 += error;
                grad1 += error * X[i];
            }

            grad0 /= n;
            grad1 /= n;

            theta0 -= lr * grad0;
            theta1 -= lr * grad1;

            if (iter % 200 == 0) {
                double loss = computeLoss(theta0, theta1);
                System.out.printf("Iter %4d | Loss: %10.2f | theta0: %.4f | theta1: %.6f%n",
                        iter, loss, theta0, theta1);
            }
        }

        return new double[]{theta0, theta1};
    }

    public static void main(String[] args) {
        System.out.println("============================================================");
        System.out.println("Linear Regression — Gradient Descent (Java)");
        System.out.println("============================================================");
        System.out.printf("Training data: %d examples%n", n);
        System.out.print("X (area m²): ");
        for (double x : X) System.out.print((int) x + " ");
        System.out.println();
        System.out.print("Y (price €k): ");
        for (double y : Y) System.out.print((int) y + " ");
        System.out.println();
        System.out.println();

        double[] theta = gradientDescent(0.00001, 2000);
        double theta0 = theta[0];
        double theta1 = theta[1];

        System.out.println();
        System.out.println("============================================================");
        System.out.printf("Result: h(x) = %.2f + %.4f * x%n", theta0, theta1);
        System.out.printf("Final loss: %.2f%n", computeLoss(theta0, theta1));
        System.out.println("============================================================");

        // Predictions
        System.out.println();
        System.out.printf("%10s | %12s | %14s%n", "Area (m²)", "Actual (€k)", "Predicted (€k)");
        System.out.println("-".repeat(42));
        for (int i = 0; i < n; i++) {
            double yPred = predict(X[i], theta0, theta1);
            System.out.printf("%10.0f | %12.0f | %14.2f%n", X[i], Y[i], yPred);
        }

        // Predict new value
        System.out.println();
        double newArea = 150;
        double predictedPrice = predict(newArea, theta0, theta1);
        System.out.printf("New prediction: %.0f m² → %.2f €k%n", newArea, predictedPrice);
    }
}
