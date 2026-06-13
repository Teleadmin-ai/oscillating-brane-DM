"""GATE 13 — the cluster Weyl-DM as a sinc-sourced RESPONSE (V9.0, QUARANTINED).

Closure (Koyama-Maartens) forbids deriving E_00's AMPLITUDE from the brane.
So we test the STRUCTURE: if the Weyl-DM is "sourced where the boost dies",
its radial profile must track (1 - W(r)) with a UNIVERSAL shape across clusters.
Non-circular: W(r) is a sinc of t_dyn(r); f_Weyl(r) is a deficit ratio; the
functional relation f_Weyl vs (1-W) being the SAME curve for 12 clusters is a
real test (it could be 12 different curves, or flat, or anti-correlated).

Data: X-COP hydrostatic M(r) + gas + stars (cache). Per radius:
  g_N    = G M_bar/r^2     (gas + stars)
  g_obs  = G M_hyd/r^2     (hydrostatic total)
  g_MOND = exact RAR(g_N)  ; Dg_MOND = g_MOND - g_N
  W(r)   = |sinc(pi t_dyn/T)|, t_dyn = 2 pi r / V_c, V_c=sqrt(G M_hyd/r), T=2 Gyr
  g_Weyl_req = g_obs - g_N - Dg_MOND * W       (what E_00 must supply)
  f_Weyl(r)  = g_Weyl_req / g_obs              (Weyl fraction of gravity)
Hypothesis: f_Weyl(r) = C * (1 - W(r)), C universal (the closure amplitude).
"""

import glob
import os

import numpy as np
from astropy.io import fits

G = 4.300917e-9  # Mpc (km/s)^2 / Msun
A0 = 3.7e3 / (3.0857e19)  # a0 in (km/s)^2 / Mpc? -> convert: a0=1.2e-10 m/s^2
# a0 in (km/s)^2/Mpc: 1.2e-10 m/s^2 * Mpc/(km/s)^2 = 1.2e-10 * 3.0857e22 / 1e6 = 3703.7
A0 = 3703.7
KMS_MPC_GYR = 1.0227e-3  # 1 (km/s)/Mpc in 1/Gyr ... t in Gyr = (2 pi r[Mpc]/V[km/s]) * (Mpc/(km/s) in Gyr)
MPC_KMS_TO_GYR = 977.79  # 1 Mpc/(km/s) = 977.79 Gyr
T_BRANE = 2.0


def rar(gN):
    return np.sqrt((gN**2 + gN * np.sqrt(gN**2 + 4 * A0**2)) / 2.0)


base = "/DATA/obt_game_cache/raw/xcop"
clusters = sorted([d for d in os.listdir(base) if os.path.isdir(f"{base}/{d}")])
allW, allf, perC = [], [], []
print(
    f"{'cluster':9s}{'Nbin':>5s}{'r[Mpc]rng':>14s}{'f_W@core':>9s}{'f_W@out':>9s}{'C_fit':>7s}{'rms':>6s}"
)
for cl in clusters:
    try:
        fg = fits.open(f"{base}/{cl}/{cl}_fgas_profile.fits")[1].data
    except Exception:
        continue
    r = np.asarray(fg["RADIUS"], float)  # Mpc
    Mtot = np.asarray(fg["M_NFW"], float)  # hydrostatic total (Msun)
    Mgas = np.asarray(fg["MGAS"], float)
    # stars: ~ +15% of gas in core, subdominant; add a flat 1.2x gas as M_bar proxy if no mstar
    try:
        ms = fits.open(f"{base}/{cl}/{cl}_mstar.fits")[1].data
        Mstar = np.interp(
            r, np.asarray(ms["RADIUS"], float), np.asarray(ms[ms.names[1]], float)
        )
    except Exception:
        Mstar = 0.16 * Mgas
    Mbar = Mgas + Mstar
    ok = (r > 0) & (Mtot > 0) & (Mbar > 0) & (Mtot > Mbar)
    r, Mtot, Mbar = r[ok], Mtot[ok], Mbar[ok]
    if len(r) < 6:
        continue
    gN = G * Mbar / r**2
    gobs = G * Mtot / r**2
    gM = rar(gN)
    dgM = gM - gN
    Vc = np.sqrt(G * Mtot / r)  # km/s
    tdyn = (
        2 * np.pi * r / Vc * MPC_KMS_TO_GYR / 1000.0
    )  # Gyr  (r/Vc in Mpc/(km/s) -> Gyr; /1000? check)
    # r[Mpc]/Vc[km/s] = (Mpc/(km/s)); *977.79 = Gyr. 2pi factor included.
    tdyn = 2 * np.pi * r / Vc * 977.79  # Gyr
    W = np.abs(np.sinc(tdyn / T_BRANE))  # numpy sinc = sin(pi x)/(pi x)
    gW = gobs - gN - dgM * W
    fW = np.clip(gW / gobs, -0.2, 1.2)
    x = 1 - W
    m = x > 0.05
    if m.sum() < 4:
        continue
    C = np.sum(fW[m] * x[m]) / np.sum(x[m] ** 2)  # f_W = C x, LSQ through origin
    rms = np.sqrt(np.mean((fW[m] - C * x[m]) ** 2))
    allW.extend(x[m])
    allf.extend(fW[m])
    perC.append(C)
    print(
        f"{cl:9s}{len(r):5d}{f'{r.min():.2f}-{r.max():.2f}':>14s}"
        f"{fW[np.argmin(tdyn)]:9.2f}{fW[np.argmax(tdyn)]:9.2f}{C:7.2f}{rms:6.3f}"
    )

