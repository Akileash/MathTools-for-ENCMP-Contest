import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed by Matplotlib 3D backend)


SAMPLES_ALONG_INTERVAL = 180
SAMPLES_AROUND_AXIS = 80


def safe_eval_expression(expr, parameter_values, parameter_name):
    """
    Evaluate user math expression with a tightly controlled namespace.
    Allowed variable is parameter_name (x or y), plus common numpy math functions.
    """
    allowed = {
        "np": np,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "arcsin": np.arcsin,
        "arccos": np.arccos,
        "arctan": np.arctan,
        "sinh": np.sinh,
        "cosh": np.cosh,
        "tanh": np.tanh,
        "exp": np.exp,
        "log": np.log,
        "sqrt": np.sqrt,
        "abs": np.abs,
        "pi": np.pi,
        "e": np.e,
    }

    local_scope = dict(allowed)
    local_scope[parameter_name] = parameter_values

    try:
        evaluated = eval(expr, {"__builtins__": {}}, local_scope)
    except Exception as exc:
        raise ValueError(f"Could not evaluate expression '{expr}'. Details: {exc}")

    arr = np.array(evaluated, dtype=float)
    if arr.ndim == 0:
        arr = np.full_like(parameter_values, float(arr), dtype=float)
    if arr.shape != parameter_values.shape:
        raise ValueError(
            "Expression output shape does not match sampled input values. "
            "Use vectorized numpy-style expressions."
        )
    return arr


def read_float(prompt_text):
    while True:
        raw = input(prompt_text).strip()
        try:
            return float(raw)
        except ValueError:
            print("Invalid input. Please enter a real number.")


def choose_menu_option(prompt_text, valid_options):
    valid_set = {str(v) for v in valid_options}
    while True:
        choice = input(prompt_text).strip()
        if choice in valid_set:
            return choice
        print(f"Invalid option. Choose one of: {', '.join(sorted(valid_set))}")


def read_expression_values(prompt_text, parameter_values, parameter_name):
    """Prompt until a valid expression is entered for the required parameter."""
    while True:
        expr = input(prompt_text).strip()
        try:
            values = safe_eval_expression(expr, parameter_values, parameter_name)
            return expr, values
        except ValueError as err:
            print(f"\nInput error: {err}")
            print(
                f"Please try again. For this setup, use '{parameter_name}' as the variable "
                f"(not the other axis variable)."
            )
            if parameter_name == "x":
                print("Example inputs: x**2, np.sin(x), 2*x + 1")
            else:
                print("Example inputs: y**2, np.sin(y), 2*y + 1")


def get_bounds(axis_kind):
    if axis_kind in ("x-axis", "y=c"):
        print("\nEnter x-limits for the interval [a, b].")
    else:
        print("\nEnter y-limits for the interval [a, b].")

    while True:
        a = read_float("Lower bound a: ")
        b = read_float("Upper bound b: ")
        if b > a:
            return a, b
        print("Upper bound must be greater than lower bound.")


def build_horizontal_surface_xaxis_like(
    parameter_values,
    function_values,
    axis_constant,
    theta_grid,
):
    """
    Build revolution surface for horizontal axis y = axis_constant.
    Parameter is x, function is y = f(x).
    """
    x_grid, t_grid = np.meshgrid(parameter_values, theta_grid)
    f_grid, _ = np.meshgrid(function_values, theta_grid)
    radius = np.abs(f_grid - axis_constant)

    X = x_grid
    Y = axis_constant + radius * np.cos(t_grid)
    Z = radius * np.sin(t_grid)
    return X, Y, Z


def build_vertical_surface_yaxis_like(
    parameter_values,
    function_values,
    axis_constant,
    theta_grid,
):
    """
    Build revolution surface for vertical axis x = axis_constant.
    Parameter is y, function is x = f(y).
    """
    y_grid, t_grid = np.meshgrid(parameter_values, theta_grid)
    f_grid, _ = np.meshgrid(function_values, theta_grid)
    radius = np.abs(f_grid - axis_constant)

    X = axis_constant + radius * np.cos(t_grid)
    Y = y_grid
    Z = radius * np.sin(t_grid)
    return X, Y, Z


