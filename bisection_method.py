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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Das Bisektionsverfahren

    **Zwischenwertsatz.** Ist $f\colon [a, b] \to \mathbb{R}$ stetig und haben $f(a)$ und $f(b)$
    verschiedene Vorzeichen, also $f(a) \cdot f(b) < 0$, dann gibt es ein $\xi \in (a, b)$ mit

    $$
    f(\xi) = 0 .
    $$

    Der Satz sagt nur, **dass** es eine Nullstelle gibt – nicht, **wo** sie liegt.
    Das Bisektionsverfahren macht aus dem Satz einen Algorithmus, der die Nullstelle beliebig genau einkreist.

    ### Die Idee: Intervall halbieren

    Starte mit einem Intervall $[a_0, b_0]$, an dessen Rändern $f$ das Vorzeichen wechselt. Dann wiederhole:

    1. Berechne den Mittelpunkt $c_k = \frac{a_k + b_k}{2}$.
    2. Ist $f(c_k) = 0$, ist man fertig.
    3. Sonst wechselt $f$ das Vorzeichen in **genau einer** der beiden Hälften $[a_k, c_k]$ oder $[c_k, b_k]$.
       Diese Hälfte ist das neue Intervall $[a_{k+1}, b_{k+1}]$.

    In jedem Schritt halbiert sich die Intervalllänge, und die Nullstelle bleibt immer im Intervall gefangen:

    $$
    b_k - a_k = \frac{b_0 - a_0}{2^k}, \qquad |c_k - \xi| \le \frac{b_k - a_k}{2} = \frac{b_0 - a_0}{2^{k+1}} .
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    polynom = mo.ui.array(
        [
            mo.ui.number(label="$a$", value=1),
            mo.ui.number(label="$b$", value=1),
            mo.ui.number(label="$c$", value=1),
            mo.ui.number(label="$d$", value=1),
        ],
        label="Koeffizienten",
    )
    return (polynom,)


