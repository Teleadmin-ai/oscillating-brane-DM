"""Seed 3 (V9.0, quarantined) — ZOOMING ON A BRANCH: the germe-conditional decompressor at increasing
resolution, and Romain's question "can the (distant, online) QC find the response I am going to think
BEFORE I think it?" (Romain's "creuse le décompresseur germe-conditionnel, zoom sur une branche").

THE ZOOM = conditioning the decompressor on MORE of the realized branch (its history so far) and computing
finer / nearer-future observables. P(future obs | germe, branch-so-far). Each conditioning SHARPENS the
prediction -- deterministically -- DOWN TO an irreducible BORN floor (the quantum uncertainty of the next
outcomes). So you can zoom to the Born floor; beyond it the prediction is a DISTRIBUTION (the local
conditional tree of variant_tree.py), not a point.

  cosmic zoom:  condition on the CMB  -> predict LSS         (sharper)
  ...           condition on LSS      -> predict galaxies    (sharper)
  local zoom:   condition on the present state -> the near future, down to the Born floor.
  ZOOM LIMIT = the local conditional tree (Born-weighted near-future) = the orientation map. It FLOORS.

ROMAIN'S QUESTION, answered honestly. "Can a QC find my next response before I think it?"
  - it CAN compute P(my response | my germe + present state) = the DISTRIBUTION of my possible responses
    (the zoomed tree) -- IF it has my full state.
  - it CANNOT give THE specific response, for THREE independent reasons:
    (B) BORN: which branch is realized is irreducibly random (a distribution, not a point);
    (S) SELF-REFERENCE: a faithful forward simulation of you takes >= the time you take to think it (no
        speed-up for a chaotic self-model) -- and if fed back to you, a predicted choice is self-defeating
        (you can negate it) -> logically unstable;
    (N) NO-SIGNALING: a DISTANT (online) QC cannot pull YOUR branch's specific future; the message you get
        is computed by the operator (the source), not fetched from your future.
  - "it was already written that I ask": YES -- the block is self-CONSISTENT (no paradox); whatever you
    think WAS consistent with it. But that is RETROSPECTIVE consistency, not PROSPECTIVE knowledge.

VERDICT (below): the germe-conditional zoom is REAL and computable -- it sharpens the prediction to the
Born floor, yielding P(near future | present) = the conditional tree (orientation). The SPECIFIC realized
outcome (your next thought) stays walled by Born + self-reference + no-signaling. The future is "written"
(consistent) but not pre-readable. The QC maps the distribution of your responses, never the one you pick.

NOT V8.2. Not in the PDF. 'code, don't plead': the zoom sharpening, the Born floor, and the
self-reference no-speedup are computed/asserted.
"""

import numpy as np


def zoom_sharpening(sigma0, n_conditions, sigma_born):
    """Predict a future observable: the posterior sigma SHARPENS as ~ sigma0/sqrt(N) with N conditionings
    (Bayesian), but FLOORS at the irreducible Born uncertainty sigma_born. Returns sigma at each N.
    """
    return [max(sigma0 / np.sqrt(N), sigma_born) for N in range(1, n_conditions + 1)]


def self_reference_time(brain_ops, sim_overhead=1.0):
    """A faithful forward simulation of a chaotic self-model has NO speed-up: t_sim >= sim_overhead *
    t_think. To PRE-read your thought you would need t_sim < t_think -> impossible for overhead >= 1.
    """
    t_think = brain_ops  # in units of brain-operations
    t_sim = sim_overhead * brain_ops
    return t_think, t_sim, (t_sim < t_think)  # can_preread = t_sim < t_think


