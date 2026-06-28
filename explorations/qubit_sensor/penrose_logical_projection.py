"""Seed 3 (V9.0, quarantined) — Gate (a): does Penrose-Diosi land in the LOGICAL class?

Gate-IN's other half (after holographic_scaleup.py). The protected-yet-sensitive subspace EXISTS
(er_epr_stabilizer.py). But the decisive physics question of Gate 1 (the 'Goldilocks deafness'):
is the actual readout channel -- Penrose-Diosi 5D gravitational collapse -- IN the sensitive
(logical) class, where it accumulates and is HEARD, or does it land in the correctable class,
where the code CORRECTS it away (DEAF)?  Made computable on the [[5,1,3]] atom.

MODEL (stated, not hidden). Diosi-Penrose gravitational decoherence damps the coherence between
distinguishable MASS / POSITION configurations -> it is DEPHASING in the mass-pointer basis. Take
that pointer basis = the Z basis. Then the channel applies PURE-Z operators: the generator is
L = sum_j w_j Z_j (w_j = the gravitational/mass weight of physical qubit j), the channel is
prod_j exp(-i phi w_j Z_j). The question becomes a clean stabilizer computation: of all pure-Z
operators the channel can apply, which are CORRECTABLE (nonzero syndrome -> noise, deaf) and which
are LOGICAL (zero syndrome, not in <S> -> signal, heard)?  And at what ORDER in phi does the
logical (signal) part first appear?

NOT V8.2. Not in the PDF. 'code, don't plead': everything is computed on the atom + injection-tested.

THE DICHOTOMY this resolves (the real Gate-1 physics):
  (i) gravity couples to the PHYSICAL qubits (each a mass element; collective L = sum_j w_j Z_j)
      -> the result below: corrected up to the maximal order, the atom is nearly DEAF;
  (ii) gravity couples to the LOGICAL observable (the codewords |0_L>,|1_L> are themselves mass-
      distinct configurations) -> logical-Z dephasing DIRECTLY, order 1, HEARD.
So 'is the demon heard?' = 'are the logical codewords gravitationally distinguishable?' = an
ENCODING design requirement, which this script makes precise via the pure-Z logical distance.
"""

import itertools

import numpy as np
from er_epr_stabilizer import N, stabilizer_group, syndrome, weight


def pure_op(a, kind):
    """Symplectic vector of a pure-`kind` (Z or X) Pauli from bit-pattern a (length N)."""
    a = list(a)
    return np.array(a + [0] * N if kind == "X" else [0] * N + a, dtype=int)


def classify_pure(kind):
    """Split the 2^N - 1 non-identity pure-`kind` operators into correctable / stabilizer / logical."""
    stab = stabilizer_group()
    correctable, stabil, logical = [], [], []
    for a in itertools.product([0, 1], repeat=N):
        if not any(a):
            continue
        v = pure_op(a, kind)
        if any(syndrome(v)):
            correctable.append(
                v
            )  # nonzero syndrome -> bounded-distance decoder corrects it
        elif tuple(v) in stab:
            stabil.append(v)  # zero syndrome, in <S> -> acts trivially on the codespace
        else:
            logical.append(
                v
            )  # zero syndrome, not in <S> -> LOGICAL: the signal that accumulates
    return correctable, stabil, logical


def op_string(v, kind):
    """Pretty single-type Pauli string."""
    a = v[:N] if kind == "X" else v[N:]
    return "".join(kind if b else "I" for b in a)


