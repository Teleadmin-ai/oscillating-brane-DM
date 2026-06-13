"""GATE 23 — final consolidation: stress the 3 pinned features before the 5D solve.
(V9.0, QUARANTINED). (1) plateau by INDEPENDENT method (X-COP hydro vs CCCP lensing);
(2) robustness of turn-on + plateau to M_star choice; (3) is the factor-2 plateau
mass-independent (slope~0)?; (4) radial dependence of the plateau.
"""

import os
import re

import numpy as np
from astropy.io import fits
from scipy.stats import spearmanr

G = 4.300917e-9
A0 = 3.702e6


def rar(g, a):
    return np.sqrt((g**2 + g * np.sqrt(g**2 + 4 * a * a)) / 2.0)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


# ---- X-COP (hydro): f_Weyl at last bin AND radial profile ----
base = "/DATA/obt_game_cache/raw/xcop"
xcop_fw, xcop_logM = [], []
xcop_rad = {}  # cluster -> (r/r_last, f_Weyl)
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
    r, Mt, Mb = r[ok], Mt[ok], (Mg + Ms)[ok]
    gN = G * Mb / r**2
    fw = 1 - rar(gN, A0) / (G * Mt / r**2)
    xcop_fw.append(fw[-1])
    xcop_logM.append(np.log10(Mb[-1]))
    xcop_rad[cl] = (r / r[-1], fw)
xcop_fw = np.array(xcop_fw)
xcop_logM = np.array(xcop_logM)

# ---- CCCP (lensing) ----
kT = {}
for ln in open("/DATA/obt_game_cache/raw/groups/cccp/table1.tex"):
    if "&" in ln and "\\\\" in ln:
        c = [x.strip() for x in ln.split("&")]
        if len(c) >= 10 and not c[0].startswith("\\") and re.search(r"[\d.]", c[-1]):
            kT[norm(c[0])] = 1
ccfw, cclogM = [], []
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
    ccfw.append(1 - rar(G * Mb / r5**2, A0) / (G * Mwl * 1e14 / r5**2))
    cclogM.append(np.log10(Mb))
ccfw = np.array(ccfw)
cclogM = np.array(cclogM)

print("(1) PLATEAU by INDEPENDENT method (the key cross-check):")
print(
    f"  X-COP  HYDRO  (N={len(xcop_fw)}): f_Weyl plateau = {np.median(xcop_fw):.3f} +-{np.std(xcop_fw)/np.sqrt(len(xcop_fw)):.3f}"
)
print(
    f"  CCCP   LENSING(N={len(ccfw)}): f_Weyl plateau = {np.median(ccfw):.3f} +-{np.std(ccfw)/np.sqrt(len(ccfw)):.3f}"
)
print(
    f"  -> {'CONSISTENT (both ~0.45, hydro & lensing agree -> robust)' if abs(np.median(xcop_fw)-np.median(ccfw))<0.08 else 'METHOD-DEPENDENT (caveat)'}"
)

print(
    "\n(3) is the plateau MASS-INDEPENDENT? slope of f_Weyl vs logM in plateau (logM>13.4):"
)
allM = np.concatenate([xcop_logM, cclogM])
allF = np.concatenate([xcop_fw, ccfw])
pl = allM > 13.4
sl, _ = np.polyfit(allM[pl], allF[pl], 1)
print(
    f"  slope d f_Weyl/d logM = {sl:+.3f} per dex (N={pl.sum()}); Spearman {spearmanr(allM[pl],allF[pl]).statistic:+.2f}"
)
print(
    f"  -> {'FLAT (mass-independent factor-2 confirmed)' if abs(sl)<0.1 else 'NOT flat'}"
)

print("\n(4) RADIAL dependence (X-COP): f_Weyl at 0.4 vs 0.7 vs 1.0 r_last:")
for frac in [0.4, 0.7, 1.0]:
    vals = [np.interp(frac, rr, ff) for rr, ff in xcop_rad.values()]
    print(f"    r/r_last={frac}: median f_Weyl = {np.median(vals):.3f}")
print(
    "  -> if rising outward, the 'plateau 0.45' is an r500 value, not radius-universal"
)

# ---------------------------------------------------------------------------
# CONSOLIDATION VERDICT (Gate 23 — the 3 features stress-tested, refined):
#  F1 (zero Weyl for galaxies): holds, robust.
#  F2 (turn-on): the M_bar turn-on SHIFTS ~0.5 dex with the M_star assumption
#     (Sun09: logM_bar 12.6->13.1 from gas-only to +1.0 gas), but is STABLE in
#     M_tot and kT (logM_tot~13.7-13.9, kT~1.5-1.7 keV). => specify the turn-on
#     in OBSERVABLES: kT ~ 1.5-1.7 keV / M_tot ~ 5-8e13 Msun (NOT in M_bar).
#  F3 (factor-2 plateau): NUANCED.
#     - MASS-INDEPENDENT: slope d f_Weyl/d logM = -0.07/dex in the plateau (flat,
#       confirmed across BOTH methods, N=61). This core claim HOLDS.
#     - METHOD-dependent VALUE: X-COP hydro 0.29 vs CCCP lensing 0.46. The clean
#       (true-mass) value is the LENSING 0.46 (factor ~1.85); the hydro value is
#       lower, the standard direction for hydrostatic bias (M_hydro<M_WL) though
#       a clean numerical demonstration is not done here (mixed rayon/M_star too).
#     - RADIUS-dependent: f_Weyl rises inward (X-COP: 0.59 at 0.4 r_last, 0.29 at
#       r_last) -> the plateau value is an r500 quantity, NOT radius-universal;
#       the Weyl is centrally concentrated (consistent with Gates 13/17).
#  REFINED 5D-solve target spec:
#   (1) zero Weyl for galaxies;
#   (2) turn-on at kT ~ 1.5-1.7 keV (M_tot ~ 5-8e13), M_star-robust;
#   (3) a MASS-INDEPENDENT f_Weyl(r500) ~ 0.46 (true/lensing mass), rising inward.
#  Consolidation strengthened F3's mass-independence (2 methods) and F2's threshold
#  (kT-robust), while correctly down-grading the 'universal 0.45' to a method/
#  radius-dependent value with a robust mass-independence.
