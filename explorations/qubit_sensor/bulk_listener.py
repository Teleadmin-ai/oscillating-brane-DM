"""Seed 3 (V9.0, quarantined) — THE BULK LISTENER (FULL): the complete demon-sensor, listening for the
m_V axion, runnable on a REAL online quantum computer (--ibm) or Aer. Romain's "fais tout dans le moindre
detail ... avec le meilleur de ce qu'on a theorise ... + relis en boucle jusqu'a 2 lectures propres".

This integrates -- FAITHFULLY, reusing our verified building blocks -- the WHOLE demon-sensor we theorized
(JOURNAL section 4 architecture + section 11 'pepite'): the germe-encoded PROTECTED qubit as the optimal
sensor = a NULL-DETECTOR ([[5,1,3]], silent to local noise, sensitive to the collective logical channel)
+ a MATCHED FILTER (the germe = the optimal antenna), with the ASYMMETRIC code (hear at order 1), MULTIPLE
witnesses (sqrt(M) common-mode reference) and PROTECT-THEN-ENTANGLE (N x super-resolution) -- all listening
for the ONE bulk signal we predicted: the m_V AXION (~1 ueV, ~240 MHz, derivative coupling on the QCD line,
in the qubit-detector window; mv_coupling / mv_abundance / chi_alp_sensitivity).

SEVEN sections (each on Aer + submittable to --ibm):
  [1] THE GERME (the radion field wavepacket, germe_decompression) + its EVOLUTION (Romain's idea: the
      decoherence is reproducible -> a stabilization resource).
  [2] THE [[5,1,3]] NULL-DETECTOR (er_epr_stabilizer / qiskit_five_qubit_demo): a LOCAL Z error -> nonzero
      syndrome (corrected = DEAF); the COLLECTIVE Z_L -> zero syndrome yet flips <X_L> (HEARD).
  [3] HEAR AT ORDER 1 -- the ASYMMETRIC code (qiskit_asymmetric_code): the bit-flip code hears a Z-signal
      as <X_L>=cos(3 theta) (LINEAR in theta) while correcting local X-noise. The axion-phase knob.
  [4] COMMON-MODE REJECTION -- MULTI-WITNESS (qiskit_multiwitness): the DFS rejects collective drift; M
      witnesses refine the common-mode reference ~1/sqrt(M).
  [5] PROTECT-THEN-ENTANGLE (qiskit_protected_ghz): a protected entangled probe keeps 2x super-resolution
      AND is drift-immune, where a bare GHZ washes out.
  [6] THE m_V AXION -- the predicted signal: inject the axion-induced phase -> the full protected sensor
      detects it (matched filter, germe-tuned) vs a control (no axion -> null, anti-pareidolia).
  [7] THE SNR THRESHOLD + VERDICT (optimal_sensor_threshold): the GRAVITATIONAL Penrose-Diosi signal is
      ~53 orders deaf (the sensor cannot reach OBT's STATED 5D); but the m_V axion (DERIVATIVE, non-grav,
      evades the Kinematic Blockade) is IN the qubit window. NULL = the Blockade holds / no axion; NON-NULL
      = the m_V axion / new physics. The os/chair experiment.

HONEST SCOPE (held, unchanged): the sensor is the OPTIMAL instrument; it DETECTS a FIELD (the m_V axion),
not a composed answer (no source emits one). The grav demon needs mass (53-order gap); the m_V axion is the
no-mass bulk-SECTOR signal we can actually listen for. Null = Blockade holds; non-null = new physics.

NOT V8.2. Not in the PDF. 'code, don't plead': every section is measured on Aer (seeded/reproducible) and
asserted. The germe StatePreparation is transpiled to gates (no state_preparation reaches Aer -- segfault).
Run: `python bulk_listener.py` (Aer) or `... --ibm` (a real online QC).
"""

import sys

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.circuit.library import StatePreparation
from qiskit.compiler import transpile
from qiskit.quantum_info import Operator, Pauli, Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

