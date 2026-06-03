#!/usr/bin/env python3
"""Full hierarchical-style per-RC EFE MCMC (reproduction of Chae 2020) for the OBT-Game.
Per galaxy: marginalize (Ydisk, Ygas, [Ybul], Dhat, i, e) with Chae's priors; recover the
e posterior. SEP test = does the RC-inferred e_free track the INDEPENDENT environmental e_env?
Run: python efe_mcmc_run.py [validate|all]
"""

import json
import sys

import emcee
import numpy as np
import pandas as pd

LOTS = "/DATA/obt_game_cache/lots"
T1 = "/DATA/obt_game_cache/raw/sparc_table1.mrt"
KPC = 3.0856775814913673e19
KMS = 1.0e3
A0 = 1.2e-10
EF = json.load(
    open("/DATA/obt_game_cache/raw/chae_efield.json")
)  # name -> [e_fit, e_env]

# SPARC table1: D, eD, Inc, eInc
TAB = {}
for ln in open(T1):
    p = ln.split()
    if len(p) >= 19 and p[0][0].isalpha():
        try:
            TAB[p[0]] = (float(p[2]), float(p[3]), float(p[5]), float(p[6]))
        except ValueError:
            pass

DF = pd.read_parquet(f"{LOTS}/sparc_rar.parquet")


def nu_e(z, e):
    e = max(e, 0.0)
    Ae = e * (1 + e / 2) / (1 + e)
    Be = 1 + e
    t = 0.5 - Ae / z
    return t + np.sqrt(t * t + Be / z)


def make_logpost(g, D, eD, Inc, eInc, fix_e=None):
    R = g.R_kpc.values * KPC
    Vobs = g.Vobs.values
    eV = np.maximum(g.eVobs.values, 2.0)
    Vd2 = g.Vdisk.values**2
    Vb2 = g.Vbul.values**2
    Vg = g.Vgas.values
    hasbul = np.any(Vb2 > 0)
    sDhat = np.log10(1 + eD / max(D, 1e-3))
    iobs = Inc
    sig_i = max(eInc, 2.0)
    # param order: log10Ydisk, log10Ygas, [log10Ybul], log10Dhat, i, [e]
    idx = {"yd": 0, "yg": 1}
    k = 2
    if hasbul:
        idx["yb"] = k
        k += 1
    idx["Dh"] = k
    k += 1
    idx["i"] = k
    k += 1
    if fix_e is None:
        idx["e"] = k
        k += 1
    ndim = k

    def lp(p):
        yd = 10 ** p[idx["yd"]]
        yg = 10 ** p[idx["yg"]]
        yb = 10 ** p[idx["yb"]] if hasbul else 0.7
        Dh = 10 ** p[idx["Dh"]]
        i = p[idx["i"]]
        e = fix_e if fix_e is not None else p[idx["e"]]
        if not (0 < e < 0.5) and fix_e is None:
            return -np.inf
        if not (5.0 < i < 90.0):
            return -np.inf
        Vbar2 = Dh * (yd * Vd2 + yb * Vb2 + yg * Vg * np.abs(Vg))
        if np.any(Vbar2 <= 0):
            return -np.inf
        gbar = Vbar2 * KMS**2 / R
        z = gbar / A0
        Vmod = np.sqrt(nu_e(z, e)) * np.sqrt(Vbar2)
        fac = np.sin(np.radians(iobs)) / np.sin(np.radians(i))
        Vrot = Vobs * fac
        sig = eV * fac
        chi2 = np.sum(((Vrot - Vmod) / sig) ** 2)
        pri = ((p[idx["yd"]] - np.log10(0.5)) / 0.1) ** 2
        pri += ((p[idx["yg"]] - 0.0) / 0.1) ** 2
        if hasbul:
            pri += ((p[idx["yb"]] - np.log10(0.7)) / 0.1) ** 2
        pri += (p[idx["Dh"]] / sDhat) ** 2
        pri += ((i - iobs) / sig_i) ** 2
        return -0.5 * (chi2 + pri)

    p0 = np.zeros(ndim)
    p0[idx["yd"]] = np.log10(0.5)
    p0[idx["i"]] = iobs
    if fix_e is None:
        p0[idx["e"]] = 0.03
    return lp, ndim, idx, p0, iobs, sig_i, sDhat, hasbul


def fit_galaxy(name, nwalk=24, nstep=1500, burn=600):
    g = DF[DF.ID == name].sort_values("R_kpc")
    if len(g) < 5 or name not in TAB:
        return None
    D, eD, Inc, eInc = TAB[name]
    lp, ndim, idx, p0, iobs, sig_i, sDhat, hasbul = make_logpost(g, D, eD, Inc, eInc)
    rng = np.random.default_rng(42)
    scale = np.full(ndim, 0.03)
    scale[idx["i"]] = max(sig_i * 0.3, 1.0)
    pos = p0 + scale * rng.standard_normal((nwalk, ndim))
    pos[:, idx["i"]] = np.clip(pos[:, idx["i"]], 6, 89)
    if "e" in idx:
        pos[:, idx["e"]] = np.clip(np.abs(pos[:, idx["e"]]), 1e-3, 0.45)
    s = emcee.EnsembleSampler(nwalk, ndim, lp)
    s.run_mcmc(pos, nstep, progress=False)
    ch = s.get_chain(discard=burn, flat=True)
    e_post = ch[:, idx["e"]]
    return float(np.median(e_post)), float(np.std(e_post)), len(g)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "validate"
    if mode == "validate":
        for nm in ["NGC5055", "NGC5033", "NGC0247", "NGC1090", "NGC6674", "DDO154"]:
            if nm in EF:
                r = fit_galaxy(nm)
                if r:
                    print(
                        f"{nm:10s} e_free={r[0]:.3f}+-{r[1]:.3f}  e_env={EF[nm][1]:.3f}  N={r[2]}"
                    )
                else:
                    print(f"{nm:10s} (skip)")
            else:
                print(f"{nm:10s} not in e_env table")
    else:
        out = {}
        names = [n for n in EF if n in set(DF.ID.unique())]
        for j, nm in enumerate(names):
            r = fit_galaxy(nm)
            if r:
                out[nm] = {"e_free": r[0], "e_err": r[1], "e_env": EF[nm][1], "N": r[2]}
            if (j + 1) % 20 == 0:
                print(f"  ... {j+1}/{len(names)}", flush=True)
        json.dump(out, open("/DATA/obt_game_cache/raw/efe_mcmc_results.json", "w"))
        d = pd.DataFrame(out).T
        from scipy.stats import spearmanr

        rho, p = spearmanr(d.e_env, d.e_free)
        print(
            f"\nDONE {len(d)} galaxies. median e_free={d.e_free.median():.3f}, e_env={d.e_env.median():.3f}"
        )
        print(f"Spearman(e_env, e_free) = {rho:+.3f} (p={p:.2e})")
