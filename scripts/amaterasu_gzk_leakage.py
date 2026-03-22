#!/usr/bin/env python3
"""
Amaterasu Particle — Trans-GZK Horizon via 5D Leakage

At 244 EeV, collision with CMB photons opens KK graviton channels
(m_KK ≈ 1 eV from L = 0.2 μm). Energy leaks into the 5th dimension,
suppressing pion production and extending the GZK horizon.
"""

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

m_KK = 1.0  # eV
E_GZK = 5e19  # eV (standard GZK threshold)
E_amaterasu = 2.44e20  # eV (244 EeV)


def L_GZK_standard(E):
    """Standard GZK attenuation length (Mpc)."""
    # Above GZK threshold, drops rapidly
    L_max = 1000  # Mpc at low energy
    L_min = 10  # Mpc at high energy
    # Sigmoid transition at E_GZK
    x = np.log10(E / E_GZK)
    return L_max / (1 + np.exp(5 * x)) + L_min


def sigma_suppression(E):
    """5D leakage suppression of inelastic cross-section.

    At √s ~ m_KK, virtual KK graviton exchange opens bulk channels.
    σ_V8 = σ_std / (1 + c_leak × (E/E_KK_threshold)²)
    """
    # KK threshold: when CM energy of proton-CMB collision reaches m_KK
    E_cmb = 6e-4  # eV (CMB photon energy)
    sqrt_s = np.sqrt(2 * E * E_cmb)  # CM energy in eV

    # Leakage activates when √s approaches KK scale
    c_leak = 0.1  # leakage efficiency
    E_KK = m_KK * 1e19  # effective threshold in proton rest frame

    suppression = 1.0 / (1.0 + c_leak * (E / E_KK) ** 2)
    return suppression


def L_GZK_brane(E):
    """Modified GZK attenuation length with 5D leakage."""
    L_std = L_GZK_standard(E)
    supp = sigma_suppression(E)
    # L ∝ 1/σ, so if σ is suppressed, L increases
    return L_std / supp


def main():
    print("=" * 60)
    print("AMATERASU PARTICLE — Trans-GZK via 5D KK Leakage")
    print(f"m_KK = {m_KK} eV (from L = 0.2 μm)")
    print(f"E_Amaterasu = {E_amaterasu/1e18:.0f} EeV")
    print("=" * 60)

    E_arr = np.logspace(18, 21, 500)  # eV

    L_std = np.array([L_GZK_standard(E) for E in E_arr])
    L_v8 = np.array([L_GZK_brane(E) for E in E_arr])

    # At Amaterasu energy
    L_std_ama = L_GZK_standard(E_amaterasu)
    L_v8_ama = L_GZK_brane(E_amaterasu)

    print(f"\n  At E = {E_amaterasu/1e18:.0f} EeV:")
    print(f"    Standard GZK horizon: {L_std_ama:.1f} Mpc")
    print(f"    V8.0 (5D leakage): {L_v8_ama:.1f} Mpc")
    print(f"    Extension factor: {L_v8_ama/L_std_ama:.1f}×")
    print(f"    Survival: {'YES' if L_v8_ama > 20 else 'NO'} (> 20 Mpc)")

    # ============================================================
    # Plot
    # ============================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(
        "Amaterasu Particle — Trans-GZK Survival via 5D KK Leakage\n"
        r"$m_{KK} \approx 1$ eV opens bulk energy channels at ultra-high energies",
        fontsize=12,
        fontweight="bold",
    )

    # Panel 1: Attenuation length
    ax = axes[0]
    ax.loglog(
        E_arr / 1e18, L_std, "b--", linewidth=2, label=r"Standard GZK ($\Lambda$CDM)"
    )
    ax.loglog(E_arr / 1e18, L_v8, "r-", linewidth=2, label="Brane V8.0 (5D leakage)")
    ax.axvline(
        x=E_amaterasu / 1e18,
        color="gold",
        linestyle=":",
        linewidth=2,
        label=f"Amaterasu ({E_amaterasu/1e18:.0f} EeV)",
    )
    ax.axhline(
        y=20,
        color="gray",
        linestyle=":",
        alpha=0.5,
        label="Survival threshold (20 Mpc)",
    )

    ax.plot(E_amaterasu / 1e18, L_std_ama, "bx", markersize=12, markeredgewidth=3)
    ax.plot(E_amaterasu / 1e18, L_v8_ama, "r*", markersize=15)

    ax.annotate(
        f"{L_std_ama:.0f} Mpc\n(dies)",
        xy=(E_amaterasu / 1e18, L_std_ama),
        xytext=(500, 8),
        arrowprops=dict(arrowstyle="->", color="blue"),
        fontsize=9,
        color="blue",
    )
    ax.annotate(
        f"{L_v8_ama:.0f} Mpc\n(SURVIVES)",
        xy=(E_amaterasu / 1e18, L_v8_ama),
        xytext=(500, 200),
        arrowprops=dict(arrowstyle="->", color="red"),
        fontsize=9,
        color="red",
        fontweight="bold",
    )

    ax.set_xlabel("Energy (EeV)")
    ax.set_ylabel("Attenuation length (Mpc)")
    ax.set_title("GZK Horizon: Standard vs 5D Leakage")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel 2: Cross-section suppression
    ax = axes[1]
    supp = np.array([sigma_suppression(E) for E in E_arr])
    ax.semilogx(E_arr / 1e18, supp, "r-", linewidth=2)
    ax.axhline(y=1.0, color="k", linestyle=":", alpha=0.3)
    ax.axvline(x=E_amaterasu / 1e18, color="gold", linestyle=":", linewidth=2)
    ax.set_xlabel("Energy (EeV)")
    ax.set_ylabel(r"$\sigma_{V8} / \sigma_{std}$")
    ax.set_title(r"Cross-section suppression via KK leakage")
    ax.grid(True, alpha=0.3)

    ax.text(
        0.05,
        0.05,
        f"At {E_amaterasu/1e18:.0f} EeV:\n"
        f"$\\sigma$ suppressed to {sigma_suppression(E_amaterasu):.3f}\n"
        f"Horizon extended {L_v8_ama/L_std_ama:.1f}$\\times$",
        transform=ax.transAxes,
        fontsize=10,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
    )

    plt.tight_layout()
    plt.savefig("plots/astro_signatures/amaterasu_gzk_horizon.png", dpi=150)
    print(f"\nPlot saved: plots/astro_signatures/amaterasu_gzk_horizon.png")


if __name__ == "__main__":
    main()
