"""CARD #22 RE-FIT ON LENSING MASSES — what the Weyl looks like under a bias-free calibration.

MODE CHERCHEUR, second half of the monster-[62b7f086] card path (Romain: 'vas y pour la note
alpha_NT et le re-fit #22 lentillage'). Card #22's global cored Weyl (f_W = 0.70, beta = 0.043)
was fit on X-COP HYDROSTATIC masses (probes.xcop_hier). The battery found the arc-core problem
lives in the mass ANCHOR. So: re-fit the SAME functional form on published joint strong+weak
LENSING masses and read off what moves.

A DECOMPOSITION LADDER — one change per rung, so nothing is confounded:
  (0) REPRODUCTION of the card: X-COP data, dynamical sinc W(r), the fit's 'simple' nu, a0=1.2e-10
      -> must return f_W = 0.70, beta = 0.043 (asserted).
  (1) + OBT's DERIVED law instead of the fit's nu. The card's fit used nu(y) = 1/2 + sqrt(1/4 + 1/y)
      (mu(x) = x/(1+x)); OBT DERIVES mu(x) = x/sqrt(1+x^2) (Gauss-Codazzi quadrature), i.e.
      g = sqrt((g_N^2 + g_N sqrt(g_N^2 + 4 a0^2))/2). At g ~ a0 the derived law boosts x1.27 where
      the fit's nu boosts x1.62 -> the derived law needs MORE Weyl. This rung prices that.
  (2) + a0(z) = cH(z)/2pi (OBT's derived scale) instead of the measured 1.2e-10.
  (3) LENSING data (Merten et al. 2015 SaWLens NFW fits, the same 9 CLASH clusters as the battery)
      with W = 1. THE PHOTON CHANNEL IS THE POINT: under ARA the sinc suppression is the TRACER's
      orbital response, so it applies to X-COP's gas dynamics but NOT to lensing (arcs_obt's own
      convention). Rungs (0)-(2) are dynamical; rung (3) is the lensing calibration -> THE NEW
      GLOBALS.
  Then: the Weyl is a mass distribution, so it must serve BOTH channels. Two closing tests --
  (a) the lensing-fitted globals predicted back onto the X-COP dynamics (with the alpha_NT-note
  mass ratio applied), and (b) the ARC TEST: do the re-fitted globals put the critical line on
  the observed giant arcs?

Baryons (declared, identical in both arms except where the data give them): BCG Hernquist
M* = 1.2e12, a = 30 kpc (the card's own choice); gas = measured MGAS(r) for X-COP, and for the
lensing arm the universal closure f_gas(R500) = 0.13 w.r.t. the LENSING mass (self-consistent with
the premise that lensing masses are the unbiased ones), bracketed 0.10-0.16.

Asserted ONLY identities + reproductions (rung 0 == the card's published (f_W, beta); the two nu
forms at their known g=a0 boosts). Everything else computed + reported. Quarantined; not sacred.
"""

import numpy as np
from astropy.io import fits
from scipy.optimize import least_squares

import alpha_nt_budget as NT
import arcs_battery as B
import arcs_obt as A

G, MSUN, KPC = A.G, A.MSUN, A.KPC
A0_LOCAL = 1.2e-10  # the card's fitted-convention MOND scale (measured value)
TGYR = 2.0
BCG_M, BCG_A = 1.2e12, 30.0  # the card's BCG (Hernquist)


def nu_card(y):
    """The 'simple' nu used by the card-#22 fit: mu(x) = x/(1+x)."""
    return 0.5 + np.sqrt(0.25 + 1.0 / np.clip(y, 1e-8, None))


def g_law(gbar, a0eff, derived):
    """MOND-sector g from g_bar at an effective (W-suppressed) a0."""
    if derived:
        return A.rar_obt(gbar, a0eff)
    return nu_card(gbar / a0eff) * gbar


def weyl_g(r_m, R5, M5, fW, beta):
    x = r_m / (beta * R5)
    m = (x - np.arctan(x)) / (1.0 / beta - np.arctan(1.0 / beta))
    return fW * G * M5 * m / r_m**2


