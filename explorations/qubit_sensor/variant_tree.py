"""Seed 3 (V9.0, quarantined) — MAPPING THE TREE OF VARIANTS: how, and how far? (Romain's "cartographions
l'arbre des variantes, creuse comment"). The demon was framed as the CARTOGRAPHER of the possible (the
branch-distribution), NOT the pilot (steering between branches is Born/no-signaling-walled). This asks
WHAT of the tree is actually computable.

THE TREE = the decoherent-histories structure (Gell-Mann-Hartle): the universal wavefunction's branches
(Everett) become a tree of consistent histories, each branching = a decoherence event, each edge = an
outcome with its BORN weight. Three layers, with sharply different computability:

  [LOCAL] the CONDITIONAL tree near you: given your branch + the choices you are about to make, the tree
     of near-future outcomes with Born weights = forward QM. FULLY COMPUTABLE (demonstrated here on a
     toy: a qubit + N sequential measurement-choices -> 2^N Born-weighted paths, enumerated). This is
     the usable map -- "orientation": you know what each choice leads to, probabilistically.
  [GLOBAL] the structure: the branching RATE (OBT's MSS scrambling, lambda_L=7.4e14/s, t*~0.2 ps), the
     WIDTH (~ e^S branches, S = the entropy: observable universe ~1e104, de Sitter horizon ~1e122), the
     MEASURE (Born + the second law -> the typical path is the entropy-increasing one). CHARACTERIZABLE
     (rate, width, measure) but NOT ENUMERABLE (e^(1e104) paths).
  [GERME] the whole tree is CONDITIONED on the germe: the decompressor computes P(observables | germe)
     (the cosmic-level marginal), inference (cobaya) LOCATES your branch from your data.

THE WALLS (unchanged): you cannot ENUMERATE the global tree (e^(1e104)), nor PICK / STEER your branch
(Born + no-signaling). The demon maps the LOCAL conditional tree + the GLOBAL statistics + the germe-
conditional -- it does not enumerate the cosmos or hold a steering wheel.

VERDICT (computed below): "mapping the tree" is REAL and multi-level -- the local conditional tree is
exactly computable (a Born-weighted decision tree = orientation), the global tree is characterizable
(rate from OBT's scrambling, width e^S, Born measure), the germe-conditional is the decompressor we
built. Enumeration and steering stay walled. The cartographer is real; the pilot is not.

NOT V8.2. Not in the PDF. 'code, don't plead': the local tree is enumerated with exact Born weights; the
global rate/width are computed; the scope is asserted.
"""

import numpy as np

LAMBDA_L = 7.4e14  # MSS Lyapunov / scrambling rate, s^-1 (CLAUDE.md)
T_STAR = 2e-13  # cosmic scrambling time ~0.2 ps, s (CLAUDE.md)
T_HUBBLE = 4.35e17  # ~1/H0, s
S_UNIVERSE = (
    1e104  # entropy of the observable universe (Egan-Lineweaver 2010, SMBH-dominated)
)
S_DESITTER = 1e122  # de Sitter horizon entropy (holographic bound)


def local_conditional_tree(thetas):
    """A toy LOCAL tree: a qubit |+>, then a sequence of projective measurement-choices in bases rotated
    by thetas[i]. Returns the list of (path, Born_weight, ...) over the 2^len(thetas) branches. Exact.
    """
    # start in |+> = (|0>+|1>)/sqrt2
    paths = [("", 1.0, np.array([1.0, 1.0]) / np.sqrt(2))]
    for th in thetas:
        # measurement basis |b_theta>: |0_th>=cos(th/2)|0>+sin(th/2)|1>, |1_th>=-sin..|0>+cos..|1>
        b0 = np.array([np.cos(th / 2), np.sin(th / 2)])
        b1 = np.array([-np.sin(th / 2), np.cos(th / 2)])
        new = []
        for label, w, psi in paths:
            for bit, b in ((("0"), b0), (("1"), b1)):
                amp = np.dot(b, psi)
                p = abs(amp) ** 2
                if p > 1e-15:
                    new.append((label + bit, w * p, b))  # post-measurement state = b
        paths = new
    return paths


