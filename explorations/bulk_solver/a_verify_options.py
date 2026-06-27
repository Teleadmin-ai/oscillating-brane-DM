"""A-phase (1) follow-up: VERIFY the other closure escapes before defaulting to the hybrid.

Romain: 'verifie les autres options, cherche la verite' -- do not default to the hybrid; verify the escapes.
Three load-bearing facts WEB-VERIFIED (June 2026), plus a fuzzy-axion calc that closes the last escape.

WEB-VERIFIED FACT 1 -- modified gravity ALONE fails the CMB (the foundation holds):
  TeVeS / relativistic MOND without a dark-matter-like component cannot fit the CMB THIRD acoustic peak
  ('it is possible to produce as high a third peak ... without non-baryonic dark matter, but at the cost of
  unacceptably high ... ISW'; 'acceptable fits to the CMB in TeVeS still need to appeal to non-baryonic
  mass'). => OBT's GEOMETRIC MOND (a^-4 Weyl, no a^-3 dust) would fail the CMB the SAME way -> it genuinely
  needs a homogeneous a^-3 component. [physicsworld.com 'cosmic combat'; astroweb.case.edu/ssm/mond/CMB6.html]

WEB-VERIFIED FACT 2 -- the resolution exists, and it is a FIELD not a particle (AeST):
  Skordis & Zlosnik 2021 -- 'the time-dependent term behaves like gravitating dust, allowing AeST to
  reproduce the angular power spectrum of the CMB and the LCDM matter power spectrum on large scales, while
  retaining a MOND limit in galaxies'. So a SCALAR-TENSOR (gravity-sector) field supplies the a^-3 dust ->
  the added sector can stay GRAVITATIONAL (no WIMP). [aanda.org AeST; OUP MNRAS 531/272; tritonstation]

WEB-VERIFIED FACT 3 -- a string/fuzzy axion is NOT halo-free (the escape I dismissed too fast):
  fuzzy/ultralight-axion DM 'produces flat halo CORES ... forms large core-like structures' -- it CLUSTERS
  (cored halos), it is NOT halo-free. [ar5iv 1609.09414; aanda fuzzy-DM dwarf rotation curves]
  Quantified below: to be ALL the DM it needs m_a > ~1e-21 eV (Lyman-alpha/structure); at that mass its
  de Broglie core is ~10 pc << galaxy -> it makes galaxy halos -> DOUBLE-COUNTS with the MOND phantom ->
  breaks OBT's zero-halo galaxies. Halo-free would need m_a < ~1e-24 eV (de Broglie >= galaxy) -- ~3 orders
  below the all-DM floor, i.e. ruled out as all-DM. No overlap.

CONCLUSION (verified, not asserted): every NATURAL OBT field fails as the AeST a^-3 dust -- Weyl (a^-4),
massive radion (clusters, a_radion_aest.py), KK gravitons (massive -> cluster), string/fuzzy axion (cored
halos OR ruled out, below). The HYBRID is CONFIRMED. The nuance: its added sector can be an AeST-class
GRAVITY-SECTOR scalar (a field, not a particle), so 'DM is gravitational' survives -- but it is NOT realized
by OBT V8.2's existing fields, so a V9.0 EXTENSION (a new gravity scalar) is required.
"""

import numpy as np

hbar_c_eV_nm = 197.327
pc_nm = 3.086e16 * 1e9  # 1 pc in nm
c_kms = 3.0e5
v_gal = 200.0
galaxy_halo_nm = 1e4 * pc_nm  # ~10 kpc, galactic halo scale


def de_broglie_pc(m_eV, v_kms):
    return hbar_c_eV_nm / (m_eV * v_kms / c_kms) / pc_nm


def main():
    print("=" * 80)
    print(
        "A/closure (1) follow-up: verify the escapes -- can ANY natural OBT field do the CMB dust?"
    )
    print("=" * 80)

    print(
        "\n[escape: string/fuzzy axion] viable all-DM mass vs the halo-free requirement:"
    )
    for m_a, lab in [
        (1e-21, "Lyman-alpha all-DM floor"),
        (1e-22, "canonical fuzzy"),
        (1e-24, "~galaxy de Broglie"),
        (1e-25, "halo-free needs"),
    ]:
        lam_pc = de_broglie_pc(m_a, v_gal)
        verdict = (
            "<< galaxy -> CORED HALO (double-counts MOND)"
            if lam_pc * pc_nm < galaxy_halo_nm
            else ">= galaxy -> halo-free BUT ruled out as all-DM"
        )
        print(
            f"   m_a={m_a:.0e} eV ({lab:22s}): de Broglie ~ {lam_pc:8.1f} pc -> {verdict}"
        )
    m_halofree = (
        hbar_c_eV_nm / galaxy_halo_nm * (c_kms / v_gal)
    )  # m s.t. de Broglie = 10 kpc
    print(
        f"   => all-DM floor m_a>~1e-21 eV vs halo-free m_a<~{m_halofree:.0e} eV: a ~{np.log10(1e-21/m_halofree):.0f}-order GAP"
    )
    print(
        "   => NO viable fuzzy axion is both all-DM AND halo-free -> the string-axion escape FAILS."
    )

    print("\n[escape table] every natural OBT field as the AeST a^-3 CMB dust:")
    rows = [
        (
            "projected Weyl E_munu",
            "a^-4 (traceless, Shiromizu-Maeda-Sasaki)",
            "NOT a^-3 -> no z_eq",
        ),
        (
            "radion (massive 0.36 eV)",
            "a^-3 condensate but de Broglie ~0.8 mm",
            "CLUSTERS -> galaxy halos",
        ),
        (
            "radion (rolling, massless)",
            "would carry dust but it is the modulus",
            "varies G ~350x LLR -> ruled out",
        ),
        ("KK gravitons (eV)", "massive", "CLUSTER -> galaxy halos"),
        (
            "string/fuzzy axion",
            "a^-3 dust",
            "CORED halos (above) or ruled out as all-DM",
        ),
    ]
    for f, prop, fate in rows:
        print(f"   {f:28s} {prop:42s} -> {fate}")

    print("\nVERDICT (verified, both ways -- 'cherche la verite'):")
    print(
        "  * FACT 1 (web): MOND-alone fails the CMB 3rd peak -> OBT genuinely needs a homogeneous a^-3 dust."
    )
    print(
        "  * FACT 3 (web+calc): a fuzzy axion is NOT halo-free (cored halos; all-DM floor and halo-free"
    )
    print(
        "    threshold are ~3 orders apart) -> the natural-string-field escape FAILS."
    )
    print(
        "  * every natural OBT field fails (table) -> the HYBRID is CONFIRMED, not a lazy default."
    )
    print(
        "  * FACT 2 (web): the resolution (AeST) is a SCALAR-TENSOR field, so the added sector can stay"
    )
    print(
        "    GRAVITATIONAL (no WIMP). 'DM is gravitational/geometric' SURVIVES -- but OBT V8.2's current"
    )
    print(
        "    fields do not realize it; a V9.0 extension (a new AeST-class gravity scalar) is required."
    )
    print(
        "  * UNAFFECTED: the galaxy/cluster geometric wins (a0=cH/2pi, mu(x), sinc, Bullet, two-scale)."
    )


if __name__ == "__main__":
    main()
