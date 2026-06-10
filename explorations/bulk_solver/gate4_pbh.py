"""
GATE 4 — the PBH-sector internal variable, the BKM phase, and the growth sign.

Gates 3a/3b proved the 5D bulk-wave sector (conservative or boundary-dissipative)
supplies neither the S8 phase lag nor a growth sign. OBT's S8 mechanism therefore
rests on the PBH-sector INTERNAL relaxational dynamics: the effective coupling
modulation X(t) following the radion drive W_d(t) through

    dX/dt = Gamma(t) * (W_d(t) - X),     Gamma(t) = Gamma_stick | Gamma_slip

with stick/slip switching synced to the cycle (OBT: Gamma_stick = 3H = 0.243/Gyr,
Gamma_slip = Gamma_rad = 20.7/Gyr, omega = 2pi/T = pi/Gyr, slip fraction ~10%),
and the BKM averaging claim delta_bulk = 0.9 arctan(om/G_st) + 0.1 arctan(om/G_sl)
= 1.36 rad.

GATE 4a: integrate the ACTUAL switched system and measure the lag of X's
fundamental vs the drive — does the BKM averaging hold for the real (switched,
possibly sawtooth-driven) system?

GATE 4b: the growth sign, with OBT's REAL numbers. EdS matter-era growth in
cosmic time (H = 2/3t), t in [t_i, 13.8] Gyr, Poisson term modulated by
G_eff/G_N = 1 + f * X(t) (f = f_osc = 0.10, T = 2.000 Gyr, phase anchored):
    D'' + 2H D' = (3/2) H^2 [1 + f X(t)] D.
Readout Delta lnD = ln(D_mod/D_smooth) at t0 = 13.8 Gyr ~ Delta S8/S8.
Decompositions that separate DERIVED from INPUT:
  - even/odd in f (f -> -f): the EVEN part is sign-definite under the coupling-
    sign freedom (candidate genuine prediction); the ODD part flips with the
    input sign convention (closure freedom).
  - waveform: sinusoid vs asymmetric stick-slip sawtooth (rise 90%, slip 10%).
  - lag: OBT Gammas vs Gamma -> infinity (X = W, no lag) vs no filtering.
  - anchoring scan: drive phase at ignition in {0, .25, .5, .75} cycles: the
    spread measures the anchoring-input component.
NOTE (honest): this integrates OBT's OWN stated G_eff(t) machinery independently;
any tension with the V8.2 S8 magnitude (4-10%) is an explorations-level audit
flag to cross-check against scripts/growth_factor.py before touching V8.2.
"""

import numpy as np
from scipy.integrate import solve_ivp

# OBT parameters (Gyr units)
T_RAD = 2.000
OM = 2.0 * np.pi / T_RAD  # = pi
G_STICK = 0.243
G_SLIP = 20.7
SLIP_FRAC = 0.10
T0 = 13.8
F_OSC = 0.10
DELTA_BKM = 0.9 * np.arctan(OM / G_STICK) + 0.1 * np.arctan(OM / G_SLIP)


# ------------------------------------------------------------------- drives
def chi(t, t_anchor=0.0):
    return ((t - t_anchor) / T_RAD) % 1.0


def W_sin(t, t_anchor=0.0):
    return np.sin(2.0 * np.pi * chi(t, t_anchor))


def W_saw(t, t_anchor=0.0):
    """Asymmetric stick-slip sawtooth: linear rise -1->+1 over the stick phase
    (1-SLIP_FRAC of the cycle), linear fall +1->-1 over the slip phase. Zero-mean."""
    x = chi(t, t_anchor)
    up = 1.0 - SLIP_FRAC
    return np.where(x < up, -1.0 + 2.0 * x / up, 1.0 - 2.0 * (x - up) / SLIP_FRAC)


def Gamma_t(t, t_anchor=0.0):
    """Slip window = the falling segment of the cycle."""
    return np.where(chi(t, t_anchor) < 1.0 - SLIP_FRAC, G_STICK, G_SLIP)


