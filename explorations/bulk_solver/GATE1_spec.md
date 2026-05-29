# Gate 1 specification — verbatim equations from Cardoso-Hiramatsu-Koyama-Seahra (arXiv:0705.1685)

Extracted May 2026 for the moving-brane reproduction. AdS5 Poincaré, radiation era.
Units below: ell = AdS radius, sigma = brane tension, a0, k constants.

## Bulk master equation (Eq. 18) — VALIDATED (Gate 0.5)
    -Omega_tt + Omega_zz + (3/z) Omega_z + (1/z^2 - k^2) Omega = 0
Reduced (Omega = z^{-3/2} psi):  4 psi_uv + [k^2 - 1/(4z^2)] psi = 0   (z=(v-u)/2).
Coefficient of Omega/z^2 confirmed = +1.

## Background / brane trajectory
- Metric: ds^2 = (ell/z)^2 (-dtau^2 + dx^2 + dz^2). Brane at z=z_b(tau), a = ell/z_b.
- Conformal-time relation:  d(eta)^2 = d(tau_b)^2 - d(z_b)^2   (eta = brane conformal time).
- Friedmann (Eq. 10):  H^2 = (1/ell^2)(rho/sigma)(2 + rho/sigma).
  High-energy (rho>>sigma):  H^2 ~ (rho/(sigma ell))^2 ;  rho ~ sigma H ell.
- Radiation era (Eq. 37):  a ~ a0 (k eta)^{1/3}  ->  z_b ∝ eta^{-1/3}.
- KEY high-energy simplification: the brane becomes nearly NULL, so the normal
  derivative  ∂_n ≈ -∂_u = -∂_t  at the brane. (This is what makes the moving
  timelike boundary tractable in the high-energy limit.)

## Brane boundary / junction condition (Eq. 28)
    [ ∂_n Omega + (1/ell)(1 + rho/sigma) Omega + (6 rho a^3 /(sigma k^2)) Delta ]_brane = 0

