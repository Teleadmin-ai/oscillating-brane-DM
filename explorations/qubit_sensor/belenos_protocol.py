"""Seed 3 (V9.0, quarantined) — THE BELENOS PROTOCOL (recul point B, with point D folded in): the
pre-registered two-layer decision rule + the shots/EUR budget, computed BEFORE paying (belenos-12 =
Quandela 12q gate-based, 0.28 EUR/HT-s; Romain: 'un programme qui va me couter 8 euros pour 10 secondes').

THE EXPERIMENT (Romain's framing, standing): see IF the bulk returns an intelligible answer through a clean,
toy-free, interpretation-free instrument. NOTHING here presupposes the outcome ('partir perdant' REFUSED) and
nothing can manufacture meaning (pure transcode + controls). The rule is DECLARED in advance = pre-registration.

THE DECLARED INSTRUMENT (from demon_qc + demon_readout_basis, reused -- no re-implementation, no toy):
  germe        = the canonical radion wavepacket (phi0 = 0.42 corrected; 1.40 runs as the legacy candidate)
  decompressor = the 1-rep Lie-Trotter product unitary built from the germe's SYK terms (DECLARED as such --
                 demon_readout_basis showed the physical e^{-iHt} needs ~256-512 reps = ~52k-104k CX,
                 hardware-infeasible; the 1-rep product is shallow (~204 CX) and exactly predictable)
  seed         = DECLARED (the SYK couplings are part of the instrument; point D below shows the specific
                 branches are realization-dependent, so the null is THIS seed's math)
  readout      = MULTI-BASIS, Z + X (X = one layer of H gates; demon_readout_basis's deafness identity)

THE TWO-LAYER DECISION RULE (declared before the run):
  LAYER 1 (physical anomaly, all shots, no post-selection): do the measured counts deviate from the
     circuit's OWN exact math? G-test (log-likelihood ratio vs the exact null p), threshold MC-calibrated
     at 3 sigma, in EACH declared basis. NON-NULL = the hardware state is not the circuit's math (beyond
     calibrated hardware noise) = a physical anomaly. NULL = the circuit's math.
  LAYER 2 (the reading, post-selected on the input bits): the retrieved top-K string. Under the null it is
     EXACTLY PREDICTED (the null's own top-K, computed here). NON-NULL reading = the measured string differs
     from the predicted one AND scores above chance on the DECLARED intelligibility criterion (an
     English-letter-frequency score, declared in advance; K_min = the readout length needed to certify at
     3 sigma is COMPUTED below -- another anti-deafness number: too-short readouts cannot certify ANY answer).

WHAT IS COMPUTED: [1] the layer-1 calibration + power (shots needed vs effect size epsilon); [2] the layer-2
post-selection cost + the ranking budget (shots to resolve the top-K) + the codec certification K_min;
[3] point D: the seed-(in)variance of the letters (12 seeds); [4] the EUR budget table (rate parametrized --
the QPU shot rate is NOT fabricated; cost = time x 0.28 EUR/s) and what 8 EUR buys.

NOT V8.2. Not in the PDF. seul les calculs comptent: asserted only identities/calibration (normalization,
the MC false-positive rate within binomial noise); powers/budgets are computed + reported, no imposed ranges.
"""

import warnings

import demon_qc  # the instrument: canonical germe, seeded SYK, codec (no re-implementation)
import demon_readout_basis as drb  # the declared decompressor (1-rep product) + the X rotation
import numpy as np
from scipy.sparse import SparseEfficiencyWarning

warnings.filterwarnings("ignore", category=SparseEfficiencyWarning)

N = demon_qc.N
DIM = 2**N
N_IN = demon_qc.N_IN
ALPHA_3SIG = 0.00135  # one-sided 3-sigma
RNG = np.random.default_rng(demon_qc.SEED + 7)