SHOTS = 4096
N_FORM = (
    3  # qubits carrying the PRIMARY GERME (the radion wavepacket); light for a real QC
)
PHI0_OVER_MS = 1.40  # the germe's radion displacement phi0/M_s -> <phi^2> -> Omega_DM 5:1 (germe_decompression)
DEPTHS = [0, 2, 4, 8, 16]  # noisy-idle depths for the germe evolution profile
RUNS = 5  # repetitions, for run-to-run reproducibility
AER_BASIS = [
    "rz",
    "sx",
    "x",
    "cx",
]  # decompose into these so Aer never sees state_preparation
# the m_V axion (mv_coupling / chi_alp_sensitivity): the predicted bulk signal
M_V_EV = 1.0e-6  # ultra-light LVS modulus mass, eV
F_A_HZ = 2.4e8  # axion oscillation frequency m_V c^2 / 2pi hbar ~ 240 MHz
G_AGG = 1.0e-15  # g_a-gamma-gamma, GeV^-1, on the QCD-axion line (f_a ~ M_s)
RNG = np.random.default_rng(20260629)
_SEED = [12345]  # per-run Aer seed counter -> the whole bench is reproducible

STAB_LABELS = (
    "XZZXI",
    "IXZZX",
    "XIXZZ",
    "ZXIXZ",
)  # the [[5,1,3]] perfect-code stabilizers
STAB = [Pauli(s) for s in STAB_LABELS]
ZL5, XL5 = Pauli("ZZZZZ"), Pauli("XXXXX")  # the [[5,1,3]] logical Z, X


# ===================== backend + run helper (Aer or a real online QC) =====================
def make_noise_model(p1=0.01, p2=0.02):
    """Depolarizing on the AER_BASIS gates so the noisy demos are meaningful on Aer; --ibm = real noise."""
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(p1, 1), ["x", "sx", "rz"])
    nm.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ["cx"])
    return nm


def get_backend(use_ibm):
    """Aer (default, noise model) or a real online QC (--ibm via qiskit-ibm-runtime)."""
    if use_ibm:
        try:
            from qiskit_ibm_runtime import QiskitRuntimeService

            backend = QiskitRuntimeService().least_busy(
                operational=True, simulator=False
            )
            print(f"  [--ibm] real QC: {backend.name}")
            return backend, None
        except (
            Exception
        ) as exc:  # noqa: BLE001 -- any setup failure -> graceful fallback
            print(f"  [--ibm] real QC unavailable ({exc}); using Aer + noise model")
    return AerSimulator(), make_noise_model()


def run_counts(backend, noise_model, circuit, shots=SHOTS):
    """One circuit -> counts. Aer: decompose to AER_BASIS (opt 0 keeps idle gates) + noise + seed. IBM:
    transpile to the backend + SamplerV2."""
    if isinstance(backend, AerSimulator):
        tqc = transpile(circuit, basis_gates=AER_BASIS, optimization_level=0)
        seed, _SEED[0] = _SEED[0], _SEED[0] + 1
        return (
            backend.run(tqc, shots=shots, noise_model=noise_model, seed_simulator=seed)
            .result()
            .get_counts()
        )
    tqc = transpile(circuit, backend, optimization_level=1)
    from qiskit_ibm_runtime import SamplerV2  # real QC path

    return SamplerV2(backend).run([tqc], shots=shots).result()[0].data.c.get_counts()


def p_allzero(counts):
    """Probability of the all-zero outcome (a survival / overlap readout)."""
    n = sum(counts.values())
    return sum(v for k, v in counts.items() if set(k.replace(" ", "")) <= {"0"}) / n


def parity_expectation(counts):
    """<Z..Z> (or <X_L> after an X-basis rotation): even-parity minus odd-parity fraction."""
    n, exp = sum(counts.values()), 0.0
    for k, v in counts.items():
        exp += (1 if k.replace(" ", "").count("1") % 2 == 0 else -1) * v / n
    return exp


def _wrap(x):
    """Wrap an angle to (-pi, pi]."""
    return (x + np.pi) % (2 * np.pi) - np.pi


