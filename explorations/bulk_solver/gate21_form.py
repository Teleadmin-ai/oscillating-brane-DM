"""GATE 21 — the FORM over 5 decades: power law or transition? (V9.0, QUARANTINED)
Combine galaxies (SPARC, f_Weyl~0 anchor) + groups (Lagana) + clusters (X-COP hydro,
CCCP lensing). Same definition f_Weyl = 1 - g_MOND/g_obs (full MOND, W=1) at the
characteristic radius. Plot f_Weyl(M_bar) over M_bar ~ 1e9-1e15 and test:
single power law f_Weyl ~ M_bar^s, OR a transition (flat ~0 for galaxies then rising)?
The galaxy anchor at f_Weyl~0 is the discriminant: a power law extrapolated down must
hit ~0 at galaxy masses, or there's an extra suppression/threshold.
"""
import csv
import os
import re

import numpy as np
from astropy.io import fits

G = 4.300917e-9; Gk = 4.300917e-6; A0 = 3.702e6; A0k = 3702.0
def rar(g, a): return np.sqrt((g**2 + g*np.sqrt(g**2 + 4*a*a))/2.0)
def norm(s): return re.sub(r'[^a-z0-9]', '', s.lower())

M, F, K = [], [], []   # log10 M_bar, f_Weyl, kind

# galaxies SPARC (outer point)
glx = {}
for ln in open("/DATA/obt_game_cache/raw/sparc_massmodels.mrt"):
    p = ln.split()
    if len(p) < 8: continue
    try: R,V,eV,vg,vd,vb=(float(p[i]) for i in (2,3,4,5,6,7))
    except: continue
    if R>0 and V>0: glx.setdefault(p[0],[]).append((R,V,eV,vg,vd,vb))
for g,a in glx.items():
    R,V,eV,vg,vd,vb=sorted(a)[-1]
    if eV/V>0.1: continue
    vb2=vg*abs(vg)+0.5*vd**2+0.7*vb**2
    if vb2<=0: continue
    gN=vb2/R; gobs=V*V/R
    Mb=vb2*R/Gk    # Msun (kpc,km/s)
    M.append(np.log10(Mb)); F.append(1-rar(gN,A0k)/gobs); K.append("galaxy")

# groups Lagana (r500)
for row in csv.DictReader(open("/DATA/obt_game_cache/raw/groups/lagana13.csv")):
    r=float(row["r500"]); Mt=float(row["Mt500"])*1e13; Mb=(float(row["Mg500"])+float(row["Ms500"]))*1e12
    gN=Gk*Mb/r**2; gobs=Gk*Mt/r**2
    M.append(np.log10(Mb)); F.append(1-rar(gN,A0k)/gobs); K.append("group")

# clusters X-COP (last bin)
base="/DATA/obt_game_cache/raw/xcop"
for cl in sorted(os.listdir(base)):
    p=f"{base}/{cl}/{cl}_fgas_profile.fits"
    if not os.path.exists(p): continue
    fg=fits.open(p)[1].data
    r=np.asarray(fg["RADIUS"],float);Mt=np.asarray(fg["M_NFW"],float);Mg=np.asarray(fg["MGAS"],float)
    try:
        ms=fits.open(f"{base}/{cl}/{cl}_mstar.fits")[1].data
        Ms=np.interp(r,np.asarray(ms["RADIUS"],float),np.asarray(ms["MSTAR"],float))
    except: Ms=0.16*Mg
    ok=(r>0)&(Mt>0); Mb=(Mg+Ms)[ok][-1]; Mt2=Mt[ok][-1]; rr=r[ok][-1]
    gN=G*Mb/rr**2; gobs=G*Mt2/rr**2
    M.append(np.log10(Mb)); F.append(1-rar(gN,A0)/gobs); K.append("cluster")

# clusters CCCP (lensing, r500WL)
kT={}
for ln in open("/DATA/obt_game_cache/raw/groups/cccp/table1.tex"):
    if '&' not in ln or '\\\\' not in ln: continue
    c=[x.strip() for x in ln.split('&')]
    if len(c)>=10 and not c[0].startswith('\\'):
        m=re.search(r'([\d.]+)',c[-1])
        if m: kT[norm(c[0])]=1
for ln in open("/DATA/obt_game_cache/raw/groups/cccp/table2.tex"):
    if '&' not in ln or '\\\\' not in ln or 'colhead' in ln: continue
    c=[x.strip() for x in ln.split('&')]
    if len(c)<5: continue
    def v(s):
        m=re.search(r'([\d.]+)\s*\\pm\s*([\d.]+)',s) or re.search(r'([\d.]+)',s)
        return float(m.group(1)) if m else None
    r5,Mwl,Mg=v(c[1]),v(c[2]),v(c[3])
    if None in (r5,Mwl,Mg): continue
    Mb=1.15*Mg*1e14; Mt=Mwl*1e14
    gN=G*Mb/r5**2; gobs=G*Mt/r5**2
    M.append(np.log10(Mb)); F.append(1-rar(gN,A0)/gobs); K.append("cluster_WL")

M,F,K=np.array(M),np.array(F),np.array(K)
print(f"N={len(M)} systems, M_bar range {M.min():.1f}-{M.max():.1f} dex (={M.max()-M.min():.1f} decades)\n")
print(f"  {'logM_bar bin':>14s}{'N':>5s}{'med f_Weyl':>12s}{'kinds':>22s}")
edges=np.arange(8.5,15.1,0.7)
cen,med=[],[]
for lo,hi in zip(edges[:-1],edges[1:]):
    m=(M>=lo)&(M<hi)
    if m.sum()<2: continue
    kk=",".join(sorted(set(k.split('_')[0] for k in K[m])))
    print(f"  {f'{lo:.1f}-{hi:.1f}':>14s}{m.sum():5d}{np.median(F[m]):12.3f}{kk:>22s}")
    cen.append((lo+hi)/2); med.append(np.median(F[m]))
cen,med=np.array(cen),np.array(med)

print("\nFORM TEST:")
# power-law fit on detected (f>0.03) systems
det=F>0.03
s,ic=np.polyfit(M[det],np.clip(F[det],0.03,None),1) if det.sum()>5 else (np.nan,np.nan)
# Better: fit log f vs log M on binned detected
bdet=med>0.03
sl,icl=np.polyfit(cen[bdet],np.log10(med[bdet]),1)
print(f"  power law f_Weyl ~ M_bar^{sl:.2f} (binned, detected)")
gal=np.median(F[K=='galaxy'])
pred_gal=10**(sl*np.median(M[K=='galaxy'])+icl)
print(f"  galaxies: observed f_Weyl = {gal:+.3f} ; power-law EXTRAPOLATION predicts {pred_gal:+.3f}")
if pred_gal < 0.05:
    print("  -> power law extrapolates to ~0 at galaxy masses: SINGLE POWER LAW consistent, NO threshold")
else:
    print("  -> power law over-predicts galaxies: a THRESHOLD/extra suppression is needed below groups")
print("\n  transition test: lowest M_bar where median f_Weyl departs from 0:")
for c0,m0 in zip(cen,med):
    flag="<-- departs" if m0>0.08 else ""
    print(f"    logM_bar={c0:.1f}: f_Weyl={m0:+.3f} {flag}")
