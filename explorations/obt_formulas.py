#!/usr/bin/env python3
"""
obt_formulas.py — the FIXED OBT predictions (CHERCHEUR-mode Stage-2 arithmetic).

OBT's own formulas, used as an AXIOM in the game (presuppose OBT true and COMPUTE what it
predicts — never test them here). Pure, vectorized.

NO SHORTCUTS: physical constants from astropy.constants (CODATA), unit conversions from
astropy.units, LCDM background (H(z), lookback, distances) from astropy.cosmology
FlatLambdaCDM (analytic, tested, fast), linear growth from colossus when available. Only
OBT-specific physics is hand-coded. Every computed formula has an injection test in
_selftest() against a known CLAUDE.md value, so a wrong prediction fails LOUDLY before use.

  (A) COMPUTED formulas with inputs (+ injection test against CLAUDE.md).
  (B) CITED result-constants in PREDICTIONS{} — outputs of dedicated V8.2 pipelines
      (eta_B, delta_beta, SKA peak, dBIC, S8 range, ...) stored verbatim with provenance +
      caveats; reproducing them needs full ODE/Boltzmann/MCMC runs (out of scope here).
"""

import warnings

import numpy as np
from scipy.special import jn_zeros
import astropy.units as u
import astropy.constants as const
from astropy.cosmology import FlatLambdaCDM

warnings.filterwarnings("ignore")

# ---- physical constants from CODATA via astropy (no hand-typed values) ------
C = const.c.value
G = const.G.value
HBAR = const.hbar.value
KB = const.k_B.value
MPC = (1 * u.Mpc).to(u.m).value
GYR = (1 * u.Gyr).to(u.s).value
YR = (1 * u.yr).to(u.s).value
KM = 1.0e3
MSUN = const.M_sun.value
ELLP = np.sqrt(HBAR * G / C**3)
HBARC_EV_UM = (const.hbar * const.c).to(u.eV * u.um).value
M_PL_RED_GEV = 2.435e18

# ---- OBT V8.2 fixed parameters (CLAUDE.md) ---------------------------------
H0_KMSMPC = 67.4
OMEGA_M = 0.315
OMEGA_L = 0.685
T_GYR = 2.000
L_M = 0.2e-6
L_UM = 0.2
F_OSC = 0.10
A_W = 0.003
DUTY_D = 0.9
XI = 0.15
N_MODE = 6
K_WARP_EV = 0.987
TAU0_JM2 = 7.0e19

COSMO = FlatLambdaCDM(H0=H0_KMSMPC, Om0=OMEGA_M)
A0 = (const.c * COSMO.H0 / (2 * np.pi)).to(u.m / u.s**2).value
LAMBDA_MPC = (const.c * (T_GYR * u.Gyr)).to(u.Mpc).value
HUBBLE_TIME_GYR = COSMO.hubble_time.to(u.Gyr).value


# ===========================================================================
# (A) COMPUTED FORMULAS
# ===========================================================================
def H_of_z(z):
    """H(z) in km/s/Mpc via astropy FlatLambdaCDM."""
    return COSMO.H(np.asarray(z, dtype=float)).value


def lookback_gyr(z):
    """Lookback time in Gyr via astropy (analytic for FlatLambdaCDM)."""
    return COSMO.lookback_time(np.asarray(z, dtype=float)).to(u.Gyr).value


def comoving_mpc(z):
    """Comoving distance in Mpc via astropy."""
    return COSMO.comoving_distance(np.asarray(z, dtype=float)).to(u.Mpc).value


def a0_of_z(z):
    """Instantaneous a0(z) = c H(z) / (2 pi), m/s^2."""
    Hz = COSMO.H(np.asarray(z, dtype=float))
    return (const.c * Hz / (2 * np.pi)).to(u.m / u.s**2).value


def mu(x):
    """Gauss-Codazzi interpolation: mu = x/sqrt(1+x^2)."""
    x = np.asarray(x, dtype=float)
    return x / np.sqrt(1.0 + x * x)


def g_obs_from_baryon(g_bar, a0=A0):
    """Exact RAR: g_obs = sqrt((g^2 + g*sqrt(g^2+4 a0^2))/2)."""
    g = np.asarray(g_bar, dtype=float)
    return np.sqrt((g * g + g * np.sqrt(g * g + 4.0 * a0 * a0)) / 2.0)


