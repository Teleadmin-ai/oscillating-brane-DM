"""Seed 3 (V9.0, quarantined) — BELENOS FEASIBILITY against the PUBLISHED hardware systematics (Oct 2026
reviewer reread, point 2: 'quelle deuxieme reference ?' + 'cherche quasiment l'impossible').

THE FACT THAT CHANGES THE PICTURE. Two independent 2026 groups have already run OUR configuration on Quandela's
Belenos and published the systematics (declared inputs below, with their sources):
  * arXiv:2606.18408 (Tully, Washburn, Simons): 8 logical modes of the 24-mode Belenos, ONE photon in mode 0,
    ~10,000 events per configuration, >340,000 detections; fixed-pattern balance bias rms 0.070 across the
    8 modes; per-point calibration offsets ~+-0.02; per-mode dump probability 0.140-0.237 vs ideal 0.125;
    session-dependent leakage floors 3.8%-12.4%; a recalibration episode (HOM visibility 90.7% -> 21.2%).
  * arXiv:2609.10216 (Wijesundara, Volpe, Stojkovic, Fotso, Thomay): Ascella + Belenos; output-port
    efficiency asymmetry 1.10; COMPILATION transmittance jitter sigma_tau = 0.026 PER CIRCUIT; 'compilation
    jitter costs a factor twenty and is not fundamental' (statistical floor 1.1e-3 -> bound 2.3e-2; that bound
    is on a deviation from the quantum partition law in the TWO-photon P(1,1) channel -- NOT a Sorkin kappa).
So 'the second reference' already exists: it is the published characterization of the same chip in the
same configuration. The Sorkin target is the best published quantum-regime bound, kappa < 2e-3 (summarized in
arXiv:2103.17209; 3e-5 with classical light). This script turns those numbers into consequences for our two
candidate runs.

THE HARDWARE MODEL (declared, scanned -- no single number imposed):
  * compilation jitter: every compiled circuit gets an independent unitary error U' = e^{i eps A} U e^{i eps B}
    (A, B GUE-random, eigenphase rms 1) -> eps = the rms rotation angle per mode. Anchors: 0.026 (the
    published per-element transmittance jitter) and 0.026*sqrt(8) = 0.074 (accumulated over an 8-mode mesh
    depth -- numerically close to the published 0.070 balance bias, reported not asserted).
  * output-port efficiencies: a FIXED pattern eta_m uniform in [1, ETA_ASYM] (shared by every circuit of a
    session), applied before the single-photon postselection (P(k | 1 detected) renormalizes over 8 ports).

WHAT IS COMPUTED:
 [1] the demon spec (belenos_job's 5 configs): P(layer-1 rejection) at 10k shots, and the FALSE-ALARM RATE of
     the A1 escalation rule ('anomaly' iff a main config REJECTS and G_main >= 3 G_ref) under pure hardware,
     i.e. no new physics.
 [2] a 3-path Sorkin (Born-rule) test realized mode-natively (blocked paths routed to dump modes, so every
     configuration is a lossless 8x8 unitary). kappa is measured PER DETECTOR (k = 0, 1, 2) and every quantity
     is kept per detector -- pooling the 3 detectors mixes biases of different size and sign (the Oct 2026
     reread catch). Computed: the ideal kappa = 0 identity (asserted), the statistical sigma_kappa vs shots,
     kappa_sys (rms AND mean) from compilation jitter and from the efficiency pattern, and the number J of
     independent recompilations (each a job of 10k shots: per-job variance = jitter^2 + statistics^2) needed to
     reach the best published single-photon bound (2e-3) GIVEN the coherent per-job bias b_k that does not
     average (the jitter bias + the kappa estimator's own O(1/shots) ratio bias, computed on 200k MC jobs): J_k
     = var_k / (target^2 - b_k^2), impossible when |b_k| >= target (J is reported only for a b_k resolved below
     the target at 2 se; it diverges at the target). A scan over declared alternative path phases + an
     ERROR-MODEL CHECK (the error placed INSIDE the mesh, 2 kinds) decide whether the clean detector is a
     DESIGN property (declarable in advance) or set by the unknown error.
 [3] the verdict + what a minimal run would still buy.

NOT V8.2. Not in the PDF. seul les calculs comptent: asserted only identities (kappa = 0 for ideal unitaries at
every scanned phase set, the internal-error model at zero error == the ideal configs, unitarity, normalization,
the null == belenos_job's spec nulls); the hardware model is declared and scanned.
"""

