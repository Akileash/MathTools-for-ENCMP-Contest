# MathTools for ENCMP Contest

This repository contains the final contest project files and versioned milestone files.

## Main Files
- `math_tools/main_final.py` - combined final launcher menu for both tools
- `math_tools/matrix_solver.py` - advanced matrix solver (exact fractions)
- `math_tools/revolution_visualizer.py` - solids of revolution 3D visualizer
- `Journal.md` - development timeline journal

## How to run and test the programs (step-by-step)

1) Open Spyder (or a terminal with Python configured for numpy and matplotlib).  
2) Set the working directory to `math_tools`.  
3) (Recommended) Run `main_final.py` to open a combined launcher menu for both tools.

## Testing matrix_solver.py

4) From `main_final.py`, choose option 1 (or run `matrix_solver.py` directly).  
5) In the menu, choose option 1 and enter a matrix size (rows and columns), then enter each row using space-separated numbers.  
6) Choose option 3 to view the REF output.  
7) Choose option 4 to view the RREF output.  
8) Choose option 5 to solve it as an augmented system [A|b] (last column is constants). Test at least:
- one system with a unique solution,
- one inconsistent system (no solution),
- one system with infinitely many solutions.
9) Choose option 6 to compute the inverse. Test at least:
- one invertible square matrix,
- one non-square matrix (should show a clear non-square error),
- one square singular matrix with determinant 0 (should show a clear determinant/dependence error).
10) Choose option 0 to exit.

## Testing revolution_visualizer.py

11) From `main_final.py`, choose option 2 (or run `revolution_visualizer.py` directly).  
12) Choose method:
- Disk Method (single boundary function), or
- Washer Method (outer and inner boundary functions).
13) Choose axis of revolution:
- x-axis,
- y-axis,
- x = c,
- y = c.
14) Enter valid bounds [a, b] with b > a.  
15) Enter function expressions using numpy-style syntax, for example:
- x**2
- np.sin(x)
- y**2
- np.cos(y)
16) A 3D matplotlib plot will appear showing the solid boundary surface(s).  
17) Close the plot window to finish the run.

## Notes

- For horizontal axes (x-axis or y = c), enter functions in the form y = f(x) using variable x.
- For vertical axes (y-axis or x = c), enter functions in the form x = f(y) using variable y.
- If an invalid expression or numeric input is entered, the program will show a clear error message.

## Version Folders
- `math_tools/v1/matrix_solver_v1.py`
- `math_tools/v1/revolution_visualizer_v1.py`
- `math_tools/v2/matrix_solver_v2.py`
- `math_tools/v2/revolution_visualizer_v2.py`

## Version Milestones

- **v1**:
  - `math_tools/v1/matrix_solver_v1.py` - REF only
  - `math_tools/v1/revolution_visualizer_v1.py` - Disk method around x-axis
- **v2**:
  - `math_tools/v2/matrix_solver_v2.py` - REF + RREF
  - `math_tools/v2/revolution_visualizer_v2.py` - Disk + Washer around x-axis
- **final**:
  - `math_tools/main_final.py` - full combined launcher
  - `math_tools/matrix_solver.py` - includes inverse + augmented system solving with detailed errors
  - `math_tools/revolution_visualizer.py` - disk/washer + x-axis/y-axis/x=c/y=c + improved validation/visual aids