def load_xcop():
    """X-COP bins exactly as probes.xcop_hier builds them (the card-#22 fit data)."""
    rows = []
    for cl, (r500, m500) in NT.XCOP.items():
        t = fits.open(f"/DATA/obt_game_cache/raw/xcop/{cl}/{cl}_fgas_profile.fits")[
            1
        ].data
        r_kpc = np.array(t["RADIUS"], float)
        if r_kpc.max() < 50:
            r_kpc *= 1000.0
        M = np.array(t["M_NFW"], float)
        Mg = np.array(t["MGAS"], float)
        sc = m500 * 1e14 / np.interp(r500, r_kpc, M)
        M, Mg = M * sc, Mg * sc
        eM = sc * (np.array(t["M_NFW_HI"], float) - np.array(t["M_NFW_LO"], float)) / 2
        sel = (r_kpc > 15) & (r_kpc < 1.05 * r500) & (M > 0) & (Mg > 0)
        idx = np.where(sel)[0][::8]
        r_m = r_kpc[idx] * KPC
        Mstar = BCG_M * (r_kpc[idx] / (r_kpc[idx] + BCG_A)) ** 2
        gobs = G * M[idx] * MSUN / r_m**2
        gbar = G * (Mg[idx] + Mstar) * MSUN / r_m**2
        sg = np.sqrt((eM[idx] / np.clip(M[idx], 1, None)) ** 2 + 0.05**2)
        td = 2 * np.pi * np.sqrt(r_m**3 / (G * M[idx] * MSUN)) / 3.156e16
        W = np.abs(np.sinc(td / TGYR))
        z = NT.XCOP_Z[cl]
        for j in range(len(idx)):
            rows.append(
                (
                    gobs[j],
                    gbar[j],
                    sg[j],
                    W[j],
                    r_m[j],
                    r500 * KPC,
                    m500 * 1e14 * MSUN,
                    z,
                )
            )
    return np.array(rows)


def load_lensing(fgas500=0.13, npts=12):
    """CLASH lensing profiles from Merten+15 SaWLens NFW fits (M200c, c200c), 30 kpc -> R500.
    W = 1 (photon channel). Baryons: BCG + universal gas closure w.r.t. the LENSING mass.
    """
    rows = []
    for name, zl, te, m2d, kt in B.BATTERY:
        key = name.split()[0]
        m500h, m200h, c200 = NT.MERTEN[key]
        cl = dict(
            name=key,
            z_l=zl,
            z_s=2.0,
            c200=c200,
            m200=m200h * 1e15 / NT.H_MERTEN,
            mstar=BCG_M,
            astar=BCG_A,
            r_arc_as=te,
        )
        h = A.Halo(cl)
        r_kpc = np.logspace(np.log10(30.0), np.log10(h.r500), npts)
        r_m = r_kpc * KPC
        M = h.m_nfw(r_kpc) / MSUN
        fg = np.clip(fgas500 * (r_kpc / h.r500) ** 0.4, 0.04, 0.16)
        Mg = fg * M
        Mstar = BCG_M * (r_kpc / (r_kpc + BCG_A)) ** 2
        gobs = G * M * MSUN / r_m**2
        gbar = G * (Mg + Mstar) * MSUN / r_m**2
        sg = np.full(
            npts, np.hypot(0.11, 0.10)
        )  # ~11% published M500 error + 10% shape floor
        for j in range(npts):
            rows.append(
                (gobs[j], gbar[j], sg[j], 1.0, r_m[j], h.r500 * KPC, h.m500, zl)
            )
    return np.array(rows)


