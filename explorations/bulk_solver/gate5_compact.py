"""
GATE 5 — the COMPACT (two-boundary) bulk: deriving the bit.

Physics: in a compact bulk there is no past null infinity, hence NO free
incoming-Weyl datum: transients (cavity ringing) decay under the brane's PBH
dissipation (babs), and the steady response to the radion drive is UNIQUE.
Driving below the cavity gap (om << m1 ~ pi/(2(z2-zb)) — the kinematic-blockade
regime), the response is elastic and in phase, with a sign set by the GEOMETRY:
the candidate derivation of the one remaining input bit (the sign of the
G_eff <-> radion coupling).

Geometry/machinery: rays from the moving brane (u = u_b,i), each ray now ENDS
at the static second boundary z = z2 (the line v = u + 2 z2). Ray nodes stored
ascending in v: [brane node (irregular)] + [regular nodes] + [far node at
v_far,i = u_b,i + 2 z2]. Bulk diamonds with per-cell dv; all ray-to-ray
transfers via general non-uniform 4-point cubic interpolation; far-boundary
node via the MIRRORED Eq. 35 triangular update (S2 = old far node, E2 = new
ray at v_far,old, d_eta2 = du, du*dv = du^2), with the far Robin coefficient
alpha2 a PARAMETER (far-BC variants: positive-tension-like -5/(2 z2),
tensor-Neumann-like -3/(2 z2), negative-tension-like -1/(2 z2); the (n.D)
convention at the far boundary uses the INTO-BULK normal n = -z hat:
(n.D)psi = -psi_z for the static boundary — validated by MMS below).

Validation [M]: MMS with the Gate-0.5 Bessel oracle psi = cos(w t) sqrt(z)
J0(q z), MOVING brane z_b(t) = z0 + A sin(Om t) + static far boundary, both
Robin coefficients defined from the oracle -> global order ~2 expected.

The bit battery [B]: dust brane + radion (gate3 setup) in the compact bulk,
PBH dissipation babs damping the ring-down; differential lock-in of
deltaG_bulk vs the radion across: far-BC variants x z2 positions x ICs.
If the IN-PHASE response sign is robust -> the bit is derived (in this model).
[K]: k-scaling of the response -> extrapolation to cosmological k (the
(k ell)^2 suppression statement).
"""

import numpy as np
from scipy.special import j0, j1

from gate1_full import Vpot
from gate3_obt import make_traj


def interp_nu(vt, varr, parr):
    """General non-uniform 4-point cubic interpolation on ascending varr."""
    n = len(varr)
    i = int(np.searchsorted(varr, vt))
    i0 = max(0, min(i - 2, n - 4))
    xs, ys = varr[i0 : i0 + 4], parr[i0 : i0 + 4]
    out = 0.0
    for a in range(4):
        term = ys[a]
        for b in range(4):
            if b != a:
                term *= (vt - xs[b]) / (xs[a] - xs[b])
        out += term
    return out


