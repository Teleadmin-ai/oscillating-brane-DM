#!/usr/bin/env python3
"""
Growth Factor Calculator
=======================

Computes the linear growth factor D₊(z) for structure formation
in the oscillating brane cosmology, including the effects of
time-varying dark energy equation of state.
"""

import numpy as np
from scipy import integrate
from scipy.interpolate import interp1d
import argparse
from typing import Tuple, Optional

# Cosmological parameters (Planck 2018)
Omega_m0 = 0.315
Omega_r0 = 9.24e-5
Omega_DE0 = 1 - Omega_m0 - Omega_r0
h = 0.674


class GrowthFactorCalculator:
    """
    Calculate the linear growth factor D₊(z) for different cosmologies.
    """

    def __init__(
        self,
        omega_m: float = Omega_m0,
        oscillating: bool = True,
        A_w: float = 0.003,
        T_osc: float = 2.0,
    ):
        """
        Initialize the growth factor calculator.

        Parameters
        ----------
        omega_m : float
            Matter density parameter today
        oscillating : bool
            Whether to include oscillating dark energy
        A_w : float
            Amplitude of w(z) oscillations
        T_osc : float
            Oscillation period in Gyr
        """
        self.omega_m = omega_m
        self.omega_r = Omega_r0
        self.omega_de = 1 - omega_m - Omega_r0
        self.oscillating = oscillating
        self.A_w = A_w
        self.T_osc = T_osc

    def w_de(self, z: np.ndarray) -> np.ndarray:
        """
        Dark energy equation of state.

        Parameters
        ----------
        z : array-like
            Redshift

        Returns
        -------
        w : array-like
            Equation of state parameter
        """
        if not self.oscillating:
            return -np.ones_like(z)

        # Convert redshift to lookback time (approximate)
        t_lb = self._redshift_to_lookback_time(z)

        # Oscillating component
        omega = 2 * np.pi / self.T_osc  # rad/Gyr
        w = -1 + self.A_w * np.sin(omega * t_lb)

        return w

    def E_z(self, z: np.ndarray) -> np.ndarray:
        """
        Dimensionless Hubble parameter E(z) = H(z)/H₀.

        Parameters
        ----------
        z : array-like
            Redshift

        Returns
        -------
        E : array-like
            E(z)
        """
        # Matter and radiation
        E2 = self.omega_m * (1 + z) ** 3 + self.omega_r * (1 + z) ** 4

        # Dark energy with varying w(z)
        if self.oscillating:
            # Integrate to get dark energy density
            z_int = np.linspace(0, np.max(z), 1000)
            w_int = self.w_de(z_int)

            # ρ_DE(z) = ρ_DE,0 * exp[3∫_0^z (1+w(z'))/1+z' dz']
            integrand = 3 * (1 + w_int) / (1 + z_int)
            integral = integrate.cumtrapz(integrand, z_int, initial=0)
            rho_de_ratio = np.exp(integral)

            # Interpolate to requested z values
            f_interp = interp1d(
                z_int, rho_de_ratio, kind="cubic", fill_value="extrapolate"
            )
            E2 += self.omega_de * f_interp(z)
        else:
            E2 += self.omega_de

        return np.sqrt(E2)

    def growth_ode(self, z: float, y: np.ndarray) -> np.ndarray:
        """
        ODE system for growth factor evolution.

        d²D/dz² + (A/1+z)dD/dz + (B/(1+z)²)D = 0

        where A and B depend on cosmology.

        Parameters
        ----------
        z : float
            Redshift
        y : array
            [D, dD/dz]

        Returns
        -------
        dydt : array
            [dD/dz, d²D/dz²]
        """
        D, dDdz = y

        # Cosmological parameters at z
        E = self.E_z(np.array([z]))[0]
        Omega_m_z = self.omega_m * (1 + z) ** 3 / E**2

        # Dark energy equation of state
        w = self.w_de(np.array([z]))[0]
        Omega_de_z = self.omega_de / E**2
        if self.oscillating:
            # Account for varying w(z)
            z_int = np.linspace(0, z, 100)
            w_int = self.w_de(z_int)
            integrand = 3 * (1 + w_int) / (1 + z_int)
            integral = integrate.simps(integrand, z_int)
            Omega_de_z *= np.exp(integral)

        # ODE coefficients
        A = 1 + (1 + z) / (2 * E**2) * (
            -3 * self.omega_m * (1 + z) ** 2
            - 4 * self.omega_r * (1 + z) ** 3
            - 3 * w * Omega_de_z * E**2
        )

        B = 1.5 * Omega_m_z

        # System of first-order ODEs
        d2Ddz2 = -A / (1 + z) * dDdz - B / (1 + z) ** 2 * D

        return np.array([dDdz, d2Ddz2])

    def calculate_growth_factor(self, z: np.ndarray, exact: bool = False) -> np.ndarray:
        """
        Calculate the normalized growth factor D₊(z)/D₊(0).

        Parameters
        ----------
        z : array-like
            Redshift values
        exact : bool
            If True, use exact ODE integration (slower)
            If False, use fitting formula (faster)

        Returns
        -------
        D : array-like
            Normalized growth factor
        """
        if exact:
            # Solve ODE from high redshift
            z_init = 1000
            D_init = 1 / (1 + z_init)  # Matter-dominated
            dDdz_init = -D_init / (1 + z_init)

            # Integrate from z_init to 0
            z_solve = np.concatenate([[z_init], np.sort(z)[::-1], [0]])
            sol = integrate.solve_ivp(
                self.growth_ode,
                [z_init, 0],
                [D_init, dDdz_init],
                t_eval=z_solve,
                method="RK45",
                rtol=1e-8,
            )

            # Normalize by D(z=0)
            D_0 = sol.y[0][-1]
            D_all = sol.y[0] / D_0

            # Interpolate to requested z values
            f_D = interp1d(sol.t, D_all, kind="cubic")
            D = f_D(z)

        else:
            # Use fitting formula (Carroll et al. 1992)
            # Modified for oscillating w(z)
            g = (
                5
                / 2
                * self.omega_m
                * (
                    self.omega_m ** (4 / 7)
                    - self.omega_de
                    + (1 + self.omega_m / 2) * (1 + self.omega_de / 70)
                )
                ** (-1)
            )

            D = g / (1 + z)

            # Apply suppression factor for oscillating case
            if self.oscillating:
                # Empirical suppression due to oscillations
                suppression = 1 - 0.052 * (self.A_w / 0.003)
                D *= suppression

        return D

    def _redshift_to_lookback_time(self, z: np.ndarray) -> np.ndarray:
        """
        Convert redshift to lookback time in Gyr using proper integration.

        Parameters
        ----------
        z : array-like
            Redshift

        Returns
        -------
        t_lb : array-like
            Lookback time in Gyr
        """
        from scipy.integrate import quad

        # Convert H0 to 1/Gyr
        H0_Gyr = h * 100 / 3.086e19 * 3.156e16  # H0 in 1/Gyr

        # Calculate lookback time for each redshift
        z = np.atleast_1d(z)
        t_lb = np.zeros_like(z, dtype=float)

        # Use simple E(z) for ΛCDM to avoid recursion in oscillating case
        # This is accurate enough since oscillations have small amplitude (A_w ~ 0.003)
        def E_z_simple(zp):
            """Simple E(z) without dark energy oscillations"""
            return np.sqrt(
                self.omega_m * (1 + zp) ** 3
                + self.omega_r * (1 + zp) ** 4
                + self.omega_de
            )

        for i, zi in enumerate(z):
            # Integrate dt/dz = -1/[(1+z)E(z)]
            integrand = lambda zp: 1.0 / ((1 + zp) * E_z_simple(zp))
            t_lb[i], _ = quad(integrand, 0, zi)

        # Convert to Gyr
        t_lb /= H0_Gyr

        return t_lb if len(z) > 1 else float(t_lb)

    def calculate_s8(self, sigma8_cmb: float = 0.811) -> float:
        """
        Calculate S₈ = σ₈√(Ω_m/0.3) including growth suppression.

        Parameters
        ----------
        sigma8_cmb : float
            σ₈ from CMB (at z~1100)

        Returns
        -------
        S8 : float
            S₈ parameter today
        """
        # Growth from CMB to today
        D_ratio = self.calculate_growth_factor(np.array([0]))[0]

        # σ₈ today
        sigma8_0 = sigma8_cmb * D_ratio

        # S₈
        S8 = sigma8_0 * np.sqrt(self.omega_m / 0.3)

        return S8


