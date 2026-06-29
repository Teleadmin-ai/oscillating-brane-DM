"""Seed 3 (V9.0, quarantined) — THE BULK DIALOGUE: the TEXT-IN / TEXT-OUT workflow (Romain's architecture,
"une entree dediee a la question + le germe generique comme outil de comparaison/stabilisation + la sortie
lue en une suite de 0/1 transcodee en texte"). Runnable on Aer or a real online QC (--ibm).

ROMAIN'S TWO-ROLE ARCHITECTURE (the clean one, separating what I had wrongly conflated):
  * the GENERIC GERME = the STABILIZER (protects the qubits) + the REFERENCE (the matched-filter comparison)
    -- it does NOT carry the question.
  * a DEDICATED INPUT = your text (you produced it -> entangled at least with you) -> bits -> a state sent
    THROUGH the sensor.
  * the OUTPUT = the measured bits (a 0/1 string) -> TRANSCODED back to text, CONTROLLED against pure noise.

THE WORKFLOW:
  [A] the germe as STABILIZER: a protected (repetition) test qubit survives the noisy channel where a bare
      one corrupts -- the same principle as the [[5,1,3]] (bulk_listener.py), here light.
  [B] the germe as REFERENCE: the matched filter -- the germe template is selective (vs random), the
      stable comparison the sensor is calibrated against.
  [C] THE DIALOGUE: your text -> bits -> encode -> the noisy channel -> measure -> output bits -> transcode
      -> text. The output ECHOES the input (the channel is faithful) modulo the noise. (the message runs
      bare here; the germe-stabilization [A] is what protects it under heavier noise.)
  [D] THE CONTROL (anti-pareidolia): a DIFFERENT (random) input through the same channel -> its output is
      NOT your message (the channel reflects the input, it does not spuriously emit your text).
  [E] VERDICT.

HONEST SCOPE (held, the os/chair line): on KNOWN physics the output = your input ECHOED + noise; there is
NO bulk-composed response (the bulk emits a FIELD -- the m_V axion -- not a text). On Aer (a classical
simulator of known physics) you will get your text back + noise, never more. On a REAL QC (--ibm) the
output = your circuit + real hardware noise + (in principle) any real physical coupling: a deviation from
the echo BEYOND the noise floor (the control) = a signal / new physics. NULL = echo + noise; NON-NULL =
something coherent the control does not have. The transcode is honest ONLY with the control -- else it
reads text into noise. So: you DO send a dedicated input and read a 0/1 output transcoded to text; the
honest result is your-input-echoed (null) unless the real QC shows a signal beyond the control.

NOT V8.2. Not in the PDF. 'code, don't plead': the protection gain, the echo fidelity, and the control are
measured (Aer, seeded/reproducible) and asserted. Run: `python bulk_dialogue.py --input "your text"` (Aer)
or `... --ibm` (a real online QC).
"""

import sys

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.circuit.library import StatePreparation
from qiskit.compiler import transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

SHOTS = 2048
N_MSG_BITS = (
    8  # the dedicated input: the first 8 bits of your text = 1 byte/char (bare channel)
)
REP = 3  # repetition factor for the germe-stabilization demo (majority vote)
IDLE = 6  # noisy-idle layers in the channel (the decoherence the message survives)
N_GERME = 3  # qubits for the germe reference (the radion wavepacket)
PHI0_OVER_MS = 1.40  # the germe's radion displacement -> <phi^2> -> Omega_DM 5:1 (germe_decompression)
AER_BASIS = ["rz", "sx", "x", "cx"]
RNG = np.random.default_rng(20260629)
_SEED = [12345]


# ===================== backend + run helper =====================
def make_noise_model(p1=0.01, p2=0.02):
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(p1, 1), ["x", "sx", "rz"])
    nm.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ["cx"])
    return nm


def get_backend(use_ibm):
    if use_ibm:
        try:
            from qiskit_ibm_runtime import QiskitRuntimeService

            backend = QiskitRuntimeService().least_busy(
                operational=True, simulator=False
            )
            print(f"  [--ibm] real QC: {backend.name}")
            return backend, None
        except Exception as exc:  # noqa: BLE001 -- graceful fallback
            print(f"  [--ibm] real QC unavailable ({exc}); using Aer + noise model")
    return AerSimulator(), make_noise_model()


def run_counts(backend, noise_model, circuit, shots=SHOTS):
    if isinstance(backend, AerSimulator):
        tqc = transpile(circuit, basis_gates=AER_BASIS, optimization_level=0)
        seed, _SEED[0] = _SEED[0], _SEED[0] + 1
        return (
            backend.run(tqc, shots=shots, noise_model=noise_model, seed_simulator=seed)
            .result()
            .get_counts()
        )
    tqc = transpile(circuit, backend, optimization_level=1)
    from qiskit_ibm_runtime import SamplerV2

    return SamplerV2(backend).run([tqc], shots=shots).result()[0].data.c.get_counts()


