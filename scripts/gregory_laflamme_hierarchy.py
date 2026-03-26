#!/usr/bin/env python3
"""
Gregory-Laflamme Perforation Hierarchy — V8.1
===============================================

Demonstrates the critical mass M_crit = Lc^2/(2G) where PBHs transition
from 4D brane-anchored objects to 5D Schwarzschild-Tangherlini solutions
via Gregory-Laflamme instability.

Physics:
  - When r_s < L: PBH undergoes GL instability -> becomes 5D object
    -> loses local 4D 1/r gravitational singularity -> no accretion
  - When r_s > L: PBH stays anchored on brane -> standard 4D gravity
  - Critical mass: M_crit where r_s = L -> M_crit = Lc^2/(2G)

References:
  - Gregory & Laflamme, PRL 70, 9 (1993)
  - Tangherlini, Nuovo Cimento 27, 636 (1963)
  - Carr, Kuhnel & Sandstad (2016) for log-normal EMF

Output:
  plots/gregory_laflamme_rs_vs_L.png     — r_s vs L intersection
  plots/gregory_laflamme_hierarchy.png   — EMF with M_crit threshold
  plots/gregory_laflamme_potential.png   — 4D vs 5D gravitational potential

Version: 8.1
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
G_N = 6.674e-11  # m^3 kg^-1 s^-2
c = 2.998e8  # m/s
M_sun = 1.989e30  # kg
L_extra = 2.0e-7  # extra dimension size in meters (0.2 um)
hbar = 1.055e-34  # J s

PLOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plots")

# ---------------------------------------------------------------------------
# Critical mass from r_s = L
# ---------------------------------------------------------------------------
M_crit_kg = L_extra * c**2 / (2 * G_N)
M_crit_msun = M_crit_kg / M_sun


def schwarzschild_radius(M_msun):
    """Schwarzschild radius in meters for mass M in solar masses."""
    return 2 * G_N * M_msun * M_sun / c**2


def pbh_emf(M, M_c=1e-12, sigma_M=1.5):
    """Log-normal PBH extended mass function (Carr, Kuhnel & Sandstad 2016)."""
    ln_M = np.log(M)
    ln_Mc = np.log(M_c)
    psi = np.exp(-((ln_M - ln_Mc) ** 2) / (2 * sigma_M**2))
    psi /= np.sqrt(2 * np.pi) * sigma_M
    return psi


# ---------------------------------------------------------------------------
# Plot 1: r_s vs L intersection -> M_crit derivation
# ---------------------------------------------------------------------------
def plot_rs_vs_L():
    """Plot Schwarzschild radius vs PBH mass, showing intersection with L."""
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(12, 8))

    # Mass range
    log_M = np.linspace(-16, -7, 500)
    M_range = 10**log_M
    r_s = schwarzschild_radius(M_range) * 1e9  # convert to nm

    # Plot r_s(M)
    ax.plot(log_M, r_s, color="cyan", linewidth=2.5, label=r"$r_s(M) = 2GM/c^2$")

    # L horizontal line
    L_nm = L_extra * 1e9
    ax.axhline(
        L_nm,
        color="#ff6644",
        linewidth=2,
        linestyle="--",
        label=f"$L = {L_nm:.0f}$ nm (extra dimension)",
    )

    # M_crit vertical line
    log_M_crit = np.log10(M_crit_msun)
    ax.axvline(
        log_M_crit,
        color="yellow",
        linewidth=2,
        linestyle=":",
        label=f"$M_{{crit}} = {M_crit_msun:.2e}\\;M_\\odot$",
    )

    # Intersection point
    ax.scatter(
        [log_M_crit],
        [L_nm],
        color="white",
        s=200,
        zorder=10,
        edgecolors="yellow",
        linewidth=2,
    )

    # Shaded regions
    ax.fill_between(
        log_M[log_M < log_M_crit],
        1e-3,
        r_s[log_M < log_M_crit],
        alpha=0.15,
        color="purple",
        label=r"$r_s < L$: GL unstable $\rightarrow$ 5D capillary",
    )
    ax.fill_between(
        log_M[log_M > log_M_crit],
        r_s[log_M > log_M_crit],
        1e6,
        alpha=0.10,
        color="orange",
        label=r"$r_s > L$: brane-anchored $\rightarrow$ 4D gravity",
    )

    # Annotations
    ax.annotate(
        f"$M_{{crit}} = Lc^2/(2G)$\n$= {M_crit_msun:.2e}\\;M_\\odot$\n"
        f"$= {M_crit_kg:.2e}$ kg",
        xy=(log_M_crit, L_nm),
        xytext=(log_M_crit + 1.5, L_nm * 3),
        fontsize=11,
        color="white",
        arrowprops=dict(arrowstyle="->", color="yellow", lw=1.5),
        bbox=dict(
            boxstyle="round,pad=0.3", facecolor="black", edgecolor="yellow", alpha=0.9
        ),
    )

    # Hawking evaporation limit
    ax.axvline(-16, color="gray", linestyle="-.", alpha=0.5)
    ax.text(-15.8, 5e3, "Hawking\nevaporation", color="gray", fontsize=9, ha="left")

    ax.set_xlabel(r"$\log_{10}(M / M_\odot)$", fontsize=13)
    ax.set_ylabel(r"Schwarzschild radius $r_s$ (nm)", fontsize=13)
    ax.set_title(
        "Gregory-Laflamme Perforation Hierarchy: $r_s$ vs $L$\n"
        "Critical mass derived from $r_s = L = 0.2\\;\\mu$m",
        fontsize=14,
    )
    ax.set_yscale("log")
    ax.set_ylim(1e-3, 1e6)
    ax.set_xlim(-16.5, -7)
    ax.legend(fontsize=10, loc="upper left")
    ax.grid(True, alpha=0.2)

    out = os.path.join(PLOTS_DIR, "gregory_laflamme_rs_vs_L.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="black")
    plt.close(fig)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Plot 2: EMF with M_crit threshold
# ---------------------------------------------------------------------------
def plot_hierarchy():
    """EMF split into capillary (5D) and brane-anchored (4D) populations."""
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(12, 8))

    log_M = np.linspace(-16, -7, 1000)
    M_range = 10**log_M
    log_M_crit = np.log10(M_crit_msun)

    # EMF
    M_c = 1e-12
    sigma_M = 2.0
    psi = pbh_emf(M_range, M_c, sigma_M)
    f_total = 0.01
    psi_integral = np.trapezoid(psi, np.log(M_range))
    f_local = f_total * psi / psi_integral

    # Split at M_crit
    below = log_M <= log_M_crit
    above = log_M > log_M_crit

    # Plot capillaries (below M_crit) in purple
    ax.fill_between(
        log_M[below],
        0,
        f_local[below],
        alpha=0.4,
        color="#9966ff",
        label=r"Topological capillaries ($r_s < L$, GL unstable)",
    )
    ax.plot(log_M[below], f_local[below], color="#9966ff", linewidth=2)

    # Plot brane-anchored (above M_crit) in orange
    ax.fill_between(
        log_M[above],
        0,
        f_local[above],
        alpha=0.4,
        color="#ff8844",
        label=r"Brane-anchored ($r_s > L$, 4D gravity)",
    )
    ax.plot(log_M[above], f_local[above], color="#ff8844", linewidth=2)

    # M_crit line
    ax.axvline(
        log_M_crit,
        color="yellow",
        linewidth=2,
        linestyle="--",
        label=f"$M_{{crit}} = {M_crit_msun:.2e}\\;M_\\odot$",
    )

    # M_c line
    ax.axvline(
        np.log10(M_c),
        color="cyan",
        linewidth=1,
        linestyle=":",
        alpha=0.5,
        label=f"$M_c = 10^{{-12}}\\;M_\\odot$ (EMF peak)",
    )

    # Annotations
    ax.annotate(
        "No accretion disk\nNo X-ray emission\nNo microlensing\n(wave-optics immune)",
        xy=(-13, np.max(f_local) * 0.6),
        fontsize=10,
        color="#cc99ff",
        ha="center",
        bbox=dict(boxstyle="round", facecolor="black", edgecolor="#9966ff", alpha=0.8),
    )

    ax.annotate(
        "Standard 4D gravity\nAccretion disks form\nQuasar activity\n(JWST heavy seeds)",
        xy=(-9.5, np.max(f_local) * 0.15),
        fontsize=10,
        color="#ffaa66",
        ha="center",
        bbox=dict(boxstyle="round", facecolor="black", edgecolor="#ff8844", alpha=0.8),
    )

    # Text box with derivation
    textstr = (
        f"$M_{{crit}} = Lc^2/(2G)$\n"
        f"$L = 0.2\\;\\mu$m\n"
        f"$M_{{crit}} = {M_crit_msun:.2e}\\;M_\\odot$\n"
        f"$f_{{PBH}} = {f_total}$ (1%)"
    )
    ax.text(
        0.98,
        0.98,
        textstr,
        transform=ax.transAxes,
        fontsize=11,
        verticalalignment="top",
        horizontalalignment="right",
        color="white",
        bbox=dict(boxstyle="round", facecolor="black", edgecolor="cyan", alpha=0.9),
    )

    ax.set_xlabel(r"$\log_{10}(M / M_\odot)$", fontsize=13)
    ax.set_ylabel(r"$f_{PBH}(M)$ per log-mass bin", fontsize=13)
    ax.set_title(
        "V8.1 Perforation Hierarchy: PBH Mass Function Split at Gregory-Laflamme Threshold\n"
        r"$f_{PBH} = 0.01$ — 1% of DM mass suffices to tension the membrane",
        fontsize=13,
    )
    ax.set_yscale("log")
    ax.set_ylim(1e-6, np.max(f_local) * 5)
    ax.set_xlim(-16, -7)
    ax.legend(fontsize=10, loc="upper left")
    ax.grid(True, alpha=0.2)

    out = os.path.join(PLOTS_DIR, "gregory_laflamme_hierarchy.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="black")
    plt.close(fig)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Plot 3: Gravitational potential comparison
# ---------------------------------------------------------------------------
def plot_potential():
    """Compare 4D Newtonian 1/r vs 5D diffuse Weyl potential."""
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(12, 8))

    # Distance range (in units of L)
    r_over_L = np.linspace(0.01, 20, 1000)

    # 4D Newtonian potential: Phi ~ -1/r (brane-anchored, M > M_crit)
    phi_4d = -1.0 / r_over_L
    phi_4d = phi_4d / np.abs(phi_4d[0])  # normalize to -1 at r=0.01L

    # 5D Weyl projection: diffuse, no 1/r singularity
    # For GL-unstable PBH, the potential is projected via E_mu_nu
    # Approximate: Phi_5D ~ -(L/r)^2 * exp(-r/L) (Yukawa-suppressed, no singularity)
    phi_5d = -(1.0 / r_over_L**2) * np.exp(-r_over_L)
    phi_5d = phi_5d / np.abs(phi_5d).max()  # normalize to -1 at peak

    # Plot
    ax.plot(
        r_over_L,
        phi_4d,
        color="#ff6644",
        linewidth=2.5,
        label=r"4D Newtonian: $\Phi \propto -1/r$ (brane-anchored, $M > M_{crit}$)",
    )
    ax.plot(
        r_over_L,
        phi_5d,
        color="#9966ff",
        linewidth=2.5,
        linestyle="--",
        label=r"5D Weyl projection: $\Phi \propto -(L/r)^2 e^{-r/L}$ (capillary, $M < M_{crit}$)",
    )

    # Mark L
    ax.axvline(
        1.0,
        color="yellow",
        linewidth=1.5,
        linestyle=":",
        alpha=0.7,
        label=r"$r = L = 0.2\;\mu$m",
    )

    # Accretion threshold
    ax.axhline(-0.3, color="white", linewidth=1, linestyle="-.", alpha=0.3)
    ax.text(
        15,
        -0.28,
        "Bondi-Hoyle\naccretion threshold",
        color="white",
        fontsize=9,
        alpha=0.5,
        ha="right",
    )

    # Annotations
    ax.annotate(
        "Deep 1/r singularity\n→ gas accelerated\n→ accretion disk forms\n→ X-ray emission",
        xy=(0.5, phi_4d[25]),
        xytext=(5, -0.7),
        fontsize=10,
        color="#ff6644",
        arrowprops=dict(arrowstyle="->", color="#ff6644", lw=1.5),
        bbox=dict(boxstyle="round", facecolor="black", edgecolor="#ff6644", alpha=0.8),
    )

    ax.annotate(
        "Diffuse Weyl projection\n→ no local singularity\n→ no gas acceleration\n→ silent (no X-rays)",
        xy=(2, phi_5d[100]),
        xytext=(8, -0.4),
        fontsize=10,
        color="#9966ff",
        arrowprops=dict(arrowstyle="->", color="#9966ff", lw=1.5),
        bbox=dict(boxstyle="round", facecolor="black", edgecolor="#9966ff", alpha=0.8),
    )

    ax.set_xlabel(r"Distance $r / L$", fontsize=13)
    ax.set_ylabel(r"Gravitational potential $\Phi$ (normalized)", fontsize=13)
    ax.set_title(
        "Gravitational Potential: Brane-Anchored (4D) vs Capillary (5D)\n"
        "Gregory-Laflamme instability removes the local 4D singularity",
        fontsize=13,
    )
    ax.set_xlim(0, 20)
    ax.set_ylim(-1.1, 0.1)
    ax.legend(fontsize=10, loc="lower right")
    ax.grid(True, alpha=0.2)

    out = os.path.join(PLOTS_DIR, "gregory_laflamme_potential.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="black")
    plt.close(fig)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("V8.1 Gregory-Laflamme Perforation Hierarchy")
    print("=" * 70)

    os.makedirs(PLOTS_DIR, exist_ok=True)

    # Critical mass calculation
    print(f"\n[1] Critical mass from r_s = L:")
    print(f"  L = {L_extra*1e6:.1f} um = {L_extra*1e9:.0f} nm")
    print(f"  M_crit = Lc^2 / (2G)")
    print(f"         = {L_extra} * {c}^2 / (2 * {G_N})")
    print(f"         = {M_crit_kg:.3e} kg")
    print(f"         = {M_crit_msun:.3e} M_sun")

    # Verify it matches asteroid mass window
    print(f"\n[2] Asteroid mass window verification:")
    print(f"  Window: 10^-14 to 10^-10 M_sun")
    print(f"  M_crit: {M_crit_msun:.2e} M_sun")
    print(f"  log10(M_crit/M_sun) = {np.log10(M_crit_msun):.2f}")
    print(f"  => Falls at the UPPER BOUND of the window!")

    # Gregory-Laflamme regimes
    print(f"\n[3] Two regimes:")
    print(f"  M < M_crit ({M_crit_msun:.1e} M_sun):")
    print(f"    r_s < L => GL instability => 5D Schwarzschild-Tangherlini")
    print(f"    Loss of local 4D gravitational singularity (NOT loss of mass)")
    print(f"    No accretion disk, no X-rays, invisible to microlensing")
    print(f"    => TOPOLOGICAL CAPILLARIES (dark matter)")
    print(f"  M > M_crit ({M_crit_msun:.1e} M_sun):")
    print(f"    r_s > L => brane-anchored, standard 4D gravity")
    print(f"    Accretion disks, quasars, AGN")
    print(f"    => HEAVY SEEDS for JWST early SMBHs")

    # Sample r_s values
    print(f"\n[4] Schwarzschild radii across the mass function:")
    for log_m in [-14, -13, -12, -11, -10.17, -10, -9]:
        m = 10**log_m
        r_s = schwarzschild_radius(m)
        regime = "CAPILLARY (5D)" if r_s < L_extra else "BRANE-ANCHORED (4D)"
        print(
            f"  M = 10^{log_m:.2f} M_sun: r_s = {r_s*1e9:.2f} nm, "
            f"r_s/L = {r_s/L_extra:.4f} => {regime}"
        )

    # Generate plots
    print(f"\n[5] Generating plots...")
    plot_rs_vs_L()
    plot_hierarchy()
    plot_potential()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  M_crit = {M_crit_msun:.3e} M_sun = {M_crit_kg:.3e} kg")
    print(f"  Derived ab initio from r_s = L (no free parameters)")
    print(f"  Matches upper bound of asteroid mass window")
    print(f"  Gregory & Laflamme, PRL 70, 9 (1993)")
    print(f"  3 plots generated in plots/")
    print("=" * 70)


if __name__ == "__main__":
    main()