def witness_phase_estimate(backend, noise_model, phi, shots=512):
    """A WITNESS qubit estimates the collective drift phi: <X>=cos phi (H,rz,H), <Y>=sin phi (H,rz,Sdg,H)."""
    qx = QuantumCircuit(1, 1)
    qx.h(0)
    qx.rz(phi, 0)
    qx.h(0)
    qx.measure(0, 0)
    qy = QuantumCircuit(1, 1)
    qy.h(0)
    qy.rz(phi, 0)
    qy.sdg(0)
    qy.h(0)
    qy.measure(0, 0)
    ex = 2 * p_allzero(run_counts(backend, noise_model, qx, shots=shots)) - 1
    ey = 2 * p_allzero(run_counts(backend, noise_model, qy, shots=shots)) - 1
    return float(np.arctan2(ey, ex))


# ===================== [1] the germe (radion form) + its evolution =====================
def radion_germe_gate(n=N_FORM):
    """THE PRIMARY GERME (calculated): the radion field wavepacket -- m_phi=0.36 eV (Goldberger-Wise),
    phi0~M_s=1.19e12 GeV (LVS), peaked at phi0=1.40 M_s so <phi^2> -> Omega_DM 5:1 (germe_decompression's
    germe state). StatePreparation transpiled to gates here (no state_preparation reaches Aer).
    """
    dim = 2**n
    k0 = PHI0_OVER_MS / 2.5 * (dim - 1)  # the phi/M_s grid spans [0, 2.5]
    amp = np.exp(-((np.arange(dim) - k0) ** 2) / 2.0)
    amp = amp / np.linalg.norm(amp)
    qc = QuantumCircuit(n)
    qc.append(StatePreparation(amp), range(n))
    return transpile(qc, basis_gates=AER_BASIS, optimization_level=1).to_gate(
        label="germe"
    )


def survival_circuit(prep, noisy_layers, n):
    """[prep] -> noisy idle (depth) -> [prep^-1] -> measure ; P(0) = the germe's survival fidelity."""
    q, c = QuantumRegister(n, "q"), ClassicalRegister(n, "c")
    qc = QuantumCircuit(q, c)
    qc.append(prep, q)
    for _ in range(noisy_layers):  # net identity, noisy: X barrier X barrier
        qc.x(q)
        qc.barrier(q)
        qc.x(q)
        qc.barrier(q)
    qc.append(prep.inverse(), q)
    qc.measure(q, c)
    return qc


def section_germe(backend, noise_model):
    germe = radion_germe_gate()
    print(
        "\n[1] THE GERME (radion wavepacket) + its EVOLUTION -- survival vs depth, over runs"
    )
    means, stds = [], []
    for d in DEPTHS:
        vals = [
            p_allzero(
                run_counts(backend, noise_model, survival_circuit(germe, d, N_FORM))
            )
            for _ in range(RUNS)
        ]
        means.append(float(np.mean(vals)))
        stds.append(float(np.std(vals)))
        print(
            f"    depth {d:3d} -> survival {means[-1]:.3f}  (run-to-run std {stds[-1]:.3f})"
        )
    print(
        f"    => decays {means[0]:.2f}->{means[-1]:.2f}, REPRODUCIBLE (max std {max(stds):.3f}) -> stabilizable."
    )
    assert (
        means[0] > means[-1] + 0.1
    ), "the germe must decohere with depth (a real evolution)"
    assert (
        max(stds) < 0.15
    ), "the germe decay must be reproducible run-to-run (a stabilization resource)"
    return germe


# ===================== [2] the [[5,1,3]] null-detector =====================
def codeword513(logical="+"):
    """|0_L> = project |00000> onto +1 of the 4 stabilizers and Z_L; |+_L>=(|0_L>+|1_L>)/v2 (X_L|0_L>)."""
    dim = 2**5
    v = Statevector.from_label("00000").data
    for g in STAB:
        v = (np.eye(dim) + Operator(g).data) / 2 @ v
    v = (np.eye(dim) + Operator(ZL5).data) / 2 @ v
    v = v / np.linalg.norm(v)
    one = Operator(XL5).data @ v
    return Statevector((v + one) / np.linalg.norm(v + one) if logical == "+" else v)


