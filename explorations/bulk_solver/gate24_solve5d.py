"""GATE 24 — the 5D solve for the cluster Weyl-DM (V9.0, QUARANTINED).
THE last step. Question: does a bulk regularity condition PROMOTE the amplitude
(the factor ~2) from IC to derived, or is it free (closure)?

PASS 1: the static master equation + its two modes, verified.
Static scalar/tensor perturbation of wavenumber k on a brane at z_b in Poincare
AdS5: psi'' = (k^2 - 1/(4 z^2)) psi  (the Gate-9 indicial form, V_eff = -1/(4z^2)
near brane; full AdS5 reduced potential k^2 - 1/(4z^2)).
General solution: psi(z) = sqrt(z) [A I0(k z) + B K0(k z)].
  - K0(kz): DECAYS as z->inf  (regular RS2 mode, normalizable)
  - I0(kz): GROWS as z->inf   (irregular; = the free Weyl charge / dark radiation)
The brane Weyl E_00 is read from Omega_b = z_b^{-3/2} psi(z_b) and its z-slope.
"""
import numpy as np
from scipy.special import i0, i1, k0, k1


def psi(z, k, A, B):
    x = k * z
    return np.sqrt(z) * (A * i0(x) + B * k0(x))


def dpsi(z, k, A, B):
    x = k * z
    rz = np.sqrt(z)
    return (A * i0(x) + B * k0(x)) / (2 * rz) + rz * k * (A * i1(x) - B * k1(x))


# --- VERIFICATION 1: do these satisfy psi'' = (k^2 - 1/(4z^2)) psi ? ---
def numerical_check():
    k = 0.7
    for A, B, tag in [(1.0, 0.0, "I0 mode"), (0.0, 1.0, "K0 mode"), (0.4, 1.6, "mixed")]:
        z = 1.3
        h = 1e-5
        d2 = (psi(z + h, k, A, B) - 2 * psi(z, k, A, B) + psi(z - h, k, A, B)) / h**2
        rhs = (k**2 - 1.0 / (4 * z**2)) * psi(z, k, A, B)
        print(f"  {tag:10s}: psi''={d2:.6f}  (k^2-1/4z^2)psi={rhs:.6f}  ratio={d2/rhs:.6f}")


# --- VERIFICATION 2: asymptotic behaviour z->inf (regular vs irregular) ---
def asymptotics():
    k = 0.7
    print("  z->inf behaviour (regularity):")
    for z in [2, 5, 10, 20]:
        K = psi(z, k, 0, 1)
        I = psi(z, k, 1, 0)
        print(f"    z={z:4d}: K0-mode psi={K:.3e} (decays->regular)  I0-mode psi={I:.3e} (grows->irregular)")


print("PASS 1 — static master equation psi'' = (k^2 - 1/(4z^2)) psi")
print("[V1] solution satisfies the ODE (ratio should be ~1.000):")
numerical_check()
print("[V2] regularity classification:")
asymptotics()
print()
print("  TWO modes confirmed: K0 (regular/normalizable, RS2-allowed) and I0 (irregular,")
print("  = the free Weyl charge). The amplitude question is: which BC fixes the A:B ratio,")
print("  and does the resulting E_00 give a mass-independent factor-2? -> PASS 2,3.")


# ============================ PASS 2 ============================
# Regular RS2 boundary condition (A=0, only the decaying K0 mode) + Israel
# junction (source = cluster mass). Does it give the factor-2, or just the
# tiny Garriga-Tanaka Yukawa correction?
def pass2():
    print("\nPASS 2 — regular RS2 (K0 only) + Israel source:")
    L = 0.2e-6  # m
    Mpc = 3.0857e22  # m
    # RS2 / Garriga-Tanaka: Phi(r) = GM/r [1 + 2 L^2/(3 r^2)] -> f_Weyl_reg = 2L^2/(3r^2)
    print("  Garriga-Tanaka regular Weyl correction f_Weyl = 2 L^2/(3 r^2):")
    for r_kpc in [40, 500, 1500]:
        r = r_kpc * 1e-3 * Mpc
        fW = 2 * L**2 / (3 * r**2)
        print(f"    r={r_kpc:5d} kpc: f_Weyl(regular) = {fW:.2e}")
    # cross-check via the mode solve: the regular-mode E_00 ~ (k L)^2 at k L -> 0
    kL = (1.0 / Mpc) * L  # k ~ 1/Mpc cluster scale
    print(f"  mode-solve cross-check: kL = {kL:.2e} -> regular-mode E_00 ~ (kL)^2 = {kL**2:.2e}")
    print("  VERDICT: the REGULAR RS2 mode gives f_Weyl ~ 1e-58 at cluster radii.")
    print("  -> regularity does NOT give the factor-2. The cluster Weyl-DM is NOT the")
    print("     normalizable bulk response to the baryonic mass. (As expected: RS2")
    print("     reproduces 4D gravity + Planck-suppressed Yukawa.)")


