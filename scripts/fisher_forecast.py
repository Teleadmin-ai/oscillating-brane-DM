#!/usr/bin/env python3
"""
Multi-Probe Fisher Forecast — V8.2
====================================

Constructs the Fisher Information Matrix from 5 cosmological probes
(Planck, DESI, Euclid, SKA, PTA) and plots 1σ/2σ confidence ellipses.

Output:
  plots/fisher_forecast.png — Confidence ellipses in 3 parameter planes

Version: 8.2
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

PLOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plots")

# ---------------------------------------------------------------------------
# Fiducial parameters and observational uncertainties
# ---------------------------------------------------------------------------
theta_fid = np.array([7e19, 2.0, 2e-7])
param_names = [r"$\tau_0$", r"$T$", r"$L$"]
param_labels_short = ["tau0", "T", "L"]

# Projected 1-sigma uncertainties per probe
# [Planck ISW, DESI Aw, Euclid S8, SKA 21cm, PTA hc]
sigma_obs = np.array([5.0, 0.005, 0.01, 1.0, 1e-15])
probe_names = ["Planck (ISW)", "DESI (A_w)", "Euclid (S8)", "SKA (21cm)", "PTA (h_c)"]

# ---------------------------------------------------------------------------
# Jacobian (physical sensitivities from V8.2 ODE structure)
# ---------------------------------------------------------------------------
J = np.zeros((5, 3))
J[0, :] = [-15.4 / 7e19, 0.0, -15.4 / 2e-7]  # ISW ~ tau0, L
J[1, :] = [0.0, 0.0, 1.0]  # A_w ~ L
J[2, :] = [-0.02 / 7e19, -0.05 / 2.0, -0.10 / 2e-7]  # S8 ~ tau0, T, L
J[3, :] = [0.0, 15.0 / 2.0, 0.0]  # 21cm ~ T
J[4, :] = [1e-15 / 7e19, -1e-15 / 2.0, 1e-15 / 2e-7]  # hc ~ tau0, T, L

# Normalized Jacobian: J_norm[alpha,i] = dO_alpha/dtheta_i * theta_fid[i]
J_norm = J * theta_fid


def build_fisher(J_norm, sigma_obs):
    """Build 3x3 Fisher matrix from normalized Jacobian and uncertainties."""
    F = np.zeros((3, 3))
    for alpha in range(len(sigma_obs)):
        F += (1.0 / sigma_obs[alpha] ** 2) * np.outer(
            J_norm[alpha, :], J_norm[alpha, :]
        )
    return F


def plot_ellipse(ax, cov_2d, n_std, **kwargs):
    """Plot 2D confidence ellipse."""
    delta_chi2 = 2.30 if n_std == 1 else 6.18
    eigenvalues, eigenvectors = np.linalg.eigh(cov_2d)
    order = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    angle = np.degrees(np.arctan2(*eigenvectors[:, 0][::-1]))
    width = 2 * np.sqrt(eigenvalues[0] * delta_chi2)
    height = 2 * np.sqrt(eigenvalues[1] * delta_chi2)
    ellip = Ellipse(xy=(0, 0), width=width, height=height, angle=angle, **kwargs)
    ax.add_patch(ellip)


def main():
    print("=" * 60)
    print("V8.2 Multi-Probe Fisher Forecast")
    print("=" * 60)

    os.makedirs(PLOTS_DIR, exist_ok=True)

    # Build total Fisher
    F_total = build_fisher(J_norm, sigma_obs)
    C_total = np.linalg.inv(F_total)
    sigma_rel = np.sqrt(np.diag(C_total))

    print("\n[1] Fisher Matrix (normalized):")
    print(F_total)

    print("\n[2] Marginalized relative errors (1-sigma):")
    for i, name in enumerate(param_labels_short):
        abs_err = sigma_rel[i] * theta_fid[i]
        print(f"  {name:>5}: {sigma_rel[i]*100:.4f}%  (abs: +/- {abs_err:.2e})")

    # Individual probe contributions
    print("\n[3] Per-probe Fisher contribution (trace):")
    for alpha in range(5):
        F_probe = (1.0 / sigma_obs[alpha] ** 2) * np.outer(
            J_norm[alpha, :], J_norm[alpha, :]
        )
        print(f"  {probe_names[alpha]:>20}: tr(F) = {np.trace(F_probe):.4e}")

    # Correlation matrix
    corr = np.zeros_like(C_total)
    for i in range(3):
        for j in range(3):
            corr[i, j] = C_total[i, j] / np.sqrt(C_total[i, i] * C_total[j, j])
    print("\n[4] Parameter correlation matrix:")
    print(corr)

    # Plot
    plt.style.use("dark_background")
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    plt.subplots_adjust(wspace=0.35)

    pairs = [(0, 1), (0, 2), (1, 2)]

    for idx, (i, j) in enumerate(pairs):
        ax = axes[idx]
        cov_2d = np.array(
            [[C_total[i, i], C_total[i, j]], [C_total[j, i], C_total[j, j]]]
        )

        plot_ellipse(
            ax,
            cov_2d,
            2,
            facecolor="cyan",
            edgecolor="cyan",
            alpha=0.3,
            label=r"95% CL (2$\sigma$)",
        )
        plot_ellipse(
            ax,
            cov_2d,
            1,
            facecolor="lime",
            edgecolor="lime",
            alpha=0.6,
            label=r"68% CL (1$\sigma$)",
        )
        ax.plot(0.0, 0.0, "r+", markersize=12, markeredgewidth=2, label="Fiducial")

        margin_i = 4 * sigma_rel[i]
        margin_j = 4 * sigma_rel[j]
        ax.set_xlim(-margin_i, margin_i)
        ax.set_ylim(-margin_j, margin_j)

        ax.set_xlabel(r"$\Delta$" + param_names[i] + r" / $\theta_{fid}$", fontsize=12)
        ax.set_ylabel(r"$\Delta$" + param_names[j] + r" / $\theta_{fid}$", fontsize=12)
        ax.grid(True, linestyle=":", alpha=0.3)
        if idx == 0:
            ax.legend(fontsize=9, loc="upper right")

    fig.suptitle(
        "OBT V8.2: Multi-Probe Fisher Forecast\nPlanck + DESI + Euclid + SKA + PTA",
        fontsize=14,
        fontweight="bold",
        color="white",
    )

    out = os.path.join(PLOTS_DIR, "fisher_forecast.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="black")
    plt.close(fig)
    print(f"\n  Saved: {out}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for i, name in enumerate(param_labels_short):
        print(f"  sigma({name})/theta = {sigma_rel[i]*100:.4f}%")
    print(f"  Correlation(tau0,T) = {corr[0,1]:.3f}")
    print(f"  Correlation(tau0,L) = {corr[0,2]:.3f}")
    print(f"  Correlation(T,L)   = {corr[1,2]:.3f}")
    print(f"  1 plot generated")
    print("=" * 60)


if __name__ == "__main__":
    main()