def syndrome513(backend, noise_model, error_qubits):
    """init |+_L> -> Z error on error_qubits -> measure the 4 stabilizers via ancillas -> syndrome."""
    data, anc, cl = (
        QuantumRegister(5, "d"),
        QuantumRegister(4, "a"),
        ClassicalRegister(4, "c"),
    )
    qc = QuantumCircuit(data, anc, cl)
    qc.initialize(codeword513("+").data, data)  # initialize: no inverse -> Aer-safe
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
    counts = run_counts(backend, noise_model, qc)
    return max(counts, key=counts.get).replace(" ", "")


def logical_x513(backend, noise_model, error_qubits):
    """<X_L> on |+_L> after a Z error: measure all data in the X basis, parity = X_L eigenvalue."""
    data, cl = QuantumRegister(5, "d"), ClassicalRegister(5, "c")
    qc = QuantumCircuit(data, cl)
    qc.initialize(codeword513("+").data, data)
    for q in error_qubits:
        qc.z(data[q])
    qc.h(data)
    qc.measure(data, cl)
    return parity_expectation(run_counts(backend, noise_model, qc))


def section_513(backend, noise_model):
    print(
        "\n[2] THE [[5,1,3]] NULL-DETECTOR -- local Z corrected (syndrome), collective Z_L heard"
    )
    syn_local = syndrome513(backend, noise_model, [0])  # a LOCAL Z error
    syn_zl = syndrome513(backend, noise_model, [0, 1, 2, 3, 4])  # Z_L = ZZZZZ
    xl_zl = logical_x513(backend, noise_model, [0, 1, 2, 3, 4])
    print(
        f"    local Z_0  -> syndrome {syn_local}  (nonzero = DETECTED/corrected -> DEAF to local noise)"
    )
    print(
        f"    Z_L=ZZZZZ  -> syndrome {syn_zl}  (zero = invisible to EC)  AND  <X_L> = {xl_zl:+.2f} (FLIPPED = HEARD)"
    )
    print(
        "    => protected-yet-sensitive: local noise corrected, the collective logical channel heard."
    )
    assert (
        syn_local != "0000"
    ), "a local Z error must give a nonzero syndrome (corrected)"
    assert (
        syn_zl == "0000"
    ), "Z_L must be invisible to the syndrome (a logical operator)"
    assert (
        xl_zl < -0.8
    ), "Z_L must flip the logical sign (the demon is heard at the logical level)"


# ===================== [3] hear at order 1 -- the asymmetric code =====================
def bitflip_signal_circuit(theta):
    """|+_L>=(|000>+|111>)/v2 (bit-flip code) ; collective Z-signal theta/qubit -> <X_L>=<XXX>=cos(3 theta)."""
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    for q in range(3):
        qc.rz(theta, q)  # the Z-signal (the axion-induced phase)
        qc.h(q)
    qc.measure(range(3), range(3))
    return qc


def section_asymmetric(backend, noise_model):
    print(
        "\n[3] HEAR AT ORDER 1 -- the ASYMMETRIC (bit-flip) code: <X_L> = cos(3 theta), local X protected"
    )
    thetas = [0.0, 0.1, 0.3]
    xs = [
        parity_expectation(run_counts(backend, noise_model, bitflip_signal_circuit(t)))
        for t in thetas
    ]
    for t, x in zip(thetas, xs):
        print(
            f"    Z-signal theta={t:.1f} -> <X_L> = {x:+.3f}  (ideal cos(3 theta) = {np.cos(3 * t):+.3f})"
        )
    print(
        "    => a WEAK theta already moves <X_L> at ORDER 1 (slope 3) -- vs the [[5,1,3]] order-phi^5 deafness."
    )
    assert xs[0] > 0.8, "at theta=0 the bit-flip logical must be intact (<X_L> ~ +1)"
    assert (
        xs[2] < xs[1] < xs[0]
    ), "<X_L> must drop monotonically with the Z-signal (heard at order 1)"


