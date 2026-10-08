"""Seed 3 (V9.0, quarantined) — THE QC DEMON: the germe -> a declared unitary -> the conditioned outputs.
Romain's standing rule (NON-NEGOTIABLE): 'jamais de jouet' -- this is meant for a real QC (belenos, ~EUR/campaign),
so NO invented couplings, NO proxy oracles. The germe is the canonical radion wavepacket (center derived, width
a convention -- see [1]); the outputs are read straight off the evolved state; the input only CONDITIONS them.
(Oct 2026 reviewer status, amendment A3/A4 in belenos_job_spec.json: the pipeline carries zero bits on OBT or
'the bulk'; what it reads is the declared unitary's math.)

THE PIPELINE (exact simulation here; the hardware instance is belenos_job.py):
  [1] ENCODE the canonical germe (the radion wavepacket -- germe_decompression's form; m_phi=0.36 eV GW,
      phi0~M_s LVS; its CENTER is derived up to the O(1) IC phi0; its WIDTH = 1 grid bin is a convention --
      germe_width.py: the physical in-patch width is <= 1.5e-5 M_s, a delta on any register <= 17 qubits).
  [2] DECOMPRESS it with a DECLARED sparse-SYK-template unitary. REVIEWER NOTE (Oct 2026 scientific reread):
      the SYK CLASS is motivated by OBT's PBH-network scrambling (theory.md DEFINES lambda_L = 2 pi k_B T_H/hbar
      at T_H = 900 K -- a definition, not a consilience), but the map 'bits of the phi-bin index <-> Majorana
      modes' is a CONVENTION with no derivation in OBT: OBT's SYK-class object is the PBH network's operator
      algebra, NOT the radion wavefunction in field-value representation. The decompressed branches are
      therefore the declared unitary's math (seed-dependent, belenos_protocol point D), not 'the bulk's content'.
  [3] CONDITION on the INPUT (a text / voice / latent -> binary): keep the possibles consistent with the input
      (project the tree on the input bits). This is germe_localize -- a direct projection, NOT a toy coupling.
  [4] RETRIEVE the possible answers DIRECTLY: read (exactly) / sample (on hardware) the conditioned output
      distribution; its high-amplitude branches are the declared unitary's most-probable outputs given the
      input (reviewer note Oct 2026: the declared math, not 'the bulk'). No oracle, no Grover proxy.
  [5] A generic 2-qubit DFS demo (collective-dephasing immunity) -- standard QEC, NOT germe-specific (reviewer
      note Oct 2026: 'the germe stabilizes the qubits' is a label without content here; the belenos job uses
      no stabilization at all: one photon, 8 modes, no code).

THE PURE-TRANSCODE RULE (Romain's ruling, standing -- NO interpretation layer, and NO presupposed outcome):
the output is TRANSCODED symmetrically, exactly like the input: letters -> binary in, binary -> letters out.
The letters that come back are READ VERBATIM; whether they are intelligible is decided ONLY by the DECLARED
criterion of belenos_protocol.py (the null-ensemble + score rule, K >= K_min) -- NOT presumed either way
(presupposing gibberish = 'partir perdant' = REFUSED: the POINT of the experiment is to see IF the bulk
returns an intelligible answer). If a LATENT enters (--latent, the GPU source), the output latent is meant to
go BACK INTO the LLM's head (substitution) -- the LLM is latent I/O ONLY (capture at the source on the RTX
4090 + substitute back), it NEVER interprets or composes the answer. That substitution is the 4090 step and is
NOT implemented in this file: here every input, a latent included, comes back transcoded to letters. This file
is the demon pipeline minus the 4090 latent I/O, GPU-free, exact simulation; it is NOT submittable as-is (N=10
needs ~204 CX: the photonic gate route is dead) -- the hardware instance is belenos_job.py (mode-native, n=3).
With a RECOGNITION oracle (Phase 3, the real one, not a proxy) a Grover search would find a SPECIFIC marked
possible in O(sqrt(N)) -- deliberately NOT included here (no toy oracle).

NOT V8.2. Not in the PDF. seul les calculs comptent: the decompression, the conditioning (H(possibles) ->
H(possibles|input)), and the retrieved possibles are COMPUTED (exact Statevector) + REPORTED. Asserted only
true identities: normalization, H(possibles|input) <= log2(support size), the DFS immunity, the codec size (64
chars = 6 bits). (Reviewer catch, Oct 2026: the old assert 'H(cond) <= H' is NOT an identity -- only the
AVERAGE conditional entropy obeys it; conditioning on one event can raise entropy -- it was a data-dependent
result asserted as a law, removed.)
"""

