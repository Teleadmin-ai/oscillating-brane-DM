"""GATE 22 — densifying the RISE with Sun09 groups: sharp threshold or gradual?
(V9.0, QUARANTINED). Adds 23 Sun09 groups (T500/r500/M500/fgas500, ar5iv T12) to
the transition zone (M_bar ~1e12-1e13.5), where Gate 21 had only ~9. Same
f_Weyl = 1 - g_MOND/g_obs (full MOND, W=1) at r500. Question: does f_Weyl turn on
SHARPLY at a threshold mass, or rise GRADUALLY galaxies->groups->clusters?
"""

import csv
import json
import os
import re

import numpy as np
from astropy.io import fits

G = 4.300917e-9
Gk = 4.300917e-6
A0 = 3.702e6
A0k = 3702.0


def rar(g, a):
    return np.sqrt((g**2 + g * np.sqrt(g**2 + 4 * a * a)) / 2.0)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


M, F, K = [], [], []

# galaxies SPARC
glx = {}
for ln in open("/DATA/obt_game_cache/raw/sparc_massmodels.mrt"):
    p = ln.split()
    if len(p) < 8:
        continue
    try:
        R, V, eV, vg, vd, vb = (float(p[i]) for i in (2, 3, 4, 5, 6, 7))
    except:
        continue
    if R > 0 and V > 0:
        glx.setdefault(p[0], []).append((R, V, eV, vg, vd, vb))
for g, a in glx.items():
    R, V, eV, vg, vd, vb = sorted(a)[-1]
    if eV / V > 0.1:
        continue
    vb2 = vg * abs(vg) + 0.5 * vd**2 + 0.7 * vb**2
    if vb2 <= 0:
        continue
    M.append(np.log10(vb2 * R / Gk))
    F.append(1 - rar(vb2 / R, A0k) / (V * V / R))
    K.append("galaxy")

# Sun09 groups (M_star ~ 0.5 M_gas estimate for kT~1 keV groups)
for g, T, r5, M5, fg in json.load(
    open("/DATA/obt_game_cache/raw/groups/sun09_parsed.json")
):
    Mt = M5 * 1e13
    Mb = 1.5 * fg * M5 * 1e13  # M_bar = (gas)(1+0.5 stars)
    gN = Gk * Mb / r5**2
    gobs = Gk * Mt / r5**2
    M.append(np.log10(Mb))
    F.append(1 - rar(gN, A0k) / gobs)
    K.append("group")

# Lagana groups
for row in csv.DictReader(open("/DATA/obt_game_cache/raw/groups/lagana13.csv")):
    r = float(row["r500"])
    Mt = float(row["Mt500"]) * 1e13
    Mb = (float(row["Mg500"]) + float(row["Ms500"])) * 1e12
    M.append(np.log10(Mb))
    F.append(1 - rar(Gk * Mb / r**2, A0k) / (Gk * Mt / r**2))
    K.append("group")

# clusters X-COP + CCCP
base = "/DATA/obt_game_cache/raw/xcop"
for cl in sorted(os.listdir(base)):
    p = f"{base}/{cl}/{cl}_fgas_profile.fits"
    if not os.path.exists(p):
        continue
    fg = fits.open(p)[1].data
    r = np.asarray(fg["RADIUS"], float)
    Mt = np.asarray(fg["M_NFW"], float)
    Mg = np.asarray(fg["MGAS"], float)
    try:
        ms = fits.open(f"{base}/{cl}/{cl}_mstar.fits")[1].data
        Ms = np.interp(
            r, np.asarray(ms["RADIUS"], float), np.asarray(ms["MSTAR"], float)
        )
    except:
        Ms = 0.16 * Mg
    ok = (r > 0) & (Mt > 0)
    Mb = (Mg + Ms)[ok][-1]
    Mt2 = Mt[ok][-1]
    rr = r[ok][-1]
    M.append(np.log10(Mb))
    F.append(1 - rar(G * Mb / rr**2, A0) / (G * Mt2 / rr**2))
    K.append("cluster")
kT = {}
for ln in open("/DATA/obt_game_cache/raw/groups/cccp/table1.tex"):
    if "&" in ln and "\\\\" in ln:
        c = [x.strip() for x in ln.split("&")]
        if len(c) >= 10 and not c[0].startswith("\\") and re.search(r"[\d.]", c[-1]):
            kT[norm(c[0])] = 1
