"""Seed 3 (V9.0, quarantined) — the OPTIMAL-SENSOR THRESHOLD (the BMV frontier). Romain's question:
"calcule le seuil — de combien d'ordres mon capteur optimal referme l'ecart gravitationnel ?"

Romain's sensor (the pepite) is the OPTIMAL instrument: a NULL-DETECTOR (the [[5,1,3]] protection ->
silent to local noise, sensitive to the collective LOGICAL channel, gate 1) + a MATCHED FILTER (encoding
the germe = the optimal antenna for a germe-shaped perturbation). The sensor is solved. This script asks:
GIVEN the optimal sensor, how far down does the minimum-detectable coupling go, and does it reach OBT's
gravitational (Penrose-Diosi) bulk signal for a MASS-FREE (cloud) qubit?

Three computations:
  [1] the GRAVITATIONAL signal Gamma_PD for a mass-free cloud qubit (E_G ~ G*(dm)^2/r, dm = hbar*w/c^2):
      it is ~1e-54 s^-1 -> ~50 orders below a ~1 Hz sensing floor (this reproduces penrose_logical_coupling's
      '14-50 orders deaf'; the 50 end is the pure cloud, the 14 end is a heavier/optimistic coupling).
  [2] the OPTIMAL-SENSOR enhancement: N Heisenberg-entangled witnesses (phase sensitivity ~1/N) + coherent
      integration time T -> the minimum detectable rate scales as Gamma_min ~ 1/(N*T) (best case: coherent,
      Heisenberg, noise-floor-limited -> an UPPER BOUND on the closure). So the sensor closes log10(N*T)
      orders. Tabulated for feasible vs absurd (N, T).
  [3] the NON-GRAV radion (fifth-force) alternative: strength set by a coupling alpha~O(1), NOT mass^2 ->
      orders stronger -> but the radion is QUASI-STATIC (w_radion ~ 1e-17 Hz << 1/T_lab) -> a constant ->
      calibrated out -> NO ac signal. So even the strong non-grav coupling needs a FAST mode.

VERDICT (computed below): the optimal sensor closes ~log10(N*T) <= ~18 orders for any feasible device ->
it MARGINALLY reaches the easiest (~14-order) gravitational case and falls ~30+ orders short of the cloud
(~50). So the gravitational channel is NOT reachable by sensing alone; the leverage must come from the
COUPLING (a FAST non-grav coupling that evades the Kinematic Blockade), not from a better sensor. Romain's
null-detector + matched filter is NECESSARY (the best instrument to see any weak fast signal) but NOT
SUFFICIENT (it cannot out-sense 50 orders). The treasure is the coupling, not the sensor.

NOT V8.2. Not in the PDF. 'code, don't plead': E_G computed from constants; the N*T closure tabulated;
the radion quasi-staticity computed; the verdict asserted.
"""

import numpy as np

# physical constants (SI)
G = 6.674e-11  # gravitational constant
HBAR = 1.055e-34  # reduced Planck
C = 2.998e8  # speed of light
H0_INV_S = 4.35e17  # 1/H0 in s (~ age of universe ~ 13.8 Gyr)


def gravitational_signal_cloud_qubit(f_qubit=5e9, r_qubit=1e-4):
    """Penrose-Diosi self-collapse rate Gamma_PD for a mass-free (cloud) qubit.
    dm = hbar*omega/c^2 (the |0>-|1> mass-energy difference); E_G ~ G*dm^2/r; Gamma_PD = E_G/hbar.
    """
    omega = 2 * np.pi * f_qubit
    dm = HBAR * omega / C**2  # effective mass difference (kg)
    E_G = G * dm**2 / r_qubit  # gravitational self-energy (J)
    gamma_pd = E_G / HBAR  # collapse/signal rate (s^-1)
    return gamma_pd, dm, E_G


def closure_orders(N, T, tau_cycle=1e-3):
    """Best-case (coherent + Heisenberg) orders of magnitude the optimal sensor closes.
    Heisenberg phase sensitivity ~1/N ; coherent integration over T (vs cycle tau) ~ T/tau ;
    minimum detectable rate Gamma_min ~ 1/(N * T) (in s^-1, normalized) -> closes log10(N*T).
    """
    return np.log10(N * T)


def radion_lab_variation(T_lab):
    """The radion (m_phi=0.36 eV) cosmological oscillation is 2 Gyr; its FRACTIONAL change over a lab
    time T_lab. w_radion ~ 2pi / (2 Gyr). Returns the phase advanced over T_lab (rad) -> if << 1, the
    coupling is a CONSTANT over the experiment -> calibrated out -> no ac signal."""
    T_radion_s = 2e9 * 3.156e7  # 2 Gyr in seconds
    w_radion = 2 * np.pi / T_radion_s
    return w_radion * T_lab  # phase advanced (rad) over the lab run