# ---------------------------------------------------- 4a: the switched filter
def relax_X(W, t_grid, t_anchor=0.0, filt="obt"):
    """Integrate dX/dt = Gamma(t)(W(t)-X) on t_grid. filt: 'obt' (switched),
    'fast' (X=W, no lag), 'stick' (constant G_STICK), 'slip' (constant G_SLIP)."""
    if filt == "fast":
        return W(t_grid, t_anchor)

    def gam(t):
        if filt == "obt":
            return float(Gamma_t(t, t_anchor))
        return G_STICK if filt == "stick" else G_SLIP

    def rhs(t, y):
        return [gam(t) * (W(np.array([t]), t_anchor)[0] - y[0])]

    sol = solve_ivp(
        rhs,
        [t_grid[0], t_grid[-1]],
        [0.0],
        t_eval=t_grid,
        method="LSODA",
        rtol=1e-8,
        atol=1e-10,
        max_step=T_RAD / 200.0,
    )
    return sol.y[0]


def lag_of(X, W, t_grid, t_anchor=0.0, n_skip=3):
    """Fundamental-harmonic lag of X behind W over integer cycles post-transient."""
    m = t_grid >= t_grid[0] + n_skip * T_RAD
    tt = t_grid[m]
    n_full = int(np.floor((tt[-1] - tt[0]) / T_RAD))
    m2 = tt <= tt[0] + n_full * T_RAD
    tt = tt[m2]

    def fourier(y):
        c = np.trapezoid(y * np.cos(OM * tt), tt)
        s = np.trapezoid(y * np.sin(OM * tt), tt)
        return np.arctan2(c, s), np.hypot(c, s)

    phX, aX = fourier(X[m][m2])
    phW, aW = fourier(W(tt, t_anchor))
    lag = (phW - phX) % (2.0 * np.pi)
    if lag > np.pi:
        lag -= 2.0 * np.pi
    return lag, aX / aW


def gate4a():
    print("[4a] switched relaxational PBH filter: lag of X vs drive (OBT params)")
    print(
        f"     BKM claim: delta = 0.9 atan(om/G_st) + 0.1 atan(om/G_sl) = {DELTA_BKM:.3f} rad"
    )
    t = np.linspace(0.0, 12 * T_RAD, 24000)
    for wname, W in [("sinusoid", W_sin), ("stick-slip sawtooth", W_saw)]:
        for filt, tag in [
            ("obt", "switched stick/slip"),
            ("stick", "const G_stick"),
            ("slip", "const G_slip"),
        ]:
            X = relax_X(W, t, filt=filt)
            lag, gain = lag_of(X, W, t)
            print(f"     {wname:20s} | {tag:20s}: lag={lag:+.3f} rad  gain={gain:.3f}")


# ----------------------------------------------------- 4b: the growth readout
def filtered_drive(W, filt, t_anchor, t_i):
    """Warm-started (limit-cycle), amplitude-normalized filter output on a dense
    grid covering [t_i, T0]: X with unit fundamental amplitude, zero mean.
    Warm start: integrate from t_i - 8 T_RAD so the filter enters the era in its
    limit cycle (physical: the motor has run since ignition)."""
    t_warm = t_i - 8.0 * T_RAD
    tg_full = np.linspace(t_warm, T0, 60000)
    X = relax_X(W, tg_full, t_anchor, filt)
    m = tg_full >= t_i
    tg, X = tg_full[m], X[m]
    # normalize the FUNDAMENTAL amplitude to 1 (G-modulation amplitude = f exactly)
    c = np.trapezoid(X * np.cos(OM * (tg - t_anchor)), tg)
    s = np.trapezoid(X * np.sin(OM * (tg - t_anchor)), tg)
    amp = 2.0 * np.hypot(c, s) / (tg[-1] - tg[0])
    X = X / max(amp, 1e-12)
    X = X - np.trapezoid(X, tg) / (tg[-1] - tg[0])  # exact zero-mean (BBN rule)
    return tg, X


