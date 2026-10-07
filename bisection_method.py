import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.express as px
    from collections.abc import Sequence
    from math import isfinite

    return Sequence, isfinite, mo, np, px


@app.cell
def _(mo):
    polynom = mo.ui.array([mo.ui.number(label="$a$",value=1),mo.ui.number(label="$b$",value=1),mo.ui.number(label="$c$",value=1),mo.ui.number(label="$d$",value=1)], label="Koeffezienten")
    return (polynom,)


@app.cell
def _(mo, np, polynom, px):
    a_poly, b_poly, c_poly, d_poly = polynom.value

    poly_x = np.linspace(-5, 5, 100)
    poly_y = (
        a_poly * poly_x**3
        + b_poly * poly_x**2
        + c_poly * poly_x
        + d_poly
    )

    _plot = px.line(
        x=poly_x,
        y=poly_y,
        range_x=[-5, 5],
        range_y=[-5, 5],
    )

    _plot.update_xaxes(
        tickmode="linear",
        tick0=0,
        dtick=1,
        showgrid=True,
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="black",
    )

    _plot.update_yaxes(
        tickmode="linear",
        tick0=0,
        dtick=1,
        showgrid=True,
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="black",
    )

    plot = mo.ui.plotly(_plot)

    mo.vstack([
        mo.md(
            f"$$y={a_poly}x^3{b_poly:+g}x^2"
            f"{c_poly:+g}x{d_poly:+g}$$"
        ),
        mo.hstack([plot, polynom]),
    ])
    return


@app.cell
def _(Sequence, isfinite):
    def bisection_method(
        poly: Sequence[float],
        a: float,
        b: float,
        tol: float = 1e-3,
        max_iter: int = 100,
    ) -> float:
        """Find a root of a cubic within a sign-changing interval."""
        if len(poly) != 4:
            raise ValueError("poly must contain four coefficients [a, b, c, d].")

        if not isfinite(tol) or tol <= 0:
            raise ValueError("tol must be finite and positive.")

        if not isinstance(max_iter, int) or max_iter < 1:
            raise ValueError("max_iter must be a positive integer.")

        if not all(isfinite(value) for value in (*poly, a, b)):
            raise ValueError("Coefficients and endpoints must be finite.")

        coef_a, coef_b, coef_c, coef_d = poly

        def f(x: float) -> float:
            value = ((coef_a * x + coef_b) * x + coef_c) * x + coef_d
            if not isfinite(value):
                raise ValueError("Polynomial evaluation produced a non-finite value.")
            return value

        a, b = sorted((a, b))
        fa, fb = f(a), f(b)

        if fa == 0:
            return a
        if fb == 0:
            return b

        if (fa > 0) == (fb > 0):
            raise ValueError("The endpoints must bracket a sign change.")

        for _ in range(max_iter):
            c = a / 2 + b / 2
            fc = f(c)
            half_width = b / 2 - a / 2

            if fc == 0 or half_width <= tol:
                return c

            if c == a or c == b:
                raise RuntimeError("Floating-point precision prevents further refinement.")

            if (fa > 0) == (fc > 0):
                a, fa = c, fc
            else:
                b = c

        raise RuntimeError(
            f"Bisection did not converge within {max_iter} iterations."
        )

    return


@app.cell
def _(Sequence):
    def bisection_steps(
        poly: Sequence[float],
        a: float,
        b: float,
        tol: float = 1e-3,
        max_iter: int = 100,
    ) -> list[tuple[float, float, float]]:
        """Return the (a, b, midpoint) triple of every bisection iteration."""
        coef_a, coef_b, coef_c, coef_d = poly

        def f(x: float) -> float:
            return ((coef_a * x + coef_b) * x + coef_c) * x + coef_d

        a, b = sorted((a, b))
        fa, fb = f(a), f(b)

        if fa == 0:
            return [(a, b, a)]
        if fb == 0:
            return [(a, b, b)]
        if (fa > 0) == (fb > 0):
            raise ValueError("f(a) und f(b) muessen verschiedene Vorzeichen haben.")

        steps = []
        for _ in range(max_iter):
            c = a / 2 + b / 2
            fc = f(c)
            steps.append((a, b, c))

            if fc == 0 or b / 2 - a / 2 <= tol:
                break

            if (fa > 0) == (fc > 0):
                a, fa = c, fc
            else:
                b = c

        return steps

    return (bisection_steps,)


@app.cell
def _(mo):
    interval_a = mo.ui.number(value=-3, step=0.1, label="$a_0$")
    interval_b = mo.ui.number(value=2, step=0.1, label="$b_0$")
    return interval_a, interval_b


@app.cell
def _(bisection_steps, interval_a, interval_b, mo, polynom):
    bisection_error = None
    try:
        bisection_history = bisection_steps(
            polynom.value, interval_a.value, interval_b.value
        )
    except ValueError as _err:
        bisection_history = []
        bisection_error = str(_err)

    bisection_step = mo.ui.slider(
        start=0,
        stop=max(len(bisection_history) - 1, 1),
        step=1,
        value=0,
        label="Schritt",
        show_value=True,
    )
    return bisection_error, bisection_history, bisection_step


@app.cell
def _(
    bisection_error,
    bisection_history,
    bisection_step,
    interval_a,
    interval_b,
    mo,
    np,
    polynom,
    px,
):
    _controls = mo.hstack([interval_a, interval_b, bisection_step], justify="start")

    mo.stop(
        not bisection_history,
        mo.vstack([_controls, mo.callout(mo.md(f"**{bisection_error}**"), kind="warn")]),
    )

    _k = min(bisection_step.value, len(bisection_history) - 1)
    _a, _b, _c = bisection_history[_k]
    _a0, _b0, _ = bisection_history[0]
    _pad = 0.15 * (_b0 - _a0)
    _coef_a, _coef_b, _coef_c, _coef_d = polynom.value


    def _f(x):
        return ((_coef_a * x + _coef_b) * x + _coef_c) * x + _coef_d


    _x = np.linspace(_a0 - _pad, _b0 + _pad, 400)
    _fig = px.line(x=_x, y=_f(_x), labels={"x": "x", "y": "f(x)"})
    _fig.add_vrect(x0=_a, x1=_b, fillcolor="orange", opacity=0.2, line_width=0)
    _fig.add_scatter(
        x=[_a, _b],
        y=[_f(_a), _f(_b)],
        mode="markers+text",
        text=["a", "b"],
        textposition="top center",
        marker=dict(size=10, color="orange"),
    )
    _fig.add_scatter(
        x=[_c],
        y=[_f(_c)],
        mode="markers+text",
        text=["c"],
        textposition="bottom center",
        marker=dict(size=12, color="red", symbol="x"),
    )
    _fig.update_xaxes(
        range=[_a0 - _pad, _b0 + _pad],
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="black",
    )
    _fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor="black", range=[min(_f(_a),-5),max(_f(_b),5)])
    _fig.update_layout(showlegend=False)

    mo.vstack([
        _controls,
        _fig,
        mo.md(
            f"Schritt {_k + 1} von {len(bisection_history)}: "
            f"$[a, b] = [{_a:.6g}, {_b:.6g}]$, "
            f"$c = {_c:.6g}$, $f(c) = {_f(_c):.3g}$, "
            f"Breite $= {_b - _a:.3g}$"
        ),
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
