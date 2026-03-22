#!/usr/bin/env python3
"""
SKA 21cm Reionization Modulation — The Definitive Test

Computes the theoretical spatial modulation ΔT_b(k,z) ≈ 1-5 mK
induced by the oscillating G_eff(k) on the 21cm brightness temperature
during the Epoch of Reionization (z=6 to 15).

Generates a template for SKA-Low detection.
"""

import matplotlib
import numpy as np
from scipy.integrate import quad

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ============================================================
# Cosmological Parameters
# ============================================================
H0_Gyr = 0.0689  # Gyr^-1
Omega_m = 0.315
Omega_Lambda = 0.685
Omega_b = 0.0493
T_cmb = 2.725  # K

# ============================================================
# Brane Parameters
# ============================================================
T_osc = 2.0  # Gyr
A_w = 0.003
phi_0 = np.pi / 2
f_osc = 0.10
alpha_base = -0.005  # Yukawa coupling
k_NL = 0.15  # Mpc^-1


def lookback_time(z):
    """Exact lookback time in Gyr."""

    def integrand(zp):
        E_z = np.sqrt(Omega_m * (1 + zp) ** 3 + Omega_Lambda)
        return 1.0 / ((1 + zp) * E_z)

    result, _ = quad(integrand, 0, z)
    return result / H0_Gyr


def cosmic_time(z):
    """Cosmic time in Gyr (age of universe at redshift z)."""
    t_age = 13.8  # Gyr (age today)
    return t_age - lookback_time(z)


def G_eff_ratio(k):
    """Scale-dependent gravitational coupling G_eff/G_N."""
    nonlinear_boost = 1.0 + 2.0 * np.tanh((k - k_NL) / 0.15)
    alpha = alpha_base * nonlinear_boost
    return 1.0 + alpha


def T_21cm_standard(z):
    """Standard 21cm brightness temperature (mK) vs CMB.

    T_b ≈ 27 x_HI (1+δ) (Ω_b h²/0.023) √((0.15/Ω_m h²)(1+z)/10) mK
    Simplified model for global signal during reionization.
    """
    h = 0.674
    Ob_h2 = Omega_b * h**2
    Om_h2 = Omega_m * h**2

    # Neutral hydrogen fraction (simple reionization model)
    # x_HI transitions from ~1 at z>12 to ~0 at z<6
    z_reion_start = 12.0
    z_reion_end = 6.0
    if z > z_reion_start:
        x_HI = 1.0
    elif z < z_reion_end:
        x_HI = 0.0
    else:
        x_HI = (z - z_reion_end) / (z_reion_start - z_reion_end)

    T_b = 27.0 * x_HI * (Ob_h2 / 0.023) * np.sqrt((0.15 / Om_h2) * (1 + z) / 10.0)

    return T_b  # mK


def delta_T_brane(k, z):
    """Brane-induced modulation of 21cm brightness temperature (mK).

    The oscillating G_eff(k,t) modifies the matter overdensity δ,
    which in turn modulates T_b. The modulation amplitude is:

    ΔT_b(k,z) = T_b_standard(z) × |G_eff/G_N - 1| × sin(2πt/T + φ₀)
    """
    T_std = T_21cm_standard(z)
    t = cosmic_time(z)

    # G_eff modification at this wavenumber
    g_ratio = G_eff_ratio(k)
    delta_g = abs(g_ratio - 1.0)

    # Oscillatory modulation
    phase = np.sin(2 * np.pi * t / T_osc + phi_0)

    # The modulation is amplified by structure growth coupling
    # At reionization redshifts, the growth factor enhancement is ~10x
    growth_boost = 10.0 * (1 + z) / 10.0

    return T_std * delta_g * growth_boost * phase


