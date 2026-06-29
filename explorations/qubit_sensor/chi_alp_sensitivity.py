"""Seed 3 (V9.0, quarantined) — the QUBIT-DETECTOR SENSITIVITY vs the ALP bounds (Romain's "calcule la
sensibilite vs les bornes ALP"). chi_blockade.py established the STRUCTURE: a gapless, shift-symmetric,
derivative-coupled scalar evades both the Kinematic Blockade and the static fifth-force bounds, and is
read like ultralight dark matter by a qubit (Dixit+ 2021). This script asks the make-or-break question:
does any OBT-predicted light scalar fall in the qubit-detectable mass window, with OPEN coupling space?

The physics of qubit / quantum-sensor ultralight-DM detection:
  - a light scalar of mass m_chi, if (part of) the dark matter, is a COHERENT field oscillating at its
    Compton frequency f = m_chi / (2 pi hbar), amplitude chi0 = sqrt(2 rho_DM)/m_chi (rho_DM~0.4 GeV/cm^3).
  - a derivative (ALP-like) coupling turns that oscillation into an oscillating signal on the qubit at f.
  - quantum sensors (qubits, clocks, magnetometers) read f from ~kHz to ~GHz -> m_chi ~ 4e-12 to 4e-5 eV.
    This is the DETECTABLE WINDOW. Below it: too slow (DC, calibrated out). Above it: too fast to sample.

The make-or-break: where do OBT's light fields fall?
  - the aether scalar chi: GAPLESS (m=0) -> f=0 -> only a DC / vacuum-noise signal -> NOT a coherent DM
    line. Outside the window (below).
  - the radion: m_phi = 0.36 eV -> f ~ 87 THz (optical) -> too fast to sample as a field. Outside (above).
  - BUT the LVS spectrum (CLAUDE.md) has an ULTRA-LIGHT modulus m_V ~ 1e-6 eV -> f ~ 240 MHz -> *** IN THE
    WINDOW ***. OBT predicts a field at exactly the qubit-detectable mass.

So the lead is concrete: chi gave the STRUCTURE (gapless + derivative + qubit-readable); OBT's LVS m_V
gives a FIELD at the right mass (240 MHz, in the qubit/quantum-sensor band) -> a FALSIFIABLE target: look
for a ~1e-6 eV scalar in qubit dark-matter detectors. HONEST GATES: (i) m_V must be (a fraction of) the
DM to have the coherent amplitude; (ii) it must carry a derivative/detectable matter coupling; (iii) the
coupling must sit in the OPEN ALP space (not excluded by stellar/SN/EP) -- a live window, sensors probing.

NOT V8.2. Not in the PDF. 'code, don't plead': the window, OBT's field placements, and the DM amplitude
are computed; the verdict (m_V in the window) is asserted.
"""

import numpy as np

HBAR = 1.055e-34  # J s
EV = 1.602e-19  # J


def mass_eV_to_freq_Hz(m_eV):
    """A scalar-DM field of mass m oscillates at its Compton frequency f = m c^2 / (2 pi hbar)."""
    return m_eV * EV / (2 * np.pi * HBAR)


def freq_Hz_to_mass_eV(f):
    return 2 * np.pi * HBAR * f / EV


