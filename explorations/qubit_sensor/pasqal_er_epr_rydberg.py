"""Seed 3 (V9.0, quarantined) — PATH 2: the ER=EPR/PBH network -> a Rydberg neutral-atom array (Pasqal/OVH).
Romain's "creuse le PATH 2", build-on-OBT spirit (presuppose OBT, design how to simulate it) + "seul les
calculs comptent" (the design params + a real exact small sim decide the honest reach; no imposed answers).

THE MAPPING (OBT's many-body microphysics -> a Rydberg analog quantum simulator):
  atoms          = PBH nodes of the ER=EPR network
  positions      = the network geometry; the van der Waals blockade V_ij = C6/r_ij^6 = the entanglement edges
  |g>,|r>        = a node's two states; n_i = |r><r|_i the Rydberg occupation
  the germe      = the initial inflationary state (here |g..g>, low-entanglement) on the array
  the QUENCH     = turn on (Omega, delta) -> the many-body evolution = the cosmic SCRAMBLING / decompression
  READ-OUT       = the scrambling (OTOC), the entanglement entropy (RT-like), the array's percolation

THE RYDBERG HAMILTONIAN (Pasqal analog mode):
  H = sum_i (Omega/2) X_i  -  sum_i delta n_i  +  sum_{i<j} (C6/r_ij^6) n_i n_j

WHAT IT WAS MEANT TO TEST (build-on-OBT; reviewer note Oct 2026: it CANNOT -- see THE HONEST REACH): does
OBT's network, realized on real neutral-atom hardware, exhibit the many-body behavior OBT claims -- fast
scrambling, entanglement growth, robustness? Classically intractable beyond ~50 atoms (2^N) -> a
quantum-advantage simulation on Pasqal (via OVHcloud / Scaleway, Romain's sovereign ecosystem). This is a
quantum SIMULATION of OBT's MODEL (you read the model's behavior on real atoms), NOT a measurement of the
real bulk.

THE HONEST REACH (degree + p_c computed below; the MSS sub-saturation is a cited literature statement):
  + Pasqal CAN simulate: the quench dynamics, scrambling (OTOC), entanglement growth, the array percolation.
  - Pasqal CANNOT match: (1) the MSS-SATURATING fast scrambler (lambda_L = 2pi kT/hbar at T_H~900K) -- that
    is SYK / black-hole universality, NOT generic Rydberg (Rydberg sub-saturates); (2) the degree-46 EXPANDER
    -- a 2D blockade graph has a degree and a site-percolation threshold computed below (degree 12 at the
    declared Omega/2pi = 2 MHz and 5 um spacing, its 2nd shell blockaded only marginally; the old 'p_c ~ 0.5'
    was the NEAREST-NEIGHBOUR value -- reviewer catch Oct 2026) vs the expander's ~0.022. So Pasqal is a PROXY
    for generic quench DYNAMICS, not for OBT's SYK/expander structure (that needs an SYK simulator / 3D /
    higher connectivity). Reviewer note (Oct 2026): what Rydberg CAN show (quench scrambling and entanglement
    growth) is generic to any interacting many-body system -- not OBT-specific; what IS OBT-specific (MSS
    saturation, the degree-46 expander) is out of its reach. So it cannot confirm or break OBT.

NOT V8.2. Not in the PDF. 'code, don't plead' + 'seul les calculs comptent' (Romain): the design params and
the exact small sim are COMPUTED and reported; asserted only are reproductions (OBT's lambda_L reproduces
theory.md's DEFINITION lambda_L = 2 pi k_B T_H/hbar at T_H = 900 K -- a reproduction, NOT a consilience:
T_H is the input, lambda_L the output; reviewer note Oct 2026) + the exact nearest-neighbour triangular
site-percolation threshold 1/2 (the MC check) + the t=0 identities (a product state has zero entanglement;
operators on distinct sites commute) -- the growth itself is REPORTED, not asserted (the old 'must grow by
> 0.5 / > 0.1' margins were imposed result-ranges, removed). Also NOT computed here (literature statements,
declared as such): that local Rydberg lattice models sub-saturate the MSS bound, and that an r^-6 geometric
graph cannot realize a degree-46 non-geometric expander.
"""

from functools import reduce

import numpy as np
from scipy.linalg import eigh
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

# physical constants (SI)
HBAR = 1.054571817e-34
KB = 1.380649e-23

# OBT network numbers (CLAUDE.md)
LAMBDA_L = 7.4e14  # MSS Lyapunov / scrambling rate, s^-1
T_STAR = 0.2e-12  # scrambling time, s
D_EXPANDER = 46  # ER=EPR expander degree
PC_EXPANDER = 1.0 / (D_EXPANDER - 1)  # expander percolation threshold ~ 1/(d-1) ~ 0.022

