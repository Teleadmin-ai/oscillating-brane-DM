"""A-phase (V9.0 closure), June 2026 -- can a halo-free homogeneous a^-3 sector exist for OBT's CMB?

Romain's A, task (1): attack the closure wall (b) = the CMB BACKGROUND, conceptually.
Mode: reviewer/auditor, prudence BOTH ways. SELF-CORRECTION of the first pass: my first version tested
only "Weyl-only" and over-stated the wall as fatal. OBT has another homogeneous candidate (the radion
condensate), and the MOND-CMB tension has a KNOWN resolution (Skordis-Zlosnik 2021, AeST). The honest
picture is three scenarios, not one.

The CMB acoustic peaks need a homogeneous a^-3 matter component ~5x baryons (Omega_m h^2 ~ 0.143) so that
matter-radiation equality z_eq = Om h^2 / Or h^2 - 1 ~ 3400 and recombination (z~1090) is in the MATTER era.

  Scenario 1 -- Weyl as the background DM: FAILS. The projected Weyl E_munu is TRACELESS
    (Shiromizu-Maeda-Sasaki) => a homogeneous isotropic Weyl has w=1/3 (radiation, a^-4), NOT a^-3 matter.
    Om(matter)=Om_b only => z_eq~540 => recombination in the RADIATION era => grossly wrong peaks.

  Scenario 2 -- radion condensate as the background DM (a^-3, Gate 10 misalignment, Om_r h^2~0.12 at
    phi0=M_s): does z_eq FINE (a^-3 matter, right abundance). BUT Gate 11: the 0.36 eV condensate CLUSTERS
    into galaxy halos => breaks OBT's halo-free (MOND) galaxies. So it pays the CMB bill but breaks galaxies.
    => the real wall is not "no a^-3 background" but the a^-3 sector's GALACTIC CLUSTERING (the MOND-CMB tension).

  Scenario 3 -- AeST (Skordis-Zlosnik 2021, PRL 127, 161302): a relativistic-MOND scalar whose homogeneous
    energy density behaves as DUST (a^-3) -> fits the Planck CMB + matter power spectrum, WHILE giving MOND
    (halo-free) in galaxies. PROOF that the tension is SURMOUNTABLE by one field. OBT's concrete target:
    realize this in its bulk/radion sector (a shift-symmetric mode that is a^-3 dust cosmologically + MOND
    galactically) -- the Weyl is not it (a^-4), the massive radion condensate clusters (Gate 11).
"""

import numpy as np

Ogamma_h2 = 2.47e-5
Neff = 3.046
nu_factor = Neff * (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)
Or_h2 = Ogamma_h2 * (1.0 + nu_factor)

Ob_h2 = 0.0224  # Planck baryons
Or_cond_h2 = 0.120  # radion-condensate misalignment (Gate 10, ~0.12-0.13 at phi0=M_s)
z_rec = 1090.0


def z_eq(Om_h2):
    return Om_h2 / Or_h2 - 1.0


def era(ze):
    return (
        "MATTER (correct peaks)"
        if z_rec < ze
        else "RADIATION (wrong peaks + huge early ISW)"
    )


def main():
    print("=" * 78)
    print(
        "A/closure task (1): can a halo-free homogeneous a^-3 sector do OBT's CMB background?"
    )
    print("=" * 78)
    print(f"radiation Or h^2 = {Or_h2:.3e}; CMB needs Om h^2 ~ 0.143 for z_eq ~ 3400\n")

    # Scenario 1: Weyl-only (Weyl is a^-4 by tracelessness -> not matter)
    z1 = z_eq(Ob_h2)
    print(
        "[S1] Weyl as background DM (traceless -> a^-4, NOT a^-3 matter): matter = baryons only"
    )
    print(
        f"     Om h^2 = {Ob_h2:.3f} -> z_eq = {z1:.0f} -> recombination in the {era(z1)}  => FAILS\n"
    )

    # Scenario 2: radion condensate (a^-3) provides the background
    Om2 = Ob_h2 + Or_cond_h2
    z2 = z_eq(Om2)
    print(
        f"[S2] radion condensate (a^-3, Gate 10) Om_cond h^2 = {Or_cond_h2:.3f}: matter = baryons + condensate"
    )
    print(
        f"     Om h^2 = {Om2:.3f} -> z_eq = {z2:.0f} -> recombination in the {era(z2)}  => z_eq OK"
    )
    print(
        "     BUT Gate 11: the 0.36 eV condensate CLUSTERS into galaxy halos => breaks halo-free galaxies."
    )
    print(
        "     => the wall is the a^-3 sector's GALACTIC CLUSTERING, not the background per se (MOND-CMB tension)\n"
    )

    # Scenario 3: the known resolution
    print(
        "[S3] AeST (Skordis-Zlosnik 2021): one MOND scalar = a^-3 DUST cosmologically (fits Planck CMB)"
    )
    print(
        "     + MOND/halo-free in galaxies. PROOF the MOND-CMB tension is SURMOUNTABLE by a single field."
    )
    print(
        f"     a^-3 dust with Om h^2~{Or_cond_h2:.2f} gives z_eq={z_eq(Om2):.0f} AND stays halo-free galactically.\n"
    )

    print("VERDICT (self-corrected, both ways):")
    print(
        "  * The CMB is NOT a proven-fatal wall for OBT. My first pass (Weyl-only) over-stated it."
    )
    print(
        "  * Weyl alone CANNOT be the background DM (tracelessness -> a^-4); that part stands."
    )
    print(
        "  * The radion condensate (a^-3) CAN pay the z_eq/CMB-background bill -- but as-is it clusters"
    )
    print(
        "    into galaxy halos (Gate 11), the MOND-CMB tension. The wall is the CLUSTERING, not the background."
    )
    print(
        "  * The tension is SURMOUNTABLE: AeST (Skordis-Zlosnik 2021) is a^-3 dust + MOND + halo-free, CMB-OK."
    )
    print(
        "  * OBT's concrete A target: realize the AeST mechanism in its bulk -- a shift-symmetric radion/"
    )
    print(
        "    brane-bending mode that is a^-3 dust cosmologically AND MOND/halo-free galactically. The massive"
    )
    print(
        "    0.36 eV condensate is NOT it (clusters); the Weyl is NOT it (a^-4). Mapping unestablished = the work."
    )
    print(
        "  * Honest fallback if no such mode exists: OBT is a HYBRID (geometric galaxies/clusters + a"
    )
    print(
        "    homogeneous CMB sector), to be stated openly. Quantitative test = an MG-CMB Boltzmann solve (task 2)."
    )


if __name__ == "__main__":
    main()
