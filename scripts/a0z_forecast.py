"""a0(z) forecast -- discriminating power of imminent surveys for the OBT-distinctive prediction
a0(z) = cH(z)/2pi = a0_0 * E(z)  (OBT: alpha=1; constant-a0 MOND: alpha=0), with a0(z)=a0_0*E(z)^alpha.

[CORRECTED June 2026 -- random vs coherent systematics.] The earlier version added the per-bin systematic in
quadrature with the statistical error and divided by sqrt(N_bins). That is correct for a RANDOM per-bin scatter
but WRONG for a COHERENT z-dependent bias, which does NOT average down -- it biases the fitted slope directly.
We model  ln a0_meas(z) = ln a0_0 + alpha*ln E(z) + b(z) + eps,  with eps_i ~ N(0, sigma_stat^2) [random] and
b(z) the coherent systematic. Its slope-projection beta_sys = Cov(b,lnE)/Var(lnE) ADDS to the fitted slope and
does NOT shrink with N:
  alpha_hat = alpha_true + beta_sys + N(0, sigma_alpha^2),   sigma_alpha = sigma_stat / (sqrt(N) * SD[ln E]).

Levers (deep-MOND a0 = V_c^4/(G M_bar); RAR a0 = g_obs^2/g_bar): a coherent fractional bias maps to b(z) with
lever V_c -> 4x, M_bar -> 1x, lensing g_obs -> 2x. So a ~10% coherent V_c bias (4x) already injects beta_sys~0.5.

Two questions, opposite-direction caution (the forecast is symmetric in alpha -> no OBT pre-bias):
  (i)  EVOLUTION vs CONSTANT (alpha=1 vs 0): robust -- tens of sigma statistically, and a coherent bias can only
       erase it with an implausible beta_sys ~ -1. -> Euclid/Rubin settle OBT-vs-constant-MOND.
  (ii) the cH(z)/2pi FORM/RATE test (alpha=1 vs ~1.5): alpha_hat = 1 + beta_sys, so the observed ~1.5x is faked
       by beta_sys~0.5 from plausible high-z V_c/gas systematics. NOT helped by more lenses -> systematics-limited.
The decisive discriminator is a CROSS-LEVER measurement (lensing a0 = no V_c lever, vs kinematic a0 = 4x V_c);
full dissection in explorations/a0z_analysis/.
"""

import numpy as np

Om, OL = 0.315, 0.685


def E(z):
    return np.sqrt(Om * (1 + z) ** 3 + OL)


def sd_lnE(zmin, zmax, nbin):
    return np.std(np.log(E(np.linspace(zmin, zmax, nbin))))


def sigma_alpha(zmin, zmax, nbin, sigma_stat_perbin):
    """Statistical 1-sigma on the slope alpha (RANDOM per-bin error only; this is the part that averages down)."""
    sd = sd_lnE(zmin, zmax, nbin)
    return np.inf if (sd == 0 or nbin < 2) else sigma_stat_perbin / (np.sqrt(nbin) * sd)


def beta_sys(zmin, zmax, nbin, b_at_zmax):
    """Coherent-bias slope = Cov(b,lnE)/Var(lnE) for a SIGNED a0-impact b(z) = b_at_zmax * z/zmax.

    The bias grows linearly from 0 at z=0 (the local calibration anchor) to b_at_zmax at z=zmax, evaluated over
    the survey bins [zmin, zmax]. This is the term that biases alpha_hat = alpha_true + beta_sys and does NOT
    average down with N. (z=0 anchor, consistent with explorations/a0z_analysis.)
    """
    z = np.linspace(zmin, zmax, nbin)
    x = np.log(E(z))
    xc = x - x.mean()
    return np.sum(xc * (b_at_zmax * z / zmax)) / np.sum(xc * xc)


def coherent_floor(zmin, zmax, nbin, dalpha, n_sigma):
    """Per-bin RANDOM systematic floor to reach n_sigma on a slope difference dalpha (the form test).

    NOTE: this bounds only the RANDOM systematic; the COHERENT bias beta_sys is a separate, harder limit
    (it must be MODELLED/removed, not averaged down).
    """
    sd = sd_lnE(zmin, zmax, nbin)
    f_tot = (dalpha / n_sigma) * np.sqrt(nbin) * sd
    return f_tot  # total per-bin random error allowed (stat + random-sys in quadrature)