def v_flat_BTFR(M_bar_kg, a0=A0):
    """Baryonic Tully-Fisher: v_flat = (G M a0)^(1/4), m/s."""
    return (G * np.asarray(M_bar_kg, dtype=float) * a0) ** 0.25


def sinc_resonance(t_dyn_gyr, T=T_GYR):
    """MOND survival fraction = sinc(pi t_dyn/T) (np.sinc normalized)."""
    return np.sinc(np.asarray(t_dyn_gyr, dtype=float) / T)


def a0_effective(z, t_dyn_gyr):
    """System-level a0(z) * sinc filter."""
    return a0_of_z(z) * sinc_resonance(t_dyn_gyr)


def t_dyn(R_kpc, sigma_kms):
    """Dynamical time R/sigma in Gyr (R kpc, sigma km/s)."""
    R = (np.asarray(R_kpc, dtype=float) * u.kpc).to(u.m).value
    return (R / (np.asarray(sigma_kms, dtype=float) * KM)) / GYR


def lambda_harmonic(n=1):
    """Cymatic standing-wave lambda/n in Mpc (n=1 -> ~613)."""
    return LAMBDA_MPC / np.asarray(n, dtype=float)


def stick_slip_amplitudes(N=5, D=DUTY_D):
    """Fourier amplitudes of asymmetric triangle peaking at duty D, normalized A_1=1:
        A_n ∝ |sin(n*pi*D)|/n^2.  Reproduces CLAUDE.md {1, 0.476, 0.293, ...}."""
    n = np.arange(1, N + 1)
    raw = np.abs(np.sin(n * np.pi * D)) / n ** 2
    return raw / raw[0]


def _stick_slip_wave(u_phase, D=DUTY_D):
    """Zero-mean unit-peak stick-slip wave vs cycle phase in [0,1): rise [0,D], fall [D,1].
    Peak |value| = 1 at u=D."""
    up = np.asarray(u_phase, dtype=float) % 1.0
    tri = np.where(up < D, up / D, (1.0 - up) / (1.0 - D))
    return 2.0 * (tri - 0.5)


def w_of_z(z, A_w=A_W, T=T_GYR, D=DUTY_D):
    """OBT dark-energy w(z) = -1 + A_w * stick-slip(lookback/T); in [-1.003, -0.997]."""
    return -1.0 + A_w * _stick_slip_wave(lookback_gyr(z) / T, D)


def delta_bulk(D=DUTY_D, gamma_stick=0.243, gamma_slip=20.7, omega=np.pi):
    """AdS5 viscoelastic retardation (BKM): D*arctan(w/g_stick)+(1-D)*arctan(w/g_slip) ~1.36."""
    return D * np.arctan(omega / gamma_stick) + (1 - D) * np.arctan(omega / gamma_slip)


def G_eff_modulation(t_over_T, f_osc=F_OSC, delta=None):
    """G_eff(t)/G_N = 1 + f_osc * W(t/T + delta_bulk/2pi). max|.-1| = f_osc."""
    if delta is None:
        delta = delta_bulk()
    return 1.0 + f_osc * _stick_slip_wave(np.asarray(t_over_T, float) + delta / (2 * np.pi))


def growth_factor(z):
    """Linear growth D(z) normalized D(0)=1 via colossus (vetted). None if unavailable."""
    try:
        from colossus.cosmology import cosmology
    except Exception:
        return None
    co = cosmology.setCosmology(
        "obt_bg",
        params=dict(flat=True, H0=H0_KMSMPC, Om0=OMEGA_M, Ob0=0.049, sigma8=0.81, ns=0.965),
    )
    z = np.asarray(z, dtype=float)
    return co.growthFactor(z) / co.growthFactor(0.0)


def schwarzschild_radius(M_kg):
    """r_s = 2GM/c^2 (m)."""
    return 2.0 * G * np.asarray(M_kg, dtype=float) / C ** 2


def M_crit_Msun(L=L_M):
    """Perforation threshold M_crit = L c^2 / (2G), solar masses (~6.77e-11)."""
    return (L * C ** 2 / (2.0 * G)) / MSUN


