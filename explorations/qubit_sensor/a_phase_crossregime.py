"""Seed 3 (V9.0, quarantined) — the CROSS-REGIME consistency test (Romain: the same a^-3 field that fits
the CMB must give the galaxy RAR without an independent halo, else it over-clumps and breaks OBT's crown
jewel). This is the seam between the CMB leg (just done) and the V8.2 galaxy MOND. Reviewer-mode: look for
where it breaks.

THE QUESTION. The A-phase fix gave OBT an a^-3 component (the mimetic/aether dust) for the CMB peaks. But
a^-3 dust with c_s^2=0 clusters EXACTLY like CDM. So evolved to z=0 it would form NFW halos at galaxies ->
galaxies get a CDM halo -> the RAR (zero-halo, mu(x)-only) BREAKS. Does it?

WHAT THIS COMPUTES (rigorous parts) + WHAT IT SCOPES (the open nonlinear piece):

[1] The two MOND triggers. Real MOND is ACCELERATION-based: modify when g < a0 (a0=cH/2pi). My CMB CLASS
    implementation used a horizon-SCALE proxy x_H = 2*pi*k/k_H (k_H=aH). They COINCIDE at the CMB (where
    a_H/a0 = 2pi exactly, so sub-horizon acoustic scales are Newtonian) but DIVERGE by ~7 orders at z=0
    galaxies: x_H ~ 1e6 (deeply sub-horizon -> the proxy says CDM) while g/a0 ~ 0.3 (the real MOND -> the
    RAR). So my CLASS proxy is CMB-valid but galaxy-INVALID -- it contains NO galaxy MOND.

[2] The linear z=0 matter power spectrum P(k) from my CLASS. The dynamical aether at A_dyn=1 SUPPRESSES
    small-scale power (~71% at k~9/Mpc) -- NOT zero, because dev_eff*k^2 -> const at high k, so the chi
    is sourced at all small scales (relire-en-boucle CAUGHT the naive 'dev_eff->0 => no galaxy effect').
    BUT the CMB constrains A_dyn ~ 0 -> at the data-preferred value the linear field is ~CDM-like at
    galaxy scales -> it WOULD over-clump; the suppression that could prevent halos is CMB-DISFAVORED.

[3] The acceleration map a0(z)=cH/2pi: CMB sub-horizon g/a0 >> 1 (Newtonian, peaks fit); galaxy outskirts
    g/a0 < 1 (MOND, the RAR). ONE function mu(g/a0) with a0=cH/2pi spans both -- the unification is the
    ACCELERATION variable (derived in a_phase_aest_action), NOT the scale proxy my linear CLASS used.

THE HONEST VERDICT (answering 'is it contradictory? is it true?'):
 * NOT mathematically contradictory -- every calc is exact + consistent. The CMB fit is TRUE (linear, the
   a^-3 field clusters like CDM -> peaks; A_dyn~0).
 * BUT the full claim -- ONE field does CMB (CDM-like) AND galaxy RAR (MOND) with NO double-DM -- is NOT
   demonstrated. My CLASS used a horizon-SCALE proxy that fits the CMB but gives NO galaxy MOND (it is
   CDM at galaxy scales, off by ~7 orders from the real acceleration-based MOND).
 * KEY TENSION (relire-caught, SUGGESTIVE): the dynamical aether's LINEAR P(k) effect is a SUPPRESSION
   (-71% at k~9 for A_dyn=1) -- the very thing that could keep the a^-3 field from clustering into galaxy
   halos. But that is EXACTLY what the CMB DISFAVORS (A_dyn~0). So the CMB pushes the field toward CDM-like
   clustering at galaxies (over-clump), while avoiding halos / the RAR wants the opposite. SUGGESTIVE only:
   the linear chi amplitude A_dyn is not rigorously the same lever as the nonlinear galaxy mu(x). The
   RIGOROUS core is the regime separation (the galaxy RAR is the NONLINEAR acceleration-based mu(g/a0)
   regime, not my linear scale-proxy CLASS) + the CDM-EQUIVALENT CMB field. AeST reorganizes it in the
   quasi-static nonlinear limit; for OBT's mu(x) it is NOT demonstrated -- the closure-adjacent open piece.
 * So the CMB leg (linear) and the galaxy RAR (nonlinear, V8.2) are SEPARATE regime computations, linked
   analytically by a0=cH/2pi, not by one numerical field. The 'contradiction' you sensed is the
   linear-CMB-CDM vs nonlinear-galaxy-MOND REGIME GAP, bridged only analytically. It is FALSIFIABLE: if
   the nonlinear MOND does not reorganize the CDM-like clustering at galaxies, OBT-AeST over-clumps and
   breaks the RAR. This is the genuine open piece -- exactly V8.2's 'an essential ingredient may be missing'.

NOT V8.2. Not in the PDF. 'code, don't plead': the triggers + the a_H/a0=2pi + the P(k) computed/asserted.
Needs the dynamical-aether classy (--force-reinstall).
"""

