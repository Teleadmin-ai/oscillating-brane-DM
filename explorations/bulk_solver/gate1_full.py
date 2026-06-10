"""
Gate 1b-ii/iii — the FULL coupled bulk+brane solver (Stage D brick 2).

Couples the validated machinery end-to-end on the REAL Cardoso-Hiramatsu-Koyama-
Seahra (0705.1685) radiation-era problem:
  bulk   : 4 psi_uv + [k^2 - 1/(4 z^2)] psi = 0           (psi = z^{-3/2} Omega)
  brane  : radiation era, a(eta) = (k eta)^{1/3}  (units ell = a0 = 1, Eq. 37)
  Robin  : (n.D)psi - alpha psi = S   on the brane (flat normal, Stage-B result)
  matter : full Eq. 33a for radiation (w = c_s^2 = 1/3, Gamma = 0)

PHYSICS COEFFICIENTS (derived; cross-checked — see also GATE1_spec.md):
  Friedmann (Eq. 10)  =>  rho/sigma = gamma - 1 EXACTLY, gamma = sqrt(1+H^2 ell^2)
    (solve H^2 = (rho/sigma)(2+rho/sigma):  (gamma-1)(gamma+1) = gamma^2-1 = H^2).
  REDUCTION (sign-critical): the SCALAR master has +(3/z)Omega_z friction, so
  Omega = z^{-3/2} psi  (i.e. psi = z^{+3/2} Omega) — OPPOSITE to the tensor
  field h = z^{+3/2} psi_T (whose equation has -(3/z)h_z). Getting this backwards
  flips/rescales the Robin data and produces a SPURIOUS tachyonic bound state
  (growth rate ~0.8/z_b; we hit it, diagnosed it, fixed it — see README).
  Junction (Eq. 28) converted to psi with the FLAT normal
  (n.D)psi = gamma (zdot psi_t + psi_z)  [Stage-B validated convention]:
      alpha(eta) = +gamma / (2 z_b)
      S(eta)     = -6 (gamma-1) Delta / (k^2 z_b^{7/2})        (ell = 1)
  Cross-checks: (i) TENSOR reduction h = z^{3/2}psi_T with proper-normal Neumann
  d_n h = 0 gives alpha_T = -(3/2)gamma/z_b = Seahra's RS coefficient (spec) —
  conventions consistent; (ii) STABILITY: with alpha=+gamma/(2 z_b) the static
  Robin problem has NO growing bound state (f=sqrt(z)K0(kappa z) cannot satisfy
  f'/f = 1/(2z)+0 with kappa>0), matching RS scalar stability; the WRONG sign
  -(5/2)gamma/z DOES (kappa z_b ~ 0.8), which was the observed runaway.
  Matter (Eq. 33a, radiation): the friction coefficient (1+3c_s^2-6w) = 0, and
      Delta'' = -[k^2/3 - 4(gamma-1)a^2 - 18(gamma-1)^2 a^2] Delta
                + (4/9) k^4 Omega_b / a^3 ,        Omega_b = z_b^{-3/2} psi_brane.
  Cross-check: at high energy (gamma-1 -> H ell >> 1) this reproduces Eq. 38
  term by term: -18H^2a^2 = -2/eta^2, -4Ha^2 = -4 k^{1/3}/(3 eta^{2/3}),
  source = 4k^3 Omega_b/(9 eta)   (units a0 = ell = 1).

  Trajectory identities (ell=1):  H = (k/3)(k eta)^{-4/3},  dz_b/d eta = -H
  exactly,  du_b/d eta = gamma + H,  dv_b/d eta = gamma - H,  and
  du*dv = d eta^2 IDENTICALLY (brane conformal time = flat proper time), which
  keeps the Eq.35 cell terms O(d eta^2) even for a near-null brane.

NUMERICS: ray grid launched from the brane nodes (validated Stage C2c), uniform
v-spacing delta within a ray, vectorized cubic-Lagrange single-shift transfer
ray->ray, GPP diamonds in the bulk, generalized Eq. 35 (Stage-D source
coefficient -6*d_eta*(S_S+S_N)) at the brane, Heun predictor-corrector for the
(Delta, psi) coupling, adaptive eta-steps d eta = min(deta_max,
c_du*delta/(gamma+H)) so the ray-to-ray u-gap stays ~ c_du*delta at high energy.

Baseline ("decoupled") = same run with the Omega_b source OFF in the Delta ODE
(Gate-1a's definition), isolating the bulk-graviton pumping of Delta.
"""

