"""Seed 3 (V9.0, quarantined) — DETECTION side: pulling a weak signal out (qiskit / Aer / IBM).

Romain's correction to gate (a): a small (order phi^N) coupling is a SENSITIVITY challenge, not a
deafness -- extracting a weak coherent signal from noise is exactly what quantum sensing does. And
the right architecture is not one big mass but TWO TWINNED systems read differentially (the
Bose-Marletto-Vedral two-mass picture). This puts that on real circuits (Aer now, IBM-submittable):

  PART A -- WITNESS / decoherence-free subspace = the TWINNED PAIR (Romain's 'qubit temoin' / 'deux
    systemes jumeles'). Encode one logical qubit across a PAIR in the DFS {|01>,|10>}. A COLLECTIVE
    dephasing Rz(phi) on BOTH (drift / common-mode) CANCELS; a DIFFERENTIAL signal Rz(theta) on one
    member only (the 'demon') is recorded as the logical phase. -> common-mode rejection: a weak
    theta survives a large phi. (This is the gravitational-gradiometer / BMV geometry: two twins,
    read by their difference.)

  PART B -- ENTANGLEMENT (GHZ) sensitivity, and its honest limit. An N-qubit GHZ probe makes the
    phase fringe oscillate N times FASTER (cos(N*theta) vs cos(theta)) = phase super-resolution ->
    Heisenberg-scaling sensitivity to a weak theta. BUT bare GHZ is FRAGILE: under local dephasing p
    its contrast decays (1-2p)^N, N times faster than a lone qubit (Huelga et al. 1997). So
    entanglement helps ONLY IF PROTECTED -- the seed's point (DFS in A; the QEC atom for scale).

These attack the DETECTION side (extract a given weak signal toward the Heisenberg limit) and, with
the twinned pair, LOWER the detectable-mass threshold -- you do not need one big mesoscopic mass.
They do NOT change the phi^N COUPLING (gate (a)'s asymmetric-code knob). Coupling x detection x
twinned-pair = the real sensor-design problem; gate (a) is an SNR question, not a deafness.

NOT V8.2. Not in the PDF. Chip qubits are not masses at 0.2um -> this validates the DETECTION
PROTOCOLS on hardware, never the demon. 'code, don't plead': Parts A and B1 are Aer measurements
asserted against closed forms; B2's fragility is the textbook (1-2p)^N, computed and labelled.
"""

import numpy as np
import qiskit
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

SHOTS = 8192
BACKEND = AerSimulator()


def _counts(qc):
    return BACKEND.run(qiskit.transpile(qc, BACKEND), shots=SHOTS).result().get_counts()


def _expectation_parity(counts):
    """<X^N> from X-basis counts = sum (-1)^(number of 1s) * probability."""
    return sum(
        (-1) ** k.replace(" ", "").count("1") * n / SHOTS for k, n in counts.items()
    )


# ---------------------------------------------------------------- PART A: twinned pair / DFS
def dfs_differential(phi, theta):
    """DFS {|01>,|10>}: collective Rz(phi) cancels; differential Rz(theta) on one twin is read."""
    qc = QuantumCircuit(2, 1)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(1)  # encode |+_L> = (|01>+|10>)/sqrt2 across the twinned pair
    qc.rz(phi, 0)
    qc.rz(phi, 1)  # COMMON-MODE drift on both twins (cancels in the DFS)
    qc.rz(theta, 0)  # DIFFERENTIAL signal on one twin only (the demon)
    qc.x(1)
    qc.cx(0, 1)
    qc.h(0)  # decode (inverse encoder)
    qc.measure(0, 0)
    return (
        2 * _counts(qc).get("0", 0) / SHOTS - 1
    )  # <X_L> = cos(theta), phi-independent


