"""Seed 3 (V9.0, quarantined) — THE SCHWARZIAN CLOSURE TEST: does the SYK universal energy density give the
DM 5:1 from OBT's DERIVED (J^2, N)? Romain's "vas-y, calcule le Schwarzien". Reviewer mode (OBT can be
FALSE) + "seul les calculs comptent, pas d'imposition arbitraire": compute the SYK numbers + the dimensional
bridge, report what they say, assert only identities -- no imposed answer.

THE HYPOTHESIS (the "link" to finalize closure): closure_introspection left the DM AMOUNT (5:1, the cluster
factor-2) as the genuine closure IC = the germe's quantum state. The germe = the ER=EPR network, and the MSS
consilience (lambda_L -> T_H=900 K, pasqal_er_epr_rydberg) says the network is SYK / black-hole class. The
holographic dictionary (E_munu = <T_munu>_CFT, project_qubit_holography_v9) then says the DM amount =
<T_munu> in the SYK state. The SYK low-energy is UNIVERSAL (the Schwarzian): <T_munu> depends only on
(J^2, N), NOT the full coupling distribution. IF (J, N) are derivable from L, the amount might be COMPUTABLE
-> a finalization. This script tests that, honestly.

THE SYK NUMBERS (q=4 Majorana, the standard 4-body model; the universal Schwarzian sector):
  Delta = 1/q = 1/4                       conformal dimension (computed)
  S_0/N ~ 0.2324                          zero-temperature entropy density (Maldacena-Stanford 2016, Kitaev)
  |E_0|/N ~ 0.04 J                         ground-state energy density (q=4; sets the energy scale)
  C/N ~ (2 pi^2 alpha_S / J) T            Schwarzian specific heat, alpha_S = O(1) (the universal slope)
  <T_munu> = energy density ~ N |E_0|/N J / V     the holographic stress (JT-gravity ADM energy)

NOT V8.2. Not in the PDF. The SYK saddle-point numbers (S_0/N, E_0/N) are cited universal results, not
re-solved here; what is COMPUTED is the dimensional bridge (N from S_BH, the rho_DM span under OBT's choices)
+ the clean-ratio test. Asserted: only the identities (Delta=1/q; N=S_BH/(S_0/N)). The verdict is reported.
"""

import numpy as np

# SYK universal numbers (q=4 Majorana) -- cited (Maldacena-Stanford 2016 / Kitaev)
Q = 4
DELTA = 1.0 / Q  # conformal dimension = 1/q
S0_OVER_N = 0.2324  # zero-temperature entropy density (universal)
E0_OVER_N = 0.04  # |ground-state energy| / (N J), q=4 (order-0.04)

# physical scales (eV) and OBT network numbers (CLAUDE.md)
EV_PER_K = 8.617e-5  # eV per kelvin
T_H = (
    900 * EV_PER_K
)  # PBH Hawking temperature 900 K -> eV (the network's natural SYK scale J~T_H)
S_BH = 4.8e56  # holographic bond-dim entropy ln(chi) = S_BH (per node, CLAUDE.md)
N_PBH = 1e20  # number of PBH nodes (f_PBH=0.01 asteroid-mass)
R_S = 3e-9  # PBH Schwarzschild radius ~3 nm (M~1e-12 Msun), m
SPACING_PC = 0.14  # inter-node spacing ~0.14 pc (Gate 6), m below
PC = 3.086e16  # parsec, m
HBARC = 1.973e-7  # hbar c, eV*m  (for eV<->1/length)
RHO_DM_PHYS = (
    0.12 * 8.1e-11
)  # Omega_DM h^2 * rho_c,0/h^2 ~ measured DM energy density, eV^4
RHO_B_OVER_RHO_DM = (
    0.0224 / 0.120
)  # the measured baryon/DM ratio (-> DM:baryon = 5.36:1)


