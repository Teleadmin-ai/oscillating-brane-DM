#!/usr/bin/env python3
"""
Scale-Dependent Growth Factor with Yukawa Screening — V7.0
============================================================

Solves the linear growth ODE delta_m(a, k) with a scale-dependent
effective gravitational constant G_eff(a, k) implementing Yukawa
screening from the extra dimension.

Physics:
  G_eff(a, k) = G_N * (1 - A_osc(a) * k^2 / (k^2 + k_Yukawa^2))

  - At large k (non-linear scales, DES): ~5% suppression
  - At small k (linear scales, KiDS/CMB): quasi-standard gravity

  Growth ODE (in scale factor a):
  D''(a) + [3/a + H'/H] D'(a) - (3/2) * Omega_m(a) * G_eff/G_N / (a^2 * E^2) * D(a) = 0

Output:
  plots/growth_scale_dependent.png

Version: 7.0
"""

import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# ---------------------------------------------------------------------------
# Cosmological parameters
# ---------------------------------------------------------------------------
H0_kmsMpc = 67.4
H0_inv_Gyr = 14.5      # 1/H0 in Gyr
Omega_m0 = 0.315
Omega_L0 = 0.685

# Yukawa screening parameters
L_extra = 2.0e-7        # extra dimension in meters
A_osc_max = 0.053       # max oscillation amplitude (tuned for ~5% suppression)
k_Yukawa = 0.05         # Yukawa screening scale in h/Mpc
a_activation = 0.1      # scale factor where oscillation activates (~QCD era)

PLOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plots")


# ---------------------------------------------------------------------------
# Cosmological functions
# ---------------------------------------------------------------------------
def E_squared(a):
    """Dimensionless Hubble parameter squared: E^2 = H^2/H0^2."""
    return Omega_m0 * a**(-3) + Omega_L0


def E(a):
    """Dimensionless Hubble parameter H/H0."""
    return np.sqrt(E_squared(a))


def Omega_m(a):
    """Matter density parameter at scale factor a."""
    return Omega_m0 * a**(-3) / E_squared(a)


def dlnE_dlna(a):
    """d ln E / d ln a for the Friedmann equation."""
    E2 = E_squared(a)
    dE2_da = -3 * Omega_m0 * a**(-4)
    return 0.5 * dE2_da * a / E2


# ---------------------------------------------------------------------------
# Scale-dependent G_eff with Yukawa screening
# ---------------------------------------------------------------------------
def A_osc(a):
    """Oscillation amplitude that activates after QCD freeze-out.

    Uses a smooth tanh activation centered on a_activation.
    """
    return A_osc_max * np.tanh(((a / a_activation) ** 3))


def G_eff_ratio(a, k):
    """G_eff(a, k) / G_N with Yukawa screening.

    G_eff/G_N = 1 - A_osc(a) * k^2 / (k^2 + k_Yukawa^2)

    - k >> k_Yukawa: G_eff/G_N ~ 1 - A_osc (full suppression)
    - k << k_Yukawa: G_eff/G_N ~ 1 (standard gravity)
    """
    yukawa_factor = k**2 / (k**2 + k_Yukawa**2)
    return 1.0 - A_osc(a) * yukawa_factor


# ---------------------------------------------------------------------------
# Growth ODE
# ---------------------------------------------------------------------------
def growth_ode(a, y, k):
    """Growth factor ODE in scale factor a.

    d^2 D / da^2 + [3/a + (d ln E / d ln a)/a] dD/da
        - (3/2) * Omega_m(a) * (G_eff/G_N) * D / (a^2 * E^2) = 0

    State: y = [D, dD/da]
    """
    D, dD = y

    E2 = E_squared(a)
    Om_a = Omega_m(a)
    dlnE = dlnE_dlna(a)

    # Coefficient of dD/da
    coeff_dD = (3.0 / a) + dlnE / a

    # Coefficient of D (gravitational source)
    Geff = G_eff_ratio(a, k)
    coeff_D = 1.5 * Om_a * Geff / (a**2 * E2) * (H0_kmsMpc * 1e3 / 3.086e22)**0  # dimensionless

    # Actually the proper form in terms of a:
    # D'' + [3/a + E'/E * 1/a] D' - (3/2) Omega_m0 / (a^5 E^2) * G_eff/G_N * D = 0
    # where E' = dE/da
    coeff_D_proper = 1.5 * Omega_m0 / (a**5 * E2) * Geff

    ddD = -coeff_dD * dD + coeff_D_proper * D
    return [dD, ddD]


