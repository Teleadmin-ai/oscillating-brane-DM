#!/usr/bin/env python3
"""SKA 21cm reionization forecast (CORRECTED + triple-checked, June 2026).

The old scripts/ska_21cm_mock.py was FLAWED: it modulated the 21cm signal with a SCALE-DEPENDENT G_eff(k)
from the Yukawa coupling -- the BANNED "scale-dependent Yukawa screening" -- never used the real temporal
f_osc, and had ad-hoc growth/noise factors. Its 5.46 mK / 5.5sigma was an artifact.

CORRECT mechanism (scale-INDEPENDENT): the temporal G_eff(t)=1+f_osc*W(t/T+delta_bulk/2pi) (same as S8)
modulates the linear GROWTH D(z) -> the collapsed fraction f_coll (exponentially sensitive) -> the
reionization history Q(z) -> the 21cm global signal T_b(z).

THEORY RE-READ (the things missed on the first pass, theory.md):
  * AMPLITUDE: reionization (z~6-15, t~0.3-0.95 Gyr) is LESS THAN ONE CYCLE from QCD ignition (T=2 Gyr).
    f_osc=0.10 is the CONVERGED limit-cycle amplitude (contraction kappa=e^-4.74/cycle); at reionization
    (first cycle) the amplitude is the IGNITION value -- theory-UNPINNED. We bracket f_osc_reion in [0.05,0.20].
  * PHASE: G_eff is anchored phase 0.0 at QCD (cosmic time) with the lag delta_bulk=1.36 rad; we scan phase.
  * WAVEFORM: W is the stick-slip sawtooth; here a sine proxy (shape approximation).
This is therefore an ORDER-OF-MAGNITUDE forecast, not a precise number; we report the honest range.
"""

import numpy as np
from scipy.integrate import cumulative_trapezoid, solve_ivp
from scipy.interpolate import interp1d
from scipy.special import erfc

Om, OL, h = 0.315, 0.685, 0.674
Ob = 0.0493
H0_Gyr = 0.0689
T_osc = 2.0
delta_bulk = 1.36  # rad, BKM phase lag (theory.md)


def E(a):
    return np.sqrt(Om / a**3 + OL)


# precompute cosmic time t(a) on a grid (avoids nested quadrature in the ODE)
_ag = np.logspace(-6, 0, 4000)
_tg = cumulative_trapezoid(1.0 / (_ag * E(_ag)), _ag, initial=0.0) / H0_Gyr
_t_of_a = interp1d(
    _ag, _tg, kind="cubic", bounds_error=False, fill_value=(0.0, _tg[-1])
)


def growth(g_eff_fn, a_eval):
    def rhs(a, y):
        D, Dp = y
        dlnE = -1.5 * Om / (a**4 * E(a) ** 2)
        src = 1.5 * Om / (a**5 * E(a) ** 2) * g_eff_fn(a) * D
        return [Dp, -(3.0 / a + dlnE) * Dp + src]

    a_i = 1e-3
    sol = solve_ivp(
        rhs,
        (a_i, 1.0),
        [a_i, 1.0],
        t_eval=np.sort(np.r_[a_eval, 1.0]),
        rtol=1e-8,
        atol=1e-12,
        dense_output=True,
    )
    return sol.sol(a_eval)[0], sol.sol(1.0)[0]


def reion(D, D0, sigma8_M, zeta):
    sigma = sigma8_M * D / D0
    f_coll = erfc(1.686 / (np.sqrt(2) * sigma))
    return np.minimum(1.0, zeta * f_coll), f_coll


def T_b(z, Q):
    Ob_h2, Om_h2 = Ob * h**2, Om * h**2
    return 27.0 * (1.0 - Q) * (Ob_h2 / 0.023) * np.sqrt((0.15 / Om_h2) * (1 + z) / 10.0)


def peak_dTb(f_osc_r, phase, z, a, D_l, D0_l, sigma8_M, zeta):
    g = lambda aa: 1.0 + f_osc_r * np.sin(2 * np.pi * _t_of_a(aa) / T_osc + phase)
    D_o, D0_o = growth(g, a)
    Q_l, _ = reion(D_l, D0_l, sigma8_M, zeta)
    Q_o, _ = reion(D_o, D0_o, sigma8_M, zeta)
    dTb = T_b(z, Q_o) - T_b(z, Q_l)
    gmod = D_o / D0_o / (D_l / D0_l) - 1.0
    return np.max(np.abs(dTb)), z[np.argmax(np.abs(dTb))], np.max(np.abs(gmod))


