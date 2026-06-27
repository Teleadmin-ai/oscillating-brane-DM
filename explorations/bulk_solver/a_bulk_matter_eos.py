"""A (1) DEEP SOLVE (no faux facile): does OBT's BULK MATTER F_mu_nu realize a HALO-FREE a^-3 (Khronon-class)?

a_bulk_matter_escape.py showed bulk matter CAN give a^-3 in principle (the wall is not absolute). The deep,
heavy question (Romain: no easy falsehood): does OBT's ACTUAL bulk matter do it? The projected F_mu_nu EoS is
fixed by the bulk scalar's LAGRANGIAN TYPE, not its detailed profile, so this is decidable analytically:

  (A) POTENTIAL MINIMUM (stabilized, static): energy = vacuum energy -> w = -1 -> a^0 (Lambda). NOT a^-3.
  (B) MASSIVE COHERENT OSCILLATION (mass m, quadratic min): <w> = 0 -> a^-3 (dust), BUT it CLUSTERS on
      scales above its de Broglie lambda ~ hbar/(m v); for m >> ~1e-24 eV that is << galaxy -> HALOS.
  (C) SHIFT-SYMMETRIC k-ESSENCE (NON-canonical kinetic term = the MOND function; the Khronon/AeST): <w> = 0
      -> a^-3 AND halo-free (the MOND function screens galactic clustering). THIS is what the CMB needs.

THE DECISIVE STRUCTURAL POINT: type (C) requires a NON-CANONICAL kinetic term (the k-essence MOND function).
A CANONICAL scalar (standard kinetic + potential) can only be type (A) [potential minimum] or type (B)
[oscillation] -> never the halo-free Khronon. So the question reduces to: does OBT have a NON-CANONICAL
k-essence bulk field that is non-canonical AT LOW (d phi)^2 (the MOND regime)? Subtlety (no faux facile):
OBT's SCALAR matter is canonical there; AND the one non-canonical structure OBT does have -- the brane
DBI/Nambu-Goto action sqrt(1+(d phi)^2) -- is non-canonical at HIGH (d phi)^2 (relativistic brane motion)
but ~CANONICAL at the LOW (d phi)^2 MOND regime (DBI ~ 1 + Y/2 - Y^2/8..., NOT the MOND K(Y) ~ Y^{3/2} at
small Y) -> it is the WRONG non-canonical. And OBT's MOND itself is GEOMETRIC (Gauss-Codazzi), not a
k-essence Lagrangian. Mapping OBT's fields:
  GW scalar (canonical + potential): minimum -> (A) Lambda; displaced/motor -> (B) massive osc m=0.36 eV.
  KS throat fluxes (static): (A) Lambda/geometric.
  LVS/CY moduli (canonical, massive): (B). String axions (canonical kinetic + non-perturbative V): (B),
    fuzzy/cluster (a_verify_options).
  brane-bending DBI: non-canonical but HIGH-Y -> ~canonical at the MOND regime -> NOT the type-(C) MOND k-essence.
=> NO OBT field is the type-(C) LOW-Y MOND k-essence Khronon. The deep solve CONFIRMS: OBT's actual bulk
   matter CANNOT supply the halo-free a^-3. The F_mu_nu escape is real in PRINCIPLE but CLOSED for OBT's
   fields -> the hybrid (an ADDED or REFORMULATED k-essence Khronon-class field) stands, thoroughly checked
   (not asserted: the wall is not absolute, but OBT's existing fields cannot cross it).
"""

import numpy as np

hbar_c_eV_nm = 197.327
nm_per_kpc = 3.0857e19 * 1e9
c_kms = 3.0e5
v_gal = 200.0


def eos_and_scaling(scalar_type):
    """(w, scaling exponent n in rho~a^n) for the three bulk-scalar Lagrangian types."""
    if scalar_type == "A_potential_min":
        return -1.0, 0.0  # Lambda
    if scalar_type in ("B_massive_osc", "C_kessence"):
        return 0.0, -3.0  # dust
    raise ValueError(scalar_type)


def clusters_into_halos(m_eV):
    """a coherent massive scalar clusters on scales > de Broglie; compare to a galaxy (~10 kpc)."""
    lam_nm = hbar_c_eV_nm / (m_eV * v_gal / c_kms)
    return (
        lam_nm < 10.0 * nm_per_kpc,
        lam_nm / nm_per_kpc,
    )  # (clusters in a ~10 kpc galaxy?, lambda in kpc)