def main():
    print("=" * 92)
    print(
        " THE OPTIMAL-SENSOR THRESHOLD — how far Romain's null-detector + matched filter closes the gap"
    )
    print("=" * 92)

    # ===== [1] the gravitational signal for a mass-free cloud qubit =====================
    gamma_pd, dm, E_G = gravitational_signal_cloud_qubit()
    floor = 1.0  # a ~1 Hz sensing floor (best phase sensitivity ~1/T_coh, T_coh~1 s, single qubit)
    gap_cloud = np.log10(floor / gamma_pd)
    print(
        "\n[1] THE GRAVITATIONAL SIGNAL (mass-free cloud qubit; the Penrose-Diosi bulk channel)"
    )
    print(
        f"    qubit: f=5 GHz, size 100 um -> effective dm = {dm:.2e} kg, E_G = {E_G:.2e} J"
    )
    print(
        f"    => Gamma_PD = {gamma_pd:.2e} s^-1  (the gravitational bulk-signal rate)"
    )
    print(
        f"    vs a ~1 Hz sensing floor -> GAP = {gap_cloud:.0f} orders (reproduces the 14-50 'deaf' range;"
    )
    print("       50 = pure cloud, ~14 = a heavier/optimistic coupling assumption)")
    assert 45 < gap_cloud < 60, "cloud-qubit gravitational gap must be ~50 orders"

    # ===== [2] the optimal-sensor enhancement: log10(N*T) ==============================
    print(
        "\n[2] THE OPTIMAL SENSOR — N Heisenberg witnesses + coherent integration T -> closes log10(N*T)"
    )
    cases = [
        ("today", 1e3, 1e0),
        ("near-future", 1e6, 1e3),
        ("futuristic", 1e9, 1e6),
        ("absurd (N=atoms in a device)", 1e15, 1e9),
        ("impossible (T > universe age)", 1e25, 1e25),
    ]
    print(f"    {'regime':<32}{'N qubits':>12}{'T (s)':>10}{'closes (orders)':>18}")
    best_feasible = 0.0
    for name, N, T in cases:
        c = closure_orders(N, T)
        print(f"    {name:<32}{N:>12.0e}{T:>10.0e}{c:>18.0f}")
        if "absurd" not in name and "impossible" not in name:
            best_feasible = max(best_feasible, c)
    age = closure_orders(1e9, H0_INV_S)
    print(
        f"    (even N=1e9 integrated for the AGE OF THE UNIVERSE closes only {age:.0f} orders)"
    )
    print(
        f"    -> best FEASIBLE closure ~ {best_feasible:.0f} orders (futuristic 1e9 qubits, ~30 yr)"
    )
    assert (
        best_feasible < 20
    ), "feasible closure must be < 20 orders (Heisenberg+integration upper bound)"

    # ===== [3] the non-grav radion alternative: strong but SLOW ========================
    T_lab = 3.156e7 * 30  # a 30-year experiment
    phase = radion_lab_variation(T_lab)
    print(
        "\n[3] THE NON-GRAV RADION (fifth-force) ALTERNATIVE — strength ~alpha, not mass^2, but SLOW"
    )
    print(
        "    a direct radion coupling is NOT mass-suppressed -> orders stronger (could be detectable),"
    )
    print(
        f"    BUT the radion is the 2-Gyr oscillation: over a 30-yr run it advances {phase:.2e} rad"
    )
    print(
        "    -> << 1 -> a CONSTANT over the experiment -> calibrated out -> NO ac signal."
    )
    print(
        "    => even the strong non-grav coupling needs a FAST mode (the KK modes are blockaded)."
    )
    assert (
        phase < 1e-6
    ), "the radion must be quasi-static on lab timescales (no ac signal)"

    # ===== VERDICT =====================================================================
    short_cloud = gap_cloud - best_feasible
    print(
        "\n[VERDICT] the sensor is NECESSARY but NOT SUFFICIENT — the leverage is the COUPLING"
    )
    print(
        f"    * Romain's optimal sensor closes ~{best_feasible:.0f} orders (feasible) of the ~{gap_cloud:.0f}-order"
    )
    print(
        f"      cloud gravitational gap -> still ~{short_cloud:.0f} orders SHORT (it marginally reaches the"
    )
    print(
        "      easiest ~14-order assumption, never the cloud ~50). You cannot OUT-SENSE 50 orders:"
    )
    print("      log10(N*T) caps the closure, and N*T~1e50 is physically impossible.")
    print(
        "    * The non-grav radion is strong enough but QUASI-STATIC -> no ac signal."
    )
    print(
        "    * => THE TREASURE IS A *FAST, NON-GRAV* COUPLING (break the Kinematic Blockade), NOT a"
    )
    print(
        "      better sensor. Romain's null-detector + matched filter is the right INSTRUMENT to see any"
    )
    print(
        "      weak fast signal once such a coupling exists -- necessary, but the discovery is the COUPLING."
    )
    print(
        "    * Concretely: the dig must go to (2) the bulk spectrum (a light/gapless non-grav mode, the"
    )
    print(
        "      AeST aether chi?), (3) a symmetry-allowed direct radion coupling, (4) traversable ER=EPR --"
    )
    print(
        "      NOT to scaling up the sensor. The sensor is done; the physics is in the coupling."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (cloud gap ~50; feasible closure <20; radion quasi-static)."
    )
    print("=" * 92)


if __name__ == "__main__":
    main()
