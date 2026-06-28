"""Seed 3 (V9.0, quarantined) — the A-PHASE residual, FULL: the late-ISW by a real line-of-sight
integral with the AeST-MODIFIED-GROWTH potentials (Romain: 'attaque le monstre pleinement, pas de
simplification' + 'relire en boucle').

The full AeST Einstein-Boltzmann module (the aether+scalar hierarchy in hi_class) is a research code;
no Fortran compiler here. So we do the next-fullest thing for the residual the acoustic peaks leave
(the LATE ISW): a GENUINE line-of-sight ISW with the potentials evolved by the MODIFIED GROWTH.

  A FIRST, WRONG attempt (recorded honestly): rescale the Weyl potential statically, W_OBT = R(k,z) W_GR.
  That FAILS -- the ISW source is dW/dz, and d(R W)/dz = R W' + W R' partially cancels, so even A=20
  does not move the ISW (a null artifact, not physics). The right physics is the modified EVOLUTION.

  THE RIGHT WAY: solve the k-dependent linear growth  D'' + (2 - 3/2 Om) D' - 3/2 Om mu_MG(k,a) D = 0
  (N=ln a) with OBT's mu_MG(k,a) = 1 +/- A*dev_eff(x), x = 2pi k / k_H(a) (a0=cH/2pi -> a_H/a0=2pi),
  dev_eff(x)=(1-mu(x))mu(x)^2 (the MOND deviation of G_eff, with a GR super-horizon cutoff: ->0 as x->0,
  ~(1-mu) sub-horizon), mu(x)=x/sqrt(1+x^2). The growth ratio g(k,z)=D_OBT/D_GR multiplies CAMB's real
  Weyl transfer: W_OBT(k,z) = W_GR(k,z) g(k,z). Then the real line-of-sight ISW:

      Delta_l(k) = -2 integral dz (dW/dz)(k,z) j_l(k chi(z)) ;  C_l = integral dk/k (k/k_p)^(ns-1) Delta_l^2.

  We BRACKET sign and amplitude A; a machinery CONTROL (a larger A) must move the ISW (the modified
  growth DOES propagate -- unlike the wrong static rescaling).

RESULT (below): at the CMB-OBSERVABLE l>=2 the dominant scales are sub-horizon (x>=20, Newtonian,
g~1), so the late-ISW shift is << cosmic variance for both signs and amplitudes. The modification is
REAL and large only at super-horizon (x<2pi) scales, which are j_l-suppressed for l>=2 -> the CMB does
not probe them. So OBT's late-time MOND does NOT spoil the low-l: computed via the modified growth.

NOT V8.2. Not in the PDF. 'code, don't plead': modified-growth ODE + real line-of-sight (CAMB Weyl +
Bessel), LambdaCDM-shape sanity-checked, a machinery control that MOVES, the result within CV. camb 1.6.6.
"""

import camb
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import spherical_jn

H0, OMBH2, OMCH2, NS, AS, TAU = 67.36, 0.02237, 0.1200, 0.9649, 2.1e-9, 0.0544
CKMS = 2.998e5  # c (km/s)
OM = (OMBH2 + OMCH2) / (H0 / 100) ** 2  # matter density ~0.31
ISW_FRACTION = 0.15  # late-ISW share of the low-l TT power (literature; conservative)
ELLS = np.array([2, 3, 5, 8, 12, 20, 30])


def mu(x):
    return x / np.sqrt(1 + x**2)


def dev_eff(x):
    """MOND deviation of G_eff with a GR super-horizon cutoff: (1-mu) sub-horizon, ->0 as x->0 (GR)."""
    m = mu(x)
    return (
        1.0 - m
    ) * m**2  # bounded (peak ~0.15 at x~1); ->0 super-horizon; ~(1-mu) sub-horizon


def omega_m_a(a):
    return OM * a**-3 / (OM * a**-3 + (1 - OM))


def kH_of_a(a):
    """Comoving Hubble wavenumber k_H = a H(a)/c (1/Mpc); matter+Lambda (radiation negligible z<6)."""
    h = H0 * np.sqrt(OM * a**-3 + (1 - OM))
    return a * h / CKMS


def growth_k(k, A, sign, a_eval):
    """Linear growth D(a) for mode k with mu_MG(k,a)=1+sign*A*(1-mu(2pi k/k_H)); return D at a_eval."""

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
    """C_l^ISW (common norm) from W(k,z): Delta_l=-2 int dz (dW/dz) j_l(k chi); C_l=int dk/k k^(ns-1) Delta^2."""
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


