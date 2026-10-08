"""Seed 3 (V9.0, quarantined) — THE GERME'S WIDTH: derived, or a resolution artifact? (Oct 2026 reviewer
reread, point 4, Romain's 'vas y je suis tes reco'.)

THE QUESTION. demon_qc / belenos_job encode 'the canonical germe' = germe_decompression's radion wavepacket,
amp(i) = exp(-(i - k0)^2 / 2) on a register spanning phi/M_s in [0, 2.5]. Its CENTER k0 is OBT-derived (up to
the IC phi0). Its WIDTH is 'one grid bin' -- a property of the register, not of the radion. What width does
the PHYSICS give? The calculation decides; nothing below is imposed.

WHAT IS COMPUTED:
 [0] the IC candidates, reproduced from germe_decompression's corrected misalignment: phi_DM (radion = all the
     DM), the legacy 1.40 (its abundance), the Gate-11 ceiling (a CDM-like condensate is f < 4% of the DM).
 [1] the canonical width in PHYSICAL units, per register size (exact std of phi under |psi|^2).
 [2] the PHYSICAL in-patch spread: a light spectator radion fluctuates by H_inf/2pi per e-fold during inflation;
     those fluctuations are CDM isocurvature, bounded by Planck. For a radion that is a fraction f of the DM
     (phi0 = phi_DM sqrt f):  S = f * 2 dphi/phi0 <= S_max  ->  dphi <= S_max phi_DM / (2 sqrt f);
     the spread inside our observable patch sums N_obs e-folds: sigma_patch = dphi sqrt(N_obs).
     (Valid in the linear regime sigma_patch << phi0, i.e. f >~ S_max sqrt(N_obs)/2 ~ 3.5e-5; rows outside
     it are flagged in the table, not used.)
     (If the radion is instead HEAVY during inflation, it does not fluctuate: the width is even smaller. So
     the isocurvature bound is an UPPER bound on the physical in-patch width in every case.)
 [3] the ACROSS-PATCH (ensemble) width: (H/2pi) sqrt(N_tot - N_obs) -- N_tot is unobservable, so this width is
     a FREE parameter; and super-horizon modes are squeezed (decohered) -> our patch has a classical phi0.
 [4] the consequence for the demon: the physical in-patch germe is ONE register bin |k0> at any register size
     up to ~17 qubits; its 'tree' is one COLUMN of the declared unitary (identity asserted at the belenos size).

NOT V8.2. Not in the PDF. seul les calculs comptent: asserted only reproductions (phi_DM = 0.42) and
identities (grid spacing, canonical formula, sigma_patch = dphi sqrt(N_obs), delta-germe tree = a column of U,
normalization).
"""

import belenos_job as bj  # the declared belenos instance: product_unitary at n = 3 (DIM = 8)
import demon_qc  # the canonical germe + the declared SYK seed (no re-implementation)
import germe_decompression as gd  # the corrected misalignment abundance (reduced Planck mass)
import numpy as np

GRID_MAX = 2.5  # the canonical register spans phi/M_s in [0, 2.5] (germe_decompression)
A_S = 2.1e-9  # Planck scalar amplitude
# Planck 2018 CDM isocurvature fraction bound (as in germe_isocurvature)
BETA_ISO = 0.038
N_OBS = 60  # e-folds of modes inside our observable patch (bracket 50 reported)
OMEGA_DM_H2 = 0.120
# Gate 11: a CDM-like 0.36-eV condensate halos galaxies -> f < 4% of the DM
F_GATE11 = 0.04
M_S_GEV = 1.19e12
N_SIZES = (3, 5, 6, 10, 12)


def bin_width(n):
    """Grid spacing of the canonical register, in M_s (the 'width' of the canonical germe's amplitude)."""
    return GRID_MAX / (2**n - 1)


def phi_grid(n):
    return GRID_MAX * np.arange(2**n) / (2**n - 1)


def canonical_std(n, phi0):
    """Exact std of phi/M_s under |germe|^2 (includes the edge truncation of the grid)."""
    p = np.abs(demon_qc.germe_state(n, phi0=phi0)) ** 2
    g = phi_grid(n)
    mu = float((p * g).sum())
    return float(np.sqrt((p * (g - mu) ** 2).sum()))


