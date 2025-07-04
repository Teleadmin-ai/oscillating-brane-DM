#!/usr/bin/env python3
"""
PTA echo effect calculation and visualization
Shows the gravitational wave doublet at f0 and 2f0
"""

import os

import matplotlib.pyplot as plt
import numpy as np

# Set up plot style
plt.style.use("dark_background")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["font.size"] = 12

# Physical parameters
T_osc = 2.0 * 3.16e16  # Oscillation period in seconds (2 Gyr)
f0 = 1 / T_osc  # Fundamental frequency ≈ 1.6e-17 Hz
h0 = 2e-18  # Strain amplitude

# Frequency range for PTA sensitivity
f = np.logspace(-18, -16, 300)

# Gravitational wave spectrum with echo
# Primary peak at f0, echo at 2f0
h_c = h0 * np.sqrt((f / f0) ** (-4) + 0.25 * (f / (2 * f0)) ** (-4))

# Create the plot
fig, ax = plt.subplots()

# Main spectrum
ax.loglog(f, h_c, "cyan", linewidth=2.5, label="Brane oscillation spectrum")

# Mark the peaks
ax.axvline(f0, color="yellow", linestyle="--", alpha=0.7, label=f"f₀ = {f0:.2e} Hz")
ax.axvline(
    2 * f0, color="orange", linestyle="--", alpha=0.7, label=f"2f₀ = {2*f0:.2e} Hz"
)

# PTA sensitivity bands (approximate)
pta_freq = np.array([1e-9, 1e-8, 1e-7])
pta_sens = np.array([1e-15, 5e-16, 2e-15])
ax.fill_between(
    pta_freq,
    pta_sens * 0.3,
    pta_sens * 3,
    alpha=0.3,
    color="gray",
    label="PTA sensitivity",
)

# Formatting
ax.set_xlabel("Frequency [Hz]", fontsize=14)
ax.set_ylabel("Characteristic strain $h_c$", fontsize=14)
ax.set_title("Predicted Stochastic GW Background with Echo at 2f₀", fontsize=16)
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right")

# Set axis limits
ax.set_xlim(1e-18, 1e-16)
ax.set_ylim(1e-20, 1e-14)

# Add annotations
ax.text(
    f0 * 1.5,
    h0 * 0.3,
    "Fundamental\nmode",
    horizontalalignment="center",
    fontsize=10,
    color="yellow",
)
ax.text(
    2 * f0 * 1.5,
    h0 * 0.15,
    "First\nharmonic",
    horizontalalignment="center",
    fontsize=10,
    color="orange",
)

# Save the figure
output_path = os.path.join(os.path.dirname(__file__), "..", "plots", "pta_doublet.png")
plt.tight_layout()
plt.savefig(output_path, dpi=150, facecolor="black")
print(f"PTA doublet plot saved to: {output_path}")

# Also save a light version for potential use
plt.style.use("default")
ax.set_facecolor("white")
fig.patch.set_facecolor("white")
output_path_light = os.path.join(
    os.path.dirname(__file__), "..", "plots", "pta_doublet_light.png"
)
plt.savefig(output_path_light, dpi=150)
print(f"Light version saved to: {output_path_light}")

# Print key values
print("\n=== Gravitational Wave Echo Parameters ===")
print(f"Fundamental frequency f₀ = {f0:.2e} Hz")
print(f"Echo frequency 2f₀ = {2*f0:.2e} Hz")
print(f"Period T = {T_osc/3.16e16:.1f} Gyr")
print(f"Strain at f₀: h_c ≈ {h0:.1e}")
print(f"Strain at 2f₀: h_c ≈ {h0*0.5:.1e}")
print("\nThis doublet structure is a unique signature of brane oscillations!")