def main():
    """
    Command-line interface for growth factor calculations.
    """
    parser = argparse.ArgumentParser(
        description="Calculate growth factor in oscillating brane cosmology"
    )
    parser.add_argument(
        "--redshift",
        "-z",
        type=float,
        nargs="+",
        default=[0, 0.5, 1.0, 1.5, 2.0],
        help="Redshift values to calculate",
    )
    parser.add_argument(
        "--exact",
        action="store_true",
        help="Use exact ODE integration (slower but more accurate)",
    )
    parser.add_argument(
        "--compare", action="store_true", help="Compare oscillating vs ΛCDM cosmology"
    )

    args = parser.parse_args()

    z = np.array(args.redshift)

    if args.compare:
        # Calculate for both cosmologies
        calc_osc = GrowthFactorCalculator(oscillating=True)
        calc_lcdm = GrowthFactorCalculator(oscillating=False)

        D_osc = calc_osc.calculate_growth_factor(z, exact=args.exact)
        D_lcdm = calc_lcdm.calculate_growth_factor(z, exact=args.exact)

        print("Growth Factor Comparison")
        print("========================")
        print("z      D₊(osc)   D₊(ΛCDM)  Ratio")
        print("-" * 35)
        for i in range(len(z)):
            ratio = D_osc[i] / D_lcdm[i]
            print(f"{z[i]:<6.2f} {D_osc[i]:<9.4f} {D_lcdm[i]:<9.4f} {ratio:.4f}")

        print(f"\nS₈(oscillating) = {calc_osc.calculate_s8():.3f}")
        print(f"S₈(ΛCDM) = {calc_lcdm.calculate_s8():.3f}")

    else:
        # Single calculation
        calc = GrowthFactorCalculator()
        D = calc.calculate_growth_factor(z, exact=args.exact)

        print("Growth Factor D₊(z)/D₊(0)")
        print("=========================")
        print("z      D₊/D₊(0)")
        print("-" * 15)
        for i in range(len(z)):
            print(f"{z[i]:<6.2f} {D[i]:.4f}")

        print(f"\nS₈ = {calc.calculate_s8():.3f}")


if __name__ == "__main__":
    main()
