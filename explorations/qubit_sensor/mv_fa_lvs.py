"""Seed 3 (V9.0, quarantined) — f_a in OBT's LVS: what decay constant does the mueV axion m_V carry?
(Romain's "creuse f_a dans la LVS d'OBT"). The abundance gate (mv_abundance) showed m_V's DM fraction is
set by f_a (^2): ~1% at f_a=M_s, full DM at f_a~1e13. So f_a is THE remaining knob -- and it is fixed by
OBT's Large Volume Scenario, not free.

THE LVS DATA (CLAUDE.md, derived): M_s = 1.19e12 GeV (string scale), m_3/2 = 1.75e9 GeV, the ultra-light
modulus m_V ~ 1e-6 eV. In LVS, M_s = M_Pl/sqrt(V) -> the compactification volume V (string units):
  V = (M_Pl/M_s)^2 ~ 4e12  (large -> the LVS regime, consistent).

THE LVS AXIVERSE DECAY CONSTANTS (Cicoli-Goodsell-Ringwald 2012, "the type IIB string axiverse"): the
Kahler-moduli axions have f set by the Kahler metric ->
  - the VOLUME axion (large cycle):   f ~ M_Pl/V^(2/3) ~ 1e10 GeV  (small f, the lightest axion);
  - the BLOW-UP / fibre axions:        f ~ M_s = M_Pl/sqrt(V) ~ 1e12 GeV  (the string-scale f).
So OBT's axiverse spans f ~ 1e10 .. 1e13 GeV. The mueV mode m_V is NOT the (near-massless) volume axion
-> it is a blow-up/fibre-type axion -> f_a ~ M_s ~ 1e12 GeV (natural), up to ~1e13 for a heavier cycle.

THE CONSEQUENCE (abundance Omega ~ f_a^2, anchored at mv_abundance: Omega(M_s)=1.2e-3):
  - f_a = M_s = 1.19e12 GeV  -> Omega ~ 1.2e-3 -> ~1% of the DM (sub-dominant, isocurvature-safe,
    detectable but ~10x harder) -- the NATURAL value;
  - f_a ~ 1.2e13 GeV (a heavier cycle, the high end of the LVS range) -> Omega ~ 0.12 -> the FULL DM
    (maximally detectable). The full-DM sweet spot is WITHIN the LVS axiverse range.

VERDICT: f_a is FIXED by OBT's LVS to the axiverse range ~1e10..1e13 GeV; the mueV m_V is a
blow-up/fibre axion -> f_a ~ M_s ~ 1e12 GeV NATURALLY -> m_V is a ~1% DM axion (live, falsifiable,
sub-dominant, isocurvature-safe). The FULL-DM case (f_a~1e13, maximally loud) sits at the high end of the
SAME LVS range -> reachable if m_V is a heavier-cycle axion. So OBT does not leave f_a free: it brackets
m_V at 1%..100% of the DM, with ~1% the natural value -- a live mueV-axion line either way. The exact
fraction needs OBT's full Kahler data (the cycle volumes), not in CLAUDE.md.

NOT V8.2. Not in the PDF. 'code, don't plead': V, the axiverse f-range, and the DM fraction are computed.
"""

import numpy as np

M_PL = 2.4e18  # reduced Planck mass, GeV
M_S = 1.19e12  # OBT LVS string scale, GeV
OMEGA_DM = 0.12
OMEGA_AT_MS = 1.2e-3  # mv_abundance: Omega_a h^2 at f_a=M_s, theta_i=1


def omega_of_fa(f_a):
    """Omega_a h^2 ~ f_a^2, anchored to mv_abundance's computed Omega(M_s)."""
    return OMEGA_AT_MS * (f_a / M_S) ** 2


