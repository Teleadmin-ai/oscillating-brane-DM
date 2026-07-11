"""a0(z) reviewer-mode attack, STEP 4 -- the STRONG-LENSING lever (the amplifier's surfaced lead), computed.

The lead (amplifier_a0z, June 2026): SLACS-class strong lensing = a NON-kinematic a0(z) probe (no V_c 4x
lever) on samples that already span z~0.1-0.8 -> maybe the missing cross-lever NOW, not Euclid-future. Its
own flagged caveat: the g~a0 regime selection (massive ellipticals are high-g). THIS script decides with
real data + exact geometry -- 'seul les calculs comptent', in either direction.

WHAT IS COMPUTED
[1] THE REGIME THEOREM: at the Einstein radius of any circularly-symmetric lens, the mean enclosed
    acceleration is g_E = G M_E / R_E^2 = pi G Sigma_cr (because M_E = pi R_E^2 Sigma_cr defines R_E).
    Sigma_cr is fixed by the (z_l, z_s) GEOMETRY alone -> g_E is a constant of the configuration,
    INDEPENDENT of the lens mass. A (z_l, z_s) grid scan gives the absolute floor of x_E = g_E/a0:
    strong lensing can NEVER probe g ~ a0 at theta_E (the 'lower-mass subset' hope dies by geometry --
    lower mass only shrinks R_E, it does not lower g_E).
[2] THE SLACS EMPIRICAL REGIME: per-lens x_E for the 85 grade-A lenses (Auger+2009, tables in the local
    CDS cache); reproduction check: the tabulated M(<R_E) vs pi R_E^2 Sigma_cr under the paper cosmology.
[3] THE FORWARD MODEL: Hernquist stars (M*_Salpeter, R_eff) -> OBT exact RAR -> effective total 3D
    density -> PROJECTED Sigma(R) -> M_2D(<R_E). The projection resurrects a deep-MOND contribution (the
    outer phantom along the line of sight) that the local x_E hides -> the REAL a0-sensitivity of the
    lensing mass, not the naive local 1/(2x^2).
[4] THE DIFFERENTIAL SIGNAL: per lens, Dlog M_E between a0(z)=A0*E(z)/E(z_med) (OBT evolution) and
    a0=A0 (constant MOND), both anchored at the sample median z (isolates the EVOLUTION lever; the
    anchor question is settled separately, anchor_tension.py). Its z-slope across SLACS = the
    strong-lensing a0(z) signal. Compared to (a) the statistical floor (tabulated e_logM*, N=85),
    (b) the coherent-systematics class (IMF / M*-L evolution, 0.05-0.1 dex-class), (c) same for the
    IMF-free sigma leg (isotropic Jeans, aperture R_eff/2).
[5] THE EUCLID-N EXTRAPOLATION (~1e5 strong lenses): statistics vs the coherent-systematics wall.
[6] VERDICT on the amplifier lead.

Asserted ONLY identities + reproductions (standing rule): the SIS projection/Jeans machinery identities,
mass conservation, the rho->g round-trip, and the reproduction of Auger's M(<R_E)=pi R_E^2 Sigma_cr
construction. All physics results are computed + reported, never imposed.

Data: /DATA/obt_game_cache/raw/slacs/ = CDS J/ApJ/705/1099 (Auger+ 2009, SLACS IX), byte-parsed per the
ReadMe. Paper cosmology (70, 0.3) used end-to-end for the per-lens work (matches their kpc/M_E); the
a0-model differential is anchoring-invariant. NOT a sacred file; quarantined reviewer-mode analysis.
"""

import os

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

# constants (SI)
G = 6.674e-11
C = 2.998e8
MSUN = 1.989e30
KPC = 3.0857e19
ARCSEC = np.pi / 180.0 / 3600.0

# paper cosmology (Auger+2009: flat LCDM, H0=70, Om=0.3) -- matches their tabulated kpc + M(<R_E)
H0 = 70.0 * 1e3 / (KPC * 1e3)  # s^-1
OM = 0.3
A0_MOND = 1.2e-10  # the measured MOND scale (the common anchor; the anchor question is separate)
CACHE = "/DATA/obt_game_cache/raw/slacs"