import os

import numpy as np

C = 2.998e8  # m/s
MPC = 3.086e22  # m
KPC = 3.086e19  # m
H0_SI = 67.36e3 / MPC  # s^-1
A0_0 = C * H0_SI / (2 * np.pi)  # MOND scale today, m/s^2
OM, OR = 0.31, 9.2e-5
OL = 1 - OM - OR


def Hz(z):
    return H0_SI * np.sqrt(OM * (1 + z) ** 3 + OR * (1 + z) ** 4 + OL)


def a0(z):
    return C * Hz(z) / (2 * np.pi)


def pk_z0(A_dyn):
    """Linear z=0 P(k) (Mpc^3) from my CLASS; A_dyn = the dynamical aether amplitude (env var)."""
    from classy import Class

    os.environ["OBT_AEST_A"] = "0"
    os.environ["OBT_AEST_DYN"] = str(A_dyn)
    m = Class()
    m.set(
        {
            "output": "mPk",
            "gauge": "newtonian",
            "P_k_max_1/Mpc": 20.0,
            "z_max_pk": 1.0,
            "H0": 67.36,
            "omega_b": 0.02237,
            "omega_cdm": 0.120,
            "n_s": 0.9649,
            "A_s": 2.1e-9,
            "tau_reio": 0.0544,
        }
    )
    m.compute()
    ks = np.logspace(-3, np.log10(15), 60)  # 1/Mpc
    pk = np.array([m.pk_lin(k, 0.0) for k in ks])
    m.struct_cleanup()
    return ks, pk