## Brane matter density-contrast evolution (Eq. 33a, full)
    Delta'' + (1 + 3 c_s^2 - 6 w) H a Delta'
      + [ c_s^2 k^2 + (3 rho a^2/(sigma ell^2)) A + (3 rho^2 a^2/(sigma^2 ell^2)) B ] Delta
      = -k^2 Gamma/rho + k^4 (1+w) Omega_b /(3 ell a^3)
  with  A = 6 c_s^2 - 1 - 8 w + 3 w^2 ,  B = 3 c_s^2 - 9 w - 4 .  (' = d/d eta)

## High-energy coupled ODE system (Eq. 38) — the amplification mechanism
    Delta'' + [ k^2/3 - 4 a0 k^{1/3}/(3 ell eta^{2/3}) - 2/eta^2 ] Delta
        = (4 k^3)/(9 ell a0^3 eta) Omega_b
    Omega_b' = (1/(3 eta)) [ 1 + 3 a0 k^{1/3} eta^{4/3}/ell ] Omega_b + 2 ell a0^3 Delta / k

## Initial data
- PS (constant-tau):  Delta(0) = N a_i^6 ,  d_eta Delta(0) = 6 N H_i a_i^7  (growing mode).
- CI (characteristic): Omega-hat only on the initial null hypersurface.
- Growing-mode (Eq. 40a):  Delta^(1) ~ (4/3)(k eta)^2 ,  Omega_b^(1) ~ a0^3 k^{-2} ell (k eta)^3.
- "late-time dynamics insensitive to the choice if placed early enough."

## Result to reproduce
Matter power spectrum amplified ">= 1 order of magnitude vs GR" on SMALL scales,
for k > k_crit (mode entering horizon at H~1/ell). k_crit physical scale ~ 10 AU
for ell=0.1mm — cosmologically tiny. Supercritical modes amplified.

## Implementation stages (each validated before the next)
- 1a (tractable now): integrate the Eq.38 coupled ODE pair (scipy), show Delta
  amplification for k>k_crit vs the bulk-decoupled (Omega_b=0) baseline. Validates
  transcription + the amplification mechanism. Does NOT validate the bulk PDE.
- 1b: full bulk double-null evolution of Omega (Gate-0.5 marcher) + the moving
  brane boundary (Eq.28) using ∂_n≈-∂_u, coupled to the Delta ODE. Reproduce the
  amplification from the FULL solver -> validates the instrument.
- Only then: Gate 2 (GR recovery, late-time low-energy) -> Gate 3 (OBT sign).

## Gate 1b moving-boundary ALGORITHM (Seahra hep-th/0602194) — verbatim

Grid: null coords u=t-z, v=t+z. Rows bounded by const-u; the brane intersects the
future boundary of row i at t_i = t_0 + i*Delta. Brane nodes are ALIGNED with the
grid by construction (no ghost points). Cubic 4-point interpolation only fills
non-aligned nodes between rows (error O(Delta^4)). Within a triangular cell the
brane arc is replaced by a straight line (error O(Delta^3); valid if Delta << r_c,
the brane radius of curvature).

DIAMOND cell update (bulk; = our validated GPP, V at south node):
    psi_n = -psi_s + (psi_w + psi_e)(1 - delta^2 V_s/8) + O(Delta^4)

TRIANGULAR (brane) cell update, Robin condition  (n.D)psi - alpha psi = 0  applied
via trapezoid over the brane segment (Eq. 35, verbatim, TENSOR/no-source case):
    psi_n ~ -[12 + 6 alpha_s d_eta + d_u d_v V_s] / [12 + 6 alpha_n d_eta + d_u d_v V_n] * psi_s
            + [24 - d_u d_v V_e] / [12 + 6 alpha_n d_eta + d_u d_v V_n] * psi_e + O(Delta^3)
  d_eta = proper distance along brane between south & north brane nodes;
  alpha(eta) = -(3/2) sqrt(1+H^2 ell^2)/z_b   (RS tensor modes).

OUR SCALAR generalization: the Robin condition is INHOMOGENEOUS,
    (n.D)Omega + (1/ell)(1+rho/sigma) Omega + (6 rho a^3/(sigma k^2)) Delta = 0   (Cardoso Eq.28)
  => alpha = -(1/ell)(1+rho/sigma), plus a SOURCE S = -(6 rho a^3/(sigma k^2)) Delta.
  The trapezoid integral gains (d_eta/2)(S_n + S_s); add this to the Eq.35 numerator.
  Potential is the SCALAR one (Gate-0.5 validated): V_psi = k^2 - 1/(4 z^2) for psi
  (= z^{-3/2} Omega), OR work directly in Omega with V_Omega = k^2 - 1/z^2 and the
  (3/z) d_z term — but psi-form reuses the validated marcher, preferred.

Convergence: 2nd order (psi_Delta - psi_exact = Delta^2 * eps). Bulk/AdS-infinity:
finite domain, future null boundary beyond which evolution is not needed (causal
domain of dependence handles it; place initial null surface deep in the past).

## Gate 1b build/validation stages (each validated before next)
- 1b-i  DE SITTER ORACLE: inertial (de Sitter) brane has the EXACT solution
        psi_exact = (z_*/z)^{3/2} Re{ [k eta - i] e^{-i k eta} }  (Seahra Eq. 44).
        Implement the moving-brane scheme (Eq.35, no matter source, alpha as above)
        and reproduce this to 2nd order. Validates the moving-boundary machinery.
- 1b-ii MATTER COUPLING: add the scalar Delta source + evolve Delta (Eq. 33a/38)
        coupled to Omega_b. 
- 1b-iii RADIATION-ERA BENCHMARK: reproduce the ~x10 short-scale amplification,
        Fig. 10 of 0705.1685 (super-horizon -> GR; k>k_crit -> amplified).

## Tooling notes (DeepSearch audit May 2026)
- NO public moving-brane solver exists (Seahra/Koyama/Cardoso codes unreleased).
  BRANECODE (gr-qc/0410001) exists but is ADM/BSSN nonlinear, misaligned.
  CLASS/CAMB/hi_class use PPF, skip the 5D bulk. => build from these equations.
- Possible accelerator: Black Hole Perturbation Toolkit (bhptoolkit.org) +
  O'Toole-Ottewill-Wardell (2010.15818) characteristic RW/Zerilli integrators
  (moving worldline boundary ~ moving brane). We instead extend our own
  Gate-0.5-validated marcher (we control + validated it).

## Stage D source term (MMS-validated, May 2026)
Inhomogeneous brane BC: (n.D)psi - alpha psi = S, with S = matter source
(for OBT/Cardoso Eq.28, S proportional to the brane density contrast Delta:
S = -(6 rho a^3/(sigma k^2)) Delta in Omega-variables). The generalized Eq.35
gains the source term on the RHS:
    [12 + 6 a_N d_eta + du dv V_N] psi_N
       = -[12 + 6 a_S d_eta + du dv V_S] psi_S + [24 - du dv V_E] psi_E
         - 6 d_eta (S_S + S_N)
The coefficient -6*d_eta was confirmed by MMS (alpha=0, S=(n.D)psi_exact):
order 3 convergence; +6 and -3 fail. Consistent with the homogeneous 6*alpha*d_eta.

## Honest caveat carried forward
Cardoso's amplification is a HIGH-ENERGY (rho>>sigma) effect; OBT's growth-sign
question is LATE-TIME LOW-ENERGY (rho<<sigma), a different regime. Gate 1 validates
the instrument; the OBT sign (Gate 3) requires adapting to the low-energy moving
brane (where, per the closure audit, the sign is a free bulk BC and regularity-
respecting solves tend to ENHANCEMENT).