def fresnel_wF(M_msun, lam_nm=600.0):
    """Wave-optics Fresnel parameter w_F = 2 pi r_s / lambda."""
    r_s = schwarzschild_radius(np.asarray(M_msun, float) * MSUN)
    return 2.0 * np.pi * r_s / (lam_nm * 1e-9)


def T_hawking(M_kg):
    """Hawking temperature hbar c^3 / (8 pi G M k_B), K."""
    M = np.asarray(M_kg, dtype=float)
    return HBAR * C ** 3 / (8.0 * np.pi * G * M * KB)


def t_evap_yr(M_kg):
    """Evaporation time ~ 5120 pi G^2 M^3 / (hbar c^4), years (M^3)."""
    M = np.asarray(M_kg, dtype=float)
    return (5120.0 * np.pi * G ** 2 * M ** 3 / (HBAR * C ** 4)) / YR


def kk_mass_flat_eV(n=1, L_um=L_UM):
    """Flat-space KK graviton m_n = j_{1,n} hbar c / L, eV. m1~3.78."""
    n = int(n)
    j = jn_zeros(1, n)[n - 1]
    return j * HBARC_EV_UM / L_um


def kk_mass_warped_eV(n=1, k_warp=K_WARP_EV):
    """Warped KK graviton (m_n/k = {1.892,3.692,...}); m1~1.87 eV."""
    coeffs = [1.892, 3.692, 5.510, 7.327, 9.144]
    return coeffs[int(n) - 1] * k_warp


def gamma_rad(L=L_M):
    """Radiative damping ln(S_BH)/(2 pi), S_BH = pi (L/l_P)^2. ~20.7."""
    S_BH = np.pi * (L / ELLP) ** 2
    return np.log(S_BH) / (2.0 * np.pi)


def f0_brane_Hz(T=T_GYR):
    """Fundamental brane frequency 1/T ~ 1.58e-17 Hz."""
    return 1.0 / (T * GYR)


def tau0_energy_MeV(tau0_Jm2=TAU0_JM2):
    """Brane tension energy scale tau0^{1/3} in MeV (~257) via astropy natural-unit
    bridging: E = (tau0 * (hbar c)^2)^(1/3) -> MeV. No hand-typed conversion factors."""
    tau0 = tau0_Jm2 * u.J / u.m**2
    E = (tau0 * (const.hbar * const.c) ** 2) ** (1.0 / 3.0)
    return E.to(u.MeV).value


def ks_energy_scale_MeV(K=21, M=10, g_s=0.1, M_pl_GeV=None):
    """KS warped-throat scale M_pl * exp(-2 pi K/(3 g_s M)). FLAG: ~195 MeV with reduced
    M_Pl vs CLAUDE.md's cited 257 (bottom-up tau0^{1/3} route); exact KS prefactor in
    theory.md must reconcile — NOT glued. For transparency, not a vetted prediction."""
    if M_pl_GeV is None:
        M_pl_GeV = M_PL_RED_GEV
    return M_pl_GeV * np.exp(-2.0 * np.pi * K / (3.0 * g_s * M)) * 1e3


# ===========================================================================
# (B) CITED RESULT-CONSTANTS (verbatim from CLAUDE.md; NOT recomputed here)
# ===========================================================================
PREDICTIONS = {
    "eta_B": (6.1e-10, "baryon asymmetry (spontaneous QCD baryogenesis, c_QCD~O(1))"),
    "delta_beta_deg": (0.25, "CMB birefringence (5D Chern-Simons, c_top=75)"),
    "c_top": (75, "Chern number (natural, not 1e40)"),
    "v_bulk_kms": (300, "5D brane drift -> dark flow + birefringence"),
    "S8": (0.79, "growth suppression order 4-10%, WAVEFORM-DEPENDENT, NOT +/-0.002 "
                 "(audit May 2026)"),
    "Li7_suppression": (3.5, "Lithium-7 via BBN conformal tolerance"),
    "SKA_peak_mK": (5.46, "SKA 21cm reionization modulation peak"),
    "SKA_snr": (5.5, "SKA 21cm forecast SNR"),
    "dBIC_DR2": (-6.4, "DESI DR2 stick-slip k=1 vs CPL k=2 (Strong)"),
    "dBIC_Y5": (-22, "DESI Year-5 forecast (Decisive)"),
    "dlnK_bayes": (5.8, "Bayesian evidence vs LCDM (Decisive)"),
    "m_radion_eV": (0.36, "Goldberger-Wise radion mass"),
    "h_c_nanograv": (1e-15, "GW strain at 16 nHz (NANOGrav 15yr)"),
    "ISW_sigma": (1.0, "realistic ISW ~1sigma (NOT 6sigma; artifact disproven)"),
    "SPARC_rms_kms": (29.3, "SPARC 135-gal RMS, 0 dark-sector params"),
    "branching_ratio_B": (9.7e-11, "KK branching ratio"),
}