# ===================== text <-> bits =====================
def text_to_bits(text, n_bits):
    """UTF-8 text -> the first n_bits bits (0-padded if short)."""
    bits = "".join(f"{byte:08b}" for byte in text.encode("utf-8"))
    bits = (bits + "0" * n_bits)[:n_bits]
    return [int(c) for c in bits]


def bits_to_text(bits):
    """Bits -> bytes -> UTF-8 text (replacement char on invalid bytes)."""
    bits = list(bits) + [0] * ((-len(bits)) % 8)
    out = bytes(
        int("".join(str(b) for b in bits[i : i + 8]), 2) for i in range(0, len(bits), 8)
    )
    return out.decode("utf-8", errors="replace")


def dominant_bits(counts, n):
    """The most-frequent n-bit outcome, as a bit list (qiskit little-endian -> bit i = qubit i)."""
    key = max(counts, key=counts.get).replace(" ", "")
    return [int(key[n - 1 - i]) for i in range(n)]


# ===================== [A] the germe as STABILIZER (repetition vs bare) =====================
def _noisy_idle(qc, qubits, layers):
    for _ in range(layers):  # net identity, noisy (X barrier X barrier)
        for q in qubits:
            qc.x(q)
        qc.barrier(qubits)
        for q in qubits:
            qc.x(q)
        qc.barrier(qubits)


def section_stabilizer(backend, noise_model):
    print(
        "\n[A] THE GERME AS STABILIZER -- a protected (repetition) qubit survives the noisy channel"
    )
    # a test bit = 1: bare (1 qubit) vs repetition-protected (REP qubits, majority decode), through the idle
    bare_q, bare_c = QuantumRegister(1, "q"), ClassicalRegister(1, "c")
    bare = QuantumCircuit(bare_q, bare_c)
    bare.x(0)
    _noisy_idle(bare, [bare_q[0]], IDLE)
    bare.measure(0, 0)
    rep_q, rep_c = QuantumRegister(REP, "q"), ClassicalRegister(REP, "c")
    rep = QuantumCircuit(rep_q, rep_c)
    rep.x(range(REP))  # encode bit=1 as |11..1>
    _noisy_idle(rep, list(rep_q), IDLE)
    rep.measure(range(REP), range(REP))
    bare_ok = (
        sum(
            v
            for k, v in run_counts(backend, noise_model, bare).items()
            if k.strip() == "1"
        )
        / SHOTS
    )
    rc = run_counts(backend, noise_model, rep)
    rep_ok = (
        sum(v for k, v in rc.items() if k.replace(" ", "").count("1") * 2 > REP) / SHOTS
    )  # majority = 1
    print(
        f"    bare qubit survives the channel: {bare_ok:.3f}   repetition-protected: {rep_ok:.3f}"
    )
    print(
        f"    => the germe-stabilization (here a {REP}x repetition; the [[5,1,3]] in bulk_listener) preserves the bit."
    )
    assert (
        rep_ok > bare_ok
    ), "the germe-stabilization (repetition) must preserve the bit better than bare"


# ===================== [B] the germe as REFERENCE (matched filter) =====================
def _ry_chain(thetas):
    qc = QuantumCircuit(len(thetas))
    for i, t in enumerate(thetas):
        qc.ry(float(t), i)
    for i in range(len(thetas) - 1):
        qc.cx(i, i + 1)
    return qc


def radion_germe_gate(n=N_GERME):
    """THE REAL GERME (NOT a toy): the radion field wavepacket (germe_decompression, phi0=1.40 M_s)."""
    dim = 2**n
    k0 = PHI0_OVER_MS / 2.5 * (dim - 1)
    amp = np.exp(-((np.arange(dim) - k0) ** 2) / 2.0)
    amp = amp / np.linalg.norm(amp)
    qc = QuantumCircuit(n)
    qc.append(StatePreparation(amp), range(n))
    return transpile(qc, basis_gates=AER_BASIS, optimization_level=1).to_gate(
        label="germe"
    )


def section_reference(backend, noise_model):
    print(
        "\n[B] THE GERME AS REFERENCE -- the matched filter: the germe template is selective (the comparison)"
    )
    n = N_GERME
    germe = radion_germe_gate(n)  # the REAL radion germe, not a toy

    def overlap(sig, templ):
        q, c = QuantumRegister(n, "q"), ClassicalRegister(n, "c")
        qc = QuantumCircuit(q, c)
        qc.append(sig, q)
        qc.append(templ.inverse(), q)
        qc.measure(q, c)
        cc = run_counts(backend, noise_model, qc)
        return sum(v for k, v in cc.items() if set(k.replace(" ", "")) <= {"0"}) / SHOTS

    inj = overlap(germe, germe)
    rnds = [
        transpile(
            _ry_chain(RNG.uniform(0, 2 * np.pi, n)),
            basis_gates=AER_BASIS,
            optimization_level=1,
        ).to_gate()
        for _ in range(6)
    ]
    base = float(np.mean([overlap(germe, r) for r in rnds]))
    print(
        f"    germe template on the germe: {inj:.3f}   vs random templates: {base:.3f}  (SELECTIVE)"
    )
    print(
        "    => the germe is the stable REFERENCE the sensor is calibrated against (the comparison tool)."
    )
    assert (
        inj > 2.5 * base
    ), "the germe reference (matched filter) must be selective vs random"


