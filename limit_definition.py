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
    # Der Grenzwert einer Folge

    Eine Folge $(a_n)_{n\in\mathbb{N}}$ **konvergiert gegen** $a \in \mathbb{R}$, wenn gilt:

    $$
    \forall \varepsilon > 0 \;\; \exists N \in \mathbb{N} \;\; \forall n \ge N: \quad |a_n - a| < \varepsilon .
    $$

    Man schreibt dann $\lim_{n\to\infty} a_n = a$.

    Die Bedingung $|a_n - a| < \varepsilon$ bedeutet: $a_n$ liegt im **$\varepsilon$-Schlauch** $(a - \varepsilon,\; a + \varepsilon)$ um $a$.

    ### Die Definition als Spiel

    Man kann die Definition als Spiel zwischen zwei Personen lesen:

    1. Die **Zweiflerin** wählt eine Toleranz $\varepsilon > 0$ – so klein sie will.
    2. Der **Beweiser** antwortet mit einem Index $N$.
    3. Der Beweiser gewinnt, wenn **alle** Folgenglieder $a_N, a_{N+1}, a_{N+2}, \dots$ im $\varepsilon$-Schlauch liegen.

    Die Folge konvergiert gegen $a$, wenn der Beweiser **auf jedes** $\varepsilon$ eine Antwort hat.
    Die Reihenfolge der Quantoren ist entscheidend: Zuerst wird $\varepsilon$ gewählt, *danach* $N$ –
    das $N$ darf also von $\varepsilon$ abhängen.
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # Größter Index, bis zu dem der Computer die Folgenglieder prüft
    CHECK_MAX = 1_000_000
    n_values = np.arange(1, CHECK_MAX + 1)

    sequences = {
        "1/n": dict(
            formula=lambda n: 1 / n,
            tex=r"a_n = \frac{1}{n}",
            limit=0.0,
            proof=r"""
    Es gilt $|a_n - 0| = \frac{1}{n} < \varepsilon \iff n > \frac{1}{\varepsilon}$.
    Wähle also $N = \lfloor 1/\varepsilon \rfloor + 1$. Dann gilt für alle $n \ge N$:
    $|a_n - 0| = \frac{1}{n} \le \frac{1}{N} < \varepsilon$.
    """,
        ),
        "(−1)ⁿ/n": dict(
            formula=lambda n: (-1.0) ** n / n,
            tex=r"a_n = \frac{(-1)^n}{n}",
            limit=0.0,
            proof=r"""
    Es gilt $|a_n - 0| = \frac{1}{n}$ – genau wie bei $\frac{1}{n}$, also funktioniert
    $N = \lfloor 1/\varepsilon \rfloor + 1$. Die Folge springt abwechselnd über und unter
    den Grenzwert: Konvergenz bedeutet **nicht**, dass sich die Folge von einer Seite nähert.
    """,
        ),
        "n/(n+1)": dict(
            formula=lambda n: n / (n + 1),
            tex=r"a_n = \frac{n}{n+1}",
            limit=1.0,
            proof=r"""
    Es gilt $|a_n - 1| = \left|\frac{n - (n+1)}{n+1}\right| = \frac{1}{n+1} < \frac{1}{n}$.
    Also funktioniert wieder $N = \lfloor 1/\varepsilon \rfloor + 1$ – auch wenn das
    nicht immer das *kleinste* passende $N$ ist. Das muss es auch nicht sein!
    """,
        ),
        "sin(n)/n": dict(
            formula=lambda n: np.sin(n) / n,
            tex=r"a_n = \frac{\sin(n)}{n}",
            limit=0.0,
            proof=r"""
    Hier kann man $|a_n|$ nicht exakt ausrechnen, aber **abschätzen**:
    $|a_n - 0| = \frac{|\sin(n)|}{n} \le \frac{1}{n}$.
    Also funktioniert $N = \lfloor 1/\varepsilon \rfloor + 1$. Das kleinste passende $N$
    ist oft deutlich kleiner – für den Beweis ist das egal.
    """,
        ),
        "1/√n": dict(
            formula=lambda n: 1 / np.sqrt(n),
            tex=r"a_n = \frac{1}{\sqrt{n}}",
            limit=0.0,
            proof=r"""
    Es gilt $\frac{1}{\sqrt{n}} < \varepsilon \iff n > \frac{1}{\varepsilon^2}$.
    Wähle $N = \lfloor 1/\varepsilon^2 \rfloor + 1$. Für $\varepsilon = 0.01$ ist das
    schon $N = 10\,001$: Die Folge konvergiert, aber **langsam** – $N$ wächst schnell,
    wenn $\varepsilon$ kleiner wird.
    """,
        ),
        "(1 + 1/n)ⁿ": dict(
            formula=lambda n: (1 + 1 / n) ** n,
            tex=r"a_n = \left(1 + \frac{1}{n}\right)^n",
            limit=float(np.e),
            proof=r"""
    Diese Folge konvergiert gegen die Eulersche Zahl $e \approx 2.71828$. Ein passendes $N$
    lässt sich hier nicht so einfach hinschreiben; man zeigt die Konvergenz z.B. über
    Monotonie und Beschränktheit. Die Definition sagt nur, dass ein $N$ **existiert** –
    man muss es nicht explizit angeben können.
    """,
        ),
        "(−1)ⁿ (divergent)": dict(
            formula=lambda n: (-1.0) ** n,
            tex=r"a_n = (-1)^n",
            limit=None,
            proof=r"""
    Die Folge springt zwischen $-1$ und $1$. Angenommen, sie konvergiert gegen ein $a$.
    Wähle $\varepsilon = 1$. Für jedes $N$ gibt es ein gerades und ein ungerades $n \ge N$, also
    $$2 = |1 - (-1)| \le |1 - a| + |a - (-1)| < \varepsilon + \varepsilon = 2,$$
    ein Widerspruch. Die Zweiflerin gewinnt also mit $\varepsilon = 1$ – egal welches $a$ und
    welches $N$ der Beweiser wählt.
    """,
        ),
    }
    return CHECK_MAX, n_values, sequences


