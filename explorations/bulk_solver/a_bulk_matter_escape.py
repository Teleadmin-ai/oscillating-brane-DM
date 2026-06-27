"""A (3)+qubit: Romain's intuition was RIGHT -- I over-stated the CMB wall by ignoring bulk MATTER (F_mu_nu).

Romain: 'did the qubit/bulk view omit an interaction with the CMB-dust question?' YES. Cherche le vrai,
both ways -> this CORRECTS my earlier analysis.

THE WALL I BUILT: the projected bulk WEYL E_mu_nu is traceless (Shiromizu-Maeda-Sasaki) -> a homogeneous
isotropic Weyl has w=1/3 -> a^-4 -> 'OBT has no homogeneous a^-3 -> can't do the CMB z_eq'.

WHAT I IGNORED: the Shiromizu-Maartens brane Einstein equation with BULK MATTER has a SECOND projection:
    G_mu_nu = -Lambda_4 h + 8piG T_brane + kappa5^4 pi_mu_nu - E_mu_nu + F_mu_nu
  - E_mu_nu = projected bulk WEYL: TRACELESS -> w=1/3 -> a^-4 ('dark radiation', the only term I used).
  - F_mu_nu = projected bulk MATTER stress (Maartens 2004), present iff there are bulk fields beyond gravity.
    F_mu_nu is NOT traceless: F^mu_mu = 2 kappa5^2 T_nn (the normal-normal bulk stress T_AB n^A n^B), nonzero
    for generic bulk matter -> its effective w is FREE -> the dark sector CAN be a^-3 (dust).

WEB-VERIFIED (the holographic dual, exactly Romain's qubit angle): 'the dark radiation from an AdS/CFT
interpretation is the thermalized dof of the CONFORMAL field theory' (-> a^-4) BUT 'if there are non-zero
bulk fields OTHER than the gravitational field, the dual theory is NOT conformal, and the effective EoS of
the GENERALIZED dark radiation can DEVIATE SIGNIFICANTLY from pure radiation' (hep-th/0509182, 'Generalized
Dark Radiation in Brane Cosmology'). So: conformal CFT = traceless Weyl = a^-4 (my wall); NON-conformal CFT
= bulk matter = F_mu_nu = w free = a^-3 possible. The geometric and holographic statements are the SAME, and
BOTH have the escape I missed.

OBT HAS bulk matter: the KS throat fluxes, the Goldberger-Wise stabilizing scalar, the LVS/CY form fields.
=> F_mu_nu != 0 -> OBT's homogeneous dark sector is E_mu_nu (a^-4) + F_mu_nu (can be a^-3), NOT a^-4 only.

CORRECTION: 'OBT structurally has no homogeneous a^-3' was OVER-STATED -- it ignored F_mu_nu. The z_eq wall
is ESCAPABLE via the bulk-matter projection. The deep open question SHRINKS to: does OBT's bulk matter give a
HALO-FREE a^-3 (the Khronon/MOND structure)? -- and that could now come FROM the bulk matter F_mu_nu (natural,
part of OBT's string setup), not an added 4D field. Romain's qubit/bulk intuition reopened A productively.
"""

import numpy as np


def w_dark(Omega_F_frac, w_F):
    """effective EoS of the dark sector E_mu_nu (w=1/3) + F_mu_nu (w=w_F), by energy fraction of F."""
    w_E = 1.0 / 3.0
    return (1.0 - Omega_F_frac) * w_E + Omega_F_frac * w_F


def scaling_exponent(w):
    """rho ~ a^{-3(1+w)}: w=1/3 -> a^-4 (radiation); w=0 -> a^-3 (dust)."""
    return -3.0 * (1.0 + w)


def main():
    print("=" * 80)
    print(
        "A (3)+qubit: the bulk-MATTER projection F_mu_nu escapes the traceless-Weyl a^-4 wall"
    )
    print("=" * 80)

    print(
        "\n[dark sector = E_mu_nu (traceless Weyl, w=1/3) + F_mu_nu (bulk matter, w free)]"
    )
    print(
        f"   pure Weyl (no bulk matter):      w_dark = {w_dark(0.0, 0.0):.2f} -> rho ~ a^{scaling_exponent(w_dark(0.0,0.0)):.1f}  (a^-4, my wall)"
    )
    for frac in (0.5, 0.9, 1.0):
        for wF, lab in [(0.0, "bulk dust")]:
            wd = w_dark(frac, wF)
            print(
                f"   +{frac*100:3.0f}% F_mu_nu ({lab}, w_F={wF}): w_dark = {wd:.2f} -> rho ~ a^{scaling_exponent(wd):.1f}"
            )
    print(
        "   => with bulk matter (w_F=0 dominating), the dark sector -> a^-3 (DUST) -> z_eq is REACHABLE."
    )
    print(
        "   (conformal CFT <-> traceless Weyl <-> a^-4; NON-conformal CFT <-> bulk matter <-> w free <-> a^-3)"
    )

    print("\nCORRECTION (cherche le vrai -- I was wrong about the ABSOLUTE wall):")
    print(
        "  * 'OBT has no homogeneous a^-3 (Weyl traceless -> a^-4)' counted ONLY the pure-gravity Weyl"
    )
    print(
        "    E_mu_nu and IGNORED the bulk-matter projection F_mu_nu. OBT HAS bulk matter (KS fluxes, GW"
    )
    print(
        "    scalar, form fields) -> F_mu_nu != 0 -> the homogeneous dark sector CAN be a^-3."
    )
    print(
        "  * the z_eq/CMB-background wall is therefore ESCAPABLE -- not absolute. Romain's qubit/bulk"
    )
    print("    intuition (a NON-conformal CFT) is exactly this escape, web-confirmed.")
    print("\nWHAT SURVIVES (the deep question, now smaller + more natural):")
    print(
        "  * the a^-3 is necessary BUT not sufficient: it must also be HALO-FREE in galaxies (the MOND-CMB"
    )
    print(
        "    tension / the Khronon structure). A normal bulk-matter F_mu_nu that is a^-3 will also cluster"
    )
    print(
        "    into galaxy halos unless it has the shift-symmetric k-essence (Khronon) structure."
    )
    print(
        "  * SO the open V9.0 question shrinks to: does OBT's BULK MATTER F_mu_nu realize a halo-free a^-3"
    )
    print(
        "    (Khronon-class)? -- a bulk solve with the KS/GW matter, MORE NATURAL than adding a 4D field."
    )
    print(
        "  * NOT yet established (needs the actual bulk-matter EoS + perturbations), but A is REOPENED:"
    )
    print(
        "    the dark sector is richer than the traceless Weyl, and the Khronon could be intrinsic to OBT."
    )


if __name__ == "__main__":
    main()
