#!/usr/bin/env python3
"""
wb_pipeline.py — wide-binary kinematic pipeline for the OBT-Game (CHERCHEUR mode).

GOAL (Stage-1+2 of the game on REAL data): from the El-Badry+2021 Gaia eDR3 wide-binary
catalogue, build, per binary, the quantities needed to confront OBT's low-acceleration
prediction with the observed sky-plane relative velocity — and to test the EXTERNAL patch
(hidden-triple fraction). It writes a clean per-binary lot to /DATA for `inspect`/`propagate`.

This is a TOOL (reviewer-mode build). It computes facts; the player (chercheur Claude)
judges. Method follows Chae 2023 / Pittordis-Sutherland conventions:
  - clean sample cuts: good parallax S/N, small parallax error, RUWE<1.4 (triple-clean),
    distance < 200 pc (so plane-of-sky velocities are well measured), sep in [1,30] kAU.
  - masses from absolute G via a simple main-sequence M_G -> mass relation (Pecaut-Mamajek-ish
    polynomial); flagged approximate — only used for the Newtonian scale, not a final result.
  - v_sky: relative proper motion (mas/yr) -> km/s using distance; this is the velocity that,
    for a bound Keplerian pair, scales as sqrt(G M / r) (times a projection factor).
  - Newtonian benchmark v_N = sqrt(G M_tot / r_proj); ratio  v_ratio = v_sky / v_N.
    OBT (mu(x), a0, with Milky-Way EFE) predicts an EXCESS (boost) of v_ratio at low
    acceleration (large sep); Newtonian predicts a sep-independent distribution.
NOTE: v_sky uses projected separation and 2D rel. p.m. — it is a STATISTICAL proxy (as in
the literature), not a per-system orbit solution. Facts are distributional; judging is mine.
"""

import os
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore")

RAW = "/DATA/obt_game_cache/raw/elbadry2021.fits.gz"
OUT = "/DATA/obt_game_cache/lots/wb_clean.parquet"

# physical constants (CODATA via astropy if available, else literals)
try:
    import astropy.units as u
    import astropy.constants as const
    G = const.G.value
    MSUN = const.M_sun.value
    AU = u.au.to(u.m)
    PC = u.pc.to(u.m)
    YR = u.yr.to(u.s)
except Exception:
    G, MSUN, AU, PC, YR = 6.674e-11, 1.989e30, 1.495978707e11, 3.0856775814913673e16, 3.1557e7
A0 = 1.0422e-10  # OBT a0 = cH0/2pi (m/s^2), from obt_formulas


def mass_from_MG(MG):
    """Very rough main-sequence mass (Msun) from absolute Gaia G magnitude. Monotonic
    decreasing; calibrated loosely to Pecaut-Mamajek (G~4.7->1 Msun, ~8->0.6, ~10->0.4).
    APPROXIMATE — sets only the Newtonian scale; flagged, not a final science number."""
    # piecewise-ish smooth fit; clip to plausible MS range
    m = 10 ** (0.0725 * (4.8 - MG))   # ~1 Msun at MG=4.8, slope ~ MS M-L
    return np.clip(m, 0.08, 3.0)


