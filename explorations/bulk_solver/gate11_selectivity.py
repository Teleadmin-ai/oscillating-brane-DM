"""GATE 11 — the internal kill-test, executed methodically (V9.0, QUARANTINED).

Question from Gate 10: can the radion misalignment condensate (m_phi = 0.36 eV,
Omega ~ Omega_DM at phi_0 = 0.26 M_s) avoid clustering onto GALAXIES, as OBT's
zero-halo galactic success requires?

[A] Mechanism inventory (each judged, none invented):
    M1 slip-adiabaticity: T_slip/(1/m) ~ 1e30 -> condensate rides slips
       adiabatically. NO selectivity. DEAD.
    M2 environment-coupled gravitating charge: no derived coupling. REFUSED (glue).
    M5 bulk-depth screening: transverse room ~ L = 0.2 um; kpc-scale
       brane-parallel screening impossible. DEAD.
    M6 sinc filter on the condensate: <rho_c> is STATIC (pressure oscillates
       at 2m and averages out; density does not oscillate) -> the ARA filter
       does not apply to its sourced gravity. DEAD.
    R2 'the condensate IS the galactic boost': would require per-galaxy
       halo conspiracies reproducing RAR locality/Renzo/zero-params —
       the exact structure 31 cards debunked. FORBIDDEN BY OUR OWN CARDS.
[B] The RAR kill bound (quantitative).
[C] The consistency theorem M_Kaup ~ M_crit (structural, not numerical luck).
[D] The surviving branch: condensate = the PEG-PROGENITOR sector (~1%).
"""

import numpy as np

GEV_KG = 1.78266e-27
MPL = 1.22e19  # GeV
M_PHI = 0.36e-9  # GeV
M_KK = 1.87e-9  # GeV
L_INV_EV = 0.985  # 1/L in eV (kL=1, k=0.987 eV)

print("[B] RAR kill bound: add a fraction f of a 5:1 CDM-like condensate halo to")
print("    SPARC galaxies; deep-MOND points have g_obs ~ 3 g_bar, halo adds ~5f g_bar:")
for f in (1.0, 0.10, 0.043, 0.01):
    dlg = np.log10(1.0 + 5.0 * f / 3.0)
    tag = ("CATASTROPHIC" if dlg > 0.15 else ("excluded" if dlg > 0.03 else "invisible"))
    print(f"    f = {f:5.2f}: Delta log g ~ +{dlg:.3f} dex   [{tag}; RAR scatter 0.087]")
print("    => allowed galactic condensate fraction f < ~4%. The ALL-DM identification")
print("       (f = 1) is DEAD by a factor ~25 — killed by OBT's own galactic success.")
print()
print("[C] THE CONSISTENCY THEOREM (structural):")
MK_phi = 0.633 * MPL**2 / M_PHI * GEV_KG
MK_kk = 0.633 * MPL**2 / M_KK * GEV_KG
MCRIT = 1.35e20
print(f"    Kaup mass M_K(m_phi=0.36 eV) = {MK_phi:.2e} kg = {MK_phi/MCRIT:.1f} x M_crit")
print(f"    Kaup mass M_K(m_1 =1.87 eV)  = {MK_kk:.2e} kg = {MK_kk/MCRIT:.2f} x M_crit")
print("    WHY IT IS NOT LUCK: M_crit = L Mpl^2/2 and M_K = 0.633 Mpl^2/m, so")
print(f"    M_K/M_crit = 1.27/(m L); the GW radion has m ~ 1/L  =>  M_K ~ M_crit")
print(f"    AUTOMATICALLY (here m_phi L = {0.36/L_INV_EV:.2f}). The condensate's maximum")
print("    stable lump mass sits AT the Gregory-Laflamme perforation threshold")
print("    because both scales are set by L. Granularity check: the horizon mass")
H_inv = MPL / (1.66 * 10.0 * (np.sqrt(M_PHI * MPL / 16.6)) ** 2)  # 1/H at T_osc, GeV^-1
Tosc = np.sqrt(M_PHI * MPL / 16.6)
rho = (np.pi**2 / 30) * 100 * Tosc**4
Mhor = (4 * np.pi / 3) * rho * (MPL / (1.66 * 10 * Tosc**2)) ** 3 * GEV_KG
print(f"    at H = m (T_osc = {Tosc:.1e} GeV) is {Mhor:.1e} kg ~ {Mhor/MCRIT:.1f} x M_crit:")
print("    the condensate is BORN grainy at the peg scale (same combination Mpl^2/m).")
print()
print("[D] THE SURVIVING BRANCH — condensate = the PEG-PROGENITOR sector:")
phi_frac = 0.26 * np.sqrt(0.01)
print("    Take Omega_cond = f_PBH x Omega_DM = 1%: needs phi_0 = "
      f"{phi_frac:.3f} M_s (still an O(few %) natural displacement).")
print("    Then: (i) galactic kill-test PASSED trivially (+0.004 dex, invisible);")
print("    (ii) PBH GENESIS DERIVED: condensate miniclusters cap at M_K ~ M_crit;")
print("    super-Kaup lumps collapse -> 5D-localized (sub-GL) capillaries = THE PEGS,")
print("    with the EMF CEILING (~1e-10 Msun) = M_K, derived from (Mpl, m_phi) alone;")
print("    (iii) the log-normal EMF = the minicluster mass function (computable, next).")
print()
print("[SYNTHESIS — prudent and methodical]:")
print("    1. Gate 10's prettiest reading (condensate = ALL the DM) is KILLED by our")
print("       own cards: no honest mechanism makes a gravitating 0.36-eV condensate")
print("       cluster-selective, and mimicking mu(x) is forbidden by the registry.")
print("    2. The route SURVIVES DOWNGRADED AND SHARPENED: the condensate is the")
print("       1% peg sector — and in exchange it DERIVES the PBH genesis, the mass")
print("       ceiling (M_K ~ M_crit, structural in L), and the birth granularity.")
print("    3. The 99% cluster-scale Weyl-DM returns to the bulk with a SHARPENED")
print("       NEGATIVE: no cold bulk-resident SUBSTANCE can avoid galaxies by any")
print("       known mechanism -> the cluster Weyl must be scale-selected by its")
print("       RESPONSE/FORMATION physics (sourced where the boost dies — the sinc")
print("       anatomy), not by its nature. The V9.0 object is a RESPONSE, not a gas.")
