import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


def read_float(prompt):
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Please enter a valid number.")


def evaluate_function(expr, x_values):
    safe = {"np": np, "sin": np.sin, "cos": np.cos, "sqrt": np.sqrt, "pi": np.pi, "x": x_values}
    return np.array(eval(expr, {"__builtins__": {}}, safe), dtype=float)


def main():
    print("=== Solids of Revolution v1 ===")
    print("Visualize DISK METHOD around the x-axis")
    expr = input("Enter y = f(x) (example: x**2 or np.sin(x)): ").strip()
    a = read_float("Lower x bound a: ")
    b = read_float("Upper x bound b: ")
    if b <= a:
        print("Upper bound must be greater than lower bound.")
        return

    x = np.linspace(a, b, 160)
    theta = np.linspace(0, 2 * np.pi, 80)
    y = evaluate_function(expr, x)

    X, T = np.meshgrid(x, theta)
    Y, _ = np.meshgrid(y, theta)
    Z = Y * np.sin(T)
    Yrot = Y * np.cos(T)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Yrot, Z, cmap="viridis", alpha=0.85, edgecolor="k", linewidth=0.15)
    ax.plot([a, b], [0, 0], [0, 0], color="black", linewidth=2)
    ax.set_title("v1 Disk Method around x-axis")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
