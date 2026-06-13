"""GATE 20 — CONSOLIDATION: stress-test the Gates 13-19 clues, try to BREAK them.
(V9.0, QUARANTINED). Pillar = Gate 18 (lensing: mass not depth, super-linear).
Mistrust checks: (1) is "M_WL~M_Gas|kT" just kT being a noisy mass proxy? Control
ALSO for M_hydro (another total-mass proxy) — does M_Gas keep predictive power?
(2) bootstrap the partials. (3) is the super-linear exponent robust to M_star and cuts?
(4) internal consistency of the four exponents.
"""

import re

import numpy as np
from scipy.stats import spearmanr

G = 4.300917e-9
A0 = 3.702e6


def rar(g, a):
    return np.sqrt((g**2 + g * np.sqrt(g**2 + 4 * a * a)) / 2.0)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


kT = {}
for ln in open("/DATA/obt_game_cache/raw/groups/cccp/table1.tex"):
    if "&" not in ln or "\\\\" not in ln:
        continue
    c = [x.strip() for x in ln.split("&")]
    if len(c) < 10:
        continue
    m = re.search(r"([\d.]+)", c[-1])
    if m and not c[0].startswith("\\"):
        try:
            kT[norm(c[0])] = float(m.group(1))
        except:
            pass
rows = []
for ln in open("/DATA/obt_game_cache/raw/groups/cccp/table2.tex"):
    if "&" not in ln or "\\\\" not in ln or "colhead" in ln:
        continue
    c = [x.strip() for x in ln.split("&")]
    if len(c) < 5:
        continue
    name = norm(c[0])

    def val(s):
        m = re.search(r"([\d.]+)\s*\\pm\s*([\d.]+)", s) or re.search(r"([\d.]+)", s)
        return float(m.group(1)) if m else None

    r500, Mwl, Mgas, Mhy = val(c[1]), val(c[2]), val(c[3]), val(c[4])
    if None in (r500, Mwl, Mgas, Mhy) or name not in kT:
        continue
    rows.append((kT[name], r500, Mwl, Mgas, Mhy))
T = np.array([r[0] for r in rows])
r5 = np.array([r[1] for r in rows])
Mwl = np.array([r[2] for r in rows])
Mg = np.array([r[3] for r in rows])
Mhy = np.array([r[4] for r in rows])
print(f"N={len(rows)} clusters with kT,r500,M_WL,M_Gas,M_hydro\n")


def resid(y, X):  # linear regression residual of log y on log X columns
    ly = np.log10(y)
    A = np.column_stack([np.log10(x) for x in X] + [np.ones(len(y))])
    co, _, _, _ = np.linalg.lstsq(A, ly, rcond=None)
    return ly - A @ co


def pcorr_multi(a, b, controls):  # partial Spearman of a,b given controls (log-linear)
    ra = resid(a, controls)
    rb = resid(b, controls)
    return spearmanr(ra, rb).statistic


print(
    "MISTRUST TEST 1 — is M_Gas just a mass proxy (kT noisy)? Control for M_hydro too:"
)
print(f"  M_WL ~ M_Gas | kT          = {pcorr_multi(Mg,Mwl,[T]):+.2f}   (Gate 18)")
print(
    f"  M_WL ~ M_Gas | M_hydro     = {pcorr_multi(Mg,Mwl,[Mhy]):+.2f}   (controls total-mass proxy)"
)
print(
    f"  M_WL ~ M_Gas | (kT,M_hydro)= {pcorr_multi(Mg,Mwl,[T,Mhy]):+.2f}   (controls BOTH mass proxies)"
)
print(
    f"  M_WL ~ kT    | (M_Gas)     = {pcorr_multi(T,Mwl,[Mg]):+.2f}   (does depth survive controlling gas?)"
)
print(
    "  READ: if M_Gas survives controlling M_hydro -> baryon-specific (real); if it vanishes ->"
)
print(
    "  M_Gas was a total-mass proxy (then result = 'Weyl tracks total mass, not depth' — still not depth)."
)

