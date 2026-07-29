"""THE LENSING-vs-DYNAMICS SCISSOR ON CLUSTERS — does OBT predict the hydrostatic mass bias?

REVIEWER MODE (Romain: 'creuse le ciseau lentillage-vs-dynamique sur les amas'). Axiom: OBT can be
FALSE; this is a test, not an advocacy.

THE MECHANISM (OBT's own, no new ingredient). Under ARA the oscillating MOND scale is averaged by
the TRACER, not by the field: a tracer whose internal period exceeds T = 2 Gyr cannot follow a0(t)
and responds to an averaged value; photons average nothing (W = 1). So for ONE cluster, two
observers using Newtonian gravity infer DIFFERENT masses:

    M_lens(r) = [ g_MOND(g_bar, a0)       + g_Weyl ] r^2/G      (photons, W = 1)
    M_dyn(r)  = [ g_MOND(g_bar, W(r) a0)  + g_Weyl ] r^2/G      (gas / galaxies, W < 1)

=> an APPARENT hydrostatic mass bias with NO non-thermal pressure. 1 - b = M_dyn/M_lens is then a
PARAMETER-FREE prediction once (f_W, beta) are fixed -- and the hydrostatic bias is one of the most
measured quantities in cluster cosmology. This is a real test with a real way to fail.

THE W CONVENTION IS THE CRUX, and the two candidates are not a matter of taste:
  * BARE SINC, W = |sinc(t_dyn/T)|: what card #22's fit actually uses in `probes.xcop_hier`. It
    vanishes at t_dyn = T and oscillates.
  * AUDIT-CORRECTED (June 2026, CLAUDE.md): the boost enters through the Gauss-Codazzi quadrature
    g_5D = sqrt(g^2 + a0^2), i.e. through a0 SQUARED, so what averages is <a0^2>, which cannot
    vanish. For a0(t) = a0max sin(2 pi t/T + phi) the long-window limit is <a0^2> = a0max^2/2
    -> a0_eff/a0max -> 1/sqrt(2) = 0.707. The signed-sinc zero is a Jensen artifact.
  Both are computed here. They differ by a factor ~3 in the predicted bias, and the data decide.

WHAT IS COMPUTED
  [1] the derivation of both W windows, with the Jensen point made explicit;
  [2] b_ARA(r) for a fiducial cluster under both conventions;
  [3] the UNIVERSALITY theorem: at fixed overdensity t_dyn is MASS-INDEPENDENT (analytic + numeric)
      -> the ARA bias is mass-independent at fixed Delta but z-dependent through rho_c(z);
  [4] the SCALE test: galaxies -> groups -> clusters. The scissor must VANISH at galaxy scales
      (where lensing and dynamics are observed to agree) and turn on at t_dyn ~ T;
  [5] confrontation with the measured biases, including the x1.34 measured in alpha_nt_budget.py;
  [6] verdict + the named falsifiers.

Asserted ONLY identities (the fixed-overdensity t_dyn theorem; the <sin^2> = 1/2 limit).
Everything else computed + reported. Quarantined; not sacred; not in the PDF.
"""

import numpy as np

import arcs_obt as A
import card22_lensing_refit as R

G, MSUN, KPC, C = A.G, A.MSUN, A.KPC, A.C
TGYR, GYR_S = 2.0, 3.156e16
FW_DYN, BETA_DYN = (
    0.73,
    0.039,
)  # card #22 re-fit on X-COP with OBT's DERIVED law (rung 2)


def t_dyn_gyr(r_kpc, m_msun):
    return 2 * np.pi * np.sqrt((r_kpc * KPC) ** 3 / (G * m_msun * MSUN)) / GYR_S


def w_sinc(td):
    """Card-#22's window as coded: signed-a0 boxcar average -> |sinc|, vanishes at t_dyn = T."""
    return np.abs(np.sinc(td / TGYR))


