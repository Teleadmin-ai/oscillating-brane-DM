"""Seed 3 (V9.0, quarantined) — THE BULK LISTENER: the QC-as-ANTENNA test bench (Romain's architecture),
runnable on a REAL online quantum computer (--ibm) or on Aer (default, with a noise model that simulates
real-QC decoherence). Romain's "vas y prepare quelque chose qu'on peut utiliser sur un ordi quantique en
ligne et relis en boucle ... travaille tes filtres, rappelle nos astuces pour stabiliser les qubits (il en
faudra plusieurs pour les points de ref), la forme primaire ... + je me demande comment la forme primaire
EVOLUE sur un vrai qubit, est-ce reproductible -> exploitable pour stabiliser ?".

ROMAIN'S ARCHITECTURE (finally restated right): the QC is NOT a calculator -- it is the ANTENNA to the
bulk: a FILTER + AMPLIFIER + MAP. You send the recording (the germe / the question) TO it; it tunes,
protects, and reads. We PROVED the germe-encoded qubit is the optimal matched-filter null-detector
(qiskit_weak_signal_detection / qiskit_multiwitness). This bench assembles that, runnable for real.

THREE parts, each measured on Aer (noise model) and submittable to a real QC (--ibm):
  [B] THE FORM'S EVOLUTION (Romain's new idea): encode the germe, let it evolve (noisy idle), un-encode,
      read the SURVIVAL vs depth, over R runs -> the decay profile + its RUN-TO-RUN reproducibility. The
      systematic decay is reproducible -> a stabilization resource (this is real-QC noise characterization).
  [C] STABILIZATION (our tricks): a BARE qubit vs a DECOHERENCE-FREE-SUBSPACE (DFS) qubit under COLLECTIVE
      dephasing -> the DFS is immune (survives) where the bare one decoheres. Repeated -> the ref points.
  [D] THE MATCHED FILTER (the antenna): INJECT a germe-shaped signal -> the germe-filter catches it (high);
      the BASELINE = the germe-filter on many random non-germe inputs -> the ~1/dim floor = NO false
      positive (anti-pareidolia, the wall from last turn). Selective: high on the germe, floor on anything.

HONEST SCOPE (held): the antenna is the OPTIMAL receiver, but an antenna receives what a SOURCE EMITS via a
CHANNEL. The channel (mapped all session) carries FIELDS (the m_V axion), not a composed answer. So [D]
proves the filter catches a germe-shaped SIGNAL with no false positive -- IF the bulk emits one (the real
bulk signal we can predict = the m_V axion, needing a dedicated detector). [B] and [C] are unconditionally
real (decoherence profiling + DFS protection). What this bench does NOT do: receive a composed answer (no
source emits it). It LISTENS, optimally; what comes is a field or noise -- let the real QC decide.

NOT V8.2. Not in the PDF. 'code, don't plead': survival decay, reproducibility, DFS immunity, and matched-
filter injection/control are measured + asserted. Run: `python bulk_listener.py` (Aer) or `... --ibm`.
Gate-based state prep (no StatePreparation -- it segfaults Aer here); transpiled to a concrete basis.
"""

import sys

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.compiler import transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

SHOTS = 4096
N_FORM = 3  # qubits carrying the primary form (the germe)
GERME_THETAS = [
    0.9,
    2.1,
    1.3,
]  # the primary form's RY pattern (a fixed, specific "form")
DEPTHS = [0, 2, 4, 8, 16]  # noisy-idle depths for the evolution profile
RUNS = 5  # repetitions, for run-to-run reproducibility
AER_BASIS = [
    "rz",
    "sx",
    "x",
    "cx",
]  # decompose into these so Aer never sees state_preparation
RNG = np.random.default_rng(20260629)
_SEED = [
    12345
]  # per-run Aer seed counter -> the whole bench is reproducible (incremented per call)


def form_gate(thetas, label="germe"):
    """A defined FORM: RY(theta_i) per qubit + a CX chain (light, invertible, entangled). The germe."""
    n = len(thetas)
    qc = QuantumCircuit(n, name=label)
    for i, th in enumerate(thetas):
        qc.ry(float(th), i)
    for i in range(n - 1):
        qc.cx(i, i + 1)
    return qc.to_gate()


def dfs_prep_gate():
    """|00> -> (|01>+|10>)/sqrt2 : the DFS state, immune to collective dephasing (H, CX, X)."""
    qc = QuantumCircuit(2, name="dfs")
    qc.h(0)
    qc.cx(0, 1)
    qc.x(1)
    return qc.to_gate()


def plus_gate():
    """|0> -> |+> : the bare qubit (decoheres under dephasing)."""
    qc = QuantumCircuit(1, name="plus")
    qc.h(0)
    return qc.to_gate()


def make_noise_model(p1=0.01, p2=0.02):
    """Depolarizing model on the AER_BASIS gates, so the evolution test is meaningful on Aer; --ibm = real."""
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(p1, 1), ["x", "sx", "rz"])
    nm.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ["cx"])
    return nm