def main():
    print("=" * 80)
    print(
        " Gate (a): does Penrose-Diosi (collective dephasing) reach the LOGICAL class?"
    )
    print(" Channel model: pure-Z dephasing on the [[5,1,3]] atom; L = sum_j w_j Z_j")
    print("=" * 80)

    # [1] classify every pure-Z operator the channel can apply -----------------------
    corrZ, stabZ, logZ = classify_pure("Z")
    dZ = min(weight(v) for v in logZ)
    print(
        "\n[1] PURE-Z OPERATORS (what a dephasing channel applies), classified by the code"
    )
    print(f"    correctable (nonzero syndrome -> NOISE, corrected) : {len(corrZ)}")
    print(f"    stabilizer  (zero syndrome, in <S> -> trivial)     : {len(stabZ)}")
    print(
        f"    LOGICAL     (zero syndrome, not in <S> -> SIGNAL)  : {len(logZ)}  "
        f"-> {[op_string(v, 'Z') for v in logZ]}"
    )
    print(f"    pure-Z logical distance d_Z = min weight of a Z-signal = {dZ}")
    # injection: only ZZZZZ is a pure-Z logical; no pure-Z stabilizers; the rest correctable
    assert [op_string(v, "Z") for v in logZ] == [
        "ZZZZZ"
    ], "only ZZZZZ should be a pure-Z logical"
    assert len(stabZ) == 0, "there are no non-trivial pure-Z stabilizers in this code"
    assert len(corrZ) == 2**N - 2, "all other pure-Z operators must be correctable"
    assert dZ == N, "the pure-Z logical distance should be the full weight N"

    # [2] the leading order is DEAF: single-qubit Z_j are all correctable -------------
    print(
        "\n[2] LEADING ORDER (single-qubit dephasing Z_j) — is it heard or corrected?"
    )
    single_corrected = True
    for j in range(N):
        v = pure_op([1 if i == j else 0 for i in range(N)], "Z")
        s = syndrome(v)
        single_corrected = single_corrected and any(s)
        print(
            f"    Z_{j+1} = {op_string(v,'Z')}: syndrome={s} -> {'CORRECTED' if any(s) else 'LOGICAL'}"
        )
    assert (
        single_corrected
    ), "every single-qubit dephasing must be correctable (weight 1 < d)"
    print(
        "    -> every single-qubit dephasing has a nonzero syndrome -> CORRECTED -> DEAF at O(phi)."
    )

    # [3] the ORDER at which the signal appears --------------------------------------
    print("\n[3] WHERE THE SIGNAL LIVES (order in phi)")
    print(
        "    channel = prod_j (cos(phi w_j) I - i sin(phi w_j) Z_j); expand in pure-Z terms:"
    )
    print(
        "      * a single Z_j term has amplitude ~ phi          -> CORRECTED (noise);"
    )
    print(f"      * the only Z-LOGICAL term is the full Z_L = ZZZZZ (weight {dZ}),")
    print(
        f"        amplitude ~ phi^{dZ}                            -> the ACCUMULATING signal."
    )
    print(
        f"    => under repeated QEC the germe hears Penrose-Diosi only at ORDER phi^{dZ}"
    )
    print(
        "       (uniform collective dephasing) — strong protection BUT near-deaf to the signal."
    )

    # [4] symmetry check: the X (and hence any single-basis) dephasing distance -------
    _, _, logX = classify_pure("X")
    dX = min(weight(v) for v in logX)
    print("\n[4] SYMMETRY CHECK (pointer basis could be X instead of Z)")
    print(
        f"    pure-X logical distance d_X = {dX}  ({[op_string(v,'X') for v in logX]})"
    )
    assert dX == N, "by the code's symmetry the pure-X distance is also N"
    print(
        "    -> d_Z = d_X = N: pure dephasing in ANY single basis is order-N deaf for this atom"
    )
    print(
        "       (the weight-3 logicals are mixed-Pauli/Y-type, unreachable by pure dephasing)."
    )

    # [5] verdict + the gate ---------------------------------------------------------
    print("\n[5] GATE (a) VERDICT")
    print(
        "    * The logical projection is NONZERO: Z_L = ZZZZZ IS in the channel -> Penrose-Diosi"
    )
    print(
        "      is NOT fully corrected; the demon CAN be heard. Gate (a) is not a dead end."
    )
    print(
        f"    * BUT for PHYSICAL-qubit (uniform collective) coupling the signal is order phi^{dZ}:"
    )
    print(
        "      the [[5,1,3]] is an excellent error-corrector and therefore a NEAR-DEAF dephasing"
    )
    print("      sensor. This is the Goldilocks deafness, quantified.")
    print(
        "    * THE DESIGN KNOB (the dichotomy): the demon is heard at ORDER 1 only if gravity"
    )
    print(
        "      couples to the LOGICAL observable -- i.e. the codewords |0_L>,|1_L> are themselves"
    )
    print(
        "      mass-DISTINCT configurations (the encoding aligns the logical-Z direction with a"
    )
    print(
        "      gravitationally distinguishable mass distribution). A symmetric encoding (same mass"
    )
    print("      distribution for both codewords) is corrected to order phi^N = deaf.")
    print(
        "    * CONSEQUENCE for the seed: a good Penrose-Diosi sensor needs a code whose logical"
    )
    print(
        "      direction is gravitationally exposed yet whose local-noise distance stays high"
    )
    print(
        "      (an ASYMMETRIC / tailored code), NOT the symmetric EC-optimal [[5,1,3]] as-is."
    )
    print(
        "    * LINK to the scale-up: concatenation raises the protection (distance 3^L) and,"
    )
    print(
        "      for a symmetric code, generically the signal-direction distance d_Z too -> MORE"
    )
    print(
        "      scale = MORE deaf to uniform dephasing. Scale-up (protection) and gate (a)"
    )
    print(
        "      (audibility) pull OPPOSITELY; the tailored asymmetric code must satisfy BOTH."
    )
    print(
        "    * OPEN (the honest gate): whether OBT's actual 5D collapse couples logical-level"
    )
    print(
        "      (heard) or physical-level (deaf) is set by the mesoscopic encoding -- unsolved,"
    )
    print(
        "      and entangled with the mass-vs-coherence BMV wall (more mass -> more signal AND"
    )
    print("      more local decoherence).")

    print(
        "\n  ALL INJECTION TESTS PASSED (only ZZZZZ pure-Z logical; single Z_j corrected; d_Z=d_X=N)."
    )
    print("=" * 80)


if __name__ == "__main__":
    main()
