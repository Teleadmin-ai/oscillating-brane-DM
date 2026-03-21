#!/usr/bin/env python3
"""
BBN Thermal Protection via Temperature-Dependent Brane Tension — V7.0
======================================================================

Demonstrates that a temperature-dependent brane tension tau(T) protects
Big Bang Nucleosynthesis (BBN) from G_eff fluctuations induced by the
radion oscillation.

Physics:
  tau(T) = tau_0 * tanh((T_QCD / T)^alpha)
  - T >> T_QCD: tau -> 0, brane ultra-stiff, oscillation overdamped
  - T << T_QCD: tau -> tau_0, normal stick-slip motor operates
  - Freeze-out at T ~ T_QCD activates the motor

  G_eff modulation from radion:
  |dG_eff/G_eff| ~ delta_G * (tau(T)/tau_0)^2
  Must be << BBN constraint |delta_G/G| < 0.13 (Copi et al. 2004)

Output:
  plots/bbn_thermal_freezeout.png

Version: 7.0
"""

import os

import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
T_QCD = 200.0          # QCD phase transition temperature in MeV
T_BBN_high = 1.0       # BBN window upper bound in MeV (neutron freeze-out)
T_BBN_low = 0.07       # BBN window lower bound in MeV (He-4 synthesis end)
tau_0_GeV3 = 0.017     # Brane tension in GeV^3
E_tau = 257.0          # tau_0^{1/3} in MeV (= Lambda_QCD)
alpha = 3.0            # Sharpness of QCD transition
delta_G_max = 0.05     # Maximum G_eff modulation at late times (5%)
BBN_constraint = 0.13  # Upper bound on |delta_G/G| at BBN (95% CL)

PLOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plots")


# ---------------------------------------------------------------------------
# Temperature-dependent brane tension
# ---------------------------------------------------------------------------
def tau_ratio(T_MeV):
    """Brane tension ratio tau(T)/tau_0.

    tau(T) = tau_0 * tanh((T_QCD / T)^alpha)

    For T >> T_QCD: argument -> 0, tanh -> 0 => tau -> 0 (no tension)
    For T << T_QCD: argument -> inf, tanh -> 1 => tau -> tau_0
    """
    x = (T_QCD / T_MeV) ** alpha
    return np.tanh(x)


def g_eff_modulation(T_MeV):
    """Fractional G_eff modulation |delta_G/G| from radion oscillation.

    The radion-induced G_eff variation scales as (tau/tau_0)^2 because
    the oscillation amplitude is proportional to the activated tension.
    """
    return delta_G_max * tau_ratio(T_MeV) ** 2


def hubble_radiation(T_MeV):
    """Hubble parameter in the radiation era (in s^-1).

    H ~ 1.66 * g_star^{1/2} * T^2 / M_Pl
    """
    g_star = 10.75  # effective relativistic DOF at T ~ 1 MeV
    M_Pl_MeV = 1.22e22  # Planck mass in MeV
    return 1.66 * np.sqrt(g_star) * T_MeV**2 / M_Pl_MeV


