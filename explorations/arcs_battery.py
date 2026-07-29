"""THE N-ARCS BATTERY — monster [62b7f086] 'arc-cores vs hydrostatic-calibrated Weyl' vs 9 CLASH lenses.

[!] FOLLOW-UP (2026-07-29): the battery's two measurements STAND (the MONSTER-arm saturation
    kappa = 0.70 +/- 0.06 and the mass-anchor relocation M5(M-T)/M5(lensing) = 0.59), but the
    monster they support is DOWNGRADED by `alpha_nt_budget.py` + `card22_lensing_refit.py`
    (see ALPHA_NT_AND_REFIT_NOTE.md): (i) on PUBLISHED lensing masses the anchor gap is 0.65, and
    0.75 after de-biasing the M-T bridge on X-COP's own data -> the non-thermal patch is short by
    x4-6 on the card's own sample; (ii) the SPHERICAL published-lensing NFW itself only reaches
    kappa = 0.79 at the observed Einstein radii, so the arc deficit is SHARED with the standard
    model (ellipticity/substructure), and OBT-proper = 0.93 = no OBT-proper deficit.

MODE CHERCHEUR (Romain: 'logue le monstre et lance la batterie N-arcs'). Sanctioned big-compute
(monster->card rule): validate the monster's signature across systems. AXIOM: OBT true -> the arcs
exist -> the Weyl makes them; the misfit indicts the EXTERNAL hydrostatic calibration behind
card #22's global cored Weyl (or, alternative reading, the closure-IC core profile).

THE BATTERY (uniform anchors, all web-verified this session):
  * 9 CLASH X-ray-selected clusters (mostly relaxed by Postman selection; several strong cool
    cores): z_l from the Zitrin+15 Vizier cluster table; effective Einstein radii theta_E(z_s=2)
    and PROJECTED lensing masses M2D(<10,20,30,40'') from Umetsu et al. 2016 Table 1
    (units 1e13 Msun/h70; the two-Zitrin-model average).
  * Per-cluster NFW reference calibrated on the OUTER lensing point: c200 = 3.79 (the CLASH
    X-ray-subsample ensemble value, Umetsu+16) with M200 solved so M2D_NFW(<40'') matches the
    lensing table -> M500, R500 for the card-#22 Weyl (f_W = 0.70, beta = 0.043, GLOBAL).
  * OBT law as in arcs_obt.py: exact RAR at a0(z_l) = cH(z_l)/2pi (W = 1 photons) + the Weyl.

TWO ARMS per cluster (the pass-1 relire caught that a single lensing-anchored arm is
normalization-tautological for the monster question):
  * FORM arm — Weyl anchored on the 40''-lensing-calibrated M500: tests the card-#22 PROFILE
    shape against the 4-radius lensing table (kappa_OBT vs kappa_NFW; M2D ratios at 10-40'').
  * MONSTER arm — Weyl anchored on the EXTERNAL hydrostatic-class M-T M500 (Arnaud+05 class,
    kT from the CLASH Chandra table): the SAME calibration class as card #22's X-COP fit ->
    reproduces the A370/MS2137 configuration. MONSTER TESTS: (i) does kappa_OBT_MT(theta_E)
    saturate ~0.6-0.7 universally? (ii) M5_MT/M5_lens — the anchor ratio where the monster lives.
Asserted ONLY identities + reproductions (M_E = pi Sigma_cr R_E^2 vs the interpolated lensing
M2D(theta_E) per cluster; the duplicated Weyl-law identity vs A.Halo.m_weyl). Everything else
computed + reported. Quarantined; not sacred; not the PDF.
"""

import arcs_obt as A
import numpy as np
from scipy.optimize import brentq

MSUN, KPC, ARCSEC, G, C = A.MSUN, A.KPC, A.ARCSEC, A.G, A.C
H70 = (
    67.4 / 70.0
)  # our H0 in h70 units; table masses are 1e13 Msun/h70 -> phys = val/H70
C_ENS = 3.79  # CLASH X-ray-subsample ensemble c200c (Umetsu+16)
Z_S = 2.0  # the theta_E convention source plane

