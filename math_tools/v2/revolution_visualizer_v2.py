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
    print("=== Revolution Visualizer v2 ===")
    print("v2 feature set: Disk + Washer methods around x-axis.")
    print("1) Disk method")
    print("2) Washer method")
    method = input("Choose method: ").strip()
    if method not in {"1", "2"}:
        print("Invalid method choice.")
        return

    a = read_float("Lower x bound a: ")
    b = read_float("Upper x bound b: ")
    if b <= a:
        print("Upper bound must be greater than lower bound.")
        return

    x = np.linspace(a, b, 160)
    theta = np.linspace(0, 2 * np.pi, 80)
    X, T = np.meshgrid(x, theta)

    if method == "1":
        expr = input("Enter y = f(x) for disk method: ").strip()
        y = evaluate_function(expr, x)
        Y, _ = np.meshgrid(y, theta)
        Yrot = Y * np.cos(T)
        Zrot = Y * np.sin(T)

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(X, Yrot, Zrot, cmap="viridis", alpha=0.85, edgecolor="k", linewidth=0.15)
        ax.plot([a, b], [0, 0], [0, 0], color="black", linewidth=2)
        ax.set_title("v2 Disk Method around x-axis")

    else:
        outer_expr = input("Enter OUTER function y = f_outer(x): ").strip()
        inner_expr = input("Enter INNER function y = f_inner(x): ").strip()
        outer_y = evaluate_function(outer_expr, x)
        inner_y = evaluate_function(inner_expr, x)

        Yo, _ = np.meshgrid(outer_y, theta)
        Yi, _ = np.meshgrid(inner_y, theta)
        Yo_rot = Yo * np.cos(T)
        Zo_rot = Yo * np.sin(T)
        Yi_rot = Yi * np.cos(T)
        Zi_rot = Yi * np.sin(T)

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(X, Yo_rot, Zo_rot, cmap="viridis", alpha=0.82, edgecolor="k", linewidth=0.12)
        ax.plot_surface(X, Yi_rot, Zi_rot, cmap="plasma", alpha=0.55, edgecolor="k", linewidth=0.10)
        ax.plot([a, b], [0, 0], [0, 0], color="black", linewidth=2)
        ax.set_title("v2 Washer Method around x-axis")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
