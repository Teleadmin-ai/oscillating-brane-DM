"""
GATE 3 — the OBT growth-sign experiment (first probe).

Setup: low-energy DUST brane (matter era) with an IMPOSED radion oscillation on
the trajectory, z_b(eta) = z_smooth(eta) * [1 + eps*sin(om*(eta-eta_i)+ph)],
evolved with the validated coupled bulk+brane solver (gate1_full machinery) and
the RETARDED bulk (data only on the initial null ray + the brane => the causal,
no-incoming-radiation solution — precisely the regularity-type BC at the heart
of the closure question).

DUST specialization of CHKS (Eq. 28 verified GENERAL-w on ar5iv; Eq. 33a):
  friction (1+3c_s^2-6w) = 1  ->  + H_c Delta'
  A = -1, B = -4  ->  bracket = -3 r a^2 - 12 r^2 a^2   (r = rho_m/sigma)
  source = k^4 Omega_b / (3 a^3)
KEY STRUCTURAL FACT (decisive for the readout): 3 r a^2 = 4 pi G rho a^2 ell^2
EXACTLY (rho/sigma = kappa4^2 ell^2 rho/6), and at low energy 3 r a^2 ->
(3/2) H_c^2 — i.e. the A-term IS the standard 4D Poisson self-gravity for dust.
The bulk field Omega_b therefore carries ONLY the 5D correction, so
    deltaG_bulk(eta) := [k^4 Omega_b/(3 a^3)] / [(3/2) H_c_smooth^2 Delta]
is the bulk's ADDITIONAL gravity in Poisson units — the quantity whose
amplitude/PHASE response to the radion oscillation is the closure question
(OBT's G_eff = G_N [1 + f_osc W(t/T + delta_bulk/2pi)], delta_bulk = 1.36 rad).

Junction (psi-variables, validated): alpha = +gamma/(2 z_b);
  S = -6 (rho_m a^3/sigma) z_b^{1/2} Delta / k^2 = -6 C3 z_b^{1/2} Delta / k^2
  (dust conservation rho_m a^3 = const even on the oscillating background).

MODELING CHOICES / CAVEATS (honest):
  (1) the radion oscillation is IMPOSED (OBT's stick-slip motor sustains it;
      the motor's own perturbations are NOT modeled — they are exactly the
      free Weyl-sourcing data of the closure problem; tonight = "motor
      unperturbed" assumption);
  (2) single-brane Poincare AdS bulk (continuum KK; OBT proper has a compact /
      two-brane bulk -> discrete KK + blockade; this run is the maximally
      dissipative causal bulk — Gate 4 variation);
  (3) compressed hierarchy: H << om < 1/ell ordering correct but ratios ~10^1
      instead of 10^26+; OBT-relevant EVANESCENT regime k > om is used for the
      headline (cosmological S8 scales have ck >> omega_radion).
"""

import numpy as np

from gate1_full import Vpot, alpha_brane, interp_at, shift_ray


# ---------------------------------------------------------------- background
def make_traj(H_i, eps, om, ph, eta_i):
    """Closed-form smooth dust background (a_i=1 at eta_i, low-energy form;
    O((C3/a^3)^2) corrections ~1e-8 here) + analytic radion modulation.
    Returns C3 and functions z(eta), zp(eta), a(eta), Hc(eta), r(eta)=rho_m/sig."""
    g_i = np.sqrt(1.0 + H_i * H_i)
    C3 = g_i - 1.0
    s2 = np.sqrt(2.0 * C3)

    def a_s(eta):
        return (1.0 + 0.5 * s2 * (eta - eta_i)) ** 2

    def z_s(eta):
        return 1.0 / a_s(eta)

    def H_s(eta):  # proper H of the smooth background (exact RS-dust on a_s)
        g = 1.0 + C3 / a_s(eta) ** 3
        return np.sqrt(np.maximum(g * g - 1.0, 0.0))

    T = 2.0 * np.pi / max(om, 1e-12)

    def ramp(eta):  # adiabatic switch-on: sin^2 over the first cycle (R(0)=R'(0)=0)
        x = (eta - eta_i) / T
        return np.where(x < 1.0, np.sin(0.5 * np.pi * np.clip(x, 0, 1)) ** 2, 1.0)

    def rampp(eta):
        x = (eta - eta_i) / T
        return np.where(
            x < 1.0,
            (np.pi / (2.0 * T)) * np.sin(np.pi * np.clip(x, 0, 1)),
            0.0,
        )

    def mod(eta):
        return 1.0 + eps * ramp(eta) * np.sin(om * (eta - eta_i) + ph)

    def modp(eta):
        return eps * (
            rampp(eta) * np.sin(om * (eta - eta_i) + ph)
            + ramp(eta) * om * np.cos(om * (eta - eta_i) + ph)
        )

    def z(eta):
        return z_s(eta) * mod(eta)

    def zp(eta):  # dz/d eta ; z_s' = -H_s exactly
        return -H_s(eta) * mod(eta) + z_s(eta) * modp(eta)

    def a(eta):
        return 1.0 / z(eta)

    def Hc(eta):  # conformal Hubble of the ACTUAL brane = -z'/z
        return -zp(eta) / z(eta)

    def r(eta):  # rho_m/sigma with dust conservation on the ACTUAL a
        return C3 * z(eta) ** 3

    return C3, z, zp, a, Hc, r


