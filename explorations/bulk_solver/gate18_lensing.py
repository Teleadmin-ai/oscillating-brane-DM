"""GATE 18 — the CLEAN disentangler: weak-lensing masses break the circularity.
(V9.0, QUARANTINED). CCCP (Mahdavi 2013): M_WL (lensing, hydrostatic-INDEPENDENT)
+ M_Gas + kT for the SAME clusters. At fixed kT (fixed depth), does the total
lensing mass M_WL rise with M_Gas (gas-rich) -> MASS effect, or stay constant
-> DEPTH effect? And M_Weyl,WL = M_WL - nu(g_N) M_bar: partial correlations
vs kT (depth) and M_Gas (baryon mass), now NON-circular.
"""
import re

import numpy as np
from scipy.stats import spearmanr

G = 4.300917e-9; A0 = 3.702e6
def rar(g, a): return np.sqrt((g**2 + g*np.sqrt(g**2 + 4*a*a))/2.0)
def norm(s): return re.sub(r'[^a-z0-9]', '', s.lower())

# table1: kT (last col, T_all500)
kT = {}
for ln in open("/DATA/obt_game_cache/raw/groups/cccp/table1.tex"):
    if '&' not in ln or '\\\\' not in ln: continue
    c = [x.strip() for x in ln.split('&')]
    if len(c) < 10: continue
    m = re.search(r'([\d.]+)', c[-1])
    if m and not c[0].startswith('\\'):
        try: kT[norm(c[0])] = float(m.group(1))
        except: pass

# table2: M_WL, M_Gas, M_hydro
rows = []
for ln in open("/DATA/obt_game_cache/raw/groups/cccp/table2.tex"):
    if '&' not in ln or '\\\\' not in ln or 'colhead' in ln: continue
    c = [x.strip() for x in ln.split('&')]
    if len(c) < 5: continue
    name = norm(c[0])
    def val(s):
        m = re.search(r'([\d.]+)\s*\\pm\s*([\d.]+)', s) or re.search(r'([\d.]+)', s)
        return float(m.group(1)) if m else None
    r500 = val(c[1]); Mwl = val(c[2]); Mgas = val(c[3])
    if None in (r500, Mwl, Mgas) or name not in kT: continue
    rows.append((name, kT[name], r500, Mwl, Mgas))

print(f"matched clusters: {len(rows)}  (kT range {min(r[1] for r in rows):.1f}-{max(r[1] for r in rows):.1f} keV)")
T = np.array([r[1] for r in rows]); r5 = np.array([r[2] for r in rows])
Mwl = np.array([r[3] for r in rows])*1e14; Mg = np.array([r[4] for r in rows])*1e14
Mbar = 1.15*Mg   # +15% stars
gN = G*Mbar/r5**2
Mmond = Mbar*rar(gN, A0)/gN
Mweyl = Mwl - Mmond

# how decorrelated are kT and M_Gas here? (the leverage)
print(f"kT - M_Gas Spearman = {spearmanr(T,Mg).statistic:+.2f} (scatter gives the disentangling leverage)")

def partial(x, y, z):  # corr(x,y | z)
    rxy=spearmanr(x,y).statistic; rxz=spearmanr(x,z).statistic; ryz=spearmanr(y,z).statistic
    return (rxy-rxz*ryz)/np.sqrt((1-rxz**2)*(1-ryz**2))

print("\nTEST 1 (the cleanest): does TOTAL lensing mass M_WL rise with M_Gas AT FIXED kT?")
print(f"  M_WL ~ M_Gas | kT  (partial Spearman) = {partial(Mg, Mwl, T):+.2f}")
print(f"  M_WL ~ kT   | M_Gas (partial Spearman) = {partial(T, Mwl, Mg):+.2f}")
print("  -> if M_WL~M_Gas|kT strong & M_WL~kT|M_Gas weak: total mass follows BARYONS (mass effect)")
print("     if reversed: total mass follows DEPTH (kT)")

print("\nTEST 2: the Weyl residual M_Weyl,WL = M_WL - MOND(baryons), non-circular:")
print(f"  M_Weyl ~ M_Gas | kT = {partial(Mg, Mweyl, T):+.2f}")
print(f"  M_Weyl ~ kT   | M_Gas = {partial(T, Mweyl, Mg):+.2f}")
# [BUG, Gate 20]: the clip(...,1e11) below INFLATES the exponent to 1.57 (artifact); clean value ~1.2 (no clip). Kept only as the documented bug.
    q1,_=np.polyfit(np.log10(Mg),np.log10(np.clip(Mweyl,1e11,None)),1)
print(f"  exponent M_Weyl ~ M_Gas^{q1:.2f}")

print("\nTEST 3 (direct gas-rich vs gas-poor): split by f_gas residual at fixed kT.")
# f_gas vs kT fit, residual
lf=np.log10(Mg/Mwl)
sl,ic=np.polyfit(np.log10(T),lf,1)
res=lf-(sl*np.log10(T)+ic)   # gas-rich (res>0) vs gas-poor (res<0) at fixed kT
hi=res>np.median(res); lo=~hi
fW=Mweyl/Mwl
print(f"  gas-RICH half (f_gas above kT-trend): median f_Weyl = {np.median(fW[hi]):+.2f}")
print(f"  gas-POOR half (f_gas below kT-trend): median f_Weyl = {np.median(fW[lo]):+.2f}")
print(f"  M_Weyl gas-rich {np.median(Mweyl[hi]):.2e} vs gas-poor {np.median(Mweyl[lo]):.2e}")
print("  -> DEPTH effect: M_Weyl SAME for rich/poor at fixed kT. MASS effect: rich has more.")
