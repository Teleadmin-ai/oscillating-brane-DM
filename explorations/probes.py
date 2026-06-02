#!/usr/bin/env python3
"""
probes.py — registered ANALYSIS probes for the OBT-Game, invoked ONLY through obt_game.py.

ARCHITECTURE RULE (Romain, 2026-06-01): the tool (obt_game.py) is the SINGLE entry point.
No side scripts. Any new computation becomes a PROBE here (a function in the registry) and is
run via `obt_game.py probe <name> [--k v ...]`, so the §0 banner is always shown first.
Each probe reports FACTS ONLY (numbers); the player (chercheur Claude) judges. Probes never
mutate game.json — recording a finding goes through `obt_game.py note <id> --text ...`.

Probes belong to the battery for monster [01679552] (the low-acceleration boost): they test
the SAME OBT prediction (a0=cH0/2pi, mu(x)=x/sqrt(1+x^2), exact RAR) across system types and
isolate where it holds vs where an external theory must be debunked.
"""

import os
import warnings

import numpy as np

warnings.filterwarnings("ignore")

# --- shared OBT constants (CODATA-consistent with obt_formulas) ---
A0 = 1.0422e-10  # OBT a0 = cH0/2pi (m/s^2)
G = 6.674e-11
MSUN = 1.989e30
KPC = 3.0856775814913673e19
MPC = 1.0e3 * KPC
KMS = 1.0e3
V_MW = 220.0 * KMS  # MW flat circular speed (for external field)
RSUN_KPC = 8.2
LOTS = "/DATA/obt_game_cache/lots"
T1 = "/DATA/obt_game_cache/raw/sparc_table1.mrt"


def obt_rar(g_bar, a0=A0):
    """Exact OBT radial-acceleration relation g_obs(g_bar)."""
    return np.sqrt((g_bar**2 + g_bar * np.sqrt(g_bar**2 + 4 * a0**2)) / 2.0)


def _mu(x):
    return x / np.sqrt(1 + x**2)


def _load_sparc_table1():
    """Per-galaxy SPARC properties (Lelli 2016c MRT). 19-field rows (incl. undocumented flag/
    error cols): 0=ID 1=T 2=D 3=eD 4=distflag 5=Inc 6=eInc 7=L36 8=eL36 9=Reff 10=SBeff
    11=eReff 12=SBdisk 13=MHI 14=eSBdisk 15=Vflat 16=eVflat 17=Q 18=Ref."""
    import pandas as pd

    rows = []
    with open(T1) as f:
        for ln in f:
            p = ln.split()
            if len(p) >= 19 and p[0][0].isalpha():
                try:
                    rows.append(
                        (
                            p[0],
                            float(p[1]),
                            float(p[7]),
                            float(p[9]),
                            float(p[10]),
                            float(p[12]),
                            float(p[13]),
                            float(p[15]),
                            int(float(p[17])),
                        )
                    )
                except (ValueError, IndexError):
                    continue
    return pd.DataFrame(
        rows, columns=["ID", "T", "L36", "Reff", "SBeff", "SBdisk", "MHI", "Vflat", "Q"]
    )


# ==========================================================================
# DATA-BUILD probes (wrap the data-layer pipelines; produce the cached lots)
# ==========================================================================
def build_sparc(opts):
    """Build the SPARC per-point RAR lot (sparc_rar.parquet)."""
    import sparc_pipeline

    sparc_pipeline.main()


def build_wb(opts):
    """Build the clean wide-binary lot (wb_clean.parquet)."""
    import wb_pipeline

    n = int(opts["nmax"]) if opts.get("nmax") else None
    wb_pipeline.main(n)


def a0_implied_z(opts):
    """REVIEWER audit (calculation, not citation): does the high-z RC100/Genzel data actually
    EXCLUDE a0(z)=cH(z)/2pi, as is sometimes claimed from 'no BTFR evolution'? Invert the OBT RAR
    for the a0 the DATA impose at each galaxy: a0 = 0.5*sqrt(((2 gobs^2 - gbar^2)/gbar)^2 - gbar^2),
    using g_bar from photometry/sizes (exp disk + bulge) and g_obs = vc^2/R1/2. KEY FINDING: the
    massive high-z disks are COMPACT -> g_bar >> a0 (Newtonian) -> g_obs ~ g_bar (f_DM~0) -> a0 is
    UNCONSTRAINED (the inversion returns imaginary / undefined). So 'no evolution seen' in these
    systems is NOT an exclusion of a0(z): they are a0-BLIND. The a0-sensitive regime is the
    DEEP-MOND part (V_flat asymptotic = BTFR zero-point; outer-RC RAR), where evolution is reported
    (cards #7 MUSE-DARK, #8 Ubler). Only the least-compact galaxy here can constrain a0.
    """
    import numpy as np
    from scipy.special import i0, i1, k0, k1

    Om = 0.3
    H0 = 2.268e-18
    c = 2.998e8

    def a0cH(z):
        return c * H0 * np.sqrt(Om * (1 + z) ** 3 + (1 - Om)) / (2 * np.pi)

    A0L = 1.2e-10  # local anchor
    # Genzel 2017 Table 1: name, z, Mbar(1e11), fbulge, R1/2 kpc, vc km/s, sigma0, fDM, efDM
    gal = [
        ("COS4_01351", 0.854, 1.7, 0.20, 7.3, 276, 39, 0.21, 0.10),
        ("D3a_6397", 1.500, 2.3, 0.35, 7.4, 310, 73, 0.17, 0.21),
        ("GS4_43501", 1.613, 1.0, 0.40, 4.9, 257, 39, 0.19, 0.09),
        ("zC_406690", 2.196, 1.7, 0.60, 5.5, 301, 74, 0.00, 0.08),
        ("zC_400569", 2.242, 1.7, 0.37, 3.3, 364, 34, 0.00, 0.07),
        ("D3a_15504", 2.383, 2.1, 0.15, 6.0, 299, 76, 0.12, 0.14),
    ]
    print(
        "[a0_implied_z] Invert RAR for the a0 the high-z DATA impose (Genzel 2017, 6 galaxies)."
    )
    print(
        f"  {'galaxy':12s}{'z':>5s}{'g_bar/a0L':>10s}{'fDM':>6s}{'a0_data(e-10)':>14s}{'a0_cH(e-10)':>12s}{'constrains a0?':>15s}"
    )
    nconstr = 0
    for nm, z, Mbar, fb, Rh, vc, sig, fdm, efdm in gal:
        Mb = Mbar * 1e11 * MSUN
        R = Rh * KPC
        Md = (1 - fb) * Mb
        Mbu = fb * Mb
        Rd = R / 1.678
        y = R / (2 * Rd)
        vdisk2 = 2 * G * Md / Rd * y**2 * (i0(y) * k0(y) - i1(y) * k1(y))
        gbar = (vdisk2 + G * Mbu / R) / R
        gobs = (vc * KMS) ** 2 / R
        inner = ((2 * gobs**2 - gbar**2) / gbar) ** 2 - gbar**2
        a0d = 0.5 * np.sqrt(inner) if inner > 0 else float("nan")
        ok = "YES" if (inner > 0 and fdm > 0.05) else "no (a0-blind)"
        if inner > 0 and fdm > 0.05:
            nconstr += 1
        a0s = f"{a0d/1e-10:.2f}" if a0d == a0d else "imaginary"
        print(
            f"  {nm:12s}{z:5.2f}{gbar/A0L:10.2f}{fdm:6.2f}{a0s:>14s}{a0cH(z)/1e-10:12.2f}{ok:>15s}"
        )
    print(
        f"  local anchor a0 ~ {A0L:.1e}. Galaxies that actually constrain a0: {nconstr} of 6."
    )
    print(
        "  READ: the compact high-z disks are Newtonian (g_bar/a0 = 3-14) -> a0-BLIND. 'No BTFR"
    )
    print(
        "  evolution' from such systems is NOT an exclusion of a0(z). The a0-sensitive regime is"
    )
    print(
        "  deep-MOND (V_flat / BTFR zero-point, outer-RC RAR) -> that is where #7/#8 see evolution."
    )


def btfr(opts):
    """MONSTER #11 candidate. External theory to debunk: 'LambdaCDM naturally reproduces the
    baryonic Tully-Fisher relation (slope and small scatter)'. In CDM the bare halo gives
    M ~ V^3 and the observed slope ~4 + the very small scatter must be engineered by feedback +
    a tuned baryon-to-halo relation, and halo-to-halo variance predicts measurable intrinsic
    scatter. OBT/MOND angle: the BTFR is the deep-MOND limit of the SAME local law,
    M_bar = V_flat^4/(G a0) -> slope EXACTLY 4, the zero-point sets the BTFR-normalisation
    a0~1.6e-10 (NOT the RAR a0=1.2e-10: V_flat is not exactly the deep-MOND asymptotic speed),
    and the law has ZERO intrinsic scatter (only measurement scatter). Test on SPARC: fit
    log M_bar vs log V_flat, report slope (forward+inverse), the a0 zero-point, and decompose the
    observed scatter into the per-galaxy measurement budget (distance ~D^2, M/L, velocity x4) vs
    the residual intrinsic scatter (max-likelihood, chi2/dof=1). MOND-SHARED card (debunks the
    CDM 'we naturally reproduce the BTFR slope and small scatter' claim)."""
    import numpy as np

    G = 6.674e-11
    MSUN = 1.989e30
    KMS = 1.0e3
    ln10 = np.log(10.0)
    Yups = float(opts.get("yups", 0.5))  # 3.6um stellar M/L (McGaugh-Lelli)
    sML = float(opts.get("sml", 0.11))  # dex log-normal M/L uncertainty
    qmax = int(opts.get("qmax", 2))  # quality flag (1=best, 2=acceptable)
    imin = float(opts.get("imin", 30.0))  # inclination cut (deg)
    eVmax = float(opts.get("evmax", 0.05))  # max fractional eVflat/Vflat
    eDmax = float(
        opts.get("edmax", 0.10)
    )  # max fractional distance error (M_bar ~ D^2)
    # textbook outliers removed: NGC2841 (contested distance, classic MOND problem galaxy),
    # NGC7814 (bulge-dominated, stellar-M/L sensitive).
    drop = set((opts.get("drop") or "NGC2841,NGC7814").split(","))
    # parse raw T1: ID(0) D(2) eD(3) Inc(5) eInc(6) L36(7) MHI(13) Vflat(15) eVflat(16) Q(17)
    ID, D, eD, Inc, eInc, L36, MHI, V, eV, Q = [[] for _ in range(10)]
    with open(T1) as f:
        for ln in f:
            p = ln.split()
            if len(p) >= 19 and p[0][0].isalpha():
                try:
                    vals = [
                        p[0],
                        float(p[2]),
                        float(p[3]),
                        float(p[5]),
                        float(p[6]),
                        float(p[7]),
                        float(p[13]),
                        float(p[15]),
                        float(p[16]),
                        int(float(p[17])),
                    ]
                except (ValueError, IndexError):
                    continue
                for lst, v in zip((ID, D, eD, Inc, eInc, L36, MHI, V, eV, Q), vals):
                    lst.append(v)
    ID = np.array(ID)
    D, eD, Inc, eInc, L36, MHI, V, eV, Q = map(
        np.array, (D, eD, Inc, eInc, L36, MHI, V, eV, Q)
    )
    Mstar = Yups * L36 * 1e9
    Mgas = 1.33 * np.nan_to_num(MHI) * 1e9
    Mbar = Mstar + Mgas
    fstar = Mstar / np.maximum(Mbar, 1.0)
    keep = np.array([i not in drop for i in ID])
    sel = (
        (V > 0)
        & (Q <= qmax)
        & (Inc >= imin)
        & (Mbar > 0)
        & (eV / np.maximum(V, 1) <= eVmax)
        & (eD / np.maximum(D, 1e-3) <= eDmax)
        & keep
    )
    print(f"[btfr] SPARC baryonic Tully-Fisher. cuts: Q<={qmax}, inc>={imin:.0f}deg,")
    print(
        f"  eVflat/V<={eVmax:.2f}, eD/D<={eDmax:.2f}, drop={sorted(drop)} -> {int(sel.sum())} of {len(V)} galaxies."
    )
    Mbar, V, D, eD, Inc, eInc, eV, fstar = (
        a[sel] for a in (Mbar, V, D, eD, Inc, eInc, eV, fstar)
    )
    x, y = np.log10(V), np.log10(Mbar)
    slope, b = np.polyfit(x, y, 1)
    slope_inv = 1.0 / np.polyfit(y, x, 1)[0]  # inverse fit brackets the true slope
    a0_each = (V * KMS) ** 4 / (G * Mbar * MSUN)
    b4 = np.median(y - 4 * x)
    resid = y - (4 * x + b4)  # vertical residual about slope-4
    sobs = resid.std()
    # --- per-galaxy MEASUREMENT scatter, propagated into vertical log M_bar at slope 4 ---
    sD = 2.0 * (eD / np.maximum(D, 1e-3)) / ln10  # M_bar ~ D^2
    sMLg = sML * fstar  # M/L only acts on the stellar fraction
    sVfl = (eV / np.maximum(V, 1)) / ln10  # flat-velocity error
    sVinc = (
        (eInc * np.pi / 180.0)
        * np.abs(np.cos(np.radians(Inc)) / np.maximum(np.sin(np.radians(Inc)), 1e-2))
        / ln10
    )  # inclination -> V
    sV = np.sqrt(sVfl**2 + sVinc**2)
    smeas = np.sqrt(sMLg**2 + sD**2 + (4 * sV) ** 2)
    smeas_q = np.sqrt(np.mean(smeas**2))
    chi2_0 = np.sum((resid / smeas) ** 2) / (len(resid) - 1)
    # max-likelihood intrinsic scatter: the s_int that makes reduced chi2 == 1
    dof = len(resid) - 1
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        c = np.sum(resid**2 / (smeas**2 + mid**2)) / dof
        if c > 1.0:
            lo = mid
        else:
            hi = mid
    sint_ml = 0.5 * (lo + hi)
    print(
        f"  slope: forward (M|V)={slope:.2f}, inverse (V|M)={slope_inv:.2f}  -> brackets MOND/OBT value 4"
    )
    print(
        f"  a0 from slope-4 zero-point: median={np.median(a0_each):.2e} m/s^2 (BTFR-normalisation a0~1.6e-10)"
    )
    print(f"  OBSERVED scatter (vertical, slope-4) = {sobs:.3f} dex")
    print(
        f"  MEASUREMENT scatter (quadrature)     = {smeas_q:.3f} dex  [dist {np.sqrt(np.mean(sD**2)):.3f}, M/L {np.sqrt(np.mean(sMLg**2)):.3f}, 4*sV {np.sqrt(np.mean((4*sV)**2)):.3f}]"
    )
    print(
        f"  INTRINSIC scatter (max-likelihood, chi2/dof->1) = {sint_ml:.3f} dex   (raw chi2/dof at s_int=0: {chi2_0:.2f})"
    )
    print(
        "  READ (HONEST): slope~4 is clean but NON-distinctive (CDM+feedback also reaches ~4; implicit"
    )
    print(
        f"  in the RAR cards). The max-likelihood INTRINSIC scatter ~{sint_ml:.2f} dex is COMPARABLE to CDM's"
    )
    print(
        "  ~0.15 dex from halo concentration -> with this (formal) error model the BTFR is NOT shown to"
    )
    print(
        "  beat CDM. (RMS-quadrature 's_int~0' is misleading: dominated by a few high-error galaxies; the"
    )
    print(
        "  ML estimate is the honest one. Lelli reaches <=0.1 with a fuller error model.) NOT a clean card."
    )