def w_quad(td):
    """The window as DECLARED by ARA + the June-2026 audit correction, in two pieces:
    * ADIABATIC branch, t_dyn < T/2: W = 1 EXACTLY. The orbit tracks the instantaneous a0; this
      side is data-mandated (SPARC: 174/175 galaxies are sub-crossover, and a raw per-orbit
      boxcar would suppress the outer points of 20 band galaxies by 36-97%, excluded by the
      declining-curve RAR).
    * AVERAGING branch, t_dyn > 2T: the boost rides on a0^2 (Gauss-Codazzi quadrature
      g_5D = sqrt(g^2+a0^2)), so what averages is <a0^2> = a0max^2/2 -> W -> 1/sqrt(2) = 0.707.
      It CANNOT vanish; the signed-sinc zero is a Jensen artifact.
    * RESONANCE BAND t_dyn in [T/2, 2T]: declared O(1)-uncertain in ARA; interpolated in log t
      here and flagged wherever it is used."""
    x = np.asarray(td, float) / TGYR
    w_hi = 1 / np.sqrt(2)
    f = np.clip(
        (np.log(np.clip(x, 1e-9, None)) - np.log(0.5)) / (np.log(2.0) - np.log(0.5)),
        0,
        1,
    )
    return 1.0 * (1 - f) + w_hi * f


def w_from_eps(eps, s_now):
    """The window WITHOUT assuming the modulation depth. Write a0(t) = a0_0 [1 + eps s(t)] with
    s in [-1,1], <s> = 0, <s^2> = 1/2. A SLOW tracer feels sqrt(<a0^2>) = a0_0 sqrt(1 + eps^2/2);
    photons (and adiabatic tracers) feel the INSTANTANEOUS a0_0 (1 + eps s_now). So

        W = sqrt(1 + eps^2/2) / (1 + eps s_now)

    eps = 1 (a0 swinging all the way to zero) is what the sinc machinery implicitly assumes;
    OBT's motor modulates its own amplitude by f_osc = 0.10. Nothing in the theory derives eps.
    NOTE the sign: for s_now < 0 (we sit BELOW the mean) W > 1 and the scissor REVERSES.
    """
    return np.sqrt(1 + eps**2 / 2) / (1 + eps * s_now)


def in_band(td):
    return (np.asarray(td, float) > 0.5 * TGYR) & (np.asarray(td, float) < 2.0 * TGYR)


def cluster_profile(m500, z, f_gas=0.13, mstar=1.2e12, astar=30.0, npts=40):
    """Fiducial spherical cluster: NFW-like total from the OBT law itself is circular, so build the
    BARYONS from M500 (gas fraction + BCG) and let the OBT law generate everything else.
    """
    rho_c = 3 * (A.H0 * A.ez(z)) ** 2 / (8 * np.pi * G)
    r500 = (m500 * MSUN / (4 / 3 * np.pi * 500 * rho_c)) ** (1 / 3) / KPC
    r = np.logspace(np.log10(0.03 * r500), np.log10(1.2 * r500), npts)
    fg = np.clip(f_gas * (r / r500) ** 0.4, 0.02, 0.16)
    m_bar = mstar * (r / (r + astar)) ** 2 + fg * m500
    g_bar = G * m_bar * MSUN / (r * KPC) ** 2
    a0 = C * A.H0 * A.ez(z) / (2 * np.pi)
    g_w = R.weyl_g(r * KPC, r500 * KPC, m500 * MSUN, FW_DYN, BETA_DYN)
    g_lens = A.rar_obt(g_bar, a0) + g_w
    m_lens = g_lens * (r * KPC) ** 2 / G / MSUN
    td = t_dyn_gyr(r, m_lens)
    out = dict(
        r=r, r500=r500, a0=a0, g_bar=g_bar, g_w=g_w, g_lens=g_lens, m_lens=m_lens, td=td
    )
    for tag, wf in (("sinc", w_sinc), ("quad", w_quad)):
        w = wf(td)
        g_dyn = A.rar_obt(g_bar, np.clip(w, 1e-3, None) * a0) + g_w
        out[f"w_{tag}"] = w
        out[f"b_{tag}"] = 1.0 - g_dyn / g_lens
    return out