def main():
    print("=" * 94)
    print(
        " CROSS-REGIME TEST — does the CMB-fitting a^-3 field over-clump at galaxies + break the RAR?"
    )
    print("=" * 94)

    # [1] the two triggers: acceleration g/a0 vs the horizon-scale proxy x_H ----------
    print(
        "\n[1] TWO MOND TRIGGERS — acceleration (real) vs horizon-scale (my CLASS proxy)"
    )
    kH0 = H0_SI / C * MPC  # comoving 1/Mpc
    # galaxy (z=0): outskirt MOND, inner Newtonian
    g_out = (150e3) ** 2 / (20 * KPC)
    g_in = (150e3) ** 2 / (2 * KPC)
    k_gal = 1.0 / 0.02  # ~20 kpc, comoving 1/Mpc
    xH_gal = 2 * np.pi * k_gal / kH0
    print(f"    galaxy outskirt: g/a0 = {g_out/A0_0:.2f}  (<1 => MOND, the RAR)")
    print(f"    galaxy inner:    g/a0 = {g_in/A0_0:.2f}  (>1 => Newtonian)")
    print(
        f"    horizon proxy at galaxy k: x_H = 2pi k/k_H = {xH_gal:.1e}  (>>1 => my CLASS says CDM)"
    )
    div = np.log10(xH_gal / (g_out / A0_0))
    print(
        f"    -> at the galaxy the two triggers DIVERGE by ~{div:.0f} orders (proxy CDM vs real MOND)"
    )
    assert (
        g_out / A0_0 < 1 < g_in / A0_0
    ), "galaxy must span Newtonian(inner) -> MOND(outskirt)"
    assert (
        xH_gal > 1e5
    ), "the horizon proxy must be deeply sub-horizon (CDM) at galaxy scales"

    # the CMB: a_H/a0 = 2pi exactly -> the proxy COINCIDES with the acceleration trigger there
    aH_aratio = (C * Hz(1100)) / a0(1100)
    print(
        f"\n    at recombination: a_H/a0 = cH/(cH/2pi) = {aH_aratio:.4f} (=2pi) -> sub-horizon acoustic"
    )
    print(
        "    scales are Newtonian (g/a0 = 2pi*(k/k_H) >> 1) -> CDM -> the peaks fit. The proxy is"
    )
    print(
        "    CMB-VALID (it equals the acceleration trigger in the linear regime) but galaxy-INVALID."
    )
    assert abs(aH_aratio - 2 * np.pi) < 1e-6, "a_H/a0 must equal 2pi exactly"

    # [2] the linear z=0 P(k): the aether's small-scale effect + the CMB constraint ---
    # (relire-en-boucle CATCH: the naive 'dev_eff->0 sub-horizon => no galaxy effect' is WRONG --
    #  dev_eff*k^2 -> const at high k (dev_eff~1/(2x^2), x=2pi k/k_H), so the dynamical chi IS sourced at
    #  all small scales and SUPPRESSES P(k). But the CMB constrains the amplitude A_dyn ~ 0.)
    print(
        "\n[2] LINEAR z=0 P(k) from CLASS — the dynamical aether's small-scale effect vs the CMB bound"
    )
    ks, pk0 = pk_z0(0.0)  # A_dyn=0 = LambdaCDM (CDM-like)
    _, pk1 = pk_z0(
        1.0
    )  # A_dyn=1 (the 'natural' OBT amplitude; CMB-disfavored at 2.3 sigma)
    for ktest in [0.05, 1.0, 10.0]:
        i = int(np.argmin(np.abs(ks - ktest)))
        print(f"    k={ks[i]:7.3f}/Mpc:  P(A_dyn=1)/P_LCDM = {pk1[i]/pk0[i]:.4f}")
    i9 = int(np.argmin(np.abs(ks - 9.0)))
    supp = 1 - pk1[i9] / pk0[i9]
    print(
        f"    -> A_dyn=1 SUPPRESSES small-scale power by up to {100*supp:.0f}% at k~9/Mpc (the propagating"
    )
    print(
        "       chi: dev_eff*k^2 -> const at high k -> it sources chi at ALL small scales, NOT zero)."
    )
    print(
        "    BUT the CMB constrains A_dyn = -0.02 +/- 0.44 (~0) -> the suppression is CMB-DISFAVORED"
    )
    print(
        "    (A_dyn=1 at 2.3 sigma) -> at the data-preferred A_dyn~0 the linear field is ~CDM-like at"
    )
    print(
        "    galaxy scales (P~LambdaCDM) -> it WOULD over-clump like CDM. The suppression that could"
    )
    print(
        "    prevent halos is exactly what the CMB does not want -- the KEY TENSION (see the verdict)."
    )
    assert (
        supp > 0.1
    ), "the dynamical chi DOES modify small scales (corrects the naive dev_eff->0)"
    # caveat: the exact suppression is a property of the RECONSTRUCTED chi EOM (cs^2=1, the source form)

    # [3] the acceleration map across z ----------------------------------------------
    print(
        "\n[3] THE UNIFICATION VARIABLE — a0(z)=cH/2pi, the ACCELERATION g/a0 (not the scale)"
    )
    print(
        f"    a0(0)={a0(0):.2e}  a0(z=1)={a0(1):.2e}  a0(rec)={a0(1100):.2e} m/s^2 (grows as cH)"
    )
    print(
        "    ONE function mu(g/a0) spans both regimes: CMB sub-horizon g/a0>>1 (Newtonian->CDM->peaks);"
    )
    print(
        "    galaxy outskirt g/a0<1 (MOND->RAR). Derived in a_phase_aest_action. But it is the"
    )
    print(
        "    ACCELERATION variable -- my linear CLASS used the scale proxy, valid only at the CMB."
    )

    # ---- verdict ------------------------------------------------------------------
    print(
        "\n[VERDICT] not contradictory; the CMB fit is true; the UNIFIED field is NOT shown — a real tension"
    )
    print(
        "    * The CMB leg is TRUE (linear: A_dyn = -0.02 +/- 0.44 ~ 0 -> the a^-3 field clusters like"
    )
    print(
        "      CDM -> the peaks). Each calculation is exact -> there is NO mathematical contradiction."
    )
    print(
        "    * TWO MOND TRIGGERS DIVERGE: my CLASS used the horizon-SCALE proxy x_H = 2pi k/k_H, which"
    )
    print(
        f"      equals the real acceleration trigger g/a0 at the CMB (a_H/a0=2pi) but is off by ~{div:.0f} orders"
    )
    print(
        "      at z=0 galaxies (x_H~1e6 [CDM] vs g/a0~0.35 [MOND]). So my CLASS holds NO galaxy MOND --"
    )
    print(
        "      it is a linear-cosmological device; the galaxy RAR is a different (acceleration) regime."
    )
    print(
        "    * KEY TENSION (the relire-caught find): the dynamical aether's LINEAR effect on galaxy-scale"
    )
    print(
        f"      P(k) is a SUPPRESSION ({100*supp:.0f}% at k~9 for A_dyn=1). That suppression is what could keep the"
    )
    print(
        "      a^-3 field from clustering into galaxy halos -- but it is EXACTLY what the CMB DISFAVORS"
    )
    print(
        "      (A_dyn~0). So the CMB pushes the field toward CDM-like clustering at galaxies (CDM-like"
    )
    print(
        "      seeds -> tends to over-clump), while avoiding halos / the RAR wants the opposite: at the"
    )
    print("      LINEAR level the CMB and the no-halo RAR pull OPPOSITELY on A_dyn.")
    print(
        "    * The galaxy RAR (no halo) is NONLINEAR + acceleration-based (mu(g/a0), g<a0). AeST resolves"
    )
    print(
        "      it in the quasi-static nonlinear limit (the field config is tied to the baryons by mu, so"
    )
    print(
        "      it does NOT form an independent halo despite CDM-like linear seeds). OBT-AeST inherits the"
    )
    print(
        "      structure; for OBT's mu(x) it is NOT demonstrated -- the closure-adjacent open piece."
    )
    print(
        "    * ANSWER (is it contradictory? is it true?): every calc is exact -> NOT a contradiction; the"
    )
    print(
        "      CMB fit is TRUE. But the unification is leg-by-leg + analytic (a0=cH/2pi), NOT one"
    )
    print(
        "      end-to-end field, and the CMB (A_dyn~0) leaves the field CDM-like at galaxy linear scales"
    )
    print(
        "      -> the WHOLE burden of the no-halo RAR falls on the UNPROVEN nonlinear MOND reorganization."
    )
    print(
        "      FALSIFIABLE: if it does not reorganize, OBT-AeST over-clumps galaxies and breaks the RAR."
    )
    print(
        "      This IS V8.2's flagged 'an essential ingredient may still be missing' -- now located: the"
    )
    print(
        "      linear/nonlinear seam, with the CMB pushing the wrong way at the linear level."
    )
    print(
        "    * HONEST SCOPE: the 'tension' is SUGGESTIVE -- the linear chi amplitude A_dyn is not"
    )
    print(
        "      rigorously the same lever as the nonlinear galaxy mu(x), and the P(k) suppression depends"
    )
    print(
        "      on the reconstructed chi EOM (cs^2=1). The RIGOROUS, reconstruction-independent core: (i)"
    )
    print(
        "      my CLASS MOND trigger is SCALE-based, off ~7 orders from the real acceleration MOND at"
    )
    print(
        "      galaxies; (ii) at the CMB-preferred A_dyn~0 the field is CDM-EQUIVALENT at galaxy linear"
    )
    print(
        "      scales; (iii) the galaxy RAR is the separate nonlinear/acceleration regime. So 'OBT-AeST"
    )
    print(
        "      fits the CMB' = 'a CDM-equivalent fits the CMB' -- NOT OBT's distinctive geometry; the"
    )
    print("      link to the galaxy RAR is the unproven nonlinear seam.")

    print(
        "\n  ALL INJECTION TESTS PASSED (galaxy spans N->MOND; a_H/a0=2pi; proxy diverges 7 orders;"
    )
    print(
        "  chi SUPPRESSES small-scale P(k), CMB-constrained to ~0 -> the linear/nonlinear seam tension)."
    )
    print("=" * 94)


if __name__ == "__main__":
    main()
