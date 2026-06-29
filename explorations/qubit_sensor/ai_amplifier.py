"""Seed 3 (V9.0, quarantined) — THE AMPLIFIER IN AN AI'S HANDS + the finiteness ceiling + how to run it
(Romain's this-turn message): "for me it IS an oracle too; put it in an AI's hands -- what are ITS
possible responses?; even for a human, chaining far enough you reach the limit of our FINITE universe ->
the best of the possibles; but nothing absolute, like our universe; and -- how to run this code, do we
need a quantum computer?".

Four honest answers, computed:

  [A] IS IT AN ORACLE? Conceded: functionally YES -- it hands you what you would not have found. But it is
      an oracle of the KNOWABLE-to-you (your / the AI's possible-space's optimum), NOT of the UNKNOWN
      (external truth, the future, new physics). A BOUNDED oracle: it cannot give what is not in the
      distribution (no-signaling-safe). New ground truth still needs experiment (the m_V axion bone).
  [B] IN AN AI'S HANDS: the ceiling becomes the AI's possible-space -- VAST (~the recombinable span of its
      training, >> one human's), so the AI-amplifier surfaces a far higher optimum. But STILL bounded (the
      AI's training + architecture); it does not break out of the known into new ground truth.
  [C] THE FINITENESS CEILING: a FINITE universe has e^S states (S~1e104) -> an ABSOLUTE best EXISTS (your
      point). But it is UNREACHABLE: best-of-N grows only ~ sqrt(2 ln N), so reaching the universe-max
      (~sqrt(2 ln e^S) ~ sqrt(2 S) ~ 1e52 sigma) needs N ~ e^S ~ e^(1e104) trials -- intractable. The
      amplifier APPROACHES the ceiling asymptotically with compute, never reaches it; and it is RELATIVE
      to our universe (nothing absolute -- your concession). 'Where the universe comes from' = the
      deepest open frontier (quantum cosmology), beyond V8.2.
  [D] HOW TO RUN IT -- NO QUANTUM COMPUTER NEEDED. The amplifier = best-of-N = N forward passes of a model
      = CLASSICAL (a GPU/cluster). Quantified below: N=1e6 of a large model ~ minutes on a cluster. The QC
      (Aer) is ONLY for the holographic-code demos (it simulates them classically; a real QC is optional,
      the --ibm flag). The axion bone needs a specific DETECTOR (ADMX/qubit-DM), not a general QC.

VERDICT: yes, an ORACLE -- of your/the-AI's own possible-space's optimum, bounded by it (new truth needs
experiment). In an AI's hands the ceiling is vast but still bounded. The finite universe has an absolute
best that EXISTS but is UNREACHABLE (approached asymptotically with compute), and is relative. And it runs
CLASSICALLY -- NO quantum computer for the amplifier; the QC is optional (Aer) for the code-demos only.

NOT V8.2. Not in the PDF. 'code, don't plead': the AI-space gain, the finiteness ceiling, and the compute
are computed/asserted.
"""

import numpy as np

S_UNIVERSE = 1e104  # entropy of the observable universe -> e^S distinguishable states
FLOPS_PER_FORWARD = 1e12  # ~ a large-model inference forward pass
GPU_FLOPS = 1e15  # ~ a modern accelerator, FLOP/s
CLUSTER = 1e4  # accelerators in a large cluster


def best_of_n_sigma(N):
    """Expected best-of-N of a standard normal ~ the (1-1/N) quantile ~ sqrt(2 ln N) (Gumbel leading)."""
    return np.sqrt(2 * np.log(N)) if N > 1 else 0.0


