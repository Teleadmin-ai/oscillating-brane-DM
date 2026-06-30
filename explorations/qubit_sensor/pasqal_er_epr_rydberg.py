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

WHAT IT TESTS (build-on-OBT): does OBT's network, realized on real neutral-atom hardware, exhibit the
many-body behavior OBT claims -- fast scrambling, entanglement growth, robustness? Classically intractable
beyond ~50 atoms (2^N) -> a quantum-advantage simulation on Pasqal (via OVHcloud / Scaleway, Romain's
sovereign ecosystem). This is a quantum SIMULATION of OBT's MODEL (you read the model's behavior on real
atoms), NOT a measurement of the real bulk.

THE HONEST REACH (computed below -- the calculations decide, not me):
  + Pasqal CAN simulate: the quench dynamics, scrambling (OTOC), entanglement growth, the array percolation.
  - Pasqal CANNOT match: (1) the MSS-SATURATING fast scrambler (lambda_L = 2pi kT/hbar at T_H~900K) -- that
    is SYK / black-hole universality, NOT generic Rydberg (Rydberg sub-saturates); (2) the degree-46 EXPANDER
    -- a 2D blockade graph has degree ~18 (geometric, computed below), p_c ~ 0.5 vs the expander's ~0.022. So Pasqal
    is a PROXY for OBT's network DYNAMICS, not its exact SYK/expander structure (that needs an SYK simulator
    / 3D / higher connectivity). The mapping is approximate, by the geometry of the platform.

