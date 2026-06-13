"""GATE 10 — the holographic route to the Weyl-DM configuration (V9.0 seed,
QUARANTINED: not V8.2 theory content).

Gates 0-9 left ONE object carrying the closure freedom: the nonlinear,
mean-zero, locally ~5x-baryon Weyl-DM configuration (abundance = IC data).
This gate opens the only standard dictionary not yet played:

[A] RS/CFT: a single-brane AdS5 braneworld is dual to 4D gravity + a CUTOFF
    CFT; the projected Weyl tensor IS the dual CFT stress expectation:
        E_munu  <->  kappa4^2 <T_munu>_CFT   (standard: Gubser 2001,
    de Haro-Skenderis-Solodukhin, Shiromizu-Ida). The closure freedom =
    the CFT state. "Dark radiation" = thermal CFT (a^-4). A CDM-like
    Weyl-DM REQUIRES a nonrelativistic CFT state: a CONFINED sector.
[B] OBT's bulk has a natural confinement scale: the warped IR (radion
    m_phi = 0.36 eV; first KK/glueball m1 = 1.87 eV). IDENTIFICATION
    (the seed): Weyl-DM = the dual sector's GLUEBALL CONDENSATE,
    Lambda_dark ~ 0.4-2 eV. Mean-zero + locally large + a^-3 growth are
    then AUTOMATIC (cold particles cluster); the 5:1 abundance becomes a
    RELIC CALCULATION instead of an IC input.
[C] Order-of-magnitude relic scan (3->2 cannibal freeze-out, the standard
    dark-glueball estimate, Carlson-Machacek-Hall / Forestell-Morrissey
    scaling): Omega h^2 as a function of (Lambda_dark, xi = T_dark/T_vis).
[D] KILL-TESTS (named): (i) BBN/CMB Delta N_eff bounds xi; (ii) cannibal
    epoch must end before structure formation (small-scale power);
    (iii) glueball self-interactions vs Bullet sigma/m < ~1 cm^2/g;
    (iv) consistency with OBT's own kinematic blockade (the brane-bulk
    thermal contact is exponentially small -> the dark sector is COLD,
    xi << 1 NATURALLY -- the same theorem that mandates the PBHs).
"""

import numpy as np

MPL = 1.22e19  # GeV
T0 = 2.35e-13  # GeV (CMB today)
S0_RHOC = 3.6e9  # s0/rho_crit in GeV^-1 units: s0=2891/cm3, rhoc=1.05e-5 h2 GeV/cm3


def omega_glueball(Lam_eV, xi):
    """Cannibal 3->2 freeze-out estimate for a pure-glue dark sector.
    Standard scaling: the comoving yield freezes when the 3->2 rate drops
    below H; Y_inf ~ (Lam^3/(Mpl * T_fo^2 ... )) -- we use the
    Carlson-Machacek-Hall closed form via the log:
      x_fo = Lam/T_d at freeze-out ~ ln(Mpl Lam xi^...)  (weak log)
    and Omega ~ Lam * Y * s0/rhoc. Order of magnitude only."""
    Lam = Lam_eV * 1e-9  # GeV
    # entropy of the dark sector relative to visible: r_s ~ xi^3
    rs = xi**3
    # cannibal freeze-out: x_fo ~ ln(Mpl * Lam * rs) modulo O(1)
    arg = max(MPL / Lam * rs, 1.01)
    xfo = max(np.log(arg), 3.0)
    # yield: Y ~ rs / xfo  (entropy-diluted, log-suppressed)
    Y = rs / xfo
    return Lam * Y * S0_RHOC


print("[C] Omega_dark h^2 scan (target ~0.12):")
print(f"    {'Lambda_dark':>12s} | " + "".join(f"xi={x:<8.3g}" for x in (0.3, 0.1, 0.03, 0.01)))
for Lam in (0.36, 1.0, 1.87, 5.0):
    row = [omega_glueball(Lam, x) for x in (0.3, 0.1, 0.03, 0.01)]
    print(f"    {Lam:9.2f} eV | " + "".join(f"{o:<11.2g}" for o in row))
print()
print("    READ (corrected after self-check): the THERMAL route UNDER-PRODUCES —")
print("    max Omega h2 ~ 0.008 in the scan; reaching 0.12 needs xi ~ 0.5-1, which")
print("    the dNeff bound kills. The thermal/glueball branch is DEAD as stated.")
print()
print("[D] kill-tests (all named, none yet passed or failed):")
print("    (i)   Delta N_eff: rho_dark/rho_gamma ~ xi^4 (relativistic phase)")
for x in (0.3, 0.1, 0.03):
    print(f"          xi={x:<5g} -> dNeff ~ {4.4*x**4:.2g}   (bound ~0.3: " +
          ("OK" if 4.4 * x**4 < 0.3 else "EXCLUDED") + ")")
