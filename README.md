# Analysis I/II – Interactive Notebooks

A collection of interactive [marimo](https://marimo.io) notebooks for the Analysis I and II lectures. Each notebook makes one concept from the lecture visual: change parameters with sliders and input fields and see right away how the mathematics responds.

The notebooks are meant to go alongside the lecture and exercises, not replace them. New notebooks will be added during the semester.

## Notebooks

| Notebook | Topic | Contents |
|---|---|---|
| [`bisection_method.py`](bisection_method.py) | Intermediate value theorem / bisection | Pick a cubic polynomial and a starting interval, then step through the bisection method one iteration at a time, deciding at each step which half to keep. See how the error halves every step and predict the number of steps in advance. |
| [`continuity.py`](continuity.py) | Continuity (ε–δ and limit definition) | Briefly play the ε–δ game, then test continuity via lim f(x) = f(x₀): send sequences towards x₀, hunt for counter-sequences, and compare left- and right-sided limits for jumps, removable gaps, poles and oscillations. |
| [`limit_definition.py`](limit_definition.py) | Limit of a sequence (ε–N definition) | Play the ε–N game: choose ε, find an N so that every term from N on lies in the ε-tube, and see how N(ε) grows as ε shrinks. |

## Getting started

You need [Python](https://www.python.org/downloads/) 3.13 or newer.

1. **Download the repository** (with `git clone` or as a ZIP) and open a terminal in the folder.

2. **Create a virtual environment and install the dependencies:**

   Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

   macOS / Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Open a notebook:**

   ```bash
   marimo run bisection_method.py
   ```

   This opens the notebook in your browser as an interactive app. To look at the code or change it, use edit mode instead:

   ```bash
   marimo edit bisection_method.py
   ```

When you come back later, you only need to activate the virtual environment again (step 2, second line) and start the notebook.

## Tips

- **Experiment:** change the values and try to predict what will happen first. The notebooks work best when you use them to check your own expectations.
- **Read the code:** in `marimo edit` mode you can see how each visualization is computed. Many algorithms (e.g. bisection) are implemented directly and are short enough to follow line by line.
- **Nothing breaks:** changes you make in edit mode only affect your local copy. If something stops working, download the file again.

## About marimo

marimo notebooks are plain Python files. Unlike Jupyter, they are *reactive*: when you change a value, every cell that depends on it updates automatically. More at [docs.marimo.io](https://docs.marimo.io).