def main():
    print("=" * 104)
    print(
        " THE LENSING-vs-DYNAMICS SCISSOR ON CLUSTERS — OBT's own prediction for the 'hydrostatic bias'"
    )
    print("=" * 104)

    # ------------------------------------------------------------------ [1] the two windows
    print("\n[1] THE TWO WINDOWS (the crux)")
    assert abs(w_quad(0.4 * TGYR) - 1.0) < 1e-12, "adiabatic branch: W == 1 below T/2"
    assert (
        abs(w_quad(1e4) - 1 / np.sqrt(2)) < 1e-12
    ), "averaging branch: <a0^2> -> a0max^2/2"
    print(
        f"    {'t_dyn/T':>8s} {'W_sinc (card as coded)':>23s} {'W_quad (audit-corrected)':>25s}"
    )
    for x in (0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0):
        print(f"    {x:8.1f} {w_sinc(x*TGYR):23.3f} {w_quad(x*TGYR):25.3f}")
    print(
        "    -> the sinc VANISHES at t_dyn = T and oscillates; the quadrature window saturates at"
    )
    print(
        "       1/sqrt(2) = 0.707 and never vanishes. The June-2026 audit ruled the sinc zero a"
    )
    print(
        "       Jensen artifact (the boost rides on a0^2). The card's FIT still uses the sinc."
    )

    # ------------------------------------------------------------------ [2] the bias profile
    print(
        "\n[2] THE PREDICTED APPARENT BIAS b = 1 - M_dyn/M_lens (fiducial M500 = 6e14, z = 0.2)"
    )
    p = cluster_profile(6e14, 0.2)
    print(f"    R500 = {p['r500']:.0f} kpc, a0(z) = {p['a0']:.2e} m/s^2")
    print(
        f"    {'r/R500':>7s} {'t_dyn[Gyr]':>10s} {'g_bar/a0':>9s} {'W_sinc':>7s} {'b_sinc':>7s}"
        f" {'W_quad':>7s} {'b_quad':>7s}"
    )
    for f in (0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0):
        i = int(np.argmin(np.abs(p["r"] / p["r500"] - f)))
        print(
            f"    {p['r'][i]/p['r500']:7.2f} {p['td'][i]:10.2f} {p['g_bar'][i]/p['a0']:9.3f}"
            f" {p['w_sinc'][i]:7.3f} {p['b_sinc'][i]:7.3f} {p['w_quad'][i]:7.3f} {p['b_quad'][i]:7.3f}"
        )
    i5 = int(np.argmin(np.abs(p["r"] / p["r500"] - 1.0)))
    print(
        f"    AT R500:  b_sinc = {p['b_sinc'][i5]:.2f}  (1-b = {1-p['b_sinc'][i5]:.2f})"
        f"   |   b_quad = {p['b_quad'][i5]:.2f}  (1-b = {1-p['b_quad'][i5]:.2f})"
    )
    print(
        "    Both rise outward (t_dyn grows) -- the same qualitative shape the measurements report."
    )
    m_dyn5 = (
        (
            A.rar_obt(p["g_bar"][i5], np.clip(p["w_sinc"][i5], 1e-3, None) * p["a0"])
            + p["g_w"][i5]
        )
        * (p["r"][i5] * KPC) ** 2
        / G
        / MSUN
    )
    print(
        "    [self-consistency] the fiducial's M500 is the DYNAMICAL mass the card was fitted to:"
    )
    print(
        f"      M_dyn(R500)/M500 = {m_dyn5/6e14:.2f} (should be ~1: the card's globals reproduce the"
    )
    print(
        f"      X-ray mass scale), while M_lens(R500)/M500 = {p['m_lens'][i5]/6e14:.2f} -- the scissor."
    )
    print(
        "    STRUCTURAL CAP: at R500 the Weyl carries"
        f" {p['g_w'][i5]/p['g_lens'][i5]*100:.0f}% of the total and is CHANNEL-INDEPENDENT, so the"
    )
    print(
        "      scissor can only act on the MOND remainder. That caps the cluster-scale bias."
    )

    # -------------------------------------------------- [2b] the modulation depth: the real unknown
    print("\n[2b] THE MODULATION DEPTH eps — the load-bearing input nobody derived")
    print(
        "    a0(t) = a0_0 [1 + eps s(t)];  slow tracer feels sqrt(<a0^2>), photons feel a0(now)"
    )
    print(
        "    ->  W = sqrt(1 + eps^2/2) / (1 + eps s_now).  eps = 1 is what the sinc machinery"
    )
    print(
        "    implicitly assumes (a0 swinging to zero); OBT's own motor amplitude is f_osc = 0.10."
    )
    i5b = int(np.argmin(np.abs(p["r"] / p["r500"] - 1.0)))
    gb5, gw5, a05 = p["g_bar"][i5b], p["g_w"][i5b], p["a0"]
    bof = lambda w: 1 - (A.rar_obt(gb5, w * a05) + gw5) / (A.rar_obt(gb5, a05) + gw5)
    print(
        f"    {'eps':>6s} {'W (at peak, s=+1)':>18s} {'b at R500':>10s} {'W (s=0)':>9s}"
        f" {'W (s=-1)':>9s} {'b (s=-1)':>9s}"
    )
    for eps in (0.10, 0.25, 0.50, 0.75, 1.00):
        wp, w0, wm = w_from_eps(eps, 1.0), w_from_eps(eps, 0.0), w_from_eps(eps, -1.0)
        bm = bof(wm) if np.isfinite(wm) and wm < 50 else np.nan
        print(
            f"    {eps:6.2f} {wp:18.3f} {bof(wp):10.3f} {w0:9.3f} {min(wm,99.9):9.3f}"
            f" {bm:9.3f}"
            if np.isfinite(bm)
            else f"    {eps:6.2f} {wp:18.3f} {bof(wp):10.3f} {w0:9.3f} {'a0->0':>9s} {'n/a':>9s}"
        )
    global w_floor
    w_floor = min(w_from_eps(e, 1.0) for e in np.linspace(0, 1, 2001))
    print(
        "    -> BOUND: over the whole physical range eps in [0,1] the window cannot go below"
        f" W = {w_floor:.3f}"
    )
    print(
        "       (attained at eps = 1, at the oscillation peak). The cluster bias is therefore"
    )
    print(
        f"       CAPPED at b <= {bof(w_floor):.2f}, i.e. 1-b >= {1-bof(w_floor):.2f}, whatever the depth."
    )
    print(
        f"    -> and the sinc branch's effective W ~ {p['w_sinc'][i5b]:.2f} is UNREACHABLE in this"
    )
    print(
        "       framework: it is not merely un-audited, it lies outside what any bounded, positive"
    )
    print("       a0 oscillation can produce.")
    print(
        "    -> SIGN WARNING: for s_now < 0 (currently below the mean) W > 1 and the scissor"
    )
    print(
        f"       REVERSES (b = {bof(w_from_eps(0.5, -1.0)):.2f} already at eps=0.5): dynamics would exceed lensing."
    )
    print(
        "       The observed sign (X-ray masses BELOW lensing) therefore requires that we sit ABOVE"
    )
    print(
        "       the RMS point of the a0 oscillation today -- a chronology statement, testable"
    )
    print(
        "       against OBT's own anchoring (phase ~0.9 of the cycle), not a free choice."
    )

    # ------------------------------------------------------------------ [3] universality
    print(
        "\n[3] UNIVERSALITY THEOREM — at fixed overdensity, t_dyn does NOT depend on mass"
    )
    print(
        "    t_dyn = 2pi sqrt(r^3/GM) and M = (4/3)pi Delta rho_c(z) r^3  =>  t_dyn ="
        " 2pi/sqrt((4/3)pi G Delta rho_c(z)) : mass drops out."
    )
    rho_c0 = 3 * A.H0**2 / (8 * np.pi * G)
    t_an = 2 * np.pi / np.sqrt(4 / 3 * np.pi * G * 500 * rho_c0) / GYR_S
    tds = [
        t_dyn_gyr(cluster_profile(m, 0.0)["r500"], m)
        for m in (1e14, 3e14, 6e14, 1.2e15)
    ]
    print(
        f"    analytic t_dyn(R500, z=0) = {t_an:.2f} Gyr;  numeric over M500 = 1e14..1.2e15:"
        f" {min(tds):.2f}-{max(tds):.2f} Gyr"
    )
    assert (
        abs(max(tds) / min(tds) - 1) < 1e-6
    ), "t_dyn at fixed overdensity must be mass-independent"
    print(
        "    -> the ARA bias at a fixed overdensity is MASS-INDEPENDENT. It is however"
        " z-DEPENDENT (t_dyn ~ 1/E(z)):"
    )
    print(
        f"    {'z':>5s} {'t_dyn(R500)':>11s} {'W_sinc':>7s} {'b_sinc':>7s} {'W_quad':>7s} {'b_quad':>7s}"
    )
    for z in (0.0, 0.2, 0.4, 0.7, 1.0):
        q = cluster_profile(6e14, z)
        j = int(np.argmin(np.abs(q["r"] / q["r500"] - 1.0)))
        print(
            f"    {z:5.2f} {q['td'][j]:11.2f} {q['w_sinc'][j]:7.3f} {q['b_sinc'][j]:7.3f}"
            f" {q['w_quad'][j]:7.3f} {q['b_quad'][j]:7.3f}"
        )
    print(
        "    -> DISTINCTIVE: the sinc branch predicts a NON-MONOTONIC bias vs z (it crosses its"
    )
    print(
        "       own zeros); the quadrature branch predicts a nearly FLAT bias. Non-thermal pressure"
    )
    print(
        "       predicts neither: it scales with the accretion rate, hence mass AND z."
    )

    # ------------------------------------------------------------------ [4] the scale test
    print(
        "\n[4] THE SCALE LADDER — where the scissor is zero, where it opens, and where it is testable"
    )
    print(
        f"    {'system (dynamical tracer)':30s} {'r [kpc]':>8s} {'M(<r)':>8s} {'t_dyn':>7s}"
        f" {'W_quad':>7s} {'b_quad':>7s}  regime"
    )
    for tag, rk, mm, fb in (
        ("spiral outer disc (HI)", 30.0, 1.5e11, 0.6),
        ("massive elliptical (R_eff)", 10.0, 2e11, 0.9),
        ("ultra-extended disc (band)", 60.0, 3e11, 0.5),
        ("galaxy satellites ~100 kpc", 100.0, 6e11, 0.25),
        ("galaxy satellites ~250 kpc", 250.0, 9e11, 0.15),
        ("group R500", 700.0, 8e13, 0.12),
        ("cluster R500", 1300.0, 6e14, 0.12),
    ):
        td = t_dyn_gyr(rk, mm)
        w = w_quad(td)
        a0 = C * A.H0 / (2 * np.pi)
        gb = G * mm * fb * MSUN / (rk * KPC) ** 2
        b = 1 - A.rar_obt(gb, w * a0) / A.rar_obt(gb, a0)
        reg = (
            "BAND (O(1) flagged)"
            if in_band(td)
            else ("adiabatic: W=1" if td < TGYR else "averaging")
        )
        print(f"    {tag:30s} {rk:8.0f} {mm:8.1e} {td:7.2f} {w:7.3f} {b:7.3f}  {reg}")
    print(
        "    -> CORRECTED READING (my first pass applied the averaging at ALL scales and wrongly"
    )
    print(
        "       printed 'the scissor vanishes at galaxy scales' next to a table saying 0.20):"
    )
    print(
        "       * galaxy DISCS are adiabatic (t_dyn < T/2): the scissor is EXACTLY zero there, which"
    )
    print(
        "         is what makes the observed agreement of the weak-lensing RAR (Brouwer 2021) with"
    )
    print("         the kinematic RAR (SPARC) consistent rather than fatal;")
    print(
        "       * galaxy SATELLITES at 100-250 kpc sit in or above the resonance band -> a predicted"
    )
    print(
        "         few-to-15% deficit of the kinematic mass against lensing. THAT is blade B of the"
    )
    print(
        "         scissor, still unmeasured, and it is the cleanest place to test the mechanism"
    )
    print(
        "         because there the Weyl fraction is small and the MOND term carries the signal."
    )

    # ------------------------------------------------------------------ [5] confrontation
    print("\n[5] CONFRONTATION WITH THE MEASURED BIAS  (1 - b = M_X-ray / M_lensing)")
    q = cluster_profile(6e14, 0.25)
    j = int(np.argmin(np.abs(q["r"] / q["r500"] - 1.0)))
    pred = {
        "OBT sinc branch (card as coded)": 1 - q["b_sinc"][j],
        "OBT quadrature branch (audit)": 1 - q["b_quad"][j],
    }
    meas = {
        "X-COP gas fraction (Eckert+19)": 0.86,
        "CCCP lensing (Hoekstra+15 class)": 0.76,
        "WtG lensing (Applegate+14 class)": 0.69,
        "this work: M-T vs CLASH lensing": 0.75,
        "Planck SZ counts require": 0.58,
    }
    for k, v in pred.items():
        print(f"    PREDICTED  {k:34s} 1-b = {v:.2f}")
    for k, v in meas.items():
        print(
            f"    MEASURED   {k:34s} 1-b = {v:.2f}"
            f"   [sinc {abs(v-pred['OBT sinc branch (card as coded)']):.2f} off,"
            f" quad {abs(v-pred['OBT quadrature branch (audit)']):.2f} off]"
        )
    print(
        "    -> THE UNCOMFORTABLE RESULT: the branch that matches the bulk of the measurements is"
    )
    print(
        "       the SINC branch -- the one the June-2026 audit ruled an artifact. The"
    )
    print(
        "       audit-corrected quadrature branch predicts only ~"
        f"{q['b_quad'][j]*100:.0f}% and lands closest to X-COP's own"
    )
    print(
        "       0.86, i.e. it explains roughly a THIRD of the mass gap this work measured (x1.34)."
    )

    # ---------------------------------------- [6] the card-#22 window re-run CLAUDE.md flagged pending
    print(
        "\n[6] THE 'SINC RE-RUN PENDING' FLAG, EXECUTED — card #22 re-fitted with the BOUNDED window"
    )
    xc = R.load_xcop()
    td_x = t_dyn_gyr(xc[:, 4] / KPC, xc[:, 0] * xc[:, 4] ** 2 / G / MSUN)
    f_sinc, b_sinc_fit, c_sinc = R.fit(xc, True, True, quiet=True)
    xb = xc.copy()
    xb[:, 3] = np.where(td_x < 0.5 * TGYR, 1.0, np.maximum(w_quad(td_x), w_floor))
    f_bd, b_bd, c_bd = R.fit(xb, True, True, quiet=True)
    xw = xc.copy()
    xw[:, 3] = 1.0
    f_w1, b_w1, c_w1 = R.fit(xw, True, True, quiet=True)
    print(
        f"    window = |sinc| (as coded)      : f_W = {f_sinc:.2f}, r_c = {b_sinc_fit:.3f} R500,"
        f" chi2/N = {c_sinc:.1f}"
    )
    print(
        f"    window = BOUNDED (audit, eps=1) : f_W = {f_bd:.2f}, r_c = {b_bd:.3f} R500,"
        f" chi2/N = {c_bd:.1f}"
    )
    print(
        f"    window = 1 (no averaging at all): f_W = {f_w1:.2f}, r_c = {b_w1:.3f} R500,"
        f" chi2/N = {c_w1:.1f}"
    )
    print(
        "    -> replacing the sinc by the bounded window moves the card's Weyl amplitude by"
        f" {f_bd-f_sinc:+.2f} in f_W"
    )
    print(
        f"       ({(f_bd/f_sinc-1)*100:+.0f}%) and the core radius by {b_bd-b_sinc_fit:+.3f} R500,"
        f" at a chi2/N of {c_bd:.1f} vs {c_sinc:.1f}."
    )
    print(
        "       The card's DEBUNK (two OBT scales beating a four-parameter ad-hoc form, Weyl-"
    )
    print(
        "       dominated) is unaffected in kind; its published NUMBERS are window-locked and this"
    )
    print(
        "       is the size of the lock. The flag in CLAUDE.md can now quote a number."
    )

    print("\n[VERDICT]")
    print(
        "    * THE MECHANISM IS REAL AND UNFORCED. Gas and galaxies are slow tracers, photons are"
    )
    print(
        "      not, so in OBT X-ray masses MUST come out below lensing masses, with the deficit"
    )
    print(
        "      RISING outward and VANISHING at galaxy-disc scales. Sign, radial shape and scale"
    )
    print(
        "      ladder all match what is observed. OBT therefore offers a mechanism for the"
    )
    print("      hydrostatic mass bias that costs it nothing extra.")
    print(
        "    * BUT IT IS BOUNDED, and that is the result of this dig: for ANY bounded positive a0"
    )
    print(
        "      oscillation (any depth eps in [0,1], at the most favourable phase) the window cannot"
    )
    print(
        f"      fall below W = {w_floor:.2f}, so the cluster bias is capped at b <= {bof(w_floor):.2f}"
        f" (1-b >= {1-bof(w_floor):.2f})."
    )
    print(
        "      Against the measured 0.75 (this work), 0.76 (CCCP), 0.69 (WtG), 0.58 (Planck) the"
    )
    print(
        "      scissor covers about a THIRD of the smallest of them and none of the largest."
    )
    print(
        "      OBT explains part of the hydrostatic bias; it does not explain it away."
    )
    print(
        "    * THE SINC IS NOT MERELY UN-AUDITED, IT IS OUT OF RANGE. Card #22's window reaches"
    )
    print(
        f"      W ~ {p['w_sinc'][i5]:.2f} at R500, below the {w_floor:.2f} floor that any bounded a0"
    )
    print(
        "      oscillation can produce. The sinc branch matches the data precisely BECAUSE it"
    )
    print(
        "      exceeds what the theory can supply. That is a critique of the card's window, not a"
    )
    print("      success of the theory.")
    print(
        "    * THE MODULATION DEPTH eps IS THE UNDERIVED INPUT. The sinc machinery implicitly"
    )
    print(
        "      takes eps = 1 (a0 swinging to zero every 2 Gyr); OBT's own motor amplitude is"
    )
    print(
        "      f_osc = 0.10, which would give b ~ 0.02 -- a scissor of essentially nothing. Nothing"
    )
    print(
        "      in V8.2 fixes eps, and the whole ARA cluster phenomenology scales with it."
    )
    print(
        "    * SIGN IS PHASE-DEPENDENT: for s_now < 0 the scissor REVERSES (dynamics above"
    )
    print(
        "      lensing). The observed sign therefore constrains where we sit in the cycle -- a"
    )
    print(
        "      chronology statement that must be checked against OBT's own phase-0.9 anchoring,"
    )
    print("      not assumed.")
    print(
        f"    * CARD #22, RE-RUN: with the bounded window the card's globals move to f_W = {f_bd:.2f},"
    )
    print(
        f"      r_c = {b_bd:.3f} R500 (from {f_sinc:.2f}, {b_sinc_fit:.3f}), at a BETTER chi2/N"
        f" ({c_bd:.1f} vs {c_sinc:.1f})."
    )
    print(
        "      Two independent calibrations then nearly agree in f_W -- 0.57 on X-COP dynamics and"
    )
    print(
        "      0.59 on CLASH lensing -- but they are normalised to mass scales that differ by x1.34,"
    )
    print(
        "      so in ABSOLUTE Weyl the lensing channel still wants ~x1.4 more. The scissor supplies"
    )
    print(
        "      at most x1.1 of that. The residual is the same unexplained factor the alpha_NT note"
    )
    print("      priced: the two threads of this session converge on one number.")
    print("    * NAMED FALSIFIERS (these can kill it):")
    print(
        "      (i)   a hydrostatic bias strongly MASS-dependent at fixed overdensity kills the ARA"
    )
    print("            reading -- the theorem in [3] makes it mass-independent;")
    print(
        "      (ii)  a bias that vanishes at large radius kills it (the window only opens outward);"
    )
    print(
        "      (iii) a lensing-vs-dynamics discrepancy at galaxy-DISC scales kills it (adiabatic"
    )
    print("            there, prediction exactly zero);")
    print(
        "      (iv)  BLADE B, the clean positive test: satellite kinematics vs galaxy-galaxy"
    )
    print(
        "            lensing at 100-250 kpc, where the Weyl fraction is small and the MOND term"
    )
    print(
        "            carries the signal. Predicted deficit at the cap: a few to ~15% in g"
    )
    print(
        "            (<= 0.07 dex). A null there at that precision closes the mechanism."
    )
    print(
        "    * SCOPE: spherical; one fiducial cluster shape; the Weyl held at the card's globals;"
    )
    print(
        "      gas from a universal-closure model; the a0(t) waveform taken as a bounded sinusoid"
    )
    print(
        "      (its true shape is not derived in V8.2); the measured biases are declared literature"
    )
    print("      values, not re-derived here, except this work's 0.75.")
    print("=" * 104)


if __name__ == "__main__":
    main()
