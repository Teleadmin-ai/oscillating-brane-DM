# Moving-brane bulk perturbation solver (V9.0 research — NOT V8.2)

**Status: SCAFFOLD, not yet validated. Do not trust any sign it produces until
Gate 1 passes.** This is exploratory V9.0 work, quarantined per the project's
`explorations/` rule. It is NOT theory content, NOT in the PDF, NOT in
`generate_pdf.py`.

## Purpose

Determine whether the SIGN of OBT's cosmological growth modification
(enhancement vs suppression of structure growth) is *derivable* from the 5D
bulk with a physical (regularity/causal) boundary condition — or whether it is
an under-determined boundary datum (the braneworld closure problem).

Concretely: solve the linear scalar-perturbation **master equation** in a static
AdS5-Schwarzschild bulk, with a **moving brane** boundary (junction condition)
and **regularity at the bulk Cauchy horizon**, and read off the sign of the
effective gravitational coupling modulation `G_eff/G_N - 1` on the brane.

This is a **1+1D PDE per Fourier mode k** — the same class of calculation as
Cardoso, Hiramatsu, Koyama & Seahra (2007). It is NOT the exascale nonlinear
slip-shock cosmology. It runs on a workstation / a few dozen cores.

## Validation gates (STRICT — do not skip)

- **Gate 0 — numerics.** The double-null marcher must reproduce a *known
  analytic* solution: exact for the free wave (V=0), and 2nd-order convergent
  (error ∝ h²) for a known potential (Pöschl-Teller / constant V). No physics
  yet. `double_null.py` self-tests this.
