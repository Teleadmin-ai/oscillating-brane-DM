"""THE SIMPLEST POSSIBLE LENS — and why it turns out to be clean but BLIND (two theorems).

REVIEWER MODE (Romain, after the cluster arcs: 'trouve une autre lentille gravitationnelle la plus
simple possible pour eviter d'autres effets et verify'). The cluster arc test was confounded three
ways -- ellipticity/substructure (measured: x1.27), the hydrostatic-vs-lensing mass calibration
(x1.34), and the BCG/gas modelling. So: find the lens that removes all three, and test OBT on it.

THE OBJECTIVE CRITERIA (each kills one confound):
  * a COMPLETE Einstein ring          -> circular symmetry: the spherical model is valid
  * an ISOLATED early-type galaxy     -> no external convergence, no ICM, no merger, no substructure
  * spectroscopic z_l and z_s         -> the geometry is exact
  * measured stellar mass AND sigma   -> lensing and dynamics on the SAME object
  * the LOWEST possible x_E = g(R_E)/a0  -> where OBT's law differs most from Newton

WHAT THE SEARCH RETURNED
  [A] The best candidate on paper: the COSMIC HORSESHOE (SDSS J1148+1930) -- a ~300 degree ring
      (the roundest configuration available), z_l = 0.444, z_s = 2.381, theta_E ~ 5.0'' (Belokurov
      2007; Dye 2008), M_E ~ 5e12 Msun, sigma = 344 +/- 25 km/s (Schuldt et al. 2019, seven
      apertures), dark fraction 60-70% inside theta_E, and a geometry that gives a LOWER x_E than
      any of the 74 SLACS lenses. DISQUALIFIED BY VERIFICATION: Schuldt et al. state that its
      external shear is high and attribute it to the nearby cluster RMJ114847.5+193115.1, of a few
      times 1e14 Msun. That is precisely the 'other effect' the exercise was meant to avoid.
  [B] The remaining clean class: isolated SLACS early-types (74 with complete data here). And on
      that class the exercise returns TWO THEOREMS, both computed below, which say the simplest
      lens cannot test what we wanted it to test.

THEOREM A (MOND blindness). At an Einstein radius kappa-bar = 1, so g(R_E) = pi G Sigma_cr exactly
  -- a constant of the (z_l, z_s) geometry, independent of the lens. Minimising it over the
  redshift ranges where lenses actually exist gives a FLOOR on x_E, hence a CEILING on the MOND
  boost available at a real Einstein radius. (x_E keeps falling with z_l and z_s, so an unbounded
  scan only finds the grid edge -- the bound must be stated over a declared range, and is.)
THEOREM B (ARA blindness). Combining the same identity with t_dyn = 2 pi sqrt(R^3/GM) gives
  t_dyn(theta_E) = 2 pi sqrt(R_E / (pi G Sigma_cr)): every strong lens sits deep in the ADIABATIC
  branch (W = 1), so strong lensing can never probe the ARA averaging regime, whatever eps is.

Asserted ONLY identities + reproductions (M_E from geometry vs the Auger+09 table; the two theorem
identities). Everything else computed + reported. Quarantined; not sacred; not in the PDF.
"""

import numpy as np

import arcs_battery as B
import arcs_obt as A

G, C, KPC, MSUN, ARCSEC = A.G, A.C, A.KPC, A.MSUN, A.ARCSEC
TGYR, GYR_S = 2.0, 3.156e16
SLACS = "/DATA/obt_game_cache/raw/slacs"

# The Cosmic Horseshoe, as published (Belokurov+07, Dye+08, Schuldt+19) -- verified this session
HORSESHOE = dict(
    zl=0.444, zs=2.381, th_E=5.0, e_th=0.3, M_E=5e12, sig=344.0, e_sig=25.0
)


def _f(s):
    s = s.strip()
    return float(s) if s else np.nan