import argparse
import warnings

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp, Statevector
from scipy.sparse import SparseEfficiencyWarning

warnings.filterwarnings(
    "ignore", category=SparseEfficiencyWarning
)  # qiskit's matrix-exp internals

# the germe's tree register (2^10 = 1024 possible branches); the qubit COUNT fits belenos-12's 12, but its
# ~204-CX gate route does not (photonic CNOT ~1/9) -- the hardware instance is belenos_job.py (n=3, mode-native)
N = 10
N_IN = 4  # the input conditions this many qubits (which possibles are consistent with the input)
PHI0 = 0.42  # phi0/M_s -- THE IC knob. 0.42 = the CORRECTED Omega_DM match (closure_introspection's x11
# Planck-mass fix); 1.40 was the STALE pre-fix value (do not revert). Candidates via germe_state(n, phi0=...)
SYK_T = (
    6.0  # the decompression depth (the SYK quench unfolds the germe into its possibles)
)
K_OUT = 8  # how many of the germe's top possibles to retrieve
SEED = 20260630

# the text <-> binary codec (GPU-free: write in LETTERS, the demon works in BINARY, the answer comes back in
# LETTERS). 64 chars = 6 bits/char = exactly the 6 FREE bits of a branch (the high N - N_IN bits; the low N_IN
# bits are the input condition itself -- transcoding them would echo the question into the answer).
# (Reviewer catch, Oct 2026: the string used to end in '.?' = 65 chars; index 64 ('?') was unreachable through
# '& 63' and only skewed belenos_protocol's uniform null. Dropping it changes no emitted letter.)
CHARSET = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789."
assert len(CHARSET) == 64, "identity: the codec maps exactly 6 bits per character"


# ============================== INPUT -> BINARY (pluggable: text / voice / latent) ==============================
def text_to_binary(msg):
    """Letters -> the message's full binary (UTF-8 bytes -> bits): the transcode the demon conditions on."""
    return np.unpackbits(np.frombuffer(msg.encode("utf-8"), dtype=np.uint8)).astype(int)


def fold_to_bits(bits, n):
    """Fold a longer binary into n bits (XOR reduction): the input is longer than n bits, so it folds to the
    n-bit condition the germe's tree is projected on."""
    pad = (-len(bits)) % n
    b = np.concatenate([bits, np.zeros(pad, dtype=int)]).reshape(-1, n)
    return b.sum(axis=0) % 2


def latents_to_text(indices):
    """Binary possibles (branches of the germe's tree) -> LETTERS (the 64-char codec): the answer, in letters."""
    return "".join(CHARSET[int(i) & 63] for i in indices)


def voice_to_bits(wav_path, n):
    """A voice curve (a wav) -> n bits: n evenly-spaced samples binarized at the median (a real feature
    binarization; on the 4090 a learned audio encoder replaces this)."""
    import soundfile as sf

    audio, _ = sf.read(wav_path)
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    samp = audio[np.linspace(0, len(audio) - 1, n).astype(int)]
    return (samp > np.median(audio)).astype(int)