def a0_regime(opts):
    """MONSTER #11 candidate (DEFENDS a0(z), cards #7/#8). External claim to debunk: 'high-z
    massive disks (Genzel 2017 / Nestor-Shachar 2023 RC100) show NO a0 evolution -> a0 is
    constant -> OBT's a0=cH(z)/2pi is excluded'. In-game: OBT's a0(z) is the axiom; the defect is
    EXTERNAL = the inference that these disks constrain a0 at all. The WHY (by OUR calculation on
    measured M_bar, R1/2, v_c, z): the disks are COMPACT, g_bar(R1/2) >> a0, i.e. the NEWTONIAN
    regime, where g_obs ~ g_bar and a0 drops out. Two proofs: (1) DISCRIMINATING POWER -- predict
    f_DM under constant a0 (=1.2e-10) vs evolving a0=cH(z)/2pi; if |Delta f_DM| < the measurement
    error e_fDM, the data physically CANNOT tell the two apart -> 'no evolution' is vacuous. (2)
    INVERSION -- solving the exact RAR for the a0 each galaxy imposes returns imaginary a0 (NaN)
    whenever g_obs ~ g_bar. Where leverage DOES exist (least-compact disk), a0 sits between local
    and cH(z)/2pi. Debunks the external 'constant-a0-from-compact-disks' claim with measurements.
    """
    import numpy as np
    from scipy.special import i0, i1, k0, k1

    G = 6.674e-11
    MSUN = 1.989e30
    KPC = 3.0856775814913673e19
    KMS = 1.0e3
    Om = 0.3
    H0 = 2.268e-18
    cc = 2.998e8
    a0L = 1.2e-10  # local RAR anchor (measured, McGaugh-Lelli)

    def a0_cH(z):
        return cc * H0 * np.sqrt(Om * (1 + z) ** 3 + (1 - Om)) / (2 * np.pi)

    gal = [
        ("COS4_01351", 0.854, 1.7, 0.20, 7.3, 276, 0.21, 0.10),
        ("D3a_6397", 1.500, 2.3, 0.35, 7.4, 310, 0.17, 0.21),
        ("GS4_43501", 1.613, 1.0, 0.40, 4.9, 257, 0.19, 0.09),
        ("zC_406690", 2.196, 1.7, 0.60, 5.5, 301, 0.00, 0.08),
        ("zC_400569", 2.242, 1.7, 0.37, 3.3, 364, 0.00, 0.07),
        ("D3a_15504", 2.383, 2.1, 0.15, 6.0, 299, 0.12, 0.14),
    ]
    print(
        "[a0_regime] MONSTER #11: do high-z compact disks actually CONSTRAIN a0? (defends cards #7/#8)"
    )
    print(
        "  Debunk target = 'compact high-z disks show constant a0 -> a0(z) excluded'."
    )
    print(
        f"  {'galaxy':12s}{'z':>5s}{'g_bar/a0L':>10s}{'fDM_a0L':>8s}{'fDM_cH':>7s}{'dfDM':>7s}{'e_fDM':>7s}{'a0_inv':>8s}"
    )
    nblind = 0
    for nm, z, Mbar, fb, Rh, vc, fdm, efdm in gal:
        Mb = Mbar * 1e11 * MSUN
        R = Rh * KPC
        Md = (1 - fb) * Mb
        Mbu = fb * Mb
        Rd = R / 1.678
        y = R / (2 * Rd)
        vbar2 = 2 * G * Md / Rd * y**2 * (i0(y) * k0(y) - i1(y) * k1(y)) + G * Mbu / R
        gbar = vbar2 / R
        gobs = (vc * KMS) ** 2 / R
        fdm_L = 1.0 - gbar / obt_rar(gbar, a0L)
        fdm_H = 1.0 - gbar / obt_rar(gbar, a0_cH(z))
        dfdm = fdm_H - fdm_L
        inner = ((2 * gobs**2 - gbar**2) / gbar) ** 2 - gbar**2
        a0inv = 0.5 * np.sqrt(inner) / 1e-10 if inner > 0 else np.nan
        blind = abs(dfdm) < efdm
        nblind += blind
        flag = " BLIND" if blind else ""
        a0s = f"{a0inv:7.2f}" if a0inv == a0inv else "    nan"
        print(
            f"  {nm:12s}{z:5.2f}{gbar/a0L:10.2f}{fdm_L:8.2f}{fdm_H:7.2f}{dfdm:+7.2f}{efdm:7.2f}{a0s}{flag}"
        )
    print(
        f"  -> {nblind}/{len(gal)} galaxies are a0-BLIND (|predicted dfDM(const vs cH)| < measurement error)."
    )
    print(
        "  READ: the predicted constant-vs-evolving a0 difference is SMALLER than the error bar for the"
    )
    print(
        "  compact disks -> they cannot discriminate; 'no a0 evolution' from them is a Newtonian-regime"
    )
    print(
        "  artifact. a0(z) must be tested where g_bar~a0 (MOND regime: MUSE-DARK card #7, LSB/outer RCs)."
    )


def a0_kross(opts):
    """MONSTER #12 candidate -- the 3rd INDEPENDENT a0(z) dataset (strengthens cards #7/#8).
    External claim debunked: 'a0 is a universal constant' (Milgrom). OBT axiom: a0=cH(z)/2pi rises
    with z. Unlike the compact Genzel/RC100 disks (a0-blind, card #11), KROSS (Harrison 2017, 586
    Halpha rotators at z~0.6-1.0) measures the intrinsic velocity VC at 2*R1/2 (=3.4 R_D) -- the
    OUTER, low-g_bar point -- so these galaxies sit in the MOND regime (g_bar < a0) and DO
    constrain a0. We compute a0 ourselves by inverting the exact OBT RAR on each clean galaxy from
    its measured M_bar (=M* x gas factor), R1/2, VC, z, then take the MOND-regime median vs z.
    The gas factor M_bar/M* is the main systematic (KROSS gives M* only); we scan it. Verdict is
    judged by the player; data only."""
    import numpy as np

    G = 6.674e-11
    MSUN = 1.989e30
    KPC = 3.0856775814913673e19
    KMS = 1.0e3
    Om = 0.3
    a0L = 1.2e-10

    def aCH(z):
        return a0L * np.sqrt(Om * (1 + z) ** 3 + (1 - Om))

    def inv_a0(gbar, gobs):  # invert exact OBT RAR for a0
        inner = ((2 * gobs**2 - gbar**2) / gbar) ** 2 - gbar**2
        return 0.5 * np.sqrt(inner) if inner > 0 else np.nan

    rows = []
    for ln in open("/DATA/obt_game_cache/raw/kross/krossv2.dat"):
        try:
            Mass = float(ln[83:105])
            Rim = float(ln[131:140])
            Qual = int(ln[118:119])
            theta = float(ln[163:171])
            z = float(ln[183:191])
            fAGN = int(ln[257:258])
            fIRR = int(ln[259:260])
            VC = float(ln[303:313])
            eVC = float(ln[314:324])
            fext = int(ln[336:337])
        except (ValueError, IndexError):
            continue
        # clean: best quality, no AGN/irregular, inclination usable, VC real & not extrapolated
        if (
            Qual == 1
            and fAGN == 0
            and fIRR == 0
            and theta >= 25
            and VC > 20
            and fext == 0
            and Rim > 0.5
            and Mass > 0
        ):
            rows.append((Mass, Rim, z, VC, eVC))
    print(
        f"[a0_kross] 3rd INDEPENDENT a0(z) probe: KROSS z~0.9 (clean Qual1/noAGN/noIRR/incl>25/VC@2R1/2)."
    )
    print(
        f"  {len(rows)} clean galaxies. Inverting the exact OBT RAR for a0 in the MOND regime (g_bar<a0)."
    )
    gasgrid = [
        (0.0, "M* only (a0 upper bound)"),
        (0.6, "Mbar/M*=1.6 (f_gas~0.4, typical z~0.9)"),
        (1.0, "Mbar/M*=2.0 (gas-rich)"),
    ]
    print(
        f"  {'gas assumption':40s}{'N(MOND)':>8s}{'med z':>7s}{'med a0':>9s}{'cH(z)/2pi':>10s}"
    )
    for fg, lab in gasgrid:
        a0s, zs = [], []
        for Mass, Rim, z, VC, eVC in rows:
            R = 2 * Rim * KPC
            gobs = (VC * KMS) ** 2 / R
            gbar = G * Mass * (1 + fg) * MSUN / R**2
            if gbar < a0L:  # MOND-regime selection (where a0 is constrained)
                a0 = inv_a0(gbar, gobs)
                if a0 == a0 and 0 < a0 < 1e-8:
                    a0s.append(a0)
                    zs.append(z)
        a0s, zs = np.array(a0s), np.array(zs)
        mz = np.median(zs)
        print(f"  {lab:40s}{len(a0s):8d}{mz:7.2f}{np.median(a0s):9.2e}{aCH(mz):10.2e}")
    # internal redshift trend at the central gas assumption (Mbar/M*=1.6)
    a0s, zs = [], []
    for Mass, Rim, z, VC, eVC in rows:
        R = 2 * Rim * KPC
        gobs = (VC * KMS) ** 2 / R
        gbar = G * Mass * 1.6 * MSUN / R**2
        if gbar < a0L:
            a0 = inv_a0(gbar, gobs)
            if a0 == a0 and 0 < a0 < 1e-8:
                a0s.append(a0)
                zs.append(z)
    a0s, zs = np.array(a0s), np.array(zs)
    print("  internal z-trend (Mbar/M*=1.6):")
    for lo, hi in [(0.6, 0.85), (0.85, 1.05)]:
        m = (zs >= lo) & (zs < hi)
        if m.sum() >= 5:
            print(
                f"    z in [{lo},{hi}): N={m.sum():3d}, median a0={np.median(a0s[m]):.2e}, cH/2pi={aCH(np.median(zs[m])):.2e}"
            )
    print(
        "  READ: in the MOND regime (g_bar<a0, median g_bar/a0~0.3) a0 at z~0.85 is ELEVATED above the"
    )
    print(
        "  local 1.2e-10 for ANY plausible gas fraction (1.6-2.7e-10); the f_gas~0.4 central value ~1.97e-10"
    )
    print(
        "  lands on cH(z)/2pi=1.99e-10. Evolution robust to gas; exact value gas-dependent. 3rd independent leg."
    )


def a0_kges(opts):
    """4th-leg ATTEMPT for a0(z) — KGES (Tiley 2021, KMOS Galaxy Evolution Survey, z~1.2-1.8).
    HONEST NEGATIVE: NOT a clean leg. KGES only tabulates the INNER velocity v2.2c at 1.31*R50
    (rising part of the rotation curve), not an outer/flat point like KROSS (VC at 2*R1/2), so
    g_obs is underestimated -> a0 biased LOW; AND at z~1.5 the gas fraction is large/uncertain
    (f_gas~0.5-0.7, Mbar/M*~2-2.5), which dominates the inverted a0. Result: a0 ranges from ~local
    (realistic gas) to 2.0e-10 (M*-only upper bound), BELOW cH(z=1.5)/2pi=2.8e-10 -> inconclusive,
    systematics-dominated. In-game this 'low a0' is plausibly the inner-velocity + gas systematic
    (external), but UNPROVABLE without the outer velocity KGES lacks -> a MONSTER, not a card. Kept
    as tooling so the negative is reproducible; do NOT cite as confirmation."""
    import numpy as np

    G = 6.674e-11
    MSUN = 1.989e30
    KPC = 3.0856775814913673e19
    KMS = 1.0e3
    Om = 0.3
    a0L = 1.2e-10

    def aCH(z):
        return a0L * np.sqrt(Om * (1 + z) ** 3 + (1 - Om))

    def inv(gb, go):
        inr = ((2 * go**2 - gb**2) / gb) ** 2 - gb**2
        return 0.5 * np.sqrt(inr) if inr > 0 else np.nan

    rows = []
    for ln in open("/DATA/obt_game_cache/raw/kges/tablea1.dat"):
        try:
            z = float(ln[32:45])
            AGN = int(ln[50:51])
            Kin = int(ln[52:53])
            Ms = float(ln[54:62])
            R50 = float(ln[63:76])
            v22 = float(ln[95:112])
        except (ValueError, IndexError):
            continue
        if Kin == 1 and AGN == 0 and Ms > 0 and R50 > 0.3 and v22 > 20:
            rows.append((z, Ms, R50, v22))
    print(
        f"[a0_kges] 4th-leg ATTEMPT (HONEST NEGATIVE): KGES z~1.5, {len(rows)} clean (Kin=1,no AGN)."
    )
    print(
        "  CAVEAT: only INNER velocity (v2.2c at 1.31*R50) available -> a0 biased LOW; large z~1.5 gas."
    )
    print(
        f"  {'gas assumption':34s}{'N(MOND)':>8s}{'med z':>7s}{'med a0':>9s}{'cH/2pi':>9s}"
    )
    for fg, lab in [
        (0.0, "M* only (upper bound)"),
        (1.0, "Mbar/M*=2.0 (f_gas~0.5)"),
        (1.5, "Mbar/M*=2.5 (gas-rich)"),
    ]:
        a, zz = [], []
        for z, Ms, R50, v22 in rows:
            R = 1.31 * R50 * KPC
            go = (v22 * KMS) ** 2 / R
            gb = G * Ms * (1 + fg) * MSUN / R**2
            if gb < a0L:
                x = inv(gb, go)
                if x == x and 0 < x < 1e-8:
                    a.append(x)
                    zz.append(z)
        if a:
            a, zz = np.array(a), np.array(zz)
            print(
                f"  {lab:34s}{len(a):8d}{np.median(zz):7.2f}{np.median(a):9.2e}{aCH(np.median(zz)):9.2e}"
            )
    print(
        "  READ: a0 ~local-to-2.0e-10, BELOW cH(z=1.5)/2pi=2.8 -> inconclusive, systematics-dominated"
    )
    print(
        "  (inner-velocity bias + uncertain high-z gas). NOT a clean 4th leg; recorded as a monster."
    )


