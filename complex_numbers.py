import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from math import factorial


    return factorial, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Komplexe Zahlen in der Technik: Eulersche Formel und Fourier-Analyse

    Komplexe Zahlen wirken zuerst wie ein Rechentrick: Man führt eine Zahl $i$ mit $i^2 = -1$ ein,
    die es "gar nicht gibt". In der Technik sind sie trotzdem überall – in der Elektrotechnik,
    der Schwingungslehre, der Signalverarbeitung (Audio, Bild, Mobilfunk), der Regelungstechnik.
    Der Grund ist eine einzige Formel:

    $$
    e^{i\varphi} = \cos\varphi + i\,\sin\varphi .
    $$

    In diesem Notebook gehst du in vier Schritten vor:

    1. **Die Formel sehen:** $e^{i\varphi}$ ist ein Punkt, der auf dem Einheitskreis läuft.
    2. **Zeiger statt Sinuskurven:** Warum Ingenieure Schwingungen als rotierende Pfeile rechnen.
    3. **Fourier-Reihen:** Jedes periodische Signal ist eine Summe von Schwingungen – also von rotierenden Pfeilen.
    4. **Signale zerlegen:** Wie man aus einem Signal die enthaltenen Frequenzen zurückgewinnt.

    Du brauchst dafür nur Wissen aus der Analysis I (Funktionen, Taylor-Reihen, Integrale).
    Probiere die Regler aus und versuche, vorherzusagen, was passiert.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Die Eulersche Formel

    Eine komplexe Zahl $z = x + iy$ ist ein Punkt in der Ebene: $x$ ist der Realteil, $y$ der Imaginärteil.
    Die Zahl $e^{i\varphi}$ liegt für jedes reelle $\varphi$ auf dem **Einheitskreis**, und zwar beim Winkel $\varphi$
    (im Bogenmaß). Ihr Realteil ist $\cos\varphi$, ihr Imaginärteil $\sin\varphi$.

    Verschiebe den Regler und beobachte, wie die Projektionen des Punktes auf die beiden Achsen
    die Kurven von Kosinus und Sinus zeichnen.
    """)
    return


@app.cell(hide_code=True)
def _(mo, np):
    phi = mo.ui.slider(
        start=0,
        stop=2 * np.pi,
        step=0.01,
        value=1.0,
        label=r"Winkel $\varphi$ (Bogenmaß)",
        show_value=True,
        full_width=True,
    )
    return (phi,)


@app.cell(hide_code=True)
def _(mo, np, phi, plt):
    _p = phi.value
    _t = np.linspace(0, 2 * np.pi, 400)

    _fig, (_ax1, _ax2) = plt.subplots(
        1, 2, figsize=(11, 4.5), gridspec_kw=dict(width_ratios=[1, 1.5]), layout="constrained"
    )

    # Einheitskreis, Punkt und Projektionen
    _ax1.plot(np.cos(_t), np.sin(_t), color="lightgray")
    _ax1.plot([0, np.cos(_p)], [0, np.sin(_p)], "-o", color="black")
    _ax1.plot([np.cos(_p), np.cos(_p)], [0, np.sin(_p)], "--", color="crimson", label="Imaginärteil $\\sin\\varphi$")
    _ax1.plot([0, np.cos(_p)], [0, 0], color="royalblue", lw=4, label="Realteil $\\cos\\varphi$")
    _ax1.set(xlim=(-1.3, 1.3), ylim=(-1.3, 1.3), xlabel="Re", ylabel="Im", title="Einheitskreis in der komplexen Ebene")
    _ax1.set_aspect("equal")
    _ax1.grid(alpha=0.3)
    _ax1.legend(loc="lower center", fontsize=8)

    # Kosinus und Sinus
    _ax2.plot(_t, np.cos(_t), color="royalblue", label="$\\cos\\varphi$")
    _ax2.plot(_t, np.sin(_t), color="crimson", label="$\\sin\\varphi$")
    _ax2.plot([_p], [np.cos(_p)], "o", color="royalblue", ms=10)
    _ax2.plot([_p], [np.sin(_p)], "o", color="crimson", ms=10)
    _ax2.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi], ["0", "π/2", "π", "3π/2", "2π"])
    _ax2.set(xlabel="φ", xlim=(0, 2 * np.pi), ylim=(-1.3, 1.3), title="Kosinus und Sinus als Funktion von φ")
    _ax2.grid(alpha=0.3)
    _ax2.legend(loc="upper right")

    _out = mo.vstack(
        [
            phi,
            _fig,
            mo.md(
                rf"""
                $e^{{i\varphi}} = {np.cos(_p):.3f} + {np.sin(_p):.3f}\,i
                \quad\Longleftrightarrow\quad
                \cos\varphi = {np.cos(_p):.3f},\ \sin\varphi = {np.sin(_p):.3f}$
                """
            ),
        ]
    )
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Warum gilt die Formel? – Mit Taylor-Reihen

    Die Exponentialfunktion hat die Reihe $e^x = \sum_{k=0}^\infty \frac{x^k}{k!}$. Setzt man $x = i\varphi$ ein
    und nutzt, dass sich die Potenzen von $i$ im Viererzyklus wiederholen,

    $$
    i^0 = 1,\quad i^1 = i,\quad i^2 = -1,\quad i^3 = -i,\quad i^4 = 1,\ \dots
    $$

    dann trennen sich gerade und ungerade Terme von selbst:

    $$
    e^{i\varphi}= \underbrace{\left(1 - \frac{\varphi^2}{2!} + \frac{\varphi^4}{4!} - \dots\right)}_{\cos\varphi}+ i\,\underbrace{\left(\varphi - \frac{\varphi^3}{3!} + \frac{\varphi^5}{5!} - \dots\right)}_{\sin\varphi} .
    $$

    Unten siehst du die Teilsummen $S_n = \sum_{k=0}^n \frac{(i\varphi)^k}{k!}$ als Pfeilkette in der
    komplexen Ebene. Der Winkel $\varphi$ ist der Regler von oben. Wie viele Terme braucht man, bis die Kette den
    Punkt auf dem Einheitskreis (Stern) erreicht? Probiere große Winkel aus.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    n_taylor = mo.ui.slider(
        start=0,
        stop=15,
        step=1,
        value=3,
        label="Anzahl Terme $n$",
        show_value=True,
        full_width=True,
    )
    return (n_taylor,)


@app.cell(hide_code=True)
def _(factorial, mo, n_taylor, np, phi, plt):
    _p = phi.value
    _n = n_taylor.value
    _terms = np.array([(1j * _p) ** k / factorial(k) for k in range(_n + 1)])
    _partial = np.cumsum(_terms)
    _path = np.concatenate([[0], _partial])  # Start im Ursprung
    _target = np.exp(1j * _p)
    _t = np.linspace(0, 2 * np.pi, 400)
    _lim = 3  # feste Achsen, damit das Bild beim Verschieben nicht springt

    _fig, _ax = plt.subplots(figsize=(6, 6), layout="constrained")
    _ax.plot(np.cos(_t), np.sin(_t), color="lightgray")
    _ax.plot(_path.real, _path.imag, "-o", color="darkorange", label=r"Teilsummen $S_0, S_1, \dots$")
    _ax.plot([_target.real], [_target.imag], "*", color="black", ms=16, label=r"$e^{i\varphi}$")
    _ax.plot([_partial[-1].real], [_partial[-1].imag], "o", color="crimson", ms=10, label=f"$S_{{{_n}}}$")
    _ax.set(xlim=(-_lim, _lim), ylim=(-_lim, _lim), xlabel="Re", ylabel="Im")
    _ax.set_aspect("equal")
    _ax.grid(alpha=0.3)
    _ax.legend(loc="upper right")

    _out = mo.vstack(
        [
            n_taylor,
            _fig,
            mo.md(
                rf"Abstand zum Ziel: $|S_{{{_n}}} - e^{{i\varphi}}| = {abs(_partial[-1] - _target):.2e}$"
                + (("  \n*Hinweis: Ein Teil der Pfeilkette liegt außerhalb des Bildausschnitts.*") if np.max(np.abs(_path)) > _lim else "")
            ),
        ]
    )
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Zeiger statt Sinuskurven

    Eine Wechselspannung (Steckdose, Audiosignal, Schwingung einer Brücke) ist eine Sinusschwingung
    $u(t) = A\cos(\omega t + \theta)$ mit Amplitude $A$, Kreisfrequenz $\omega$ und Phase $\theta$.
    Mit der Eulerschen Formel ist das der Realteil eines **rotierenden Pfeils**:

    $$
    A\cos(\omega t + \theta) = \operatorname{Re}\!\left( \underbrace{A e^{i\theta}}_{\text{Zeiger } z}\; e^{i\omega t} \right) .
    $$

    Die Zahl $z = A e^{i\theta}$ trägt Amplitude und Phase. Der Faktor $e^{i\omega t}$ sorgt nur für die Drehung –
    für alle Schwingungen mit gleichem $\omega$ ist er derselbe. Das hat eine praktische Folge:

    > **Zwei Schwingungen gleicher Frequenz zu addieren heißt, zwei Pfeile zu addieren.**

    Ohne komplexe Zahlen müsste man Additionstheoreme für Sinus und Kosinus verwenden.
    Hier genügt $z = z_1 + z_2$. Wähle unten zwei Schwingungen (mit $\omega = 1$) und lasse die Zeit laufen.
    """)
    return


