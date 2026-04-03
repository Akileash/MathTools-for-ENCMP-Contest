def gcd(a, b):
    a = abs(a)
    b = abs(b)
    while b != 0:
        a, b = b, a % b
    return a if a != 0 else 1


class Rational:
    def __init__(self, numerator=0, denominator=1):
        if denominator == 0:
            raise ValueError("Denominator cannot be 0.")
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        if numerator == 0:
            self.n = 0
            self.d = 1
            return
        g = gcd(numerator, denominator)
        self.n = numerator // g
        self.d = denominator // g

    @staticmethod
    def from_string(token):
        text = token.strip()
        if not text:
            raise ValueError("Empty value is not valid.")
        if "/" in text:
            parts = text.split("/")
            if len(parts) != 2:
                raise ValueError(f"Invalid fraction format: {token}")
            num = int(parts[0].strip())
            den = int(parts[1].strip())
            return Rational(num, den)
        if "." in text:
            sign = -1 if text.startswith("-") else 1
            bare = text[1:] if text.startswith("-") else text
            pieces = bare.split(".")
            if len(pieces) != 2 or not pieces[0].isdigit() or not pieces[1].isdigit():
                raise ValueError(f"Invalid decimal format: {token}")
            integer_part = int(pieces[0]) if pieces[0] else 0
            frac_part = pieces[1]
            denominator = 10 ** len(frac_part)
            numerator = integer_part * denominator + int(frac_part)
            return Rational(sign * numerator, denominator)
        return Rational(int(text), 1)

    def __add__(self, other):
        return Rational(self.n * other.d + other.n * self.d, self.d * other.d)

    def __sub__(self, other):
        return Rational(self.n * other.d - other.n * self.d, self.d * other.d)

    def __mul__(self, other):
        return Rational(self.n * other.n, self.d * other.d)

    def __truediv__(self, other):
        if other.n == 0:
            raise ValueError("Division by zero is not allowed.")
        return Rational(self.n * other.d, self.d * other.n)

    def __neg__(self):
        return Rational(-self.n, self.d)

    def is_zero(self):
        return self.n == 0

    def abs_float(self):
        return abs(self.n / self.d)

    def __str__(self):
        if self.d == 1:
            return str(self.n)
        return f"{self.n}/{self.d}"


ZERO = Rational(0, 1)
ONE = Rational(1, 1)


def copy_matrix(matrix):
    return [[Rational(cell.n, cell.d) for cell in row] for row in matrix]


def matrix_shape(matrix):
    return len(matrix), len(matrix[0]) if matrix else 0


def format_matrix(matrix):
    """Format a matrix for clean terminal output using exact fractions."""
    if not matrix:
        return "[]"
    string_rows = [[str(cell) for cell in row] for row in matrix]
    widths = []
    for col in range(len(string_rows[0])):
        max_w = max(len(string_rows[row][col]) for row in range(len(string_rows)))
        widths.append(max_w)

    lines = []
    for row in string_rows:
        padded = [row[col].rjust(widths[col]) for col in range(len(row))]
        lines.append("[ " + "  ".join(padded) + " ]")
    return "\n".join(lines)


def select_pivot_row(mat, pivot_row, col):
    best_index = -1
    best_size = -1.0
    for r in range(pivot_row, len(mat)):
        if not mat[r][col].is_zero():
            size = mat[r][col].abs_float()
            if size > best_size:
                best_size = size
                best_index = r
    return best_index


def row_echelon_form(matrix):
    """Compute REF using exact Gaussian elimination on rationals."""
    mat = copy_matrix(matrix)
    rows, cols = matrix_shape(mat)
    pivot_row = 0

    for col in range(cols):
        if pivot_row >= rows:
            break
        max_index = select_pivot_row(mat, pivot_row, col)
        if max_index == -1:
            continue
        if max_index != pivot_row:
            mat[pivot_row], mat[max_index] = mat[max_index], mat[pivot_row]

        pivot_val = mat[pivot_row][col]
        for r in range(pivot_row + 1, rows):
            if mat[r][col].is_zero():
                continue
            factor = mat[r][col] / pivot_val
            for c in range(col, cols):
                mat[r][c] = mat[r][c] - factor * mat[pivot_row][c]
        pivot_row += 1

    return mat