def get_backend(use_ibm):
    """Aer (default, with noise model) or a real online QC (--ibm via qiskit-ibm-runtime)."""
    if use_ibm:
        try:
            from qiskit_ibm_runtime import QiskitRuntimeService

            service = QiskitRuntimeService()
            backend = service.least_busy(operational=True, simulator=False)
            print(f"  [--ibm] real QC: {backend.name}")
            return backend, None
        except (
            Exception
        ) as exc:  # noqa: BLE001 -- any setup failure -> graceful fallback
            print(f"  [--ibm] real QC unavailable ({exc}); using Aer + noise model")
    return AerSimulator(), make_noise_model()


def run_counts(backend, noise_model, circuit, shots=SHOTS):
    """Run one circuit, return counts. Aer: decompose to AER_BASIS (opt 0 keeps the idle gates) + noise.
    IBM: transpile to the backend + SamplerV2."""
    if isinstance(backend, AerSimulator):
        tqc = transpile(circuit, basis_gates=AER_BASIS, optimization_level=0)
        seed, _SEED[0] = (
            _SEED[0],
            _SEED[0] + 1,
        )  # distinct-but-reproducible seed per run
        return (
            backend.run(tqc, shots=shots, noise_model=noise_model, seed_simulator=seed)
            .result()
            .get_counts()
        )
    tqc = transpile(circuit, backend, optimization_level=1)
    from qiskit_ibm_runtime import SamplerV2  # real QC path

    job = SamplerV2(backend).run([tqc], shots=shots)
    return job.result()[0].data.c.get_counts()


def p_allzero(counts):
    """Probability of the all-zero outcome (the survival / overlap readout)."""
    n = sum(counts.values())
    z = sum(v for k, v in counts.items() if set(k.replace(" ", "")) <= {"0"})
    return z / n


def survival_circuit(prep, noisy_layers, n):
    """[prep] -> [noisy idle of given depth] -> [prep^-1] -> measure ; P(0) = the survival fidelity."""
    q, c = QuantumRegister(n, "q"), ClassicalRegister(n, "c")
    qc = QuantumCircuit(q, c)
    qc.append(prep, q)
    for _ in range(
        noisy_layers
    ):  # net-identity but noisy: X then X per qubit, barrier-separated
        qc.x(q)
        qc.barrier(q)
        qc.x(q)
        qc.barrier(q)
    qc.append(prep.inverse(), q)
    qc.measure(q, c)
    return qc


def overlap_circuit(signal_prep, template_prep, n):
    """[signal] -> [template^-1] -> measure ; P(0) = |<template|signal>|^2 (the matched-filter response)."""
    q, c = QuantumRegister(n, "q"), ClassicalRegister(n, "c")
    qc = QuantumCircuit(q, c)
    qc.append(signal_prep, q)
    qc.append(template_prep.inverse(), q)
    qc.measure(q, c)
    return qc


