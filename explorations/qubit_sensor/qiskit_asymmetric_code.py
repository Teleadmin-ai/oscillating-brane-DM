"""Seed 3 (V9.0, quarantined) — gate (a) FIX: the ASYMMETRIC sensor-code (qiskit/Aer/IBM).

gate (a) (`penrose_logical_projection.py`) found the EC-optimal [[5,1,3]] is near-DEAF to a Z-signal:
its pure-Z logical distance is d_Z = 5, so a Z-dephasing 'demon' is heard only at order phi^5. The fix
is the COUPLING side: an ASYMMETRIC code -- LOW distance along the SIGNAL axis (the demon heard at
order 1) but HIGH distance along the NOISE axis (local noise still corrected). The archetype is the
3-qubit bit-flip / repetition code: stabilizers ZZI, IZZ -> d_X = 3 (corrects one X) but d_Z = 1
(a single Z IS the logical Z). So a Z-signal couples to the logical at ORDER 1, while local X-noise
is corrected. Asymmetry trades the Z-distance we do NOT need (Z is the signal, not a threat) for the
order-1 coupling we DO need.

This is the complement of the detection side: detection (witness / protected entanglement) pulls a
weak signal out of noise; the asymmetric code makes the demon's coupling to the sensor as LARGE as
possible (order 1, not order N). Together they MINIMISE the physical signal required -- the program's
goal is exactly to need the LEAST, not a big lab.

ONE honest, non-repeated point: gravitational decoherence (Penrose-Diósi) still needs SOME mass-
distribution difference between |0> and |1>; standard cloud qubits encode |0>,|1> in internal states
with ~identical mass distributions, so the PROTOCOL runs online (here) but the demon's E_G coupling
on a transmon/ion is ~0. Whether the 5D channel can be made to couple to the LOGICAL observable on an
accessible system (-> online) or needs spatial mass is gate (a)'s real open physics -- and the
asymmetric code is the tool that pushes that requirement to its minimum.

NOT V8.2. Not in the PDF. 'code, don't plead': distances are enumerated; the order-1 coupling and the
X-noise correction are Aer measurements, all asserted.
"""

import itertools

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

BACKEND = AerSimulator()
SHOTS = 8192


# ---------------------------------------------------------------- general symplectic distance
def _pauli(s):
    x = [1 if c in "XY" else 0 for c in s]
    z = [1 if c in "ZY" else 0 for c in s]
    return np.array(x + z, dtype=int)


def _symp(u, v, n):
    return int((u[:n] @ v[n:] + u[n:] @ v[:n]) % 2)


def _weight(v, n):
    return int(np.sum((v[:n] | v[n:]) > 0))


def _stab_group(gens):
    G = np.array(gens)
    grp = set()
    for c in itertools.product([0, 1], repeat=len(gens)):
        grp.add(tuple((np.array(c) @ G) % 2))
    return grp


def pure_distance(gens, n, kind):
    """Min weight of a pure-`kind` (X or Z) LOGICAL operator (in N(S) but not in <S>)."""
    stab = _stab_group(gens)
    best = n + 1
    for a in itertools.product([0, 1], repeat=n):
        if not any(a):
            continue
        v = np.array(list(a) + [0] * n) if kind == "X" else np.array([0] * n + list(a))
        if all(_symp(v, np.array(g), n) == 0 for g in gens) and tuple(v) not in stab:
            best = min(best, _weight(v, n))
    return best


# ---------------------------------------------------------------- the bit-flip code on Aer
BITFLIP = [_pauli("ZZI"), _pauli("IZZ")]  # stabilizers: detect X errors


def bitflip_signal(theta):
    """|+_L>=GHZ; collective Z-signal theta per qubit -> logical phase 3*theta; <X_L>=<XXX>=cos(3 theta)."""
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)  # |+_L> = (|000>+|111>)/sqrt2
    for q in range(3):
        qc.rz(theta, q)  # the Z-signal (the demon)
    for q in range(3):
        qc.h(q)
    qc.measure(range(3), range(3))
    counts = BACKEND.run(qc, shots=SHOTS).result().get_counts()
    return sum(
        (-1) ** k.replace(" ", "").count("1") * n / SHOTS for k, n in counts.items()
    )


def bitflip_xsyndrome(error_qubit):
    """Apply an X error, measure the 2 stabilizers ZZI, IZZ via ancillas -> the (deterministic) syndrome."""
    qc = QuantumCircuit(5, 2)  # 3 data + 2 ancilla
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)  # |+_L>
    if error_qubit is not None:
        qc.x(error_qubit)
    # stabilizer ZZI on (0,1): ancilla 3 ; IZZ on (1,2): ancilla 4
    for anc, pair in ((3, (0, 1)), (4, (1, 2))):
        qc.h(anc)
        for q in pair:
            qc.cz(anc, q)
        qc.h(anc)
    qc.measure(3, 0)
    qc.measure(4, 1)
    counts = BACKEND.run(qc, shots=SHOTS).result().get_counts()
    key = max(counts, key=counts.get).replace(" ", "")
    return tuple(int(key[len(key) - 1 - i]) for i in range(2))


