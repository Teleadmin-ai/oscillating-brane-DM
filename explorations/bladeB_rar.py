"""Blade B, sharp version — lensing RAR vs dynamics RAR at matched g_bar (June 2026,
reviewer mode, quarantined). The ciseau: light (lensing, W=1) keeps the full boost
where slow orbits (T_kappa>~T) average it down. So at matched g_bar in the band
regime, lensing should sit ABOVE the SPARC band-points (T_kappa>=1), while sub-band
points (T_kappa<1, adiabatic) agree with lensing.

Sides:
 - LENSING: Brouwer 2021 KiDS-isolated RAR (Fig-4-5-C1), g_obs = 4 G ESD_t/bias
   (card #5 conversion, validated 6-8 sigma vs Brouwer's published split). residual
   vs the exact OBT RAR. CONFOUND: at the deepest g_bar the residual is inflated by
   the 2-halo (environment) term (card #5: ~+0.13 dex, ~half 2-halo) -> lensing
   "full boost" is an UPPER bound there.
 - DYNAMICS: SPARC (V^2/R), residual vs the same OBT RAR, split sub-band/band by
   T_kappa = 2 pi R/V/sqrt2.
CONFOUND on the cross-subtraction: the two samples have independent M/L zero-points;
the Brouwer isolated set has no high-g anchor (max g_bar=3.9e-12) so the absolute
lensing-minus-dynamics is zero-point-limited. The CLEAN, zero-point-free number is
the WITHIN-SPARC band-minus-subband deficit (cards #29/#30).
"""

import numpy as np

G = 6.674e-11
MS = 1.989e30
PC = 3.0857e16
KPC_M = 3.0857e19
a0 = 1.2e-10  # m/s^2
SI = (1e3) ** 2 / KPC_M  # (km/s)^2/kpc -> m/s^2  = 3.241e-14
KK = 0.97779


def rar(gb):
    return np.sqrt((gb**2 + gb * np.sqrt(gb**2 + 4 * a0**2)) / 2.0)