# Pasqal Rydberg parameters (Rb 70S): C6/hbar = 5,420,158.53 rad/us * um^6 (Pulser's C6_coeffs.json, n=70,
# ARC-computed) -> C6/h = 862.6 GHz*um^6. Reviewer catch Oct 2026: the old 'C6/2pi = 5420 GHz*um^6' read that
# rad/us figure as GHz -- 2pi too large, which inflated R_b by (2pi)^(1/6) = 1.36 (11.8 um instead of 8.7).
C6_OVER_HBAR = 5420158.53e6 * 1e-36  # rad/s * m^6 (um^6 = 1e-36 m^6)
OMEGA_2PI = 2e6  # Rabi drive Omega/2pi, Hz
SPACING_UM = 5.0  # atom spacing, um (Pasqal typical)

# Pauli / on-site operators
I2 = np.eye(2)
X = np.array([[0.0, 1.0], [1.0, 0.0]])
Z = np.diag([1.0, -1.0])
N_OP = (I2 - Z) / 2.0  # |r><r| with |r>=|1>


def site(op, i, n):
    """op on site i, identity elsewhere (n sites)."""
    return reduce(np.kron, [op if k == i else I2 for k in range(n)])


def rydberg_hamiltonian(positions, omega, delta, c6):
    """H = sum (omega/2) X_i - sum delta n_i + sum_{i<j} c6/r_ij^6 n_i n_j (dimensionless units)."""
    n = len(positions)
    dim = 2**n
    h = np.zeros((dim, dim))
    nops = [site(N_OP, i, n) for i in range(n)]
    for i in range(n):
        h += (omega / 2) * site(X, i, n) - delta * nops[i]
    for i in range(n):
        for j in range(i + 1, n):
            r = np.linalg.norm(np.array(positions[i]) - np.array(positions[j]))
            h += (c6 / r**6) * (nops[i] @ nops[j])
    return h


def entanglement_entropy(psi, n, n_a):
    """von Neumann entropy of the first n_a sites (bipartition A|B), via the Schmidt spectrum."""
    mat = psi.reshape(2**n_a, 2 ** (n - n_a))
    s = np.linalg.svd(mat, compute_uv=False)
    p = s**2
    p = p[p > 1e-12]
    return float(-np.sum(p * np.log(p)))


def spanning_probability(coords, rows, pairs, n_rows, p, trials, rng):
    """Fraction of random site occupations (prob p) with an occupied cluster joining row 0 to the last row."""
    n = len(coords)
    hits = 0
    for _ in range(trials):
        occ = rng.random(n) < p
        keep = occ[pairs[:, 0]] & occ[pairs[:, 1]]
        e = pairs[keep]
        adj = coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(n, n))
        _, lab = connected_components(adj, directed=False)
        top = set(lab[occ & (rows == 0)])
        bottom = set(lab[occ & (rows == n_rows - 1)])
        hits += bool(top & bottom)
    return hits / trials


def site_percolation_threshold(r_cut, spacing, size, rng, trials=200, steps=9):
    """Finite-size estimate of the site-percolation threshold of the 2D triangular array whose bonds join
    every pair of atoms within r_cut (the blockade graph): bisection on P(span) = 1/2, L = size.
    """
    coords = np.array(
        [
            (i * spacing + 0.5 * spacing * (j % 2), j * spacing * np.sqrt(3) / 2)
            for j in range(size)
            for i in range(size)
        ]
    )
    rows = np.repeat(np.arange(size), size)
    # (n_pairs, 2) even when r_cut reaches no neighbour (an empty graph never spans)
    pairs = np.array(
        sorted(cKDTree(coords).query_pairs(r_cut * (1 + 1e-9))), dtype=int
    ).reshape(-1, 2)
    lo, hi = 0.0, 1.0
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        if spanning_probability(coords, rows, pairs, size, mid, trials, rng) < 0.5:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def otoc_squared_commutator(h, psi0, w, v, ts):
    """C(t) = <psi|[W(t),V]^dag [W(t),V]|psi> -- grows from 0 as W(t) spreads onto V's site (scrambling)."""
    evals, evecs = eigh(h)
    out = []
    for t in ts:
        u = evecs @ (np.exp(-1j * evals * t)[:, None] * evecs.conj().T)
        wt = u.conj().T @ w @ u
        comm = wt @ v - v @ wt
        out.append(float(np.vdot(comm @ psi0, comm @ psi0).real))
    return np.array(out)