@app.cell(hide_code=True)
def _(CHECK_MAX, mo, sequences):
    sequence_choice = mo.ui.dropdown(
        options=list(sequences), value="1/n", label="Folge"
    )
    epsilon = mo.ui.slider(
        steps=[1, 0.5, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001],
        value=0.1,
        label=r"Zweiflerin wählt $\varepsilon$",
        show_value=True,
    )
    N_choice = mo.ui.number(
        start=1, stop=CHECK_MAX // 2, step=1, value=3, label="Beweiser wählt $N$"
    )
    n_display = mo.ui.slider(
        start=10, stop=500, step=10, value=50, label="Anzeigen bis $n =$", show_value=True
    )
    zoom_switch = mo.ui.switch(label=r"Auf den $\varepsilon$-Schlauch zoomen")
    show_solution = mo.ui.switch(label="Kleinstes $N$ verraten")
    return (
        N_choice,
        epsilon,
        n_display,
        sequence_choice,
        show_solution,
        zoom_switch,
    )


@app.cell(hide_code=True)
def _(mo, sequence_choice, sequences):
    _default_limit = sequences[sequence_choice.value]["limit"]
    limit_candidate = mo.ui.number(
        value=1.0 if _default_limit is None else _default_limit,
        step=0.05,
        label="Vermuteter Grenzwert $a$",
    )
    return (limit_candidate,)