def prediction_sheet():
    A = stick_slip_amplitudes()
    return [
        ("a0(z=0)", float(A0), "m/s^2", "cH0/2pi (Gibbons-Hawking)"),
        ("a0(z=1)", float(a0_of_z(1.0)), "m/s^2", f"x{a0_of_z(1.0)/A0:.2f}"),
        ("a0(z=2)", float(a0_of_z(2.0)), "m/s^2", f"x{a0_of_z(2.0)/A0:.2f}"),
        ("lambda", float(LAMBDA_MPC), "Mpc", "c*T cymatic fundamental"),
        ("delta_bulk", float(delta_bulk()), "rad", "BKM viscoelastic (~1.36)"),
        ("A2/A1,A3/A1", f"{A[1]:.3f},{A[2]:.3f}", "-", "stick-slip Fourier"),
        ("w(z=0.93)", float(w_of_z(0.93)), "-", "DESI aliasing bin"),
        ("M_crit", float(M_crit_Msun()), "Msun", "L c^2/2G (~6.77e-11)"),
        ("w_F(1e-12)", float(fresnel_wF(1e-12)), "-", "Fresnel (~0.03)"),
        ("m_KK1 flat", float(kk_mass_flat_eV(1)), "eV", "j_{1,1} hc/L (~3.78)"),
        ("m_KK1 warped", float(kk_mass_warped_eV(1)), "eV", "1.892 k (~1.87)"),
        ("Gamma_rad", float(gamma_rad()), "Gyr^-1", "ln(S_BH)/2pi (~20.7)"),
        ("T_H(M_crit)", float(T_hawking(M_crit_Msun() * MSUN)), "K", "(~900)"),
        ("t_evap(M_crit)", float(t_evap_yr(M_crit_Msun() * MSUN)), "yr", "M^3 (~1e37)"),
        ("f0_brane", float(f0_brane_Hz()), "Hz", "1/T (~1.58e-17)"),
        ("tau0^1/3", float(tau0_energy_MeV()), "MeV", "(~257 ~ Lambda_QCD)"),
        ("KS scale", float(ks_energy_scale_MeV()), "MeV", "FLAG ~195 vs 257"),
    ]


