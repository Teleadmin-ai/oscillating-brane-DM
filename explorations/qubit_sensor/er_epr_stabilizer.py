"""Seed 3 (V9.0, quarantined) — OBT's ER=EPR network as an EXPLICIT stabilizer code.

First concrete step of Seed 3 (explorations/README.md): write OBT's holographic
ER=EPR / HaPPY network as an explicit stabilizer quantum-error-correcting code, and
identify the LOGICAL SUBSPACE that is 'protected-yet-sensitive' -- protected against
generic local decoherence (the noise) yet still coupled to the ONE channel the brane
leaves open (the Penrose-Diosi 5D collapse). That coupled subspace is gate 1 (the
'Goldilocks deafness') made concrete.

NOT V8.2. Not in the PDF. No physical claim of V8.2. 'code, don't plead': every
numeric statement is computed and injection-tested against the KNOWN [[5,1,3]]
properties (k=1, d=3, perfect single-error code) via assert.

THE FAITHFUL ATOM. OBT invokes the holographic-QEC picture (MERA/HaPPY, ER=EPR
expander graph, RT transition, 'the most robust QEC code physically conceivable').
The canonical holographic stabilizer code (Pastawski-Yoshida-Harlow-Preskill 2015,
'HaPPY') is built from the [[5,1,3]] 'perfect' pentagon code tiled on a hyperbolic
tessellation. So the explicit ATOM of the ER=EPR code is the [[5,1,3]] stabilizer
code: 5 physical qubits (a PBH node + its 4 ER=EPR neighbours), 1 logical qubit
(one germe degree of freedom), distance 3. Tiling it on OBT's expander graph is the
scale-up (distance grows; the erasure threshold -> the percolation threshold
p_c ~ 2.2% that OBT already claims).

THE GOLDILOCKS, MADE PRECISE. A stabilizer code of distance d:
  - CORRECTS any error of weight <= floor((d-1)/2)   -> DEAF to LOCAL noise;
  - a non-trivial logical operator (min weight = d) has ZERO syndrome (invisible to
    the code's own checks) yet rotates the encoded qubit -> SENSITIVE to a COLLECTIVE
    (high-weight, correlated) channel that lands in the logical class.
The separation is by OPERATOR WEIGHT (local vs collective), set by the code distance.
Penrose-Diosi collapse couples to the whole superposition's mass distribution -> a
COLLECTIVE channel -> it can reach the logical qubit, while generic thermal/local
decoherence (weight 1) is corrected away. That is how a qubit can be 'stable by
construction' yet still hear the demon: protect the local, leave the collective open.

OPEN GATE (flagged, not hidden): this script proves the MECHANISM is possible (a code
can be protected-yet-sensitive when the signal is collective and the noise is local).
It does NOT prove OBT's actual gravitational channel maps to a logical-class operator
rather than a correctable one -- that is the physics still to be done.
"""

import itertools

import numpy as np

N = 5  # physical qubits in the perfect-code atom (PBH node + 4 ER=EPR neighbours)


# ---------------------------------------------------------------- symplectic helpers
def pauli(s):
    """Pauli string ('XZZXI') -> length-2N binary symplectic vector (x|z)."""
    x = [1 if c in "XY" else 0 for c in s]
    z = [1 if c in "ZY" else 0 for c in s]
    return np.array(x + z, dtype=int)


def symp(u, v):
    """Symplectic inner product mod 2: 0 = commute, 1 = anticommute."""
    xu, zu = u[:N], u[N:]
    xv, zv = v[:N], v[N:]
    return int((xu @ zv + zu @ xv) % 2)


def weight(v):
    """Number of qubits on which the Pauli acts non-trivially."""
    return int(np.sum((v[:N] | v[N:]) > 0))


