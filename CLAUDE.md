# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A teaching resource for Analysis I/II students: interactive [marimo](https://marimo.io) notebooks that visualize lecture concepts. The audience is students, so notebooks should favor clarity and readable code over cleverness. Each topic is one self-contained `.py` notebook at the repo root (currently `bisection_method.py`). When adding a notebook, also add a row to the notebook table in `README.md`. `data/` and `models/` exist but are empty placeholders. There is no test suite, linter config, or build step.

## Environment & commands

Python 3.13 virtualenv in `.venv/` (Windows), dependencies pinned in `requirements.txt` (marimo, numpy, plotly, scipy, sympy, pandas, matplotlib, jupyterlab).

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

marimo edit bisection_method.py      # interactive editing in the browser
marimo run bisection_method.py       # read-only app mode
python bisection_method.py           # executes the notebook as a script
marimo check bisection_method.py     # lint notebook structure
```

`__marimo__/session/` holds marimo's cached session state (cell outputs); it is generated, not source.

## Notebook conventions

These files are marimo notebooks, not plain scripts — edits must respect marimo's reactive model:

- Every cell is an `@app.cell` function. Its parameters are the global names it reads; its `return` tuple lists the globals it defines. marimo builds the dependency graph from these signatures, so keep them in sync with the body when editing.
- A global name may be defined in only one cell. Cell-local helpers/temporaries use a leading underscore (`_fig`, `_f`, `_k`) to avoid collisions.
- All imports live in the first cell and are passed to other cells via parameters.
- UI elements (`mo.ui.number`, `mo.ui.array`, `mo.ui.slider`) must be defined in one cell and have their `.value` read in a different, downstream cell.
- Plots use `plotly.express`; layouts use `mo.vstack` / `mo.hstack`; `mo.stop(...)` short-circuits a cell with a fallback output.
- User-facing text (labels, markdown, some error messages) is in German; math is rendered with LaTeX in `mo.md`.

## bisection_method.py structure

Cubic polynomial `ax^3 + bx^2 + cx + d` with coefficients from the `polynom` UI array. Two bisection implementations coexist: `bisection_method` (returns the root, validates inputs, raises on non-convergence) and `bisection_steps` (returns the `(a, b, midpoint)` history that drives the step slider and visualization). Both evaluate the polynomial via Horner's scheme and compute midpoints as `a/2 + b/2` to avoid overflow — changes to the algorithm usually need to be applied to both.