def single_ramsey(phi, theta):
    """A lone qubit: <X> = cos(phi+theta) -- the weak theta is swamped by the drift phi."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.rz(phi + theta, 0)
    qc.h(0)
    qc.measure(0, 0)
    return 2 * _counts(qc).get("0", 0) / SHOTS - 1


# ---------------------------------------------------------------- PART B: GHZ sensitivity
def parity_fringe(n, theta, ghz):
    """<X^n> after a phase theta per qubit. GHZ -> cos(n*theta); separable -> cos(theta)^n."""
    qc = QuantumCircuit(n, n)
    if ghz:
        qc.h(0)
        for k in range(1, n):
            qc.cx(0, k)
    else:
        for k in range(n):
            qc.h(k)
    for k in range(n):
        qc.rz(theta, k)
    for k in range(n):
        qc.h(k)
    qc.measure(range(n), range(n))
    return _expectation_parity(_counts(qc))


def main():
    print("=" * 80)
    print(
        " DETECTION of a weak signal on real circuits (qiskit/Aer) — twinned pair + entanglement"
    )
    print("=" * 80)

    # ===== PART A: twinned pair / DFS common-mode rejection =========================
    print(
        "\n[A] TWINNED PAIR / DFS  (a weak differential signal survives a large common drift)"
    )
    theta = 0.30  # the weak 'demon' signal (rad); cos(theta) = 0.955
    phis = np.linspace(0, 2 * np.pi, 12, endpoint=False)
    dfs_vals = [dfs_differential(p, theta) for p in phis]
    single_vals = [single_ramsey(p, theta) for p in phis]
    print(f"    weak signal theta = {theta} rad  (cos theta = {np.cos(theta):.3f})")
    print(
        f"    DFS pair <X_L> over 12 drifts phi: mean {np.mean(dfs_vals):+.3f}, std {np.std(dfs_vals):.3f}"
    )
    print(
        f"    lone qubit <X> over 12 drifts phi: mean {np.mean(single_vals):+.3f}, std {np.std(single_vals):.3f}"
    )
    assert abs(np.mean(dfs_vals) - np.cos(theta)) < 0.05, "DFS must read cos(theta)"
    assert (
        np.std(dfs_vals) < 0.05
    ), "DFS must be drift-independent (common-mode rejected)"
    assert np.std(single_vals) > 0.4, "the lone qubit must be swamped by the drift"
    print(
        "    -> the twinned pair reads cos(theta) for EVERY drift phi (std ~0): the witness"
    )
    print(
        "       cancels the common-mode and isolates the weak signal; the lone qubit is swamped."
    )

    # ===== PART B: entanglement super-resolution (Heisenberg) + honest fragility =====
    print("\n[B] ENTANGLEMENT (GHZ) — phase super-resolution and its honest fragility")
    N = 4
    ghz_pi_N = parity_fringe(N, np.pi / N, True)
    sep_pi_N = parity_fringe(N, np.pi / N, False)
    print(f"    (B1) noiseless fringe, N = {N}  (Aer):")
    print(
        f"         GHZ <X^N>(pi/N) = {ghz_pi_N:+.3f}  (cos(pi) = -1: a half-period already)"
    )
    print(
        f"         sep <X^N>(pi/N) = {sep_pi_N:+.3f}  (cos(pi/N)^N ~ {np.cos(np.pi/N)**N:.2f}: barely moved)"
    )
    assert ghz_pi_N < -0.9, "GHZ must reach -1 at theta=pi/N (N x faster)"
    assert sep_pi_N > 0.0, "separable barely moves at theta=pi/N"
    print(
        f"         -> GHZ RESOLVES theta {N}x finer (phase super-resolution); the per-shot"
    )
    print(
        f"            metrological precision gain is sqrt(N) = {np.sqrt(N):.1f}x (Heisenberg vs SQL)."
    )
    p = 0.08  # local dephasing per qubit
    print(
        f"    (B2) honest fragility under local dephasing p = {p}  (closed form, Huelga 1997):"
    )
    for nv in (1, 2, 4):
        print(f"         N={nv}: contrast (1-2p)^N = {(1 - 2 * p) ** nv:.3f}")
    assert (1 - 2 * p) ** N < (1 - 2 * p), "GHZ (N>1) decays faster than a lone qubit"
    print(
        f"         -> the {N}x sensitivity is bought at {N}x faster decoherence: bare GHZ is"
    )
    print(
        "            FRAGILE to local noise. Entanglement helps ONLY IF protected (DFS/QEC)."
    )

    # ===== synthesis ================================================================
    print(
        "\n[C] SYNTHESIS — is the weak demon signal detectable, and must the mass be big?"
    )
    print(
        "    * NOT deaf: the twinned pair / witness rejects common-mode (A) and entanglement"
    )
    print(
        "      gives phase super-resolution (B1) -- weak coherent signals ARE extractable."
    )
    print(
        "    * Bare entanglement is noise-fragile (B2) -> it must be PROTECTED. The DFS pair (A)"
    )
    print(
        "      is the minimal protected probe; the QEC atom (er_epr_stabilizer.py) is the scalable"
    )
    print("      one. Protected-entangled twin sensing = the seed's qubit-sensor.")
    print(
        "    * ON THE MASS (Romain's point): you do NOT need one big mesoscopic mass. Quantum"
    )
    print(
        "      sensing LOWERS the detectable-mass threshold; the right geometry is TWO TWINNED"
    )
    print(
        "      (entangled) systems read DIFFERENTIALLY -- exactly the Bose-Marletto-Vedral"
    )
    print(
        "      two-mass setup -- whose frontier is moving to SMALLER masses precisely because of"
    )
    print(
        "      better quantum sensing. The hard limit is QUANTITATIVE (the demon's E_G ~ G*m^2"
    )
    print(
        "      must exceed the irreducible DIFFERENTIAL-noise floor for achievable N x T), not a"
    )
    print(
        "      fixed 'mesoscopic' mass. (Smaller still loses signal as E_G ~ m^2; a sweet spot"
    )
    print(
        "      remains near R ~ L where 5D is on and the per-twin mass is appreciable.)"
    )
    print(
        "    * Honest scope: DETECTION protocol only (no chip qubit is a mass); the phi^N COUPLING"
    )
    print(
        "      is separate (gate (a)). Coupling x detection x twinned-pair = the design problem."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (twin DFS rejects drift; GHZ Nx fringe; fragility (1-2p)^N)."
    )
    print("=" * 80)


if __name__ == "__main__":
    main()
