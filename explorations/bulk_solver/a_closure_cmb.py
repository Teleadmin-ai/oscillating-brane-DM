"""A-phase (V9.0 closure), June 2026 -- the CMB-background obstruction to pure geometric (Weyl) DM.

Romain's A: can the inflation/holographic (it-from-qubit) route fix the closure datum (the DM amount)?
Auditor finding (test, don't glue): the inflation-entanglement thread (QUBIT_HOLOGRAPHY_NOTE.md) addresses
the PERTURBATION spectrum (the "bit", Gate 7 = the bulk dark-radiation primordial spectrum). But there is a
deeper, STRUCTURAL obstruction at the CMB BACKGROUND, forced by the tracelessness of the projected Weyl:

  Shiromizu-Maeda-Sasaki (2000): the brane-projected Weyl tensor E_munu is TRACELESS, E^mu_mu = 0.
  => a HOMOGENEOUS + ISOTROPIC Weyl has -rho + 3p = 0 -> p = rho/3 -> w = 1/3 = RADIATION (rho ~ a^-4),
     BBN-limited via Delta N_eff. There is NO homogeneous a^-3 (CDM-like) Weyl background, by symmetry.

  The CMB acoustic peaks need a homogeneous a^-3 matter component ~5x baryons (Omega_m h^2 ~ 0.143) so that
  matter-radiation equality sits at z_eq ~ 3400 and recombination (z ~ 1090) falls in the MATTER era
  (constant potentials -> the observed peak heights). The INHOMOGENEOUS Weyl (the geometric DM) is mean-zero
  -> contributes nothing to the background H(z) -> cannot move z_eq. So Weyl-only DM puts z_eq far too low.

This script quantifies that: it is structural, not a fitting detail. The inflation/holographic route does
NOT address it (it sets perturbations, not the background expansion).
"""

import numpy as np

# --- radiation density today (photons + 3.046 neutrinos) ---
Ogamma_h2 = 2.47e-5
Neff = 3.046
nu_factor = Neff * (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)
Or_h2 = Ogamma_h2 * (1.0 + nu_factor)

Ob_h2 = 0.0224  # Planck baryons
Om_h2_LCDM = 0.143  # Planck total matter (baryons + CDM)
z_rec = 1090.0  # recombination


def z_eq(Om_h2):
    return Om_h2 / Or_h2 - 1.0


def main():
    print("=" * 74)
    print("A/closure: the CMB-background obstruction to pure geometric (Weyl) DM")
    print("=" * 74)
    print(f"radiation Or h^2 = {Or_h2:.3e} (photons x {1+nu_factor:.3f} for nu)\n")

    print("[1] Tracelessness -> Weyl EoS (analytic, Shiromizu-Maeda-Sasaki):")
    print(
        "    E^mu_mu = 0, isotropic  =>  -rho_W + 3 p_W = 0  =>  w_W = p_W/rho_W = 1/3 = RADIATION (a^-4)."
    )
    print(
        "    => the homogeneous Weyl is dark radiation (BBN-limited), NOT a CDM-like (a^-3) background.\n"
    )

    zL, zO = z_eq(Om_h2_LCDM), z_eq(Ob_h2)
    print("[2] matter-radiation equality z_eq = Om h^2 / Or h^2 - 1:")
    print(f"    LCDM      (Om h^2 = {Om_h2_LCDM}) : z_eq = {zL:5.0f}   (Planck ~3400)")
    print(
        f"    Weyl-only (Om h^2 = Ob h^2 = {Ob_h2}) : z_eq = {zO:5.0f}   (baryons are the only homogeneous matter)"
    )
    print(f"    ratio = {zL/zO:.1f}x lower for Weyl-only.\n")

    print("[3] where does recombination (z_rec = 1090) fall?")
    for name, ze in [("LCDM", zL), ("Weyl-only", zO)]:
        era = (
            "MATTER (potentials ~const -> correct peaks)"
            if z_rec < ze
            else "RADIATION (potentials DECAY -> wrong peaks + huge early ISW)"
        )
        print(
            f"    {name:10s}: z_rec={z_rec:.0f} vs z_eq={ze:.0f}  ->  recombination in the {era}"
        )
    print()

    print("[4] what Weyl-only would need vs what it can give:")
    needed = Om_h2_LCDM - Ob_h2
    print(
        f"    CMB needs a homogeneous a^-3 component  Delta(Om h^2) = {needed:.3f}  (~{needed/Ob_h2:.1f}x baryons)."
    )
    print(
        f"    homogeneous Weyl can give: w=1/3 radiation, BBN cap ~0.1 x Or h^2 ~ {0.1*Or_h2:.1e} (a^-4) -> {needed/(0.1*Or_h2):.0e}x too little AND wrong scaling."
    )
    print(
        f"    inhomogeneous Weyl (geometric DM): mean = 0 by construction -> 0 contribution to background H(z)."
    )
    print(
        f"    quadratic backreaction <E_munu^2> ~ pi_munu term ~ 1e-40 (theory.md) -> negligible.\n"
    )

    print("VERDICT (auditor, both ways):")
    print(
        "  * pure geometric (Weyl) DM is STRUCTURALLY incompatible with the CMB background: tracelessness"
    )
    print(
        "    forbids a homogeneous a^-3 Weyl, so z_eq ~ 540 (not 3400) and recombination falls in the"
    )
    print(
        "    radiation era -> the acoustic peaks are grossly wrong. The inhomogeneous (geometric) DM is"
    )
    print(
        "    mean-zero and cannot move z_eq. This is DEEPER than the inflation-entanglement chain, which"
    )
    print("    sets the perturbation spectrum (the bit), NOT the background expansion.")
    print(
        "  * escapes: (a) radion condensate (a^-3, homogeneous) -> Gate 11 REFUSED (0.36 eV clusters into"
    )
    print(
        "    galaxy halos, kills the zero-halo MOND success); (b) a separate cold KK/particle component ->"
    )
    print(
        "    same galaxy-halo problem + dilutes 'DM is geometry'. So the CMB background is the real V9.0 wall."
    )
    print(
        "  * the qubit/holographic route RELOCATES the perturbation datum (CFT state <- inflation), but does"
    )
    print(
        "    not supply a homogeneous a^-3 background. A genuine resolution needs a NON-Weyl homogeneous"
    )
    print(
        "    sector for z_eq -- which is exactly what 'DM is purely geometric' tries to avoid. Honest tension."
    )


if __name__ == "__main__":
    main()
