"""Seed 3 (V9.0, quarantined) — the [[5,1,3]] code on REAL circuits (qiskit / Aer / IBM-ready).

Puts gate 1 + gate (a) on actual qubits: a qiskit circuit of the [[5,1,3]] perfect ('HaPPY')
code, runnable on the Aer simulator now and submittable to IBM Quantum hardware. It tests the
OUT/CODE side of Gate-IN -- the protected-yet-sensitive SYNDROME structure -- NOT the demon:
superconducting/trapped-ion qubits are not mesoscopic masses at 0.2um and feel no 5D collapse,
so this validates the CODE machinery on hardware, not the Penrose-Diosi physics.

Demonstrated on the circuit and cross-checked against qiskit's own Pauli algebra + Aer:
  - no error             -> syndrome 0000   (the prepared state IS a codeword);
  - single-qubit Z_j     -> syndrome NONZERO (local noise DETECTED -> correctable: GATE 1, deaf);
  - collective Z_L=ZZZZZ -> syndrome 0000   (INVISIBLE to the checks: GATE a) yet it flips the
                            logical sign on |+_L> (the 'demon' acts on the germe, not corrected).

NOT V8.2. Not in the PDF. 'code, don't plead': the codeword is verified a +1 eigenstate of all
stabilizers (statevector); every Aer syndrome is asserted against qiskit's Pauli.commutes; the
logical flip is asserted from Aer counts.

NOTE on conventions: everything is in qiskit's qubit ordering (qubit 0 = least significant);
the syndrome BITS therefore need not match the numpy atom (er_epr_stabilizer.py) bit-for-bit,
but the STRUCTURE (single-Z detected, Z_L invisible) is convention-independent and is what gates
1 and (a) rest on. Self-consistency (Aer == qiskit algebra) is the injection test.
"""

import numpy as np
import qiskit
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Operator, Pauli, Statevector
from qiskit_aer import AerSimulator

STAB_LABELS = ("XZZXI", "IXZZX", "XIXZZ", "ZXIXZ")  # the [[5,1,3]] stabilizers
STAB = [Pauli(s) for s in STAB_LABELS]
ZL = Pauli("ZZZZZ")  # logical Z
XL = Pauli("XXXXX")  # logical X
DIM = 2**5
SHOTS = 4096
BACKEND = AerSimulator()


def _project(v, g):
    """Apply the projector (I+g)/2 onto the +1 eigenspace of Pauli g to statevector data v."""
    G = Operator(g).data
    return (np.eye(DIM) + G) / 2 @ v


def codeword(logical="0"):
    """|0_L> = project |00000> onto +1 of all 4 stabilizers AND of Z_L; |+_L> = (|0_L>+|1_L>)/v2."""
    v = Statevector.from_label("00000").data
    for g in STAB:
        v = _project(v, g)
    v = _project(v, ZL)  # +1 of Z_L picks |0_L>
    v = v / np.linalg.norm(v)
    if logical == "0":
        return Statevector(v)
    one = Operator(XL).data @ v  # |1_L> = X_L |0_L>
    if logical == "1":
        return Statevector(one / np.linalg.norm(one))
    plus = (v + one) / np.linalg.norm(v + one)  # |+_L>
    return Statevector(plus)


def expected_syndrome(error_qubits):
    """Syndrome of a pure-Z error on `error_qubits` (qiskit indices), via qiskit's Pauli algebra."""
    label = ["I"] * 5
    for q in error_qubits:
        label[4 - q] = "Z"  # qiskit label index 4-q == qubit q
    E = Pauli("".join(label))
    return tuple(0 if g.commutes(E) else 1 for g in STAB)


def syndrome_from_aer(error_qubits, init_state):
    """Build init -> Z-error -> 4 stabilizer measurements; run Aer; return the (deterministic) syndrome."""
    data, anc = QuantumRegister(5, "d"), QuantumRegister(4, "a")
    cl = ClassicalRegister(4, "s")
    qc = QuantumCircuit(data, anc, cl)
    qc.initialize(init_state.data, data)
    for q in error_qubits:
        qc.z(data[q])
    for i, g in enumerate(STAB):
        qc.h(anc[i])
        for k in range(5):
            xk, zk = bool(g.x[k]), bool(g.z[k])
            if xk and zk:
                qc.cy(anc[i], data[k])
            elif xk:
                qc.cx(anc[i], data[k])
            elif zk:
                qc.cz(anc[i], data[k])
        qc.h(anc[i])
        qc.measure(anc[i], cl[i])
    counts = (
        BACKEND.run(qiskit.transpile(qc, BACKEND), shots=SHOTS).result().get_counts()
    )
    key = max(counts, key=counts.get)  # deterministic -> dominant key
    bits = key.replace(" ", "")
    return tuple(int(bits[len(bits) - 1 - i]) for i in range(4)), counts[key] / SHOTS


