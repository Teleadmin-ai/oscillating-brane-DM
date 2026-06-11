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
    - **GATE 3b — DONE (June 2026): dissipation does NOT rescue the BKM lag.**
      Absorptive PBH-impedance boundary term added to the perturbed junction,
      (n.D)psi = alpha psi + S + b*d_eta psi (integrates EXACTLY in Eq.35:
      denominator 12(1+b), psi_S coefficient 12(1-b); energy flux -b(psi_t)^2
      < 0 confirms b>0 absorbs; GR recovery unaffected, scheme stable+converged).
      Sweep b in [0.02, 2] — the physically-mapped stick->slip bracket
      (Gamma_eff/om ~ b/(om z_b): b_stick~0.02, b_slip~2): measured lag goes
      -0.04 -> +0.16 rad, i.e. |lag| <= 0.16 EVERYWHERE, an order of magnitude
      below delta_bulk = 1.36, and the TREND (lag increasing with absorption,
      elastic-dominated A/eps ~ 0.13 throughout) is OPPOSITE to the relaxational
      BKM ansatz arctan(om/Gamma) (which predicts 1.48 at stick -> 0.10 at
      slip). Secular growth rate stays at the phase-flipping ~6e-7 floor.
      SHARPENED CONCLUSION (Gates 3a+3b together): the 5D bulk-wave sector —
      conservative OR boundary-dissipative — supplies NEITHER the S8 phase lag
      NOR a growth sign of either sign. Both must come from the PBH-sector
      INTERNAL relaxational dynamics (the first-order-relaxation ansatz for
      G_eff with rates Gamma_stick/Gamma_slip), which is now the single
      load-bearing unproven step of the S8 mechanism. Self-consistency note:
      OBT's own kinematic blockade implies the compact bulk at om*ell ~ 1e-26
      is gapped/stiffer still -> even smaller bulk lag; the single-brane
      gapless continuum tested here was the MOST favorable case for a bulk lag.
    - **GATE 4 — DONE (June 2026): the program's final answer.** `gate4_pbh.py`
      models the PBH-sector internal variable explicitly: dX/dt = Gamma(t)
      (W_drive - X) with OBT's stick/slip switching (Gamma_stick=0.243,
      Gamma_slip=20.7, om=pi, slip 10%), warm-started to its limit cycle,
      amplitude-normalized, exact zero-mean (BBN rule); growth = EdS matter era
      to 13.8 Gyr with G_eff = 1 + f_osc X(t), f_osc = 0.10.
      **4a (BKM check):** the TRUE switched-system lag is 1.477 rad for a
      sinusoidal drive (stick-dominated; const-Gamma arctan limits 1.485/0.151
      reproduced exactly) and 1.047 rad for the stick-slip sawtooth, vs BKM's
      1.359: BKM is a fair estimate but the lag is WAVEFORM-DEPENDENT (1.0-1.5
      rad), not a universal constant.
      **4b (the sign):** exact decomposition in the coupling sign f -> -f
      (scaling checks: EVEN ratio 4.00 = f^2, ODD ratio 2.00 = f):
        * ODD part (first order): +/- 5-10% = exactly the S8-claimed magnitude,
          but its SIGN is set by [coupling-sign bit (+/-f)] x [anchoring phase]
          x [waveform] — the closure INPUTS. Sin and sawtooth both flip with
          the anchor; the warm start removed an earlier spurious anchor-
          robustness (cold-transient artifact, caught).
        * EVEN part (second order): NEGATIVE in ALL configurations tested
          (waveforms x filters x anchors x t_i) = a genuinely DERIVED,
          coupling-sign-proof UNIVERSAL SUPPRESSION (growth response is concave
          in G), but only -0.01%..-0.2% at f=0.1 (grows ~logarithmically as the
          motor starts earlier; adiabatic-window Jensen effect).
      **VERDICT (Gates 0-4 complete):** the 5D bulk-wave sector supplies
      neither phase nor sign (3a/3b); the PBH relaxational sector supplies a
      real but waveform-dependent lag (1.0-1.5 rad) and an S8-scale growth
      effect whose SIGN is one INPUT BIT short of a prediction (coupling sign;
      plus anchoring phase and waveform shape), exactly as the closure audit
      held — now proven quantitatively; the only universally DERIVED sign is a
      second-order suppression ~30-100x smaller than the S8 claim. OBT's
      -4..-10% magnitude IS reproducible with its anchored inputs (the odd part
      reaches it), so V8.2's published epistemic framing ("consistency with the
      tension, not a precision prediction"; "sign is an input at the level of
      LambdaCDM's Omega_c") is VINDICATED ab initio. Optional cross-check left: two-brane compact bulk.
    - **GATE 4c — DONE (June 2026): the incoming-Weyl input channel,
      demonstrated constructively in the full PDE.** The closure problem's free
      bulk datum = the initial-null-ray data (left-movers swept by the brane).
      Injecting a constant-Omega wave-train (k=0.15 < om_v: propagating;
      sin^2-ramped): (i) the induced dG modulation is PERFECTLY linear
      (rms/Ain = 5.833 at both test amplitudes; Omega-amplitude ~0.017 already
      gives dG ~ f_osc = 0.1 — the channel is efficient); (ii) in interference
      with the radion, the growth shift carries a FIRST-order component exactly
      antisymmetric in the datum's sign (0.5 ln D(+A)/D(-A) = -2.39e-5 at
      A=0.002; +2.39e-5 at -A; linearity ratio 2.00) and dependent on the
      datum's phase (pi/2 doubles it); the pure-injection part is 2nd order
      (-3e-10, negligible). CONSTRUCTIVE PROOF of the second input channel:
      the free incoming-bulk datum sets the sign and size of the growth effect,
      linearly. Together with 4b (coupling-sign/anchoring/waveform inputs), the
      closure freedom is now exhibited explicitly in BOTH channels.
      **THE GATE PROGRAM (0 -> 4c) IS COMPLETE.**
    - **GATE 5 — the compact two-boundary bulk: THE BIT DERIVED, AND ITS
      CHANNEL COSMOLOGICALLY DEAD (June 2026).** `gate5_compact.py`: rays end
      at a static second boundary z2 (mirrored Eq.35 far update + non-uniform
      cubic transfers, MMS-validated to order 2-3 with a MOVING brane). The
      compact bulk has NO incoming-Weyl freedom (4c's channel closes); the
      steady response to the radion is unique. Findings, in order:
      (1) the solver DETECTS the positive-tension far-brane tachyon
      (alpha2=-5/2z2: surface mode sigma~0.8/z2 = the observed blowup) — the
      RS slab's negative-tension requirement found dynamically;
      (2) the UNSTABILIZED scalar cavity is tachyonic at low k and
      resonance-structured in (z2, k) — the classic RS1 radion-modulus
      instability, detected ab initio (sign flips/blowups in the first sweeps
      were THIS, not numerics: damping-robust, convergence-clean);
      (3) with the Goldberger-Wise gap (m2 in the bulk potential; OBT has
      m_phi = 0.36 eV) the cavity is stable at all k and the in-phase response
      sign becomes UNIFORMLY POSITIVE across far-BCs, depths (incl. the
      ex-anomalous z2off=2.0), GW stiffness, dissipation: inphase
      +0.087..+0.107, phi ~ +0.03 — **sign(dG_bulk/d z_b) = + is DERIVED** in
      the stabilized compact model;
      (4) BUT the fixed-ratio scaling (om = k/2; the S8 scales sit at
      ck >> om_radion — om = ck only at the 613 Mpc cymatic crossover) kills
      the channel as ~k^3..k^4 (0.1018 -> 0.0024 over k 0.6 -> 0.2): at
      cosmological k*ell ~ 1e-30 the derived channel is dead beyond any
      relevance (stronger than the audit's (kL)^2 estimate).
      **FINAL SYNTHESIS OF THE WHOLE PROGRAM:** every bulk configuration
      tested — retarded, dissipative, compact, compact-stabilized — yields the
      same answer: the bulk's derivable response is positive, elastic,
      lag-free, and cosmologically negligible; the S8-scale modulation and its
      sign are irreducibly properties of the brane-local PBH/motor sector
      (coupling-sign bit + anchoring + waveform, Gate 4b). The closure freedom
      is not a bulk mystery: it is the PBH microphysics' one unfixed sign.
      Caveats: crude constant-mass GW model, imposed trajectory, unperturbed
      motor, compressed hierarchy (trend-based extrapolation over k 0.6->0.2).
    - **GATE 6 — the PBH-network microphysics (June 2026): the motor's
      mechanical layer DERIVED; every computed brane-local G-channel closed;
      the bit's final address = bulk dark-radiation initial conditions.**
      `gate6_pbh_micro.py`: [A] THE PEG THEOREM — a brane perforated by a 5D
      Tangherlini horizon has E(d) = -sigma(4pi/3)(r_h^2-d^2)^{3/2}: stable
      symmetric anchoring with k_peg = 4 pi sigma r_h (numeric = analytic to
      7 digits) and a DERIVED detachment threshold d_crit = r_h; with the EMF
      reaching M_crit (r_h = L), the network's effective threshold is O(0.1 L):
      OBT's phi_crit ~ 0.1 L derived in order of magnitude from its own mass
      function. [B] THE SAWTOOTH EMERGES: an overdamped brane + 4000
      EMF-distributed pegs (detach at r_h, re-pin after a scrambling delay)
      self-organizes into relaxation oscillations with SLIP DUTY = 0.13 (OBT
      posits ~0.10 — not tuned) and velocity contrast ~4e7. [C] MAGNITUDE
      AUDIT of all brane-local G-coupling channels (OBT numbers; inter-peg
      distance ~0.14 pc): peg strain ~1e-69, inter-peg bowing ~1e-47,
      compact-bulk Weyl ~1e-90 (Gate 5) — all dead; warp-position ~1e-1 is the
      right size but LLR-forbidden (the audit's channel 1); and the
      Z2-symmetric peg sector has NO linear G(d) coupling by parity (its
      2-omega modulation has derived positive sign but dead magnitude).
      **FINAL ADDRESS OF THE BIT: no computed channel carries f_osc = 0.1;
      the surviving carrier is the bulk dark-radiation (mu) sector's
      COSMOLOGICAL INITIAL perturbations — genuine initial-condition data, at
      the epistemic level of LambdaCDM's primordial spectrum. The program has
      walked the S8 freedom from "somewhere in the bulk BCs" down to "the
      primordial perturbation spectrum of the bulk's dark-radiation content" —
      while DERIVING, on the way, the motor's springs, threshold, and
      waveform.**
    - **GATE 7 — the mu-sector (June 2026): the program's last word.**
      `gate7_mu.py`: [A] the BBN-max dark-radiation background (rho_E/rho_m =
      1.5e-5/a) leaves the Gates 0-6 background machinery unchanged (corrections
      ~1e-2 only at a <= 1e-3). [B] BRACKET THEOREM: for the radion-DRIVEN
      response, mu only sets the far boundary's nature, which strictly
      interpolates between the two measured extremes — mu=0 compact = perfect
      reflector (Gate 5: +0.087..+0.107, dies ~k^3-4) and open Poincare =
      perfect absorber (Gate 3a: +0.13, same death) — both giving the SAME sign
      and the same cosmological k-death: the driven channel's verdict is
      mu-INDEPENDENT. (The verbatim Kodama-Ishibashi scalar potential remains
      the VERIFY item for a full mu!=0 PDE; the bracket substitutes for the
      sign question.) [C] THE ROOM: integrating the growth equation with a
      radion-locked Weyl-radiation drive against the BBN-max background, the
      S8-scale carriage requires delta_E/<E> ~ 5e2 (early-era carriage,
      r_E ~ 1e-2 at a ~ 1e-3) up to ~1e4 (late carriage) — the Weyl
      'perturbation' must exceed its own homogeneous mean by 2.7-4 orders,
      radion-phase-locked universe-wide: a deeply NONLINEAR mean-zero
      configuration, which is the SAME object as OBT's geometric dark matter.
      [D] FINAL SYNTHESIS OF GATES 0-7: every LINEAR channel is now either
      DERIVED (driven response: sign +, elastic, lag-free, cosmologically dead
      by k^3-4) or CLOSED (peg-elastic 1e-69/1e-47, warp LLR-forbidden, Z2
      parity) or QUANTIFIED as initial-condition data (the nonlinear Weyl-DM
      configuration's 10% radion-locked response = f_osc AND the bit, one
      object, one level below the geometric-DM conjecture). The V9.0 frontier
      is the NONLINEAR bulk solve of the Weyl-DM configuration under the
      radion. THE GATE PROGRAM (0 -> 7) IS CLOSED.
    - **GATE 8 — the Weyl-DM radion coupling: THE BIT CLOSED, THE S8 NUMBER
      DERIVED (June 2026).** `gate8_weyl_dm.py`. Scope resolution: the
      "nonlinear" Weyl-DM configuration is nonlinear only in the
      FRW-perturbation sense; at halo densities the BULK treatment of a lump
      is exactly linear -> the bit lives in the lump's STATIC bulk response,
      solvable EXACTLY: psi = sqrt(z)[A I0(kappa z) + B K0(kappa z)] with the
      validated junction + stable far BC (2x2 closed form; validation hook
      reproduces the dynamic runs' mean dG in sign/order, drift-consistent).
      PARITY RESOLUTION: a comoving lump has even E(dz) — but the AdS WARP
      breaks the parity: the coupling c = dln(dG)/dln(z_b) is warp-derived.
      RESULTS: c = +1.27..+1.59 UNIFORMLY (far-BCs, comoving/fixed z2, GW
      stiffness, open/compact) and STABLE AS k -> 0 (this channel does NOT die
      at large scales: halo-internal readout, unlike the cosmological drive);
      LLR-SAFE (it modulates the DM sector's gravitating mass, not laboratory
      G). Predicted f_osc = c x (radion 10%, itself Gate-6-derived) x (DM
      share 5/6) = 0.106..0.133 — OBT's posited 0.10 RECOVERED from geometry.
      FINAL INTEGRATION (every parameter derived or OBT-chronology-fixed:
      sawtooth waveform [Gate 6], coupling sign + [warp], f_eff [Gate 8],
      anchor 0 [13.8/2.0 = 6.9 cycles = phase 0.9 today], 4a filter):
      **DlnD = -7.2%..-9.0% (headline -7.7%) = SUPPRESSION, inside OBT's
      claimed -4..-10% S8 window; the wrong sign would give +7.5% enhancement
      and is EXCLUDED by the warp.** Cross-checks: no-filter -11.9%, sinusoid
      -3.4% (the audit's waveform factor ~2 persists as modeling residual —
      but the waveform itself is now derived). ASSUMPTIONS (each named):
      linear-bulk static lump + gate-standard junction/readout; LLR-safety and
      halo-readout arguments (stated, not full calcs); EdS growth; W_saw
      idealization; F_web direction = toward the bulk (+z, per the theory's
      own wording); relaxational filter ansatz; compressed-hierarchy statics.
      STATUS: V9.0 model-chain result, NOT promoted into V8.2 (that requires
      Romain's call + an independent cross-AI audit pass, per tradition).
      Falsification handle: observations settling on S8 ENHANCEMENT would
      refute the chain.
    - **GATE 8 AUDIT (June 2026, self-audit, adversarial) — TWO FINDINGS;
      THE -7.7% CLAIM IS DOWNGRADED TO CONDITIONAL.**
      **[F1 — observable-identification fragility of the sign.]** The coupling
      decomposes as c(dG) = c(R) + 2.5: the RAW bulk response slope is
      NEGATIVE (c(R) = -1.14 at k=0.6, -1.00 at k=0.3); the positive sign of c
      comes entirely from the z_b^{5/2} Poisson-unit conversion exponents.
      The sign therefore depends on which z_b-powers belong to the physical
      G-modulation vs background bookkeeping — defensible as defined (the
      bulk-to-matter gravity ratio) but NOT uniquely forced; a clean
      derivation needs the actual geodesic force from the full perturbed
      metric. The 'uniform derived +' is downgraded to 'derived within one
      defensible observable identification'.
      **[F2 — the critical gap: linear dressing vs the nonlinear Weyl-DM.]**
      The Gate-8 dG is the LINEAR bulk dressing of a matter lump = exactly the
      closure audit's channel 2 — and my own k-scan shows dG ~ k^2 (exponents
      1.70/1.88/1.97), i.e. dG ~ 5e-53 at physical halo scales: the dressing
      is DEAD, as channel 2 always was. The claimed f_osc = c x 0.1 conflated
      the modulation OF THE DRESSING FRACTION with a modulation of total halo
      gravity. For a DM-dominated halo the gravitating mass is the NONLINEAR
      IC-assembled Weyl configuration, whose radion coupling depends on its
      bulk z-PROFILE — which the linear lump calculation does not determine.
      A quick probe: if the configuration is the quasi-zero-mode (Omega ~ 1/z),
      the projected-amplitude slope is ~ -1 — OPPOSITE sign. The coupling is
      PROFILE-DEPENDENT.
      **POST-AUDIT VERDICT: the bit RE-OPENS, now residing in the nonlinear
      Weyl-DM configuration's bulk z-profile. The -7.2..-9.0% suppression
      stands only as a CONDITIONAL: IF the configuration's coupling is
      c ~ +1.4 (warp-asymmetric, dressing-like profile), THEN the S8 chain
      closes at -7.7%; the quasi-zero-mode profile would flip it. The genuine
      next derivation (the recovery path): identify the Weyl-DM with the
      LONGEST-LIVED quasi-bound mode of the bulk wave operator (anything else
      decays — a selection principle, not an IC), compute ITS profile slope at
      the brane -> the coupling becomes derivable with no IC freedom. The
      Gates 0-7 conclusions are UNAFFECTED (they were structural/negative
      results); Gate 6's positives stand with stated softness (phi_crit as a
      bracket; sawtooth duty parameter-soft, emergence robust). The sacred
      files and the site were never touched by the Gate-8 claim (quarantine
      held).**
    - **GATE 8 RECOVERY PROBE + AUDIT FINAL STATE (June 2026): the doubt
      CONCENTRATES into one calculable question.** (1) F2 largely CLOSES: the
      raw profile slopes of all natural Weyl-DM candidate configurations agree
      to 0.14 — dressing −1.137, exact zero-mode (psi = sqrt z, Omega = 1/z)
      −1.000, GW gap-edge mode −1.000 — so under any CONSISTENT observable
      convention the profile-dependence is mild; the configuration's shape is
      NOT the blocker. (2) F1 DEEPENS: the conversion-exponent question also
      touches the DYNAMIC gates' readout — the a^3 factor in dG contributes
      ~0.21*eps of bookkeeping wiggle vs the ~0.13*eps measured in-phase
      signal, so the measured '+' in Gates 3a/5 is convention-mixed at O(1)
      too (the PDE solutions and all structural results stand; only the
      G_eff-readout DEFINITION is at stake). AUDIT FINAL STATE: the S8 sign
      hangs on exactly ONE well-defined derivation — express the brane growth
      equation entirely in physical variables (CHKS formalism, verbatim) and
      identify unambiguously which z_b-dependences constitute G_eff vs
      background bookkeeping. Until then: raw-slope convention -> c ~ -1
      (G_DM weaker toward the IR -> enhancement +6.6% via the 4b table);
      gate-standard convention -> c ~ +1.4 (suppression -7.7%). ONE sharp
      question, two branches, both numbers ready — the next session's first
      target. The audit did its job: it tried to kill, drew blood twice,
      closed one wound itself, and left the chain with a single named
      load-bearing question instead of diffuse confidence. Dust brane (w=0 coefficients of
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