# ------------------------------------------------------------------ the run
def run_gate3(
    k=0.6,
    H_i=0.02,
    eps=0.03,
    om=0.3,
    ph=0.0,
    n_cyc=4.0,
    delta=0.05,
    deta_max=0.025,
    c_du=1.0,
    coupling=1.0,
):
    """Dust brane + imposed radion oscillation, coupled retarded bulk.
    Histories: Delta, Omega_b, deltaG_bulk (bulk gravity in Poisson units)."""
    eta_i = 0.0
    Trad = 2.0 * np.pi / om
    eta_f = eta_i + n_cyc * Trad
    C3, zf, zpf, af, Hcf, rf = make_traj(H_i, eps, om, ph, eta_i)

    # brane node arrays (adaptive rule; ~uniform here since gamma ~ 1)
    etas = [eta_i]
    while etas[-1] < eta_f:
        g = np.sqrt(1.0 + zpf(etas[-1]) ** 2)
        h = min(deta_max, c_du * delta / (g + abs(zpf(etas[-1]))), eta_f - etas[-1])
        etas.append(etas[-1] + h)
    eta = np.array(etas)
    zb = zf(eta)
    gam = np.sqrt(1.0 + zpf(eta) ** 2)
    tau = np.empty_like(eta)
    tau[0] = 0.0
    for i in range(len(eta) - 1):  # Simpson with analytic midpoint
        h = eta[i + 1] - eta[i]
        gm = np.sqrt(1.0 + zpf(0.5 * (eta[i] + eta[i + 1])) ** 2)
        tau[i + 1] = tau[i] + h * (gam[i] + 4.0 * gm + gam[i + 1]) / 6.0
    ub, vb = tau - zb, tau + zb
    N = len(eta) - 1
    vmax = vb[-1] + 8 * delta

    # dust growing-mode IC on the SMOOTH background (ramp => exact at eta_i),
    # shared by all runs; retarded bulk starts empty
    _, _, _, _, Hc_s0, _ = make_traj(H_i, 0.0, om, 0.0, eta_i)
    D, dD = 1.0, Hc_s0(eta_i) * 1.0
    M0 = int(np.floor((vmax - vb[0]) / delta)) + 1
    psir = np.zeros(M0)

    def S_brane(etax, Delta):  # junction matter source (dust: rho_m a^3/sig = C3)
        return -6.0 * C3 * np.sqrt(zf(etax)) * Delta / (k * k)

    def rk4_dust(eta0, h, D, dD, Ob0, Ob1):
        def f(t, y):
            av = af(t)
            rv = rf(t)
            br = -3.0 * rv * av * av - 12.0 * rv * rv * av * av  # A=-1, B=-4
            Ob = Ob0 + (Ob1 - Ob0) * (t - eta0) / h if h > 0 else Ob0
            src = coupling * k**4 * Ob / (3.0 * av**3)
            return np.array([y[1], -Hcf(t) * y[1] - br * y[0] + src])

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

    hE, hD, hOb = [eta[0]], [D], [zb[0] ** -1.5 * psir[0]]
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
        S_S = S_brane(eta[i], D)
        psiS = psir[0]
        psiE = interp_at(psir, dv / delta)
        den = 12.0 + 6.0 * aN * h + du * dv * Vn

        def eq35(S_N):
            return (
                -(12.0 + 6.0 * aS * h + du * dv * Vs) / den * psiS
                + (24.0 - du * dv * Ve) / den * psiE
                - 6.0 * h * (S_S + S_N) / den
            )

        Dp, _ = rk4_dust(eta[i], h, D, dD, Ob_S, Ob_S)
        psiN = eq35(S_brane(eta[i + 1], Dp))
        Ob_N = zb[i + 1] ** -1.5 * psiN
        D, dD = rk4_dust(eta[i], h, D, dD, Ob_S, Ob_N)
        psiN = eq35(S_brane(eta[i + 1], D))
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
        hOb.append(Ob_N)

    eta_h = np.array(hE)
    D_h = np.array(hD)
    Ob_h = np.array(hOb)
    # smooth-background conformal Hubble for the Poisson normalization
    _, _, _, _, Hc_s, _ = make_traj(H_i, 0.0, om, 0.0, eta_i)
    Hcs = Hc_s(eta_h)
    dG = (k**4 * Ob_h / (3.0 * af(eta_h) ** 3)) / (1.5 * Hcs**2 * D_h)
    return {"eta": eta_h, "Delta": D_h, "Ob": Ob_h, "dG": dG, "om": om, "ph": ph}


