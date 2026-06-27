"""A-phase (1) deep: does OBT's bulk NATURALLY contain the AeST/Khronon field content?

Romain's (1): AeST needs (i) a unit-timelike vector 'aether' + (ii) a noncanonical shift-symmetric scalar.
Does OBT already have them? Web-verified field content:
  * AeST (Skordis-Zlosnik 2021): unit-timelike vector A_mu + shift-symmetric k-essence scalar phi; the
    scalar 'evolves as shift-symmetric k-essence -> cosmological energy density similar to dust ~(1+z)^3'.
  * KHRONON route (Blanchet-Marsat 2011 arXiv:1205.0400; Blanchet 2024 JCAP11(2024)040): a SCALAR ALONE
    (a 'Khronon' = a dynamical preferred-time foliation) gives MOND galactically + 'agreement with the CMB
    anisotropies at linear cosmological scales'. => NO aether vector is required; a foliation scalar suffices.

OBT's natural fields: metric; radion phi (scalar); brane normal n^mu (SPACELIKE, the extra dim); E_mu_nu,
K_mu_nu (tensors); KK gravitons (massive); string axions/moduli (KS/LVS).

MAPPING:
  AETHER (unit-TIMELIKE vector): OBT's natural vector is the brane normal n^mu, which is SPACELIKE (extra-dim
    direction), not timelike. So OBT has no natural AeST aether -- BUT the Khronon route does not need one.
  KHRONON (preferred-time foliation scalar): OBT's radion DOES define a preferred time -- grad(phi) is a
    preferred-time direction (the cosmological/brane-proper time). So structurally the radion IS a khronon
    candidate. The catch is QUANTITATIVE + structural:
    - the Khronon/MOND scalar lives at the cosmological scale (~H_0 ~ 1e-33 eV; massless/Goldstone-like,
      its scale enters via the k-essence MOND function, not a mass);
    - OBT's radion is a HARD massive modulus, m_phi = 0.36 eV (Goldberger-Wise), ~32 orders heavier;
    - and the GW mass breaks the SHIFT SYMMETRY the khronon's k-essence (a^-3 dust) requires.
  => the radion is the right TYPE of object (a preferred-time scalar) but the WRONG field (32 orders too
     heavy, canonical+massive, not shift-symmetric k-essence).

VERDICT: OBT does NOT naturally contain the AeST/Khronon structure. The radion<->khronon analogy is
QUALITATIVE (both are preferred-time scalars) but QUANTITATIVELY wrong. A V9.0 extension needs a NEW
~massless (~H_0-scale) shift-symmetric khronon scalar -- NOT the radion, NOT the (spacelike) normal. The
aether-vector is not the obstacle (Khronon route avoids it); the radion's MASS is.
"""

import numpy as np

hbar_eV_s = 6.582e-16  # eV s
H0_per_s = 67.4 / 3.0857e19  # km/s/Mpc -> /s
m_khronon = hbar_eV_s * H0_per_s  # cosmological/MOND scale of a khronon-like field (eV)
m_radion = 0.36  # eV (Goldberger-Wise)


def main():
    print("=" * 80)
    print(
        "A/closure (1) deep: does OBT naturally contain the AeST/Khronon field content?"
    )
    print("=" * 80)

    print("\n[aether: unit-timelike vector]")
    print(
        "   AeST needs a unit-TIMELIKE vector A_mu. OBT's natural vector = the brane normal n^mu, which is"
    )
    print(
        "   SPACELIKE (the extra-dim direction) -> NOT the aether. BUT the Khronon route (Blanchet) needs"
    )
    print(
        "   NO vector -- a foliation scalar suffices -> the aether is not the real obstacle."
    )

    print("\n[khronon: preferred-time foliation scalar]")
    print(
        "   OBT's radion grad(phi) DOES define a preferred time -> structurally a khronon candidate."
    )
    print(
        f"   But the khronon/MOND scalar lives at the cosmological scale ~H_0 = {m_khronon:.1e} eV"
    )
    print(
        f"   (massless/Goldstone-like), whereas OBT's radion is m_phi = {m_radion} eV (Goldberger-Wise):"
    )
    print(
        f"   ratio = {m_radion/m_khronon:.1e} -> the radion is ~{np.log10(m_radion/m_khronon):.0f} ORDERS too heavy."
    )
    print(
        "   Plus the GW mass breaks the SHIFT SYMMETRY the khronon's k-essence (a^-3 dust) requires."
    )

    print("\nVERDICT: OBT does NOT naturally contain the AeST/Khronon structure.")
    print(
        "  * aether (timelike vector): absent (the normal is spacelike) -- but not needed (Khronon route)."
    )
    print(
        "  * khronon (preferred-time scalar): the radion is the right TYPE but the WRONG field --"
    )
    print(
        f"    ~{np.log10(m_radion/m_khronon):.0f} orders too heavy ({m_radion} eV vs ~H_0 ~ {m_khronon:.0e} eV), canonical+massive,"
    )
    print(
        "    not the shift-symmetric k-essence a khronon needs (GW mass breaks the shift symmetry)."
    )
    print(
        "  * => a V9.0 extension needs a NEW ~massless ~H_0-scale shift-symmetric khronon scalar, NOT the"
    )
    print(
        "    radion and NOT the (spacelike) normal. The radion<->khronon analogy is qualitative only."
    )
    print(
        "  * the aether-vector is NOT the obstacle (Khronon route avoids it); the radion's MASS is."
    )
    print(
        "  * consistent with a_radion_reformulation.py (the radion can't be the AeST field) + a_verify_options"
    )
    print(
        "    (every natural OBT field fails) -> the HYBRID/added-gravity-scalar conclusion is robust."
    )


if __name__ == "__main__":
    main()