@app.cell(hide_code=True)
def _(CHECK_MAX, limit_candidate, n_values, np, sequence_choice, sequences):
    selected = sequences[sequence_choice.value]
    a_values = selected["formula"](n_values)
    deviation = np.abs(a_values - limit_candidate.value)

    # tail_max[k] = größte Abweichung |a_n - a| unter allen Gliedern ab n = k + 1
    tail_max = np.maximum.accumulate(deviation[::-1])[::-1]


    def smallest_N(eps):
        """Kleinstes N mit |a_n - a| < eps für alle N <= n <= CHECK_MAX (sonst None)."""
        inside_from_here = tail_max < eps
        if not inside_from_here.any():
            return None
        N = int(np.argmax(inside_from_here)) + 1
        # Ein N, das erst in der zweiten Hälfte des geprüften Bereichs auftaucht,
        # ist meist nur ein Artefakt des endlichen Ausschnitts (z.B. bei (-1)^n).
        return N if N <= CHECK_MAX // 2 else None

    return a_values, deviation, selected, smallest_N


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Spiel: Finde ein passendes $N$

    1. Wähle eine Folge und einen vermuteten Grenzwert $a$.
    2. Die Zweiflerin wählt ein $\varepsilon$.
    3. Du bist der Beweiser: Suche ein $N$, sodass **ab $N$ alle Punkte grün** sind.
    4. Mache $\varepsilon$ kleiner. Was passiert mit $N$? Gibt es immer ein passendes $N$?

    Graue Punkte (vor $N$) spielen keine Rolle – **endlich viele** Ausreißer sind erlaubt.
    """)
    return


@app.cell(hide_code=True)
def _(
    CHECK_MAX,
    N_choice,
    a_values,
    deviation,
    epsilon,
    limit_candidate,
    mo,
    n_display,
    n_values,
    np,
    px,
    selected,
    sequence_choice,
    show_solution,
    smallest_N,
    zoom_switch,
):
    _eps = epsilon.value
    _a = limit_candidate.value
    _N = int(N_choice.value)
    _n_show = n_display.value

    _n = n_values[:_n_show]
    _y = a_values[:_n_show]
    _status = np.where(
        _n < _N,
        "n < N (spielt keine Rolle)",
        np.where(deviation[:_n_show] < _eps, "n ≥ N, im ε-Schlauch", "n ≥ N, außerhalb"),
    )

    _fig = px.scatter(
        x=_n,
        y=_y,
        color=_status,
        color_discrete_map={
            "n < N (spielt keine Rolle)": "lightgray",
            "n ≥ N, im ε-Schlauch": "seagreen",
            "n ≥ N, außerhalb": "crimson",
        },
        labels={"x": "n", "y": "a_n", "color": ""},
    )
    _fig.add_hrect(y0=_a - _eps, y1=_a + _eps, fillcolor="seagreen", opacity=0.15, line_width=0)
    _fig.add_hline(y=_a, line_dash="dash", line_color="black", annotation_text="a")
    _fig.add_hline(y=_a + _eps, line_dash="dot", line_color="seagreen", annotation_text="a + ε")
    _fig.add_hline(y=_a - _eps, line_dash="dot", line_color="seagreen", annotation_text="a − ε")
    if _N <= _n_show:
        _fig.add_vline(x=_N - 0.5, line_color="royalblue", line_width=2, annotation_text="N")

    if zoom_switch.value:
        _y_range = [_a - 3 * _eps, _a + 3 * _eps]
    else:
        _low = min(_y.min(), _a - _eps)
        _high = max(_y.max(), _a + _eps)
        _pad = 0.1 * (_high - _low)
        _y_range = [_low - _pad, _high + _pad]
    _fig.update_yaxes(range=_y_range)
    _fig.update_layout(legend=dict(orientation="h", y=1.12))

    # Prüfe alle Glieder von N bis CHECK_MAX, nicht nur die angezeigten
    _violations = np.nonzero(deviation[_N - 1 :] >= _eps)[0]
    _best_N = smallest_N(_eps)

    if len(_violations) == 0:
        _feedback = mo.callout(
            mo.md(
                f"**Gewonnen!** Für alle $n$ mit ${_N} \\le n \\le {CHECK_MAX:,}$ gilt "
                f"$|a_n - a| < \\varepsilon = {_eps}$. Jedes größere $N$ funktioniert dann auch."
            ),
            kind="success",
        )
    else:
        _n_bad = _N + int(_violations[0])
        _text = (
            f"**Noch nicht:** $a_{{{_n_bad}}} = {a_values[_n_bad - 1]:.6g}$ liegt außerhalb, "
            f"denn $|a_{{{_n_bad}}} - a| = {deviation[_n_bad - 1]:.4g} \\ge \\varepsilon$."
        )
        if _best_N is None:
            _text += (
                f" Im geprüften Bereich ($N \\le {CHECK_MAX // 2:,}$) gibt es **kein** passendes $N$. "
                "Ist $a$ vielleicht gar nicht der Grenzwert – oder konvergiert die Folge nur sehr langsam?"
            )
        else:
            _text += " Versuche ein größeres $N$."
        _feedback = mo.callout(mo.md(_text), kind="danger")

    if show_solution.value:
        if _best_N is None:
            _solution = mo.md(
                f"Für $\\varepsilon = {_eps}$ gibt es im geprüften Bereich "
                f"($N \\le {CHECK_MAX // 2:,}$) **kein** passendes $N$."
            )
        else:
            _solution = mo.md(
                f"Das kleinste passende $N$ für $\\varepsilon = {_eps}$ ist $N = {_best_N:,}$."
            )
    else:
        _solution = mo.md("")

    if _N > _n_show:
        _hint = mo.md(
            f"*Dein $N = {_N:,}$ liegt rechts vom angezeigten Bereich – "
            f"vergrößere „Anzeigen bis n“, um es zu sehen.*"
        )
    else:
        _hint = mo.md("")

    mo.vstack([
        mo.hstack([sequence_choice, limit_candidate], justify="start"),
        mo.md(f"$${selected['tex']}$$"),
        mo.hstack([epsilon, N_choice], justify="start"),
        mo.hstack([n_display, zoom_switch, show_solution], justify="start"),
        _fig,
        _hint,
        _feedback,
        _solution,
        mo.accordion({"Beweisidee: Wie findet man $N$ allgemein?": mo.md(selected["proof"])}),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Wie hängt $N$ von $\varepsilon$ ab?

    Für jedes $\varepsilon$ gibt es ein kleinstes passendes $N(\varepsilon)$. Der Graph zeigt diese
    Funktion (beide Achsen logarithmisch). Je kleiner $\varepsilon$, desto größer wird typischerweise $N$.

    **Konvergenz heißt:** $N(\varepsilon)$ darf beliebig groß werden, aber es muss für **jedes**
    $\varepsilon > 0$ **existieren**. Bricht die Kurve ab, gibt es ein $\varepsilon$, für das der
    Beweiser verliert – dann konvergiert die Folge nicht gegen $a$.
    """)
    return


