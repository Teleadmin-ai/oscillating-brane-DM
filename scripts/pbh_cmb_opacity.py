#!/usr/bin/env python3
"""
PBH Impact on CMB Optical Depth
===============================

Calculate the contribution of primordial black holes (PBH) to the
CMB optical depth τ and compare with Planck constraints.

Based on literature:
- Ali-Haïmoud & Kamionkowski (2017) - PBH accretion effects
- Poulin et al. (2017) - CMB constraints on PBH
- Serpico et al. (2020) - Updated PBH constraints
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from scipy.special import erf

# Physical constants
c = 2.998e8  # m/s
G = 6.674e-11  # m³/kg/s²
M_sun = 1.989e30  # kg
pc = 3.086e16  # m
Mpc = 1e6 * pc
year = 365.25 * 24 * 3600  # s
Gyr = 1e9 * year

# Cosmological parameters
h = 0.674
H0 = h * 100 * 1e3 / Mpc  # s⁻¹
Omega_m = 0.315
Omega_b = 0.049
Omega_Lambda = 1 - Omega_m
rho_crit_0 = 3 * H0**2 / (8 * np.pi * G)  # kg/m³

# CMB parameters
z_reion = 7.67  # Planck 2018 reionization redshift
tau_planck = 0.054  # Planck 2018 optical depth
sigma_tau = 0.007  # Planck uncertainty

# Atomic parameters
sigma_T = 6.65e-29  # m² (Thomson cross section)
m_p = 1.673e-27  # kg (proton mass)
m_e = 9.109e-31  # kg (electron mass)


class PBHOpacity:
    """
    Calculate CMB optical depth from PBH accretion.
    """

    def __init__(self, f_pbh=0.01, M_pbh=1e-11, f_osc=0.10):
        """
        Initialize PBH parameters.

        Parameters
        ----------
        f_pbh : float
            Fraction of dark matter in PBHs
        M_pbh : float
            PBH mass in solar masses
        f_osc : float
            Oscillating fraction (affects accretion)
        """
        self.f_pbh = f_pbh
        self.M_pbh = M_pbh * M_sun  # Convert to kg
        self.f_osc = f_osc

        # Derived parameters
        self.n_pbh_0 = self._pbh_number_density()

    def _pbh_number_density(self):
        """Current PBH number density."""
        rho_dm_0 = (Omega_m - Omega_b) * rho_crit_0
        return self.f_pbh * rho_dm_0 / self.M_pbh

    def bondi_accretion_rate(self, z):
        """
        Bondi-Hoyle accretion rate.

        Based on Ali-Haïmoud & Kamionkowski (2017).
        """
        # Gas properties at redshift z
        T_gas = 2.73 * (1 + z)  # K (assumes no heating)
        if z < 200:
            # Post-decoupling temperature evolution
            T_gas = 2.73 * (1 + z) ** 2 / (1 + z / 200)

        # Sound speed
        c_s = np.sqrt(1.38e-23 * T_gas / m_p)  # m/s

        # Relative velocity (from structure formation)
        v_rel = 30e3 * np.sqrt(1 + z) / np.sqrt(1000)  # m/s

        # Effective velocity
        v_eff = np.sqrt(c_s**2 + v_rel**2)

        # Gas density
        rho_gas = Omega_b * rho_crit_0 * (1 + z) ** 3

        # Bondi radius
        r_B = G * self.M_pbh / v_eff**2

        # Accretion rate with suppression factor
        lambda_factor = np.exp(4.5 / (3 + (v_rel / c_s) ** 3))
        M_dot = 4 * np.pi * lambda_factor * (G * self.M_pbh) ** 2 * rho_gas / v_eff**3

        # Enhancement from oscillating brane
        if self.f_osc > 0:
            # Oscillations enhance local density contrasts
            enhancement = 1 + self.f_osc * np.sin(2 * np.pi * z / 50)
            M_dot *= enhancement

        return M_dot

    def luminosity_accretion(self, z):
        """
        Luminosity from accretion onto PBH.

        Assumes radiative efficiency η ~ 0.1.
        """
        eta = 0.1  # Radiative efficiency
        M_dot = self.bondi_accretion_rate(z)
        return eta * M_dot * c**2

    def ionization_rate(self, z):
        """
        Ionization rate from PBH accretion.

        Returns
        -------
        dn_e/dt : float
            Ionization rate in m⁻³ s⁻¹
        """
        # Number density of PBHs at redshift z
        n_pbh = self.n_pbh_0 * (1 + z) ** 3

        # Luminosity per PBH
        L_pbh = self.luminosity_accretion(z)

        # Average photon energy (assume blackbody at 10⁷ K)
        T_acc = 1e7  # K
        E_photon = 2.7 * 1.38e-23 * T_acc  # J

        # Ionization energy of hydrogen
        E_ion = 13.6 * 1.602e-19  # J

        # Efficiency of ionization (fraction of energy going to ionization)
        f_ion = 0.3

        # Ionization rate per hydrogen atom
        n_H = Omega_b * rho_crit_0 * (1 + z) ** 3 / m_p

        # Number of ionizations per second per volume
        n_ion_per_vol = f_ion * n_pbh * L_pbh / E_ion

        # Ionization rate per hydrogen atom (s^-1)
        ionization_rate = n_ion_per_vol / n_H

        return ionization_rate

    def optical_depth_pbh(self, z_min=0, z_max=30):
        """
        Calculate optical depth to CMB from PBH ionization.

        τ = ∫ n_e σ_T c dt = ∫ n_e σ_T c / (H(z)(1+z)) dz
        """
        # Calculate optical depth with proper normalization
        def integrand(z):
            # Total ionization fraction (standard + PBH)
            x_e = self._ionization_fraction(z)

            # Electron density
            n_H = Omega_b * rho_crit_0 * (1 + z) ** 3 / m_p
            n_e = x_e * n_H

            # Hubble parameter
            H_z = H0 * np.sqrt(Omega_m * (1 + z) ** 3 + Omega_Lambda)

            return n_e * sigma_T * c / (H_z * (1 + z))

        # Calculate total optical depth
        tau_total, _ = integrate.quad(integrand, z_min, z_max, limit=100)

        # Return total optical depth
        return tau_total

    def _ionization_fraction(self, z):
        """
        Ionization fraction including PBH contribution.

        Based on simplified Saha equation with PBH heating.
        """
        # Standard reionization (tanh model)
        Delta_z = 0.5
        x_e_std = 0.5 * (1 - np.tanh((z - z_reion) / Delta_z))

        # For high redshift, use recombination history
        if z > 1100:
            # Pre-recombination: fully ionized
            return 1.0
        elif z > 200:
            # During/after recombination
            # Residual ionization ~ 2e-4 at z=200
            x_e_residual = 2e-4 * (1 + z / 200) ** 2
            return x_e_residual
        elif z > z_reion + 2:
            # Dark ages - only PBH contribution
            # PBH ionization builds up slowly
            x_e_residual = 2e-4  # Background ionization
            
            # Use realistic accretion-based ionization
            if self.f_pbh > 0:
                # Calculate ionization rate from PBH accretion
                ion_rate = self.ionization_rate(z)
                # Approximate steady-state ionization fraction
                # Balance ionization and recombination
                alpha_rec = 2.6e-13 * (z/1000)**0.7  # cm³/s recombination coefficient
                n_H = Omega_b * rho_crit_0 * (1 + z) ** 3 / m_p  # m⁻³
                n_H_cgs = n_H * 1e-6  # cm⁻³
                x_e_pbh = ion_rate / (alpha_rec * n_H_cgs * 1e-6)  # Convert units
                x_e_pbh = min(x_e_pbh * self.f_pbh, 0.1)  # Cap at 10%
            else:
                x_e_pbh = 0
                
            return x_e_residual + x_e_pbh
        else:
            # Standard reionization dominates
            return x_e_std

    def tau_components(self):
        """
        Break down optical depth into components.
        """
        # Standard reionization without PBHs
        pbh_temp = self.f_pbh
        self.f_pbh = 0
        tau_std = self.optical_depth_pbh()
        self.f_pbh = pbh_temp

        # Total with PBH contribution
        tau_total = self.optical_depth_pbh()

        # PBH excess
        tau_pbh_only = tau_total - tau_std

        # Funnel enhancement (from oscillating brane model)
        tau_funnel = self._tau_funnel_enhancement()

        return {
            "standard": tau_std,
            "pbh": tau_pbh_only,
            "funnel": tau_funnel,
            "total": tau_total + tau_funnel,
        }

    def _tau_standard(self):
        """Standard optical depth without PBHs."""
        # Use Planck fitting formula
        return 0.054

    def _tau_funnel_enhancement(self):
        """
        Enhancement from PBH funnels in oscillating brane model.

        Based on increased local density from gravitational focusing.
        """
        # Funnel radius ~ Schwarzschild radius
        r_s = 2 * G * self.M_pbh / c**2

        # Enhancement volume fraction
        f_funnel = self.f_pbh * (r_s / (10 * pc)) ** 3 * 1e6  # Rough estimate

        # Enhanced ionization in funnels
        enhancement_factor = 10  # Density enhancement in funnels

        return self._tau_standard() * f_funnel * (enhancement_factor - 1)


def literature_constraints():
    """
    Compile constraints from literature.
    """
    constraints = {
        "Ali-Haimoud2017": {
            "M_pbh": np.logspace(-15, -9, 50),  # Solar masses
            "f_pbh_max": np.array(
                [
                    1e-3,
                    1e-3,
                    1e-3,
                    1e-3,
                    1e-3,  # Rough interpolation
                    1e-2,
                    1e-2,
                    1e-2,
                    1e-2,
                    1e-2,
                    1e-1,
                    1e-1,
                    1e-1,
                    1e-1,
                    1e-1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1e-1,
                    1e-1,
                    1e-1,
                    1e-1,
                    1e-1,
                    1e-2,
                    1e-2,
                    1e-2,
                    1e-2,
                    1e-2,
                    1e-3,
                    1e-3,
                    1e-3,
                    1e-3,
                    1e-3,
                    1e-4,
                    1e-4,
                    1e-4,
                    1e-4,
                    1e-4,
                    1e-5,
                    1e-5,
                    1e-5,
                    1e-5,
                    1e-5,
                ]
            ),
            "constraint": "CMB anisotropies",
        },
        "Serpico2020": {
            "M_pbh": np.array([1e-13, 1e-12, 1e-11, 1e-10, 1e-9]),
            "f_pbh_max": np.array([1e-2, 1e-2, 0.1, 0.3, 0.1]),
            "constraint": "CMB spectral distortions",
        },
        "Poulin2017": {
            "tau_excess_max": 0.012,  # Maximum excess optical depth
            "confidence": "95% CL",
            "constraint": "Planck τ measurement",
        },
    }

    return constraints


def plot_tau_vs_fpbh(M_pbh=1e-11, save_path="plots/tau_vs_fpbh.png"):
    """
    Plot optical depth as a function of PBH fraction.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    # Range of f_pbh to test
    f_pbh_array = np.logspace(-5, -1, 50)
    tau_array = []
    tau_pbh_array = []

    for f in f_pbh_array:
        pbh = PBHOpacity(f_pbh=f, M_pbh=M_pbh, f_osc=0.10)
        components = pbh.tau_components()
        tau_array.append(components["total"])
        tau_pbh_array.append(components["pbh"])

    # Plot results
    ax.semilogx(f_pbh_array, tau_array, "b-", linewidth=2, label="Total τ")
    ax.semilogx(
        f_pbh_array, [0.054] * len(f_pbh_array), "k--", label="Standard τ (no PBH)"
    )

    # Planck constraint band
    ax.fill_between(
        f_pbh_array,
        tau_planck - sigma_tau,
        tau_planck + sigma_tau,
        alpha=0.3,
        color="red",
        label="Planck 2018",
    )

    # Poulin constraint
    tau_max = 0.054 + 0.012  # Poulin+2017 limit
    ax.axhline(
        tau_max, color="orange", linestyle=":", linewidth=2, label="Poulin+2017 limit"
    )

    # Find f_pbh where tau exceeds Poulin limit
    idx_exceed = np.where(np.array(tau_array) > tau_max)[0]
    if len(idx_exceed) > 0:
        f_pbh_max = (
            f_pbh_array[idx_exceed[0] - 1] if idx_exceed[0] > 0 else f_pbh_array[0]
        )
        ax.axvline(
            f_pbh_max,
            color="green",
            linestyle="-.",
            label=f"$f_{{PBH}}^{{max}} = {f_pbh_max:.1e}$",
        )

    ax.set_xlabel(r"$f_{\rm PBH}$")
    ax.set_ylabel(r"Optical depth $\tau$")
    ax.set_xlim(1e-5, 1e-1)
    ax.set_ylim(0.04, 0.08)
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    ax.set_title(
        f"CMB Optical Depth vs PBH Fraction ($M_{{\\rm PBH}} = 10^{{-11}} M_\\odot$)"
    )

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"τ vs f_PBH plot saved to {save_path}")

    return fig