def solve_growth(k, a_range=(0.001, 1.0), n_points=2000):
    """Solve the growth ODE for a given k.

    Initial conditions: D(a_init) = a_init, D'(a_init) = 1
    (matter-dominated growing mode).
    """
    a_eval = np.linspace(a_range[0], a_range[1], n_points)
    a_init = a_range[0]

    # Initial conditions (growing mode in matter era: D ~ a)
    y0 = [a_init, 1.0]

    sol = solve_ivp(
        lambda a, y: growth_ode(a, y, k),
        a_range, y0,
        method="RK45",
        t_eval=a_eval,
        rtol=1e-10,
        atol=1e-12,
    )

    if sol.success:
        return sol.t, sol.y[0]
    else:
        print(f"  Growth ODE failed for k={k}: {sol.message}")
        return None, None


# ---------------------------------------------------------------------------
# Main computation and plotting
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("V7.0 Scale-Dependent Growth Factor (Yukawa Screening)")
    print("=" * 70)

    os.makedirs(PLOTS_DIR, exist_ok=True)

    # k values to solve
    k_grid = np.logspace(-3, 1, 50)  # h/Mpc
    k_highlight = [0.001, 0.01, 0.05, 0.1, 0.5, 1.0]

    print(f"\n[1] Parameters:")
    print(f"  A_osc_max = {A_osc_max}")
    print(f"  k_Yukawa = {k_Yukawa} h/Mpc")
    print(f"  L = {L_extra*1e6:.1f} um")

    # Solve LCDM reference (k=0, no modification)
    print("\n[2] Solving LCDM reference growth...")
    a_lcdm, D_lcdm = solve_growth(k=0.0)
    D_lcdm_final = D_lcdm[-1]
    print(f"  D_LCDM(a=1) = {D_lcdm_final:.6f}")

    # Solve for each k
    print(f"\n[3] Solving growth for {len(k_grid)} k values...")
    D_ratio_final = np.zeros_like(k_grid)
    D_evolution = {}

    for i, k in enumerate(k_grid):
        a, D = solve_growth(k)
        if D is not None:
            D_ratio_final[i] = D[-1] / D_lcdm_final
            if k in k_highlight or any(abs(k - kh) / kh < 0.1 for kh in k_highlight):
                D_evolution[k] = (a, D / D_lcdm)

    print(f"  Done. D(a=1, k) / D_LCDM(a=1) range: "
          f"[{D_ratio_final.min():.4f}, {D_ratio_final.max():.4f}]")

    # Report key values
    print("\n[4] Growth suppression at key scales:")
    for k in k_highlight:
        idx = np.argmin(np.abs(k_grid - k))
        suppression = (1 - D_ratio_final[idx]) * 100
        print(f"  k = {k:.3f} h/Mpc: D/D_LCDM = {D_ratio_final[idx]:.4f} "
              f"({suppression:.1f}% suppression)")

    # Implied S8
    # S8 probes k ~ 0.1-0.3 h/Mpc
    k_s8 = 0.15
    idx_s8 = np.argmin(np.abs(k_grid - k_s8))
    S8_ratio = D_ratio_final[idx_s8]
    print(f"\n  Implied S8 ratio (at k~{k_s8}): {S8_ratio:.4f}")
    print(f"  S8 suppression: {(1-S8_ratio)*100:.1f}%")

    # --- Plotting ---
    print("\n[5] Generating plot...")
    plt.style.use("dark_background")
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(12, 10), height_ratios=[2, 1],
        gridspec_kw={"hspace": 0.12},
    )

    # --- Upper panel: D(k)/D_LCDM at a=1 ---
    ax1.plot(k_grid, D_ratio_final, color="#00ffcc", linewidth=2.5,
             label="V7.0 Yukawa screening")
    ax1.axhline(1.0, color="gray", linestyle=":", alpha=0.4)

    # Survey bands
    # DES Y3: k ~ 0.1-1 h/Mpc, S8 = 0.776 => suppression ~ 5-6%
    ax1.axvspan(0.1, 1.0, color="orange", alpha=0.08, label="DES Y3 range")
    # KiDS-1000: k ~ 0.05-0.5, less tension
    ax1.axvspan(0.01, 0.1, color="cyan", alpha=0.05, label="KiDS/CMB range")

    # Reference lines
    ax1.axhline(0.95, color="orange", linestyle="--", alpha=0.4,
                label=r"5% suppression ($S_8$ = 0.79)")
    ax1.axhline(0.99, color="cyan", linestyle="--", alpha=0.4,
                label="1% suppression")

    # Mark k_Yukawa
    ax1.axvline(k_Yukawa, color="yellow", linestyle=":", alpha=0.4,
                label=f"$k_{{Yukawa}}$ = {k_Yukawa} h/Mpc")

    ax1.set_xscale("log")
    ax1.set_xlabel(r"Wavenumber $k$ (h/Mpc)", fontsize=13)
    ax1.set_ylabel(r"$D(a=1, k) / D_{\Lambda CDM}(a=1)$", fontsize=13)
    ax1.set_title(
        r"V7.0: Scale-Dependent Growth Suppression via Yukawa Screening"
        "\n"
        r"$G_{eff}(k) = G_N \left(1 - A_{osc} \cdot k^2/(k^2 + k_Y^2)\right)$",
        fontsize=13,
    )
    ax1.set_ylim(0.92, 1.02)
    ax1.set_xlim(k_grid[0], k_grid[-1])
    ax1.legend(fontsize=9, loc="lower left")

    # --- Lower panel: D(a, k)/D_LCDM(a) for selected k ---
    colors_k = {"0.001": "white", "0.01": "#66ccff",
                "0.05": "#ffcc00", "0.1": "#ff9966",
                "0.5": "#ff6699", "1.0": "#cc66ff"}

    for k, (a, D_ratio) in sorted(D_evolution.items()):
        k_str = f"{k:.3f}"
        color = colors_k.get(k_str, "#00ffcc")
        label = f"k = {k} h/Mpc"
        ax2.plot(a, D_ratio, color=color, linewidth=1.5, label=label)

    ax2.axhline(1.0, color="gray", linestyle=":", alpha=0.4)
    ax2.set_xlabel("Scale factor $a$", fontsize=13)
    ax2.set_ylabel(r"$D(a,k) / D_{\Lambda CDM}(a)$", fontsize=13)
    ax2.set_ylim(0.92, 1.02)
    ax2.legend(fontsize=8, ncol=3, loc="lower left")

    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, "growth_scale_dependent.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="black")
    plt.close(fig)
    print(f"  Saved: {out}")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  DES scales (k~0.1-1):  ~{(1-D_ratio_final[np.argmin(np.abs(k_grid-0.3))])*100:.1f}% suppression")
    print(f"  KiDS/CMB (k~0.01):     ~{(1-D_ratio_final[np.argmin(np.abs(k_grid-0.01))])*100:.1f}% suppression")
    print(f"  => Scale-dependent: DES sees tension, KiDS/CMB see less")
    print("=" * 70)


if __name__ == "__main__":
    main()
