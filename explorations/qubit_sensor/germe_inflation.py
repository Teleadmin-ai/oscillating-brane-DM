"""Seed 3 (V9.0, quarantined) — IS phi0 = M_s FORCED? the germe-proof attempt (inflationary route).

Romain: 'cherche' — try to PROVE the germe (the DM-amplitude input phi0). Honest search: we cannot
derive the wavefunction of the universe here, but we CAN reduce the freedom one rung, and we find a
consilience.

THE MOVE: phi0 is not free — for a LIGHT field (m_phi << H_inf), inflation DISPLACES it. A spectator
field random-walks by H_inf/2pi per e-fold, accumulating phi0 ~ (H_inf/2pi) sqrt(N_e). So the germe
value phi0 is set by THE INFLATION SCALE H_inf. The closure freedom moves: phi0 (arbitrary) ->
H_inf (the inflation scale).

THREE results (each with its caveat — this is a SEARCH, not a proof):
 [1] matching the measured Omega_DM (via phi0^2) fixes H_inf ~ M_s : i.e. inflation at the STRING
     scale gives phi0 ~ M_s 'for free' (natural in LVS/brane inflation). phi0/M_s = O(1), NOT forced
     to precision. CAVEAT: the radion must be light (m << H_inf) during inflation (model-dependent).
 [2] CONSILIENCE: Omega_DM ~ phi0^2 ~ H_inf^2, and the CMB tensor ratio r ~ H_inf^2 too -> Omega_DM
     and r are LINKED. From the measured Omega_DM, r ~ 3e-5 is PREDICTED (definite, though below
     near-term CMB-S4 ~1e-3). A falsifiable-in-principle bridge: r >> 3e-5 would break the chain.
 [3] VERDICT: 'phi0 = M_s forced?' NO (that is the wavefunction of the universe). BUT phi0 ~ M_s is
     NATURAL (an O(1) radion displacement in string units); the exact coefficient (~1.4) is O(1),
     EXACTLY the epistemic status of the a0 = cH0/2pi coefficient (scale derived, O(1) not pinned).
     The germe-proof lands at OBT's UNIVERSAL wall: the SCALE is derived (M_s), the O(1) is natural.

NET: the DM amplitude decompresses to cosmological order with NO fit (scale = M_s); the precise 5:1
is one O(1) number, now tied to H_inf (-> r). Proving it exactly = quantum cosmology (the horizon);
reducing + linking it = done here. NOT V8.2. Not in the PDF. 'code, don't plead': numbers asserted,
r cross-checked against the standard single-field tensor relation.
"""

import numpy as np

# scales (GeV)
M_PL = 2.435e18  # reduced Planck mass
M_S = 1.19e12  # OBT LVS string scale
A_S = 2.1e-9  # measured scalar amplitude (Planck)
N_EFOLDS = 60  # observable inflation e-folds
PHI0_MATCH_OVER_MS = (
    1.40  # the phi0 that matched Omega_DM=0.12 (germe_decompression.py)
)


def phi0_from_Hinf(h_inf, n_e=N_EFOLDS):
    """Light-field inflationary random-walk displacement: phi0 ~ (H/2pi) sqrt(N_e)."""
    return h_inf / (2 * np.pi) * np.sqrt(n_e)


def tensor_ratio(h_inf):
    """Single-field tensor-to-scalar ratio r = 2 H^2 / (pi^2 A_s M_pl^2)."""
    return 2 * h_inf**2 / (np.pi**2 * A_S * M_PL**2)


