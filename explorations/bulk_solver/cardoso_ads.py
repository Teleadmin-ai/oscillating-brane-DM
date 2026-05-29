"""
Verified AdS5 (Poincare, mu=0) reduced master potential + Gate 0.5 validation.

Source equation (Cardoso, Hiramatsu, Koyama & Seahra 2007, arXiv:0705.1685,
Eq. 18), Poincare coords (tau, z), AdS5, bulk master variable Omega:

    -Omega_{,tau tau} + Omega_{,zz} + (3/z) Omega_{,z} + (1/z^2 - k^2) Omega = 0

The +1 coefficient of Omega/z^2 was confirmed verbatim against the paper (two
independent extractions; explicitly NOT 3, 15/4, or -3).

Remove the first-derivative term with  Omega = z^{-3/2} psi  (2*alpha+3=0):

    psi_{,tau tau} - psi_{,zz} = (1/(4 z^2) - k^2) psi
  <=>  4 psi_{,uv} + V psi = 0,   u = tau - z, v = tau + z,  z = (v-u)/2,
       V(u,v) = k^2 - 1/(4 z^2) = k^2 - 1/(v-u)^2 .

Exact separable solution (used as the Gate 0.5 oracle):
    psi(tau,z) = cos(omega tau) * sqrt(z) * J_0(q z),   q = sqrt(omega^2 - k^2),
since sqrt(z) J_0(qz) satisfies  chi'' + (q^2 + 1/(4 z^2)) chi = 0  exactly.

Gate 0.5 PASSES iff the (Gate-0-validated) double-null marcher reproduces this
analytic mode at 2nd order. This validates the POTENTIAL implementation, with no
moving brane yet (that is Gate 1).
"""
import numpy as np
from scipy.special import j0

import double_null as dn


def V_psi(U, V, k):
    """Reduced AdS5 potential for 4 psi_{,uv} + V psi = 0, with z=(V-U)/2 so that
    1/(4 z^2) = 1/(V-U)^2. Valid where V>U (z>0); keep the domain off z=0."""
    return k ** 2 - 1.0 / (V - U) ** 2


def analytic_mode(tau, z, k, omega):
    """Exact separable solution psi = cos(omega tau) sqrt(z) J_0(q z), q=sqrt(omega^2-k^2).
    Requires omega>k so q is real (oscillatory mode)."""
    q = np.sqrt(omega ** 2 - k ** 2)
    return np.cos(omega * tau) * np.sqrt(z) * j0(q * z)


def gate05(k=1.0, omega=3.0):
    """Evolve from analytic initial data on the two null segments and compare to
    the analytic mode in the interior. Domain: square [u0,u0+H]x[v0,v0+H] with
    v0-u0=2, H=1  ->  z=(v-u)/2 in [0.5,1.5] (bounded away from the z=0 boundary).
    Returns (max_errors, convergence_order)."""
    u0, v0, H = 0.0, 2.0, 1.0

    def dataA(u):                      # on v = v0 (varying u)
        return analytic_mode((u + v0) / 2.0, (v0 - u) / 2.0, k, omega)

    def dataB(v):                      # on u = u0 (varying v)
        return analytic_mode((u0 + v) / 2.0, (v - u0) / 2.0, k, omega)

    def probe(n):
        h = H / (n - 1)
        u, v, Om = dn.solve_square(u0, v0, h, n,
                                   lambda U, V: V_psi(U, V, k), dataA, dataB)
        UU, VV = np.meshgrid(u, v, indexing="ij")
        exact = analytic_mode((UU + VV) / 2.0, (VV - UU) / 2.0, k, omega)
        return np.max(np.abs(Om - exact))

    e1, e2, e3 = probe(129), probe(257), probe(513)
    order = (np.log2(e1 / e2) + np.log2(e2 / e3)) / 2.0
    return (e1, e2, e3), order