def main():
    print("=" * 100)
    print(
        " THE GERME'S WIDTH — derived, or a resolution artifact? (the calculation decides)"
    )
    print("=" * 100)

    # ===== [0] the IC candidates (reproduced, not quoted) =====
    om_ms, _ = gd.misalignment_omega(gd.M_S, gd.M_PHI)  # Omega h^2 at phi0 = M_s
    phi_dm = float(np.sqrt(OMEGA_DM_H2 / om_ms))  # phi0/M_s for radion = all the DM
    assert (
        abs(phi_dm - 0.42) < 0.01
    ), "reproduction: the corrected all-DM phi0 = 0.42 M_s"
    om_140 = om_ms * 1.40**2
    phi_gate11 = phi_dm * np.sqrt(F_GATE11)
    print(
        "\n[0] THE IC CANDIDATES (germe_decompression's corrected misalignment, reproduced)"
    )
    print(
        f"      Omega h^2(phi0 = M_s) = {om_ms:.3f}  ->  radion = ALL the DM at phi0 = {phi_dm:.3f} M_s"
    )
    print(
        f"      legacy phi0 = 1.40 M_s -> Omega h^2 = {om_140:.2f} = {om_140/OMEGA_DM_H2:.0f}x the measured DM"
        "  -> OVER-PRODUCTION: excluded by the DM density itself"
    )
    print(
        f"      Gate 11 (a CDM-like condensate halos galaxies, f < {F_GATE11:.0%}) -> phi0 < {phi_gate11:.3f} M_s;"
    )
    print(
        f"      so phi0 = {phi_dm:.2f} (f = 1) is viable ONLY if the radion's a^-3 sector clusters MOND-like"
    )
    print(
        "      (the a_phase AeST reading -- the UNPROVEN galaxy seam), not as plain CDM."
    )

    # ===== [1] the canonical width in physical units =====
    print(
        "\n[1] THE CANONICAL WIDTH in physical units (amplitude width = 1 grid bin, by construction)"
    )
    print(
        "      n    modes    bin (M_s)    std of phi under |germe|^2 (M_s, phi0=0.42)"
    )
    canon_sd = {}
    for n in N_SIZES:
        g = phi_grid(n)
        assert np.allclose(
            np.diff(g), bin_width(n)
        ), "identity: grid spacing = 2.5/(2^n - 1)"
        k0 = 0.42 / GRID_MAX * (2**n - 1)
        ref = np.exp(-((np.arange(2**n) - k0) ** 2) / 2.0)
        assert np.allclose(
            demon_qc.germe_state(n, phi0=0.42), ref / np.linalg.norm(ref)
        ), "identity: demon_qc.germe_state == the canonical formula"
        canon_sd[n] = canonical_std(n, 0.42)
        print(f"     {n:2d}   {2**n:6d}    {bin_width(n):.2e}    {canon_sd[n]:.2e}")
    print(
        "    => the SAME 'canonical germe' is a different physical state at every register size:"
    )
    print("       its width is a property of the REGISTER, not of the radion.")

    # ===== [2] the physical in-patch spread (Planck isocurvature) =====
    s_max = float(np.sqrt(A_S * BETA_ISO / (1.0 - BETA_ISO)))
    print("\n[2] THE PHYSICAL IN-PATCH SPREAD — bounded by Planck CDM isocurvature")
    print(
        f"      beta_iso < {BETA_ISO} -> S_max = {s_max:.2e} per e-fold; sigma_patch = (H/2pi) sqrt(N_obs),"
        f" N_obs = {N_OBS}"
    )
    print(
        "      f (radion share)   phi0 (M_s)   H_inf max (GeV)   sigma_patch max (M_s)   in bins: n=3      n=10"
        "    sigma/phi0"
    )

    def sigma_max(f, n_obs=N_OBS):
        return s_max * phi_dm * np.sqrt(n_obs) / (2.0 * np.sqrt(f))

    for f in (1.0, F_GATE11, 1e-3, 1e-5):
        phi0 = phi_dm * np.sqrt(f)
        dphi = s_max * phi0 / (2.0 * f)  # per-e-fold, in M_s
        h_max = 2.0 * np.pi * dphi * M_S_GEV
        sp = sigma_max(f)
        assert (
            abs(sp - dphi * np.sqrt(N_OBS)) < 1e-15
        ), "identity: sigma_patch = dphi sqrt(N_obs)"
        # the linear isocurvature S = 2 dphi/phi0 needs the spread SMALL vs the mean; flag where it is not
        valid = "" if sp < phi0 else "  <- sigma >= phi0: linear formula INVALID here"
        print(
            f"      {f:9.0e}          {phi0:.2e}     {h_max:.2e}          {sp:.2e}            "
            f"{sp/bin_width(3):.1e}   {sp/bin_width(10):.1e}      {sp/phi0:.1e}{valid}"
        )
    # sigma_patch = phi0  <=>  S_max sqrt(N_obs) / (2 f) = 1
    f_cross = s_max * np.sqrt(N_OBS) / 2.0
    print(
        f"      (below a radion share f = S_max sqrt(N_obs)/2 = {f_cross:.1e} the bound leaves the linear regime:"
    )
    print(
        "      the radion is fluctuation-dominated, its mean is no 'displacement', and it is irrelevant to the DM)"
    )
    sp1 = sigma_max(1.0)
    n_res = int(np.ceil(np.log2(GRID_MAX / sp1 + 1.0)))
    print(
        f"      (N_obs = 50 instead of 60 changes sigma by {np.sqrt(50/60):.2f}x; the conclusion is insensitive)"
    )
    print(
        f"    => at f = 1 the physical spread is {sp1:.1e} M_s: ONE register bin needs n >= {n_res} qubits."
    )
    for n in (3, 10):
        excess = (canon_sd[n] / sp1) ** 2
        print(
            f"       read as an in-patch state, the canonical germe at n={n} carries {excess:.1e}x the"
            " isocurvature power Planck allows"
        )
    print(
        "       (and a heavy-during-inflation radion fluctuates even less: this is an UPPER bound on the width)."
    )

    # ===== [3] the ensemble (across-patch) width + decoherence =====
    print(
        "\n[3] THE ENSEMBLE (ACROSS-PATCH) WIDTH — the only place a broad 'germe' could live"
    )
    print(
        "      sigma_ens = (H/2pi) sqrt(N_tot - N_obs): N_tot (total e-folds) is unobservable -> FREE parameter."
    )
    print(
        f"      super-horizon modes are squeezed by ~e^(2N): for the largest observable mode e^(2N_obs) ~"
        f" 1e{2*N_OBS*np.log10(np.e):.0f}"
    )
    print(
        "      -> decohered (Polarski-Starobinsky): OUR patch carries a CLASSICAL phi0. A register superposition"
    )
    print(
        "      sum_k sqrt(p_k)|k> encodes the ENSEMBLE of patches (an Everett/stochastic ensemble), by convention."
    )

    # ===== [4] the consequence for the demon =====
    print(
        "\n[4] THE CONSEQUENCE FOR THE DEMON — the physical germe is ONE bin; its tree is ONE column of U"
    )
    # the declared belenos instance (same seed, same draw, same T as belenos_job)
    rng = np.random.default_rng(demon_qc.SEED)
    h = demon_qc.sparse_syk(bj.N_JOB, 2 * bj.N_JOB, rng)
    u = bj.product_unitary(h, demon_qc.SYK_T, reps=1)
    for phi0, label in (
        (phi_dm, "all-DM (f=1)"),
        (phi_gate11, "Gate-11 ceiling"),
        (0.0, "no displacement"),
    ):
        k0 = int(round(phi0 / GRID_MAX * (bj.DIM - 1)))
        delta = np.zeros(bj.DIM)
        delta[k0] = 1.0
        tree = np.abs(u @ delta) ** 2
        assert np.allclose(
            tree, np.abs(u[:, k0]) ** 2
        ), "identity: delta-germe tree = |column k0 of U|^2"
        assert abs(tree.sum() - 1.0) < 1e-12, "normalization"
        print(f"      phi0 = {phi0:.3f} M_s ({label:15s}) -> bin k0 = {k0} at n=3")
    canon_tree = np.abs(u @ demon_qc.germe_state(bj.N_JOB, phi0=phi_dm)) ** 2
    k_dm = int(round(phi_dm / GRID_MAX * (bj.DIM - 1)))
    tv = 0.5 * float(np.abs(canon_tree - np.abs(u[:, k_dm]) ** 2).sum())
    print(
        f"      canonical-germe tree vs the physical (delta) tree at n=3: TV = {tv:.3f}"
    )
    print(
        f"    => at the belenos size every Gate-11-viable phi0 (< {phi_gate11:.3f} M_s) falls in bin 0 -- the SAME"
    )
    print(
        "       register state as an undisplaced radion. The 'tree' of a physical germe is one column of"
    )
    print(
        "       the declared unitary: it carries phi0 to n bits, scrambled by a convention. Nothing else."
    )

    print("\n[VERDICT] the germe's width is NOT derived:")
    print(
        f"    * physical in-patch width <= {sp1:.1e} M_s (Planck isocurvature) -> a delta at any n <= {n_res-1};"
    )
    print(
        "    * the canonical 1-bin width, read as an in-patch state, is Planck-EXCLUDED; read as an ensemble"
    )
    print(
        "      state, its width is the free N_tot -- either way it is a convention, not OBT physics;"
    )
    print(
        f"    * phi0 = 1.40 over-produces the DM {om_140/OMEGA_DM_H2:.0f}x (excluded); phi0 = 0.42 needs the unproven"
    )
    print(
        "      AeST seam (else Gate 11 excludes it); the Gate-11-viable range is bin 0 on 8 modes."
    )
    print(
        "    The germe's CENTER is OBT physics (up to the IC); its WIDTH and its SUPERPOSITION are ours."
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