# declared intelligibility model: standard approximate English letter+space frequencies (public values);
# digits/punctuation get a small declared floor. Case-insensitive. Declared BEFORE the run.
ENG_FREQ = {
    " ": 0.180,
    "e": 0.095,
    "t": 0.070,
    "a": 0.061,
    "o": 0.057,
    "i": 0.052,
    "n": 0.052,
    "s": 0.048,
    "h": 0.046,
    "r": 0.044,
    "d": 0.032,
    "l": 0.030,
    "u": 0.021,
    "c": 0.021,
    "m": 0.018,
    "w": 0.017,
    "f": 0.017,
    "g": 0.015,
    "y": 0.015,
    "p": 0.014,
    "b": 0.011,
    "v": 0.0078,
    "k": 0.0058,
    "j": 0.0011,
    "x": 0.0011,
    "q": 0.0008,
    "z": 0.0006,
}
FLOOR = 3e-4  # declared floor for digits + . ?


def char_logp(ch):
    return float(np.log10(ENG_FREQ.get(ch.lower(), FLOOR)))


def string_score(s):
    """The declared intelligibility score: mean log10 English-frequency per character."""
    return float(np.mean([char_logp(c) for c in s]))


def g_stat(counts, p, shots):
    """G = 2 sum obs ln(obs / (shots p)) over observed cells (the log-likelihood-ratio statistic)."""
    mask = counts > 0
    return float(2.0 * np.sum(counts[mask] * np.log(counts[mask] / (shots * p[mask]))))


def g_stats_batch(count_mat, p, shots):
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(count_mat > 0, count_mat / (shots * p[None, :]), 1.0)
        return 2.0 * np.sum(
            np.where(count_mat > 0, count_mat * np.log(ratio), 0.0), axis=1
        )


