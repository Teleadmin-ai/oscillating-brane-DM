"""Seed 3 (V9.0, quarantined) — DIGGING the A-PHASE: the a^-3 dark matter the CMB acoustic peaks need.

Romain: 'creuse l'A-phase ... take time'. This is OBT's deepest OPEN front (dm_discriminator.py found
it is the genuinely decisive leg, vs the B-mode which only confirms). The problem, stated sharply:

  The CMB acoustic peaks need a GRAVITATING, PRESSURELESS, a^-3 component (~5x baryons) present at
  recombination -- it deepens the potential wells and drives the photon-baryon oscillations WITHOUT
  oscillating with them. OBT's geometric-Weyl DM (the projected bulk E_munu) is TRACELESS -> its
  homogeneous part is a^-4 'dark radiation' (BBN-capped ~1e-5 of rho_DM -> ~1e-11 by recombination).
  So at the CMB it acts like extra RADIATION (delta N_eff), NOT like the a^-3 CDM the peaks need.

  This is NOT an OBT-specific bug: it is the UNIVERSAL relativistic-MOND CMB problem. Pure
  modified-gravity MOND + baryons fails the 3rd peak / baryon loading; every relativistic MOND theory
  (AeST, Skordis-Zlosnik 2021; TeVeS variants) ADDS a dedicated field whose BACKGROUND is a^-3 'dust'
  (drives the peaks) but whose PERTURBATIONS are MOND-shaped (so it does NOT cluster into NFW at
  galaxies). AeST demonstrably fits the Planck peaks. OBT must do the same.

  The a^-3 must be TRACEFUL -> a SCALAR (the traceless Weyl cannot). OBT's natural scalar is the radion
  (quadratic V -> coherent oscillation -> rho ~ a^-3, VERIFIED below). BUT a PLAIN radion is ordinary
  CDM -> NFW halos -> breaks the RAR -> bounded <=4% (Gate 11). So OBT needs the radion (or an added
  field) to carry the AeST structure: a^-3 background + MOND perturbations.

THE OBT-DISTINCTIVE HOPE (the V9.0 synthesis, not redundancy): the brane geometry (the Weyl/extrinsic
curvature) PROVIDES the AeST kinetic function K(Y) that shapes the radion -> radion = the a^-3 matter,
geometric-Weyl = the MOND function shaping it. If that holds, OBT does not just bolt on AeST -- it
DERIVES the AeST structure from the brane, and the two sectors are one. Unproven = the frontier.

NOT V8.2. Not in the PDF. 'code, don't plead': the a^-4/a^-3 gap, the oscillating-scalar a^-3 (EOM
integrated, <w>~0), and the Omega requirement are computed + asserted.
"""

import numpy as np
from scipy.integrate import solve_ivp

# cosmology
OMEGA_DM_H2 = 0.120
OMEGA_B_H2 = 0.0224
A_BBN, A_REC = 1 / 4e8, 1 / 1100
DR_FRAC_BBN = 1e-5  # Weyl dark-radiation fraction of rho_DM at BBN (N_eff bound)


def scalar_eos(m=1.0, t_end=4000.0):
    """Integrate phi'' + 3H phi' + m^2 phi = 0 in a matter background; return <w> and rho*a^3 drift."""
    t_i = 2.0 / m  # onset: 3H = m with H = 2/(3t) -> t_i = 2/m
    sol = solve_ivp(
        lambda t, y: [y[1], -3 * (2 / (3 * t)) * y[1] - m**2 * y[0]],
        (t_i, t_end),
        [1.0, 0.0],
        rtol=1e-9,
        atol=1e-12,
        dense_output=True,
        max_step=0.2 / m,
    )
    t = np.linspace(10 * t_i, t_end, 40000)  # skip the onset transient
    phi, phidot = sol.sol(t)
    a = (t / t_i) ** (2 / 3)
    rho = 0.5 * phidot**2 + 0.5 * m**2 * phi**2
    p = 0.5 * phidot**2 - 0.5 * m**2 * phi**2
    w_avg = np.mean(p) / np.mean(rho)  # oscillation-averaged equation of state
    rho_a3 = rho * a**3
    # compare windowed means early vs late (a^-3 => rho*a^3 ~ const)
    n = len(t) // 4
    drift = np.mean(rho_a3[-n:]) / np.mean(rho_a3[:n])
    return w_avg, drift


