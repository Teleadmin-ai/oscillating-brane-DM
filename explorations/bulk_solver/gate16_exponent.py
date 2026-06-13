"""GATE 16 — the deflection law: exponent + primary variable (V9.0, QUARANTINED).
Accumulate the simplest clue: M_Weyl (residual beyond FULL MOND) vs candidate
primary variables |Phi|, V_c, M_bar, M_tot. Which is tightest? What exponent?
A simple exponent + a tight variable points at the brane-deflection mechanism.
Groups (Lagana13) + clusters (X-COP), the Weyl-detected systems (N~21).
"""
import csv
import os

import numpy as np
from astropy.io import fits
from scipy.stats import spearmanr

Gk = 4.300917e-6; GM = 4.300917e-9
A0k = 3702.0; A0M = 3.702e6
def rar(g, a): return np.sqrt((g**2 + g*np.sqrt(g**2 + 4*a*a))/2.0)

sys = []  # dict per system: Vc, Mbar, Mtot, Mweyl, Phi, kind
# groups
for row in csv.DictReader(open("/DATA/obt_game_cache/raw/groups/lagana13.csv")):
    r=float(row["r500"]); Mt=float(row["Mt500"])*1e13
    Mb=(float(row["Mg500"])+float(row["Ms500"]))*1e12
    gN=Gk*Mb/r**2; gobs=Gk*Mt/r**2
    Mmond=Mb*rar(gN,A0k)/gN
    Mw=Mt-Mmond
    Vc=np.sqrt(Gk*Mt/r)
    Phi=Vc**2*(1+np.log(5))  # NFW-ish |Phi(r500)| ~ Vc^2 (1+ln c), c~5
    sys.append(dict(Vc=Vc,Mbar=Mb,Mtot=Mt,Mweyl=max(Mw,1e9),Phi=Phi,kind="group"))
# clusters: integrate |Phi| = int g dr properly
base="/DATA/obt_game_cache/raw/xcop"
for cl in sorted(os.listdir(base)):
    p=f"{base}/{cl}/{cl}_fgas_profile.fits"
    if not os.path.exists(p): continue
    fg=fits.open(p)[1].data
    r=np.asarray(fg["RADIUS"],float); Mt=np.asarray(fg["M_NFW"],float); Mg=np.asarray(fg["MGAS"],float)
    try:
        ms=fits.open(f"{base}/{cl}/{cl}_mstar.fits")[1].data
        Ms=np.interp(r,np.asarray(ms["RADIUS"],float),np.asarray(ms["MSTAR"],float))
    except: Ms=0.16*Mg
    ok=(r>0)&(Mt>0)&(Mg+Ms>0); r,Mt,Mb=r[ok],Mt[ok],(Mg+Ms)[ok]
    g=GM*Mt/r**2
    Phi=np.trapezoid(g,r)+g[-1]*r[-1]   # |Phi(0)| ~ int_0^rmax g dr + tail
    i=-1
    gN=GM*Mb[i]/r[i]**2; gobs=g[i]
    Mmond=Mb[i]*rar(gN,A0M)/gN
    Mw=Mt[i]-Mmond
    Vc=np.sqrt(GM*Mt[i]/r[i])
    sys.append(dict(Vc=Vc,Mbar=Mb[i],Mtot=Mt[i],Mweyl=max(Mw,1e9),Phi=Phi,kind="cluster"))

import numpy as np
Vc=np.array([s["Vc"] for s in sys]); Mb=np.array([s["Mbar"] for s in sys])
Mt=np.array([s["Mtot"] for s in sys]); Mw=np.array([s["Mweyl"] for s in sys])
Phi=np.array([s["Phi"] for s in sys])
fW=Mw/Mt
print(f"N = {len(sys)} (Weyl-detected: groups + clusters)")
print("\nLog-log regression  log M_Weyl = q*log X + const  (which X is primary?):")
for name,X in [("V_c",Vc),("|Phi|",Phi),("M_bar",Mb),("M_tot",Mt)]:
    lx,ly=np.log10(X),np.log10(Mw)
    q,c=np.polyfit(lx,ly,1)
    resid=ly-(q*lx+c)
    scat=np.std(resid)
    rho=spearmanr(X,Mw).statistic
    print(f"  vs {name:6s}: exponent q = {q:+.2f}  scatter = {scat:.3f} dex  Spearman={rho:+.2f}")
print("\nf_Weyl = M_Weyl/M_tot vs well depth:")
for name,X in [("V_c",Vc),("|Phi|",Phi)]:
    q,c=np.polyfit(np.log10(X),fW,1)  # f_W linear in log(well)
    print(f"  f_Weyl vs log {name}: slope = {q:+.3f} per dex  (f_W rises with depth)")
print(f"\n  median f_Weyl: groups={np.median(fW[:9]):.2f}  clusters={np.median(fW[9:]):.2f}")
print("\n  READ: the TIGHTEST variable (smallest scatter) = the primary driver;")
print("  a SIMPLE exponent (1, 4/3, 2...) points at the deflection law. M_bar would")
print("  mean 'Weyl tracks baryons' (a mass effect); |Phi|/V_c would mean 'Weyl tracks")
print("  well DEPTH' (a deflection effect) -- the discriminating clue.")
