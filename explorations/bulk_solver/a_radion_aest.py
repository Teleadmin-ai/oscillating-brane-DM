"""A-phase (V9.0 closure), June 2026 -- does OBT's MOND sector map to AeST? (the radion<->AeST mapping)

Task: the CMB-DM resolution exists (Skordis-Zlosnik 2021, AeST: a^-3 dust + MOND + halo-free, fits Planck).
Can OBT INHERIT it? AeST's halo-free a^-3 dust comes from a MASSLESS, SHIFT-SYMMETRIC scalar: the "dust"
is the conserved shift-charge density (J^0 ~ a^-3), NOT a massive-particle condensate: it is CDM-like on
large scales (sources the CMB/LSS) but in GALAXIES gives the MOND force (screened by the K(Y) MOND function),
NOT a clustered particle halo. The decisive question is whether OBT has such a mode.

OBT's light sector: (i) the radion -- MASSIVE (Goldberger-Wise, m_phi = 0.36 eV, required to stabilize the
extra dimension and set the KK spectrum); (ii) the projected Weyl -- a^-4 (traceless); (iii) KK gravitons --
massive (eV). NONE is a massless shift-symmetric scalar. The radion's a^-3 (its coherent oscillation = the
Gate-10 condensate) is an AXION-LIKE massive condensate -> it CLUSTERS (Gate 11), unlike AeST's shift-charge.

This script quantifies the decisive obstruction: a 0.36 eV scalar clusters on all scales far below a galaxy
(its de Broglie / fuzzy-Jeans scale is microscopic), so it forms halos -- it cannot be AeST's halo-free dust.
A halo-free (fuzzy) a^-3 component needs m ~ 1e-23 eV (de Broglie at v~200 km/s for ~kpc; the canonical
fuzzy-DM soliton value is ~1e-22 eV at dwarf velocities) -- the radion is ~22-23 orders too heavy. The radion
MASS (stabilization) is structurally incompatible with the AeST SHIFT SYMMETRY (halo-free dust).
"""

import numpy as np

hbar_c_eV_nm = 197.327  # eV nm
nm_per_kpc = 3.0857e19 * 1e9  # 1 kpc in nm (3.0857e19 m * 1e9 nm/m)
c = 3.0e5  # km/s
v_gal = 200.0  # km/s, galactic velocity scale


def de_broglie_nm(m_eV, v_kms):
    """coherent-scalar de Broglie wavelength lambda = hbar/(m v) = hbar c/(m v) (v in units of c)."""
    beta = v_kms / c
    return hbar_c_eV_nm / (m_eV * beta)


def m_for_lambda(lambda_nm, v_kms):
    """the mass whose de Broglie wavelength equals lambda_nm at v_kms (the fuzzy/halo-free threshold)."""
    beta = v_kms / c
    return hbar_c_eV_nm / (lambda_nm * beta)


def main():
    print("=" * 76)
    print(
        "A/closure: does OBT's radion map to the AeST halo-free a^-3 dust? (decisive test)"
    )
    print("=" * 76)
    print(
        "AeST halo-free a^-3 dust  <=>  a MASSLESS, SHIFT-SYMMETRIC scalar (dust = conserved shift-charge).\n"
    )

    m_radion = 0.36  # eV (Goldberger-Wise)
    lam = de_broglie_nm(m_radion, v_gal)
    print(
        f"[radion] m = {m_radion} eV (Goldberger-Wise; stabilizes the extra dim + sets the KK spectrum)"
    )
    print(
        f"         de Broglie at v={v_gal:.0f} km/s: lambda = {lam:.2e} nm = {lam/1e6:.2e} mm = {lam/nm_per_kpc:.1e} kpc"
    )
    print(
        f"         -> lambda << galaxy (~kpc) by {nm_per_kpc/lam:.0e}x  =>  clusters on ALL galactic scales => HALOS"
    )
    print(
        "         (= the Gate-11 result: the 0.36 eV condensate halos the galaxies, kills zero-halo MOND)\n"
    )

    m_fuzzy = m_for_lambda(nm_per_kpc, v_gal)
    print(
        f"[halo-free threshold] to stay smooth on ~kpc (fuzzy-DM), need m <~ {m_fuzzy:.1e} eV"
    )
    print(
        f"         the radion (0.36 eV) is ~{np.log10(m_radion/m_fuzzy):.0f} ORDERS too heavy -> cannot be halo-free.\n"
    )

    print(
        "[shift symmetry] AeST's dust is the conserved charge of a SHIFT-SYMMETRIC (massless) scalar."
    )
    print(
        "         OBT's radion has a MASS (Goldberger-Wise) -> NO shift symmetry -> no shift-charge dust;"
    )
    print(
        "         its a^-3 is instead a massive oscillation condensate -> clusters (above). Mass vs shift"
    )
    print(
        "         symmetry is the structural conflict: OBT needs the mass (stabilization), AeST needs it gone.\n"
    )

    print("VERDICT (decisive, both ways):")
    print(
        "  * OBT does NOT map to AeST as formulated. The decisive obstruction is part (B): OBT has no"
    )
    print(
        "    massless shift-symmetric scalar. Its only a^-3 candidate (the massive radion condensate)"
    )
    print(
        "    clusters into halos (de Broglie ~1 mm << kpc; ~22-23 orders above the fuzzy threshold),"
    )
    print(
        "    exactly the opposite of AeST's halo-free shift-charge dust. The Weyl is a^-4; the KK are massive."
    )
    print(
        "  * So OBT does NOT inherit AeST's CMB fit. The radion MASS (needed for stabilization + the KK"
    )
    print(
        "    spectrum) is structurally incompatible with the AeST shift symmetry (needed for halo-free dust)."
    )
    print(
        "  * Honest options: (i) a PRINCIPLED HYBRID -- add an AeST-class massless-screened scalar for the"
    )
    print(
        "    CMB background, keep the geometric Weyl for galaxy/cluster phenomenology (adds a field, but"
    )
    print(
        "    each sector does what it is good at); (ii) reformulate the radion sector (massless + MOND-"
    )
    print(
        "    screening instead of a hard Goldberger-Wise mass) -- a major change, conflicts with the KK"
    )
    print(
        "    spectrum + extra-dim stabilization; (iii) accept the CMB-DM as an open problem. The honest"
    )
    print(
        "    default is (i): OBT is NOT 'DM is purely geometric' at the CMB -- it needs a homogeneous sector."
    )


if __name__ == "__main__":
    main()
