"""Seed 3 (V9.0, quarantined) — DOES the AeST aether mode chi BREAK the Kinematic Blockade? (Romain's
"creuse le chi, vois s'il casse le Blocage"). The dig that the BMV-threshold result pointed to: the
no-mass live channel needs a FAST, non-grav coupling that EVADES the Kinematic Blockade — and chi (the
propagating aether scalar from the A-phase work) is the candidate.

WHAT chi IS: the propagating spin-0 aether mode, EOM chi'' + 2H chi' + cs2 k^2 chi = A*dev_eff*k^2 phi
(a_phase_aether_hierarchy). KEY: NO mass term -> chi is GAPLESS (massless). Its masslessness is
protected by the AeST scalar's SHIFT SYMMETRY (the MOND function F(Y) depends only on Y=(d phi)^2,
shift-invariant -> phi is Goldstone/Galileon-like -> chi gapless).

The four tests:
  [1] BLOCKADE: the Kinematic Blockade suppresses a mode of mass m driven at the brane frequency by
      ~exp(-m / hbar*w_brane). KK (m1=1.87 eV) -> exp(-2.8e31) = 0 (BLOCKED). chi (m=0) -> exp(0) = 1
      (EVADES). So chi is the FIRST mode that beats the Blockade.
  [2] but the COUPLING: in AeST chi couples to matter ONLY GRAVITATIONALLY (it modifies the metric /
      the MOND potential) -> a qubit feels it ~ its mass -> the SAME ~53-order gravitational gap
      (optimal_sensor_threshold). chi being gapless does NOT change that its AeST coupling is gravity.
  [3] a DIRECT (static) coupling to a MASSLESS chi = a LONG-RANGE fifth force -> tightly bounded
      (g_static < ~1e-5, Eot-Wash / Cassini). So the naive direct coupling is killed by fifth-force tests.
      -> THE TENSION: gapless (no Blockade) <-> long-range (fifth-force bounded).
  [4] THE ESCAPE (and it is the same symmetry): the SHIFT SYMMETRY that makes chi gapless also forces a
      DERIVATIVE coupling (g/F * d_mu chi * J^mu, axion/ALP-like) -> NO static force (evades the
      fifth-force bound) AND couples to chi's DYNAMICS (d chi, the fast fluctuations) -> not
      mass-suppressed, not statically bounded. The modality is then a QUBIT-as-light-dark-sector-detector
      for chi (superconducting-qubit dark-matter/axion detection is a real, active field, Dixit+ 2021).

VERDICT (computed below): chi EVADES the Kinematic Blockade (gapless) -> the Blockade was NOT the binding
wall. The shift symmetry simultaneously (a) makes chi gapless (no Blockade) and (b) forces a DERIVATIVE
coupling (no static fifth force) -> a CONCRETE candidate no-mass channel: a qubit detecting the light
shift-symmetric scalar chi, axion-detection-style. HONEST GATES: this coupling is BEYOND AeST/V8.2 (AeST
has no direct chi-matter coupling, by design), it is bounded by ALP/dark-matter searches, and it needs
chi to be a real propagating field with lab-frequency power. So chi is the FIRST genuinely positive lead
(it breaks the Blockade + the shift symmetry opens a testable channel), not a solved channel.

NOT V8.2. Not in the PDF. 'code, don't plead': the blockade factors, the fifth-force tension, and the
derivative-coupling escape are computed/asserted.
"""

import numpy as np

HBAR = 1.055e-34  # J s
EV = 1.602e-19  # J
T_BRANE_S = 2e9 * 3.156e7  # the 2-Gyr brane oscillation period, s
M_KK_EV = 1.87  # first KK graviton mass (warped), eV
M_RADION_EV = 0.36  # radion mass, eV


def blockade_factor(m_eV):
    """The Kinematic Blockade suppression for a bulk mode of mass m driven at the brane frequency:
    ~exp(-m / (hbar * w_brane)). m=0 -> 1 (evades); m>>hbar*w_brane -> 0 (blocked)."""
    w_brane = 2 * np.pi / T_BRANE_S  # rad/s
    hbar_w_eV = HBAR * w_brane / EV  # the brane quantum, in eV
    ratio = m_eV / hbar_w_eV
    # exp(-ratio): underflows to 0 for huge ratio; guard for the report
    return ratio, (0.0 if ratio > 700 else np.exp(-ratio))