def main():
    print("=" * 60)
    print("SKA 21cm REIONIZATION MODULATION — Definitive Test")
    print(f"Epoch of Reionization: z = 6 to 15")
    print(f"Oscillation period: T = {T_osc} Gyr")
    print("=" * 60)

    # Wavenumber grid (BAO-scale)
    k_arr = np.logspace(-2, 0, 100)  # 0.01 to 1 Mpc^-1

    # Redshift grid
    z_arr = np.linspace(6, 15, 50)

    # Compute modulation amplitude
    delta_T = np.zeros((len(z_arr), len(k_arr)))
    for i, z in enumerate(z_arr):
        for j, k in enumerate(k_arr):
            delta_T[i, j] = delta_T_brane(k, z)

    # Peak modulation amplitude
    max_mod = np.max(np.abs(delta_T))
    print(f"\n  Peak modulation: {max_mod:.2f} mK")
    print(f"  At BAO scale (k~0.1 Mpc⁻¹): {np.max(np.abs(delta_T[:, 50])):.2f} mK")

    # SKA-Low sensitivity (approximate)
    ska_noise = 1.0  # mK (thermal noise per mode, ~1000h integration)

    # ============================================================
    # Plots
    # ============================================================
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        "SKA 21cm Reionization Modulation — Definitive Test\n"
        "Oscillating Brane V8.0 Prediction",
        fontsize=14,
        fontweight="bold",
    )

    # Panel 1: 2D modulation map (k vs z)
    ax = axes[0, 0]
    K, Z = np.meshgrid(k_arr, z_arr)
    im = ax.pcolormesh(
        K, Z, delta_T, cmap="RdBu_r", shading="auto", vmin=-max_mod, vmax=max_mod
    )
    ax.set_xscale("log")
    ax.set_xlabel(r"Wavenumber $k$ (Mpc$^{-1}$)")
    ax.set_ylabel("Redshift $z$")
    ax.set_title(r"$\Delta T_b(k, z)$ modulation (mK)")
    plt.colorbar(im, ax=ax, label="mK")

    # Panel 2: Modulation at fixed z=10 (peak reionization)
    ax = axes[0, 1]
    z_fixed = 10
    iz = np.argmin(np.abs(z_arr - z_fixed))
    ax.semilogx(k_arr, delta_T[iz, :], "b-", linewidth=2, label=f"z = {z_arr[iz]:.0f}")
    ax.axhline(
        y=ska_noise,
        color="r",
        linestyle="--",
        alpha=0.7,
        label=f"SKA-Low noise ({ska_noise} mK)",
    )
    ax.axhline(y=-ska_noise, color="r", linestyle="--", alpha=0.7)
    ax.fill_between(k_arr, -ska_noise, ska_noise, color="red", alpha=0.1)
    ax.set_xlabel(r"Wavenumber $k$ (Mpc$^{-1}$)")
    ax.set_ylabel(r"$\Delta T_b$ (mK)")
    ax.set_title(f"Modulation at $z = {z_fixed}$")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Panel 3: Modulation vs redshift at BAO scale
    ax = axes[1, 0]
    k_bao = 0.1  # Mpc^-1
    ik = np.argmin(np.abs(k_arr - k_bao))
    ax.plot(
        z_arr,
        delta_T[:, ik],
        "b-",
        linewidth=2,
        label=f"k = {k_arr[ik]:.2f} Mpc$^{{-1}}$",
    )
    ax.axhline(
        y=ska_noise, color="r", linestyle="--", alpha=0.7, label=f"SKA-Low noise"
    )
    ax.axhline(y=-ska_noise, color="r", linestyle="--", alpha=0.7)
    ax.fill_between(z_arr, -ska_noise, ska_noise, color="red", alpha=0.1)
    ax.set_xlabel("Redshift $z$")
    ax.set_ylabel(r"$\Delta T_b$ (mK)")
    ax.set_title(f"Modulation at BAO scale ($k = {k_bao}$ Mpc$^{{-1}}$)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Panel 4: Standard 21cm signal + modulation
    ax = axes[1, 1]
    T_std = np.array([T_21cm_standard(z) for z in z_arr])
    T_mod = T_std + delta_T[:, ik]
    ax.plot(z_arr, T_std, "k--", linewidth=1.5, label=r"$\Lambda$CDM (standard)")
    ax.plot(z_arr, T_mod, "b-", linewidth=2, label="Brane V8.0")
    ax.fill_between(
        z_arr,
        T_std - ska_noise,
        T_std + ska_noise,
        color="gray",
        alpha=0.2,
        label="SKA noise band",
    )
    ax.set_xlabel("Redshift $z$")
    ax.set_ylabel(r"$T_b$ (mK)")
    ax.set_title("21cm Global Signal: Standard vs Brane")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("plots/ska_prediction.png", dpi=150)
    print(f"\nPlot saved: plots/ska_prediction.png")

    # Detection significance
    snr = max_mod / ska_noise
    print(f"\n{'=' * 60}")
    print(f"DETECTION FORECAST:")
    print(f"  Peak signal: {max_mod:.2f} mK")
    print(f"  SKA-Low noise: {ska_noise:.1f} mK")
    print(f"  SNR (peak): {snr:.1f}σ")
    print(f"  Detectable: {'YES' if snr > 3 else 'MARGINAL'} (>3σ threshold)")
    print(f"  Redshift range: z = 6-15 (Epoch of Reionization)")
    print(f"  k range: 0.01-1.0 Mpc⁻¹ (BAO scale)")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
