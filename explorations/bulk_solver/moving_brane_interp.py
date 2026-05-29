"""
Stage C2c: the PROPER moving-brane solver (no shortcut) for a GENERAL,
ACCELERATING trajectory z_b(t) -- which is what the real OBT radion is.

Method (Seahra-style): rays launched from the brane points B_i=(u_i^b, v_i^b) at
brane times t_i=t0+i*dt. Each ray i stores psi at v = v_i^b + m*delta (m=0 = the
brane node). To advance ray i -> ray i+1, ray i's data is sampled at the
v-positions ray i+1 needs via CUBIC 4-point interpolation (the off-grid transfer).
Brane node via Seahra Eq.35 (validated); bulk nodes via the GPP diamond.

Bricks, each validated:
  1. cubic_interp  -> O(h^4) on a known function.
  2. run_accel     -> MMS vs the Bessel oracle on an ACCELERATING brane -> order 2.
"""

import numpy as np
from scipy.special import j0, j1


# ---- Brick 1: 4-point Lagrange cubic interpolation ----
def cubic_interp(xt, xs, ys):
    out = 0.0
    for i in range(4):
        term = ys[i]
        for j in range(4):
            if j != i:
                term *= (xt - xs[j]) / (xs[i] - xs[j])
        out += term
    return out


def interp_ray(vt, vray, psiray):
    """Cubic-interpolate a ray (uniform ascending v) at v=vt; clamp the 4-stencil."""
    n = len(vray)
    dv = vray[1] - vray[0]
    k0 = int(np.floor((vt - vray[0]) / dv)) - 1
    k0 = max(0, min(k0, n - 4))
    return cubic_interp(vt, vray[k0 : k0 + 4], psiray[k0 : k0 + 4])


def test_interp():
    f = lambda x: np.cos(2.3 * x) * np.exp(0.1 * x)  # noqa: E731
    print("Brick 1: cubic interpolation order (expect ~4)")
    prev = None
    for n in [20, 40, 80, 160]:
        xs = np.linspace(0.0, 3.0, n)
        ys = f(xs)
        xt = np.linspace(0.2, 2.8, 97)  # interior targets
        err = max(abs(interp_ray(x, xs, ys) - f(x)) for x in xt)
        o = "-" if prev is None else f"{np.log2(prev / err):.2f}"
        print(f"  n={n:4d}  err={err:.3e}  order={o}")
        prev = err


# ---- Brick 2: accelerating-brane evolution (ray grid + interpolation) ----
def _psi(u, v, w, q):
    t, z = 0.5 * (u + v), 0.5 * (v - u)
    return np.cos(w * t) * np.sqrt(z) * j0(q * z)


def run_accel(N, A=0.1, Om=0.9, T=0.5, w=3.0, k=1.0, z0=1.0, t0=1.0, R=1.5):
    q = np.sqrt(w**2 - k**2)
    zb = lambda t: z0 + A * np.sin(Om * t)  # noqa: E731  (ACCELERATING)
    zbd = lambda t: A * Om * np.cos(Om * t)  # noqa: E731
    dt = T / N
    tb = t0 + dt * np.arange(N + 1)
    ub, vb = tb - zb(tb), tb + zb(tb)
    delta = dt
    vmax = vb[0] + R

    def Vf(uu, vv):
        return k**2 - 1.0 / (vv - uu) ** 2

    def alpha(t):
        z = zb(t)
        pt = -w * np.sin(w * t) * np.sqrt(z) * j0(q * z)
        pz = np.cos(w * t) * (j0(q * z) / (2 * np.sqrt(z)) - q * np.sqrt(z) * j1(q * z))
        pv = np.cos(w * t) * np.sqrt(z) * j0(q * z)
        return (zbd(t) * pt + pz) / np.sqrt(1.0 - zbd(t) ** 2) / pv

    # ray 0 = initial data
    vray = [vb[0] + delta * np.arange(int((vmax - vb[0]) / delta) + 1)]
    psir = [_psi(ub[0], vray[0], w, q)]
    err = 0.0
    for i in range(N):
        vr_new = vb[i + 1] + delta * np.arange(int((vmax - vb[i + 1]) / delta) + 1)
        ps_new = np.empty_like(vr_new)
        # brane node (m=0) via Eq.35
        du, dv = ub[i + 1] - ub[i], vb[i + 1] - vb[i]
        deta = (
            0.5 * (np.sqrt(1 - zbd(tb[i]) ** 2) + np.sqrt(1 - zbd(tb[i + 1]) ** 2)) * dt
        )
        aS, aN = alpha(tb[i]), alpha(tb[i + 1])
        Vs, Vn, Ve = Vf(ub[i], vb[i]), Vf(ub[i + 1], vb[i + 1]), Vf(ub[i], vb[i + 1])
        psiS = psir[i][0]
        psiE = interp_ray(vb[i + 1], vray[i], psir[i])  # ray i at v=vb[i+1]
        den = 12.0 + 6.0 * aN * deta + du * dv * Vn
        ps_new[0] = (
            -(12.0 + 6.0 * aS * deta + du * dv * Vs) / den * psiS
            + (24.0 - du * dv * Ve) / den * psiE
        )
        # bulk nodes via diamond (A=ray_i(v_low), B=ray_i(v_high), C=prev on new ray)
        for m in range(1, len(vr_new)):
            v_low, v_high = vr_new[m - 1], vr_new[m]
            Ac = interp_ray(v_low, vray[i], psir[i])
            Bc = interp_ray(v_high, vray[i], psir[i])
            Cc = ps_new[m - 1]
            Vc = 0.25 * (
                Vf(ub[i], v_low)
                + Vf(ub[i], v_high)
                + Vf(ub[i + 1], v_low)
                + Vf(ub[i + 1], v_high)
            )
            ps_new[m] = Bc + Cc - Ac - (du * delta / 8.0) * Vc * (Bc + Cc)
        vray.append(vr_new)
        psir.append(ps_new)
        err = max(err, np.max(np.abs(ps_new - _psi(ub[i + 1], vr_new, w, q))))
    return err


if __name__ == "__main__":
    test_interp()
    print("\nBrick 2: ACCELERATING-brane evolution (ray grid + interp), MMS vs Bessel")
    print(f"{'N':>6s}{'Linf err':>14s}{'order':>8s}")
    prev = None
    for N in [40, 80, 160, 320]:
        e = run_accel(N)
        o = "-" if prev is None else f"{np.log2(prev / e):.2f}"
        print(f"{N:6d}{e:14.3e}{o:>8s}")
        prev = e
