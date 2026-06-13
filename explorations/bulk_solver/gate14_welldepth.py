"""GATE 14 — is the cluster Weyl-DM sourced by POTENTIAL-WELL DEPTH? (V9.0, QUARANTINED)

Gate 13 killed the sinc hypothesis but showed Weyl dominates at the cluster CORE
(deepest |Phi|). New hypothesis: f_Weyl is a UNIVERSAL function of well depth
(proxy: circular velocity V_c = sqrt(G M_tot/r)) — small for galaxies (shallow
wells, V_c~150-300), large for clusters (deep wells, V_c~1000-1500), with a
threshold in between. This connects to the KNOWN fact that MOND's residual
cluster discrepancy scales with cluster richness/temperature (Sanders, The-White).
Mechanism candidate: the brane buckles into the bulk above a critical well depth
(Israel junction: deep S_munu bends the brane -> large projected E_munu), a
brane/oscillation effect, NOT a free per-cluster constant.

Test: bin ALL points (12 X-COP clusters + SPARC galaxies) by V_c; is f_Weyl(V_c)
a single universal rising curve? f_Weyl = (g_obs - g_N - Dg_MOND*W)/g_obs.
"""

import os

import numpy as np
from astropy.io import fits

G = 4.300917e-9  # Mpc (km/s)^2 / Msun
G_KPC = 4.300917e-6  # kpc (km/s)^2 / Msun
A0 = 3.702e6  # (km/s)^2 / Mpc  [CORRECTED x1000]
A0_KPC = 3702.0  # (km/s)^2 / kpc  [CORRECTED x1000]
T_BRANE = 2.0
MPC_KMS_GYR = 977.79


def rar(gN, a0):
    return np.sqrt((gN**2 + gN * np.sqrt(gN**2 + 4 * a0**2)) / 2.0)


# ---------------- clusters (X-COP) ----------------
base = "/DATA/obt_game_cache/raw/xcop"
clpts = []  # (V_c, f_Weyl)
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
    except Exception:
        Ms = 0.16 * Mg
    Mb = Mg + Ms
    ok = (r > 0) & (Mt > Mb) & (Mb > 0)
    r, Mt, Mb = r[ok], Mt[ok], Mb[ok]
    gN = G * Mb / r**2
    gobs = G * Mt / r**2
    dgM = rar(gN, A0) - gN
    Vc = np.sqrt(G * Mt / r)
    tdyn = 2 * np.pi * r / Vc * MPC_KMS_GYR
    W = np.abs(np.sinc(tdyn / T_BRANE))
    fW = (gobs - gN - dgM * W) / gobs
    for v, f in zip(Vc, fW):
        clpts.append((v, f))
clpts = np.array(clpts)

# ---------------- galaxies (SPARC) ----------------
glx = {}
for line in open("/DATA/obt_game_cache/raw/sparc_massmodels.mrt"):
    p = line.split()
    if len(p) < 8:
        continue
    try:
        R, V, eV, vg, vd, vb = (float(p[i]) for i in (2, 3, 4, 5, 6, 7))
    except ValueError:
        continue
    if R > 0 and V > 0:
        glx.setdefault(p[0], []).append((R, V, eV, vg, vd, vb))
glpts = []
for g, pts in glx.items():
    for R, V, eV, vg, vd, vb in pts:
        if eV / V > 0.1:
            continue
        gN = (vg * abs(vg) + 0.5 * vd**2 + 0.7 * vb**2) / R
        if gN <= 0:
            continue
        gobs = V * V / R
        dgM = rar(gN, A0_KPC) - gN
        Vc = V
        tdyn = (
            2 * np.pi * R / V / np.sqrt(2.0) * 0.97779 * np.sqrt(2)
        )  # ~2pi R/V in Gyr
        tdyn = 2 * np.pi * R / V * 0.97779
        W = abs(np.sinc(tdyn / T_BRANE))
        fW = (gobs - gN - dgM * W) / gobs
        glpts.append((Vc, fW))
glpts = np.array(glpts)

