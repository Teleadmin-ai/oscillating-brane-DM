#!/usr/bin/env python3
"""
Generate all figures for the oscillating brane website
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

from brane_dynamics import BraneOscillator
from growth_factor import GrowthFactorCalculator

# Set up plotting style
plt.style.use("dark_background")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["font.size"] = 12
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3

# Output directory
output_dir = os.path.join(os.path.dirname(__file__), "..", "plots")
os.makedirs(output_dir, exist_ok=True)


def generate_w_z_plot():
    """Generate w(z) oscillation plot"""
    print("Generating w(z) plot...")

    # Initialize models
    brane = BraneOscillator()

    # Redshift range
    z = np.linspace(0, 3, 1000)

    # Calculate w(z)
    w_osc = brane.equation_of_state(z)
    w_lcdm = -np.ones_like(z)

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(z, w_osc, "cyan", linewidth=2.5, label="Oscillating Brane")
    ax.plot(z, w_lcdm, "gray", linewidth=2, linestyle="--", label="ΛCDM")

    # Highlight oscillation amplitude
    ax.axhline(y=-1.003, color="yellow", linestyle=":", alpha=0.5)
    ax.axhline(y=-0.997, color="yellow", linestyle=":", alpha=0.5)
    ax.fill_between(z, -1.003, -0.997, alpha=0.2, color="yellow")

    ax.set_xlabel("Redshift z", fontsize=14)
    ax.set_ylabel("Equation of state w(z)", fontsize=14)
    ax.set_title("Dark Energy Oscillations in Brane Cosmology", fontsize=16)
    ax.legend(loc="lower right")
    ax.set_xlim(0, 3)
    ax.set_ylim(-1.005, -0.995)

    plt.tight_layout()
    plt.savefig(
        os.path.join(output_dir, "w_z_oscillations.png"), dpi=150, facecolor="black"
    )
    plt.close()


def generate_growth_factor_plot():
    """Generate growth factor comparison plot"""
    print("Generating growth factor plot...")

    # Initialize calculators
    calc_lcdm = GrowthFactorCalculator(oscillating=False)
    calc_osc = GrowthFactorCalculator(oscillating=True)

    # Redshift range
    z = np.logspace(-2, 1, 100)

    # Calculate growth factors
    D_lcdm = calc_lcdm.calculate_growth_factor(z, exact=False)
    D_osc = calc_osc.calculate_growth_factor(z, exact=False)

    # Create plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Top panel: Growth factor
    ax1.loglog(1 + z, D_lcdm, "gray", linewidth=2, label="ΛCDM")
    ax1.loglog(1 + z, D_osc, "cyan", linewidth=2.5, label="Oscillating Brane")
    ax1.set_ylabel("Growth Factor D₊(z)", fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Bottom panel: Ratio
    ratio = D_osc / D_lcdm
    ax2.semilogx(1 + z, ratio, "orange", linewidth=2.5)
    ax2.axhline(y=0.948, color="yellow", linestyle="--", label="5.2% suppression")
    ax2.set_xlabel("1 + z", fontsize=14)
    ax2.set_ylabel("D₊(osc) / D₊(ΛCDM)", fontsize=14)
    ax2.set_ylim(0.94, 1.01)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.suptitle("Structure Growth Suppression in Oscillating Brane Model", fontsize=16)
    plt.tight_layout()
    plt.savefig(
        os.path.join(output_dir, "growth_factor_comparison.png"),
        dpi=150,
        facecolor="black",
    )
    plt.close()


def generate_timeline_plot():
    """Generate cosmic timeline visualization"""
    print("Generating timeline plot...")

    # Timeline data
    epochs = ["Inflation", "Reheating", "Relaxation", "Current"]
    times = [1e-34, 1e-32, 1e9 * 365 * 24 * 3600, 13.8e9 * 365 * 24 * 3600]  # seconds
    tensions = [1e50, 1e30, 1e25, 7e19]  # J/m²

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot tension evolution
    ax.loglog(times, tensions, "o-", color="cyan", linewidth=3, markersize=10)

    # Add epoch labels
    for i, (t, tau, epoch) in enumerate(zip(times, tensions, epochs)):
        ax.annotate(
            epoch,
            (t, tau),
            xytext=(10, 20),
            textcoords="offset points",
            fontsize=12,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="black", alpha=0.7),
            arrowprops=dict(arrowstyle="->", color="white", alpha=0.5),
        )

    # Add current oscillation region
    t_now = times[-1]
    ax.axvspan(t_now / 2, t_now, alpha=0.2, color="yellow", label="Oscillation era")

    ax.set_xlabel("Cosmic Time [s]", fontsize=14)
    ax.set_ylabel("Brane Tension τ [J/m²]", fontsize=14)
    ax.set_title("Evolution of Brane Tension from Big Bang to Today", fontsize=16)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(
        os.path.join(output_dir, "cosmic_timeline.png"), dpi=150, facecolor="black"
    )
    plt.close()


def main():
    """Generate all figures"""
    print("Generating figures for oscillating brane website...")

    generate_w_z_plot()
    generate_growth_factor_plot()
    generate_timeline_plot()

    print(f"\nAll figures saved to: {output_dir}")
    print("Remember to add these to your Jekyll site!")


if __name__ == "__main__":
    main()
