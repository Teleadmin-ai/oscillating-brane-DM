"""A (1) STEP-BACK (Romain, before the full warped-DBI calc): is my ~32-order estimate far off? did I miss an
essential ingredient? why wouldn't the QUBIT link in too? cherche le vrai.

Romain's deep intuition: the bulk projects onto the brane, and WHAT it projects depends on the QUANTUM
WITNESSES of what it projects onto; maybe the warp has a QUANTUM impact, changing the brane's expression via
the qubit at the center of the bulk. -> step back before grinding the calculation.

CHECK 1 (quantitative -- is the estimate far off?): the warped-DBI non-canonical scale is the (warped) brane
tension ~ tau0^{1/3} = 257 MeV. To be a LOW-(dphi)^2 MOND k-essence it would have to sit at a0 ~ H0. Compute
the warp budget: how many e-folds kL does OBT have, vs how many are needed to bring 257 MeV (or M_Pl) down to
a0? If OBT's warp is far short, the full warped-DBI EoS is MOOT (the door is closed by the warp magnitude).

CHECK 2 (the qubit link -- Romain is right that it links): list the holographic/qubit routes and their fates.

CHECK 3 (the 'quantum witnesses' = state-dependent projection): identify which OBT mechanism this IS.
"""

import numpy as np

M_Pl_eV = 1.22e28  # Planck mass
E_QCD = 2.57e8  # tau0^{1/3} = 257 MeV (the KS-throat IR / brane scale), eV
H0_eV = 1.44e-33  # a0 ~ H0 scale, eV
m1_flat, m1_warped = (
    3.78,
    1.87,
)  # KK graviton mass (eV): flat-space vs warped (CLAUDE.md)


def main():
    print("=" * 84)
    print(
        "A (1) STEP-BACK: is the warped-DBI estimate far off? + the qubit link + quantum witnesses"
    )
    print("=" * 84)

    print("\n[CHECK 1] OBT's warp budget vs what reaching a0 would need:")
    kL_extra = np.log(
        m1_flat / m1_warped
    )  # the L=0.2um extra-dim warp (from the KK mass shift)
    kL_throat = np.log(M_Pl_eV / E_QCD)  # the KS throat: M_Pl -> 257 MeV
    kL_to_a0_from_QCD = np.log(E_QCD / H0_eV)  # 257 MeV -> a0
    kL_to_a0_total = np.log(M_Pl_eV / H0_eV)  # M_Pl -> a0
    print(
        f"   OBT extra-dim warp (m1 3.78->1.87 eV):  kL = {kL_extra:5.2f} e-folds (small, ~factor 2)"
    )
    print(f"   KS throat warp (M_Pl -> 257 MeV):        kL = {kL_throat:5.1f} e-folds")
    print(
        f"   OBT total warp budget:                   kL ~ {kL_extra + kL_throat:5.1f} e-folds"
    )
    print(
        f"   needed to reach a0 from 257 MeV:         kL = {kL_to_a0_from_QCD:5.1f}  ({kL_to_a0_from_QCD - kL_throat:.0f} MORE than OBT has)"
    )
    print(f"   needed to reach a0 from M_Pl:            kL = {kL_to_a0_total:5.1f}")
    short_orders = np.log10(E_QCD / H0_eV)
    print(
        f"   => the warp STOPS at 257 MeV; the warped-DBI scale is ~{short_orders:.0f} ORDERS above a0."
    )
    print(
        f"   => my ~32-order estimate is NOT far off (actually ~{short_orders:.0f}); the full warped-DBI EoS is MOOT"
    )
    print(
        f"      (OBT's warp budget {kL_extra + kL_throat:.0f} << the {kL_to_a0_total:.0f} e-folds a0 would need)."
    )

    print(
        "\n[CHECK 2] the qubit/holographic link (Romain is right it links) -- but every route hits the wall:"
    )
    routes = [
        (
            "E_mu_nu = <T_mu_nu>_CFT",
            "conformal CFT -> traceless -> a^-4",
            "the wall (not a^-3)",
        ),
        (
            "holographic RG / TTbar cutoff",
            "sqrt-deformation ~ DBI -> HIGH-(dphi)^2",
            "wrong non-canonical",
        ),
        (
            "entanglement -> emergent gravity",
            "a0 = cH/2pi (Verlinde/Gibbons-Hawking)",
            "MOND in galaxies, NOT CMB",
        ),
        (
            "CFT massless modes",
            "= the stress tensor -> graviton/Weyl",
            "a^-4, not a scalar Khronon",
        ),
        (
            "CFT scalar operators",
            "= radion / moduli (lifted, massive)",
            "type (B) cluster, not massless",
        ),
        (
            "KS-throat IR (confining)",
            "mass gap -> glueballs/KK ~ 257 MeV/eV",
            "massive, cluster",
        ),
    ]
    for r, what, fate in routes:
        print(f"   {r:32s} {what:42s} -> {fate}")
    print(
        "   => the qubit DOES link, but gives a^-4 / massive / DBI-high-Y / galaxy-MOND -- NEVER the massless"
    )
    print(
        "      low-(dphi)^2 a^-3 Khronon. No massless scalar emerges from the bulk entanglement (only the"
    )
    print("      graviton/Weyl is massless; every bulk scalar is GW/np-lifted).")

    print(
        "\n[CHECK 3] the 'quantum witnesses' (the projection depends on the brane's quantum state):"
    )
    print(
        "   This IS a real OBT mechanism -- it is exactly the GEOMETRIC-DM response: E_mu_nu responds to the"
    )
    print(
        "   brane matter distribution (state-dependent projection) -> the inhomogeneous Weyl = galaxy/cluster"
    )
    print(
        "   DM. But that is the RESPONSE (inhomogeneous), NOT the homogeneous CMB a^-3 BACKGROUND. So Romain's"
    )
    print(
        "   intuition strengthens the galaxy/cluster sector (already OBT's win), not the CMB-background gap."
    )

    print("\nVERDICT (step-back, cherche le vrai):")
    print(
        "  * estimate NOT far off: OBT's warp (~46 e-folds) stops at 257 MeV; a0 needs ~140 e-folds -> the"
    )
    print(
        f"    warped-DBI scale is ~{short_orders:.0f} orders above a0 -> the full warped-DBI EoS is MOOT (door closed by warp)."
    )
    print(
        "  * the qubit links (Romain right) but every holographic route hits the SAME wall (a^-4 / massive /"
    )
    print(
        "    DBI-high-Y / galaxy-MOND); no massless a^-3 Khronon emerges from the bulk entanglement."
    )
    print(
        "  * the 'quantum-witness' state-dependent projection IS the geometric-DM response (galaxies/clusters),"
    )
    print(
        "    not the homogeneous CMB a^-3 background -> it reinforces OBT's win, not the gap."
    )
    print(
        "  * => the hybrid stands at the DEEPEST level (classical warped-DBI moot + quantum/qubit walled). The"
    )
    print(
        "    missing a^-3 halo-free Khronon is genuinely absent from OBT's structure, classically AND quantumly."
    )
    print(
        "    Romain's intuitions were RIGHT (the qubit links; the projection is state-dependent) -- and chased"
    )
    print(
        "    to the end, they confirm rather than break the wall. No faux facile; the truth is the hybrid."
    )


if __name__ == "__main__":
    main()
