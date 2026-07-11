"""Seed 3 (V9.0, quarantined) — the m_V EFFECTIVE HALOSCOPE COUPLING and its f_a-INVARIANCE.

Support calculation for the community-facing note (mv_axion_note.md). The chain mv_coupling ->
mv_abundance -> mv_fa_lvs left the DM fraction as the one f_a-dependent unknown (1% natural at f_a~M_s,
100% at the LVS high end) -- suggesting the experimental target is f_a-uncertain. THIS script computes
what a haloscope ACTUALLY measures and finds it is NOT: the signal power is g^2 rho_a, so the effective
(density-weighted) coupling is g_eff = g * sqrt(Omega_a/Omega_DM); with g = (alpha/2pi) C / f_a and the
misalignment Omega ~ f_a^2 (a string ALP: m_a is instanton-set, INDEPENDENT of f_a -- unlike the QCD
axion), the f_a dependence CANCELS EXACTLY below saturation:

    g_eff = (alpha/2pi) * C * theta_i / f_a,DM        (f_a,DM = the full-DM decay constant)

-> ONE f_a-invariant experimental target, g_eff ~ 1e-16 GeV^-1 at m ~ 1 micro-eV (242 MHz), instead of a
three-decade f_a bracket. Computed here: [1] the reproduction of the chain's published numbers (asserted
as reproductions); [2] the invariance (asserted as the algebraic identity it is, on a numerical f_a scan);
[3] the QCD-band comparison (KSVZ/DFSZ at these masses + the crossing masses); [4] the FLASH overlay
(arXiv:2309.00351: 100-300 MHz, DFSZ-class phases) + CAST margins. Everything else reported, not imposed.

INVARIANCE ASSUMPTIONS (stated, they are the chain's own): (i) m_a independent of f_a (string ALP,
instanton-set mass; the QCD axion has m ~ 1/f_a and does NOT enjoy this cancellation); (ii) standard
misalignment, theta_i fixed, no post-T_osc entropy injection; (iii) below over-closure saturation
(f_a <= f_a,DM); (iv) the local axion fraction clusters like the bulk DM (rho_a,local/rho_DM,local =
Omega_a/Omega_DM). NOT V8.2, not the PDF. 'seul les calculs comptent'.
"""

import numpy as np

# constants
ALPHA = 1.0 / 137.036
H_EV_S = 4.135667e-15  # Planck h, eV s
M_PL_FULL = (
    1.22e19  # GeV (the 1.66*sqrt(g*) radiation-era H formula uses the FULL Planck mass)
)
GEV3_PER_CM3 = (1.0 / 5.068e13) ** 3  # 1 cm^-3 in GeV^3
S0 = 2891.0 * GEV3_PER_CM3  # entropy density today, GeV^3
RHO_C_H2 = 1.054e-5 * GEV3_PER_CM3  # critical density / h^2, GeV^4
OMEGA_DM_H2 = 0.12

# OBT's derived channel (mv_coupling / mv_fa_lvs, re-verified this session)
M_A_EV = 1.0e-6  # the LVS ultralight scale (order-of-magnitude)
M_S = 1.19e12  # GeV, the OBT LVS string scale (natural f_a)
G_STAR = 80.0  # relativistic dof at T_osc ~ 16 GeV

# QCD-axion comparison (Gorghetto-Villadoro class: m_a = 5.70 mueV at f_a = 1e12 GeV)
M_QCD_AT_1E12 = 5.70e-6  # eV
C_KSVZ, C_DFSZ = 1.92, 0.75

# FLASH (arXiv:2309.00351): 100-300 MHz band, QCD-axion masses quoted 0.49-1.49 mueV;
# phase-1 (microstrip SQUID) g ~ 1e-16, phase-2 (100 mK) g ~ 2e-17
FLASH_BAND_MHZ = (100.0, 300.0)
FLASH_G1, FLASH_G2 = 1.0e-16, 2.0e-17
CAST_BOUND = 6.6e-11  # GeV^-1


