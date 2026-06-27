"""DIG: the ~15% LOCAL-ANCHOR tension -- a0(0)=cH0/2pi vs the measured MOND a0 (reviewer mode, both ways).

Two questions, kept separate:
  (A) Is the ~13-15% offset a REAL tension, given the measured a0's error budget?
  (B) Is the 1/2pi coefficient actually DERIVED (clean Unruh=Gibbons-Hawking), or a numerical coincidence?

(A) The canonical MOND scale (McGaugh, Lelli & Schombert 2016, PRL 117, 201101) is
       g_dagger = 1.20 +- 0.02 (random) +- 0.24 (SYSTEMATIC, dominated by the stellar M/L normalization) x1e-10.
    For comparison to a THEORY value the SYSTEMATIC floor (+-0.24, ~20%) is the relevant one (it shifts a0
    coherently via Upsilon_*). cH0/2pi sits inside it -> we compute the n_sigma both ways.

(B) The OBT text derives a0 = cH0/2pi by INVERTING the Unruh relation T=hbar*a/(2*pi*c*kB) and setting T=T_GH.
    We check that algebra explicitly. T_GH = hbar*H0/(2*pi*kB) (Gibbons-Hawking / de Sitter). Then:
       Unruh-inversion: a0 = 2*pi*c*kB*T_GH/hbar = c*H0   (the 2pi's CANCEL -> NOT cH0/2pi; 2pi too big!)
       thermal-freq   : a0 =       c*kB*T_GH/hbar = cH0/2pi (this is the form that gives the OBT value)
    So 'Unruh temp = GH temp' gives a0 = cH0 (~5x the data); the cH0/2pi value needs a DIFFERENT relation
    (a ~ c x thermal frequency), i.e. the 1/2pi is a choice/coincidence, not the clean Unruh=GH result.
"""

import numpy as np

c = 2.998e8  # m/s
Mpc_m = 3.0857e22  # m
hbar = 1.0546e-34  # J s
kB = 1.381e-23  # J/K

# measured MOND scale (McGaugh-Lelli-Schombert 2016), x1e-10 m/s^2
A0_MOND, A0_RAND, A0_SYST = 1.20, 0.02, 0.24


def H0_si(H0_kms_mpc):
    return H0_kms_mpc * 1e3 / Mpc_m  # 1/s


def a0_forms(H0_kms_mpc):
    H0 = H0_si(H0_kms_mpc)
    T_GH = hbar * H0 / (2 * np.pi * kB)  # Gibbons-Hawking temperature (K)
    return {
        "cH0/2pi (OBT value)": c * H0 / (2 * np.pi),
        "cH0 (clean Unruh=GH)": c * H0,
        "cH0/6 (other common form)": c * H0 / 6.0,
        "c*kB*T_GH/hbar (thermal-freq)": c * kB * T_GH / hbar,
        "2pi*c*kB*T_GH/hbar (Unruh-inv)": 2 * np.pi * c * kB * T_GH / hbar,
    }, T_GH


def main():
    print("=" * 92)
    print(
        "DIG: the local-anchor 'tension' a0(0)=cH0/2pi vs measured MOND a0 = 1.20 +-0.02(rand) +-0.24(syst)"
    )
    print("=" * 92)

    print(
        "\n[A] Numbers vs the measured a0, at three H0 (a0 is a LOCAL z~0 measurement):"
    )
    print(
        f"    measured: a0 = {A0_MOND} +-{A0_RAND}(rand) +-{A0_SYST}(syst) x1e-10 m/s^2  (MLS 2016)\n"
    )
    print(
        f"  {'H0':>5} | {'cH0/2pi':>9} | offset% | {'n_sig(rand)':>11} | {'n_sig(syst)':>11} | verdict"
    )
    for H0 in (67.4, 70.0, 73.0):
        forms, _ = a0_forms(H0)
        a0 = forms["cH0/2pi (OBT value)"] / 1e-10
        off = (A0_MOND - a0) / A0_MOND * 100
        ns_rand = abs(A0_MOND - a0) / A0_RAND
        ns_syst = abs(A0_MOND - a0) / A0_SYST
        verdict = "CONSISTENT (within syst)" if ns_syst < 1 else "tension"
        print(
            f"  {H0:>5.1f} | {a0:>9.3f} | {off:>6.1f}% | {ns_rand:>10.1f}s | {ns_syst:>10.2f}s | {verdict}"
        )
    print(
        "  -> vs the SYSTEMATIC floor (+-0.24, the Upsilon_*-dominated absolute-scale error) the offset is"
        " <=0.7 sigma = NOT a significant tension. (vs the random +-0.02 it looks ~8-13 sigma, but that is the"
        " precision of the MEAN at fixed M/L, NOT the absolute-scale error -- the wrong comparison for a theory.)"
    )

    print(
        "\n[B] Is the 1/2pi coefficient DERIVED? Check the Unruh=GH algebra at H0=67.4:"
    )
    forms, T_GH = a0_forms(67.4)
    print(f"    T_GH = hbar*H0/(2pi*kB) = {T_GH:.3e} K")
    for label, val in forms.items():
        ratio = val / (A0_MOND * 1e-10)
        print(
            f"    a0 [{label:32s}] = {val:.3e} = {val/1e-10:6.3f} x1e-10  ({ratio:4.2f}x the data)"
        )
    print(
        "  -> 'Unruh temp = GH temp' (a0=2pi*c*kB*T_GH/hbar) gives a0 = cH0 = ~5.5x the measured a0 -- the 2pi's"
    )
    print(
        "     CANCEL. The OBT value cH0/2pi instead needs a0 = c*kB*T_GH/hbar (a ~ c x thermal frequency), which"
    )
    print(
        "     is NOT the Unruh relation. So the 1/2pi is a thermal-frequency CHOICE + numerical coincidence, not"
    )
    print(
        "     the clean Unruh=GH result. (The published theory.md algebra '2pi*c*kB*T_H/hbar -> cH0/2pi' is off"
    )
    print("     by 2pi: that expression equals cH0.)")

    print("\nVERDICT (both ways):")
    print(
        "  * GOOD for OBT: the ~13% offset (cH0/2pi=1.04 at H0=67.4) is WITHIN the SPARC a0 SYSTEMATIC (+-20%,"
    )
    print(
        "    Upsilon_*-dominated) -> <=0.7 sigma -> NOT a significant tension. (Earlier 'mild ~1 sigma' was a"
    )
    print(
        "    mild OVER-statement; it is really a within-systematic consistency.) At H0=73 it is 0.3 sigma."
    )
    print(
        "  * HONEST for OBT: a0 = cH0/2pi is FORM-derived (a0 propto H0, thermodynamic) but the O(1) COEFFICIENT"
    )
    print(
        "    1/2pi is coincidence-level -- the clean Unruh=GH gives cH0 (~5.5x too big), and other thermal"
    )
    print(
        "    arguments give cH0/6, 2cH0, etc., all within ~15% of each other and the data. This is exactly the"
    )
    print(
        "    Milgrom/Verlinde/McCulloch prior-art status (a0~cH0 to an O(1) factor) that CLAUDE.md already grants."
    )
    print(
        "  * NET: the 'anchor tension' is not a tension; the real lesson is that OBT's a0 is a CONSISTENCY at the"
    )
    print(
        "    ~15% coefficient level, not a sub-15% prediction. theory.md's a0 derivation should fix the 2pi"
    )
    print(
        "    algebra and temper 'the 2pi is exact Matsubara, derived ab initio' -> 'form derived; coefficient O(1)'."
    )


if __name__ == "__main__":
    main()