def main():
    print("=" * 82)
    print(
        "A (1) DEEP SOLVE: can OBT's actual bulk matter F_mu_nu be the halo-free a^-3 (Khronon)?"
    )
    print("=" * 82)

    print("\n[EoS by bulk-scalar Lagrangian type]")
    for t, lab in [
        ("A_potential_min", "potential minimum (static)"),
        ("B_massive_osc", "massive coherent oscillation"),
        ("C_kessence", "shift-symmetric k-essence (Khronon)"),
    ]:
        w, n = eos_and_scaling(t)
        print(
            f"   {lab:38s}: w={w:+.0f} -> rho ~ a^{n:.0f}"
            + ("  (Lambda, not a^-3)" if n == 0 else "  (a^-3 dust)")
        )

    print(
        "\n[clustering of a type-(B) massive oscillation: does it make galaxy halos? (galaxy ~10 kpc)]"
    )
    for m_eV, lab in [
        (0.36, "OBT radion/GW (motor)"),
        (1e-22, "canonical fuzzy"),
        (1e-24, "~galaxy threshold"),
        (1e-25, "halo-free regime"),
    ]:
        cl, lam_kpc = clusters_into_halos(m_eV)
        print(
            f"   m={m_eV:.0e} eV ({lab:22s}): de Broglie={lam_kpc:.1e} kpc -> {'CLUSTERS -> halos' if cl else 'halo-free'}"
        )
    print(
        "   => type (B) is halo-free only for m <~ 1e-24 eV (de Broglie > galaxy); OBT's fields are"
    )
    print("      >= 0.36 eV -> ~32 orders too heavy -> all CLUSTER into halos.")

    print(
        "\n[the decisive point: type (C) needs a kinetic term NON-CANONICAL at LOW (d phi)^2 (the MOND function)]"
    )
    print(
        "   canonical scalar -> only (A)/(B); brane DBI is non-canonical but at HIGH (d phi)^2, ~canonical at"
    )
    print(
        "   the low-acceleration MOND regime (wrong non-canonical); OBT's MOND is geometric, not k-essence."
    )
    print("   OBT's bulk fields, mapped:")
    rows = [
        (
            "GW scalar (canonical+V)",
            "min -> (A) Lambda; displaced -> (B) m=0.36 eV",
            "Lambda or clustering a^-3",
        ),
        ("KS throat fluxes (static)", "(A) Lambda/geometric", "Lambda, not a^-3"),
        ("LVS/CY moduli (canonical)", "(B) massive", "clustering a^-3"),
        (
            "string axions (canonical+npV)",
            "(B) fuzzy/massive",
            "clustering a^-3 (cored halos)",
        ),
        (
            "brane-bending (DBI)",
            "non-canonical but HIGH-Y, ~canonical at MOND",
            "not the low-Y MOND k-essence",
        ),
    ]
    for f, typ, fate in rows:
        print(f"     {f:32s} {typ:46s} -> {fate}")

    print("\nVERDICT (deep solve, both ways):")
    print(
        "  * F_mu_nu CAN be a^-3 in principle (the wall is NOT absolute -- a_bulk_matter_escape stands)."
    )
    print(
        "  * BUT a halo-free a^-3 needs type (C): a kinetic term non-canonical AT LOW (d phi)^2 (the MOND"
    )
    print(
        "    function), at the cosmological scale. OBT's scalar matter is canonical there -> (A)/(B); its one"
    )
    print(
        "    non-canonical structure (the brane DBI) is non-canonical at HIGH (d phi)^2, ~canonical at the MOND"
    )
    print(
        "    regime (wrong non-canonical); and OBT's MOND is GEOMETRIC, not k-essence. NONE is the type-(C)"
    )
    print(
        "    low-Y MOND k-essence Khronon. (Confirms a_obt_aest_content: no ~massless shift-symmetric k-essence.)"
    )
    print(
        "  * => OBT's ACTUAL bulk matter CANNOT supply the halo-free a^-3. The F_mu_nu escape is real in"
    )
    print(
        "    PRINCIPLE but CLOSED for OBT's fields. The hybrid (an ADDED/REFORMULATED k-essence Khronon-class"
    )
    print("    gravity field) stands -- now thoroughly checked, not asserted.")
    print(
        "  * the genuine V9.0 door (sharp, not rigorously closed): can a WARPED brane/flux DBI give a kinetic"
    )
    print(
        "    term non-canonical at LOW (d phi)^2 (a true MOND k-essence)? PROBABLY NOT -- the DBI non-canonical"
    )
    print(
        "    scale is the (warped) brane tension, ~32+ orders ABOVE a_0 ~ H_0 -- but the rigorous warped-DBI"
    )
    print(
        "    calculation is the honest next deep step (it would reformulate OBT's geometric MOND as a k-essence)."
    )


if __name__ == "__main__":
    main()