def omega_h2(f_a_gev, m_a_ev=M_A_EV, theta=1.0):
    """Standard misalignment relic (self-contained, matches mv_abundance): 3H=m_a sets T_osc,
    n_a/s conserved, rho_a0 = m_a * (n_a/s) * s0."""
    m_gev = m_a_ev * 1e-9
    t_osc = np.sqrt(m_gev * M_PL_FULL / (3 * 1.66 * np.sqrt(G_STAR)))
    n_a = 0.5 * m_gev * (theta * f_a_gev) ** 2
    s_osc = (2 * np.pi**2 / 45) * G_STAR * t_osc**3
    return m_gev * (n_a / s_osc) * S0 / RHO_C_H2, t_osc


def g_agg(f_a_gev, c=1.0):
    return (ALPHA / (2 * np.pi)) * c / f_a_gev


def main():
    print("=" * 100)
    print(
        " m_V EFFECTIVE HALOSCOPE COUPLING — the f_a-INVARIANCE (support calc for mv_axion_note.md)"
    )
    print("=" * 100)

    # ===== [1] reproductions of the chain's published numbers =====
    om_ms, t_osc = omega_h2(M_S)
    g_ms = g_agg(M_S)
    f_dm = M_S * np.sqrt(OMEGA_DM_H2 / om_ms)  # Omega ~ f_a^2
    nu_mhz = M_A_EV / H_EV_S / 1e6
    assert (
        abs(g_ms / 9.76e-16 - 1) < 0.02
    ), "reproduce mv_coupling: g(f_a=M_s) ~ 9.8e-16"
    assert abs(t_osc / 16.3 - 1) < 0.05, "reproduce mv_abundance: T_osc ~ 16.3 GeV"
    assert (
        abs(om_ms / 1.20e-3 - 1) < 0.05
    ), "reproduce mv_abundance: Omega h^2(M_s) ~ 1.2e-3"
    assert (
        abs(f_dm / 1.19e13 - 1) < 0.05
    ), "reproduce mv_abundance: full-DM f_a ~ 1.2e13"
    print("\n[1] REPRODUCTIONS (the chain's numbers, re-derived self-contained):")
    print(f"      nu(m_V=1e-6 eV) = {nu_mhz:.0f} MHz; T_osc = {t_osc:.1f} GeV")
    print(
        f"      g(f_a=M_s) = {g_ms:.2e} GeV^-1; Omega h^2(M_s, theta=1) = {om_ms:.2e} = "
        f"{om_ms/OMEGA_DM_H2*100:.1f}% DM; full-DM f_a = {f_dm:.2e} GeV"
    )

    # ===== [2] THE INVARIANCE (the algebraic identity, verified on a scan) =====
    fas = np.logspace(10, np.log10(f_dm), 200)
    g_eff = np.array(
        [
            g_agg(f) * np.sqrt(min(omega_h2(f)[0], OMEGA_DM_H2) / OMEGA_DM_H2)
            for f in fas
        ]
    )
    pred = (
        ALPHA / (2 * np.pi)
    ) / f_dm  # the identity: g_eff = (alpha/2pi) C theta / f_a,DM
    assert (
        np.max(np.abs(g_eff / pred - 1)) < 1e-9
    ), "the f_a-invariance identity (below saturation)"
    print(
        f"\n[2] THE f_a-INVARIANCE (identity verified on f_a in [1e10, {f_dm:.1e}], 200 points):"
    )
    print("      g_eff = g * sqrt(Omega_a/Omega_DM) = (alpha/2pi) C theta_i / f_a,DM")
    print(f"            = {pred:.2e} * C * theta_i  GeV^-1   -- INDEPENDENT of f_a")
    print(
        "      (g ~ 1/f_a and Omega ~ f_a^2 cancel exactly; holds because the string-ALP mass is"
    )
    print(
        "       instanton-set, independent of f_a -- the QCD axion does NOT enjoy this. So the"
    )
    print("       three-decade LVS f_a bracket collapses to ONE experimental target.)")

    # ===== [3] the QCD band at these masses + the crossings =====
    print(
        "\n[3] vs THE QCD BAND (m_a = 5.70 mueV * 1e12/f_a; KSVZ |C|=1.92, DFSZ |C|=0.75):"
    )
    print(
        "      m (mueV)   nu (MHz)   g_KSVZ      g_DFSZ      OBT g_eff   OBT natural g (f_a=M_s)"
    )
    for m in (0.3, 0.64, 1.0, 1.49, 3.0):
        f_qcd = 1e12 * M_QCD_AT_1E12 / (m * 1e-6)
        gk, gd = g_agg(f_qcd, C_KSVZ), g_agg(f_qcd, C_DFSZ)
        print(
            f"      {m:6.2f}   {m*1e-6/H_EV_S/1e6:7.0f}   {gk:.2e}   {gd:.2e}   {pred:.2e}   {g_ms:.2e}"
        )
    m_x_dfsz = pred / (g_agg(1e12 * M_QCD_AT_1E12 / 1e-6, C_DFSZ)) * 1.0  # g_QCD ~ m
    m_x_ksvz = pred / (g_agg(1e12 * M_QCD_AT_1E12 / 1e-6, C_KSVZ)) * 1.0
    print("      -> the invariant floor CROSSES the QCD band inside the target decade:")
    print(
        f"         above DFSZ below m = {m_x_dfsz:.2f} mueV; above KSVZ below m = {m_x_ksvz:.2f} mueV"
    )
    print(
        f"      -> the QCD-axion mass at f_a=M_s would be {1e6*M_QCD_AT_1E12*1e12/M_S:.1f} mueV"
        f" (within ~5x of m_V ~ 1 mueV: near, not on, the QCD relation)"
    )

    # ===== [4] FLASH overlay + CAST margin =====
    print("\n[4] THE EXPERIMENTAL MATCH (computed margins):")
    print(
        f"      FLASH band {FLASH_BAND_MHZ[0]:.0f}-{FLASH_BAND_MHZ[1]:.0f} MHz: the OBT central"
        f" target {nu_mhz:.0f} MHz is INSIDE it"
    )
    print(
        f"      FLASH phase-1 g ~ {FLASH_G1:.0e}: the OBT floor is {pred/FLASH_G1:.2f}x it"
        f" (C=theta=1) -> phase-1 GRAZES the floor"
    )
    print(
        f"      FLASH phase-2 g ~ {FLASH_G2:.0e}: the floor is {pred/FLASH_G2:.1f}x ABOVE it"
        f" -> phase-2 cuts x{pred/FLASH_G2:.0f} BELOW the whole bracket = DECISIVE at C,theta=O(1)"
    )
    print(
        f"      CAST helioscope bound {CAST_BOUND:.1e} (rho-independent, constrains g not g_eff):"
    )
    print(
        f"        natural corner g = {g_ms:.1e} -> {np.log10(CAST_BOUND/g_ms):.1f} orders below CAST"
        f" (unconstrained); the whole bracket g in [{g_agg(f_dm):.1e}, {g_agg(1e10):.1e}] stays"
        f" {np.log10(CAST_BOUND/g_agg(1e10)):.1f}+ orders below"
    )

    # ===== VERDICT =====
    print(
        "\n[VERDICT] the m_V bone has ONE f_a-invariant experimental coordinate, not a bracket:"
    )
    print(
        f"    m ~ 1 mueV-scale (nu ~ {nu_mhz:.0f} MHz central; the LVS scale is order-of-magnitude),"
    )
    print(
        f"    g_eff = {pred:.1e} * C * theta_i GeV^-1 (f_a-INVARIANT below saturation),"
    )
    print(
        f"    crossing the QCD band inside the decade; CAST-open by ~5 orders; sitting INSIDE the"
    )
    print(
        f"    declared FLASH band, at its phase-1 depth, x{pred/FLASH_G2:.0f} above its phase-2 depth."
    )
    print(
        "    Gates unchanged (axion-vs-saxion id; C, theta_i = O(1); the mueV scale itself is"
    )
    print(
        "    order-of-magnitude; invariance assumptions i-iv in the docstring). Falsifiable: a scan"
    )
    print(
        "    of the mueV decade at g_eff below ~1e-17 kills the whole misalignment chain at O(1)"
    )
    print("    angles -- the bone dies cleanly; a detection near the floor matches it.")
    print("=" * 100)


if __name__ == "__main__":
    main()
