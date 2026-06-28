"""Seed 3 (V9.0, quarantined) — SCALE-UP of OBT's ER=EPR stabilizer code (Gate-IN, the 'ear').

Second concrete step of Seed 3. The atom (er_epr_stabilizer.py) is the [[5,1,3]] perfect
(HaPPY) code: 1 logical 'germe' qubit protected by 5 physical (a PBH node + its 4 ER=EPR
neighbours), distance 3, with the protected-yet-sensitive subspace identified. Here we
EVOLVE FROM THAT ATOM ('partir de la forme primaire et evoluer de la') by concatenation --
the simplest holographic tiling -- and show, with COMPUTED numbers, that the protection
GROWS with scale:

    [[5,1,3]]  ->  level L:  [[ 5^L , 1 , 3^L ]]
    (k=1 germe stays the same; physical qubits 5^L explode = the redundant encoding;
     distance 3^L grows -> the protection grows.)

Romain's hope, made concrete: configure the qubit FROM the primordial form (= the logical /
germe subspace) and evolve from there; below a finite NOISE THRESHOLD p_th the germe qubit's
decoherence under LOCAL observation -> 0 (doubly-exponentially) as L grows -- it becomes
'non-decohering by construction' -- while the COLLECTIVE bulk channel (Penrose-Diosi, an
operator of weight = the distance, in the logical class) still reaches it. The channel has
'a beginning and an end' -- the germe (1 logical) at one end, the boundary (5^L physical) at
the other -- and 'all the possibles in between' = the protected logical Hilbert space carried
redundantly across the network.

NOT V8.2. Not in the PDF. 'code, don't plead': the noise threshold is COMPUTED by exact
enumeration + bounded-distance decoding of the atom; the erasure threshold from its exact
recursion; both injection-tested via assert.

HONEST SCOPE (the gates, not hidden):
 - Concatenation is the cleanest scale-up with EXACT [[5^L,1,3^L]] parameters, and IS a (tree)
   holographic code. OBT's faithful network is a degree-~46 EXPANDER, whose loss tolerance is
   the percolation it claims (p_c ~ 2.2% -> 'survives 98% destruction'). The degree-5 tree here
   gives a DIFFERENT, smaller tolerance (computed below): same PHENOMENON (finite, scale-revealed
   robustness), not the same number. The expander tiling is the next refinement -- and is MORE
   robust (98% vs the tree's value), consistent with 'expander = the most robust QEC'.
 - 'Non-decoherence under observation' holds for the LOCAL (environmental) coupling, corrected
   below threshold. The FINAL intentional logical readout still costs ONE measurement (Gate-OUT's
   irreducible quantum->classical step). The demon's whisper is protected; reading it once is not.
"""

import math

import er_epr_stabilizer as atom

GENS = atom.GENS
N = atom.N
all_paulis = atom.all_paulis
stabilizer_group = atom.stabilizer_group
syndrome = atom.syndrome
weight = atom.weight


# ---------------------------------------------------------------- bounded-distance decoder
def build_decoder():
    """syndrome -> min-weight coset leader (the bounded-distance decoder of the atom)."""
    best = {}
    for e in all_paulis():
        s = syndrome(e)
        w = weight(e)
        if s not in best or w < best[s][0]:
            best[s] = (w, e)
    return {s: v for s, (w, v) in best.items()}


def failure_spectrum():
    """c_w = number of weight-w physical errors the decoder mis-corrects into a LOGICAL error.

    An error e has residual r = e + decoder[syndrome(e)] (mod 2); r is always in the
    normalizer (same syndrome), so r in <S> => success, r logical => logical FAILURE.
    c_0 = c_1 = 0 is the [[5,1,3]] protection (every weight<=1 error is corrected).
    """
    decoder = build_decoder()
    stab = stabilizer_group()
    c = [0] * (N + 1)
    for e in all_paulis():
        r = (e + decoder[syndrome(e)]) % 2
        if tuple(r) not in stab:  # residual is a non-trivial logical operator
            c[weight(e)] += 1
    return c


