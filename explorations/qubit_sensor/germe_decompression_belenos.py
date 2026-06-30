"""Seed 3 (V9.0, quarantined) — germe_decompression FOR belenos-12 (Quandela, 12q gate-based, OVH): the
FORWARD germe-decompressor on a real SYK-class (black-hole) substrate. Romain's "code germe_decompression
pour belenos-12, reprend nos idees (la comparaison avec le germe pour stabiliser / le filtre adapte)".

WHY belenos-12 (gate-based) and not orion (Pasqal analog): the OBT network is SYK / black-hole class (the
MSS consilience lambda_L -> T_H=900 K, pasqal_er_epr_rydberg). SYK needs all-to-all 4-Majorana couplings --
universal gate-based, NOT Rydberg-geometric. belenos-12 (12 qubits = N=24 Majorana) is the OVH machine that
CAN run a (sparse) SYK. Here a SPARSE SYK on n=6 qubits (N=12 Majorana) keeps the depth feasible.

THE FORWARD DECOMPRESSOR (the honest, useful role -- NOT a closure-finalizer):
  ENCODE the germe (the radion wavepacket, germe_decompression's phi0=1.40 M_s state) on n qubits
   -> DECOMPRESS by a SPARSE-SYK quench (Trotterized e^{-iHt}, H = sum J_abcd gamma_a gamma_b gamma_c gamma_d
      via Jordan-Wigner; the black-hole-class scrambling = the cosmic decompression)
   -> READ: [the TREE] the output distribution unfolds per depth (entropy grows, like germe_tree_decompressor);
            [the MATCHED FILTER / germe-as-reference] the germe overlap decorrelates as it scrambles;
            [the ENTANGLEMENT / RT-like] S(half) grows from the low-entanglement germe.

SCOPE (the os/chair line, held): this RUNS a germe-CANDIDATE forward on a real SYK substrate and reads its
observables -> it TESTS OBT germe-candidates against the universe (forward), it does NOT DERIVE the germe nor
FINALIZE closure (syk_schwarzian_closure: the amount = the IC; measuring reads the input's consequences, it
does not invert to the input). Same epistemic level as the cobaya inference -- forward, not inverse.

NOT V8.2. Not in the PDF. 'code, don't plead' + 'seul les calculs comptent': the germe overlap decorrelation,
the entanglement growth, and the tree-entropy growth are COMPUTED (exact Statevector, n=6) + asserted only as
sim-correctness (the quench scrambles/entangles/unfolds) -- no imposed result-ranges. Runs here on the exact
simulator; the gate circuit is submittable to belenos-12 via OVH/Quandela (Perceval), sampling the same reads.
"""

import warnings

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp, Statevector, partial_trace
from scipy.sparse import SparseEfficiencyWarning

warnings.filterwarnings(
    "ignore", category=SparseEfficiencyWarning
)  # qiskit's matrix-exp internals

N_QUBITS = 6  # n qubits = N=12 Majorana (fits belenos-12's 12; sparse SYK keeps the depth feasible)
N_TERMS = (
    12  # sparse-SYK: ~N random 4-Majorana terms (k~1 sparse, not the full C(12,4)=495)
)
PHI0_OVER_MS = 1.40  # the germe's radion displacement (germe_decompression's phi0)
DEPTHS = [0.0, 0.5, 1.0, 2.0, 4.0]  # decompression depths (Trotterized evolution time)
RNG = np.random.default_rng(20260629)


def majorana(k, n):
    """The k-th Majorana (0..2n-1) via Jordan-Wigner, as a SparsePauliOp (a single Pauli string)."""
    qubit, kind = k // 2, k % 2
    lab = ["I"] * n
    for j in range(qubit):
        lab[j] = "Z"
    lab[qubit] = "X" if kind == 0 else "Y"
    return SparsePauliOp(
        "".join(reversed(lab))
    )  # qiskit little-endian: rightmost = qubit 0


def sparse_syk(n, n_terms, rng):
    """H = sum_{a<b<c<d} J_abcd gamma_a gamma_b gamma_c gamma_d (real Gaussian J; Hermitian for q=4 distinct)."""
    n_maj = 2 * n
    quads = set()
    while len(quads) < n_terms:
        quads.add(tuple(sorted(int(x) for x in rng.choice(n_maj, 4, replace=False))))
    h = SparsePauliOp("I" * n, coeffs=[0.0])
    for a, b, c, d in quads:
        term = majorana(a, n) @ majorana(b, n) @ majorana(c, n) @ majorana(d, n)
        h = h + float(rng.standard_normal()) * term
    return h.simplify()


def germe_statevector(n):
    """THE GERME: the radion field wavepacket (peaked at phi0=1.40 M_s) -- germe_decompression's state."""
    dim = 2**n
    k0 = PHI0_OVER_MS / 2.5 * (dim - 1)  # phi/M_s grid in [0, 2.5]
    amp = np.exp(-((np.arange(dim) - k0) ** 2) / 2.0)
    return Statevector(amp / np.linalg.norm(amp))


def decompress(germe_sv, h, t):
    """ENCODE the germe -> DECOMPRESS by e^{-iHt} (Trotterized SYK quench) -> the evolved state."""
    qc = QuantumCircuit(N_QUBITS)
    qc.prepare_state(germe_sv, range(N_QUBITS))
    if t > 0:
        qc.append(PauliEvolutionGate(h, time=t), range(N_QUBITS))
    return Statevector(qc)


