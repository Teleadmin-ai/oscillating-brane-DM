"""GATE 12 — the minicluster mass function: AUDIT FIRST (V9.0, QUARANTINED).

Methodical rule: before computing the EMF mass function from Gate 11's
"condensate is born grainy at the peg scale", AUDIT that premise. Gate 11
[C] read the HORIZON mass at H=m (Mpl^2/2m ~ 2.7 M_crit) as the grain mass.
But a minicluster's DM mass is the condensate's DM inside that horizon, i.e.
the horizon mass times rho_phi/rho_tot at onset -- NOT the total horizon mass.
This gate computes that factor and tests whether the claim survives.
"""

import numpy as np

GEV_KG = 1.78266e-27
MSUN_KG = 1.989e30
MPL = 1.22e19  # GeV (non-reduced; M_Kaup, M_crit conventions in Gate 11)
M_PHI = 0.36e-9  # GeV
M_S = 1.19e12  # GeV (LVS string scale)
GSTAR = 100.0
MCRIT = 1.35e20  # kg (L c^2 / 2G)

# --- onset of oscillation: H = m ---
T_osc = (M_PHI * MPL / (1.66 * np.sqrt(GSTAR))) ** 0.5
H_osc = M_PHI
rho_tot = 3 * H_osc**2 * MPL**2 / (8 * np.pi)  # GeV^4
phi0_1pct = 0.026 * M_S  # 1% DM (Gate 10/11)
phi0_allDM = 0.26 * M_S  # all DM (Gate 10, killed Gate11)

print("[A] AUDIT of Gate 11's 'grainy at the peg scale':")
M_hor = rho_tot * (4 * np.pi / 3) / H_osc**3 * GEV_KG  # total horizon mass
print(
    f"    T_osc = {T_osc:.2e} GeV ; total horizon mass at H=m = {M_hor:.2e} kg"
    f" = {M_hor/MCRIT:.1f} M_crit  [what Gate 11 quoted]"
)
for tag, phi0, frac in [
    ("1% DM (phi0=0.026 Ms)", phi0_1pct, 0.01),
    ("all DM (phi0=0.26 Ms)", phi0_allDM, 1.0),
]:
    rho_phi = 0.5 * M_PHI**2 * phi0**2
    ratio = rho_phi / rho_tot
    M_seed = rho_phi * (4 * np.pi / 3) / H_osc**3 * GEV_KG  # DM mass in horizon
    print(
        f"    {tag}: rho_phi/rho_tot = {ratio:.1e}  ->  DM minicluster SEED mass"
        f" = {M_seed:.1e} kg = {M_seed/MSUN_KG:.1e} Msun"
    )
print(
    f"\n    EMF window (V8.2): 1e-14 to 1e-10 Msun = {1e-14*MSUN_KG:.1e} to {1e-10*MSUN_KG:.1e} kg"
)
print(
    "    VERDICT: the condensate's DM-grain seed (~1e4 kg) is ~12-16 ORDERS below the"
)
print(
    "    EMF window. Gate 11 confused the TOTAL horizon mass (Mpl^2/m) with the DM-grain"
)
print(
    "    mass (= horizon x rho_phi/rho_tot ~ 1e-17). *** Gate 11's 'PBH genesis derived,"
)
print(
    "    EMF ceiling derived' is RETRACTED. *** The condensate does NOT make the pegs by"
)
print("    misalignment fragmentation. (The #24 reflex applied to our own gate.)")

print(
    "\n[B] What the M_Kaup ~ M_crit coincidence ACTUALLY is (dimensional, not causal):"
)
MK = 0.633 * MPL**2 / M_PHI * GEV_KG
print(
    f"    M_Kaup(m_phi) = {MK:.2e} kg = {MK/MCRIT:.1f} M_crit ; both = Mpl^2/(O(1) m), m~1/L."
)
print(
    "    TRUE as a scale identity (a Kaup-mass boson star, IF one formed, would collapse"
)
print(
    "    to r_s ~ L = the GL threshold). NOT a genesis: forming an M_Kaup soliton needs"
)
print(
    "    hierarchical growth from ~1e4 kg seeds to ~1e20 kg — 16 decades, unquantified."
)
print(
    "    So: a structural consistency of SCALES (real, elegant), not a derivation of pegs."
)

print("\n[C] What SURVIVES, honestly:")
print(
    "    (1) Gate 10's misalignment number stands: a coherent radion condensate carries"
)
print(
    "        Omega h^2 = 0.12 at phi0=0.26 Ms (or 1% at 0.026 Ms) — within OBT's derived"
)
print(
    "        scales, axion-angle epistemics. A real candidate for SOME of the budget."
)
print(
    "    (2) Gate 11's galactic kill stands: an all-DM 0.36-eV condensate halos galaxies"
)
print(
    "        (dead x25). So the condensate is at most a sub-dominant coherent component."
)
print(
    "    (3) RETRACTED: the condensate = PBH-peg progenitor. The pegs keep their V8.2"
)
print(
    "        origin (inflationary small-scale spike, an INPUT). Condensate and pegs are"
)
print("        SEPARATE sectors; no unification claimed.")
print(
    "    (4) OPEN TENSION (named): if the condensate is the ~1% 'tent-peg' budget, it is"
)
print(
    "        DIFFUSE (coherent field), so it does NOT provide the capillary/ER=EPR/Gamma_rad"
)
print(
    "        roles the discrete PBH pegs play. Replacing pegs with condensate would orphan"
)
print(
    "        the dissipation mechanism. => the condensate ADDS to, not replaces, the pegs."
)

print("\n[SYNTHESIS — the audit strengthens by subtracting]:")
print(
    "    Gate 12 is an AUDIT gate. It kills Gate 11's prettiest corollary (PBH genesis"
)
print(
    "    from the condensate) by a clean 12-16 order magnitude calc, keeping the sacred"
)
print(
    "    files free of a false unification. The scale-identity M_Kaup~M_crit~Mpl^2/m is"
)
print(
    "    real but dimensional. The program's load-bearing V9.0 object is UNCHANGED and"
)
print(
    "    re-sharpened: the cluster-selective Weyl-DM is a RESPONSE sourced where the boost"
)
print(
    "    dies (the sinc anatomy), not a bulk substance and not the condensate. The door to"
)
print(
    "    the bulk is still the nonlinear response solve — now with one false key discarded."
)