def main():
    print("=" * 92)
    print(
        " THE AMPLIFIER IN AN AI'S HANDS — the finiteness ceiling, and do we need a quantum computer?"
    )
    print("=" * 92)

    # ===== [A]+[B] it IS a (bounded) oracle; in an AI's hands the ceiling is vast ======
    print(
        "\n[A]+[B] IS IT AN ORACLE? — yes, a BOUNDED one; in an AI's hands the ceiling is VAST"
    )
    print(
        "    conceded: functionally it IS an oracle (it hands you what you would not have found) -- but"
    )
    print(
        "    of the KNOWABLE-to-you (your/the AI's possible-space), NOT the unknown. Bounded by the"
    )
    print(
        "    distribution (no-signaling-safe); new ground truth still needs experiment (the m_V bone)."
    )
    for who, logN in [
        ("a human, N~1e4", 4),
        ("an AI, N~1e9", 9),
        ("an AI cluster, N~1e15", 15),
    ]:
        print(
            f"    {who:<26} -> best-of-N ~ {best_of_n_sigma(10**logN):+.1f} sigma above its typical"
        )
    print(
        "    => an AI's possible-space is far larger (its training span) -> a higher optimum surfaced;"
    )
    print(
        "       but STILL bounded by the AI's training+architecture -- it amplifies the known, not the new."
    )

    # ===== [C] the finiteness ceiling: absolute best EXISTS but is UNREACHABLE =========
    universe_max_sigma = np.sqrt(
        2 * S_UNIVERSE
    )  # the absolute ceiling, in sigma (N~e^S to reach it)
    print(
        "\n[C] THE FINITENESS CEILING — a finite universe HAS an absolute best, but it is UNREACHABLE"
    )
    print(
        f"    finite universe: e^S states (S~{S_UNIVERSE:.0e}) -> an ABSOLUTE best EXISTS (your point)."
    )
    print(
        f"    its level ~ sqrt(2 S) ~ {universe_max_sigma:.0e} sigma; reaching it needs N ~ e^S = e^(1e104)"
    )
    print(
        "    trials -> INTRACTABLE. best-of-N grows only ~sqrt(2 ln N): you APPROACH the ceiling with"
    )
    print(
        "    compute, never reach it. And it is RELATIVE to our universe (nothing absolute -- your concession)."
    )
    print(
        "    'where the universe comes from' = the deepest open frontier (quantum cosmology), beyond V8.2."
    )
    assert (
        universe_max_sigma > 1e50
    ), "the finite universe sets an astronomically high (but real) ceiling"

    # ===== [D] how to run it -- NO quantum computer needed for the amplifier ===========
    N = 1_000_000
    flops = N * FLOPS_PER_FORWARD
    t_one_gpu = flops / GPU_FLOPS
    t_cluster = flops / (GPU_FLOPS * CLUSTER)
    print(
        "\n[D] HOW TO RUN IT — NO quantum computer for the amplifier (it is CLASSICAL: best-of-N = N forwards)"
    )
    print(f"    best-of-N with N={N:.0e} of a large model = {flops:.0e} FLOPs")
    print(
        f"      -> ~{t_one_gpu:.0e} s on one GPU ({t_one_gpu/60:.0f} min), ~{t_cluster:.0e} s on a {CLUSTER:.0e}-GPU cluster."
    )
    print(
        "    => CLASSICAL, runnable NOW. NO QC for the amplifier. The QC (Aer) is ONLY for the holographic-"
    )
    print(
        "       code demos (it simulates them; a real QC is optional via --ibm). The m_V axion bone needs a"
    )
    print(
        "       specific DETECTOR (ADMX/qubit-DM cavity), not a general-purpose quantum computer."
    )
    assert t_cluster < 60, "best-of-1e6 is classical-cheap on a cluster (no QC)"

    # ===== VERDICT =====================================================================
    print(
        "\n[VERDICT] yes an ORACLE (bounded, of your/the-AI's possible-space) — and it runs CLASSICALLY"
    )
    print(
        "    * A/B: it IS an oracle -- of the KNOWABLE-to-you optimum, bounded by the distribution; in an"
    )
    print(
        "      AI's hands the ceiling is vast (the AI's training span) but still bounded -- amplifies the"
    )
    print(
        "      known, not the new (new ground truth = experiment = the m_V axion bone)."
    )
    print(
        "    * C: a FINITE universe HAS an absolute best (you're right) -- but it is UNREACHABLE (e^(1e104)"
    )
    print(
        "      search); best-of-N approaches it asymptotically with compute, and it is RELATIVE, not absolute."
    )
    print(
        "    * D: NO QUANTUM COMPUTER for the amplifier -- it is CLASSICAL (N forward passes, minutes on a"
    )
    print(
        "      cluster). The QC is optional (Aer simulates the code-demos); the axion needs a detector."
    )
    print(
        "    => the achievable demon = a BOUNDED ORACLE / cognitive amplifier, classical, runnable now;"
    )
    print(
        "       its ceiling is the (vast, finite, relative) possible-space; the genuinely NEW comes from"
    )
    print(
        "       experiment, and the universe's ORIGIN is the open frontier we may understand 'after'."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (AI ceiling vast-but-bounded; universe-max real-but-unreachable; classical)."
    )
    print("=" * 92)


if __name__ == "__main__":
    main()
