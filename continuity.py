import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.express as px

    return mo, np, px


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Stetigkeit

    Anschaulich ist eine Funktion $f$ **stetig** in $x_0$, wenn kleine Änderungen von $x$ nur
    kleine Änderungen von $f(x)$ bewirken: Der Graph hat bei $x_0$ keinen Sprung, kein Loch und
    schwingt nicht wild hin und her.

    Mathematisch gibt es dafür zwei gleichwertige Definitionen:

    1. die **$\varepsilon$-$\delta$-Definition** – kurz in Abschnitt 1,
    2. die **Grenzwert-Definition** $\lim_{x \to x_0} f(x) = f(x_0)$ mit Folgen – ab Abschnitt 2.
       Mit dieser Definition arbeitet man in der Praxis meistens.
    """)
    return


@app.cell(hide_code=True)
def _(np):
    def with_value_at(g, x0, f0):
        """Funktion, die für x != x0 den Wert g(x) und an der Stelle x0 den Wert f0 hat."""

        def f(x):
            x = np.asarray(x, dtype=float)
            with np.errstate(divide="ignore", invalid="ignore"):
                y = g(x)
            return np.where(x == x0, f0, y)

        return f


    functions = {
        "x²": dict(
            f=with_value_at(lambda x: x**2, 1.0, 1.0),
            tex=r"f(x) = x^2",
            x0=1.0,
            f0=1.0,
            left="1",
            right="1",
            limit=1.0,
            window=1.0,
            y_range=[-0.5, 4.5],
            special={},
            explanation=r"""
    Aus $x_n \to 1$ folgt mit den Grenzwertsätzen $x_n^2 = x_n \cdot x_n \to 1 \cdot 1 = 1 = f(1)$ –
    für **jede** Folge. Genauso sind alle Polynome überall stetig.
    """,
        ),
        "Sprungfunktion": dict(
            f=with_value_at(lambda x: np.where(x < 0, 0.0, 1.0), 0.0, 1.0),
            tex=r"f(x) = \begin{cases} 0 & x < 0 \\ 1 & x \ge 0 \end{cases}",
            x0=0.0,
            f0=1.0,
            left="0",
            right="1",
            limit=None,
            window=1.0,
            y_range=[-0.5, 1.5],
            special={},
            explanation=r"""
    Von rechts gilt $f(x_n) = 1 \to 1 = f(0)$, von links aber $f(x_n) = 0 \to 0 \ne f(0)$.
    Links- und rechtsseitiger Grenzwert sind verschieden, also existiert $\lim_{x\to 0} f(x)$ nicht:
    eine **Sprungstelle**.
    """,
        ),
        "Hebbare Lücke": dict(
            f=with_value_at(lambda x: (x**2 - 1) / (x - 1), 1.0, 3.0),
            tex=r"f(x) = \begin{cases} \dfrac{x^2 - 1}{x - 1} & x \ne 1 \\ 3 & x = 1 \end{cases}",
            x0=1.0,
            f0=3.0,
            left="2",
            right="2",
            limit=2.0,
            window=1.0,
            y_range=[0, 4],
            special={},
            explanation=r"""
    Für $x \ne 1$ ist $\frac{x^2 - 1}{x - 1} = \frac{(x-1)(x+1)}{x-1} = x + 1 \to 2$.
    Der Grenzwert existiert, ist aber **nicht** gleich $f(1) = 3$. Definiert man stattdessen
    $f(1) = 2$, wird $f$ stetig – deshalb heißt die Stelle **hebbare Unstetigkeit**.
    """,
        ),
        "sin(x)/x": dict(
            f=with_value_at(lambda x: np.sin(x) / x, 0.0, 1.0),
            tex=r"f(x) = \begin{cases} \dfrac{\sin x}{x} & x \ne 0 \\ 1 & x = 0 \end{cases}",
            x0=0.0,
            f0=1.0,
            left="1",
            right="1",
            limit=1.0,
            window=3.0,
            y_range=[-0.5, 1.5],
            special={},
            explanation=r"""
    Der berühmte Grenzwert $\lim_{x\to 0} \frac{\sin x}{x} = 1$ (z.B. mit der Reihe
    $\sin x = x - \frac{x^3}{6} + \dots$). Mit $f(0) = 1$ ist $f$ stetig: Die Definitionslücke
    von $\frac{\sin x}{x}$ wurde **stetig fortgesetzt**.
    """,
        ),
        "|x|": dict(
            f=with_value_at(np.abs, 0.0, 0.0),
            tex=r"f(x) = |x|",
            x0=0.0,
            f0=0.0,
            left="0",
            right="0",
            limit=0.0,
            window=1.0,
            y_range=[-0.5, 1.5],
            special={},
            explanation=r"""
    Aus $x_n \to 0$ folgt $|x_n| \to 0 = f(0)$. Der Graph hat bei $0$ einen **Knick** – $f$ ist dort
    nicht differenzierbar, aber trotzdem stetig.
    """,
        ),
        "sin(1/x)": dict(
            f=with_value_at(lambda x: np.sin(1 / x), 0.0, 0.0),
            tex=r"f(x) = \begin{cases} \sin\left(\frac{1}{x}\right) & x \ne 0 \\ 0 & x = 0 \end{cases}",
            x0=0.0,
            f0=0.0,
            left=None,
            right=None,
            limit=None,
            window=1.0,
            y_range=[-1.5, 1.5],
            special={
                "speziell: xₙ = 1/(πn)": lambda n, x0: 1 / (np.pi * n),
                "speziell: xₙ = 1/(π/2 + 2πn)": lambda n, x0: 1 / (np.pi / 2 + 2 * np.pi * n),
            },
            explanation=r"""
    Für $x_n = \frac{1}{\pi n}$ ist $f(x_n) = \sin(\pi n) = 0 \to 0 = f(0)$ – diese Folge passt.
    Für $x_n = \frac{1}{\pi/2 + 2\pi n}$ ist aber $f(x_n) = 1 \to 1 \ne f(0)$.
    Zwei Folgen mit verschiedenen Grenzwerten: $\lim_{x\to 0} f(x)$ existiert nicht.
    Egal wie man $f(0)$ wählt, $f$ wird nie stetig.
    """,
        ),
        "x·sin(1/x)": dict(
            f=with_value_at(lambda x: x * np.sin(1 / x), 0.0, 0.0),
            tex=r"f(x) = \begin{cases} x \sin\left(\frac{1}{x}\right) & x \ne 0 \\ 0 & x = 0 \end{cases}",
            x0=0.0,
            f0=0.0,
            left="0",
            right="0",
            limit=0.0,
            window=1.0,
            y_range=[-1, 1],
            special={
                "speziell: xₙ = 1/(π/2 + 2πn)": lambda n, x0: 1 / (np.pi / 2 + 2 * np.pi * n),
            },
            explanation=r"""
    Die Funktion schwingt unendlich oft, aber die Ausschläge werden kleiner:
    $|f(x_n) - 0| = |x_n| \cdot \left|\sin\tfrac{1}{x_n}\right| \le |x_n| \to 0$ für **jede** Folge $x_n \to 0$.
    Also ist $f$ in $0$ stetig.
    """,
        ),
        "1/x": dict(
            f=with_value_at(lambda x: 1 / x, 0.0, 0.0),
            tex=r"f(x) = \begin{cases} \dfrac{1}{x} & x \ne 0 \\ 0 & x = 0 \end{cases}",
            x0=0.0,
            f0=0.0,
            left=r"-\infty",
            right=r"+\infty",
            limit=None,
            window=1.0,
            y_range=[-10, 10],
            special={},
            explanation=r"""
    Für $x_n = \frac{1}{n}$ ist $f(x_n) = n \to \infty$: Die Bildfolge ist unbeschränkt und
    konvergiert nicht. Bei $0$ liegt eine **Polstelle** – egal welchen Wert $f(0)$ bekommt,
    $f$ ist dort unstetig.
    """,
        ),
    }

    sequences = {
        "von rechts: xₙ = x₀ + 1/n": lambda n, x0: x0 + 1 / n,
        "von links: xₙ = x₀ − 1/n": lambda n, x0: x0 - 1 / n,
        "alternierend: xₙ = x₀ + (−1)ⁿ/n": lambda n, x0: x0 + (-1.0) ** n / n,
    }
    return functions, sequences


@app.cell(hide_code=True)
def _(np, px):
    def plot_function(fn, half_width=None):
        """Graph von f um x0; f(x0) als gefüllter Punkt, eine Lücke im Graphen als offener Kreis."""
        x0 = fn["x0"]
        w = fn["window"] if half_width is None else half_width
        x_left = np.linspace(x0 - w, x0, 3000, endpoint=False)
        x_right = np.linspace(x0 + w, x0, 3000, endpoint=False)[::-1]
        x = np.concatenate([x_left, [x0], x_right])
        y = fn["f"](x).astype(float)
        # Linke und rechte Hälfte nicht über x0 hinweg verbinden
        y[len(x_left)] = np.nan

        fig = px.line(x=x, y=y, labels={"x": "x", "y": "f(x)"})
        if fn["limit"] is not None and fn["limit"] != fn["f0"]:
            fig.add_scatter(
                x=[x0],
                y=[fn["limit"]],
                mode="markers",
                marker=dict(size=11, color="white", line=dict(color="royalblue", width=2)),
            )
        fig.add_scatter(
            x=[x0], y=[fn["f0"]], mode="markers", marker=dict(size=11, color="black")
        )
        fig.update_xaxes(range=[x0 - w, x0 + w])
        fig.update_yaxes(range=fn["y_range"])
        fig.update_layout(showlegend=False)
        return fig

    return (plot_function,)


@app.cell(hide_code=True)
def _(functions, mo):
    function_choice = mo.ui.dropdown(
        options=list(functions), value="x²", label="Funktion"
    )
    epsilon = mo.ui.slider(
        steps=[1, 0.5, 0.2, 0.1, 0.05, 0.01],
        value=0.5,
        label=r"Zweiflerin wählt $\varepsilon$",
        show_value=True,
    )
    delta = mo.ui.slider(
        steps=[1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.001],
        value=0.5,
        label=r"Beweiser wählt $\delta$",
        show_value=True,
    )
    zoom_switch = mo.ui.switch(label=r"Auf die $\delta$-Umgebung zoomen")
    n_show = mo.ui.slider(
        start=1, stop=50, step=1, value=10, label="Folgenglieder bis $n =$", show_value=True
    )
    return delta, epsilon, function_choice, n_show, zoom_switch


@app.cell(hide_code=True)
def _(function_choice, functions):
    selected = functions[function_choice.value]
    return (selected,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Die $\varepsilon$-$\delta$-Definition

    $f\colon D \to \mathbb{R}$ heißt **stetig in** $x_0 \in D$, wenn gilt:

    $$
    \forall \varepsilon > 0 \;\; \exists \delta > 0 \;\; \forall x \in D: \quad
    |x - x_0| < \delta \implies |f(x) - f(x_0)| < \varepsilon .
    $$

    Das ist dasselbe Spiel wie beim Grenzwert einer Folge: Die **Zweiflerin** wählt eine
    Toleranz $\varepsilon$ für die $y$-Werte (grüner Streifen). Der **Beweiser** antwortet mit einem
    $\delta$ (blauer Streifen). Er gewinnt, wenn der Graph über dem ganzen blauen Streifen im
    grünen Streifen bleibt. Rote Punkte zeigen, wo das nicht klappt.
    """)
    return


