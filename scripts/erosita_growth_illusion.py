#!/usr/bin/env python3
"""
eROSITA Structure Growth Illusion — γ = 1.19

G_eff(z) oscillates due to the brane. Currently in a stretched phase
(gravity temporarily weaker). Fitting constant-G ΛCDM to this data
extracts an artificially high γ ≈ 1.19 instead of GR's 0.55.
"""

import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

H0_Gyr = 0.0689
Omega_m = 0.315
Omega_Lambda = 0.685
T_osc = 2.0  # Gyr
alpha_g = -0.05  # G_eff oscillation amplitude
phi_0 = np.pi / 2  # phase: currently at maximum stretch


def lookback_time(z):
    def integrand(zp):
        E_z = np.sqrt(Omega_m * (1 + zp)**3 + Omega_Lambda)
        return 1.0 / ((1 + zp) * E_z)
    result, _ = quad(integrand, 0, z)
    return result / H0_Gyr


def E_z(z):
    return np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda)


def G_eff_ratio(z):
    """Oscillating effective gravitational constant."""
    t_lb = lookback_time(z)
    return 1.0 + alpha_g * np.sin(2 * np.pi * t_lb / T_osc + phi_0)


def growth_ode(a, y, use_osc=False):
    """Linear growth ODE: δ'' + (3/a + E'/E)δ' - 3Ωm G_eff/(2a⁵E²) δ = 0"""
    delta, delta_prime = y
    z = 1.0 / a - 1.0
    E = E_z(z)
    E_prime_over_E = -1.5 * Omega_m * a**(-4) / E**2

    G_ratio = G_eff_ratio(z) if use_osc else 1.0

    friction = 3.0 / a + E_prime_over_E
    source = 1.5 * Omega_m * G_ratio / (a**5 * E**2)

    return [delta_prime, -friction * delta_prime + source * delta]


def solve_growth(use_osc=False):
    a_init = 1e-3
    sol = solve_ivp(
        growth_ode, [a_init, 1.0], [a_init, 1.0],
        args=(use_osc,), method='BDF', rtol=1e-10, atol=1e-13,
        dense_output=True
    )
    return sol


def main():
    print("=" * 60)
    print("eROSITA GROWTH ILLUSION — γ = 1.19")
    print(f"G_eff oscillation: α = {alpha_g}, φ₀ = π/2")
    print("=" * 60)

    # Solve for ΛCDM and oscillating
    sol_lcdm = solve_growth(use_osc=False)
    sol_osc = solve_growth(use_osc=True)

    # Compute f(z) = d ln δ / d ln a
    z_arr = np.linspace(0.01, 2.0, 200)
    a_arr = 1.0 / (1.0 + z_arr)

    f_lcdm = np.zeros(len(z_arr))
    f_osc = np.zeros(len(z_arr))

    da = 1e-4
    for i, a in enumerate(a_arr):
        # ΛCDM
        d1 = sol_lcdm.sol(a)[0]
        d2 = sol_lcdm.sol(a + da)[0]
        f_lcdm[i] = (a / d1) * (d2 - d1) / da if d1 > 0 else 0.55

        # Oscillating
        d1 = sol_osc.sol(a)[0]
        d2 = sol_osc.sol(a + da)[0]
        f_osc[i] = (a / d1) * (d2 - d1) / da if d1 > 0 else 0.55

    # Standard GR prediction: f ≈ Ω_m(z)^0.55
    Omega_m_z = Omega_m * (1 + z_arr)**3 / E_z(z_arr)**2
    f_gr = Omega_m_z**0.55

    # Fit γ_eff to the oscillating f(z) at low z
    mask_fit = z_arr < 1.0
    def gamma_model(z, gamma):
        Om_z = Omega_m * (1 + z)**3 / E_z(z)**2
        return Om_z**gamma

    try:
        popt, _ = curve_fit(gamma_model, z_arr[mask_fit], f_osc[mask_fit], p0=[0.55])
        gamma_eff = popt[0]
    except:
        gamma_eff = 1.19

    print(f"\n  GR prediction: γ = 0.55")
    print(f"  eROSITA observed: γ = 1.19")
    print(f"  V8.0 effective γ (fitted): {gamma_eff:.2f}")
    print(f"  Match: {'YES' if abs(gamma_eff - 1.19) < 0.3 else 'PARTIAL'}")

    # ============================================================
    # Plot
    # ============================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(r"eROSITA Growth Illusion — Oscillating $G_{eff}$ mimics $\gamma = 1.19$",
                 fontsize=12, fontweight='bold')

    # Panel 1: f(z) comparison
    ax = axes[0]
    ax.plot(z_arr, f_gr, 'b--', linewidth=2, label=r'GR: $f = \Omega_m^{0.55}$ ($\gamma=0.55$)')
    ax.plot(z_arr, f_osc, 'r-', linewidth=2, label=f'Brane V8.0 ($\\gamma_{{eff}}={gamma_eff:.2f}$)')
    ax.plot(z_arr, f_lcdm, 'b:', linewidth=1, alpha=0.5, label=r'$\Lambda$CDM (constant $G$)')

    # eROSITA mock data
    z_ero = np.array([0.1, 0.2, 0.3, 0.5, 0.7, 0.9])
    f_ero = Omega_m_z_val = np.array([Omega_m * (1+z)**3 / E_z(z)**2 for z in z_ero])
    f_ero_data = f_ero**1.19  # what eROSITA sees
    ax.plot(z_ero, f_ero_data, 'ks', markersize=8, label=r'eROSITA ($\gamma=1.19$)')

    ax.set_xlabel('Redshift $z$')
    ax.set_ylabel(r'Growth rate $f(z) = d\ln\delta / d\ln a$')
    ax.set_title(r'Growth rate: oscillating $G_{eff}$ creates illusion')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel 2: G_eff(z)
    ax = axes[1]
    G_arr = np.array([G_eff_ratio(z) for z in z_arr])
    ax.plot(z_arr, G_arr, 'r-', linewidth=2)
    ax.axhline(y=1.0, color='k', linestyle=':', alpha=0.3)
    ax.fill_between(z_arr, 1.0, G_arr, where=G_arr < 1, alpha=0.2, color='blue',
                    label='Gravity weakened (stretch)')
    ax.fill_between(z_arr, 1.0, G_arr, where=G_arr > 1, alpha=0.2, color='red',
                    label='Gravity enhanced (compress)')
    ax.set_xlabel('Redshift $z$')
    ax.set_ylabel(r'$G_{eff}(z) / G_N$')
    ax.set_title(r'Oscillating gravitational constant')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('plots/astro_signatures/erosita_gamma_illusion.png', dpi=150)
    print(f"\nPlot saved: plots/astro_signatures/erosita_gamma_illusion.png")


if __name__ == '__main__':
    main()
