#!/usr/bin/env python3
"""
Klebanov-Strassler Landscape Scanner — Quantifying QCD Naturalness

Systematically sweeps the string theory flux landscape to compute the
geometric probability of generating the 257 MeV QCD scale without
fine-tuning.

Exact Diophantine grid of valid (K, M) pairs under the Tadpole limit
(K × M ≤ 972) and throat stability bound (K > M ≥ 2). Monte Carlo
marginalization over the perturbative string coupling g_s.

Output: plots/ks_landscape_distribution.png
"""

import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def scan_ks_landscape(tadpole_max=972, N_samples=10_000_000, N_throats=50):
    """Scan the KS flux landscape and compute QCD window probability."""
    M_pl_eV = 2.43e27  # Reduced Planck mass in eV

    # 1. Exact Diophantine grid of allowed (K, M) flux integers
    # For a stable Klebanov-Strassler throat: K > M >= 2
    K_vals = np.arange(1, tadpole_max + 1)
    M_vals = np.arange(1, tadpole_max + 1)
    K, M = np.meshgrid(K_vals, M_vals)

    valid_mask = (K * M <= tadpole_max) & (K > M) & (M >= 2)
    K_valid = K[valid_mask]
    M_valid = M[valid_mask]
    total_valid_pairs = len(K_valid)

    # 2. Monte Carlo sampling of the landscape
    np.random.seed(42)
    idx = np.random.randint(0, total_valid_pairs, N_samples)
    K_sample = K_valid[idx]
    M_sample = M_valid[idx]
    # Log-uniform sampling of string coupling in perturbative regime
    gs_sample = 10 ** np.random.uniform(np.log10(0.01), np.log10(0.30), N_samples)

    # 3. Calculate Warp Exponent W
    W = (2 * np.pi * K_sample) / (3 * gs_sample * M_sample)

    # Restrict to physically sensible supergravity regime
    sg_mask = (W >= 10) & (W <= 100)
    W_sg = W[sg_mask]
    Lambda_eV = M_pl_eV * np.exp(-W_sg)

    # 4. Target the QCD Confinement Window [200 MeV, 300 MeV]
    target_min_eV = 2e8
    target_max_eV = 3e8

    qcd_mask = (Lambda_eV >= target_min_eV) & (Lambda_eV <= target_max_eV)
    p_single = np.sum(qcd_mask) / len(W_sg)
    p_multi = 1 - (1 - p_single) ** N_throats

    print(f"\n{'=' * 60}")
    print(f"KS LANDSCAPE STATISTICAL RESULTS")
    print(f"{'=' * 60}")
    print(f"  Topologically valid (K,M) pairs: {total_valid_pairs}")
    print(f"  Valid supergravity vacua evaluated: {len(W_sg)}")
    print(f"  Vacua in QCD window [200,300] MeV: {np.sum(qcd_mask)}")
    print(
        f"  Single-throat probability: {p_single*100:.3f}%"
        f" (approx 1 in {int(1/p_single) if p_single > 0 else 'inf'})"
    )
    print(f"  Multi-throat probability ({N_throats} throats): {p_multi*100:.1f}%")
    print(f"  => ~1 in {int(1/p_multi)} CY manifolds has a QCD throat")
    print(f"{'=' * 60}")

    # 5. Plotting the distribution
    os.makedirs("plots", exist_ok=True)
    log10_Lambda = np.log10(Lambda_eV)

    plt.figure(figsize=(10, 6))
    plt.hist(log10_Lambda, bins=200, density=True, color="royalblue", alpha=0.7)
    log10_min = np.log10(target_min_eV)
    log10_max = np.log10(target_max_eV)

    plt.axvspan(
        log10_min,
        log10_max,
        color="crimson",
        alpha=0.5,
        label=(
            f"QCD Window (200-300 MeV)\n"
            f"Single Throat Prob: {p_single*100:.3f}%\n"
            f"Multi-Throat ({N_throats}): {p_multi*100:.1f}%"
        ),
    )
    plt.axvline(
        np.log10(257e6),
        color="black",
        linestyle="--",
        label=r"OBT Ignition Scale ($\tau_0^{1/3} = 257$ MeV)",
    )

    plt.title(
        "Energy Scale Distribution in the Klebanov-Strassler Flux Landscape",
        fontsize=14,
    )
    plt.xlabel(r"$\log_{10}(\Lambda_{IR} / \mathrm{eV})$", fontsize=12)
    plt.ylabel("Probability Density", fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("plots/ks_landscape_distribution.png", dpi=300)
    print(f"\nPlot saved to plots/ks_landscape_distribution.png")

    return {
        "total_pairs": total_valid_pairs,
        "p_single": p_single,
        "p_multi": p_multi,
        "N_throats": N_throats,
    }


if __name__ == "__main__":
    scan_ks_landscape()
