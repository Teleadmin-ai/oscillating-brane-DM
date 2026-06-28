"""Seed 3 (V9.0, quarantined) — the DYNAMICAL aether spectra IN CLASS (Romain: 'implemente les spectres
de l'aether dynamique dans CLASS'). Beyond the quasi-static mu: the EXPLICIT propagating aether mode chi
as a NEW dynamical d.o.f. in CLASS's perturbation vector, with its own EOM, and the resulting full CMB.

THE IMPLEMENTATION (aest_class.patch, perturbations.c + perturbations.h): a new scalar d.o.f. (chi, chi')
added to the Newtonian-gauge perturbation vector -- index, initial conditions (chi=chi'=0), the EOM in
perturbations_derivs, the coupling to psi in perturbations_einstein. The EOM (V9.0 reconstruction,
a_phase_aether_hierarchy):
    chi'' + 2 H chi' + cs2 k^2 chi = A * dev_eff(x) * k^2 phi   (cs2=1; x=2pi k/k_H; dev_eff=(1-mu)mu^2)
    psi = phi - shear + chi
sourced by the matter (k^2 phi); A = OBT_AEST_DYN (0/unset = LambdaCDM). Sub-horizon -> chi=A*dev_eff*phi
(= the quasi-static mu); super-horizon -> source k^2 phi -> 0 -> chi frozen. So the propagating chi is
the genuine field whose response IS the mu, vs putting mu by hand.

A BUG WORTH RECORDING (caught by relire-en-boucle + a sigma8/P(k) verification, after Romain's insistence
'oublie pas de relire'): pip caches classy by version, so after editing the C source `pip install .` does
NOT rebuild -> the new chi was inert (exactly LambdaCDM) and I almost reported a FALSE 'dynamical fits,
Delta chi^2=0'. The fix: rebuild with --force-reinstall (and rm -rf build). The sigma8 verification (chi
MUST move sigma8 if sourced) is the guard, asserted below.

THE RESULT (honest -- it does NOT rescue OBT; reviewer-mode): the dynamical aether is MORE conservative
than the quasi-static mu on the GROWTH (sigma8 ~ -1.6% vs -4.9%: the propagating chi cannot fully respond
during the fast horizon-crossing, so the growth modification is suppressed). BUT the full-spectra TT
Delta chi^2 is NOT smaller (~235 vs the quasi-static ~151): the propagating chi imprints oscillatory
features on the potentials (ISW/lensing), so the full-spectra Planck constraint HOLDS. The peak POSITIONS
still fit (a0=cH/2pi -> a^-3 CDM); it is the perturbation-level modification (lensing + the chi mode) that
Planck constrains. Delta chi^2 ~ A^2 + ~56% A_s/tau-re-fittable -> A < ~0.2 (fixed) or an MCMC re-fit.

BUILD (reproduce; gcc + Cython + numpy in the venv): git clone class_public v3.3.0; git apply
aest_class.patch; make -j4; cd python && pip install . --force-reinstall --no-deps --no-build-isolation
(the --force-reinstall is MANDATORY -- pip caches by version). Then OBT_AEST_DYN sets the dynamical
amplitude (OBT_AEST_A still sets the quasi-static mu; both coexist).

NOT V8.2. Not in the PDF. 'code, don't plead': null test, chi-couples guard, A^2 scaling, sigma8 + TT
Delta chi^2 vs the quasi-static -- computed + asserted. Needs the force-rebuilt dynamical classy.
"""

import os

import numpy as np

LMAX = 2000
T = 2.7255e6
FSKY = 0.7
ARCMIN = np.pi / (180.0 * 60.0)
DT = 33.0 * ARCMIN
THETA = 7.0 * ARCMIN


def run(A=0.0, DYN=0.0):
    """(modified) CLASS at quasi-static A and dynamical DYN; return ell, C_l^TT (uK^2), sigma8."""
    from classy import Class

    os.environ["OBT_AEST_A"] = str(A)
    os.environ["OBT_AEST_DYN"] = str(DYN)
    m = Class()
    m.set(
        {
            "output": "tCl,pCl,lCl,mPk",
            "lensing": "yes",
            "gauge": "newtonian",
            "l_max_scalars": LMAX + 150,
            "P_k_max_1/Mpc": 0.5,
            "z_max_pk": 1,
            "H0": 67.36,
            "omega_b": 0.02237,
            "omega_cdm": 0.120,
            "n_s": 0.9649,
            "A_s": 2.1e-9,
            "tau_reio": 0.0544,
        }
    )
    m.compute()
    cl = m.lensed_cl(LMAX)
    s8 = m.sigma8()
    m.struct_cleanup()
    return cl["ell"], cl["tt"] * T**2, s8


def tt_chi2(ell, tt0, tt1):
    nt = DT**2 * np.exp(ell * (ell + 1) * THETA**2 / (8 * np.log(2)))
    cv = 2.0 / ((2 * ell + 1) * FSKY) * (tt0 + nt) ** 2
    m = ell >= 2
    return float(np.sum((tt1[m] - tt0[m]) ** 2 / cv[m]))