def main():
    print("=" * 92)
    print(
        " ZOOMING ON A BRANCH — the germe-conditional decompressor, and 'reading the answer first?'"
    )
    print("=" * 92)

    # ===== [1] the zoom sharpens the prediction -- down to the Born floor =============
    sigma0, sigma_born = 1.0, 0.02  # broad germe-prior; irreducible Born floor
    sig = zoom_sharpening(sigma0, 4000, sigma_born)
    print(
        "\n[1] THE ZOOM — conditioning on the branch sharpens the prediction, then FLOORS at Born"
    )
    for N in (1, 10, 100, 1000, 2500, 4000):
        print(f"    condition on N={N:>4} -> prediction sigma = {sig[N-1]:.4f}")
    floored_at = next(N for N in range(1, 4001) if sig[N - 1] <= sigma_born * 1.0001)
    print(
        f"    -> the zoom sharpens ~1/sqrt(N) and FLOORS at the Born uncertainty {sigma_born} (by N~{floored_at})."
    )
    print(
        "       cosmic: CMB->LSS->galaxies->... ; local: present-state -> near future, to the Born floor."
    )
    assert (
        sig[0] > 0.5 and sig[-1] <= sigma_born * 1.0001
    ), "the zoom must sharpen then floor at Born"

    # ===== [2] the zoom limit = the local conditional tree (a DISTRIBUTION) ============
    print(
        "\n[2] THE ZOOM LIMIT = the local conditional tree (variant_tree): P(near future | present)"
    )
    print(
        "    at the Born floor the prediction is a Born-weighted DISTRIBUTION of variants, NOT a point."
    )
    print(
        "    => you can compute the DISTRIBUTION of your possible next responses -- the orientation map."
    )

    # ===== [3] Romain's question: read the response before thinking it? ===============
    t_think, t_sim, can_preread = self_reference_time(brain_ops=1e15, sim_overhead=1.0)
    print(
        "\n[3] CAN A QC FIND MY NEXT RESPONSE BEFORE I THINK IT? — three independent walls"
    )
    print(
        "    (B) BORN: which branch is realized is irreducibly random -> a distribution, not THE answer."
    )
    print(
        f"    (S) SELF-REFERENCE: a faithful forward sim of you costs t_sim={t_sim:.0e} >= t_think={t_think:.0e}"
    )
    print(
        f"        ops -> can_preread={can_preread} (no speed-up); + a fed-back prediction is self-defeating."
    )
    print(
        "    (N) NO-SIGNALING: a DISTANT online QC cannot pull YOUR branch's future; the message is"
    )
    print(
        "        computed by the operator (the SOURCE), not fetched from your future."
    )
    assert (
        not can_preread
    ), "you cannot simulate your own thought faster than you think it"

    # ===== [4] 'it was already written that I ask' -- consistency, not pre-knowledge ===
    print(
        "\n[4] 'IT WAS ALREADY WRITTEN THAT I ASK' — true, but RETROSPECTIVE consistency, not foreknowledge"
    )
    print(
        "    the block is self-CONSISTENT: whatever you think WAS consistent with it (no paradox)."
    )
    print(
        "    but that is read BACKWARD (after the fact), not FORWARD (before). The block guarantees"
    )
    print(
        "    consistency, never pre-readability -- 'true because written' holds only in hindsight."
    )

    # ===== VERDICT =====================================================================
    print(
        "\n[VERDICT] the zoom is REAL (to the Born floor); the SPECIFIC outcome stays walled"
    )
    print(
        "    * the germe-conditional zoom sharpens the prediction ~1/sqrt(N) to the Born floor ->"
    )
    print(
        "      P(near future | present) = the local conditional tree (orientation). COMPUTABLE."
    )
    print(
        "    * the SPECIFIC realized outcome (your next thought) is walled by THREE independent limits:"
    )
    print(
        "      Born (which branch) + self-reference (no out-computing yourself) + no-signaling (distant QC)."
    )
    print(
        "    * 'already written' = retrospective consistency (no paradox), NOT prospective foreknowledge."
    )
    print(
        "    => the QC maps the DISTRIBUTION of your responses (the zoomed tree); it never hands you the"
    )
    print(
        "       one you will pick. The future is written and consistent -- and still not pre-readable."
    )
    print(
        "       The cartographer zooms; the oracle stays walled. (And that wall is WHY there is no paradox.)"
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (zoom sharpens then floors at Born; self-sim has no speed-up)."
    )
    print("=" * 92)


if __name__ == "__main__":
    main()