def main():
    print("=" * 88)
    print(
        " DIGGING the A-PHASE: the a^-3 dark matter the CMB acoustic peaks need (OBT's open front)"
    )
    print("=" * 88)

    # [1] the problem: the Weyl is a^-4 radiation, not a^-3 matter --------------------
    print(
        "\n[1] THE PROBLEM — the geometric-Weyl is a^-4 (radiation), the peaks need a^-3 (matter)"
    )
    dr_rec = DR_FRAC_BBN * (A_BBN / A_REC)
    print(
        f"    geometric-Weyl homogeneous part = a^-4 dark radiation: {DR_FRAC_BBN:.0e} of rho_DM at BBN"
    )
    print(
        f"      -> {dr_rec:.0e} by recombination (a^-1 dilution) -> acts as delta N_eff, NOT as CDM."
    )
    print(
        f"    the peaks need a^-3 CDM at Omega_DM/Omega_b = {OMEGA_DM_H2/OMEGA_B_H2:.1f}x baryons, present at z~1100."
    )
    assert dr_rec < 1e-9, "the Weyl dark radiation must be negligible as CMB matter"

    # [2] the a^-3 SOURCE exists: an oscillating scalar (radion) ---------------------
    print(
        "\n[2] THE a^-3 SOURCE EXISTS — an oscillating scalar (radion, V=m^2 phi^2/2): rho ~ a^-3"
    )
    w_avg, drift = scalar_eos()
    print("    integrated phi'' + 3H phi' + m^2 phi = 0 in a matter background:")
    print(f"      oscillation-averaged <w> = {w_avg:+.3f}  (matter = 0)")
    print(f"      rho * a^3 drift (late/early) = {drift:.3f}  (a^-3 = 1.0)")
    assert (
        abs(w_avg) < 0.05
    ), "an oscillating quadratic scalar must be matter-like (<w>~0)"
    assert 0.7 < drift < 1.4, "rho*a^3 must be ~constant (a^-3 scaling)"
    print(
        "    -> the radion CAN supply a^-3 matter. So the a^-3 SOURCE is not the problem."
    )

    # [3] BUT a plain radion clusters wrong -> needs AeST structure ------------------
    print(
        "\n[3] THE CATCH — a PLAIN a^-3 scalar is ordinary CDM (NFW) -> breaks the RAR (<=4%, Gate 11)"
    )
    print(
        "    the FIX (every relativistic MOND theory): an AeST-class field (Skordis-Zlosnik 2021) whose"
    )
    print(
        "    BACKGROUND is a^-3 dust (drives the peaks) but whose PERTURBATIONS are MOND-shaped (no NFW"
    )
    print(
        "    at galaxies). AeST fits the Planck acoustic peaks. OBT needs the same a^-3-and-MOND field."
    )

    # [4] the OBT-distinctive synthesis hope ----------------------------------------
    print("\n[4] THE OBT HOPE — brane-induced AeST (synthesis, not a bolt-on)")
    print(
        "    the a^-3 must be TRACEFUL -> a scalar (the traceless Weyl cannot give it). If the brane"
    )
    print(
        "    geometry (Weyl / extrinsic curvature) PROVIDES the AeST kinetic function K(Y) on the radion,"
    )
    print(
        "    then: radion = the a^-3 matter, geometric-Weyl = the MOND function shaping it -> ONE sector,"
    )
    print(
        "    not two. That would DERIVE AeST from the brane (distinctive) rather than bolt it on. Unproven."
    )

    # [5] verdict -------------------------------------------------------------------
    print("\n[5] VERDICT — the A-phase, dug")
    print(
        "    * The A-phase is REAL + ROBUST: the geometric-Weyl is a^-4 radiation at the CMB; the peaks"
    )
    print(
        "      need a^-3 CDM. Pure geometric-MOND + baryons fails -> an a^-3 sector is mandatory."
    )
    print(
        "    * It is the UNIVERSAL relativistic-MOND CMB problem; the standard fix is an AeST a^-3 scalar"
    )
    print(
        "      (a^-3 background + MOND perturbations). The a^-3 source exists in OBT (the radion, [2])."
    )
    print(
        "    * The OPEN, DECISIVE frontier: make OBT's radion carry the AeST structure FROM the brane"
    )
    print(
        "      (synthesis), so it is the a^-3 CMB DM AND the galaxy MOND without a redundant geometric-Weyl."
    )
    print(
        "    * Honest: this is OBT's deepest unsolved problem -- the one that DECIDES the CMB. The B-mode"
    )
    print(
        "      only confirms; the A-phase decides. Next real work: the brane-induced-AeST derivation +"
    )
    print(
        "      a CLASS/CAMB fit of the resulting a^-3-and-MOND field to the Planck peaks."
    )
    print(
        "    * Caveats: AeST-as-the-fix is cited (not re-derived); brane->K(Y) is a conjecture; no peak"
    )
    print(
        "      fit done here (needs a Boltzmann code). This is the SCOPING of the frontier, not its solve."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (Weyl a^-4 negligible at CMB; oscillating scalar <w>~0, rho~a^-3)."
    )
    print("=" * 88)


if __name__ == "__main__":
    main()