def fit(data, derived, a0_derived, label="", quiet=False):
    gobs, gbar, sg, W, r_m, R5, M5, z = data.T
    lny = np.log(gobs)
    a0 = (
        A.C * A.H0 * np.array([A.ez(zz) for zz in z]) / (2 * np.pi)
        if a0_derived
        else A0_LOCAL * np.ones_like(z)
    )

    def model(th):
        fW, lb = th
        return np.log(
            g_law(gbar, np.clip(W, 1e-3, None) * a0, derived)
            + weyl_g(r_m, R5, M5, fW, np.exp(lb))
        )

    best = None
    for f0 in (0.3, 0.5, 0.7, 0.9):
        for b0 in (-3.5, -2.0, -1.0):
            o = least_squares(
                lambda th: (model(th) - lny) / sg,
                x0=[f0, b0],
                bounds=([0.0, -4.6], [1.6, 0.7]),
            )
            c2 = float((o.fun**2).sum())
            if best is None or c2 < best[0]:
                best = (c2, o.x)
    fW, beta = best[1][0], float(np.exp(best[1][1]))
    res = model(best[1]) - lny
    rms = float(np.sqrt(np.mean(res**2)) / np.log(10))
    if not quiet:
        print(
            f"    {label:56s} f_W = {fW:5.2f}   r_c = {beta:.3f} R500   "
            f"chi2/N = {best[0]/len(data):5.2f}   rms {rms:.3f} dex"
        )
    return fW, beta, best[0] / len(data)


