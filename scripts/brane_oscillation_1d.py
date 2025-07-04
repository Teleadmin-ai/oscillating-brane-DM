#!/usr/bin/env python3
"""
1D Prototype: Oscillating Brane in Expanding Universe
Solves for radion field evolution with Goldberger-Wise potential
Based on O3 pro's theoretical development suggestions
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.constants import c, G

# Physical constants
M_P = 1.22e19  # GeV (Planck mass)
H0 = 2.2e-18  # Hz (Hubble constant)
GeV_to_J = 1.602e-10  # Conversion factor


class BraneOscillator1D:
    """
    Simplified 1D model of oscillating brane (radion field)
    in an expanding FRW universe
    """

    def __init__(self, tau_0=7e19, L=2e-7, T_osc=2.0):
        """
        Initialize oscillator parameters.

        Parameters
        ----------
        tau_0 : float
            Brane tension in J/m²
        L : float
            Extra dimension size in meters
        T_osc : float
            Oscillation period in Gyr
        """
        self.tau_0 = tau_0
        self.L = L
        self.T_osc = T_osc

        # Derived parameters
        self.omega_0 = 2 * np.pi / (T_osc * 1e9 * 365.25 * 24 * 3600)  # rad/s
        self.m_radion = self.omega_0 * 6.582e-16 / c**2 * GeV_to_J  # Effective mass

    def goldberger_wise_potential(self, z):
        """
        Goldberger-Wise stabilization potential.

        V(z) = (1/2) * k_eff * (z - L)²  (harmonic approximation)
        """
        # Effective spring constant normalized to avoid overflow
        # k_eff = ω₀² * τ₀ * L² / ρ_crit where ρ_crit ~ 10^17 J/m³
        rho_crit = 1e17  # Critical density scale
        k_eff = self.omega_0**2 * (self.tau_0 / rho_crit) * self.L**2

        return 0.5 * k_eff * (z - self.L) ** 2 * rho_crit

    def potential_derivative(self, z):
        """
        Derivative of the potential dV/dz.
        """
        # Normalized spring constant
        rho_crit = 1e17
        k_eff = self.omega_0**2 * (self.tau_0 / rho_crit) * self.L**2

        return k_eff * (z - self.L) * rho_crit

    def hubble_parameter(self, t):
        """
        Time-dependent Hubble parameter.
        Simple matter-dominated approximation.
        """
        t_0 = 13.8e9 * 365.25 * 24 * 3600  # Current age in seconds
        # H(t) = H0 * (t0/t)^(2/3) for matter domination
        return H0 * (t_0 / t) ** (2 / 3)

    def radion_evolution(self, t, y):
        """
        Evolution equations for the radion field.

        d²z/dt² + 3H(t)dz/dt + dV/dz = 0

        Parameters
        ----------
        t : float
            Time in seconds
        y : array
            [z, dz/dt]
        """
        z, z_dot = y

        # Hubble damping
        H = self.hubble_parameter(t)

        # Potential force
        V_prime = self.potential_derivative(z)

        # Acceleration
        z_ddot = -3 * H * z_dot - V_prime / self.tau_0

        return [z_dot, z_ddot]

    def solve_evolution(self, t_span, z_init, z_dot_init, n_points=1000):
        """
        Solve the radion evolution equations.

        Parameters
        ----------
        t_span : tuple
            (t_initial, t_final) in Gyr
        z_init : float
            Initial displacement from equilibrium
        z_dot_init : float
            Initial velocity
        n_points : int
            Number of time points
        """
        # Convert to seconds
        t_span_s = tuple(t * 1e9 * 365.25 * 24 * 3600 for t in t_span)

        # Time array
        t_eval = np.linspace(t_span_s[0], t_span_s[1], n_points)

        # Initial conditions
        y0 = [z_init, z_dot_init]

        # Solve ODE
        sol = solve_ivp(
            self.radion_evolution, t_span_s, y0, t_eval=t_eval, method="RK45", rtol=1e-8
        )

        # Convert time back to Gyr
        if sol.success:
            t_gyr = sol.t / (1e9 * 365.25 * 24 * 3600)
            return t_gyr, sol.y[0], sol.y[1]
        else:
            raise RuntimeError(f"Integration failed: {sol.message}")

    def plot_evolution(self, t, z, z_dot):
        """
        Plot the radion field evolution.
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        # Displacement
        ax1.plot(t, z / self.L, "b-", linewidth=2)
        ax1.set_ylabel("z/L (dimensionless)", fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.set_title("Radion Field Evolution in Expanding Universe", fontsize=14)

        # Velocity
        ax2.plot(t, z_dot / (self.L * H0), "r-", linewidth=2)
        ax2.set_xlabel("Time (Gyr)", fontsize=12)
        ax2.set_ylabel("dz/dt / (L·H₀)", fontsize=12)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def energy_analysis(self, t, z, z_dot):
        """
        Analyze energy components over time.
        """
        # Kinetic energy density
        rho_kin = 0.5 * self.tau_0 * (z_dot / self.L) ** 2

        # Potential energy density
        V = self.goldberger_wise_potential(z)
        rho_pot = V / self.L

        # Total energy
        rho_total = rho_kin + rho_pot

        # Equation of state
        w = (rho_kin - rho_pot) / rho_total

        return rho_kin, rho_pot, w

    def check_energy_conservation(self, t, z, z_dot):
        """
        Check energy conservation (without Hubble damping for pure oscillator).
        Returns relative error in total energy.
        """
        # Total energy at each time
        E_kin = 0.5 * self.tau_0 * self.L * z_dot**2
        E_pot = self.goldberger_wise_potential(z) * self.L

        # For harmonic oscillator, E_total should be constant
        # (Hubble damping is accounted for in the equations of motion)
        E_total = E_kin + E_pot

        # Check conservation
        E_initial = E_total[0]
        relative_error = np.abs((E_total - E_initial) / E_initial)

        return relative_error


def main():
    """
    Demonstrate 1D brane oscillation evolution.
    """
    print("1D Brane Oscillation Prototype")
    print("=" * 40)

    # Initialize oscillator
    oscillator = BraneOscillator1D()

    print(f"Brane tension: τ₀ = {oscillator.tau_0:.2e} J/m²")
    print(f"Extra dimension: L = {oscillator.L:.2e} m")
    print(f"Natural frequency: {oscillator.omega_0:.2e} rad/s")
    print(f"Oscillation period: T = {oscillator.T_osc:.1f} Gyr")

    # Initial conditions: displaced from equilibrium
    z_init = 1.2 * oscillator.L  # 20% displacement
    z_dot_init = 0  # Start at rest

    # Solve evolution from 1 Gyr to 13.8 Gyr
    t, z, z_dot = oscillator.solve_evolution(
        t_span=(1.0, 13.8), z_init=z_init, z_dot_init=z_dot_init, n_points=2000
    )

    # Plot results
    fig = oscillator.plot_evolution(t, z, z_dot)
    plt.savefig("plots/radion_evolution_1d.png", dpi=150, bbox_inches="tight")

    # Energy analysis at current time
    idx_now = -1
    rho_kin, rho_pot, w = oscillator.energy_analysis(t, z, z_dot)

    print(f"\nCurrent epoch (t = {t[idx_now]:.1f} Gyr):")
    print(f"  z/L = {z[idx_now]/oscillator.L:.3f}")
    print(f"  Kinetic energy: {rho_kin[idx_now]:.2e} J/m³")
    print(f"  Potential energy: {rho_pot[idx_now]:.2e} J/m³")
    print(f"  Equation of state w = {w[idx_now]:.3f}")

    # Check energy conservation
    t_seconds = t * 1e9 * 365.25 * 24 * 3600
    energy_error = oscillator.check_energy_conservation(t_seconds, z, z_dot)
    max_error = np.max(energy_error)
    print(f"\nEnergy conservation check:")
    print(f"  Maximum relative error: {max_error:.2e}")
    if max_error < 1e-3:
        print("  ✓ Energy conserved to 0.1%")
    else:
        print("  ⚠ Energy conservation violated!")

    # Plot energy evolution
    fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax1.semilogy(t, rho_kin, "b-", label="Kinetic", linewidth=2)
    ax1.semilogy(t, rho_pot, "r-", label="Potential", linewidth=2)
    ax1.semilogy(t, rho_kin + rho_pot, "k--", label="Total", linewidth=1.5)
    ax1.set_ylabel("Energy Density (J/m³)", fontsize=12)
    ax1.legend(loc="upper right")
    ax1.grid(True, alpha=0.3)
    ax1.set_title("Energy Components Evolution", fontsize=14)

    ax2.plot(t, w, "g-", linewidth=2)
    ax2.axhline(-1, color="k", linestyle=":", alpha=0.5)
    ax2.set_xlabel("Time (Gyr)", fontsize=12)
    ax2.set_ylabel("Equation of State w", fontsize=12)
    ax2.set_ylim(-1.1, -0.9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("plots/radion_energy_1d.png", dpi=150, bbox_inches="tight")

    print(
        "\nPlots saved to plots/radion_evolution_1d.png and plots/radion_energy_1d.png"
    )


if __name__ == "__main__":
    main()