@app.cell(hide_code=True)
def _(
    delta,
    epsilon,
    function_choice,
    mo,
    np,
    plot_function,
    selected,
    zoom_switch,
):
    _x0, _f0 = selected["x0"], selected["f0"]
    _eps, _delta = epsilon.value, delta.value

    # Fein abgetastetes offenes Intervall (x0 - δ, x0 + δ)
    _xs = _x0 + _delta * np.linspace(-1, 1, 20001)[1:-1]
    _dev = np.abs(selected["f"](_xs) - _f0)
    _bad = ~(_dev < _eps)  # auch inf/nan zählen als Verletzung

    if zoom_switch.value:
        _fig = plot_function(selected, half_width=3 * _delta)
        _fig.update_yaxes(range=[_f0 - 3 * _eps, _f0 + 3 * _eps])
    else:
        _fig = plot_function(selected)
    _fig.add_hrect(
        y0=_f0 - _eps, y1=_f0 + _eps, fillcolor="seagreen", opacity=0.15, line_width=0
    )
    _fig.add_vrect(
        x0=_x0 - _delta, x1=_x0 + _delta, fillcolor="royalblue", opacity=0.12, line_width=0
    )
    _bad_idx = np.flatnonzero(_bad)
    if len(_bad_idx) > 0:
        _shown = _bad_idx[:: max(1, len(_bad_idx) // 300)]
        _fig.add_scatter(
            x=_xs[_shown],
            y=selected["f"](_xs[_shown]),
            mode="markers",
            marker=dict(size=5, color="crimson"),
        )

    if len(_bad_idx) == 0:
        _feedback = mo.callout(
            mo.md(
                f"**Gewonnen!** Für alle geprüften $x$ mit $|x - x_0| < \\delta = {_delta}$ gilt "
                f"$|f(x) - f(x_0)| < \\varepsilon = {_eps}$. Wähle ein kleineres $\\varepsilon$."
            ),
            kind="success",
        )
    else:
        # Die Verletzung, die am nächsten an x0 liegt
        _i = _bad_idx[np.argmin(np.abs(_xs[_bad_idx] - _x0))]
        _feedback = mo.callout(
            mo.md(
                f"**Noch nicht:** Für $x = {_xs[_i]:.4g}$ ist $|f(x) - f(x_0)| = {_dev[_i]:.3g} "
                f"\\ge \\varepsilon$. Versuche ein kleineres $\\delta$. Wenn **kein** $\\delta$ hilft, "
                "ist $f$ in $x_0$ unstetig."
            ),
            kind="danger",
        )

    mo.vstack([
        function_choice,
        mo.md(f"$${selected['tex']}, \\qquad x_0 = {_x0:g}$$"),
        mo.hstack([epsilon, delta, zoom_switch], justify="start"),
        _fig,
        _feedback,
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Stetigkeit über Grenzwerte

    Die $\varepsilon$-$\delta$-Definition ist präzise, aber im Alltag mühsam. Meistens arbeitet man mit
    Grenzwerten von **Folgen** – die kennen wir schon.

    **Grenzwert einer Funktion.** Man schreibt $\lim_{x \to x_0} f(x) = c$, wenn für **jede** Folge
    $(x_n)$ in $D$ mit $x_n \ne x_0$ und $x_n \to x_0$ gilt:

    $$
    f(x_n) \to c .
    $$

    **Stetigkeit.** $f$ ist stetig in $x_0$, wenn

    $$
    \lim_{x \to x_0} f(x) = f(x_0) .
    $$

    In der Praxis prüft man drei Dinge:

    1. $f(x_0)$ ist **definiert**.
    2. Der Grenzwert $\lim_{x \to x_0} f(x)$ **existiert**. Insbesondere müssen der
       linksseitige Grenzwert $\lim_{x \to x_0^-} f(x)$ (nur $x_n < x_0$) und der rechtsseitige
       Grenzwert $\lim_{x \to x_0^+} f(x)$ (nur $x_n > x_0$) existieren und **gleich** sein.
    3. Der Grenzwert ist **gleich** $f(x_0)$.

    Beide Definitionen sind gleichwertig: Eine Funktion ist genau dann $\varepsilon$-$\delta$-stetig,
    wenn sie die Grenzwert-Bedingung erfüllt.
    """)
    return


@app.cell(hide_code=True)
def _(mo, selected, sequences):
    sequence_options = {**sequences, **selected["special"]}
    sequence_choice = mo.ui.dropdown(
        options=list(sequence_options), value=list(sequence_options)[0], label="Folge"
    )
    return sequence_choice, sequence_options


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Experiment: Folgen gegen $x_0$ schicken

    1. Wähle eine Funktion und eine Folge $x_n \to x_0$.
    2. Links siehst du die Punkte $(x_n, f(x_n))$ auf dem Graphen, rechts die Bildfolge $f(x_n)$.
    3. Konvergiert $f(x_n)$ gegen $f(x_0)$ (schwarzer Punkt bzw. gestrichelte Linie)?

    **Wichtig:** Passt eine Folge, ist das noch **kein** Beweis für Stetigkeit – es muss für
    **alle** Folgen gelten. Passt aber eine einzige Folge **nicht**, ist $f$ in $x_0$ sicher unstetig.
    Versuche, für die unstetigen Funktionen eine solche Gegenfolge zu finden.
    """)
    return


@app.cell(hide_code=True)
def _(
    function_choice,
    mo,
    n_show,
    np,
    plot_function,
    px,
    selected,
    sequence_choice,
    sequence_options,
):
    _x0, _f0 = selected["x0"], selected["f0"]
    _seq = sequence_options[sequence_choice.value]

    # Viele Folgenglieder berechnen, um die Konvergenz von f(x_n) abzuschätzen
    _n_all = np.arange(1, 100_001)
    _x_all = _seq(_n_all, _x0)
    _y_all = selected["f"](_x_all).astype(float)
    _tail = _y_all[50_000:]
    _converges = bool(np.all(np.isfinite(_tail)) and np.ptp(_tail) < 1e-3)
    _L = float(_y_all[-1])

    _n = _n_all[: n_show.value]
    _xn = _x_all[: n_show.value]
    _yn = _y_all[: n_show.value]

    _fig_graph = plot_function(selected)
    _fig_graph.add_scatter(
        x=_xn,
        y=_yn,
        mode="markers",
        marker=dict(size=8, color=_n, colorscale="Viridis"),
        hovertext=[f"n = {_i}" for _i in _n],
    )
    _fig_graph.update_layout(title="Punkte (xₙ, f(xₙ)) auf dem Graphen")

    _fig_seq = px.scatter(
        x=_n,
        y=_yn,
        color=_n,
        color_continuous_scale="Viridis",
        labels={"x": "n", "y": "f(xₙ)", "color": "n"},
    )
    _fig_seq.add_hline(
        y=_f0, line_dash="dash", line_color="black", annotation_text="f(x₀)"
    )
    _fig_seq.update_layout(title="Bildfolge f(xₙ)", coloraxis_showscale=False)

    if not _converges:
        _feedback = mo.callout(
            mo.md(
                "**Gegenfolge gefunden:** $f(x_n)$ konvergiert **nicht**. Also existiert "
                "$\\lim_{x \\to x_0} f(x)$ nicht, und $f$ ist in $x_0$ **unstetig**. "
                "Eine einzige solche Folge genügt als Beweis."
            ),
            kind="danger",
        )
    elif abs(_L - _f0) >= 1e-3:
        _feedback = mo.callout(
            mo.md(
                f"**Gegenfolge gefunden:** $f(x_n) \\to {_L:.4g}$, aber $f(x_0) = {_f0:g}$. "
                "Also ist $f$ in $x_0$ **unstetig**. Eine einzige solche Folge genügt als Beweis."
            ),
            kind="danger",
        )
    else:
        _feedback = mo.callout(
            mo.md(
                f"**Diese Folge passt:** $f(x_n) \\to {_L:.4g} \\approx f(x_0) = {_f0:g}$. "
                "Das ist ein Indiz, aber **kein Beweis** für Stetigkeit – es muss für **jede** "
                "Folge $x_n \\to x_0$ gelten. Probiere andere Folgen aus!"
            ),
            kind="success",
        )

    mo.vstack([
        mo.hstack([function_choice, sequence_choice], justify="start"),
        mo.md(f"$${selected['tex']}, \\qquad x_0 = {_x0:g}, \\qquad f(x_0) = {_f0:g}$$"),
        n_show,
        mo.hstack([_fig_graph, _fig_seq], widths="equal"),
        _feedback,
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Links- und rechtsseitiger Grenzwert

    Ein schneller Test in der Praxis: Werte $f$ dicht links und dicht rechts von $x_0$ aus,
    also $f(x_0 - h)$ und $f(x_0 + h)$ für immer kleinere $h$. Nähern sich beide Spalten demselben
    Wert – und ist das $f(x_0)$?

    Entscheide selbst und klappe dann die Auflösung auf.
    """)
    return


@app.cell(hide_code=True)
def _(function_choice, mo, np, selected):
    _x0, _f0 = selected["x0"], selected["f0"]
    _h = 10.0 ** -np.arange(1, 7)
    _table = mo.ui.table(
        [
            {
                "h": f"{_hi:g}",
                "f(x₀ − h)": f"{float(selected['f'](_x0 - _hi)):.6g}",
                "f(x₀ + h)": f"{float(selected['f'](_x0 + _hi)):.6g}",
            }
            for _hi in _h
        ],
        selection=None,
    )

    _limit = selected["limit"]
    _limit_exists = _limit is not None
    _is_continuous = _limit_exists and _limit == _f0


    def _mark(ok):
        return "✅" if ok else "❌"


    def _side(sign, value):
        """Einseitigen Grenzwert als LaTeX anzeigen; None bedeutet: existiert nicht."""
        _lim = f"\\lim_{{x \\to x_0^{sign}}} f(x)"
        return f"${_lim}$ existiert nicht" if value is None else f"${_lim} = {value}$"


    if _limit_exists:
        _step2 = "Beide existieren und sind gleich."
        _relation = "=" if _is_continuous else r"\ne"
        _step3 = f"$\\lim_{{x \\to x_0}} f(x) = {_limit:g} {_relation} f(x_0) = {_f0:g}$."
    else:
        _step2 = "Sie sind nicht gleich bzw. existieren nicht, also existiert der Grenzwert **nicht**."
        _step3 = "Ohne Grenzwert kann er auch nicht gleich $f(x_0)$ sein."

    _checklist = mo.md(
        f"""
    1. {_mark(True)} $f(x_0)$ ist definiert: $f({_x0:g}) = {_f0:g}$.
    2. {_mark(_limit_exists)} Linksseitiger Grenzwert: {_side("-", selected["left"])}.
       Rechtsseitiger Grenzwert: {_side("+", selected["right"])}. {_step2}
    3. {_mark(_is_continuous)} {_step3}
    """
    )
    _verdict = mo.callout(
        mo.md(
            f"**$f$ ist in $x_0 = {_x0:g}$ {'stetig' if _is_continuous else 'unstetig'}.**\n"
            + selected["explanation"]
        ),
        kind="success" if _is_continuous else "danger",
    )

    mo.vstack([
        function_choice,
        mo.md(f"$${selected['tex']}, \\qquad x_0 = {_x0:g}$$"),
        _table,
        mo.accordion({"Auflösung: Ist $f$ in $x_0$ stetig?": mo.vstack([_checklist, _verdict])}),
    ])
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
        r"1. Bei $\sin(1/x)$ liefert die Folge $x_n = \frac{1}{\pi n}$ genau $f(x_n) \to f(0)$. Ist $f$ also stetig?": mo.md(r"""
    Nein. Die Definition verlangt $f(x_n) \to f(x_0)$ für **jede** Folge $x_n \to x_0$. Mit
    $x_n = \frac{1}{\pi/2 + 2\pi n}$ gilt $f(x_n) = 1 \not\to 0$. Eine passende Folge beweist nichts,
    eine einzige unpassende Folge beweist Unstetigkeit.
    """),
        r"2. Wie muss man bei der hebbaren Lücke $f(1)$ wählen, damit $f$ stetig wird?": mo.md(r"""
    $f(1) = 2$, denn $\lim_{x \to 1} \frac{x^2 - 1}{x - 1} = \lim_{x \to 1} (x + 1) = 2$. Allgemein: Existiert
    $\lim_{x \to x_0} f(x)$, kann man eine Lücke durch diesen Wert **stetig schließen**
    (wie bei $\frac{\sin x}{x}$ mit $f(0) = 1$).
    """),
    r"3. Kann man bei der Sprungfunktion $f(0)$ so wählen, dass $f$ stetig wird?": mo.md(r"""
    Nein. Der linksseitige Grenzwert ist $0$, der rechtsseitige $1$. Der Grenzwert
    $\lim_{x \to 0} f(x)$ existiert also gar nicht – und dann hilft kein Wert für $f(0)$.
    Dasselbe gilt für $\sin(1/x)$ und $1/x$.
    """),
        r"4. „Stetig heißt: Man kann den Graphen ohne Absetzen zeichnen.“ Stimmt das?": mo.md(r"""
    Nur als grobe Faustregel auf Intervallen. Zwei Gegenbeispiele:

    - $x \sin(1/x)$ (mit $f(0) = 0$) ist stetig, schwingt aber bei $0$ unendlich oft – zeichnen kann
      man das nicht.
    - $f(x) = \frac{1}{x}$ auf $D = \mathbb{R} \setminus \{0\}$ ist **stetig**, denn sie ist in jedem Punkt
      ihres Definitionsbereichs stetig. Die Stelle $0$ gehört nicht zu $D$, also wird dort nichts geprüft.
      Unstetig wird sie erst, wenn man ihr wie oben einen Wert $f(0)$ gibt.
    """),
        r"5. $|x|$ hat bei $0$ einen Knick. Ist sie dort unstetig?": mo.md(r"""
    Nein. Stetig heißt „kein Sprung, kein Loch“, nicht „glatt“. $|x|$ ist bei $0$ stetig, aber nicht
    **differenzierbar**: Die Steigung springt von $-1$ auf $1$. Jede differenzierbare Funktion ist
    stetig, aber nicht umgekehrt.
    """),
        r"6. Wie hängt die $\varepsilon$-$\delta$-Definition mit der Folgen-Definition zusammen?": mo.md(r"""
    Sie sind gleichwertig. Die eine Richtung ist kurz: Sei $f$ $\varepsilon$-$\delta$-stetig und $x_n \to x_0$.
    Zu $\varepsilon > 0$ gibt es ein $\delta$, und wegen $x_n \to x_0$ gibt es ein $N$ mit $|x_n - x_0| < \delta$
    für alle $n \ge N$. Dann gilt $|f(x_n) - f(x_0)| < \varepsilon$ für alle $n \ge N$, also $f(x_n) \to f(x_0)$.
    Das $\delta$ der Funktion wird zum $N$ der Folge.
    """),
        r"7. Die Wertetabelle in Abschnitt 4 sieht gut aus. Ist das ein Beweis?": mo.md(r"""
    Nein. Die Tabelle prüft nur endlich viele, speziell gewählte Stellen. Beispiel:
    $f(x) = \sin(\pi / x)$ mit $f(0) = 0$. Für $h = 10^{-k}$ ist $f(\pm h) = \sin(\pm\pi \cdot 10^k) = 0$, die Tabelle
    zeigt also nur Nullen – trotzdem ist $f$ in $0$ unstetig (gleiche Begründung wie bei $\sin(1/x)$).
    Tabellen sind ein gutes Werkzeug, um eine **Vermutung** zu finden; beweisen muss man sie anders.
    """),
    })
    return


if __name__ == "__main__":
    app.run()