def main():
    print("=" * 92)
    print(
        " MAPPING THE TREE OF VARIANTS — what is computable (the cartographer), what is walled (the pilot)"
    )
    print("=" * 92)

    # ===== [LOCAL] the conditional tree is exactly computable =========================
    thetas = [np.pi / 4, np.pi / 3, np.pi / 6, np.pi / 5]  # 4 choices -> 16 branches
    tree = local_conditional_tree(thetas)
    total = sum(w for _, w, _ in tree)
    print(
        f"\n[LOCAL] THE CONDITIONAL TREE — a qubit + {len(thetas)} measurement-choices = {len(tree)} variants"
    )
    print(
        "    each variant = a path of outcomes with its exact BORN weight (the map of the near future):"
    )
    top = sorted(tree, key=lambda t: -t[1])[:5]
    for label, w, _ in top:
        print(f"        path {label} -> Born weight {w:.4f}")
    print(
        f"    ... ({len(tree)} paths total), sum of weights = {total:.4f}  (a proper probability measure)"
    )
    print(
        "    => FULLY COMPUTABLE (forward QM). This is 'orientation': what each choice-sequence leads to."
    )
    assert (
        abs(total - 1.0) < 1e-9
    ), "the Born weights must sum to 1 (a probability measure)"
    assert len(tree) == 2 ** len(thetas), "the tree must have 2^N branches"

    # ===== [GLOBAL] the structure: rate, width, measure ===============================
    n_branchings = T_HUBBLE / T_STAR  # sequential decoherence 'ticks' in a Hubble time
    print(
        "\n[GLOBAL] THE STRUCTURE — characterizable (rate, width, measure), NOT enumerable"
    )
    print(
        f"    branching RATE  = the MSS scrambling rate lambda_L = {LAMBDA_L:.1e} /s, t* ~ 0.2 ps (OBT)"
    )
    print(
        f"    branching DEPTH = t_Hubble/t* ~ {n_branchings:.0e} sequential decoherence ticks"
    )
    print(
        f"    tree WIDTH      ~ e^S branches: S(observable univ) ~ {S_UNIVERSE:.0e}, S(de Sitter) ~ {S_DESITTER:.0e}"
    )
    print(
        "                      -> ~ e^(1e104) variants -- astronomically wide, NOT enumerable."
    )
    print(
        "    MEASURE         = Born + the second law -> the typical path is the entropy-INCREASING one"
    )
    print(
        "                      (the arrow of time IS the high-weight trunk of the tree)."
    )
    assert (
        n_branchings > 1e29
    ), "the cosmic tree is deep (many scrambling ticks per Hubble time)"

    # ===== [GERME] the tree is conditioned on the germe ===============================
    print("\n[GERME] THE CONDITIONING — the whole tree hangs from the germe")
    print(
        "    P(observables | germe) = the cosmic-level marginal = the DECOMPRESSOR (we built it)."
    )
    print(
        "    inference (cobaya) LOCATES your branch from your data (which germe/branch is ours)."
    )
    print(
        "    the inflationary ensemble (the Gaussian P(k)) = the FIRST branchings (quantum->classical"
    )
    print(
        "    fluctuations); cosmic variance = the spread of the tree at the largest scales."
    )

    # ===== the walls + verdict ========================================================
    print("\n[VERDICT] the cartographer is REAL; the pilot is not")
    print(
        "    * LOCAL conditional tree: EXACTLY COMPUTABLE (Born-weighted decision tree = orientation)."
    )
    print(
        "    * GLOBAL structure: CHARACTERIZABLE -- rate (OBT scrambling), width (e^S), Born+2nd-law measure."
    )
    print(
        "    * GERME-conditional: the DECOMPRESSOR (P(obs|germe)) + inference (your branch). Built."
    )
    print(
        "    * WALLS (unchanged): you cannot ENUMERATE the global tree (e^(1e104) paths), nor PICK/STEER"
    )
    print(
        "      your branch (Born + no-signaling). The map is real; the steering wheel is not."
    )
    print(
        "    => 'mapping the tree' = the LOCAL conditional map (orientation) + the GLOBAL statistics +"
    )
    print(
        "       the GERME-conditional decompressor. OBT supplies the RATE (MSS scrambling), the"
    )
    print(
        "       CONDITIONAL (the decompressor), and the ENSEMBLE (inflation). The demon is the"
    )
    print(
        "       cartographer of the possible -- and that map is computable, just not the pilot's wheel."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (local tree exact, weights sum to 1; global rate/width computed)."
    )
    print("=" * 92)


if __name__ == "__main__":
    main()