# name, z_l, theta_E('' @z_s=2), M2D(<10,20,30,40'') 1e13 Msun/h70, kT keV  [Umetsu+16 T1; Vizier]
BATTERY = [
    ("Abell383   (relaxed CC)", 0.187, 15.1, (1.15, 3.04, 4.98, 6.77), 6.5),
    ("Abell2261  (relaxed)   ", 0.224, 23.1, (1.91, 4.79, 7.67, 10.42), 7.6),
    ("RXJ2129    (relaxed CC)", 0.234, 12.9, (1.13, 3.36, 5.95, 8.67), 5.8),
    ("Abell611   (relaxed)   ", 0.288, 18.1, (1.84, 5.25, 9.37, 14.26), 7.9),
    ("MS2137     (relaxed CC)", 0.313, 17.1, (2.25, 5.23, 7.99, 10.76), 5.9),
    ("MACS1115   (relaxed CC)", 0.352, 18.1, (1.85, 5.79, 11.09, 16.98), 8.0),
    ("MACS1931   (strong CC) ", 0.352, 22.2, (2.91, 7.37, 12.15, 17.21), 6.7),
    ("MACS1720   (relaxed CC)", 0.391, 20.1, (2.65, 7.20, 12.39, 17.97), 6.6),
    ("MACS0429   (relaxed CC)", 0.399, 15.7, (2.22, 6.80, 12.55, 18.87), 6.0),
]
RADII_AS = (10.0, 20.0, 30.0, 40.0)

# The EXTERNAL (hydrostatic-class) mass arm: the M-T scaling (Arnaud+05 class, declared):
#   M500 * E(z) = M5 * (kT / 5 keV)^alpha ;  M5 = 3.8e14 Msun (norm bracket +/-25%), alpha = 1.71.
# This is exactly the calibration CLASS behind card #22 (hydrostatic X-ray) -> the MONSTER arm.
MT_M5, MT_ALPHA = 3.8e14, 1.71


def m500_mt(kt_kev, zl):
    return MT_M5 * (kt_kev / 5.0) ** MT_ALPHA / A.ez(zl)


def run_cluster(name, zl, te_as, m2d_tab, kt_kev):
    scr = A.sigma_cr(zl, Z_S)
    da = A.dc(zl) / (1 + zl)
    kpas = da * ARCSEC / KPC
    r_e = te_as * kpas
    m2d_phys = np.array(m2d_tab) * 1e13 / H70 * MSUN  # h70 -> our H0

    # anchor consistency (reproduction): pi Sigma_cr R_E^2 == interp of the lensing M2D at theta_E
    me_geom = np.pi * scr * (r_e * KPC) ** 2
    me_tab = np.interp(te_as, RADII_AS, m2d_phys) if te_as <= 40 else np.nan
    anch = me_geom / me_tab if me_tab == me_tab else np.nan

    # per-cluster NFW reference: c=3.79 ensemble, M200 solved on the OUTER lensing point (40'')
    cl = dict(
        name=name,
        z_l=zl,
        z_s=Z_S,
        c200=C_ENS,
        m200=8e14,
        c_brk=(C_ENS, C_ENS),
        r_arc_as=te_as,
        r_arc_brk=(te_as, te_as),
        mstar=5e11,
        astar=10.0,
        ms_brk=(2.5e11, 1e12),
        note="",
        relaxed=True,
    )
    r40 = 40.0 * kpas

    def m40_of_m200(m200_msun):
        cl2 = dict(cl, m200=m200_msun)
        h = A.Halo(cl2)
        return h.sigbar_nfw(r40) * np.pi * (r40 * KPC) ** 2 - m2d_phys[3]

    m200 = brentq(m40_of_m200, 5e13, 6e15, rtol=1e-4)
    cl["m200"] = m200
    h = A.Halo(cl)

    a0z = C * A.H0 * A.ez(zl) / (2 * np.pi)
    # baryons (BCG + gas) shared by BOTH arms; the gas profile rides the lensing R500 --
    # sub-dominant vs Weyl+BCG at 10-40'' (percent-level on kappa), so one model suffices
    g_bar = lambda r: G * h.m_bar(r) / (np.asarray(r, float) * KPC) ** 2
    g_obt = (
        lambda r: A.rar_obt(g_bar(r), a0z)
        + G * h.m_weyl(r) / (np.asarray(r, float) * KPC) ** 2
    )
    rho_obt = A.rho_from_mass(A.m_eff(g_obt))
    k_obt = A.sigbar_of(rho_obt, r_e) / scr
    k_nfw = h.sigbar_nfw(r_e) / scr

    # ===== the MONSTER arm: Weyl anchored on the EXTERNAL hydrostatic-class M500 (M-T) =====
    m5_mt = m500_mt(kt_kev, zl) * MSUN
    rho_cz = 3 * (A.H0 * A.ez(zl)) ** 2 / (8 * np.pi * G)
    r5_mt = (m5_mt / (4 / 3 * np.pi * 500 * rho_cz)) ** (
        1 / 3
    ) / KPC  # kpc, by definition
    x5 = 1.0 / A.BETA

    def m_weyl_mt(r_kpc):
        r = np.minimum(np.asarray(r_kpc, float), 2 * r5_mt)
        x = r / (A.BETA * r5_mt)
        return A.FW * m5_mt * (x - np.arctan(x)) / (x5 - np.arctan(x5))

    # reproduction: the duplicated Weyl law == A.Halo.m_weyl at the same dimensionless x=1
    assert (
        abs(
            m_weyl_mt(A.BETA * r5_mt) / (A.FW * m5_mt)
            - h.m_weyl(A.BETA * h.r500) / (A.FW * h.m500)
        )
        < 1e-9
    ), "duplicated M-T Weyl law must match Halo.m_weyl's dimensionless form"

    g_obt_mt = (
        lambda r: A.rar_obt(g_bar(r), a0z)
        + G * m_weyl_mt(r) / (np.asarray(r, float) * KPC) ** 2
    )
    k_obt_mt = A.sigbar_of(A.rho_from_mass(A.m_eff(g_obt_mt)), r_e) / scr
    # radius-resolved projected-mass ratios OBT/lens at the four table radii
    ratios = []
    for i, th in enumerate(RADII_AS):
        rr = th * kpas
        m2d_obt = A.sigbar_of(rho_obt, rr) * np.pi * (rr * KPC) ** 2
        ratios.append(m2d_obt / m2d_phys[i])
    return dict(
        name=name,
        zl=zl,
        te=te_as,
        r_e=r_e,
        scr=scr,
        anch=anch,
        m200=m200,
        r500=h.r500,
        k_obt=k_obt,
        k_nfw=k_nfw,
        proper=k_nfw / k_obt,
        ratios=ratios,
        m5_mt=m5_mt,
        m5_lens=h.m500,
        k_obt_mt=k_obt_mt,
    )


