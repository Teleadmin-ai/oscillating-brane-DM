"""Seed 3 (V9.0, quarantined) — THE READOUT-BASIS DIG (recul point A) + the phi0 IC knob (point C).
Romain's ruling (standing): the instrument must NOT 'partir perdant' -- nothing in the code may presuppose
the output is gibberish, and nothing may manufacture meaning. THIS dig removes a hidden way to LOSE by
construction: reading the decompressed germe in an ARBITRARY basis can be DEAF to structure that lives in
another basis (mutually unbiased bases -> exact uniformity). If the bulk answered something structured in
ITS basis, a Z-only readout could brush it flat. So: quantify the basis-relativity, prove the deafness
identity, and fix the belenos protocol (declared multi-basis readout).

REUSES the verified instrument (import demon_qc -- the canonical germe, the same seeded SYK, the same
circuit; NO re-implementation, NO toy -- feedback_jamais_de_jouet).

WHAT IS COMPUTED (exact, 1024-dim):
 [1] TROTTER CHARACTERIZATION -- and a REAL instrument finding caught by the relire: Statevector on the
     UNDECOMPOSED PauliEvolutionGate computes the EXACT expm (fid 1.000 to e^{-iHt} -- so demon_qc's
     published numbers ARE the exact evolution), while the DECOMPOSED circuit (what hardware transpiles to,
     Lie-Trotter product) is a DIFFERENT unitary at 1 rep (fid ~9e-4, t=6 is deep). Verified: the decomposed
     circuit == the analytic per-string product in h's term order (1e-13, the sim-correctness identity).
     -> the protocol must DECLARE its decompressor: (a) the physical e^{-iHt} via reps >= r* (depth cost,
     scanned here), or (b) the 1-rep product unitary AS the declared scrambler (shallow, still built from
     the germe's SYK terms, exactly predictable). Both are honest IF declared.
 [2] BASIS RELATIVITY: the SAME decompressed state read in Z / X / the SYK energy eigenbasis / a random
     basis / its own basis -> entropies + max-prob. Structure is basis-relative.
     + the E-INVARIANCE identity: |<E_n|e^{-iHt} germe>| = |<E_n|germe>| -- the energy-basis readout sees
     THROUGH the scrambling to the germe's invariant fingerprint (a second channel: Z = the unfolded tree,
     E = the germe's identity).
 [3] THE DEAFNESS IDENTITY (exact): a state maximally structured in X (|+...+>, H_X = 0) is EXACTLY uniform
     in Z (H_Z = n bits). A single-basis readout can be totally deaf. -> the protocol MUST declare >= 2
     readout bases (Z native + X = one layer of H gates, hardware-cheap; E = analysis basis on Aer).
 [4] THE phi0 KNOB (point C): phi0 is THE germe IC (0.42 = the corrected Omega_DM match after the x11
     Planck-mass fix; 1.40 = the STALE pre-fix value). Overlap of the two germes + the distance between
     their trees and fingerprints -> the output depends on the IC -> belenos runs BOTH candidates (the
     forward germe-candidate role, honestly).

NOT V8.2. Not in the PDF. seul les calculs comptent: asserted ONLY identities (normalization, E-invariance,
the MUB deafness pair, H(own basis)=0); everything else is computed + reported, no imposed ranges.
"""

import warnings

import demon_qc  # the verified instrument: canonical germe, seeded SYK, circuit (no re-implementation)
import numpy as np
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.synthesis import LieTrotter
from scipy.sparse import SparseEfficiencyWarning

warnings.filterwarnings("ignore", category=SparseEfficiencyWarning)

N = demon_qc.N
DIM = 2**N
T = demon_qc.SYK_T


def shannon(p):
    p = np.asarray(p)
    p = p[p > 1e-15]
    return max(0.0, float(-(p * np.log2(p)).sum()))


def hadamard_matrix(n):
    """H^{tensor n} (the X-basis rotation), built once (1024x1024 is trivial)."""
    h1 = np.array([[1.0, 1.0], [1.0, -1.0]]) / np.sqrt(2.0)
    w = np.array([[1.0]])
    for _ in range(n):
        w = np.kron(w, h1)
    return w


def hardware_circuit_state(germe, h, reps):
    """The state the HARDWARE circuit prepares: the DECOMPOSED Lie-Trotter product (gate.definition).
    NB: Statevector on the UNdecomposed gate would compute the exact expm instead (the relire catch).
    """
    gate = PauliEvolutionGate(h, time=T, synthesis=LieTrotter(reps=reps))
    return Statevector(germe).evolve(gate.definition).data