def plot_surfaces(
    axis_choice_label,
    method_label,
    axis_kind,
    axis_constant,
    surfaces,
    axis_line_points,
):
    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Draw each boundary surface (outer and, for washers, inner).
    for i, (X, Y, Z, cmap_name, alpha_value, legend_name) in enumerate(surfaces):
        ax.plot_surface(
            X,
            Y,
            Z,
            cmap=cmap_name,
            alpha=alpha_value,
            edgecolor="k",
            linewidth=0.15,
            antialiased=True,
            label=legend_name if i == 0 else None,
        )

    # Draw a translucent reference plane containing the axis of rotation.
    x_min = min(np.min(surface[0]) for surface in surfaces)
    x_max = max(np.max(surface[0]) for surface in surfaces)
    y_min = min(np.min(surface[1]) for surface in surfaces)
    y_max = max(np.max(surface[1]) for surface in surfaces)
    z_min = min(np.min(surface[2]) for surface in surfaces)
    z_max = max(np.max(surface[2]) for surface in surfaces)

    if axis_kind in ("x-axis", "y=c"):
        x_plane = np.linspace(x_min, x_max, 50)
        z_plane = np.linspace(z_min, z_max, 50)
        Xp, Zp = np.meshgrid(x_plane, z_plane)
        Yp = np.full_like(Xp, axis_constant, dtype=float)
        ax.plot_surface(Xp, Yp, Zp, color="gray", alpha=0.18, edgecolor="none")
    else:
        y_plane = np.linspace(y_min, y_max, 50)
        z_plane = np.linspace(z_min, z_max, 50)
        Yp, Zp = np.meshgrid(y_plane, z_plane)
        Xp = np.full_like(Yp, axis_constant, dtype=float)
        ax.plot_surface(Xp, Yp, Zp, color="gray", alpha=0.18, edgecolor="none")

    ax.plot(
        axis_line_points[0],
        axis_line_points[1],
        axis_line_points[2],
        color="black",
        linewidth=2.0,
    )

    ax.set_title(f"Solid of Revolution ({method_label}) around {axis_choice_label}")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(elev=25, azim=40)
    plt.tight_layout()
    plt.show()