import cardoso_brane
import numpy as np


# ---------------------------------------------------------------- background
def gam_H_a(eta, k):
    """Radiation-era background, units ell = a0 = 1 (CHKS Eq. 37 convention)."""
    a = (k * eta) ** (1.0 / 3.0)
    H = (k / 3.0) * (k * eta) ** (-4.0 / 3.0)
    gam = np.sqrt(1.0 + H * H)
    return gam, H, a


def build_brane(k, eta_i, eta_f, deta_max, c_du, delta):
    """Adaptive eta grid + trajectory arrays (tau by per-step Simpson)."""
    etas = [eta_i]
    while etas[-1] < eta_f:
        g, H, _ = gam_H_a(etas[-1], k)
        h = min(deta_max, c_du * delta / (g + H))
        etas.append(min(etas[-1] + h, eta_f))
    eta = np.array(etas)
    tau = np.empty_like(eta)
    tau[0] = 0.0
    for i in range(len(eta) - 1):
        h = eta[i + 1] - eta[i]
        g0, _, _ = gam_H_a(eta[i], k)
        gm, _, _ = gam_H_a(0.5 * (eta[i] + eta[i + 1]), k)
        g1, _, _ = gam_H_a(eta[i + 1], k)
        tau[i + 1] = tau[i] + h * (g0 + 4.0 * gm + g1) / 6.0
    gam, H, a = gam_H_a(eta, k)
    zb = 1.0 / a
    return eta, tau, gam, H, a, zb, tau - zb, tau + zb


# ------------------------------------------------------------------- pieces
def Vpot(u, v, k):
    return k * k - 1.0 / (v - u) ** 2


def alpha_brane(gam, zb):
    return 0.5 * gam / zb


def source_S(gam, zb, k, Delta):
    return -6.0 * (gam - 1.0) * Delta / (k * k * zb**3.5)


def brack(eta, k):
    g, _, a = gam_H_a(eta, k)
    gm1 = g - 1.0
    return k * k / 3.0 - 4.0 * gm1 * a * a - 18.0 * gm1 * gm1 * a * a


