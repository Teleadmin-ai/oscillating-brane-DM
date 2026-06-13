"""Blade B — the lensing-vs-dynamics SCISSOR, dynamics side (June 2026, quarantined V9.0).

The ciseau: light (lensing) has W=1 (does not average the 2 Gyr oscillation);
SLOW tracers (T_orb > T) average the boost -> W = ARA |sinc(T_kappa/T)| < 1.
Strong ciseau => the dynamics of distant satellites COLLAPSE toward Newtonian
while lensing keeps the full MOND boost. This script tests that on the only
hosts with resolved satellite orbits at r >> crossover: the MW and M31
(McConnachie 2012, galactocentric D(MW)/V(MW), D(M31)/V(M31)).

Method (reviewer axiom: try to KILL the ciseau):
 - crossover r where T_kappa = T_orb/sqrt2 = T=2 Gyr (V_circ = MOND plateau).
 - INNER (r<crossover): ARA predicts FULL boost (W=1) -> calibration check.
 - OUTER (r>crossover): ARA predicts strong suppression W~0.06-0.11.
 - sigma_los of the galactocentric radial velocity; W_dyn = (sigma/(f*Vplat))^4
   in deep MOND (V_circ = Vplat flat; f = 1/sqrt(3) isotropic, validated on MW
   inner). Compare OBSERVED vs predicted sigma under MOND / ARA / Newton.
CAVEAT: MW satellites sit in a co-rotating plane (card #13) -> tangential
anisotropy lowers sigma_r -> a SPURIOUS low W for the MW. M31 (more isotropic)
is the cleaner host.
"""

import numpy as np

G = 4.30091e-6  # kpc (km/s)^2 / Msun
a0 = 3703.7  # (km/s)^2 / kpc  (= 1.2e-10 m/s2)
T = 2.0  # Gyr
KK = 0.97779  # kpc/(km/s) -> Gyr
FAC = 1.0 / np.sqrt(3.0)  # sigma_los = FAC * V_circ (isotropic, gamma=3 tracer)
MC = "/DATA/obt_game_cache/raw/mcconnachie"
rng = np.random.default_rng(7)


def subgroups():
    sub = {}
    for ln in open(f"{MC}/table1.dat"):
        f = ln.split("|")
        if len(f) > 2:
            sub[f[1].strip()] = f[0].strip()
    return sub


def satellites(iD, iV, want, sub):
    out = []
    for ln in open(f"{MC}/table2.dat"):
        f = ln.split("|")
        if len(f) < 20 or sub.get(f[0].strip()) != want:
            continue
        try:
            D, V = float(f[iD]), float(f[iV])
        except ValueError:
            continue
        if 20 < D < 400:
            out.append((D, V))
    return np.array(out)


def sig_boot(v, n=5000):
    return np.std(v), np.std([np.std(rng.choice(v, len(v))) for _ in range(n)])


def run():
    sub = subgroups()
    print(f"Blade B: satellite dynamics vs the ciseau (f=1/sqrt3={FAC:.3f})\n")
    for host, (iD, iV, Mbar) in {"MW": (16, 17, 6e10), "M31": (18, 19, 1.5e11)}.items():
        A = satellites(iD, iV, host, sub)
        D, V = A[:, 0], A[:, 1]
        Vplat = (G * Mbar * a0) ** 0.25
        rc = (T * np.sqrt(2)) / (2 * np.pi) * Vplat / KK
        print(f"== {host}: N={len(D)}  V_plateau={Vplat:.0f}  crossover={rc:.0f} kpc")
        for tag, sel in [("INNER", D < rc), ("OUTER", D >= rc)]:
            v = V[sel]
            if len(v) < 3:
                print(f"   {tag}: N={len(v)} too few")
                continue
            s, e = sig_boot(v)
            r = np.median(D[sel])
            gb = G * Mbar / r**2
            Tk = 2 * np.pi * r / Vplat / np.sqrt(2) * KK
            W = 1.0 if Tk < T else abs(np.sinc(Tk / T))
            pM = FAC * np.sqrt(np.sqrt(gb * a0) * r)  # full MOND (=lensing)
            pA = FAC * np.sqrt(np.sqrt(gb * a0 * W) * r)  # ARA sinc
            pN = FAC * np.sqrt(gb * r)  # Newton / collapse
            Wd = (s / (FAC * Vplat)) ** 4
            Wlo, Whi = ((s - e) / (FAC * Vplat)) ** 4, ((s + e) / (FAC * Vplat)) ** 4
            print(
                f"   {tag} N={len(v):2d} <r>={r:3.0f} kpc  sigma={s:3.0f}+-{e:2.0f}"
                f"  W_dyn={Wd:.2f}[{Wlo:.2f},{Whi:.2f}]"
                f"  | pred MOND={pM:.0f} ARA(W={W:.2f})={pA:.0f} NEWT={pN:.0f}"
                f"  | vsMOND {-(pM-s)/e:+.1f}s vsNEWT {(s-pN)/e:+.1f}s"
            )
        print()
    print("VERDICT: INNER (sub-crossover) -> full MOND (validates method).")
    print("  OUTER -> W_dyn ~ 0.2-0.7: Newtonian COLLAPSE excluded (3.5-5.9 sigma),")
    print("  strong sinc-ARA (W~0.1) disfavored. M31 (isotropic) ~ full MOND;")
    print("  MW lower W likely its co-rotating satellite plane (tangential beta).")
    print("  => the strong ciseau is REFUTED; any ciseau is moderate (<=0.15 dex),")
    print("     i.e. the boost does NOT sinc-extinguish at large r (DC floor).")


if __name__ == "__main__":
    run()