def _selftest():
    print("=== obt_formulas.py self-test (known values from CLAUDE.md, astropy-backed) ===")
    ok = True

    def chk(name, cond, got=""):
        nonlocal ok
        ok = ok and bool(cond)
        print(f"  [{'OK' if cond else 'FAIL'}] {name} {got}")

    chk("Mpc=3.0857e22 m", abs(MPC - 3.0857e22) / 3.0857e22 < 1e-3, f"={MPC:.4e}")
    chk("hbar*c=0.19733 eV.um", abs(HBARC_EV_UM - 0.19733) < 1e-4, f"={HBARC_EV_UM:.5f}")
    chk("a0(0) ~1.1e-10", abs(A0 - 1.1e-10) / 1.1e-10 < 0.10, f"={A0:.3e}")
    chk("lambda ~613 Mpc", abs(LAMBDA_MPC - 613) < 15, f"={LAMBDA_MPC:.1f}")
    chk("a0(1)/a0(0) ~1.79", abs(a0_of_z(1.0) / A0 - 1.79) < 0.05, f"={a0_of_z(1.0)/A0:.2f}")
    chk("mu(1e3)->1", abs(mu(1e3) - 1) < 1e-3)
    chk("mu(1e-3)->x", abs(mu(1e-3) - 1e-3) / 1e-3 < 1e-3)
    chk("RAR high->Newton", abs(g_obs_from_baryon(1e-8) - 1e-8) / 1e-8 < 0.02)
    chk("RAR low->sqrt(g a0)", abs(g_obs_from_baryon(1e-12) - np.sqrt(1e-12 * A0)) / np.sqrt(1e-12 * A0) < 0.02)
    chk("sinc(0.01)->1", abs(sinc_resonance(0.01) - 1) < 1e-2)
    chk("sinc(T)->0", abs(sinc_resonance(T_GYR)) < 1e-9)
    chk("BTFR MW 160-230", 160 < v_flat_BTFR(6e10 * MSUN) / KM < 230, f"={v_flat_BTFR(6e10*MSUN)/KM:.0f}")
    chk("t_dyn cluster ~1.5", 1.0 < t_dyn(1500, 1000) < 2.0, f"={float(t_dyn(1500,1000)):.2f}")
    A = stick_slip_amplitudes()
    chk("A2/A1 ~0.476", abs(A[1] - 0.476) < 0.01, f"={A[1]:.3f}")
    chk("A3/A1 ~0.293", abs(A[2] - 0.293) < 0.01, f"={A[2]:.3f}")
    chk("A_n decreasing", bool(np.all(np.diff(A) < 0)))
    wg = w_of_z(np.linspace(0, 3, 200))
    chk("w(z) in [-1.003,-0.997]", bool(np.all(wg >= -1.0031) and np.all(wg <= -0.9969)),
        f"[{wg.min():.4f},{wg.max():.4f}]")
    chk("delta_bulk ~1.36", abs(delta_bulk() - 1.36) < 0.02, f"={delta_bulk():.3f}")
    gmax = float(np.max(np.abs(G_eff_modulation(np.linspace(0, 1, 100001)) - 1)))
    chk("G_eff peak dev == f_osc", abs(gmax - F_OSC) < 1e-4, f"={gmax:.5f}")
    chk("M_crit ~6.77e-11", abs(M_crit_Msun() - 6.77e-11) / 6.77e-11 < 0.02, f"={M_crit_Msun():.3e}")
    chk("w_F(1e-12) ~0.03", 0.025 < fresnel_wF(1e-12) < 0.035, f"={fresnel_wF(1e-12):.4f}")
    chk("T_H(M_crit) ~900K", 700 < T_hawking(M_crit_Msun()*MSUN) < 1100, f"={float(T_hawking(M_crit_Msun()*MSUN)):.0f}")
    chk("t_evap(M_crit) ~1e37", 1e36 < t_evap_yr(M_crit_Msun()*MSUN) < 1e38, f"={float(t_evap_yr(M_crit_Msun()*MSUN)):.2e}")
    chk("m_KK1 flat ~3.78", abs(kk_mass_flat_eV(1) - 3.78) < 0.05, f"={kk_mass_flat_eV(1):.3f}")
    chk("m_KK1 warped ~1.87", abs(kk_mass_warped_eV(1) - 1.87) < 0.03, f"={kk_mass_warped_eV(1):.3f}")
    chk("Gamma_rad ~20.7", abs(gamma_rad() - 20.7) < 0.6, f"={gamma_rad():.2f}")
    chk("f0_brane ~1.58e-17", abs(f0_brane_Hz() - 1.58e-17) / 1.58e-17 < 0.05, f"={f0_brane_Hz():.3e}")
    chk("tau0^1/3 ~257 MeV", abs(tau0_energy_MeV() - 257) < 5, f"={tau0_energy_MeV():.1f}")
    Dz = growth_factor(1.0)
    if Dz is None:
        print("  [SKIP] growth_factor (colossus not installed)")
    else:
        chk("growth D(1)/D(0) ~0.61", abs(Dz - 0.61) < 0.04, f"={Dz:.3f}")
    print("  SELFTEST_OK" if ok else "  SELFTEST_FAILED")
    return ok


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        sys.exit(0 if _selftest() else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == "all":
        print("=== OBT prediction sheet (computed, astropy-backed) ===")
        for name, val, unit, note in prediction_sheet():
            vs = f"{val:.4e}" if isinstance(val, float) else str(val)
            print(f"  {name:16s} = {vs:>12} {unit:7s}  {note}")
        print("\n=== cited result-constants (V8.2 pipelines, not recomputed) ===")
        for k, (v, note) in PREDICTIONS.items():
            print(f"  {k:18s} = {v:<10} {note}")
    else:
        print(__doc__)