for ln in open("/DATA/obt_game_cache/raw/groups/cccp/table2.tex"):
    if "&" not in ln or "\\\\" not in ln or "colhead" in ln:
        continue
    c = [x.strip() for x in ln.split("&")]
    if len(c) < 5:
        continue

    def v(s):
        m = re.search(r"([\d.]+)\s*\\pm\s*([\d.]+)", s) or re.search(r"([\d.]+)", s)
        return float(m.group(1)) if m else None

    r5, Mwl, Mg = v(c[1]), v(c[2]), v(c[3])
    if None in (r5, Mwl, Mg):
        continue
    Mb = 1.15 * Mg * 1e14
    Mt = Mwl * 1e14
    M.append(np.log10(Mb))
    F.append(1 - rar(G * Mb / r5**2, A0) / (G * Mt / r5**2))
    K.append("cluster")

M, F, K = np.array(M), np.array(F), np.array(K)
ng = np.sum(K == "group")
print(
    f"N={len(M)} (groups now {ng}: 23 Sun09 + 9 Lagana). M_bar {M.min():.1f}-{M.max():.1f} dex\n"
)
print(f"  {'logM_bar':>10s}{'N':>4s}{'med f_Weyl':>12s}{'kinds':>16s}")
for lo in np.arange(9.0, 14.6, 0.4):
    m = (M >= lo) & (M < lo + 0.4)
    if m.sum() < 2:
        continue
    kk = ",".join(sorted(set(K[m])))
    print(f"  {lo:.1f}-{lo+0.4:.1f}{m.sum():4d}{np.median(F[m]):12.3f}{kk:>16s}")
# fit the rise: logistic-ish — find turn-on and slope
gp = K == "group"
print(
    f"\n  GROUP zone (N={gp.sum()}): M_bar {M[gp].min():.1f}-{M[gp].max():.1f}, f_Weyl median {np.median(F[gp]):+.2f}"
)
from scipy.stats import spearmanr

print(
    f"  within groups: Spearman(M_bar,f_Weyl) = {spearmanr(M[gp],F[gp]).statistic:+.2f} (rise slope sign)"
)
# sharp vs gradual: f_Weyl in group sub-bins
for lo in [11.5, 12.0, 12.5, 13.0]:
    m = gp & (M >= lo) & (M < lo + 0.5)
    if m.sum() >= 2:
        print(
            f"    groups logM {lo:.1f}-{lo+0.5:.1f}: N={m.sum()}, f_Weyl={np.median(F[m]):+.3f}"
        )

# ---------------------------------------------------------------------------
# VERDICT (rise densified with 23 Sun09 groups -> 32 groups in the transition):
#  f_Weyl(M_bar): ~0 for galaxies (logM<11.8, 3 flat decades) -> turns on at
#  logM_bar~12.2 (0.09) -> rises through 12.6-13.0 (0.29) -> PLATEAUS ~0.45 for
#  clusters (logM 13.4-14.6: 0.46,0.46,0.44).
#  => MODERATELY SHARP TRANSITION centred at M_bar ~ 4e12 (kT~1.5 keV, V_c~450),
#  from 0 to the factor-2 plateau over ~1-1.5 decade. NEITHER a discontinuous
#  threshold (no 0->0.45 jump) NOR a soft power law (it saturates and the rise is
#  steeper than a power law) -> a REGIME CHANGE of the brane response at a soft
#  mass threshold ~4e12 Msun(bar).
#  The 5D bulk solve must reproduce THREE pinned features:
#   (1) zero Weyl for galaxies (M_bar < ~1e12),
#   (2) a moderately sharp turn-on centred at M_bar ~ 4e12 (over ~1 decade),
#   (3) a mass-independent factor-2 (f_Weyl~0.45) plateau for clusters.
#  CAVEATS: M_star handled differently per catalog (Sun09 0.5*M_gas estimate,
#  Lagana/X-COP real, CCCP 0.15*M_gas) -> shifts the group placement at the ~0.1
#  dex level; mixed mass methods (RAR/hydro/lensing) carry cross-systematics;
#  group scatter is real (Spearman +0.43); Lovisari15 not added (ar5iv longtable
#  not machine-parseable; 32 groups already define the rise).