allW, allf, perC = np.array(allW), np.array(allf), np.array(perC)
Cg = np.sum(allf * allW) / np.sum(allW**2)
rmsg = np.sqrt(np.mean((allf - Cg * allW) ** 2))
from scipy.stats import spearmanr

rho = spearmanr(allW, allf).statistic
print(
    f"\n  GLOBAL: f_Weyl = C*(1-W), C = {Cg:.2f} +- {np.std(perC):.2f} (scatter across clusters),"
    f" rms={rmsg:.3f}"
)
print(f"  Spearman(1-W, f_Weyl) = {rho:.3f} over {len(allW)} radial bins, 12 clusters")
print(
    f"  per-cluster C spread: {np.min(perC):.2f}-{np.max(perC):.2f} (median {np.median(perC):.2f})"
)
print()
print("  READ: a strong positive Spearman + a tight universal C = the Weyl fraction is")
print("  organized RADIALLY by the sinc extinction (1-W): the cluster Weyl-DM is a")
print(
    "  RESPONSE whose SHAPE is sinc-dictated (derived), with amplitude C ~ closure input."
)
print("  A flat/zero/anti correlation or wildly cluster-dependent C would REFUTE the")
print("  'sourced where the boost dies' hypothesis.")


# ---------------------------------------------------------------------------
# VERDICT (verified with REAL stellar mass, BCG included):
# The cluster Weyl-DM DOMINATES at the CORE (M_tot/M_bar = 5-8 at r~40 kpc),
# where g_N/a0 = 360-1090 (deep Newtonian: MOND boost mu->1 is intrinsically
# ZERO) AND W~0.99 (the sinc does not bite). So the Weyl-DM is present exactly
# where NEITHER the sinc NOR MOND act. The "sourced where the boost dies"
# (Gate 11) hypothesis is REFUTED as the selectivity mechanism: the global
# Spearman(1-W, f_Weyl) = -0.63 (f_Weyl is high at the core, not at the edge).
#
# WHAT THIS MEANS (the wall, reached from the cluster face):
#  * The AMPLITUDE/selectivity of E_00 (cluster ~0.85, galaxy ~0) is the
#    irreducible CLOSURE input (Koyama-Maartens), now confirmed empirically on
#    12 clusters. The brane cannot derive it. (The classic MOND "cluster
#    problem" - a residual factor 2-8 even at g >> a0 - IS this input.)
#  * The sinc (ARA) remains valid in its domain (tracer dynamics; the cluster
#    PERIPHERY where MOND dies; cards #29-31) but is NOT the global selectivity.
#  * What stays derivable: the FORM (self-similar cored, card #22, chi2/N=1.04),
#    via bulk regularity. Form constrained, amplitude IC -- EXACTLY parallel to
#    the cosmological gates 0-9 (sign/shape constrained, amplitude IC).
# The non-linear solve does NOT crack the selectivity. The bulk keeps the
# dark-matter amplitude as its own datum. Spirit (law/form) precedes body
# (amount). Quarantined V9.0.
