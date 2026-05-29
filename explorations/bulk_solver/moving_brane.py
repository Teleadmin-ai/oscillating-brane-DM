"""
Gate 1b-i: validate Seahra's moving-brane triangular-cell update (Eq. 35) by the
method of manufactured solutions (MMS), BEFORE running a full evolution.

Triangular (brane) cell: S=(u_S,v_S) brane, E=(u_S,v_N) bulk, N=(u_N,v_N) brane.
S->E along u=u_S (outgoing into bulk), E->N along v=v_N (ingoing to brane).
Seahra Eq. 35 (with potential V):
    psi_N = -[12 + 6 a_S d_eta + du dv V_S]/[12 + 6 a_N d_eta + du dv V_N] psi_S
            + [24 - du dv V_E]/[12 + 6 a_N d_eta + du dv V_N] psi_E
Robin: (n.D)psi - alpha psi = 0;  a_{S,N}=alpha at brane nodes;  d_eta = proper
distance along brane S->N (trapezoid, 2nd order); du=u_N-u_S, dv=v_N-v_S.

MMS: choose an EXACT solution psi of 4 psi_uv + V psi = 0 and a trajectory z_b(t);
DEFINE alpha := (n.D)psi/psi at the brane nodes; feed into Eq. 35 with exact S,E
values; check it recovers psi(N). Per-step error must vanish as O(dt^3).

  Stage A: flat (V=0), psi=F(u)+G(v).
  Stage B: AdS,  V=k^2-1/(4z^2)=k^2-1/(v-u)^2,  psi=cos(w t)sqrt(z)J0(q z) (the
           Gate-0.5 validated mode), q=sqrt(w^2-k^2), z=(v-u)/2, t=(u+v)/2.
Normal derivative used (hypothesis): FLAT Minkowski (t,z) normal, since the
reduced-variable wave equation is in flat (u,v) operators.
    (n.D)psi = [zdot psi_t + psi_z]/sqrt(1-zdot^2).
"""

import numpy as np
from scipy.special import j0, j1


def eq35_update(tS, dt, psi_uv, dn_psi_t, Vfunc, zb, zbdot):
    """One Eq.35 brane-node update; returns (predicted psi_N, exact psi_N)."""
    tN = tS + dt
    zS, zN = zb(tS), zb(tN)
    uS, vS = tS - zS, tS + zS
    uN, vN = tN - zN, tN + zN
    uE, vE = uS, vN  # bulk node
    psiS, psiE = psi_uv(uS, vS), psi_uv(uE, vE)
    aS = dn_psi_t(tS) / psi_uv(uS, vS)
    aN = dn_psi_t(tN) / psi_uv(uN, vN)
    deta = 0.5 * (np.sqrt(1 - zbdot(tS) ** 2) + np.sqrt(1 - zbdot(tN) ** 2)) * dt
    du, dv = uN - uS, vN - vS
    Vs, Vn, Ve = Vfunc(uS, vS), Vfunc(uN, vN), Vfunc(uE, vE)
    den = 12.0 + 6.0 * aN * deta + du * dv * Vn
    psiN = (
        -(12.0 + 6.0 * aS * deta + du * dv * Vs) / den * psiS
        + (24.0 - du * dv * Ve) / den * psiE
    )
    return psiN, psi_uv(uN, vN)


def convergence(label, psi_uv, dn_psi_t, Vfunc, zb, zbdot, tS=0.5):
    print(f"\n=== {label} ===")
    print(f"{'dt':>10s}{'|err|':>14s}{'ratio':>8s}{'order':>8s}")
    prev = None
    for dt in [0.1, 0.05, 0.025, 0.0125, 0.00625]:
        pN, pex = eq35_update(tS, dt, psi_uv, dn_psi_t, Vfunc, zb, zbdot)
        err = abs(pN - pex)
        if prev is None:
            print(f"{dt:10.5f}{err:14.3e}{'-':>8s}{'-':>8s}")
        else:
            print(f"{dt:10.5f}{err:14.3e}{prev / err:8.2f}{np.log2(prev / err):8.2f}")
        prev = err


# ---- shared trajectory: timelike brane z_b(t)=z0+A sin(Om t), |zdot|<1 ----
z0, A, Om = 1.0, 0.10, 0.9
zb = lambda t: z0 + A * np.sin(Om * t)  # noqa: E731
zbdot = lambda t: A * Om * np.cos(Om * t)  # noqa: E731

# ---- Stage A: flat, psi = F(u)+G(v) ----
kF, kG = 1.3, 0.7
F = lambda u: np.sin(kF * u)  # noqa: E731
G = lambda v: np.cos(kG * v)  # noqa: E731
Fp = lambda u: kF * np.cos(kF * u)  # noqa: E731
Gp = lambda v: -kG * np.sin(kG * v)  # noqa: E731
psiA = lambda u, v: F(u) + G(v)  # noqa: E731


def dnA(t):
    u, v = t - zb(t), t + zb(t)
    zd = zbdot(t)
    psi_t = Fp(u) + Gp(v)
    psi_z = -Fp(u) + Gp(v)
    return (zd * psi_t + psi_z) / np.sqrt(1 - zd**2)


VA = lambda u, v: 0.0  # noqa: E731

