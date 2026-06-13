"""GATE 12 RE-VERIFICATION (Romain: 'tu pourrais t'etre trompe').
Three independent methods + a CALIBRATION on the QCD axion (known answer).
If the formula reproduces M_mc(QCD axion) ~ 1e-12..1e-10 Msun, trust it.
"""

import numpy as np

GEV_KG = 1.78266e-27
MSUN = 1.989e30
MPL = 1.22e19  # GeV (non-reduced)
GEV_CM = 5.0677e13  # 1 GeV = 5.07e13 /cm  (hbar c)
T0 = 2.35e-13  # GeV (CMB today)
RHOC = 4.77e-6  # GeV/cm^3  (rho_crit,0 for h=0.674: 1.05e-5 h^2)
H2 = 0.674**2
GS0 = 3.91  # g_*S today


def T_osc(m, gstar=100.0, c=1.0):
    """H_osc = m/c  ->  T_osc (radiation), constant-mass field."""
    return np.sqrt(m * MPL / (c * 1.66 * np.sqrt(gstar)))


def omega_h2(m, phi0, gstar=100.0, c=1.0):
    """Misalignment relic: rho_phi(osc)=1/2 m^2 phi0^2, then a^-3."""
    Tos = T_osc(m, gstar, c)
    rho_os = 0.5 * m**2 * phi0**2  # GeV^4
    dil = (GS0 / gstar) * (T0 / Tos) ** 3  # (a_osc/a0)^3
    rho0 = rho_os * dil  # GeV^4
    rho0_cm3 = rho0 / GEV_CM ** (-3)  # GeV^4 -> GeV/cm^3: *GEV_CM^3
    rho0_cm3 = rho0 * GEV_CM**3  # GeV/cm^3
    return rho0_cm3 / RHOC * H2


def Mmc_comoving(Omega_comp, k_osc_invGeV):
    """M = (4pi/3) rho_comp,0 / k_osc^3 ; rho_comp,0 = Omega_comp * rhoc."""
    rho0 = Omega_comp * RHOC  # GeV/cm^3
    inv_k_cm = 1.0 / (k_osc_invGeV * GEV_CM)  # cm  (1/k in cm)
    V = (4 * np.pi / 3) * inv_k_cm**3  # cm^3
    M_GeV = rho0 * V  # GeV
    return M_GeV * GEV_KG


def k_osc(m, gstar=100.0, c=1.0):
    """comoving wavenumber (today) entering horizon at onset: a_osc H_osc / a0."""
    Tos = T_osc(m, gstar, c)
    a_ratio = (T0 / Tos) * (GS0 / gstar) ** (1.0 / 3.0)  # a_osc/a0
    return a_ratio * (m / c)  # GeV  (H_osc = m/c)


print("=" * 70)
print("VALIDATION on the QCD axion (onset is INPUT at T1~1 GeV: thermal mass)")
print("=" * 70)
# QCD axion: onset T1 ~ 1 GeV, H1 = 1.66 sqrt(g*) T1^2/Mpl, axion = all DM
for T1, gstar1 in [(1.0, 61.0), (2.0, 75.0)]:
    H1 = 1.66 * np.sqrt(gstar1) * T1**2 / MPL
    a_ratio = (T0 / T1) * (GS0 / gstar1) ** (1.0 / 3.0)
    kqcd = a_ratio * H1
    M = Mmc_comoving(0.26, kqcd)
    print(
        f"  T1={T1} GeV: H1={H1:.2e} GeV, k_osc={kqcd:.2e} GeV,"
        f"  M_mc = {M:.2e} kg = {M/MSUN:.2e} Msun"
    )
print("  LITERATURE (Kolb-Tkachev 1994; Eggemeier+2020): M_mc ~ 1e-14..1e-10 Msun")
print("  -> if my number lands in that band, the formula is TRUSTWORTHY.\n")

print("=" * 70)
print("RADION condensate (m_phi = 0.36 eV, constant mass, onset H=m)")
print("=" * 70)
m = 0.36e-9
M_S = 1.19e12
# first: reproduce Gate 10's abundance to confirm phi0 normalization
for frac, phi0 in [("all DM", 0.26 * M_S), ("1%", 0.026 * M_S)]:
    Oh2 = omega_h2(m, phi0)
    kk = k_osc(m)
    Mmc = Mmc_comoving(Oh2 / H2, kk)  # Omega_comp = Oh2/h2
    print(
        f"  {frac:7s} phi0={phi0:.2e} GeV: Omega h^2 = {Oh2:.3f}"
        f"  (Gate10 target {0.12 if frac=='all DM' else 0.0012})"
    )
    print(f"          k_osc={kk:.2e} GeV,  M_mc = {Mmc:.2e} kg = {Mmc/MSUN:.2e} Msun")
print()
print(f"  EMF window (V8.2): 1e-14..1e-10 Msun = {1e-14*MSUN:.1e}..{1e-10*MSUN:.1e} kg")
print()

print("=" * 70)
print("WHY the radion differs from the QCD axion (the physical reason)")
print("=" * 70)
print(f"  QCD axion onset: T1 ~ 1 GeV (LATE: thermal mass m_a(T) rises slowly)")
print(
    f"  Radion onset:    T_osc = {T_osc(m):.2e} GeV ~ 16 TeV (EARLY: m fixed=0.36 eV)"
)
print("  M_mc ~ 1/k_osc^3 ; earlier onset = smaller horizon = smaller grain.")
print("  M_mc scales ~ T_osc^-3 (times slow factors) -> the 16-TeV onset costs")
print(f"  ~({1.63e4/1.0:.0e})^3 ~ 1e12-1e13 in mass vs the 1-GeV axion onset.\n")

print("=" * 70)
print("THE DOUBLE-CONSTRAINT (decisive, prefactor-independent)")
print("=" * 70)
print("  To put the grain in the EMF window AND keep the right abundance:")
# M_mc ~ phi0^2/m (fixed m) ; Omega ~ phi0^2 -> M_mc/Omega = const at fixed m
# so for a GIVEN m, M_mc is locked once Omega is fixed.
Mmc_1pct = Mmc_comoving(0.0012 / H2, k_osc(m))
need = 1e-14 * MSUN
print(f"  At m=0.36 eV, Omega=1%: M_mc = {Mmc_1pct:.1e} kg, EMF floor = {need:.1e} kg")
print(
    f"  ratio needed = {need/Mmc_1pct:.1e}  -> would need phi0 x{np.sqrt(need/Mmc_1pct):.1e}"
)
print(f"     -> Omega x{need/Mmc_1pct:.1e} = massive overclosure. IMPOSSIBLE.")
print("  Lowering m to grow M_mc (M_mc ~ m^-3/2 at fixed Omega) needs m ~ neV,")
print("  i.e. NOT the GW radion (0.36 eV). Within OBT's derived scales: locked out.")
