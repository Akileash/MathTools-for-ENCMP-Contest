# Development Journal

Project: Math Tools
Start Date: February 15
Current Date: April 3

---

## February 15 - Planning
- Split the project into two parts: matrix solver and solids of revolution visualizer.
- Chose terminal menus for easy testing.
- Confirmed we would stay inside the allowed library list.

---

## March 1 - v1 Milestone
- Built matrix input and REF workflow.
- Kept this version intentionally simple.
- Set up first runnable version files.

### v1
- Matrix: REF only (`math_tools/v1/matrix_solver_v1.py`)
- Revolution: Disk method around x-axis (`math_tools/v1/revolution_visualizer_v1.py`)

---

## March 15 - Visualizer Prototype
- Built the first 3D plotting flow.
- Tested function input/evaluation and graph rendering.
- Validated basic behavior on sample functions.

---

## March 29 - v2 Milestone
- Added RREF to the matrix side.
- Added washer method to the revolution side.
- Improved prompts and input validation.

### v2
- Matrix: REF + RREF (`math_tools/v2/matrix_solver_v2.py`)
- Revolution: Disk + Washer around x-axis (`math_tools/v2/revolution_visualizer_v2.py`)

---

## April 3 - Final Version
- Final matrix solver uses exact fractions and includes solving/inverse checks.
- Final revolution visualizer supports disk/washer with axis options (`x-axis`, `y-axis`, `x=c`, `y=c`).
- Added unified final launcher and synced docs.

### final
- `math_tools/main_final.py`
- `math_tools/matrix_solver.py`
- `math_tools/revolution_visualizer.py`