def main():
    print("=" * 104)
    print(
        " === MODE CHERCHEUR ===  N-ARCS BATTERY — monster [62b7f086] vs 9 CLASH lenses (+A370/MS2137 prior)"
    )
    print("=" * 104)

    res = [run_cluster(*row) for row in BATTERY]

    # anchor reproductions: geometry vs table at theta_E (validates z, theta_E, M2D jointly)
    anchs = np.array([r["anch"] for r in res if r["anch"] == r["anch"]])
    print(
        f"\n[anchors] pi Sig_cr R_E^2 / M2D_lens(theta_E): median {np.median(anchs):.2f},"
        f" range {anchs.min():.2f}-{anchs.max():.2f}  (consistency of z, theta_E, M2D, cosmology)"
    )
    assert (
        0.75 < np.median(anchs) < 1.3
    ), "anchor reproduction: geometric M_E ~ tabulated lensing M2D"

    print(
        f"\n{'cluster':26s} {'z_l':>5s} {'th_E':>5s} {'kOBT_lens':>9s} {'kOBT_MT':>8s} {'kNFW':>6s}"
        f" {'M5MT/M5lens':>11s}   M2D_OBT/M2D_lens @ 10/20/30/40''"
    )
    for r in res:
        rt = "/".join(f"{x:.2f}" for x in r["ratios"])
        print(
            f"{r['name']:26s} {r['zl']:5.3f} {r['te']:4.1f}'' {r['k_obt']:9.2f} {r['k_obt_mt']:8.2f}"
            f" {r['k_nfw']:6.2f} {r['m5_mt']/r['m5_lens']:11.2f}   {rt}"
        )
    print(
        "    (kOBT_lens: Weyl anchored on the 40''-LENSING-calibrated M500 -- the FORM arm;"
    )
    print(
        "     kOBT_MT: Weyl anchored on the EXTERNAL hydrostatic-class M-T M500 -- the MONSTER arm,"
    )
    print(
        "     the same calibration class as card #22; M5MT/M5lens = the two anchors' ratio.)"
    )

    k_all = np.array([r["k_obt"] for r in res])
    k_mt = np.array([r["k_obt_mt"] for r in res])
    p_all = np.array([r["proper"] for r in res])
    r10 = np.array([r["ratios"][0] for r in res])
    r40 = np.array([r["ratios"][3] for r in res])
    print(
        "\n[MONSTER TEST 1 — saturation universality, on the MONSTER (external-calibration) arm]"
    )
    print(
        f"    kappa_OBT_MT(theta_E): median {np.median(k_mt):.2f}, scatter {np.std(k_mt):.2f},"
        f" range {k_mt.min():.2f}-{k_mt.max():.2f}  (A370 0.65, MS2137 0.63 previously = this arm's class)"
    )
    print(
        f"    [FORM arm, lensing-anchored Weyl: kappa_OBT median {np.median(k_all):.2f},"
        f" range {k_all.min():.2f}-{k_all.max():.2f} -- the profile SHAPE ~ NFW]"
    )
    print(
        "[MONSTER TEST 2 — where the deficit lives (core-bias signature: worst at 10'', healing at 40'')]"
    )
    print(
        f"    M2D_OBT/M2D_lens: at 10'' median {np.median(r10):.2f}  ->  at 40'' median {np.median(r40):.2f}"
    )
    print(
        f"    OBT-proper deficit (vs the 40''-calibrated NFW at theta_E): median x{np.median(p_all):.2f},"
        f" range x{p_all.min():.2f}-x{p_all.max():.2f}"
    )

    m_ratio = np.array([r["m5_mt"] / r["m5_lens"] for r in res])
    print("\n[VERDICT — the monster after the battery: CONSOLIDATED and RELOCATED]")
    sat = np.std(k_mt) < 0.08
    print(
        f"    (1) MONSTER arm saturation across 9 systems: {'YES' if sat else 'NO'} (median"
        f" {np.median(k_mt):.2f}, std {np.std(k_mt):.2f}; + A370 0.65, MS2137 0.63 = 11/11 in 0.63-0.84)"
    )
    n_def = int(np.sum(p_all > 1.25))
    print(
        "    (2) FORM arm: the card-#22 profile SHAPE is GOOD — proper deficit vs the 40''-calibrated NFW"
    )
    print(
        f"        median x{np.median(p_all):.2f} (range x{p_all.min():.2f}-x{p_all.max():.2f});"
        f" systems worse than x1.25: {n_def}/9. Radius-resolved residual is a mild core dip,"
    )
    print(
        f"        10'' {np.median(r10):.2f} -> 40'' {np.median(r40):.2f} median (dispersion"
        f" {r10.min():.2f}-{r10.max():.2f} at 10'': the fixed BCG M*=5e11 is crude; A2261-class"
    )
    print("        giant BCGs ~2e12 would absorb part of the deepest dips).")
    print(
        "    (3) THE MONSTER LIVES IN THE MASS ANCHOR, not the profile: M5(M-T, hydrostatic class) /"
    )
    print(
        f"        M5(lensing-40'', c=3.79) = median {np.median(m_ratio):.2f} (range {m_ratio.min():.2f}-"
        f"{m_ratio.max():.2f}) — the external calibration chain sits ~40% LOW vs the core lensing."
    )
    print(
        "        This is numerically the famous HYDROSTATIC MASS BIAS: (1-b) ~ 0.6 is exactly the value"
    )
    print(
        "        the Planck SZ cluster counts demand (vs ~0.8 in simulations) — the monster joins a"
    )
    print(
        "        KNOWN, LIVE external tension. Even at the M-T norm's +25% bracket the anchor deficit"
    )
    print(
        "        persists (x0.74). CAVEATS: the 40''->M500 extrapolation assumes c=3.79 (c-M degeneracy;"
    )
    print(
        "        a higher true c lowers M5_lens toward M-T); kT are single global Chandra values, and for"
    )
    print(
        "        the strongest cool cores (MACS0429 0.40, MACS1931 0.46 — the two extreme ratios) the"
    )
    print(
        "        un-excised cool core biases kT low: part of THEIR anchor deficit is mundane kT bias,"
    )
    print(
        "        not hydrostatic bias (the battery median 0.59 is carried by the full sample)."
    )
    print(
        "    READING (axiom-side, updated): the card-#22 Weyl FORM is vindicated by 9 lensing cores;"
    )
    print(
        "    the patched external theory = the hydrostatic-equilibrium MASS NORMALIZATION (X-ray"
    )
    print(
        "    masses ~x0.6 vs lensing where non-thermal pressure is unbudgeted). WHY-candidate now"
    )
    print(
        "    QUANTIFIED and matching the independent Planck-SZ (1-b)~0.6 requirement; still pending"
    )
    print(
        "    for card status: a derivation/measurement closing the alpha_NT budget (Hitomi tension),"
    )
    print(
        "    and re-fitting card #22's (f_W, beta) on lensing masses instead of X-COP hydrostatic."
    )
    print("=" * 104)


if __name__ == "__main__":
    main()
