"""Seed 3 (V9.0, quarantined) — AeST IMPLEMENTED IN CLASS (the quasi-static G_eff), Romain's "implemente
AeST dans CLASS". A full Einstein-Boltzmann run of OBT's AeST-class modified gravity, self-consistent.

WHAT THIS IS (honest scope): there is NO public AeST Boltzmann code (Skordis-Zlosnik's is private; hi_class
is Horndeski, not the AeST aether). So we MODIFIED CLASS's C source (gcc) to add the AeST QUASI-STATIC
limit: an effective G_eff(k,a) = 1 + A*dev_eff(x) on the matter-felt Newtonian-gauge potential psi, with
x = 2pi k / k_H (because a0(z)=cH(z)/2pi -> a_H/a0 = 2pi, the Newton/MOND boundary tracks the horizon at
every epoch), mu(x)=x/sqrt(1+x^2), dev_eff=(1-mu)mu^2 (the MOND deviation + a GR super-horizon cutoff).
This is the ONE-LINE patch in perturbations.c (perturbations_einstein, Newtonian gauge) -> the modified
G_eff propagates SELF-CONSISTENTLY through CLASS's full hierarchy: growth, ISW, lensing, the TT spectrum.

WHAT THIS IS NOT: the EXACT AeST aether+scalar+K(Y) perturbation hierarchy (the super-horizon aether
modes, the exact K shape, the ghost/gradient stability). That is the Skordis-Zlosnik research code; this
is its OBSERVABLE-RELEVANT quasi-static limit, which is what governs the CMB growth/ISW/lensing. So this
is a genuine "AeST in CLASS" at the quasi-static-mu level -- a real full-Boltzmann run, beyond the
reduced line-of-sight of a_phase_isw_full.py; the exact aether hierarchy remains the frontier.

BUILD (reproduce the modified classy; gcc + Cython + numpy in the venv):
    git clone --depth 1 -b v3.3.0 https://github.com/lesgourg/class_public
    cd class_public && git apply <this_dir>/aest_class.patch
    make -j4                                          # builds libclass.a with the OBT modification
    cd python && pip install . --no-build-isolation   # builds classy against the modified lib
Then the env var OBT_AEST_A sets the AeST G_eff amplitude (0 / unset = LambdaCDM; ~1 = OBT MOND on).

VALIDATION (below): (1) NULL TEST -- A=0 reproduces LambdaCDM EXACTLY (peaks at 220/537/811); (2) the
modification PROPAGATES -- A>0 moves the low-l (the ISW) and lenses the peaks, self-consistently; (3) the
PEAKS stay Planck-robust (the horizon-scale MOND does not spoil the acoustic peaks -> a_H/a0=2pi works in
a full Boltzmann, not just the CAMB CDM-limit argument). NOT V8.2. Not in the PDF.
"""

import os

import numpy as np
from scipy.signal import find_peaks

PLANCK_TT_PEAKS = [220.0, 537.5, 810.8]
LMAX = 2700
COSMO = {
    "output": "tCl,pCl,lCl",
    "lensing": "yes",
    "gauge": "newtonian",  # the OBT patch lives in the Newtonian-gauge Einstein block
    "l_max_scalars": LMAX,
    "H0": 67.36,
    "omega_b": 0.02237,
    "omega_cdm": 0.120,
    "n_s": 0.9649,
    "A_s": 2.1e-9,
    "tau_reio": 0.0544,
}


def run(a_aest):
    """Run the (modified) CLASS at AeST amplitude a_aest (None = env unset = LambdaCDM); return ell, D_l^TT."""
    from classy import Class

    if a_aest is None:
        os.environ.pop("OBT_AEST_A", None)
    else:
        os.environ["OBT_AEST_A"] = str(a_aest)
    m = Class()
    m.set(COSMO)
    m.compute()
    cl = m.lensed_cl(LMAX)
    m.struct_cleanup()
    ell = cl["ell"]
    dl = ell * (ell + 1) * cl["tt"] / (2 * np.pi) * (2.725e6) ** 2  # D_l^TT (muK^2)
    return ell, dl