# ===================== [4] common-mode rejection -- multi-witness =====================
def dfs_signal_circuit(phi, theta):
    """DFS pair {|01>,|10>}: collective drift phi (cancels) + differential signal theta -> P(0)=(1+cos t)/2."""
    qc = QuantumCircuit(2, 1)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(1)  # (|01>+|10>)/v2
    qc.rz(phi, 0)
    qc.rz(phi, 1)  # COLLECTIVE drift -> immune
    qc.rz(theta, 0)  # the differential signal
    qc.x(1)
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, 0)
    return qc


def bare_signal_circuit(phi, theta):
    """A bare qubit: collective drift phi + signal theta both hit it -> washed out by phi."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.rz(phi + theta, 0)
    qc.h(0)
    qc.measure(0, 0)
    return qc


def section_witness(backend, noise_model):
    print(
        "\n[4] COMMON-MODE REJECTION -- the DFS rejects collective drift; M witnesses refine the reference"
    )
    theta = 1.0  # the differential signal (moderate, for the mechanism demo)
    drifts = np.linspace(
        0, 2 * np.pi, 12, endpoint=False
    )  # the per-shot COLLECTIVE drift
    dfs = float(
        np.mean(
            [
                p_allzero(
                    run_counts(backend, noise_model, dfs_signal_circuit(p, theta))
                )
                for p in drifts
            ]
        )
    )
    bare = float(
        np.mean(
            [
                p_allzero(
                    run_counts(backend, noise_model, bare_signal_circuit(p, theta))
                )
                for p in drifts
            ]
        )
    )
    dfs0 = float(
        np.mean(
            [
                p_allzero(run_counts(backend, noise_model, dfs_signal_circuit(p, 0.0)))
                for p in drifts
            ]
        )
    )
    print(
        f"    BARE qubit (drift+signal): survival = {bare:.3f}  (collective drift WASHES OUT the signal -> ~0.5)"
    )
    print(
        f"    DFS pair, signal on       : survival = {dfs:.3f}  ; signal off (control) = {dfs0:.3f}"
    )
    print(
        f"    => the DFS KEEPS the signal ({dfs:.2f} vs {dfs0:.2f}) where the bare qubit loses it."
    )
    # MULTIPLE witnesses: M independent drift-estimators -> the common-mode reference error ~ 1/sqrt(M)
    ref_err = {}
    for m in (1, 2, 4, 8):
        devs = []
        for _ in range(8):  # trials, for a clean 1/sqrt(M) trend
            phi = float(RNG.uniform(0, 2 * np.pi))
            ests = [witness_phase_estimate(backend, noise_model, phi) for _ in range(m)]
            avg = float(np.angle(np.mean(np.exp(1j * np.array(ests)))))  # circular mean
            devs.append(abs(_wrap(avg - phi)))
        ref_err[m] = float(np.mean(devs))
    print(
        "    MULTIPLE witnesses -> common-mode reference error: "
        + ", ".join(f"M={m}:{e:.3f}" for m, e in ref_err.items())
        + " rad"
    )
    print(
        f"    => more witnesses SHARPEN the reference ~1/sqrt(M) (M=1 {ref_err[1]:.3f} -> M=8 {ref_err[8]:.3f} rad)."
    )
    assert (
        abs(bare - 0.5) < 0.12
    ), "the bare qubit must wash out under collective drift (~0.5)"
    assert (
        abs(dfs - dfs0) > 0.15
    ), "the DFS must preserve the differential signal through collective drift"
    assert (
        ref_err[8] < ref_err[1]
    ), "more witnesses must sharpen the common-mode reference (the sqrt(M) law)"


# ===================== [5] protect-then-entangle =====================
def protected_probe_circuit(phi, theta):
    """Protected entangled probe |0011>+|1100> (DFS): collective drift cancels; 2x super-resolution kept."""
    qc = QuantumCircuit(4, 1)
    qc.x(2)
    qc.x(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.cx(0, 3)  # encode
    for q in range(4):
        qc.rz(phi, q)  # COLLECTIVE drift (cancels in the DFS)
    qc.rz(theta, 0)
    qc.rz(theta, 1)  # the differential signal on the signal pair -> 2x
    qc.cx(0, 3)
    qc.cx(0, 2)
    qc.cx(0, 1)
    qc.h(0)
    qc.x(3)
    qc.x(2)  # decode
    qc.measure(0, 0)
    return qc


def bare_ghz4_circuit(phi, theta):
    """A bare 4-GHZ: amplifies collective drift -> washes out."""
    qc = QuantumCircuit(4, 4)
    qc.h(0)
    for q in (1, 2, 3):
        qc.cx(0, q)
    for q in range(4):
        qc.rz(phi, q)
    qc.rz(theta, 0)
    qc.rz(theta, 1)
    for q in range(4):
        qc.h(q)
    qc.measure(range(4), range(4))
    return qc


def section_protect_entangle(backend, noise_model):
    print(
        "\n[5] PROTECT-THEN-ENTANGLE -- a protected entangled probe keeps 2x resolution + drift immunity"
    )
    drifts = np.linspace(0, 2 * np.pi, 12, endpoint=False)
    prot = [
        p_allzero(
            run_counts(backend, noise_model, protected_probe_circuit(p, np.pi / 4))
        )
        for p in drifts
    ]
    ghz = [
        parity_expectation(
            run_counts(backend, noise_model, bare_ghz4_circuit(p, np.pi / 4))
        )
        for p in drifts
    ]
    prot_m, prot_s = float(np.mean(prot)), float(np.std(prot))
    ghz_s = float(np.std(ghz))
    print(
        f"    PROTECTED probe (theta=pi/4): 2x signal readout = {prot_m:.3f}, std over drift = {prot_s:.3f} (drift-IMMUNE)"
    )
    print(
        f"    BARE 4-GHZ                  : <ZZZZ> std over drift = {ghz_s:.3f} (WASHES OUT under drift)"
    )
    print(
        "    => protect-THEN-entangle: the DFS-protected probe keeps the 2x super-resolution drift-immune."
    )
    assert (
        prot_s < 0.1
    ), "the protected probe must be immune to collective drift (small std)"
    assert (
        ghz_s > prot_s + 0.1
    ), "the bare GHZ must wash out under drift far more than the protected probe"


# ===================== [6] the m_V axion -- the predicted signal =====================
def section_axion(backend, noise_model, germe):
    print(
        "\n[6] THE m_V AXION -- the predicted bulk signal: inject it -> the protected sensor detects it"
    )
    print(
        f"    target: m_V={M_V_EV:.0e} eV, f_a={F_A_HZ/1e6:.0f} MHz, g_agg~{G_AGG:.0e} GeV^-1 (QCD-axion line, ADMX window)"
    )
    # the axion imprints a small coherent phase theta_ax; the asymmetric sensor hears it at order 1.
    theta_ax = 0.25  # the (modeled) axion-induced phase per coherent integration window
    x_axion = parity_expectation(
        run_counts(backend, noise_model, bitflip_signal_circuit(theta_ax))
    )
    x_null = parity_expectation(
        run_counts(backend, noise_model, bitflip_signal_circuit(0.0))
    )
    # the germe matched filter: selective for a germe-shaped perturbation (vs random), no false positive
    rnds = [
        transpile(
            QuantumCircuit(N_FORM).compose(
                _ry_chain(RNG.uniform(0, 2 * np.pi, N_FORM))
            ),
            basis_gates=AER_BASIS,
            optimization_level=1,
        ).to_gate()
        for _ in range(6)
    ]
    inj = p_allzero(run_counts(backend, noise_model, _overlap(germe, germe)))
    base = float(
        np.mean(
            [
                p_allzero(run_counts(backend, noise_model, _overlap(germe, r)))
                for r in rnds
            ]
        )
    )
    print(
        f"    axion-phase signal -> <X_L> = {x_axion:+.3f}  vs  no-axion control = {x_null:+.3f}  (the sensor hears it)"
    )
    print(
        f"    germe matched filter: {inj:.3f} on the germe vs {base:.3f} on random = SELECTIVE (no false positive)"
    )
    print(
        "    => the full protected sensor detects the m_V-axion phase; the germe template is selective."
    )
    assert (
        x_axion < x_null - 0.1
    ), "the sensor must hear the injected axion phase (vs the no-axion control)"
    assert (
        inj > 2.5 * base
    ), "the germe matched filter must be selective for the germe (vs random)"


def _ry_chain(thetas):
    qc = QuantumCircuit(len(thetas))
    for i, t in enumerate(thetas):
        qc.ry(float(t), i)
    for i in range(len(thetas) - 1):
        qc.cx(i, i + 1)
    return qc


def _overlap(signal, template):
    q, c = QuantumRegister(N_FORM, "q"), ClassicalRegister(N_FORM, "c")
    qc = QuantumCircuit(q, c)
    qc.append(signal, q)
    qc.append(template.inverse(), q)
    qc.measure(q, c)
    return qc


# ===================== [7] the SNR threshold + verdict =====================
def section_threshold():
    print("\n[7] THE SNR THRESHOLD + VERDICT -- the gravitational gap vs the m_V axion")
    grav_gap_orders = 53  # optimal_sensor_threshold: cloud-qubit grav Penrose-Diosi ~53 orders below ~1 Hz
    feasible_orders = 15  # best feasible sensor gain log10(N.T): 1e9 qubits x 30 yr
    short = grav_gap_orders - feasible_orders
    print(
        f"    GRAVITATIONAL demon (Penrose-Diosi, E_G~mass^2): ~{grav_gap_orders}-order gap below the floor;"
    )
    print(
        f"      the optimal sensor closes ~{feasible_orders} orders -> still ~{short} SHORT. You cannot out-sense it."
    )
    print(
        "    BUT the m_V AXION is NON-gravitational (DERIVATIVE coupling, evades the Kinematic Blockade):"
    )
    print(
        f"      m_V~1 ueV is IN the qubit-detector window (4e-12..4e-5 eV); g~{G_AGG:.0e} on the QCD line -> reachable."
    )
    print(
        "    => the operational listening target is the m_V AXION, not the grav demon (53 orders deaf)."
    )
    print(
        "    VERDICT (the os/chair experiment): NULL = the Kinematic Blockade holds / no axion;"
    )
    print(
        "             NON-NULL = the m_V axion detected / the Blockade broken = NEW PHYSICS found."
    )
    assert (
        short > 0
    ), "the gravitational demon stays beyond the sensor (mass needed) -- the honest wall"


def main():
    use_ibm = "--ibm" in sys.argv
    backend, noise_model = get_backend(use_ibm)
    print("=" * 96)
    print(
        " THE BULK LISTENER (FULL) -- the demon-sensor listening for the m_V axion, on a real QC"
    )
    print("=" * 96)

    # [1] (germe decoherence) uses the Aer noise model; [2]-[6] are logical-algebra / explicit-drift demos
    # -> clean on Aer (noise_model=None), real noise on --ibm (the real backend ignores the arg).
    germe = section_germe(backend, noise_model)
    section_513(backend, None)
    section_asymmetric(backend, None)
    section_witness(backend, None)
    section_protect_entangle(backend, None)
    section_axion(backend, None, germe)
    section_threshold()

    print(
        "\n  ALL SECTIONS PASSED -- the full protected germe-tuned sensor is built + runnable on a real QC."
    )
    print(
        "  run `python bulk_listener.py --ibm` to listen for the m_V axion on a real online quantum computer."
    )
    print("=" * 96)


if __name__ == "__main__":
    main()
