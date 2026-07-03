"""Seed 3 (V9.0, quarantined) — POINT E: the m_V axion (g_agamma) on the PHOTONIC chip (belenos = photons).
Romain's 'vas y' on the last recul point: OBT's ONE derived bulk channel is the m_V axion (~1 ueV LVS Kahler
axion, g_agamma ~ 1e-15 GeV^-1 on the QCD line, in the qubit window) -- and belenos-12 is PHOTONIC (Quandela,
optical single photons), while the axion couples to PHOTONS (L = -(g/4) a F Ftilde -> polarization rotation).
So: could the demon-run on belenos ALSO be an axion run? THE ORDER OF MAGNITUDE DECIDES ('seul les calculs
comptent' -- computed, not presumed, in EITHER direction).

THE PHYSICS (standard axion electrodynamics, no toy):
  * the DM axion is a COHERENT classical field a(t) = a0 cos(m t), a0 = sqrt(2 rho_a)/m (rho_a = kappa x the
    local DM density; kappa = the m_V DM fraction: ~1% natural at f_a~M_s, up to 100% at the LVS high end).
  * light crossing the field gets its linear polarization rotated by Dtheta = (g/2)[a(t_out) - a(t_in)]
    (carrier-frequency independent). A chip transit (L ~ cm) is SHORT vs the axion period (~4 ns) ->
    Dtheta_rms = (g/2) a0 (m L)/sqrt(2)  -- the short-baseline suppression m*L.
  * an OPTICAL cavity can enhance only while the light stays < half an axion period (the storage-time cap):
    max gain = (c / 2 f_a) / L  -- the reason ueV axions are hunted with MICROWAVE cavities + magnets, not
    optical interferometers.

WHAT IS COMPUTED: [1] the OBT channel numbers (f_a=240 MHz, g=(alpha/2pi)/M_s ~ 1e-15 -- both REPRODUCE the
session's derived values, asserted as reproductions) + the coherent field a0 (the energy-density identity
0.5 m^2 a0^2 = rho asserted); [2] the per-transit rotation on the chip (kappa x L grid) = the best-case
probability tilt epsilon on a polarization readout; [3] the belenos detectability: shots to 3 sigma, time,
EUR; [4] the chip's actual g-reach (8-EUR budget and 1 year) vs the CAST bound and vs OBT's g; [5] the
optical-cavity cap. VERDICT + the INTERPRETIVE COROLLARY for the belenos protocol (pre-registered): can a
layer-1 anomaly be attributed to the m_V axion, or not? The numbers answer.

HONEST FRAME: the estimate below is the OPTIMISTIC bound (free-space polarization interferometry at the
quantum limit); the waveguide reality (path encoding, pinned polarization) is WEAKER. Not V8.2, not the PDF.
"""

import numpy as np

# constants (standard values, declared)
ALPHA = 1.0 / 137.036
H_EV_S = 4.135667e-15  # Planck h, eV s
C_CM_S = 2.998e10  # cm/s
CM_IN_INV_GEV = 5.068e13  # 1 cm in GeV^-1 (1/hbar c)
RHO_DM_GEV_CM3 = 0.4  # local DM density (standard 0.3-0.45)

# OBT's derived channel (the session's chain: chi -> ALP -> m_V -> f_a; CLAUDE.md)
M_A_EV = 1.0e-6  # m_V ~ 1 ueV (the LVS blow-up/fibre Kahler axion)
F_A_GEV = 1.19e12  # f_a ~ M_s (OBT-derived string scale)
KAPPAS = {"natural (f_a~M_s, ~1% DM)": 0.01, "full-DM sweet spot": 1.00}
LS_CM = [1.0, 10.0]  # chip optical path lengths considered
RATE = 1.0e4  # shots/s (the favorable end of the protocol's parametrization)
EUR_PER_S = 0.28
CAST_BOUND = 6.6e-11  # GeV^-1 (helioscope bound, PDG)