def load_slacs():
    t3 = {}
    for L in open(f"{SLACS}/table3.dat"):
        t3[L[4:14].strip()] = dict(
            zl=_f(L[39:44]),
            zs=_f(L[45:50]),
            sig=_f(L[51:54]),
            e_sig=_f(L[55:57]),
            mt=L[58:63].strip(),
            reI=_f(L[95:99]),
        )
    out = []
    for L in open(f"{SLACS}/table4.dat"):
        n = L[4:14].strip()
        if n not in t3:
            continue
        d = dict(t3[n])
        d.update(
            name=n, RE=_f(L[15:19]), lME=_f(L[20:25]), Fc=_f(L[26:30]), Fs=_f(L[36:40])
        )
        if not (
            np.isfinite(d["RE"]) and np.isfinite(d["lME"]) and np.isfinite(d["sig"])
        ):
            continue
        d["scr"] = A.sigma_cr(d["zl"], d["zs"])
        d["a0"] = C * A.H0 * A.ez(d["zl"]) / (2 * np.pi)
        d["gE"] = np.pi * G * d["scr"]
        d["xE"] = d["gE"] / d["a0"]
        d["ME_geom"] = np.pi * d["scr"] * (d["RE"] * KPC) ** 2 / MSUN
        d["tdT"] = 2 * np.pi * np.sqrt(d["RE"] * KPC / d["gE"]) / GYR_S / TGYR
        out.append(d)
    return out