def reduced_row_echelon_form(matrix):
    """Compute RREF using exact Gauss-Jordan elimination on rationals."""
    mat = copy_matrix(matrix)
    rows, cols = matrix_shape(mat)
    pivot_row = 0

    for col in range(cols):
        if pivot_row >= rows:
            break
        max_index = select_pivot_row(mat, pivot_row, col)
        if max_index == -1:
            continue
        if max_index != pivot_row:
            mat[pivot_row], mat[max_index] = mat[max_index], mat[pivot_row]

        pivot_val = mat[pivot_row][col]
        for c in range(cols):
            mat[pivot_row][c] = mat[pivot_row][c] / pivot_val

        for r in range(rows):
            if r == pivot_row or mat[r][col].is_zero():
                continue
            factor = mat[r][col]
            for c in range(cols):
                mat[r][c] = mat[r][c] - factor * mat[pivot_row][c]
        pivot_row += 1

    return mat


def is_zero_row(row):
    for value in row:
        if not value.is_zero():
            return False
    return True


def count_nonzero_rows(matrix):
    """Count rows that are not entirely zero."""
    count = 0
    for row in matrix:
        if not is_zero_row(row):
            count += 1
    return count


def solve_augmented_system(augmented):
    """
    Solve an augmented linear system [A|b] using RREF analysis.
    Returns (status, message, solution_data).
    """
    rows, cols = matrix_shape(augmented)

    if cols < 2:
        return (
            "error",
            "Error: An augmented matrix must have at least 2 columns (variables + constants).",
            None,
        )

    variable_count = cols - 1
    rref_aug = reduced_row_echelon_form(augmented)

    for r in range(rows):
        left_zero = is_zero_row(rref_aug[r][:-1])
        right_nonzero = not rref_aug[r][-1].is_zero()
        if left_zero and right_nonzero:
            return (
                "no_solution",
                "No solution: the system is inconsistent (a row reduces to [0 ... 0 | nonzero]).",
                {"rref": rref_aug},
            )

    left_part = [row[:-1] for row in rref_aug]
    rank_a = count_nonzero_rows(left_part)
    rank_aug = count_nonzero_rows(rref_aug)

    if rank_a < rank_aug:
        return (
            "no_solution",
            "No solution: rank(A) < rank([A|b]), so the system is inconsistent.",
            {"rref": rref_aug},
        )

    if rank_a < variable_count:
        return (
            "infinite",
            (
                "Infinitely many solutions: rank(A) = rank([A|b]) < number of variables. "
                "At least one variable is free."
            ),
            {"rref": rref_aug},
        )

    solution = [ZERO for _ in range(variable_count)]
    for row in rref_aug:
        pivot_col = -1
        nonzero_count = 0
        for c in range(variable_count):
            if not row[c].is_zero():
                nonzero_count += 1
                pivot_col = c
        if nonzero_count == 1 and pivot_col >= 0:
            solution[pivot_col] = row[-1]

    return (
        "unique",
        "Unique solution found.",
        {"rref": rref_aug, "solution": solution},
    )


def determinant(matrix):
    """Compute determinant exactly via elimination."""
    mat = copy_matrix(matrix)
    n = len(mat)
    swap_count = 0
    det_value = ONE

    for col in range(n):
        pivot_row = select_pivot_row(mat, col, col)
        if pivot_row == -1:
            return ZERO
        if pivot_row != col:
            mat[col], mat[pivot_row] = mat[pivot_row], mat[col]
            swap_count += 1
        pivot = mat[col][col]
        det_value = det_value * pivot
        for r in range(col + 1, n):
            if mat[r][col].is_zero():
                continue
            factor = mat[r][col] / pivot
            for c in range(col, n):
                mat[r][c] = mat[r][c] - factor * mat[col][c]

    if swap_count % 2 == 1:
        det_value = -det_value
    return det_value