# ----------------------------------------------------------------- analysis
def lockin(r, skip_cyc=2.0):
    """Project deltaG_bulk onto sin/cos of the radion phase over the last full
    cycles (after ramp + burn-in). Returns (amplitude, phase[rad], mean)."""
    om = r["om"]
    T = 2.0 * np.pi / om
    eta = r["eta"]
    m = (eta >= eta[0] + skip_cyc * T) & (
        eta <= eta[0] + np.floor(eta[-1] / T + 1e-9) * T
    )
    x = om * (eta[m] - eta[0]) + r["ph"]
    y = r["dG"][m]
    y0 = np.trapezoid(y, eta[m]) / (eta[m][-1] - eta[m][0])
    yc = y - y0
    span = eta[m][-1] - eta[m][0]
    As = 2.0 * np.trapezoid(yc * np.sin(x), eta[m]) / span
    Ac = 2.0 * np.trapezoid(yc * np.cos(x), eta[m]) / span
    return np.hypot(As, Ac), np.arctan2(Ac, As), y0


def diff_lockin(r_eps, r_0, epsv, skip_cyc=2.0):
    """DIFFERENTIAL lock-in: subtract the smooth run's dG (interpolated onto the
    eps-run grid) to remove the secular 5D-correction drift exactly, detrend the
    residual linearly over the window, then project onto the radion phase.
    Returns (A/eps, phase[rad])."""
    om = r_eps["om"]
    T = 2.0 * np.pi / om
    eta = r_eps["eta"]
    dG0 = np.interp(eta, r_0["eta"], r_0["dG"])
    y = r_eps["dG"] - dG0
    m = (eta >= eta[0] + skip_cyc * T) & (
        eta <= eta[0] + np.floor(eta[-1] / T + 1e-9) * T
    )
    ew, yw = eta[m], y[m]
    cfit = np.polyfit(ew, yw, 1)  # residual linear trend
    yw = yw - np.polyval(cfit, ew)
    x = om * (ew - eta[0]) + r_eps["ph"]
    span = ew[-1] - ew[0]
    As = 2.0 * np.trapezoid(yw * np.sin(x), ew) / span
    Ac = 2.0 * np.trapezoid(yw * np.cos(x), ew) / span
    return np.hypot(As, Ac) / epsv, np.arctan2(Ac, As)