print("\nMISTRUST TEST 2 — bootstrap the key partials (1000 resamples):")
rng = np.random.default_rng(0)
for lab, fn in [
    ("M_WL~M_Gas|kT", lambda i: pcorr_multi(Mg[i], Mwl[i], [T[i]])),
    ("M_WL~kT|M_Gas", lambda i: pcorr_multi(T[i], Mwl[i], [Mg[i]])),
    ("M_WL~M_Gas|(kT,Mhy)", lambda i: pcorr_multi(Mg[i], Mwl[i], [T[i], Mhy[i]])),
]:
    bs = []
    for _ in range(1000):
        i = rng.integers(0, len(rows), len(rows))
        try:
            bs.append(fn(i))
        except:
            pass
    bs = np.array(bs)
    print(
        f"  {lab:22s}: {np.median(bs):+.2f}  [{np.percentile(bs,16):+.2f},{np.percentile(bs,84):+.2f}]"
    )

print("\nMISTRUST TEST 3 — super-linear exponent robustness (M_Weyl ~ M_Gas^q):")
for fstar, lab in [(0.0, "gas only"), (0.15, "+15% stars"), (0.30, "+30% stars")]:
    Mbar = (1 + fstar) * Mg
    gN = G * Mbar * 1e14 / r5**2
    Mw = Mwl - Mbar * rar(gN, A0) / gN
    ok = Mw > 0
    q, _ = np.polyfit(np.log10(Mbar[ok]), np.log10(Mw[ok]), 1)
    print(f"  {lab:12s}: q = {q:.2f}  (N={ok.sum()})")

print("\nINTERNAL CONSISTENCY of the four exponents:")
print("  local rho-rho 1.49 (G19, circ.) | radial slope 1.68 (G17, circ.) |")
print("  system M-M hydro 1.42 (G16) | system M-M LENSING 1.57 (G18, CLEAN)")
print("  -> all super-linear ~1.4-1.7; the clean non-circular one (lensing) = 1.57.")

# ---------------------------------------------------------------------------
# CONSOLIDATION VERDICT (mistrust paid off — a real bug caught):
#
# WHAT HOLDS (robust under stress-testing):
#  * MASS not depth: M_WL ~ M_Gas|kT = +0.66 [+0.55,+0.75] (bootstrap), survives
#    controlling M_hydro too (+0.70), while M_WL~kT|M_Gas = -0.24 (depth anti-, weak).
#    The Weyl-DM tracks MASS, not potential-well depth. SOLID. (Caveat: 'baryon-
#    specific vs total-mass' stays ambiguous — M_Gas is also the tightest M_500 proxy,
#    and the M_hydro control is contaminated by hydrostatic bias possibly gas-correlated.)
#  * NOT the sinc (Gate 13). SOLID.
#  * Amplitude = closure/IC. SOLID (multi-face: Gates 3-9 cosmology, 13-18 clusters).
#  * MODEST super-linearity: clean wide-range (no clip) M_Weyl ~ M_bar^1.19 [1.05,1.34]
#    -> f_Weyl rises ~M_bar^0.2 (groups 0.15 -> clusters 0.4, x2.8). q>1 but only just.
#
# WHAT WAS CORRECTED / FALLS (the bug):
#  * Gate 18's exponent 1.57 was a CLIP ARTIFACT (np.clip(Mweyl,1e11) inflates the
#    slope). Clean value: q~1.2 (wide range) / 0.79 (CCCP-only, narrow, ill-levered).
#  * Gate 19's "quadratic SMS p~1.5-2, FORM derived": NOT supported by the clean
#    exponent. q=1.19 is barely super-linear, much closer to LINEAR (1) than QUADRATIC
#    (2). The quadratic pi_munu remains the only nonlinear SMS term, but the data do
#    NOT confirm a quadratic exponent -> the mechanism's exact form is NOT pinned.
#  * Gate 19's local p=1.49 was circular (rho_Weyl from M_tot) + dM/dr-noisy.
#
# NET after consolidation: the SOLID accumulated clue is "Weyl-DM tracks baryonic
# MASS (not depth), with modest super-linearity q~1.2 and IC amplitude." The exact
# exponent and the quadratic-mechanism claim are WITHDRAWN/weakened. Do NOT take the
# last step (5D bulk solve) on a quadratic premise — the data only support a weakly
# super-linear mass-tracking, mechanism-form open. Mistrust before the leap: justified.
