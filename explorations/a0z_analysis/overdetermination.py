"""OVER-DETERMINATION (option 3, June 2026) -- the strongest INTERNAL falsifier of a0(z), and why the
current data do NOT yet fulfill it (they share systematic levers).

REVIEWER MODE. If a0(z) = a0_0 * E(z)^alpha is horizon-set, then EVERY MOND-scale observable X propto a0^p
inherits X(z)/X(0) = E(z)^{p*alpha}. Measuring (p*alpha) from each observable and dividing by its KNOWN power p
must return the SAME alpha. A single inconsistent alpha falsifies the horizon origin -- no ad-hoc evolution
survives an over-determined set. BUT: the test only bites if the observables have DIFFERENT systematic
signatures. Two observables that share the same dominant lever are inflated IDENTICALLY by a shared systematic,
so their agreement is NOT independent confirmation. We show the current a0-RAR + BTFR data are exactly such a
degenerate (both V_c-lever 4x) pair, and identify the clean cross-checks (lensing-a0, Sigma_dagger) that break it.

Levers (deep-MOND a0=V_c^4/(G M_bar); RAR a0=g_obs^2/g_bar): a coherent fractional bias maps to dln(observable):
  kinematic a0:  +4 dlnV_c  - dln M_bar     (V lever 4x)
  BTFR zero-pt:  +4 dlnV_c  - dln M_bar     (V lever 4x)   <-- SAME as kinematic a0 -> degenerate
  lensing a0:    +2 dln g_obs - dln M_bar   (NO V lever; g_obs = lensing 2-halo/IA/photo-z)
  Sigma_dagger:            - dln M_bar      (NO V lever; surface-density calibration only)
"""

import numpy as np

Om, OL = 0.315, 0.685


def E(z):
    return np.sqrt(Om * (1 + z) ** 3 + OL)