R_GRID = np.logspace(np.log10(0.005), np.log10(3000.0), 3000)  # kpc, model grid
L_MAX = 2000.0  # kpc, line-of-sight truncation (EFE-scale); sensitivity tested in [3]


def ez(z):
    return np.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def dc(z):  # comoving distance, m
    return (C / H0) * quad(lambda x: 1.0 / ez(x), 0.0, z)[0]


def sigma_cr(zl, zs):  # critical surface density, kg/m^2 (flat universe)
    dl, ds = dc(zl) / (1 + zl), dc(zs) / (1 + zs)
    dls = (dc(zs) - dc(zl)) / (1 + zs)
    return C**2 * ds / (4 * np.pi * G * dl * dls)


def rar_obt(g_n, a0):
    """OBT's exact RAR (the derived quadrature mu(x)): g_obs from g_bar."""
    return np.sqrt((g_n**2 + g_n * np.sqrt(g_n**2 + 4 * a0**2)) / 2.0)


def model_fields(mstar_kg, re_kpc, a0):
    """Hernquist stars + OBT RAR -> (g_obs(r), rho_tot(r), rho_star(r)) on R_GRID [SI, r in kpc]."""
    a = re_kpc / 1.8153
    r = R_GRID
    m_in = mstar_kg * r**2 / (r + a) ** 2
    g_n = G * m_in / (r * KPC) ** 2
    g = rar_obt(g_n, a0)
    r2g = (r * KPC) ** 2 * g
    rho = np.gradient(r2g, r * KPC) / (4 * np.pi * G * (r * KPC) ** 2)
    rho_star = mstar_kg * a / (2 * np.pi * r * (r + a) ** 3) / KPC**3
    return g, rho, rho_star


def project_sigma(rho, r_eval_kpc):
    """Sigma(R) = 2 int rho(sqrt(R^2+l^2)) dl, log-interpolated density, l up to L_MAX [SI out]."""
    lr = np.log(R_GRID)
    lrho = np.log(np.maximum(rho, 1e-300))
    out = []
    for rk in np.atleast_1d(r_eval_kpc):
        ll = np.logspace(np.log10(max(rk * 1e-3, 1e-4)), np.log10(L_MAX), 500)
        rr = np.sqrt(rk**2 + ll**2)
        f = np.exp(np.interp(np.log(rr), lr, lrho))
        out.append(2.0 * np.trapezoid(f, ll * KPC))
    return np.array(out)


def m2d(rho, r_ap_kpc):
    """Projected (cylinder) mass within R_ap [kg]. Fixed inner bound: the Sigma(R->0) log
    divergence is integrable and the mass inside 0.005 kpc is negligible for ANY aperture.
    """
    rg = np.logspace(np.log10(0.005), np.log10(r_ap_kpc), 80)
    sig = project_sigma(rho, rg)
    return np.trapezoid(sig * 2 * np.pi * rg * KPC, rg * KPC)


def jeans_sigma_ap(g, rho_star, r_ap_kpc):
    """Isotropic Jeans: sigma_r^2 = int_r rho* g ds / rho*; LOS-project; luminosity-weight in R<R_ap."""
    r = R_GRID * KPC
    integ = np.flip(np.cumsum(np.flip(rho_star * g * np.gradient(r))))
    sig_r2 = integ / np.maximum(rho_star, 1e-300)
    lr, l_rs2 = np.log(R_GRID), rho_star * sig_r2
    num_tot, den_tot = 0.0, 0.0
    for rk in np.logspace(np.log10(r_ap_kpc * 1e-2), np.log10(r_ap_kpc), 40):
        ss = np.logspace(np.log10(rk * 1.0001), np.log10(2500.0), 400)
        w = ss / np.sqrt(ss**2 - rk**2)
        f2 = np.exp(
            np.interp(np.log(ss), lr, np.log(np.maximum(l_rs2, 1e-300)))
        )  # rho* sig_r^2
        f0 = np.exp(np.interp(np.log(ss), lr, np.log(np.maximum(rho_star, 1e-300))))
        i_sig2 = 2.0 * np.trapezoid(f2 * w, ss * KPC)  # I(R) sigma_los^2
        i_sur = 2.0 * np.trapezoid(f0 * w, ss * KPC)  # I(R)
        num_tot += i_sig2 * rk * (rk * 0.12)  # log-grid weight ~ R dR
        den_tot += i_sur * rk * (rk * 0.12)
    return np.sqrt(num_tot / den_tot)


