#!/usr/bin/env python3
"""
Ab Initio Airy-Yukawa Matrix Elements — V8.2
=============================================

Exact quantum mechanical derivation of the transition matrix element
<1|δV|6> for the qBOUNCE experiment (ILL Grenoble), replacing the
phenomenological exponential fit with an ab initio calculation.

Physics:
  - Unperturbed system: quantum bouncer (neutron in linear gravity)
  - Eigenstates: Airy functions ψ_n(z) = N_n Ai(z/z0 - ε_n)
  - Perturbation: Yukawa potential δV(z) = V_0 exp(-z/L) from L = 0.2 μm
  - Analytical limit (L ≪ z0): <1|δV|6> ≈ -2 V_0 (L/z0)^3
  - Numerical validation: 97.5% agreement with exact integration

The analytical result emerges from Taylor-expanding the Airy functions
near the mirror surface (z ≈ 0), where the Yukawa exponential concentrates
the integrand, reducing the overlap integral to a standard Gamma function.

References:
  - Jenke et al. (2014): qBOUNCE Rabi spectroscopy
  - Abele, Jenke et al.: Gravitational quantum states
  - Albeverio et al. (2005): Self-adjoint extensions (Robin parameter)

Output:
  plots/qbounce_airy_yukawa.png — Matrix element convergence plot

Version: 8.2
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.special import ai_zeros, airy

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
m_n = 1.674927471e-27  # Neutron mass (kg)
g = 9.80665  # Gravitational acceleration (m/s^2)
hbar = 1.054571817e-34  # Reduced Planck constant (J s)

# Characteristic scales
z0 = (hbar**2 / (2 * m_n**2 * g)) ** (1 / 3)  # Gravitational length scale
z0_um = z0 * 1e6  # ~ 5.8686 μm
L_phys = 0.2  # Extra dimension size (μm)
L_scaled = L_phys / z0_um  # Dimensionless ratio L/z0 ~ 0.034

PLOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plots")

# ---------------------------------------------------------------------------
# Airy zeros and normalization
# ---------------------------------------------------------------------------
# ai_zeros returns (a, ap, ai, aip):
#   a[n]   = n-th zero of Ai(x)        (negative: -2.338, -4.088, ...)
#   ap[n]  = n-th zero of Ai'(x)       (negative: -1.019, -3.248, ...)
#   ai[n]  = Ai(ap[n])                 (value of Ai at zeros of Ai')
#   aip[n] = Ai'(a[n])                 (derivative of Ai at zeros of Ai → normalization!)
a_zeros, _, _, deriv_at_zeros = ai_zeros(10)


def psi_scaled(n, u):
    """Normalized wavefunction in dimensionless units u = z/z0.

    ψ_n(u) = Ai(u + a_n) / |Ai'(a_n)|

    where a_n < 0 is the n-th zero of Ai, so ψ_n(0) = Ai(a_n) = 0 (Dirichlet BC).
    Normalization: ∫₀^∞ ψ_n² du = [Ai'(a_n)]² / [Ai'(a_n)]² = 1.
    Identity: ∫_{a_n}^∞ Ai²(t) dt = [Ai'(a_n)]² (from Airy DE antiderivative).
    """
    idx = n - 1
    ai_val, _, _, _ = airy(u + a_zeros[idx])
    norm = np.abs(deriv_at_zeros[idx])
    return ai_val / norm


# ---------------------------------------------------------------------------
# Exact numerical integration
# ---------------------------------------------------------------------------
def integrand_mn(u, m, n, L_ratio):
    """Integrand for <m|δV|n> in dimensionless units."""
    return psi_scaled(m, u) * psi_scaled(n, u) * np.exp(-u / L_ratio)


def compute_matrix_element(m, n, L_ratio):
    """Compute <m|δV|n> / V_0 via numerical quadrature."""
    result, error = quad(
        integrand_mn, 0, 50, args=(m, n, L_ratio), limit=1000, epsabs=1e-15
    )
    return result


# ---------------------------------------------------------------------------
# Analytical approximation (Taylor expansion near z=0)
# ---------------------------------------------------------------------------
def analytical_16(L_ratio):
    """Analytical limit: <1|δV|6> ≈ -2 V_0 (L/z0)^3.

    Derivation:
      Near z=0, Ai(z/z0 - ε_n) ≈ Ai'(-ε_n) * (z/z0) since Ai(-ε_n)=0.
      Normalized: ψ_n(z) ≈ sgn(Ai'(-ε_n)) * z/z0^{3/2}
      Product: ψ_1 * ψ_6 ≈ -z^2/z0^3 (sign alternates)
      Integral: ∫ z^2 e^{-z/L} dz = 2L^3 (Gamma function)
      Result: <1|δV|6> ≈ -2(L/z0)^3 * V_0
    """
    return -2.0 * L_ratio**3


# ---------------------------------------------------------------------------
# Scan over L values
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("V8.2 Ab Initio Airy-Yukawa Matrix Elements")
    print("=" * 70)

    os.makedirs(PLOTS_DIR, exist_ok=True)

    print(f"\n  Gravitational length z0 = {z0_um:.4f} μm")
    print(f"  Extra dimension L       = {L_phys} μm")
    print(f"  Ratio L/z0              = {L_scaled:.5f}")

    # --- Single point validation ---
    print("\n[1] Exact matrix element <1|δV|6> at L = 0.2 μm:")
    I_16_num = compute_matrix_element(1, 6, L_scaled)
    I_16_ana = analytical_16(L_scaled)
    ratio = I_16_num / I_16_ana * 100

    print(f"  Numerical (exact):  {I_16_num:.6e} × V₀")
    print(f"  Analytical (-2L³): {I_16_ana:.6e} × V₀")
    print(f"  Agreement:          {ratio:.1f}%")

    # --- Diagonal elements ---
    print("\n[2] Diagonal matrix elements <n|δV|n>:")
    for n in range(1, 7):
        I_nn = compute_matrix_element(n, n, L_scaled)
        print(f"  <{n}|δV|{n}> = {I_nn:.6e} × V₀")

    # --- Scan over L ---
    print("\n[3] Scanning L/z0 ratio...")
    L_ratios = np.logspace(-2, -0.3, 50)
    numerical_vals = []
    analytical_vals = []

    for lr in L_ratios:
        numerical_vals.append(compute_matrix_element(1, 6, lr))
        analytical_vals.append(analytical_16(lr))

    numerical_vals = np.array(numerical_vals)
    analytical_vals = np.array(analytical_vals)
    agreement = numerical_vals / analytical_vals * 100

    # --- Plot ---
    plt.style.use("dark_background")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), height_ratios=[2, 1])

    # Top panel: matrix elements
    ax1.plot(
        L_ratios * z0_um,
        np.abs(numerical_vals),
        color="cyan",
        linewidth=2,
        label=r"Numerical $|\langle 1|\delta V|6\rangle|$ (exact)",
    )
    ax1.plot(
        L_ratios * z0_um,
        np.abs(analytical_vals),
        color="lime",
        linewidth=2,
        linestyle="--",
        label=r"Analytical $2(L/z_0)^3$",
    )
    ax1.axvline(L_phys, color="red", linestyle=":", alpha=0.7, label=f"L = {L_phys} μm")
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel(r"Extra dimension $L$ (μm)", fontsize=12)
    ax1.set_ylabel(r"$|\langle 1|\delta V|6\rangle| / V_0$", fontsize=12)
    ax1.set_title(
        r"Ab Initio Airy-Yukawa Matrix Element: $\langle 1|\delta V|6\rangle$",
        fontsize=13,
    )
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.2)

    ax1.text(
        0.03,
        0.05,
        rf"At $L = {L_phys}\,\mu$m:"
        + "\n"
        + rf"Numerical = ${I_16_num:.3e} \times V_0$"
        + "\n"
        + rf"Analytical = ${I_16_ana:.3e} \times V_0$"
        + "\n"
        + rf"Agreement = {ratio:.1f}%",
        transform=ax1.transAxes,
        fontsize=10,
        color="white",
        verticalalignment="bottom",
        bbox=dict(boxstyle="round", facecolor="black", edgecolor="cyan", alpha=0.9),
    )

    # Bottom panel: agreement ratio
    ax2.plot(L_ratios * z0_um, agreement, color="gold", linewidth=2)
    ax2.axhline(100, color="white", linestyle="--", alpha=0.3)
    ax2.axhline(97.5, color="lime", linestyle=":", alpha=0.5, label="97.5%")
    ax2.axvline(L_phys, color="red", linestyle=":", alpha=0.7)
    ax2.set_xscale("log")
    ax2.set_xlabel(r"Extra dimension $L$ (μm)", fontsize=12)
    ax2.set_ylabel("Numerical / Analytical (%)", fontsize=12)
    ax2.set_title("Convergence of Analytical Approximation", fontsize=13)
    ax2.set_ylim(80, 105)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.2)

    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, "qbounce_airy_yukawa.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="black")
    plt.close(fig)
    print(f"\n  Saved: {out}")

    # --- Summary ---
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Analytical result: <1|δV|6> = -2 V₀ (L/z₀)³")
    print(f"  At L = {L_phys} μm: agreement = {ratio:.1f}% with exact integration")
    print(f"  The phenomenological fit λ(z) is NOW REPLACED by ab initio QM")
    print(f"  1 plot generated")
    print("=" * 70)


if __name__ == "__main__":
    main()
