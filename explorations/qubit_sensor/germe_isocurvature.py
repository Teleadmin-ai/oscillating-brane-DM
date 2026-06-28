"""Seed 3 (V9.0, quarantined) — DIGGING the Omega_DM <-> r consilience: the ISOCURVATURE stress-test.

Romain: 'creuse la consilience Omega_DM <-> r'. Reviewer move: try to BREAK it first. The consilience
(germe_inflation.py) rests on phi0 ~ H_inf (a light radion random-walks during inflation). But a light
field present during inflation FLUCTUATES -> it sources CDM ISOCURVATURE, which Planck constrains hard
(beta_iso < 0.038). So the random-walk route is testable RIGHT NOW against existing CMB data.

THE TEST (standard axion-isocurvature, applied to the radion):
  S = delta(rho_DM)/rho_DM = 2 * delta_phi / phi0,  delta_phi = H_inf/2pi (de Sitter fluctuation).
  - RANDOM-WALK route (phi0 = (H_inf/2pi) sqrt(N_e), the consilience's premise):
      S = 2/sqrt(N_e) ~ 0.26  -- INDEPENDENT of H_inf -> P_S/P_zeta ~ (S/zeta)^2 ~ 3e7
      -> EXCLUDED by Planck (beta_iso<0.038) by ~9 orders. The NAIVE consilience (r~3e-5) is DEAD.
  - CLASSICAL route (phi0 = M_s a minimum-offset, NOT the random-walk): S = 2(H_inf/2pi)/M_s -> small
      ONLY if H_inf << M_s. Planck S < ~9e-6 forces H_inf < ~3e7 GeV (LOW-scale inflation)
      -> r < ~2e-14 (UNDETECTABLE), and phi0 is now H_inf-INDEPENDENT -> NO Omega_DM<->r link.

THE FLIP (the honest, cleaner result): the naive 'Omega_DM predicts r~3e-5' dies, but digging extracts
something BETTER and near-future-testable: **radion-misalignment DM REQUIRES low-scale inflation
(H_inf < 3e7 GeV) -> r UNDETECTABLE (<2e-14); a B-mode detection r >~ 1e-3 (CMB-S4 / LiteBIRD) would
EXCLUDE radion-misalignment DM.** And that DISCRIMINATES OBT's two DM pictures: the geometric-Weyl DM
(the main theory; abundance = bulk BC) makes NO such requirement, so a B-mode detection would FAVOR
geometric-Weyl over radion-misalignment.

NOT V8.2. Not in the PDF. 'code, don't plead': the isocurvature amplitudes, the Planck bound, the
implied H_inf and r are all computed + asserted. Reviewer honesty: the pretty consilience broke; the
honest residue is a sharper test.
"""

import numpy as np

N_EFOLDS = 60
A_S = 2.1e-9  # scalar amplitude (Planck)
ZETA = np.sqrt(A_S)  # adiabatic curvature rms ~ 4.6e-5
BETA_ISO = 0.038  # Planck 2018 CDM isocurvature fraction bound (95%, ~uncorrelated)
M_S = 1.19e12  # OBT string scale (GeV)
M_PL = 2.435e18  # reduced Planck mass (GeV)


def iso_power_ratio(s_rms):
    """Isocurvature-to-adiabatic POWER ratio P_S/P_zeta from the per-mode isocurvature amplitude S."""
    return (s_rms / ZETA) ** 2


def beta_to_power_ratio(beta):
    """beta_iso = P_S/(P_S+P_zeta) -> P_S/P_zeta."""
    return beta / (1 - beta)


def tensor_ratio(h_inf):
    return 2 * h_inf**2 / (np.pi**2 * A_S * M_PL**2)