@app.cell(hide_code=True)
def _(mo):
    interval_a = mo.ui.number(value=-3, step=0.1, label="$a_0$")
    interval_b = mo.ui.number(value=2, step=0.1, label="$b_0$")
    tolerance = mo.ui.slider(
        steps=[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-8, 1e-10],
        value=1e-3,
        label="Toleranz",
        show_value=True,
    )
    zoom_switch = mo.ui.switch(label="Auf das aktuelle Intervall zoomen")
    return interval_a, interval_b, tolerance, zoom_switch


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Polynom und Startintervall wählen

    Wir untersuchen kubische Polynome $f(x) = ax^3 + bx^2 + cx + d$. Polynome sind stetig, der
    Zwischenwertsatz ist also anwendbar. Wähle die Koeffizienten und ein Startintervall $[a_0, b_0]$
    (orange markiert), an dessen Rändern $f$ das Vorzeichen wechselt.
    """)
    return


@app.cell(hide_code=True)
def _(interval_a, interval_b, mo, np, polynom, px):
    _coef_a, _coef_b, _coef_c, _coef_d = polynom.value
    _a0, _b0 = sorted((interval_a.value, interval_b.value))


    def _f(x):
        return ((_coef_a * x + _coef_b) * x + _coef_c) * x + _coef_d


    _x_low = min(-5, _a0 - 0.5)
    _x_high = max(5, _b0 + 0.5)
    _x = np.linspace(_x_low, _x_high, 400)
    _fig = px.line(x=_x, y=_f(_x), labels={"x": "x", "y": "f(x)"})
    _fig.add_vrect(x0=_a0, x1=_b0, fillcolor="orange", opacity=0.2, line_width=0)
    _fig.add_scatter(
        x=[_a0, _b0],
        y=[_f(_a0), _f(_b0)],
        mode="markers+text",
        text=["a₀", "b₀"],
        textposition="top center",
        marker=dict(size=10, color="orange"),
    )
    _fig.update_xaxes(
        range=[_x_low, _x_high],
        dtick=1,
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="black",
    )
    _fig.update_yaxes(range=[-5, 5], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor="black")
    _fig.update_layout(showlegend=False)

    _fa0, _fb0 = _f(_a0), _f(_b0)
    if _fa0 == 0 or _fb0 == 0:
        _check = mo.callout(
            mo.md("Ein Randpunkt ist **schon eine Nullstelle** – da gibt es nichts mehr zu halbieren."),
            kind="info",
        )
    elif (_fa0 > 0) != (_fb0 > 0):
        _check = mo.callout(
            mo.md(
                f"$f(a_0) = {_fa0:.4g}$ und $f(b_0) = {_fb0:.4g}$ haben **verschiedene Vorzeichen**. "
                f"Nach dem Zwischenwertsatz liegt in $({_a0:g}, {_b0:g})$ mindestens eine Nullstelle."
            ),
            kind="success",
        )
    else:
        _check = mo.callout(
            mo.md(
                f"$f(a_0) = {_fa0:.4g}$ und $f(b_0) = {_fb0:.4g}$ haben **dasselbe Vorzeichen**. "
                "Der Zwischenwertsatz sagt dann nichts: Im Intervall kann es Nullstellen geben – oder auch keine. "
                "Das Bisektionsverfahren kann hier nicht starten."
            ),
            kind="warn",
        )

    mo.vstack([
        mo.md(f"$$f(x) = {_coef_a:g}x^3 {_coef_b:+g}x^2 {_coef_c:+g}x {_coef_d:+g}$$"),
        mo.hstack([_fig, mo.vstack([polynom, interval_a, interval_b])], widths=[3, 1]),
        _check,
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Der Algorithmus in Python

    Die beiden Funktionen unten setzen das Verfahren um. `bisection_method` liefert nur die
    Näherung für die Nullstelle und prüft die Eingaben sorgfältig. `bisection_steps` merkt sich
    zusätzlich jedes Zwischenintervall – daraus entstehen die Grafiken weiter unten.

    Zwei Details:

    - Das Polynom wird mit dem **Horner-Schema** $((ax + b)x + c)x + d$ ausgewertet: weniger Multiplikationen als $ax^3 + bx^2 + cx + d$.
    - Der Mittelpunkt wird als `a / 2 + b / 2` berechnet statt als `(a + b) / 2`. Für sehr große Gleitkommazahlen
      könnte `a + b` überlaufen (`inf`), obwohl der Mittelpunkt selbst darstellbar ist.
    """)
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

    return (bisection_method,)


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
            raise ValueError("f(a₀) und f(b₀) müssen verschiedene Vorzeichen haben.")

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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Schritt für Schritt

    Schiebe den Regler „Schritt“ nach rechts und verfolge, wie das orange Intervall schrumpft.

    **Mitdenken:** Bevor du einen Schritt weitergehst, entscheide anhand der Vorzeichen von
    $f(a)$, $f(c)$ und $f(b)$, in welcher Hälfte die Nullstelle weiter gesucht wird.
    Schalte den Zoom ein, wenn das Intervall zu klein zum Erkennen wird.
    """)
    return


@app.cell(hide_code=True)
def _(bisection_steps, interval_a, interval_b, mo, polynom, tolerance):
    bisection_error = None
    try:
        bisection_history = bisection_steps(
            polynom.value, interval_a.value, interval_b.value, tol=tolerance.value
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


@app.cell(hide_code=True)
def _(bisection_step, mo):
    # Wird bei jedem neuen Schritt neu angelegt, damit die Antwort zurückgesetzt wird
    half_guess = mo.ui.radio(
        options=["linke Hälfte [a, c]", "rechte Hälfte [c, b]"],
        label=f"Wo geht die Suche nach Schritt {bisection_step.value + 1} weiter?",
    )
    return (half_guess,)


@app.cell(hide_code=True)
def _(
    bisection_error,
    bisection_history,
    bisection_step,
    half_guess,
    interval_a,
    interval_b,
    mo,
    np,
    polynom,
    px,
    tolerance,
    zoom_switch,
):
    _controls = mo.vstack([
        mo.hstack([interval_a, interval_b, tolerance], justify="start"),
        mo.hstack([bisection_step, zoom_switch], justify="start"),
    ])

    mo.stop(
        not bisection_history,
        mo.vstack([_controls, mo.callout(mo.md(f"**{bisection_error}**"), kind="warn")]),
    )

    _k = min(bisection_step.value, len(bisection_history) - 1)
    _a, _b, _c = bisection_history[_k]
    _a0, _b0, _ = bisection_history[0]
    _coef_a, _coef_b, _coef_c, _coef_d = polynom.value


    def _f(x):
        return ((_coef_a * x + _coef_b) * x + _coef_c) * x + _coef_d


    # Ohne Zoom: ganzes Startintervall; mit Zoom: nur das aktuelle Intervall
    _low, _high = (_a, _b) if zoom_switch.value else (_a0, _b0)
    _pad = 0.15 * (_high - _low)
    _x = np.linspace(_low - _pad, _high + _pad, 400)
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
        range=[_low - _pad, _high + _pad],
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="black",
    )
    _fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor="black")
    _fig.update_layout(showlegend=False)


    def _sign(value):
        return "+" if value > 0 else ("-" if value < 0 else "0")


    _sign_table = mo.md(
        f"""
    | | $a$ | $c$ | $b$ |
    |---|---|---|---|
    | $x$ | ${_a:.6g}$ | ${_c:.6g}$ | ${_b:.6g}$ |
    | Vorzeichen von $f(x)$ | ${_sign(_f(_a))}$ | ${_sign(_f(_c))}$ | ${_sign(_f(_b))}$ |
    """
    )

    # Rückmeldung zur Frage, in welcher Hälfte es weitergeht
    _is_last = _k == len(bisection_history) - 1
    _fa, _fc = _f(_a), _f(_c)
    _correct = "linke Hälfte [a, c]" if (_fa > 0) != (_fc > 0) else "rechte Hälfte [c, b]"
    if _fc == 0:
        _feedback = mo.callout(mo.md(f"$f(c) = 0$: **Nullstelle exakt getroffen** bei $c = {_c:.6g}$!"), kind="success")
    elif _is_last:
        _feedback = mo.callout(
            mo.md(
                f"**Fertig.** Die halbe Intervalllänge $\\frac{{b - a}}{{2}} = {_b / 2 - _a / 2:.3g}$ "
                f"ist höchstens die Toleranz ${tolerance.value:g}$. Näherung: $\\xi \\approx {_c:.10g}$."
            ),
            kind="success",
        )
    elif half_guess.value is None:
        _feedback = mo.md("")
    elif half_guess.value == _correct:
        _feedback = mo.callout(
            mo.md(f"**Richtig!** $f$ wechselt in der {_correct} das Vorzeichen. Gehe einen Schritt weiter."),
            kind="success",
        )
    else:
        _feedback = mo.callout(
            mo.md(
                "**Nicht ganz.** Gesucht ist die Hälfte, an deren Rändern $f$ **verschiedene** Vorzeichen hat. "
                "Vergleiche das Vorzeichen von $f(c)$ mit dem von $f(a)$."
            ),
            kind="danger",
        )

    _all_steps = mo.ui.table(
        [
            {
                "Schritt": _i + 1,
                "a": f"{_ai:.10g}",
                "b": f"{_bi:.10g}",
                "c": f"{_ci:.10g}",
                "f(c)": f"{_f(_ci):.3g}",
                "b − a": f"{_bi - _ai:.3g}",
            }
            for _i, (_ai, _bi, _ci) in enumerate(bisection_history)
        ],
        selection=None,
        pagination=True,
        page_size=10,
    )

    mo.vstack([
        _controls,
        _fig,
        mo.md(
            f"Schritt {_k + 1} von {len(bisection_history)}: "
            f"$[a, b] = [{_a:.6g}, {_b:.6g}]$, Breite $b - a = {_b - _a:.3g}$, "
            f"$f(c) = {_fc:.3g}$"
        ),
        _sign_table,
        mo.md("") if _is_last or _fc == 0 else half_guess,
        _feedback,
        mo.accordion({"Tabelle aller Schritte": _all_steps}),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Wie schnell konvergiert das Verfahren?

    Die Intervalllänge halbiert sich in jedem Schritt – **unabhängig von $f$**. Nach $n$ Schritten
    ist der Fehler des Mittelpunkts höchstens $\frac{b_0 - a_0}{2^n}$. Für eine Toleranz $\delta$
    braucht man also

    $$
    \frac{b_0 - a_0}{2^n} \le \delta
    \quad\iff\quad
    n \ge \log_2 \frac{b_0 - a_0}{\delta}
    $$

    Schritte. Das lässt sich **vorher** ausrechnen! Im Graphen (logarithmische $y$-Achse) wird die
    Halbierung zu einer Geraden. Der tatsächliche Fehler $|c_k - \xi|$ liegt immer unter der
    Schranke, springt aber unregelmäßig: Manchmal liegt der Mittelpunkt zufällig sehr nahe an $\xi$.
    """)
    return


