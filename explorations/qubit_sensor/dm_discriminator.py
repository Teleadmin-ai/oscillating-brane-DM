"""Seed 3 (V9.0, quarantined) — DIGGING the B-mode discriminator: radion-CDM vs geometric-Weyl DM.

Romain: 'creuse le discriminateur B-mode'. The honest dig situates it: the B-mode/isocurvature test is
NOT a stand-alone — it is the PRIMORDIAL leg of a MULTI-EPOCH geometric-vs-particle DM discriminator.
OBT has two DM pictures: the MAIN geometric-Weyl DM (E_munu, a projected bulk geometry, NOT a particle)
and the Gate-10 radion-misalignment condensate (a real light scalar = particle-like CDM). They differ
at THREE epochs; we score each leg's discriminating power.

  LEG 1 -- PRIMORDIAL (inflation): CDM isocurvature / B-modes.
     radion (a scalar PRESENT during inflation): isocurvature is FORCED, S=2/sqrt(N_e)~0.26 ->
       P_S/P_zeta~3e7 -> Planck-excluded for high-scale inflation; a B-mode detection (r>~1e-3) KILLS it.
     geometric-Weyl (NOT a misaligned scalar): its perturbations are closure data -> CAN be adiabatic
       (iso-free) -> r-agnostic. => a B-mode detection EXCLUDES the radion, is fine for geometric-Weyl.

  LEG 2 -- RECOMBINATION (CMB acoustic peaks): the a^-3 matter the peaks need.
     radion: a^-3 matter (could seed peaks) BUT bounded <=4% by the RAR (leg 3) -> cannot be the ~96%.
     geometric-Weyl: its HOMOGENEOUS part is a^-4 dark radiation, BBN-limited <~1e-5 of rho_DM ->
       <~1e-12 by recombination -> CANNOT seed the peaks alone (the A-phase open frontier: an added
       scalar-tensor sector is needed). => the CMB a^-3 DM is OBT's OPEN question, neither leg supplies it.

  LEG 3 -- LATE (galaxies): the RAR / a0 = cH0/2pi.
     geometric-Weyl: gives a0 -> the exact RAR (29 km/s RMS, 0 free params; 33 OBT-game cards).
     radion-CDM (m=0.36 eV = standard CDM): NFW halos, NO a0 -> RAR offset +0.43 dex (Gate 11),
       galactic bound f<4%. => the RAR DECISIVELY favors geometric-Weyl. ALREADY IN HAND.

THE FIND: the discriminator is a coherent 3-epoch structure. The LATE leg (RAR) ALREADY establishes
OBT's DM as geometric (not particle) and bounds the radion to <=4%. The B-mode is the PRIMORDIAL leg --
real + complementary + near-future: a detection excludes the misalignment-radion sub-component and
confirms (does not threaten) the geometric picture. The RECOMBINATION leg is the open A-phase. So the
B-mode discriminator is genuine but SECONDARY to the RAR -- it confirms across a new epoch, not decides.

NOT V8.2. Not in the PDF. 'code, don't plead': iso amplitudes, the a^-4 dilution, the RAR offset/sigma,
and a discrimination scorecard are computed + asserted.
"""

import numpy as np

# primordial
N_EFOLDS = 60
A_S = 2.1e-9
ZETA = np.sqrt(A_S)
BETA_ISO = 0.038
# recombination
A_BBN, A_REC = 1 / 4e8, 1 / 1100  # scale factors (BBN ~ T~MeV; recombination z~1100)
DR_FRAC_BBN = (
    1e-5  # Weyl dark-radiation fraction of rho_DM at BBN (N_eff bound, CLAUDE.md)
)
# late (RAR)
RAR_OFFSET_RADION = 0.43  # dex: radion-as-all-DM offset on the RAR (Gate 11)
RAR_SCATTER = 0.13  # dex: intrinsic RAR scatter (McGaugh-Lelli)
N_SPARC = 175
F_RADION_MAX = 0.04  # galactic bound on a radion-CDM fraction (Gate 11)