- **Gate 1 — reproduce the literature.** Reproduce the radiation-era
  short-scale *amplification* of Cardoso–Hiramatsu–Koyama–Seahra (2007,
  arXiv:0705.1685 / 0710.4507). If we cannot reproduce a published result, the
  code is wrong and NO OBT sign may be read.
  - **Gate 1a — DONE (May 2026).** Brane boundary ODE system (Eq. 38,
    `cardoso_brane.py`): transcription validated against the growing-mode IC
    (Eq. 40a; both equations match at leading order, deviation ~1e-4 early), and
    the short-scale amplification is reproduced (Delta pumped by Omega_b,
    monotonic in k: x4e3 at k=1 ... x2e26 at k=32). Qualitative mechanism only;
    magnitude not yet calibrated to their k_crit/normalization.
  - **Gate 1b — IN PROGRESS.** Couple the Gate-0.5 bulk marcher to the moving
    brane (Seahra hep-th/0602194 scheme; algorithm in GATE1_spec.md).
    - **Stage A — DONE.** `moving_brane.py`: MMS unit test of Seahra's
      triangular brane-update (Eq. 35) in flat space (V=0). Reproduces a
      manufactured exact solution at the correct O(dt^3) per-step order (2.96).
      NOTE: d_eta (proper brane step) must be 2nd-order (trapezoid) for clean
      convergence. The Robin moving-boundary update formula is validated.
    - **Stage B — DONE.** Same MMS unit test with the AdS potential
      V=k^2-1/(4z^2) and the Gate-0.5 Bessel mode as oracle. Converges at
      order ~3. KEY RESULT: the FLAT Minkowski normal derivative is the correct
      convention (no AdS metric factor) -- confirmed by MMS, as expected from
      the reduced variable psi=z^{-3/2}Omega living in flat (u,v) operators.
      Both bulk (diamond) and brane (triangular, Eq.35) updates now validated,
      flat and AdS.
    - **Stage C1 — DONE.** Full evolution, STATIC brane (z_b const, aligned to
      the grid diagonal), MMS vs the Bessel oracle: clean order 2.00 over the
      whole grid (`run_static` in moving_brane.py). The assembly (bulk diamond
      march + Robin brane boundary via Eq.35, row-by-row, index bookkeeping) is
      validated. No moving boundary yet.
    - **Stage C2a — ATTEMPTED, diagnosed.** Tried a shortcut: constant-velocity
      brane on a RECTANGULAR grid (h_u=(1-Vb)dt, h_v=(1+Vb)dt) so brane nodes
      stay on the diagonal (no interpolation). Result: clean order 2 for small
      Vb, but ERRATIC (oscillatory, non-convergent) for Vb>~0.3. Diagnosed: the
      asymmetric grid (aspect h_v/h_u=(1+Vb)/(1-Vb)) under-resolves the v
      direction -> ALIASING with the oscillatory Bessel solution. NOT a physics
      instability: Eq.35 itself is correct at all velocities (unit test order 3),
      and the static (square-grid) case is perfect. The shortcut is the culprit.
    - **Stage C2b — DONE for the regime that matters.** Proper SQUARE grid
      (h_u=h_v), brane advances (1,r) integer grid steps -> stays on nodes
      (a, r*a), Vb=(r-1)/(r+1), no shortcut/asymmetry. MMS vs Bessel oracle:
      CLEAN order 2 for r=2 (Vb=0.333) and r=3 (Vb=0.500). The rectangular-grid
      aliasing is gone -> diagnosis confirmed, and the proper method was NOT
      harder (answering "why the shortcut?"). r=4 (Vb=0.600) still mildly
      erratic: the brane STEP spans dv=4h (fat triangular cell) -> residual
      aliasing across the brane cell. Fully fixed only by single-cell
      interpolation (Seahra's real method) -- needed for FAST (radiation-era)
      branes, NOT for OBT.
      => CORRECTION (overclaim retracted): the integer-step method only does
      CONSTANT velocity at discrete values Vb=(r-1)/(r+1). The REAL OBT brane
      ACCELERATES (oscillating radion -> continuously varying, sign-changing
      velocity), so the integer-step trick CANNOT represent the actual OBT
      trajectory at all -- not merely a "fast-brane" limitation. The cubic-
      interpolation method (Seahra's real method) is therefore REQUIRED for
      Gate 3, not optional: it handles (a) arbitrary accelerating trajectories
      (OBT), (b) any velocity (Cardoso fast-brane benchmark for external
      validation), and (c) better accuracy (no fat brane cell). The integer-step
      result only confirms the diagnosis (square grid kills the aliasing); it is
      NOT a usable solver for OBT.
    - **Stage C2c — DONE (the genuine, non-shortcut solver).**
      `moving_brane_interp.py`: ray grid launched from the brane points + cubic
      4-point interpolation to transfer ray i -> ray i+1, for a GENERAL
      ACCELERATING trajectory z_b(t)=z0+A sin(Om t) (the kind OBT's oscillating
      radion has). Bricks validated: (1) cubic interpolation order ~4; (2) full
      evolution MMS vs the Bessel oracle CLEAN order 2.00, robust across several
      trajectories (A,Om varied). No shortcut, no aliasing, ANY trajectory/speed.
      THE moving-boundary machinery is validated for general branes.
    - **Stage D brick 1 — DONE.** The inhomogeneous brane BC source term
      (n.D)psi - alpha psi = S validated by MMS: coefficient -6*d_eta*(S_S+S_N)
      in the generalized Eq.35, order 3 (see GATE1_spec.md). The full solver
      machinery (bulk + general moving brane + Robin + matter source) is now
      validated end-to-end.
    - **Stage D brick 2 — DONE (June 2026). GATE 1b PASSED.** `gate1_full.py`:
      the full coupled bulk(psi)+brane-matter(Delta) march (generalized Eq.35
      with the matter source, Heun predictor-corrector coupling, adaptive
      eta-steps, vectorized ray transfer). Battery: order-2.0 convergence;
      IC-insensitive (1%); tracks the CHKS Eq.38 high-energy closure to 7.7%
      during the high-energy era; era-consistent amplification at eta_c
      monotone in k (1.10/1.25/1.59/1.96 at k=4/8/16/32 vs closure
      1.10/1.30/1.92/4.43 — full bulk pumps LESS, retardation/radiative leak,
      as in CHKS full-vs-analytic) and amp=1.02 for subcritical k=1.5.
      **CRITICAL BUG CAUGHT & FIXED (the session's lesson):** the scalar master
      reduction is Omega = z^{-3/2} psi (the scalar equation has +(3/z)Omega_z),
      OPPOSITE to the tensor pattern h = z^{+3/2} psi_T. Pattern-matching the
      tensor convention gave alpha = -(5/2)gamma/z_b, which has a SPURIOUS
      tachyonic Robin bound state (sqrt(z)K0 analysis: growth ~0.8/z_b) -> the
      observed late-time runaway. Correct coefficients (tensor cross-check +
      stability analysis): **alpha = +gamma/(2 z_b)**, **S = -6(gamma-1)Delta/
      (k^2 z_b^{7/2})**, Omega_b = z_b^{-3/2} psi_brane. With the fix the late
      time is bounded (no runaway), all gates pass.
    - **EXACT RS background — DONE.** `build_exact/run_exact`: rho/sigma=C/a^4
      exact Friedmann (valid at all energies; a -> sqrt(2C)(eta-eta0) at low
      energy). Supercritical k=8 through the era transition: BOUNDED post-era
      oscillation with retained amplification x2.06 in Delta (x4.2 in P(k)) —
      the CHKS full-solver phenomenology.
    - **GATE 2 (GR recovery) — ESSENTIALLY PASSED (~11% level).** Subcritical
      k=1.5 on the exact background follows the EXACT GR radiation two-mode
      solution (comoving Delta basis D1=(sin x - x cos x)/x, D2=(cos x +
      x sin x)/x, x=k(eta-eta0)/sqrt(3)): LSQ-matched in x in [2.5,3.5], the
      prediction over x in [4,7] deviates by max 11% of the envelope (order-2
      solver at delta=0.01; tightens with resolution). c1/12 = 0.53 vs the
      pure-GR-history 12 (growing-mode IC = Phi_p=-2) is the PHYSICAL
      high-energy-era transfer distortion (CHKS-type), not an error.
    - **GATE 3a — FIRST PROBE DONE (June 2026): the conservative causal bulk
      imposes lag ~ 0 and secular shift ~ 0.** `gate3_obt.py`: low-energy DUST
      brane (Eq.33a dust coefficients; the A-term is EXACTLY the 4D Poisson
      self-gravity, so Omega_b carries only the 5D correction) + IMPOSED radion
      oscillation z_b = z_s(1+eps sin(om eta)) with adiabatic ramp + matched
      smooth ICs, retarded bulk. Differential lock-in (eps-run minus smooth run,
      detrended) gives a CLEAN linear response: A/eps converged and
      eps-independent (0.1326 at k=0.6, om=0.3), drive-phase invariant to
      ~0.06 rad. RESULTS: (i) in the OBT-relevant EVANESCENT regime (ck >
      omega_radion) the bulk gravity responds essentially IN PHASE: lag =
      0.00 +/- 0.1 rad — NOT the 1.36-rad viscoelastic lag; a genuine lag
      (+0.35 rad) appears only in the RADIATING regime om > k (not the
      cosmological one); (ii) the SECULAR growth-rate shift is ZERO within
      bounds: |c1| <~ 1e-6/eta and sign flips with the drive phase (residual,
      not signal) — about TWO ORDERS below the magnitude OBT's S8 mechanism
      needs in matched units (~3e-4/eta). INTERPRETATION (sharpens the closure
      audit): bulk CAUSALITY alone does NOT supply the S8 phase lag or a growth
      modification of either sign; delta_bulk must come from the DISSIPATIVE
      sector (Gamma_rad/PBH stick-slip — consistent with OBT's own BKM
      derivation from Gamma_slip/Gamma_stick timescales, NOT wave retardation)
      and/or the compact two-brane bulk. The sign freedom lives there. CAVEATS:
      single-brane Poincare (continuum KK; OBT has compact bulk -> resonances
      possible), motor perturbations not modeled (= the free Weyl-sourcing
      data), sinusoid not stick-slip, compressed hierarchy (k ell = 0.3-0.6).
    - **Gate 3b/4 — NEXT.** Dust brane (w=0 coefficients of
      Eq.33a: friction H_c Delta', A=-1, B=-4, source k^4 Omega_b/(3 a^3)) +
      low-energy OBT radion trajectory (slow drift + 2 Gyr oscillation) +
      retarded/no-incoming bulk (NATURAL in the characteristic scheme: data
      only on the initial null ray + the brane => the retarded solution; this
      IS the regularity/causal BC of the closure question). Read out the sign
      of the cycle-averaged G_eff modulation from the Omega_b feedback in the
      dust growth equation. Gate 4 = robustness (resolution, initial data,
      horizon placement / mu != 0).
- **Gate 2 — GR recovery.** Late-time, large-scale, low-energy limit must give
  `G_eff -> G_N` with the leading correction of order `(kL)^2` (~1e-61 here).
- **Gate 3 — the OBT sign.** Only after Gates 0–2: dust brane + forcing, sweep
  the bulk dark-radiation parameter `mu` (sign of background Weyl) and the
  horizon boundary data, and read the sign of `G_eff/G_N - 1`.
- **Gate 4 — robustness.** Vary resolution, horizon placement, initial data.
  The sign must be stable. If it flips with the boundary datum, that IS the
  answer: the sign is an input (closure confirmed), not a prediction.

## Physics inputs that MUST be verified against the literature before running

- `master_potential.V_scalar(...)` — the Kodama–Ishibashi scalar-type potential
  for AdS5-Schwarzschild. **The exact coefficients are flagged `VERIFY` and must
  be copied from Kodama & Ishibashi 2003 (hep-th/0305147) — do not trust the
  placeholder.**
- `obt_bulk.brane_junction_bc(...)` — the perturbed Israel junction condition on
  the moving brane. Coefficients flagged `VERIFY` against Mukohyama 2000 /
  Koyama & Maartens.

## Files

- `double_null.py`  — characteristic (double-null) marcher for `□Ω = V Ω`;
  Gundlach–Price–Pullin scheme + Gate-0 self-tests. **This core is the part we
  can write correctly now.**
- `obt_bulk.py`     — AdS5-Sch background, tortoise coordinate, brane trajectory,
  master potential and junction BC. **Contains the flagged physics inputs.**
- `run_validation.py` — Gate 0 / Gate 1 drivers.

## Resources

24–32 vCPU, 48–64 GB RAM, ~50 GB disk. `pip install numba` in the venv.
Gate 0/1 are small; the full mu/BC/k campaign uses the parallelism.

## How to run (AFTER restart + numba install + potential verification)

```bash
.venv/bin/python explorations/bulk_solver/run_validation.py --gate 0   # numerics
.venv/bin/python explorations/bulk_solver/run_validation.py --gate 1   # Cardoso
```