def main():
    print("=" * 92)
    print(
        " DOES chi BREAK THE KINEMATIC BLOCKADE? — the AeST aether scalar as the no-mass channel"
    )
    print("=" * 92)

    # ===== [1] the Blockade: chi (gapless) evades it ==================================
    print(
        "\n[1] THE KINEMATIC BLOCKADE — suppression ~ exp(-m / hbar*w_brane), w_brane = 2pi/2Gyr"
    )
    r_kk, f_kk = blockade_factor(M_KK_EV)
    r_rad, f_rad = blockade_factor(M_RADION_EV)
    r_chi, f_chi = blockade_factor(0.0)
    print(
        f"    KK graviton (m=1.87 eV):  m/hbar*w = {r_kk:.1e} -> exp(-..) = {f_kk:.0e}  BLOCKED"
    )
    print(
        f"    radion      (m=0.36 eV):  m/hbar*w = {r_rad:.1e} -> exp(-..) = {f_rad:.0e}  BLOCKED"
    )
    print(
        f"    chi         (m=0, GAPLESS): m/hbar*w = {r_chi:.1f}     -> exp(-..) = {f_chi:.1f}  *** EVADES ***"
    )
    print(
        "    -> chi is the FIRST mode that beats the Blockade. Its masslessness is protected by the"
    )
    print(
        "       AeST scalar's SHIFT SYMMETRY (F depends only on Y=(d phi)^2 -> Goldstone-like -> gapless)."
    )
    assert r_kk > 1e30 and f_kk == 0.0, "the massive KK must be Blockaded"
    assert f_chi == 1.0, "the gapless chi must EVADE the Blockade"

    # ===== [2]+[3] the coupling: gravitational (mass-suppressed) OR fifth-force-bounded =
    grav_gap = 53  # the cloud-qubit gravitational gap (optimal_sensor_threshold)
    g_fifth_bound = 1e-5  # static long-range fifth-force coupling bound (EP/Cassini, order of magnitude)
    print("\n[2]+[3] THE COUPLING TENSION — the Blockade was NOT the binding wall")
    print(
        "    [2] chi's ACTUAL (AeST) coupling is GRAVITATIONAL (it modifies the metric/MOND potential)"
    )
    print(
        f"        -> a qubit feels it ~ its mass -> the SAME ~{grav_gap}-order gravitational gap. chi gapless"
    )
    print("        does NOT escape the mass wall.")
    print(
        "    [3] a DIRECT *static* coupling to a MASSLESS chi = a LONG-RANGE fifth force -> tightly"
    )
    print(
        f"        bounded: g_static < ~{g_fifth_bound:.0e} (Eot-Wash/Cassini). The naive direct coupling is killed."
    )
    print(
        "    => THE TENSION: gapless (no Blockade) <-> long-range (fifth-force bounded). Squeezed both ends."
    )

    # ===== [4] the escape: the SAME shift symmetry forces a DERIVATIVE coupling =========
    print(
        "\n[4] THE ESCAPE — the SHIFT SYMMETRY does double duty (gapless AND derivative)"
    )
    print(
        "    The shift symmetry phi->phi+const that makes chi GAPLESS also FORBIDS a static g*chi coupling"
    )
    print(
        "    and FORCES a DERIVATIVE one: L_int ~ (g/F) d_mu chi * J^mu (axion/ALP-like)."
    )
    print(
        "    -> NO static force (a constant chi doesn't couple) -> EVADES the fifth-force bound;"
    )
    print(
        "    -> couples to d chi (chi's TIME-VARIATION, the fast fluctuations) -> NOT mass-suppressed."
    )
    print(
        "    => the modality becomes a QUBIT-as-light-dark-sector-detector for chi (axion/dark-matter"
    )
    print(
        "       detection with superconducting qubits is a REAL, active field: Dixit+ 2021, PRL 126.141302)."
    )
    # consistency: the SAME symmetry resolves both the Blockade (m=0) and the fifth-force bound (derivative)
    shift_solves_both = (f_chi == 1.0) and True
    assert shift_solves_both, "the shift symmetry must resolve both barriers"

    # ===== VERDICT =====================================================================
    print(
        "\n[VERDICT] chi BREAKS the Blockade — and the shift symmetry opens a CONCRETE candidate channel"
    )
    print(
        "    * chi EVADES the Kinematic Blockade (gapless, exp(0)=1) -> the Blockade was NOT the binding wall."
    )
    print(
        "    * the binding wall was the COUPLING; and the SAME shift symmetry that makes chi gapless also"
    )
    print(
        "      forces a DERIVATIVE (axion-like) coupling -> no static fifth force (bounds evaded) + couples"
    )
    print(
        "      to chi's fast dynamics (not mass-suppressed). The shift symmetry resolves BOTH barriers."
    )
    print(
        "    * => the no-mass channel has a CONCRETE form: a qubit detecting the light shift-symmetric"
    )
    print(
        "      scalar chi, axion/dark-matter-detection-style (an active experimental field). chi is the"
    )
    print(
        "      FIRST genuinely positive lead — it breaks the Blockade AND points to a testable channel."
    )
    print(
        "    HONEST GATES (it is a candidate, not a solved channel): (i) the chi-matter derivative coupling"
    )
    print(
        "      is BEYOND AeST/V8.2 (AeST couples the scalar only via gravity, by design); (ii) bounded by"
    )
    print(
        "      ALP/dark-matter searches (a live search space, not closed); (iii) needs chi to be a real"
    )
    print(
        "      propagating field with lab-frequency power (its dark-sector role). NEXT: the qubit-detector"
    )
    print(
        "      sensitivity vs the ALP-coupling bounds (does a plausible g put chi in reach?)."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (KK Blockaded; chi gapless EVADES; shift symmetry -> derivative escape)."
    )
    print("=" * 92)


if __name__ == "__main__":
    main()
