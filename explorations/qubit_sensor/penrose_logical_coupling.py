"""Seed 3 (V9.0, quarantined) — THE REAL QUESTION: is OBT's 5D coupling logical-level AND strong
enough to detect ONLINE (no mesoscopic mass)?  A quantitative estimate, not a refrain.

Romain's standing challenge: a detection system aims to NOT need a lab -> can the 5D channel couple
to the LOGICAL observable on an accessible (cloud) qubit? Two honest sub-questions, computed here:

  (1) IS the coupling logical-level?  YES. OBT's detectable 5D signature (the 5D-enhanced Penrose-
      Diósi collapse) is a DECOHERENCE of the encoded superposition -- it dephases the LOGICAL qubit;
      it does NOT require reading a literal moving mass. Romain's instinct on the NATURE is right.

  (2) IS it strong enough online?  This is gravitational: its STRENGTH is E_G = G*(dm)^2 / scale
      (x the 5D enhancement eta below L=0.2um), dm = the mass-energy difference between |0> and |1>.
      We compute the logical-dephasing rate Gamma = E_G/hbar for a transmon, a trapped-ion motional
      superposition, and a mesoscopic nanosphere, and compare to the best sensing-stack floor
      (asymmetric order-1 coupling + protected-GHZ + long integration => ~1e-4 /s).

VERDICT (below): the coupling is logical-level (1), but its gravitational strength (2) is tens of
orders too small for cloud qubits (tiny dm) -> ONLINE is DEAF for OBT's *gravitational* 5D; the
nanosphere sits ~at the sensing floor (the frontier). The sensing stack MINIMISES the mass needed
(it SETS the floor) but cannot lift a cloud qubit's Gamma by ~14-50 orders. The only online escape
would be a NON-gravitational, DYNAMICAL 5D coupling (strength set by a coupling constant, not by dm)
-- which OBT V8.2 does NOT have (gravity is the sole bulk force; SM forces are brane-confined). That
escape is genuinely open, but it is NEW PHYSICS beyond V8.2, not OBT's stated prediction.

NOT V8.2. Not in the PDF. 'code, don't plead': order-of-magnitude estimates, cross-checked against
Penrose's canonical ~1e3-1e4 s for a ~100 nm grain (and scripts/penrose_diosi_5d.py).
"""

import numpy as np

G = 6.674e-11  # N m^2 / kg^2
HBAR = 1.0546e-34  # J s
C = 2.998e8  # m/s
AMU = 1.6605e-27  # kg
L = 0.2e-6  # the extra dimension (m)

# Best-case sensing-stack floor: smallest logical-dephasing rate detectable with the asymmetric
# order-1 code + protected GHZ + long integration ~ 1 / (T_coh * sqrt(N_qubits * repetitions)).
GAMMA_FLOOR = 1.0 / (1.0 * np.sqrt(1e8))  # ~1e-4 /s (T_coh~1 s, N*reps~1e8)


def eta_5d(scale):
    """5D enhancement of E_G below L (from scripts/penrose_diosi_5d.py: ~2-3 at L, growing below)."""
    return float(np.clip(L / scale, 1.0, 10.0)) if scale < L else 1.0


def gamma_logical(dm, sep, size):
    """Gravitational logical-dephasing rate Gamma = E_G/hbar; E_G ~ G*dm^2/scale * eta, scale=max(sep,size)."""
    scale = max(sep, size)
    e_g = G * dm**2 / scale * eta_5d(scale)
    return e_g / HBAR  # 1/s


SYSTEMS = {
    # name: (dm [kg], separation [m], size [m], note)
    "transmon (cloud)": (
        HBAR
        * 2
        * np.pi
        * 5e9
        / C**2,  # dm = hbar*omega/c^2 (only an ENERGY difference)
        0.0,  # internal states: no spatial separation
        1e-3,  # delocalised over the ~mm circuit
        "internal states: dm is only the microwave energy/c^2 -> minuscule",
    ),
    "trapped-ion motional (cloud-ish)": (
        171 * AMU,  # one Yb ion
        0.1e-6,  # motional superposition ~0.1 um
        1e-10,  # ion wavepacket ~0.1 nm
        "one atom: a real spatial superposition but a tiny mass",
    ),
    "nanosphere (BMV frontier)": (
        1e9 * AMU,  # ~10^9 amu
        100e-9,  # ~100 nm superposition
        100e-9,  # ~100 nm sphere (sub-L -> 5D on)
        "mesoscopic mass + sub-0.2um: the only one with appreciable E_G",
    ),
}


