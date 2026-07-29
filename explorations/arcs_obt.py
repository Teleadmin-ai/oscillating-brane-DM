"""GIANT-ARC CLUSTERS vs OBT's two-scale law — card #22 CONFIRMED or a MONSTER? (2-lens test)

Romain, after abell370_obt.py: 'ca sent le monstre. tu as une autre carte dedans ou tu confortes la
22? surtout en obtenant la meme veracite de calcul avec une autre lentille gravitationnelle.'

THE DISCRIMINANT: on A370 (extreme bimodal merger) the total convergence deficit x1.54 decomposed as
x1.34 SHARED sphericity (the WL-NFW reference carries it too) x1.15 OBT-proper. A RELAXED arc
cluster removes the sphericity refuge: there the standard NFW places the critical line ON the arc
(kappa_NFW(R_arc) ~ 1), so whatever deficit OBT shows is OBT-PROPER. Two clean outcomes, declared:
  * OBT-proper deficit stays ~ x1.1-1.2  -> card #22 CONFORTED (A370's residual was geometry);
  * OBT-proper deficit blows up (>~x1.4) -> a MONSTER for the registry: 'strong-lensing cores vs
    the GLOBAL cored Weyl' (the card's own central-concentration caveat, now quantified as a real
    failure mode on the cleanest possible terrain).

THE SECOND LENS: MS 2137.3-2353 — THE textbook relaxed arc cluster (cool-core, circular isophotes;
the first radial arc ever found; Fort's school again: Gavazzi & Fort 2003). Web-verified anchors:
z_l = 0.313; tangential arc at ~15'' and radial arc at ~5'' from the BCG, sources z = 1.501/1.502
(Donnarumma et al. 2009, arXiv:0902.4051 — X-ray Chandra NFW M200 = 4.4 +/- 0.3 e14 Msun, no high
concentration, X-ray/SL RECONCILED: the spherical NFW genuinely fits this lens). Historical bonus:
MS2137 was already used to constrain MOND (Sanders-class 2002 paper) — pure MOND fails it in the
literature too. c200 is bracketed [6-10, central 8] (declared; the reconciliation statement pins
the NFW reference near kappa(R_arc)=1 regardless).

SAME LAW, SAME CODE PATH AS A370 (zero per-object freedom): g_tot = rar_OBT(g_bar; a0(z_l)) + g_Weyl
with the card-#22 GLOBAL Weyl (f_W = 0.70, beta = r_c/R500 = 0.043; M_W = f_W M500 (x - atan x)/
(x5 - atan x5)), lensing W = 1 (photons), a0(z_l) = cH(z_l)/2pi. Baryons: declared literature-class
brackets per cluster (BCG(+ICL) Hernquist + rising cumulative gas fraction).

Asserted ONLY identities + reproductions (SIS projection; NFW Sigma-bar numeric == analytic;
M200 recovery; and the A370 numbers of abell370_obt.py reproduced by this generalized code path).
All physics computed + reported. Quarantined exploration; NOT a sacred file, not in the PDF.
CARD/MONSTER decision = Romain's (the game gate); this script supplies the computed answer.
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

G, C, MSUN, KPC = 6.674e-11, 2.998e8, 1.989e30, 3.0857e19
ARCSEC = np.pi / 180 / 3600
H0 = 67.4 * 1e3 / (KPC * 1e3)
OM = 0.315
H_LITTLE = 0.674
FW, BETA = 0.70, 0.043  # card #22 GLOBAL Weyl parameters (xcop_hier best fit)
R_GRID = np.logspace(np.log10(1.0), np.log10(8000.0), 3000)  # kpc

CLUSTERS = [
    dict(
        name="Abell 370 (bimodal MERGER — the founding arc)",
        z_l=0.375,
        z_s=0.725,
        m200=1.54e15 / H_LITTLE,
        c200=5.27,
        c_brk=(5.27, 5.27),
        r_arc_as=25.0,
        r_arc_brk=(20.0, 30.0),
        mstar=4e12,
        astar=50.0,
        ms_brk=(2e12, 8e12),
        note="Umetsu+22 WL+Chandra; LOS elongation = their headline (sphericity deficit expected)",
        relaxed=False,
    ),
    dict(
        name="MS 2137-2353 (RELAXED cool-core — the discriminant)",
        z_l=0.313,
        z_s=1.501,
        m200=4.4e14,
        c200=8.0,
        c_brk=(6.0, 10.0),
        r_arc_as=15.0,
        r_arc_brk=(14.0, 16.0),
        mstar=5e11,
        astar=10.0,
        ms_brk=(2.5e11, 1e12),
        note="Donnarumma+09 Chandra NFW (X-ray/SL reconciled); first radial arc; Gavazzi & Fort 2003",
        relaxed=True,
    ),
]


def ez(z):
    return np.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def dc(z):
    return (C / H0) * quad(lambda x: 1 / ez(x), 0, z)[0]


def sigma_cr(zl, zs):
    dl, ds = dc(zl) / (1 + zl), dc(zs) / (1 + zs)
    dls = (dc(zs) - dc(zl)) / (1 + zs)
    return C**2 * ds / (4 * np.pi * G * dl * dls)


def rar_obt(g_n, a0):
    return np.sqrt((g_n**2 + g_n * np.sqrt(g_n**2 + 4 * a0**2)) / 2)


class Halo:
    """Per-cluster geometry + mass components (spherical; radii in kpc, masses in kg)."""

    def __init__(self, cl, c200=None, mstar=None, fgas_fac=1.0):
        self.cl = cl
        self.c = cl["c200"] if c200 is None else c200
        self.mstar = (cl["mstar"] if mstar is None else mstar) * MSUN
        self.fgf = fgas_fac
        self.m200 = cl["m200"] * MSUN
        rho_cz = 3 * (H0 * ez(cl["z_l"])) ** 2 / (8 * np.pi * G)
        self.r200 = (self.m200 / (4 / 3 * np.pi * 200 * rho_cz)) ** (1 / 3) / KPC
        self.rs = self.r200 / self.c
        self.mu = np.log(1 + self.c) - self.c / (1 + self.c)
        self.r500 = brentq(
            lambda r: self.m_nfw(r) - 4 / 3 * np.pi * 500 * rho_cz * (r * KPC) ** 3,
            50,
            4000,
        )
        self.m500 = float(self.m_nfw(self.r500))
        self.rtr = (
            2 * self.r500
        )  # declared Weyl truncation (sensitivity shown for A370 already)

    def m_nfw(self, r_kpc):
        x = np.asarray(r_kpc, float) / self.rs
        return self.m200 * (np.log(1 + x) - x / (1 + x)) / self.mu

    def sigbar_nfw(self, R_kpc):
        x = R_kpc / self.rs
        rho_s = self.m200 / (4 * np.pi * (self.rs * KPC) ** 3 * self.mu)
        if abs(x - 1) < 1e-8:
            h = 1 + np.log(0.5)
        elif x < 1:
            h = np.arccosh(1 / x) / np.sqrt(1 - x**2) + np.log(x / 2)
        else:
            h = np.arccos(1 / x) / np.sqrt(x**2 - 1) + np.log(x / 2)
        return 4 * rho_s * (self.rs * KPC) * h / x**2

    def m_bar(self, r_kpc):
        r = np.asarray(r_kpc, float)
        fg = np.clip(self.fgf * 0.13 * (r / self.r500) ** 0.4, 0.04, 0.14 * self.fgf)
        return self.mstar * r**2 / (r + self.cl["astar"]) ** 2 + fg * self.m_nfw(r)

    def m_weyl(self, r_kpc):
        r = np.minimum(np.asarray(r_kpc, float), self.rtr)
        x = r / (BETA * self.r500)
        x5 = 1.0 / BETA
        return FW * self.m500 * (x - np.arctan(x)) / (x5 - np.arctan(x5))


def rho_from_mass(m_func):
    m = m_func(R_GRID)
    rho = np.gradient(m, R_GRID * KPC) / (4 * np.pi * (R_GRID * KPC) ** 2)
    return lambda r: np.interp(np.asarray(r, float), R_GRID, np.maximum(rho, 0.0))


def sigbar_of(rho_f, r_proj_kpc, lmax_kpc=8000.0):
    rg = np.logspace(np.log10(0.05), np.log10(r_proj_kpc), 90)
    sig = []
    for rk in rg:
        ll = np.logspace(np.log10(max(rk * 1e-3, 0.05)), np.log10(lmax_kpc), 400)
        sig.append(2 * np.trapezoid(rho_f(np.sqrt(rk**2 + ll**2)), ll * KPC))
    return np.trapezoid(np.array(sig) * 2 * np.pi * rg * KPC, rg * KPC) / (
        np.pi * (r_proj_kpc * KPC) ** 2
    )


def crit_radius(rho_f, scr, lo=2.0, hi=900.0):
    try:
        return brentq(lambda R: sigbar_of(rho_f, R) - scr, lo, hi, xtol=0.3)
    except ValueError:
        return np.nan


def m_eff(g_func):
    return (
        lambda r: g_func(np.asarray(r, float)) * (np.asarray(r, float) * KPC) ** 2 / G
    )


def analyze(cl, quiet=False, c200=None, mstar=None, fgas_fac=1.0):
    h = Halo(cl, c200=c200, mstar=mstar, fgas_fac=fgas_fac)
    scr = sigma_cr(cl["z_l"], cl["z_s"])
    da = dc(cl["z_l"]) / (1 + cl["z_l"])
    kpas = da * ARCSEC / KPC
    r_arc = cl["r_arc_as"] * kpas
    a0z = C * H0 * ez(cl["z_l"]) / (2 * np.pi)
    g_bar = lambda r: G * h.m_bar(r) / (np.asarray(r, float) * KPC) ** 2
    laws = {
        "Newton": lambda r: g_bar(r),
        "MOND": lambda r: rar_obt(g_bar(r), a0z),
        "OBT": lambda r: rar_obt(g_bar(r), a0z)
        + G * h.m_weyl(r) / (np.asarray(r, float) * KPC) ** 2,
    }
    out = dict(h=h, scr=scr, kpas=kpas, r_arc=r_arc, a0z=a0z)
    for k, gf in laws.items():
        rho = rho_from_mass(m_eff(gf))
        out[f"k_{k}"] = sigbar_of(rho, r_arc) / scr
        out[f"re_{k}"] = crit_radius(rho, scr)
    out["k_NFW"] = h.sigbar_nfw(r_arc) / scr
    out["re_NFW"] = brentq(lambda R: h.sigbar_nfw(R) - scr, 2, 900)
    if not quiet:
        me = np.pi * scr * (r_arc * KPC) ** 2
        print(f"\n### {cl['name']}")
        print(f"    [{cl['note']}]")
        print(
            f"    z_l={cl['z_l']}, z_s={cl['z_s']}; 1''={kpas:.2f} kpc; arc at {cl['r_arc_as']:.0f}''"
            f" = {r_arc:.0f} kpc; Sigma_cr={scr:.2f} kg/m^2; a0(z_l)={a0z:.2e} ({a0z/(C*H0/2/np.pi):.2f}x local)"
        )
        print(
            f"    R500={h.r500:.0f} kpc, M500={h.m500/MSUN:.2e}; M_E(arc)=pi Sig_cr R^2 = {me/MSUN:.2e} Msun"
        )
        print(f"    {'law':8s} {'kappa(R_arc)':>13s} {'R_E':>16s}")
        for k in ("Newton", "MOND", "OBT"):
            re = out[f"re_{k}"]
            re_s = f"{re:5.0f} kpc={re/kpas:5.1f}''" if re == re else "   none        "
            print(f"    {k:8s} {out[f'k_{k}']:13.2f} {re_s:>16s}")
        print(
            f"    {'NFW-ref':8s} {out['k_NFW']:13.2f} {out['re_NFW']:5.0f} kpc={out['re_NFW']/kpas:5.1f}''"
        )
        tot = 1 / out["k_OBT"]
        shared = 1 / out["k_NFW"]
        proper = out["k_NFW"] / out["k_OBT"]
        print(
            f"    DEFICIT: total x{tot:.2f} = shared-sphericity x{shared:.2f} (NFW ref) x OBT-proper x{proper:.2f}"
        )
    return out


def main():
    print("=" * 100)
    print(
        " GIANT ARCS vs OBT (card-#22 globals, zero per-object freedom) — conforte la 22, ou monstre ?"
    )
    print("=" * 100)

    # identities (same machinery as abell370_obt, revalidated)
    v = 1000e3
    sis_rho = lambda r: v**2 / (4 * np.pi * G * (np.asarray(r, float) * KPC) ** 2)
    ll = np.logspace(-2, np.log10(8000.0), 600)
    s_num = 2 * np.trapezoid(sis_rho(np.sqrt(100.0**2 + ll**2)), ll * KPC)
    assert abs(s_num / (v**2 / (4 * G * 100 * KPC)) - 1) < 0.02, "SIS identity"
    h370 = Halo(CLUSTERS[0])
    assert (
        abs(sigbar_of(rho_from_mass(h370.m_nfw), 300.0) / h370.sigbar_nfw(300.0) - 1)
        < 0.04
    ), "NFW projection identity"
    assert abs(h370.m_nfw(h370.r200) / h370.m200 - 1) < 1e-6, "M200 recovery"

    results = {}
    for cl in CLUSTERS:
        results[cl["name"]] = analyze(cl)

    # reproduction of abell370_obt.py by this generalized path (published numbers)
    r370 = results[CLUSTERS[0]["name"]]
    assert (
        abs(r370["k_OBT"] - 0.65) < 0.03
    ), "reproduce abell370_obt: kappa_OBT(A370) ~ 0.65"
    assert (
        abs(r370["re_OBT"] - 38) < 4
    ), "reproduce abell370_obt: R_E(OBT, A370) ~ 38 kpc"
    print(
        "\n[reproduction] the generalized code path reproduces abell370_obt.py on A370 (0.65 / 38 kpc) OK"
    )

    # bracket sensitivity on the DISCRIMINANT lens (MS2137): c200, stars, gas corners
    ms = CLUSTERS[1]
    corners = {}
    for lab, kw in (
        ("c-", dict(c200=ms["c_brk"][0])),
        ("c+", dict(c200=ms["c_brk"][1])),
        ("bar-", dict(mstar=ms["ms_brk"][0], fgas_fac=0.6)),
        ("bar+", dict(mstar=ms["ms_brk"][1], fgas_fac=1.4)),
    ):
        r = analyze(ms, quiet=True, **kw)
        corners[lab] = (r["k_OBT"], r["k_NFW"], r["k_NFW"] / r["k_OBT"])
    print("\n[MS2137 bracket corners]  (kappa_OBT, kappa_NFW, OBT-proper deficit):")
    for lab, (ko, kn, pr) in corners.items():
        print(f"    {lab:4s}: kappa_OBT={ko:.2f}  kappa_NFW={kn:.2f}  proper=x{pr:.2f}")

    # the RECONCILED concentration: Donnarumma+09 say X-ray/SL agree, i.e. their NFW puts the
    # critical line ON the arc -> solve c200 s.t. R_E^NFW = R_arc; the OBT-proper deficit AT that c
    # is the literature-preferred reading.
    da_ms = dc(ms["z_l"]) / (1 + ms["z_l"])
    r_arc_ms = ms["r_arc_as"] * da_ms * ARCSEC / KPC
    scr_ms = sigma_cr(ms["z_l"], ms["z_s"])

    def re_nfw_of_c(c):
        hh = Halo(ms, c200=c)
        return brentq(lambda R: hh.sigbar_nfw(R) - scr_ms, 1, 900) - r_arc_ms

    try:
        c_rec = brentq(re_nfw_of_c, 5.0, 16.0)
        r_rec = analyze(ms, quiet=True, c200=c_rec)
        prop_rec = r_rec["k_NFW"] / r_rec["k_OBT"]
        print(
            f"\n[MS2137 RECONCILED reading] c200 solving Donnarumma's X-ray/SL agreement (R_E^NFW = arc):"
        )
        print(
            f"    c_rec = {c_rec:.1f} -> kappa_NFW = {r_rec['k_NFW']:.2f}, kappa_OBT = {r_rec['k_OBT']:.2f}"
            f" -> OBT-proper deficit x{prop_rec:.2f}  <- the literature-preferred reading"
        )
    except ValueError:
        c_rec, prop_rec = np.nan, np.nan
        print(
            "\n[MS2137 RECONCILED reading] no c in [5,16] places R_E on the arc (reported)"
        )

    # ===== THE ANSWER =====
    rms = results[ms["name"]]
    prop_370 = r370["k_NFW"] / r370["k_OBT"]
    prop_ms = rms["k_NFW"] / rms["k_OBT"]
    prop_lo = min(c[2] for c in corners.values())
    prop_hi = max(c[2] for c in corners.values())
    print("\n[THE ANSWER — conforte la 22, ou monstre ?]")
    print(
        f"    OBT-proper deficit:  A370 (merger) x{prop_370:.2f}   |   MS2137 (RELAXED) x{prop_ms:.2f}"
        f"  [corners x{prop_lo:.2f}-x{prop_hi:.2f}]"
    )
    print(
        f"    NFW reference on the relaxed lens: kappa_NFW(R_arc) = {rms['k_NFW']:.2f} (the X-ray/SL"
    )
    print(
        "    reconciliation of Donnarumma+09 says the spherical NFW fits THIS lens — the sphericity"
    )
    print("    refuge is gone; whatever OBT misses here is OBT-PROPER.)")
    if prop_rec == prop_rec:
        print(
            f"    RECONCILED reading (preferred): OBT-proper x{prop_rec:.2f} at c200={c_rec:.1f}"
        )
    k370, kms = r370["k_OBT"], rms["k_OBT"]
    print(
        f"    STRUCTURAL PATTERN: kappa_OBT(R_arc) = {k370:.2f} (A370) vs {kms:.2f} (MS2137) — the"
    )
    print(
        "    GLOBAL cored Weyl appears to SATURATE the arc-radius convergence near ~0.6-0.65"
    )
    print(
        "    regardless of the cluster: if that holds on N more arcs, the global profile predicts"
    )
    print(
        "    'no critical line beyond ~tens of kpc' — contradicted by every giant arc. That IS the"
    )
    print("    monster hypothesis, stated testably.")
    prop_class = prop_rec if prop_rec == prop_rec else prop_ms
    if prop_class <= 1.25:
        print(
            "    -> VERDICT CLASS: card #22 CONFORTED — the relaxed lens shows the same small proper"
        )
        print("       deficit; A370's gap was geometry, as claimed.")
    elif prop_class <= 1.45:
        print(
            "    -> VERDICT CLASS: MARGINAL — the proper deficit grows on the clean terrain; the"
        )
        print(
            "       central-concentration caveat is biting but within the card's population scatter."
        )
    else:
        print(
            "    -> VERDICT CLASS: MONSTER — on the cleanest terrain the GLOBAL cored Weyl misses the"
        )
        print(
            "       strong-lensing core by a factor the population scatter cannot absorb. Registry"
        )
        print(
            "       entry proposed: 'strong-lensing cores vs the cored global Weyl' (the card-#22"
        )
        print(
            "       central-concentration caveat, quantified as a real failure mode; the per-object"
        )
        print(
            "       r_c fix = closure-IC freedom, refused; a derived core-concentration mechanism is"
        )
        print("       the missing piece).")
    print(
        "\n    Literature cross-check: MS2137 was already used to constrain MOND (2002-class paper) —"
    )
    print(
        "    pure MOND failing this arc is corroborated; the question here is OBT's Weyl CORE, not"
    )
    print(
        "    MOND. Honest scope: spherical models; declared baryon/c200 brackets; hydrostatic-mass"
    )
    print(
        "    method CONSISTENT with the card-#22 calibration (X-COP); 2 lenses = a discriminant test,"
    )
    print(
        "    not yet a statistics. CARD/MONSTER logging = Romain's call (the game gate)."
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
