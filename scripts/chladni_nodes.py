#!/usr/bin/env python3
"""
Chladni Resonance Nodes — Big Ring & Giant Arc

The universe-brane vibrates transversally with T = 2.0 Gyr.
Like a Chladni plate, 3D space forms acoustic-geometric standing waves.
Matter accumulates at nodal lines, producing mega-structures that
exceed ΛCDM's maximum clustering scale (370 Mpc).

The Big Ring (~400 Mpc) and Giant Arc (~1000 Mpc) are Chladni nodes.
"""

import numpy as np
from scipy.special import spherical_jn as _sph_jn

def sph_j(n, x):
    """Spherical Bessel j_n(x), handles scalar output."""
    val = _sph_jn(n, x)
    return float(val) if np.isscalar(val) else val
from scipy.integrate import quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ============================================================
# Cosmological Parameters
# ============================================================
H0 = 67.4           # km/s/Mpc
H0_Gyr = 0.0689
Omega_m = 0.315
Omega_Lambda = 0.685
c_km = 3e5           # km/s
T_osc = 2.0          # Gyr


def comoving_distance(z):
    """Comoving distance in Mpc."""
    def integrand(zp):
        E_z = np.sqrt(Omega_m * (1 + zp)**3 + Omega_Lambda)
        return c_km / (H0 * E_z)
    result, _ = quad(integrand, 0, z)
    return result


def lookback_time(z):
    """Lookback time in Gyr."""
    def integrand(zp):
        E_z = np.sqrt(Omega_m * (1 + zp)**3 + Omega_Lambda)
        return 1.0 / ((1 + zp) * E_z)
    result, _ = quad(integrand, 0, z)
    return result / H0_Gyr


def main():
    print("=" * 60)
    print("CHLADNI RESONANCE NODES — Big Ring & Giant Arc")
    print(f"Brane oscillation period: T = {T_osc} Gyr")
    print("=" * 60)

    # Effective wave speed: the brane oscillation propagates as a
    # geometric perturbation through expanding space.
    # v_eff = comoving_distance(z_eff) / lookback_time(z_eff)
    # At z ~ 0.8 (Big Ring redshift):
    z_eff = 0.8
    chi_eff = comoving_distance(z_eff)
    t_eff = lookback_time(z_eff)
    v_eff = chi_eff / t_eff  # Mpc/Gyr

    print(f"\n  Effective wave speed at z={z_eff}: {v_eff:.0f} Mpc/Gyr")

    # Fundamental spatial wavelength from T_osc
    lambda_fund = v_eff * T_osc
    k_fund = 2 * np.pi / lambda_fund

    print(f"  Fundamental wavelength: λ₀ = {lambda_fund:.0f} Mpc")
    print(f"  Fundamental wavenumber: k₀ = {k_fund:.5f} Mpc⁻¹")

    # Radial grid
    r = np.linspace(10, 2000, 1000)  # Mpc

    # Standing wave density modulation: spherical Bessel j₀
    # δρ/ρ ∝ [j₀(k₀r)]² + β[j₀(2k₀r)]² (fundamental + first overtone)
    j0_fund = np.array([sph_j(0, k_fund * ri) for ri in r])
    j0_over = np.array([sph_j(0, 2 * k_fund * ri) for ri in r])

    delta_rho = j0_fund**2 + 0.4 * j0_over**2

    # Normalize
    delta_rho /= np.max(delta_rho)

    # Find peaks (nodal accumulation zones)
    from scipy.signal import find_peaks
    peaks, properties = find_peaks(delta_rho, height=0.2, distance=50)
    peak_radii = r[peaks]
    peak_heights = delta_rho[peaks]

    print(f"\n  Density peaks (Chladni nodes):")
    for i, (rp, hp) in enumerate(zip(peak_radii, peak_heights)):
        gly = rp * 3.26e-3  # Mpc to Gly
        print(f"    Node {i+1}: r = {rp:.0f} Mpc ({gly:.1f} Gly), amplitude = {hp:.3f}")

    # ΛCDM max
    lambda_max_lcdm = 370  # Mpc
    print(f"\n  ΛCDM max clustering: {lambda_max_lcdm} Mpc")
    print(f"  Big Ring observed: ~400 Mpc (1.3 Gly)")
    print(f"  Giant Arc observed: ~1000 Mpc (3.3 Gly)")

    # ============================================================
    # 2D Chladni heatmap
    # ============================================================
    # Create 2D slice through the standing wave pattern
    N = 500
    x = np.linspace(-1500, 1500, N)
    y = np.linspace(-1500, 1500, N)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)

    # 2D pattern with angular modulation (ℓ=2 mode adds ring structure)
    theta = np.arctan2(Y, X)
    pattern = np.zeros_like(R)
    for i in range(N):
        for j in range(N):
            rij = R[i, j]
            if rij > 0:
                j0 = sph_j(0, k_fund * rij)
                j2 = sph_j(2, k_fund * rij) if rij > 1 else 0
                pattern[i, j] = j0**2 + 0.3 * j2**2 * np.cos(2 * theta[i, j])**2
            else:
                pattern[i, j] = 1.0

    pattern /= np.max(pattern)

    # ============================================================
    # Plot
    # ============================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(r'Chladni Resonance Nodes — Brane Standing Waves ($T = 2$ Gyr)'
                 '\nMatter accumulates at geometric nodes like sand on a vibrating plate',
                 fontsize=12, fontweight='bold')

    # Panel 1: Radial density profile
    ax = axes[0]
    ax.plot(r, delta_rho, 'b-', linewidth=2)
    ax.plot(peak_radii, peak_heights, 'rv', markersize=10, label='Chladni nodes')
    ax.axvline(x=400, color='orange', linestyle='--', alpha=0.7, label='Big Ring (~400 Mpc)')
    ax.axvline(x=1000, color='purple', linestyle='--', alpha=0.7, label='Giant Arc (~1000 Mpc)')
    ax.axvline(x=lambda_max_lcdm, color='gray', linestyle=':', alpha=0.5,
               label=f'$\\Lambda$CDM max ({lambda_max_lcdm} Mpc)')
    ax.set_xlabel('Comoving distance (Mpc)')
    ax.set_ylabel(r'$\delta\rho / \rho$ (normalized)')
    ax.set_title('Radial density modulation')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel 2: 2D Chladni heatmap
    ax = axes[1]
    im = ax.pcolormesh(X, Y, pattern, cmap='inferno', shading='auto')
    # Draw circles at Big Ring and Giant Arc scales
    theta_circle = np.linspace(0, 2 * np.pi, 100)
    ax.plot(400 * np.cos(theta_circle), 400 * np.sin(theta_circle),
            'w--', linewidth=1.5, label='Big Ring')
    ax.plot(1000 * np.cos(theta_circle), 1000 * np.sin(theta_circle),
            'c--', linewidth=1.5, label='Giant Arc')
    ax.set_xlabel('x (Mpc)')
    ax.set_ylabel('y (Mpc)')
    ax.set_title('2D Chladni pattern (cosmic slice)')
    ax.legend(fontsize=9, loc='upper right')
    ax.set_aspect('equal')
    plt.colorbar(im, ax=ax, label=r'$\delta\rho/\rho$')

    plt.tight_layout()
    plt.savefig('plots/astro_signatures/chladni_mega_structures.png', dpi=150)
    print(f"\nPlot saved: plots/astro_signatures/chladni_mega_structures.png")


if __name__ == '__main__':
    main()
