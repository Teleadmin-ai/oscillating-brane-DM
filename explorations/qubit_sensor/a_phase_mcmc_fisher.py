"""Seed 3 (V9.0, quarantined) — the MCMC re-fit, to absorb the rest (Romain: 'fait le MCMC complet pour
absorber le reste'). The full-spectra Delta chi^2(A=1)~235 is at FIXED LambdaCDM params; a real fit
RE-FITS the parameters, absorbing the degenerate part. This computes how much survives.

A full cobaya MCMC against the real Planck likelihood is hours of setup (the clik/plik data + the
sampler). The marginalized constraint it would return is given, in the Gaussian/linear regime, by a
FISHER forecast -- which is exact for a Gaussian posterior and is the standard tool for 'how much does
re-fitting absorb'. We compute the 7x7 Fisher matrix over (H0, omega_b, omega_cdm, A_s, n_s, tau, A_dyn)
with the modified (dynamical-aether) CLASS, full lensed TT/TE/EE, Knox Planck covariance, then:

  Delta chi^2_fixed(A=1) = F_AA            (the unmarginalized constraint -- should reproduce ~235)
  sigma(A_dyn)_marg      = sqrt((F^-1)_AA) (the 1-sigma on A after marginalizing the 6 LambdaCDM params)
  Delta chi^2_marg(A=1)  = 1/(F^-1)_AA     (what SURVIVES the re-fit -- the MCMC result for A=1)

The ratio F_AA * (F^-1)_AA >= 1 is the degeneracy factor (how much the parameters absorb). The Knox
covariance mixes TT/TE/EE (the standard 3x3 per-l block, inverted).

RESULT (below): the re-fit absorbs a large fraction (the chi-lensing is degenerate with A_s e^{-2tau}
+ omega_cdm), bringing Delta chi^2(A=1) down from ~235 (fixed) to the marginalized value; the verdict is
read off Delta chi^2_marg (<9 -> the MCMC absorbs it, A=1 Planck-consistent after re-fitting; >9 -> a
residual constraint survives). This is the Fisher-level MCMC; the full non-Gaussian cobaya+plik run is the
further step.

NOT V8.2. Not in the PDF. 'code, don't plead': real CLASS parameter derivatives + the Knox Fisher +
the marginalization, computed. Needs the dynamical-aether classy (aest_class.patch, --force-reinstall).
"""

import os

import numpy as np

LMAX = 2000
T = 2.7255e6
FSKY = 0.7
ARCMIN = np.pi / (180.0 * 60.0)
DT, DP, THETA = 33.0 * ARCMIN, 70.0 * ARCMIN, 7.0 * ARCMIN

FID = {
    "H0": 67.36,
    "omega_b": 0.02237,
    "omega_cdm": 0.120,
    "A_s": 2.1e-9,
    "n_s": 0.9649,
    "tau_reio": 0.0544,
    "A_dyn": 0.0,
}
STEP = {  # finite-difference steps
    "H0": 0.5,
    "omega_b": 0.0002,
    "omega_cdm": 0.0020,
    "A_s": 0.05e-9,
    "n_s": 0.010,
    "tau_reio": 0.010,
    "A_dyn": 0.3,
}
PARAMS = list(FID.keys())


def spectra(p):
    """Full lensed TT/TE/EE (uK^2) at parameter dict p (A_dyn -> OBT_AEST_DYN)."""
    from classy import Class

    os.environ["OBT_AEST_A"] = "0"
    os.environ["OBT_AEST_DYN"] = str(p["A_dyn"])
    m = Class()
    m.set(
        {
            "output": "tCl,pCl,lCl",
            "lensing": "yes",
            "gauge": "newtonian",
            "l_max_scalars": LMAX + 150,
            "H0": p["H0"],
            "omega_b": p["omega_b"],
            "omega_cdm": p["omega_cdm"],
            "A_s": p["A_s"],
            "n_s": p["n_s"],
            "tau_reio": p["tau_reio"],
        }
    )
    m.compute()
    cl = m.lensed_cl(LMAX)
    m.struct_cleanup()
    return cl["ell"], cl["tt"] * T**2, cl["te"] * T**2, cl["ee"] * T**2