import json
import os
import warnings

import belenos_job as bj
import numpy as np
from scipy.linalg import expm
from scipy.sparse import SparseEfficiencyWarning

warnings.filterwarnings("ignore", category=SparseEfficiencyWarning)

DIM = 8
ETA_ASYM = 1.10  # output-port efficiency asymmetry (arXiv:2609.10216)
EPS_ANCHORS = {"published element jitter": 0.026, "accumulated over depth 8": 0.074}
EPS_SCAN = (0.003, 0.01, 0.026, 0.074)
N_SHOTS = 10_000  # belenos_job's declared shots per config (= the published ~10k events per config)
# best published quantum-regime (single photons / molecules) Sorkin bound, as summarized in arXiv:2103.17209
# (kappa < 2e-3 quantum regime; < 3e-5 with classical light)
KAPPA_BEST = 2e-3
# detected single photons per second: NOT published -> parametrized
RATES = (1e3, 1e4, 1e5)
EUR_PER_S = 0.28  # OVH Quantum Platform price for belenos, EUR per HT-second (as communicated by Romain)
MC = np.random.default_rng(20261007)
SPEC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "belenos_job_spec.json")


def gue(rng, d=DIM):
    a = rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))
    h = (a + a.conj().T) / 2.0
    w = np.linalg.eigvalsh(h)
    return h / np.sqrt(np.mean(w**2))  # eigenphase rms 1


def jitter(u, eps, rng):
    """One compiled realization: independent unitary errors before and after (eigenphase rms eps each)."""
    if eps == 0:
        return u
    return expm(1j * eps * gue(rng)) @ u @ expm(1j * eps * gue(rng))


def detected(p, eta):
    """Single-photon postselection with output-port efficiencies eta: P(k | exactly one photon detected)."""
    q = eta * p
    return q / q.sum()


def g_stat(counts, p):
    """G of one count vector vs the null p -- belenos_job's own statistic (one implementation for both)."""
    return float(bj.g_stats_batch(counts[None, :], p, counts.sum())[0])


def g_threshold(p, shots, alpha=bj.ALPHA_3SIG, draws=bj.MC_DECIDE):
    """The 3-sigma G threshold at belenos_job's DECIDING precision (MC_DECIDE null draws; 4000 draws, the
    first version, realize 0.55-2.3 alpha)."""
    null = bj.g_stats_batch(MC.multinomial(shots, p, size=draws), p, shots)
    return float(np.quantile(null, 1.0 - alpha))


# ------------------------------------------------------------------ the Sorkin configurations
PATHS, DUMPS = (0, 1, 2), (3, 4, 5)
SUBSETS = [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]
ALPHA_DECLARED = (0.0, 0.7, 1.9)  # declared path phases (any generic choice)
# declared alternative generic phase sets, scanned at the accumulated anchor
ALPHA_SCAN = ((0.0, 0.3, 2.5), (0.0, 1.2, 0.4), (0.0, 2.0, 4.0))


def sorkin_stages(alpha=ALPHA_DECLARED):
    """The 3 mesh stages (V, W, {S: P_S}): V splits mode 0 into the 3 paths (equal weight, path phases alpha),
    P_S routes every blocked path j to its dump mode j+3 (a swap: lossless 'blocking'), W = a 3-mode DFT
    recombining the paths onto detectors 0-2."""
    a = np.eye(DIM, dtype=complex)
    a[:, 0] = 0.0
    a[list(PATHS), 0] = np.exp(1j * np.array(alpha)) / np.sqrt(3.0)
    v, _ = np.linalg.qr(a)
    v[:, 0] *= np.vdot(v[:, 0], a[:, 0]) / abs(np.vdot(v[:, 0], a[:, 0]))
    w = np.eye(DIM, dtype=complex)
    w[:3, :3] = np.exp(2j * np.pi * np.outer(range(3), range(3)) / 3.0) / np.sqrt(3.0)
    perms = {}
    for s in SUBSETS:
        perm = np.eye(DIM)
        for j, d in zip(PATHS, DUMPS):
            if j not in s:
                perm[[j, d]] = perm[[d, j]]
        perms[s] = perm
    return v, w, perms


