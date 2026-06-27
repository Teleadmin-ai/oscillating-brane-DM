"""A-phase (V9.0 closure), task (1): the Goldstone-screened reformulation -- can the radion BE the AeST field?

Romain's (1): could OBT's radion be a MASSLESS, shift-symmetric scalar (AeST-class, halo-free a^-3 dust)
INSTEAD of a massive Goldberger-Wise radion, so OBT recovers a purely-geometric DM that also fits the CMB?

Decisive: NO. The radion is the extra-dimension MODULUS -- it sets the 4D Newton constant G and the particle
masses via the warp factor. That single fact traps it; both horns of the dichotomy fail:

  HORN A -- STABILIZED (massive, Goldberger-Wise m_phi=0.36 eV, the actual OBT radion): its a^-3 is the
    coherent-oscillation condensate, which CLUSTERS (de Broglie ~0.8 mm << kpc) -> galaxy halos (Gate 11)
    -> NOT AeST's halo-free dust. (Established in a_radion_aest.py; recomputed here for self-containedness.)

  HORN B -- ROLLING (massless, shift-symmetric, AeST-like): a cosmologically-significant rolling scalar
    has phidot ~ sqrt(rho_DM) ~ sqrt(Omega_DM) H_0 M_Pl, so it excurses Delta phi ~ sqrt(Omega_DM) M_Pl ~
    0.5 M_Pl over a Hubble time. The radion sets G via the warp (dlnG/dphi ~ O(1/M_Pl)), so Delta(lnG) ~ 0.5
    -> Gdot/G ~ 0.5 H_0 ~ 3.5e-11/yr, ~350x the lunar-laser-ranging bound |Gdot/G| < ~1e-13/yr -> RULED OUT
    (and only WORSE for a warp-enhanced coupling). The radion is NOT an independent AeST scalar that may
    roll freely; it is the modulus, and a rolling modulus varies the lab constants. (Consistent with the
    'Gdot/G trap' in CLAUDE.md: OBT's macroscopic G_eff(t) must live in the Weyl-coupling sector, NOT in a
    rolling modulus.)

DEEPER (the structural root): OBT's MOND is GEOMETRIC -- a0=cH/2pi from the Gibbons-Hawking horizon, mu(x)
from Gauss-Codazzi, the dark sector = the projected Weyl, which is a^-4 (traceless). AeST's MOND is a SCALAR
FIELD whose cosmology is a^-3 dust. The geometric origin (OBT's distinctive a0=cH/2pi) is exactly WHY OBT
cannot do AeST's one-field (MOND + a^-3 dust) trick: geometry gives a^-4, a scalar gives a^-3. To get AeST's
a^-3 dust OBT would have to REPLACE its geometric MOND with a scalar MOND (= become AeST, losing a0=cH/2pi)
or ADD a separate AeST-engineered field (= the hybrid). Neither is a free reformulation of the radion.

VERDICT: (1) FAILS. The hybrid is the honest default; 'DM is purely geometric' holds at galaxy/cluster
scales (OBT's strength) but NOT at the CMB, where an added homogeneous sector is required.
"""

import numpy as np

# --- HORN A: stabilized radion clusters (de Broglie) ---
hbar_c_eV_nm = 197.327
nm_per_kpc = 3.0857e19 * 1e9
c_kms = 3.0e5
m_radion = 0.36  # eV
v_gal = 200.0  # km/s
lam_dB_nm = hbar_c_eV_nm / (m_radion * v_gal / c_kms)

# --- HORN B: rolling radion varies G ---
H0_per_yr = 67.4 / 3.0857e19 * 3.156e7  # 67.4 km/s/Mpc -> /s -> /yr
LLR_bound = 1e-13  # |Gdot/G| < ~1e-13 /yr (lunar laser ranging, Hofmann & Mueller 2018)
Omega_DM = 0.26
# A scalar carrying Omega_DM as a^-3 dust has phidot ~ sqrt(rho_DM) ~ sqrt(Omega_DM) H_0 M_Pl, so its
# excursion over a Hubble time is Delta phi ~ phidot/H_0 ~ sqrt(Omega_DM) M_Pl ~ 0.5 M_Pl. The radion sets G
# via the warp (dlnG/dphi ~ O(1/M_Pl)) -> dlnG ~ sqrt(Omega_DM) ~ 0.5 -> Gdot/G ~ 0.5 H_0 (order of magnitude;
# >= this, since a warped/enhanced coupling only makes dlnG/dphi LARGER).
GdotG_rolling = np.sqrt(Omega_DM) * H0_per_yr


def main():
    print("=" * 78)
    print(
        "A/closure (1): can the radion BE the AeST field? (Goldstone-screened reformulation)"
    )
    print("=" * 78)

    print("\n[HORN A] STABILIZED radion (massive 0.36 eV) -> a^-3 condensate CLUSTERS:")
    print(
        f"   de Broglie at v={v_gal:.0f} km/s: lambda = {lam_dB_nm/1e6:.2f} mm = {lam_dB_nm/nm_per_kpc:.1e} kpc"
    )
    print(
        f"   lambda << kpc by {nm_per_kpc/lam_dB_nm:.0e}x -> clusters -> galaxy halos (Gate 11) -> NOT AeST halo-free."
    )

    print(
        "\n[HORN B] ROLLING radion (massless, AeST-like) -> varies G (the modulus sets the constants):"
    )
    print(
        "   carry Omega_DM as dust -> phidot ~ sqrt(Omega_DM) H_0 M_Pl -> Delta phi ~ sqrt(Omega_DM) M_Pl ~ 0.5 M_Pl"
    )
    print(
        f"   -> Delta(lnG) ~ 0.5 -> Gdot/G ~ 0.5 H_0 = {GdotG_rolling:.1e} /yr  vs  LLR bound {LLR_bound:.0e} /yr"
    )
    print(
        f"   -> {GdotG_rolling/LLR_bound:.0f}x over the bound -> RULED OUT (worse for a warp-enhanced coupling)."
    )

    print("\n[STRUCTURAL ROOT] OBT's MOND is GEOMETRIC, not a scalar field:")
    print(
        "   a0 = cH/2pi (Gibbons-Hawking horizon), mu(x) (Gauss-Codazzi), dark sector = projected Weyl ~ a^-4."
    )
    print(
        "   AeST's MOND is a SCALAR whose cosmology is a^-3 dust. Geometry -> a^-4; a scalar -> a^-3."
    )
    print(
        "   OBT's distinctive a0=cH/2pi is EXACTLY why it cannot do AeST's one-field (MOND + a^-3 dust) trick."
    )

    print("\nVERDICT: (1) FAILS -- the radion cannot be the AeST field.")
    print(
        "  * stabilized -> clusters (Horn A); rolling -> varies G, ruled out (Horn B). The modulus is trapped."
    )
    print(
        "  * to get AeST's a^-3 dust OBT must either REPLACE geometric MOND with scalar MOND (= become AeST,"
    )
    print(
        "    losing a0=cH/2pi), or ADD a separate AeST-engineered field (= the hybrid). No free reformulation."
    )
    print(
        "  * => the HYBRID is the honest default: geometric MOND/Weyl for galaxy+cluster scales (OBT's win),"
    )
    print(
        "    + an added homogeneous a^-3 sector for the CMB. 'DM is purely geometric' does NOT reach the CMB."
    )
    print(
        "  * silver lining: the galaxy/cluster geometric results (a0=cH/2pi, mu(x), sinc, Bullet, cluster"
    )
    print(
        "    two-scale) are UNAFFECTED -- the hybrid only concerns the cosmological background/CMB sector."
    )


if __name__ == "__main__":
    main()
