"""Seed 3 (V9.0, quarantined) — THE EXACT PERCEVAL/OVH JOB for belenos (Quandela, gate-based photonic,
0.28 EUR/HT-s). Romain's 'prepare le job perceval/ovh exact pour belenos comme ca ce sera deja la'.

THE HARDWARE-HONEST DESIGN (computed, not assumed):
  * photonic 2-qubit gates are PROBABILISTIC (heralded/postselected CNOT ~ 1/9 success). The N=10 protocol
    circuit has ~204 CX -> herald probability ~(1/9)^204 ~ 1e-194 = DEAD as a gate-translated job. COMPUTED
    below for the minimal instance too (the gate route stays dead even at ~20 CX).
  * the NATIVE photonic fact: a SINGLE PHOTON over m modes undergoes an ARBITRARY m x m unitary
    DETERMINISTICALLY (Clements/Reck mesh -- no postselection). So the belenos v1 job runs the protocol's
    MINIMAL INSTANCE mode-natively: n=3 qubits <-> DIM=8 modes, ONE photon, the EXACT 8x8 declared unitary
    (germe prep + the 1-rep SYK product + the basis rotation, FOLDED into a single matrix), detection = which
    mode clicks. Everything the protocol declares survives EXACTLY at this size; nothing is a toy.

THE DECLARED INSTANCE (the same code path as demon_qc/demon_readout_basis -- imported, not re-implemented):
  germe        = demon_qc.germe_state(3, phi0) -- the SAME canonical formula at dim=8 (declared resolution);
                 BOTH candidates phi0 = 0.42 (corrected) and 1.40 (legacy).
  decompressor = the 1-rep Lie-Trotter product of the n=3 sparse-SYK (demon_qc.sparse_syk, the declared seed),
                 validated == drb.manual_product_state (identity).
  readout      = Z and X (X = H^(x3) FOLDED into the run unitary -- free on modes), 4 main configs
                 (+ the A1 hardware-reference config = 5 total).
  input        = 'talk to the bulk' -> 1 conditioning bit at this size (N_IN=1, declared reduced).
  rules        = the two-layer belenos_protocol rules, RECOMPUTED exactly for this instance (thresholds,
                 power, null-ensemble reading bands), written to belenos_job_spec.json = the pre-registration.

SCOPE (honest): the 8-branch instance carries LAYER 1 (anomaly vs our own exact math, in 2 bases, both
germe candidates) end-to-end on real hardware + a REDUCED reading (3-bit branches -> the first-8-chars
codec); the FULL 64-branch reading (K_min=6 chars) needs dim=64 modes or a CX-feasible gate route -- future.
The interpretive corollary (axion_photonic_chip) holds: an anomaly here CANNOT be the m_V axion (16+ orders).

AMENDMENTS (July 2026, committed BEFORE any run -- the 'pertinence' recul):
  A1 (the hardware floor): on a real Clements mesh the layer-1 G-test vs the IDEAL null is EXPECTED to
     reject for mundane reasons (fabrication/phase error ~% level) -- that rejection is NOT an anomaly. A
     5th DECLARED config is added, the HARDWARE REFERENCE (canonical germe x the product unitary of the
     DISTINCT declared seed 20260711, Z basis): same circuit class, its only role = measure the mundane
     G-inflation. ESCALATION RULE (declared): a main config's rejection counts as 'layer-1 anomaly
     (unmodeled)' ONLY if its G/dof >= R_ESC = 3.0 x the reference's; otherwise 'hardware-consistent'.
     Honest: n=1 reference = an order-of-magnitude floor (mesh error is config-dependent); this extends
     the anti-pareidolia philosophy from the reading layer to the anomaly layer.
  A2 (the declared interpretation): OBT itself predicts the NULL here -- the priced channel inventory is
     closed (gravitational ~53 orders [optimal_sensor_threshold]; m_V axion 16-18 orders [point E]; radion
     quasi-static -> calibrated out; KK blockaded; chi-derivative = the m_V class), and encoding the
     germe's FORM creates a REPLICA, not an entanglement (same-structure != entangled; no interaction
     Hamiltonian beyond the priced channels). So the run tests [hardware fidelity to the declared unitary]
     + [UNMODELED physics]; it does NOT test OBT: a null is NOT 'OBT survived a test', an anomaly is NOT
     attributable to OBT's bulk (nor to m_V). Both declared before any token is spent.

RUN:  python belenos_job.py                        -> builds + validates + local SLOS dry-run + writes the spec
      python belenos_job.py --token T [--platform qpu:belenos] [--shots 20000]   -> SUBMITS to the real QPU
      (adjust --platform to the exact id shown in the OVH/Quandela console; the token comes from the console.)

NOT V8.2. Not in the PDF. seul les calculs comptent: asserted only identities (unitarity, photonic dist ==
the qubit null, product == manual, calibration FPR); no imposed ranges, no toy.
"""

