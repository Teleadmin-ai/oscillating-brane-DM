"""
GATE 8 — the Weyl-DM configuration's radion coupling: the static exact solve.

SCOPE CLARIFICATION (what "the nonlinear solve" decomposes into): the audit's
"nonlinear Weyl-DM configuration" is nonlinear in the FRW-perturbation sense
(delta >> mean), NOT in the bulk-field sense — at halo densities rho/sigma is
minuscule, so the BULK treatment of a lump is exactly LINEAR. The configuration
therefore splits into (i) the lump's static bulk structure & its radion
coupling — computable EXACTLY here — and (ii) its cosmological assembly
history (the a^-3 clustering: still IC/closure data). THE BIT LIVES IN (i).

THE PARITY RESOLUTION. A brane-comoving lump gives an EVEN E(delta z) — no
linear radion coupling — EXCEPT that the AdS WARP breaks z -> -z parity: the
same brane source generates a different bulk response at different depths z_b
(the master potential's -1/(4 z^2) term is the warp). The linear coupling
    c := d ln(dG_bulk) / d ln(z_b)
is therefore warp-derived, of order unity, giving f_osc = c * (dz_b/z_b) ~
c * 0.1 for OBT's radion amplitude — the right size. CRUCIALLY this channel is
LLR-SAFE: it modulates the WEYL/DM sector's effective gravitating mass (halos),
not the laboratory Newton constant (solar-system masses are baryonic, with
negligible Weyl content): the audit's channel-1 exclusion does not apply.
And it is NOT k^3-suppressed like the cosmological drive: the readout happens
at the halo's own internal scales.

THE EXACT SOLVE. Static master equation psi'' = (kappa^2 - 1/(4 z^2)) psi,
kappa^2 = k^2 + m2 (m2 = GW stabilization gap): general solution
    psi(z) = sqrt(z) [ A I0(kappa z) + B K0(kappa z) ]   (EXACT).
BCs: brane (validated junction, static gamma=1): psi'(z_b) - psi(z_b)/(2 z_b)
= S (unit matter source S = -6 C3 sqrt(z_b) Delta / k^2); far boundary
(stable tensor-like Robin, n = -z): psi'(z2) = -(a2fac/z2) psi(z2).
Solve 2x2 -> Omega_b = z_b^{-3/2} psi(z_b) -> the static bulk gravity
    dG = k^4 Omega_b / (3 a^3) / ((3/2) H_c^2 Delta) = -(2/3) k^2 z_b^{5/2} R,
R = Omega_b/S — the SAME readout as Gates 3-5 (validation hook: must
reproduce the dynamic runs' mean dG at matching parameters).

Then sweep z_b at fixed bulk (and the comoving-z2 variant): c = dln dG/dln z_b
-> sign (the bit) and magnitude (f_osc = c * 0.1).
"""

import numpy as np
from scipy.special import i0, i1, k0, k1

C3 = np.sqrt(1.0 + 0.02**2) - 1.0  # dust background at H_i = 0.02 (gates 3-7)


def static_response(z_b, k, z2, a2fac=-1.5, m2=0.0):
    """Exact static solve. Returns (R = Omega_b per unit S, dG in Poisson units
    for the gate-standard dust source)."""
    kap = np.sqrt(k * k + m2)

    def psi_pair(z):
        rz = np.sqrt(z)
        x = kap * z
        f = rz * np.array([i0(x), k0(x)])
        fp = np.array(
            [
                i0(x) / (2 * rz) + rz * kap * i1(x),
                k0(x) / (2 * rz) - rz * kap * k1(x),
            ]
        )
        return f, fp

    fb, fpb = psi_pair(z_b)
    ff, fpf = psi_pair(z2)
    # brane row: psi'(z_b) - psi(z_b)/(2 z_b) = S (unit S = 1)
    rowb = fpb - fb / (2.0 * z_b)
    # far row: psi'(z2) + (a2fac/z2) psi(z2) = 0
    rowf = fpf + (a2fac / z2) * ff
    M = np.array([rowb, rowf])
    rhs = np.array([1.0, 0.0])
    A, B = np.linalg.solve(M.T @ np.eye(2) if False else np.vstack([rowb, rowf]), rhs)
    psi_b = A * fb[0] + B * fb[1]
    R = z_b ** (-1.5) * psi_b  # Omega_b per unit S
    # gate-standard dust readout: S = -6 C3 sqrt(z_b) Delta / k^2 ;
    # dG = k^4 Omega_b/(3 a^3) / (1.5 H_c^2 Delta), a=1/z_b, H_c^2 = 2 C3/a
    dG = -(2.0 / 3.0) * k * k * z_b**2.5 * R
    return R, dG