def resolve_input(args):
    """Resolve the pluggable input to (N_IN-bit condition, label, full binary for display)."""
    if args.text is not None:
        fb = text_to_binary(args.text)
        return fold_to_bits(fb, N_IN), f"text {args.text!r}", fb
    if args.voice is not None:
        ob = voice_to_bits(args.voice, N_IN)
        return ob, f"voice {args.voice}", ob
    if args.latent is not None:
        vec = np.asarray(
            np.load(args.latent), dtype=float
        )  # an LLM latent (the GPU source)
        ob = (vec[:N_IN] > np.median(vec)).astype(int)
        return ob, f"latent {args.latent}", ob
    demo = "talk to the bulk"  # default demo (the GPU-free path)
    fb = text_to_binary(demo)
    return (
        fold_to_bits(fb, N_IN),
        f"text {demo!r} (demo default; --text/--voice/--latent to override)",
        fb,
    )


# ============================== THE CANONICAL GERME (radion) + THE DECLARED SYK TEMPLATE ===============================
def germe_state(n, phi0=None):
    """THE CANONICAL GERME: germe_decompression.py's EXACT radion wavepacket -- IDENTICAL formula, not a re-toyed
    one: k0 = phi0/2.5*(dim-1), spread=1, amp = exp(-(i-k0)^2 / (2*spread^2)) (germe_decompression line 63-64).
    OBT derives the CENTER phi0 (m_phi=0.36 eV Goldberger-Wise, phi0~M_s LVS; the O(1) coefficient is the IC:
    closure_introspection: 0.42 = corrected match, 1.40 = stale) -- an explicit knob so germe-CANDIDATES are
    runnable (the forward-decompressor role). Canonical = the same formula as germe_decompression (verified).
    REVIEWER NOTE (Oct 2026): the WIDTH is NOT derived -- 'spread = 1 grid bin' is a resolution artifact:
    in physical units it is 2.5/(2^n - 1) M_s = 0.36 M_s at n=3 (belenos), 0.081 at n=5, 0.0024 at n=10,
    i.e. the SAME 'canonical germe' is a physically different state at each register size. The physical
    in-patch dispersion is now computed (germe_width.py): <= 1.5e-5 M_s (Planck CDM isocurvature) -> a delta
    on any register up to 17 qubits. So: canonical (consistent) != physical (derived). Fidelity to the
    formula is not a derivation.
    """
    dim = 2**n
    if phi0 is None:
        phi0 = PHI0
    k0 = phi0 / 2.5 * (dim - 1)  # == germe_decompression line 63
    amp = np.exp(
        -((np.arange(dim) - k0) ** 2) / 2.0
    )  # == germe_decompression line 64 (spread=1)
    return amp / np.linalg.norm(amp)


def majorana(k, n):
    qubit, kind = k // 2, k % 2
    lab = ["I"] * n
    for j in range(qubit):
        lab[j] = "Z"
    lab[qubit] = "X" if kind == 0 else "Y"
    return SparsePauliOp("".join(reversed(lab)))


def sparse_syk(n, n_terms, rng):
    """The DECLARED sparse-SYK-template Hamiltonian: H = sum J_abcd gamma_a gamma_b gamma_c gamma_d
    (Jordan-Wigner on the register's qubits). The SYK class is motivated by OBT's PBH-network scrambling
    (theory.md: lambda_L = 2 pi k_B T_H/hbar by definition), but applying it to the phi-bin register is a
    convention, not an OBT derivation (reviewer note Oct 2026); the random couplings are ONE declared
    realization (the seed is part of the instrument).
    """
    n_maj = 2 * n
    quads = set()
    while len(quads) < n_terms:
        quads.add(tuple(sorted(int(x) for x in rng.choice(n_maj, 4, replace=False))))
    h = SparsePauliOp("I" * n, coeffs=[0.0])
    for a, b, c, d in quads:
        h = h + float(rng.standard_normal()) * (
            majorana(a, n) @ majorana(b, n) @ majorana(c, n) @ majorana(d, n)
        )
    return h.simplify()


