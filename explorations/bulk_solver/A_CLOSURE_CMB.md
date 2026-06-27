# A-phase (V9.0 closure): the CMB-background question for geometric DM

**Status: V9.0 auditor finding, quarantined (NOT V8.2, NOT theory, NOT PDF).**
June 2026. Romain's "attack A", task (1): is the closure wall (b) — the CMB BACKGROUND — fatal, or can a
**halo-free homogeneous a⁻³ sector** exist? Mode: reviewer/auditor, prudence BOTH ways (test, don't glue —
and self-correct when a first pass over-states). Companions: `QUBIT_HOLOGRAPHY_NOTE.md` (the
inflation-entanglement thread), `a_closure_cmb.py` (the z_eq numbers).

## The requirement
The CMB acoustic peaks need a homogeneous **a⁻³** matter component ~5× baryons (Ω_m h²≈0.143) so that
matter-radiation equality z_eq=Ω_m h²/Ω_r h²−1≈3400 puts recombination (z≈1090) in the **matter** era
(constant potentials → the observed peak heights). Whatever plays the DM must (i) be homogeneous + a⁻³ for
z_eq, (ii) cluster on ~100 Mpc at recombination to source the wells, **and** (iii) stay halo-free in
galaxies to preserve OBT's MOND rotation curves. (i)+(iii) is the MOND-CMB tension.

## Three scenarios (`a_closure_cmb.py`)
- **S1 — Weyl as the background DM: FAILS.** The projected Weyl E_μν is **traceless** (Shiromizu-Maeda-
  Sasaki) ⇒ a homogeneous isotropic Weyl has w=1/3 (radiation, a⁻⁴), *not* a⁻³ matter. Matter = baryons
  only ⇒ z_eq≈**535** ⇒ recombination in the **radiation** era ⇒ grossly wrong peaks. The inhomogeneous
  (geometric) Weyl is mean-zero ⇒ 0 contribution to H(z). **So the Weyl cannot be the CMB background DM.**
- **S2 — radion condensate (a⁻³, Gate 10 misalignment, Ω_cond h²≈0.12 at φ₀=M_s): does z_eq, breaks
  galaxies.** With baryons + condensate, Ω_m h²≈0.142 ⇒ z_eq≈**3407** ⇒ recombination in the matter era ✓.
  **But** Gate 11: the 0.36 eV condensate clusters into galaxy halos ⇒ kills the zero-halo MOND success.
  So the wall is **not** "no a⁻³ background" — it is the a⁻³ sector's **galactic clustering** (the tension).
- **S3 — AeST (Skordis-Złošnik 2021, PRL 127, 161302): the resolution exists.** A relativistic-MOND scalar
  whose homogeneous energy density behaves as **dust (a⁻³)** → fits the Planck CMB + matter power spectrum,
  *while* giving MOND (halo-free) in galaxies. Proof by construction that the MOND-CMB tension is
  **surmountable by a single field**.

## Self-correction (prudence both ways)
My first pass tested only S1 ("Weyl-only") and called the CMB an almost-fatal structural wall. That
**over-stated** it. OBT has S2 (a real a⁻³ candidate that pays the z_eq bill), and S3 proves the tension is
surmountable in principle. The honest statement is narrower and sharper: *the Weyl cannot be the background
DM (a⁻⁴); the only open problem is finding a halo-free a⁻³ sector — which is known to be possible (AeST).*

## Verdict
- The CMB is **not** a proven-fatal wall for OBT. What is solid: the **Weyl alone cannot** supply the
  homogeneous a⁻³ background (tracelessness). What is open but **surmountable**: a halo-free a⁻³ sector
  (AeST exists; OBT must realize it).
- **OBT's concrete A target:** realize the AeST mechanism inside the bulk — a **shift-symmetric radion /
  brane-bending mode that is a⁻³ dust cosmologically AND MOND/halo-free galactically.** The massive 0.36 eV
  condensate is *not* it (clusters, Gate 11); the Weyl is *not* it (a⁻⁴). OBT already gets a₀=cH/2π + μ(x)
  from the radion/bulk MOND sector — the question is whether that same sector carries an AeST-class dust mode.
  Mapping unestablished = the V9.0 work.
- **Honest fallback:** if no such mode exists, OBT's position is a **hybrid** (geometric Weyl for
  galaxies/clusters + a homogeneous sector for the CMB) — to be stated openly, at the cost of "DM is purely
  geometric".

## How this relates to the qubit thread
The qubit/inflation-entanglement thread addresses the **perturbation spectrum** (clustering, Gate 7). It is
orthogonal to (and moot until) the **background** question here is settled: there is no point predicting the
δE_μν spectrum from inflation if the homogeneous a⁻³ sector that the CMB needs is not identified. So the
ordering is: **first settle the AeST-mode mapping (this note), then the inflation perturbation chain.**

## Next steps
1. **The AeST mapping (the make-or-break, conceptual→analytic):** does OBT's radion/brane-bending MOND
   sector admit a shift-symmetric a⁻³-dust mode à la Skordis-Złošnik? Compare the OBT bulk action to the
   AeST Lagrangian (the K(Y) MOND function + the dust-producing kinetic term). If yes → OBT inherits AeST's
   CMB fit; if no → hybrid.
2. **Quantitative confirmation (task 2):** an MG-CMB Boltzmann solve (CLASS/CAMB + brane + the a⁻³ sector)
   to turn z_eq into an actual peak prediction — only worthwhile once step 1 picks the sector.
3. The inflation-entanglement perturbation chain — **after** 1.