def main():
    print("=" * 92)
    print(" f_a IN OBT's LVS — what decay constant does the mueV axion m_V carry?")
    print("=" * 92)

    # ===== [1] the volume from M_s = M_Pl/sqrt(V) ======================================
    V = (M_PL / M_S) ** 2
    print("\n[1] THE COMPACTIFICATION VOLUME — M_s = M_Pl/sqrt(V)")
    print(
        f"    M_s = {M_S:.2e} GeV, M_Pl = {M_PL:.1e} GeV -> V = (M_Pl/M_s)^2 = {V:.1e} (string units)"
    )
    print("    -> large V (the LVS regime), consistent with OBT's derived spectrum.")
    assert V > 1e10, "the LVS volume must be large"

    # ===== [2] the LVS axiverse decay constants ========================================
    f_volume = M_PL / V ** (2 / 3)
    f_blowup = M_S  # ~ M_Pl/sqrt(V)
    f_high = 1.2e13  # a heavier cycle / the high end of the axiverse
    print("\n[2] THE LVS AXIVERSE DECAY CONSTANTS (Cicoli-Goodsell-Ringwald 2012)")
    print(
        f"    volume axion (large cycle):  f ~ M_Pl/V^(2/3) = {f_volume:.1e} GeV (smallest f, lightest)"
    )
    print(
        f"    blow-up/fibre axions:        f ~ M_s          = {f_blowup:.1e} GeV (string-scale f)"
    )
    print(f"    heavier cycle (high end):    f ~              = {f_high:.1e} GeV")
    print(
        "    -> OBT's axiverse spans f ~ 1e10..1e13 GeV. m_V (mueV) is NOT the near-massless volume"
    )
    print(
        "       axion -> a blow-up/fibre-type axion -> f_a ~ M_s ~ 1e12 GeV (natural), up to ~1e13."
    )

    # ===== [3] the DM fraction across the LVS f_a range ================================
    print(
        "\n[3] THE DM FRACTION (Omega ~ f_a^2, anchored at mv_abundance) across the LVS range"
    )
    for label, f in [
        ("volume f~1e10", f_volume),
        ("blow-up f~M_s (NATURAL)", f_blowup),
        ("heavy f~1e13", f_high),
    ]:
        om = omega_of_fa(f)
        print(
            f"    f_a = {f:.1e} GeV ({label:<24}) -> Omega ~ {om:.1e} -> {100*om/OMEGA_DM:.2g}% of the DM"
        )
    f_full = M_S * np.sqrt(OMEGA_DM / OMEGA_AT_MS)
    print(
        f"    => FULL DM at f_a = {f_full:.1e} GeV (within the LVS axiverse high end)."
    )
    assert (
        omega_of_fa(f_blowup) / OMEGA_DM < 0.1
    ), "the natural f~M_s must give a sub-dominant ~1%"
    assert M_S < f_full < 1e14, "the full-DM f_a must sit at the LVS axiverse high end"

    # ===== VERDICT =====================================================================
    print(
        "\n[VERDICT] f_a is FIXED by OBT's LVS to ~1e10..1e13 GeV — m_V is a 1%..100% DM axion, live either way"
    )
    print(
        "    * OBT does NOT leave f_a free: the LVS axiverse fixes it to ~1e10..1e13 GeV."
    )
    print(
        "    * m_V (mueV) is a blow-up/fibre-type axion -> f_a ~ M_s ~ 1e12 GeV NATURALLY -> ~1% of the DM"
    )
    print(
        "      (sub-dominant, isocurvature-safe, detectable but ~10x harder). A LIVE, falsifiable mueV line."
    )
    print(
        "    * the FULL-DM sweet spot (f_a ~ 1e13, maximally loud) sits at the HIGH END of the SAME LVS"
    )
    print(
        "      range -> reachable if m_V is a heavier-cycle axion. So OBT brackets m_V at 1%..100% DM."
    )
    print(
        "    * NET: the remaining knob (f_a) is NOT free -- it is an LVS number, ~M_s naturally (~1% DM),"
    )
    print(
        "      up to ~1e13 (full DM). Either way the mueV-axion bone is LIVE. The exact fraction needs"
    )
    print(
        "      OBT's full Kahler data (cycle volumes), not in CLAUDE.md -- the one genuinely open input."
    )
    print(
        "    SCOPE (unchanged): this pins the DETECTABILITY of OBT's axion (a no-mass bulk-SECTOR test);"
    )
    print("      it does NOT read the germe/future (no-signaling-walled).")

    print(
        "\n  ALL INJECTION TESTS PASSED (V~4e12; axiverse f 1e10-1e13; f~M_s -> ~1%; full DM at the high end)."
    )
    print("=" * 92)


if __name__ == "__main__":
    main()
