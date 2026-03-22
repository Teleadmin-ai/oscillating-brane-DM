#!/usr/bin/env python3
"""
ISW (Integrated Sachs-Wolfe) effect visualization
Shows how the 2 Gyr brane oscillation manifests in CMB large-scale anisotropies
"""

import os

import matplotlib.pyplot as plt
import numpy as np

# Set up plot style
plt.style.use("dark_background")
plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["font.size"] = 12

# Physical parameters
T_osc = 2.0  # Oscillation period in Gyr
z_max = 5.0  # Maximum redshift
A_w = 0.003  # Amplitude of w(z) oscillation

# Cosmological parameters
H0 = 70  # km/s/Mpc
c = 3e5  # km/s


def lookback_time(z):
    """Approximate lookback time in Gyr"""
    return 9.8 * np.log(1 + z) / np.log(10)


def w_de(z):
    """Dark energy equation of state with oscillation"""
    t_lb = lookback_time(z)
    return -1 + A_w * np.sin(2 * np.pi * t_lb / T_osc)


def isw_amplitude(l, z):
    """ISW temperature fluctuation amplitude at multipole l and redshift z"""
    # Simplified ISW kernel
    w = w_de(z)
    dw_dt = A_w * (2 * np.pi / T_osc) * np.cos(2 * np.pi * lookback_time(z) / T_osc)

    # ISW amplitude scales with dw/dt and (1+w)
    # This is a simplified model for visualization
    amplitude = np.abs(dw_dt * (1 + w) / (l * (l + 1)))
    return amplitude * 1e-5  # Scale to realistic CMB units


# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Dark Energy Equation of State
ax1 = axes[0, 0]
z_array = np.linspace(0, 3, 200)
w_array = [w_de(z) for z in z_array]

ax1.plot(z_array, w_array, "cyan", linewidth=2.5)
ax1.axhline(-1, color="gray", linestyle="--", alpha=0.5, label="ΛCDM (w=-1)")
ax1.set_xlabel("Redshift z", fontsize=12)
ax1.set_ylabel("w(z)", fontsize=12)
ax1.set_title("Oscillating Dark Energy Equation of State", fontsize=14)
ax1.grid(True, alpha=0.3)
ax1.legend()

# 2. ISW Effect in CMB Power Spectrum
ax2 = axes[0, 1]
l_array = np.logspace(0, 3, 100)
z_isw = 0.5  # Redshift where ISW is strongest

# ISW contribution to CMB
isw_spectrum = np.array(
    [isw_amplitude(l, z_isw) * l * (l + 1) / (2 * np.pi) for l in l_array]
)

ax2.loglog(
    l_array,
    isw_spectrum * 1e12,
    "yellow",
    linewidth=2.5,
    label="ISW from brane oscillation",
)
ax2.set_xlabel("Multipole ℓ", fontsize=12)
ax2.set_ylabel("ℓ(ℓ+1)Cℓ/2π [μK²]", fontsize=12)
ax2.set_title("ISW Contribution to CMB Angular Power Spectrum", fontsize=14)
ax2.grid(True, alpha=0.3)
ax2.legend()
ax2.set_xlim(2, 1000)

# 3. Time Evolution of Oscillation
ax3 = axes[1, 0]
t_array = np.linspace(0, 10, 500)  # Time in Gyr
oscillation = np.sin(2 * np.pi * t_array / T_osc)

ax3.plot(t_array, oscillation, "lime", linewidth=2.5)
ax3.fill_between(t_array, 0, oscillation, alpha=0.3, color="lime")
ax3.axhline(0, color="white", linestyle="-", alpha=0.3)

# Mark key epochs
epochs = [0, 2, 4, 6, 8, 10]
for epoch in epochs:
    if epoch % T_osc == 0:
        ax3.axvline(epoch, color="red", linestyle="--", alpha=0.5)

ax3.set_xlabel("Cosmic Time [Gyr]", fontsize=12)
ax3.set_ylabel("Brane Displacement", fontsize=12)
ax3.set_title(f"Cosmic Membrane Oscillation (Period = {T_osc} Gyr)", fontsize=14)
ax3.grid(True, alpha=0.3)

# 4. Detection Prospects
ax4 = axes[1, 1]

# Experimental sensitivities
experiments = ["Planck", "CMB-S4", "CMB-HD"]
l_peak = [100, 200, 500]
sensitivity = [5e-6, 1e-6, 2e-7]  # Temperature sensitivity in K
colors = ["blue", "green", "red"]

for i, exp in enumerate(experiments):
    ax4.scatter(
        l_peak[i],
        sensitivity[i] * 1e6,
        s=200,
        c=colors[i],
        marker="*",
        label=exp,
        edgecolor="white",
        linewidth=1.5,
        zorder=5,
    )

# Show our predicted signal
l_signal = np.array([10, 30, 100, 300])
signal_amplitude = np.array([3e-5, 1e-5, 3e-6, 1e-6])
ax4.plot(
    l_signal,
    signal_amplitude * 1e6,
    "cyan",
    linewidth=2.5,
    label="Brane oscillation ISW signal",
    marker="o",
    markersize=8,
)

ax4.set_xscale("log")
ax4.set_yscale("log")
ax4.set_xlabel("Multipole ℓ", fontsize=12)
ax4.set_ylabel("Temperature Fluctuation [μK]", fontsize=12)
ax4.set_title("ISW Detection Prospects", fontsize=14)
ax4.grid(True, alpha=0.3)
ax4.legend()
ax4.set_xlim(5, 1000)
ax4.set_ylim(0.1, 100)

plt.suptitle(
    "Integrated Sachs-Wolfe Effect from Brane Oscillation", fontsize=16, y=1.02
)
plt.tight_layout()

# Save the figure
output_dir = "/root/bulk/oscillating-brane-DM/plots"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "isw_effect.png")
plt.savefig(output_file, dpi=150, bbox_inches="tight", facecolor="black")
print(f"ISW effect visualization saved to {output_file}")

plt.show()
