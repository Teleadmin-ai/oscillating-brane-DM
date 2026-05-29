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

## Honest caveat carried forward
Cardoso's amplification is a HIGH-ENERGY (rho>>sigma) effect; OBT's growth-sign
question is LATE-TIME LOW-ENERGY (rho<<sigma), a different regime. Gate 1 validates
the instrument; the OBT sign (Gate 3) requires adapting to the low-energy moving
brane (where, per the closure audit, the sign is a free bulk BC and regularity-
respecting solves tend to ENHANCEMENT).
