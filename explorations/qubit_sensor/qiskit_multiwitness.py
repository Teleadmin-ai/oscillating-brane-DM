"""Seed 3 (V9.0, quarantined) — do SEVERAL witnesses help? (qiskit / Aer / IBM, Romain's question).

Romain: 'plusieurs qubits temoins non affectes augmentent-ils la sensibilite?' Answer, computed on
real circuits (Aer; qiskit 2.4.2 in the venv), with the honest scalings:

  PART A -- M witnesses sharpen the common-mode REFERENCE (toward a floor).
    A weak signal theta sits on the sensor; a large random drift phi is common to sensor + witnesses.
    Phase estimate of the sensor is psi_s ~ phi + theta; of each witness psi_w ~ phi (no theta).
    theta_est = psi_s - circular_mean(psi_w[:M]).
      * 0 witnesses  -> theta is SWAMPED by phi (std ~ 1.8 rad: unmeasurable);
      * 1 witness    -> theta is RECOVERED (the big jump);
      * M witnesses  -> the witness-reference noise falls ~1/sqrt(M): std -> sqrt(sigma_s^2 +
                        sigma_w^2 / M), saturating at the SENSOR's own floor sigma_s.
    So more witnesses help -- via a better reference (sqrt(M)) -- with DIMINISHING returns once the
    common mode is well subtracted (the sensor's own, non-common noise then dominates).

  PART B -- witnesses/protection let ENTANGLEMENT survive collective noise.
    Under a random collective drift phi: a bare 2-qubit GHZ has <XX> = cos(2*phi + theta) -- it
    AMPLIFIES the collective noise (x2 for N=2) and washes out (std large, mean ~0). The DFS pair
    {|01>,|10>} is IMMUNE (<X_L> = cos(theta), phi-independent). So bare entanglement is HURT by
    collective noise; the witness/DFS protection is what lets a (later, logical) GHZ keep its N x
    super-resolution. Protect first, then entangle.

NET (the answer): yes, more witnesses raise sensitivity -- (sqrt(M) better reference) + (immunity) +
(they ENABLE protected entanglement, the unbounded N x gain) -- but they REDUCE NOISE, they do not
amplify the coupling (the phi^N knob is gate (a)'s asymmetric code), and the floor is the irreducible
non-common noise + the signal size. Witnesses = immunity; entangled sensors = signal.

NOT V8.2. Not in the PDF. Chip qubits are not masses at 0.2um -> this is the DETECTION protocol.
'code, don't plead': every number is an Aer measurement (seeded Monte-Carlo) asserted against the law.
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

BACKEND = AerSimulator()
EST_SHOTS = 512  # finite shots -> realistic phase-readout noise (Part A)
SHOTS = 8192  # Part B contrasts
RNG = np.random.default_rng(20260628)


def _expz(qc, shots):
    counts = (
        BACKEND.run(qc, shots=shots).result().get_counts()
    )  # Aer transpiles internally
    return 2 * counts.get("0", 0) / shots - 1  # <Z> = P0 - P1


def phase_estimate(angle, shots=EST_SHOTS):
    """Two-quadrature Ramsey: prepare |+>, Rz(angle), read <X> and <Y> -> phase = atan2(<Y>,<X>)."""
    qx = QuantumCircuit(1, 1)
    qx.h(0)
    qx.rz(angle, 0)
    qx.h(0)
    qx.measure(0, 0)
    qy = QuantumCircuit(1, 1)
    qy.h(0)
    qy.rz(angle, 0)
    qy.sdg(0)
    qy.h(0)
    qy.measure(0, 0)
    return np.arctan2(_expz(qy, shots), _expz(qx, shots))


def _circmean(angles):
    return np.arctan2(np.mean(np.sin(angles)), np.mean(np.cos(angles)))


def _wrap(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def dfs_xl(phi, theta):
    """DFS pair {|01>,|10>}: <X_L> = cos(theta), independent of the collective drift phi."""
    qc = QuantumCircuit(2, 1)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(1)
    qc.rz(phi, 0)
    qc.rz(phi, 1)  # collective drift
    qc.rz(theta, 0)  # differential signal
    qc.x(1)
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, 0)
    return _expz(qc, SHOTS)


def ghz_xx(phi, theta):
    """Bare 2-qubit GHZ: <XX> = cos(2*phi + theta) -- the collective drift is AMPLIFIED, not cancelled."""
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)  # GHZ (|00>+|11>)/sqrt2
    qc.rz(phi, 0)
    qc.rz(phi, 1)  # collective drift
    qc.rz(theta, 0)  # differential signal
    qc.h(0)
    qc.h(1)
    qc.measure([0, 1], [0, 1])
    counts = (
        BACKEND.run(qc, shots=SHOTS).result().get_counts()
    )  # Aer transpiles internally
    return sum(
        (-1) ** k.replace(" ", "").count("1") * n / SHOTS for k, n in counts.items()
    )


def main():
    print("=" * 80)
    print(
        " Do SEVERAL witnesses help?  (qiskit/Aer) — common-mode reference + protected entanglement"
    )
    print("=" * 80)

    # ===== PART A: M witnesses sharpen the reference (toward a floor) ================
    print(
        "\n[A] M WITNESSES -> sharper common-mode reference (seeded Monte-Carlo on Aer)"
    )
    theta, trials, Mmax = 0.50, 80, 8
    Ms = (1, 2, 4, 8)
    sensor_only, est = [], {M: [] for M in Ms}
    for _ in range(trials):
        phi = RNG.uniform(0, 2 * np.pi)
        psi_s = phase_estimate(phi + theta)
        psi_w = [phase_estimate(phi) for _ in range(Mmax)]
        sensor_only.append(_wrap(psi_s))  # no witness: estimate ~ phi+theta (swamped)
        for M in Ms:
            est[M].append(_wrap(psi_s - _circmean(psi_w[:M])))
    std0 = np.std(sensor_only)
    print(
        f"    signal theta = {theta} rad;  {trials} trials;  {EST_SHOTS} shots/quadrature"
    )
    print(
        f"    0 witnesses : std(theta_est) = {std0:.3f} rad  (theta SWAMPED by the drift)"
    )
    for M in Ms:
        s, m = np.std(est[M]), np.mean(est[M])
        print(
            f"    M={M:<2}witness: std = {s:.3f} rad,  mean = {m:+.3f}  (theta recovered)"
        )
        assert abs(m - theta) < 0.06, f"theta must be recovered with M={M} witnesses"
    s1, s8 = np.std(est[1]), np.std(est[8])
    print(
        f"    -> 0->1 witness: the BIG jump ({std0:.2f} -> {s1:.2f} rad: theta becomes measurable)."
    )
    print(
        f"    -> 1->8 witnesses: the sqrt(M) refinement ({s1:.3f} -> {s8:.3f}; predicted ratio"
    )
    print(
        f"       sqrt((1+1)/(1+1/8)) = {np.sqrt(2/1.125):.2f}, measured {s1/s8:.2f}) -> saturates at the"
    )
    print(
        "       sensor's own floor: diminishing returns once the common mode is subtracted."
    )
    assert std0 > 1.0, "without a witness the signal must be swamped"
    assert s8 < 0.9 * s1, "more witnesses must reduce the residual (sqrt(M) reference)"
    assert s1 < 0.5 * std0, "one witness must already rescue the signal"

    # ===== PART B: protection lets entanglement survive collective noise =============
    print(
        "\n[B] WHY PROTECT THE ENTANGLEMENT  (bare GHZ vs DFS under a random collective drift)"
    )
    phis = RNG.uniform(0, 2 * np.pi, 24)
    dfs_vals = [dfs_xl(p, theta) for p in phis]
    ghz_vals = [ghz_xx(p, theta) for p in phis]
    print(
        f"    over 24 random collective drifts phi  (signal theta = {theta}, cos theta = {np.cos(theta):.3f}):"
    )
    print(
        f"    DFS pair  <X_L>: mean {np.mean(dfs_vals):+.3f}, std {np.std(dfs_vals):.3f}  (IMMUNE: keeps cos theta)"
    )
    print(
        f"    bare GHZ  <XX> : mean {np.mean(ghz_vals):+.3f}, std {np.std(ghz_vals):.3f}  (WASHES OUT: cos(2phi+theta))"
    )
    assert np.std(dfs_vals) < 0.1 and abs(np.mean(dfs_vals) - np.cos(theta)) < 0.1
    assert (
        np.std(ghz_vals) > 0.4
    ), "bare GHZ must wash out under random collective drift"
    print(
        "    -> bare entanglement AMPLIFIES collective noise (x2 here) and dies; the DFS/witness"
    )
    print(
        "       is immune. So you must PROTECT first, then entangle: a logical GHZ over DFS-"
    )
    print(
        "       protected qubits keeps the N x super-resolution that bare GHZ loses to noise."
    )

    # ===== synthesis ================================================================
    print("\n[C] ANSWER — do several witnesses raise sensitivity?")
    print("    YES, by THREE channels, only one unbounded:")
    print(
        "    1. better common-mode REFERENCE ~1/sqrt(M)  (A) -- but saturates at the sensor floor;"
    )
    print(
        "    2. more IMMUNITY (a larger decoherence-free subspace) -- robustness, not signal;"
    )
    print(
        "    3. they ENABLE protected entanglement (B) -> the N x Heisenberg gain bare GHZ can't"
    )
    print("       keep under noise. THIS is the unbounded lever.")
    print(
        "    Honest: witnesses REDUCE NOISE, they do not amplify the phi^N coupling (gate (a)'s"
    )
    print(
        "    asymmetric code does). Floor = the irreducible non-common noise + the signal E_G."
    )
    print(
        "    Architecture: a few witnesses (immunity) + many entangled+protected sensors (signal)."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (witness rescues + sqrt(M) refines; DFS immune, bare GHZ washes)."
    )
    print("=" * 80)


if __name__ == "__main__":
    main()