def plot_constraints(save_path="plots/pbh_cmb_constraints.png"):
    """
    Plot PBH constraints including our model predictions.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Left panel: f_pbh constraints
    constraints = literature_constraints()

    # Ali-Haimoud constraints
    ah = constraints["Ali-Haimoud2017"]
    ax1.loglog(
        ah["M_pbh"], ah["f_pbh_max"], "k-", linewidth=2, label="Ali-Haïmoud+2017"
    )

    # Serpico constraints
    serp = constraints["Serpico2020"]
    ax1.loglog(
        serp["M_pbh"], serp["f_pbh_max"], "ro", markersize=8, label="Serpico+2020"
    )

    # Our model predictions
    M_pbh_range = np.logspace(-13, -9, 20)
    f_pbh_model = []

    for M in M_pbh_range:
        pbh = PBHOpacity(f_pbh=0.1, M_pbh=M, f_osc=0.10)
        tau_components = pbh.tau_components()

        # Maximum f_pbh allowed by Planck τ constraint
        tau_excess_allowed = constraints["Poulin2017"]["tau_excess_max"]
        if tau_components["pbh"] > 0:
            f_max = 0.1 * tau_excess_allowed / tau_components["pbh"]
            f_pbh_model.append(min(1.0, f_max))
        else:
            f_pbh_model.append(1.0)

    ax1.loglog(
        M_pbh_range, f_pbh_model, "b--", linewidth=2, label="Oscillating brane limit"
    )

    # Formatting
    ax1.set_xlabel(r"$M_{\rm PBH}$ ($M_\odot$)")
    ax1.set_ylabel(r"$f_{\rm PBH}$ (max)")
    ax1.set_xlim(1e-15, 1e-8)
    ax1.set_ylim(1e-5, 1.5)
    ax1.legend(loc="best")
    ax1.grid(True, alpha=0.3)
    ax1.set_title("PBH Abundance Constraints from CMB")

    # Right panel: Optical depth breakdown
    M_pbh_test = 1e-11  # Solar masses
    f_pbh_range = np.logspace(-4, -1, 20)

    tau_std = []
    tau_pbh = []
    tau_total = []

    for f in f_pbh_range:
        pbh = PBHOpacity(f_pbh=f, M_pbh=M_pbh_test, f_osc=0.10)
        components = pbh.tau_components()
        tau_std.append(components["standard"])
        tau_pbh.append(components["pbh"])
        tau_total.append(components["total"])

    ax2.semilogx(f_pbh_range, tau_std, "k-", label="Standard reionization")
    ax2.semilogx(f_pbh_range, tau_total, "b-", linewidth=2, label="Total")
    ax2.fill_between(
        f_pbh_range, tau_std, tau_total, alpha=0.3, label="PBH contribution"
    )

    # Planck constraint
    ax2.axhline(tau_planck, color="red", linestyle="--", label="Planck measurement")
    ax2.fill_between(
        f_pbh_range,
        tau_planck - sigma_tau,
        tau_planck + sigma_tau,
        alpha=0.2,
        color="red",
    )

    ax2.set_xlabel(r"$f_{\rm PBH}$")
    ax2.set_ylabel(r"Optical depth $\tau$")
    ax2.set_xlim(1e-4, 1e-1)
    ax2.set_ylim(0.04, 0.08)
    ax2.legend(loc="best")
    ax2.grid(True, alpha=0.3)
    ax2.set_title(f"CMB Optical Depth ($M_{{\\rm PBH}} = 10^{{-11}} M_\\odot$)")

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"Constraints plot saved to {save_path}")

    return fig


def main():
    """
    Calculate PBH impact on CMB optical depth.
    """
    print("PBH Impact on CMB Optical Depth")
    print("=" * 50)

    # Model parameters
    M_pbh = 1e-11  # Solar masses (from theory)
    f_pbh = 0.01  # 1% of DM in PBHs
    f_osc = 0.10  # Oscillating fraction

    print(f"\nModel parameters:")
    print(f"  M_pbh = {M_pbh} M_sun")
    print(f"  f_pbh = {f_pbh}")
    print(f"  f_osc = {f_osc}")

    # Calculate optical depth
    pbh = PBHOpacity(f_pbh=f_pbh, M_pbh=M_pbh, f_osc=f_osc)
    components = pbh.tau_components()

    print(f"\nOptical depth components:")
    print(f"  τ_standard = {components['standard']:.4f}")
    print(f"  τ_PBH      = {components['pbh']:.4f}")
    print(f"  τ_funnel   = {components['funnel']:.4f}")
    print(f"  τ_total    = {components['total']:.4f}")

    print(f"\nPlanck constraint: τ = {tau_planck:.3f} ± {sigma_tau:.3f}")

    # Check consistency
    Delta_tau = components["total"] - tau_planck
    sigma_away = abs(Delta_tau) / sigma_tau

    print(f"\nModel prediction:")
    print(f"  Δτ = {Delta_tau:.4f} ({sigma_away:.1f}σ from Planck)")

    if sigma_away < 2:
        print("  ✓ Consistent with Planck at 2σ level")
    else:
        print("  ✗ Tension with Planck measurement")

    # Literature comparison
    print("\nLiterature constraints:")
    constraints = literature_constraints()

    print(
        f"  Poulin+2017: Δτ < {constraints['Poulin2017']['tau_excess_max']:.3f} at 95% CL"
    )
    print(f"  Our model: Δτ = {components['pbh'] + components['funnel']:.4f}")

    # Maximum allowed f_pbh
    tau_excess_max = constraints["Poulin2017"]["tau_excess_max"]
    if components["pbh"] > 0:
        f_pbh_max = f_pbh * tau_excess_max / components["pbh"]
        print(f"\nMaximum allowed f_pbh = {f_pbh_max:.3f} for M = {M_pbh} M_sun")

    # Generate plots
    print("\nGenerating constraint plots...")
    plot_constraints()

    # Generate tau vs f_pbh plot
    print("\nGenerating τ vs f_PBH plot...")
    plot_tau_vs_fpbh(M_pbh=M_pbh)

    # Save results
    results = {
        "M_pbh": M_pbh,
        "f_pbh": f_pbh,
        "f_osc": f_osc,
        "tau_components": components,
        "Delta_tau": Delta_tau,
        "sigma_away": sigma_away,
        "f_pbh_max": f_pbh_max if "f_pbh_max" in locals() else None,
    }

    np.save("data/pbh_cmb_results.npy", results)
    print("\nResults saved to data/pbh_cmb_results.npy")


if __name__ == "__main__":
    main()
