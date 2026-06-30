"""Seed 3 (V9.0, quarantined) — THE CLOSURE INTROSPECTION: have we ALREADY solved the closure problem
without making the link? Reviewer mode (axiom: OBT can be FALSE -- I verify, I do not glue). Romain's
question: "n'aurais-tu pas deja de quoi resoudre la fermeture sans avoir fait le lien ?".

THE HYPOTHESIS TO TEST (my over-optimistic first-pass): closure is already at the a0-LEVEL -- the FORM
derived (gates 0-24), the SIGN derived (gates 8-9), the 5:1 DM AMOUNT computed-from-the-germe
(germe_decompression) up to an O(1) coefficient phi0 = the wavefunction of the universe -- exactly the
epistemic status of a0 = cH0/2pi (derived form x an O(1) coefficient). If true, the link just wasn't made.

This audit assembles every closure piece and assesses each HONESTLY (derived / a0-level / genuine IC), and
-- crucially, reviewer mode -- RE-DERIVES the load-bearing number (germe_decompression's 5:1) instead of
citing it. THE AUDIT CATCHES A REAL BUG and the hypothesis FAILS:

  [BUG] germe_decompression.misalignment_omega uses the FULL Planck mass (1.22e28 eV) where Friedmann
        H = sqrt(pi^2 g_*/90) T^2 / M_Pl needs the REDUCED M_Pl (2.435e27 eV). Mixing the convention
        undercounts H by sqrt(8pi)=5.01 -> T_osc 2.24x too big -> Omega 2.24^3 = 11.2x TOO SMALL.
        Corrected Omega_DM h^2(phi0=M_s) = 0.68 (NOT 0.06); the right DM needs phi0 = 0.42 M_s (NOT 1.40).

  [CONSEQUENCE] the corrected radion OVER-produces DM ~6x at the natural phi0~M_s, and Gate 11 already
        showed a 0.36-eV condensate as ALL the DM is dead at galaxies (it would halo them, f<4%). So the
        cosmic 5:1 is NOT cleanly the radion misalignment -- the radion is sub-dominant; the 5:1 is the
        geometric-Weyl amount = the closure IC (gates 0-24's own conclusion). So the AMOUNT is NOT at the
        a0-level; only the SIGN is derived.

VERDICT (honest, reviewer mode): the hypothesis is FALSE -- we did NOT secretly solve closure. The audit
CONFIRMS + SHARPENS the gates-0-24 conclusion: the FORM is derived, the SIGN is derived (within premises),
the AMOUNT (cosmic 5:1 + cluster factor-2) remains the genuine closure IC (the bulk integration constants /
the Weyl amplitude). My first-pass was too optimistic; the germe_decompression 5:1 was buggy + over-produces
+ conflicts with Gate 11. What WOULD close it = pin the Weyl amount / the germe's quantum state (PATH 2, the
quantum simulation) -- still genuinely open.

NOT V8.2. Not in the PDF. 'code, don't plead': the misalignment is re-derived with both Planck conventions,
the bug + the corrected numbers are computed and asserted, the ledger is explicit.
"""

import numpy as np

# cosmology constants in eV (matching germe_decompression.py for a like-for-like check)
M_PL_FULL = 1.2209e28  # full Planck mass (G^-1/2) -- what germe_decompression used
M_PL_RED = M_PL_FULL / np.sqrt(
    8 * np.pi
)  # reduced Planck mass (8piG)^-1/2 = 2.435e27 eV (CORRECT)
T0 = 2.35e-4  # CMB temperature today, eV
GS0, GSTAR = 3.91, 106.75  # entropy dof today / at oscillation onset
RHO_C = 8.1e-11  # rho_c,0 / h^2, eV^4
OMEGA_B_H2 = 0.0224
OMEGA_DM_H2 = 0.120
M_S = 1.19e21  # OBT LVS string scale = 1.19e12 GeV, in eV
M_PHI = 0.36  # OBT radion (Goldberger-Wise) mass, eV


def misalignment_omega(phi0, m, m_pl):
    """Radiation-era vacuum-misalignment relic Omega h^2 (constant mass). m_pl sets the Friedmann H:
    3H(T_osc)=m with H = sqrt(pi^2 g_*/90) T^2 / m_pl -> T_osc = sqrt(m m_pl/(3 sqrt(pi^2 g_*/90))).
    """
    t_osc = (m * m_pl / (3 * np.sqrt(np.pi**2 * GSTAR / 90))) ** 0.5
    rho_osc = 0.5 * m**2 * phi0**2
    dilution = (GS0 / GSTAR) * (T0 / t_osc) ** 3
    return rho_osc * dilution / RHO_C, t_osc