def sorkin_unitaries(alpha=ALPHA_DECLARED):
    """U_S = W . P_S . V: every U_S is an 8x8 unitary (mode-native, one photon, deterministic)."""
    v, w, perms = sorkin_stages(alpha)
    return {s: w @ perms[s] @ v for s in SUBSETS}


def internal_error_probs(alpha, eps, kind, rng):
    """One compiled realization with the error INSIDE the mesh, at the two cuts V | P_S | W: kind = 'gue'
    (a GUE rotation of eigenphase rms eps at each cut) or 'phase' (independent random phases of rms eps on
    every mode at each cut). Returns the 8-mode distribution of every config S."""
    v, w, perms = sorkin_stages(alpha)
    out = {}
    for s in SUBSETS:
        if kind == "gue":
            e1, e2 = expm(1j * eps * gue(rng)), expm(1j * eps * gue(rng))
        else:
            e1, e2 = (
                np.diag(np.exp(1j * eps * rng.standard_normal(DIM))) for _ in range(2)
            )
        out[s] = np.abs((w @ e2 @ perms[s] @ e1 @ v)[:, 0]) ** 2
    return out


def sorkin_kappa(probs):
    """probs[S] = 8-mode distribution of config S (last axis; leading axes = independent draws) -> kappa(k)
    for the detectors k = 0, 1, 2."""
    i = {s: probs[s][..., :3] for s in SUBSETS}
    eps3 = (
        i[(0, 1, 2)]
        - i[(0, 1)]
        - i[(0, 2)]
        - i[(1, 2)]
        + i[(0,)]
        + i[(1,)]
        + i[(2,)]
        - i[()]
    )
    delta = (
        np.abs(i[(0, 1)] - i[(0,)] - i[(1,)])
        + np.abs(i[(0, 2)] - i[(0,)] - i[(2,)])
        + np.abs(i[(1, 2)] - i[(1,)] - i[(2,)])
    )
    return eps3 / delta


def fmt3(x, f="{:.1e}"):
    """A per-detector triple, printed as 'k0 / k1 / k2'."""
    return " / ".join(f.format(v) for v in x)


def classify(b, se):
    """A detector's coherent bias vs the target, resolved at 2 standard errors."""
    if abs(b) + 2.0 * se < KAPPA_BEST:
        return "below"
    if abs(b) - 2.0 * se >= KAPPA_BEST:
        return "above"
    return "unresolved"