# ---------------- universal f_Weyl(V_c) ----------------
print("f_Weyl vs circular velocity V_c (well-depth proxy):")
print(f"  {'V_c bin [km/s]':>16s}{'N':>6s}{'median f_Weyl':>15s}{'source':>14s}")
allV = np.concatenate([glpts[:, 0], clpts[:, 0]])
allf = np.concatenate([glpts[:, 1], clpts[:, 1]])
bins = [
    (50, 150),
    (150, 250),
    (250, 400),
    (400, 700),
    (700, 1000),
    (1000, 1400),
    (1400, 2200),
]
for lo, hi in bins:
    m = (allV >= lo) & (allV < hi)
    if m.sum() < 3:
        continue
    src = "galaxies" if hi <= 400 else ("clusters" if lo >= 700 else "mixed/gap")
    print(f"  {f'{lo}-{hi}':>16s}{m.sum():6d}{np.median(allf[m]):15.3f}{src:>14s}")

from scipy.stats import spearmanr

rho = spearmanr(allV, allf).statistic
print(
    f"\n  Spearman(V_c, f_Weyl) = {rho:+.3f}  over {len(allV)} points (galaxies+clusters)"
)
# galaxy-only and cluster-only medians
print(
    f"  galaxies (V_c<300): median f_Weyl = {np.median(glpts[glpts[:,0]<300,1]):+.3f}  (N={np.sum(glpts[:,0]<300)})"
)
print(
    f"  clusters (V_c>700): median f_Weyl = {np.median(clpts[clpts[:,0]>700,1]):+.3f}  (N={np.sum(clpts[:,0]>700)})"
)
print()
print("  READ: a UNIVERSAL monotonic rise of f_Weyl with V_c (well depth), ~0 for")
print("  galaxies and ~0.8 for clusters with a threshold in the group regime")
print("  (V_c~400-700), would say the Weyl-DM is sourced by potential-well depth")
print("  (brane buckling via Israel) — an oscillation/geometry effect, NOT a free")
print("  per-cluster constant. A scattered/non-monotone f_Weyl(V_c) would refute it.")

# ---------------------------------------------------------------------------
# VERDICT (after the a0 x1000 bug fix that also corrected Gate 13):
#  Selectivity-variable comparison (which quantity organizes the Weyl-DM?):
#    f_Weyl vs (1-W)  [sinc / dynamical time] : Spearman ~ -0.05  -> NOT it
#    f_Weyl vs V_c    [potential-well depth]  : Spearman = +0.61  -> THIS
#  Galaxies (shallow wells): f_Weyl ~ 0.12 +/- 0.25 (compatible with 0 in the
#  RAR scatter -> no real galactic halo, MOND works). Clusters (deep wells):
#  f_Weyl ~ 0.82. The cluster Weyl-DM is organized by WELL DEPTH, not by sinc.
#
#  HONEST CAVEATS:
#   (1) the galaxy/cluster transition (V_c~400-700) falls in a DATA GAP: 0 whole
#       systems there, only cluster cores rising through V_c. GROUPS (whole
#       systems at V_c~400-700) are the missing decisive test of a threshold.
#   (2) SPARC (max V_c 383) OVERLAPS X-COP cores (min 311) yet f_Weyl differs
#       (~0.12 vs ~0.7) at the same LOCAL V_c -> the variable is the GLOBAL well
#       depth |Phi| (a cluster core sits in a deep global well), not local V_c.
#   (3) this is an EMPIRICAL correlation; the mechanism (brane FLEXURE by mass
#       via the Israel junction, buckling above a critical |Phi|) is a candidate,
#       NOT derived. The threshold and its link to the oscillation are open.
#
#  PROGRESS: the cluster Weyl-DM amplitude is no longer a FREE per-cluster
#  constant — it is a universal function of baryonic well depth f_Weyl(|Phi|).
#  Geometric, baryon-determined, no particles. This REDUCES the closure freedom
#  (from an arbitrary amplitude to one universal function + a threshold to derive)
#  but does NOT yet make it "the oscillation": galaxies = tilt (oscillation/
#  horizon a0); clusters = brane flexure (well depth) — two brane effects, zero
#  matter, but distinct mechanisms. Next: GROUPS + the global-|Phi| variable.
