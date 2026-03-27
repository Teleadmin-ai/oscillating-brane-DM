#!/usr/bin/env python3
"""
Cymatic Dark Matter Halos — DF2 Dark-Matter-Free Galaxies

The 2 Gyr oscillation creates 3D spatial standing waves. Galaxies
at NODES experience no geometric DM (like NGC 1052-DF2/DF4).
Galaxies at ANTINODES experience maximum apparent DM.
"""

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

lambda_wave = 600  # Mpc (coherence length of brane standing wave)


def apparent_dm_fraction(x_Mpc):
    """Apparent DM-to-baryon ratio from standing wave amplitude."""
    amplitude = np.abs(np.cos(2 * np.pi * x_Mpc / lambda_wave))
    return 10.0 * amplitude  # max M_DM/M_b = 10 at antinodes


def main():
    print("=" * 60)
    print("CYMATIC DARK MATTER — DF2/DF4 Node Explanation")
    print(f"Standing wave coherence length: λ = {lambda_wave} Mpc")
    print("=" * 60)

    np.random.seed(42)
    N_galaxies = 1000
    x_gal = np.random.uniform(0, 1500, N_galaxies)  # Mpc
    dm_frac = apparent_dm_fraction(x_gal) * (1 + 0.2 * np.random.randn(N_galaxies))
    dm_frac = np.maximum(dm_frac, 0)

    # Find node galaxies (DF2-like)
    node_mask = dm_frac < 0.5
    antinode_mask = dm_frac > 8.0

    print(f"\n  Total galaxies: {N_galaxies}")
    print(
        f"  Node galaxies (DM-free, like DF2): {np.sum(node_mask)} ({100*np.mean(node_mask):.1f}%)"
    )
    print(
        f"  Antinode galaxies (max DM): {np.sum(antinode_mask)} ({100*np.mean(antinode_mask):.1f}%)"
    )
    print(f"  Node positions (first 5): {x_gal[node_mask][:5].astype(int)} Mpc")

    # Spatial profile
    x_profile = np.linspace(0, 1500, 1000)
    dm_profile = apparent_dm_fraction(x_profile)

    # ============================================================
    # Plot
    # ============================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(
        "Cymatic Dark Matter — Standing Wave Nodes explain DF2/DF4\n"
        r"Galaxies at nodes: no DM. Galaxies at antinodes: max DM.",
        fontsize=12,
        fontweight="bold",
    )

    # Panel 1: Scatter plot
    ax = axes[0]
    ax.scatter(
        x_gal[~node_mask & ~antinode_mask],
        dm_frac[~node_mask & ~antinode_mask],
        s=5,
        c="gray",
        alpha=0.4,
        label="Normal galaxies",
    )
    ax.scatter(
        x_gal[node_mask],
        dm_frac[node_mask],
        s=30,
        c="cyan",
        edgecolors="blue",
        label=f"DF2-like nodes ({np.sum(node_mask)})",
    )
    ax.scatter(
        x_gal[antinode_mask],
        dm_frac[antinode_mask],
        s=30,
        c="red",
        alpha=0.6,
        label=f"Max DM antinodes ({np.sum(antinode_mask)})",
    )
    ax.plot(
        x_profile,
        dm_profile,
        "b-",
        linewidth=1.5,
        alpha=0.5,
        label=r"$|cos(2\pi x/\lambda)|$",
    )
    ax.set_xlabel("Comoving position (Mpc)")
    ax.set_ylabel(r"Apparent $M_{DM}/M_b$")
    ax.set_title("Galaxy DM fraction vs spatial position")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel 2: Histogram of DM fractions
    ax = axes[1]
    ax.hist(
        dm_frac, bins=50, color="steelblue", alpha=0.7, edgecolor="navy", density=True
    )
    ax.axvline(
        x=0.5,
        color="cyan",
        linestyle="--",
        linewidth=2,
        label="DF2 threshold (DM-free)",
    )
    ax.axvline(
        x=5.0, color="green", linestyle="--", linewidth=1.5, label="Milky Way (~5)"
    )
    ax.set_xlabel(r"Apparent $M_{DM}/M_b$")
    ax.set_ylabel("Probability density")
    ax.set_title("Distribution of apparent DM fractions")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Add text
    ax.text(
        0.95,
        0.95,
        f"Node galaxies: {100*np.mean(node_mask):.1f}%\n(DM-free, like DF2/DF4)\n\n"
        f"Antinode galaxies: {100*np.mean(antinode_mask):.1f}%\n(Maximum apparent DM)",
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
    )

    plt.tight_layout()
    plt.savefig("plots/df2_cymatic_nodes.png", dpi=150)
    print(f"\nPlot saved: plots/df2_cymatic_nodes.png")


if __name__ == "__main__":
    main()