def gf2_rank(rows):
    """Rank over GF(2) of a list of binary vectors."""
    M = [r.copy() % 2 for r in rows]
    r = 0
    ncol = len(M[0])
    for c in range(ncol):
        piv = next((i for i in range(r, len(M)) if M[i][c]), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(len(M)):
            if i != r and M[i][c]:
                M[i] = (M[i] + M[r]) % 2
        r += 1
    return r


# ---------------------------------------------------------------- the [[5,1,3]] code
GEN_STR = ("XZZXI", "IXZZX", "XIXZZ", "ZXIXZ")  # standard cyclic generators
GENS = [pauli(s) for s in GEN_STR]
Z_L = pauli("ZZZZZ")
X_L = pauli("XXXXX")


def stabilizer_group():
    """All 2^(n-k) elements of <GENS> (mod phase) = GF(2) row space."""
    G = np.array(GENS)
    grp = set()
    for coeffs in itertools.product([0, 1], repeat=len(GENS)):
        v = (np.array(coeffs) @ G) % 2
        grp.add(tuple(v))
    return grp


def all_paulis():
    for bits in itertools.product([0, 1], repeat=2 * N):
        yield np.array(bits, dtype=int)


def normalizer():
    """All Paulis commuting with every generator (the centralizer of S)."""
    return [v for v in all_paulis() if all(symp(v, g) == 0 for g in GENS)]


def syndrome(e):
    return tuple(symp(e, g) for g in GENS)


def min_weight_logical_rep(logical):
    """Min-weight representative of a logical operator's coset (logical x stabilizer)."""
    stab = stabilizer_group()
    best = logical.copy()
    for s in stab:
        cand = (logical + np.array(s)) % 2
        if weight(cand) < weight(best):
            best = cand
    return best


def main():
    print("=" * 78)
    print(
        " OBT ER=EPR network -> explicit stabilizer code  (Seed 3, V9.0, quarantined)"
    )
    print(" Atom = the [[5,1,3]] perfect code (the HaPPY holographic tensor)")
    print("=" * 78)

    # [1] the explicit code -----------------------------------------------------
    G = np.array(GENS)
    rank = gf2_rank([g.copy() for g in GENS])
    k = N - rank
    commute = all(symp(GENS[i], GENS[j]) == 0 for i in range(4) for j in range(4))
    print("\n[1] EXPLICIT STABILIZER CODE")
    for s, g in zip(GEN_STR, GENS):
        print(f"      g = {s}   (x|z) = {g.tolist()}")
    print(f"    generators pairwise commute : {commute}")
    print(f"    independent (GF(2) rank)    : {rank}/4")
    print(f"    physical qubits n           : {N}")
    print(f"    logical qubits  k = n-rank  : {k}")
    assert commute and rank == 4 and k == 1, "not a valid [[5,1,k]] code"

    # [2] distance + perfectness ------------------------------------------------
    stab = stabilizer_group()
    norm = normalizer()
    logical_ops = [v for v in norm if tuple(v) not in stab]  # N(S) \ <S>
    distance = min(weight(v) for v in logical_ops)
    print("\n[2] DISTANCE + PERFECTNESS")
    print(f"    |stabilizer group <S>|      : {len(stab)}   (= 2^(n-k) = 16)")
    print(f"    |normalizer N(S)|           : {len(norm)}   (= 2^(n+k) = 64)")
    print(f"    |logical ops N(S)\\<S>|      : {len(logical_ops)}   (= 64-16 = 48)")
    print(f"    code distance d = min wt    : {distance}")
    assert distance == 3, "distance should be 3"

    w1 = [e for e in all_paulis() if weight(e) == 1]
    synds = [syndrome(e) for e in w1]
    distinct = len(set(synds))
    nonzero = all(any(s) for s in synds)
    print(f"    weight-1 errors             : {len(w1)} (=3n)")
    print(
        f"    -> distinct nonzero syndromes: {distinct}/{len(w1)}, all nonzero={nonzero}"
    )
    print("    -> 15 errors fill all 15 nonzero 4-bit syndromes = PERFECT code")
    assert distinct == 15 and nonzero, "not a perfect single-error code"
    # injection: a weight-2 error must COLLIDE with a weight-1 syndrome (so d is not >3)
    w2 = [e for e in all_paulis() if weight(e) == 2]
    collide = any(syndrome(e2) in set(synds) for e2 in w2)
    print(f"    injection: a weight-2 error shares a weight-1 syndrome : {collide}")
    assert (
        collide
    ), "expected syndrome collision at weight 2 (confirms d=3, corrects only 1)"

    # [3] logical operators -----------------------------------------------------
    print("\n[3] LOGICAL OPERATORS (the germe degree of freedom)")
    for name, L in (("Z_L", Z_L), ("X_L", X_L)):
        in_norm = all(symp(L, g) == 0 for g in GENS)
        in_stab = tuple(L) in stab
        rep = min_weight_logical_rep(L)
        print(
            f"    {name}: commutes-with-all-stabilizers={in_norm}, in-<S>={in_stab}, "
            f"weight={weight(L)} -> min-weight rep weight={weight(rep)}"
        )
        assert in_norm and not in_stab
    anti = symp(Z_L, X_L)
    print(
        f"    symp(Z_L, X_L) = {anti}  (=1 -> they anticommute, a genuine logical qubit)"
    )
    assert anti == 1

    # [4] the Goldilocks: protected-yet-sensitive subspace ----------------------
    print("\n[4] THE GOLDILOCKS SUBSPACE (gate 1, made concrete)")
    e_local = pauli("XIIII")  # a generic LOCAL (weight-1) decoherence event
    s_local = syndrome(e_local)
    print(f"    LOCAL noise  e=XIIII (weight {weight(e_local)}): syndrome={s_local}")
    print(
        "      -> nonzero syndrome -> DETECTED + CORRECTED -> logical qubit UNTOUCHED"
    )
    print("      => the codespace is DEAF to local decoherence (protected).")
    L_coll = min_weight_logical_rep(X_L)  # a COLLECTIVE, logical-class operator
    s_coll = syndrome(L_coll)
    print(
        f"\n    COLLECTIVE signal  L (weight {weight(L_coll)}, logical class): syndrome={s_coll}"
    )
    print(
        "      -> ZERO syndrome -> INVISIBLE to the code's checks (not 'corrected away')"
    )
    print("      -> yet L is a logical operator -> it ROTATES the encoded qubit")
    print(
        "      => the codespace is SENSITIVE to a collective channel (it accumulates)."
    )
    print(
        "\n    PROTECTED-YET-SENSITIVE: the SAME codespace rejects weight-1 noise (syndrome"
        "\n    != 0, corrected) but registers a weight-3 collective operator (syndrome = 0,"
        "\n    logical). The separator is OPERATOR WEIGHT, set by the distance d=3."
    )

    # [5] OBT mapping + gates ---------------------------------------------------
    print("\n[5] OBT MAPPING + GATES (the physics, honestly flagged)")
    print(
        "    * Penrose-Diosi 5D collapse couples to the whole mass distribution = a"
        "\n      COLLECTIVE, correlated channel -> candidate logical-class operator -> the"
        "\n      readout lands in the protected-yet-sensitive (logical) subspace."
    )
    print(
        "    * Generic thermal/local decoherence = weight-1 -> corrected away -> the"
        "\n      sensor is stable 'by construction' (gate: stability from structure)."
    )
    print(
        "    * OPEN GATE (unproven): that OBT's actual gravitational channel maps to a"
        "\n      logical-class operator and NOT a correctable one. This script shows the"
        "\n      mechanism is POSSIBLE, not that OBT realizes it. (Goldilocks gate 1.)"
    )
    print(
        "    * SCALE-UP: tile this [[5,1,3]] atom on OBT's expander graph (HaPPY) -> the"
        "\n      distance grows with the network; the erasure threshold -> a percolation"
        "\n      threshold ~ OBT's claimed p_c ~ 2.2% (d=46). Quantum LDPC / expander codes"
        "\n      (Tillich-Zemor) are the 'most robust' family OBT's wording points at."
    )
    print("\n  ALL INJECTION TESTS PASSED (k=1, d=3, perfect, anticommuting logicals).")
    print("=" * 78)


if __name__ == "__main__":
    main()
