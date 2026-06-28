"""Seed 3 (V9.0, quarantined) — PROTECT-THEN-ENTANGLE: a protected entangled probe (qiskit/Aer/IBM).

The payoff of the detection arc. `qiskit_weak_signal_detection.py` showed bare GHZ gives N x phase
super-resolution but is killed by collective noise; `qiskit_multiwitness.py` showed the witness/DFS
is immune. This closes it: an entangled probe placed INSIDE the collective decoherence-free subspace
keeps BOTH -- the N x super-resolution AND the immunity. 'Protect first, then entangle.'

The probe (4 qubits): |psi> = (|0011> + |1100>)/sqrt2  (q0 q1 q2 q3).
  * COLLECTIVE dephasing Rz(phi) on all 4 CANCELS: both branches carry two |1>s -> sum of Z = 0
    -> the probe is in the DFS of collective dephasing (IMMUNE), like the twin pair but entangled.
  * a DIFFERENTIAL signal Rz(theta) on the signal pair (q0,q1) gives the branches a relative phase
    2*theta -> N x = 2 x super-resolution (the entanglement enhancement) on the demon's signal.
Contrast: a bare 4-qubit GHZ (|0000>+|1111>) under the same collective drift has <XXXX> =
cos(4*phi + 2*theta) -> it AMPLIFIES the drift x4 and washes out. Same entanglement, no protection.

NOT V8.2. Not in the PDF. Chip qubits are not masses at 0.2um -> this is the DETECTION protocol, the
'protect-then-entangle' architecture of the seed's qubit-sensor; not the demon. 'code, don't plead':
every number is an Aer measurement asserted against the closed form.
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

BACKEND = AerSimulator()
SHOTS = 8192


def _counts(qc):
    return (
        BACKEND.run(qc, shots=SHOTS).result().get_counts()
    )  # Aer transpiles internally


def _encode(qc):
    """|0000> -> (|0011>+|1100>)/sqrt2 : a GHZ between the (q0,q1) and (q2,q3) pairs, balanced (DFS)."""
    qc.x(2)
    qc.x(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.cx(0, 3)


def protected_probe(phi, theta):
    """Entangled probe in the collective-DFS: returns <Z_q0> after decode = cos(2*theta), phi-immune."""
    qc = QuantumCircuit(4, 1)
    _encode(qc)
    for q in range(4):
        qc.rz(phi, q)  # COLLECTIVE drift on all four (cancels in the DFS)
    qc.rz(theta, 0)
    qc.rz(
        theta, 1
    )  # DIFFERENTIAL signal on the signal pair -> 2*theta (super-resolution)
    qc.cx(0, 3)  # decode (inverse encoder)
    qc.cx(0, 2)
    qc.cx(0, 1)
    qc.h(0)
    qc.x(3)
    qc.x(2)
    qc.measure(0, 0)
    return 2 * _counts(qc).get("0", 0) / SHOTS - 1  # cos(2 theta), independent of phi


def bare_ghz4(phi, theta):
    """Bare 4-qubit GHZ: <XXXX> = cos(4*phi + 2*theta) -- amplifies the collective drift x4, washes out."""
    qc = QuantumCircuit(4, 4)
    qc.h(0)
    for q in range(1, 4):
        qc.cx(0, q)  # GHZ (|0000>+|1111>)/sqrt2
    for q in range(4):
        qc.rz(phi, q)  # COLLECTIVE drift
    qc.rz(theta, 0)
    qc.rz(theta, 1)  # same differential signal on the signal pair
    for q in range(4):
        qc.h(q)
    qc.measure(range(4), range(4))
    counts = _counts(qc)
    return sum(
        (-1) ** k.replace(" ", "").count("1") * n / SHOTS for k, n in counts.items()
    )


def main():
    print("=" * 80)
    print(
        " PROTECT-THEN-ENTANGLE (qiskit/Aer) — an entangled probe inside the collective DFS"
    )
    print("=" * 80)
    theta = 0.30
    rng = np.random.default_rng(20260628)
    phis = rng.uniform(0, 2 * np.pi, 24)

    # [1] immunity to collective drift: protected probe vs bare GHZ ===================
    print(f"\n[1] IMMUNITY to a random collective drift  (signal theta = {theta:.2f})")
    prot = [protected_probe(p, theta) for p in phis]
    bare = [bare_ghz4(p, theta) for p in phis]
    print(
        f"    protected probe  <Z>  : mean {np.mean(prot):+.3f}, std {np.std(prot):.3f}  "
        f"(target cos 2theta = {np.cos(2 * theta):+.3f}) -> IMMUNE"
    )
    print(
        f"    bare 4-qubit GHZ <XXXX>: mean {np.mean(bare):+.3f}, std {np.std(bare):.3f}  "
        "(cos(4 phi + 2 theta)) -> WASHES OUT"
    )
    assert np.std(prot) < 0.1, "the protected probe must be immune to collective drift"
    assert (
        abs(np.mean(prot) - np.cos(2 * theta)) < 0.1
    ), "protected probe must read cos(2 theta)"
    assert np.std(bare) > 0.4, "bare GHZ must wash out under random collective drift"

    # [2] the entanglement is still there: 2x super-resolution =======================
    print("\n[2] SUPER-RESOLUTION retained  (entanglement survives the protection)")
    # protected probe fringe = cos(2 theta): reaches -1 at theta = pi/2 (a single qubit's cos(theta)=0 there)
    at_half = protected_probe(0.0, np.pi / 2)
    at_quarter = protected_probe(0.0, np.pi / 4)
    print(
        f"    protected <Z>(theta=pi/2) = {at_half:+.3f}  (cos(pi) = -1: a half-period -> 2x faster)"
    )
    print(f"    protected <Z>(theta=pi/4) = {at_quarter:+.3f}  (cos(pi/2) = 0)")
    assert (
        at_half < -0.9
    ), "the protected probe must keep the 2x super-resolution (cos 2theta)"
    assert abs(at_quarter) < 0.1, "cos(2*pi/4)=cos(pi/2)=0"
    print(
        "    -> the probe oscillates in 2*theta = 2x super-resolution, AND (from [1]) is immune to"
    )
    print(
        "       collective drift. The entanglement enhancement SURVIVES because it lives in the DFS."
    )

    # [3] synthesis ==================================================================
    print("\n[3] SYNTHESIS — protect-then-entangle WORKS")
    print(
        "    * bare GHZ: entanglement -> N x super-resolution, but collective noise (amplified x4)"
    )
    print("      washes it out (std 0.7).")
    print(
        "    * protected entangled probe (|0011>+|1100>, in the collective DFS): KEEPS the 2x"
    )
    print(
        "      super-resolution AND is immune (std ~0). The witnesses/DFS that protect the qubit"
    )
    print(
        "      are exactly what let the entanglement deliver its Heisenberg gain under noise."
    )
    print(
        "    * This is the seed's qubit-sensor in miniature: protected + entangled. Scaling the"
    )
    print(
        "      DFS (more witnesses) + the logical GHZ (more signal qubits) pushes N x further --"
    )
    print(
        "      bounded only by the irreducible non-common noise + the demon's E_G (the BMV wall)."
    )
    print(
        "    * Honest: DETECTION protocol on chip qubits (no mass at 0.2um); the phi^N COUPLING is"
    )
    print("      still gate (a)'s asymmetric-code knob, separate.")

    print(
        "\n  ALL INJECTION TESTS PASSED (protected immune + cos 2theta; 2x super-resolution; bare washes)."
    )
    print("=" * 80)


if __name__ == "__main__":
    main()
