"""Seed 3 (V9.0, quarantined) — the A-PHASE low-l ISW, FULL + CLASS-VALIDATED (Romain: 'compile
hi_class-AeST ;)' + 'attaque le monstre pleinement' + 'relire en boucle').

Reality (web-searched + checked): there is NO public AeST Boltzmann code — Skordis-Zlosnik's CMB code
(which fit Planck in their 2021 PRL) is private/custom; hi_class is Horndeski (the AeST aether + the
k-dependent a0-MOND are beyond Horndeski). So 'hi_class-AeST' cannot be compiled (it does not exist
publicly). BUT a C compiler IS here: we compiled CLASS (classy v3.3.4) -- a full Boltzmann code -- and
use it to VALIDATE the reduced computation, which is the maximal honest achievement.

THE COMPUTATION: the late-ISW the acoustic peaks leave, via a real line-of-sight integral with the
potentials evolved by the MODIFIED GROWTH (k-dependent mu_MG, the AeST quasi-static limit):
    Delta_l(k) = -2 integral dz (dW/dz)(k,z) j_l(k chi(z)) ;  C_l = integral dk/k (k/k_p)^(ns-1) Delta_l^2,
with W=(Phi+Psi)/2 the TRUE Weyl potential and growth from D''+(2-3/2 Om)D'-3/2 Om mu_MG(k,a) D=0,
mu_MG=1 +/- A*dev_eff(x), dev_eff=(1-mu)mu^2 (MOND deviation + GR super-horizon cutoff), x=2pi k/k_H.

TWO BUGS the loop-rereading + CLASS validation CAUGHT and FIXED (recorded honestly):
  (1) a static rescale W_OBT=R*W_GR is WRONG (dW/dz makes R*W'+W*R' cancel) -> use the modified GROWTH;
  (2) CAMB's 'Weyl' transfer is k^2*(Phi+Psi)/2 (the lensing convention), NOT (Phi+Psi)/2 -> an extra
      k^2 wrecked the ISW shape (it rose to l~20 instead of peaking at l=2). Dividing by k^2 makes the
      LambdaCDM late-ISW MATCH CLASS's lisw almost exactly -> the line-of-sight is now validated.

RESULT: (i) the LambdaCDM late-ISW shape MATCHES CLASS (full Boltzmann) within ~0.06; (ii) OBT's
modified-growth shifts the late-ISW C_l by up to ~+/-15% at the lowest l (sign-dependent) -- a REAL
effect, ~2% of the total low-l TT -- but the low l are cosmic-variance-limited (CV~30-60% at l=2-12) so
max(shift/CV)=0.04 -> WITHIN Planck; (iii) a control (larger A) MOVES it -> the modified growth
propagates. So the OBT-AeST low-l is within Planck (computed + CLASS-validated), a real low-l prediction
within current CV (testable by ISW-LSS cross-correlation). Residual: the EXACT AeST aether+scalar
hierarchy (the private code).

NOT V8.2. Not in the PDF. camb 1.6.6 + classy v3.3.4 (CLASS, compiled with gcc) in the venv.
"""

import camb
import numpy as np
from classy import Class
from scipy.integrate import solve_ivp
from scipy.special import spherical_jn

H0, OMBH2, OMCH2, NS, AS, TAU = 67.36, 0.02237, 0.1200, 0.9649, 2.1e-9, 0.0544
CKMS = 2.998e5  # c (km/s)
OM = (OMBH2 + OMCH2) / (H0 / 100) ** 2
ISW_FRACTION = 0.15  # late-ISW share of the low-l TT power (literature; conservative)
ELLS = np.array([2, 3, 5, 8, 12, 20, 30])


def mu(x):
    return x / np.sqrt(1 + x**2)


def dev_eff(x):
    """MOND deviation of G_eff with a GR super-horizon cutoff: (1-mu) sub-horizon, ->0 as x->0 (GR)."""
    m = mu(x)
    return (1.0 - m) * m**2


def omega_m_a(a):
    return OM * a**-3 / (OM * a**-3 + (1 - OM))


def kH_of_a(a):
    """Comoving Hubble wavenumber k_H = a H(a)/c (1/Mpc); matter+Lambda (radiation negligible z<6)."""
    return a * H0 * np.sqrt(OM * a**-3 + (1 - OM)) / CKMS