def main():
    print("=" * 96)
    print(
        " PATH 2 — the ER=EPR/PBH network -> a Rydberg array (Pasqal/OVH): design + an exact small sim"
    )
    print("=" * 96)

    # ===== [1] the MSS reproduction: OBT's lambda_L is DEFINED as the MSS bound at T_H (theory.md) ====
    print(
        "\n[1] THE SCRAMBLING SCALE -- reproducing theory.md's DEFINITION lambda_L = 2 pi k_B T_H / hbar"
    )
    t_mss = (
        HBAR * LAMBDA_L / (2 * np.pi * KB)
    )  # T at which lambda_L = 2pi kT/hbar (MSS saturation)
    print(
        f"    OBT: lambda_L = {LAMBDA_L:.2e} /s, t* = {T_STAR*1e12:.1f} ps  (lambda_L * t* = {LAMBDA_L*T_STAR:.2f})"
    )
    print(f"    MSS-saturation temperature T = hbar*lambda_L/(2pi kB) = {t_mss:.0f} K")
    print(
        "    => recovers T_H ~ 900 K BY CONSTRUCTION: theory.md defines lambda_L = 2 pi k_B T_H/hbar"
    )
    print(
        "       (MSS saturation is ASSUMED for the PBHs, not derived). A reproduction, not a consilience."
    )
    assert (
        800 < t_mss < 1000
    ), "reproduction of theory.md's definition lambda_L = 2 pi k_B T_H/hbar at T_H ~ 900 K"

    # ===== [2] the Pasqal design params (computed) ====================================================
    print(
        "\n[2] THE PASQAL DESIGN -- blockade radius, spacing, the 2D array degree (computed)"
    )
    omega_si = 2 * np.pi * OMEGA_2PI  # rad/s
    r_b_um = (C6_OVER_HBAR / omega_si) ** (
        1 / 6
    ) * 1e6  # blockade radius where V(R_b) = hbar Omega, in um
    # 2D triangular array at SPACING_UM: count atoms within R_b of a central atom
    pts = [
        (i * SPACING_UM + 0.5 * SPACING_UM * (j % 2), j * SPACING_UM * np.sqrt(3) / 2)
        for i in range(-4, 5)
        for j in range(-4, 5)
    ]
    c = np.array([0.0, 0.0])
    dists = [float(np.linalg.norm(np.array(p) - c)) for p in pts]
    degree_2d = sum(0 < d <= r_b_um for d in dists)
    r_out = max(d for d in dists if 0 < d <= r_b_um)  # the outermost blockaded shell
    print(
        f"    Omega/2pi = {OMEGA_2PI/1e6:.0f} MHz, C6/2pi = {C6_OVER_HBAR / (2 * np.pi) * 1e36 / 1e9:.1f} GHz*um^6,"
        f" spacing = {SPACING_UM:.0f} um"
    )
    print(
        f"    blockade radius R_b = (C6/Omega)^(1/6) = {r_b_um:.2f} um  (> spacing -> neighbours blockaded);"
        f" outermost blockaded shell at {r_out:.2f} um, V/Omega = {(r_b_um / r_out) ** 6:.3f}"
    )
    print(
        f"    => a 2D triangular array gives degree ~ {degree_2d} (atoms within R_b) vs OBT's expander d = {D_EXPANDER}"
    )
    # site percolation of the ACTUAL blockade graph, computed -- not assumed to be the nearest-neighbour 0.5
    rng_perc = np.random.default_rng(20261007)
    pc_nn = site_percolation_threshold(SPACING_UM, SPACING_UM, 48, rng_perc)
    assert (
        abs(pc_nn - 0.5) < 0.03
    ), "reproduction: nearest-neighbour triangular site percolation p_c = 1/2 (exact, finite-size L=48)"
    pc_2d = site_percolation_threshold(r_b_um, SPACING_UM, 48, rng_perc)
    print(
        f"       percolation (site, MC, L=48): nearest-neighbour check p_c = {pc_nn:.3f} (exact 1/2 reproduced);"
    )
    print(
        f"       the degree-{degree_2d} blockade graph p_c = {pc_2d:.3f} vs the expander ~1/(d-1) = {PC_EXPANDER:.3f}"
    )
    print(
        f"       (site loss tolerated: {1 - pc_2d:.0%} for the 2D graph vs {1 - PC_EXPANDER:.0%} for the expander;"
    )
    print("       2D geometry cannot reach the expander's robustness).")
    print(
        f"       (the outermost shell is blockaded only marginally, V/Omega = {(r_b_um / r_out) ** 6:.3f}: without it"
        f" the graph is the nearest-neighbour one, p_c = {pc_nn:.3f})"
    )

    # ===== [3] the exact small sim: the quench scrambles + entangles (numpy, N=10) ====================
    print(
        "\n[3] THE EXACT SMALL SIM -- germe |g..g> -> quench -> scrambling (OTOC) + entanglement (N=10)"
    )
    n = 10
    positions = [
        (i, 0.0) for i in range(n)
    ]  # a 1D chain (clean light-cone for the OTOC)
    omega, delta, c6_dimless = (
        1.0,
        1.0,
        2.0,
    )  # units of Omega; V_nn = c6_dimless (moderate blockade)
    h = rydberg_hamiltonian(positions, omega, delta, c6_dimless)
    psi0 = np.zeros(2**n)
    psi0[0] = 1.0  # the germe = |g..g> = |0..0> (low entanglement)
    ts = np.linspace(
        0, 16, 33
    )  # long enough for the OTOC light-cone to traverse the chain
    evals, evecs = eigh(h)
    s_t, surv = [], []
    for t in ts:
        psit = evecs @ (np.exp(-1j * evals * t) * (evecs.conj().T @ psi0))
        s_t.append(entanglement_entropy(psit, n, n // 2))
        surv.append(abs(np.vdot(psi0, psit)) ** 2)
    s_t = np.array(s_t)
    w0, vlast = site(Z, 0, n), site(
        Z, n - 1, n
    )  # OTOC between the two ends of the chain
    c_otoc = otoc_squared_commutator(h, psi0, w0, vlast, ts)
    # Page's exact mean entropy of a random pure state on dims m = d_A <= n = d_B (the volume-law reference):
    # S = sum_{k=n+1}^{mn} 1/k - (m-1)/(2n)
    d_a, d_b = 2 ** (n // 2), 2 ** (n - n // 2)
    s_page = float(
        np.sum(1.0 / np.arange(d_b + 1, d_a * d_b + 1)) - (d_a - 1) / (2 * d_b)
    )
    print(
        f"    entanglement entropy S(half): {s_t[0]:.2f} (germe) -> {s_t.max():.2f} nat (grows + saturates;"
        f" Page random-state value {s_page:.2f} = the volume law)"
    )
    print(
        f"    OTOC end-to-end C(t): {c_otoc[0]:.3f} (t=0) -> {c_otoc.max():.3f} (scrambles: info spreads 0 -> {n-1})"
    )
    print(
        f"    germe survival |<g..g|psi(t)>|^2: {surv[0]:.2f} -> {min(surv):.3f} (the germe decompresses)"
    )
    print(
        "    => the quench SCRAMBLES (OTOC grows from 0) and ENTANGLES (S grows from 0) -- GENERIC for"
    )
    print(
        "       any interacting chain (here exactly, N=10); not an OBT-specific signature."
    )
    assert (
        abs(s_t[0]) < 1e-12
    ), "identity: the product germe |g..g> has zero entanglement"
    assert (
        abs(c_otoc[0]) < 1e-12
    ), "identity: operators on distinct sites commute at t=0"

    # ===== [4] the honest reach + the verdict ========================================================
    print(
        "\n[4] THE HONEST REACH (the calculations decide) + the Pasqal large-run spec"
    )
    print(
        "    PASQAL CAN test (quantum-advantage at N~100, classically intractable): the quench dynamics,"
    )
    print(
        "    the scrambling (OTOC), the entanglement growth (toward a thermal VOLUME law after a quench),"
    )
    print("    the array percolation.")
    print(
        "    PASQAL CANNOT match: (1) the MSS-SATURATING fast scrambler (T_H~900 K, SYK universality) --"
    )
    print(
        "    Rydberg sub-saturates the MSS bound (it is not SYK); (2) the degree-46 EXPANDER -- a 2D"
    )
    print(
        f"    blockade graph is degree ~{degree_2d}, p_c={pc_2d:.3f} vs the expander {PC_EXPANDER:.3f}. -> Pasqal is a PROXY for"
    )
    print(
        "    generic quench DYNAMICS, not OBT's SYK/expander STRUCTURE (that needs an SYK simulator / 3D)."
    )
    print(
        "    LARGE-RUN SPEC (Pasqal via OVHcloud/Scaleway): N~100 atoms, a 2D/3D array, quench (Omega,delta)"
    )
    print(
        "    ramp, measure OTOC + S(A) + the connected correlations -> read the scrambling/entanglement of"
    )
    print(
        "    the OBT-network MODEL on real atoms. VERDICT: NOT a test of OBT -- the reachable behavior is"
    )
    print(
        "    generic quench scrambling, and the OBT-specific claims (MSS saturation, expander) are out of Pasqal's"
    )
    print(
        "    reach (the platform's geometry, computed above) and would need an SYK-class simulator."
    )

    print(
        "\n  COMPUTED: the lambda_L definition reproduced (T_H=900K in -> lambda_L out); R_b + 2D degree + its site-"
    )
    print("  percolation threshold (MC, validated on the exact nearest-neighbour 1/2);")
    print(
        "  the N=10 quench (growth reported). CITED, not computed: Rydberg sub-saturates MSS; no expander."
    )
    print(
        "  REPORTED (no imposed ranges): the entropy/OTOC values, the honest reach. seul les calculs comptent."
    )
    print("=" * 96)


if __name__ == "__main__":
    main()