def battery():
    print("=== GATE 3 battery: dust brane + imposed radion oscillation ===")
    print("convention: delta z/z = +eps*sin(om*eta~); dG response fitted as")
    print("A*sin(om*eta~ + phi). OBT BKM claims a retardation phase ~1.36 rad.\n")

    print("[P] pre-check (eps=0): dust GR recovery on the smooth background:")
    r0 = run_gate3(eps=0.0)
    lnD = np.log(r0["Delta"])
    # growth index p = dlnDelta/dlna over the second half
    _, zf, _, af, _, _ = make_traj(0.02, 0.0, 0.3, 0.0, 0.0)
    lna = np.log(af(r0["eta"]))
    h2 = r0["eta"] > 0.5 * r0["eta"][-1]
    p = np.polyfit(lna[h2], lnD[h2], 1)[0]
    print(f"    growth index p = dlnD/dlna = {p:.3f}   (GR-EdS dust: 1.000)")
    print(
        f"    residual bulk gravity <dG> = {np.mean(r0['dG'][h2]):+.4f} (5D correction, small)"
    )

    print("\n[G3] headline (k=0.6, om=0.3 — OBT-like evanescent regime k>om),")
    print("    DIFFERENTIAL lock-in (eps-run minus smooth run, detrended):")
    rc = run_gate3(eps=0.03)
    Ae, phi = diff_lockin(rc, r0, 0.03)
    print(f"    bulk response: A/eps = {Ae:.4f},  PHASE phi = {phi:+.3f} rad")
    print(f"    (lag = {-phi:+.3f} rad; OBT/BKM viscoelastic claim: lag ~ 1.36 rad)")
    net = rc["Delta"][-1] / r0["Delta"][-1] - 1.0
    print(
        f"    net growth (osc vs smooth, 4 cycles, matched IC+ramp): ratio-1 = {net:+.2e}"
    )

    print("\n[R] robustness / regime sweep (differential lock-in):")
    base0 = {"k": r0}
    for tag, kw in [
        ("eps/2 (linearity)", dict(eps=0.015)),
        ("phase pi/2 (invariance)", dict(eps=0.03, ph=np.pi / 2)),
        ("k=0.3 (marginal)", dict(eps=0.03, k=0.3)),
        ("om=0.6,k=0.3 (radiating)", dict(eps=0.03, k=0.3, om=0.6)),
        ("delta/2 (convergence)", dict(eps=0.03, delta=0.025, deta_max=0.0125)),
    ]:
        rr = run_gate3(**kw)
        kw0 = {kk: vv for kk, vv in kw.items() if kk not in ("eps", "ph")}
        kw0["eps"] = 0.0
        rz = run_gate3(**kw0)
        epsv = kw.get("eps", 0.03)
        Ae, phi = diff_lockin(rr, rz, epsv)
        netr = rr["Delta"][-1] / rz["Delta"][-1] - 1.0
        print(f"    {tag:26s}: A/eps={Ae:8.4f}  phi={phi:+.3f} rad  net={netr:+.2e}")


def secular_rate(kw, n_cyc=6.0):
    """Secular growth-rate shift: fit ln(D_osc/D_smooth) = c0 + c1*eta + A sin +
    B cos over cycles >=2. A TRUE secular term must be drive-phase invariant;
    sign flips under ph-shifts expose residual oscillatory leakage instead."""
    r1 = run_gate3(n_cyc=n_cyc, **kw)
    kw0 = {kk: vv for kk, vv in kw.items() if kk not in ("eps", "ph")}
    r0 = run_gate3(eps=0.0, n_cyc=n_cyc, **kw0)
    D0 = np.interp(r1["eta"], r0["eta"], r0["Delta"])
    y = np.log(r1["Delta"] / D0)
    om = r1["om"]
    T = 2 * np.pi / om
    eta = r1["eta"]
    m = eta >= eta[0] + 2.0 * T
    ew, yw = eta[m], y[m]
    X = np.vstack([np.ones_like(ew), ew, np.sin(om * ew), np.cos(om * ew)]).T
    c, *_ = np.linalg.lstsq(X, yw, rcond=None)
    return c[1]


def secular_battery():
    """[S] the growth-SIGN readout. Result (June 2026): |c1| <~ 1e-6/eta AND the
    sign flips with the drive phase => the conservative retarded bulk produces NO
    measurable secular growth modification (bound ~2 orders below the magnitude
    OBT's S8 mechanism would need in matched units, ~3e-4/eta)."""
    print(
        "[S] secular rate c1 = d ln(D_osc/D_sm)/d eta  [true effect must be ph-invariant]"
    )
    for tag, kw in [
        ("ph=0    ", dict(eps=0.03)),
        ("ph=pi/2 ", dict(eps=0.03, ph=np.pi / 2)),
        ("ph=pi   ", dict(eps=0.03, ph=np.pi)),
        ("eps=.015", dict(eps=0.015)),
    ]:
        print(f"    {tag}: c1 = {secular_rate(kw):+.3e}")


if __name__ == "__main__":
    battery()
    print()
    secular_battery()