def battery_validate():
    print("[V] validation hook: static dG vs the dynamic runs' mean dG:")
    for tag, kw, ref in [
        (
            "open-like (z2 deep, m2=0), k=0.6",
            dict(z2=20.0, m2=0.0),
            "+0.06..0.08 (Gate 3a mean)",
        ),
        (
            "compact m2=0, z2=zb+2.5, k=0.6",
            dict(z2=3.5, m2=0.0),
            "+0.0725 (Gate5 [P] m2=0)",
        ),
        (
            "compact m2=0.5 (stabilized)",
            dict(z2=3.5, m2=0.5),
            "~+0.10 osc-mean (Gate5 [B''])",
        ),
    ]:
        _, dG = static_response(1.0, 0.6, **kw)
        print(f"    {tag:34s}: dG_static = {dG:+.4f}   [dyn: {ref}]")


def battery_coupling():
    print("\n[C8] THE COUPLING c = dln(dG)/dln(z_b) — sign (the bit) and size:")
    print(f"    {'config':40s}{'dG(zb=1)':>10s}{'c':>8s}{'f_osc=c*0.1':>12s}")
    for tag, kw, comoving in [
        ("headline: k=0.6, z2=3.5, m2=0.5", dict(k=0.6, z2=3.5, m2=0.5), False),
        ("z2 comoving (z2-zb=2.5 fixed)", dict(k=0.6, z2=None, m2=0.5), True),
        ("far-BC a2=-0.5/z2", dict(k=0.6, z2=3.5, m2=0.5, a2fac=-0.5), False),
        ("m2=1.0 (stiffer GW)", dict(k=0.6, z2=3.5, m2=1.0), False),
        ("m2=0 (unstabilized)", dict(k=0.6, z2=3.5, m2=0.0), False),
        ("k=0.3", dict(k=0.3, z2=3.5, m2=0.5), False),
        ("k=0.15", dict(k=0.15, z2=3.5, m2=0.5), False),
        ("k=0.05 (toward halo-scale limit)", dict(k=0.05, z2=3.5, m2=0.5), False),
        ("open bulk (z2=20)", dict(k=0.6, z2=20.0, m2=0.5), False),
    ]:
        zb = 1.0
        h = 0.02
        kws = dict(kw)
        if comoving:
            d1 = static_response(
                zb * (1 + h), kws["k"], zb * (1 + h) + 2.5, m2=kws["m2"]
            )[1]
            d0 = static_response(
                zb * (1 - h), kws["k"], zb * (1 - h) + 2.5, m2=kws["m2"]
            )[1]
            dgc = static_response(zb, kws["k"], zb + 2.5, m2=kws["m2"])[1]
        else:
            z2v = kws.pop("z2")
            kv = kws.pop("k")
            d1 = static_response(zb * (1 + h), kv, z2v, **kws)[1]
            d0 = static_response(zb * (1 - h), kv, z2v, **kws)[1]
            dgc = static_response(zb, kv, z2v, **kws)[1]
        c = (np.log(np.abs(d1)) - np.log(np.abs(d0))) / (2 * h)
        print(f"    {tag:40s}{dgc:+10.4f}{c:+8.3f}{c*0.1:+12.3f}")
    print("\n    READ: dG > 0 (bulk adds gravity to the lump) and c (the warp-parity-")
    print(
        "    breaking coupling) give f_osc = c * (radion 10%). The SIGN of c is the bit"
    )
    print(
        "    for the Weyl-DM channel; LLR-safe (DM-sector-only modulation); halo-scale"
    )
    print("    readout (not k^3-suppressed like the cosmological drive).")


def battery_final():
    """[FINAL] the derived-S8 run: every chain parameter derived or
    OBT-chronology-fixed. RESULT (June 2026): DlnD = -7.2%..-9.0% (headline
    -7.7%) = SUPPRESSION, inside OBT's claimed -4..-10% window; the wrong sign
    (-f) would give +7.5% enhancement and is EXCLUDED by the warp-derived
    c > 0. Cross-checks: no-filter -11.9%, sinusoid -3.4% (the audit's
    waveform factor-2 spread persists as modeling residual, but the waveform
    itself is now derived = sawtooth)."""
    from gate4_pbh import W_saw, W_sin, growth

    print("[FINAL] derived-S8: sawtooth (Gate6) + sign/size from warp (Gate8)")
    print("        + DM share 5/6 + OBT chronology anchor + 4a filter:")
    for tag, c in [("c=1.27", 1.27), ("c=1.363", 1.363), ("c=1.59", 1.59)]:
        f = c * 0.1 * (5.0 / 6.0)
        print(
            f"    {tag:10s}: f_eff={f:.3f}  DlnD = {growth(+f, W_saw, 'obt', 0.0):+.4f}"
        )
    f = 1.363 * 0.1 * (5.0 / 6.0)
    print(
        f"    wrong sign: DlnD = {growth(-f, W_saw, 'obt', 0.0):+.4f} (EXCLUDED by Gate 8)"
    )


if __name__ == "__main__":
    battery_validate()
    battery_coupling()
    print()
    battery_final()