def run_compact(
    k=0.6,
    H_i=0.02,
    eps=0.03,
    om=0.3,
    ph=0.0,
    n_cyc=4.0,
    delta=0.05,
    deta_max=0.025,
    z2_off=2.5,
    alpha2_fac=-2.5,
    babs=0.05,
    coupling=1.0,
    m2=0.0,
    mms=None,
):
    """Compact-bulk coupled march. alpha2 = alpha2_fac / z2. m2 = effective
    Goldberger-Wise stabilization gap added to the bulk potential (V -> V + m2):
    a CRUDE effective model of the stabilized scalar sector (flagged modeling
    choice; the unstabilized cavity is tachyonic at low k = the known RS1
    radion instability, which this solver detects ab initio).
    mms: None for physics; else dict(w=..., A=..., Om=..., z0=..., t0=...) runs
    the MMS oracle test (returns max global error instead of histories)."""
    eta_i = 0.0
    if mms is None:
        Trad = 2.0 * np.pi / om
        eta_f = eta_i + n_cyc * Trad
        C3, zf, zpf, af, Hcf, rf = make_traj(H_i, eps, om, ph, eta_i)
        # smooth twin for the Poisson normalization
        _, _, _, _, Hc_s, _ = make_traj(H_i, 0.0, om, 0.0, eta_i)
    else:
        w, Aosc, Omosc, z0m, t0m = (mms[x] for x in ("w", "A", "Om", "z0", "t0"))
        qm = np.sqrt(w * w - k * k)
        eta_f = mms.get("T", 1.0)
        zf = lambda t: z0m + Aosc * np.sin(Omosc * (t + t0m))  # noqa: E731
        zpf = lambda t: Aosc * Omosc * np.cos(Omosc * (t + t0m))  # noqa: E731

        def oracle(u, v):
            t, z = 0.5 * (u + v), 0.5 * (v - u)
            return np.cos(w * t) * np.sqrt(z) * j0(qm * z)

        def dn_brane(t_coord, z, zd):
            """Moving-brane flat normal at the node's COORDINATE time t_coord,
            position z, with zd = dz/dtau (coordinate velocity = zpf/gamma)."""
            pt = -w * np.sin(w * t_coord) * np.sqrt(z) * j0(qm * z)
            pz = np.cos(w * t_coord) * (
                j0(qm * z) / (2 * np.sqrt(z)) - qm * np.sqrt(z) * j1(qm * z)
            )
            return (zd * pt + pz) / np.sqrt(1.0 - zd * zd)

        def dn_far(t, z2v):  # static far boundary, INTO-bulk normal = -z hat
            pz = np.cos(w * t) * (
                j0(qm * z2v) / (2 * np.sqrt(z2v)) - qm * np.sqrt(z2v) * j1(qm * z2v)
            )
            return -pz

    # trajectory arrays (proper-time parametrization, Simpson tau)
    etas = [eta_i]
    while etas[-1] < eta_f:
        g = np.sqrt(1.0 + zpf(etas[-1]) ** 2)
        h = min(deta_max, delta / (g + abs(zpf(etas[-1]))), eta_f - etas[-1])
        etas.append(etas[-1] + h)
    eta = np.array(etas)
    zb = zf(eta)
    gam = np.sqrt(1.0 + zpf(eta) ** 2)
    tau = np.empty_like(eta)
    tau[0] = 0.0
    for i in range(len(eta) - 1):
        h = eta[i + 1] - eta[i]
        gm = np.sqrt(1.0 + zpf(0.5 * (eta[i] + eta[i + 1])) ** 2)
        tau[i + 1] = tau[i] + h * (gam[i] + 4.0 * gm + gam[i + 1]) / 6.0
    ub, vb = tau - zb, tau + zb
    z2 = zb[0] + z2_off
    vfar = ub + 2.0 * z2
    N = len(eta) - 1
    a2 = alpha2_fac / z2

    def ray_nodes(i):
        M = int(np.floor((vfar[i] - vb[i]) / delta))
        reg = vfar[i] - delta * np.arange(M - 1, -1, -1)  # ascending, ends at vfar
        return np.concatenate(([vb[i]], reg))

    # ray 0
    varr = ray_nodes(0)
    if mms is None:
        psir = np.zeros_like(varr)
        D, dD = 1.0, Hc_s(eta_i) * 1.0
        hE, hD, hOb = [eta[0]], [D], [zb[0] ** -1.5 * psir[0]]
    else:
        psir = np.array([oracle(ub[0], v) for v in varr])
        err = 0.0

    for i in range(N):
        h = eta[i + 1] - eta[i]
        du = ub[i + 1] - ub[i]
        dvb = vb[i + 1] - vb[i]
        vnew = ray_nodes(i + 1)
        pnew = np.empty_like(vnew)

        # ---- brane node (Eq.35 with dissipation babs; MMS: oracle alphas) ----
        if mms is None:
            aS = 0.5 * gam[i] / zb[i]
            aN = 0.5 * gam[i + 1] / zb[i + 1]
            S_S = -6.0 * C3 * np.sqrt(zb[i]) * D / (k * k)
        else:
            zdS = zpf(eta[i]) / gam[i]
            zdN = zpf(eta[i + 1]) / gam[i + 1]
            aS = dn_brane(0.5 * (ub[i] + vb[i]), zb[i], zdS) / oracle(ub[i], vb[i])
            aN = dn_brane(0.5 * (ub[i + 1] + vb[i + 1]), zb[i + 1], zdN) / oracle(
                ub[i + 1], vb[i + 1]
            )
            S_S = 0.0
        Vs = Vpot(ub[i], vb[i], k) + m2
        Vn = Vpot(ub[i + 1], vb[i + 1], k) + m2
        Ve = Vpot(ub[i], vb[i + 1], k) + m2
        psiS = psir[0]
        psiE = interp_nu(vb[i + 1], varr, psir)
        den = 12.0 * (1.0 + babs) + 6.0 * aN * h + du * dvb * Vn

        def eq35(S_N):
            return (
                -(12.0 * (1.0 - babs) + 6.0 * aS * h + du * dvb * Vs) / den * psiS
                + (24.0 - du * dvb * Ve) / den * psiE
                - 6.0 * h * (S_S + S_N) / den
            )

        if mms is None:
            # Heun for the dust Delta (as gate3: A=-1, B=-4, w=0)
            def rk4_dust(D0, dD0, Ob0, Ob1):
                def f(t, y):
                    av = af(t)
                    rv = rf(t)
                    br = -3.0 * rv * av * av - 12.0 * rv * rv * av * av
                    Ob = Ob0 + (Ob1 - Ob0) * (t - eta[i]) / h if h > 0 else Ob0
                    return np.array(
                        [
                            y[1],
                            -Hcf(t) * y[1]
                            - br * y[0]
                            + coupling * k**4 * Ob / (3.0 * av**3),
                        ]
                    )

                y = np.array([D0, dD0])
                t0_, hh = eta[i], 0.5 * h
                for _ in range(2):
                    k1 = f(t0_, y)
                    k2 = f(t0_ + 0.5 * hh, y + 0.5 * hh * k1)
                    k3 = f(t0_ + 0.5 * hh, y + 0.5 * hh * k2)
                    k4 = f(t0_ + hh, y + hh * k3)
                    y = y + (hh / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
                    t0_ += hh
                return y[0], y[1]

            Ob_S = zb[i] ** -1.5 * psir[0]
            Dp, _ = rk4_dust(D, dD, Ob_S, Ob_S)
            pn0 = eq35(-6.0 * C3 * np.sqrt(zb[i + 1]) * Dp / (k * k))
            ObN = zb[i + 1] ** -1.5 * pn0
            D, dD = rk4_dust(D, dD, Ob_S, ObN)
            pn0 = eq35(-6.0 * C3 * np.sqrt(zb[i + 1]) * D / (k * k))
            ObN = zb[i + 1] ** -1.5 * pn0
        else:
            pn0 = eq35(0.0)
        pnew[0] = pn0

        # ---- bulk diamonds (ascending; per-cell dv; nonuniform transfers) ----
        for jj in range(1, len(vnew) - 1):
            v_lo, v_hi = vnew[jj - 1], vnew[jj]
            Aval = psiE if jj == 1 else interp_nu(v_lo, varr, psir)
            Bval = interp_nu(v_hi, varr, psir)
            Cval = pnew[jj - 1]
            dvc = v_hi - v_lo
            Vc = m2 + 0.25 * (
                Vpot(ub[i], v_lo, k)
                + Vpot(ub[i], v_hi, k)
                + Vpot(ub[i + 1], v_lo, k)
                + Vpot(ub[i + 1], v_hi, k)
            )
            pnew[jj] = Bval + Cval - Aval - (du * dvc / 8.0) * Vc * (Bval + Cval)

        # ---- far-boundary node (mirrored Eq.35; static: d_eta2 = du) ----
        if mms is None:
            a2S = a2N = a2
        else:
            a2S = dn_far(0.5 * (ub[i] + vfar[i]), z2) / oracle(ub[i], vfar[i])
            a2N = dn_far(0.5 * (ub[i + 1] + vfar[i + 1]), z2) / oracle(
                ub[i + 1], vfar[i + 1]
            )
        V_S2 = Vpot(ub[i], vfar[i], k) + m2
        V_N2 = Vpot(ub[i + 1], vfar[i + 1], k) + m2
        V_E2 = Vpot(ub[i + 1], vfar[i], k) + m2
        psiS2 = psir[-1]
        psiE2 = interp_nu(vfar[i], vnew[:-1], pnew[:-1])
        den2 = 12.0 + 6.0 * a2N * du + du * du * V_N2
        pnew[-1] = (
            -(12.0 + 6.0 * a2S * du + du * du * V_S2) / den2 * psiS2
            + (24.0 - du * du * V_E2) / den2 * psiE2
        )

        varr, psir = vnew, pnew
        if mms is None:
            hE.append(eta[i + 1])
            hD.append(D)
            hOb.append(ObN)
        else:
            ex = np.array([oracle(ub[i + 1], v) for v in vnew])
            err = max(err, np.max(np.abs(pnew - ex)))

    if mms is not None:
        return err
    eta_h, D_h, Ob_h = np.array(hE), np.array(hD), np.array(hOb)
    Hcs = Hc_s(eta_h)
    dG = (k**4 * Ob_h / (3.0 * af(eta_h) ** 3)) / (1.5 * Hcs**2 * D_h)
    return {"eta": eta_h, "Delta": D_h, "Ob": Ob_h, "dG": dG, "om": om, "ph": ph}


# ------------------------------------------------------------------ batteries
def battery_mms():
    print("[M] MMS: moving brane + static far boundary, Bessel oracle (expect ~2):")
    prev = None
    for dl in [0.08, 0.04, 0.02, 0.01]:
        e = run_compact(
            k=1.0,
            delta=dl,
            deta_max=dl / 2,
            z2_off=1.5,
            babs=0.0,
            mms=dict(w=3.0, A=0.10, Om=0.9, z0=1.0, t0=1.0, T=1.0),
        )
        o = "-" if prev is None else f"{np.log2(prev / e):.2f}"
        print(f"    delta={dl:5.3f}: Linf={e:.3e}  order={o}")
        prev = e


# ------------------------------------------------------------------ batteries
def battery_bit():
    """[B] the bit, STABLE far-BCs only. FINDINGS (June 2026): (i) alpha2 =
    -5/(2 z2) (positive-tension-like far brane) is EXCLUDED by the solver
    itself: it supports a tachyonic far-surface mode (kappa ~ 2.5/z2 ->
    sigma ~ 0.39 -> e^{sigma*span} ~ 1e14, exactly the observed blowup) — the
    characteristic scheme dynamically detecting that an RS slab needs a
    NEGATIVE-tension far brane; (ii) on the stable far-BCs the in-phase
    response is POSITIVE and convergent in the physical ordering om < ck <<
    kappa_1, BUT the compact spectrum makes the sign RESONANCE-STRUCTURED at
    compressed hierarchy: z2_off=2.0 flips via a 3-omega harmonic landing on a
    cavity mode (killed by raising babs — see battery_kprime), and k <= om
    crosses the zero-mode dispersion (om = ck) where the response blows up and
    rotates. In OBT's REAL hierarchy (om << ck << 1/ell by 26+ orders) no
    crossing is possible: the system sits in the global static limit."""
    import numpy as np

    from gate3_obt import diff_lockin

    B = dict(alpha2_fac=-1.5)
    print("[B] in-phase response, stable far-BCs (eps=0.03, k=0.6, om=0.3):")
    for tag, kw in [
        ("headline a2=-1.5/z2 z2off=2.5", dict()),
        ("a2=-0.5/z2 (neg-tension-like)", dict(alpha2_fac=-0.5)),
        ("z2_off=3.0", dict(z2_off=3.0)),
        ("babs=0.10", dict(babs=0.10)),
        ("babs=0.02", dict(babs=0.02)),
        ("drive phase pi/2", dict(ph=np.pi / 2)),
        ("delta/2", dict(delta=0.025, deta_max=0.0125)),
    ]:
        kk = {**B, **kw, "eps": 0.03}
        rc = run_compact(**kk)
        k0 = {k_: v for k_, v in kk.items() if k_ not in ("eps", "ph")}
        rz = run_compact(eps=0.0, **k0)
        A, phi = diff_lockin(rc, rz, 0.03)
        print(f"    {tag:30s}: inphase={A * np.cos(phi):+8.4f} (phi={phi:+.3f})")


def battery_kprime():
    """[K'] fixed-ratio scaling om = k/2 (the physical ordering om < ck
    everywhere) + the z2off=2.0 harmonic-resonance diagnosis."""
    import numpy as np

    from gate3_obt import diff_lockin

    B = dict(alpha2_fac=-1.5)
    print("[K'] om = k/2 fixed-ratio scaling (sub-zero-mode everywhere):")
    for kv in [0.6, 0.4, 0.3, 0.2]:
        rc = run_compact(eps=0.03, k=kv, om=kv / 2, **B)
        rz = run_compact(eps=0.0, k=kv, om=kv / 2, **B)
        A, phi = diff_lockin(rc, rz, 0.03)
        print(
            f"    k={kv:4.2f}: inphase={A * np.cos(phi):+8.4f}"
            f"  /k^2={A * np.cos(phi) / kv**2:+.4f}  (phi={phi:+.3f})"
        )
    print("[R'] z2off=2.0 anomaly vs damping (harmonic-resonance test):")
    for tag, kw in [
        ("babs=0.05 (anomalous)", dict(z2_off=2.0)),
        ("babs=0.30 (Q killed)", dict(z2_off=2.0, babs=0.30)),
    ]:
        kk = {**B, **kw, "eps": 0.03}
        rc = run_compact(**kk)
        k0 = {k_: v for k_, v in kk.items() if k_ != "eps"}
        rz = run_compact(eps=0.0, **k0)
        A, phi = diff_lockin(rc, rz, 0.03)
        print(f"    {tag:24s}: inphase={A * np.cos(phi):+8.4f} (phi={phi:+.3f})")


def battery_stabilized():
    """[S] THE DERIVATION (June 2026). GW-stabilized cavity (m2 = effective
    Goldberger-Wise gap; OBT has m_phi = 0.36 eV): stability restored at all k,
    and the in-phase response sign becomes UNIFORMLY POSITIVE across the whole
    model space — far-BCs, cavity depths (incl. the ex-anomalous z2off=2.0),
    stabilization stiffness, dissipation: inphase = +0.087..+0.107, phi ~ +0.03
    (elastic, in phase). THE BIT IS DERIVED in the stabilized compact model:
    sign(dG_bulk / d(z_b)) = +. BUT the fixed-ratio scaling (om = k/2, the
    physical ordering: S8 scales have ck >> om_radion; om = ck only at the
    613 Mpc cymatic crossover) shows the channel dies as ~k^3..k^4
    (0.1018 -> 0.0024 for k 0.6 -> 0.2) => at cosmological k*ell ~ 1e-30 the
    derived channel is suppressed beyond ANY relevance (stronger than the
    audit's (kL)^2). FINAL: the only bulk-derivable sign is + but carries no
    cosmological weight; the S8-scale bit remains irreducibly the brane-local
    PBH coupling sign (Gate 4b), in EVERY bulk configuration tested."""
    import numpy as np

    from gate3_obt import diff_lockin

    B = dict(alpha2_fac=-1.5, m2=0.5)
    print("[S] GW-stabilized: sign sweep (k=0.6, om=0.3):")
    for tag, kw in [
        ("headline z2off=2.5", dict()),
        ("z2off=2.0 (ex-flip)", dict(z2_off=2.0)),
        ("a2=-0.5/z2", dict(alpha2_fac=-0.5)),
        ("m2=1.0", dict(m2=1.0)),
        ("babs=0.10", dict(babs=0.10)),
    ]:
        kk = {**B, **kw, "eps": 0.03}
        rc = run_compact(**kk)
        k0 = {k_: v for k_, v in kk.items() if k_ != "eps"}
        rz = run_compact(eps=0.0, **k0)
        A, phi = diff_lockin(rc, rz, 0.03)
        print(f"    {tag:22s}: inphase={A * np.cos(phi):+8.4f} (phi={phi:+.3f})")
    print("[K''] fixed-ratio om=k/2 scaling (stabilized):")
    for kv in [0.6, 0.4, 0.3, 0.2]:
        rc = run_compact(eps=0.03, k=kv, om=kv / 2, **B)
        rz = run_compact(eps=0.0, k=kv, om=kv / 2, **B)
        A, phi = diff_lockin(rc, rz, 0.03)
        print(
            f"    k={kv:4.2f}: inphase={A * np.cos(phi):+8.4f}  /k^2={A * np.cos(phi) / kv**2:+.4f}"
        )


if __name__ == "__main__":
    battery_mms()
    print()
    battery_bit()
    print()
    battery_kprime()
    print()
    battery_stabilized()