def compute_inverse(matrix):
    """Compute inverse with explicit reasoned errors (exact rational arithmetic)."""
    rows, cols = matrix_shape(matrix)

    if rows != cols:
        return (
            None,
            "Error: This matrix cannot be inverted because it is not a square matrix.",
        )

    det_value = determinant(matrix)
    if det_value.is_zero():
        return (
            None,
            (
                "Error: This matrix cannot be inverted because its determinant is exactly 0, "
                "meaning it contains linearly dependent rows/columns."
            ),
        )

    n = rows
    augmented = []
    for r in range(n):
        left = [Rational(matrix[r][c].n, matrix[r][c].d) for c in range(n)]
        right = [ONE if r == c else ZERO for c in range(n)]
        augmented.append(left + right)

    augmented_rref = reduced_row_echelon_form(augmented)

    # Left block must be identity after Gauss-Jordan.
    for r in range(n):
        for c in range(n):
            expected = ONE if r == c else ZERO
            if (
                augmented_rref[r][c].n != expected.n
                or augmented_rref[r][c].d != expected.d
            ):
                return (
                    None,
                    (
                        "Error: This matrix cannot be inverted because it is singular "
                        "(linearly dependent rows/columns)."
                    ),
                )

    inverse = [row[n:] for row in augmented_rref]
    return inverse, None


def read_positive_int(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value <= 0:
                print("Please enter a positive integer.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")


def input_matrix():
    print("\nEnter matrix dimensions:")
    n_rows = read_positive_int("Number of rows: ")
    n_cols = read_positive_int("Number of columns: ")

    data = []
    print("\nEnter each row with space-separated values.")
    print("Allowed entry formats: integer (3), fraction (7/5), or decimal (0.25).")
    for r in range(n_rows):
        while True:
            raw = input(f"Row {r + 1}: ").strip()
            parts = raw.split()
            if len(parts) != n_cols:
                print(f"Please enter exactly {n_cols} values.")
                continue
            try:
                row = [Rational.from_string(x) for x in parts]
                data.append(row)
                break
            except ValueError:
                print("Invalid row: use integers, decimals, or fractions like a/b.")

    matrix = data
    print("\nMatrix stored successfully.")
    print(format_matrix(matrix))
    return matrix


def display_solution(solution):
    parts = []
    for idx, val in enumerate(solution, start=1):
        parts.append(f"x{idx} = {val}")
    return ", ".join(parts)


def print_menu():
    print("\n=== Advanced Matrix Solver ===")
    print("1) Enter/replace matrix")
    print("2) Show current matrix")
    print("3) Compute Row Echelon Form (REF)")
    print("4) Compute Reduced Row Echelon Form (RREF)")
    print("5) Solve as augmented system [A|b]")
    print("6) Compute inverse matrix")
    print("0) Exit")


def main():
    current_matrix = None

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            current_matrix = input_matrix()

        elif choice == "2":
            if current_matrix is None:
                print("No matrix loaded yet.")
            else:
                print("\nCurrent matrix:")
                print(format_matrix(current_matrix))

        elif choice == "3":
            if current_matrix is None:
                print("No matrix loaded yet.")
                continue
            ref = row_echelon_form(current_matrix)
            print("\nRow Echelon Form (REF):")
            print(format_matrix(ref))

        elif choice == "4":
            if current_matrix is None:
                print("No matrix loaded yet.")
                continue
            rref = reduced_row_echelon_form(current_matrix)
            print("\nReduced Row Echelon Form (RREF):")
            print(format_matrix(rref))

        elif choice == "5":
            if current_matrix is None:
                print("No matrix loaded yet.")
                continue
            status, message, data = solve_augmented_system(current_matrix)
            print(f"\n{message}")
            if data is not None and "rref" in data:
                print("RREF of augmented matrix:")
                print(format_matrix(data["rref"]))
            if status == "unique" and data is not None and "solution" in data:
                print("Solution:")
                print(display_solution(data["solution"]))

        elif choice == "6":
            if current_matrix is None:
                print("No matrix loaded yet.")
                continue
            inverse, error = compute_inverse(current_matrix)
            if error is not None:
                print(f"\n{error}")
            else:
                print("\nInverse matrix:")
                print(format_matrix(inverse))

        elif choice == "0":
            print("Exiting Advanced Matrix Solver.")
            break

        else:
            print("Invalid menu option. Please choose from the listed options.")


if __name__ == "__main__":
    main()