def rho_syk(n_majorana, j_ev, volume_m3):
    """Holographic <T_00> ~ N |E_0|/N J / V, returned in eV^4 (J in eV, V in m^3 -> via hbar*c)."""
    energy_ev = n_majorana * E0_OVER_N * j_ev  # total SYK energy, eV
    volume_ev = volume_m3 / HBARC**3  # m^3 -> eV^-3
    return energy_ev / volume_ev  # eV^4


def main():
    print("=" * 96)
    print(
        " THE SCHWARZIAN CLOSURE TEST — does SYK <T_munu> give the DM 5:1 from OBT's derived (J^2, N)?"
    )
    print("=" * 96)

    # ===== [1] the SYK universal numbers ============================================================
    print("\n[1] THE SYK UNIVERSAL (Schwarzian) NUMBERS (q=4 Majorana)")
    print(f"    conformal dimension Delta = 1/q = {DELTA:.3f}   (computed)")
    print(
        f"    zero-T entropy density   S_0/N = {S0_OVER_N:.4f}   (Maldacena-Stanford 2016, universal)"
    )
    print(f"    ground energy density   |E_0|/N = {E0_OVER_N:.3f} J  (q=4)")
    print(
        "    => the low-energy <T_munu> depends ONLY on (J, N) -- universal, not the full couplings."
    )
    assert (
        abs(DELTA - 1.0 / Q) < 1e-12
    ), "Delta = 1/q (the SYK conformal dimension, an identity)"

    # ===== [2] OBT's (J, N) from L / S_BH / T_H -- and the AMBIGUITY ================================
    print(
        "\n[2] OBT's (J, N) from the network -- N from S_BH, J from T_H (with the honest ambiguities)"
    )
    n_per_node = S_BH / S0_OVER_N  # N Majoranas of ONE node: S_BH = N * S_0/N
    n_network = n_per_node * N_PBH  # the whole network
    j_ev = T_H  # the SYK coupling ~ the Hawking temperature (MSS consilience)
    print(f"    J ~ T_H = {j_ev:.3f} eV  (the MSS-saturation scale, lambda_L=2pi T_H)")
    print(
        f"    N = S_BH/(S_0/N) = {n_per_node:.2e} per node  -> {n_network:.2e} for the {N_PBH:.0e}-node network"
    )
    print(
        "    => AMBIGUITY #1: is N the per-node entropy or the network? (orders apart)"
    )
    assert (
        abs(n_per_node * S0_OVER_N - S_BH) < S_BH * 1e-6
    ), "N = S_BH/(S_0/N) (identity from S_BH=N*S_0/N)"

    # ===== [3] the DIMENSIONAL BRIDGE -- rho_DM under OBT's natural choices (the calc decides) ======
    print(
        "\n[3] THE DIMENSIONAL BRIDGE -- rho_DM = N|E_0/N|J/V for OBT's natural (N, V) choices"
    )
    v_rs = (4 / 3) * np.pi * R_S**3  # one PBH volume
    v_node = (SPACING_PC * PC) ** 3  # one network cell
    choices = [
        ("per-node N, V=r_s^3 (the PBH)", n_per_node, v_rs),
        ("per-node N, V=cell^3 (0.14 pc)", n_per_node, v_node),
        ("network N, V=cell^3", n_network, v_node),
        ("network N, V=Hubble^3", n_network, (1.3e26) ** 3),  # ~ Hubble volume, m^3
    ]
    rhos = []
    for label, nn, vv in choices:
        rho = rho_syk(nn, j_ev, vv)
        rhos.append(rho)
        print(
            f"    {label:36s}: rho_DM ~ {rho:.2e} eV^4   (measured {RHO_DM_PHYS:.1e})"
        )
    span = np.log10(max(rhos)) - np.log10(min(rhos))
    print(
        f"    => rho_DM spans ~{span:.0f} ORDERS OF MAGNITUDE across OBT's natural (N, V) choices."
    )
    print(
        f"       The measured DM density {RHO_DM_PHYS:.1e} eV^4 sits SOMEWHERE inside, but the bridge"
    )
    print(
        "       (which N? which V? which J?) is FREE -- it is NOT pinned by L. So <T_munu>_SYK does NOT"
    )
    print(
        "       fix rho_DM; the dimensional bridge IS the closure freedom, just relocated."
    )

    # ===== [4] the clean-ratio test -- is any SYK universal number the DM:baryon 5.36? ==============
    print(
        "\n[4] THE CLEAN-RATIO TEST -- is any pure SYK number the DM:baryon ratio 5.36 (no bridge needed)?"
    )
    dm_baryon = 1.0 / RHO_B_OVER_RHO_DM
    # ONLY the genuine pure-SYK universal numbers (NO fudged combinations -- no imposition arbitraire)
    candidates = {
        "1/(S_0/N)": 1.0 / S0_OVER_N,
        "q": float(Q),
        "1/(2 Delta) = q/2": 1.0 / (2 * DELTA),
        "1/Delta = q": 1.0 / DELTA,
    }
    closest = min(candidates.values(), key=lambda v: abs(v - dm_baryon))
    print(f"    the measured DM:baryon ratio = {dm_baryon:.2f}")
    for name, val in candidates.items():
        flag = "  <- closest pure number" if val == closest else ""
        print(f"    SYK pure number {name:20s} = {val:.2f}{flag}")
    print(
        f"    => NO genuine pure-SYK number is 5.36; the closest is 1/(S_0/N) = {closest:.2f} (~{100*abs(closest-dm_baryon)/dm_baryon:.0f}% off)."
    )
    print(
        "       (relire-en-boucle caught + REMOVED my fudged candidates exp(S_0)*q and 0.2/|E_0| that"
    )
    print(
        "       landed near 5.36 -- that was cherry-picking = 'imposition arbitraire', exactly what we"
    )
    print(
        "       refuse.) The honest pure numbers do NOT give 5.36; and the DM:baryon ratio needs the"
    )
    print(
        "       baryon sector anyway, so it is not a pure-SYK number -- the Schwarzian finalizes nothing."
    )

    # ===== [5] verdict =============================================================================
    print("\n[5] VERDICT -- does the Schwarzian finalize closure? (the calc decides)")
    print(
        "    NO. The SYK Schwarzian gives UNIVERSAL numbers (Delta=1/4, S_0/N=0.2324, |E_0/N|~0.04), and"
    )
    print(
        "    the link is real (the amount = <T_munu>_SYK). BUT: (a) the dimensional bridge (N, V, J) spans"
    )
    print(
        f"    ~{span:.0f} orders -> rho_DM is NOT pinned by L; (b) no pure SYK number is the DM:baryon 5.36;"
    )
    print(
        "    (c) the ratio needs the baryon sector anyway. So the Schwarzian SHARPENS the residual (the"
    )
    print(
        "    amount = the SYK energy density, universal in (J^2,N)) but does NOT finalize the 5:1 -- the"
    )
    print(
        "    dimensional bridge / the (N,V,J) identification IS the closure IC, relocated not solved."
    )
    print(
        "    closure_introspection STANDS: FORM+SIGN derived, the AMOUNT is the genuine IC. We are NOT"
    )
    print(
        "    'good' -- but we now know precisely why: the bridge from the universal SYK <T_munu> to the"
    )
    print(
        "    physical density needs the germe's (N,V,J), = the wavefunction of the universe, still open."
    )

    print(
        "\n  COMPUTED: Delta=1/q, N=S_BH/(S_0/N); the rho_DM bridge span; the clean-ratio test. REPORTED:"
    )
    print(
        "  no finalization (the bridge is free) -- seul les calculs comptent, et ils disent: relocalisé, pas resolu."
    )
    print("=" * 96)


if __name__ == "__main__":
    main()