def main():
    print("=" * 74)
    print(
        "SKA 21cm forecast (CORRECTED + triple-checked) -- temporal scale-INDEP G_eff(t)"
    )
    print("=" * 74)
    z = np.linspace(5.5, 16, 60)
    a = 1.0 / (1 + z)
    D_l, D0_l = growth(lambda aa: 1.0, a)

    # calibrate zeta so LCDM reionization completes near z~6.5
    sigma8_M = 2.5
    iz = np.argmin(np.abs(z - 6.5))
    zeta = 1.0 / erfc(1.686 / (np.sqrt(2) * sigma8_M * D_l[iz] / D0_l))
    print(
        f"[calib] zeta={zeta:.0f} (LCDM Q->1 @ z~6.5); sigma8_M={sigma8_M}; t(z=6)={_t_of_a(1/7.0):.2f} Gyr, t(z=15)={_t_of_a(1/16.0):.2f} Gyr"
    )
    print(
        f"[note]  reionization spans ~{_t_of_a(1/16.0):.2f}-{_t_of_a(1/7.0):.2f} Gyr = {_t_of_a(1/16.0)/T_osc:.2f}-{_t_of_a(1/7.0)/T_osc:.2f} cycles from QCD -> FIRST cycle (amplitude unpinned)"
    )

    print(
        "\n[SCAN] peak |Delta T_b| (mK) over the honest uncertainty grid (amplitude x phase):"
    )
    print(
        f"  {'f_osc_reion':>12} | "
        + " | ".join(f"phase={p:>4}" for p in ["0", "dlt", "pi/2", "pi"])
    )
    phases = {"0": 0.0, "dlt": delta_bulk, "pi/2": np.pi / 2, "pi": np.pi}
    rows = {}
    for fr in (0.02, 0.05, 0.10, 0.20):
        row = [
            peak_dTb(fr, ph, z, a, D_l, D0_l, sigma8_M, zeta)[0]
            for ph in phases.values()
        ]
        rows[fr] = row
        print(f"  {fr:>12.2f} | " + " | ".join(f"{v:8.2f}" for v in row))
    allpk = [v for row in rows.values() for v in row]
    lo, hi = min(allpk), max(allpk)
    print(
        f"\n  RANGE: peak |Delta T_b| = {lo:.2f} - {hi:.2f} mK across amplitude(0.02-0.20) x phase"
    )
    print(
        f"  (nominal f_osc=0.10: ~{min(rows[0.10]):.1f}-{max(rows[0.10]):.1f} mK; but the amplitude AT reionization is"
    )
    print(
        f"   theory-unpinned -- f_osc=0.02 gives ~{min(rows[0.02]):.1f} mK (undetectable); see the amplitude caveat below)"
    )

    print("\n[SNR] foreground-limited detectability (order of magnitude):")
    for noise, lab in [
        (1.0, "optimistic 1 mK (deeply fg-cleaned)"),
        (5.0, "realistic 5 mK (residual fg)"),
    ]:
        print(f"  SNR(peak)/{lab} = {lo/noise:.1f} - {hi/noise:.1f} sigma")

    print("\nHONEST VERDICT (triple-checked):")
    print(
        "  * the OLD 5.46 mK / 5.5sigma is an ARTIFACT of the BANNED scale-dependent Yukawa -- discard it."
    )
    print(
        "  * the corrected scale-INDEPENDENT mechanism gives an ORDER-OF-MAGNITUDE peak ~few mK, but with"
    )
    print(
        "    LARGE theory-unpinned amplitude uncertainty (Delta T_b is ~proportional to it): reionization is"
    )
    print(
        "    <1 cycle from QCD ignition, so the amplitude is the FIRST-CYCLE value -- set by the competition"
    )
    print(
        "    between the QCD ignition kick (could be > 0.10) and the cosmic-web forcing F_web that sustains the"
    )
    print(
        "    limit cycle, which is WEAK before large-scale structure forms (z<~3, so could be << 0.10). Unpinned"
    )
    print(
        "    in BOTH directions -> Delta T_b could be << 1 mK (undetectable) or ~few mK. Phase carries delta_bulk;"
    )
    print(
        "    waveform is a sawtooth not a sine; SNR is foreground-DOMINATED (global signal vs ~1e4 K Galactic fg)."
    )
    print(
        "  * => SKA 21cm is a PLAUSIBLE order-of-magnitude test (~mK, marginal SNR), NOT a precise"
    )
    print(
        "    'definitive 5.5sigma'. predictions.md should be DOWNGRADED accordingly. A real number needs"
    )
    print(
        "    21cmFAST + the first-cycle amplitude from the ignition ODE + a foreground/noise pipeline."
    )


if __name__ == "__main__":
    main()