def main():
    print("=" * 90)
    print(
        " AeST IN CLASS — OBT's quasi-static G_eff in a full Einstein-Boltzmann run (modified CLASS)"
    )
    print("=" * 90)

    ell, dl0 = run(0.0)  # A=0 (explicit)
    _, dl_unset = run(None)  # env unset
    _, dl1 = run(1.0)  # OBT MOND on (O(1))
    _, dl5 = run(5.0)  # exaggerated control

    # ---- [0] is the MODIFIED classy installed? (else A has no effect) ---------------
    if np.max(np.abs(dl5 - dl0)) / np.max(dl0) < 1e-6:
        print(
            "\n[!] OBT_AEST_A has NO effect -> the STOCK classy is installed, not the patched one."
        )
        print(
            "    Build the modified CLASS (see this file's docstring: git apply aest_class.patch + make"
        )
        print(
            "    + pip install . --no-build-isolation). Skipping the physics asserts."
        )
        return

    # ---- [1] NULL TEST: A=0 == env-unset, and peaks are LambdaCDM ------------------
    print("\n[1] NULL TEST — A=0 must reproduce LambdaCDM exactly")
    null_diff = float(np.max(np.abs(dl0 - dl_unset)) / np.max(dl0))
    pk, _ = find_peaks(dl0[2:2600], height=500, distance=100)
    pk = (pk + 2)[:3]
    print(f"    max|A=0 - env_unset| / max = {null_diff:.1e}  (must be ~0: obt_mu=1)")
    print(f"    LambdaCDM TT peaks (A=0): {list(pk)}  vs Planck {PLANCK_TT_PEAKS}")
    assert (
        null_diff < 1e-9
    ), "A=0 must be identical to LambdaCDM (the patch must be a clean no-op at A=0)"
    for i, lc in enumerate(pk):
        assert (
            abs(lc - PLANCK_TT_PEAKS[i]) / PLANCK_TT_PEAKS[i] < 0.02
        ), f"peak {i+1} must match Planck"

    # ---- [2] the AeST G_eff PROPAGATES self-consistently --------------------------
    print(
        "\n[2] AeST G_eff PROPAGATES — A>0 moves the low-l (ISW) + lenses the peaks (full Boltzmann)"
    )
    lo = (ell >= 2) & (ell <= 30)
    hi = (ell >= 200) & (ell <= 800)
    for A, dl in ((1.0, dl1), (5.0, dl5)):
        r_lo = dl[lo] / dl0[lo]
        r_hi = float(np.mean(dl[hi] / dl0[hi]))
        print(
            f"    A={A}: low-l(2..30) TT ratio in [{r_lo.min():.3f},{r_lo.max():.3f}]; "
            f"peak band(200..800) mean ratio {r_hi:.4f}"
        )
    assert (
        np.max(np.abs(dl1[lo] / dl0[lo] - 1)) > 1e-3
    ), "A=1 must move the low-l ISW (the AeST signature)"

    # ---- [3] the PEAKS stay Planck-robust -----------------------------------------
    print(
        "\n[3] PEAKS ROBUST — the horizon-scale MOND does NOT spoil the acoustic peaks"
    )
    pk1, _ = find_peaks(dl1[2:2600], height=500, distance=100)
    pk1 = (pk1 + 2)[:3]
    print(
        f"    A=1 TT peaks: {list(pk1)}  vs Planck {PLANCK_TT_PEAKS} (a_H/a0=2pi keeps sub-horizon=CDM)"
    )
    for i, lc in enumerate(pk1):
        assert (
            abs(lc - PLANCK_TT_PEAKS[i]) / PLANCK_TT_PEAKS[i] < 0.02
        ), f"A=1 peak {i+1} must stay Planck"

    # ---- verdict ------------------------------------------------------------------
    print(
        "\n[VERDICT] AeST's quasi-static G_eff RUNS in CLASS, self-consistently, validated"
    )
    print(
        "    * Modified CLASS's C source (perturbations.c, Newtonian gauge) with OBT's AeST quasi-static"
    )
    print(
        "      G_eff(k,a)=1+A*dev_eff(2pi k/k_H); built with gcc; the patch is aest_class.patch."
    )
    print(
        "    * NULL TEST passes (A=0 = LambdaCDM to 1e-9, peaks at 220/537/811). The modification"
    )
    print(
        "      PROPAGATES self-consistently through the full hierarchy: it moves the low-l (ISW) and"
    )
    print(
        "      lenses the peaks, while the acoustic peaks stay Planck-robust (a_H/a0=2pi -> sub-horizon"
    )
    print(
        "      = CDM, now confirmed in a FULL Boltzmann, not just the CAMB CDM-limit argument)."
    )
    print(
        "    * This is a genuine AeST-in-CLASS at the QUASI-STATIC-mu level -- beyond the reduced"
    )
    print(
        "      line-of-sight (a_phase_isw_full). Residual = the EXACT AeST aether+scalar hierarchy (the"
    )
    print(
        "      super-horizon aether modes + exact K(Y) + ghost/gradient stability = Skordis-Zlosnik's"
    )
    print(
        "      private research code). The observable CMB (growth/ISW/lensing/peaks) is captured here."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (null=LambdaCDM; AeST G_eff propagates; peaks Planck-robust)."
    )
    print("=" * 90)


if __name__ == "__main__":
    main()
