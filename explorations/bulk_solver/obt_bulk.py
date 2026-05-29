"""
AdS5-Schwarzschild background + moving brane + master potential + junction BC.

CONFIDENT pieces (standard, written out): f(r), tortoise r*(r), horizon r_h,
brane Friedmann trajectory.

FLAGGED pieces (MUST be verified against the literature before any run is
trusted): the Kodama-Ishibashi scalar master potential V_scalar, and the
perturbed Israel junction boundary condition coefficients. These carry sign
risk and are marked `VERIFY`.

References to copy exact forms from:
  - Kodama & Ishibashi, Prog.Theor.Phys. 110 (2003) 701, hep-th/0305147
    (scalar-type gravitational perturbation master eq + potential in AdS-Sch).
  - Mukohyama, Phys.Rev. D62 (2000) 084015, hep-th/0004067 (brane master var).
  - Koyama & Maartens; Cardoso, Hiramatsu, Koyama, Seahra 2007 (0705.1685).
"""
import numpy as np
from scipy.integrate import quad

# ----- units: set AdS radius ell = L = 1; restore physical scales at readout -----
ELL = 1.0


def f_bulk(r, mu):
    """AdS5-Schwarzschild metric function, flat 3-space (k=0).
    f(r) = r^2/ell^2 - mu/r^2.  mu = bulk BH mass = background dark radiation.
    Sign of mu is the background closure freedom (BBN-bounded, sign free)."""
    return r ** 2 / ELL ** 2 - mu / r ** 2


def horizon_radius(mu):
    """Bulk Cauchy horizon: f(r_h)=0 -> r_h = (mu * ell^2)^(1/4) for mu>0.
    For mu<=0 there is no horizon (pure-AdS Poincare case)."""
    if mu <= 0:
        return None
    return (mu * ELL ** 2) ** 0.25


def tortoise(r, mu, r_ref=None):
    """r*(r) = integral dr / f(r). Reference point r_ref (default: just outside
    the brane scale). Used to build the null coordinates u=t-r*, v=t+r*."""
    if r_ref is None:
        r_ref = 1.0
    val, _ = quad(lambda x: 1.0 / f_bulk(x, mu), r_ref, r, limit=200)
    return val


def friedmann_Hsq(a, rho, sigma, kappa5_sq, mu):
    """Brane Friedmann eq from the junction condition (flat, RS-tuned):
       H^2 = (kappa5^4/36)(sigma+rho)^2 - 1/ell^2 + mu/a^4.
    The cross term sigma*rho -> 8 pi G rho/3; rho^2 -> high-energy; mu/a^4 -> dark
    radiation. This is the standard moving-brane (Kraus-Ida) result."""
    return (kappa5_sq ** 2 / 36.0) * (sigma + rho) ** 2 - 1.0 / ELL ** 2 + mu / a ** 4


# ==========================================================================
# FLAGGED PHYSICS INPUT #1 — master potential. VERIFY before trusting.
# ==========================================================================
def V_scalar(r, k, mu, VERIFIED=False):
    """Kodama-Ishibashi scalar-type master potential for AdS5-Schwarzschild.

    STRUCTURE (schematic, D=5): V_S(r) = f(r) * [ k^2/r^2 + U_geom(r; mu) ],
    where U_geom collects the curvature/mass terms. The EXACT U_geom (including
    every coefficient and sign) must be copied from Kodama-Ishibashi 2003
    eq.(for the scalar-type potential, n=3 spatial dims). The placeholder below
    is a PLACEHOLDER ONLY and will be wrong in detail.

    Do not run physics with VERIFIED=False."""
    if not VERIFIED:
        raise NotImplementedError(
            "V_scalar: copy the exact Kodama-Ishibashi 2003 scalar potential "
            "(hep-th/0305147) before use. Placeholder is not trustworthy."
        )
    fr = f_bulk(r, mu)
    # --- PLACEHOLDER skeleton (REPLACE with verified KI expression) ---
    U_geom = 0.0  # VERIFY: KI curvature+mass terms here
    return fr * (k ** 2 / r ** 2 + U_geom)


# ==========================================================================
# FLAGGED PHYSICS INPUT #2 — perturbed junction (moving-brane) BC. VERIFY.
# ==========================================================================
def brane_junction_bc(tau, state, matter_pert, VERIFIED=False):
    """Perturbed Israel junction condition on the moving brane r=a(tau).

    Returns the boundary relation  A dOmega/dn + B Omega + C dOmega/dtau = Source,
    with A,B,C from the trajectory (a, adot, f(a)) and Source from the brane
    matter perturbations (delta_rho, theta; brane anisotropic stress = 0 for dust).
    EXACT coefficients: Mukohyama 2000 / Koyama-Maartens. VERIFY before use."""
    if not VERIFIED:
        raise NotImplementedError(
            "brane_junction_bc: copy exact coefficients from Mukohyama 2000 / "
            "Koyama-Maartens before use."
        )
    raise NotImplementedError("fill verified coefficients")


# ==========================================================================
# READOUT — the sign we are after (built once Omega is solved at the brane)
# ==========================================================================
def effective_G_modulation(Omega_brane, derivs, background):
    """From Omega and its derivatives at the brane, reconstruct the Bardeen
    potentials Phi, Psi and the effective Poisson coupling:
        -k^2 Phi / a^2 = 4 pi G_eff rho delta   ->   (G_eff/G_N - 1)
    Return its time-averaged sign over the growth window:
       > 0  enhancement, < 0  suppression.
    Implemented once V_scalar and the junction BC are verified (Gate 3)."""
    raise NotImplementedError("Gate 3: implement after Gates 0-2 pass.")