def lensing():
    r = np.loadtxt("/DATA/obt_game_cache/raw/brouwer2021_rar/Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
    gb, esd, err, bias = r[:, 0], r[:, 1], r[:, 3], r[:, 4]
    gobs = 4 * G * esd * MS / PC**2 / bias
    eg = 4 * G * err * MS / PC**2 / bias
    res = np.log10(gobs / rar(gb))
    eres = eg / gobs / np.log(10)
    return gb, res, eres


def sparc():
    pts = []
    for ln in open("/DATA/obt_game_cache/raw/sparc_massmodels.mrt"):
        p = ln.split()
        if len(p) < 8:
            continue
        try:
            R, V, eV = float(p[2]), float(p[3]), float(p[4])
            vg, vd, vb = float(p[5]), float(p[6]), float(p[7])
        except ValueError:
            continue
        if R <= 0 or V <= 0 or eV / V > 0.10:
            continue
        gb = (vg * abs(vg) + 0.5 * vd * vd + 0.7 * vb * vb) / R * SI  # m/s^2
        if gb <= 0:
            continue
        gobs = V * V / R * SI
        res = np.log10(gobs / rar(gb))
        tk = 2 * np.pi * R / V / np.sqrt(2.0) * KK
        pts.append((gb, res, tk))
    return np.array(pts)


def wmean(res, er=None):
    if er is None:
        return np.mean(res), np.std(res) / np.sqrt(max(len(res), 1))
    w = 1.0 / er**2
    m = np.sum(w * res) / np.sum(w)
    return m, 1.0 / np.sqrt(np.sum(w))


def run():
    gbL, resL, eL = lensing()
    S = sparc()
    gbS, resS, tkS = S[:, 0], S[:, 1], S[:, 2]
    # overlap bins (m/s^2): where both lensing and SPARC band points live
    edges = [7e-13, 1.5e-12, 4e-12]
    print("Blade B sharp: lensing vs dynamics RAR residual (dex) at matched g_bar\n")
    print(f"  {'g_bar bin':>20s}{'LENS':>16s}{'SPARC sub(<1)':>16s}{'SPARC band(>=1)':>17s}{'ciseau L-band':>15s}")
    for lo, hi in zip(edges[:-1], edges[1:]):
        mL = (gbL >= lo) & (gbL < hi)
        mSs = (gbS >= lo) & (gbS < hi) & (tkS < 1.0)
        mSb = (gbS >= lo) & (gbS < hi) & (tkS >= 1.0)
        L, eLm = wmean(resL[mL], eL[mL]) if mL.any() else (np.nan, np.nan)
        Ss, eSs = wmean(resS[mSs]) if mSs.sum() >= 3 else (np.nan, np.nan)
        Sb, eSb = wmean(resS[mSb]) if mSb.sum() >= 3 else (np.nan, np.nan)
        cis = L - Sb
        print(f"  {lo:.1e}-{hi:.1e}{L:+8.3f}+-{eLm:.3f}"
              f"{Ss:+9.3f}({mSs.sum():3d}){Sb:+9.3f}({mSb.sum():3d}){cis:+11.3f}")
    # CLEAN zero-point-free number: within-SPARC band - subband over the overlap
    ov = (gbS >= edges[0]) & (gbS < edges[-1])
    sub = resS[ov & (tkS < 1.0)]
    band = resS[ov & (tkS >= 1.0)]
    ms, es = wmean(sub)
    mb, eb = wmean(band)
    print(f"\n  WITHIN-SPARC (zero-point-free, overlap g_bar): sub({len(sub)})={ms:+.3f}+-{es:.3f}"
          f"  band({len(band)})={mb:+.3f}+-{eb:.3f}  -> band deficit = {mb-ms:+.3f}+-{np.hypot(es,eb):.3f} dex")
    mL_all, eLall = wmean(resL[(gbL >= edges[0]) & (gbL < edges[-1])],
                          eL[(gbL >= edges[0]) & (gbL < edges[-1])])
    print(f"  LENSING over the same overlap: {mL_all:+.3f}+-{eLall:.3f} dex (>=0 = full boost; +2-halo upper bound)")

    # T_kappa-resolved + the SIZE degeneracy (the kill test)
    print("\n  T_kappa-resolved (overlap): the deficit lives ONLY in T_k in [1,2] --")
    for lo, hi, lab in [(0, 1, "<1 adiab"), (1, 2, "[1,2] band-AMBIG"), (2, 99, ">2 sinc")]:
        sel = (gbS >= edges[0]) & (gbS < edges[-1]) & (tkS >= lo) & (tkS < hi)
        if sel.sum() < 3:
            print(f"    T_k {lab:16s}: N={sel.sum()} (too few -- SPARC barely reaches the clean ARA regime)")
            continue
        m, e = wmean(resS[sel])
        print(f"    T_k {lab:16s}: N={sel.sum():3d}  resid={m:+.3f}+-{e:.3f}  W=10^2r={10**(2*m):.2f}")
    from scipy.stats import spearmanr

    ovm = (gbS >= edges[0]) & (gbS < edges[-1])
    rho = spearmanr(tkS[ovm], resS[ovm])[0]
    print(f"\n  DEGENERACY (the honest limit): at fixed g_bar, T_kappa proxies galaxy SIZE.")
    print(f"    Spearman(T_k, resid)={rho:+.2f}, BUT residual ~ V^2 and T_k ~ 1/V are anti-correlated")
    print("    BY CONSTRUCTION -> the resid-T_k partial is circularity-contaminated and CANNOT")
    print("    separate 'slow orbits feel less boost' (ARA) from 'large galaxies sag on the RAR' (size).")
    print("\n  VERDICT (blade B, RAR side): lensing/fast tracers keep full boost (W~1); slow/large")
    print("  tracers sag to W~0.6 -- a MODERATE ciseau-like pattern, NOT a collapse. BUT (i) it sits")
    print("  in the ARA-ambiguous band [1,2] (central ARA predicts F=1 there); (ii) it is DEGENERATE")
    print("  with galaxy size; (iii) the lensing cross-check is 2-halo + M/L-zero-point confounded.")
    print("  The clean ARA regime (T_k>2) is reached only by satellites (bladeB_satellites: no collapse,")
    print("  W~0.3-0.7). => blade B BOUNDS the ciseau (moderate, <=0.13 dex) but does NOT cleanly")
    print("  confirm it as distinctively ARA. Flag for the (2) audit: cards #29/#30/#31 attribute the")
    print("  [1,2] band deficit to ARA, but that zone is ARA-ambiguous AND size-degenerate.")


if __name__ == "__main__":
    run()