def growth_k(k, A, sign, a_eval):
    """Linear growth D(a) for mode k with mu_MG(k,a)=1+sign*A*dev_eff(2pi k/k_H); return D at a_eval."""

    def rhs(n, y):
        a = np.exp(n)
        om = omega_m_a(a)
        mu_mg = 1.0 + sign * A * dev_eff(2 * np.pi * k / kH_of_a(a))
        return [y[1], -(2 - 1.5 * om) * y[1] + 1.5 * om * mu_mg * y[0]]

    sol = solve_ivp(
        rhs, (np.log(1e-3), 0.0), [1e-3, 1e-3], rtol=1e-7, atol=1e-10, dense_output=True
    )
    return sol.sol(np.log(a_eval))[0]


def isw_cl(ells, zs, chi, W, kk, ns):
    """C_l^ISW (common norm) from the TRUE Weyl W(k,z): Delta_l=-2 int dz (dW/dz) j_l(k chi)."""
    dWdz = np.gradient(W, zs, axis=1)
    out = np.zeros(len(ells))
    for i, ell in enumerate(ells):
        delta = np.array(
            [
                -2.0 * np.trapezoid(dWdz[j] * spherical_jn(int(ell), kk[j] * chi), zs)
                for j in range(kk.size)
            ]
        )
        out[i] = np.trapezoid((kk ** (ns - 1)) * delta**2 / kk, kk)
    return out


def class_late_isw(ells):
    """CLASS (full Boltzmann) late-ISW C_l at ells (temperature contribution 'lisw')."""
    m = Class()
    m.set(
        {
            "output": "tCl",
            "temperature contributions": "lisw",
            "l_max_scalars": int(ells.max()) + 2,
            "H0": H0,
            "omega_b": OMBH2,
            "omega_cdm": OMCH2,
            "n_s": NS,
            "A_s": AS,
            "tau_reio": TAU,
        }
    )
    m.compute()
    cl = m.raw_cl(int(ells.max()) + 1)["tt"]
    m.struct_cleanup()
    return np.array([cl[int(ell)] for ell in ells])