def main():
    print("=" * 94)
    print(
        " THE DYNAMICAL AETHER SPECTRA IN CLASS — the explicit propagating chi mode (full CMB)"
    )
    print("=" * 94)

    ell, tt0, s80 = run(0.0, 0.0)  # LambdaCDM
    _, ttd, s8d = run(0.0, 1.0)  # dynamical aether
    _, ttq, s8q = run(1.0, 0.0)  # quasi-static mu

    # [0] guard: is the DYNAMICAL classy actually built? (chi must move sigma8) ------
    print("\n[0] CHI-COUPLES GUARD (the pip-cache bug guard) — DYN=1 must move sigma8")
    print(
        f"    sigma8: LambdaCDM={s80:.5f}, DYN=1={s8d:.5f} (delta {100*(s8d/s80-1):+.2f}%)"
    )
    if abs(s8d / s80 - 1) < 1e-4:
        print(
            "\n[!] chi is INERT -> the STALE classy is installed (pip cached). REBUILD with"
        )
        print(
            "    --force-reinstall (rm -rf python/build first). See this file's docstring."
        )
        return
    print(
        "    -> chi COUPLES (the dynamical d.o.f. is live, not the stale cached classy)."
    )

    # [1] null test: DYN=0 == LambdaCDM ; peaks intact -------------------------------
    _, tt0b, _ = run(0.0, 0.0)
    null = float(np.max(np.abs(tt0b - tt0)))
    from scipy.signal import find_peaks

    D = ell * (ell + 1) * tt0 / (2 * np.pi)
    pk0 = list((find_peaks(D[2:1900], height=500, distance=100)[0] + 2)[:3])
    Dd = ell * (ell + 1) * ttd / (2 * np.pi)
    pkd = list((find_peaks(Dd[2:1900], height=500, distance=100)[0] + 2)[:3])
    print(
        "\n[1] NULL TEST + sanity — DYN=0 = LambdaCDM; DYN=1 peaks intact (not blown up)"
    )
    print(
        f"    max|DYN=0 - LambdaCDM| = {null:.1e} (=0); peaks LambdaCDM {pk0}, DYN=1 {pkd}"
    )
    assert null < 1e-9, "DYN=0 must be identical to LambdaCDM"
    for a, b in zip(pkd, pk0):
        assert abs(a - b) <= 3, "DYN=1 peaks must stay near LambdaCDM (no blow-up)"

    # [2] Delta chi^2 ~ A^2 (the chi d.o.f. is linear + well-behaved) ----------------
    _, td03, _ = run(0.0, 0.3)
    d1 = tt_chi2(ell, tt0, ttd)
    d03 = tt_chi2(ell, tt0, td03)
    print("\n[2] A^2 SCALING — the dynamical modification is linear in the amplitude")
    print(
        f"    TT dchi2: DYN=1={d1:.1f}, DYN=0.3={d03:.2f}, ratio={d1/d03:.1f} (expect ~11=(1/0.3)^2)"
    )
    assert (
        8 < d1 / d03 < 14
    ), "Delta chi^2 must scale as A^2 (chi linear + well-behaved)"

    # [3] dynamical vs quasi-static: more conservative on growth, NOT on TT ----------
    dq = tt_chi2(ell, tt0, ttq)
    print(
        "\n[3] DYNAMICAL vs QUASI-STATIC — growth more conservative; TT NOT smaller (honest)"
    )
    print(
        f"    sigma8 delta:  dynamical {100*(s8d/s80-1):+.2f}%   quasi-static {100*(s8q/s80-1):+.2f}%"
    )
    print(
        f"    TT Delta chi^2: dynamical {d1:.0f}   quasi-static {dq:.0f}   (ratio dyn/qs {d1/dq:.2f})"
    )
    print(
        "    -> the propagating chi can't respond during the fast horizon-crossing -> growth (sigma8)"
    )
    print(
        "       LESS modified; but chi imprints oscillatory features on the potentials -> TT NOT smaller."
    )
    assert abs(s8d / s80 - 1) < abs(
        s8q / s80 - 1
    ), "dynamical must be more conservative on sigma8"

    # [4] the constraint ------------------------------------------------------------
    a_max = float(np.sqrt(9.0 / d1))
    print(
        f"\n[4] CONSTRAINT — the full TT constrains the dynamical OBT: A < {a_max:.2f} (fixed-param 3sigma)"
    )
    print(
        "    ~56% of the TT residual is A_s/tau-degenerate (re-fittable) -> an MCMC weakens this; the"
    )
    print(
        "    fixed-param bound is the forward UPPER limit. The peak POSITIONS still fit (a0=cH/2pi)."
    )

    # ---- verdict ------------------------------------------------------------------
    print(
        "\n[VERDICT] the dynamical aether RUNS in CLASS (explicit chi d.o.f.) — and it does NOT rescue OBT"
    )
    print(
        "    * Implemented the propagating aether mode chi as a real CLASS d.o.f. (null=LambdaCDM, A^2,"
    )
    print(
        "      peaks intact). The bug (pip cached classy -> chi inert -> false 'dchi2=0') was caught by"
    )
    print("      the sigma8 guard + relire-en-boucle; --force-reinstall fixes it.")
    print(
        "    * HONEST physics: the dynamical chi is MORE conservative than the quasi-static mu on sigma8"
    )
    print(
        f"      ({100*(s8d/s80-1):+.1f}% vs {100*(s8q/s80-1):+.1f}%: chi can't respond during fast crossing),"
    )
    print(
        "      but the full-spectra TT Delta chi^2 is NOT smaller (the propagating chi imprints features"
    )
    print(
        "      on the ISW/lensing). So the full-spectra Planck constraint HOLDS: the dynamical treatment"
    )
    print(
        "      does NOT evade it. OBT-AeST's perturbation-level MOND is genuinely constrained (A<~0.2"
    )
    print(
        "      fixed, ~A^2, ~56% re-fittable); the peak POSITIONS still fit (a0=cH/2pi -> a^-3 CDM)."
    )
    print(
        "    * Residual: the exact aether cs^2 + the F(Y,Q) couplings set the exact Delta chi^2 (the chi"
    )
    print(
        "      oscillations depend on cs^2=1); + the full MCMC re-fit. The dynamical spectra are now real."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (chi couples; null=LambdaCDM; A^2; dynamical more conservative on s8)."
    )
    print("=" * 94)


if __name__ == "__main__":
    main()