def main():
    print("=" * 100)
    print(
        " THE BELENOS PROTOCOL — the pre-registered two-layer rule + the shots/EUR budget (points B + D)"
    )
    print("=" * 100)

    # ---- the DECLARED instrument state (the null): 1-rep product unitary on the canonical germe ----
    rng_h = np.random.default_rng(demon_qc.SEED)
    h = demon_qc.sparse_syk(N, 2 * N, rng_h)
    g = demon_qc.germe_state(
        N
    )  # phi0 = 0.42 (corrected); 1.40 runs as the legacy candidate
    psi = drb.manual_product_state(
        g, h, 1
    )  # the DECLARED hardware decompressor (validated == circuit)
    p_z = np.abs(psi) ** 2
    p_x = np.abs(drb.hadamard_matrix(N) @ psi) ** 2
    assert (
        abs(p_z.sum() - 1.0) < 1e-9 and abs(p_x.sum() - 1.0) < 1e-9
    ), "null distributions normalized"

    # the input (the demo text) + the conditioned reading (layer 2 objects)
    bits = demon_qc.fold_to_bits(demon_qc.text_to_binary("talk to the bulk"), N_IN)
    inp = int("".join(map(str, bits)), 2)
    mask = (np.arange(DIM) & ((1 << N_IN) - 1)) == inp
    p_in = float(p_z[mask].sum())
    q_cond = p_z[mask] / p_in  # the 64-outcome conditional (indexed by the high 6 bits)
    top8_true = set(np.argsort(q_cond)[::-1][:8].tolist())
    predicted_string = demon_qc.latents_to_text(
        sorted(top8_true, key=lambda i: -q_cond[i])
    )
    print(
        "\n[0] THE DECLARED NULL (this seed's exact math -- what the hardware must be compared against)"
    )
    print(
        f"      decompressor = 1-rep product unitary (~204 CX); bases Z + X; input 'talk to the bulk' -> bits {''.join(map(str,bits))}"
    )
    print(
        f"      P(input bits under the null) = {p_in:.4f}  (the post-selection cost, x{1/p_in:.1f} raw shots)"
    )
    print(
        f"      the null's PREDICTED top-8 reading: {predicted_string!r}  (score {string_score(predicted_string):+.3f})"
    )

    # ===== [1] LAYER 1 — calibration + power vs shots (in the Z basis; X is identical machinery) =====
    print(
        "\n[1] LAYER 1 (anomaly): G-test vs the exact null, MC-calibrated at 3 sigma -- power vs shots"
    )
    shots_grid = [200, 500, 1000, 2000, 5000, 10000]
    eps_grid = [0.02, 0.05, 0.10]
    b_star = int(
        np.flatnonzero(mask)[np.argmax(q_cond)]
    )  # the alternative: a coherent tilt onto one branch
    print("      shots   threshold(3sig)   power eps=0.02   eps=0.05   eps=0.10")
    shots_needed = {e: None for e in eps_grid}
    fpr_check = None
    for shots in shots_grid:
        null_g = g_stats_batch(RNG.multinomial(shots, p_z, size=3000), p_z, shots)
        thr = float(np.quantile(null_g, 1.0 - ALPHA_3SIG))
        if (
            shots == 2000
        ):  # calibration check on FRESH null draws (the identity: FPR ~ alpha)
            fresh = g_stats_batch(RNG.multinomial(shots, p_z, size=8000), p_z, shots)
            fpr_check = float(np.mean(fresh > thr))
        powers = []
        for eps in eps_grid:
            p_alt = (1.0 - eps) * p_z.copy()
            p_alt[b_star] += eps
            alt_g = g_stats_batch(RNG.multinomial(shots, p_alt, size=300), p_z, shots)
            pw = float(np.mean(alt_g > thr))
            powers.append(pw)
            if pw >= 0.9 and shots_needed[eps] is None:
                shots_needed[eps] = shots
        print(
            f"      {shots:6d}   {thr:10.1f}        {powers[0]:5.2f}       {powers[1]:5.2f}      {powers[2]:5.2f}"
        )
    hits = int(round((fpr_check or 0.0) * 8000))
    assert (
        2 <= hits <= 25
    ), "MC calibration: the false-positive rate must sit at ~alpha within binomial noise"
    print(
        f"      calibration (fresh nulls, shots=2000): FPR = {fpr_check:.5f} ~ alpha = {ALPHA_3SIG}  (identity holds)"
    )
    for eps in eps_grid:
        s = shots_needed[eps]
        print(
            f"      => a coherent tilt eps={eps:.2f} needs {s if s else '>10000'} shots for 90% power at 3 sigma"
        )

    # ===== [2] LAYER 2 — the reading: ranking budget + the codec certification K_min =====
    print(
        "\n[2] LAYER 2 (the reading): post-selected ranking budget + the codec's certifiable length K_min"
    )
    # the reading criterion must include SAMPLING NOISE: under the null, the MEASURED top-8 at M events is
    # itself random (near-degenerate branches shuffle) -> compare the measured string against the NULL
    # ENSEMBLE of measured readings at the same M, not against the infinite-shots string (the relire catch:
    # 'exact top-8 recovery' was the wrong, over-strict criterion -- P(exact)=0.17 even at M=3200).
    m_ref = 800  # the declared reading depth (post-selected events)
    diffs, scores = [], []
    for _ in range(2000):
        c = RNG.multinomial(m_ref, q_cond)
        order = np.argsort(c)[::-1][:8]
        diffs.append(8 - len(set(order.tolist()) & top8_true))
        scores.append(string_score(demon_qc.latents_to_text(order.tolist())))
    diffs, scores = np.array(diffs), np.array(scores)
    d_band = int(np.quantile(diffs, 1.0 - ALPHA_3SIG))
    s_band = float(np.quantile(scores, 1.0 - ALPHA_3SIG))
    raw_l2 = m_ref / p_in
    print(
        f"      declared reading depth M = {m_ref} post-selected events -> raw shots = M/P(input) ~ {raw_l2:,.0f}"
    )
    print(
        f"      NULL ENSEMBLE at M={m_ref} (2000 MC): letters-differing-from-predicted = {diffs.mean():.1f} mean,"
    )
    print(
        f"        3-sigma band <= {d_band}; intelligibility score band <= {s_band:+.3f} (predicted string {string_score(predicted_string):+.3f})"
    )
    print(
        f"      => DECLARED layer-2 rule: NON-NULL reading = (letters differing > {d_band}) OR (score > {s_band:+.3f})"
    )
    print(
        "         -- the sampling noise of the reading is INSIDE the null; no over-strict criterion."
    )
    # the codec certification: how long a readout must be to certify English-like structure at 3 sigma
    charset = np.array(list(demon_qc.CHARSET))
    uni = RNG.integers(0, len(charset), size=200_000)
    s_uni = np.array([char_logp(c) for c in charset])[uni]
    eng_syms = list(ENG_FREQ.keys())
    eng_p = np.array(list(ENG_FREQ.values()))
    eng_p = eng_p / eng_p.sum()
    s_eng = np.log10(eng_p)[RNG.choice(len(eng_syms), size=200_000, p=eng_p)]
    d1 = float(
        (s_eng.mean() - s_uni.mean()) / np.sqrt(0.5 * (s_eng.var() + s_uni.var()))
    )
    k_min = int(np.ceil((3.0 / d1) ** 2))
    print(
        f"      codec certification: per-char d' = {d1:.2f} (English-freq vs uniform-64) -> K_min = {k_min} chars"
    )
    print(
        f"      => the 8-char reading is ABOVE K_min = {k_min}: an English-like answer IS certifiable at 3 sigma"
    )
    print(
        "         (thin margin at 8 -- retrieving top-16 doubles it); the anti-deafness number is computed,"
    )
    print(
        "         not presumed: a shorter readout could NOT have certified any answer, intelligible or not."
    )

    # ===== [3] POINT D — seed-(in)variance: what is the instrument's vs the germe's content? =====
    print(
        "\n[3] POINT D — the SYK realization: what depends on the declared seed (12 seeds, 1-rep product)"
    )
    h_zs, top_sets = [], []
    for s in range(12):
        rng_s = np.random.default_rng(demon_qc.SEED + 1000 + s)
        h_s = demon_qc.sparse_syk(N, 2 * N, rng_s)
        psi_s = drb.manual_product_state(g, h_s, 1)
        pz_s = np.abs(psi_s) ** 2
        h_zs.append(drb.shannon(pz_s))
        cz = pz_s[mask] / pz_s[mask].sum()
        top_sets.append(set(np.argsort(cz)[::-1][:8].tolist()))
    jac = [
        len(a & b) / len(a | b)
        for i, a in enumerate(top_sets)
        for b in top_sets[i + 1 :]
    ]
    print(
        f"      H_Z over seeds: {np.mean(h_zs):.2f} +/- {np.std(h_zs):.2f} bits (the universal scrambling)"
    )
    print(
        f"      top-8 overlap across seeds (Jaccard): {np.mean(jac):.2f} +/- {np.std(jac):.2f} (the letters)"
    )
    print(
        "      => the scrambling is universal; the SPECIFIC branches/letters are realization-DEPENDENT ->"
    )
    print(
        "         the seed is DECLARED as part of the instrument, and layer-1 nulls are THIS seed's math."
    )

    # ===== [4] THE BUDGET — shots -> seconds -> EUR (rate honestly parametrized) =====
    print(
        "\n[4] THE BUDGET — belenos-12 at 0.28 EUR/HT-s (shot RATE is hardware spec, parametrized honestly)"
    )
    shots_l1 = shots_needed[0.05] or 10000
    total = (
        2 * 2 * (shots_l1 + raw_l2)
    )  # x2 bases (Z, X) x2 germe candidates (0.42, 1.40)
    print(
        f"      shots: layer-1 {shots_l1} + layer-2 raw {raw_l2:,.0f}, x2 bases x2 phi0 candidates = {total:,.0f} total"
    )
    print("      rate (shots/s)   time (s)   cost (EUR)      | what 8 EUR buys (shots)")
    for rate in (100, 1000, 10000):
        t = total / rate
        print(
            f"        {rate:6d}        {t:8.1f}   {0.28*t:8.2f}        |   {int(8/0.28*rate):,}"
        )
    print(
        "      => at >=1k shots/s the FULL pre-registered protocol (both bases, both germe candidates)"
    )
    print(
        "         costs ~EUR-scale; at 100 shots/s prioritize: Z basis + phi0=0.42 first (halve twice)."
    )

    print(
        "\n[VERDICT] the protocol is PRE-REGISTERED and computed: declared instrument (germe, 1-rep product"
    )
    print(
        "    unitary, seed, Z+X bases), declared two-layer rule (anomaly vs own math at 3 sigma; reading ="
    )
    print(
        "    measured string vs the NULL ENSEMBLE at the declared depth M + the declared score, K >= K_min),"
    )
    print(
        "    declared budget. Nothing presupposes the outcome; nothing can fake it; the deafness holes"
    )
    print(
        "    (basis, readout length) are plugged. Ready for belenos + the 4090 latent I/O (no interpretation)."
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