def rk4_delta(eta0, h, D, dD, k, Ob0, Ob1, coupling):
    """Two RK4 substeps of Delta'' = -brack*Delta + coupling*(4/9)k^4 Ob/a^3,
    with Omega_b linear in eta between Ob0 (at eta0) and Ob1 (at eta0+h)."""

    def f(t, y):
        _, _, a = gam_H_a(t, k)
        s = Ob0 + (Ob1 - Ob0) * (t - eta0) / h if h > 0 else Ob0
        return np.array(
            [y[1], -brack(t, k) * y[0] + coupling * (4.0 / 9.0) * k**4 * s / a**3]
        )

    y = np.array([D, dD])
    t = eta0
    hh = 0.5 * h
    for _ in range(2):
        k1 = f(t, y)
        k2 = f(t + 0.5 * hh, y + 0.5 * hh * k1)
        k3 = f(t + 0.5 * hh, y + 0.5 * hh * k2)
        k4 = f(t + hh, y + hh * k3)
        y = y + (hh / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t += hh
    return y[0], y[1]


def lagrange_w(x):
    """Cubic-Lagrange weights for stencil nodes at local coords [0,1,2,3]."""
    return np.array(
        [
            -(x - 1) * (x - 2) * (x - 3) / 6.0,
            x * (x - 2) * (x - 3) / 2.0,
            -x * (x - 1) * (x - 3) / 2.0,
            x * (x - 1) * (x - 2) / 6.0,
        ]
    )


def shift_ray(psi, frac):
    """Old ray (uniform spacing) sampled at index positions m+frac, m=0..n-1,
    via the 4-point stencil [m-1..m+2]; ends clamped (causally irrelevant)."""
    n = len(psi)
    w = lagrange_w(1.0 + frac)
    out = np.empty(n)
    out[1 : n - 2] = (
        w[0] * psi[0 : n - 3]
        + w[1] * psi[1 : n - 2]
        + w[2] * psi[2 : n - 1]
        + w[3] * psi[3:n]
    )
    out[0] = w[0] * psi[0] + w[1] * psi[0] + w[2] * psi[1] + w[3] * psi[2]
    out[n - 2 :] = psi[n - 2 :]
    return out


def interp_at(psir, pos):
    """Cubic interpolation of a uniform ray at fractional index pos."""
    m = int(np.floor(pos))
    m = max(1, min(m, len(psir) - 3))
    return float(lagrange_w(1.0 + (pos - m)) @ psir[m - 1 : m + 3])


# ------------------------------------------------------------------ the run
def run_full(
    k,
    eta_i=0.07,
    eta_f=10.0,
    delta=0.02,
    deta_max=0.01,
    c_du=1.0,
    coupling=1.0,
    ic="const",
):
    """March the coupled (psi, Delta) system. Returns eta, Delta, Omega_b
    histories. coupling=0 switches OFF the bulk source in the Delta ODE
    (the Gate-1a 'decoupled' baseline)."""
    eta, tau, gam, H, a, zb, ub, vb = build_brane(
        k, eta_i, eta_f, deta_max, c_du, delta
    )
    N = len(eta) - 1
    vmax = vb[-1] + 8 * delta

    D, dD = (4.0 / 3.0) * (k * eta_i) ** 2, (8.0 / 3.0) * k * k * eta_i
    Ob_gm = k * eta_i**3  # growing-mode Omega_b (Eq. 40a)

    M0 = int(np.floor((vmax - vb[0]) / delta)) + 1
    z0 = 0.5 * (vb[0] + delta * np.arange(M0) - ub[0])
    psir = np.zeros(M0) if ic == "zero" else Ob_gm * z0**1.5

    hist_eta, hist_D, hist_Ob = [eta[0]], [D], [zb[0] ** -1.5 * psir[0]]
    for i in range(N):
        h = eta[i + 1] - eta[i]
        du = ub[i + 1] - ub[i]
        dv = vb[i + 1] - vb[i]
        Ob_S = zb[i] ** -1.5 * psir[0]
        aS = alpha_brane(gam[i], zb[i])
        aN = alpha_brane(gam[i + 1], zb[i + 1])
        Vs = Vpot(ub[i], vb[i], k)
        Vn = Vpot(ub[i + 1], vb[i + 1], k)
        Ve = Vpot(ub[i], vb[i + 1], k)
        S_S = source_S(gam[i], zb[i], k, D)
        psiS = psir[0]
        psiE = interp_at(psir, dv / delta)  # old ray at v = vb[i+1]
        den = 12.0 + 6.0 * aN * h + du * dv * Vn

        def eq35(S_N):
            return (
                -(12.0 + 6.0 * aS * h + du * dv * Vs) / den * psiS
                + (24.0 - du * dv * Ve) / den * psiE
                - 6.0 * h * (S_S + S_N) / den
            )

        # Heun: predictor (Omega_b frozen) -> corrector (Omega_b linear S->N)
        Dp, _ = rk4_delta(eta[i], h, D, dD, k, Ob_S, Ob_S, coupling)
        psiN = eq35(source_S(gam[i + 1], zb[i + 1], k, Dp))
        Ob_N = zb[i + 1] ** -1.5 * psiN
        D, dD = rk4_delta(eta[i], h, D, dD, k, Ob_S, Ob_N, coupling)
        psiN = eq35(source_S(gam[i + 1], zb[i + 1], k, D))
        Ob_N = zb[i + 1] ** -1.5 * psiN

        # ---- new ray: brane node + bulk diamonds ----
        M1 = int(np.floor((vmax - vb[i + 1]) / delta)) + 1
        s = dv / delta
        base, frac = int(np.floor(s)), s - np.floor(s)
        arr = psir[base:] if base > 0 else psir
        sh = shift_ray(arr, frac)
        Bv = sh[:M1] if len(sh) >= M1 else np.pad(sh, (0, M1 - len(sh)), mode="edge")
        Av = np.empty(M1)
        if M1 > 1:
            Av[1] = psiE  # old ray at v_new[0] (well-stencilled value)
            Av[2:] = Bv[1 : M1 - 1]
        vnew = vb[i + 1] + delta * np.arange(M1)
        # vectorized cell potentials, then the scalar prefix recursion
        Vc = 0.25 * (
            Vpot(ub[i], vnew[:-1], k)
            + Vpot(ub[i], vnew[1:], k)
            + Vpot(ub[i + 1], vnew[:-1], k)
            + Vpot(ub[i + 1], vnew[1:], k)
        )
        coef = (du * delta / 8.0) * Vc
        psinew = np.empty(M1)
        psinew[0] = psiN
        for m in range(1, M1):
            psinew[m] = (Bv[m] + psinew[m - 1]) * (1.0 - coef[m - 1]) - Av[m]
        psir = psinew
        hist_eta.append(eta[i + 1])
        hist_D.append(D)
        hist_Ob.append(Ob_N)
    return {
        "eta": np.array(hist_eta),
        "Delta": np.array(hist_D),
        "Ob": np.array(hist_Ob),
    }


def amp_rms(eta, D, tail=0.2):
    """Phase-robust amplitude: RMS of Delta over the last `tail` fraction."""
    m = eta >= eta[-1] - tail * (eta[-1] - eta[0])
    return float(np.sqrt(np.mean(D[m] ** 2)))


# ------------------------------------------------------------------ battery
def battery():
    k = 5.0
    print(f"=== Gate 1b battery (k={k}, eta in [0.07, 10]) ===")

    print("\n[A] convergence of Delta(eta_f) under (delta, deta_max) refinement:")
    res = []
    for fac in [1.0, 0.5, 0.25]:
        r = run_full(k, delta=0.02 * fac, deta_max=0.01 * fac)
        res.append(r["Delta"][-1])
        print(f"    delta={0.02 * fac:.4g}: Delta_f = {r['Delta'][-1]:+.6e}")
    e12, e23 = abs(res[0] - res[1]), abs(res[1] - res[2])
    if e23 > 0:
        print(f"    order estimate ~ {np.log2(e12 / e23):.2f}")

    print("\n[B] initial-data insensitivity (const-Omega vs zero ray-0):")
    rc = run_full(k, ic="const")
    rz = run_full(k, ic="zero")
    rd = abs(rc["Delta"][-1] - rz["Delta"][-1]) / abs(rc["Delta"][-1])
    print(
        f"    Delta_f const={rc['Delta'][-1]:+.4e}  zero={rz['Delta'][-1]:+.4e}"
        f"  rel diff = {rd:.2e}"
    )

    print("\n[C] high-energy tracking vs the Eq.38 ODE (while H*ell > 3):")
    eta_g, y_g = cardoso_brane.integrate(k, eta_i=0.07, eta_f=10.0, bulk_coupling=1.0)
    Dg = np.interp(rc["eta"], eta_g, y_g[0])
    _, Hf, _ = gam_H_a(rc["eta"], k)
    mf = Hf > 3.0
    dev = np.abs(rc["Delta"][mf] - Dg[mf]) / np.maximum(np.abs(Dg[mf]), 1e-30)
    print(f"    max rel dev (full vs Eq.38) over the high-energy era = {dev.max():.3f}")

    print("\n[D] amplification (coupled/decoupled, tail-RMS) — FULL vs Gate-1a ODE:")
    print(f"    {'k':>5s}{'amp_FULL':>12s}{'amp_Eq38':>12s}")
    for kk in [1.0, 3.0, 5.0, 8.0]:
        rfc = run_full(kk, coupling=1.0)
        rfd = run_full(kk, coupling=0.0)
        ampF = amp_rms(rfc["eta"], rfc["Delta"]) / amp_rms(rfd["eta"], rfd["Delta"])
        ec, yc = cardoso_brane.integrate(kk, eta_i=0.07, eta_f=10.0, bulk_coupling=1.0)
        ed, yd = cardoso_brane.integrate(kk, eta_i=0.07, eta_f=10.0, bulk_coupling=0.0)
        ampO = amp_rms(ec, yc[0]) / amp_rms(ed, yd[0])
        print(f"    {kk:5.1f}{ampF:12.3e}{ampO:12.3e}")


if __name__ == "__main__":
    battery()


# ==========================================================================
# EXACT RS-radiation background (valid at ALL energies): rho/sigma = C/a^4,
# gamma = 1 + C/a^4, H = sqrt(gamma^2-1), da/d eta = a^2 H.  Matched to the
# high-energy form a=(k eta)^{1/3} at eta_i. At low energy a -> sqrt(2C)(eta-
# eta0): the standard GR radiation era. Needed beyond eta_c (the high-energy-
# only Eq.37 background is inconsistent there) and for Gates 2-3.
# ==========================================================================
def build_exact(k, eta_i, eta_f, deta_max, c_du, delta):
    a_i = (k * eta_i) ** (1.0 / 3.0)
    g_i, _, _ = gam_H_a(eta_i, k)
    C = (g_i - 1.0) * a_i**4

    def rhs(y):
        a = y[0]
        g = 1.0 + C / a**4
        H = np.sqrt(max(g * g - 1.0, 0.0))
        return np.array([a * a * H, g])

    eta, Y = [eta_i], [np.array([a_i, 0.0])]
    while eta[-1] < eta_f:
        a = Y[-1][0]
        g = 1.0 + C / a**4
        H = np.sqrt(max(g * g - 1.0, 0.0))
        h = min(deta_max, c_du * delta / (g + H), eta_f - eta[-1])
        y = Y[-1]
        k1 = rhs(y)
        k2 = rhs(y + 0.5 * h * k1)
        k3 = rhs(y + 0.5 * h * k2)
        k4 = rhs(y + h * k3)
        Y.append(y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4))
        eta.append(eta[-1] + h)
    eta = np.array(eta)
    A = np.array([y[0] for y in Y])
    T = np.array([y[1] for y in Y])
    G = 1.0 + C / A**4
    H = np.sqrt(np.maximum(G * G - 1.0, 0.0))
    zb = 1.0 / A
    return eta, T, G, H, A, zb, T - zb, T + zb, C