def main():
    print("=== Solids of Revolution 3D Visualizer ===")
    print("This tool visualizes solids formed using disk/washer-style boundaries.")

    print("\nChoose method:")
    print("1) Disk Method (single boundary function)")
    print("2) Washer Method (outer and inner boundary functions)")
    method_choice = choose_menu_option("Method: ", {"1", "2"})
    method_label = "Disk Method" if method_choice == "1" else "Washer Method"

    print("\nChoose axis of revolution:")
    print("1) x-axis")
    print("2) y-axis")
    print("3) x = c (vertical line)")
    print("4) y = c (horizontal line)")
    axis_choice = choose_menu_option("Axis: ", {"1", "2", "3", "4"})

    axis_label = ""
    axis_constant = 0.0
    if axis_choice == "1":
        axis_label = "x-axis"
        axis_constant = 0.0
    elif axis_choice == "2":
        axis_label = "y-axis"
        axis_constant = 0.0
    elif axis_choice == "3":
        axis_constant = read_float("Enter constant c for axis x = c: ")
        axis_label = f"x = {axis_constant}"
    else:
        axis_constant = read_float("Enter constant c for axis y = c: ")
        axis_label = f"y = {axis_constant}"

    # Horizontal axes use y = f(x). Vertical axes use x = f(y).
    axis_kind = "x-axis" if axis_choice == "1" else "y-axis" if axis_choice == "2" else "x=c" if axis_choice == "3" else "y=c"
    lower, upper = get_bounds(axis_kind)
    param = np.linspace(lower, upper, SAMPLES_ALONG_INTERVAL)
    theta = np.linspace(0.0, 2.0 * np.pi, SAMPLES_AROUND_AXIS)

    if axis_kind in ("x-axis", "y=c"):
        variable_name = "x"
        if method_choice == "1":
            prompt_one = "Enter function y = f(x) using x (example: x**2 or np.sin(x)): "
            _, f_vals = read_expression_values(prompt_one, param, variable_name)

            X, Y, Z = build_horizontal_surface_xaxis_like(param, f_vals, axis_constant, theta)
            axis_line_x = np.linspace(lower, upper, 2)
            axis_line_y = np.full(2, axis_constant)
            axis_line_z = np.zeros(2)
            surfaces = [(X, Y, Z, "viridis", 0.85, "Boundary surface")]

        else:
            _, outer_vals = read_expression_values(
                "Enter OUTER function y = f_outer(x): ", param, variable_name
            )
            _, inner_vals = read_expression_values(
                "Enter INNER function y = f_inner(x): ", param, variable_name
            )

            outer_radius = np.abs(outer_vals - axis_constant)
            inner_radius = np.abs(inner_vals - axis_constant)
            if np.mean(outer_radius - inner_radius) < 0:
                print("Note: Swapping outer and inner functions based on average radius.")
                outer_vals, inner_vals = inner_vals, outer_vals

            Xo, Yo, Zo = build_horizontal_surface_xaxis_like(param, outer_vals, axis_constant, theta)
            Xi, Yi, Zi = build_horizontal_surface_xaxis_like(param, inner_vals, axis_constant, theta)
            axis_line_x = np.linspace(lower, upper, 2)
            axis_line_y = np.full(2, axis_constant)
            axis_line_z = np.zeros(2)
            surfaces = [
                (Xo, Yo, Zo, "viridis", 0.82, "Outer boundary"),
                (Xi, Yi, Zi, "plasma", 0.55, "Inner boundary"),
            ]

    else:
        variable_name = "y"
        if method_choice == "1":
            prompt_one = "Enter function x = f(y) using y (example: y**2 or np.sin(y)): "
            _, f_vals = read_expression_values(prompt_one, param, variable_name)

            X, Y, Z = build_vertical_surface_yaxis_like(param, f_vals, axis_constant, theta)
            axis_line_x = np.full(2, axis_constant)
            axis_line_y = np.linspace(lower, upper, 2)
            axis_line_z = np.zeros(2)
            surfaces = [(X, Y, Z, "viridis", 0.85, "Boundary surface")]

        else:
            _, outer_vals = read_expression_values(
                "Enter OUTER function x = f_outer(y): ", param, variable_name
            )
            _, inner_vals = read_expression_values(
                "Enter INNER function x = f_inner(y): ", param, variable_name
            )

            outer_radius = np.abs(outer_vals - axis_constant)
            inner_radius = np.abs(inner_vals - axis_constant)
            if np.mean(outer_radius - inner_radius) < 0:
                print("Note: Swapping outer and inner functions based on average radius.")
                outer_vals, inner_vals = inner_vals, outer_vals

            Xo, Yo, Zo = build_vertical_surface_yaxis_like(param, outer_vals, axis_constant, theta)
            Xi, Yi, Zi = build_vertical_surface_yaxis_like(param, inner_vals, axis_constant, theta)
            axis_line_x = np.full(2, axis_constant)
            axis_line_y = np.linspace(lower, upper, 2)
            axis_line_z = np.zeros(2)
            surfaces = [
                (Xo, Yo, Zo, "viridis", 0.82, "Outer boundary"),
                (Xi, Yi, Zi, "plasma", 0.55, "Inner boundary"),
            ]

    plot_surfaces(
        axis_choice_label=axis_label,
        method_label=method_label,
        axis_kind=axis_kind,
        axis_constant=axis_constant,
        surfaces=surfaces,
        axis_line_points=(axis_line_x, axis_line_y, axis_line_z),
    )


if __name__ == "__main__":
    main()
