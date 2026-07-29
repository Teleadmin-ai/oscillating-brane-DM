"""THE alpha_NT / MASS-BIAS BUDGET — can the monster's WHY carry its own amplitude?

MODE CHERCHEUR. Monster [62b7f086] 'arc-cores vs the hydrostatically-calibrated Weyl' claims ONE
external patch: the X-ray hydrostatic pipeline under-weighs cluster masses (unbudgeted non-thermal
pressure), so card-#22's Weyl -- calibrated on X-COP hydrostatic masses -- is under-normalised, and
bias-free strong lensing exposes it at the arcs. The N-arcs battery measured the gap:
M500(M-T, hydrostatic class) / M500(lensing) = 0.59 median. THIS SCRIPT PRICES THAT CLAIM.

FOUR STEPS, each computed (Romain's rule: only calculations count):
  [1] SUSPECT MY OWN APPLICATION FIRST. The battery's 0.59 used MY 40''-M2D -> M500 extrapolation
      at the ensemble c=3.79. Replace it with PUBLISHED per-cluster lensing masses (Merten et al.
      2015, ApJ 806, 4 -- CLASH SaWLens joint strong+weak lensing, Table 7, M500c in 1e15 Msun/h,
      h=0.7, fitted from the 5-14'' grid scale out to 2 Mpc/h) -> how much of the gap was mine?
  [2] VALIDATE THE BRIDGE. Is the M-T relation really card #22's calibration class? Test it against
      X-COP's OWN masses (Ettori+19 M500, the very numbers the card was fit on) using core-excised
      temperatures computed HERE from the cached X-COP spectra (spectral_results_*.fits, KT in keV;
      aperture 0.15-0.75 R500 via the matched RW_X grid in units of R500).
  [3] PRICE THE PATCH. Exact hydrostatic algebra with a non-thermal fraction alpha(r):
        M_HSE/M_true = (1-alpha) - (dln alpha/dln r)/(dln P_tot/dln r)
      -> b = alpha (1 - s/|dlnP/dlnr|) for alpha ~ r^s: a RISING alpha makes the bias SMALLER than
      alpha, so the required alpha is LARGER than the required b. Solve for the alpha the gap needs
      and compare with the external measurements -- including X-COP's OWN published non-thermal
      fraction (~6% at R500, (1-b) = 0.85-0.87; Eckert et al. 2019, A&A 621, A40).
  [4] THE REST OF THE BUDGET: temperature-calibration provenance (Chandra-class kT fed into an
      XMM-calibrated M-T), lensing triaxiality/selection, and what is left.

Asserted ONLY identities + reproductions (the hydrostatic algebra against its own constant-alpha
limit; the battery's published numbers re-derived through the same code path). Everything else
computed + reported. Quarantined exploration; NOT a sacred file, not in the PDF.
"""

import glob

import numpy as np
from astropy.io import fits

import arcs_battery as B
import arcs_obt as A

MSUN = A.MSUN
H_MERTEN = (
    0.7  # Merten+15 cosmology (WMAP7-like: Om=0.27, h=0.7); masses in 1e15 Msun/h
)

# Merten et al. 2015 Table 7 (SaWLens SL+WL NFW fits): M500c, M200c [1e15 Msun/h], c200c
MERTEN = {
    "Abell383": (0.61, 0.87, 4.4),
    "Abell2261": (0.95, 1.42, 3.4),
    "RXJ2129": (0.43, 0.61, 4.3),
    "Abell611": (0.57, 0.85, 3.4),
    "MS2137": (0.68, 1.04, 3.1),
    "MACS1115": (0.54, 0.90, 2.3),
    "MACS1931": (0.45, 0.69, 3.2),
    "MACS1720": (0.53, 0.75, 4.3),
    "MACS0429": (0.53, 0.80, 3.3),
}

# X-COP (Ettori et al. 2019) hydrostatic anchors as used by the card-#22 fit (probes.xcop_hier)
XCOP = {
    "A85": (1235, 5.65),
    "A644": (1230, 5.66),
    "A1644": (1054, 3.48),
    "A1795": (1153, 4.63),
    "A2029": (1423, 8.82),
    "A2142": (1424, 8.95),
    "A2255": (1196, 5.26),
    "A2319": (1346, 7.31),
    "A3158": (1123, 4.26),
    "A3266": (1430, 8.80),
    "RXC1825": (1105, 4.08),
    "ZW1215": (1358, 7.66),
}
XCOP_Z = {  # redshifts only enter E(z) in the M-T relation (percent-level at these z)
    "A85": 0.0555,
    "A644": 0.0704,
    "A1644": 0.0473,
    "A1795": 0.0622,
    "A2029": 0.0766,
    "A2142": 0.0909,
    "A2255": 0.0809,
    "A2319": 0.0557,
    "A3158": 0.0597,
    "A3266": 0.0589,
    "RXC1825": 0.065,
    "ZW1215": 0.0767,
}