def main():
    print("=" * 86)
    print(
        " DIGGING Omega_DM <-> r : the ISOCURVATURE stress-test (try to break the consilience)"
    )
    print("=" * 86)

    allowed = beta_to_power_ratio(BETA_ISO)  # max allowed P_S/P_zeta
    s_max = ZETA * np.sqrt(allowed)  # max allowed isocurvature amplitude
    print(
        f"\n    Planck: beta_iso < {BETA_ISO} -> P_S/P_zeta < {allowed:.3f} -> S < {s_max:.1e}"
    )

    # [1] the RANDOM-WALK route (the consilience's premise) --------------------------
    print(
        "\n[1] RANDOM-WALK route (phi0 = (H_inf/2pi) sqrt(N_e) -- the basis of r~3e-5)"
    )
    s_rw = 2 / np.sqrt(N_EFOLDS)  # S = 2 delta_phi/phi0 = 2/sqrt(N_e), H-independent
    ratio_rw = iso_power_ratio(s_rw)
    print(f"    isocurvature S = 2/sqrt(N_e) = {s_rw:.3f}  (INDEPENDENT of H_inf)")
    print(
        f"    => P_S/P_zeta = {ratio_rw:.1e}  vs allowed {allowed:.3f}  -> EXCLUDED by ~{np.log10(ratio_rw/allowed):.0f} orders"
    )
    assert (
        ratio_rw > 1e6
    ), "the random-walk route must be grossly excluded by isocurvature"
    print(
        "    -> the NAIVE consilience (Omega_DM -> r~3e-5) is DEAD: its mechanism (random-walk phi0)"
    )
    print(
        "       over-produces CDM isocurvature by ~9 orders. Crossing fingers wasn't enough. :)"
    )

    # [2] the CLASSICAL route (the viable radion-DM) --------------------------------
    print(
        "\n[2] CLASSICAL route (phi0 = M_s minimum-offset, NOT random-walk) -- what survives"
    )
    # S = 2(H_inf/2pi)/M_s < s_max  ->  H_inf < s_max * pi * M_s
    h_inf_max = s_max * np.pi * M_S
    r_max = tensor_ratio(h_inf_max)
    print(
        f"    S = 2(H_inf/2pi)/M_s < {s_max:.1e}  ->  H_inf < {h_inf_max:.1e} GeV (LOW-scale inflation)"
    )
    print(
        f"    => r < {r_max:.1e}  (UNDETECTABLE; and phi0 is now H_inf-independent -> NO Omega_DM<->r link)"
    )
    assert h_inf_max < 1e8, "isocurvature must force low-scale inflation for radion-DM"
    assert r_max < 1e-13, "the surviving radion-DM must predict undetectable r"

    # [3] the FLIP -- the cleaner, testable result ----------------------------------
    print("\n[3] THE FLIP — the honest, sharper consilience")
    r_s4 = 1e-3  # CMB-S4 / LiteBIRD reach
    print(
        f"    radion-misalignment DM => r < {r_max:.0e} (undetectable). A B-mode detection r >~ {r_s4:.0e}"
    )
    print(
        f"    (CMB-S4 / LiteBIRD) would EXCLUDE radion-misalignment DM (it overshoots by ~{np.log10(r_s4/r_max):.0f} orders)."
    )
    assert (
        r_s4 / r_max > 1e9
    ), "a B-mode detection must cleanly exceed the radion-DM ceiling"
    print(
        "    -> NOT 'Omega_DM predicts r~3e-5' (that died), but the OPPOSITE + testable:"
    )
    print(
        "       radion-DM FORBIDS observable primordial B-modes. A detection kills it."
    )

    # [4] verdict -------------------------------------------------------------------
    print("\n[4] VERDICT — the consilience, dug")
    print(
        "    * The pretty form (Omega_DM -> r~3e-5) BROKE under isocurvature (random-walk phi0 excluded)."
    )
    print(
        "    * The honest residue is SHARPER + near-future-testable: radion-misalignment DM requires"
    )
    print(
        "      low-scale inflation (H_inf<3e7 GeV) -> r undetectable; a B-mode detection EXCLUDES it."
    )
    print(
        "    * It DISCRIMINATES OBT's two DM pictures: the geometric-Weyl DM (main theory, abundance ="
    )
    print(
        "      bulk BC, NOT a misaligned scalar) makes no such MISALIGNMENT-isocurvature requirement ->"
    )
    print(
        "      a B-mode detection would FAVOR geometric-Weyl. So r discriminates OBT's two DM mechanisms."
    )
    print(
        "    * Caveats: assumes radion-misalignment DM (vs geometric Weyl); quadratic potential;"
    )
    print("      uncorrelated isocurvature; standard single-field tensor relation.")

    print(
        "\n  ALL INJECTION TESTS PASSED (random-walk iso-excluded ~9 orders; radion-DM -> H<3e7 GeV, r<2e-14)."
    )
    print("=" * 86)


if __name__ == "__main__":
    main()