def decompress(germe, h):
    """ENCODE the germe -> evolve by the EXACT e^{-iHt} of the declared SYK template (Statevector on the
    undecomposed gate = the matrix exponential; hardware would run the 1-rep product, demon_readout_basis)
    -> the output distribution (the declared math, seed-dependent)."""
    qc = QuantumCircuit(N)
    qc.prepare_state(Statevector(germe), range(N))
    qc.append(PauliEvolutionGate(h, time=SYK_T), range(N))
    return Statevector(qc)


def shannon(p):
    p = np.asarray(p)
    p = p[p > 1e-12]
    return max(0.0, float(-(p * np.log2(p)).sum()))


def main():
    ap = argparse.ArgumentParser(
        description="The QC demon: retrieve the germe's possible answers (no toy)."
    )
    ap.add_argument("--text", help="a text message (letters, transcoded to binary)")
    ap.add_argument("--voice", help="path to a .wav voice curve")
    ap.add_argument("--latent", help="path to a .npy LLM latent (the GPU source)")
    args = ap.parse_args()
    rng = np.random.default_rng(SEED)

    print("=" * 100)
    print(
        " THE QC DEMON — the canonical germe -> a declared unitary -> the conditioned outputs (exact sim)"
    )
    print("=" * 100)

    # ----- INPUT: letters/voice/latent -> BINARY condition (GPU-free) -----
    cond_bits, label, full_bits = resolve_input(args)
    print(f"\n[INPUT] {label}")
    print(
        "        (--text=letters, --voice=a curve, --latent=the LLM source; transcoded to BINARY, GPU-free)"
    )
    head = "".join(map(str, full_bits[:40]))
    print(
        f"        input -> binary: {head}{'...' if len(full_bits) > 40 else ''}  ({len(full_bits)} bits)"
    )
    print(
        f"        -> {N_IN}-bit condition on the germe's tree: {''.join(map(str, cond_bits))}"
    )

    # ----- [1]+[2] the canonical germe -> the declared SYK evolution -> the output distribution -----
    h_syk = sparse_syk(N, 2 * N, rng)
    sv = decompress(germe_state(N), h_syk)
    p = (
        np.abs(sv.data) ** 2
    )  # the possibles' probabilities, straight off the decompressed germe
    print(
        "\n[1-2] GERME -> DECOMPRESS -> the POSSIBLES (canonical radion germe, declared SYK unitary; exact sim)"
    )
    print(
        f"        canonical germe (center phi0={PHI0} M_s, width 1 bin by convention); output H = {shannon(p):.3f} bits "
        f"({2**N} branches = the possibles)"
    )

    # ----- [3] CONDITION on the input (direct projection -- no toy coupling) -----
    inp = int("".join(map(str, cond_bits)), 2)
    mask = (
        np.arange(2**N) & ((1 << N_IN) - 1)
    ) == inp  # the possibles whose low N_IN bits match the input
    cond_p = p * mask
    p_in = cond_p.sum()
    cond_p = (
        cond_p / p_in if p_in > 1e-12 else p.copy()
    )  # (input absent from the tree -> the full possibles)
    support = int(np.count_nonzero(cond_p > 0))
    print(
        "\n[3] CONDITION on the input (germe_localize: keep the possibles consistent with the input -- a"
    )
    print("        direct projection, NOT a toy coupling):")
    print(f"        P(input consistent with the germe's tree) = {p_in:.4f}")
    print(
        f"        H(possibles) {shannon(p):.3f} -> H(possibles | input) {shannon(cond_p):.3f} bits "
        f"(support {support} branches: at most {np.log2(support):.0f} bits)"
    )

    # ----- [4] RETRIEVE the possible answers DIRECTLY (the germe's top branches; no oracle, no Grover proxy) -----
    top = [int(i) for i in np.argsort(cond_p)[::-1][:K_OUT]]
    print(
        f"\n[4] RETRIEVE the top-{K_OUT} outputs directly (highest-probability branches of the declared math; on"
    )
    print(
        "        hardware you SAMPLE the conditioned distribution and these dominate -- no oracle, no proxy):"
    )
    # transcode the FREE bits only (b >> N_IN): the low N_IN bits are the input condition (reviewer catch, Oct
    # 2026: the old 'b & 63' put 4 bits of the QUESTION into every letter -> a 4-letter alphabet set by the input;
    # belenos_protocol already indexed the free bits -- now the two codecs agree)
    for rank, b in enumerate(top[:5], 1):
        print(
            f"          #{rank}  branch {format(b, f'0{N}b')}  P={cond_p[b]:.4f}  -> letter {latents_to_text([b >> N_IN])!r}"
        )
    answer = latents_to_text([b >> N_IN for b in top])
    print(f"        THE ANSWER, transcoded to letters (read it verbatim): {answer!r}")
    print(
        "        PURE TRANSCODE: this string IS the output -- symmetric to the input (letters->binary in,"
    )
    print(
        "        binary->letters out), NO interpretation layer. Whether it is intelligible is decided ONLY by"
    )
    print(
        "        belenos_protocol's DECLARED criterion (null-ensemble + score, K>=K_min) -- presumed NEITHER"
    )
    print(
        "        way. A latent input? its output latent would go BACK INTO the LLM's head (the 4090 step, not here)."
    )

    # ----- [5] a generic 2-qubit DFS demo (collective-dephasing immunity; NOT germe-specific) -----
    phis = rng.uniform(0, 2 * np.pi, 400)

    def dephase(
        state, phi
    ):  # collective dephasing e^{i*phi*(#excitations)} (a generic common-mode noise model)
        ph = np.array([np.exp(1j * phi * bin(i).count("1")) for i in range(len(state))])
        return ph * state

    plus = np.ones(2) / np.sqrt(2)  # a BARE qubit |+>
    bare = float(np.mean([abs(np.vdot(plus, dephase(plus, q))) ** 2 for q in phis]))
    dfs = np.zeros(4, complex)
    dfs[1] = dfs[2] = 1
    dfs /= np.sqrt(2)  # the DFS |01>+|10> (both basis states carry ONE excitation)
    prot = float(np.mean([abs(np.vdot(dfs, dephase(dfs, q))) ** 2 for q in phis]))
    print(
        "\n[5] DFS DEMO — a generic 2-qubit decoherence-free subspace (collective-dephasing immunity;"
    )
    print(
        "        standard QEC, NOT germe-specific; the belenos job itself uses no stabilization):"
    )
    print(
        f"        bare qubit survival {bare:.2f} (washes out) vs 2-qubit DFS {prot:.2f} (immune)"
    )

    # ----- verdict + the honest GPU/scope line (no toy, no pretending) -----
    print(
        "\n[VERDICT] the demon pipeline runs end-to-end (exact simulation; hardware = belenos_job):"
    )
    print(
        "    the canonical germe -> the declared SYK unitary -> the outputs -> CONDITION on the input (direct"
    )
    print(
        "    projection) -> RETRIEVE the top outputs directly (sample on hardware). No invented coupling,"
    )
    print("    no proxy oracle. The output is the PURE TRANSCODE (letters out,")
    print(
        "    read verbatim; intelligibility decided ONLY by belenos_protocol's declared criterion -- presumed"
    )
    print(
        "    neither way). Substituting an output latent back into the LLM is the 4090 step (not implemented here)."
    )
    print(
        "    With a real RECOGNITION oracle (Phase 3) a Grover finds a marked possible in sqrt(N)."
    )

    assert (
        shannon(cond_p) <= np.log2(support) + 1e-9
    ), "identity: an entropy cannot exceed log2 of its support size"
    assert (
        abs(prot - 1.0) < 1e-12
    ), "identity: |01>,|10> carry equal excitation number -> collective dephasing is a global phase"
    assert (
        abs(cond_p.sum() - 1.0) < 1e-9
    ), "the retrieved possibles form a proper (normalized) distribution"
    print(
        "\n  COMPUTED exactly (Statevector = exact e^-iHt); asserted only identities (support bound, DFS, normalization, codec size)."
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