def main(nmax=None):
    from astropy.io import fits
    import pandas as pd

    if not os.path.exists(RAW):
        print(f"FATAL: catalogue not found {RAW}")
        sys.exit(2)
    print(f"[wb] reading {RAW} ...")
    with fits.open(RAW, memmap=True) as h:
        d = h[1].data
        cols = ("sep_AU", "parallax1", "parallax2", "parallax_error1", "parallax_error2",
                "pmra1", "pmra2", "pmdec1", "pmdec2",
                "pmra_error1", "pmra_error2", "pmdec_error1", "pmdec_error2",
                "ruwe1", "ruwe2", "phot_g_mean_mag1", "phot_g_mean_mag2")
        df = pd.DataFrame({c: np.array(d[c], dtype=float) for c in cols})
    print(f"[wb] {len(df):,} rows loaded")

    # --- clean sample cuts (triple-clean, good astrometry, nearby) ---
    plx = df["parallax1"]
    dist_pc = 1000.0 / plx                       # pc (parallax in mas)
    sn1 = df["parallax1"] / df["parallax_error1"]
    sn2 = df["parallax2"] / df["parallax_error2"]
    sel = (
        (df["ruwe1"] < 1.4) & (df["ruwe2"] < 1.4) &        # triple-clean (single-star astrometry)
        (sn1 > 20) & (sn2 > 20) &                          # good parallax S/N
        (plx > 5) &                                        # distance < 200 pc
        (df["sep_AU"] > 1e3) & (df["sep_AU"] < 3e4) &      # 1-30 kAU (the MOND-transition band)
        np.isfinite(df["pmra1"]) & np.isfinite(df["pmra2"]) &
        np.isfinite(df["pmdec1"]) & np.isfinite(df["pmdec2"]) &
        np.isfinite(df["phot_g_mean_mag1"]) & np.isfinite(df["phot_g_mean_mag2"])
    )
    df = df[sel].copy()
    dist_pc = dist_pc[sel]
    print(f"[wb] {len(df):,} after clean cuts (RUWE<1.4, plx S/N>20, d<200pc, sep 1-30 kAU)")

    # --- masses from absolute G ---
    MG1 = df["phot_g_mean_mag1"] + 5 * np.log10(df["parallax1"] / 100.0)  # M = m + 5 log10(plx_mas/100)
    MG2 = df["phot_g_mean_mag2"] + 5 * np.log10(df["parallax2"] / 100.0)
    m1 = mass_from_MG(MG1)
    m2 = mass_from_MG(MG2)
    Mtot = m1 + m2

    # --- relative sky-plane velocity from proper motions ---
    dpm_ra = df["pmra1"] - df["pmra2"]            # mas/yr
    dpm_dec = df["pmdec1"] - df["pmdec2"]
    dpm = np.sqrt(dpm_ra**2 + dpm_dec**2)         # mas/yr
    # mas/yr * distance(pc) -> km/s :  v = 4.74 * mu(arcsec/yr) * d(pc); mu in arcsec = mas/1000
    v_sky = 4.74047 * (dpm / 1000.0) * dist_pc    # km/s
    # error on dpm (quadrature) -> v error
    dpm_err = np.sqrt(df["pmra_error1"]**2 + df["pmra_error2"]**2 +
                      df["pmdec_error1"]**2 + df["pmdec_error2"]**2)
    v_sky_err = 4.74047 * (dpm_err / 1000.0) * dist_pc

    # --- Newtonian benchmark velocity at projected separation ---
    r = df["sep_AU"].values * AU
    v_N = np.sqrt(G * Mtot.values * MSUN / r) / 1e3   # km/s
    g_int = G * Mtot.values * MSUN / r**2             # internal accel (m/s^2)
    x = g_int / A0                                    # acceleration parameter

    out = df[["sep_AU", "ruwe1", "ruwe2"]].copy()
    out["dist_pc"] = dist_pc.values
    out["Mtot"] = Mtot.values
    out["x_acc"] = x                # g_int/a0 : >>1 Newtonian, <<1 deep-MOND
    out["v_sky"] = v_sky.values
    out["v_sky_err"] = v_sky_err.values
    out["v_N"] = v_N
    out["v_ratio"] = v_sky.values / v_N            # ~1 Newtonian bound; OBT predicts excess at low x
    out["v_snr"] = v_sky.values / np.maximum(v_sky_err.values, 1e-9)

    if nmax:
        out = out.iloc[:nmax]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    out.to_parquet(OUT, index=False)
    print(f"[wb] wrote {len(out):,} clean binaries -> {OUT}")

    # quick facts (no conclusion)
    for lo, hi, lab in [(3, 1e9, "Newtonian x>3"), (0.3, 3, "transition 0.3<x<3"), (0, 0.3, "deep-MOND x<0.3")]:
        m = (out["x_acc"] >= lo) & (out["x_acc"] < hi) & (out["v_snr"] > 2)
        if m.sum() > 5:
            print(f"  [{lab:18s}] N={m.sum():6d}  median v_ratio={out.loc[m,'v_ratio'].median():.2f}")
    print("[wb] DONE (facts only; classification is the player's).")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else None
    main(n)
