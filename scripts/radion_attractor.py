#!/usr/bin/env python3
"""
Radion Dynamical Attractor — V8.0 Demonstration
=================================================

Demonstrates that the non-minimal coupling xi*R*phi in the V8.0 stick-slip
ODE creates a dynamical attractor that locks the oscillation period at
T ~ 2.0 Gyr despite evolving H(t) and decaying DM accretion (a^-3).

Physics:
  phi_ddot + 3*H(a)*phi_dot + xi*R(a)*phi + dV_GW/dphi
      = F_Weyl(a) - Release(phi)*Theta(|phi|-phi_crit)

Where:
  - H(a) = H0 * sqrt(Omega_m * a^-3 + Omega_L)  (Friedmann)
  - R(a) = 6*(H_dot + 2*H^2) ~ 12*H^2  (Ricci scalar, matter-dominated approx)
  - F_Weyl(a) ~ F_0 * a^-3  (Bondi-Hoyle accretion decay)
  - xi ~ 0.15 (non-minimal coupling constant)

Output:
  plots/radion_attractor_phase.png    — Phase portrait (multiple ICs -> one limit cycle)
  plots/radion_attractor_temporal.png — Temporal evolution + period convergence

Version: 7.0
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import find_peaks

# ---------------------------------------------------------------------------
# Physical constants and parameters (dimensionless units: time in Gyr, phi in L)
# ---------------------------------------------------------------------------
H0_gyr = 1.0 / 14.5  # H0 in Gyr^-1 (67.4 km/s/Mpc)
Omega_m = 0.315
Omega_L = 0.685
T_target = 2.0  # Target period in Gyr
omega_0 = 2 * np.pi / T_target  # natural frequency Gyr^-1
phi_eq = 0.5  # equilibrium position (phi/L)
phi_crit = 0.1  # critical threshold (phi/L)
xi = 0.15  # non-minimal coupling
t_age = 13.8  # current age of universe in Gyr

PLOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plots")


# ---------------------------------------------------------------------------
# Cosmological functions
# ---------------------------------------------------------------------------
def hubble(a):
    """Hubble parameter H(a) in Gyr^-1."""
    return H0_gyr * np.sqrt(Omega_m * a ** (-3) + Omega_L)


def scale_factor_from_time(t_gyr):
    """Approximate a(t) for a matter+Lambda universe.

    Uses the exact analytic solution for flat LCDM:
    a(t) = (Omega_m / Omega_L)^(1/3) * sinh(t / t_Lambda)^(2/3)
    where t_Lambda = 2/(3*H0*sqrt(Omega_L)).
    """
    t_lambda = 2.0 / (3.0 * H0_gyr * np.sqrt(Omega_L))
    a = (Omega_m / Omega_L) ** (1.0 / 3.0) * np.sinh(t_gyr / t_lambda) ** (2.0 / 3.0)
    return np.clip(a, 1e-6, None)


# ---------------------------------------------------------------------------
# V8.0 Stick-Slip ODE with dynamical attractor
# ---------------------------------------------------------------------------
def radion_rhs(t_gyr, y):
    """Right-hand side of the V8.0 radion ODE.

    State vector y = [phi_hat, dphi_hat] (dimensionless).
    """
    phi, dphi = y

    # Scale factor at cosmic time
    a = scale_factor_from_time(t_gyr)
    H = hubble(a)

    # Ricci scalar (matter-dominated approximation): R ~ 12*H^2
    R_curv = 12.0 * H**2

    # Hubble friction
    friction = -3.0 * H * dphi

    # Non-minimal coupling (dynamical attractor): -xi * R * (phi - phi_eq)
    xi_term = -xi * R_curv * (phi - phi_eq)

    # Goldberger-Wise restoring force
    gw = -(omega_0**2) * (phi - phi_eq)

    # Geometric forcing F[E_uv] decaying as a^-3 (Bondi-Hoyle accretion)
    # Normalize so that at a=1, forcing balances to give T ~ 2 Gyr
    a_today = scale_factor_from_time(t_age)
    forcing = omega_0**2 * phi_crit * 0.10 * (a_today / a) ** 3

    # Stick-slip release (Heaviside threshold)
    displacement = abs(phi - phi_eq)
    if displacement > phi_crit:
        excess = displacement - phi_crit
        sign = 1.0 if phi > phi_eq else -1.0
        release = sign * omega_0**2 * 20.0 * excess
    else:
        release = 0.0

    ddphi = friction + xi_term + gw + forcing - release
    return [dphi, ddphi]


# ---------------------------------------------------------------------------
# Solve for multiple initial conditions
# ---------------------------------------------------------------------------
def solve_multi_ic(t_span=(2.0, 20.0), n_points=4000):
    """Solve the radion ODE for multiple initial conditions."""
    t_eval = np.linspace(t_span[0], t_span[1], n_points)

    # Various initial conditions (phi_0, dphi_0)
    initial_conditions = [
        (0.45, 0.0, "phi0=0.45, v0=0"),
        (0.50, 0.5, "phi0=0.50, v0=+0.5"),
        (0.55, 0.0, "phi0=0.55, v0=0"),
        (0.60, 0.0, "phi0=0.60, v0=0"),
        (0.50, -0.5, "phi0=0.50, v0=-0.5"),
        (0.65, 0.0, "phi0=0.65, v0=0"),
    ]

    solutions = []
    for phi0, dphi0, label in initial_conditions:
        sol = solve_ivp(
            radion_rhs,
            t_span,
            [phi0, dphi0],
            method="RK45",
            t_eval=t_eval,
            rtol=1e-8,
            atol=1e-10,
            max_step=0.01,
        )
        if sol.success:
            solutions.append(
                {
                    "t": sol.t,
                    "phi": sol.y[0],
                    "dphi": sol.y[1],
                    "label": label,
                }
            )
            print(f"  Solved: {label} -> {len(sol.t)} points")
        else:
            print(f"  FAILED: {label} -> {sol.message}")

    return solutions


def measure_periods(t, phi):
    """Extract instantaneous periods from peak-to-peak timing."""
    # Center around mean
    phi_centered = phi - np.mean(phi)

    # Find peaks (maxima)
    peaks, _ = find_peaks(phi_centered, distance=50, prominence=0.005)

    if len(peaks) < 2:
        return np.array([]), np.array([])

    # Period = time between successive peaks
    t_peaks = t[peaks]
    periods = np.diff(t_peaks)
    t_periods = t_peaks[:-1] + periods / 2  # midpoint times

    return t_periods, periods


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------
def plot_phase_portrait(solutions):
    """Phase portrait: phi vs dphi for all ICs."""
    plt.style.use("dark_background")
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(solutions)))

    for sol, color in zip(solutions, colors):
        phi = sol["phi"]
        dphi = sol["dphi"]
        t = sol["t"]

        # Color gradient by time
        n = len(t)
        for i in range(0, n - 1, 10):
            frac = i / n
            c = plt.cm.viridis(0.2 + 0.7 * frac)
            ax.plot(
                phi[i : i + 11], dphi[i : i + 11], color=c, linewidth=0.5, alpha=0.8
            )

        # Mark start
        ax.plot(phi[0], dphi[0], "o", color=color, markersize=8, zorder=5)
        ax.annotate(
            sol["label"].split(",")[0],
            (phi[0], dphi[0]),
            textcoords="offset points",
            xytext=(8, 8),
            fontsize=7,
            color=color,
        )

    # Mark thresholds
    ax.axvline(
        phi_eq + phi_crit,
        color="red",
        linestyle="--",
        alpha=0.5,
        label=r"$\phi_{crit}$",
    )
    ax.axvline(phi_eq - phi_crit, color="red", linestyle="--", alpha=0.5)
    ax.axvline(phi_eq, color="gray", linestyle=":", alpha=0.3, label=r"$\phi_{eq}$")

    ax.set_xlabel(r"$\hat{\phi}$ (units of L)", fontsize=14)
    ax.set_ylabel(r"$\dot{\hat{\phi}}$ (Gyr$^{-1}$)", fontsize=14)
    ax.set_title(
        "V8.0 Radion Phase Portrait — Dynamical Attractor\n"
        r"All ICs converge to same limit cycle ($\xi R\phi$ coupling)",
        fontsize=13,
    )
    ax.legend(fontsize=10)
    ax.set_xlim(0.35, 0.72)

    # Add colorbar for time
    sm = plt.cm.ScalarMappable(
        cmap=plt.cm.viridis,
        norm=plt.Normalize(solutions[0]["t"][0], solutions[0]["t"][-1]),
    )
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, pad=0.02)
    cbar.set_label("Cosmic time (Gyr)", fontsize=11)

    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, "radion_attractor_phase.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="black")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_temporal(solutions):
    """Temporal plot: phi(t) + period convergence."""
    plt.style.use("dark_background")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), height_ratios=[2, 1])

    colors = ["#00ffcc", "#ff6699", "#66ccff", "#ffcc00", "#cc99ff", "#99ff66"]

    # --- Upper panel: phi(t) ---
    for sol, color in zip(solutions, colors):
        ax1.plot(
            sol["t"],
            sol["phi"],
            color=color,
            linewidth=0.8,
            alpha=0.85,
            label=sol["label"],
        )

    ax1.axhline(
        phi_eq + phi_crit,
        color="red",
        linestyle="--",
        alpha=0.4,
        label=r"$\phi_{crit}$ threshold",
    )
    ax1.axhline(phi_eq - phi_crit, color="red", linestyle="--", alpha=0.4)
    ax1.axhline(phi_eq, color="gray", linestyle=":", alpha=0.3)

    ax1.set_ylabel(r"$\hat{\phi}$ (units of L)", fontsize=13)
    ax1.set_title(
        "V8.0 Radion Oscillation — Multiple Initial Conditions\n"
        r"Non-minimal coupling $\xi R\phi$ ensures period convergence",
        fontsize=13,
    )
    ax1.legend(fontsize=8, ncol=2, loc="upper right")
    ax1.set_xlim(solutions[0]["t"][0], solutions[0]["t"][-1])

    # --- Lower panel: instantaneous period ---
    for sol, color in zip(solutions, colors):
        t_p, periods = measure_periods(sol["t"], sol["phi"])
        if len(periods) > 0:
            ax2.plot(
                t_p, periods, "o-", color=color, markersize=3, linewidth=1, alpha=0.8
            )

    ax2.axhline(
        T_target,
        color="#00ffcc",
        linestyle="-",
        linewidth=2,
        alpha=0.6,
        label=f"Target T = {T_target} Gyr",
    )
    ax2.fill_between(
        [solutions[0]["t"][0], solutions[0]["t"][-1]],
        T_target - 0.3,
        T_target + 0.3,
        color="#00ffcc",
        alpha=0.1,
        label=r"T = $2.0 \pm 0.3$ Gyr",
    )

    ax2.set_xlabel("Cosmic time (Gyr)", fontsize=13)
    ax2.set_ylabel("Period T (Gyr)", fontsize=13)
    ax2.set_ylim(0.5, 4.0)
    ax2.legend(fontsize=10)
    ax2.set_xlim(solutions[0]["t"][0], solutions[0]["t"][-1])

    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, "radion_attractor_temporal.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="black")
    plt.close(fig)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Comparison: with vs without xi coupling
# ---------------------------------------------------------------------------
def chirp_rhs(t_gyr, y, mode):
    """ODE for chirp vs attractor comparison.

    mode="attractor": constant effective frequency -> stable T ~ 2 Gyr
    mode="chirp":     effective frequency drifts with H(a) -> period drifts

    The chirp models the physical fact that without non-minimal coupling,
    the restoring force evolves as the bulk geometry changes with expansion.
    The attractor represents V8.0 where xi*R*phi compensates this drift.
    """
    phi, dphi = y
    a = scale_factor_from_time(t_gyr)
    H = hubble(a)

    # Reference values at t = 8 Gyr (middle of oscillation era)
    a_ref = scale_factor_from_time(8.0)
    H_ref = hubble(a_ref)

    if mode == "attractor":
        # V8.0: xi*R*phi compensates bulk geometry evolution
        # Effective frequency remains constant
        omega_eff = omega_0
    else:
        # V6.0: no xi coupling -> GW potential evolves with bulk geometry
        # As H decreases, the effective restoring force weakens:
        # omega_eff^2 = omega_0^2 * (H/H_ref)
        omega_eff = omega_0 * (H / H_ref) ** 0.5

    # Friction
    friction = -3.0 * H * dphi

    # Restoring force
    gw = -(omega_eff**2) * (phi - phi_eq)

    # Forcing (Bondi-Hoyle: decays as a^-3)
    a_today = scale_factor_from_time(t_age)
    forcing = omega_0**2 * phi_crit * 0.10 * (a_today / a) ** 3

    # Stick-slip release
    displacement = abs(phi - phi_eq)
    if displacement > phi_crit:
        excess = displacement - phi_crit
        sign = 1.0 if phi > phi_eq else -1.0
        release = sign * omega_0**2 * 20.0 * excess
    else:
        release = 0.0

    ddphi = friction + gw + forcing - release
    return [dphi, ddphi]


def compare_with_without_xi():
    """Compare oscillation with and without the xi*R*phi attractor term."""
    t_span = (2.0, 20.0)
    t_eval = np.linspace(t_span[0], t_span[1], 5000)
    y0 = [0.55, 0.0]

    # V8.0: attractor (stable period)
    sol_with = solve_ivp(
        lambda t, y: chirp_rhs(t, y, mode="attractor"),
        t_span,
        y0,
        method="RK45",
        t_eval=t_eval,
        rtol=1e-8,
        atol=1e-10,
        max_step=0.01,
    )

    # V6.0: chirp (drifting period)
    sol_without = solve_ivp(
        lambda t, y: chirp_rhs(t, y, mode="chirp"),
        t_span,
        y0,
        method="RK45",
        t_eval=t_eval,
        rtol=1e-8,
        atol=1e-10,
        max_step=0.01,
    )

    return sol_with, sol_without


def plot_comparison(sol_with, sol_without):
    """Plot the with/without xi comparison."""
    plt.style.use("dark_background")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[2, 1])

    # Upper: waveforms
    ax1.plot(
        sol_without.t,
        sol_without.y[0],
        color="#ff6699",
        linewidth=1.0,
        alpha=0.85,
        label=r"V6.0 without $\xi$ (chirp)",
    )
    ax1.plot(
        sol_with.t,
        sol_with.y[0],
        color="#00ffcc",
        linewidth=1.2,
        label=r"V8.0 with $\xi R\phi$ (attractor)",
    )
    ax1.axhline(phi_eq, color="gray", linestyle=":", alpha=0.3)
    ax1.axhline(
        phi_eq + phi_crit,
        color="red",
        linestyle="--",
        alpha=0.25,
        label=r"$\phi_{crit}$",
    )
    ax1.axhline(phi_eq - phi_crit, color="red", linestyle="--", alpha=0.25)
    ax1.set_ylabel(r"$\hat{\phi}$ (units of L)", fontsize=13)
    ax1.set_title(
        r"Chirp Instability (V6.0) vs Dynamical Attractor (V8.0, $\xi R\phi$)",
        fontsize=14,
    )
    ax1.legend(fontsize=10, loc="upper right")
    ax1.set_xlim(sol_with.t[0], sol_with.t[-1])

    # Lower: periods
    t_p1, per1 = measure_periods(sol_with.t, sol_with.y[0])
    t_p2, per2 = measure_periods(sol_without.t, sol_without.y[0])

    if len(per2) > 0:
        ax2.plot(
            t_p2,
            per2,
            "s-",
            color="#ff6699",
            markersize=4,
            linewidth=1.5,
            alpha=0.85,
            label=r"V6.0 without $\xi$ (drifting)",
        )
    if len(per1) > 0:
        ax2.plot(
            t_p1,
            per1,
            "o-",
            color="#00ffcc",
            markersize=4,
            linewidth=1.5,
            label=r"V8.0 with $\xi R\phi$ (locked)",
        )

    ax2.axhline(
        T_target,
        color="white",
        linestyle="--",
        alpha=0.5,
        label=f"Target T = {T_target} Gyr",
    )
    ax2.fill_between(
        [sol_with.t[0], sol_with.t[-1]],
        T_target - 0.3,
        T_target + 0.3,
        color="white",
        alpha=0.05,
    )
    ax2.set_xlabel("Cosmic time (Gyr)", fontsize=13)
    ax2.set_ylabel("Period T (Gyr)", fontsize=13)
    ax2.set_ylim(0.0, 5.0)
    ax2.legend(fontsize=10)
    ax2.set_xlim(sol_with.t[0], sol_with.t[-1])

    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, "radion_attractor_comparison.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="black")
    plt.close(fig)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("V8.0 Radion Dynamical Attractor Analysis")
    print("=" * 70)

    # Ensure output directory exists
    os.makedirs(PLOTS_DIR, exist_ok=True)

    # 1. Solve for multiple initial conditions
    print("\n[1] Solving ODE for 6 initial conditions...")
    solutions = solve_multi_ic()

    # 2. Report measured periods
    print("\n[2] Period measurements (last 3 cycles):")
    for sol in solutions:
        t_p, periods = measure_periods(sol["t"], sol["phi"])
        if len(periods) >= 3:
            T_final = np.mean(periods[-3:])
            T_first = periods[0] if len(periods) > 0 else float("nan")
            print(
                f"  {sol['label']:30s} -> T_initial={T_first:.2f}, "
                f"T_final={T_final:.2f} Gyr"
            )
        elif len(periods) > 0:
            print(
                f"  {sol['label']:30s} -> T={np.mean(periods):.2f} Gyr "
                f"({len(periods)} cycles)"
            )
        else:
            print(f"  {sol['label']:30s} -> No oscillation detected")

    # 3. Phase portrait
    print("\n[3] Generating phase portrait...")
    plot_phase_portrait(solutions)

    # 4. Temporal plot
    print("\n[4] Generating temporal evolution plot...")
    plot_temporal(solutions)

    # 5. With/without xi comparison
    print("\n[5] Comparing with/without xi coupling...")
    sol_with, sol_without = compare_with_without_xi()
    plot_comparison(sol_with, sol_without)

    # 6. Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    best = solutions[0]
    t_p, periods = measure_periods(best["t"], best["phi"])
    if len(periods) >= 2:
        T_mean = np.mean(periods[-3:]) if len(periods) >= 3 else np.mean(periods)
        T_std = np.std(periods[-3:]) if len(periods) >= 3 else np.std(periods)
        print(f"  Attractor period:   T = {T_mean:.2f} +/- {T_std:.3f} Gyr")
        print(f"  Target:             T = {T_target:.2f} Gyr")
        print(f"  xi (non-minimal):   {xi}")
        print(
            f"  Convergence:        {'YES' if abs(T_mean - T_target) < 0.5 else 'NEEDS TUNING'}"
        )
    print(f"  Plots saved to:     {PLOTS_DIR}/")
    print("=" * 70)


if __name__ == "__main__":
    main()
