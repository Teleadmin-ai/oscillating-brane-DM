"""
Double-null characteristic marcher for the bulk master equation

    4 d^2 Omega / du dv  +  V(u,v) Omega = 0      i.e.   Omega_{,uv} = -(1/4) V Omega

Scheme: Gundlach, Price & Pullin, Phys. Rev. D 49, 883 (1994).
For a square cell with corners S=(i,j), E=(i+1,j), W=(i,j+1), N=(i+1,j+1):

    Omega_N = Omega_E + Omega_W - Omega_S - (h^2/8) V_C (Omega_E + Omega_W)

  derived from  integral_cell Omega_{,uv} = Omega_N - Omega_E - Omega_W + Omega_S
  and           integral_cell -(1/4) V Omega ~ -(1/4) V_C * (Omega_E+Omega_W)/2 * h^2.

For V == 0 the update is exactly the d'Alembert relation Omega = A(u)+B(v), so the
free-field test below must hold to machine precision. The convergence test verifies
2nd-order accuracy (error ∝ h^2) for nonzero V. THIS FILE IS THE VALIDATED CORE
(Gate 0). No OBT physics here.

NOTE: numba is optional. If absent, the pure-numpy fallback works (slower). Nothing
in this file is executed on import; call the functions from run_validation.py.
"""
import numpy as np

try:
    from numba import njit
    _HAVE_NUMBA = True
except Exception:  # numba not installed yet — pure-python fallback
    _HAVE_NUMBA = False

    def njit(*args, **kwargs):
        # Support both @njit and @njit(cache=True). If called as a bare
        # decorator, args == (func,); otherwise return a no-op decorator.
        if len(args) == 1 and callable(args[0]) and not kwargs:
            return args[0]

        def deco(func):
            return func

        return deco


@njit(cache=True)
def _march(Omega, Vgrid, h):
    """In-place double-null march on a square initial-characteristic-value grid.

    Omega[i, j] : i indexes u (rows), j indexes v (cols). Row i=0 and column j=0
    must be pre-filled with the initial data on the two null segments. Vgrid[i,j]
    is the potential at node (i,j); the cell-center value is the 4-node average.
    """
    nu, nv = Omega.shape
    for i in range(nu - 1):
        for j in range(nv - 1):
            S = Omega[i, j]
            E = Omega[i + 1, j]
            W = Omega[i, j + 1]
            Vc = 0.25 * (Vgrid[i, j] + Vgrid[i + 1, j] + Vgrid[i, j + 1] + Vgrid[i + 1, j + 1])
            Omega[i + 1, j + 1] = E + W - S - (h * h / 8.0) * Vc * (E + W)
    return Omega


def solve_square(u0, v0, h, n, V_func, dataA, dataB):
    """Solve on [u0,u0+(n-1)h] x [v0,v0+(n-1)h] with initial data on the two null
    boundaries. V_func(u,v) -> potential. dataA(u) sets Omega on v=v0; dataB(v) sets
    Omega on u=u0. Consistency at the corner: dataA(u0) must equal dataB(v0).
    Returns (u, v, Omega)."""
    u = u0 + h * np.arange(n)
    v = v0 + h * np.arange(n)
    UU, VV = np.meshgrid(u, v, indexing="ij")
    # broadcast handles V_func returning a scalar or a full array, force C-contig float64
    Vgrid = np.ascontiguousarray(
        np.broadcast_to(np.asarray(V_func(UU, VV), dtype=np.float64), UU.shape)
    )
    a_vals = np.asarray(dataA(u), dtype=np.float64)   # on v = v0 boundary
    b_vals = np.asarray(dataB(v), dtype=np.float64)   # on u = u0 boundary
    if not np.isclose(a_vals[0], b_vals[0]):          # corner must be single-valued
        raise ValueError("inconsistent initial data at the corner (u0,v0)")
    Omega = np.zeros((n, n), dtype=np.float64)
    Omega[:, 0] = a_vals
    Omega[0, :] = b_vals
    _march(Omega, Vgrid, h)
    return u, v, Omega


# --------------------------------------------------------------------------
# Gate 0 self-tests (no physics). Call from run_validation.py --gate 0
# --------------------------------------------------------------------------
def gate0_free_field(n=257):
    """V=0: solution must be exactly A(u)+B(v) to machine precision."""
    A = lambda u: np.exp(-((u - 1.5) ** 2))          # noqa: E731
    B = lambda v: 0.7 * np.sin(v)                      # noqa: E731
    h = 3.0 / (n - 1)
    u, v, Om = solve_square(0.0, 0.0, h, n, lambda U, V: np.zeros_like(U),
                            dataA=lambda uu: A(uu) + B(0.0),
                            dataB=lambda vv: A(0.0) + B(vv))
    UU, VV = np.meshgrid(u, v, indexing="ij")
    exact = A(UU) + B(VV)
    err = np.max(np.abs(Om - exact))
    return err  # expect ~1e-13 or better


def gate0_convergence(Vconst=2.0):
    """Constant V: self-convergence (Richardson) must approach 2nd order.
    Returns measured order p (expect ~2)."""
    A = lambda u: np.exp(-((u - 1.0) ** 2) * 4)        # noqa: E731
    B = lambda v: np.exp(-((v - 1.0) ** 2) * 4)        # noqa: E731

    def probe(n):
        h = 2.0 / (n - 1)
        u, v, Om = solve_square(0.0, 0.0, h, n, lambda U, V: Vconst * np.ones_like(U),
                                dataA=lambda uu: A(uu) + B(0.0),
                                dataB=lambda vv: A(0.0) + B(vv))
        return Om[-1, -1]  # value at the far corner

    n1, n2, n3 = 129, 257, 513
    p1, p2, p3 = probe(n1), probe(n2), probe(n3)
    # Richardson order estimate from three halvings
    num, den = (p1 - p2), (p2 - p3)
    if abs(den) < 1e-15 or abs(num) < 1e-15:
        return float("nan")  # degenerate (already at round-off floor)
    return np.log2(abs(num / den))  # expect ~2.0