def main():
    print("=" * 92)
    print(
        " A-PHASE residual FULL — late-ISW via the MODIFIED GROWTH + a real line-of-sight integral"
    )
    print("=" * 92)

    # ---- CAMB LambdaCDM: chi(z), the Weyl transfer W_GR(k,z) -----------------------
    zs = np.linspace(0.02, 6.0, 70)
    kk = np.logspace(-4.3, -1.3, 80)  # 1/Mpc
    a_eval = 1.0 / (1.0 + zs)
    pars = camb.set_params(H0=H0, ombh2=OMBH2, omch2=OMCH2, ns=NS, As=AS, tau=TAU)
    pars.set_matter_power(redshifts=list(zs[::7]), kmax=0.2)
    results = camb.get_results(pars)
    chi = results.comoving_radial_distance(zs)
    W_gr = results.get_redshift_evolution(kk, zs, ["Weyl"])[:, :, 0]  # (nk, nz)

    # ---- modified growth: g(k,z) = D_OBT/D_GR (the RIGHT physics) ------------------
    D_gr = growth_k(0.0, 0.0, +1, a_eval)  # LambdaCDM growth (mu_MG=1, k-independent)

    def weyl_obt(A, sign):
        g = np.array([growth_k(k, A, sign, a_eval) / D_gr for k in kk])  # (nk, nz)
        return W_gr * g

    # ---- sanity: LambdaCDM late-ISW rises to low l --------------------------------
    cl_lcdm = isw_cl(ELLS, zs, chi, W_gr, kk, NS)
    Dl = ELLS * (ELLS + 1) * cl_lcdm
    print(
        "\n[sanity] LambdaCDM late-ISW l(l+1)C_l (normalized; should be smooth, low-l weighted)"
    )
    print("   l   :", "  ".join(f"{e:>6d}" for e in ELLS))
    print("   D_l :", "  ".join(f"{v:6.2f}" for v in Dl / Dl.max()))
    assert (
        cl_lcdm[0] > cl_lcdm[-1] > 0
    ), "the late-ISW C_l must rise to low l (the ISW signature)"

    # ---- OBT modified-growth ISW, bracketed ---------------------------------------
    print(
        "\n[OBT] mu_MG=1 +/- A*dev_eff(x), dev_eff=(1-mu)mu^2 (GR cutoff); W_OBT=W_GR*D_OBT/D_GR (mod. growth)"
    )
    x_obs = 2 * np.pi * (2.0 / chi[np.argmin(abs(zs - 1.0))]) / kH_of_a(0.5)
    print(
        f"      observable late-ISW (l>=2) probes x ~ {x_obs:.0f} (Newtonian, dev_eff={dev_eff(x_obs):.4f}); the"
    )
    print(
        "      modification peaks ~0.15 at x~1 (MOND onset, k~k_H/2pi -> l<1), j_l-suppressed for l>=2."
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
                f"    A={A}, sign={sign:+d}: ISW ratio l=2..30 in [{ratio.min():.4f},{ratio.max():.4f}]; "
                f"max(shift/CV)={np.max(lowl_shift/cv):.4f} -> {'WITHIN CV' if within else 'EXCEEDS CV(!)'}"
            )
            assert (
                within
            ), f"A={A} sign={sign}: low-l ISW shift must be within cosmic variance"
    print(
        f"    worst over the bracket: low-l shift / cosmic variance = {worst:.4f}  (<1 = within)"
    )

    # ---- machinery control: a larger A MUST move the ISW (modified growth propagates) -
    move = float(
        np.max(np.abs(isw_cl(ELLS, zs, chi, weyl_obt(5.0, +1), kk, NS) / cl_lcdm - 1))
    )
    print(
        f"    [control] A=5: max|ISW ratio-1| = {move:.3f} -> the modified growth PROPAGATES (not a null)"
    )
    assert (
        move > 0.005
    ), "a larger A must visibly move the ISW (the modified growth must propagate)"

    # ---- verdict ------------------------------------------------------------------
    print(
        "\n[VERDICT] the late-ISW residual is WITHIN cosmic variance (modified growth, line-of-sight)"
    )
    print(
        "    * Real modified-growth ODE (k-dependent mu_MG) -> g(k,z) -> W_OBT=W_GR*g -> a real"
    )
    print(
        "      line-of-sight ISW (CAMB Weyl + Bessel). The control (a larger A=5) MOVES the ISW, so the"
    )
    print(
        "      machinery propagates (the earlier static-rescaling null was an artifact, now fixed)."
    )
    print(
        "    * At CMB-OBSERVABLE l>=2 the dominant scales are sub-horizon (x>=20, Newtonian, g~1):"
    )
    print(
        "      the low-l shift is << cosmic variance for both signs and amplitudes. The big modification"
    )
    print(
        "      is super-horizon (x<2pi), j_l-suppressed for l>=2 -> the CMB does not probe it."
    )
    print(
        "    * WHY: a0(z)=cH(z)/2pi -> a_H/a0=2pi keeps the Newton/MOND transition AT the horizon, so"
    )
    print(
        "      the whole observable CMB (peaks AND low-l) sits in the Newtonian regime -> ~LambdaCDM."
    )
    print(
        "    * With a_phase_camb_fit.py (peaks <0.5%): the OBT-AeST TT is consistent with Planck across"
    )
    print(
        "      l. Honest residual: the EXACT AeST mu-Sigma + polarization + lensing need the hi_class-"
    )
    print(
        "      AeST module; here the growth + line-of-sight are real, the mu-Sigma input is bracketed."
    )

    print(
        "\n  ALL INJECTION TESTS PASSED (LambdaCDM ISW sane; control PROPAGATES; OBT low-l within CV)."
    )
    print("=" * 92)


if __name__ == "__main__":
    main()
