import numpy as np


def read_int(prompt):
    while True:
        try:
            value = int(input(prompt).strip())
            if value <= 0:
                print("Please enter a positive integer.")
                continue
            return value
        except ValueError:
            print("Invalid integer input.")


def input_matrix():
    rows = read_int("Rows: ")
    cols = read_int("Columns: ")
    data = []
    print("Enter each row as space-separated numbers.")
    for r in range(rows):
        while True:
            raw = input(f"Row {r + 1}: ").strip().split()
            if len(raw) != cols:
                print(f"Please enter exactly {cols} values.")
                continue
            try:
                data.append([float(x) for x in raw])
                break
            except ValueError:
                print("Row must contain only numbers.")
    return np.array(data, dtype=float)


def ref(matrix):
    m = matrix.copy().astype(float)
    rows, cols = m.shape
    pivot_row = 0
    for c in range(cols):
        if pivot_row >= rows:
            break
        pivot = None
        for r in range(pivot_row, rows):
            if abs(m[r, c]) > 1e-10:
                pivot = r
                break
        if pivot is None:
            continue
        if pivot != pivot_row:
            m[[pivot_row, pivot]] = m[[pivot, pivot_row]]
        for r in range(pivot_row + 1, rows):
            factor = m[r, c] / m[pivot_row, c]
            m[r, c:] -= factor * m[pivot_row, c:]
        pivot_row += 1
    m[np.abs(m) < 1e-10] = 0.0
    return m


def rref(matrix):
    m = ref(matrix)
    rows, cols = m.shape
    for r in range(rows - 1, -1, -1):
        pivot_col = None
        for c in range(cols):
            if abs(m[r, c]) > 1e-10:
                pivot_col = c
                break
        if pivot_col is None:
            continue
        m[r, :] /= m[r, pivot_col]
        for up in range(r):
            factor = m[up, pivot_col]
            m[up, :] -= factor * m[r, :]
    m[np.abs(m) < 1e-10] = 0.0
    return m


def main():
    print("=== Matrix Solver v2 ===")
    print("v2 feature set: REF + RREF.")
    matrix = input_matrix()
    print("\nREF:")
    print(ref(matrix))
    print("\nRREF:")
    print(rref(matrix))


if __name__ == "__main__":
    main()