NOT V8.2. Not in the PDF. 'code, don't plead' + 'seul les calculs comptent' (Romain): the design params and
the exact small sim are COMPUTED and reported; asserted only are verifiable identities (OBT's lambda_L -> the
T_H=900K MSS consilience) + sim-correctness (the quench scrambles + entangles) -- no imposed result-ranges.
"""

from functools import reduce

import numpy as np
from scipy.linalg import eigh

# physical constants (SI)
HBAR = 1.054571817e-34
KB = 1.380649e-23

# OBT network numbers (CLAUDE.md)
LAMBDA_L = 7.4e14  # MSS Lyapunov / scrambling rate, s^-1
T_STAR = 0.2e-12  # scrambling time, s
D_EXPANDER = 46  # ER=EPR expander degree
PC_EXPANDER = 1.0 / (D_EXPANDER - 1)  # expander percolation threshold ~ 1/(d-1) ~ 0.022

# Pasqal Rydberg parameters (representative, Rb ~70S)
C6_OVER_2PI = (
    5420e9 * 1e-36
)  # C6/2pi in Hz*m^6 (5420 GHz*um^6 -> Hz*m^6); um=1e-6 m -> um^6=1e-36 m^6
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

    # ===== [1] the MSS consilience: OBT's lambda_L is MSS-saturating at the PBH Hawking temperature ====
    print(
        "\n[1] THE SCRAMBLING SCALE -- OBT's lambda_L vs the MSS bound (a verifiable identity)"
    )
    t_mss = (
        HBAR * LAMBDA_L / (2 * np.pi * KB)
    )  # T at which lambda_L = 2pi kT/hbar (MSS saturation)
    print(
        f"    OBT: lambda_L = {LAMBDA_L:.2e} /s, t* = {T_STAR*1e12:.1f} ps  (lambda_L * t* = {LAMBDA_L*T_STAR:.2f})"
    )
    print(f"    MSS-saturation temperature T = hbar*lambda_L/(2pi kB) = {t_mss:.0f} K")
    print(
        "    => this EQUALS the PBH Hawking temperature T_H ~ 900 K (CLAUDE.md) -- OBT's network is a"
    )
    print(
        "       black-hole-class MSS-SATURATING fast scrambler (SYK universality), by its own numbers."
    )
    assert (
        800 < t_mss < 1000
    ), "OBT's lambda_L must be MSS-saturating at T_H ~ 900 K (verifiable identity)"

    # ===== [2] the Pasqal design params (computed) ====================================================
    print(
        "\n[2] THE PASQAL DESIGN -- blockade radius, spacing, the 2D array degree (computed)"
    )
    omega_si = 2 * np.pi * OMEGA_2PI  # rad/s
    c6_si = 2 * np.pi * C6_OVER_2PI  # rad*m^6/s
    r_b_um = (c6_si / omega_si) ** (
        1 / 6
    ) * 1e6  # blockade radius where V(R_b)=Omega, in um
    # 2D triangular array at SPACING_UM: count atoms within R_b of a central atom
    pts = [
        (i * SPACING_UM + 0.5 * SPACING_UM * (j % 2), j * SPACING_UM * np.sqrt(3) / 2)
        for i in range(-4, 5)
        for j in range(-4, 5)
    ]
    c = np.array([0.0, 0.0])
    degree_2d = sum(0 < np.linalg.norm(np.array(p) - c) <= r_b_um for p in pts)
    print(
        f"    Omega/2pi = {OMEGA_2PI/1e6:.0f} MHz, C6/2pi = {C6_OVER_2PI*1e36/1e9:.0f} GHz*um^6, spacing = {SPACING_UM:.0f} um"
    )
    print(
        f"    blockade radius R_b = (C6/Omega)^(1/6) = {r_b_um:.1f} um  (> spacing -> neighbours blockaded)"
    )
    print(
        f"    => a 2D triangular array gives degree ~ {degree_2d} (atoms within R_b) vs OBT's expander d = {D_EXPANDER}"
    )
    print(
        f"       percolation: 2D site p_c ~ 0.5 vs the expander p_c ~ 1/(d-1) = {PC_EXPANDER:.3f} (the expander is"
    )
    print(
        "       far more robust; 2D geometry cannot reach the expander's connectivity)."
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
    print(
        f"    entanglement entropy S(half): {s_t[0]:.2f} (germe) -> {s_t.max():.2f} bits-nat (grows + saturates)"
    )
    print(
        f"    OTOC end-to-end C(t): {c_otoc[0]:.3f} (t=0) -> {c_otoc.max():.3f} (scrambles: info spreads 0 -> {n-1})"
    )
    print(
        f"    germe survival |<g..g|psi(t)>|^2: {surv[0]:.2f} -> {min(surv):.3f} (the germe decompresses)"
    )
    print(
        "    => the quench SCRAMBLES (OTOC grows from 0) and ENTANGLES (S grows from 0) -- the OBT"
    )
    print(
        "       many-body behavior emerges on the Rydberg Hamiltonian (here exactly, N=10)."
    )
    assert (
        s_t.max() > s_t[0] + 0.5
    ), "the quench must grow entanglement (the germe decompresses)"
    assert (
        c_otoc.max() > c_otoc[0] + 0.1
    ), "the OTOC must grow from 0 (scrambling: info reaches the far end)"

    # ===== [4] the honest reach + the verdict ========================================================
    print(
        "\n[4] THE HONEST REACH (the calculations decide) + the Pasqal large-run spec"
    )
    print(
        "    PASQAL CAN test (quantum-advantage at N~100, classically intractable): the quench dynamics,"
    )
    print(
        "    the scrambling (OTOC), the entanglement growth (RT-like area law), the array percolation."
    )
    print(
        "    PASQAL CANNOT match: (1) the MSS-SATURATING fast scrambler (T_H~900 K, SYK universality) --"
    )
    print(
        "    Rydberg sub-saturates the MSS bound (it is not SYK); (2) the degree-46 EXPANDER -- a 2D"
    )
    print(
        f"    blockade graph is degree ~{degree_2d}, p_c~0.5 vs the expander {PC_EXPANDER:.3f}. -> Pasqal is a PROXY for"
    )
    print(
        "    OBT's network DYNAMICS, not its SYK/expander STRUCTURE (that needs an SYK simulator / 3D)."
    )
    print(
        "    LARGE-RUN SPEC (Pasqal via OVHcloud/Scaleway): N~100 atoms, a 2D/3D array, quench (Omega,delta)"
    )
    print(
        "    ramp, measure OTOC + S(A) + the connected correlations -> read the scrambling/entanglement of"
    )
    print(
        "    the OBT-network MODEL on real atoms. VERDICT: a genuine but PARTIAL test -- it confirms (or"
    )
    print(
        "    breaks) OBT's qualitative many-body dynamics; the MSS/expander specifics are out of Pasqal's"
    )
    print(
        "    reach (the platform's geometry, computed above) and would need an SYK-class simulator."
    )

    print(
        "\n  COMPUTED: MSS->T_H=900K identity; R_b + 2D degree; the N=10 quench scrambles + entangles."
    )
    print(
        "  REPORTED (no imposed ranges): the entropy/OTOC values, the honest reach. seul les calculs comptent."
    )
    print("=" * 96)


if __name__ == "__main__":
    main()