pass2()


# ============================ PASS 3 ============================
# The FREE mode (I0 / Weyl charge / dark radiation): it must carry the factor-2.
# Project it: f_Weyl(k) for self-similar clusters, and test mass-(in)dependence.
def pass3():
    print("\nPASS 3 — the free Weyl mode (I0), its projection and mass-scaling:")
    # free mode psi = A sqrt(z) I0(kz); at brane kz_b<<1 -> I0~1 -> Omega_b = A/z_b
    # CHKS dictionary (static): E_00 ~ k^2 Omega_b / ell  -> rho_Weyl ~ k^2 A/(z_b ell)
    # M_Weyl(<R) ~ rho_Weyl R^3 ; k ~ 1/R ; self-similar clusters: rho_bar~const, R~M^(1/3)
    print("  free-mode projection (kz_b<<1): rho_Weyl ~ A k^2/(z_b ell), k~1/R")
    print("  f_Weyl = M_Weyl/M_bar ~ [A k^2/(z_b ell)] R^3 / (rho_bar R^3) = A k^2/(z_b ell rho_bar)")
    print("  self-similar (rho_bar~const, R~M^1/3): f_Weyl ~ A/R^2 ~ A * M^(-2/3)  [at FIXED A]")
    print()
    # numerical: f_Weyl(M) at fixed A vs A~M^(2/3)
    print(f"  {'M_tot':>8s}{'R~M^1/3':>9s}{'f_Weyl(A fix)':>14s}{'f_Weyl(A~M^2/3)':>16s}")
    for logM in [13.0, 13.5, 14.0, 14.5]:
        M = 10**logM
        R = (M / 1e14) ** (1 / 3.0)  # normalized
        f_Afix = 0.46 * (M / 1e14) ** (-2 / 3.0)  # at fixed A (norm to 0.46 at 1e14)
        f_Ascale = 0.46  # if A ~ M^2/3, the M-dependence cancels -> constant
        print(f"  {logM:8.1f}{R:9.2f}{f_Afix:14.3f}{f_Ascale:16.3f}")
    print()
    print("  OBSERVED (Gate 21-23): f_Weyl ~ 0.45 MASS-INDEPENDENT (flat plateau).")
    print("  -> the free mode at FIXED amplitude gives f_Weyl ~ M^(-2/3) (NOT flat);")
    print("     mass-independence REQUIRES the Weyl charge to scale A ~ M^(2/3).")
    print("  Is A~M^(2/3) derivable? The brane equations + regularity do NOT fix A at all")
    print("  (closure: A is the bulk integration constant). So neither the amplitude (0.46)")
    print("  NOR its mass-scaling (A~M^2/3) is derived on the brane. Only the radial FORM")
    print("  of the mode (the profile shape) is fixed by the master equation.")


# ============================ PASS 4 ============================
def pass4():
    print("\nPASS 4 — confront the 3 target features + verdict:")
    print("  F1 zero Weyl for galaxies: the free mode ~A k^2 -> for galaxies (small wells,")
    print("     low-density, MOND-complete) the required A is ~0 -> consistent IF A is set")
    print("     by the (cluster-selective) closure data; NOT derived, but not violated.")
    print("  F2 turn-on at kT~1.5 keV: a transition in A(system) -> closure/IC, not derived.")
    print("  F3 mass-independent factor-2: requires A~M^(2/3) (IC); only the radial PROFILE")
    print("     (centrally concentrated, the I0-mode shape) is derived -- consistent with the")
    print("     observed inward rise (Gates 17/23).")
    print()
    print("  VERDICT of the 5D solve (the last step):")
    print("  * Regular RS2 mode -> f_Weyl ~ 1e-59 (Yukawa): the baryonic mass does NOT source")
    print("    the cluster dark matter on the brane. (PASS 2)")
    print("  * The cluster Weyl-DM IS the FREE Weyl mode (dark radiation / Weyl charge), whose")
    print("    amplitude A is the bulk integration constant = the CLOSURE/IC datum. (PASS 1,3)")
    print("  * The brane + regularity derive ONLY the radial PROFILE (the mode shape); the")
    print("    AMPLITUDE (factor-2), the MASS-SCALING (A~M^2/3 -> mass-independence), and the")
    print("    TURN-ON are all closure/IC -- NOT promoted to derived. (PASS 3,4)")
    print("  => The regularity condition does NOT promote the amplitude. Closure CONFIRMED")
    print("     from the static-cluster face, consistent with the cosmological Gates 0-9 and")
    print("     the sacred-file framing (geometric DM at the epistemic level of LCDM's Omega_c).")
    print("  The honest end: OBT REINTERPRETS cluster dark matter as the free bulk Weyl mode")
    print("  (geometry, not particles) and DERIVES its profile shape; the AMOUNT is the bulk's")
    print("  own datum. The brane derives the form; the bulk holds the amount. Spirit, then body.")


pass3()
pass4()