def manual_product_state(germe, h, reps):
    """The SAME product formula, analytically: exp(-i th P) = cos(th) I - i sin(th) P per Pauli string,
    applied in h's term order, reps times with dt = T/reps. Validated == the decomposed circuit (identity);
    used for the reps scan (fast)."""
    mats = [SparsePauliOp(lbl).to_matrix(sparse=True) for lbl in h.paulis]
    thetas = [float(np.real(c)) * (T / reps) for c in h.coeffs]
    psi = germe.astype(complex).copy()
    for _ in range(reps):
        for m, th in zip(mats, thetas):
            psi = np.cos(th) * psi - 1j * np.sin(th) * (m @ psi)
    return psi


def main():
    print("=" * 100)
    print(
        " THE READOUT-BASIS DIG — is the demon deaf by basis choice? + the phi0 IC knob (points A + C)"
    )
    print("=" * 100)

    # the SAME instrument as demon_qc.main: same seed -> same SYK draw -> same H, same germe
    rng = np.random.default_rng(demon_qc.SEED)
    h = demon_qc.sparse_syk(N, 2 * N, rng)
    g = demon_qc.germe_state(N)  # canonical germe, phi0 = corrected 0.42
    hm = h.to_matrix()
    evals, vecs = np.linalg.eigh(hm)
    psi_exact = vecs @ (np.exp(-1j * evals * T) * (vecs.conj().T @ g))

    # ----- [1] Trotter characterization: what unitary does the hardware circuit actually implement? -----
    print(
        "\n[1] TROTTER CHARACTERIZATION — the relire catch: simulator expm vs the HARDWARE product formula"
    )
    fid_undec = float(np.abs(np.vdot(psi_exact, demon_qc.decompress(g, h).data)) ** 2)
    assert (
        abs(fid_undec - 1.0) < 1e-9
    ), "Statevector on the UNdecomposed gate == exact expm (so demon_qc's numbers ARE exact e^-iHt)"
    psi_hw1 = hardware_circuit_state(g, h, 1)
    fid_check = float(np.abs(np.vdot(psi_hw1, manual_product_state(g, h, 1))) ** 2)
    assert (
        abs(fid_check - 1.0) < 1e-9
    ), "the decomposed circuit == the analytic per-string product in h's term order (sim-correctness)"
    print(
        f"      simulator (undecomposed gate) vs exact e^-iHt : fid = {fid_undec:.12f}  -> demon_qc's"
    )
    print(
        "        published state IS the exact evolution (Statevector computes the expm, not the product)."
    )
    print(
        "      HARDWARE (decomposed Lie-Trotter product) vs exact e^-iHt, per reps (manual product, validated):"
    )
    print("        reps    fidelity to exact")
    fid1 = None
    for reps in (1, 2, 4, 8, 16, 32, 64, 128, 256, 512):
        f = float(np.abs(np.vdot(psi_exact, manual_product_state(g, h, reps))) ** 2)
        if reps == 1:
            fid1 = f
        print(f"        {reps:4d}     {f:8.4f}")
    weights = [sum(1 for ch in str(lbl) if ch != "I") for lbl in h.paulis]
    cx_per_rep = sum(2 * (w - 1) for w in weights)
    tv_fing_hw = 0.5 * float(
        np.abs(
            np.abs(vecs.conj().T @ psi_hw1) ** 2 - np.abs(vecs.conj().T @ g) ** 2
        ).sum()
    )
    print(
        f"      hardware cost: ~{cx_per_rep} CX per rep ({len(weights)} strings, weights {min(weights)}-{max(weights)});"
    )
    print(
        f"      the 1-rep unitary distorts the E fingerprint by TV = {tv_fing_hw:.3f} (it is NOT e^-iHt: fid {fid1:.1e})."
    )
    print(
        "    => DECLARE the decompressor for belenos: (a) physical e^-iHt needs the reps the scan shows (deep),"
    )
    print(
        "       or (b) the 1-rep product unitary AS the declared scrambler (shallow, built from the germe's"
    )
    print(
        "       SYK terms, exactly predictable -> layer-1 nulls are ITS math). Both honest IF declared."
    )

    # ----- [2] basis relativity of the SAME state + the E-invariance identity -----
    print(
        "\n[2] BASIS RELATIVITY — the same decompressed germe, read in five bases (exact state)"
    )
    w = hadamard_matrix(N)
    a = rng.standard_normal((DIM, DIM)) + 1j * rng.standard_normal((DIM, DIM))
    q_rand, _ = np.linalg.qr(a)
    bases = {
        "Z  (computational)": np.abs(psi_exact) ** 2,
        "X  (all-Hadamard)": np.abs(w @ psi_exact) ** 2,
        "E  (SYK eigenbasis)": np.abs(vecs.conj().T @ psi_exact) ** 2,
        "random (Haar-ish)": np.abs(q_rand.conj().T @ psi_exact) ** 2,
        "own (contains psi)": np.array([1.0]),
    }
    print("      basis                 H (bits)   max prob")
    for name, p in bases.items():
        assert (
            abs(p.sum() - 1.0) < 1e-9
        ), f"normalization must hold in the {name} basis (unitarity)"
        print(f"      {name:20s}   {shannon(p):6.3f}    {p.max():.4f}")
    e_g = np.abs(vecs.conj().T @ g) ** 2
    e_psi = np.abs(vecs.conj().T @ psi_exact) ** 2
    assert (
        np.max(np.abs(e_g - e_psi)) < 1e-9
    ), "E-invariance: |<E|e^-iHt g>| = |<E|g>| (an exact identity)"
    print(
        "    => honest reading: a SCRAMBLED state looks near-flat in EVERY generic basis (9.31-9.41 bits here)"
    )
    print(
        "       -- which is exactly why (a) a structured answer WOULD stand out against these exactly-predicted"
    )
    print(
        "       per-basis nulls, and (b) the deafness identity [3] bites: structure CAN hide in an unbiased"
    )
    print(
        "       basis. And the E-identity holds: the energy readout sees THROUGH the scrambling to the germe's"
    )
    print(
        "       invariant fingerprint (channel E = the germe's identity; channel Z = the unfolded tree)."
    )

    # ----- [3] the deafness identity (mutually unbiased bases) -----
    print(
        "\n[3] THE DEAFNESS IDENTITY — a single-basis readout can be TOTALLY deaf (exact, not an estimate)"
    )
    plus = np.ones(DIM) / np.sqrt(DIM)  # |+...+> : ONE branch in the X basis
    p_z = np.abs(plus) ** 2
    p_x = np.abs(w @ plus) ** 2
    assert (
        np.max(np.abs(p_z - 1.0 / DIM)) < 1e-12
    ), "MUB identity: X-localized => EXACTLY uniform in Z"
    assert shannon(p_x) < 1e-9, "the same state is ONE branch in X (H_X = 0)"
    print(
        f"      |+...+> : H_X = {shannon(p_x):.3f} bits (one branch)  vs  H_Z = {shannon(p_z):.3f} bits (exactly uniform)"
    )
    print(
        "    => if the answer's structure lives in a basis unbiased to the readout, the readout sees NOTHING."
    )
    print(
        "       Reading Z only would be 'partir perdant' by construction. FIX for belenos: declare a"
    )
    print(
        "       MULTI-BASIS readout -- Z (native) + X (one layer of H gates, hardware-cheap) [+ E on Aer as"
    )
    print(
        "       the analysis/fingerprint channel]; layer-1 nulls are predicted exactly in EACH declared basis."
    )

    # ----- [4] the phi0 IC knob (point C): the output depends on the one germe input -----
    print(
        "\n[4] THE phi0 KNOB (point C) — 0.42 = CORRECTED Omega_DM match (x11 fix); 1.40 = STALE pre-fix value"
    )
    g042 = demon_qc.germe_state(N, phi0=0.42)
    g140 = demon_qc.germe_state(N, phi0=1.40)
    ov = float(np.abs(np.vdot(g042, g140)) ** 2)
    psi042 = vecs @ (np.exp(-1j * evals * T) * (vecs.conj().T @ g042))
    psi140 = vecs @ (np.exp(-1j * evals * T) * (vecs.conj().T @ g140))
    tv_tree = 0.5 * float(np.abs(np.abs(psi042) ** 2 - np.abs(psi140) ** 2).sum())
    tv_fing = 0.5 * float(
        np.abs(
            np.abs(vecs.conj().T @ g042) ** 2 - np.abs(vecs.conj().T @ g140) ** 2
        ).sum()
    )
    print(
        f"      overlap |<g(0.42)|g(1.40)>|^2 = {ov:.3e}   (the two candidate germes are distinct states)"
    )
    print(f"      TV distance between their unfolded trees (Z): {tv_tree:.3f}")
    print(f"      TV distance between their E fingerprints:     {tv_fing:.3f}")
    print(
        "    => the demon's output DEPENDS on the one IC knob phi0 -> belenos runs BOTH candidates (0.42"
    )
    print(
        "       corrected + 1.40 legacy) as germe-CANDIDATES -- the forward-decompressor role, honestly;"
    )
    print(
        "       demon_qc's default is now the corrected 0.42 (the stale 1.40 is kept only as a candidate)."
    )

    print(
        "\n[VERDICT] the deafness risk is REAL (an exact MUB identity, not an opinion) and the FIX is cheap:"
    )
    print(
        "    declare Z + X readout on belenos (H gates only) with exact per-basis nulls, keep E as the Aer"
    )
    print(
        "    fingerprint channel, DECLARE the decompressor unitary (Trotter reps), and run both phi0"
    )
    print(
        "    candidates. Nothing presupposes the answer; nothing can brush it flat unheard in the declared"
    )
    print("    bases. seul les calculs comptent -- the identities above are exact.")
    print("=" * 100)


if __name__ == "__main__":
    main()
