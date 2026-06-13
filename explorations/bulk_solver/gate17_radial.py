"""GATE 17 — radial disentangler: does the Weyl density track BARYONS or DEPTH?
(V9.0, QUARANTINED). Whole-system points are degenerate (kT-M_bar is a tight 1D
sequence, Spearman 0.93). The disentangler is the RADIAL profile within clusters,
where rho_bar(r) [steep] and |Phi(r)| [flat/deep] have OPPOSITE shapes.

Per cluster, per radius: rho_bar(r)=(1/4pi r^2)dM_bar/dr (local baryon density),
rho_Weyl(r)=(1/4pi r^2)dM_Weyl/dr with M_Weyl=M_tot - M_bar*nu(g_N) [full MOND],
|Phi(r)| from the potential. Test: is rho_Weyl/rho_bar constant (tracks baryons,
a local mass/source effect) or rising outward (more extended -> tracks depth/
global potential, a deflection effect)?  And the log-slopes: gamma_Weyl vs
gamma_bar.
"""
import os

import numpy as np
from astropy.io import fits

GM = 4.300917e-9; A0M = 3.702e6
def rar(g, a): return np.sqrt((g**2 + g*np.sqrt(g**2 + 4*a*a))/2.0)

base = "/DATA/obt_game_cache/raw/xcop"
ratios_in, ratios_out, sl_w, sl_b = [], [], [], []
allr_norm, allratio = [], []
for cl in sorted(os.listdir(base)):
    p = f"{base}/{cl}/{cl}_fgas_profile.fits"
    if not os.path.exists(p): continue
    fg = fits.open(p)[1].data
    r = np.asarray(fg["RADIUS"], float); Mt = np.asarray(fg["M_NFW"], float); Mg = np.asarray(fg["MGAS"], float)
    try:
        ms = fits.open(f"{base}/{cl}/{cl}_mstar.fits")[1].data
        Ms = np.interp(r, np.asarray(ms["RADIUS"], float), np.asarray(ms["MSTAR"], float))
    except Exception:
        Ms = 0.16*Mg
    ok = (r > 0) & (Mt > 0) & (Mg+Ms > 0) & np.isfinite(Mt)
    r, Mt, Mb = r[ok], Mt[ok], (Mg+Ms)[ok]
    if len(r) < 12: continue
    gN = GM*Mb/r**2
    Mmond = Mb*rar(gN, A0M)/gN
    Mw = Mt - Mmond
    # local densities via dM/dr (log-spaced, smooth)
    def dens(M):
        dM = np.gradient(M, r)
        return dM/(4*np.pi*r**2)
    rho_b = dens(Mb); rho_w = dens(Mw)
    good = (rho_b > 0) & (rho_w > 0)
    rg, rwb = r[good], (rho_w/rho_b)[good]
    if good.sum() < 8: continue
    r500 = r[-1]/1.0  # last bin ~ r500-ish
    # ratio at inner third vs outer third
    n=len(rg)
    ratios_in.append(np.median(rwb[:n//3])); ratios_out.append(np.median(rwb[-n//3:]))
    # log-slopes (outer half, where profiles are clean)
    h=slice(n//2,n)
    sw=np.polyfit(np.log(rg[h]), np.log(rho_w[good][h]),1)[0]
    sb=np.polyfit(np.log(rg[h]), np.log(rho_b[good][h]),1)[0]
    sl_w.append(sw); sl_b.append(sb)
    for rr,rat in zip(rg/r500, rwb):
        allr_norm.append(rr); allratio.append(rat)

ri,ro=np.array(ratios_in),np.array(ratios_out)
print(f"N clusters = {len(ri)}")
print(f"rho_Weyl/rho_bar  inner third: median = {np.median(ri):.2f}")
print(f"rho_Weyl/rho_bar  outer third: median = {np.median(ro):.2f}")
print(f"  -> ratio rises outward by factor {np.median(ro)/np.median(ri):.1f}"
      f"  ({'Weyl MORE EXTENDED than baryons' if np.median(ro)>np.median(ri)*1.3 else 'tracks baryons'})")
print(f"\nlog-density slopes (outer half):")
print(f"  baryons gamma_bar = {np.median(sl_b):+.2f}  (steep)")
print(f"  Weyl    gamma_Weyl= {np.median(sl_w):+.2f}  ({'SHALLOWER = more extended' if np.median(sl_w)>np.median(sl_b) else 'similar'})")
print(f"  Delta(gamma) = {np.median(sl_w)-np.median(sl_b):+.2f}")
print()
print("INTERPRETATION:")
print("  rho_Weyl tracks rho_bar (constant ratio, equal slopes) => MASS/local-source effect.")
print("  rho_Weyl more extended (rising ratio, shallower slope)  => DEPTH/global-potential")
print("  effect (the brane-deflection picture): the Weyl is sourced by the WELL, not the")
print("  local baryon density -> it pools where |Phi| is deep, smeared over the whole halo.")