@app.cell(hide_code=True)
def _(bisection_history, bisection_method, mo, np, polynom, px, tolerance):
    mo.stop(not bisection_history, mo.md("*Kein gültiges Startintervall – siehe oben.*"))

    _a0, _b0, _ = bisection_history[0]
    _length = _b0 - _a0
    _steps = np.arange(1, len(bisection_history) + 1)
    _bound = _length / 2.0**_steps

    # Genaue Referenz-Nullstelle, um den tatsächlichen Fehler zu messen
    try:
        _xi = bisection_method(
            polynom.value, _a0, _b0, tol=1e-12 * max(1, abs(_a0), abs(_b0)), max_iter=200
        )
    except (ValueError, RuntimeError):
        _xi = None

    _curves = {"Fehlerschranke (b₀ − a₀) / 2ⁿ": _bound}
    if _xi is not None:
        _error = np.array([abs(_c - _xi) for _, _, _c in bisection_history])
        # log-Achse: exakte Treffer (Fehler 0) nicht zeichnen
        _curves["tatsächlicher Fehler |cₙ − ξ|"] = np.where(_error > 0, _error, np.nan)

    _fig = px.line(
        x=_steps,
        y=list(_curves.values()),
        markers=True,
        log_y=True,
        labels={"x": "Schritt n", "value": "Fehler", "variable": ""},
    )
    for _trace, _name in zip(_fig.data, _curves):
        _trace.name = _name
    _fig.add_hline(
        y=tolerance.value, line_dash="dot", line_color="gray", annotation_text="Toleranz δ"
    )
    _fig.update_layout(legend=dict(orientation="h", y=1.12))

    _predicted = max(1, int(np.ceil(np.log2(_length / tolerance.value))))
    _actual = len(bisection_history)
    _text = (
        f"Vorhersage: $n = \\lceil \\log_2 \\frac{{{_length:g}}}{{{tolerance.value:g}}} \\rceil = {_predicted}$ Schritte. "
        f"Tatsächlich gebraucht: **{_actual}**."
    )
    if _actual < _predicted:
        _text += " (Früher fertig, weil ein Mittelpunkt die Nullstelle exakt getroffen hat.)"

    mo.vstack([_fig, mo.md(_text)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Verständnisfragen

    Probiere die Fragen zuerst selbst im Notebook aus und klappe dann die Antwort auf.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        r"1. Warum braucht das Verfahren einen Vorzeichenwechsel? Probiere $f(x) = x^2$ auf $[-1, 1]$.": mo.md(r"""
    Wähle $a = 0,\ b = 1,\ c = 0,\ d = 0$. Dann ist $f(-1) = f(1) = 1 > 0$, obwohl $f(0) = 0$.
    Ohne Vorzeichenwechsel weiß das Verfahren nicht, welche Hälfte es behalten soll – und der
    Zwischenwertsatz garantiert auch keine Nullstelle (z.B. hat $x^2 + 1$ gar keine).
    Nullstellen, bei denen $f$ das Vorzeichen **nicht** wechselt (doppelte Nullstellen), findet
    das Bisektionsverfahren deshalb nicht.
    """),
        r"2. Was passiert, wenn im Startintervall mehrere Nullstellen liegen?": mo.md(r"""
    Wähle $f(x) = x^3 - x$ (also $a = 1,\ b = 0,\ c = -1,\ d = 0$) mit Nullstellen $-1, 0, 1$.
    Das Verfahren findet **eine** davon – welche, hängt vom Startintervall ab. Vergleiche
    $[-2, 1.5]$, $[-1.5, 2]$ und $[-2, 2]$ (hier trifft schon der erste Mittelpunkt die Nullstelle $0$).
    Der Zwischenwertsatz garantiert eben nur *mindestens eine* Nullstelle.
    """),
        r"3. Wie viele Schritte braucht man für die Genauigkeit $10^{-6}$, wenn das Startintervall Länge $1$ hat?": mo.md(r"""
    Man braucht $\frac{1}{2^n} \le 10^{-6}$, also $n \ge \log_2 10^6 \approx 19.93$, d.h. $n = 20$ Schritte –
    für **jede** stetige Funktion. Faustregel: Pro Dezimalstelle braucht man etwa
    $\log_2 10 \approx 3.3$ Halbierungen.
    """),
        r"4. Inwiefern ist das Bisektionsverfahren ein Beweis des Zwischenwertsatzes?": mo.md(r"""
    Die Intervalle $[a_k, b_k]$ bilden eine **Intervallschachtelung**: $(a_k)$ ist monoton wachsend,
    $(b_k)$ monoton fallend, beide beschränkt, und $b_k - a_k \to 0$. Nach dem Vollständigkeitsaxiom
    konvergieren beide gegen dasselbe $\xi$. Da stets $f(a_k) \cdot f(b_k) < 0$ gilt und $f$ stetig ist, folgt
    $$f(\xi)^2 = \lim_{k\to\infty} f(a_k) \cdot f(b_k) \le 0, \quad\text{also}\quad f(\xi) = 0.$$
    Genau so wird der Zwischenwertsatz in vielen Vorlesungen bewiesen. Über $\mathbb{Q}$ funktioniert
    das nicht: $x^2 - 2$ wechselt auf $[1, 2]$ das Vorzeichen, hat aber keine rationale Nullstelle.
    """),
        r"5. Ist die Stetigkeit wirklich nötig? Was passiert bei $f(x) = \frac{1}{x}$ auf $[-1, 1]$?": mo.md(r"""
    $f(-1) = -1 < 0 < 1 = f(1)$, aber $\frac{1}{x}$ hat keine Nullstelle. Das Verfahren läuft trotzdem
    und schrumpft das Intervall auf die Polstelle $0$ zusammen – dort ist $f$ nicht einmal definiert.
    Ohne Stetigkeit liefert die Intervallschachtelung einen Punkt, aber keine Nullstelle.
    """),
        r"6. Warum wird der Mittelpunkt als `a / 2 + b / 2` berechnet?": mo.md(r"""
    Mathematisch ist $\frac{a}{2} + \frac{b}{2} = \frac{a + b}{2}$. Auf dem Computer haben Gleitkommazahlen aber
    einen größten Wert (etwa $1.8 \cdot 10^{308}$). Für $a = b = 10^{308}$ ergibt `a + b` schon `inf`,
    während `a / 2 + b / 2` korrekt $10^{308}$ liefert. Rechnen mit Gleitkommazahlen folgt nicht
    immer den Regeln der reellen Zahlen.
    """),
        r"7. Kann man die Toleranz beliebig klein wählen?": mo.md(r"""
    Mathematisch ja, auf dem Computer nicht: Gleitkommazahlen liegen nicht beliebig dicht.
    Irgendwann gibt es zwischen $a$ und $b$ keine weitere darstellbare Zahl, und der Mittelpunkt $c$ ist gleich
    $a$ oder $b$. `bisection_method` erkennt diesen Fall und bricht mit einer Fehlermeldung ab,
    statt endlos weiterzulaufen.
    """),
    })
    return


if __name__ == "__main__":
    app.run()