def main():
    print("=" * 100)
    print(
        " POINT E — the m_V axion (g_agamma) on the PHOTONIC chip: the order of magnitude decides"
    )
    print("=" * 100)

    # ===== [1] the OBT channel numbers (reproductions asserted) =====
    m_gev = M_A_EV * 1e-9
    f_hz = M_A_EV / H_EV_S  # the axion oscillation frequency
    g = (ALPHA / (2 * np.pi)) / F_A_GEV  # the axion-photon coupling
    rho_gev4 = RHO_DM_GEV_CM3 / CM_IN_INV_GEV**3  # GeV^4
    a0_full = (
        np.sqrt(2 * rho_gev4) / m_gev
    )  # the coherent field amplitude at kappa=1, GeV
    assert (
        abs(f_hz / 2.42e8 - 1) < 0.05
    ), "f_a must reproduce the session's ~240 MHz (m_V ~ 1 ueV)"
    assert (
        abs(g / 9.8e-16 - 1) < 0.05
    ), "g_agamma must reproduce the session's ~1e-15 GeV^-1 (f_a=M_s)"
    assert (
        abs(0.5 * m_gev**2 * a0_full**2 / rho_gev4 - 1) < 1e-9
    ), "energy-density identity rho = m^2 a0^2 / 2"
    print("\n[1] THE OBT CHANNEL (the derived numbers, reproduced)")
    print(
        f"      m_V = {M_A_EV:.0e} eV  ->  f_a = {f_hz/1e6:.0f} MHz (period {1e9/f_hz:.1f} ns)"
    )
    print(f"      g_agamma = (alpha/2pi)/M_s = {g:.2e} GeV^-1 (the QCD-line value)")
    print(
        f"      coherent field a0(kappa=1) = sqrt(2 rho)/m = {a0_full:.2e} GeV  (rho_local = {RHO_DM_GEV_CM3} GeV/cm^3)"
    )

    # ===== [2] the per-transit rotation on the chip =====
    print(
        "\n[2] THE CHIP EFFECT — polarization rotation per transit (the best-case qubit tilt epsilon)"
    )
    print(
        "      kappa                         L(cm)   m*L      theta_rms (rad) = the tilt epsilon"
    )
    thetas = {}
    for lab, kap in KAPPAS.items():
        a0 = a0_full * np.sqrt(kap)
        for L in LS_CM:
            ml = m_gev * (L * CM_IN_INV_GEV)  # dimensionless short-baseline factor
            th = (g / 2) * a0 * ml / np.sqrt(2)
            thetas[(lab, L)] = th
            print(f"      {lab:28s}  {L:5.0f}   {ml:.3f}    {th:.2e}")
    print(
        "      (the transit ~L/c ~ 33-330 ps << the 4.1 ns axion period -> the m*L suppression is mild;"
    )
    print("       the smallness is the COUPLING x FIELD, not the baseline.)")

    # ===== [3] belenos detectability: shots to 3 sigma =====
    print(
        "\n[3] DETECTABILITY ON BELENOS — shots to 3 sigma at the quantum limit (SNR = theta sqrt(N))"
    )
    th_best = max(thetas.values())  # full DM, L=10 cm: the MOST favorable case
    n_3sig = (3.0 / th_best) ** 2
    t_s = n_3sig / RATE
    print(f"      most favorable case (full DM, L=10 cm): theta = {th_best:.2e} rad")
    print(f"      shots to 3 sigma N = (3/theta)^2 = {n_3sig:.1e}")
    print(
        f"      at {RATE:.0e} shots/s: {t_s:.1e} s = {t_s/3.15e7:.1e} years ({t_s/3.15e7/1.38e10:.1e} ages of the universe)"
    )
    print(f"      cost at {EUR_PER_S} EUR/s: {EUR_PER_S*t_s:.1e} EUR")

    # ===== [4] the chip's actual g-reach vs the bounds =====
    print(
        "\n[4] THE CHIP'S g-REACH (invert: what coupling WOULD the chip see?) vs the real bounds"
    )
    a0 = a0_full  # reach quoted at kappa=1 (most favorable)
    ml = m_gev * (LS_CM[-1] * CM_IN_INV_GEV)
    per_g = (a0 / 2) * ml / np.sqrt(2)  # theta per unit g
    for lab, n in [
        ("the 8-EUR budget (2.9e5 shots)", 8 / EUR_PER_S * RATE),
        ("one FULL YEAR at 1e4/s", 3.15e7 * RATE),
    ]:
        g_reach = (3.0 / np.sqrt(n)) / per_g
        print(
            f"      {lab:34s}: g_reach = {g_reach:.1e} GeV^-1"
            f"  ({np.log10(g_reach/CAST_BOUND):.0f} orders ABOVE the CAST bound {CAST_BOUND:.1e};"
            f" {np.log10(g_reach/g):.0f} above OBT's {g:.1e})"
        )

    # ===== [5] the optical-cavity cap (why no resonant rescue at optical) =====
    print(
        "\n[5] THE OPTICAL-CAVITY CAP — resonant enhancement is bounded by the axion half-period storage"
    )
    for L in LS_CM:
        gain = (C_CM_S / (2 * f_hz)) / L
        print(
            f"      L = {L:4.0f} cm: max cavity gain = (c/2f_a)/L = {gain:.0f}x  -> closes ~{np.log10(gain):.1f} of the"
            f" ~{np.log10((3.0/np.sqrt(3.15e7*RATE))/per_g/g):.0f} missing orders"
        )
    print(
        "      => even a PERFECT optical cavity gains ~1-2 orders of the ~17+ missing: mueV axions are"
    )
    print(
        "         MICROWAVE-cavity territory (resonant AT 240 MHz + a magnet + years) -- exactly PATH 3."
    )

    # ===== VERDICT + the interpretive corollary (gaps COMPUTED, not hand-quoted) =====
    th_worst = min(thetas.values())
    th_min_year = 3.0 / np.sqrt(3.15e7 * RATE)  # one-year quantum-limited 3-sigma floor
    gap_lo = np.log10(th_min_year / th_best)
    gap_hi = np.log10(th_min_year / th_worst)
    print("\n[VERDICT] the photonic chip is NOT an axion detector -- quantitatively:")
    print(
        f"    the derived channel's imprint on a chip transit is theta ~ {th_worst:.0e}-{th_best:.0e} rad,"
    )
    print(
        f"    {gap_lo:.0f}-{gap_hi:.0f} orders below even a ONE-YEAR quantum-limited readout (theta_min = {th_min_year:.1e} rad),"
    )
    print(
        "    and the optical-cavity cap (~60x) cannot bridge it. The m_V bone STAYS PATH 3 (ADMX/HAYSTAC-"
    )
    print(
        "    class microwave cavity + magnet). Same shape as optimal_sensor_threshold's gravitational verdict:"
    )
    print(
        "    you cannot out-sense the coupling; the LEVERAGE is the dedicated resonant instrument."
    )
    print(
        "\n[COROLLARY — PRE-REGISTERED INTERPRETATION for the belenos protocol] a layer-1 anomaly on belenos"
    )
    print(
        f"    CANNOT be attributed to the m_V axion (OBT's only derived bulk field is {gap_lo:.0f}+ orders too weak on"
    )
    print(
        "    the chip), and a belenos NULL does NOT constrain the axion. The demon-run and the axion bone"
    )
    print(
        "    are CLEANLY DECOUPLED instruments -- declared BEFORE any run, so no post-hoc pareidolia can"
    )
    print(
        "    dress a chip anomaly as 'the derived bulk field'. An anomaly, if seen, is UNMODELED physics."
    )
    print(
        "\n  COMPUTED; asserted only the reproductions (240 MHz, 1e-15) + the energy-density identity."
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