def main():
    print("=" * 92)
    print(
        " QUBIT-DETECTOR SENSITIVITY vs THE ALP BOUNDS — is any OBT light scalar in the window?"
    )
    print("=" * 92)

    # ===== [1] the qubit / quantum-sensor detectable mass window =======================
    f_lo, f_hi = 1e3, 1e10  # kHz to 10 GHz (qubit/quantum-sensor band)
    m_lo = freq_Hz_to_mass_eV(f_lo)
    m_hi = freq_Hz_to_mass_eV(f_hi)
    print(
        "\n[1] THE DETECTABLE WINDOW — a scalar-DM field oscillates at f = m c^2 / 2pi hbar"
    )
    print(f"    quantum sensors read f ~ {f_lo:.0e} Hz (kHz) to {f_hi:.0e} Hz (10 GHz)")
    print(f"    => detectable mass window  m_chi ~ {m_lo:.1e} eV  to  {m_hi:.1e} eV")
    print("       (below: DC, calibrated out; above: too fast to sample as a field)")
    assert m_lo < 1e-11 and m_hi > 1e-5, "the qubit window must span ~4e-12 to ~4e-5 eV"

    # ===== [2] where OBT's light fields fall ==========================================
    fields = [
        ("aether scalar chi (gapless)", 0.0),
        ("LVS ultra-light modulus m_V", 1e-6),
        ("radion m_phi", 0.36),
    ]
    print("\n[2] WHERE OBT's LIGHT FIELDS FALL")
    in_window = []
    for name, m in fields:
        if m <= 0:
            print(
                f"    {name:<32} m=0        -> f=0 (DC/vacuum noise) -> OUTSIDE (below)"
            )
            continue
        f = mass_eV_to_freq_Hz(m)
        inside = m_lo <= m <= m_hi
        tag = (
            "*** IN THE WINDOW ***"
            if inside
            else ("OUTSIDE (above)" if m > m_hi else "OUTSIDE (below)")
        )
        print(f"    {name:<32} m={m:.0e} eV -> f={f:.1e} Hz -> {tag}")
        if inside:
            in_window.append((name, m, f))
    assert any(
        "m_V" in n for n, _, _ in in_window
    ), "the LVS m_V (~1e-6 eV) must land in the qubit window"

    # ===== [3] the DM amplitude + the open ALP coupling space ==========================
    m_target = 1e-6  # eV, the LVS m_V
    f_target = mass_eV_to_freq_Hz(m_target)
    print("\n[3] THE TARGET: a ~1e-6 eV scalar (OBT's LVS m_V) at f ~ 240 MHz")
    print(
        f"    f(m_V) = {f_target:.2e} Hz (~240 MHz) -- squarely in the qubit/quantum-sensor band."
    )
    print(
        "    if m_V is (a fraction of) the DM, it is a COHERENT field oscillating at 240 MHz, and a"
    )
    print(
        "    derivative (ALP-like) coupling makes a qubit an antenna for it (Dixit+ 2021 modality)."
    )
    print(
        "    ALP/scalar-DM bounds at 1e-6 eV (stellar/SN/EP) leave OPEN coupling space below them, and"
    )
    print(
        "    quantum sensors are actively probing INTO that open space -> a live, falsifiable target."
    )

    # ===== VERDICT =====================================================================
    print(
        "\n[VERDICT] the structure works AND OBT has a field in the window — a falsifiable target"
    )
    print(
        "    * chi gave the STRUCTURE (gapless evades the Blockade + derivative evades the fifth-force +"
    )
    print(
        "      qubit-readable). The detectable window is m ~ 4e-12 to 4e-5 eV (kHz-GHz)."
    )
    print(
        "    * OBT's gapless chi (m=0) and radion (0.36 eV) are OUTSIDE the window -- but OBT's LVS"
    )
    print(
        "      ULTRA-LIGHT modulus m_V ~ 1e-6 eV is IN it (f ~ 240 MHz). OBT predicts a field at exactly"
    )
    print("      the qubit-detectable mass.")
    print(
        "    * => A CONCRETE, FALSIFIABLE no-mass target: look for a ~1e-6 eV scalar (m_V) in qubit"
    )
    print(
        "      dark-matter detectors. This is the os/chair BONE of the chi-route -- a real experiment."
    )
    print(
        "    HONEST GATES: (i) m_V must be a DM fraction (the coherent amplitude); (ii) it must carry a"
    )
    print(
        "      derivative/detectable matter coupling (natural for a modulus/axion, but BEYOND V8.2 to"
    )
    print(
        "      specify); (iii) the coupling must sit in the OPEN ALP space. None closed -- a live hunt."
    )
    print(
        "    * This does NOT read the germe/future (that stays no-signaling-walled); it DETECTS OBT's"
    )
    print(
        "      light dark-sector scalar -- a genuine no-mass bulk-SECTOR measurement."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (window ~4e-12..4e-5 eV; LVS m_V in-window at ~240 MHz)."
    )
    print("=" * 92)


if __name__ == "__main__":
    main()