def main():
    print("=" * 104)
    print(
        " === MODE CHERCHEUR ===  CARD #22 RE-FIT ON LENSING MASSES  (monster [62b7f086], part 2)"
    )
    print("=" * 104)

    # law identity: the two interpolations' boost at g_N = a0
    b_card = nu_card(1.0)
    b_der = A.rar_obt(1.0, 1.0)
    assert abs(b_card - (0.5 + np.sqrt(1.25))) < 1e-12
    assert abs(b_der - np.sqrt((1 + np.sqrt(5)) / 2)) < 1e-12
    print(
        f"\n[law] boost at g_N = a0:  card-fit nu = {b_card:.3f} x   vs   OBT-derived (Gauss-Codazzi)"
        f" = {b_der:.3f} x  -> the derived law is weaker by {b_card/b_der:.2f}x"
    )

    xc = load_xcop()
    ln = load_lensing()
    print(
        f"\n[data] X-COP dynamical bins: {len(xc)} (12 clusters, r>15 kpc, 1/8 thinning)"
    )
    print(
        f"       CLASH lensing points : {len(ln)} (9 clusters, 30 kpc -> R500, Merten+15 SaWLens)"
    )

    print("\n[THE LADDER] one change per rung")
    f0, b0, _ = fit(
        xc,
        derived=False,
        a0_derived=False,
        label="(0) card reproduction: X-COP, W(r), fit-nu, a0=1.2e-10",
    )
    assert (
        abs(f0 - 0.70) < 0.02 and abs(b0 - 0.043) < 0.004
    ), "rung 0 must reproduce card #22"
    f1, b1, _ = fit(
        xc,
        derived=True,
        a0_derived=False,
        label="(1) + OBT's DERIVED mu(x) (Gauss-Codazzi quadrature)",
    )
    f2, b2, _ = fit(
        xc,
        derived=True,
        a0_derived=True,
        label="(2) + a0(z) = cH(z)/2pi instead of 1.2e-10",
    )
    f3, b3, _ = fit(
        ln,
        derived=True,
        a0_derived=True,
        label="(3) LENSING masses + W=1 (photon channel)  <== NEW GLOBALS",
    )

    print(
        "    [note] the X-COP rungs' chi2/N is large because the card's calibrated intrinsic scatter"
    )
    print(
        "     (sigma_int = 0.327 in ln = 0.142 dex, the hydrostatic-bias/asphericity term) is NOT added"
    )
    print(
        "     here; it changes the chi2, not the best fit -- rung (0) reproduces the card exactly."
    )

    print(
        "\n[WHAT MOVED — absolute Weyl mass at R500 is M_W = f_W x M500, so BOTH factors count]"
    )
    m5_x = np.median(xc[:, 6]) / MSUN
    m5_l = np.median(ln[:, 6]) / MSUN
    print(
        f"    median M500: X-COP (hydrostatic) {m5_x:.2e}   CLASH (lensing) {m5_l:.2e}"
    )
    print(
        f"    f_W: {f0:.2f} (card) -> {f1:.2f} (derived law) -> {f2:.2f} (a0(z)) -> {f3:.2f} (lensing+W=1)"
    )
    print(
        f"    r_c: {b0:.3f} -> {b1:.3f} -> {b2:.3f} -> {b3:.3f} R500"
        f"   (physical core {b0*np.median(xc[:,5])/KPC:.0f} kpc -> {b3*np.median(ln[:,5])/KPC:.0f} kpc)"
    )
    print(
        "    Weyl amplitude at a FIXED cluster (f_W x M500), lensing vs card, at the alpha_NT-note"
    )
    print(
        f"    mass ratio 1.34: x{f3/f0*1.34:.2f}"
        "   [my pre-computation hand-waved 'x1.7' in the battery commit -- the calculation says"
        f" x{f3/f0*1.34:.2f}: that hand-wave is corrected]"
    )

    print("\n[SENSITIVITY of the new globals]")
    for fg in (0.10, 0.16):
        fw, bb, _ = fit(load_lensing(fgas500=fg), True, True, quiet=True)
        print(f"    f_gas(R500) = {fg:.2f} -> f_W = {fw:.2f}, r_c = {bb:.3f} R500")
    xcw = xc.copy()
    xcw[:, 3] = 1.0
    fwx, bbx, _ = fit(xcw, True, True, quiet=True)
    print(
        f"    channel test: X-COP data re-fit with W=1 (i.e. the sinc switched off) -> f_W = {fwx:.2f},"
        f" r_c = {bbx:.3f} -> the W channel alone moves f_W by {abs(fwx-f2):.2f}"
    )

    print(
        "\n[CLOSING TEST (a)] the LENSING-fitted Weyl predicted back onto X-COP dynamics"
    )
    gobs, gbar, sg, W, r_m, R5, M5, z = xc.T
    a0z = A.C * A.H0 * np.array([A.ez(zz) for zz in z]) / (2 * np.pi)
    td0 = (
        2 * np.pi * np.sqrt(r_m**3 / (gobs * r_m**2)) / 3.156e16
    )  # t_dyn from the measured g
    for bias, tag in (
        (1.0, "X-COP masses as published"),
        (1.34, "X-COP masses x1.34 (alpha_NT note)"),
    ):
        # heavier cluster -> shorter dynamical time -> LESS sinc suppression: W moves with the bias
        Wb = np.abs(np.sinc(td0 / np.sqrt(bias) / TGYR))
        pred = g_law(gbar, np.clip(Wb, 1e-3, None) * a0z, True) + weyl_g(
            r_m, R5 * bias ** (1 / 3), M5 * bias, f3, b3
        )
        r = np.log10(pred / (gobs * bias))
        print(
            f"    {tag:36s}: median residual {np.median(r):+.3f} dex, rms {np.std(r):.3f} dex"
            f"   (median W {np.median(Wb):.2f})"
        )

    print(
        "\n[CLOSING TEST (b)] THE ARC TEST — do the re-fitted globals make the giant arcs?"
    )
    print(
        f"    {'cluster':11s} {'th_E':>5s} {'kappa_OBT(card)':>16s} {'kappa_OBT(new)':>15s}"
        f" {'kappa_NFW(Merten)':>18s} {'OBT-proper':>14s}"
    )
    kn, ko, kf, kbcg = [], [], [], []
    for name, zl, te, m2d, kt in B.BATTERY:
        key = name.split()[0]
        m500h, m200h, c200 = NT.MERTEN[key]
        cl = dict(
            name=key,
            z_l=zl,
            z_s=2.0,
            c200=c200,
            m200=m200h * 1e15 / NT.H_MERTEN,
            mstar=BCG_M,
            astar=BCG_A,
            r_arc_as=te,
        )
        h = A.Halo(cl)
        scr = A.sigma_cr(zl, 2.0)
        kpas = A.dc(zl) / (1 + zl) * A.ARCSEC / KPC
        r_e = te * kpas
        a0 = A.C * A.H0 * A.ez(zl) / (2 * np.pi)

        def kap(fW, beta, bm=BCG_M, ba=BCG_A):
            gb = (
                lambda r: G
                * (
                    bm
                    * MSUN
                    * np.asarray(r, float) ** 2
                    / (np.asarray(r, float) + ba) ** 2
                    + np.clip(0.13 * (np.asarray(r, float) / h.r500) ** 0.4, 0.04, 0.16)
                    * h.m_nfw(r)
                )
                / (np.asarray(r, float) * KPC) ** 2
            )
            gt = lambda r: A.rar_obt(gb(r), a0) + weyl_g(
                np.asarray(r, float) * KPC, h.r500 * KPC, h.m500, fW, beta
            )
            return A.sigbar_of(A.rho_from_mass(A.m_eff(gt)), r_e) / scr

        k_card, k_new = kap(f0, b0), kap(f3, b3)
        k_nfw = h.sigbar_nfw(r_e) / scr
        kbcg.append([kap(f3, b3, bm, ba) for bm, ba in ((5e11, 10.0), (3e12, 50.0))])
        kn.append(k_nfw), ko.append(k_card), kf.append(k_new)
        print(
            f"    {key:11s} {te:4.1f}'' {k_card:16.2f} {k_new:15.2f} {k_nfw:18.2f}"
            f" {k_nfw/k_new:14.2f}"
        )
    kn, ko, kf = np.array(kn), np.array(ko), np.array(kf)
    print(
        f"    medians: card {np.median(ko):.2f}   re-fitted {np.median(kf):.2f}   Merten NFW"
        f" {np.median(kn):.2f}   OBT-proper {np.median(kn/kf):.2f}   (the arc requires kappa ~ 1)"
    )
    kb = np.array(kbcg)
    print(
        f"    BCG sensitivity of kappa_OBT(new): M*=5e11/a=10kpc -> {np.median(kb[:,0]):.2f},"
        f" M*=1.2e12/30kpc -> {np.median(kf):.2f}, M*=3e12/50kpc -> {np.median(kb[:,1]):.2f}"
        f"  (OBT-proper {np.median(kn/kb[:,0]):.2f} / {np.median(kn/kf):.2f} /"
        f" {np.median(kn/kb[:,1]):.2f})"
    )

    print(
        "\n    *** THE FINDING THAT MATTERS *** the PUBLISHED LENSING NFW, evaluated spherically,"
    )
    print(
        f"    reaches only kappa = {np.median(kn):.2f} at the observed effective Einstein radii --"
        f" a x{1/np.median(kn):.2f} deficit"
    )
    print(
        "    for the STANDARD model on lensing-derived masses. That is the known ellipticity +"
    )
    print(
        "    substructure boost that the 2D lens models (which measure theta_E) contain and no"
    )
    print(
        "    spherical model can. EXTERNAL CORROBORATION (declared, Meneghetti et al. 2007): the"
    )
    print(
        "    lensing cross-section budget is ~40% ellipticity, ~30% substructure, ~10% asymmetries,"
    )
    print(
        "    and spherical modelling systematically misestimates the inner slope (~0.4 in the mean);"
    )
    print(
        "    spherically symmetric halos 'fail to reproduce the lensing signal'. It is NOT an OBT"
    )
    print("    effect. Against that same-geometry reference the")
    print(
        f"    OBT-proper ratio is {np.median(kn/kf):.2f} (range {np.min(kn/kf):.2f}-{np.max(kn/kf):.2f})"
        " = NO OBT-proper deficit at the arcs."
    )

    # ------------------------------------------------- post-mortem: where the monster's number came from
    print(
        "\n[POST-MORTEM] the monster's x1.40-1.56 'OBT-proper' deficit came from ONE contested mass model"
    )
    zl, te = 0.313, 17.1
    scr = A.sigma_cr(zl, 2.0)
    r_e = te * A.dc(zl) / (1 + zl) * A.ARCSEC / KPC
    for tag, m200, c200 in (
        ("Donnarumma+09 Chandra X-ray (used by arcs_obt)", 4.4e14, 9.6),
        ("Merten+15 SaWLens lensing   (used here)      ", 1.04e15 / NT.H_MERTEN, 3.1),
    ):
        hh = A.Halo(
            dict(
                name="MS2137",
                z_l=zl,
                z_s=2.0,
                c200=c200,
                m200=m200,
                mstar=BCG_M,
                astar=BCG_A,
                r_arc_as=te,
            )
        )
        print(
            f"    {tag}: M200 = {m200:.2e}, c = {c200:.1f} -> kappa_NFW(arc) ="
            f" {hh.sigbar_nfw(r_e)/scr:.2f}"
        )
    print(
        "    the two published mass models of the SAME cluster differ by"
        f" x{(1.04e15/NT.H_MERTEN)/4.4e14:.1f} in M200 --"
    )
    print(
        "    the high-concentration X-ray model puts the critical line ON the arc, the lensing model"
    )
    print(
        "    does not. arcs_obt measured OBT against the FORMER; that choice, not OBT, produced the"
    )
    print("    x1.56 'OBT-proper' deficit that flipped the verdict to MONSTER.")

    print("\n[VERDICT — the monster is DOWNGRADED by its own follow-up]")
    print(
        "    * THE NEW GLOBALS (lensing-calibrated, OBT's derived law, photon channel):"
        f"  f_W = {f3:.2f},  r_c = {b3:.3f} R500"
    )
    print(
        f"      (physical core ~{b3*np.median(ln[:,5])/KPC:.0f} kpc). Absolute Weyl amplitude at a fixed"
    )
    print(
        f"      cluster: x{f3/f0*1.34:.2f} vs the card -- NOT the x1.7 I hand-waved in the battery commit."
    )
    print(
        f"    * The ladder splits cleanly: derived mu(x) {f1-f0:+.2f}, a0(z) {f2-f1:+.2f},"
    )
    print(
        f"      lensing+photon-channel {f3-f2:+.2f} in f_W. The single biggest term is the ARA CHANNEL"
    )
    print(
        "      (W=1 for photons restores the MOND boost the sinc had suppressed), not the mass scale."
    )
    print(
        "    * ARC TEST, THE HEADLINE: the SPHERICAL published-lensing NFW itself reaches only"
        f" kappa = {np.median(kn):.2f}"
    )
    print(
        "      at the observed effective Einstein radii. Neither model makes the arcs in spherical"
    )
    print(
        f"      symmetry -- the missing x{1/np.median(kn):.2f} is the ellipticity/substructure boost that the 2D"
    )
    print(
        "      models measuring theta_E contain by construction. At the SAME calibration and the SAME"
    )
    print(
        f"      geometry, OBT-proper = {np.median(kn/kf):.2f}: NO OBT-proper deficit."
    )
    print(
        "    * SO: the monster's premise ('the global cored Weyl saturates arc convergence and cannot"
    )
    print(
        "      make giant arcs') is NOT established. It was measured against a per-object"
    )
    print(
        "      high-concentration X-ray mass model on one cluster; on published lensing masses the"
    )
    print(
        "      standard model shows the same deficit. THE MONSTER IS DOWNGRADED, NOT PROMOTED."
    )
    print(
        "    * WHAT SURVIVES, and is worth keeping: (i) the hydrostatic-vs-lensing mass gap x1.34"
    )
    print(
        "      (alpha_nt_budget.py) -- real, external, unresolved, and NOT ours to arbitrate;"
    )
    print(
        "      (ii) an OBT-INTERNAL channel tension: a single global Weyl calibrated on the photon"
    )
    print(
        "      channel under-predicts the dynamical channel by ~0.1-0.2 dex (closing test (a)) --"
    )
    print(
        "      that is the lensing-vs-dynamics SCISSOR, measured here on clusters, and it is an"
    )
    print(
        "      OBT question, not a debunk of anyone. Out of the game, into the reviewer ledger."
    )
    print(
        "    * Scope: the lensing 'data' are published NFW fits (Merten Table 7), not the raw"
    )
    print(
        "      non-parametric reconstruction; gas is a universal-closure model, not measured; both"
    )
    print(
        "      arms are spherical; the samples differ (X-COP z~0.06 vs CLASH z~0.2-0.4)."
    )
    print("=" * 104)


if __name__ == "__main__":
    main()