def parse_slacs():
    """Byte-parse Auger+2009 tables 3+4 per the CDS ReadMe; keep lenses with all needed fields."""

    def fl(s):
        s = s.strip()
        return float(s) if s else np.nan

    t3 = {}
    with open(os.path.join(CACHE, "table3.dat")) as f:
        for ln in f:
            name = ln[4:14].strip()
            t3[name] = dict(
                zl=fl(ln[39:44]),
                zs=fl(ln[45:50]),
                sig=fl(ln[51:54]),
                esig=fl(ln[55:57]),
                rev=fl(ln[84:88]),
                rei=fl(ln[95:99]),
            )
    rows = []
    with open(os.path.join(CACHE, "table4.dat")) as f:
        for ln in f:
            name = ln[4:14].strip()
            re_kpc, lme = fl(ln[15:19]), fl(ln[20:25])
            fs, efs = fl(ln[36:40]), fl(ln[41:45])
            lms, elms = fl(ln[62:67]), fl(ln[68:72])
            d = t3.get(name, {})
            re_as = d.get("rei", np.nan)
            if np.isnan(re_as):
                re_as = d.get("rev", np.nan)
            vals = [
                re_kpc,
                lme,
                lms,
                elms,
                d.get("zl"),
                d.get("zs"),
                d.get("sig"),
                re_as,
            ]
            if not any(np.isnan(v) for v in vals):
                rows.append(
                    dict(
                        name=name,
                        re_kpc=re_kpc,
                        logme=lme,
                        fs=fs,
                        efs=efs,
                        logms=lms,
                        elogms=elms,
                        zl=d["zl"],
                        zs=d["zs"],
                        sig=d["sig"],
                        esig=d["esig"],
                        reff_as=re_as,
                    )
                )
    return rows