import argparse
import json
import os
import warnings

import demon_qc  # the instrument: canonical germe, seeded SYK, codec, input transcode
import demon_readout_basis as drb  # the declared product decompressor + the X rotation
import numpy as np
from scipy.sparse import SparseEfficiencyWarning

warnings.filterwarnings("ignore", category=SparseEfficiencyWarning)

N_JOB = 3  # the minimal instance: 3 qubits <-> DIM = 8 modes, ONE photon (deterministic on modes)
DIM = 2**N_JOB
N_IN_JOB = 1  # conditioning bits at this size (declared reduced)
INPUT_TEXT = "talk to the bulk"
PHI0S = [0.42, 1.40]  # the corrected candidate + the legacy candidate
ALPHA_3SIG = 0.00135
M_REF = 400  # declared reading depth (post-selected events) for the null-ensemble bands
SEED_REF = 20260711  # amendment A1: the hardware-reference's DISTINCT declared seed (the amendment date)
R_ESC = 3.0  # amendment A1: escalation factor -- anomaly only if G/dof >= R_ESC x the reference's
EUR_PER_S = 0.28
SPEC_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "belenos_job_spec.json"
)


def product_unitary(h, t, reps=1):
    """The DECLARED decompressor as a matrix: the Lie-Trotter product in h's term order (same order as
    drb.manual_product_state: factor k applied to the state first => U = m_last @ ... @ m_1).
    """
    from qiskit.quantum_info import SparsePauliOp

    u = np.eye(DIM, dtype=complex)
    for lbl, c in zip(h.paulis, h.coeffs):
        pm = SparsePauliOp(lbl).to_matrix()
        th = float(np.real(c)) * (t / reps)
        u = (np.cos(th) * np.eye(DIM) - 1j * np.sin(th) * pm) @ u
    return np.linalg.matrix_power(u, reps) if reps > 1 else u


def prep_unitary(germe):
    """An 8x8 unitary whose FIRST COLUMN is the germe (QR + phase fix): the photon enters mode 0, the mesh
    prepares the germe -- state prep is FREE on modes (part of the same interferometer).
    """
    a = np.eye(DIM, dtype=complex)
    a[:, 0] = germe
    q, _ = np.linalg.qr(a)
    q[:, 0] *= np.vdot(q[:, 0], germe) / abs(
        np.vdot(q[:, 0], germe)
    )  # phase so column0 == germe
    return q


def shannon(p):
    p = np.asarray(p)
    p = p[p > 1e-15]
    return max(0.0, float(-(p * np.log2(p)).sum()))


def g_stats_batch(count_mat, p, shots):
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(count_mat > 0, count_mat / (shots * p[None, :]), 1.0)
        return 2.0 * np.sum(
            np.where(count_mat > 0, count_mat * np.log(ratio), 0.0), axis=1
        )