def tree_entropy(sv):
    """The TREE: Shannon entropy (bits) of the output distribution -- the germe unfolding into variants."""
    p = np.abs(sv.data) ** 2
    p = p[p > 1e-12]
    return float(-(p * np.log2(p)).sum())


def vn_entropy(rho):
    """von Neumann entropy (nats) of a reduced density matrix -- the RT-like entanglement."""
    ev = np.linalg.eigvalsh(rho.data)
    ev = ev[ev > 1e-12]
    return float(-(ev * np.log(ev)).sum())


def main():
    print("=" * 96)
    print(
        " germe_decompression FOR belenos-12 — the FORWARD germe-decompressor on a SYK (black-hole) substrate"
    )
    print("=" * 96)

    h = sparse_syk(N_QUBITS, N_TERMS, RNG)
    germe = germe_statevector(N_QUBITS)
    half = list(range(N_QUBITS // 2, N_QUBITS))  # the B half (traced out for S_A)
    print(
        f"\n  sparse SYK: N={2*N_QUBITS} Majorana on {N_QUBITS} qubits, {len(h)} Pauli terms (k~1 sparse)"
    )
    print(
        f"  germe: the radion wavepacket (phi0={PHI0_OVER_MS} M_s) -- a LOW-entanglement localized state"
    )

    print(
        "\n[1] DECOMPRESS the germe by the SYK quench -- read the TREE + MATCHED FILTER + ENTANGLEMENT"
    )
    print(
        "    depth t   germe overlap   S_entangle(half)   tree entropy(bits)   (the germe unfolds)"
    )
    overlaps, s_ent, s_tree = [], [], []
    for t in DEPTHS:
        sv = decompress(germe, h, t)
        ov = float(
            np.abs(germe.inner(sv)) ** 2
        )  # MATCHED FILTER: germe-as-reference overlap
        se = vn_entropy(partial_trace(sv, half))  # ENTANGLEMENT (RT-like), nats
        st = tree_entropy(sv)  # TREE: output-distribution entropy
        overlaps.append(ov)
        s_ent.append(se)
        s_tree.append(st)
        print(f"     {t:4.1f}      {ov:8.3f}        {se:8.3f}           {st:8.3f}")

    # CONTROL (anti-pareidolia): a RANDOM input's overlap with the germe -- the germe-as-reference is selective
    rc = RNG.standard_normal(2**N_QUBITS) + 1j * RNG.standard_normal(2**N_QUBITS)
    ctrl_overlap = float(np.abs(germe.inner(Statevector(rc / np.linalg.norm(rc)))) ** 2)

    print(
        "\n[2] WHAT THE READS MEAN (the germe decompresses on the black-hole substrate)"
    )
    print(
        f"    * MATCHED FILTER (germe-as-reference): overlap {overlaps[0]:.2f} (t=0, the germe) -> {min(overlaps):.3f}"
    )
    print(
        "      -- selective on the germe at t=0, DECORRELATES as the SYK scrambles it. CONTROL: a RANDOM"
    )
    print(
        f"      input overlaps the germe at {ctrl_overlap:.3f} ~ 1/dim ({1/2**N_QUBITS:.3f}) -- the germe is the"
    )
    print(
        "      stable, SELECTIVE REFERENCE the decompressor reads against (not pareidolia)."
    )
    print(
        f"    * ENTANGLEMENT (RT-like): S(half) {s_ent[0]:.2f} (low-entanglement germe) -> {max(s_ent):.2f} nat (grows)."
    )
    print(
        f"    * TREE: output entropy {s_tree[0]:.2f} -> {max(s_tree):.2f} bits -- the germe UNFOLDS into the"
    )
    print(
        "      variant distribution (germe_tree_decompressor, here on a real SYK quench, not a toy U)."
    )
    assert (
        overlaps[0] > 0.9
    ), "the matched filter must be selective on the germe at t=0 (germe-as-reference)"
    assert (
        min(overlaps) < overlaps[0] - 0.3
    ), "the germe overlap must decorrelate as the SYK scrambles it"
    assert (
        max(s_ent) > s_ent[0] + 0.3
    ), "the SYK quench must ENTANGLE the germe (the decompression)"
    assert (
        max(s_tree) > s_tree[0] + 0.5
    ), "the germe must UNFOLD into the variant tree (entropy grows)"
    assert (
        ctrl_overlap < overlaps[0] - 0.5
    ), "the germe-as-reference must be SELECTIVE (a random input overlaps it far less than the germe)"

    print(
        "\n[3] VERDICT — a FORWARD germe-decompressor on a real SYK (black-hole) substrate (belenos-12)"
    )
    print(
        "    * ENCODE the germe -> DECOMPRESS by the SYK quench -> READ the tree/entanglement/matched filter."
    )
    print(
        "    * the germe is the STABILIZER/REFERENCE (the matched filter), our toolkit's idea, on real SYK."
    )
    print(
        "    * SCOPE (held): this RUNS a germe-CANDIDATE forward + reads its observables -> it TESTS OBT germe-"
    )
    print(
        "      candidates against the universe (forward), it does NOT derive the germe nor FINALIZE closure"
    )
    print(
        "      (the amount = the IC; measurement reads the input's consequences, it does not invert)."
    )
    print(
        "    * RUN: exact here (Statevector, n=6); the gate circuit is submittable to belenos-12 via"
    )
    print("      OVH/Quandela (Perceval), sampling the same reads (~EUR/campaign).")
    print(
        "\n  COMPUTED + asserted only as sim-correctness (scrambles/entangles/unfolds); no imposed ranges."
    )
    print("=" * 96)


if __name__ == "__main__":
    main()