def main():
    print("=" * 86)
    print(
        " THE REAL QUESTION: is OBT's 5D coupling logical-level AND online-detectable?"
    )
    print("=" * 86)

    print("\n[1] IS THE COUPLING LOGICAL-LEVEL?  YES.")
    print(
        "    OBT's detectable 5D signature is the 5D-enhanced Penrose-Diósi COLLAPSE -- a DECOHERENCE"
    )
    print(
        "    of the encoded superposition. It dephases the LOGICAL qubit; no literal moving-mass"
    )
    print(
        "    readout is needed. (Romain's instinct on the NATURE of the coupling is right.)"
    )

    print(
        "\n[2] IS IT STRONG ENOUGH ONLINE?  Gamma = E_G/hbar,  E_G ~ G*dm^2/scale * eta(5D)"
    )
    print(
        f"    best sensing-stack floor (order-1 code + protected GHZ + integration): {GAMMA_FLOOR:.0e} /s"
    )
    print(
        f"    {'system':<34}{'dm [kg]':>9}{'Gamma [1/s]':>13}{'tau [s]':>10}{'orders below floor':>20}"
    )
    gammas = {}
    for name, (dm, sep, size, note) in SYSTEMS.items():
        g = gamma_logical(dm, sep, size)
        gammas[name] = g
        below = np.log10(GAMMA_FLOOR / g)
        tag = "AT THE FRONTIER" if below < 2 else f"DEAF (~1e{below:.0f} below)"
        print(f"    {name:<34}{dm:>9.1e}{g:>13.1e}{1/g:>10.1e}{tag:>20}")
        print(f"        ({note})")

    tau_nano = 1 / gammas["nanosphere (BMV frontier)"]
    print(
        f"\n    cross-check: nanosphere tau = {tau_nano:.1e} s ~ Penrose's canonical 1e3-1e4 s"
    )
    assert 1e2 < tau_nano < 1e6, "nanosphere collapse time must be ~1e3-1e4 s (Penrose)"
    assert (
        np.log10(GAMMA_FLOOR / gammas["nanosphere (BMV frontier)"]) < 2
    ), "nanosphere ~ at the floor"
    assert (
        np.log10(GAMMA_FLOOR / gammas["trapped-ion motional (cloud-ish)"]) > 6
    ), "ion must be deaf"
    assert (
        np.log10(GAMMA_FLOOR / gammas["transmon (cloud)"]) > 30
    ), "transmon must be utterly deaf"
    print(
        "    -> the nanosphere sits ~at the sensing floor (the frontier); a trapped ion is ~14"
    )
    print(
        "       orders below; a transmon ~50. The sensing stack buys a few orders (N, sqrt(reps)),"
    )
    print("       NOT 14-50. MASS is what brings Gamma UP to the floor (E_G ~ dm^2).")

    print(
        "\n[3] THE ENERGY-SHIFT ROUTE (the best NON-mass candidate) — why it carries no signal"
    )
    alpha, omega, t_coh = 1e-6, 2 * np.pi * 5e9, 1e-4
    print(
        f"    a 5D radion shift of the qubit gap: dE/E ~ alpha ~ {alpha:.0e} (NOT mass-suppressed!)"
    )
    print(
        f"    -> phase over coherence ~ alpha*omega*T_coh = {alpha*omega*t_coh:.2f} rad: looks HUGE..."
    )
    print(
        "    BUT a CONSTANT gap shift is absorbed into the qubit's calibrated frequency -> NOT a"
    )
    print(
        "    signal. It would count only if DYNAMICAL (modulated) or position-dependent; OBT's radion"
    )
    print(
        "    is DC over a lab run (2 Gyr) and the static Yukawa is calibrated out. No free signal."
    )

    print("\n[4] VERDICT — the honest answer to 'the real question'")
    print(
        "    * The coupling IS logical-level (it dephases the encoded qubit): Romain right on NATURE."
    )
    print(
        "    * But OBT's DETECTABLE 5D (the gravitational Penrose-Diósi collapse) has gravitational"
    )
    print(
        "      STRENGTH (E_G ~ G*dm^2): cloud qubits (tiny dm) are ~14-50 orders below the best"
    )
    print(
        "      sensing floor -> ONLINE is DEAF for OBT's stated 5D. The nanosphere is the frontier."
    )
    print(
        "    * The sensing stack (asymmetric order-1 + protected GHZ + integration) MINIMISES the"
    )
    print(
        "      mass needed (it SETS the floor) but cannot lift Gamma by 14-50 orders."
    )
    print(
        "    * The ONLY online escape = a NON-gravitational, DYNAMICAL 5D coupling (strength set by a"
    )
    print(
        "      coupling constant, not by dm). OBT V8.2 has none -> that is NEW PHYSICS beyond V8.2,"
    )
    print(
        "      genuinely open but not OBT's prediction. For OBT as it stands, the mass IS needed."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (nanosphere ~Penrose 1e4 s, at floor; ion ~14 below; transmon ~50)."
    )
    print("=" * 86)


if __name__ == "__main__":
    main()