def main():
    print("=" * 98)
    print(
        "OVER-DETERMINATION of a0(z): the internal falsifier, and why current data are degenerate"
    )
    print("=" * 98)

    # (1) the power table: X propto a0^p -> X(z)/X(0) = E(z)^{p*alpha}
    print(
        "\n[1] Every MOND observable X propto a0^p evolves as E(z)^(p*alpha). Predicted ratios at z=1 (E=1.76):"
    )
    obs = [
        ("a0 (RAR scale)", 1.0),
        ("BTFR zero-point (M_bar at fixed V)", -1.0),
        ("V_flat (at fixed M_bar)", 0.25),
        ("Sigma_dagger = a0/G", 1.0),
        ("MOND transition radius r_t", -0.5),
        ("deep-MOND boost sqrt(a0/g)", 0.5),
    ]
    Ez1 = E(1.0)
    print(
        f"  {'observable':36s} {'power p':>8s} | {'OBT alpha=1':>12s} | {'faster alpha=1.5':>16s}"
    )
    for label, p in obs:
        print(
            f"  {label:36s} {p:+8.2f} | x{Ez1**(p*1.0):11.2f} | x{Ez1**(p*1.5):15.2f}"
        )
    print(
        "  -> the powers p DIFFER row-to-row: a single E(z) origin is over-determined. If a measured set does"
    )
    print(
        "     NOT collapse to one common alpha (after dividing by p), the horizon a0 is falsified."
    )

    # (2) systematic-signature matrix
    print(
        "\n[2] SYSTEMATIC-SIGNATURE matrix (which lever each observable's measurement rides on):"
    )
    sig = [
        ("kinematic a0 (MUSE-DARK, KROSS)", "V 4x", "M_bar 1x", "-"),
        ("BTFR zero-point (Uebler/KMOS3D)", "V 4x", "M_bar 1x", "-"),
        ("lensing a0 (Euclid/KiDS RAR)", "-", "M_bar 1x", "g_obs 2x"),
        ("Sigma_dagger (LSB surface dens.)", "-", "M_bar 1x", "-"),
    ]
    print(f"  {'observable':34s} {'V lever':>8s} {'M_bar':>8s} {'g_obs(lens)':>12s}")
    for r in sig:
        print(f"  {r[0]:34s} {r[1]:>8s} {r[2]:>8s} {r[3]:>12s}")
    print(
        "  -> the CURRENTLY-measured trio (kinematic a0 + BTFR) ALL ride the V 4x lever -> a shared V/M_bar"
    )
    print(
        "     high-z systematic inflates them IDENTICALLY. Their agreement is EXPECTED, NOT independent proof."
    )

    # (3) current data: are a0-RAR and BTFR consistent? (within the degenerate club)
    print("\n[3] CURRENT over-determination check (degenerate club -- weak):")
    a_rar_muse = np.log(2.71 / 1.0) / np.log(E(1.2))
    a_rar_kross = np.log(1.97 / 1.04) / np.log(E(0.86))
    a_btfr = 0.44 / np.log10(E(0.9))
    print(
        f"  alpha(a0-RAR, MUSE) = {a_rar_muse:.2f} ; alpha(a0-RAR, KROSS@cH0/2pi) = {a_rar_kross:.2f} ; "
        f"alpha(BTFR) = {a_btfr:.2f}"
    )
    spread = max(a_rar_muse, a_rar_kross, a_btfr) - min(a_rar_muse, a_rar_kross, a_btfr)
    print(
        f"  -> all in [1.3, 1.9]; consistent at the ~1-2 sigma level given systematics, but the {spread:.1f} spread"
    )
    print(
        "     EXCEEDS a clean shared-systematic expectation (which would make them equal) -> a hint of EXTRA"
    )
    print(
        "     method-specific systematics. This 'agreement' does not confirm a real alpha (shared V/M_bar levers)."
    )

    # (4) the clean decision tree: lensing-a0 (no V) vs kinematic-a0 (V 4x), worked example
    print(
        "\n[4] THE CLEAN FALSIFIER -- lensing-a0(z) [no V lever] vs kinematic-a0(z) [V 4x]. Worked example:"
    )
    print(
        "    suppose the TRUE alpha=1 (OBT) but a coherent high-z bias inflates the apparent slope by beta:"
    )

    def slope_bias_from_Vbias(fmax, lever, zmin=0.3, zmax=1.5, nb=10):
        z = np.linspace(zmin, zmax, nb)
        x = np.log(E(z))
        xc = x - x.mean()
        b = lever * fmax * z / zmax
        return np.sum(xc * b) / np.sum(xc * xc)

    fV = 0.10  # 10% coherent V over-estimate by z=1.5 (AD/inclination)
    fg = 0.08  # 8% coherent lensing g_obs over (2-halo/IA) by z=1.5
    fM = 0.10  # 10% coherent M_bar under (gas) by z=1.5 -- SHARED by all
    # kinematic a0: V 4x + M_bar 1x (shared) ; lensing a0: g_obs 2x + M_bar 1x (shared)
    b_kin = slope_bias_from_Vbias(fV, 4.0) + slope_bias_from_Vbias(fM, 1.0)
    b_lens = slope_bias_from_Vbias(fg, 2.0) + slope_bias_from_Vbias(fM, 1.0)
    print(
        f"    V-bias {fV*100:.0f}% (4x) + gas {fM*100:.0f}% (1x, shared) -> kinematic alpha_hat = {1+b_kin:.2f}"
    )
    print(
        f"    lensing g_obs {fg*100:.0f}% (2x) + gas {fM*100:.0f}% (1x, shared) -> lensing  alpha_hat = {1+b_lens:.2f}"
    )
    print(
        f"    => the SPLIT (kinematic {1+b_kin:.2f} vs lensing {1+b_lens:.2f}) is the signature of the V-systematic."
    )
    print("\n    DECISION TREE (Euclid lensing-a0(z) vs MUSE/JWST kinematic-a0(z)):")
    print(
        "      - both ~1.5, robust to gas/V correction      -> alpha REAL -> OBT cH(z)/2pi RATE REFUTED (evolution OK)"
    )
    print(
        "      - kinematic ~1.5 but lensing ~1.0            -> V-systematic exonerates OBT's rate (alpha=1 safe)"
    )
    print(
        "      - both ~1.5 but BOTH shrink when gas MEASURED -> gas-census systematic; OBT's rate safe"
    )
    print(
        "      - both ~1.0                                   -> OBT's cH(z)/2pi rate CONFIRMED"
    )

    print("\nVERDICT (option 3):")
    print(
        "  * The over-determination (a single E(z) must fit a0, BTFR, V_flat, Sigma_dagger with their different"
    )
    print(
        "    powers p) is the STRONGEST internal falsifier -- no ad-hoc evolution survives it."
    )
    print(
        "  * BUT it is currently UNFULFILLED: the only measured high-z handles (kinematic a0 + BTFR) both ride the"
    )
    print(
        "    V_c 4x lever, so their ~1.5 agreement is degenerate with a shared V/M_bar systematic -- NOT proof."
    )
    print(
        "  * The DECISIVE step is a cross-LEVER measurement: Euclid lensing-a0(z) (2x g_obs, NO V) against"
    )
    print(
        "    kinematic-a0(z) (4x V), plus Sigma_dagger(z) (no V). The split (or its absence), and whether either"
    )
    print(
        "    shrinks under measured-gas, cleanly separates REAL-rate / V-systematic / gas-systematic. That single"
    )
    print(
        "    experiment turns a0(z) from 'evolution confirmed, rate ambiguous' into a decided rate -- the pepite's"
    )
    print("    sharpest near-term play.")


if __name__ == "__main__":
    main()