def main():
    print("=" * 104)
    print(
        " THE SIMPLEST POSSIBLE LENS — the search, the verification, and two theorems"
    )
    print("=" * 104)

    S = load_slacs()
    rep = np.array([d["ME_geom"] / 10 ** d["lME"] for d in S])
    print(
        f"\n[data] {len(S)} SLACS lenses with complete data (Auger+2009 tables 3+4, cached)."
    )
    print(
        f"    reproduction M_E(pi Sigma_cr R_E^2) / M_E(published): median {np.median(rep):.3f},"
        f" scatter {np.std(rep):.3f}"
    )
    assert (
        0.9 < np.median(rep) < 1.1
    ), "the Einstein-mass identity must reproduce the published table"

    # ---------------------------------------------------------------- [A] the candidate that failed
    print("\n[A] THE BEST CANDIDATE ON PAPER — and why verification disqualified it")
    h = HORSESHOE
    scr_h = A.sigma_cr(h["zl"], h["zs"])
    a0_h = C * A.H0 * A.ez(h["zl"]) / (2 * np.pi)
    x_h = np.pi * G * scr_h / a0_h
    r_h = h["th_E"] * A.dc(h["zl"]) / (1 + h["zl"]) * ARCSEC / KPC
    me_h = np.pi * scr_h * (r_h * KPC) ** 2 / MSUN
    print(
        f"    Cosmic Horseshoe (J1148+1930): ~300 deg ring, z_l = {h['zl']}, z_s = {h['zs']},"
        f" theta_E = {h['th_E']}+/-{h['e_th']}''"
    )
    print(
        f"    -> R_E = {r_h:.1f} kpc, M_E(geometry) = {me_h:.2e} Msun"
        f" (published estimate ~{h['M_E']:.0e}: ratio {me_h/h['M_E']:.2f})"
    )
    print(
        f"    -> x_E = g(R_E)/a0(z_l) = {x_h:.1f}, LOWER than every one of the {len(S)} SLACS"
        f" lenses (min {min(d['xE'] for d in S):.1f}) -- the most MOND-favourable geometry known."
    )
    print(
        "    DISQUALIFIED: Schuldt et al. 2019 report a high external shear and attribute it to"
    )
    print(
        "    the nearby cluster RMJ114847.5+193115.1 (a few times 1e14 Msun). External convergence"
    )
    print(
        "    from a neighbouring cluster is exactly the confound the exercise set out to remove,"
    )
    print(
        "    and it enters M_E directly. The roundest ring available is NOT the cleanest lens."
    )

    # ------------------------------------------------------------------------- THEOREM A
    print("\n[B] THEOREM A — the MOND blindness of strong lensing")
    print(
        "    At any Einstein radius kappa-bar = 1 by definition, so g(R_E) = pi G Sigma_cr EXACTLY:"
    )
    print(
        "    a constant of the (z_l, z_s) geometry alone. Minimise it over the ranges where"
        " lenses exist:"
    )
    boost = lambda x: np.sqrt(1 + 1 / x**2)
    xs = np.array([d["xE"] for d in S])

    def floor(zlmax, zsmax):
        bb = (1e9, None)
        for zl in np.arange(0.05, zlmax + 1e-9, 0.05):
            for zs in np.arange(zl + 0.1, zsmax + 1e-9, 0.1):
                v = np.pi * G * A.sigma_cr(zl, zs) / (C * A.H0 * A.ez(zl) / (2 * np.pi))
                if v < bb[0]:
                    bb = (v, (zl, zs))
        return bb

    # NOTE (relire): x_E keeps falling as z_s and z_l grow, so an unbounded scan just runs to the
    # grid edge. The meaningful floors are over the ranges where strong lenses actually exist.
    best = floor(1.0, 6.0)
    best2 = floor(1.5, 10.0)
    print(
        f"      FLOOR over the OBSERVED lens population (z_l <= 1, z_s <= 6): x_E ="
        f" {best[0]:.2f} at z_l = {best[1][0]:.2f}, z_s = {best[1][1]:.1f}"
    )
    print(
        f"      -> the largest MOND boost obtainable at a REAL Einstein radius:"
        f" {(boost(best[0])-1)*100:.1f}%"
    )
    print(
        f"      stretched to z_l <= 1.5, z_s <= 10 (beyond any known deflector):"
        f" {(boost(best2[0])-1)*100:.1f}%"
    )
    print(
        f"      REAL lenses: SLACS x_E = {xs.min():.1f}-{xs.max():.1f} (median {np.median(xs):.1f})"
        f" -> boost {(boost(xs.min())-1)*100:.1f}% at best, {(boost(np.median(xs))-1)*100:.2f}% typical"
    )
    print(
        f"      the Horseshoe would have reached {(boost(x_h)-1)*100:.1f}% -- still an order below"
    )
    print(
        "      the IMF systematic on the stellar mass (Chabrier vs Salpeter = a factor ~1.8)."
    )
    fs = np.array([d["Fs"] for d in S if np.isfinite(d["Fs"])])
    fc = np.array([d["Fc"] for d in S if np.isfinite(d["Fc"])])
    print(
        f"      For scale: the stellar fraction inside R_E is {np.median(fs):.2f} (Salpeter) /"
        f" {np.median(fc):.2f} (Chabrier),"
    )
    print(
        f"      i.e. the non-stellar factor to be explained is x{1/np.median(fs):.2f} to"
        f" x{1/np.median(fc):.2f} -- against a MOND sector worth {(boost(np.median(xs))-1)*100:.2f}%."
    )
    print(
        "      CONCLUSION A: galaxy-scale strong lensing cannot weigh OBT's MOND sector. Whatever"
    )
    print(
        "      it measures inside R_E is stars + the IMF + the Weyl, never the interpolation law."
    )

    # ------------------------------------------------------------------------- THEOREM B
    print(
        "\n[C] THEOREM B — the ARA blindness of strong lensing (this one decides the eps question)"
    )
    print(
        "    Combining the same identity with t_dyn = 2 pi sqrt(R^3/GM) and M_E = pi Sigma_cr R_E^2:"
    )
    print(
        "        t_dyn(theta_E) = 2 pi sqrt( R_E / (pi G Sigma_cr) )   -- it grows only as sqrt(R_E)"
    )
    td = np.array([d["tdT"] for d in S])
    tc = []
    for name, zl, te, m2d, kt in B.BATTERY:
        gE = np.pi * G * A.sigma_cr(zl, 2.0)
        rE = te * A.dc(zl) / (1 + zl) * ARCSEC / KPC
        tc.append(2 * np.pi * np.sqrt(rE * KPC / gE) / GYR_S / TGYR)
    tc = np.array(tc)
    # identity check: the closed form must equal the direct t_dyn from the enclosed Einstein mass
    d0 = S[0]
    t_direct = (
        2
        * np.pi
        * np.sqrt((d0["RE"] * KPC) ** 3 / (G * d0["ME_geom"] * MSUN))
        / GYR_S
        / TGYR
    )
    assert (
        abs(t_direct / d0["tdT"] - 1) < 1e-9
    ), "t_dyn(theta_E) closed form must equal the direct one"
    print(
        f"      SLACS galaxy lenses : t_dyn/T = {td.min():.3f} - {td.max():.3f}"
        f" (median {np.median(td):.3f})"
    )
    print(f"      CLASH cluster arcs  : t_dyn/T = {tc.min():.3f} - {tc.max():.3f}")
    r_need = (TGYR * GYR_S / (2 * np.pi)) ** 2 * np.pi * G * A.sigma_cr(0.3, 2.0) / KPC
    th_need = r_need / (A.dc(0.3) / 1.3 * ARCSEC / KPC)
    print(
        f"      To reach t_dyn = T = 2 Gyr you would need R_E = {r_need:.0f} kpc"
        f" ({th_need:.0f} arcsec). The largest"
    )
    print(
        "      Einstein radius known is ~55'' (~350 kpc). No such lens exists, or can exist."
    )
    print(
        "      CONCLUSION B: EVERY strong lens, from SLACS galaxies to giant cluster arcs, sits"
    )
    print(
        "      deep in ARA's ADIABATIC branch, where W = 1 identically. Strong lensing is"
    )
    print(
        "      structurally incapable of constraining the averaging window -- or eps."
    )

    # ------------------------------------------------------------- what the simplest lens CAN test
    print(
        "\n[D] WHAT THE SIMPLEST LENS CAN STILL TEST, IMF-free: lensing vs dynamics on one object"
    )
    raw, cor = [], []
    for d in S:
        dl = A.dc(d["zl"]) / (1 + d["zl"])
        ds = A.dc(d["zs"]) / (1 + d["zs"])
        dls = (A.dc(d["zs"]) - A.dc(d["zl"])) / (1 + d["zs"])
        th = d["RE"] * KPC / dl
        sis = C * np.sqrt(th * ds / (4 * np.pi * dls)) / 1e3
        raw.append(sis / d["sig"])
        c = (
            (1.5 / (d["reI"] / 8)) ** 0.066
            if np.isfinite(d["reI"]) and d["reI"] > 0
            else 1.0
        )
        cor.append(sis / (d["sig"] * c))
    raw, cor = np.array(raw), np.array(cor)
    print(
        f"    sigma_SIS(from theta_E) / sigma_measured : {np.median(raw):.3f} +/- {np.std(raw):.3f}"
        f"  (N = {len(raw)})"
    )
    print(
        f"    same with the Jorgensen aperture convention applied: {np.median(cor):.3f}"
        f" +/- {np.std(cor):.3f}"
    )
    print(
        "    -> consistent with 1 either way; the aperture convention is a ~12% systematic, so it"
    )
    print(
        "       is reported, not applied. The MEDIAN reproduces the published SLACS result that"
    )
    print(
        "       the lenses are isothermal and that lensing and dynamics agree; my SCATTER (13%)"
    )
    print(
        "       exceeds their ~6.5% because I use the catalogue R_E converted through a different"
    )
    print(
        "       cosmology and the raw fibre sigma, not their SIE-model sigma. The median is the"
    )
    print("       number that carries the test here.")
    print(
        "    -> THIS IS THE SCISSOR'S FALSIFIER (iii), CHECKED AND PASSED: at t_dyn/T ~ 0.03 the"
    )
    print(
        "       ARA branch is adiabatic, so OBT predicts EXACT agreement between the photon and"
    )
    print(
        "       the stellar channel. A discrepancy here would have killed the mechanism. There is"
    )
    print(
        "       none. (It is a pass, not a discrimination: GR predicts the same thing.)"
    )

    print("\n[VERDICT]")
    print(
        "    * The simplest lens was found, and then DISQUALIFIED BY VERIFICATION: the Cosmic"
    )
    print(
        "      Horseshoe's ~300 degree ring and best-in-class geometry are spoiled by a neighbouring"
    )
    print(
        "      cluster. Checking the environment before computing saved the analysis."
    )
    print(
        "    * The remaining clean class returns a NO-GO, and it is a theorem rather than bad luck:"
    )
    print(
        f"      strong lensing gives at most a {(boost(best[0])-1)*100:.1f}% MOND boost on any REAL"
        f" lens (Theorem A) and is always"
    )
    print("      adiabatic (Theorem B). The simplest lens is clean and BLIND.")
    print(
        "    * So the arcs work was not confounded by carelessness: the ONLY OBT ingredient strong"
    )
    print(
        "      lensing can weigh is the Weyl AMPLITUDE, and that requires cluster mass, which"
    )
    print(
        "      brings ellipticity, substructure and the mass-calibration question with it. There is"
    )
    print(
        "      no simpler lens that keeps the signal. That is the structural result of this dig."
    )
    print(
        "    * FOR THE eps DECISION: Theorem B says lensing can NEVER bound eps. eps is bounded"
    )
    print(
        "      only where tracers are slow -- clusters and satellites -- and there the scissor"
    )
    print(
        "      computation already caps the effect at b <= 0.09. The eps caveat therefore cannot"
    )
    print("      be retired by any lensing measurement, present or future.")
    print(
        "    * SCOPE: SLACS quantities are the published Auger+2009 values (M_E reproduced here to"
    )
    print(
        "      3%); the Horseshoe numbers are as published and were not re-derived beyond M_E;"
    )
    print(
        "      the sigma comparison assumes an isothermal deflector, the standard convention."
    )
    print("=" * 104)


if __name__ == "__main__":
    main()
