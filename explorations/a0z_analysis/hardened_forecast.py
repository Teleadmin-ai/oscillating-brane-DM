"""a0(z) HARDENED forecast (option 1, June 2026) -- separate RANDOM from COHERENT systematics.

REVIEWER MODE (axiom: OBT can be false). The published scripts/a0z_forecast.py adds a per-bin systematic
f_sys in quadrature with the statistical error and divides by sqrt(N_bins). That is CORRECT for a random
per-bin scatter but WRONG for a COHERENT z-dependent bias -- which is exactly the kind the high-z baryonic /
velocity census injects, and exactly what drives the observed ~1.5x rate excess.

MODEL.  Fit a straight line  ln a0_measured(z) = ln a0_0 + alpha * ln E(z) + b(z) + eps,  with
  E(z) = sqrt(Om(1+z)^3 + OL),   eps_i ~ N(0, sigma_stat^2)  [random per-bin -> averages down],
  b(z) = the COHERENT systematic impact on ln a0 (already SIGNED; see lever recap below).
Decompose b(z) along the regressor: the part proportional to ln E(z), beta_sys = Cov(b,lnE)/Var(lnE), adds
DIRECTLY to the fitted slope and does NOT shrink with N; a z-independent offset shifts only the intercept:
  alpha_hat = alpha_true + beta_sys + N(0, sigma_alpha^2),   sigma_alpha = sigma_stat / (sqrt(N) * SD[ln E]).

LEVER RECAP (deep-MOND a0 = V_c^4/(G M_bar); RAR a0 = g_obs^2/g_bar) -> dln a0 = 4 dlnV_c - dln M_bar
(kinematic) or 2 dln g_obs - dln M_bar (lensing). So a fractional bias in the measured observable maps to a
SIGNED b(z):
  - V_c over-estimated by f  ->  b = +4f   (a0 inflated)      | V_c under (beam smearing) -> b = -4f
  - M_bar under-counted by f ->  b = +f    (a0 inflated)      | M_bar over (local M/L too high) -> b = -f
  - lensing g_obs over by f  ->  b = +2f   (a0 inflated)
The systematics therefore go BOTH ways; only the NET coherent b(z) biases alpha (dissected in script B).

CONSEQUENCES (checked numerically):
  (i)  EVOLUTION test (alpha != 0): robust -- fails only if beta_sys ~ -alpha_true ~ -1 (a huge bias that
       ANTI-tracks E(z)). Euclid/Rubin settle OBT-vs-constant-MOND.
  (ii) RATE test (alpha=1 vs 1.5, the cH(z)/2pi form): alpha_hat = 1 + beta_sys, so a coherent beta_sys ~ 0.5
       makes alpha_true=1 LOOK like 1.5. NOT helped by more lenses -> systematics-limited, the real frontier.
"""

import numpy as np

Om, OL = 0.315, 0.685


def E(z):
    return np.sqrt(Om * (1 + z) ** 3 + OL)


def sd_lnE(zmin, zmax, nbin):
    return np.std(np.log(E(np.linspace(zmin, zmax, nbin))))


def sigma_alpha(zmin, zmax, nbin, sigma_stat_perbin):
    """Statistical 1-sigma on slope alpha from a straight-line fit ln a0 vs ln E(z)."""
    sd = sd_lnE(zmin, zmax, nbin)
    return np.inf if (sd == 0 or nbin < 2) else sigma_stat_perbin / (np.sqrt(nbin) * sd)


def beta_sys(zmin, zmax, nbin, b_of_z):
    """Coherent-bias slope = Cov(b, lnE)/Var(lnE); b_of_z = SIGNED impact on ln a0 (lever already applied)."""
    z = np.linspace(zmin, zmax, nbin)
    x = np.log(E(z))
    xc = x - x.mean()
    return np.sum(xc * b_of_z(z)) / np.sum(xc * xc)


def lin_to_zmax(fmax, zmax=1.5):
    """A bias growing linearly from 0 at z=0 to fmax at zmax (fractional, in the measured observable)."""
    return lambda z: fmax * z / zmax