# ---- Stage B: AdS, psi = cos(w t) sqrt(z) J0(q z), V = k^2 - 1/(v-u)^2 ----
wB, kB = 3.0, 1.0
qB = np.sqrt(wB**2 - kB**2)


def psiB(u, v):
    t, z = 0.5 * (u + v), 0.5 * (v - u)
    return np.cos(wB * t) * np.sqrt(z) * j0(qB * z)


def dnB(t):
    z = zb(t)
    u, v = t - z, t + z
    zd = zbdot(t)
    psi_t = -wB * np.sin(wB * t) * np.sqrt(z) * j0(qB * z)
    psi_z = np.cos(wB * t) * (
        j0(qB * z) / (2 * np.sqrt(z)) - qB * np.sqrt(z) * j1(qB * z)
    )
    return (zd * psi_t + psi_z) / np.sqrt(1 - zd**2)


VB = lambda u, v: kB**2 - 1.0 / (v - u) ** 2  # = k^2 - 1/(4 z^2)   # noqa: E731


if __name__ == "__main__":
    print("Gate 1b-i: MMS unit tests of Seahra Eq. 35 (per-step error -> O(dt^3))")
    convergence("Stage A (flat, V=0)", psiA, dnA, VA, zb, zbdot)
    convergence("Stage B (AdS, V=k^2-1/4z^2, flat normal)", psiB, dnB, VB, zb, zbdot)


# ==========================================================================
# Stage C1: FULL evolution with a STATIC brane (z_b = z0 const), MMS validation.
# Brane aligns with the grid diagonal (v0-u0 = 2 z0 -> brane nodes at j=i).
# Domain: wedge j >= i. Initial data on the i=0 null line; Robin BC on the brane
# (Eq.35); diamond updates in the bulk. Validate against the Gate-0.5 Bessel mode.
# ==========================================================================
def _psi_exact(u, v, w, q):
    t, z = 0.5 * (u + v), 0.5 * (v - u)
    return np.cos(w * t) * np.sqrt(z) * j0(q * z)


def run_static(N, T=1.0, w=3.0, k=1.0, z0=1.0):
    q = np.sqrt(w**2 - k**2)
    h = T / N
    u = 0.0 + h * np.arange(N + 1)
    v = 2.0 * z0 + h * np.arange(N + 1)  # v0-u0 = 2 z0 -> brane at j=i
    psi = np.full((N + 1, N + 1), np.nan)
    for j in range(N + 1):  # initial data on i=0 null line
        psi[0, j] = _psi_exact(u[0], v[j], w, q)

    def Vf(uu, vv):
        return k**2 - 1.0 / (vv - uu) ** 2

    def alpha_brane(t):  # static: zdot=0 -> (n.D)=psi_z
        z = z0
        psi_z = np.cos(w * t) * (
            j0(q * z) / (2 * np.sqrt(z)) - q * np.sqrt(z) * j1(q * z)
        )
        return psi_z / (np.cos(w * t) * np.sqrt(z) * j0(q * z))

    for i in range(1, N + 1):
        # brane node (i,i) via Eq.35: S=(i-1,i-1), E=(i-1,i)
        tS = 0.5 * (u[i - 1] + v[i - 1])
        tN = 0.5 * (u[i] + v[i])
        aS, aN = alpha_brane(tS), alpha_brane(tN)
        deta = h  # proper dist along static brane
        du = dv = h
        Vs, Vn, Ve = Vf(u[i - 1], v[i - 1]), Vf(u[i], v[i]), Vf(u[i - 1], v[i])
        den = 12.0 + 6.0 * aN * deta + du * dv * Vn
        psi[i, i] = (
            -(12.0 + 6.0 * aS * deta + du * dv * Vs) / den * psi[i - 1, i - 1]
            + (24.0 - du * dv * Ve) / den * psi[i - 1, i]
        )
        # bulk nodes (i,j), j>i, via diamond: node=E+W-S-(h^2/8)Vc(E+W)
        for j in range(i + 1, N + 1):
            E, W, S = psi[i, j - 1], psi[i - 1, j], psi[i - 1, j - 1]
            Vc = 0.25 * (
                Vf(u[i - 1], v[j - 1])
                + Vf(u[i], v[j - 1])
                + Vf(u[i - 1], v[j])
                + Vf(u[i], v[j])
            )
            psi[i, j] = E + W - S - (h * h / 8.0) * Vc * (E + W)

    # L-inf error over all computed nodes (j>=i)
    err = 0.0
    for i in range(N + 1):
        for j in range(i, N + 1):
            err = max(err, abs(psi[i, j] - _psi_exact(u[i], v[j], w, q)))
    return err


if __name__ == "__main__":
    import sys

    if "--stageC" in sys.argv:
        print(
            "Stage C1: full evolution, STATIC brane, vs Bessel oracle (expect order ~2)"
        )
        print(f"{'N':>6s}{'Linf err':>14s}{'order':>8s}")
        prev = None
        for N in [50, 100, 200, 400]:
            e = run_static(N)
            if prev is None:
                print(f"{N:6d}{e:14.3e}{'-':>8s}")
            else:
                print(f"{N:6d}{e:14.3e}{np.log2(prev / e):8.2f}")
            prev = e