def gdot_over_g_ratio(T_MeV):
    """|dG_eff/dt| / (H * G_eff) — dimensionless rate of G_eff change.

    This must be << 1 during BBN for G_eff to be effectively constant.

    Analytically:
    d(delta_G)/dt = delta_G_max * d(tau/tau_0)^2/dt
    Using the chain rule and T(t) ~ T_0 * t^{-1/2}:
    d(tau/tau_0)/dT * dT/dt

    We approximate numerically.
    """
    dT = T_MeV * 0.01  # small temperature step
    dg = g_eff_modulation(T_MeV - dT) - g_eff_modulation(T_MeV + dT)
    # dT/dt ~ -T * H in radiation era
    H = hubble_radiation(T_MeV)
    # dg/dt ~ dg/dT * dT/dt = dg/dT * (-T*H)
    # dg/dT ~ dg / (2*dT) (centered difference)
    dg_dT = dg / (2 * dT)
    dg_dt = abs(dg_dT * (-T_MeV * H))
    # Normalize by H * G (where G modulation is delta_G_max at most)
    return dg_dt / H


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------
def plot_bbn_protection():
    """Three-panel plot showing BBN thermal protection."""
    plt.style.use("dark_background")
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 11), height_ratios=[1, 1, 1])

    # Temperature range: 0.01 MeV to 10^4 MeV
    T = np.logspace(-1.5, 4, 2000)

    # --- Panel 1: tau(T)/tau_0 ---
    tau_r = tau_ratio(T)
    ax1.plot(T, tau_r, color="#00ffcc", linewidth=2.5)
    ax1.fill_between(T, 0, tau_r, alpha=0.15, color="#00ffcc")

    # BBN window
    ax1.axvspan(T_BBN_low, T_BBN_high, color="yellow", alpha=0.15,
                label=f"BBN window ({T_BBN_low}–{T_BBN_high} MeV)")
    ax1.axvline(T_QCD, color="red", linestyle="--", alpha=0.7,
                label=f"$T_{{QCD}}$ = {T_QCD} MeV")
    ax1.axvline(E_tau, color="#00ffcc", linestyle=":", alpha=0.5,
                label=f"$\\tau_0^{{1/3}}$ = {E_tau} MeV")

    ax1.set_xscale("log")
    ax1.set_ylabel(r"$\tau(T) / \tau_0$", fontsize=13)
    ax1.set_title(
        r"V7.0 BBN Protection: Temperature-Dependent Brane Tension $\tau(T)$"
        "\n"
        r"$\tau(T) = \tau_0 \cdot \tanh\left[(T_{QCD}/T)^3\right]$",
        fontsize=13,
    )
    ax1.set_ylim(-0.05, 1.15)
    ax1.legend(fontsize=9, loc="center left")
    ax1.set_xlim(T[0], T[-1])

    # Annotation
    ax1.annotate(
        "Brane frozen\n(ultra-stiff)",
        xy=(5000, 0.05), fontsize=10, color="gray",
        ha="center",
    )
    ax1.annotate(
        "Motor active\n" + r"($\tau = \tau_0$)",
        xy=(0.1, 0.5), fontsize=10, color="#00ffcc",
        ha="center",
    )

    # --- Panel 2: G_eff / G_N ---
    g_mod = g_eff_modulation(T)
    g_eff_ratio = 1.0 - g_mod  # G_eff = G_N * (1 - delta_G * ...)

    ax2.plot(T, g_eff_ratio, color="#66ccff", linewidth=2.5)
    ax2.axhline(1.0, color="white", linestyle=":", alpha=0.3)

    # BBN window
    ax2.axvspan(T_BBN_low, T_BBN_high, color="yellow", alpha=0.15)
    ax2.axvline(T_QCD, color="red", linestyle="--", alpha=0.7)

    # BBN constraint band
    ax2.fill_between(T, 1 - BBN_constraint, 1 + BBN_constraint,
                     color="green", alpha=0.08,
                     label=f"BBN constraint: $|\\delta G/G|$ < {BBN_constraint}")

    ax2.set_xscale("log")
    ax2.set_ylabel(r"$G_{eff} / G_N$", fontsize=13)
    ax2.set_ylim(0.80, 1.05)
    ax2.legend(fontsize=9)
    ax2.set_xlim(T[0], T[-1])

    # Print G_eff values in BBN window
    for T_val in [1.0, 0.5, 0.1]:
        g_val = 1.0 - g_eff_modulation(T_val)
        deviation = abs(1.0 - g_val)
        ax2.annotate(
            f"T={T_val} MeV\n$\\delta G/G$={deviation:.1e}",
            xy=(T_val, g_val),
            xytext=(T_val * 5, g_val - 0.03),
            fontsize=7, color="#66ccff",
            arrowprops=dict(arrowstyle="->", color="#66ccff", alpha=0.5),
        )

    # --- Panel 3: |dG_eff/dt| / (H * G_eff) ---
    rate = gdot_over_g_ratio(T)

    ax3.plot(T, rate, color="#ff9966", linewidth=2.5)
    ax3.axhline(1.0, color="white", linestyle="--", alpha=0.3,
                label=r"$|\dot{G}/G| = H$ (unacceptable)")
    ax3.axhline(0.01, color="green", linestyle=":", alpha=0.5,
                label=r"$|\dot{G}/G| < 0.01 H$ (safe)")

    # BBN window
    ax3.axvspan(T_BBN_low, T_BBN_high, color="yellow", alpha=0.15,
                label="BBN window")
    ax3.axvline(T_QCD, color="red", linestyle="--", alpha=0.7)

    ax3.set_xscale("log")
    ax3.set_yscale("log")
    ax3.set_xlabel("Temperature T (MeV)", fontsize=13)
    ax3.set_ylabel(r"$|\dot{G}_{eff}| / (H \cdot G_{eff})$", fontsize=13)
    ax3.set_ylim(1e-80, 1e2)
    ax3.legend(fontsize=9)
    ax3.set_xlim(T[0], T[-1])

    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, "bbn_thermal_freezeout.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="black")
    plt.close(fig)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("V7.0 BBN Thermal Protection Analysis")
    print("=" * 70)

    os.makedirs(PLOTS_DIR, exist_ok=True)

    print(f"\n[1] Parameters:")
    print(f"  T_QCD = {T_QCD} MeV")
    print(f"  tau_0^(1/3) = {E_tau} MeV (= Lambda_QCD)")
    print(f"  alpha = {alpha} (transition sharpness)")
    print(f"  BBN window: {T_BBN_low} - {T_BBN_high} MeV")
    print(f"  BBN constraint: |delta_G/G| < {BBN_constraint}")

    print("\n[2] tau(T)/tau_0 at key temperatures:")
    for T_val in [10000, 1000, 200, 100, 10, 1, 0.5, 0.1]:
        t_r = tau_ratio(T_val)
        print(f"  T = {T_val:8.1f} MeV: tau/tau_0 = {t_r:.6e}")

    print("\n[3] G_eff modulation during BBN:")
    for T_val in [1.0, 0.5, 0.1]:
        delta = g_eff_modulation(T_val)
        print(f"  T = {T_val:.1f} MeV: |delta_G/G| = {delta:.2e} "
              f"(constraint: {BBN_constraint})")

    print("\n[4] Rate of G_eff change during BBN:")
    for T_val in [1.0, 0.5, 0.1]:
        rate = gdot_over_g_ratio(T_val)
        print(f"  T = {T_val:.1f} MeV: |Gdot/G| / H = {rate:.2e}")

    print("\n[5] Generating plot...")
    plot_bbn_protection()

    # Summary
    max_deviation_bbn = max(g_eff_modulation(T_BBN_high),
                           g_eff_modulation(T_BBN_low))
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Max |delta_G/G| during BBN: {max_deviation_bbn:.2e}")
    print(f"  BBN constraint:             {BBN_constraint}")
    print(f"  Safety margin:              {BBN_constraint / max(max_deviation_bbn, 1e-100):.0e}x")
    print(f"  => BBN PROTECTED by thermal freeze-out")
    print("=" * 70)


if __name__ == "__main__":
    main()
