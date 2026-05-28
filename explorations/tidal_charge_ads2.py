"""Maillon 1 & 2 verification: tidal-charge brane black hole.
f(r) = 1 - 2GM/r + q/r^2   (units GM=1, so r in units of GM, q = tidal charge)
Checks: horizon structure vs sign of q; extremality; near-horizon AdS2 x S2;
Hawking temperature T_H(q) and the collapse to 0 at extremality.
Known-case injections validate the T_H machinery before trusting conclusions.
"""
import numpy as np

def f(r, q):    return 1 - 2/r + q/r**2
def fp(r, q):   return 2/r**2 - 2*q/r**3        # f'(r)
def fpp(r, q):  return -4/r**3 + 6*q/r**4        # f''(r)

def horizons(q):
    disc = 1 - q                                  # r = 1 +/- sqrt(1-q)
    if disc < 0:  return []                        # naked singularity
    if disc == 0: return [1.0]                     # extremal double root
    return [r for r in (1-np.sqrt(disc), 1+np.sqrt(disc)) if r > 0]

def T_H(q):                                        # T = f'(r_h)/4pi (GM=1 units)
    hs = horizons(q)
    if not hs: return None
    return fp(max(hs), q)/(4*np.pi)

PASS, FAIL = "PASS", "**FAIL**"
print("="*68)
print("INJECTION / KNOWN CASES (validate before trusting)")
# Schwarzschild q=0: r_h=2, T_H = 1/(8pi)
TH0 = T_H(0.0); known = 1/(8*np.pi)
print(f"  [I0] Schwarzschild q=0: r_h={max(horizons(0.0)):.3f} (exp 2), "
      f"T_H={TH0:.6f} vs 1/(8pi)={known:.6f} -> {PASS if abs(TH0-known)<1e-9 else FAIL}")
# RN-like extremal q=1: r_h=1, T_H=0
print(f"  [I1] extremal q=1: horizons={horizons(1.0)} (exp [1.0]), "
      f"T_H={T_H(1.0):.2e} (exp 0) -> {PASS if abs(T_H(1.0))<1e-12 else FAIL}")
# naked q>1
print(f"  [I2] q=1.5: horizons={horizons(1.5)} (exp none) -> {PASS if horizons(1.5)==[] else FAIL}")

print("="*68)
print("MAILLON 1 — horizon structure vs tidal-charge SIGN")
print(f"  {'q':>7} | {'#horizons':>9} | {'r_h(outer)':>10} | {'extremal?':>9}")
for q in [-1.0,-0.5,0.0,0.5,0.9,1.0,1.5]:
    hs=horizons(q)
    nh=len(hs); rh=f"{max(hs):.3f}" if hs else "  --  "
    ext = "YES" if (len(hs)==1 and abs(q-1.0)<1e-9) else "no"
    print(f"  {q:7.2f} | {nh:9d} | {rh:>10} | {ext:>9}")
print("  -> q<0 (default braneworld sign): single horizon, NEVER extremal, no AdS2 throat")
print("  -> AdS2 throat requires q = +1 exactly (q = (GM)^2), positive & extremal")

print("="*68)
print("MAILLON 2 — near-horizon AdS2 x S2 at extremality (q=1)")
# f(r) = (1 - 1/r)^2 ; double root at r=1
r0 = 1.0
print(f"  f(1.01,1) = {f(1.01,1.0):.6e}  vs  (r-1)^2 = {(0.01)**2:.6e}  (quadratic touch)")
fpp_h = fpp(r0,1.0)
L_ads = np.sqrt(2.0/fpp_h)
print(f"  f''(r_h)={fpp_h:.4f} (exp 2)  ->  AdS2 radius L=sqrt(2/f'')={L_ads:.4f}, "
      f"S2 radius=r_h={r0:.4f}")
print(f"  -> near-horizon = AdS2({L_ads:.2f}) x S2({r0:.2f}): {PASS if abs(L_ads-1)<1e-9 else FAIL}")

print("="*68)
print("THE INTERNAL TENSION — T_H collapses as you approach the AdS2 throat")
print("  V8.2 treats PBH as Schwarzschild, T_H ~ 900 K (Hawking immunity + finite-T scrambling).")
print(f"  {'q':>8} | {'T_H/T_H(Schw)':>13} | {'~T_H [K] if Schw=900K':>22}")
for q in [0.0,0.5,0.9,0.99,0.999,0.99999,1.0]:
    th=T_H(q); ratio=th/TH0
    Tk = ratio*900
    print(f"  {q:8.5f} | {ratio:13.4f} | {Tk:22.2f}")
print("  -> a CLEAN AdS2 throat needs q->1 (extremal) => T_H->0, contradicting the 900 K /")
print("     fast-scrambler PBH that Gamma_rad = ln(S_BH)/2pi relies on. Same PBH can't be both.")