def growth(f, W, filt="obt", t_anchor=0.0, t_i=0.05):
    """EdS matter-era growth with G_eff = 1 + f*X(t); returns ln(D/D_smooth) at T0."""
    tg, X = filtered_drive(W, filt, t_anchor, t_i)
    Xi = lambda t: np.interp(t, tg, X)  # noqa: E731

    def rhs(t, y):
        H = 2.0 / (3.0 * t)
        return [y[1], -2.0 * H * y[1] + 1.5 * H * H * (1.0 + f * Xi(t)) * y[0]]

    # growing-mode IC: D ~ t^(2/3)
    y0 = [t_i ** (2.0 / 3.0), (2.0 / 3.0) * t_i ** (-1.0 / 3.0)]
    s1 = solve_ivp(
        rhs,
        [t_i, T0],
        y0,
        method="LSODA",
        rtol=1e-10,
        atol=1e-12,
        max_step=T_RAD / 100.0,
    )

    def rhs0(t, y):
        H = 2.0 / (3.0 * t)
        return [y[1], -2.0 * H * y[1] + 1.5 * H * H * y[0]]

    s0 = solve_ivp(
        rhs0,
        [t_i, T0],
        y0,
        method="LSODA",
        rtol=1e-10,
        atol=1e-12,
        max_step=T_RAD / 100.0,
    )
    return np.log(s1.y[0, -1] / s0.y[0, -1])


def gate4b():
    print("\n[4b] growth response, OBT numbers (f=0.10, T=2 Gyr, EdS to 13.8 Gyr):")
    print("     DlnD ~ DS8/S8; OBT V8.2 claims -4..-10%")
    print(
        f"     {'waveform':>10s}{'filter':>10s}{'anchor':>8s}{'DlnD(+f)':>12s}{'DlnD(-f)':>12s}{'EVEN':>11s}{'ODD':>11s}"
    )
    rows = []
    for wname, W in [("sin", W_sin), ("sawtooth", W_saw)]:
        for filt in ["obt", "fast"]:
            for anc in [0.0, 0.25, 0.5, 0.75]:
                dp = growth(+F_OSC, W, filt, anc * T_RAD)
                dm = growth(-F_OSC, W, filt, anc * T_RAD)
                ev, od = 0.5 * (dp + dm), 0.5 * (dp - dm)
                rows.append((wname, filt, anc, dp, dm, ev, od))
                print(
                    f"     {wname:>10s}{filt:>10s}{anc:8.2f}{dp:+12.2e}{dm:+12.2e}{ev:+11.2e}{od:+11.2e}"
                )
    ev_all = np.array([r[5] for r in rows])
    od_all = np.array([r[6] for r in rows])
    print(
        f"     EVEN part (coupling-sign-proof): range [{ev_all.min():+.2e}, {ev_all.max():+.2e}]"
    )
    print(
        f"     ODD  part (flips with input sign): range [{od_all.min():+.2e}, {od_all.max():+.2e}]"
    )
    # f-scaling check (sawtooth+obt, anchor 0): EVEN ~ f^2, ODD ~ f
    dp1, dm1 = growth(+F_OSC, W_saw, "obt", 0.0), growth(-F_OSC, W_saw, "obt", 0.0)
    dp2, dm2 = growth(+F_OSC / 2, W_saw, "obt", 0.0), growth(
        -F_OSC / 2, W_saw, "obt", 0.0
    )
    print(
        f"     f-scaling (saw/obt/anc0): EVEN(f)/EVEN(f/2)={(dp1+dm1)/(dp2+dm2):.2f} (expect ~4),"
        f" ODD(f)/ODD(f/2)={(dp1-dm1)/(dp2-dm2):.2f} (expect ~2)"
    )


if __name__ == "__main__":
    gate4a()
    gate4b()