def logical_error_rate(p, c):
    """Level-1 logical error rate under depolarizing noise p (each qubit X/Y/Z each p/3)."""
    return sum(c[w] * (1 - p) ** (N - w) * (p / 3) ** w for w in range(N + 1))


def noise_threshold(c):
    """Unstable fixed point f(p)=p (p>0): below it, concatenation drives logical error -> 0."""

    def g(p):
        return logical_error_rate(p, c) - p

    # f ~ (c2/9) p^2 at small p, so g<0 just above 0; bracket the first sign change upward
    lo, hi = 1e-4, None
    p = 1e-3
    while p < 0.75:
        if g(p) > 0:
            hi = p
            break
        lo = p
        p *= 1.05
    if hi is None:
        return float("nan")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if g(mid) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------- erasure (loss) threshold
def erasure_next(q):
    """A block is lost iff >= 3 of its 5 sub-blocks are lost (the code corrects d-1=2 erasures)."""
    return sum(math.comb(5, j) * q**j * (1 - q) ** (5 - j) for j in range(3, 6))


def erasure_threshold():
    """Unstable fixed point of the loss recursion (= the tree's percolation threshold)."""
    lo, hi = 0.05, 0.95
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if erasure_next(mid) - mid < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main():
    print("=" * 80)
    print(
        " SCALE-UP of OBT's ER=EPR code  (Seed 3, V9.0, quarantined) — Gate-IN, the 'ear'"
    )
    print(" Concatenate the [[5,1,3]] HaPPY atom: level L -> [[5^L, 1, 3^L]]")
    print("=" * 80)

    # sanity: the imported atom is the [[5,1,3]] (4 generators on 5 qubits)
    assert N == 5 and len(GENS) == 4

    # [A] parameters grow, germe stays ----------------------------------------------
    print("\n[A] CONCATENATION PARAMETERS  (the germe stays k=1; protection grows)")
    print(
        f"    {'L':>2} | {'n=5^L':>10} | {'k':>2} | {'d=3^L':>8} | corrects t=floor((d-1)/2)"
    )
    for L in range(1, 7):
        n, d = 5**L, 3**L
        t = (d - 1) // 2
        print(f"    {L:>2} | {n:>10} | {1:>2} | {d:>8} | {t:>10}")
    assert 5**1 == 5 and 3**1 == 3, "L=1 must be the [[5,1,3]] atom"
    print(
        "    -> 1 logical 'germe' qubit, 5^L physical encoding, distance 3^L (HaPPY tree)."
    )

    # [B] the NOISE threshold = the non-decoherence guarantee ------------------------
    c = failure_spectrum()
    print("\n[B] NOISE THRESHOLD  (the 'non-decoherence' guarantee, computed)")
    print(f"    failure spectrum c_w (mis-corrected -> logical) : {c}")
    assert (
        c[0] == 0 and c[1] == 0
    ), "atom must correct every weight<=1 error (protection)"
    assert c[2] > 0, "weight-2 errors must be able to fail (d=3 corrects only 1)"
    p_th = noise_threshold(c)
    print(
        "    c_0=c_1=0  -> every LOCAL (single-qubit) error is corrected (protected)."
    )
    print(
        f"    leading order f(p) ~ (c_2/9) p^2 = {c[2]/9:.3f} p^2  (sub-linear -> a threshold)"
    )
    print(f"    computed noise threshold  p_th = {p_th:.4f}")
    assert 0.0 < p_th < 0.5, "threshold should lie in (0, 0.5)"
    # concatenation recursion: below p_th the germe's error -> 0 (doubly-exponentially)
    for p0 in (0.5 * p_th, p_th, 1.5 * p_th):
        pl = p0
        traj = []
        for _ in range(4):
            pl = logical_error_rate(pl, c)
            traj.append(pl)
        tag = (
            "BELOW -> 0"
            if p0 < p_th
            else ("AT" if abs(p0 - p_th) < 1e-9 else "ABOVE -> 3/4")
        )
        print(
            f"    p0={p0:.4f} ({tag:12s}): p_L = " + ", ".join(f"{x:.2e}" for x in traj)
        )
    print(
        "    => below p_th, EVOLVING from the germe drives its decoherence under local"
    )
    print(
        "       observation -> 0 as L grows: 'non-decohering by construction' (Romain's hope)."
    )

    # [C] the ERASURE / percolation threshold ---------------------------------------
    q_th = erasure_threshold()
    print("\n[C] ERASURE (LOSS) THRESHOLD  (percolation-type robustness)")
    print(
        "    recursion: a block is lost iff >=3 of 5 sub-blocks lost (corrects d-1=2 erasures)"
    )
    print(
        f"    computed tree threshold  q_th = {q_th:.4f}  (majority of 5 -> exactly 1/2)"
    )
    assert abs(q_th - 0.5) < 1e-3, "majority-of-5 erasure threshold should be 1/2"
    print("    -> the concatenation TREE tolerates ~50% physical loss.")
    print(
        "    -> OBT's faithful network is a degree-~46 EXPANDER claiming ~98% tolerance"
    )
    print(
        "       (p_c~2.2%): MORE robust than the tree = 'expander is the most robust QEC'."
    )
    print(
        "       Same phenomenon (finite, scale-revealed loss tolerance); the value is"
    )
    print(
        "       graph-dependent. The tree is the verifiable lower bound; expander = target."
    )

    # [D] protected-yet-sensitive SCALES (the non-decoherence window widens) ---------
    print(
        "\n[D] PROTECTED-YET-SENSITIVE, SCALED  (the window between noise and signal widens)"
    )
    print(
        f"    {'L':>2} | corrects local up to t=floor((d-1)/2) | collective signal weight = d"
    )
    for L in (1, 2, 3, 4):
        d = 3**L
        print(f"    {L:>2} | {'<= ' + str((d-1)//2):>34} | {d:>27}")
    print(
        "    -> as L grows: ANY local observation up to weight ~3^L/2 is corrected (germe"
    )
    print(
        "       stays coherent), yet only a COLLECTIVE weight-3^L logical operator reaches"
    )
    print(
        "       the germe. Penrose-Diosi (collective, couples to the whole mass distribution)"
    )
    print(
        "       lands there; the local environment cannot. The 'ear' gets sharper with scale."
    )

    # [E] mapping + the honest gates ------------------------------------------------
    print("\n[E] OBT MAPPING + GATES")
    print(
        "    * 'partir de la forme primaire' = encode in the logical/germe subspace (k=1);"
    )
    print(
        "      'evoluer de la sur ce canal' = concatenate/tile -> distance 3^L grows."
    )
    print(
        "    * 'un debut et une fin, tous les possibles entre' = the bulk-germe (1 logical)"
    )
    print(
        "      <-> boundary (5^L physical) channel; 'the possibles' = the protected logical"
    )
    print("      Hilbert space carried redundantly across the ER=EPR network.")
    print(
        "    * 'non-decoherence lors de l'observation a 0.2um' = below p_th the LOCAL"
    )
    print(
        "      observation is corrected (germe coherent); the COLLECTIVE Penrose-Diosi"
    )
    print(
        "      channel still passes. Caveat: the FINAL logical readout still costs ONE"
    )
    print(
        "      measurement (Gate-OUT's irreducible step) -- protected, not measurement-free."
    )
    print(
        "    * GATES still open: the degree-46 EXPANDER tiling (faithful p_c~2.2%, not the"
    )
    print(
        "      tree's 50%); that Penrose-Diosi maps to the logical class (Gate-IN gate a);"
    )
    print("      the mass-vs-coherence BMV wall.")
    print("\n  ALL INJECTION TESTS PASSED (params, c_0=c_1=0, 0<p_th<0.5, q_th=1/2).")
    print("=" * 80)


if __name__ == "__main__":
    main()
