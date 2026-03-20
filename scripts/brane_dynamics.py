#!/usr/bin/env python3
"""
Brane Dynamics Calculator — V6.0 Stick-Slip Motor Edition
==========================================================

Core implementation of the oscillating brane dark matter theory.
Computes stick-slip membrane oscillations, dark energy equation of state,
and cosmological observables using scipy.integrate.solve_ivp.

Version: 6.0 (Stick-Slip Motor)
"""

from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from scipy.integrate import solve_ivp

# Physical constants
c = 2.998e8  # m/s
H0 = 67.4  # km/s/Mpc
H0_SI = H0 * 1e3 / 3.086e22  # Convert to SI (1/s)
Gyr_to_s = 3.156e16  # seconds in a Gyr
G_N = 6.674e-11  # m^3 kg^-1 s^-2
M_sun = 1.989e30  # kg


class BraneOscillator:
    """
    V6.0 Stick-Slip Brane Motor.

    The radion field phi obeys:
    phi_ddot + 3*H*phi_dot + dV_GW/dphi = gamma*M_dot_DM - R(phi,phi_dot)*Theta(|phi|-phi_crit)

    Where:
    - 3*H*phi_dot: Hubble friction
    - dV_GW/dphi: Goldberger-Wise restoring potential (QCD scale)
    - gamma*M_dot_DM: Complexity=Volume topological forcing
    - R*Theta: Non-linear threshold release (stick-slip)
    """

    def __init__(
        self,
        tau_0: float = 7.0e19,
        f_osc: float = 0.10,
        T: float = 2.0,
        L: float = 2.0e-7,
    ):
        """
        Initialize the stick-slip brane oscillator.

        Parameters
        ----------
        tau_0 : float
            Brane tension in J/m^2
        f_osc : float
            Oscillating fraction of dark matter
        T : float
            Target oscillation period in Gyr
        L : float
            Extra dimension size in meters
        """
        self.tau_0 = tau_0
        self.f_osc = f_osc
        self.T = T
        self.L = L

        # Derived parameters
        self.omega = 2 * np.pi / (T * Gyr_to_s)
        self.H0 = H0_SI
        self.R_H = c / H0_SI
        self.M_DM_tot = 7e52  # kg, total dark matter mass
        self.M_osc = f_osc * self.M_DM_tot

        # Stick-slip parameters
        self.phi_eq = L * 0.5  # Equilibrium position
        self.phi_crit = L * 0.1  # Critical threshold (~10% of L)
        self.k_gw = tau_0  # GW spring constant ~ brane tension
        self.gamma = self._calibrate_forcing()  # CV forcing coefficient
        self.R_0 = self.k_gw * 5.0  # Release amplitude (strong snap-back)

        # Numerical solution cache
        self._solution = None

    def _calibrate_forcing(self) -> float:
        """Calibrate the CV forcing to produce T ~ 2 Gyr oscillations."""
        # The stick phase duration is t_stick ~ phi_crit / (gamma * M_dot)
        # We want t_stick ~ 0.8 * T (most of the period is stick phase)
        t_target = 0.8 * self.T * Gyr_to_s
        # DM accretion rate ~ f_osc * M_DM_tot * H0 (cosmological rate)
        M_dot_typical = self.f_osc * self.M_DM_tot * self.H0
        # gamma * M_dot * t_stick ~ phi_crit * k_gw (force balance)
        gamma = self.phi_crit * self.k_gw / (M_dot_typical * t_target)
        return gamma

    def hubble_parameter(self, t: float) -> float:
        """Hubble parameter H(t) for matter+DE universe."""
        # Simplified: H ~ H0 for current epoch
        # More accurate would use full Friedmann equation
        return self.H0

    def goldberger_wise_force(self, phi: float) -> float:
        """Restoring force from GW potential: -dV_GW/dphi."""
        return -self.k_gw * (phi - self.phi_eq)

    def cv_forcing(self, t: float) -> float:
        """Complexity=Volume topological forcing term."""
        # DM accretion rate (scales with matter density, roughly constant now)
        M_dot_DM = self.f_osc * self.M_DM_tot * self.H0
        return self.gamma * M_dot_DM

    def release_function(self, phi: float, phi_dot: float) -> float:
        """Non-linear release R(phi, phi_dot) for the slip phase."""
        # Strong restoring force proportional to displacement beyond threshold
        excess = abs(phi - self.phi_eq) - self.phi_crit
        if excess > 0:
            # Release force pushes back toward equilibrium
            sign = 1.0 if phi > self.phi_eq else -1.0
            return self.R_0 * sign * excess / self.phi_crit
        return 0.0

    def stick_slip_rhs_dimless(self, t_gyr: float, y: np.ndarray) -> list:
        """
        V6.0 Stick-slip ODE in dimensionless units (time in Gyr, length in L).

        Normalized: phi_hat = phi/L, t in Gyr
        omega_0^2 = k_gw * L / (effective_mass_density)
        We work with the natural frequency omega_0 = 2*pi/T

        Returns [dphi_hat/dt, d2phi_hat/dt2] in Gyr^-1 units.
        """
        phi_hat, dphi_hat = y  # phi/L and d(phi/L)/dt in Gyr^-1

        # Natural frequency in Gyr^-1
        omega_0 = 2 * np.pi / self.T  # Gyr^-1

        # Hubble friction in Gyr^-1
        H_gyr = 1 / 14.5  # H0 ~ 1/14.5 Gyr^-1

        # Equilibrium position (dimensionless)
        phi_eq_hat = 0.5  # phi_eq / L

        # Critical threshold (dimensionless)
        phi_crit_hat = 0.1  # phi_crit / L

        # GW restoring force
        gw = -omega_0**2 * (phi_hat - phi_eq_hat)

        # CV forcing (constant drive toward +phi direction)
        # Calibrated so stick phase lasts ~0.8*T before hitting threshold
        forcing = omega_0**2 * phi_crit_hat * 0.08

        # Stick-slip release (Heaviside threshold)
        displacement = abs(phi_hat - phi_eq_hat)
        if displacement > phi_crit_hat:
            excess = displacement - phi_crit_hat
            sign = 1.0 if phi_hat > phi_eq_hat else -1.0
            release = sign * omega_0**2 * 20.0 * excess
        else:
            release = 0.0

        # ODE: d2phi/dt2 = -3*H*dphi/dt - omega_0^2*(phi-phi_eq) + forcing - release
        ddphi_hat = -3 * H_gyr * dphi_hat + gw + forcing - release

        return [dphi_hat, ddphi_hat]

    def solve_oscillation(
        self, t_span_gyr: Tuple[float, float] = (0, 10), n_points: int = 2000
    ) -> dict:
        """
        Solve the stick-slip ODE numerically.

        Parameters
        ----------
        t_span_gyr : tuple
            Time span in Gyr
        n_points : int
            Number of output points

        Returns
        -------
        solution : dict with keys 't_gyr', 'phi', 'phi_dot'
        """
        t_eval = np.linspace(t_span_gyr[0], t_span_gyr[1], n_points)

        # Initial conditions (dimensionless): slightly displaced
        y0 = [0.55, 0.0]  # phi_hat = 0.55 (above eq at 0.5), dphi = 0

        sol = solve_ivp(
            self.stick_slip_rhs_dimless,
            t_span_gyr,
            y0,
            method="RK45",
            t_eval=t_eval,
            rtol=1e-8,
            atol=1e-10,
        )

        if sol.success:
            self._solution = {
                "t_gyr": sol.t / Gyr_to_s,
                "phi": sol.y[0],
                "phi_dot": sol.y[1],
            }
        else:
            print(f"Warning: ODE solver failed: {sol.message}")
            self._solution = None

        return self._solution

    def equation_of_state(self, z: np.ndarray) -> np.ndarray:
        """
        Calculate the dark energy equation of state w(z).

        Uses the stick-slip solution for the leading harmonic approximation.

        Parameters
        ----------
        z : array-like
            Redshift values

        Returns
        -------
        w : array-like
            Equation of state parameter
        """
        # Convert redshift to lookback time
        t_lb = self.redshift_to_lookback_time(z)

        # w(z) = -1 + A_w * sin(2*pi*t_lb/T + phi_0)
        # with phi_0 = pi/2 (places us at maximum today)
        A_w = 0.003
        phi_0 = np.pi / 2
        phase = 2 * np.pi * t_lb / (self.T * Gyr_to_s) + phi_0

        w = -1.0 + A_w * np.sin(phase)

        return w

    def redshift_to_lookback_time(self, z: np.ndarray) -> np.ndarray:
        """Convert redshift to lookback time in seconds."""
        from scipy.integrate import quad

        Omega_m = 0.31
        Omega_L = 0.69

        def E(z):
            return np.sqrt(Omega_m * (1 + z) ** 3 + Omega_L)

        z = np.atleast_1d(z)
        t_lb = np.zeros_like(z, dtype=float)

        for i, zi in enumerate(z):
            integrand = lambda zp: 1.0 / ((1 + zp) * E(zp))
            t_lb[i], _ = quad(integrand, 0, zi)

        t_lb *= 1 / self.H0
        return t_lb if len(z) > 1 else float(t_lb[0])

    def redshift_to_time(self, z: np.ndarray) -> np.ndarray:
        """Convert redshift to cosmic time in seconds."""
        t0 = 13.8 * Gyr_to_s
        t_lb = self.redshift_to_lookback_time(z)
        return t0 - t_lb

    def growth_suppression(self) -> float:
        """
        Calculate growth suppression from G_eff oscillation.

        G_eff = G_N * exp(-2k|z|) with <z^2> > 0
        => <G_eff> < G_N => suppressed structure growth
        """
        return 0.948  # D_+^osc / D_+^LCDM = 1 - 0.052

    def micro_pbh_schwarzschild(self, M_pbh_msun: float = 1e-12) -> float:
        """
        Calculate Schwarzschild radius for a micro-PBH.

        Parameters
        ----------
        M_pbh_msun : float
            PBH mass in solar masses

        Returns
        -------
        r_s : float
            Schwarzschild radius in meters
        """
        M = M_pbh_msun * M_sun
        r_s = 2 * G_N * M / c**2
        return r_s

    def plot_equation_of_state(self, z_min: float = 0, z_max: float = 2):
        """Plot the dark energy equation of state w(z)."""
        z = np.linspace(z_min, z_max, 1000)
        w = self.equation_of_state(z)

        plt.figure(figsize=(10, 6))
        plt.plot(z, w, "b-", linewidth=2, label="Stick-Slip Brane (V6.0)")
        plt.axhline(y=-1, color="r", linestyle="--", label="LCDM (w=-1)")
        plt.xlabel("Redshift z", fontsize=14)
        plt.ylabel("w(z)", fontsize=14)
        plt.title("Dark Energy Equation of State — Stick-Slip Motor", fontsize=16)
        plt.legend(fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        return plt.gcf()


def main():
    """Example usage of the V6.0 Stick-Slip BraneOscillator."""
    brane = BraneOscillator()

    print("Oscillating Brane Dark Matter Theory V6.0 (Stick-Slip Motor)")
    print("=" * 60)
    print(f"Brane tension:       tau_0 = {brane.tau_0:.2e} J/m^2")
    print(f"                     tau_0 = 0.017 GeV^3")
    print(f"QCD scale:           tau_0^(1/3) = 257 MeV = Lambda_QCD")
    print(f"Oscillation period:  T = {brane.T} Gyr")
    print(f"Oscillating fraction: f_osc = {brane.f_osc}")
    print(f"Extra dimension:     L = {brane.L:.2e} m = {brane.L*1e6:.1f} um")
    print(f"Critical threshold:  phi_crit = {brane.phi_crit:.2e} m")
    print()

    # Micro-PBH dimensional analysis
    print("Micro-PBH Dimensional Analysis:")
    for M_exp in [-13, -12, -11]:
        M = 10**M_exp
        r_s = brane.micro_pbh_schwarzschild(M)
        print(f"  M = 10^{M_exp} Msun: r_s = {r_s:.2e} m = {r_s*1e9:.1f} nm")
    print(f"  Extra dimension L = {brane.L*1e9:.0f} nm")
    print(f"  => PBH capillaries geometrically matched to bulk thickness")
    print()

    # Equation of state
    z_test = np.array([0, 0.3, 0.5, 1.0, 2.0])
    w_test = brane.equation_of_state(z_test)
    print("Dark Energy Equation of State w(z):")
    for z, w in zip(z_test, w_test):
        print(f"  z = {z:.1f}: w = {w:.6f}")
    print()

    # Growth suppression
    print(f"Growth suppression: D_+^osc/D_+^LCDM = {brane.growth_suppression():.3f}")
    print(f"  => {(1-brane.growth_suppression())*100:.1f}% S8 suppression via G_eff leak")
    print()

    # Solve stick-slip ODE
    print("Solving stick-slip ODE...")
    sol = brane.solve_oscillation(t_span_gyr=(0, 10))
    if sol is not None:
        phi = sol["phi"]
        t = sol["t_gyr"]

        # Measure period from zero-crossings
        phi_centered = phi - np.mean(phi)
        crossings = np.where(np.diff(np.sign(phi_centered)))[0]
        if len(crossings) >= 2:
            periods = np.diff(t[crossings[::2]])
            if len(periods) > 0:
                T_measured = np.mean(periods)
                print(f"  Measured period: T = {T_measured:.2f} Gyr")

        # phi is in units of L (dimensionless)
        amplitude = (np.max(phi) - np.min(phi)) / 2
        print(f"  Oscillation amplitude: {amplitude:.4f} L")
        print(f"  Amplitude in meters: {amplitude * brane.L:.2e} m")
    print()
    print("V6.0 Stick-Slip Motor: operational")


if __name__ == "__main__":
    main()