@app.cell(hide_code=True)
def _(mo, np):
    amp1 = mo.ui.slider(0, 2, step=0.1, value=1.0, label="Amplitude $A_1$", show_value=True)
    amp2 = mo.ui.slider(0, 2, step=0.1, value=1.0, label="Amplitude $A_2$", show_value=True)
    theta2 = mo.ui.slider(
        0, 2 * np.pi, step=0.05, value=1.5, label=r"Phase $\theta_2$ (die erste hat $\theta_1 = 0$)", show_value=True
    )
    time_t = mo.ui.slider(0, 2 * np.pi, step=0.05, value=0.0, label="Zeit $t$", show_value=True, full_width=True)
    return amp1, amp2, theta2, time_t


@app.function
def add_arrow(ax, start, end, color, width=2):
    """Zeichnet einen Pfeil von start nach end (komplexe Zahlen) in die Achse ax."""
    ax.annotate(
        "",
        xy=(end.real, end.imag),
        xytext=(start.real, start.imag),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=width, shrinkA=0, shrinkB=0),
    )


@app.cell(hide_code=True)
def _(amp1, amp2, mo, np, plt, theta2, time_t):
    _z1 = amp1.value
    _z2 = amp2.value * np.exp(1j * theta2.value)
    _t0 = time_t.value
    _rot = np.exp(1j * _t0)
    _x = np.linspace(0, 4 * np.pi, 600)
    _s1 = (_z1 * np.exp(1j * _x)).real
    _s2 = (_z2 * np.exp(1j * _x)).real
    _total = _s1 + _s2
    _lim = 4.3  # feste Achsen: max. Amplituden 2 + 2, plus Rand

    _fig, (_ax1, _ax2) = plt.subplots(
        1, 2, figsize=(11, 4.5), gridspec_kw=dict(width_ratios=[1, 1.5]), layout="constrained"
    )

    # Zeiger in der komplexen Ebene
    add_arrow(_ax1, 0j, _z1 * _rot, "royalblue")
    add_arrow(_ax1, _z1 * _rot, (_z1 + _z2) * _rot, "crimson")
    add_arrow(_ax1, 0j, (_z1 + _z2) * _rot, "black", width=3)
    _ax1.plot([], [], color="royalblue", label="Schwingung 1")
    _ax1.plot([], [], color="crimson", label="Schwingung 2")
    _ax1.plot([], [], color="black", label="Summe")
    _ax1.set(xlim=(-_lim, _lim), ylim=(-_lim, _lim), xlabel="Re", ylabel="Im", title="Zeiger in der komplexen Ebene")
    _ax1.set_aspect("equal")
    _ax1.grid(alpha=0.3)
    _ax1.legend(loc="lower center", fontsize=8, ncols=3)

    # Zeitverlauf
    _ax2.plot(_x, _s1, color="royalblue")
    _ax2.plot(_x, _s2, color="crimson")
    _ax2.plot(_x, _total, color="black", lw=2.5)
    _ax2.axvline(_t0, color="gray", ls=":")
    _ax2.set(xlabel="t", xlim=(0, 4 * np.pi), ylim=(-_lim, _lim), title="Zeitverlauf (Realteil der Zeiger)")
    _ax2.grid(alpha=0.3)

    _amp_sum = abs(_z1 + _z2)
    _out = mo.vstack(
        [
            mo.hstack([mo.vstack([amp1, amp2, theta2]), time_t], widths=[1, 1], align="center"),
            _fig,
            mo.md(
                rf"""
                Amplitude der Summe: $|z_1 + z_2| = {_amp_sum:.3f}$ –
                das ist die Höhe der schwarzen Kurve. Sind beide Schwingungen in Phase ($\theta_2 = 0$),
                addieren sich die Amplituden. Bei $\theta_2 = \pi$ (Gegenphase) löschen sie sich aus,
                wenn $A_1 = A_2$ gilt – das Prinzip hinter Noise-Cancelling-Kopfhörern.
                """
            ),
        ]
    )
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Fourier-Reihen: Jedes Signal ist eine Summe rotierender Pfeile

    Bisher hatten wir reine Sinusschwingungen. Echte Signale – ein Rechtecksignal in einer Digitalschaltung, der Klang
    einer Geige, ein Herzschlag im EKG – sind es nicht. Der Mathematiker Fourier hatte aber eine erstaunliche Idee:

    > **Jedes periodische Signal lässt sich als Summe von Sinusschwingungen mit den Frequenzen
    > $1, 2, 3, \dots$ schreiben.**

    Für eine $2\pi$-periodische Funktion $f$ lautet das

    $$
    f(x) \approx \sum_{k=1}^{n} b_k \sin(kx) ,
    $$

    wobei die Zahlen $b_k$ bestimmen, wie stark die $k$-te Schwingung vertreten ist. (Die Signale unten sind
    ungerade Funktionen, deshalb genügen Sinus-Terme.) Mit der Eulerschen Formel ist jeder Summand
    $b_k \sin(kx) = \operatorname{Im}\!\big(b_k e^{ikx}\big)$ die Höhe eines Pfeils der Länge $|b_k|$, der mit Geschwindigkeit $k$
    rotiert. Das ganze Signal ist also die Höhe der Spitze einer **Kette rotierender Pfeile**.

    Wähle eine Signalform und erhöhe die Zahl der Terme. Verschiebe $x$, um die Pfeile laufen zu sehen.
    """)
    return


@app.cell(hide_code=True)
def _(mo, np):
    wave = mo.ui.dropdown(
        options=["Rechteck", "Sägezahn", "Dreieck"], value="Rechteck", label="Signalform"
    )
    n_terms = mo.ui.slider(1, 30, step=1, value=3, label="Anzahl Terme $n$", show_value=True, full_width=True)
    x_pos = mo.ui.slider(-np.pi, np.pi, step=0.02, value=0.5, label="Position $x$", show_value=True, full_width=True)
    return n_terms, wave, x_pos


@app.cell
def _(np):
    def target(wave, x):
        """Das exakte Signal (2π-periodisch)."""
        if wave == "Rechteck":
            return np.sign(np.sin(x))
        if wave == "Sägezahn":
            return (x + np.pi) % (2 * np.pi) - np.pi
        return 2 / np.pi * np.arcsin(np.sin(x))  # Dreieck

    def fourier_terms(wave, n):
        """Die ersten n von null verschiedenen Koeffizienten (k, b_k) von f(x) = Σ b_k sin(kx)."""
        terms = []
        k = 0
        while len(terms) < n:
            k += 1
            if wave == "Rechteck" and k % 2 == 1:
                terms.append((k, 4 / (np.pi * k)))
            elif wave == "Sägezahn":
                terms.append((k, 2 * (-1) ** (k + 1) / k))
            elif wave == "Dreieck" and k % 2 == 1:
                terms.append((k, 8 / (np.pi**2 * k**2) * (-1) ** ((k - 1) // 2)))
        return terms

    return fourier_terms, target


@app.cell(hide_code=True)
def _(fourier_terms, mo, n_terms, np, plt, target, wave, x_pos):
    _terms = fourier_terms(wave.value, n_terms.value)
    _x0 = x_pos.value
    _xs = np.linspace(-np.pi, np.pi, 800)
    _approx = sum(b * np.sin(k * _xs) for k, b in _terms)
    _approx_at_x0 = sum(b * np.sin(k * _x0) for k, b in _terms)

    # Pfeilkette: der k-te Pfeil ist b_k * exp(i k x0)
    _arrows = [b * np.exp(1j * k * _x0) for k, b in _terms]
    _centers = np.concatenate([[0j], np.cumsum(_arrows)])
    # Feste Achsen pro Signalform (unabhängig von n und x): größte Reichweite der Kette mit 30 Termen
    _full = np.array(fourier_terms(wave.value, 30))
    _grid = np.linspace(-np.pi, np.pi, 200)
    _chains = np.cumsum(_full[:, 1] * np.exp(1j * np.outer(_grid, _full[:, 0])), axis=1)
    _lim = min(max(1.1 * float(np.max(np.abs(_chains))), 1.3), 4.0)  # beim Sägezahn bewusst gekappt (Sprungstelle)
    _ylim = 1.25 * float(np.max(np.abs(target(wave.value, _xs))))

    _fig, (_ax1, _ax2) = plt.subplots(
        1, 2, figsize=(11, 4.8), gridspec_kw=dict(width_ratios=[1, 1.5]), layout="constrained"
    )

    _c = np.linspace(0, 2 * np.pi, 100)
    for _i, (_k, _b) in enumerate(_terms):
        # Kreis, den die Spitze dieses Pfeils beim Drehen durchläuft
        _circ = _centers[_i] + abs(_b) * np.exp(1j * _c)
        _ax1.plot(_circ.real, _circ.imag, color="lightgray", lw=1)
        add_arrow(_ax1, _centers[_i], _centers[_i + 1], "royalblue" if _i % 2 == 0 else "crimson")
    # Höhe der Spitze = Funktionswert der Näherung
    _ax1.plot([_centers[-1].real], [_centers[-1].imag], "o", color="black")
    _ax1.axhline(_approx_at_x0, color="black", ls=":")
    _ax1.set(xlim=(-_lim, _lim), ylim=(-_lim, _lim), xlabel="Re", ylabel="Im", title="Pfeilkette zur Position x")
    _ax1.set_aspect("equal")
    _ax1.grid(alpha=0.3)

    _ax2.plot(_xs, target(wave.value, _xs), color="lightgray", lw=4, label="exaktes Signal")
    _ax2.plot(_xs, _approx, color="black", label=f"Summe der ersten {n_terms.value} Terme")
    _ax2.plot([_x0], [_approx_at_x0], "o", color="black", ms=9)
    _ax2.set_xticks([-np.pi, 0, np.pi], ["-π", "0", "π"])
    _ax2.set(xlabel="x", xlim=(-np.pi, np.pi), ylim=(-_ylim, _ylim), title="Signal und Näherung")
    _ax2.grid(alpha=0.3)
    _ax2.legend(loc="upper left")

    _formel = {
        "Rechteck": r"\frac{4}{\pi}\left(\sin x + \frac{\sin 3x}{3} + \frac{\sin 5x}{5} + \dots\right)",
        "Sägezahn": r"2\left(\sin x - \frac{\sin 2x}{2} + \frac{\sin 3x}{3} - \dots\right)",
        "Dreieck": r"\frac{8}{\pi^2}\left(\sin x - \frac{\sin 3x}{9} + \frac{\sin 5x}{25} - \dots\right)",
    }[wave.value]

    _out = mo.vstack(
        [
            mo.hstack([wave, n_terms], widths=[1, 2], align="center"),
            x_pos,
            _fig,
            mo.md(rf"Reihe: $f(x) = {_formel}$"),
        ]
    )
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Was fällt auf?**

    - Schon wenige Pfeile liefern eine brauchbare Näherung, jeder weitere Pfeil ist kleiner und dreht schneller.
    - Beim **Dreieck** sind die Koeffizienten wie $1/k^2$ – die Reihe konvergiert sehr schnell, weil das Signal keine Sprünge hat.
    - Beim **Rechteck** und **Sägezahn** fallen sie nur wie $1/k$. An der Sprungstelle bleibt ein Überschwinger von etwa 9 %
      des Sprungs, egal wie viele Terme man nimmt (*Gibbssches Phänomen*). Scharfe Kanten brauchen hohe Frequenzen.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Signale zerlegen: Welche Frequenzen stecken drin?

    In der Praxis geht man meistens den umgekehrten Weg: Man misst ein Signal (Mikrofon, Beschleunigungssensor,
    Funkempfänger) und will wissen, **welche Frequenzen es enthält**. Die Antwort liefert ein Integral.

    Ist $f(x) = \sum_k b_k \sin(kx)$ auf $[-\pi, \pi]$, dann gilt

    $$
    b_k = \frac{1}{\pi} \int_{-\pi}^{\pi} f(x)\,\sin(kx)\,dx .
    $$

    Der Grund: $\int_{-\pi}^{\pi} \sin(kx)\sin(mx)\,dx = 0$ für $k \ne m$ und $= \pi$ für $k = m$ (nachrechenbar mit
    den Additionstheoremen). Multipliziert man $f$ mit $\sin(kx)$ und integriert, "überlebt" nur der Term mit
    der passenden Frequenz. Das Integral misst also, wie gut $f$ zur $k$-ten Schwingung passt.

    Unten mischst du selbst ein Signal aus sechs Schwingungen und fügst Rauschen hinzu. Das Integral
    (numerisch berechnet) findet die Mischung wieder, und zwar das **Spektrum** als Balkendiagramm.
    Die Rauten zeigen die Amplituden, die du eingestellt hast.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mix = mo.ui.array(
        [
            mo.ui.slider(0, 2, step=0.1, value=v, label=f"$k={k}$", show_value=True)
            for k, v in zip(range(1, 7), [1.0, 0.0, 0.5, 0.0, 0.3, 0.0])
        ],
        label="Amplituden der Schwingungen",
    )
    noise = mo.ui.slider(0, 2, step=0.1, value=0.0, label="Rauschen", show_value=True)
    return mix, noise


@app.cell(hide_code=True)
def _(mix, mo, noise, np, plt):
    _x = np.linspace(-np.pi, np.pi, 2000)
    _a = np.array(mix.value)
    _rng = np.random.default_rng(42)  # festes Rauschen, damit nur der Regler etwas ändert
    _f = sum(_a[k - 1] * np.sin(k * _x) for k in range(1, 7)) + noise.value * _rng.normal(size=_x.size)

    _ks = np.arange(1, 13)
    _b = np.array([np.trapezoid(_f * np.sin(k * _x), _x) / np.pi for k in _ks])

    _fig, (_ax1, _ax2) = plt.subplots(
        1, 2, figsize=(11, 4.2), gridspec_kw=dict(width_ratios=[1.2, 1]), layout="constrained"
    )
    _ax1.plot(_x, _f, color="black", lw=1)
    _ax1.set_xticks([-np.pi, 0, np.pi], ["-π", "0", "π"])
    _ax1.set(xlabel="x", xlim=(-np.pi, np.pi), ylim=(-5, 5), title="Signal $f(x)$")
    _ax1.grid(alpha=0.3)

    _ax2.bar(_ks, _b, color="royalblue", label="berechnet")
    _ax2.plot(range(1, 7), _a, "D", color="crimson", ms=8, label="eingestellt")
    _ax2.set_xticks(_ks)
    _ax2.set(xlabel="Frequenz $k$", ylim=(-0.5, 2.2), title="Spektrum $b_k$")
    _ax2.grid(alpha=0.3)
    _ax2.legend(loc="upper right")

    _out = mo.vstack([mo.hstack([mix, noise], widths=[1, 1], align="center"), _fig])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Zusammenfassung

    - $e^{i\varphi} = \cos\varphi + i\sin\varphi$: Die komplexe Exponentialfunktion beschreibt eine **Drehung**.
    - Schwingungen gleicher Frequenz addiert man als **Zeiger** (komplexe Zahlen); Amplitude und Phase stecken in $z = Ae^{i\theta}$.
    - Jedes periodische Signal ist eine Summe von Schwingungen (**Fourier-Reihe**), und ihre Anteile berechnet man mit **Integralen**.
    - Die Zerlegung eines Signals in seine Frequenzen ist die Grundlage von MP3, JPEG, Mobilfunk, Radar, Schwingungsanalyse
      und vielem mehr.

    **Ausblick:** In der Literatur schreibt man die Reihe meist komplex, ohne Sinus und Kosinus getrennt:

    $$
    f(x) = \sum_{k=-\infty}^{\infty} c_k\, e^{ikx}, \qquad c_k = \frac{1}{2\pi}\int_{-\pi}^{\pi} f(x)\,e^{-ikx}\,dx .
    $$

    Das ist dieselbe Idee wie hier, nur kompakter: Jeder Summand ist ein rotierender Pfeil, und das Integral
    liest Länge und Startwinkel dieses Pfeils aus dem Signal ab. Wer sich dafür interessiert, findet das im
    Wahlfach zur Fourier-Analyse und Signalverarbeitung, und die schnelle Variante dieser Rechnung heißt *FFT*.
    """)
    return


if __name__ == "__main__":
    app.run()