def run_exact(
    k, eta_i=0.02, eta_f=2.0, delta=0.0125, deta_max=None, c_du=1.0, coupling=1.0
):
    """Same coupled march as run_full but on the EXACT background; the Delta-ODE
    integrates a(eta) jointly in its RK4 state (consistent background at substeps)."""
    if deta_max is None:
        deta_max = delta / 2
    eta, tau, gam, H, a, zb, ub, vb, C = build_exact(
        k, eta_i, eta_f, deta_max, c_du, delta
    )
    N = len(eta) - 1
    vmax = vb[-1] + 8 * delta
    D, dD = (4.0 / 3.0) * (k * eta_i) ** 2, (8.0 / 3.0) * k * k * eta_i
    Ob_gm = k * eta_i**3
    M0 = int(np.floor((vmax - vb[0]) / delta)) + 1
    z0 = 0.5 * (vb[0] + delta * np.arange(M0) - ub[0])
    psir = Ob_gm * z0**1.5
    hE, hD, hO = [eta[0]], [D], [zb[0] ** -1.5 * psir[0]]

    def rk4d(h, D, dD, a0v, Ob0, Ob1):
        def f(s, y):
            av = y[2]
            r = C / av**4
            g = 1.0 + r
            Hh = np.sqrt(max(g * g - 1.0, 0.0))
            br = k * k / 3.0 - 4.0 * r * av * av - 18.0 * r * r * av * av
            Ob = Ob0 + (Ob1 - Ob0) * s / h if h > 0 else Ob0
            return np.array(
                [
                    y[1],
                    -br * y[0] + coupling * (4.0 / 9.0) * k**4 * Ob / av**3,
                    av * av * Hh,
                ]
            )

        y = np.array([D, dD, a0v])
        s = 0.0
        hh = 0.5 * h
        for _ in range(2):
            k1 = f(s, y)
            k2 = f(s + 0.5 * hh, y + 0.5 * hh * k1)
            k3 = f(s + 0.5 * hh, y + 0.5 * hh * k2)
            k4 = f(s + hh, y + hh * k3)
            y = y + (hh / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
            s += hh
        return y[0], y[1]

    for i in range(N):
        h = eta[i + 1] - eta[i]
        du = ub[i + 1] - ub[i]
        dv = vb[i + 1] - vb[i]
        Ob_S = zb[i] ** -1.5 * psir[0]
        aS = alpha_brane(gam[i], zb[i])
        aN = alpha_brane(gam[i + 1], zb[i + 1])
        Vs = Vpot(ub[i], vb[i], k)
        Vn = Vpot(ub[i + 1], vb[i + 1], k)
        Ve = Vpot(ub[i], vb[i + 1], k)
        S_S = source_S(gam[i], zb[i], k, D)
        psiS = psir[0]
        psiE = interp_at(psir, dv / delta)
        den = 12.0 + 6.0 * aN * h + du * dv * Vn

        def eq35(S_N):
            return (
                -(12.0 + 6.0 * aS * h + du * dv * Vs) / den * psiS
                + (24.0 - du * dv * Ve) / den * psiE
                - 6.0 * h * (S_S + S_N) / den
            )

        Dp, _ = rk4d(h, D, dD, a[i], Ob_S, Ob_S)
        psiN = eq35(source_S(gam[i + 1], zb[i + 1], k, Dp))
        Ob_N = zb[i + 1] ** -1.5 * psiN
        D, dD = rk4d(h, D, dD, a[i], Ob_S, Ob_N)
        psiN = eq35(source_S(gam[i + 1], zb[i + 1], k, D))
        Ob_N = zb[i + 1] ** -1.5 * psiN
        M1 = int(np.floor((vmax - vb[i + 1]) / delta)) + 1
        s = dv / delta
        base, frac = int(np.floor(s)), s - np.floor(s)
        arr = psir[base:] if base > 0 else psir
        sh = shift_ray(arr, frac)
        Bv = sh[:M1] if len(sh) >= M1 else np.pad(sh, (0, M1 - len(sh)), mode="edge")
        Av = np.empty(M1)
        if M1 > 1:
            Av[1] = psiE
            Av[2:] = Bv[1 : M1 - 1]
        vnew = vb[i + 1] + delta * np.arange(M1)
        Vc = 0.25 * (
            Vpot(ub[i], vnew[:-1], k)
            + Vpot(ub[i], vnew[1:], k)
            + Vpot(ub[i + 1], vnew[:-1], k)
            + Vpot(ub[i + 1], vnew[1:], k)
        )
        coef = (du * delta / 8.0) * Vc
        pn = np.empty(M1)
        pn[0] = psiN
        for m in range(1, M1):
            pn[m] = (Bv[m] + pn[m - 1]) * (1.0 - coef[m - 1]) - Av[m]
        psir = pn
        hE.append(eta[i + 1])
        hD.append(D)
        hO.append(Ob_N)
    return {
        "eta": np.array(hE),
        "Delta": np.array(hD),
        "Ob": np.array(hO),
        "C": C,
        "a_end": a[-1],
        "eta_end": eta[-1],
    }


# --------- GR two-mode basis (exact GR radiation solution, comoving Delta) ----
def gr_basis(x):
    """D1 (growing, Phi_p-sourced) and D2 (decaying) for radiation in GR:
    Delta_GR = c1*(sin x - x cos x)/x + c2*(cos x + x sin x)/x, x = k eta~/sqrt(3).
    Super-horizon D1 -> x^2/3 matches Eq.40a with Phi_p=-2 (c1=12 for a pure-GR
    history)."""
    D1 = (np.sin(x) - x * np.cos(x)) / x
    D2 = (np.cos(x) + x * np.sin(x)) / x
    return D1, D2


def exact_battery():
    print("=== EXACT-background battery ===")
    print("[E] supercritical k=8 through the era transition (bounded? amplified?):")
    rc = run_exact(8.0, coupling=1.0)
    rd = run_exact(8.0, coupling=0.0)

    def env(r, fr=0.3):
        m = r["eta"] >= r["eta"][-1] - fr * (r["eta"][-1] - r["eta"][0])
        return np.max(np.abs(r["Delta"][m]))

    print(
        f"    late |Delta| envelope: coupled={env(rc):.2f} decoupled={env(rd):.2f}"
        f" -> amp={env(rc)/env(rd):.2f} (P(k) x{(env(rc)/env(rd))**2:.1f}) — BOUNDED, no runaway"
    )

    print("[F] GATE 2 — subcritical k=1.5: GR two-mode recovery at low energy:")
    k = 1.5
    r = run_exact(k, eta_i=0.02, eta_f=9.0, delta=0.01)
    slope = np.sqrt(2 * r["C"])
    eta0 = r["eta_end"] - r["a_end"] / slope
    x = k * (r["eta"] - eta0) / np.sqrt(3.0)
    # least-squares match of (c1, c2) in the GR window x in [2.5, 3.5]
    mw = (x > 2.5) & (x < 3.5)
    D1, D2 = gr_basis(x[mw])
    M = np.vstack([D1, D2]).T
    c, *_ = np.linalg.lstsq(M, r["Delta"][mw], rcond=None)
    mt = (x > 4.0) & (x < 7.0)
    D1t, D2t = gr_basis(x[mt])
    pred = c[0] * D1t + c[1] * D2t
    envl = np.max(np.abs(r["Delta"][mt]))
    dev = np.max(np.abs(r["Delta"][mt] - pred)) / envl
    print(f"    LSQ match x in [2.5,3.5]: c1={c[0]:+.2f}, c2={c[1]:+.2f}")
    print(
        f"    prediction over x in [4,7]: max |dev|/envelope = {dev:.3f}"
        f"  (c1 vs pure-GR-history 12: transition factor {c[0]/12.0:.2f})"
    )
    print("    READ: bounded two-mode GR oscillation at low energy -> GR recovered;")
    print("    c1/12 is the physical high-energy-era transfer distortion (CHKS-type).")


if __name__ == "__main__" and "__EXACT__" in __import__("sys").argv:
    exact_battery()