def main():
    print("=" * 100)
    print(
        " BELENOS FEASIBILITY — our runs against the PUBLISHED hardware systematics of the same chip"
    )
    print("=" * 100)
    print(
        "\n  declared inputs: arXiv:2606.18408 (same config: 1 photon, mode 0, 8 logical modes, ~10k/config)"
    )
    print(
        f"  + arXiv:2609.10216 (compile jitter 0.026/circuit, port asymmetry {ETA_ASYM}); best single-photon"
        f" Sorkin bound {KAPPA_BEST:.0e}"
    )

    # ===== [1] the demon spec under the hardware model =====
    with open(SPEC) as f:
        spec = json.load(f)
    cfgs = {}
    for name, c in spec["configs"].items():
        u = np.array(c["unitary_re"]) + 1j * np.array(c["unitary_im"])
        assert np.allclose(
            u @ u.conj().T, np.eye(DIM), atol=1e-9
        ), "unitarity of the spec configs"
        p = np.abs(u[:, 0]) ** 2
        assert np.allclose(
            p, c["null_probs"], atol=1e-12
        ), "identity: null == the spec's declared null"
        cfgs[name] = (u, p)
    ref_name = spec["layer1_hardware_floor"]["reference_config"]
    mains = [k for k in cfgs if k != ref_name]
    thr = {k: g_threshold(p, N_SHOTS) for k, (_, p) in cfgs.items()}
    print(
        f"\n[1] THE DEMON SPEC ({len(cfgs)} configs, {N_SHOTS} shots each) under pure hardware (NO new physics)"
    )
    print(
        "      eps      mean TV(ideal,hw)   P(layer-1 rejects | config)   A1 false alarm P(any main 'anomaly')"
    )
    # sessions per eps (binomial se on a ~0.2 rate: ~0.006; the first version's 400 gave ~0.02)
    trials = 4000
    rej_frac, alarm_frac = {}, {}
    for eps in EPS_SCAN:
        rej, tvs, alarms = [], [], 0
        for _ in range(trials):
            eta = MC.uniform(
                1.0, ETA_ASYM, DIM
            )  # one session = one fixed efficiency pattern
            g = {}
            for k, (u, p) in cfgs.items():
                q = detected(np.abs(jitter(u, eps, MC)[:, 0]) ** 2, eta)
                tvs.append(0.5 * float(np.abs(q - p).sum()))
                g[k] = g_stat(MC.multinomial(N_SHOTS, q), p)
                rej.append(g[k] > thr[k])
            alarms += any(
                g[k] > thr[k] and g[k] >= bj.R_ESC * g[ref_name] for k in mains
            )
        rej_frac[eps] = float(np.mean(rej))
        alarm_frac[eps] = alarms / trials
        a_se = np.sqrt(alarm_frac[eps] * (1.0 - alarm_frac[eps]) / trials)
        print(
            f"     {eps:5.3f}        {np.mean(tvs):.4f}                 {rej_frac[eps]:5.2f}"
            f"                          {alarm_frac[eps]:5.3f} +- {a_se:.3f}"
        )
    r_lo, r_hi = (rej_frac[e] for e in EPS_ANCHORS.values())
    a_lo, a_hi = sorted(alarm_frac[e] for e in EPS_ANCHORS.values())
    print(
        f"    => layer 1 rejects {r_lo:.0%} (element anchor) to {r_hi:.0%} (accumulated anchor) of the configs"
    )
    print("       on pure hardware: the A1 premise, confirmed;")
    print(
        f"       the A1 rule's FALSE-ALARM rate at the anchors is {a_lo:.0%}-{a_hi:.0%}: an 'unmodeled anomaly' flag that"
    )
    print(
        "       fires this often on pure hardware cannot certify anything. The n=1 reference is too thin."
    )

    # ===== [2] the Sorkin (Born-rule) test, mode-native, PER DETECTOR =====
    us = sorkin_unitaries()
    probs = {}
    for s, u in us.items():
        assert np.allclose(u @ u.conj().T, np.eye(DIM), atol=1e-12), "unitarity of U_S"
        probs[s] = np.abs(u[:, 0]) ** 2
        assert (
            abs(probs[s].sum() - 1.0) < 1e-12
        ), "dump routing keeps every config normalized"
    k_ideal = sorkin_kappa(probs)
    assert (
        np.max(np.abs(k_ideal)) < 1e-12
    ), "identity: Born rule -> kappa = 0 for ideal unitaries"
    print(
        f"\n[2] A 3-PATH SORKIN TEST, mode-native ({len(SUBSETS)} configs; blocked paths -> dump modes), PER DETECTOR"
    )
    print(
        f"      ideal unitaries: kappa = {np.max(np.abs(k_ideal)):.1e} (the Born identity holds)"
    )

    def kappa_stat(shots, draws=200_000):
        """ONE job of `shots` per config on ideal unitaries, `draws` MC jobs (vectorized), per detector: the
        statistical scatter, the ESTIMATOR bias and its MC se -- kappa = eps/delta is a ratio of noisy sums, so
        each job carries an O(1/shots) bias that does not average over recompilations.
        """
        ks = sorkin_kappa(
            {s: MC.multinomial(shots, probs[s], size=draws) / shots for s in SUBSETS}
        )
        sd = ks.std(axis=0)
        return sd, ks.mean(axis=0), sd / np.sqrt(draws)

    def kappa_sys(u_set, eps, eta_on, draws=400):
        """Per detector: rms, mean (= the coherent bias b_k) and the MC standard error of the mean."""
        ks = []
        for _ in range(draws):
            eta = MC.uniform(1.0, ETA_ASYM, DIM) if eta_on else np.ones(DIM)
            ks.append(
                sorkin_kappa(
                    {
                        s: detected(np.abs(jitter(u_set[s], eps, MC)[:, 0]) ** 2, eta)
                        for s in SUBSETS
                    }
                )
            )
        ks = np.array(ks)
        se = np.std(ks, axis=0) / np.sqrt(len(ks))
        return np.sqrt(np.mean(ks**2, axis=0)), np.mean(ks, axis=0), se

    print(
        "      statistics (200k MC jobs): shots/config   sigma_kappa (detector 0 / 1 / 2)"
        "    estimator bias (0 / 1 / 2)"
    )
    stat = {}
    for shots in (10_000, 100_000, 1_000_000):
        stat[shots] = kappa_stat(shots)
        print(
            f"                         {shots:9.0e}     {fmt3(stat[shots][0])}"
            f"    {fmt3(stat[shots][1], '{:+.1e}')}"
        )
    # ONE job of N_SHOTS per config: its scatter and its estimator bias (O(1/shots): only more shots per job
    # shrink it, recompilations do not)
    k_stat_job, b_stat, b_stat_se = stat[N_SHOTS]
    k_eta_rms, k_eta_mean, _ = kappa_sys(us, 0.0, True)
    print(
        f"      efficiency pattern alone (eta in [1,{ETA_ASYM}], perfect unitaries): kappa_sys rms {fmt3(k_eta_rms)}"
    )
    print(
        f"        (mean {fmt3(k_eta_mean, '{:+.1e}')}) -- static per session, needs calibrating out"
    )
    print(
        f"      compilation jitter (perfect efficiencies), per job of {N_SHOTS} shots (stat {fmt3(k_stat_job)}):"
    )
    print("        eps    kappa_sys rms (detector 0 / 1 / 2)")
    for eps in EPS_SCAN:
        print(f"        {eps:5.3f}   {fmt3(kappa_sys(us, eps, False)[0])}")
    print(
        f"      estimator bias per job of {N_SHOTS} shots: {fmt3(b_stat, '{:+.1e}')} (se {fmt3(b_stat_se)})"
        " -- added to the jitter bias below"
    )
    # the averaging premise: a SECOND-order (eps^2) jitter bias does not average down over recompilations, nor
    # does the estimator bias; only the random part does -> J_k = var_k / (target^2 - b_k^2) with b_k the
    # total per-job bias, impossible when |b_k| >= target
    print(
        f"      recompilations J to reach {KAPPA_BEST:.0e}, PER DETECTOR, given its per-job bias b_k (jitter: 30000-draw MC):"
    )
    below, bias, tot, var_by = {}, {}, {}, {}
    for label, eps_a in EPS_ANCHORS.items():
        k_rms, b_jit, b_jit_se = kappa_sys(us, eps_a, False, draws=30000)
        # the compilation-jitter bias alone (used by the phase scan + the error-model check below)
        bias[eps_a] = (b_jit, b_jit_se)
        # the coherent PER-JOB bias = jitter + estimator (additive to leading order; both are declared above)
        b, b_se = b_jit + b_stat, np.sqrt(b_jit_se**2 + b_stat_se**2)
        tot[eps_a] = (b, b_se)
        # the RANDOM part per job: jitter variance (rms^2 - mean^2) + statistics
        var_k = (k_rms**2 - b_jit**2) + k_stat_job**2
        var_by[eps_a] = var_k
        print(f"        eps = {eps_a} ({label}):")
        below[eps_a] = []
        for k in range(3):
            cls = classify(b[k], b_se[k])
            head = (
                f"          detector {k}: b = {b[k]:+.1e} +- {b_se[k]:.1e} (jitter {b_jit[k]:+.1e}"
                f" + estimator {b_stat[k]:+.1e}; {abs(b[k]) / KAPPA_BEST:.0%} of target; {cls} at 2 se)"
            )
            if cls == "below":
                below[eps_a].append(k)
            # J ~ 1/(target^2 - b^2) diverges at the target: a J is reported ONLY for a bias resolved below it
            if cls == "above":
                print(head + " -> IMPOSSIBLE: the bias alone exceeds the target")
                continue
            if cls == "unresolved":
                print(
                    head + " -> J UNDETERMINED: the bias is within 2 se of the target"
                )
                continue
            j = int(np.ceil(var_k[k] / (KAPPA_BEST**2 - b[k] ** 2)))
            n_tot = len(SUBSETS) * j * N_SHOTS
            costs = ", ".join(
                f"{EUR_PER_S * n_tot / r:,.0f} EUR @{r:.0e}/s" for r in RATES
            )
            print(head + f" -> J = {j:,} per config = {n_tot:.1e} shots at 10k/job")
            print(f"            cost: {costs} (+ per-job overhead, not modeled)")
    eps_acc = EPS_ANCHORS["accumulated over depth 8"]
    print(
        f"      PHASE SCAN at the accumulated anchor (eps = {eps_acc}, 30000 draws per set): signed b_k / target"
    )
    rows = [(ALPHA_DECLARED, "declared", *bias[eps_acc])]
    for alpha in ALPHA_SCAN:
        u_set = sorkin_unitaries(alpha)
        p_set = {s: np.abs(u_set[s][:, 0]) ** 2 for s in SUBSETS}
        assert (
            np.max(np.abs(sorkin_kappa(p_set))) < 1e-12
        ), "identity: kappa = 0 for ideal unitaries at every scanned phase set"
        rows.append(
            (alpha, "scanned", *kappa_sys(u_set, eps_acc, False, draws=30000)[1:])
        )
    ratios, n_below, n_none = [], 0, 0
    for alpha, tag, b, b_se in rows:
        cls = [classify(b[k], b_se[k]) for k in range(3)]
        ratios += list(np.abs(b) / KAPPA_BEST)
        n_below += cls.count("below")
        n_none += "below" not in cls
        print(
            f"        alpha = {alpha} ({tag}): {fmt3(b / KAPPA_BEST, '{:+.2f}')}  ({', '.join(cls)})"
        )
    print(
        f"        => over {len(ratios)} (phase set, detector) pairs |b_k|/target spans {min(ratios):.2f}-{max(ratios):.2f};"
        f" {n_below} resolved below it at 2 se;"
    )
    print(
        f"           phase sets with NO detector resolved below: {n_none} of {len(rows)}. WHICH detector is clean (if any)"
    )
    print("           moves with the phases.")
    # ERROR-MODEL CHECK: is the clean detector a property of the DESIGN (the phases) or of the error model?
    print(
        "      ERROR-MODEL CHECK (declared phases, accumulated anchor, 30000 draws each): signed b_k / target"
    )
    cls_wrap = [classify(*(x[k] for x in bias[eps_acc])) for k in range(3)]
    print(
        f"        GUE wrap (the declared model): {fmt3(bias[eps_acc][0] / KAPPA_BEST, '{:+.2f}')}"
        f"  ({', '.join(cls_wrap)})"
    )
    # the design question compares the JITTER bias across error models (the estimator bias is model-free)
    clean_sets = [{k for k in range(3) if cls_wrap[k] == "below"}]
    for kind, label in (
        ("gue", "GUE inside the mesh"),
        ("phase", "phases inside the mesh"),
    ):
        p0 = internal_error_probs(ALPHA_DECLARED, 0.0, kind, MC)
        assert all(
            np.allclose(p0[s], probs[s], atol=1e-12) for s in SUBSETS
        ), "identity: the internal-error model at zero error == the ideal configs"
        ks = np.array(
            [
                sorkin_kappa(internal_error_probs(ALPHA_DECLARED, eps_acc, kind, MC))
                for _ in range(30000)
            ]
        )
        b, b_se = ks.mean(axis=0), ks.std(axis=0) / np.sqrt(len(ks))
        cls = [classify(b[k], b_se[k]) for k in range(3)]
        clean_sets.append({k for k in range(3) if cls[k] == "below"})
        print(f"        {label}: {fmt3(b / KAPPA_BEST, '{:+.2f}')}  ({', '.join(cls)})")
    common = set.intersection(*clean_sets)
    print(
        f"        => detector(s) clean under all {len(clean_sets)} error models: {sorted(common) or 'none'}"
        + (
            " -> a DESIGN property (declarable in advance)"
            if common
            else " -> set by the unknown error model"
        )
    )
    print(
        "      (the bias is model-dependent in size, generic in kind: kappa is nonlinear in the probabilities)"
    )
    print(
        "      the session drift (published leakage floors 3.8%-12.4% between sessions) is COHERENT too: it does"
    )
    print(
        "      not average down -- every subset must be interleaved inside each session."
    )

    # ===== [3] verdict =====
    print("\n[VERDICT]")
    print(
        f"    * The demon run: layer 1 is DECIDED by the published hardware (it rejects {r_lo:.0%}-{r_hi:.0%} of the"
    )
    print(
        f"      configs); the A1 escalation rule false-alarms {a_lo:.0%}-{a_hi:.0%} of the time on pure hardware"
    )
    print("      (the anchors of [1]) -> no anomaly can be certified.")
    print(
        "      Its layer 2 is empty at 8 modes (A3). It buys ZERO science; it reproduces arXiv:2606.18408."
    )

    eps_el = EPS_ANCHORS["published element jitter"]
    # usable = clean by design (all 3 error models) AND J-feasible at both anchors with the TOTAL per-job bias
    decl = sorted(common & set(below[eps_el]) & set(below[eps_acc]))
    print(
        "    * The Sorkin 'quasi-impossible': systematics-limited by COMPILATION, exactly as 2609.10216 found;"
    )
    print(
        "      the coherent second-order bias is PER DETECTOR and moves with the path phases ([2] scan: at the"
    )
    print(
        f"      accumulated anchor |b_k| spans {min(ratios):.2f}-{max(ratios):.2f}x the target; phase sets with no clean"
        f" detector at all: {n_none} of {len(rows)})."
    )
    if decl:
        k = decl[0]
        j_el, j_acc = (
            int(np.ceil(var_by[e][k] / (KAPPA_BEST**2 - tot[e][0][k] ** 2)))
            for e in (eps_el, eps_acc)
        )
        j10 = int(np.ceil(var_by[eps_el][k] / (KAPPA_BEST / 10) ** 2))
        print(
            f"      With the declared phases detector {k} is clean at both anchors (GUE wrap) and under all 3 error"
        )
        print(
            "      models (accumulated anchor) -> a DESIGN property, declarable in advance. MATCHING the published"
        )
        print("      bound there is feasible in-model:")
        print(
            f"      J = {j_el:,}-{j_acc:,} recompilations per config, AFTER calibrating out the efficiency pattern (its"
        )
        print(
            f"      kappa rms is {k_eta_rms[k] / KAPPA_BEST:.1f}x the target on detector {k}) -- a platform replication, not"
            " a new bound."
        )
        print(
            f"      BEATING it 10x needs J >= {j10:,} per config even at zero bias ({len(SUBSETS) * j10 * N_SHOTS:.1e}"
            " shots), and a bias"
        )
        print(
            f"      resolved at {KAPPA_BEST / 10:.0e} (the MC resolves +-{2 * tot[eps_el][1][k]:.0e} at 2 se):"
            " a calibrated compiler"
        )
        print(
            "      bias model of the real chip, which no published characterization provides."
        )
    elif not common:
        print(
            "      With the declared phases no detector is clean under all 3 error models: WHICH detector is"
        )
        print(
            "      clean is set by the unknown compiler error -> it cannot be declared in advance."
        )
    else:
        print(
            f"      With the declared phases detector(s) {sorted(common)} are clean by design (all 3 error models),"
        )
        print(
            "      but their total per-job bias is not resolved below the target at both anchors -> no J."
        )
    print(
        "      Not competitive for a NEW bound on a programmable compiled mesh -- the physical multi-slit stays the"
    )
    print("      right tool.")
    check = 2000  # the A4 pipeline check: one config, 2k shots
    costs = ", ".join(
        f"{EUR_PER_S * check / r:.2f} EUR @{r:.0e}/s" for r in (1e2,) + RATES
    )
    print(
        f"    * What a minimal run still buys: ONE config, {check} shots -- measures OUR detection rate +"
    )
    print(
        "      billing and validates submission + retrieval. Cost at the unpublished rate:"
    )
    print(f"      {costs} (+ any per-job minimum, unpublished).")
    print(
        "      Nothing more is justified FOR OBT (a design-declared Sorkin run would be a separate, non-OBT project)."
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