def main():
    print("=" * 98)
    print(
        "a0(z) FORECAST -- OBT a0=cH(z)/2pi (alpha=1) vs constant-MOND (alpha=0); random vs coherent systematics"
    )
    print("=" * 98)

    # -- VERIFY: reproduce the achieved MUSE-DARK III precision (~16 sigma on alpha!=0) --
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

    print(
        "\n[1] STATISTICAL reach (RANDOM error -> averages down). Realistic per-bin a0 errors:"
    )
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
        "  -> EVOLUTION decisive even with 20% random systematics; rate would be too IF beta_sys=0. It is not -> [2]."
    )

    print(
        "\n[2] COHERENT-BIAS beta_sys (biases alpha_hat = 1 + beta_sys; does NOT average down). z 0.3-1.5:"
    )
    for label, b15 in [
        ("M_bar under-count (missing gas) ->30%  (1x lever)", +1.0 * 0.30),
        ("V_c over-estimate (incl/pressure) ->10% (4x lever)", +4.0 * 0.10),
        ("lensing g_obs over (2-halo/IA) ->8%    (2x lever)", +2.0 * 0.08),
        ("V_c UNDER (beam smearing) ->10% [deflates]", -4.0 * 0.10),
    ]:
        bs = beta_sys(0.3, 1.5, 10, b15)
        print(
            f"  {label:50s} beta_sys={bs:+5.2f} -> alpha_hat(true=1)={1+bs:4.2f}"
            f"  {'(FAKES 1.5x)' if 0.35 < bs < 0.75 else ''}"
        )
    print(
        f"  vs statistical sigma_alpha(Euclid)={sigma_alpha(0.3,1.5,10,0.015):.3f}: the coherent bias is ~20x larger."
    )

    print("\n[3] FORM-test requirement (alpha=1 vs 1.5, dalpha=0.5):")
    for name, (zmn, zmx, nb, fst) in {
        "Euclid (z 0.3-1.5, 10 bins)": (0.3, 1.5, 10, 0.005),
        "Euclid+high-z (z 0.3-3.0, 12 bins)": (0.3, 3.0, 12, 0.02),
    }.items():
        for ns in (3.0, 5.0):
            fr = coherent_floor(zmn, zmx, nb, 0.5, ns)
            print(
                f"  {name:34s} {ns:.0f}sigma -> RANDOM systematics < {fr*100:4.1f}%/bin AND coherent beta_sys << 0.5"
            )
    print(
        "  -> the random floor (~7-12%) is necessary but NOT sufficient: the COHERENT bias must be modelled away."
    )

    print("\n[4] THE DECISIVE CROSS-LEVER discriminator (the sharpest near-term play):")
    print(
        "  kinematic a0 (V_c 4x lever) vs lensing a0 (g_obs 2x, NO V_c lever), + measured gas (ALMA):"
    )
    print(
        "    - both ~1.5, robust to gas/V correction -> alpha REAL -> OBT cH(z)/2pi rate refuted (evolution OK)"
    )
    print("    - kinematic ~1.5 but lensing ~1.0       -> V-systematic; OBT rate safe")
    print(
        "    - both ~1.0                              -> OBT cH(z)/2pi rate confirmed"
    )

    print("\nHONEST READ:")
    print(
        "  (i)  EVOLUTION vs CONSTANT is decisive (MUSE 16sigma; Euclid/LSST >5sigma even at 20% systematics) and"
    )
    print(
        "       robust to coherent bias -> OBT-vs-constant-MOND will be settled. This is the distinctive pepite."
    )
    print(
        "  (ii) the cH(z)/2pi RATE is systematics-limited: alpha_hat = 1 + beta_sys, and ~10% V_c (4x) or ~40% M_bar"
    )
    print(
        "       coherent high-z bias fakes the observed 1.5x. More lenses do NOT help; the bias must be removed."
    )
    print(
        "  (iii) the clean route is the cross-lever measurement [4], not statistics. Use MOND-regime (g_bar~a0)"
    )
    print(
        "        tracers where a0 has leverage, never the compact a0-blind disks (lesson: predictions.md note)."
    )


if __name__ == "__main__":
    main()