def main():
    ap = argparse.ArgumentParser(
        description="The exact Perceval/OVH job for belenos (minimal instance)."
    )
    ap.add_argument(
        "--token",
        help="the OVH/Quandela access token (from the console); absent = dry-run only",
    )
    ap.add_argument(
        "--platform",
        default="qpu:belenos",
        help="the platform id AS SHOWN in the OVH console",
    )
    ap.add_argument(
        "--shots", type=int, default=20000, help="shots per config on the QPU"
    )
    args = ap.parse_args()
    rng = np.random.default_rng(
        demon_qc.SEED
    )  # the DECLARED seed (same as the whole instrument)
    mc = np.random.default_rng(demon_qc.SEED + 7)

    print("=" * 100)
    print(
        " THE BELENOS JOB — the exact Perceval/OVH submission (minimal instance, mode-native, no toy)"
    )
    print("=" * 100)

    # ===== [1] the declared instance: germe + SYK + the folded run unitaries =====
    h = demon_qc.sparse_syk(N_JOB, 2 * N_JOB, rng)
    u_prod = product_unitary(h, drb.T, reps=1)
    assert np.allclose(
        u_prod @ u_prod.conj().T, np.eye(DIM), atol=1e-9
    ), "the product unitary is unitary"
    g042 = demon_qc.germe_state(N_JOB, phi0=0.42)
    assert np.allclose(
        u_prod @ g042, drb.manual_product_state(g042, h, 1), atol=1e-9
    ), "U_product == the validated manual product (the declared decompressor, as a matrix)"
    w_x = drb.hadamard_matrix(N_JOB)
    bit = int(demon_qc.fold_to_bits(demon_qc.text_to_binary(INPUT_TEXT), N_IN_JOB)[0])
    mask = (np.arange(DIM) & 1) == bit  # the branches consistent with the input bit
    print(
        f"\n[1] THE DECLARED INSTANCE — n={N_JOB} qubits = {DIM} modes, ONE photon; seed {demon_qc.SEED}"
    )
    print(
        f"      SYK: {len(h)} strings on {N_JOB} qubits; T={drb.T}; input {INPUT_TEXT!r} -> bit {bit}"
    )
    configs = {}
    for phi0 in PHI0S:
        germe = demon_qc.germe_state(N_JOB, phi0=phi0)
        u_prep = prep_unitary(germe)
        assert np.allclose(
            u_prep[:, 0], germe, atol=1e-9
        ), "prep unitary's column 0 IS the germe"
        for basis, w in (("Z", np.eye(DIM)), ("X", w_x)):
            u_run = (
                w @ u_prod @ u_prep
            )  # ONE folded unitary: prep + decompress + basis rotation
            p_null = (
                np.abs(u_run[:, 0]) ** 2
            )  # photon in mode 0 -> the EXACT null distribution
            assert np.allclose(
                p_null, np.abs(w @ (u_prod @ germe)) ** 2, atol=1e-12
            ), "photonic mode distribution == the qubit-path null (the construction identity)"
            configs[f"phi0={phi0}_basis={basis}"] = {"u": u_run, "p": p_null}
            print(
                f"      config phi0={phi0} basis={basis}: H(null) = {shannon(p_null):.3f} bits"
            )

    # AMENDMENT A1 -- the HARDWARE REFERENCE config (declared): same construction class, DISTINCT seed;
    # its ONLY role = measure the hardware's mundane G-inflation (the layer-1 floor). NOT a germe candidate.
    h_ref = demon_qc.sparse_syk(N_JOB, 2 * N_JOB, np.random.default_rng(SEED_REF))
    u_prod_ref = product_unitary(h_ref, drb.T, reps=1)
    assert np.allclose(
        u_prod_ref @ u_prod_ref.conj().T, np.eye(DIM), atol=1e-9
    ), "the reference product unitary is unitary"
    u_ref = u_prod_ref @ prep_unitary(g042)  # canonical germe, Z basis
    p_ref = np.abs(u_ref[:, 0]) ** 2
    assert np.allclose(
        p_ref, np.abs(u_prod_ref @ g042) ** 2, atol=1e-12
    ), "reference mode distribution == its qubit-path null (the construction identity)"
    ref_key = f"REF_seed={SEED_REF}_basis=Z"
    configs[ref_key] = {"u": u_ref, "p": p_ref}
    tv_ref = 0.5 * float(np.abs(p_ref - configs["phi0=0.42_basis=Z"]["p"]).sum())
    print(
        f"      config {ref_key} (A1 HARDWARE FLOOR): H(null) = {shannon(p_ref):.3f} bits;"
        f" TV to the primary null = {tv_ref:.3f} (reported, not asserted)"
    )

    # ===== [2] the gate-route feasibility (computed -- why mode-native) =====
    weights = [sum(1 for ch in str(lbl) if ch != "I") for lbl in h.paulis]
    cx = sum(2 * (w - 1) for w in weights)
    print(
        "\n[2] WHY MODE-NATIVE (computed): the gate route is photonically DEAD even at this minimal size"
    )
    print(
        f"      gate route: ~{cx} CX at 1 rep; heralded CNOT ~ 1/9 -> success ~ (1/9)^{cx} ~ 1e{cx*np.log10(1/9):.0f}"
    )
    print(
        "      mode-native: ONE photon x an 8x8 mesh (Clements) = DETERMINISTIC (success ~ transmission)."
    )

    # ===== [3] layer-1 rules RECOMPUTED for this instance (thresholds + power) =====
    print(
        "\n[3] LAYER 1 for THIS instance — G-test vs the exact null (primary config phi0=0.42, Z)"
    )
    p_z = configs["phi0=0.42_basis=Z"]["p"]
    cond = p_z * mask
    p_in = float(cond.sum())
    q_cond = cond / p_in
    b_star = int(np.argmax(cond))
    print("      shots   threshold(3sig)   power eps=0.02   eps=0.05   eps=0.10")
    thresholds, shots_needed = {}, {}
    fpr = None
    for shots in (100, 500, 2000, 5000, 10000, 20000):
        null_g = g_stats_batch(mc.multinomial(shots, p_z, size=3000), p_z, shots)
        thr = float(np.quantile(null_g, 1.0 - ALPHA_3SIG))
        thresholds[shots] = thr
        if shots == 500:
            fresh = g_stats_batch(mc.multinomial(shots, p_z, size=8000), p_z, shots)
            fpr = float(np.mean(fresh > thr))
        pws = []
        for eps in (0.02, 0.05, 0.10):
            p_alt = (1 - eps) * p_z.copy()
            p_alt[b_star] += eps
            pw = float(
                np.mean(
                    g_stats_batch(mc.multinomial(shots, p_alt, size=300), p_z, shots)
                    > thr
                )
            )
            pws.append(pw)
            if pw >= 0.9 and eps not in shots_needed:
                shots_needed[eps] = shots
        print(
            f"      {shots:5d}   {thr:10.2f}        {pws[0]:5.2f}       {pws[1]:5.2f}      {pws[2]:5.2f}"
        )
    hits = int(round((fpr or 0) * 8000))
    assert (
        2 <= hits <= 25
    ), "MC calibration: FPR ~ alpha within binomial noise (the identity)"
    print(f"      calibration FPR = {fpr:.5f} ~ {ALPHA_3SIG} (the identity holds)")
    print(
        "      HONEST (computed -- corrects my first guess): dim-8 needs MORE shots per eps than dim-1024"
    )
    print(
        "      (8 fat cells give the G-test LESS leverage than 1024 thin ones; dim-1024 eps=0.05 took 1000):"
    )
    for eps in (0.02, 0.05, 0.10):
        s = shots_needed.get(eps)
        print(
            f"      => eps={eps:.2f}: {s if s else '>20000'} shots for 90% power at 3 sigma"
        )

    # ===== [3b] the hardware floor -- amendment A1 (declared escalation rule) =====
    print(
        "\n[3b] THE HARDWARE FLOOR (amendment A1, declared): on real hardware the ideal-null G-test is"
    )
    print(
        "      EXPECTED to reject for mundane reasons (Clements mesh fabrication/phase error ~% level);"
    )
    print(
        f"      such a rejection is NOT an anomaly. The reference config ({ref_key}) measures that mundane"
    )
    print(
        "      G-inflation on the SAME circuit class. ESCALATION RULE: 'layer-1 anomaly (unmodeled)' ONLY"
    )
    print(
        f"      if a main config's G/dof >= {R_ESC:.1f} x the reference's G/dof; else 'hardware-consistent'."
    )
    print(
        "      (n=1 reference sample -> an order-of-magnitude floor, mesh error is config-dependent; the"
    )
    print(
        "      anti-pareidolia philosophy extended from the reading layer to the anomaly layer.)"
    )

    # ===== [4] the reduced reading (declared) =====
    print(
        f"\n[4] THE REDUCED READING — P(input bit) = {p_in:.3f}; conditional over {int(mask.sum())} branches"
    )
    top = np.argsort(q_cond)[::-1][:4]
    predicted = demon_qc.latents_to_text([int(i) for i in top])
    # ORDER-sensitive statistic (the relire catch: with only 4 conditional branches the top-4 SET is always
    # complete -> trivial; the reading is the RANKED string, so the null statistic = positions that differ)
    diffs = []
    for _ in range(2000):
        c = mc.multinomial(M_REF, q_cond)
        o = np.argsort(c)[::-1][:4]
        diffs.append(int(np.sum(o != top)))
    d_band = int(np.quantile(diffs, 1.0 - ALPHA_3SIG))
    print(
        f"      predicted RANKED reading (top-4, 3-bit codec): {predicted!r}; null band (order-sensitive):"
    )
    print(
        f"        positions-differing mean {np.mean(diffs):.2f}, 3-sigma band <= {d_band}"
        f"  -> NON-NULL reading = more than {d_band} ranked positions differ"
    )
    print(
        f"      raw shots for the reading = M_ref/P(bit) = {M_REF/p_in:,.0f}   (REDUCED reading: the full"
    )
    print(
        "      64-branch K_min=6 reading needs dim=64 modes or a CX-feasible gate route -- declared future.)"
    )

    # ===== [5] write the pre-registration spec =====
    # the declared layer-1 target at this instance: eps=0.05 if the grid reached it, else eps=0.10 (computed)
    l1 = shots_needed.get(0.05) or shots_needed.get(0.10) or 20000
    per_config = max(l1, int(M_REF / p_in))
    total = (
        len(configs) * per_config
    )  # 5 configs (4 mains + the A1 hardware reference), layer1 + reading each
    spec = {
        "instance": {
            "n_qubits": N_JOB,
            "modes": DIM,
            "seed": demon_qc.SEED,
            "syk_T": drb.T,
            "input_text": INPUT_TEXT,
            "input_bit": bit,
            "phi0_candidates": PHI0S,
        },
        "decision_rules": {
            "layer1": {
                "test": "G vs the exact null, MC 3-sigma",
                "thresholds_by_shots": thresholds,
                "shots_for_90pct_power": {str(k): v for k, v in shots_needed.items()},
                "hardware_floor_escalation": (
                    "a main config's rejection counts as 'layer-1 anomaly (unmodeled)' ONLY if its G/dof"
                    f" >= {R_ESC} x the reference config's G/dof ({ref_key}, at matched shots); otherwise"
                    " it is classified 'hardware-consistent' (expected: ideal-null rejection from ~% mesh"
                    " error is mundane)"
                ),
            },
            "layer2": {
                "M_ref": M_REF,
                "predicted_reading": predicted,
                "ranked_positions_differ_band": d_band,
            },
            "corollary": "an anomaly CANNOT be attributed to the m_V axion (axion_photonic_chip: 16+ orders)",
        },
        "layer1_hardware_floor": {
            "reference_config": ref_key,
            "reference_seed": SEED_REF,
            "r_esc": R_ESC,
            "role": (
                "measure the hardware's mundane G-inflation on the same circuit class; n=1 reference ="
                " an order-of-magnitude floor (mesh error is config-dependent), declared honestly"
            ),
        },
        "declared_interpretation": {
            "obt_prediction": (
                "OBT itself predicts the NULL on this run: the priced channel inventory is closed"
                " (gravitational ~53 orders below floor [optimal_sensor_threshold]; m_V axion 16-18 orders"
                " [axion_photonic_chip]; radion quasi-static -> calibrated out; KK blockaded;"
                " chi-derivative = the m_V class, no resonance/magnet). Encoding the germe's FORM creates"
                " a REPLICA, not an entanglement (same-structure != entangled; no interaction Hamiltonian"
                " beyond the priced channels)."
            ),
            "what_this_run_tests": (
                "hardware fidelity to the declared unitary + unmodeled physics; it does NOT test OBT"
            ),
            "forbidden_readings": [
                "a NULL is not 'OBT survived a test'",
                "an anomaly is not attributable to OBT's bulk",
                "an anomaly is not attributable to the m_V axion (the point-E corollary)",
            ],
        },
        "amendments": [
            {
                "id": "A1",
                "date": "2026-07-11",
                "before_any_run": True,
                "summary": (
                    "hardware-reference config added (distinct declared seed, same circuit class);"
                    " layer-1 escalation requires G/dof >= R_ESC x the reference's G/dof"
                ),
            },
            {
                "id": "A2",
                "date": "2026-07-11",
                "before_any_run": True,
                "summary": (
                    "declared interpretation: OBT predicts the null; the run tests hardware + unmodeled"
                    " physics, NOT OBT; forbidden readings listed"
                ),
            },
        ],
        "configs": {
            k: {
                "unitary_re": v["u"].real.tolist(),
                "unitary_im": v["u"].imag.tolist(),
                "null_probs": v["p"].tolist(),
                "input_state": [1] + [0] * (DIM - 1),
            }
            for k, v in configs.items()
        },
        "budget": {
            "shots_per_config": per_config,
            "n_configs": len(configs),
            "total_shots": total,
            "eur_per_s": EUR_PER_S,
            "cost_eur_at_rate": {
                str(r): round(total / r * EUR_PER_S, 2) for r in (100, 1000, 10000)
            },
        },
        "submission": {
            "platform": args.platform,
            "note": "adjust platform id to the OVH/Quandela console",
        },
    }
    with open(SPEC_PATH, "w") as f:
        json.dump(spec, f)
    print(
        f"\n[5] PRE-REGISTRATION WRITTEN -> {SPEC_PATH} (unitaries + nulls + rules + A1/A2 amendments +"
        " budget; the job IS this file)"
    )
    print(
        f"      budget: {total:,} shots total ({len(configs)} configs x {per_config:,}); cost "
        + ", ".join(
            f"{v} EUR @{k}/s" for k, v in spec["budget"]["cost_eur_at_rate"].items()
        )
    )

    # ===== [6] Perceval: local SLOS dry-run (validation) + the real submission =====
    print(
        "\n[6] PERCEVAL — local SLOS dry-run (validates the mesh) + the QPU submission block"
    )
    try:
        import perceval as pcvl

        for name, cfg in configs.items():
            circ = pcvl.Circuit(DIM)
            circ.add(0, pcvl.Unitary(pcvl.Matrix(cfg["u"])))
            proc = pcvl.Processor("SLOS", circ)
            proc.with_input(pcvl.BasicState([1] + [0] * (DIM - 1)))
            res = pcvl.algorithm.Sampler(proc).probs()["results"]
            p_sim = np.zeros(DIM)
            for state, pr in res.items():
                p_sim[[state[i] for i in range(DIM)].index(1)] += float(pr)
            assert np.allclose(
                p_sim, cfg["p"], atol=1e-9
            ), f"SLOS dry-run == the exact null ({name})"
        print(
            f"      local SLOS dry-run: ALL {len(configs)} configs (4 mains + the A1 reference) reproduce"
            " the exact nulls (identity holds) ✓"
        )
        if args.token:
            print(f"      SUBMITTING to {args.platform} ({args.shots} shots/config)...")
            for name, cfg in configs.items():
                rp = pcvl.RemoteProcessor(args.platform, token=args.token)
                circ = pcvl.Circuit(DIM)
                circ.add(0, pcvl.Unitary(pcvl.Matrix(cfg["u"])))
                rp.set_circuit(circ)
                rp.with_input(pcvl.BasicState([1] + [0] * (DIM - 1)))
                rp.min_detected_photons_filter(1)
                job = pcvl.algorithm.Sampler(rp).sample_count.execute_async(args.shots)
                print(f"        {name}: job id {getattr(job, 'id', job)}")
            print(
                "      -> collect the counts, then compare to the spec's nulls with the layer-1/2 rules."
            )
        else:
            print(
                "      no --token: DRY-RUN ONLY (the submission block is ready; token + platform id come"
            )
            print(
                "      from the OVH/Quandela console; re-run with --token ... to submit)."
            )
    except ImportError:
        print(
            "      perceval not installed here -- the spec file still carries the full job (install"
        )
        print("      perceval-quandela and re-run for the dry-run + submission).")

    print(
        "\n[VERDICT] the belenos job is READY: 5 folded 8x8 unitaries (both germe candidates x Z/X + the"
    )
    print(
        "    A1 hardware-reference floor), ONE photon, deterministic mode-native mesh; exact nulls,"
    )
    print(
        "    3-sigma rules, reading bands, the A1 escalation rule and the A2 declared interpretation"
    )
    print(
        "    (OBT itself predicts the null -- the run tests hardware + unmodeled physics, NOT OBT) are"
    )
    print(
        "    pre-registered in the spec file; the gate route is quantitatively dead (why mode-native);"
    )
    print(
        "    submission = --token from the OVH console. Nothing presupposes the outcome; read it verbatim."
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
