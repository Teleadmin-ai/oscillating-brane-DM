"""DISSECT THE 1.5x (option 2, June 2026) -- is a0(z) rising ~1.5x faster than cH(z)/2pi a SYSTEMATIC or REAL?

REVIEWER MODE, both ways. The 3 datasets (MUSE-DARK RAR, KROSS RAR, Uebler BTFR) agree a0 ~doubles by z~1 and
~1.5x faster than the OBT horizon rate a0 = cH(z)/2pi (alpha=1). Within OBT (a0 horizon-fixed) the excess is
ascribed to high-z systematics. We BUILD the budget and ask: does it cover Delta(alpha), or is a real alpha>1
forced (which would REFUTE the cH(z)/2pi RATE -- the evolution survives, but not its Gibbons-Hawking value)?

THREE contributions to the apparent alpha, kept separate and honest:
  (A) LOCAL ANCHOR: alpha = [ln a0(z) - ln a0(0)] / ln E(z) depends on a0(0). OBT predicts a0(0)=cH0/2pi
      (1.04e-10 at H0=67.4 .. 1.13 at H0=73); canonical MOND a0 = 1.2+-0.1. So OBT's local a0 is ~7-15% LOW
      -> a mild ~1sigma tension AT z=0, AND a ~0.3 shift in alpha_obs depending on which anchor is used.
  (B) HIGH-Z COHERENT SYSTEMATICS (the levers; deep-MOND a0=V_c^4/(G M_bar)): V_c over-estimate -> +4f,
      M_bar under-count -> +f, lensing g_obs over -> +2f. A z-growing bias biases the slope by beta_sys.
  (C) The REAL alpha (what OBT predicts = 1; what 'a0 faster than H' would need > 1).
The data cannot yet separate (C) from (A)+(B). We quantify (A) and (B) to show Delta(alpha)_obs sits inside them.
"""

import numpy as np

Om, OL = 0.315, 0.685
C_M_S = 2.998e8
MPC_KM = 3.086e19


def E(z):
    return np.sqrt(Om * (1 + z) ** 3 + OL)


def cH0_over_2pi(H0_kms_mpc):
    """OBT local acceleration a0(0) = cH0/2pi, in 1e-10 m/s^2."""
    H0 = H0_kms_mpc / MPC_KM  # 1/s
    return C_M_S * H0 / (2 * np.pi) / 1e-10


def alpha_ratio(z, a0_z, a0_local):
    return np.log(a0_z / a0_local) / np.log(E(z))


def alpha_btfr(z, dlogMbar_dex):
    """BTFR offset Delta(log M_bar) at fixed V (dex) -> alpha (anchor-independent: it is differential)."""
    return -dlogMbar_dex / np.log10(E(z))


def f_gas_tacconi(z):
    """Cold-gas fraction f_gas=M_gas/M_bar at M*~10^10.5 (Tacconi+2018/Genzel+2015): mu~0.1(1+z)^2.5."""
    mu = 0.1 * (1 + z) ** 2.5
    return mu / (1 + mu)


def beta_linear(b_at_zmax, zmin=0.3, zmax=1.5, nb=10):
    """beta_sys for a coherent a0-impact b(z) growing linearly 0 -> b_at_zmax over [0, zmax]."""
    z = np.linspace(zmin, zmax, nb)
    x = np.log(E(z))
    xc = x - x.mean()
    return np.sum(xc * (b_at_zmax * z / zmax)) / np.sum(xc * xc)