def main():
    print("=" * 94)
    print(
        " THE CLOSURE INTROSPECTION — have we already solved closure? (reviewer mode: OBT can be FALSE)"
    )
    print("=" * 94)

    # ===== [1] re-derive the load-bearing number: germe_decompression's 5:1 ==========
    print(
        "\n[1] RE-DERIVE the 5:1 (germe_decompression) -- FULL vs REDUCED Planck mass in Friedmann"
    )
    omega_full, tosc_full = misalignment_omega(
        M_S, M_PHI, M_PL_FULL
    )  # what germe_decompression used
    omega_red, tosc_red = misalignment_omega(
        M_S, M_PHI, M_PL_RED
    )  # the CORRECT Friedmann
    print(
        f"    germe_decompression (FULL M_Pl, the bug): T_osc={tosc_full/1e12:.1f} TeV, Omega(M_s) h^2={omega_full:.3f}"
    )
    print(
        f"    CORRECT (REDUCED M_Pl, Friedmann)       : T_osc={tosc_red/1e12:.1f} TeV, Omega(M_s) h^2={omega_red:.3f}"
    )
    print(
        f"    => the bug factor = (T_full/T_red)^3 = {(tosc_full/tosc_red)**3:.1f}  (T~sqrt(M_Pl) so = (8pi)^(3/4) = {(8*np.pi)**0.75:.1f})"
    )
    print(
        f"    => germe_decompression's Omega(M_s)=0.06 is ~11x TOO LOW; the correct value is {omega_red:.2f}."
    )
    # only the VERIFIABLE is asserted: I reproduce germe_decompression's number with the FULL mass, and
    # the bug factor is the exact math identity (8pi)^(3/4). The corrected Omega is a RESULT, reported.
    assert (
        abs(omega_full - 0.06) < 0.02
    ), "I must reproduce germe_decompression's number with the FULL mass (the cross-check that pins the bug)"
    assert (
        abs((tosc_full / tosc_red) ** 3 - (8 * np.pi) ** 0.75) < 1.0
    ), "the bug factor is the exact identity (8pi)^(3/4) (T~sqrt(M_Pl), M_Pl ratio sqrt(8pi))"

    # ===== [2] the consequence: phi0 for the right DM, and the over-production ========
    print(
        "\n[2] CONSEQUENCE -- the corrected phi0 for the right DM, and the over-production tension"
    )
    phi0_buggy = M_S * np.sqrt(
        OMEGA_DM_H2 / omega_full
    )  # germe_decompression's 1.40 M_s
    phi0_correct = M_S * np.sqrt(OMEGA_DM_H2 / omega_red)  # the corrected value
    print(
        f"    germe_decompression: phi0 = {phi0_buggy/M_S:.2f} M_s (the published 1.40 M_s)"
    )
    print(
        f"    CORRECTED         : phi0 = {phi0_correct/M_S:.2f} M_s -> the radion OVER-produces {omega_red/OMEGA_DM_H2:.1f}x at phi0=M_s"
    )
    print(
        "    => still O(1) (phi0~0.4 M_s natural), BUT now a mild over-production the natural phi0~M_s must tame;"
    )
    print(
        "       and Gate 11 ALREADY killed a 0.36-eV condensate as ALL the DM (it halos galaxies, f<4%)."
    )
    print(
        "    => so the cosmic 5:1 is NOT cleanly the radion misalignment -- the radion is SUB-DOMINANT;"
    )
    print(
        "       the 5:1 is the geometric-Weyl amount = the closure IC (gates 0-24's own conclusion)."
    )
    assert (
        abs(phi0_buggy / M_S - 1.40) < 0.1
    ), "I must reproduce germe_decompression's published phi0=1.40 M_s with the FULL mass (the cross-check)"
    # phi0_correct is a RESULT of the calc (no imposed range) -- reported above.

    # ===== [3] the closure ledger: piece by piece, the honest epistemic status =======
    print(
        "\n[3] THE CLOSURE LEDGER -- each piece, honest status (derived / a0-level / genuine IC)"
    )
    ledger = [
        (
            "the LAWS / FORM (a0=cH/2pi, mu(x), sinc, mass-tracking, saturated transition)",
            "DERIVED",
            "gates 0-24 + the geometric mu(x); the brane derives the FORM",
        ),
        (
            "the growth SIGN (S8 suppression vs enhancement)",
            "DERIVED*",
            "gates 8-9 Indicial Theorem (c_phys in (0,1]); *conditional on linear-bulk/quasi-static",
        ),
        (
            "the cosmic DM AMOUNT (the 5:1)",
            "IC",
            "the geometric-Weyl amount (bulk integration constant); the radion candidate is buggy+over-produces+sub-dominant",
        ),
        (
            "the cluster Weyl AMPLITUDE (the factor-2)",
            "IC",
            "gate 24: the free bulk Weyl mode amplitude; the FORM is constrained, the amplitude is not",
        ),
        (
            "the a^-3 CLUSTERING (CMB CDM-like growth)",
            "FORM derived",
            "the radion-AeST 2-sector (a_phase_*); Planck-consistent A_dyn=-0.02+-0.44; the amount is IC",
        ),
    ]
    for piece, status, note in ledger:
        print(f"    [{status:>11}] {piece}")
        print(f"                  {note}")
    derived = sum(1 for _, s, _ in ledger if s.startswith("DERIVED") or "derived" in s)
    ic = sum(1 for _, s, _ in ledger if s == "IC")
    print(
        f"    => {derived} pieces derived (FORM + SIGN + clustering-form), {ic} pieces genuine IC (the two AMOUNTS)."
    )
    # the ledger is my HONEST ASSESSMENT (interpretation), reported -- not asserted (no imposed verdict).

    # ===== [4] the a0-level test: is the AMOUNT at a0's epistemic level? ==============
    print(
        "\n[4] THE a0-LEVEL TEST -- is the AMOUNT at a0's status (derived form x an O(1) coefficient)?"
    )
    print(
        "    a0 = cH0/2pi : the FORM (a0 ~ H0) is DERIVED; the 1/2pi is an O(1) coefficient (prior art)."
    )
    print(
        "    the 5:1      : the radion-misalignment FORM exists, BUT (a) the number was buggy (x11),"
    )
    print(
        "                   (b) corrected it OVER-produces at the natural phi0~M_s, (c) Gate 11 makes the"
    )
    print(
        "                   radion sub-dominant -> the 5:1 is the WEYL IC, not a derived-form x O(1)."
    )
    print(
        "    => the SIGN reaches a0-level (a derived theorem); the AMOUNT does NOT (it is a genuine IC,"
    )
    print(
        "       not a derived form with an O(1) coefficient). The hypothesis FAILS for the amount."
    )

    # ===== [5] verdict ===============================================================
    print("\n[5] VERDICT -- did we already solve closure without the link?")
    print(
        "    NO. The audit (reviewer mode) caught a real bug (full-vs-reduced Planck mass, x11) and the"
    )
    print(
        "    over-optimistic first-pass FAILS: the cosmic 5:1 is NOT a clean germe derivation (buggy +"
    )
    print(
        "    over-produces + Gate-11 sub-dominant), so the AMOUNT stays the genuine closure IC."
    )
    print(
        "    WHAT HOLDS (confirmed + sharpened, = gates 0-24): the FORM is derived, the SIGN is derived"
    )
    print(
        "    (within premises), the a^-3 clustering-FORM is derived (Planck-consistent); the two AMOUNTS"
    )
    print("    (cosmic 5:1 + cluster factor-2) remain the bulk's closure ICs.")
    print(
        "    WHAT WOULD CLOSE IT: pin the Weyl amount / the germe's quantum state = the wavefunction of"
    )
    print(
        "    the universe -> exactly PATH 2 (the Pasqal/Rydberg germe simulation). Still genuinely open."
    )
    print(
        "    HONEST NET: closure is NOT secretly solved; it is LOCATED (the two amounts = the germe's"
    )
    print(
        "    quantum state), and the route to a clue is the quantum simulation. My first-pass over-claimed."
    )
    print(
        "    ACTION FLAGGED: fix germe_decompression.py (full->reduced M_Pl; 0.06->0.68; 1.40->0.42 M_s)"
    )
    print("    and the CLAUDE.md numbers that cite it.")

    print(
        "\n  VERIFIED (the only asserts): germe's number reproduced with the FULL mass + the (8pi)^(3/4)"
    )
    print(
        "  bug identity. The corrected Omega=0.68, phi0=0.42 M_s, the ledger and the verdict are CALCULATED /"
    )
    print(
        "  ASSESSED and reported -- no imposed result-ranges (only the calculation counts)."
    )
    print("=" * 94)


if __name__ == "__main__":
    main()