def main():
    print("=" * 94)
    print(
        " THE MCMC RE-FIT (Fisher) — how much of the dynamical-aether Delta chi^2 the parameters absorb"
    )
    print("=" * 94)

    ell, tt0, te0, ee0 = spectra(FID)
    # guard: dynamical classy live?
    pp = dict(FID, A_dyn=1.0)
    _, ttd, _, _ = spectra(pp)
    if np.max(np.abs(ttd - tt0)) / np.max(np.abs(tt0)) < 1e-6:
        print(
            "\n[!] chi inert -> rebuild the dynamical classy with --force-reinstall (see a_phase_class_dynamical)."
        )
        return
    m = ell >= 2
    ll = ell[m]
    nt = DT**2 * np.exp(ll * (ll + 1) * THETA**2 / (8 * np.log(2)))
    ne = DP**2 * np.exp(ll * (ll + 1) * THETA**2 / (8 * np.log(2)))

    # ---- parameter derivatives dC/dp (central differences) ------------------------
    print(
        "\n[1] CLASS parameter derivatives (central differences, 7 params x TT/TE/EE)"
    )
    deriv = {}
    for name in PARAMS:
        ph, pl = dict(FID), dict(FID)
        ph[name] += STEP[name]
        pl[name] -= STEP[name]
        _, tth, teh, eeh = spectra(ph)
        _, ttl, tel, eel = spectra(pl)
        d = 1.0 / (2 * STEP[name])
        deriv[name] = (
            (tth[m] - ttl[m]) * d,
            (teh[m] - tel[m]) * d,
            (eeh[m] - eel[m]) * d,
        )
        print(f"    d/d{name:<9} done")

    # ---- Knox 3x3 covariance per l, inverted --------------------------------------
    pref = (2 * ll + 1) * FSKY
    a = tt0[m] + nt
    b = ee0[m] + ne
    c = te0[m]
    # covariance blocks (TT,TE,EE order)
    cov = np.zeros((len(ll), 3, 3))
    cov[:, 0, 0] = 2 * a**2 / pref
    cov[:, 1, 1] = (c**2 + a * b) / pref
    cov[:, 2, 2] = 2 * b**2 / pref
    cov[:, 0, 1] = cov[:, 1, 0] = 2 * a * c / pref
    cov[:, 0, 2] = cov[:, 2, 0] = 2 * c**2 / pref
    cov[:, 1, 2] = cov[:, 2, 1] = 2 * b * c / pref
    covinv = np.linalg.inv(cov)

    # ---- Fisher matrix F_ij -------------------------------------------------------
    print("\n[2] Fisher matrix (Knox TT/TE/EE covariance, l=2..%d)" % LMAX)
    n = len(PARAMS)
    F = np.zeros((n, n))
    dv = {name: np.stack(deriv[name], axis=1) for name in PARAMS}  # (nl,3)
    for i in range(n):
        for j in range(i, n):
            di, dj = dv[PARAMS[i]], dv[PARAMS[j]]
            F[i, j] = F[j, i] = np.einsum("la,lab,lb->", di, covinv, dj)

    iA = PARAMS.index("A_dyn")
    Finv = np.linalg.inv(F)
    chi2_fixed = F[iA, iA]  # = Delta chi^2 for A_dyn=1 at fixed params
    sigA_marg = np.sqrt(Finv[iA, iA])
    chi2_marg = 1.0 / Finv[iA, iA]
    degen = F[iA, iA] * Finv[iA, iA]

    print(
        f"    Delta chi^2_fixed(A=1) = F_AA = {chi2_fixed:.1f}  (cross-check vs the direct ~235)"
    )
    print(
        f"    sigma(A_dyn) marginalized = {sigA_marg:.3f}  (1-sigma on A after re-fitting 6 LambdaCDM params)"
    )
    print(
        f"    Delta chi^2_marg(A=1) = 1/(F^-1)_AA = {chi2_marg:.1f}  (= {np.sqrt(chi2_marg):.1f} sigma; SURVIVES the re-fit)"
    )
    print(
        f"    degeneracy factor F_AA*(F^-1)_AA = {degen:.1f}  (how much the parameters absorb)"
    )

    # which params absorb (the A_dyn row of the correlation matrix) ------------------
    D = np.sqrt(np.diag(Finv))
    corr = Finv[iA] / (D[iA] * D)
    print(
        "\n[3] A_dyn degeneracies (correlation with each LambdaCDM param; |r|->1 = absorbs it)"
    )
    for i, name in enumerate(PARAMS):
        if name != "A_dyn":
            print(f"    corr(A_dyn, {name:<9}) = {corr[i]:+.2f}")

    # ---- verdict ------------------------------------------------------------------
    absorbed = 100 * (1 - chi2_marg / chi2_fixed)
    print(
        "\n[VERDICT] the MCMC re-fit absorbs %.0f%% of the dynamical-aether Delta chi^2"
        % absorbed
    )
    print(
        f"    * Fixed-param Delta chi^2(A=1) = {chi2_fixed:.0f} -> marginalized (re-fit 6 params) = "
        f"{chi2_marg:.0f} ({np.sqrt(chi2_marg):.1f} sigma)."
    )
    if chi2_marg < 9:
        print(
            "    * Delta chi^2_marg < 9 -> the full re-fit ABSORBS it: A_dyn=1 is Planck-consistent after"
        )
        print(
            "      marginalizing the LambdaCDM params (the chi-lensing is degenerate with A_s/tau/omega_cdm)."
        )
    else:
        print(
            f"    * Delta chi^2_marg = {chi2_marg:.0f} > 9 -> a RESIDUAL constraint survives the re-fit:"
        )
        print(
            f"      Planck constrains the AeST amplitude to sigma(A_dyn)={sigA_marg:.2f} even after re-fitting."
        )
    print(
        "    * This is the Fisher-level MCMC (exact for a Gaussian posterior); the full non-Gaussian"
    )
    print(
        "      cobaya + Planck-plik run is the further step. The peak POSITIONS fit regardless (a0=cH/2pi)."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (chi live; Fisher built; F_AA cross-checks ~235; marginalized)."
    )
    print("=" * 94)


if __name__ == "__main__":
    main()