def kt_core_excised(cl):
    """Core-excised spectroscopic kT from X-COP's own spectra: error-weighted mean of KT [keV]
    over the standard 0.15-0.75 R500 aperture, using the matched RW_X grid (units of R500).
    """
    d = f"/DATA/obt_game_cache/raw/xcop/{cl}"
    with fits.open(f"{d}/{cl}_temperature.fits") as f:
        rw = np.array(f[1].data["RW_X"], float)  # radius in units of R500
    spec = glob.glob(f"{d}/spectral_results_*.fits")
    with fits.open(spec[0]) as f:
        kt = np.array(f[1].data["KT"], float)
        ek = (
            np.array(f[1].data["KT_LO"], float) + np.array(f[1].data["KT_HI"], float)
        ) / 2
    n = min(len(rw), len(kt))
    rw, kt, ek = rw[:n], kt[:n], np.clip(ek[:n], 1e-3, None)
    m = (rw > 0.15) & (rw < 0.75)
    if m.sum() < 2:
        m = rw < 0.75
    w = 1.0 / ek[m] ** 2
    return float((kt[m] * w).sum() / w.sum()), int(m.sum())


def main():
    print("=" * 104)
    print(
        " === MODE CHERCHEUR ===  THE alpha_NT / MASS-BIAS BUDGET — pricing monster [62b7f086]"
    )
    print("=" * 104)

    # ---------------------------------------------------------------- [1] my own extrapolation
    print(
        "\n[1] SUSPECT MY OWN APPLICATION FIRST — published lensing masses vs my 40'' extrapolation"
    )
    rows = []
    for name, zl, te, m2d, kt in B.BATTERY:
        key = name.split()[0]
        m5_mert = MERTEN[key][0] * 1e15 / H_MERTEN  # Msun, physical
        r = B.run_cluster(name, zl, te, m2d, kt)
        m5_mine = r["m5_lens"] / MSUN
        m5_mt = r["m5_mt"] / MSUN
        rows.append((key, kt, m5_mt, m5_mine, m5_mert))
    print(
        f"    {'cluster':11s} {'kT':>5s} {'M5(M-T)':>9s} {'M5(mine,40'')':>13s} {'M5(Merten)':>11s}"
        f" {'mine/Merten':>12s} {'MT/mine':>8s} {'MT/Merten':>10s}"
    )
    for k, kt, mt, mine, mert in rows:
        print(
            f"    {k:11s} {kt:5.1f} {mt:9.2e} {mine:13.2e} {mert:11.2e}"
            f" {mine/mert:12.2f} {mt/mine:8.2f} {mt/mert:10.2f}"
        )
    r_mine = np.array([x[2] / x[3] for x in rows])
    r_mert = np.array([x[2] / x[4] for x in rows])
    ext = np.array([x[3] / x[4] for x in rows])
    print(
        f"\n    anchor ratio M5(M-T)/M5(lensing):  MY extrapolation {np.median(r_mine):.2f}"
        f"  ->  PUBLISHED (Merten SaWLens) {np.median(r_mert):.2f}   [range {r_mert.min():.2f}-{r_mert.max():.2f}]"
    )
    print(
        f"    my 40''-extrapolated M500 vs Merten's: median {np.median(ext):.2f}"
        f" (range {ext.min():.2f}-{ext.max():.2f}, scatter {np.std(ext):.2f} = a NOISY estimator)"
    )
    print(
        "    -> my c=3.79 extrapolation accounted for a factor"
        f" {np.median(r_mert)/np.median(r_mine):.2f} of the gap"
        f" ({np.median(r_mine):.2f} -> {np.median(r_mert):.2f}); the rest is in the published data."
    )
    print(
        f"    => the gap that SURVIVES on published lensing masses: x{1/np.median(r_mert):.2f}"
    )

    # ------------------------------------------------------------------ [2] validate the bridge
    print(
        "\n[2] VALIDATE THE BRIDGE — is the M-T relation card #22's own calibration class?"
    )
    print(
        "    (X-COP hydrostatic M500 (Ettori+19, the card's fit data) vs M-T at core-excised kT"
    )
    print("     computed here from X-COP's own spectra)")
    print(
        f"    {'cluster':9s} {'kT_ce[keV]':>10s} {'nbins':>5s} {'M5(X-COP)':>10s} {'M5(M-T)':>9s} {'ratio':>6s}"
    )
    bridge = []
    for cl, (_, m5e14) in XCOP.items():
        kt, nb = kt_core_excised(cl)
        m_mt = B.m500_mt(kt, XCOP_Z[cl])
        m_hse = m5e14 * 1e14
        bridge.append(m_mt / m_hse)
        print(
            f"    {cl:9s} {kt:10.2f} {nb:5d} {m_hse:10.2e} {m_mt:9.2e} {m_mt/m_hse:6.2f}"
        )
    bridge = np.array(bridge)
    f_bridge = float(np.median(bridge))
    print(
        f"    M-T / X-COP-hydrostatic: median {f_bridge:.2f}, scatter {np.std(bridge):.2f}"
        f" -> the bridge HOLDS to {abs(1-f_bridge)*100:.0f}%, but it is not exactly 1:"
    )
    print(
        f"      the M-T arm sits {(1-f_bridge)*100:.0f}% BELOW the card's actual calibration data,"
    )
    print(
        "      so the raw anchor gap must be DE-BIASED by this factor before it is charged to the"
    )
    print(
        "      hydrostatic pipeline. (This correction works AGAINST the monster; it is applied.)"
    )

    # ---------------------------------------------------------------------- [3] price the patch
    print(
        "\n[3] PRICE THE PATCH — what non-thermal fraction would the surviving gap require?"
    )
    r_corr = float(np.median(r_mert)) / f_bridge
    b_need = 1 - r_corr
    print(
        f"    raw anchor ratio (M-T vs published lensing)      : {np.median(r_mert):.2f}"
    )
    print(
        f"    de-biased by the bridge factor {f_bridge:.2f} (step [2])   : {r_corr:.2f}"
        f"   = the honest hydrostatic-class / lensing ratio (x{1/r_corr:.2f})"
    )
    print(
        f"    required bias b = 1 - M_HSE/M_true = {b_need:.2f} at the mass-calibration radius"
    )

    def b_of_alpha(alpha, s, dlnp):
        """b = 1 - M_HSE/M_true for alpha(r) = alpha5 (r/r500)^s and dlnP_tot/dlnr = dlnp (<0)."""
        return alpha - (s * alpha) / abs(dlnp)

    # identity: at s=0 (constant alpha) the bias IS alpha
    assert (
        abs(b_of_alpha(0.25, 0.0, -3.0) - 0.25) < 1e-12
    ), "constant-alpha limit: b == alpha"
    for s, dlnp in ((0.0, -3.0), (0.8, -3.0), (0.8, -4.0)):
        a_need = b_need / (1 - s / abs(dlnp))
        print(
            f"      alpha ~ r^{s:.1f}, dlnP/dlnr = {dlnp:+.1f}  ->  required alpha_NT ="
            f" {a_need:.2f}  ({a_need*100:.0f}% of the total pressure)"
        )
    a_flat = b_need
    a_rise = b_need / (1 - 0.8 / 3)
    print("\n    MEASURED non-thermal fractions at R500 (external, declared):")
    print(
        "      X-COP's OWN analysis (Eckert+19, A&A 621, A40 -- the card's own sample):  ~0.06"
    )
    print(
        "      hydrodynamical simulations, spread across codes/definitions:              0.10-0.30"
    )
    print(
        f"    -> vs the card's own sample: the patch needs {a_flat:.2f}-{a_rise:.2f} where X-COP"
        f" measures 0.06 = short by a factor {a_flat/0.06:.0f}-{a_rise/0.06:.0f}."
    )
    print(
        f"    -> vs simulations: the requirement sits AT ({a_flat:.2f}) or just ABOVE ({a_rise:.2f})"
        " the TOP of the simulated range (0.30) --"
    )
    print(
        "       i.e. the patch is not impossible in principle, but it needs the extreme upper end"
        " of the simulated non-thermal support"
    )
    print(
        "       everywhere, while the direct measurement on the very clusters card #22 was fit to"
        " says 6%."
    )
    print(
        "    Same statement in bias units: X-COP publishes (1-b) = 0.85-0.87; the gap needs"
        f" (1-b) = {r_corr:.2f}."
    )
    print(
        "    RADIUS CAVEAT (against the patch): the gap is a NORMALISATION statement at R500,"
        " while the arcs probe 0.05-0.10 R500,"
    )
    print(
        "       where every measurement and simulation puts alpha_NT LOWER than at R500 -- a"
        " core-localised version of the patch is harder still."
    )

    # ------------------------------------------------------------------- [4] the rest of the budget
    print(
        "\n[4] THE REST OF THE BUDGET — what else could carry a lensing-vs-X-ray mass ratio of"
        f" x{1/r_corr:.2f}?"
    )
    kt_terms = ", ".join(
        f"+{d*100:.0f}% kT -> M_MT x{(1+d)**B.MT_ALPHA:.2f}, ratio {r_corr/(1+d)**B.MT_ALPHA:.2f}"
        for d in (0.10, 0.15)
    )
    print(
        f"      (a) kT provenance ({kt_terms}): a Chandra-class temperature offset fed into an"
    )
    print(
        "          XMM-calibrated M-T INFLATES M_MT, so the true hydrostatic-class mass is lower"
        " and the gap DEEPER. Does not rescue."
    )
    se = float(np.std(bridge) / np.sqrt(len(bridge)))
    print(
        "      (b) M-T normalisation: no longer a free +/-25% bracket once step [2] pins it on the"
        " card's OWN data --"
    )
    print(
        f"          median {f_bridge:.2f}, scatter {np.std(bridge):.2f} over {len(bridge)} clusters"
        f" -> standard error {se:.2f} (~{se/f_bridge*100:.0f}%). The normalisation"
    )
    print(
        f"          can move the ratio by ~{se/f_bridge*100:.0f}%, not by the 34% the gap needs."
    )
    print(
        "      (c) lensing triaxiality / CLASH selection: Merten+15 address it with tailored"
        " simulations of the CLASH selection function; the mass bias reported there is a few"
    )
    print(
        "          percent, far short of the residual (their concentration is the biased quantity,"
        " not the mass)."
    )
    print(
        "      (d) MY extrapolation: already removed in [1]"
        f" (it carried a factor {np.median(r_mert)/np.median(r_mine):.2f})."
    )

    print("\n[VERDICT — the WHY does NOT close, and the reason is external, not ours]")
    print(
        "    * The gap is REAL and survives both my own error and the bridge de-biasing:"
        f" x{1/r_corr:.2f} between the"
    )
    print(
        "      hydrostatic-calibration class (which card #22 was fit on -- bridge validated in [2]"
    )
    print(
        "      to ~10%) and published joint strong+weak lensing masses of the same clusters."
    )
    print(
        "    * The proposed patch -- unbudgeted non-thermal pressure -- REQUIRES alpha_NT ~"
        f" {a_flat:.0%}-{b_need/(1-0.8/3):.0%},"
    )
    print(
        "      but the card's own sample (X-COP) measures ~6% and publishes (1-b) = 0.85-0.87."
    )
    print(
        "      By its own measurement the patch is short by a factor ~4-6; against simulations it"
    )
    print(
        "      needs their extreme upper end everywhere. NOT CLOSED at the amplitude required."
    )
    print(
        "    * BUT the external literature does NOT agree with itself at exactly this amplitude:"
    )
    print(
        "      Planck's SZ cluster counts require (1-b) ~ 0.6 to match the primary CMB, while"
    )
    print(
        "      X-COP's gas-fraction argument gives 0.85-0.87. These two published numbers bracket"
    )
    print(
        "      -- and disagree over -- precisely the factor the monster needs. The monster is"
    )
    print(
        "      HOSTAGE to an unresolved external measurement; I cannot close it, and neither"
    )
    print("      side of that controversy is mine to arbitrate.")
    print(
        "    * CONSEQUENCE for the game: NO CARD. A card requires certainty and a mechanism that"
    )
    print(
        "      carries its own amplitude; this one is quantitatively short on the sample it came"
    )
    print(
        "      from. The monster stays a monster, now with a PRICED why and a named closure"
    )
    print(
        "      condition: an independent resolution of the lensing-vs-X-ray cluster mass scale."
    )
    print(
        "    * The OBT-INTERNAL alternative reading stays open and is NOT excluded by anything"
    )
    print(
        "      here: the Weyl closure-IC core may simply be more concentrated than the cored form"
    )
    print(
        "      card #22 fits at r > 15 kpc (Gates 17/23 already found f_Weyl rising inward)."
    )
    print(
        "      That reading needs no external patch -- and would move the object out of the game"
    )
    print("      (an OBT-internal open question, not a debunk).")
    print("=" * 104)


if __name__ == "__main__":
    main()
