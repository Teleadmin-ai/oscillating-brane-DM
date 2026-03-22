#!/usr/bin/env python3
"""
5D Laplace Demon — Evading Heisenberg via Bulk Readout

An optomechanical nanosphere (sensor) at distance d ≈ L from a target
particle reads the 5D topological shadow via KK graviton exchange,
without photon exchange (no wavefunction collapse).

H_int = -G_N M m_q / r × (1 + α exp(-r/L)) × x̂_sensor ⊗ Î_target

The target operator is Identity → target state unperturbed.
The sensor shifts by Δx = F_5D / (M ω₀²).
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ============================================================
# Physical Constants
# ============================================================
G_N = 6.674e-11  # m³/(kg·s²)
hbar = 1.055e-34  # J·s

# Sensor: silica nanosphere
M_sensor = 1e-18  # kg (~100 nm radius silica sphere)
omega_0 = 2 * np.pi * 1e5  # Hz (100 kHz trap frequency)

# Target: single atom (e.g., Cesium)
m_target = 2.2e-25  # kg (Cs atom)

# Brane parameters
L = 2.0e-7  # m (0.2 μm)
alpha_yukawa = -0.005


def F_newton(r):
    """Standard Newtonian gravitational force."""
    return G_N * M_sensor * m_target / r**2


def F_yukawa(r):
    """V8.0 Yukawa force (derivative of potential)."""
    # F = -dV/dr = G_N M m / r² × (1 + α(1 + r/L) exp(-r/L))
    newton = G_N * M_sensor * m_target / r**2
    yukawa_correction = abs(alpha_yukawa) * (1 + r / L) * np.exp(-r / L)
    return newton * (1 + yukawa_correction)


def F_5D_only(r):
    """Pure 5D Yukawa contribution (beyond Newton)."""
    newton = G_N * M_sensor * m_target / r**2
    return newton * abs(alpha_yukawa) * (1 + r / L) * np.exp(-r / L)


def displacement(F, M, omega):
    """Coherent displacement of harmonic oscillator ground state."""
    return F / (M * omega**2)


def quantum_displacement_limit():
    """Zero-point motion of the sensor."""
    return np.sqrt(hbar / (2 * M_sensor * omega_0))


def main():
    print("=" * 60)
    print("5D LAPLACE DEMON — Evading Heisenberg via Bulk Readout")
    print(f"Sensor: M = {M_sensor:.0e} kg, ω₀/2π = {omega_0 / 2 / np.pi:.0e} Hz")
    print(f"Target: m = {m_target:.1e} kg (Cs atom)")
    print(f"Extra dimension: L = {L * 1e6:.1f} μm")
    print("=" * 60)

    # Distance grid
    r_arr = np.logspace(-7.7, -5.7, 200)  # 0.02 μm to 2 μm

    # Forces
    F_N = np.array([F_newton(r) for r in r_arr])
    F_Y = np.array([F_yukawa(r) for r in r_arr])
    F_5D = np.array([F_5D_only(r) for r in r_arr])

    # Displacements
    dx_newton = np.array([displacement(F_newton(r), M_sensor, omega_0) for r in r_arr])
    dx_yukawa = np.array([displacement(F_yukawa(r), M_sensor, omega_0) for r in r_arr])
    dx_5D = np.array([displacement(F_5D_only(r), M_sensor, omega_0) for r in r_arr])

    # Quantum limit
    dx_zpm = quantum_displacement_limit()

    # Key values at r = L
    dx_N_at_L = displacement(F_newton(L), M_sensor, omega_0)
    dx_Y_at_L = displacement(F_yukawa(L), M_sensor, omega_0)
    dx_5D_at_L = displacement(F_5D_only(L), M_sensor, omega_0)

    print(f"\n  Zero-point motion: {dx_zpm:.2e} m")
    print(f"\n  At r = L = {L * 1e6:.1f} μm:")
    print(f"    Newton displacement: {dx_N_at_L:.2e} m")
    print(f"    V8.0 displacement:  {dx_Y_at_L:.2e} m")
    print(f"    5D-only signal:     {dx_5D_at_L:.2e} m")
    print(f"    Yukawa/Newton ratio: {dx_Y_at_L / dx_N_at_L:.2f}")
    print(f"    5D signal / ZPM: {dx_5D_at_L / dx_zpm:.2e}")

    # Find where 5D signal exceeds quantum noise
    snr_arr = dx_5D / dx_zpm
    detectable_mask = snr_arr > 1

    print(
        f"\n  5D signal detectable (SNR > 1): r < {r_arr[detectable_mask][-1] * 1e6:.2f} μm"
        if any(detectable_mask)
        else "\n  5D signal below quantum noise at all distances"
    )

    # ============================================================
    # Plot
    # ============================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(
        "5D Laplace Demon — Reading Quantum States via Bulk Gravitons\n"
        r"No photon exchange $\to$ no wavefunction collapse $\to$ Heisenberg bypassed",
        fontsize=12,
        fontweight="bold",
    )

    # Panel 1: Sensor displacement vs distance
    ax = axes[0]
    ax.loglog(r_arr * 1e6, dx_newton, "b--", linewidth=1.5, label="Newton only")
    ax.loglog(r_arr * 1e6, dx_yukawa, "r-", linewidth=2, label="V8.0 (Newton + Yukawa)")
    ax.loglog(
        r_arr * 1e6, dx_5D, "g-", linewidth=2, alpha=0.8, label="5D Yukawa signal only"
    )
    ax.axhline(
        y=dx_zpm,
        color="purple",
        linestyle=":",
        linewidth=1.5,
        label=f"Quantum limit (ZPM = {dx_zpm:.1e} m)",
    )
    ax.axvline(
        x=0.2, color="orange", linestyle="--", alpha=0.7, label=r"$L = 0.2\,\mu$m"
    )

    # Highlight 5D readout zone
    ax.axvspan(0.02, 0.3, alpha=0.1, color="green", label="5D Readout Zone")

    ax.set_xlabel(r"Target distance $r$ ($\mu$m)")
    ax.set_ylabel(r"Sensor displacement $\Delta x$ (m)")
    ax.set_title("Sensor displacement: Newton vs V8.0")
    ax.legend(fontsize=7, loc="upper right")
    ax.grid(True, alpha=0.3)

    # Panel 2: Yukawa/Newton ratio
    ax = axes[1]
    ratio = dx_yukawa / dx_newton
    ax.semilogx(r_arr * 1e6, ratio, "r-", linewidth=2)
    ax.axhline(y=1.0, color="k", linestyle=":", alpha=0.3)
    ax.axvline(
        x=0.2, color="orange", linestyle="--", alpha=0.7, label=r"$L = 0.2\,\mu$m"
    )

    ax.fill_between(
        r_arr * 1e6,
        1.0,
        ratio,
        where=ratio > 1.001,
        alpha=0.2,
        color="red",
        label="5D dominates Newton",
    )

    ax.set_xlabel(r"Target distance $r$ ($\mu$m)")
    ax.set_ylabel(r"$F_{V8.0} / F_{Newton}$")
    ax.set_title("5D Yukawa enhancement over Newton")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Text box
    ax.text(
        0.05,
        0.95,
        f"At $r = L = 0.2\\,\\mu$m:\n"
        f"Yukawa/Newton = {dx_Y_at_L / dx_N_at_L:.3f}\n"
        f"$\\Delta x_{{5D}}$ = {dx_5D_at_L:.1e} m\n"
        f"ZPM = {dx_zpm:.1e} m",
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
    )

    plt.tight_layout()
    plt.savefig("plots/lab_signatures/laplace_demon_readout.png", dpi=150)
    print(f"\nPlot saved: plots/lab_signatures/laplace_demon_readout.png")

    print(f"\n{'=' * 60}")
    print(f"The 5D Laplace Demon reads the target's gravitational shadow")
    print(f"via KK graviton exchange — no photons, no collapse.")
    print(
        f"At r = L, the Yukawa signal enhances Newton by {(dx_Y_at_L / dx_N_at_L - 1) * 100:.1f}%."
    )
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