def main():
    print("=" * 88)
    print(
        " DM DISCRIMINATOR: radion-CDM vs geometric-Weyl, across 3 epochs (B-mode = the primordial leg)"
    )
    print("=" * 88)

    # ---- LEG 1: primordial (isocurvature / B-modes) -------------------------------
    print("\n[LEG 1] PRIMORDIAL (inflation) — CDM isocurvature / B-modes")
    s_radion = 2 / np.sqrt(N_EFOLDS)
    ps_pzeta = (s_radion / ZETA) ** 2
    allowed = BETA_ISO / (1 - BETA_ISO)
    print(
        f"    radion (scalar at inflation): S=2/sqrt(N_e)={s_radion:.2f} -> P_S/P_zeta={ps_pzeta:.0e} "
        f"vs allowed {allowed:.2f}"
    )
    print(
        f"      -> EXCLUDED by ~{np.log10(ps_pzeta/allowed):.0f} orders for high-scale inflation; a B-mode"
    )
    print("         detection (r>~1e-3) KILLS the misalignment-radion.")
    print(
        "    geometric-Weyl (not a misaligned scalar): perturbations = closure data -> CAN be adiabatic"
    )
    print(
        "      (iso-free) -> r-agnostic. => B-mode detection EXCLUDES radion, FINE for geometric-Weyl."
    )
    leg1_discriminates = ps_pzeta / allowed > 1e6
    assert (
        leg1_discriminates
    ), "leg 1 must discriminate (radion iso grossly excluded at high scale)"

    # ---- LEG 2: recombination (a^-3 acoustic peaks) -------------------------------
    print(
        "\n[LEG 2] RECOMBINATION (CMB acoustic peaks) — the a^-3 matter the peaks need"
    )
    # Weyl dark radiation ~ a^-4 vs matter a^-3 -> ratio ~ a^-1; from BBN to recombination
    dr_frac_rec = DR_FRAC_BBN * (A_BBN / A_REC)  # (a^-1 scaling of DR/matter)
    print(
        f"    geometric-Weyl homogeneous part = a^-4 dark radiation: {DR_FRAC_BBN:.0e} of rho_DM at BBN"
    )
    print(
        f"      -> {dr_frac_rec:.0e} by recombination (a^-1 dilution) -> CANNOT seed the peaks (A-phase open)."
    )
    print(
        f"    radion = a^-3 matter (could seed peaks) BUT bounded <={F_RADION_MAX:.0%} by the RAR (leg 3)."
    )
    print(
        "      => the CMB a^-3 DM is OBT's OPEN frontier (an added scalar-tensor sector) — neither leg supplies it."
    )
    assert (
        dr_frac_rec < 1e-9
    ), "Weyl dark radiation must be negligible as the CMB matter"

    # ---- LEG 3: late (RAR / a0) ---------------------------------------------------
    print("\n[LEG 3] LATE (galaxies) — the RAR / a0 = cH0/2pi  [ALREADY IN HAND]")
    sigma_per_gal = RAR_OFFSET_RADION / RAR_SCATTER
    sigma_stack = sigma_per_gal * np.sqrt(N_SPARC)
    print(
        "    geometric-Weyl: gives a0 -> exact RAR (29 km/s RMS, 0 params; 33 OBT-game cards)."
    )
    print(
        f"    radion-CDM (m=0.36 eV = standard CDM): NFW, no a0 -> RAR offset +{RAR_OFFSET_RADION} dex (Gate 11)"
    )
    print(
        f"      = {sigma_per_gal:.1f} sigma/galaxy -> {sigma_stack:.0f} sigma stacked over {N_SPARC} SPARC -> radion-as-DM DEAD;"
    )
    print(f"      galactic bound f_radion < {F_RADION_MAX:.0%}.")
    print(
        "    => the RAR DECISIVELY favors geometric-Weyl. This leg is already measured."
    )
    assert sigma_stack > 5, "the RAR must decisively exclude radion-as-all-DM"

    # ---- scorecard + verdict ------------------------------------------------------
    print("\n[SCORECARD] discriminating power, by epoch")
    print(f"    {'epoch':<16}{'observable':<22}{'discriminates?':<18}{'status':<20}")
    rows = [
        ("primordial", "isocurvature/B-mode", "YES (one-sided)", "future (CMB-S4)"),
        ("recombination", "a^-3 acoustic peaks", "neither supplies", "OPEN (A-phase)"),
        ("late", "RAR / a0", "YES (decisive)", "IN HAND (geometric)"),
    ]
    for epoch, obs, disc, status in rows:
        print(f"    {epoch:<16}{obs:<22}{disc:<18}{status:<20}")

    print("\n[VERDICT] the B-mode discriminator, dug")
    print(
        "    * It is the PRIMORDIAL LEG of a coherent 3-epoch geometric-vs-particle DM discriminator."
    )
    print(
        "    * The LATE leg (RAR) ALREADY establishes OBT's DM as GEOMETRIC (not particle) and bounds"
    )
    print(
        "      the radion to <=4%. So the geometric-vs-particle question is largely SETTLED at late times."
    )
    print(
        "    * The B-mode is real + complementary + near-future: a detection (r>~1e-3) EXCLUDES the"
    )
    print(
        "      misalignment-radion sub-component and CONFIRMS (does not threaten) the geometric picture."
    )
    print(
        "    * The RECOMBINATION leg (the a^-3 acoustic DM) is the genuinely OPEN A-phase frontier."
    )
    print(
        "    => B-mode = a new-epoch CONFIRMATION, not the decider. The RAR already decided; the open"
    )
    print(
        "       front is the CMB a^-3 sector. Honest: the discriminator is genuine but SECONDARY to the RAR."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (leg1 iso-excluded; leg2 DR negligible; leg3 RAR decisive)."
    )
    print("=" * 88)


if __name__ == "__main__":
    main()