def main():
    print("=" * 98)
    print(
        "DISSECTING THE 1.5x: is a0(z) faster than cH(z)/2pi a SYSTEMATIC, or a REAL alpha>1?"
    )
    print("=" * 98)

    a_OBT = cH0_over_2pi(67.4)
    a_OBT_hi = cH0_over_2pi(73.0)
    print(f"\n[1a] LOCAL ANCHOR (contribution A -- a known, often-skipped subtlety):")
    print(
        f"  OBT a0(0)=cH0/2pi = {a_OBT:.2f}e-10 (H0=67.4) .. {a_OBT_hi:.2f}e-10 (H0=73);  MOND a0 = 1.20+-0.10."
    )
    print(
        f"  -> OBT's local a0 is ~{(1-a_OBT/1.20)*100:.0f}-{(1-a_OBT_hi/1.20)*100:.0f}% BELOW MOND's value: a mild"
        " ~1sigma OBT tension AT z=0 itself (independent of any high-z effect). Carry it honestly."
    )

    print(
        "\n[1b] OBSERVED alpha (a0 ~ E^alpha) -- anchor-dependent for RAR, differential for BTFR:"
    )
    rows = [
        ("MUSE-DARK RAR z=1.2, a0=2.71 (own z0=1.0)", alpha_ratio(1.2, 2.71, 1.0)),
        ("KROSS RAR z=0.86, a0=1.97 | anchor cH0/2pi", alpha_ratio(0.86, 1.97, a_OBT)),
        ("KROSS RAR z=0.86, a0=1.97 | anchor MOND 1.2", alpha_ratio(0.86, 1.97, 1.20)),
        ("Uebler BTFR z=0.9, Delta=-0.44 dex (differential)", alpha_btfr(0.9, -0.44)),
    ]
    a_obs = [a for _, a in rows]
    for label, a in rows:
        print(f"  {label:50s} -> alpha_obs = {a:4.2f}  (Delta_alpha {a-1:+4.2f})")
    print(
        f"  => alpha_obs SCATTERS over [{min(a_obs):.2f}, {max(a_obs):.2f}] -- a spread of {max(a_obs)-min(a_obs):.1f} >> any"
    )
    print(
        "     statistical error -> the measurement is SYSTEMATIC/anchor-dominated, and OBT's alpha=1 sits at the"
        " LOW end (KROSS@MOND-anchor = 0.99). The '1.5x' is the rough centre of a systematics-broadened scatter."
    )

    print("\n[2] GAS-CENSUS budget (M_bar lever 1x). f_gas(z) Tacconi:")
    print(
        "    "
        + "  ".join(f"f_gas({z})={f_gas_tacconi(z):.2f}" for z in (0.0, 0.5, 0.9, 1.5))
    )
    for lab, fa in [
        ("M* only (no gas)", 0.0),
        ("fixed gas f=0.375 (KROSS Mbar/M*=1.6)", 0.375),
        ("Tacconi evolving gas (correct)", None),
    ]:
        b15 = 0.0 if fa is None else np.log((1 - fa) / (1 - f_gas_tacconi(1.5)))
        print(
            f"  {lab:40s} dln a0(z=1.5)={b15:+.2f} -> beta_gas={beta_linear(b15):+.2f}"
        )

    print("\n[3] VELOCITY budget (V_c lever 4x -- the big one, sign uncertain):")
    sig, vrot = 40.0, 180.0
    f_ad = np.sqrt(1 + 4 * (sig / vrot) ** 2) - 1
    print(
        f"  asymmetric-drift at z~1 (sigma={sig:.0f}, V={vrot:.0f}): {f_ad*100:.0f}% V swing -> dln a0 = +-{4*f_ad:.2f}"
        f" (4x) -> beta_V = +-{abs(beta_linear(4*f_ad)):.2f};  inclination +-5% V -> beta +-{abs(beta_linear(4*0.05)):.2f}"
    )

    print("\n[4] NET coherent beta_sys vs observed Delta_alpha:")
    gas_hi = beta_linear(np.log(1 / (1 - f_gas_tacconi(1.5))))  # M*-only
    v_swing = abs(beta_linear(4 * f_ad)) + abs(beta_linear(4 * 0.05))
    print(
        f"  gas [0, +{gas_hi:.2f}] (0 if correct, +{gas_hi:.2f} if M*-only) ;  V+incl +-{v_swing:.2f}"
        f"  =>  beta_sys in [{-v_swing:+.2f}, {gas_hi+v_swing:+.2f}]"
    )
    print(
        f"  PLUS the local-anchor shift ~+-0.3 (contribution A).  Observed Delta_alpha [{min(a_obs)-1:+.2f},"
        f" {max(a_obs)-1:+.2f}] is FULLY inside (A)+(B)."
    )

    print("\nVERDICT (option 2) -- both ways, honest:")
    print(
        "  * The 1.5x is NOT a refutation of OBT's cH(z)/2pi: Delta_alpha_obs (~+0.4..+0.9, scattered down to ~0)"
    )
    print(
        "    sits fully inside the local-anchor shift (~0.3) PLUS the high-z coherent-systematic budget (gas up to"
    )
    print(
        "    +0.8 if M*-only, V/incl +-0.65). The huge inter-survey scatter (alpha_obs 1.0->1.9) is itself the"
    )
    print(
        "    tell-tale of systematic domination, and OBT's alpha=1 sits at the LOW edge (KROSS@MOND-anchor=0.99)."
    )
    print(
        "  * NOT confirmed-systematic either: the budget is wide enough that a REAL alpha~1.5 also fits. The rate"
    )
    print(
        "    is UNDETERMINED. If a clean survey (gas MEASURED, AD/beam/incl <5%, anchored to cH0/2pi) STILL shows"
    )
    print(
        "    1.5x, OBT's Gibbons-Hawking RATE is refuted (evolution survives; a0~E^1.5 would need a new origin)."
    )
    print(
        "  * NEW honest caveat surfaced: the LOCAL a0=cH0/2pi (1.04) is ~15% below MOND's 1.2 -- a mild ~1sigma"
    )
    print(
        "    z=0 tension on OBT's ABSOLUTE a0 (the H0 value matters: H0=73 -> 1.13, closer). Separate from the rate."
    )
    print(
        "  * CLEAN DISCRIMINATOR -> script C: lensing RAR (g_obs lever 2x, NO V lever) vs kinematic RAR (V lever"
    )
    print(
        "    4x) + measured-gas. If both still 1.5x, the V-systematic is exonerated (-> gas or real); the over-"
    )
    print(
        "    determination across a0/BTFR/Sigma_dagger (different M_bar powers) is the internal falsifier."
    )


if __name__ == "__main__":
    main()