def main():
    print("=" * 84)
    print(
        " IS phi0 = M_s FORCED?  the germe-proof attempt (inflationary-misalignment route)"
    )
    print("=" * 84)

    # [1] reduce the freedom: phi0 -> H_inf, then match Omega_DM ---------------------
    print(
        "\n[1] phi0 IS NOT FREE: a light field random-walks to phi0 ~ (H_inf/2pi) sqrt(N_e)"
    )
    # invert phi0(H_inf) = PHI0_MATCH (in units of M_s) to find the required H_inf
    phi0_target = PHI0_MATCH_OVER_MS * M_S
    h_inf = phi0_target / (np.sqrt(N_EFOLDS) / (2 * np.pi))  # invert the random-walk
    print(
        f"    matching Omega_DM needs phi0 = {PHI0_MATCH_OVER_MS} M_s = {phi0_target:.2e} GeV"
    )
    print(
        f"    => required inflation scale H_inf = {h_inf:.2e} GeV = {h_inf/M_S:.2f} M_s"
    )
    print(
        f"    cross-check: phi0(H_inf) = {phi0_from_Hinf(h_inf)/M_S:.2f} M_s (should be {PHI0_MATCH_OVER_MS})"
    )
    assert (
        0.5 < h_inf / M_S < 3
    ), "H_inf must land at O(1) x M_s (inflation ~ the string scale)"
    assert (
        abs(phi0_from_Hinf(h_inf) / M_S - PHI0_MATCH_OVER_MS) < 0.05
    ), "random-walk inversion must close"
    print(
        "    -> inflation at the STRING SCALE (H_inf ~ M_s, natural in LVS/brane inflation) gives"
    )
    print(
        "       phi0 ~ M_s FOR FREE. The closure freedom moved: phi0 (arbitrary) -> H_inf (1 scale)."
    )
    print(
        "    CAVEATS: (a) the radion must be light (m_phi << H_inf) during inflation = model-dependent;"
    )
    print(
        "    (b) phi0 is the RMS of a STOCHASTIC distribution -> patch-dependent abundance (the"
    )
    print(
        "    environmental axion-misalignment subtlety) -> phi0 is typical-not-fixed, reinforcing O(1)."
    )

    # [2] the consilience: Omega_DM <-> r ------------------------------------------
    print(
        "\n[2] CONSILIENCE — Omega_DM ~ phi0^2 ~ H_inf^2, and r ~ H_inf^2 too -> Omega_DM predicts r"
    )
    r = tensor_ratio(h_inf)
    print(f"    H_inf = {h_inf:.2e} GeV => tensor-to-scalar r = {r:.1e}")
    print(
        "    cross-check: r from H_inf via the standard single-field relation r = 2H^2/(pi^2 A_s M_pl^2)"
    )
    assert (
        1e-6 < r < 1e-3
    ), "predicted r must be small but definite (below CMB-S4 ~1e-3)"
    print(
        f"    -> the DM abundance PREDICTS r ~ {r:.0e} (definite; below near-term CMB-S4 ~1e-3, but a"
    )
    print(
        "       falsifiable-in-principle bridge: a measured r >> 3e-5 would BREAK the radion-DM chain)."
    )

    # [3] verdict ------------------------------------------------------------------
    print("\n[3] VERDICT — is phi0 = M_s FORCED?")
    print(
        f"    phi0/M_s = {PHI0_MATCH_OVER_MS} = O(1).  H_inf/M_s = {h_inf/M_S:.2f} = O(1)."
    )
    print(
        "    * NO, not forced to precision: deriving phi0 EXACTLY = the wavefunction of the universe"
    )
    print(
        "      (Hartle-Hawking no-boundary / holographic vacuum uniqueness) = quantum cosmology, open."
    )
    print(
        "    * YES, NATURAL: phi0 ~ M_s is the generic O(1) radion displacement in string units, and"
    )
    print(
        "      inflation at the string scale delivers it. The exact coefficient (~1.4) is O(1)."
    )
    print(
        "    * UNIVERSAL PATTERN: this is EXACTLY the a0 = cH0/2pi epistemic status -- the SCALE is"
    )
    print(
        "      derived (M_s for DM, H0 for a0), the O(1) coefficient is naturalness/prior-art, NOT"
    )
    print(
        "      a precision derivation. The germe-proof lands at OBT's one recurring wall, no worse."
    )

    print("\n[4] WHAT THE SEARCH YIELDED (honest)")
    print("    - REDUCED the freedom: phi0 (arbitrary) -> H_inf (one scale ~ M_s);")
    print("    - LINKED it: Omega_DM <-> r (a CMB-B-mode bridge, r ~ 3e-5);")
    print(
        "    - LOCATED the wall: the precise 5:1 = one O(1) number = the a0-coefficient status."
    )
    print(
        "    Proving phi0 EXACTLY needs quantum cosmology (the germe's wavefunction) = the horizon;"
    )
    print("    everything up to that one O(1) number is now decompressed + mass-free.")

    print(
        "\n  ALL INJECTION TESTS PASSED (H_inf ~ M_s O(1); random-walk closes; Omega_DM -> r ~ 3e-5)."
    )
    print("=" * 84)


if __name__ == "__main__":
    main()