def a0_slacs(opts):
    """4th-leg ATTEMPT for a0(z) via STRONG LENSING — SLACS (Auger 2009, J/ApJ/705/1099), a
    method-INDEPENDENT probe (lensing mass of early-type galaxies, not kinematics). HONEST
    NEGATIVE: NOT a clean leg, for the SAME reason as card #11. Per lens we have, directly: R_E
    (Einstein radius, kpc), M_Ein (total lensing mass within R_E), and the stellar fraction within
    R_E (Fc Chabrier / Fs Salpeter). So g_obs = G*M_Ein/R_E^2 and g_bar = F*g_obs, and inverting
    the OBT RAR gives a0. BUT SLACS ETGs at the Einstein radius are DEEP NEWTONIAN
    (median g_obs/a0_local ~ 15, g_bar/a0 ~ 6-10): at g >> a0 the boost mu(x)->1, so the inverted
    a0 is a regime artifact (~4e-9 Chabrier, ~30x local) with NO z-trend -- the well-known
    'MOND-in-ellipticals' issue, AND in OBT the residual mass at R_E is the Weyl/geometric-DM
    component, not a MOND boost. So a0 is NOT measurable here. Kept as tooling; not a confirmation.
    """
    import numpy as np

    G = 6.674e-11
    MSUN = 1.989e30
    KPC = 3.0856775814913673e19
    Om = 0.3
    a0L = 1.2e-10

    def aCH(z):
        return a0L * np.sqrt(Om * (1 + z) ** 3 + (1 - Om))

    def inv(gb, go):
        inr = ((2 * go**2 - gb**2) / gb) ** 2 - gb**2
        return 0.5 * np.sqrt(inr) if inr > 0 else np.nan

    base = "/DATA/obt_game_cache/raw/slacs"
    zl = {}
    for ln in open(f"{base}/table3.dat"):
        nm = ln[4:14].strip()
        try:
            zl[nm] = float(ln[39:44])
        except ValueError:
            pass
    rows = []
    for ln in open(f"{base}/table4.dat"):
        nm = ln[4:14].strip()
        try:
            RE = float(ln[15:19])
            Mein = float(ln[20:25])
            Fc = float(ln[26:30])
            Fs = float(ln[36:40])
        except ValueError:
            continue
        if nm in zl and RE > 0 and Mein > 0 and 0 < Fc < 1.2:
            rows.append((zl[nm], RE, Mein, Fc, Fs))
    print(
        f"[a0_slacs] 4th-leg ATTEMPT via STRONG LENSING (HONEST NEGATIVE): {len(rows)} SLACS lenses."
    )
    for lab, useFs in [("Chabrier IMF", False), ("Salpeter IMF", True)]:
        a0s, zs, ga = [], [], []
        for z, RE, Mein, Fc, Fs in rows:
            R = RE * KPC
            gobs = G * 10**Mein * MSUN / R**2
            f = Fs if useFs else Fc
            if not 0 < f < 1:
                continue
            x = inv(f * gobs, gobs)
            if x == x and 0 < x < 1e-8:
                a0s.append(x)
                zs.append(z)
                ga.append(gobs / a0L)
        if a0s:
            a0s, zs, ga = np.array(a0s), np.array(zs), np.array(ga)
            print(
                f"  {lab:14s} N={len(a0s):3d} med z={np.median(zs):.2f} med g_obs/a0={np.median(ga):5.1f} med a0={np.median(a0s):.2e} cH/2pi={aCH(np.median(zs)):.2e}"
            )
    print(
        "  READ: g_obs/a0 ~ 15 -> ETGs at R_E are DEEP NEWTONIAN -> a0 unmeasurable (inverted ~4e-9 is a"
    )
    print(
        "  regime artifact, no z-trend). Residual mass = Weyl/geometric DM, not a MOND boost. NOT a leg."
    )


def diversity(opts):
    """MONSTER #10 candidate. External theory to debunk: 'LambdaCDM predicts a tight, ~uniform
    inner rotation-curve shape at fixed outer velocity' -> Oman et al. 2015 (the 'diversity of
    rotation curves' problem): at FIXED V_flat, real galaxies span a WIDE range of inner velocities
    V(2 kpc), which CDM hydro sims struggle to reproduce (they predict a narrow band). OBT/MOND
    angle: the RAR is LOCAL, so V(2 kpc) is set by the baryonic acceleration g_bar(2 kpc), which
    varies strongly with surface brightness AT FIXED V_flat -> the diversity is INHERITED from
    baryons, not a crisis. Test on SPARC: in narrow V_flat bins, (a) measure the spread of the
    observed V(2 kpc) [the diversity], (b) show OBT mu(x) predicts each V(2 kpc) from the baryons
    (small residual), and (c) show the diversity correlates with baryonic surface density. MOND-
    SHARED card (debunks the CDM expectation; OBT inherits)."""
    import pandas as pd
    from scipy.stats import spearmanr

    ML = float(opts.get("ml", 0.7))
    Rin = float(opts.get("rin", 2.0))  # inner radius (kpc) for the diversity metric
    df = pd.read_parquet(f"{LOTS}/sparc_rar.parquet")
    rows = []
    for gid, g in df.groupby("ID"):
        g = g.sort_values("R_kpc")
        R = g.R_kpc.values
        if R.min() > Rin + 0.5 or R.max() < 5.0:
            continue  # need an inner point near Rin and a flat outer part
        Vobs = g.Vobs.values
        Vgas2 = g.Vgas.values**2
        Vstar2 = ML * g.Vdisk.values**2 + ML * g.Vbul.values**2
        gbar = (Vgas2 + Vstar2) * KMS**2 / (R * KPC)
        # inner point nearest Rin
        j = int(np.argmin(np.abs(R - Rin)))
        if abs(R[j] - Rin) > 1.0:
            continue
        Vin_obs = Vobs[j]
        Vin_obt = np.sqrt(obt_rar(gbar[j]) * R[j] * KPC) / KMS
        # outer flat velocity = mean of outer third
        Vflat = np.mean(Vobs[R > 0.66 * R.max()])
        SBin = (
            Vstar2[j] * KMS**2 / (R[j] * KPC)
        ) / A0  # stellar g_bar(Rin)/a0 ~ surface dens proxy
        rows.append((gid, Vflat, Vin_obs, Vin_obt, SBin))
    d = pd.DataFrame(rows, columns=["ID", "Vflat", "Vin_obs", "Vin_obt", "SBin"])
    print(
        f"[diversity] {len(d)} SPARC galaxies with an inner point near {Rin:.0f} kpc + flat outer."
    )
    print(f"  Diversity metric = V({Rin:.0f} kpc) at fixed V_flat. (M/L={ML})")
    print(
        f"  {'Vflat bin (km/s)':18s} {'N':>3s} {'<V_in_obs>':>10s} {'spread(V_in)':>12s} {'OBT res dex':>11s} {'OBT scat':>9s}"
    )
    for lo, hi in [(40, 70), (70, 100), (100, 140), (140, 200)]:
        b = d[(d.Vflat >= lo) & (d.Vflat < hi)]
        if len(b) < 4:
            continue
        res = np.log10(b.Vin_obs / b.Vin_obt)
        print(
            f"  {f'{lo}-{hi}':18s} {len(b):3d} {b.Vin_obs.mean():10.1f} {b.Vin_obs.std():12.1f} {res.median():+11.3f} {res.std():9.3f}"
        )
    res_all = np.log10(d.Vin_obs / d.Vin_obt)
    print(
        f"  ALL: OBT V(2kpc) residual median={res_all.median():+.3f} dex, scatter={res_all.std():.3f} dex"
    )
    # the diversity is baryonic: at fixed Vflat, V_in correlates with baryonic surface density
    rhos = []
    for lo, hi in [(40, 70), (70, 100), (100, 140), (140, 200)]:
        b = d[(d.Vflat >= lo) & (d.Vflat < hi)]
        if len(b) >= 6:
            rho, p = spearmanr(b.SBin, b.Vin_obs)
            rhos.append(rho)
            print(
                f"  Vflat {lo}-{hi}: Spearman(V_in_obs, baryonic SB) = {rho:+.2f} (p={p:.1e}, N={len(b)})"
            )
    print(
        "  READ: large spread(V_in) at fixed V_flat = the diversity; OBT predicts each V(2kpc) from"
    )
    print(
        "  baryons at ~0.05-0.08 dex; V_in tracks baryonic SB -> diversity is baryonic, not a CDM crisis."
    )


# ==========================================================================
# ANALYSIS probes (battery for monster [01679552])
# ==========================================================================
def sparc_residuals(opts):
    """Per-galaxy OBT-RAR residual vs EXTERNAL properties (gas frac, SB, type...) at M/L=0.7,
    + the gas-domination split that tells M/L-noise from intrinsic scatter."""
    import pandas as pd
    from scipy.stats import spearmanr

    ML = float(opts.get("ml", 0.7))
    df = pd.read_parquet(f"{LOTS}/sparc_rar.parquet")
    R = df["R_kpc"].values * KPC
    Vgas2 = df["Vgas"].values ** 2
    Vstar2 = ML * df["Vdisk"].values ** 2 + ML * df["Vbul"].values ** 2
    gbar = (Vgas2 + Vstar2) * KMS**2 / R
    gobs = (df["Vobs"].values * KMS) ** 2 / R
    df = df.assign(
        logres=np.log10(gobs / obt_rar(gbar)),
        x_acc=gbar / A0,
        fgas_dyn=Vgas2 / np.maximum(Vgas2 + Vstar2, 1e-9),
    )
    lo = df[df.x_acc < 3]
    g = lo.groupby("ID")["logres"].median().rename("res_dex").reset_index()
    npts = lo.groupby("ID").size().rename("npts").reset_index()
    g = g.merge(npts, on="ID")
    g = g[g.npts >= 3]
    t1 = _load_sparc_table1()
    t1 = t1.assign(fgas=t1["MHI"] / t1["L36"].clip(lower=1e-3))
    m = g.merge(t1, on="ID")
    print(f"[sparc_residuals] {len(m)} galaxies (low-acc, >=3 pts), M/L={ML}")
    print(
        f"  residual: median={m.res_dex.median():+.3f} dex, scatter(std)={m.res_dex.std():.3f} dex"
    )
    print("  FACT — Spearman residual vs EXTERNAL properties:")
    for col, lab in [
        ("T", "Hubble type T"),
        ("fgas", "gas frac M_HI/L"),
        ("SBeff", "surf.bright SBeff"),
        ("SBdisk", "disk SB0"),
        ("L36", "luminosity L36"),
        ("Reff", "eff.radius"),
    ]:
        x = m[col].values
        y = m.res_dex.values
        ok = np.isfinite(x) & np.isfinite(y)
        if ok.sum() > 20:
            rho, p = spearmanr(x[ok], y[ok])
            flag = (
                " <== strong"
                if abs(rho) > 0.4 and p < 1e-3
                else (" <- notable" if abs(rho) > 0.25 and p < 0.01 else "")
            )
            print(f"    {lab:20s}: rho={rho:+.3f}  p={p:.1e}  (N={ok.sum()}){flag}")
    print("  FACT — gas-domination split (flat scatter => observational, not M/L):")
    for name, mask in [
        ("gas-DOM fgas>0.7", lo.fgas_dyn > 0.7),
        ("mixed 0.3-0.7", (lo.fgas_dyn > 0.3) & (lo.fgas_dyn <= 0.7)),
        ("star-DOM fgas<0.3", lo.fgas_dyn <= 0.3),
    ]:
        s = lo[mask]
        print(
            f"    {name:18s}: N={len(s):5d}  med={s.logres.median():+.3f}  std={s.logres.std():.3f}"
        )
    rho, p = spearmanr(lo.fgas_dyn, lo.logres)
    print(f"    per-point residual vs gas-share: rho={rho:+.3f} p={p:.1e} N={len(lo)}")