def main():
    print("=" * 100)
    print(
        "a0(z) HARDENED FORECAST -- statistics (sigma_alpha) vs the coherent-bias slope (beta_sys), the real wall"
    )
    print("=" * 100)

    # -- VERIFY against achieved MUSE-DARK III precision (reproduce ~16 sigma on alpha!=0) --
    sa_muse = sigma_alpha(0.4, 1.4, 4, 0.024)
    print(
        f"\n[VERIFY] MUSE-DARK III (4 bins z 0.4-1.4, 2.4%/bin): sigma_alpha={sa_muse:.3f} -> alpha=1 vs 0 at "
        f"{1/sa_muse:.0f}sigma (published a1=1.59+-0.10 = 16sigma) {'OK' if 13 < 1/sa_muse < 20 else 'CHECK'}"
    )
    print(
        "[VERIFY] symmetric in alpha (rejects alpha=0 AND alpha=1 equally -> no OBT pre-bias); "
        f"nbin=1 -> sigma_alpha={sigma_alpha(0.4,1.4,1,0.02):.0f} (no leverage); "
        f"sigma_stat->0 -> sigma_alpha={sigma_alpha(0.4,1.4,10,1e-6):.0e}"
    )

    print("\n[1] STATISTICAL reach (variance only) -- realistic per-bin a0 errors:")
    for name, (zmn, zmx, nb, fst) in {
        "Euclid lensing RAR (z 0.3-1.5, 10 bins)": (0.3, 1.5, 10, 0.015),
        "Rubin/LSST lensing RAR (z 0.2-1.2, 10 bins)": (0.2, 1.2, 10, 0.012),
        "high-z kinematic RAR MUSE/JWST (z 0.5-3, 6 bins)": (0.5, 3.0, 6, 0.06),
    }.items():
        sa = sigma_alpha(zmn, zmx, nb, fst)
        print(
            f"  {name:48s} {fst*100:4.1f}%/bin -> sigma_alpha={sa:6.4f} | evolution(1vs0) {1/sa:5.1f}s | "
            f"rate(1vs1.5) IF beta=0 {0.5/sa:5.1f}s"
        )
    print(
        "  -> statistics alone make BOTH tests look decisive. But the rate test only if beta_sys=0. See [2]."
    )

    print(
        "\n[2] COHERENT-BIAS slope beta_sys (biases alpha_hat = alpha_true + beta_sys). Plausible high-z models,"
    )
    print("    z 0.3-1.5, SIGNED a0-impact b(z) (lever applied) -- they go BOTH ways:")
    zmn, zmx, nb = 0.3, 1.5, 10
    sa_euclid = sigma_alpha(zmn, zmx, nb, 0.015)
    models = [
        (
            "M_bar under-count (missing gas) ->30%",
            lambda z: +1.0 * lin_to_zmax(0.30)(z),
        ),
        (
            "V_c over-estimate (incl/pressure) ->10%",
            lambda z: +4.0 * lin_to_zmax(0.10)(z),
        ),
        ("V_c over-estimate ->6%", lambda z: +4.0 * lin_to_zmax(0.06)(z)),
        ("lensing g_obs over (2-halo/IA) ->8%", lambda z: +2.0 * lin_to_zmax(0.08)(z)),
        (
            "V_c UNDER (beam smearing) ->10% [deflates]",
            lambda z: -4.0 * lin_to_zmax(0.10)(z),
        ),
        (
            "M_bar over (local M/L) ->20% [deflates]",
            lambda z: -1.0 * lin_to_zmax(0.20)(z),
        ),
    ]
    for label, bfun in models:
        bs = beta_sys(zmn, zmx, nb, bfun)
        tag = (
            "FAKES the 1.5x rate"
            if 0.35 < bs < 0.75
            else ("inflates" if bs > 0 else "DEFLATES (against)")
        )
        print(
            f"  {label:46s} beta_sys={bs:+5.2f} => alpha_hat(true=1)={1+bs:4.2f}  ({tag})"
        )
    print(
        f"\n  statistical sigma_alpha(Euclid)={sa_euclid:.3f}; coherent |beta_sys|~0.2-0.5 = "
        f"{0.45/sa_euclid:.0f}x the statistical error. The rate test is systematics-dominated."
    )

    print("\n[3] What it takes to FAKE each verdict (the robustness asymmetry):")
    # invert beta_sys = b_slope for a linear bias b(z) = B*(z/zmax): beta = B * Cov(z/zmax, lnE)/Var(lnE)
    z = np.linspace(zmn, zmx, nb)
    x = np.log(E(z))
    xc = x - x.mean()
    g = (z / zmx) - (z / zmx).mean()
    k = np.sum(xc * g) / np.sum(
        xc * xc
    )  # beta_sys = B_amplitude * k, B = a0-impact at z=zmax
    B_erase = -1.0 / k  # need beta_sys = -1 (erase alpha=1)
    B_rate = +0.5 / k  # need beta_sys = +0.5 (fake 1->1.5)
    print(
        f"  ERASE evolution (alpha 1->0): need a coherent a0-impact b(zmax)={B_erase:+.2f} that ANTI-tracks E(z)"
    )
    print(
        f"    = M_bar OVER-count growing to {abs(B_erase)*100:.0f}% (lever 1x) or V_c UNDER to "
        f"{abs(B_erase)/4*100:.0f}% (lever 4x). Implausible (wrong sign + huge) -> EVOLUTION IS SAFE."
    )
    print(
        f"  FAKE 1.5x rate (alpha 1->measured 1.5): need b(zmax)={B_rate:+.2f} = V_c over-estimate "
        f"{B_rate/4*100:.0f}% (4x lever) or M_bar under-count {B_rate*100:.0f}% (1x lever)."
    )
    print(
        "    BOTH are within plausible high-z budgets -> RATE IS FRAGILE / systematics-limited."
    )

    print("\nVERDICT (option 1):")
    print(
        "  * EVOLUTION (a0 evolves; OBT vs constant-MOND): tens of sigma statistically AND robust to coherent"
    )
    print(
        "    bias (erasing it needs an implausible wrong-sign beta_sys~-1). Euclid/Rubin SETTLE it. The pepite."
    )
    print(
        "  * RATE (cH(z)/2pi form, alpha=1 vs 1.5): alpha_hat = 1 + beta_sys; a coherent ~10% V_c (4x) or ~40%"
    )
    print(
        "    M_bar (1x) high-z bias injects beta_sys~0.5 -> exactly the observed 1.5x. Consistent with"
    )
    print(
        "    alpha_true=1 + bias. The form test needs beta_sys MODELLED/REMOVED, not more lenses. -> script B."
    )


if __name__ == "__main__":
    main()