@app.cell(hide_code=True)
def _(CHECK_MAX, epsilon, limit_candidate, mo, np, px, smallest_N):
    _eps_grid = np.logspace(-3, 0, 61)
    _N_of_eps = np.array(
        [np.nan if (_N := smallest_N(_e)) is None else _N for _e in _eps_grid], dtype=float
    )

    _fig = px.line(
        x=_eps_grid,
        y=_N_of_eps,
        markers=True,
        log_x=True,
        log_y=True,
        labels={"x": "ε", "y": "kleinstes N(ε)"},
    )
    _current_N = smallest_N(epsilon.value)
    if _current_N is not None:
        _fig.add_scatter(
            x=[epsilon.value],
            y=[_current_N],
            mode="markers",
            marker=dict(size=14, color="crimson"),
            name="aktuelles ε",
        )
    _fig.update_xaxes(autorange="reversed")
    _fig.update_layout(showlegend=False)

    _missing = _eps_grid[np.isnan(_N_of_eps)]
    if len(_missing) == 0:
        _verdict = mo.callout(
            mo.md(
                "Für **jedes** getestete $\\varepsilon$ gibt es ein passendes $N$. "
                "Das ist ein starkes Indiz für Konvergenz – ein Beweis ist es nicht (siehe Fragen unten)."
            ),
            kind="success",
        )
    else:
        _verdict = mo.callout(
            mo.md(
                f"Für $\\varepsilon \\le {_missing.max():.3g}$ wurde im geprüften Bereich "
                f"($N \\le {CHECK_MAX // 2:,}$) **kein** passendes $N$ gefunden. Entweder konvergiert "
                f"die Folge **nicht** gegen $a = {limit_candidate.value:g}$ – oder sie konvergiert so "
                f"langsam, dass $N$ noch größer sein müsste (wie bei $1/\\sqrt{{n}}$). "
                f"Welcher Fall vorliegt, kann nur ein **Beweis** klären."
            ),
            kind="warn",
        )

    mo.vstack([_fig, _verdict])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Verständnisfragen

    Probiere die Fragen zuerst selbst im Spiel oben aus und klappe dann die Antwort auf.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        r"1. Muss $N$ das kleinstmögliche sein?": mo.md(r"""
    Nein. Es genügt **irgendein** passendes $N$; jedes größere $N$ funktioniert dann auch.
    In Beweisen nimmt man deshalb oft ein bequemes, grob abgeschätztes $N$
    (siehe $\frac{\sin(n)}{n}$).
    """),
        r"2. Dürfen Folgenglieder außerhalb des $\varepsilon$-Schlauchs liegen?": mo.md(r"""
    Ja, aber nur **endlich viele** – nämlich höchstens $a_1, \dots, a_{N-1}$.
    Daraus folgt: Ändert man endlich viele Glieder einer Folge, ändert sich der Grenzwert nicht.
    """),
        r"3. Muss die Folge ihren Grenzwert erreichen oder sich monoton nähern?": mo.md(r"""
    Nein. $\frac{1}{n}$ wird nie gleich $0$, und $\frac{(-1)^n}{n}$ springt ständig über und
    unter den Grenzwert. Es kommt nur darauf an, dass die Abstände $|a_n - a|$ irgendwann
    dauerhaft kleiner als $\varepsilon$ sind.
    """),
        r"4. Wähle bei $\frac{1}{n}$ den falschen Kandidaten $a = 0.1$. Für welche $\varepsilon$ verliert der Beweiser?": mo.md(r"""
    Für jedes $\varepsilon < 0.1$. Die Folgenglieder kommen $0$ beliebig nahe, also ist
    $|a_n - 0.1|$ für große $n$ fast $0.1$ – ein Schlauch mit $\varepsilon < 0.1$ um $0.1$
    wird irgendwann für immer verlassen. (Bei $\varepsilon = 0.1$ ist der Schlauch $(0,\, 0.2)$,
    und $\frac{1}{n} > 0$ liegt ab $n = 6$ darin – die strikte Ungleichung $<$ zählt!) Für große $\varepsilon$ gewinnt der Beweiser zwar
    noch, aber die Definition verlangt **alle** $\varepsilon > 0$.
    """),
        r"5. Der Computer prüft bis $n = 1\,000\,000$. Ist das ein Beweis?": mo.md(r"""
    Nein. Die Definition verlangt $|a_n - a| < \varepsilon$ für **alle** $n \ge N$ – das sind
    unendlich viele. Der Computer kann immer nur endlich viele Glieder prüfen; dahinter könnte
    die Folge den Schlauch wieder verlassen. Ein Beweis braucht ein Argument, das für alle $n$
    gilt (siehe „Beweisidee“ im Spiel).
    """),
        r"6. Was passiert, wenn man die Quantoren vertauscht: $\exists N \; \forall \varepsilon > 0 \; \forall n \ge N: |a_n - a| < \varepsilon$?": mo.md(r"""
    Dann müsste **ein festes** $N$ für **alle** $\varepsilon$ funktionieren. Für $n \ge N$
    wäre dann $|a_n - a|$ kleiner als jede positive Zahl, also $a_n = a$. Diese Aussage
    beschreibt nur Folgen, die ab einem Index **konstant** gleich $a$ sind – z.B. nicht
    $\frac{1}{n}$. Die Reihenfolge der Quantoren macht den ganzen Unterschied!
    """),
        r"7. Wie lautet die Verneinung: Was heißt „$(a_n)$ konvergiert **nicht** gegen $a$“?": mo.md(r"""
    Man verneint, indem man jeden Quantor umdreht und die Ungleichung verneint:
    $$
    \exists \varepsilon > 0 \;\; \forall N \in \mathbb{N} \;\; \exists n \ge N: \quad |a_n - a| \ge \varepsilon .
    $$
    Im Spiel: Die Zweiflerin hat ein $\varepsilon$, bei dem **jedes** $N$ des Beweisers
    scheitert, weil danach immer wieder ein Glied außerhalb des Schlauchs liegt.
    Probiere es mit $(-1)^n$ und $\varepsilon = 1$ aus.
    """),
    })
    return


if __name__ == "__main__":
    app.run()