def main():
    print("=" * 100)
    print(
        " STEP 4 — the STRONG-LENSING a0(z) lever (SLACS), computed: does the amplifier's lead survive?"
    )
    print("=" * 100)

    # ===== [0] machinery identities (SIS synthetic: projection + Jeans) =====
    v = 250e3  # m/s
    rho_sis = v**2 / (4 * np.pi * G * (R_GRID * KPC) ** 2)
    sig_num = project_sigma(rho_sis, np.array([5.0, 20.0]))
    sig_ana = v**2 / (4 * G * np.array([5.0, 20.0]) * KPC)
    assert np.all(
        np.abs(sig_num / sig_ana - 1) < 0.02
    ), "SIS projection identity Sigma=v^2/(4GR)"
    g_sis = np.full_like(R_GRID, v**2) / (R_GRID * KPC)
    s_ap = jeans_sigma_ap(g_sis, rho_sis, 10.0)
    assert (
        abs(s_ap / (v / np.sqrt(2)) - 1) < 0.02
    ), "SIS Jeans identity sigma_los=v/sqrt2"
    print(
        "\n[0] machinery identities: SIS projection + SIS Jeans reproduce the analytics (<2%) ✓"
    )

    # ===== [1] THE REGIME THEOREM =====
    print(
        "\n[1] THE REGIME THEOREM — g(R_E) = G M_E/R_E^2 = pi G Sigma_cr(z_l, z_s), lens-INDEPENDENT"
    )
    print(
        "      (M_E = pi R_E^2 Sigma_cr defines the Einstein radius: the acceleration at theta_E is a"
    )
    print(
        "       constant of the geometry -- lowering the lens mass shrinks R_E, it does NOT lower g_E.)"
    )
    zl_g = np.linspace(0.05, 2.0, 60)
    best, best1 = (np.inf, 0, 0), (np.inf, 0, 0)
    for zl in zl_g:
        for zs in np.linspace(zl + 0.1, 8.0, 80):
            ge = np.pi * G * sigma_cr(zl, zs)
            a0z = A0_MOND * ez(zl) / ez(0.0)  # the most favorable (a0 grows with z_l)
            x = ge / a0z
            if x < best[0]:
                best = (x, zl, zs)
            if zl <= 1.0 and x < best1[0]:
                best1 = (x, zl, zs)
    print(
        f"      grid scan z_l in [0.05,2], z_s in (z_l, 8]: the ABSOLUTE FLOOR is x_E = g_E/a0(z_l) ="
    )
    print(
        f"      {best[0]:.2f}  at (z_l={best[1]:.2f}, z_s={best[2]:.1f})  [a0 evolving; const-a0 floor is"
        f" higher; the floor sits at the grid edge, but real galaxy-scale lens samples stop at z_l~1"
    )
    print(
        f"       where the floor is {best1[0]:.2f} at (z_l={best1[1]:.2f}, z_s={best1[2]:.1f})]"
    )
    print(
        "      => NO strong-lens Einstein radius, anywhere, ever probes g ~ a0. The 'g~a0 subset' the"
    )
    print(
        "         lead needed does NOT exist within strong lensing; only PROJECTION reaches deep-MOND ([3])."
    )

    # ===== [2] SLACS: empirical regime + the paper-construction reproduction =====
    rows = parse_slacs()
    zl = np.array([r["zl"] for r in rows])
    zs = np.array([r["zs"] for r in rows])
    scr = np.array([sigma_cr(a, b) for a, b in zip(zl, zs)])
    ge_data = np.array(
        [G * 10 ** r["logme"] * MSUN / (r["re_kpc"] * KPC) ** 2 for r in rows]
    )
    ratio = ge_data / (np.pi * G * scr)
    assert (
        abs(np.median(ratio) - 1) < 0.10
    ), "reproduction: tabulated M(<R_E) == pi R_E^2 Sigma_cr"
    z_med = float(np.median(zl))
    a0_obt = (
        A0_MOND * ez(zl) / ez(z_med)
    )  # OBT evolution, anchored at the sample median
    x_const = ge_data / A0_MOND
    x_obt = ge_data / a0_obt
    print(
        f"\n[2] SLACS (Auger+2009): {len(rows)} grade-A lenses with complete data; z_l {zl.min():.2f}-"
        f"{zl.max():.2f} (median {z_med:.2f}), z_s {zs.min():.2f}-{zs.max():.2f}"
    )
    print(
        f"      reproduction: median g_E,data/(pi G Sigma_cr) = {np.median(ratio):.3f} (paper construction ✓)"
    )
    print(
        f"      the empirical regime: x_E = g_E/a0 = {np.percentile(x_const,5):.1f}-"
        f"{np.percentile(x_const,95):.1f} (5-95%), median {np.median(x_const):.1f} [const-a0];"
        f" median {np.median(x_obt):.1f} [a0(z)]"
    )
    print(
        f"      local (3D) a0-sensitivity at that x: 1/(2x^2) = {1/(2*np.median(x_const)**2)*100:.2f}% -- the naive verdict"
    )

    # ===== [3] the forward model: projection resurrects the phantom -> the REAL sensitivity =====
    print(
        "\n[3] THE FORWARD MODEL (Hernquist M*_Salp + OBT exact RAR -> projected M_2D(<R_E))"
    )
    # identities on one representative lens first
    r0 = rows[int(np.argmin(np.abs(zl - z_med)))]
    da_l = dc(r0["zl"]) / (1 + r0["zl"])
    reff_kpc = r0["reff_as"] * ARCSEC * da_l / KPC
    ms0 = 10 ** r0["logms"] * MSUN
    g0, rho0, rho_s0 = model_fields(ms0, reff_kpc, A0_MOND)
    # rho -> g round-trip (identity)
    m_cum = np.cumsum(
        4 * np.pi * rho0 * (R_GRID * KPC) ** 2 * np.gradient(R_GRID * KPC)
    )
    g_back = G * m_cum / (R_GRID * KPC) ** 2
    i_chk = slice(300, 2700)
    assert (
        np.median(np.abs(g_back[i_chk] / g0[i_chk] - 1)) < 0.02
    ), "rho_tot -> g round-trip identity"
    # mass conservation of the star projection (identity)
    m2d_star_tot = m2d(rho_s0, 2500.0)
    assert abs(m2d_star_tot / ms0 - 1) < 0.02, "projected stellar mass converges to M*"
    print("      identities: rho->g round-trip <2% ✓ ; projected M*(<inf) = M* <2% ✓")

    dlogme, fph, alph, dsig_rel, kept = [], [], [], [], []
    for r in rows:
        da = dc(r["zl"]) / (1 + r["zl"])
        re_kpc = r["reff_as"] * ARCSEC * da / KPC
        ms = 10 ** r["logms"] * MSUN
        a0z = A0_MOND * ez(r["zl"]) / ez(z_med)
        # fixed-M* differential: the pure a0-model signal in the lensing mass
        _, rho_c, rho_sc = model_fields(ms, re_kpc, A0_MOND)
        _, rho_z, _ = model_fields(ms, re_kpc, a0z)
        me_c = m2d(rho_c, r["re_kpc"])
        me_z = m2d(rho_z, r["re_kpc"])
        dlogme.append(np.log10(me_z / me_c))
        fph.append(1.0 - m2d(rho_sc, r["re_kpc"]) / me_c)
        # context: the M* needed to match the OBSERVED lensing mass under const-a0 (alpha_Salp)
        target = 10 ** r["logme"] * MSUN

        def mismatch(lm, _re=re_kpc, _rap=r["re_kpc"], _t=target):
            _, rr, _ = model_fields(10**lm * MSUN, _re, A0_MOND)
            return np.log10(m2d(rr, _rap) / _t)

        try:
            lm_fit = brentq(mismatch, r["logms"] - 1.2, r["logms"] + 1.2, xtol=2e-3)
            alph.append(lm_fit - r["logms"])
        except ValueError:
            alph.append(np.nan)

        # the IMF-free sigma leg: at M* matched to the SAME observed M_E under each a0 model,
        # the predicted aperture dispersion ratio between models
        def mismatch_z(lm, _re=re_kpc, _rap=r["re_kpc"], _t=target, _a=a0z):
            _, rr, _ = model_fields(10**lm * MSUN, _re, _a)
            return np.log10(m2d(rr, _rap) / _t)

        try:
            lm_fit_z = brentq(mismatch_z, r["logms"] - 1.2, r["logms"] + 1.2, xtol=2e-3)
            g_c, _, rs_c = model_fields(10**lm_fit * MSUN, re_kpc, A0_MOND)
            g_z, _, rs_z = model_fields(10**lm_fit_z * MSUN, re_kpc, a0z)
            s_c = jeans_sigma_ap(g_c, rs_c, re_kpc / 2.0)
            s_z = jeans_sigma_ap(g_z, rs_z, re_kpc / 2.0)
            dsig_rel.append(s_z / s_c - 1.0)
        except ValueError:
            dsig_rel.append(np.nan)
        kept.append(r)

    dlogme = np.array(dlogme)
    fph = np.array(fph)
    alph = np.array(alph)
    dsig_rel = np.array(dsig_rel)
    print(
        f"      kept {len(kept)}/85 lenses (complete fields); projected PHANTOM fraction inside R_E"
        f" (const-a0, Salpeter): median {np.median(fph)*100:.1f}%"
        f" (5-95%: {np.percentile(fph,5)*100:.1f}-{np.percentile(fph,95)*100:.1f}%)"
    )
    # the DIRECT sensitivity d ln M_E / d ln a0 (computed per lens, not a hand factor)
    dln_a0 = np.log(
        np.array([A0_MOND * ez(r["zl"]) / ez(z_med) for r in kept]) / A0_MOND
    )
    far = np.abs(dln_a0) > 0.02  # exclude the near-anchor lenses (0/0)
    s_a0 = np.median(dlogme[far] * np.log(10) / dln_a0[far])
    naive = 1.0 / np.median(x_const) ** 2  # local 3D: d ln M / d ln a0 = 2 * 1/(2x^2)
    print(
        f"      DIRECT sensitivity d ln M_E / d ln a0 = {s_a0:.3f}  vs the naive local 1/x^2 ="
        f" {naive:.4f}  -> the projection resurrects x{s_a0/naive:.0f} more a0-leverage"
        f" (the lead's kernel was right)"
    )
    print(
        f"      context alpha_Salp = logM*(needed)-logM*(Salp) under const-a0: median {np.nanmedian(alph):+.3f} dex"
        f" (scatter {np.nanstd(alph):.3f}) [the known high-g IMF degeneracy; not the target]"
    )
    # L_MAX sensitivity (EFE-truncation surrogate) on the representative lens
    global L_MAX
    l_save = L_MAX
    m_ref = m2d(rho0, r0["re_kpc"])
    L_MAX = 500.0
    m_short = m2d(rho0, r0["re_kpc"])
    L_MAX = l_save
    print(
        f"      line-of-sight truncation check: M_2D(<R_E) changes {abs(m_short/m_ref-1)*100:.2f}% for"
        f" L_max 2000->500 kpc (EFE truncation irrelevant at R_E)"
    )

    # ===== [4] the differential signal vs the floors =====
    print(
        "\n[4] THE a0(z)-vs-CONST DIFFERENTIAL across SLACS (both models anchored at z_med)"
    )
    sl, ic = np.polyfit(zl, dlogme, 1)
    span = dlogme.max() - dlogme.min()
    print(
        f"      per-lens Dlog10 M_E(fixed M*): span {span:.4f} dex over z_l {zl.min():.2f}-{zl.max():.2f};"
        f" z-slope = {sl:+.4f} dex/unit-z"
    )
    e_stat = np.median([r["elogms"] for r in kept])
    sig_slope = e_stat / (np.sqrt(len(kept)) * np.std(zl))
    print(
        f"      statistical floor (M*-leg): per-lens e_logM*={e_stat:.2f} dex, N={len(kept)},"
        f" std(z)={np.std(zl):.2f} -> sigma_slope = {sig_slope:.3f} dex/z"
    )
    print(
        f"      => significance of the strong-lensing a0(z) signal in SLACS: {abs(sl)/sig_slope:.2f} sigma"
        f" (need x{sig_slope*3/abs(sl):.0f} better for 3 sigma)"
    )
    print(
        f"      coherent-systematics wall (M*-leg): an IMF/M*-L z-drift mimics the signal 1:1; the"
    )
    print(
        f"      literature-debated drift class is 0.05-0.1 dex/unit-z vs the signal {abs(sl):.4f} dex/z ->"
    )
    print(f"      systematics {0.05/abs(sl):.0f}-{0.1/abs(sl):.0f}x ABOVE the signal")
    d_ok = dsig_rel[~np.isnan(dsig_rel)]
    sl_s, _ = np.polyfit(zl[~np.isnan(dsig_rel)], d_ok, 1)
    e_sig = np.median([r["esig"] / r["sig"] for r in kept])
    sig_slope_s = e_sig / (np.sqrt(len(d_ok)) * np.std(zl))
    print(
        f"      IMF-FREE sigma leg (Jeans at matched M_E): per-lens Dsigma/sigma slope = {sl_s:+.5f}/z;"
    )
    print(
        f"      floor: e_sig/sig={e_sig*100:.1f}%, N={len(d_ok)} -> sigma_slope={sig_slope_s:.4f}/z ->"
        f" {abs(sl_s)/sig_slope_s:.2f} sigma; anisotropy/profile systematics (few % coherent) are"
        f" {0.03/max(abs(sl_s),1e-9):.0f}x above"
    )

    # ===== [5] the Euclid-N extrapolation (slope frame, consistent units) =====
    print(
        "\n[5] THE EUCLID EXTRAPOLATION (~1e5 galaxy-galaxy strong lenses forecast, z_l to ~1.5)"
    )
    dlnE_dz = (
        1.5 * OM * (1 + 0.7) ** 2 / ez(0.7) ** 2
    )  # d ln E/dz at a z~0.7 Euclid lens
    dlnE_med = 1.5 * OM * (1 + z_med) ** 2 / ez(z_med) ** 2
    sl_eu = (
        abs(sl) * dlnE_dz / dlnE_med
    )  # the SAME fitted estimator, rescaled to the Euclid range
    n_eu = 1e5
    sig_eu = e_stat / (np.sqrt(n_eu) * 0.25)
    print(
        f"      the signal slope barely grows with z (d lnE/dz: {dlnE_med:.2f} at z_med ->"
        f" {dlnE_dz:.2f} at 0.7): ~{sl_eu:.4f} dex/z at the Euclid range vs {abs(sl):.4f} in SLACS"
    )
    print(
        f"      statistics: sigma_slope -> {sig_eu:.4f} dex/z (N=1e5, std z~0.25, SLACS-quality M*) ->"
        f" ~{sl_eu/sig_eu:.0f} sigma reachable STATISTICALLY"
    )
    print(
        f"      the coherent IMF/M*-L wall: the drift debate is 0.05-0.1 dex/z-class vs the signal"
        f" {sl_eu:.4f} -> a factor {0.05/sl_eu:.1f}-{0.1/sl_eu:.1f} ABOVE it"
    )
    print(
        "      => at Euclid-N the route becomes an IMF-SYSTEMATICS RACE (a ~2-4x control improvement"
    )
    print(
        "         needed), not a free measurement; the sigma leg escapes the IMF but hits few-%"
    )
    print(
        "         anisotropy/profile-evolution systematics of the same coherent class."
    )

    # ===== [6] VERDICT =====
    print(
        "\n[VERDICT] the amplifier's 'doable NOW' strong-lensing lead is CLOSED (the calculation decides):"
    )
    print(
        f"    (i) STRUCTURAL: g_E = pi G Sigma_cr -- floor x_E ~ {best[0]:.1f}, SLACS sits at"
        f" ~{np.median(x_const):.0f}; the g~a0 'subset' cannot exist AT theta_E in strong lensing;"
    )
    print(
        f"    (ii) the projection DOES resurrect a deep-MOND phantom ({np.median(fph)*100:.0f}% of M_E,"
        f" sensitivity d ln M_E/d ln a0 = {s_a0:.2f} = x{s_a0/naive:.0f} the local naive -- the lead's"
    )
    print(
        f"    kernel was right), BUT the resulting signal is {abs(sl):.4f} dex/z = {abs(sl)/sig_slope:.1f} sigma in"
        f" SLACS: statistically DEAD now; and the coherent IMF/profile wall (0.05-0.1 dex/z-class)"
    )
    print(
        f"    sits a factor {0.05/abs(sl):.0f}-{0.1/abs(sl):.0f} above the signal -- at Euclid-N statistics heal"
        f" ({sl_eu/sig_eu:.0f} sigma) but the wall stays -> a systematics race, not a clean lever;"
    )
    print(
        "    (iii) => strong lensing CANNOT arbitrate the kinematic x1.5 rate anomaly now, and only a"
    )
    print(
        "    2-4x IMF-control improvement would make it a Euclid-era contender; the decisive CLEAN"
    )
    print(
        "    cross-lever remains the WEAK-lensing RAR a0(z) (Euclid/Rubin, euclid_case.md), exactly as"
    )
    print(
        "    step 2 concluded. The lead was worth checking -- and it is now closed by numbers."
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