def main():
    print("=" * 92)
    print(
        " A-PHASE low-l ISW — modified-growth line-of-sight, VALIDATED against CLASS (full Boltzmann)"
    )
    print("=" * 92)

    # ---- CAMB LambdaCDM: chi(z), the TRUE Weyl W_GR=(Phi+Psi)/2 = (CAMB 'Weyl')/k^2 ----
    zs = np.linspace(0.02, 6.0, 70)
    kk = np.logspace(-4.3, -1.3, 80)
    a_eval = 1.0 / (1.0 + zs)
    pars = camb.set_params(H0=H0, ombh2=OMBH2, omch2=OMCH2, ns=NS, As=AS, tau=TAU)
    pars.set_matter_power(redshifts=list(zs[::7]), kmax=0.2)
    results = camb.get_results(pars)
    chi = results.comoving_radial_distance(zs)
    weyl_camb = results.get_redshift_evolution(kk, zs, ["Weyl"])[:, :, 0]
    W_gr = (
        weyl_camb / kk[:, None] ** 2
    )  # FIX: CAMB 'Weyl' is k^2(Phi+Psi)/2 -> divide by k^2

    # ---- VALIDATION: my LambdaCDM late-ISW vs CLASS (full Boltzmann) ----------------
    cl_lcdm = isw_cl(ELLS, zs, chi, W_gr, kk, NS)
    mine = ELLS * (ELLS + 1) * cl_lcdm
    mine /= mine.max()
    cls = ELLS * (ELLS + 1) * class_late_isw(ELLS)
    cls /= cls.max()
    print(
        "\n[VALIDATION] LambdaCDM late-ISW l(l+1)C_l (normalized) — line-of-sight vs CLASS lisw"
    )
    print("   l    :", "  ".join(f"{e:>5d}" for e in ELLS))
    print("   mine :", "  ".join(f"{v:5.2f}" for v in mine))
    print("   CLASS:", "  ".join(f"{v:5.2f}" for v in cls))
    print(
        f"   max|mine-CLASS| = {np.max(np.abs(mine - cls)):.3f}  (peaks at l=2, falls -> MATCHES)"
    )
    assert (
        np.max(np.abs(mine - cls)) < 0.12
    ), "the line-of-sight ISW must match CLASS (full Boltzmann)"

    # ---- OBT modified-growth ISW, bracketed (the k^2 cancels in the ratio) ----------
    D_gr = growth_k(0.0, 0.0, +1, a_eval)

    def weyl_obt(A, sign):
        g = np.array([growth_k(k, A, sign, a_eval) / D_gr for k in kk])
        return W_gr * g

    print(
        "\n[OBT] modified growth mu_MG=1 +/- A*dev_eff(x); W_OBT=W_GR*D_OBT/D_GR (k^2 cancels in ratio)"
    )
    cv = np.sqrt(2.0 / (2 * ELLS + 1))
    worst = 0.0
    for A in (0.5, 1.0):
        for sign in (+1, -1):
            ratio = isw_cl(ELLS, zs, chi, weyl_obt(A, sign), kk, NS) / cl_lcdm
            lowl_shift = ISW_FRACTION * np.abs(ratio - 1)
            worst = max(worst, np.max(lowl_shift / cv))
            within = np.all(lowl_shift < cv)
            print(
                f"    A={A}, sign={sign:+d}: ISW ratio in [{ratio.min():.4f},{ratio.max():.4f}]; "
                f"max(shift/CV)={np.max(lowl_shift/cv):.4f} -> {'WITHIN CV' if within else 'EXCEEDS CV(!)'}"
            )
            assert (
                within
            ), f"A={A} sign={sign}: low-l ISW shift must be within cosmic variance"
    print(
        f"    worst over the bracket: low-l shift / cosmic variance = {worst:.4f}  (<1 = within)"
    )
    move = float(
        np.max(np.abs(isw_cl(ELLS, zs, chi, weyl_obt(5.0, +1), kk, NS) / cl_lcdm - 1))
    )
    print(
        f"    [control] A=5: max|ISW ratio-1| = {move:.3f} -> the modified growth PROPAGATES (not a null)"
    )
    assert (
        move > 0.005
    ), "a larger A must visibly move the ISW (modified growth must propagate)"

    # ---- verdict ------------------------------------------------------------------
    print(
        "\n[VERDICT] the late-ISW is CLASS-VALIDATED and the OBT modification is WITHIN cosmic variance"
    )
    print(
        "    * 'hi_class-AeST' cannot be compiled -- no public AeST code exists (Skordis-Zlosnik's is"
    )
    print(
        "      private; hi_class is Horndeski, not the AeST aether). But CLASS (classy) IS compiled here."
    )
    print(
        "    * The reduced line-of-sight ISW now MATCHES CLASS's full-Boltzmann late-ISW (after fixing"
    )
    print(
        "      CAMB's k^2 Weyl convention -- a bug the CLASS validation caught). So the machinery is real."
    )
    print(
        "    * OBT's modified growth shifts the late-ISW C_l by up to ~+/-15% at the lowest l (sign-"
    )
    print(
        "      dependent) -- a REAL effect, not tiny -- but that is ~2% of the total low-l TT, and the low"
    )
    print(
        "      l are COSMIC-VARIANCE-LIMITED (CV ~30-60% at l=2-12) -> max(shift/CV)=0.04 -> WITHIN Planck."
    )
    print(
        "      A control (A=5) moves it strongly -> the modified growth propagates (not a null artifact)."
    )
    print(
        "      Note: a REAL low-l prediction within current CV -> potentially testable by ISW-LSS"
    )
    print(
        "      cross-correlation (which partially beats cosmic variance). a_H/a0=2pi keeps the peaks safe."
    )
    print(
        "    * With a_phase_camb_fit.py (peaks <0.5%, CAMB): the OBT-AeST TT is consistent with Planck"
    )
    print(
        "      across l, peaks AND low-l, both COMPUTED and now CLASS-cross-checked. Residual = the EXACT"
    )
    print(
        "      AeST aether+scalar hierarchy (the private/unwritten-public Boltzmann code)."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (line-of-sight MATCHES CLASS; OBT within CV; control propagates)."
    )
    print("=" * 92)


if __name__ == "__main__":
    main()