def main():
    use_ibm = "--ibm" in sys.argv
    backend, noise_model = get_backend(use_ibm)
    print("=" * 94)
    print(
        " THE BULK LISTENER — the QC-as-antenna bench (germe form + stabilization + matched filter)"
    )
    print("=" * 94)

    germe = form_gate(GERME_THETAS)

    # ===== [B] THE FORM'S EVOLUTION — Romain's idea: profile it, is it reproducible? ====
    print(
        "\n[B] THE PRIMARY FORM'S EVOLUTION on the qubit (survival vs depth, over runs)"
    )
    print(
        "    depth   survival(mean)   run-to-run std   (reproducible decay = a stabilization resource)"
    )
    means, stds = [], []
    for d in DEPTHS:
        vals = [
            p_allzero(
                run_counts(backend, noise_model, survival_circuit(germe, d, N_FORM))
            )
            for _ in range(RUNS)
        ]
        m, s = float(np.mean(vals)), float(np.std(vals))
        means.append(m)
        stds.append(s)
        print(f"    {d:3d}      {m:6.3f}          {s:6.3f}")
    print(
        f"    => the form decays {means[0]:.2f} -> {means[-1]:.2f} with depth (decoherence); the decay is"
    )
    print(
        f"       REPRODUCIBLE run-to-run (max std {max(stds):.3f}) -> profilable + correctable (stabilize)."
    )
    assert (
        means[0] > means[-1] + 0.1
    ), "the primary form must decohere with depth (a real evolution)"
    assert (
        max(stds) < 0.15
    ), "the form's decay must be REPRODUCIBLE run-to-run (a stabilization resource)"

    # ===== [C] STABILIZATION — our DFS trick vs a bare qubit, under collective dephasing =
    print(
        "\n[C] STABILIZATION — bare qubit vs DECOHERENCE-FREE-SUBSPACE under COLLECTIVE dephasing"
    )
    plus, dfs = plus_gate(), dfs_prep_gate()
    bare_s, dfs_s = [], []
    for phi in np.linspace(
        0, 2 * np.pi, 16, endpoint=False
    ):  # a GRID of collective drifts (clean avg)
        qb, cb = QuantumRegister(1, "q"), ClassicalRegister(1, "c")
        b_qc = QuantumCircuit(qb, cb)
        b_qc.append(plus, qb)
        b_qc.rz(phi, qb[0])
        b_qc.append(plus.inverse(), qb)
        b_qc.measure(qb, cb)
        bare_s.append(p_allzero(run_counts(backend, noise_model, b_qc)))
        qd, cd = QuantumRegister(2, "q"), ClassicalRegister(2, "c")
        d_qc = QuantumCircuit(qd, cd)
        d_qc.append(dfs, qd)
        d_qc.rz(phi, qd[0])
        d_qc.rz(phi, qd[1])  # SAME phi on both = collective -> DFS immune
        d_qc.append(dfs.inverse(), qd)
        d_qc.measure(qd, cd)
        dfs_s.append(p_allzero(run_counts(backend, noise_model, d_qc)))
    bare_m, dfs_m = float(np.mean(bare_s)), float(np.mean(dfs_s))
    print(
        f"    BARE qubit under collective drift : survival = {bare_m:.3f}  (decoheres -> ~0.5 averaged)"
    )
    print(
        f"    DFS qubit (our trick)             : survival = {dfs_m:.3f}  (IMMUNE -> stays high)"
    )
    print(
        f"    => the DFS protects: +{dfs_m - bare_m:.3f} survival. Several such reference qubits give the"
    )
    print("       common-mode reference (the points de ref) -- protect-then-listen.")
    assert (
        dfs_m > bare_m + 0.15
    ), "the DFS must protect against collective dephasing (our stabilization trick)"

    # ===== [D] THE MATCHED FILTER (the antenna) — injection vs control (anti-pareidolia) ==
    print(
        "\n[D] THE MATCHED FILTER (the antenna) — does it catch a germe-signal WITHOUT false positives?"
    )

    def resp(sig, templ):
        return p_allzero(
            run_counts(backend, noise_model, overlap_circuit(sig, templ, N_FORM))
        )

    inj = resp(germe, germe)  # germe-signal through the germe-filter -> matched (high)
    randoms = [form_gate(RNG.uniform(0, 2 * np.pi, N_FORM), f"r{i}") for i in range(8)]
    baseline = float(
        np.mean([resp(r, germe) for r in randoms])
    )  # non-germe -> the floor
    floor = 1.0 / 2**N_FORM  # 1/dim = the random-overlap floor
    print(
        f"    INJECTION (germe-signal -> germe-filter): {inj:.3f}  (the antenna catches the germe)"
    )
    print(
        f"    BASELINE  (8 random non-germe inputs -> germe-filter, avg): {baseline:.3f}  (~1/dim = {floor:.3f})"
    )
    print(
        f"       => SELECTIVE: {inj:.2f} on the germe vs {baseline:.2f} on random = no false positive."
    )
    assert (
        inj > baseline + 0.3
    ), "the matched filter must catch the germe far above its random baseline"
    assert (
        baseline < 0.30
    ), "on non-germe inputs the germe-filter must sit near the 1/dim floor (no false positive)"

    # ===== VERDICT ===================================================================
    print(
        "\n[VERDICT] the antenna is BUILT + runnable (Aer now, --ibm for a real online QC)"
    )
    print(
        "    * [B] the primary form's decoherence is profilable + REPRODUCIBLE -> a stabilization resource"
    )
    print("          (Romain's idea, real -- it IS QC noise characterization).")
    print(
        "    * [C] our DFS trick PROTECTS the qubit against collective drift (the stabilization + ref points)."
    )
    print(
        "    * [D] the germe matched-filter CATCHES a germe-signal with NO false positive on noise (the antenna)."
    )
    print(
        "    * SCOPE (held): an antenna receives what a SOURCE EMITS via a CHANNEL. The channel carries"
    )
    print(
        "      FIELDS (the m_V axion), not a composed answer. So [D] proves the filter is ready -- IF the"
    )
    print(
        "      bulk emits a germe-shaped signal, it catches it (no false positive). The real predictable"
    )
    print(
        "      bulk signal = the m_V axion (a dedicated detector). This bench LISTENS, optimally; what"
    )
    print(
        "      comes back on a real QC is a field or noise -- and we let the real QC decide, not the math."
    )
    print(
        "    => run `python bulk_listener.py --ibm` to listen on a real online QC (submits ~66 circuits;"
    )
    print(
        "       for a serious run, batch them into one Sampler job to cut queue time)."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (form decoheres reproducibly; DFS protects; matched filter, no false +)."
    )
    print("=" * 94)


if __name__ == "__main__":
    main()