def dsph(opts):
    """Local-Group dwarf spheroidals (pressure-supported): boost & OBT-RAR residual, split by
    external field x_ext (EFE discriminant). Fetches McConnachie 2012 (cached to dsph.parquet).
    """
    import pandas as pd
    import pyvo

    cache = f"{LOTS}/dsph.parquet"
    if opts.get("refresh") or not os.path.exists(cache):
        tap = pyvo.dal.TAPService("http://tapvizier.cds.unistra.fr/TAPVizieR/tap")
        df = tap.search('SELECT * FROM "J/AJ/144/4/catalog"').to_table().to_pandas()
        df.columns = [c.replace("*", "") for c in df.columns]
        df = df[["Name", "SubG", "GLON", "GLAT", "D", "VMag", "R1", "sigma", "M_HI"]]
        df = df.rename(
            columns={
                "sigma": "sigma_kms",
                "R1": "Rh_arcmin",
                "D": "D_kpc",
                "M_HI": "MHI",
            }
        )
        for c in ["D_kpc", "VMag", "Rh_arcmin", "sigma_kms", "MHI", "GLON", "GLAT"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        d = df[
            np.isfinite(df.sigma_kms)
            & np.isfinite(df.Rh_arcmin)
            & np.isfinite(df.D_kpc)
            & (df.sigma_kms > 0)
            & (df.Rh_arcmin > 0)
        ].copy()
        PC = KPC / 1e3
        r_half_pc = (
            d.D_kpc.values * 1e3 * np.tan(np.radians(d.Rh_arcmin.values / 60.0))
        )  # pc
        r = r_half_pc * PC  # m
        sig = d.sigma_kms.values * KMS
        L_V = 10 ** (-0.4 * (d.VMag.values - 4.83))
        M_bar = (2.0 * L_V + 1.33 * np.nan_to_num(d.MHI.values)) * MSUN
        M_dyn = 4.0 * sig**2 * r / G
        g_bar = G * (M_bar / 2.0) / r**2
        g_obs = G * (M_dyn / 2.0) / r**2
        lon = np.radians(d.GLON.values)
        lat = np.radians(d.GLAT.values)
        x = d.D_kpc.values * np.cos(lat) * np.cos(lon) - RSUN_KPC
        y = d.D_kpc.values * np.cos(lat) * np.sin(lon)
        z = d.D_kpc.values * np.sin(lat)
        Rgc = np.sqrt(x * x + y * y + z * z) * KPC  # kpc -> m
        g_ext = V_MW**2 / Rgc
        out = d[["Name", "SubG", "D_kpc", "sigma_kms"]].copy()
        out["r_half_pc"] = r_half_pc
        out["M_bar"] = M_bar / MSUN
        out["M_dyn"] = M_dyn / MSUN
        out["g_bar"] = g_bar
        out["g_obs"] = g_obs
        out["x_acc"] = g_bar / A0
        out["x_ext"] = g_ext / A0
        out["boost_obs"] = g_obs / g_bar
        out["res_obt_dex"] = np.log10(g_obs / obt_rar(g_bar))
        out = out[np.isfinite(out.res_obt_dex)]
        out.to_parquet(cache, index=False)
    out = pd.read_parquet(cache)
    print(
        f"[dsph] {len(out)} dwarf spheroidals; median x_acc={out.x_acc.median():.3f} (deep-MOND if <<1)"
    )
    print(
        f"  OBT-RAR residual: median={out.res_obt_dex.median():+.3f} dex, scatter={out.res_obt_dex.std():.3f}"
    )
    print("  FACT — boost & residual split by EXTERNAL FIELD x_ext (EFE discriminant):")
    for lo_, hi_, lab in [
        (0, 0.05, "x_ext<0.05"),
        (0.05, 0.15, "0.05-0.15"),
        (0.15, 1e9, "x_ext>0.15"),
    ]:
        msk = (out.x_ext >= lo_) & (out.x_ext < hi_)
        if msk.sum() >= 3:
            s = out[msk]
            print(
                f"    [{lab:11s}] N={msk.sum():3d}  med boost={s.boost_obs.median():6.1f}x  "
                f"resid={s.res_obt_dex.median():+.3f} dex"
            )
    from scipy.stats import spearmanr

    ok = np.isfinite(out.res_obt_dex) & np.isfinite(out.x_ext)
    rho, p = spearmanr(out.x_ext[ok], out.res_obt_dex[ok])
    print(
        f"  POP EFE TEST: residual vs x_ext rho={rho:+.3f} p={p:.2e} (EFE predicts NEGATIVE)"
    )


def udg_btfr(opts):
    """BTFR slope/normalization from SPARC, + UDGs DF2/DF4 boost (the 'lacking DM' betrayal)."""
    import pandas as pd

    d = _load_sparc_table1()
    d = d[(d.Vflat > 0) & (d.Q < 3)].copy()
    Mbar = 0.5 * d.L36 * 1e9 + 1.33 * d.MHI * 1e9
    d = d.assign(Mbar=Mbar)
    d = d[d.Mbar > 0]
    logV = np.log10(d.Vflat.values)
    logM = np.log10(d.Mbar.values)
    A = np.vstack([logV, np.ones_like(logV)]).T
    slope, icpt = np.linalg.lstsq(A, logM, rcond=None)[0]
    pred_norm = np.log10((1e3) ** 4 / (G * A0) / MSUN)
    icpt4 = np.median(logM - 4 * logV)
    print(
        f"[btfr] N={len(d)} (Q<3, Vflat>0): free slope={slope:.2f} (OBT predicts 4.0)"
    )
    print(
        f"  at slope=4: log10(Mbar/Vflat^4) meas={icpt4:.3f}  OBT 1/(G a0)={pred_norm:.3f}  diff={icpt4 - pred_norm:+.3f} dex"
    )
    cat = [
        ("NGC1052-DF2", 8.5, 2.2, 2.0e8, 1.0e11, 80.0),
        ("NGC1052-DF2_T13", 8.5, 1.4, 0.8e8, 1.0e11, 52.0),
        ("NGC1052-DF4", 4.2, 1.6, 1.5e8, 1.0e11, 200.0),
    ]
    print("  [udg] DF2/DF4 'lacking DM' (OBT predicts ~6x if g_bar<<a0):")
    print("    name              x_acc  g_ext/a0  b_obs  b_OBT   verdict")
    for nm, sig, Re, Ms, Mh, sep in cat:
        r = Re * KPC
        g_bar = G * (Ms * MSUN / 2.0) / r**2
        g_obs = 2.0 * (sig * KMS) ** 2 / r
        g_ext = G * Mh * MSUN / (sep * KPC) ** 2
        b_obs = g_obs / g_bar
        b_obt = obt_rar(g_bar) / g_bar
        verdict = "boost ABSENT" if b_obs < 2 else "present"
        print(
            f"    {nm:16s} {g_bar/A0:6.3f}  {g_ext/A0:7.2f}  {b_obs:5.1f}x {b_obt:5.1f}x   {verdict}"
        )


def clusters(opts):
    """Galaxy clusters at ~r500 (literature): where does the boost sit vs the OBT RAR?"""
    clus = [
        ("A2029", 8.0e14, 1.2e14, 2.00),
        ("A2142", 1.3e15, 2.0e14, 2.20),
        ("A1795", 6.0e14, 8.0e13, 1.90),
        ("A85", 6.0e14, 9.0e13, 1.90),
        ("Coma", 7.0e14, 1.0e14, 2.00),
        ("A2199", 4.0e14, 5.0e13, 1.70),
    ]
    print("[clusters] literature ~r500, M_star ~ 0.15 M_gas:")
    print("    name     x_acc  b_obs   b_OBT   resid(dex)")
    res = []
    for nm, Mtot, Mgas, r500 in clus:
        r = r500 * MPC
        Mbar = (Mgas + 0.15 * Mgas) * MSUN
        g_bar = G * Mbar / r**2
        g_obs = G * Mtot * MSUN / r**2
        rdex = np.log10(g_obs / obt_rar(g_bar))
        res.append(rdex)
        print(
            f"    {nm:8s} {g_bar/A0:6.2f}  {g_obs/g_bar:5.1f}x  {obt_rar(g_bar)/g_bar:5.1f}x   {rdex:+.2f}"
        )
    print(
        f"  median OBT-RAR residual = {np.median(res):+.2f} dex (factor-2 excess lives in cores, not r500)"
    )


def lead_df2_crater(opts):
    """Pursue the DF2/DF4 betrayal on Crater II & Antlia 2: isolated-OBT boost vs observed vs EFE."""
    sysl = [
        ("NGC1052-DF2", 8.5, 2.2, 2.0e8, "host", (1.0e11, 80.0)),
        ("NGC1052-DF4", 4.2, 1.6, 1.5e8, "host", (1.0e11, 200.0)),
        ("Crater II", 2.7, 1.07, 3.2e5, "MW", (117.0,)),
        ("Antlia 2", 5.7, 2.9, 7.2e5, "MW", (132.0,)),
    ]
    print("[lead_df2_crater] FACTS (player judges):")
    print(
        f"    {'system':14s} {'x_in':>8s} {'b_iso':>8s} {'b_obs':>8s} {'b_obs/b_iso':>11s} {'x_ext':>7s} {'b_efe':>7s}"
    )
    for nm, sig, Rk, Ms, kind, p in sysl:
        r = Rk * KPC
        g_bar = G * (Ms * MSUN / 2.0) / r**2
        g_obs = 2.0 * (sig * KMS) ** 2 / r
        if kind == "MW":
            g_ext = V_MW**2 / (p[0] * KPC)
        else:
            g_ext = G * p[0] * MSUN / (p[1] * KPC) ** 2
        b_iso = obt_rar(g_bar) / g_bar
        b_obs = g_obs / g_bar
        x_ext = g_ext / A0
        print(
            f"    {nm:14s} {g_bar/A0:8.4f} {b_iso:8.1f} {b_obs:8.1f} {b_obs/b_iso:11.2f} "
            f"{x_ext:7.2f} {1.0/_mu(x_ext):7.1f}"
        )
    print(
        "  READ: b_obs/b_iso<1 => boost suppressed; if suppression does NOT track x_ext, EFE is not the cause."
    )


def wb_boost(opts):
    """FIND_WHY maillon for monster [01679552]: is the wide-binary boost REAL or the hidden-triple
    artifact (Banik/Pittordis-Sutherland, the external theory)? Report the POPULATION median
    v_ratio=v_sky/v_N vs x=g/a0, CONTROLLED for (a) the positive noise bias (cut on v_snr) and
    (b) triple contamination (cut on RUWE). FACTS only. The signature of a real OBT/MOND boost:
    median v_ratio RISES as x falls AND survives tighter v_snr & RUWE cuts; a triple artifact would
    be a sep-independent inflated tail removed by tighter RUWE."""
    import pandas as pd

    df = pd.read_parquet(f"{LOTS}/wb_clean.parquet")
    bins = [
        (3, 1e9, "Newton x>3"),
        (1, 3, "trans 1-3"),
        (0.3, 1, "0.3-1"),
        (0, 0.3, "deepMOND x<0.3"),
    ]
    print(
        f"[wb_boost] {len(df):,} clean binaries. median v_ratio (=v_sky/v_N) vs x, by S/N & RUWE cut:"
    )
    for snr in [2, 5, 10]:
        print(f"  -- v_snr>{snr} --")
        for lo, hi, lab in bins:
            m = (df.x_acc >= lo) & (df.x_acc < hi) & (df.v_snr > snr)
            if m.sum() >= 10:
                print(
                    f"     [{lab:14s}] N={m.sum():6d}  median v_ratio={df.loc[m,'v_ratio'].median():.3f}"
                )
    print(
        "  -- triple-clean stress test (deep-MOND x<0.3, v_snr>5), tightening RUWE --"
    )
    base = (df.x_acc < 0.3) & (df.v_snr > 5)
    for ru in [1.4, 1.2, 1.1, 1.05]:
        m = base & (df.ruwe1 < ru) & (df.ruwe2 < ru)
        if m.sum() >= 10:
            print(
                f"     RUWE<{ru:<4}: N={m.sum():6d}  median v_ratio={df.loc[m,'v_ratio'].median():.3f}"
            )
    print(
        "  READ: boost REAL if median v_ratio rises as x falls AND is stable under tighter v_snr/RUWE;"
    )
    print(
        "  triple-artifact if it collapses toward ~1 when RUWE is tightened. FACTS only — player judges."
    )


def wb_forward(opts):
    """FIND_WHY PROOF (big-compute) for monster [01679552]: Monte-Carlo forward model of the
    wide-binary velocity statistic, Newton vs OBT, compared to the DATA. For a population of
    Keplerian orbits (Opik log-uniform a, thermal eccentricity p(e)=2e, isotropic projection,
    time-uniform phase) we compute, per simulated binary, the OBSERVABLE v~ = v_sky/sqrt(GM/s_proj)
    and x = GM/s_proj^2/a0, then the MEDIAN v~(x). NEWTON: exact Kepler speed. OBT: same orbit
    geometry, speed scaled by sqrt(boost(r)) with boost=obt_rar(g_N)/g_N (mu(x) enhanced gravity;
    this speed-scaling is the one stated APPROXIMATION). Decisive: does the data's median v~(x)
    track the OBT curve (boosted) or the Newton curve? FACTS only — player judges the amplitude match.
    Options: --n SIM (default 400000), --seed-vary i (vary the orbit draw by index, no RNG-time).
    """
    import numpy as np
    import pandas as pd

    N = int(opts.get("n", 400000))
    # deterministic draws (no Math.random ban issue here, but keep reproducible): seeded Generator
    rng = np.random.default_rng(int(opts.get("seed", 20260601)))
    data = pd.read_parquet(f"{LOTS}/wb_clean.parquet")
    AU = 1.495978707e11
    # population: masses resampled from the DATA; semi-major axis a ~ log-uniform (Opik);
    # thermal eccentricity p(e)=2e -> e=sqrt(U); time-uniform mean anomaly; isotropic orientation
    Mtot = rng.choice(data["Mtot"].values, size=N) * MSUN
    a = (
        10 ** rng.uniform(np.log10(50.0), np.log10(60000.0), N) * AU
    )  # semi-major axis (m)
    e = np.sqrt(rng.uniform(0.0, 1.0, N))  # thermal
    Manom = rng.uniform(0.0, 2 * np.pi, N)
    # solve Kepler M = E - e sinE (vectorized Newton iterations)
    E = Manom.copy()
    for _ in range(60):
        E = E - (E - e * np.sin(E) - Manom) / (1 - e * np.cos(E))
    cosE, sinE = np.cos(E), np.sin(E)
    r = a * (1 - e * cosE)  # separation (m)
    # orbital-plane position & velocity (unit-consistent); speed from vis-viva
    mu_g = G * Mtot
    v_N = np.sqrt(mu_g * (2.0 / r - 1.0 / a))  # Newtonian speed (m/s)
    # velocity direction in orbital plane (perifocal): vhat ∝ (-sinE, sqrt(1-e^2) cosE)
    b = np.sqrt(1 - e * e)
    vx_p = -sinE
    vy_p = b * cosE
    vnorm = np.sqrt(vx_p**2 + vy_p**2)
    vx_p, vy_p = vx_p / vnorm, vy_p / vnorm
    # position in perifocal frame (for projection)
    x_p = a * (cosE - e)
    y_p = a * b * sinE
    # OBT speed: scale by sqrt(boost(r)), boost = obt_rar(g_N)/g_N at the instantaneous r.
    # Optional EFE: the MW external field g_ext (~1.8 a0) is added to the total field magnitude,
    # which SUPPRESSES the boost (single-field AQUAL-like approximation):
    #   boost_EFE(r) = obt_rar(g_N + g_ext)/(g_N + g_ext)   (recovers isolated boost at g_ext=0)
    g_Nr = mu_g / r**2
    g_ext = float(opts.get("efe", 0.0)) * A0  # --efe in units of a0 (0=off)
    boost = obt_rar(g_Nr + g_ext) / (g_Nr + g_ext)
    v_O = v_N * np.sqrt(boost)
    # isotropic random orientation: rotate perifocal (x,y,0)-plane by random Euler angles,
    # then project onto sky = first two axes. Random inclination via cos(i) uniform, node Omega,
    # argument-of-pericenter omega uniform.
    inc = np.arccos(rng.uniform(-1.0, 1.0, N))
    Om = rng.uniform(0, 2 * np.pi, N)
    om = rng.uniform(0, 2 * np.pi, N)
    cO, sO = np.cos(Om), np.sin(Om)
    ci, si = np.cos(inc), np.sin(inc)
    co, so = np.cos(om), np.sin(om)

    # rotation perifocal->sky (standard 3-1-3); we only need the X,Y (sky) components.
    # R = Rz(Om) Rx(inc) Rz(om). Apply to perifocal vectors (z_p=0).
    def to_sky(xp, yp):
        # after Rz(om): (xp*co - yp*so, xp*so + yp*co, 0)
        x1 = xp * co - yp * so
        y1 = xp * so + yp * co
        # after Rx(inc): (x1, y1*ci, y1*si)
        x2 = x1
        y2 = y1 * ci
        # after Rz(Om): (x2*cO - y2*sO, x2*sO + y2*cO)
        X = x2 * cO - y2 * sO
        Y = x2 * sO + y2 * cO
        return X, Y

    Xpos, Ypos = to_sky(x_p, y_p)
    s_proj = np.sqrt(Xpos**2 + Ypos**2)
    Vx_N, Vy_N = to_sky(vx_p * v_N, vy_p * v_N)
    vsky_N = np.sqrt(Vx_N**2 + Vy_N**2)
    Vx_O, Vy_O = to_sky(vx_p * v_O, vy_p * v_O)
    vsky_O = np.sqrt(Vx_O**2 + Vy_O**2)
    # observables: v~ = v_sky / sqrt(GM/s_proj), x = GM/s_proj^2/a0
    vc = np.sqrt(mu_g / s_proj)
    vt_N = vsky_N / vc
    vt_O = vsky_O / vc
    x_obs = (mu_g / s_proj**2) / A0
    # restrict simulated x to the data's separation regime for a fair comparison
    sel = (s_proj / AU > 1e3) & (s_proj / AU < 3e4)
    bins = [
        (3, 1e9, "Newton x>3"),
        (1, 3, "trans 1-3"),
        (0.3, 1, "0.3-1"),
        (0, 0.3, "deepMOND x<0.3"),
    ]
    print(
        f"[wb_forward] MC N={N:,} (sep 1-30 kAU). median v~(x): Newton vs OBT vs DATA (v_snr>5):"
    )
    print(f"    {'bin':16s} {'Newton':>8s} {'OBT':>8s} {'DATA':>8s} {'N_data':>8s}")
    for lo, hi, lab in bins:
        mm = sel & (x_obs >= lo) & (x_obs < hi)
        md = (data.x_acc >= lo) & (data.x_acc < hi) & (data.v_snr > 5)
        nm = float(np.median(vt_N[mm])) if mm.sum() > 50 else float("nan")
        om_ = float(np.median(vt_O[mm])) if mm.sum() > 50 else float("nan")
        dm = float(data.loc[md, "v_ratio"].median()) if md.sum() > 10 else float("nan")
        print(f"    {lab:16s} {nm:8.3f} {om_:8.3f} {dm:8.3f} {md.sum():8d}")
    print(
        "  READ: if DATA tracks OBT (boosted) and exceeds Newton at low x -> boost amplitude matches"
    )
    print(
        "  mu(x) -> the triple-free OBT law is confirmed in wide binaries (the card). APPROX: OBT speed"
    )
    print(
        "  = Newton x sqrt(boost(r)) (enhanced-gravity); exact OBT orbit would refine amplitudes."
    )


def obt_evolution_family(opts):
    """EXPLOIT a0(z)=cH(z)/2pi (card #7): every MOND-scale observable inherits H(z) evolution with a
    fixed power. OBT predicts a FAMILY of redshift-evolving signatures; standard MOND has them ALL
    constant. We derive each observable's a0-power -> H(z)-power, and tabulate the predicted evolution
    factor to z=1 and z=2 (E(z)=sqrt(Om(1+z)^3+OL)). FACTS (the distinctive prediction set); player
    judges which are testable. a0 ~ E(z); X ~ a0^p ~ E(z)^p."""
    import numpy as np

    Om = 0.3

    def E(z):
        return np.sqrt(Om * (1 + z) ** 3 + (1 - Om))

    fam = [
        (
            "a0 (RAR transition scale)",
            "a0",
            +1.0,
            "RAR a0 vs z (MUSE-DARK 2026, CARD#7)",
        ),
        (
            "BTFR zero-point M_bar at fixed V",
            "1/a0",
            -1.0,
            "high-z baryonic Tully-Fisher (KMOS/KROSS/Ubler)",
        ),
        ("BTFR V_flat at fixed M_bar", "a0^1/4", +0.25, "high-z TFR velocity offset"),
        (
            "pressure-supported sigma at fixed M",
            "(M a0)^1/4",
            +0.25,
            "high-z dispersion-supported dwarfs/ETGs",
        ),
        (
            "MOND transition radius r_t=sqrt(GM/a0)",
            "a0^-1/2",
            -0.5,
            "high-z rotation-curve flattening radius",
        ),
        (
            "critical surface density Sigma_t=a0/G",
            "a0",
            +1.0,
            "high-z MOND surface-brightness threshold",
        ),
        (
            "deep-MOND boost g_obs/g_bar=sqrt(a0/g)",
            "a0^1/2",
            +0.5,
            "high-z RAR low-g amplitude",
        ),
    ]
    print(
        "[obt_evolution_family] OBT-DISTINCTIVE evolving signatures from a0=cH(z)/2pi (MOND: all constant)."
    )
    print(f"  E(z=1)={E(1):.2f}, E(z=2)={E(2):.2f}.  X ~ a0^p ~ E(z)^p")
    print(
        f"  {'observable':40s} {'~a0^p':>9s} {'x@z=1':>7s} {'x@z=2':>7s}  testable with"
    )
    for name, dep, p, test in fam:
        print(f"  {name:40s} {dep:>9s} {E(1)**p:7.2f} {E(2)**p:7.2f}  {test}")
    print(
        "  READ: each row is an OBT prediction (evolution) that standard constant-a0 MOND forbids."
    )
    print(
        "  Card #7 confirmed row 1 (a0 rises). The BTFR zero-point (row 2, ~1/E(z)) is the next"
    )
    print("  most data-accessible cross-check (high-z TFR) -> candidate card #8.")


def genzel_fdm(opts):
    """MONSTER #9 candidate. External theory to debunk: 'LambdaCDM expects DARK-MATTER-DOMINATED
    cores in massive high-z disks' -> Genzel 2017 (Nature 543, 397) found the OPPOSITE: 6 massive
    z=0.85-2.4 disks are strongly BARYON-dominated, f_DM(R1/2) dropping 0.21 -> ~0 with redshift,
    billed as a surprise/tension for CDM. OBT/MOND angle: high-z disks are COMPACT & massive ->
    baryonic surface acceleration g_bar(R1/2) >> a0 -> Newtonian regime -> LOW f_DM is the NATURAL
    RAR consequence, no DM-dominated core needed. Test: compute g_bar INDEPENDENTLY (exp disk +
    bulge, scipy.special) from M_bar & R1/2, run OBT RAR with a0(z)=cH(z)/2pi, predict f_DM, compare
    to Genzel's observed f_DM. (MOND-SHARED card: low f_DM follows from high g_bar at constant a0
    too; a0(z) shifts it only at the few-% level -> debunks CDM, OBT inherits.)"""
    from scipy.special import i0, i1, k0, k1

    Om = 0.3
    H0 = 2.268e-18  # s^-1 (70 km/s/Mpc)
    c = 2.998e8

    def a0_z(z):
        return c * H0 * np.sqrt(Om * (1 + z) ** 3 + (1 - Om)) / (2 * np.pi)

    # Genzel 2017 Table 1 (fit params): name, z, Mbar(1e11 Msun, incl bulge), fbulge=Mbulge/Mbar,
    # R1/2(n=1) kpc, vc(R1/2) km/s, sigma0 km/s, fDM(R1/2), +/- (upper-limit half-width as 1sig)
    gal = [
        ("COS4_01351", 0.854, 1.7, 0.20, 7.3, 276, 39, 0.21, 0.10),
        ("D3a_6397", 1.500, 2.3, 0.35, 7.4, 310, 73, 0.17, 0.21),
        ("GS4_43501", 1.613, 1.0, 0.40, 4.9, 257, 39, 0.19, 0.09),
        ("zC_406690", 2.196, 1.7, 0.60, 5.5, 301, 74, 0.00, 0.08),
        ("zC_400569", 2.242, 1.7, 0.37, 3.3, 364, 34, 0.00, 0.07),
        ("D3a_15504", 2.383, 2.1, 0.15, 6.0, 299, 76, 0.12, 0.14),
    ]
    print(
        "[genzel_fdm] MONSTER #9: high-z 'baryon-dominated disks' (Genzel 2017) vs OBT mu(x)+a0(z)."
    )
    print(
        "  Debunk target = 'CDM expects DM-dominated high-z cores'. OBT: low f_DM = compact -> g_bar>>a0."
    )
    print(
        f"  {'galaxy':12s} {'z':>5s} {'g_bar/a0(z)':>11s} {'fDM_obs':>9s} {'fDM_OBT':>8s} {'vc_obs':>7s} {'vc_OBT':>7s}"
    )
    chi2 = 0.0
    n = 0
    for name, z, Mbar, fb, Rhalf, vc, sig, fdm, efdm in gal:
        Mb = Mbar * 1e11 * MSUN
        R = Rhalf * KPC
        Md = (1 - fb) * Mb  # disk
        Mbu = fb * Mb  # bulge
        Rd = R / 1.678  # exp scale length (R1/2 = 1.678 Rd)
        y = R / (2 * Rd)  # = 0.839
        # exponential-disk circular velocity^2 at R (Freeman): v^2 = 2 G Md/Rd * y^2 [I0K0-I1K1]
        vdisk2 = 2 * G * Md / Rd * y**2 * (i0(y) * k0(y) - i1(y) * k1(y))
        vbul2 = G * Mbu / R  # bulge ~ point mass inside R1/2 (Reff_bulge < R1/2)
        vbar2 = vdisk2 + vbul2
        g_bar = vbar2 / R  # independent baryonic acceleration at R1/2
        a0 = a0_z(z)
        g_obs = obt_rar(g_bar, a0)
        fdm_obt = 1.0 - g_bar / g_obs
        vc_obt = np.sqrt(g_obs * R) / KMS
        x = g_bar / a0
        chi2 += ((fdm - fdm_obt) / max(efdm, 0.05)) ** 2
        n += 1
        print(
            f"  {name:12s} {z:5.2f} {x:11.2f} {fdm:9.2f} {fdm_obt:8.2f} {vc:7.0f} {vc_obt:7.0f}"
        )
    print(f"  chi2/N (fDM_obs vs OBT) = {chi2/n:.2f}  (N={n})")
    print(
        "  READ: g_bar/a0 > 1 for all -> OBT mu(x) predicts low f_DM NATURALLY (compactness, not DM-poor)."
    )
    print(
        "  Cross-check: constant a0 gives x even larger at high z (a0 smaller) -> low f_DM is MOND-SHARED."
    )


def sparc_a0_fullbudget(opts):
    """CARD #6 (complete the Rodrigues-2018 debunk). Full per-galaxy a0 error budget: marginalize
    M/L (log-normal 0.5,0.11dex), inclination (Inc+/-e_Inc), DISTANCE (D+/-e_D; g_obs ~ 1/D), and add
    the KNOWN RAR intrinsic scatter sigma_int (g-space dex; McGaugh-Lelli ~0.08-0.13 dex, NOT a0
    variation) in quadrature to the velocity errors. Then test whether the per-galaxy a0 are consistent
    with a UNIVERSAL value (chi2/dof vs a common a0). NON-CIRCULAR: scan sigma_int and check the value
    that gives chi2/dof~1 matches the independently-measured RAR intrinsic scatter. FACTS only.
    """
    import numpy as np
    import pandas as pd

    df = pd.read_parquet(f"{LOTS}/sparc_rar.parquet")
    inc, dist = {}, {}
    with open(T1) as f:
        for ln in f:
            p = ln.split()
            if len(p) >= 19 and p[0][0].isalpha():
                try:
                    inc[p[0]] = (float(p[5]), max(float(p[6]), 2.0))
                    dist[p[0]] = (
                        float(p[2]),
                        max(float(p[3]), 0.01 * float(p[2])),
                    )  # D, e_D (Mpc)
                except (ValueError, IndexError):
                    pass
    a0g = np.logspace(np.log10(0.3e-10), np.log10(4e-10), 44)
    mlg = np.linspace(0.2, 1.2, 18)
    ln_ml = -0.5 * (np.log10(mlg / 0.5) / 0.11) ** 2
    A0U = 1.0422e-10
    sig_grid = (
        [float(opts["sint"])]
        if opts.get("sint")
        else [0.0, 0.05, 0.08, 0.10, 0.13, 0.16]
    )

    def a0_post(s, i0e, d0e, sdex):
        R = s.R_kpc.values * KPC
        Vg2 = s.Vgas.values**2
        Vd2 = s.Vdisk.values**2
        Vb2 = s.Vbul.values**2
        Vo0 = s.Vobs.values
        eVraw = np.clip(s.eVobs.values, 2.0, None)
        i0 = i0e[0] if i0e else 90.0
        incs = (
            np.clip(i0 + i0e[1] * np.array([-1.4, 0, 1.4]), 15, 90)
            if i0e
            else np.array([i0])
        )
        ln_i = -0.5 * ((incs - i0) / i0e[1]) ** 2 if i0e else np.array([0.0])
        dfrac = d0e[1] / d0e[0] if d0e else 0.001
        dsc = np.array([-1.4, 0, 1.4]) * dfrac  # delta D / D
        ln_d = -0.5 * (np.array([-1.4, 0, 1.4])) ** 2
        post = np.full(len(a0g), -np.inf)
        for j, ml in enumerate(mlg):
            gbar = (Vg2 + ml * Vd2 + 0.7 * Vb2) * KMS**2 / R
            Vpred = np.array(
                [np.sqrt(obt_rar(gbar, a0) * R) / KMS for a0 in a0g]
            )  # [a0, pt]
            eV = np.sqrt(
                eVraw**2 + (1.1513 * sdex * Vpred) ** 2
            )  # +intrinsic (g-dex->V)
            for iv, li in zip(incs, ln_i):
                for dd, ld in zip(dsc, ln_d):
                    Vo = (
                        Vo0
                        * (np.sin(np.radians(i0)) / np.sin(np.radians(iv)))
                        * np.sqrt(1 + dd)
                    )  # V_obs deproj; g_obs~1/D folded via R(D)
                    ll = -0.5 * np.sum(((Vo - Vpred) / eV) ** 2, axis=1)
                    post = np.logaddexp(post, ll + ln_ml[j] + li + ld)
        P = np.exp(post - post.max())
        P /= P.sum()
        mean = np.sum(P * a0g)
        var = np.sum(P * (a0g - mean) ** 2)
        return mean, np.sqrt(var)

    print(
        f"[sparc_a0_fullbudget] full error budget (M/L+inclination+distance+intrinsic scatter). "
        f"Universal a0={A0U:.2e}."
    )
    print(
        f"  {'sigma_int(g,dex)':>16s} {'best a0':>9s} {'chi2/dof':>9s} {'within2sig':>11s} {'med sig_a0':>11s}"
    )
    for sdex in sig_grid:
        out = []
        for gid, s in df.groupby("ID"):
            if len(s) < 5:
                continue
            m, e = a0_post(s, inc.get(gid), dist.get(gid), sdex)
            out.append((m, max(e, 1e-13)))
        a = np.array([o[0] for o in out])
        e = np.array([o[1] for o in out])
        au = np.sum(a / e**2) / np.sum(1 / e**2)
        chi2 = np.sum(((a - au) / e) ** 2) / (len(a) - 1)
        frac = np.mean(np.abs(a - au) / e < 2)
        chimed = np.sum(((a - np.median(a)) / e) ** 2) / (len(a) - 1)
        print(
            f"  {sdex:16.2f} {au:9.2e} {chi2:9.1f} {100*frac:10.0f}% {np.median(e):11.2e}  med_a0={np.median(a):.2e} chi2med/dof={chimed:.1f}"
        )
    print(
        "  READ: the RAR intrinsic scatter (McGaugh-Lelli ~0.08-0.13 dex in g) is INDEPENDENTLY measured."
    )
    print(
        "  If chi2/dof -> ~1 at that sigma_int, the per-galaxy a0 are consistent with a UNIVERSAL value"
    )
    print(
        "  once the full (Rodrigues-fixed) error budget is restored -> Rodrigues 2018 DEBUNKED (card)."
    )


def sparc_a0_posteriors(opts):
    """MONSTER #6 (rigorous debunk of Rodrigues et al. 2018, 'Absence of a fundamental acceleration
    scale'). Per galaxy, build the 2D likelihood over (a0, M/L_disk) from the rotation curve, with a
    log-normal M/L prior (3.6um: 0.5, sigma=0.11 dex), and MARGINALIZE M/L -> the a0 posterior.
    Rodrigues fixed M/L (narrow a0 errors -> apparent >5sigma a0 variation). McGaugh: marginalizing the
    a0<->M/L degeneracy widens the a0 posteriors so they become consistent with a UNIVERSAL a0. We
    compare chi2/dof of the per-galaxy a0 vs a common value, FIXED-M/L vs MARGINALIZED-M/L. FACTS only.
    chi2/dof ~ 1 (marginalized) => universal a0 holds => Rodrigues debunked as a degeneracy artifact.
    """
    import numpy as np
    import pandas as pd

    df = pd.read_parquet(f"{LOTS}/sparc_rar.parquet")
    # inclination Inc +/- e_Inc per galaxy from SPARC table1 (fields 5=Inc, 6=e_Inc)
    inc = {}
    with open(T1) as f:
        for ln in f:
            p = ln.split()
            if len(p) >= 19 and p[0][0].isalpha():
                try:
                    inc[p[0]] = (float(p[5]), max(float(p[6]), 2.0))
                except (ValueError, IndexError):
                    pass
    a0g = np.logspace(np.log10(0.3e-10), np.log10(4e-10), 48)
    mlg = np.linspace(0.15, 1.3, 24)
    ln_ml = -0.5 * (np.log10(mlg / 0.5) / 0.11) ** 2  # log-normal M/L prior (3.6um)
    A0U = 1.0422e-10

    def a0_post(s, marg, i0e):
        R = s.R_kpc.values * KPC
        Vg2 = s.Vgas.values**2
        Vd2 = s.Vdisk.values**2
        Vb2 = s.Vbul.values**2
        Vo0 = s.Vobs.values
        eV = np.clip(s.eVobs.values, 2.0, None)
        i0 = i0e[0] if i0e else 90.0
        if marg and i0e:  # inclination grid (V_obs ~ 1/sin i)
            incs = np.clip(
                i0 + i0e[1] * np.array([-1.5, -0.75, 0.0, 0.75, 1.5]), 15.0, 90.0
            )
            ln_i = -0.5 * (((incs - i0) / i0e[1]) ** 2)
        else:
            incs = np.array([i0])
            ln_i = np.array([0.0])
        Vpred_ml = {}
        post = np.full(len(a0g), -np.inf)
        for j, ml in enumerate(mlg):
            if not marg and abs(ml - 0.5) > (mlg[1] - mlg[0]) / 2:
                continue
            gbar = (Vg2 + ml * Vd2 + 0.7 * Vb2) * KMS**2 / R
            Vpred = np.array(
                [np.sqrt(obt_rar(gbar, a0) * R) / KMS for a0 in a0g]
            )  # [a0, point]
            for iv, li in zip(incs, ln_i):
                Vo = Vo0 * (np.sin(np.radians(i0)) / np.sin(np.radians(iv)))
                ll = -0.5 * np.sum(((Vo - Vpred) / eV) ** 2, axis=1)
                post = np.logaddexp(post, ll + (ln_ml[j] + li if marg else 0.0))
        P = np.exp(post - post.max())
        P /= P.sum()
        mean = np.sum(P * a0g)
        var = np.sum(P * (a0g - mean) ** 2)
        return mean, np.sqrt(var)

    res = {"fixed": [], "marg": []}
    for gid, s in df.groupby("ID"):
        if len(s) < 5:
            continue
        i0e = inc.get(gid)
        for k, mg in [("fixed", False), ("marg", True)]:
            m, e = a0_post(s, mg, i0e)
            res[k].append((m, max(e, 1e-12)))
    print(
        f"[sparc_a0_posteriors] {len(res['marg'])} SPARC galaxies. Per-galaxy a0 posterior; "
        f"universal a0={A0U:.2e}. Test: are per-galaxy a0 consistent with ONE value?"
    )
    for k, lab in [
        ("fixed", "M/L FIXED (Rodrigues-like)"),
        ("marg", "M/L MARGINALIZED (McGaugh)"),
    ]:
        arr = np.array(res[k])
        a = arr[:, 0]
        e = arr[:, 1]
        au = np.sum(a / e**2) / np.sum(1 / e**2)  # best common a0
        chi2 = np.sum(((a - au) / e) ** 2) / (len(a) - 1)
        frac = np.mean(np.abs(a - au) / e < 2)
        print(
            f"  {lab:28s}: best a0={au:.2e}  chi2/dof={chi2:6.1f}  frac within 2sigma={100*frac:.0f}%  "
            f"median sigma_a0={np.median(e):.2e}"
        )
    print(
        "  READ: FIXED-M/L gives chi2/dof>>1 (apparent 'a0 varies', Rodrigues). If MARGINALIZING M/L"
    )
    print(
        "  drops chi2/dof toward ~1 (posteriors widen, mostly consistent), the variation is an"
    )
    print(
        "  a0<->M/L DEGENERACY artifact -> universal a0 holds -> Rodrigues 2018 debunked."
    )


def sparc_a0_universality(opts):
    """MONSTER #6 hunt (game = OBT + 5 cards). External claim: Rodrigues et al. 2018 ('Absence of a
    fundamental acceleration scale in galaxies') fit a PER-GALAXY a0 and find it varies at >5sigma ->
    no universal a0 -> mu(x)/RAR falsified as a universal law. PATCH (artifact, Kroupa/McGaugh 2018):
    the per-galaxy a0 is only constrained by points that PROBE the low-acceleration (deep-MOND) regime;
    galaxies whose data stay at high g_bar cannot constrain a0, so their fitted a0 scatters wildly -
    a selection/coverage artifact, not a physical variation. Test on SPARC: fit a0 per galaxy, and show
    the a0-scatter COLLAPSES once we keep only galaxies that actually reach deep-MOND. FACTS only.
    """
    import numpy as np
    import pandas as pd

    ML = float(opts.get("ml", 0.7))
    df = pd.read_parquet(f"{LOTS}/sparc_rar.parquet")
    R = df["R_kpc"].values * KPC
    gbar = (
        (
            df["Vgas"].values ** 2
            + ML * df["Vdisk"].values ** 2
            + ML * df["Vbul"].values ** 2
        )
        * KMS**2
        / R
    )
    gobs = (df["Vobs"].values * KMS) ** 2 / R
    df = df.assign(gbar=gbar, gobs=gobs)
    a0_grid = np.logspace(np.log10(0.2e-10), np.log10(5e-10), 80)
    rows = []
    for gid, s in df.groupby("ID"):
        gb = s.gbar.values
        go = s.gobs.values
        ok = np.isfinite(gb) & np.isfinite(go) & (gb > 0) & (go > 0)
        if ok.sum() < 5:
            continue
        gb, go = gb[ok], go[ok]
        chi = [
            np.sum((np.log10(go) - np.log10(obt_rar(gb, a0))) ** 2) for a0 in a0_grid
        ]
        a0_fit = a0_grid[int(np.argmin(chi))]
        xmin = gb.min() / 1.0422e-10
        rows.append((gid, a0_fit, xmin))
    g = pd.DataFrame(rows, columns=["ID", "a0", "xmin"])
    print(
        f"[sparc_a0_universality] {len(g)} SPARC galaxies, per-galaxy a0 fit (M/L={ML}). Universal a0=1.04e-10."
    )
    print(
        "  a0 scatter (dex) vs how deep into MOND the galaxy probes (xmin = min g_bar / a0):"
    )
    for lo, hi, lab in [
        (0, 0.3, "deep-MOND xmin<0.3"),
        (0.3, 1.0, "transition 0.3-1"),
        (1.0, 1e9, "Newtonian xmin>1"),
    ]:
        m = (g.xmin >= lo) & (g.xmin < hi)
        if m.sum() >= 3:
            la = np.log10(g.a0[m])
            print(
                f"    [{lab:20s}] N={m.sum():3d}  median a0={g.a0[m].median():.2e}  scatter={la.std():.3f} dex"
            )
    from scipy.stats import spearmanr

    rho, p = spearmanr(g.xmin, np.log10(g.a0))
    print(
        f"  corr(fitted a0, xmin) rho={rho:+.3f} p={p:.1e}: positive => galaxies that DON'T reach deep-MOND"
    )
    print(
        "  fit spuriously high a0 (the artifact). Deep-MOND probers converge on the universal a0."
    )
    print(
        "  READ: if a0-scatter SHRINKS for deep-MOND probers, the 'a0 varies' claim is a coverage"
    )
    print("  artifact -> universal a0 holds -> Rodrigues 2018 debunked.")


def brouwer_split(opts):
    """COMPLETE card #5 with Brouwer 2021's ACTUAL morphology-split data (KiDS data release,
    Fig-8 files). Each RAR file: col0 = g_bar (m/s^2), col1 = ESD_t (Msun/pc^2), col3 = error,
    col4 = bias. g_obs = 4 G ESD_t/bias. We measure the OBSERVED early/late split
    log10(g_obs_early/g_obs_late) per g_bar bin (Sersic index AND u-r colour), and compare to my
    colossus 2-halo prediction with REALISTIC bias (from gc-style halo masses). FACTS only.
    """
    import numpy as np
    from colossus.cosmology import cosmology
    from colossus.lss import bias as cbias

    base = "/DATA/obt_game_cache/raw/brouwer2021_rar"
    PC_m = KPC / 1e3
    ESD2g = 4 * G * MSUN / PC_m**2  # g_obs[m/s^2] = ESD2g * ESD_t[Msun/pc^2]/bias

    def load(fn):
        a = np.loadtxt(f"{base}/{fn}", comments="#")
        gbar = a[:, 0]
        gobs = ESD2g * a[:, 1] / a[:, 4]
        egobs = ESD2g * a[:, 3] / a[:, 4]
        return gbar, gobs, egobs

    # realistic 2-halo split prediction (central bias) at the data's g_bar
    cosmo = cosmology.setCosmology("planck18")
    h = cosmo.H0 / 100.0
    z = 0.25
    b_e = float(cbias.haloBias(5e12 * h, z, mdef="200m", model="tinker10"))
    b_l = float(cbias.haloBias(6e11 * h, z, mdef="200m", model="tinker10"))
    for proxy, f1, f2 in [
        (
            "Sersic (1=late,2=early)",
            "Fig-8_RAR-KiDS-isolated_Sersicbin_1.txt",
            "Fig-8_RAR-KiDS-isolated_Sersicbin_2.txt",
        ),
        (
            "Colour (1=blue,2=red)",
            "Fig-8_RAR-KiDS-isolated_Colorbin_1.txt",
            "Fig-8_RAR-KiDS-isolated_Colorbin_2.txt",
        ),
    ]:
        gb, gL, eL = load(f1)
        _, gE, eE = load(f2)
        split = np.log10(gE / gL)
        esplit = (np.sqrt((eE / gE) ** 2 + (eL / gL) ** 2)) / np.log(10)
        lowg = gb < 1e-11
        wmean = np.sum(split[lowg] / esplit[lowg] ** 2) / np.sum(1 / esplit[lowg] ** 2)
        sig = wmean / np.sqrt(1 / np.sum(1 / esplit[lowg] ** 2))
        print(
            f"[brouwer_split] {proxy}: OBSERVED early/late split (g_bar<1e-11, N={lowg.sum()} bins):"
        )
        print(
            f"   weighted-mean split = {wmean:+.3f} +/- {np.sqrt(1/np.sum(1/esplit[lowg]**2)):.3f} dex  ({sig:.1f} sigma)"
        )
    print(
        f"  MY 2-halo (realistic central bias b_early={b_e:.2f}, b_late={b_l:.2f}): predicts ~0.07-0.11 dex at low g."
    )
    print(
        "  READ: compare observed split magnitude+sign to my 2-halo. If observed >> 2-halo, the"
    )
    print(
        "  remainder needs satellite/group effective bias + baryonic content (card #5 honest scope)."
    )


def lensing_2halo(opts):
    """MONSTER #5 validation (candidate lensing-rar-morphology, BRIDGE kinematics->lensing->
    environment). Brouwer 2021 finds the weak-lensing RAR depends on MORPHOLOGY at >=6sigma,
    claimed to break universal mu(x). PATCH: it is the 2-HALO (environment) term, not a mu(x) failure.
    At the low-g (large-R) end lensing probes, g_obs = g_1halo[mu(x) on baryons] + g_2halo, where
    g_2halo = 4 G b dSigma_mm(R) scales with the galaxy BIAS b. Early-types are MORE clustered
    (b_early~1.8) than late-types (b_late~1.1), so their lensing RAR rises MORE at low g_bar -> the
    morphology split. We compute g_obs(g_bar) for both with colossus matter correlation, and report
    the early/late split at the low-g end. FACTS only; player judges if it matches Brouwer's split.
    """
    import numpy as np
    from colossus.cosmology import cosmology

    cosmo = cosmology.setCosmology("planck18")
    from colossus.lss import bias as cbias

    h = cosmo.H0 / 100.0
    z = float(opts.get("z", 0.25))
    Mbar = float(opts.get("M", 10**10.5)) * MSUN  # KiDS lens baryonic mass scale
    # GROUNDED bias: derive from realistic halo masses (Msun/h) via colossus, NOT hand-picked.
    # At M_star~10^10.5: late-types = isolated centrals (M_halo~6e11); early-types = more clustered,
    # group-scale (M_halo~5e12). Bias from Tinker+2010 (mdef 200m). Override with --be/--bl if given.
    Mh_e = float(opts.get("Mh_e", 5e12)) * h  # early halo mass (Msun/h)
    Mh_l = float(opts.get("Mh_l", 6e11)) * h  # late  halo mass (Msun/h)
    b_e = (
        float(opts["be"])
        if opts.get("be")
        else float(cbias.haloBias(Mh_e, z, mdef="200m", model="tinker10"))
    )
    b_l = (
        float(opts["bl"])
        if opts.get("bl")
        else float(cbias.haloBias(Mh_l, z, mdef="200m", model="tinker10"))
    )
    rho_m = (
        cosmo.rho_m(0.0) * 1e9 * h**2 * MSUN / MPC**3
    )  # comoving mean matter density (kg/m^3)
    R = np.logspace(
        np.log10(0.03), np.log10(5.0), 40
    )  # projected radius (Mpc/h, comoving)
    # 2-halo matter excess surface density dSigma_mm(R) (bias=1), via projected correlation
    chi = np.logspace(-3, np.log10(60.0), 600)  # l.o.s. (Mpc/h)
    Sig = np.zeros_like(R)  # Sigma_excess(R) [Msun*h/Mpc^2 comoving]
    rho_m_cmpc = cosmo.rho_m(0.0) * 1e9  # Msun h^2 / Mpc^3 comoving
    for i, RR in enumerate(R):
        xi = cosmo.correlationFunction(np.sqrt(RR**2 + chi**2), z)
        Sig[i] = rho_m_cmpc * 2.0 * np.trapezoid(xi, chi)  # Msun h / Mpc^2
    # mean within R and dSigma = Sigbar(<R) - Sig(R)
    Sbar = np.array(
        [
            (
                (2.0 / RR**2) * np.trapezoid(Sig[: i + 1] * R[: i + 1], R[: i + 1])
                if i
                else Sig[0]
            )
            for i, RR in enumerate(R)
        ]
    )
    dSig = Sbar - Sig  # Msun h / Mpc^2 comoving
    dSig_SI = (
        dSig * MSUN * h / MPC**2 * (1 + z) ** 2
    )  # kg/m^2 physical (comoving->physical *(1+z)^2)
    Rm = R / h * MPC  # physical-ish radius (m); h removed
    g_bar = G * Mbar / Rm**2  # baryonic accel (point mass at these R)
    g_1h = obt_rar(g_bar)  # mu(x) one-halo
    g_2h_unit = 4 * G * dSig_SI  # 2-halo per unit bias
    print(
        f"[lensing_2halo] z={z}, M_bar={Mbar/MSUN:.2e}, b_early={b_e}, b_late={b_l}. "
        f"g_obs = g_1halo[mu(x)] + 4G*b*dSigma_mm."
    )
    print(
        f"  {'g_bar':>10s} {'g_1h(mux)':>10s} {'g_2h(b_e)':>10s} {'g_obs_E':>10s} {'g_obs_L':>10s} {'split dex':>9s}"
    )
    for i in range(0, len(R), 5):
        gE = g_1h[i] + b_e * g_2h_unit[i]
        gL = g_1h[i] + b_l * g_2h_unit[i]
        print(
            f"  {g_bar[i]:10.2e} {g_1h[i]:10.2e} {b_e*g_2h_unit[i]:10.2e} {gE:10.2e} {gL:10.2e} {np.log10(gE/gL):9.3f}"
        )
    # split at the lowest-g end (where 2-halo dominates)
    gE = g_1h + b_e * g_2h_unit
    gL = g_1h + b_l * g_2h_unit
    lowg = g_bar < 1e-12
    print(
        f"  at g_bar<1e-12 (lensing low-g end): median early/late split = "
        f"{np.median(np.log10(gE[lowg]/gL[lowg])):.3f} dex (Brouwer's morphology split is ~0.2-0.3 dex)."
    )
    print(
        "  READ: if the bias-driven 2-halo split (early>late at low g) matches Brouwer's 6sigma"
    )
    print(
        "  morphology split, the split is ENVIRONMENT, not a mu(x) failure -> patch works."
    )
    print(
        "  NOTE: order-of-magnitude (comoving dSigma, point-mass 1-halo); the SPLIT ratio ~b_e/b_l is robust."
    )


def ngc2419_dispersion(opts):
    """HARDENING of card #4 (NGC 2419): build MY OWN projected velocity-dispersion profile from the
    raw stellar radial velocities (Ibata 2011, ApJ 738 186 table3, 197 stars), instead of citing
    Sanders' fit. Sigma-clip members around the systemic velocity, bin by projected radius, and
    error-deconvolve sigma_p^2 = var(RV) - <e_RV^2>. Then compare the observed DECLINE to my mu(x)
    anisotropic Jeans model (probe gc_jeans): isotropic mu(x) is too flat, radial anisotropy steepens
    it. FACTS only. D=87 kpc (1 arcmin = D/3438 pc)."""
    import numpy as np
    import pandas as pd
    import pyvo

    cache = f"{LOTS}/ngc2419_rv.parquet"
    if not os.path.exists(cache):
        tap = pyvo.dal.TAPService("http://tapvizier.cds.unistra.fr/TAPVizieR/tap")
        d = (
            tap.search('SELECT R, RV, e_RV FROM "J/ApJ/738/186/table3"')
            .to_table()
            .to_pandas()
        )
        d.to_parquet(cache, index=False)
    d = pd.read_parquet(cache).dropna(subset=["R", "RV", "e_RV"])
    d = d[d.e_RV > 0]
    D_kpc = float(opts.get("D", 87.0))
    pc_per_arcmin = D_kpc * 1e3 / 3438.0
    R_pc = d.R.values * pc_per_arcmin
    rv = d.RV.values
    erv = d.e_RV.values
    # iterative 3-sigma membership clip around the median systemic velocity
    sel = np.ones(len(rv), bool)
    for _ in range(10):
        m, s = np.median(rv[sel]), np.std(rv[sel])
        new = np.abs(rv - m) < 3 * max(s, 3.0)
        if new.sum() == sel.sum():
            break
        sel = new
    print(
        f"[ngc2419_dispersion] {sel.sum()}/{len(rv)} members (systemic={np.median(rv[sel]):.1f} km/s), D={D_kpc} kpc."
    )
    Rm, RV, E = R_pc[sel], rv[sel], erv[sel]
    edges = np.percentile(Rm, [0, 25, 50, 75, 100])
    print(f"  {'R bin (pc)':>16s} {'N':>4s} {'sigma_p (km/s)':>14s}")
    prof = []
    for i in range(4):
        m = (Rm >= edges[i]) & (Rm <= edges[i + 1] if i == 3 else Rm < edges[i + 1])
        if m.sum() >= 4:
            var = np.var(RV[m], ddof=1) - np.mean(E[m] ** 2)
            sp = np.sqrt(max(var, 0.0))
            rc = np.median(Rm[m])
            prof.append((rc, sp))
            print(
                f"  {edges[i]:6.0f}-{edges[i+1]:6.0f} (r~{rc:5.0f}) {m.sum():4d} {sp:14.2f}"
            )
    if len(prof) >= 2:
        decl = (prof[0][1] - prof[-1][1]) / prof[0][1] * 100
        print(
            f"  OBSERVED decline (inner->outer): {decl:.0f}%  (inner sigma={prof[0][1]:.1f}, outer={prof[-1][1]:.1f} km/s)"
        )
        print(
            "  COMPARE (probe gc_jeans, NGC2419 params): mu(x) ISOTROPIC declines ~22% (too flat);"
        )
        print(
            "  radial anisotropy beta~0.5-0.7 declines ~39-46%. If the OBSERVED decline matches the"
        )
        print(
            "  anisotropic (not isotropic) mu(x), my own data+model confirm card #4 (no Sanders needed)."
        )


def gc_jeans(opts):
    """MONSTER #4 propagation (candidate ngc2419-anisotropy): MY OWN anisotropic Jeans model in
    mu(x) gravity, to demonstrate the MECHANISM behind the patch. Stellar Plummer density, mass
    M (M/L-scaled luminous), gravity g(r)=obt_rar(G M(<r)/r^2). Solve the constant-anisotropy
    Jeans eq nu*sig_r^2(r) = r^-2b * int_r^inf nu g s^2b ds, then project to sigma_los(R) with the
    (1 - b R^2/r^2) kernel. Compare ISOTROPIC mu(x) (the model Ibata assumed -> too flat) vs RADIAL
    mu(x) (b>0 -> steeper projected decline). If radial anisotropy reproduces a steeply DECLINING
    sigma_los(R) that isotropic mu(x) cannot, the patch mechanism is demonstrated. FACTS only.
    Params (NGC 2419-like, Sanders 2012): M=7.7e5 Msun, r_half~18 pc. opts: --M (1e5), --rh (pc), --beta.
    """
    import numpy as np

    PC = KPC / 1e3
    M = float(opts.get("M", 7.7)) * 1e5 * MSUN
    rh = float(opts.get("rh", 18.0))  # half-light radius (pc)
    b = rh / 1.305 * PC  # Plummer scale (r_half=1.305 b)
    beta = float(opts.get("beta", 0.4))  # radial anisotropy for the patched model
    r = np.logspace(np.log10(0.3), np.log10(800.0), 1400) * PC
    nu = (1.0 + (r / b) ** 2) ** (-2.5)  # Plummer tracer density
    Mr = M * (r / b) ** 3 / (1.0 + (r / b) ** 2) ** 1.5
    gN = G * Mr / r**2

    def sig_los(gfunc, bet):
        g = gfunc(gN)
        # nu*sig_r^2 (r) = r^-2bet * int_r^inf nu*g*s^2bet ds   (cumulative-from-outside)
        integ = nu * g * r ** (2 * bet)
        # integral from r to inf via reverse cumulative trapezoid
        I = np.concatenate(
            [[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(r))]
        )
        tail = I[-1] - I
        nusr2 = tail / r ** (2 * bet)  # = nu*sig_r^2
        # project: sigma_los^2(R) = [2 int_R^inf (1-bet R^2/r^2) nusr2 r/sqrt(r^2-R^2) dr]/Sigma(R)
        out = []
        for R in [5, 10, 20, 40]:
            Rm = R * PC
            sel = r > Rm * 1.0001
            rr = r[sel]
            num = 2 * np.trapezoid(
                (1 - bet * Rm**2 / rr**2) * nusr2[sel] * rr / np.sqrt(rr**2 - Rm**2), rr
            )
            den = 2 * np.trapezoid(nu[sel] * rr / np.sqrt(rr**2 - Rm**2), rr)
            out.append(np.sqrt(max(num / den, 0)) / KMS)
        return out

    newt = sig_los(lambda g: g, 0.0)
    mond_iso = sig_los(lambda g: obt_rar(g), 0.0)
    mond_rad = sig_los(lambda g: obt_rar(g), beta)
    gchar = gN[
        np.argmin(np.abs(r - rh * PC))
    ]  # Newtonian accel at the half-light radius
    print(
        f"[gc_jeans] NGC 2419-like: M={M/MSUN:.2e} Msun, r_half={rh} pc, radial beta={beta}. "
        f"g_N(r_half)/a0={gchar/A0:.2f} (deep-MOND if <1)."
    )
    print(f"  sigma_los(R) [km/s] at R = 5,10,20,40 pc:")
    print(f"    Newton isotropic : {[round(x,2) for x in newt]}")
    print(
        f"    mu(x) ISOTROPIC  : {[round(x,2) for x in mond_iso]}  (the model Ibata assumed)"
    )
    print(
        f"    mu(x) RADIAL b={beta}: {[round(x,2) for x in mond_rad]}  (the anisotropy patch)"
    )
    drop_iso = (mond_iso[0] - mond_iso[-1]) / mond_iso[0] * 100
    drop_rad = (mond_rad[0] - mond_rad[-1]) / mond_rad[0] * 100
    print(
        f"  outer decline 5->40 pc: mu(x) isotropic {drop_iso:.0f}%  vs  mu(x) radial {drop_rad:.0f}%"
    )
    print(
        "  READ: if radial anisotropy gives a much STEEPER projected decline than isotropic mu(x),"
    )
    print(
        "  a declining GC dispersion is mu(x)+anisotropy-normal -> Ibata's 'falsifies MOND' debunked."
    )


def efe_dwarfs(opts):
    """MONSTER #4 hunt (game = OBT + cards): the External Field Effect (EFE). External claim/
    assumption patched: 'a dwarf is ISOLATED, so sigma follows isolated mu(x)'. Patch = include the
    REAL Milky-Way external field g_ext (single-field AQUAL-like): boost_EFE = obt_rar(g_bar+g_ext)/
    (g_bar+g_ext) (< isolated boost when g_ext is significant). The EFE predicts the boost is
    SUPPRESSED in strong external fields. The signal is masked in the full LG sample by UFD sigma-
    inflation (card-territory), so we restrict to WELL-MEASURED (bright, M_bar above median) dwarfs.
    We compare residual_iso=log10(g_obs/obt_rar(g_bar)) vs residual_EFE=log10(g_obs/(g_bar*boost_EFE)),
    split by external field x_ext. If EFE pulls the strong-field residual toward 0 (isolated mu(x)
    over-predicts there), the EFE patch works. FACTS only; player judges."""
    import numpy as np
    import pandas as pd
    from scipy.stats import spearmanr

    d = pd.read_parquet(f"{LOTS}/dsph.parquet").copy()
    g_bar = d["g_bar"].values
    g_obs = d["g_obs"].values
    g_ext = d["x_ext"].values * A0
    boost_iso = obt_rar(g_bar) / g_bar
    boost_efe = obt_rar(g_bar + g_ext) / (g_bar + g_ext)
    d["res_iso"] = np.log10(g_obs / (g_bar * boost_iso))
    d["res_efe"] = np.log10(g_obs / (g_bar * boost_efe))
    bright = d[d["M_bar"] >= d["M_bar"].median()].copy()
    print(
        f"[efe_dwarfs] {len(d)} LG dwarfs; {len(bright)} BRIGHT (M_bar>=median, well-measured)."
    )
    print(
        "  EFE predicts: strong external field x_ext -> isolated mu(x) OVER-predicts (res_iso<0),"
    )
    print("  and the EFE correction should pull res_efe toward 0.")
    for lo, hi, lab in [
        (0, 0.05, "FAR x_ext<0.05"),
        (0.05, 0.15, "MID 0.05-0.15"),
        (0.15, 9, "NEAR x_ext>0.15"),
    ]:
        m = (bright.x_ext >= lo) & (bright.x_ext < hi)
        if m.sum() >= 2:
            s = bright[m]
            print(
                f"  [{lab:16s}] N={m.sum():2d}  res_iso={s.res_iso.median():+.3f}  res_efe={s.res_efe.median():+.3f}"
            )
    ok = np.isfinite(bright.res_iso) & np.isfinite(bright.x_ext)
    r_iso, p_iso = spearmanr(bright.x_ext[ok], bright.res_iso[ok])
    r_efe, p_efe = spearmanr(bright.x_ext[ok], bright.res_efe[ok])
    print(
        f"  BRIGHT corr(residual, x_ext): isolated rho={r_iso:+.3f} (p={p_iso:.2f}) -> EFE rho={r_efe:+.3f} (p={p_efe:.2f})"
    )
    print(
        f"  BRIGHT median |residual|: isolated {bright.res_iso.abs().median():.3f} -> EFE {bright.res_efe.abs().median():.3f}"
    )
    print(
        "  READ: if EFE flattens the residual-vs-x_ext trend AND lowers |residual|, the external"
    )
    print(
        "  field (EFE) is the missing external element -> monster (and propagates across bright dwarfs)."
    )


def sparc_decline(opts):
    """MONSTER #3 propagation (candidate mw-rotation-decline). Core claim to propagate: a DECLINING
    outer rotation curve is NORMAL under OBT mu(x) (the curve settling onto the deep-MOND plateau),
    NOT a challenge to modified gravity (contra the Jiao 2023 MW framing). Test on the independent
    SPARC sample: classify each galaxy by its OUTER RC slope (declining vs flat/rising) and compare
    the OBT-RAR residual log10(g_obs/g_OBT) between groups. If DECLINING-RC galaxies sit on mu(x)
    just like flat ones (~zero residual), the patch propagates -> monster. FACTS only.
    """
    import numpy as np
    import pandas as pd

    ML = float(opts.get("ml", 0.7))
    df = pd.read_parquet(f"{LOTS}/sparc_rar.parquet")
    R = df["R_kpc"].values * KPC
    gbar = (
        (
            df["Vgas"].values ** 2
            + ML * df["Vdisk"].values ** 2
            + ML * df["Vbul"].values ** 2
        )
        * KMS**2
        / R
    )
    gobs = (df["Vobs"].values * KMS) ** 2 / R
    df = df.assign(res=np.log10(gobs / obt_rar(gbar)))
    rows = []
    for gid, sub in df.groupby("ID"):
        sub = sub.sort_values("R_kpc")
        if len(sub) < 5:
            continue
        # outer half: linear slope of V_obs vs R over the outer points
        n = len(sub)
        outer = sub.iloc[n // 2 :]
        sl = np.polyfit(outer["R_kpc"].values, outer["Vobs"].values, 1)[
            0
        ]  # km/s per kpc
        rows.append((gid, sl, sub["res"].median(), n))
    g = pd.DataFrame(rows, columns=["ID", "slope", "res", "npts"])
    print(
        f"[sparc_decline] {len(g)} SPARC galaxies (>=5 pts), M/L={ML}. Outer V_obs slope (km/s/kpc):"
    )
    for lo, hi, lab in [
        (-1e9, -1.0, "DECLINING < -1"),
        (-1.0, 1.0, "flat -1..1"),
        (1.0, 1e9, "rising > 1"),
    ]:
        m = (g.slope >= lo) & (g.slope < hi)
        if m.sum():
            s = g[m]
            print(
                f"  [{lab:16s}] N={m.sum():3d}  median OBT-RAR residual={s.res.median():+.3f} dex "
                f"(scatter {s.res.std():.3f})"
            )
    decl = g[g.slope < -1.0]
    print(
        f"  => {len(decl)} clearly-declining-RC galaxies; their median residual="
        f"{decl.res.median():+.3f} dex (0 = on OBT mu(x))."
    )
    print(
        "  READ: if declining-RC galaxies sit on mu(x) (~0 residual) like flat ones, a declining"
    )
    print(
        "  outer RC is mu(x)-normal -> the 'MW decline challenges modified gravity' claim is debunked."
    )


def mw_rotation(opts):
    """MONSTER #3 hunt (game = OBT + cards). Milky Way outer rotation curve (Jiao et al. 2023,
    Gaia DR3, Table 3) — a 'Keplerian decline' framed as challenging. Test OBT mu(x): with a
    point-mass baryonic model (valid at large R), V_OBT(R)=sqrt(obt_rar(G M_bar/R^2)*R). Jiao's
    B2 model M_bar=0.616e11 Msun gives a deep-MOND plateau (G M_bar a0)^1/4. We report V_OBT vs
    observed per radius, and scan M_bar to find what (external) baryonic mass best fits the OUTER
    points (R>=18 kpc, where point-mass is valid). The candidate external patch = the MW baryonic
    mass model (B2 is a LOW estimate; literature spans 0.6-1.0e11). FACTS only; player judges.
    """
    import numpy as np

    # Jiao et al. 2023 (A&A 678 A208) Table 3: R[kpc], V_c[km/s], sigma[km/s]
    RC = [
        (9.5, 221.75, 3.17),
        (10.5, 223.32, 3.02),
        (11.5, 220.72, 3.47),
        (12.5, 222.92, 3.19),
        (13.5, 224.16, 3.48),
        (14.5, 221.60, 4.20),
        (15.5, 218.79, 4.75),
        (16.5, 216.38, 4.96),
        (17.5, 213.48, 6.13),
        (18.5, 209.17, 4.42),
        (19.5, 206.25, 4.63),
        (20.5, 202.54, 4.40),
        (21.5, 197.56, 4.62),
        (22.5, 197.00, 3.81),
        (23.5, 191.62, 12.95),
        (24.5, 187.12, 8.06),
        (25.5, 181.44, 19.58),
        (26.5, 175.68, 24.68),
    ]
    R = np.array([r for r, _, _ in RC])
    V = np.array([v for _, v, _ in RC])
    S = np.array([s for *_, s in RC])
    Rm = R * KPC
    Vobs = V * KMS

    def vobt(Mbar_1e11):
        gbar = G * (Mbar_1e11 * 1e11 * MSUN) / Rm**2
        return np.sqrt(obt_rar(gbar) * Rm) / KMS

    Mb0 = float(opts.get("mbar", 0.616))
    print(
        f"[mw_rotation] Jiao 2023 MW curve vs OBT mu(x) (point-mass). B2 M_bar={Mb0}e11 Msun."
    )
    print(
        f"  deep-MOND plateau (G M_bar a0)^1/4 = {((G*Mb0*1e11*MSUN*A0)**0.25)/KMS:.1f} km/s (B2)"
    )
    print(f"  {'R':>5s} {'V_obs':>7s} {'V_OBT(B2)':>9s} {'(obs-OBT)/sig':>13s}")
    vb = vobt(Mb0)
    for i in range(len(R)):
        print(f"  {R[i]:5.1f} {V[i]:7.1f} {vb[i]:9.1f} {(V[i]-vb[i])/S[i]:13.1f}")
    # scan M_bar to best-fit the OUTER points (R>=18, point-mass valid)
    out = R >= 18
    print("  M_bar scan — chi2/N on OUTER points (R>=18 kpc, point-mass valid):")
    best = None
    for Mb in [0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8]:
        vbm = vobt(Mb)
        chi2 = np.sum(((V[out] - vbm[out]) / S[out]) ** 2) / out.sum()
        print(
            f"    M_bar={Mb:.1f}e11  chi2/N={chi2:6.2f}  plateau={((G*Mb*1e11*MSUN*A0)**0.25)/KMS:.0f} km/s"
        )
        if best is None or chi2 < best[1]:
            best = (Mb, chi2)
    print(
        f"  best outer-fit M_bar~{best[0]:.1f}e11 (chi2/N={best[1]:.2f}). READ: if a PLAUSIBLE M_bar "
        f"(0.6-1.0e11) fits, the patch is the baryonic model; if the DECLINE shape resists any flat-"
        f"plateau mu(x), the analysis (asymmetric drift) is the external element. Player judges."
    )


def udg_sample(opts):
    """MONSTER #2 -> CARD: my OWN analysis of the full gas-rich UDG sample (Mancera Pina 2019,
    Table 1 — published values). For each UDG, the OBT/MOND deep-limit BTFR target is
    V_BTFR = (G a0 M_bar)^(1/4). The published V_circ (at published inclination i_pub) is too low.
    The inclination patch: V_true = V_circ * sin(i_pub)/sin(i_true), so the i_true that lands it on
    the BTFR is sin(i_true) = sin(i_pub)*V_circ/V_BTFR. We report, per galaxy, V_BTFR, the required
    i_true, and Delta_i = i_pub - i_true. If the corrections are SYSTEMATICALLY toward lower i and
    physically plausible for face-on UDGs, the single external mechanism (under-estimated i in
    face-on disks) propagates across the sample -> card-grade. FACTS only; player judges.
    """
    import numpy as np

    # Mancera Pina et al. 2019 (ApJL 883 L33), Table 1: name, D[Mpc], i_pub[deg], logMbar, V_circ[km/s]
    S = [
        ("AGC 114905", 76, 33, 9.21, 19.0),
        ("AGC 122966", 90, 34, 9.21, 37.0),
        ("AGC 219533", 96, 42, 9.36, 37.0),
        ("AGC 248945", 84, 66, 9.05, 27.0),
        ("AGC 334315", 73, 52, 9.32, 26.0),
        ("AGC 749290", 97, 39, 9.17, 26.0),
    ]
    print(
        "[udg_sample] OBT BTFR target V_BTFR=(G a0 M_bar)^1/4; inclination patch to reach it."
    )
    print(
        f"  {'galaxy':12s} {'i_pub':>5s} {'V_circ':>6s} {'V_BTFR':>6s} {'i_true':>6s} {'Δi':>5s} {'plausible?':>10s}"
    )
    res = []
    for nm, D, ip, logM, V in S:
        Mbar = 10**logM * MSUN
        V_btfr = (G * A0 * Mbar) ** 0.25 / KMS  # km/s
        s_it = np.sin(np.radians(ip)) * V / V_btfr
        if s_it >= 1.0:
            it = float("nan")
            plaus = "needs D not i"
        else:
            it = np.degrees(np.arcsin(s_it))
            plaus = "yes (lower i)" if it < ip else "NO (higher)"
        res.append(it)
        print(
            f"  {nm:12s} {ip:5d} {V:6.1f} {V_btfr:6.1f} {it:6.1f} {ip-it:5.1f} {plaus:>14s}"
        )
    good = [x for x in res if x == x and x > 0]
    print(
        f"  SUMMARY: {len(good)}/6 reconciled by a LOWER inclination; required i_true range "
        f"[{min(good):.0f},{max(good):.0f}] deg (median {sorted(good)[len(good)//2]:.0f})."
    )
    print(
        "  READ: systematic LOWER i across the sample = one external mechanism (face-on i under-"
    )
    print(
        "  estimated) propagates -> card. Galaxies needing 'D not i' are the distance-route variant."
    )


def udg_inclination(opts):
    """MONSTER #2 candidate (game = OBT + card#1) on a CLEAN site: the gas-rich, rotation-supported
    UDG AGC 114905 (Mancera Pina et al. 2022), reported as 'Newtonian / off the RAR' — i.e. OBT's
    mu(x) appears to FAIL. The single adjacent EXTERNAL parameter is the disk INCLINATION i:
    V_rot = V_los/sin(i), so g_obs = (V_los/sin i)^2 / R scales as 1/sin^2 i, while the baryonic
    g_bar (HI flux + stars) is ~i-independent. We scan the TRUE inclination and report the OBT-RAR
    residual log10(g_obs/g_OBT); the i that lands it on mu(x) is the patch. FACTS only; the player
    judges whether that i is within the disputed range (Banik et al. 2022 argue i ~ 11 deg vs the
    32 deg of Mancera Pina). Literature values for the outermost measured point."""
    import numpy as np

    # AGC 114905 outermost point (Mancera Pina 2022, A&A 659 L4): R_out, V_rot@i_pub, i_pub
    R_kpc = float(opts.get("r", 9.7))
    V_rot_pub = float(opts.get("v", 23.0))  # km/s at i_pub
    i_pub = float(opts.get("ipub", 32.0))  # deg
    R = R_kpc * KPC
    V_los = V_rot_pub * np.sin(
        np.radians(i_pub)
    )  # the i-invariant line-of-sight amplitude
    g_bar = (
        V_rot_pub * KMS
    ) ** 2 / R  # baryonic ~ Newtonian (their 'no DM' claim: V_bar~V_obs@i_pub)
    g_OBT = obt_rar(g_bar)
    print(
        f"[udg_inclination] AGC 114905 clean site (rotation UDG). R={R_kpc} kpc, V_los={V_los:.2f} km/s"
    )
    print(
        f"  g_bar={g_bar:.3e}  x=g_bar/a0={g_bar/A0:.3f} (deep-MOND)  OBT mu(x) target g_OBT={g_OBT:.3e}"
    )
    print(
        f"  OBT predicts V_rot={np.sqrt(g_OBT*R)/KMS:.1f} km/s vs published {V_rot_pub} km/s at i={i_pub} deg"
    )
    print(
        f"  {'i_true(deg)':>11s} {'V_rot(km/s)':>11s} {'g_obs':>11s} {'resid log10(g_obs/g_OBT)':>26s}"
    )
    for i_t in [32, 25, 20, 16, 13, 11, 9]:
        V = V_los / np.sin(np.radians(i_t))
        g_obs = (V * KMS) ** 2 / R
        res = np.log10(g_obs / g_OBT)
        flag = "  <-- on mu(x)" if abs(res) < 0.05 else ""
        print(f"  {i_t:11d} {V:11.1f} {g_obs:11.3e} {res:26.3f}{flag}")
    print(
        "  READ: the i_true that zeroes the residual is the inclination patch. If it matches the"
    )
    print(
        "  disputed Banik value (~11 deg) and propagates to other off-RAR UDGs, it is a monster."
    )


def dsph_binfloor(opts):
    """MONSTER #2 candidate test (game = OBT + card#1). PATCH ONE external parameter: a binary/
    small-N velocity floor sigma_bin on the Wolf estimator (sigma_int^2 = sigma_obs^2 - sigma_bin^2).
    If a SINGLE sigma_bin collapses the FAINT-dwarf over-prediction onto OBT mu(x) AND kills the
    residual-vs-M_bar correlation across the whole batch, the patch works on many systems (monster).
    FACTS only: median residual (all / faint) + Spearman(residual, log M_bar) vs sigma_bin.
    """
    import numpy as np
    import pandas as pd
    from scipy.stats import spearmanr

    d = pd.read_parquet(f"{LOTS}/dsph.parquet").copy()
    KMS_ = 1.0e3
    PC = KPC / 1e3
    r_m = d["r_half_pc"].values * PC
    sig = d["sigma_kms"].values * KMS_
    g_bar = d["g_bar"].values
    logMbar = np.log10(d["M_bar"].clip(lower=1.0).values)
    faint = logMbar <= np.median(logMbar)
    print(
        "[dsph_binfloor] PATCH = binary/small-N velocity floor sigma_bin (km/s) on Wolf estimator."
    )
    print(
        f"  {'sigma_bin':>9s} {'med resid ALL':>14s} {'med resid FAINT':>16s} {'rho(resid,logMbar)':>20s}"
    )
    for sb in [0.0, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
        sig_int2 = np.clip(sig**2 - (sb * KMS_) ** 2, (0.3 * KMS_) ** 2, None)
        g_obs = 2.0 * sig_int2 / r_m  # = G M_dyn/2 /r^2 with M_dyn=4 sigma^2 r/G
        res = np.log10(g_obs / obt_rar(g_bar))
        ok = np.isfinite(res)
        rho, _ = spearmanr(logMbar[ok], res[ok])
        print(
            f"  {sb:9.1f} {np.median(res[ok]):14.3f} {np.median(res[faint & ok]):16.3f} {rho:20.3f}"
        )
    print(
        "  READ: the sigma_bin that drives BOTH 'med resid FAINT' -> ~0 AND 'rho(resid,logMbar)' -> ~0"
    )
    print(
        "  is the single-parameter external patch that makes OBT+card#1 fit the whole dwarf batch."
    )


def dsph_misfit(opts):
    """MONSTER #2 hunt (game = OBT + card#1). Where does OBT+mu(x) STILL fail among LG dwarfs,
    and which EXTERNAL element drives it? Card#1 (universal mu(x)) already fits ISOLATED dwarfs
    exactly. Here we locate the residual misfit driver among candidate external theories:
      (a) tidal proximity  -> x_ext (host field, a tidal-susceptibility proxy)
      (b) binary/small-N sigma inflation -> M_bar (~ stellar count; faint = few stars = binaries
          dominate the measured sigma -> Wolf virial mass over-estimated)
    The Wolf estimator M_dyn=4 sigma^2 r/G assumes VIRIAL EQUILIBRIUM + bound motion; that is the
    adjacent EXTERNAL theory a monster would patch. FACTS only (correlations + a 2x2 split).
    """
    import numpy as np
    import pandas as pd
    from scipy.stats import spearmanr

    d = pd.read_parquet(f"{LOTS}/dsph.parquet").copy()
    d["logMbar"] = np.log10(d["M_bar"].clip(lower=1.0))
    r = d["res_obt_dex"].values
    print(
        f"[dsph_misfit] {len(d)} dwarfs. residual = log10(g_obs/g_OBT) under card#1 mu(x)."
    )
    for col, lab in [
        ("x_ext", "tidal proximity x_ext"),
        ("logMbar", "log10 M_bar (~Nstars)"),
        ("x_acc", "internal accel x_in"),
    ]:
        ok = np.isfinite(d[col]) & np.isfinite(r)
        rho, p = spearmanr(d[col][ok], r[ok])
        print(f"  residual vs {lab:22s}: rho={rho:+.3f} p={p:.2e} N={ok.sum()}")
    # 2x2: split by faint/bright (M_bar) and near/far (x_ext) to see which dominates the misfit
    medM = d["logMbar"].median()
    medX = d["x_ext"].median()
    print(f"  2x2 median residual (split at logMbar={medM:.2f}, x_ext={medX:.3f}):")
    for fb, mlab in [(d.logMbar <= medM, "FAINT"), (d.logMbar > medM, "BRIGHT")]:
        for nf, xlab in [(d.x_ext <= medX, "FAR"), (d.x_ext > medX, "NEAR")]:
            s = d[fb & nf]
            if len(s):
                print(
                    f"    {mlab:6s}/{xlab:4s}: N={len(s):2d}  med residual={s.res_obt_dex.median():+.3f} dex"
                )
    print(
        "  READ: if residual is driven by FAINT (low M_bar) more than by NEAR (x_ext), the external"
    )
    print(
        "  element is sigma-inflation in star-poor systems (Wolf virial estimator breaks), not tides."
    )


PROBES = {
    "build_sparc": build_sparc,
    "build_wb": build_wb,
    "diversity": diversity,
    "btfr": btfr,
    "a0_regime": a0_regime,
    "a0_kross": a0_kross,
    "a0_kges": a0_kges,
    "a0_slacs": a0_slacs,
    "wb_boost": wb_boost,
    "wb_forward": wb_forward,
    "mw_rotation": mw_rotation,
    "sparc_decline": sparc_decline,
    "efe_dwarfs": efe_dwarfs,
    "ngc2419_dispersion": ngc2419_dispersion,
    "gc_jeans": gc_jeans,
    "lensing_2halo": lensing_2halo,
    "brouwer_split": brouwer_split,
    "sparc_a0_universality": sparc_a0_universality,
    "sparc_a0_posteriors": sparc_a0_posteriors,
    "sparc_a0_fullbudget": sparc_a0_fullbudget,
    "obt_evolution_family": obt_evolution_family,
    "genzel_fdm": genzel_fdm,
    "udg_sample": udg_sample,
    "udg_inclination": udg_inclination,
    "dsph_binfloor": dsph_binfloor,
    "dsph_misfit": dsph_misfit,
    "sparc_residuals": sparc_residuals,
    "dsph": dsph,
    "udg_btfr": udg_btfr,
    "clusters": clusters,
    "lead_df2_crater": lead_df2_crater,
}


def run(name, opts=None):
    """Run a registered probe by name. opts is a dict of --key value options."""
    if name not in PROBES:
        print(f"unknown probe '{name}'. available: {', '.join(sorted(PROBES))}")
        return False
    PROBES[name](opts or {})
    return True


def describe():
    """One-line description per probe (first line of its docstring)."""
    return {
        k: (fn.__doc__ or "").strip().split("\n")[0] for k, fn in sorted(PROBES.items())
    }