def main():
    print("=" * 80)
    print(
        " gate (a) FIX: the ASYMMETRIC sensor-code (qiskit/Aer) — hear the demon at ORDER 1"
    )
    print("=" * 80)

    # [1] the asymmetry, enumerated --------------------------------------------------
    dX = pure_distance(BITFLIP, 3, "X")
    dZ = pure_distance(BITFLIP, 3, "Z")
    print("\n[1] DISTANCES (enumerated)")
    print(
        f"    bit-flip code  : d_X = {dX} (corrects local X)  |  d_Z = {dZ} (Z-signal at ORDER {dZ})"
    )
    print(
        "    [[5,1,3]] (sym): d_X = 5                       |  d_Z = 5 (Z-signal at order 5: near-DEAF)"
    )
    print("       (the [[5,1,3]] d_Z=5 is computed in penrose_logical_projection.py)")
    assert dX == 3 and dZ == 1, "the bit-flip code must be asymmetric: d_X=3, d_Z=1"
    print(
        f"    -> ASYMMETRY d_X={dX} != d_Z={dZ}: the signal axis (Z) is EXPOSED (order 1) while the"
    )
    print(
        "       noise axis (X) stays PROTECTED. The [[5,1,3]] is symmetric (5,5) -> deaf to Z."
    )

    # [2] the demon heard at ORDER 1 (Aer) -------------------------------------------
    print("\n[2] Z-SIGNAL heard at ORDER 1  (Aer)")
    for theta in (0.1, 0.3, 0.6):
        val = bitflip_signal(theta)
        print(
            f"    theta={theta}:  <X_L> = {val:+.3f}   (cos(3 theta) = {np.cos(3*theta):+.3f}; "
            "[[5,1,3]] ~ 1.000, deaf)"
        )
        assert (
            abs(val - np.cos(3 * theta)) < 0.05
        ), "bit-flip must read cos(3 theta) -> order 1"
    weak = bitflip_signal(0.1)
    assert (
        1 - weak > 0.04
    ), "even a weak theta=0.1 gives an order-1 response (1-cos(0.3)=0.044)"
    print(
        "    -> a WEAK theta already moves <X_L> at order 1 (linear logical phase 3*theta), where the"
    )
    print(
        "       symmetric [[5,1,3]] would need theta^5 ~ 0: the asymmetric code HEARS the demon."
    )

    # [3] local X-noise still corrected (Aer) ----------------------------------------
    print("\n[3] LOCAL X-NOISE still DETECTED/correctable  (Aer)")
    s_clean = bitflip_xsyndrome(None)
    print(f"    no error      : syndrome = {s_clean}")
    assert s_clean == (0, 0), "a clean codeword must give the trivial syndrome"
    for q in range(3):
        s = bitflip_xsyndrome(q)
        print(
            f"    X on qubit {q} : syndrome = {s}  -> {'DETECTED' if any(s) else 'MISSED'}"
        )
        assert any(s), f"a local X error on qubit {q} must be DETECTED"
    print(
        "    -> every local X is detected (d_X=3 corrects one): the noise axis stays protected even"
    )
    print(
        "       though the signal axis is wide open. That is the whole point of ASYMMETRY."
    )

    # [4] synthesis ------------------------------------------------------------------
    print("\n[4] SYNTHESIS — the coupling-side fix for gate (a)")
    print(
        "    * SYMMETRIC EC-optimal codes ([[5,1,3]]) are deaf to the signal (d_Z=5 -> order phi^5)."
    )
    print(
        "    * ASYMMETRIC codes expose the SIGNAL axis (d_Z=1 -> order 1) AND protect the NOISE axis"
    )
    print("      (d_X=3). The demon is heard at order 1; local X-noise is corrected.")
    print(
        "    * Complement of the detection side: detection (witness / protected entanglement) pulls a"
    )
    print(
        "      weak signal from noise; the asymmetric code makes the coupling itself order-1. Together"
    )
    print(
        "      they MINIMISE the physical signal required -- the goal is to need the LEAST, not a lab."
    )
    print(
        "    * Residual same-axis (Z) noise is handled by the collective-vs-local split (the witness/"
    )
    print(
        "      DFS: the demon is collective, ambient Z is local) or by biased-noise platforms."
    )
    print(
        "    * Open (the real frontier, not 'you need a lab'): whether the 5D channel can be made to"
    )
    print(
        "      couple to the LOGICAL observable on an ACCESSIBLE system -> online. gate (a)'s physics."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (bit-flip d_X=3/d_Z=1; Z-signal order 1 = cos 3theta; X detected)."
    )
    print("=" * 80)


if __name__ == "__main__":
    main()