def logical_x_expectation(error_qubits):
    """<X_L> on |+_L> after a Z-error: measure all data in the X basis, parity = X_L eigenvalue."""
    data = QuantumRegister(5, "d")
    cl = ClassicalRegister(5, "m")
    qc = QuantumCircuit(data, cl)
    qc.initialize(codeword("+").data, data)
    for q in error_qubits:
        qc.z(data[q])
    qc.h(data)  # rotate X basis -> Z basis
    qc.measure(data, cl)
    counts = (
        BACKEND.run(qiskit.transpile(qc, BACKEND), shots=SHOTS).result().get_counts()
    )
    exp = 0.0
    for key, n in counts.items():
        parity = key.replace(" ", "").count("1") % 2
        exp += ((-1) ** parity) * n / SHOTS
    return exp


def main():
    print("=" * 78)
    print(" [[5,1,3]] code on real circuits (qiskit/Aer) — gate 1 + gate (a) on qubits")
    print("=" * 78)

    # [0] verify the prepared state IS a codeword (statevector injection test) --------
    cw = codeword("0")
    eig = [np.real(cw.expectation_value(g)) for g in STAB]
    zl_eig = np.real(cw.expectation_value(ZL))
    print("\n[0] CODEWORD CHECK (statevector)")
    print(f"    <g_i> for the 4 stabilizers : {[round(e, 6) for e in eig]}")
    print(f"    <Z_L>                       : {round(zl_eig, 6)}")
    assert all(abs(e - 1) < 1e-9 for e in eig), "|0_L> must be +1 of every stabilizer"
    assert abs(zl_eig - 1) < 1e-9, "|0_L> must be +1 of Z_L"
    print("    -> prepared state is a valid |0_L> codeword.")

    # [1] no error -> syndrome 0000 --------------------------------------------------
    print("\n[1] NO ERROR")
    s, frac = syndrome_from_aer([], cw)
    print(f"    Aer syndrome = {s}  (fraction {frac:.3f})")
    assert s == (0, 0, 0, 0), "a clean codeword must give the trivial syndrome"

    # [2] single-qubit Z_j -> NONZERO (GATE 1: local noise detected/correctable) ------
    print("\n[2] SINGLE-QUBIT Z_j  (local noise — GATE 1)")
    for q in range(5):
        s, frac = syndrome_from_aer([q], cw)
        exp = expected_syndrome([q])
        ok = s == exp and any(s)
        print(
            f"    Z_q{q}: Aer={s}  qiskit-algebra={exp}  nonzero={any(s)}  [{'OK' if ok else 'MISMATCH'}]"
        )
        assert s == exp, f"Aer syndrome must match qiskit's Pauli algebra for Z_q{q}"
        assert any(
            s
        ), f"a single-qubit error must be DETECTED (nonzero syndrome) for Z_q{q}"
    print(
        "    -> every single-qubit Z is DETECTED -> correctable -> the germe is protected (deaf)."
    )

    # [3] collective Z_L=ZZZZZ -> syndrome 0000 (GATE a: invisible to the checks) -----
    print("\n[3] COLLECTIVE Z_L = ZZZZZ  (the 'demon' — GATE a)")
    s, frac = syndrome_from_aer([0, 1, 2, 3, 4], cw)
    exp = expected_syndrome([0, 1, 2, 3, 4])
    print(f"    Aer syndrome = {s}  qiskit-algebra={exp}  (fraction {frac:.3f})")
    assert s == (0, 0, 0, 0) and exp == (
        0,
        0,
        0,
        0,
    ), "Z_L must be INVISIBLE (zero syndrome)"
    print(
        "    -> Z_L gives ZERO syndrome: the collective channel is NOT corrected (invisible)."
    )

    # [4] but Z_L DOES act on the logical qubit (GATE a: the demon is heard) ----------
    print("\n[4] LOGICAL EFFECT on |+_L>  (is the invisible Z_L actually heard?)")
    xl_clean = logical_x_expectation([])
    xl_zl = logical_x_expectation([0, 1, 2, 3, 4])
    print(f"    <X_L> on |+_L>            = {xl_clean:+.3f}  (expect +1)")
    print(
        f"    <X_L> after Z_L           = {xl_zl:+.3f}  (expect -1 -> logical phase-flipped)"
    )
    assert xl_clean > 0.9, "|+_L> should have <X_L> = +1"
    assert xl_zl < -0.9, "Z_L must flip the logical sign (it is a logical operator)"
    print("    -> Z_L is INVISIBLE to the syndrome (3) yet FLIPS the logical sign (4):")
    print(
        "       the collective 'demon' channel is HEARD by the germe while local noise is caught."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (codeword valid; Z_j detected; Z_L invisible + logical)."
    )
    print(
        "  Runs on Aer here; the same circuit submits to IBM Quantum (real superconducting qubits)"
    )
    print(
        "  to demonstrate the CODE -- not the demon (no mass at 0.2um -> no 5D collapse on chip)."
    )
    print("=" * 78)


if __name__ == "__main__":
    main()