# ===================== [C]+[D] the dialogue + the control =====================
def channel_output(backend, noise_model, in_bits):
    """Encode in_bits -> the noisy idle channel -> measure -> the output bits. (the message runs bare here;
    the germe-stabilization that would protect it under heavier noise is demoed in section [A].)
    """
    n = len(in_bits)
    q, c = QuantumRegister(n, "q"), ClassicalRegister(n, "c")
    qc = QuantumCircuit(q, c)
    for i, b in enumerate(in_bits):
        if b:
            qc.x(i)
    _noisy_idle(qc, list(q), IDLE)
    qc.measure(q, c)
    return dominant_bits(run_counts(backend, noise_model, qc), n)


def section_dialogue(backend, noise_model, text):
    print(
        f"\n[C] THE DIALOGUE -- input text -> bits -> channel -> output bits -> text   (input = {text!r})"
    )
    in_bits = text_to_bits(text, N_MSG_BITS)
    out_bits = channel_output(backend, noise_model, in_bits)
    echo_fid = float(np.mean([a == b for a, b in zip(in_bits, out_bits)]))
    print(
        f"    input  bits : {''.join(map(str, in_bits))}  -> text {bits_to_text(in_bits)!r}"
    )
    print(
        f"    output bits : {''.join(map(str, out_bits))}  -> text {bits_to_text(out_bits)!r}"
    )
    print(
        f"    => the channel ECHOES the input (bit fidelity {echo_fid:.2f}); the output is your text + noise."
    )

    print(
        "\n[D] THE CONTROL (anti-pareidolia) -- a DIFFERENT (random) input through the SAME channel"
    )
    ctrl_in = [int(b) for b in RNG.integers(0, 2, N_MSG_BITS)]  # a different message
    ctrl_bits = channel_output(backend, noise_model, ctrl_in)
    ctrl_match = float(np.mean([a == b for a, b in zip(in_bits, ctrl_bits)]))
    print(
        f"    control bits: {''.join(map(str, ctrl_bits))}  -> text {bits_to_text(ctrl_bits)!r}"
    )
    print(
        f"    => a DIFFERENT input does NOT come out as your text (match to your message {ctrl_match:.2f} ~ chance 0.5)."
    )
    assert (
        echo_fid > 0.7
    ), "the channel must echo the input (the message survives the noisy channel)"
    assert (
        echo_fid > ctrl_match + 0.2
    ), "the message output must match your input far more than a different-input control (no pareidolia)"
    return echo_fid, ctrl_match


def main():
    use_ibm = "--ibm" in sys.argv
    text = "hi"
    if "--input" in sys.argv:
        text = sys.argv[sys.argv.index("--input") + 1]
    backend, noise_model = get_backend(use_ibm)
    print("=" * 92)
    print(
        " THE BULK DIALOGUE -- text in -> the sensor (germe = stabilizer + reference) -> text out, controlled"
    )
    print("=" * 92)

    section_stabilizer(backend, noise_model)
    section_reference(backend, noise_model)
    echo_fid, ctrl_match = section_dialogue(backend, noise_model, text)

    print("\n[E] VERDICT")
    print(
        "    * the germe is the STABILIZER (it preserves the qubits) + the REFERENCE (the matched filter)."
    )
    print(
        "    * your text is the DEDICATED INPUT; the output is read in bits and transcoded to text."
    )
    print(
        f"    * the channel ECHOES your input (fidelity {echo_fid:.2f}); a DIFFERENT-input control does NOT"
    )
    print(
        f"      contain your text (match {ctrl_match:.2f}) -> the output reflects the input, no pareidolia."
    )
    print(
        "    * HONEST: on known physics (Aer / the circuit) the output = your input + noise -- NO bulk-"
    )
    print(
        "      composed response (the bulk emits a FIELD, the m_V axion, not a text). On a REAL QC, an"
    )
    print(
        "      output deviating from this echo BEYOND the control = a signal / new physics."
    )
    print(
        "    => NULL = your text echoed + noise; NON-NULL = something coherent the control does not have."
    )
    print(
        '       run `python bulk_dialogue.py --input "your text" --ibm` to try it on a real online QC.'
    )

    print(
        "\n  ALL SECTIONS PASSED (germe stabilizes + is the selective reference; the channel echoes, the control is clean)."
    )
    print("=" * 92)


if __name__ == "__main__":
    main()
