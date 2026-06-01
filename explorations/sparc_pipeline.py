#!/usr/bin/env python3
"""
sparc_pipeline.py — SPARC rotation-curve pipeline for the OBT-Game (CHERCHEUR mode).

The SIMPLE, low-noise system to understand the WHY of the wide-binary monster: same
low-acceleration regime (g ~ a0) but velocities ~10-100 km/s measured to a few km/s
(~100x cleaner than wide-binary proper motions). If OBT's boost is real, it must appear
here cleanly — and the SPARC radial-acceleration relation (RAR) is exactly that test.

Per data point: g_bar = V_bar^2/R (V_bar^2 = Vgas^2 + ML*Vdisk^2 + ML*Vbul^2, ML=0.5 at 3.6um),
g_obs = V_obs^2/R. OBT predicts the exact RAR  g_obs = sqrt((g_bar^2 + g_bar*sqrt(g_bar^2
+ 4 a0^2))/2)  with a0 = cH0/2pi (no free parameter). We write a per-point lot to /DATA and
report the FACT: how well OBT's RAR matches, vs Newton (g_obs=g_bar), across the g_bar range.
Facts only; the player judges.
"""

import os
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore")

RAW = "/DATA/obt_game_cache/raw/sparc_massmodels.mrt"
OUT = "/DATA/obt_game_cache/lots/sparc_rar.parquet"
A0 = 1.0422e-10            # OBT a0 = cH0/2pi (m/s^2)
KPC = 3.0856775814913673e19  # m
KMS = 1.0e3
ML = 0.5                  # disk M/L at 3.6um (standard SPARC value)


def obt_rar(g_bar, a0=A0):
    """Exact OBT radial-acceleration relation g_obs(g_bar)."""
    return np.sqrt((g_bar**2 + g_bar*np.sqrt(g_bar**2 + 4*a0**2)) / 2.0)


def main():
    import pandas as pd
    if not os.path.exists(RAW):
        print(f"FATAL: {RAW} missing"); sys.exit(2)

    rows = []
    with open(RAW) as f:
        started = False
        for ln in f:
            if ln.startswith("--------") :
                started = True if "CamB" not in ln else started
            # data lines: start with a galaxy id (non-space) and have many numeric fields
            parts = ln.split()
            if len(parts) >= 9 and parts[0][0].isalpha() is False:
                pass
            # robust: a data row has >=9 fields and parts[1] parses as float (distance)
            if len(parts) >= 9:
                try:
                    float(parts[1]); float(parts[2]); float(parts[3])
                except ValueError:
                    continue
                gid = parts[0]
                D, R, Vobs, eVobs, Vgas, Vdisk, Vbul = (float(parts[i]) for i in range(1, 8))
                rows.append((gid, D, R, Vobs, eVobs, Vgas, Vdisk, Vbul))
    df = pd.DataFrame(rows, columns=["ID", "D", "R_kpc", "Vobs", "eVobs", "Vgas", "Vdisk", "Vbul"])
    print(f"[sparc] {len(df):,} data points, {df['ID'].nunique()} galaxies")

    R = df["R_kpc"].values * KPC
    Vbar2 = (df["Vgas"]**2 + ML*df["Vdisk"]**2 + ML*df["Vbul"]**2).values * KMS**2  # (m/s)^2
    Vobs = df["Vobs"].values * KMS
    g_bar = Vbar2 / R
    g_obs = Vobs**2 / R
    g_obt = obt_rar(g_bar)
    g_newton = g_bar

    out = df.copy()
    out["g_bar"] = g_bar
    out["g_obs"] = g_obs
    out["g_obt"] = g_obt
    out["x_acc"] = g_bar / A0
    out["ratio_obs_newton"] = g_obs / g_newton            # >1 = the "missing gravity" boost
    out["ratio_obs_obt"] = g_obs / g_obt                  # ~1 if OBT's RAR is right
    # keep finite, physical points with a real velocity error
    out = out[np.isfinite(out["ratio_obs_obt"]) & (out["eVobs"] > 0) & (g_bar > 0)]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    out.to_parquet(OUT, index=False)
    print(f"[sparc] wrote {len(out):,} points -> {OUT}")

    print("\nFACT — boost g_obs/g_Newton vs acceleration regime (same regimes as wide binaries):")
    for lo, hi, lab in [(3, 1e9, "Newton x>3"), (0.3, 3, "trans 0.3<x<3"), (0, 0.3, "deepMOND x<0.3")]:
        m = (out["x_acc"] >= lo) & (out["x_acc"] < hi)
        if m.sum() > 5:
            print(f"  [{lab:16s}] N={m.sum():5d}  median g_obs/g_N={out.loc[m,'ratio_obs_newton'].median():.2f}"
                  f"   median g_obs/g_OBT={out.loc[m,'ratio_obs_obt'].median():.3f}")
    # global: how tight is OBT's RAR?
    r = out["ratio_obs_obt"]
    print(f"\nOBT RAR fit (g_obs/g_OBT): median={r.median():.3f}, "
          f"16-84%=[{r.quantile(.16):.2f},{r.quantile(.84):.2f}]  (1.0 = OBT exact, no free param)")
    print("[sparc] DONE (facts only; classification is the player's).")


if __name__ == "__main__":
    main()