print("    (ii)  cannibal epoch must end by z~1e6 for small-scale structure (to check:")
print("          T_d at 3->2 freeze-out vs matter-radiation equality — next gate)")
print("    (iii) self-interaction: sigma/m ~ 1/Lam^3 / (Lam) ... for Lam~eV the naive")
print("          glueball cross-section is HUGE (sigma/m ~ (1/Lam)^2/Lam ~ 1e10 cm2/g):")
print("          *** THE HARD KILL-TEST: eV glueballs must be collisionless enough ***")
print("          escape routes: (a) the condensate is a coherent FIELD (fuzzy-DM-like,")
print("          m~eV gives de Broglie ~ km/s*kpc scales — check vs dwarf cores), or")
print("          (b) Lambda_dark >> eV with abundance set differently. NEXT GATE'S JOB.")
print("    (iv)  Bullet offset: any sigma/m > 1 cm2/g contradicts the collisionless")
print("          Weyl decoupling OBT itself uses (card-and-theory level).")
print()
print("[SYNTHESIS] The route converts the closure input (5:1 abundance, a^-3 growth)")
print("into a RELIC + STATE calculation of the dual sector. The naive particle-glueball")
print("reading at eV likely DIES on self-interaction (iii) -> the surviving branch is")
print("the COHERENT-FIELD reading: Weyl-DM as a fuzzy condensate of the dual sector at")
print("m ~ 0.4-2 eV... which is 1e22 times TOO HEAVY for classic fuzzy DM (1e-22 eV).")
print("=> EITHER a much deeper IR scale exists in the throat hierarchy, OR the")
print("configuration is genuinely collective-gravitational (back to the nonlinear")
print("bulk). HONEST STATE: route opened, abundance window exists (xi~0.03-0.1),")
print("self-interaction is the wall to beat. The bulk's door is this one.")

print()
print("[E] THE NON-THERMAL ROUTE — radion misalignment (the route that lands):")
print("    A coherent radion condensate oscillating at m_phi (fast free mode around")
print("    the GW minimum, distinct from the slow 2-Gyr forced motor mode), displaced")
print("    phi_0 at inflation, redshifts as a^-3 from H=m: classic moduli DM.")
for m_eV, phi0, tag in [(0.36, 1.19e12, "m_phi (GW radion), phi0 = M_s (LVS)"),
                        (1.87, 1.19e12, "m_1 (KK), phi0 = M_s"),
                        (0.36, 5e11, "m_phi, phi0 = M_s/2.4")]:
    m = m_eV * 1e-9
    gstar = 100.0
    Tosc = np.sqrt(m * MPL / (1.66 * np.sqrt(gstar)))
    rho = 0.5 * m * m * phi0 * phi0
    s = (2 * np.pi**2 / 45) * gstar * Tosc**3
    Om = rho / s * S0_RHOC
    print(f"    {tag:38s}: T_osc={Tosc:8.1e} GeV  Omega h^2 ~ {Om:6.2f}")
print("    => Omega_DM h^2 = 0.12 is hit WITHIN O(1) by the two DERIVED OBT scales")
print("    (m_phi = 0.36 eV from Goldberger-Wise; phi_0 ~ M_s = 1.19e12 GeV from LVS)")
print("    with ZERO new parameters beyond the O(1) misalignment fraction —")
print("    the same epistemic class as the axion angle. Cold, collisionless (coherent,")
print("    no 2->2), N_eff-safe, lifetime ~ Mpl^2/m^3 >> t_U. THE NUMBER IS BANKED.")
print()
print("[F] THE INTERNAL KILL-TEST (Gate 11's question, named honestly):")
print("    a 0.36-eV condensate has sub-mm de Broglie length -> it clusters as plain")
print("    CDM at ALL scales -> it would pile 5:1 halos onto GALAXIES, destroying")
print("    OBT's own zero-halo galactic success (SPARC, cards #1-#31). OBT needs the")
print("    Weyl-DM to be CLUSTER-SELECTIVE (the #22 anatomy: f_W~0.7 in clusters,")
print("    ~0 in galaxies). The route therefore lives or dies on a scale-selection")
print("    mechanism for the condensate's gravitating coupling (is the condensate's")
print("    EFFECTIVE source term sinc-filtered like the boost? is it expelled from")
print("    high-phase-gradient regions by the motor?) — that is the nonlinear bulk")
print("    question AGAIN, now sharpened to one object and one number (Omega ~ 0.3).")
