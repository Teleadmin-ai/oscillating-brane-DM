# CLAUDE.md - Project Information for AI Assistants

## 🛑 RULE ZERO — DISCUSS BEFORE ACTING 🛑
**When the user asks a question ("comment on fait ça ?", "à ton avis ?"), ANSWER the question and STOP.**
- Do NOT start reading files, writing code, or making changes after answering a question
- WAIT for explicit approval ("vas-y", "fais-le", "ok") before any action
- The user thinks out loud and discusses before deciding — respect that process
- EXCEPTION: if the user gives a direct instruction (not a question), execute it immediately
- Breaking this rule wastes work and causes destructive changes

## ⛔ SACRED RULE — READ THIS FIRST ⛔
The following .md files compose the PDF and are the SOLE source of truth for the theory:
1. `discoveries.md` — 30 phenomena addressed (4 Tier 1 exact + 13 Tier 2 analytical + 13 Tier 3 exploratory) + 10 collateral theoretical discoveries
2. `theory.md` — core theoretical framework (motor, ODE, BBN, QCD, stability, PBH, bulk)
3. `chronology.md` — cosmic chronology, tension calibration, MOND
4. `predictions.md` — observational predictions, tests, Bayesian evidence
5. `docs/theoretical_foundations.md` — pedagogical EFT foundations (linearized toy model; full V8.2 non-smooth dynamics are in theory.md)
6. `laboratory.md` — laboratory proofs (qBOUNCE, 5D Geometric Bypass)
7. `tools.md` — computational tools

**ALL theoretical content MUST be written in these files and ONLY these files.**
**The PDF MUST contain ALL of these files and ONLY these files (+ index.md as intro).**
**It is STRICTLY FORBIDDEN to:**
- Add theoretical content in a file that is not in this list
- Remove any of these files from the PDF pipeline
- Create new .md files for theory content (the 7 files above cover ALL topics — enrich them, do NOT create new ones)
- Move content between these files without verifying NOTHING is lost

**New .md files may ONLY be created for non-theory site pages (e.g., about, research, refutation) that are NOT in the PDF.**

**After ANY modification to these 7 files, you MUST regenerate and push the PDF:**
```bash
python3 scripts/generate_pdf.py
git add oscillating_brane_theory_latest.pdf oscillating_brane_theory_latest.md.txt output/oscillating_brane_theory_latest.pdf output/oscillating_brane_theory_latest.combined.md
git commit -m "Regenerate PDF + markdown" && git push
```
**If you forget, the PDF on the site will be stale and inconsistent with the site pages.**

**After ANY theoretical addition or modification, you MUST also update CLAUDE.md** (REQUIRED concepts, BANNED concepts, Key Parameters, Computational Validations, Key References) to reflect the new content BEFORE committing. CLAUDE.md is the authoritative reference for all future conversations.

**When reading theory files, ALWAYS read them COMPLETELY — never use grep/sed/chunks as a substitute for full reading.** The complete theory is ~140k tokens (16% of context budget). With 1M context, there is NO reason to economize. Partial reads cause missed errors and inconsistencies. For theory.md (~2300 lines), use 2 Read calls if needed — but read ALL of it. Science demands completeness, not shortcuts.

**Breaking these rules causes data loss and inconsistency between the site and the PDF.**

## Project Overview
**Oscillating Brane Cosmology V8.2 (Hybrid Topology Edition)** - The universe is a vibrating 4D membrane in 5D AdS space, driven by a hybrid stick-slip motor: macroscopic Cosmic Web forcing via Israel junction conditions (the muscle) + microscopic thermodynamically mandated PBH network for local energy dissipation (the metronome). ℓ=0 coherence from inflation; ER=EPR as optional topological UV-completion. Gregory-Laflamme instability provides an ab initio derivation of the PBH mass window.

**Author**: Romain Provencal (provencal.romain@teleadmin.net) - Independent conceptual researcher
**AI Collaborators**: Claude (Anthropic) & Gemini DeepThink (Google) as theoretical co-processors

## Repository
- **GitHub**: https://github.com/Teleadmin-ai/oscillating-brane-DM
- **Website**: https://higgs-cosmology.com/
- **Owner**: Teleadmin-ai (NOT "Teleadmin")
- **Version**: V8.2 Hybrid Topology Edition (March 2026)

## CRITICAL: Theory V8.2 Paradigm

### Core Physics — The Hybrid Motor:
- **Bulk**: Non-local topological state, spacetime is emergent (Van Raamsdonk 2010)
- **Connectivity**: PBH network (thermodynamically mandatory via DOS theorem); ER=EPR (Maldacena & Susskind 2013) as optional topological interpretation
- **Oscillation ODE** (hybrid stick-slip, NOT harmonic):
  `φ̈ + (3H + Γ_rad)φ̇ + ξRφ + ∂V_GW/∂φ = F_web[E_μν]·(1-3w) - R_PBH(φ,φ̇)Θ(|φ|-φ_crit)`
  - **F_web[E_μν] (the Muscle)**: Macroscopic forcing from the Cosmic Web. Superclusters, filaments, and voids create inhomogeneous stress S_μν on the brane. Via Israel junction conditions ΔK_μν = -κ₅²(S_μν - ⅓S h_μν), this generates the projected Weyl tensor E_μν — a continuous 5D tidal force pressing the brane toward the bulk
  - **R_PBH·Θ (the Metronome)**: Microscopic release via the thermodynamically mandated network of asteroid-mass PBHs (exponential DOS theorem). When φ reaches φ_crit, the PBH network absorbs kinetic energy locally (MSS scrambling). ℓ=0 coherence is an inflationary causal fossil (like CMB isotropy)
  - **(3H + Γ_rad)φ̇**: Hubble friction + radiative damping via bulk graviton emission (KK modes) during slip phase
  - **ξRφ**: Non-minimal coupling → dynamical PLL attractor locking T = 2.000 Gyr (chronodynamic eigenvalue, N=6 mode)
  - **(1-3w)**: Trace coupling. = 0 for radiation (conformal symmetry, BBN safe), = 1 after QCD (trace anomaly, motor ON)
- **BBN protection**: Via **conformal symmetry** (T^μ_μ = 0 for radiation w=1/3). QCD chiral symmetry breaking ignites motor at Λ_QCD = 257 MeV
- **5D stability**: **Radiative damping** via bulk graviton emission during slip phase caps amplitude
- **Period stability (anti-chirp)**: ξRφ non-minimal coupling acts as **geometric Phase-Locked Loop**. Three competing decays (Hubble friction ↓, Cosmic Web forcing ↓, curvature feedback ↓) cancel on attractor manifold. |dT/T| < 10⁻³ per Hubble time. Van der Pol oscillator analogy.
- **PBH wave-optics immunity**: For M ~ 10⁻¹² M☉, r_s ≈ 3 nm ≪ λ_opt ≈ 600 nm. Fresnel parameter w_F = 2πr_s/λ ≈ 0.03 ≪ 1. Subaru-HSC is physically blind (deep wave-optics regime). Micro-PBH capillaries rehabilitated
- **Dark energy**: w(z) = -1 + Σ A_n sin(2πn t_lb/T + φ_n) — exact Fourier decomposition of stick-slip sawtooth (not just fundamental). A₂/A₁=47.6%, A₃/A₁=29.3%. DESI's "phantom crossing" is aliasing of geometric shock at z≈0.93 (phase 82.8%, just before QCD cliff). ΔBIC ≈ -6.4 vs CPL (DR2, Strong — k=1 vs k=2, Occam rewards OBT), forecast -22 (Year 5, Decisive).
- **S₈ suppression**: ODE integration with BKM-derived phase δ_bulk=1.36 rad → growth suppression of **order 4–10%** (S₈ ≈ 0.79), consistent with the S₈ tension. **NOT a ±0.002 precision figure** (audit May 2026): the value depends at the factor-~2 level on the non-derivable slip-waveform shape (exponential ansatz ~4.5%, triangular ~10% at the SAME derived phase, sinusoid even sign-flips). The ±0.002 (k_slip∈[3,5]) is only the WITHIN-ansatz variation, not cross-family. δ_bulk IS genuinely derived (arctan viscoelastic, z_eff-robust via saturation) — that part is solid; the S₈ precision is not. Exact zero-mean centering MANDATORY (DC bias violates BBN). f_osc/D/T anchored to DESI w(z) — itself small (A_w=0.003) → say "consistency" not "rigidity". S₈ aligns with the cosmic-shear-low side of the BIFURCATED tension; the eROSITA cluster-high side is in tension with OBT (eROSITA γ DEMOTED to T3, audit May 2026).
- **ISW modulation** (NOT a 6σ resonance): CMB ℓ=10-20. The Δχ²=32.9/6σ was a covariance-omission artifact (Sachs-Wolfe cosmic variance omitted) — DECISIVELY DISPROVEN (DeepSearch audit May 2026): late-ISW is sub-dominant (~10-20% of low-ℓ power), cosmic-variance ceiling Δχ²_max~11.5 over ℓ=10-20 makes a 32.9 improvement mathematically impossible; Planck low-ℓ shows NO excess (deficit); A_ISW=0.96±0.30 from cross-corr. Realistic significance ~1σ. T2, CLASS/CAMB pending. NOT a falsifiable pillar
- **Anchors**: Micro-PBHs with **extended log-normal mass function** (10⁻¹⁴ to 10⁻¹⁰ M☉). Dual role: topological capillaries AND local heat sinks (exponential DOS, MSS scrambling). ER=EPR provides optional geometric interpretation of their entanglement
- **Laboratory tests**: qBOUNCE (ultra-cold quantum neutrons, ILL) + levitated nanoscale optomechanics. Bypass Casimir at sub-micron scale

### Epistemological Framework:
- **30 phenomena addressed** (tiered: 4 Tier 1 exact resolutions + 13 Tier 2 analytical frameworks + 13 Tier 3 exploratory perspectives):
  - Core T1 (after audits): emergent MOND geometric derivation — μ(x)=x/√(1+x²) from the Gauss-Codazzi quadrature (VERIFIED May 2026: g_5D=√(g²+a₀²)+projection → exact RAR, both limits) for SPARC galaxy rotation curves (RMS 29.3 km/s; a₀=cH₀/2π is prior art Milgrom/Verlinde, the μ(x) FORM is the derived novelty). DEMOTED from the old "4 core T1": DESI w(z) (×700 too small), S₈ (waveform-dependent + growth sign a free bulk BC), wide binary γ_g (Chae 2025) — wide binaries now T2: the anomaly is OBSERVATIONALLY CONTESTED (Chae/Hernandez see MOND boost; Pittordis-Sutherland/Banik find Newtonian fits better — unresolved, hidden triples), AND γ_g(u) is MOND's boost (OBT inherits, NOT OBT-distinctive). ISW also T2 (~1σ). So the robust T1 core is essentially the MOND μ(x) derivation (galactic kinematics)
  - 8 established: neutrino masses, DM invisibility (LZ), emergent MOND (ab initio: a₀=cH₀/2π from Gibbons-Hawking thermodynamics, μ(x)=x/√(1+x²) from 5D geometric tilt, cluster failure via 2 Gyr resonance; SPARC 135 galaxies: RMS 29.3 km/s, 0 free params vs NFW 35.0 km/s, 270 params), JWST early galaxies, early SMBHs, cosmological constant, cosmic dipole, Hubble tension
  - 4 validated connections: Lithium-7 (BBN conformal tolerance), baryon asymmetry (spontaneous QCD baryogenesis, c_QCD=O(1)), Big Ring/Giant Arc (Chladni resonance), CMB birefringence (5D geometric Chern-Simons, c_top=75)
  - 3 astrophysical signatures: Hubble's 43 anomalous objects (ER=EPR topological scarring), dark flow unification (v_bulk=300 km/s), Chladni mega-structures
  - 4 multi-messenger astrophysical: NANOGrav GWB overtones, eROSITA γ=1.19 illusion, DF2/DF4 cymatic nodes, Amaterasu trans-GZK (5D KK leakage)
  - 9 extended phenomenology (March 2026): KBC Void (cymatic λ=c×T=613 Mpc), quasar polarization alignment (Weyl shear), Dark Flow (brane drift inertia), Space Roar/ARCADE 2 (cumulative slip synchrotron), ORCs (PBH topological shock), Methuselah star (G_eff aging ×1.105), White Dwarf Q-Branch (thermo-gravitational pumping), Planet 9 illusion (MOND EFE), Flyby anomaly (brane drift vortex)
- **10 collateral theoretical discoveries** (autonomous theorems transcending cosmology): KdF 4-branch tensor (pure math), AdS₅ viscoelastic retardation (dynamical systems), percolation immunity (quantum info), kinematic blockade (GR/QFT), sinc averaging (galactic dynamics), γ(M) spectrum (large-scale structure), spectral flattening (GW astronomy), rigid template ΔBIC (Bayesian stats), multi-throat selection (string pheno), trans-scalar QCD 0.11σ (fundamental physics)
- **Ab initio derivations**: c_top=75 (Chern number, not 10⁴⁰), c_QCD=O(1) (not ε_CP=10⁻⁶), v_bulk=300 km/s (single parameter → dark flow + birefringence)
- **Definitive future test**: SKA 21cm reionization modulation (2027+)
- **Complementary tests**: Vera Rubin/LSST, qBOUNCE/optomechanics, Euclid
- **Theory is purely tensorial and geometric** — no dependence on astrophysical controversies
- **Cross-AI audit status (March 2026)**: Math validated 100% by Gemini DeepThink. Phase 1: independent recalculation (τ₀→257 MeV, a₀=cH₀/2π, Fresnel w_F=0.031, Δβ=0.25°, Schwinger 10⁻³¹). Phase 2 (Series 1): 9 DeepThink prompts (Fourier spectrum, exact S₈ ODE, MOND ab initio, Seeley-DeWitt numerics, Dirichlet anomaly, 3D Floquet, LVS+multi-throat, dynamical Schwinger, finite-N corrections). Phase 3 (Series 2): 9 DeepThink prompts (Kinematic Blockade, NANOGrav spectral flattening, AdS₅ viscoelastic retardation, Press-Schechter γ(M), MOND sinc theorem, ΔBIC forecast, Fisher analytical 3×3, KdF 4-branch tensor, Kesten-McKay percolation immunity). Phase 4 (Series 3): 9 DeepThink prompts (exact a₅ Seeley-DeWitt, exact spectral zeta, continuous γ(M) exclusion theorem, 3-component Bullet Cluster, ab initio SPARC, multi-harmonic sinc, non-perturbative steepest descent, graph Laplacian determinant, exact RT finite-N). All peer-review attack vectors addressed. 60 derivations total.
- **Audit-driven corrections (March 2026)**: S₈ spatial→temporal (then ab initio 4.50% via BKM theorem), neutron lifetime removed, MOND formula derived ab initio (cH₀/2π from Gibbons-Hawking), 6 Unicode-in-math formulas fixed, τ₀ posterior 19.51→19.85. **Late March 2026 epistemological hardening**: m₁ 19.2→3.78 eV (ℏc conversion), t_evap 10⁴⁷→10³⁷ yr (M³ scaling), QCD "Proof"→"Phenomenological Coincidence" (Ansatz status), φ_eff "exact invariant"→AdS₅ viscoelastic retardation δ_bulk=1.36 rad (BKM theorem, zero additional free params), T 2.0±0.3→2.000±0.003 (observationally anchored eigenvalue), model → 4 continuous EFT params + 1 integer (transparent parametric matrix), tier system (T1/T2/T3) for anomaly classification, Bayesian [2.8,4.13]→5.8 (Decisive, prior-independent), MOND scope note (Milgrom priority), Schwinger 10¹²→10⁹ (m₁ cascade), superlatifs moderated, 39th decimal→10⁻³⁰ sanctuary (QFT restraint)

### BANNED Concepts (NEVER use):
- "Point Unique" 0D, Ringermacher, GW doublet/NANOGrav, Bulk-Infinity
- "Block Universe", "tiny hammers"/"momentum hit"/"dark matter impacts"
- "Simple harmonic oscillator"/"SHO" as the dynamics
- JWST LRDs as anchors
- τ₀ = 2.2 × 10⁻⁵ GeV³ (wrong), contact@higgs-cosmology.com (nonexistent)
- w(z) without phase φ₀, Version 4/5/6/7.x references
- **"holographic thermodynamics"** / **"entropic force"**
- **"Complexity=Volume" as the motor** (ok as historical motivation only)
- **EDGES/CatWISE as confirmations**
- **Single PBH mass 10⁻¹² M☉** (must use extended mass function)
- **"global S₈ suppression of 5.2%" / "S₈=0.797±0.002 precision" / "cross-observational rigidity"** (must be time-dependent; honest value is growth suppression of order 4–10%, S₈≈0.79, waveform-shape dependent at factor-~2 — NOT ±0.002. δ_bulk derived but the S₈ value is consistency-with-tension, not a precision prediction; audit May 2026)
- **"Scale-Dependent Yukawa Screening" for S₈** (k/k_L ~ 10⁻²⁹ at cosmological scales → no spatial dependence)
- **Neutron Lifetime Anomaly / Bottle vs Beam** (double counting error + T^μ_μ=0 for EM fields → removed)
- **"temperature-dependent brane tension" / "τ(T)"** (replaced by conformal symmetry)
- **"MORRIS" experiment** (operates at 1 mm, blinded by Casimir)
- **qBOUNCE "observed anomaly" / "λ=2.73 forced by the experiment" / "55× amplification with resolution" / qBOUNCE as a falsifiable smoking gun** (DeepSearch + internal audit, May 2026: (1) qBOUNCE has NEVER reported an anomaly — all results consistent with standard QM, used to set BSM limits (Jenke 2014, Cronenberg 2018). The "λ=2.73" is a 2025 THEORY toy-fit (Sung/Koch/Jenke/Abele/Bondar arXiv:2510.15341) to a known ~3.9σ instrumental SYSTEMATIC in g, NOT a physical discovery. (2) "55× amplification with resolution" is a category error — the neutron wavefunction scale (~10μm) is fixed regardless of detector resolution; overlap with the 0.2μm Yukawa is fixed at 2(L/z₀)³~8×10⁻⁵. (3) The level shift is δE/E~2×10⁻⁸ at nominal α=−0.005, ~10⁻⁶ even at natural radion coupling α~O(1) — both ≪10⁻⁴ GRS precision. Observability needs α~25 (~75× above natural) = fine-tuning, refused. (4) Casimir does NOT forbid large α at 0.2μm — α_max~10¹² (Decca 2005, sub-μm gravity weakly constrained) — but OBT predicts small α regardless. The 3.1% n-splitting is real in SHAPE but unobservable in amplitude. qBOUNCE = consistency check, NOT a falsifiable test. α=−0.005 is an unmotivated input, not derived (theory.md asserts it; foundations doc gives a conflicting α<10⁻⁵))
- **"ISW resonance Δχ²=32.9 (6σ)" / "smoking gun" / "ISW proves the oscillating brane" / ISW as a falsifiable pillar** (DeepSearch + internal audit, May 2026: the 32.9 is a covariance-omission artifact — OBT-vs-ΛCDM ISW spectra compared while omitting the dominant Sachs-Wolfe cosmic variance (~16-25× larger). Three independent disproofs: (1) cosmic-variance ceiling — ΛCDM already fits ℓ=10-20 with χ²≈11.5, so a 32.9 IMPROVEMENT is mathematically impossible (max possible ~11.5); (2) Planck low-ℓ shows NO excess at ℓ=10-20, rather a deficit (low quadrupole, ℓ≈20-30 dip); (3) A_ISW=0.96±0.30 from CMB-LSS cross-correlation, consistent with ΛCDM, no 6σ anywhere (Granett supervoid is ~3-4σ, local, real-space, NOT a global harmonic resonance). Corrected realistic significance ~1σ. ISW is a sub-dominant (~10-20% of low-ℓ power), cosmic-variance-limited weak consistency check, T2, CLASS/CAMB pending — NOT a smoking gun)
- **"eROSITA γ=1.19 confirms OBT" / "γ(M) ascending uniquely distinguishes OBT from f(R)" / eROSITA as a falsifiable OBT pillar** (DeepSearch + audit May 2026: γ=1.19±0.21 is REAL — Artis et al. 2024/2025, eRASS1, ~3σ above GR's 0.55 — but MISAPPROPRIATED. (1) It is driven by HIGH σ8 at intermediate z (excess EARLY growth); and the SAME survey's primary cosmology (Ghirardini et al. 2024) gives S8=0.86±0.01, σ8=0.88 — ABOVE Planck, cluster-ABUNDANT, the OPPOSITE of the cluster DEFICIT (S8≈0.79) OBT's suppression mechanism requires. (2) The "constant-G pipeline reads a 55% deficit and inflates γ" narrative is wrong: Artis fit γ as a free parameter directly. (3) "f(R) predicts universal γ" is FALSE — f(R) is scale-dependent via the scalaron Compton wavelength → mass-dependent γ; and an apparent γ(M) is degenerate with mundane systematics (AGN feedback, miscentering, non-Gaussian MOR scatter). (4) The S8 tension is BIFURCATED (cosmic-shear-low ~0.77 vs cluster-high ~0.86); a single-sign temporal G_eff fits one side but WORSENS the other → OBT aligns with shear, is in TENSION with eROSITA clusters. eROSITA is NOT a confirmation; it is a tension. **THEORY-FILE REFRAME DONE (May 2026)**: theory.md (audit caveat block at start of eROSITA section + f(R)/strict-falsifiable/tier fixes), discoveries.md §6.2 (T2→T3 + audit) + §9.6 + table, predictions.md table + shield synthesis reframed. The REQUIRED "eROSITA falsifiable prediction" / "eROSITA non-linear" entries below are SUPERSEDED — kept only as historical record of the mechanism, demoted to T3 exploratory)
- **"Warped Shielding" as mere geometric filter** (replaced by radiative damping)
- **Farrah et al. (2023)** / **BH cosmological coupling** / **k = 3.11** (refuted by JWST at 11σ, incompatible with virialized systems)
- **"Little Red Dots"** as relevant to anchor mechanism
- **f_PBH = 10% / f_PBH = 0.10** (must be 1% / 0.01 everywhere — "tent pegs" metaphor)
- **"loss of mass" for GL-unstable PBHs** (must say "loss of local 4D gravitational singularity")
- **M_crit formula involving τ₀** (M_crit = Lc²/(2G), purely geometric, τ₀ is NOT in this formula)
- **"GL softening suppresses Bondi-Hoyle accretion" / "softened potential → no accretion disk" for sub-M_crit PBHs** (accretion-darkness audit + DeepSearch, May 2026: WRONG ON SCALE. The sub-micron softening (r≲L=0.2μm) cannot gate accretion — Bondi-Hoyle is set at the accretion radius r_acc=2GM/(v²+c_s²)~0.3–100 m, i.e. 10⁶–10⁹ × L, where the potential is fully 4D. DeepSearch confirmed: the exact 5D Tangherlini potential goes as −1/r² (STEEPER near horizon, not softer), and the brane-projected tidal-charge term q/r² is ~10⁻⁷ of Newtonian at r_acc (q~r_s²~10⁻¹⁴ m²). The X-ray darkness is MUNDANE: asteroid-mass Bondi luminosity L_acc~10⁻²⁸ L☉ (Ṁ∝M², ~3×10⁻¹⁷ kg/s, L~0.3 W), flow collisionless (Knudsen≫1). Say "X-ray dark by standard low-Bondi accretion at asteroid mass", NOT "5D geometric softening suppresses accretion". Perforation hierarchy still governs the MICROLENSING transition (Pillar B), NOT accretion. The "loss of local 4D gravitational singularity" wording is OK as micro-geometry, but must NOT be causally linked to accretion darkness)
- **"heavy seeds 10³–10⁵ M☉ from PBH accretion above M_crit" / "heavy PBH seed tail"** (audit May 2026: mathematically impossible. Bondi growth of a sub-10 M☉ object over a Hubble time is bounded to ~1.4× (growth integral M(t)=M_i/(1−M_i∫K dt), fractional growth ∝ M_i); and 10³–10⁵ M☉ is 13–18 orders above the stated EMF ceiling (10⁻¹⁰ M☉) → no such tail exists. Early-SMBH explanation must rest on capillary GAS-CHANNELING (~10²⁰ kg anchors seed baryon agglomeration around topological nodes), NOT PBH grown to SMBH mass by accretion)
- **"instantaneous synchronization"** (must say "non-local quantum phase coherence" — no superluminal signaling)
- **"τ₀ cools/relaxes from 10⁵⁰"** (τ₀ is geometrically FIXED by KS flux integers, what relaxes is oscillation AMPLITUDE)
- **MLE = -0.016 as transverse contraction** (this captures the longitudinal exponent; true transverse κ = e^{-4.74} from Liouville-Filippov)
- **Scalar Ψ₄ in 5D** (must use CMPP 3×3 STF matrix Ψ_ij^(5) — SO(3) little group has 5 polarizations)
- **Global constant κ_Z4** in AMR (must be AMR-level-indexed scalar field κ_Z4^(ℓ) = 1.4/Δt_ℓ)
- **Explicit Berger-Oliger for 10³² ratio** (CFL wall: 28 million billion years per step on Frontier → must use IMEX)
- **Single-throat KKLT uplift** (QCD throat is 45 orders too weak for global LVS uplift → must use multi-throat architecture)
- **"Classical graviton Bremsstrahlung" for Γ_rad** (continuous 5D GR gives Γ_rad ≡ 0 due to kinematic blockade m₁T_slip ~ 3.6×10³¹; Γ_rad is quantum informational viscosity, NOT radiation)
- **m₁ = 19.2 eV** (wrong — missing ℏc conversion; correct: m₁ = j_{1,1}ℏc/L ≈ 3.78 eV flat-space, 1.87 eV warped)
- **"φ_eff = exact topological invariant"** or **"geometric dephasing 1.35π"** (replaced by AdS₅ viscoelastic retardation δ_bulk = 1.36 rad, derived ab initio from BKM Averaging Theorem)
- **"Proof" for QCD connection** (τ₀^{1/3}≈Λ_QCD is a phenomenological Ansatz, not a proof — KS convergence is 0.11σ motivation, not demonstration)
- **t_evap ~ 10⁴⁷ years** (wrong M³ scaling; correct: ~10³⁷ years at M_crit)
- **"Israel minus sign" for S₈ suppression** (diagnostic table proved: G_eff=G_N(1-f_osc×W) gives +12.1% ENHANCEMENT, not suppression. The physics is a continuous phase DELAY δ_bulk=1.36 rad, not a sign flip. Use G_eff=G_N[1+f_osc×W(t/T+δ_bulk/(2π))] with PLUS sign)
- **"2 free parameters" or "3 free parameters"** (model has 4 continuous EFT parameters: τ₀, L fundamental + D, f_osc effective macroscopic + topological integer N=6. Derived: T=2.000 Gyr, δ_bulk=1.36 rad. Always use the honest parametric matrix)
- **T = 2.0 ± 0.3 Gyr** (stale — T is now a derived chronodynamic eigenvalue: T=13.80/6.9=2.000±0.003 Gyr)
- **"ER=EPR is necessary for Γ_rad"** (false dichotomy — Γ_rad derives from local PBH thermodynamics: exponential DOS theorem + MSS scrambling. Zero wormholes needed)
- **"ER=EPR synchronizes ℓ=0"** (ℓ=0 coherence is an inflationary causal fossil, like CMB isotropy. ER=EPR is optional topological UV-completion)
- **"Kinematic Blockade therefore ER=EPR"** (argument by elimination / false dichotomy. Correct chain: Kinematic Blockade → exponential DOS needed → only BH have it → PBHs thermodynamically mandatory)
- **Claiming a₀=cH₀/2π as "novel OBT discovery"** (prior art: Milgrom 1983, Verlinde 2016, Pazy 2013, McCulloch 2007. OBT novelty is μ(x) from Gauss-Codazzi + sinc extinction, NOT a₀ itself)
- **"Pillar H" / KK Bremsstrahlung for ASASSN-14ko or partial TDE orbital decay** (DeepThink #1 audit, May 2026: Kinematic Blockade is absolute — Schwinger exponent exp(-10²⁹) for direct emission, exp(-10¹⁴) for SMBH-Hawking-KK channel, exp(-10¹⁹) for virtual KK exchange, Floquet forbidden by 22-order frequency gap. ω_orb~10⁻²² eV vs m₁=1.87 eV. dot{P}_OBT ≤ exp(-10¹⁴)×dot{P}_GW ≡ 0. ASASSN-14ko's dot{P}~10⁻³ MUST be attributed to 4D astrophysics — Roche overflow, non-conservative mass transfer, or disk drag. OBT V8.2 mathematically forbids itself from explaining this anomaly)
- **WQFT/Calabi-Yau "Analytical Bypass" for Γ_rad** (DeepThink #2 audit, May 2026: Hodge diamond mismatch is categorical — KS physical CY3 P⁴[18]_{1,1,1,6,9} has h^{1,1}=2, h^{2,1}=272, χ=-540. Driesse et al. 2024 5PM virtual CY3 has h^{1,1}=1, h^{2,1}=1, χ=0. DISTINCT FAMILIES, no Picard-Fuchs isomorphism, no motivic correspondence. The 5PM CY3 is dimensional regularization geometry of 4D Feynman parametric space — purely a mathematical tool, NOT a physical compactification shadow. Same CY3 appears in QED self-energy and fishnet integrals. Conflating mathematical regularization with physical compactification is an ontological category error. Γ_rad extraction remains via PBH thermodynamics + exponential DOS theorem; no analytical bypass exists)
- **"Horizon Informational Viscosity" Pathway for SMBH-mediated bulk emission** (Pathway 3 of cross-AI critique, May 2026: SMBH T_H~10⁻¹⁴ eV thermal suppression exp(-m₁/T_H)=exp(-10¹⁴) freezes Hawking-KK channel. SMBH 4D-anchoring (M>>M_crit) does NOT bypass kinematic frequency mismatch. Even with S_BH~10⁹¹ exponential DOS, sub-threshold orbital perturbation cannot pump real KK quanta of mass m₁=1.87 eV. Pathway 3 dies on the same Kinematic Blockade as Pillar H direct emission)
- **Classical bulk channels (Weyl drag, radion zero-mode, membrane paradigm) for partial TDE orbital decay** (DeepThink #3 audit, May 2026: triple suppression closes the classical loophole left open after DeepThink #1. (a) Chandrasekhar dynamical friction in Weyl fluid: ρ_Weyl~10⁻¹⁶ kg/m³ × M_*=1 M☉ → dot{P}_Weyl/P~10⁻²⁶, suppressed by extreme mass ratio. (b) Membrane paradigm tidal heating: scales as (M_*/M_SMBH)²~10⁻¹⁵, suppressed by ASASSN-14ko mass hierarchy. (c) Radion scalar dipole: even bypassing Cassini ω_BD>40000 bound (best ~10⁻⁹), Goldberger-Wise gives m_φ≈0.36 eV → ω_orb~10⁻²² eV << m_φ → radion is ALSO Kinematically Blockaded → strict zero. Total: dot{P}_OBT_classical << 10⁻⁶ << dot{P}_GW. ASASSN-14ko's dot{P}~10⁻³ is definitively 4D astrophysical (Roche lobe overflow, tidally inflated stellar envelope, non-conservative mass transfer per Linial-Sari, Yao+, Bandopadhyay+). Holistic intuition that "bulk is involved" is qualitatively right (Weyl fluid IS bulk projection) but quantitatively negligible for orbital observables)
- **Claiming the radion is "effectively massless" or "zero-mode" for local processes** (DeepThink #3 audit, May 2026: Goldberger-Wise stabilization gives m_φ≈0.36 eV, a warped IR scale analogous to m₁ KK gap. Cosmological 2 Gyr period is FORCED anharmonic stick-slip via F_web Israel macro-forcing, NOT free radion oscillation at natural mass frequency. Local radion response to sub-eV sources is Yukawa-suppressed with range ℏc/m_φ~0.5 μm. The Generalized Kinematic Blockade applies to ALL massive bulk modes: KK gravitons (m₁=1.87 eV) AND radion (m_φ=0.36 eV). Only the 4D zero-mode tensor graviton and the continuous Weyl fluid sector remain kinematically open — both already accounted in dot{P}_GW~10⁻⁶ baseline)
- **"OBT derives the dark matter abundance" / "the 5:1 DM:baryon ratio is predicted" / "the Weyl-fluid a⁻³ clustering is derived"** (geometric-DM closure-problem audit, May 2026: the projected Weyl tensor E_μν is a FREE bulk field, Bianchi-constrained (∇^μ E_μν = κ₅⁴ ∇^μ π_μν) but NOT sourced by the ~1% PBH rest mass — so there is NO factor-~500 amplitude contradiction (the worry that 1% mass → only 1% effect is misplaced: the amplitude is a bulk integration constant, not the PBH mass). BUT equally the 5:1 DM:baryon amplitude AND the CDM-like a⁻³ clustering are bulk BOUNDARY CONDITIONS, under-determined by the braneworld closure problem (Koyama; Maartens 2004 — brane perturbation eqs don't close without the full 5D bulk solution). Quantitative nails: (a) the quadratic π_μν term is ~10⁻⁴⁰–10⁻⁴⁶ (theory.md) → DM is entirely E_μν, not the high-energy correction; (b) the HOMOGENEOUS Weyl is "dark radiation" diluting as a⁻⁴, BBN-limited (ΔN_eff) to ≲10⁻⁵ of ρ_DM → the gravitating DM must reside ENTIRELY in the inhomogeneous component (cosmic mean ≈0, locally ~5× baryons, with compensating repulsive E_00 in voids since E^μ_μ=0) — a strong specific configuration that linear perturbation theory cannot produce, a conjecture pending a dynamical bulk solution. Epistemic status: geometric DM is a CONSISTENT REINTERPRETATION of the NATURE of dark matter (geometric, not particulate), at the SAME level as ΛCDM's fitted Ω_c — NOT a derivation of abundance or clustering. The kinematic results (MOND μ(x), sinc filter, Bullet 150 kpc offset GIVEN a dominant collisionless component) are robust; the AMOUNT and GROWTH of that component are inputs. Use "reinterprets/accommodates", NOT "derives", for the DM amplitude)

### REQUIRED Concepts (V8.2):
- **Geometric DM = reinterpretation, not derivation (closure problem)**: OBT reinterprets the NATURE of dark matter (E_μν geometric projection, not WIMPs) but does NOT derive its abundance. The 5:1 amplitude + a⁻³ clustering are bulk boundary conditions, under-determined by the Koyama-Maartens braneworld closure problem. No factor-500 contradiction (E_μν is a free bulk field, not pegged to the 1% PBH mass). Homogeneous Weyl = dark radiation (a⁻⁴, BBN ≲10⁻⁵ of DM) → DM is the inhomogeneous part (mean≈0, locally ~5× baryons). Same epistemic level as ΛCDM's Ω_c. Note added to theory.md (after SMS Poisson eq) + discoveries.md §3.4. Kinematic results (MOND, sinc, Bullet offset given dominant collisionless component) robust; amplitude+growth are inputs
- **Growth-sector SIGN is a free bulk boundary condition (closure), NOT a prediction — Ġ/G is the trap** (bulk-sign audit May 2026; web-researched Koyama astro-ph/0701015, Maartens, Cardoso-Hiramatsu-Koyama-Seahra 0705.1685, phantom-brane 1603.01277 + computed): the SIGN of OBT's S8/growth modulation (enhancement vs suppression) is under-determined. Established braneworld result: the Weyl anisotropic-stress evolution is ABSENT from the brane equations → BC-dependent ("perturbations grow moderately or rapidly depending on the BC", Koyama). Three sectors checked: (1) geometric G_N from brane-in-warp — sign computable from the warp BUT a ~10% G_N oscillation over 2 Gyr gives Ġ/G~3×10⁻¹⁰/yr, ~3000× over the Lunar-Laser-Ranging bound 10⁻¹³/yr → RULED OUT locally (the 1−3w trick gates WHEN the motor runs, not WHETHER a real G_N variation is local; we're in matter era 1−3w≈1); (2) sourced Weyl/KK — suppressed by (kL)²~10⁻⁶¹ at cosmological scales → far too small for 10%; (3) free homogeneous Weyl BC — the ONLY sector both ~10% AND large-scale-confined (evades Ġ/G), but its sign+amplitude are exactly the closure-undetermined data. So viability FORCES OBT into the sector where the sign is NOT derivable. Worked bulk solves WITH regularity (phantom brane, Cardoso-Seahra) give ENHANCEMENT — opposite to OBT's chosen suppression. δ_bulk respects causality (lag ∈[0,π/2], bounded) but does NOT fix the sign zero-point. VERDICT: OBT's S8/eROSITA growth sign is an INPUT (epistemic level of ΛCDM's Ω_c), not a prediction — UNLESS the full moving-brane bulk solve with a regularity BC imposes it (active V9.0 work, see explorations/bulk_solver). This is the single ROOT CAUSE behind the session's recurring sign-trouble (S8 natural +12% enhancement → patched to suppression by δ_bulk; eROSITA observes abundance not deficit; GL "softening" is actually steeper Tangherlini)
- **Hybrid motor**: F_web (Cosmic Web macro-forcing) + R_PBH (micro-PBH local thermodynamic dissipation, MSS scrambling)
- **Israel junction conditions** ΔK_μν = -κ₅²(S_μν - ⅓S h_μν) for macro-forcing
- **Projected Weyl tensor E_μν** generated by Cosmic Web inhomogeneity
- **ER=EPR entangled PBH network** as optional topological UV-completion (NOT load-bearing for Γ_rad or ℓ=0)
- **Wave-optics immunity**: Fresnel parameter w_F = 2πr_s/λ ≈ 0.03 ≪ 1 rehabilitates PBHs
- **Trace coupling (1-3w)**: conformal BBN protection + QCD trace anomaly ignition
- **Radiative damping Γ_rad** via bulk graviton emission
- **ξRφ non-minimal coupling** as dynamical attractor
- **Extended mass function (EMF)** log-normal for PBHs
- **Time-dependent G_eff(t)** for S₈ suppression (same mechanism as eROSITA)
- **SKA 21cm** as definitive future test
- **qBOUNCE + optomechanics** for sub-micron lab tests
- **Gregory-Laflamme instability** as ab initio derivation of the upper PBH mass bound
- **M_crit = Lc²/(2G) ≈ 6.77 × 10⁻¹¹ M☉** (perforation hierarchy threshold, from r_s = L)
- **f_PBH = 0.01 (1%)** everywhere ("tent pegs" metaphor — 1% mass tensions the membrane, 99% is Weyl geometry)
- **"Loss of local 4D gravitational singularity"** (NOT "loss of mass") for sub-M_crit PBHs → 5D Schwarzschild-Tangherlini
- **Double miracle at M_crit**: w_F(M_crit) = 2π×200/600 ≈ 2.09 — GL topological transition AND optical detection threshold coincide at same mass. NOTE (audit May 2026): this coincidence is double-edged — it means the OPTICAL microlensing cliff is DEGENERATE with the generic wave-optics detection edge (any PBH goes optically dark below ~10⁻¹⁰ M☉), so an optical cliff alone CANNOT prove the GL mechanism specifically. Distinctive confirmation needs a non-wave-optics probe below M_crit
- **Sugiyama et al. 2026**: 4 PBH candidates at 10⁻⁷ M☉ (above M_crit), zero below — consistent with perforation hierarchy. CAVEAT (audit May 2026): the "zero below" is ALSO exactly what wave-optics predicts regardless of GL (HSC blind below ~10⁻¹⁰ M☉) → CONSISTENT with the cliff, NOT a confirmation of the GL mechanism specifically
- **Popperian Falsifiability Shield — HONEST TIERING (audit May 2026, NOT 6 uniform pillars)**: the 6 candidate signatures are NOT of equal strength. **(B) GL Microlensing Cliff** at M_crit (Roman/HSC) = the ONLY genuinely distinctive, currently-testable pillar — CAVEAT: optically degenerate with the generic wave-optics detection edge (distinctive confirmation of the GL mechanism needs a non-wave-optics probe below M_crit). **(A) Bullet Cluster 150 kpc offset + (F) Galactic Center No-Spike** (GRAVITY S2 ≲1200 M☉, excludes Gondolo-Silk γ≥0.83) = CONSISTENCY CHECKS shared with ΛCDM (A falsifies pure MOND not OBT-vs-ΛCDM; F constrains the Weyl profile not the PBH network, "no spike" shared with SIDM/fuzzy/feedback). **(C) Femtolensing cepstral stacking** = SPECULATIVE (finite-source washout, Katz 2018, kills the per-event fringe; √N×0=0; "mathematically guaranteed" WITHDRAWN). **(D) Dynamical Heating** = EMPTY at asteroid mass (heating ∝ M_PBH×f_PBH ~10¹³ below Brandt threshold; predicts null = ΛCDM null). **(E) Astrometric Wrinkling** = UNOBSERVABLE (~10⁻⁷ μas, 8 orders below Gaia) + non-distinctive (10²⁰ kg = asteroid gravitationally). NET: distinctive currently-testable falsifiability rests essentially on (B). Do NOT claim "6 independent falsifiable pillars no continuum can mimic". NOTE (May 2026): eROSITA γ(M), once billed as the strongest distinctive prediction outside this shield, is itself now DEMOTED to T3 exploratory (see BANNED "eROSITA γ=1.19") — the genuinely distinctive future test is SKA 21cm; among current data, (B) is the main distinctive handle (degeneracy noted)
- **PBH X-ray invisibility = mundane low-Bondi darkness (NOT a 5D mechanism)**: asteroid-mass PBH (10²⁰ kg) are X-ray dark because Bondi luminosity L_acc~10⁻²⁸ L☉ (Ṁ∝M², tiny mass + fast motion, flow collisionless Kn≫1) — standard 4D astrophysics, shared by any asteroid-mass PBH. Confirmed by CMB-accretion literature (Ali-Haïmoud-Kamionkowski 2017 M≳10² M☉; Poulin 2017 ≳2 M☉; Serpico 2020 ≳20-50 M☉ → asteroid mass 10¹⁰-10¹² below threshold = the "asteroid-mass sanctuary"). The ONE environment with observable accretion is NS endo-parasitism (Capela-Pshirkov-Tinyakov) → NS→sub-solar-BH collapse, but OBT survives at f_PBH=0.01 (NOT a stable X-ray disk). Do NOT attribute the darkness to GL softening (see BANNED)
- **Electromagnetic Silence of the Bulk (consistency check, NOT a falsifiability pillar)**: The KK graviton decay G_KK→γγ at λ=1.32 μm was DEMOTED from "Pillar F" to a null-result consistency check (DeepThink #7-bis audit, May 2026). Ab initio: coupling universally set by reduced 4D Planck mass M̄_Pl≈2.43×10²⁷ eV (no warped enhancement in macroscopic-L regime), Γ(G_KK→γγ)=m₁³/(80π M̄_Pl²)≈4.4×10⁻⁵⁷ eV → τ_KK≈1.5×10⁴¹ s (~3.4×10²³ × age of universe). Halo surface brightness I(1.32μm)~10⁻²⁷ nW m⁻² sr⁻¹ — 28 orders of magnitude below JWST/CIBER/AKARI floor (~10 nW m⁻² sr⁻¹). Verdict: UNFALSIFIABLE. OBT's dark sector is intrinsically electromagnetically silent (Planck-suppressed, zero fine-tuning) — a structural strength vs axion/sterile-neutrino models that must tune to evade CIB, but NOT a testable prediction. Empirical confirmation: DeepSearch May 2026 found no 1.32 μm line in any pTDE/QPE (ASASSN-14ko, J0456-20, AT 2022dbl, QPEs) — consistent with the unfalsifiable verdict
- **Orthogonal Discriminant Theorem**: null WIMP detection is necessary but insufficient (shared by MOND/Verlinde). OBT breaks degeneracy via intersection: [null WIMP + Bullet Cluster offset + chronodynamics w(z)/S₈/ISW]. NOTE (May 2026): qBOUNCE REMOVED from this falsifiable intersection (was a 4th leg, now 3) — demoted to consistency check (effect δE/E~10⁻⁶ to 10⁻⁸ ≪ 10⁻⁴ GRS sensitivity). Intersection is now 3-way, not 4-way
- **5D-enhanced gravitational collapse (Penrose-Diósi re-cast) — definitive FUTURE test, conditional**: OBT predicts a mesoscopic superposition SMALLER than L=0.2μm collapses faster than the standard 4D Penrose-Diósi rate, because its gravitational self-energy E_G is sourced at sub-L separations where gravity is 5D-stronger. τ_collapse=ℏ/E_G; Monte-Carlo of E_G with bracketing crossover kernels (sharp 4D→5D + resummed Garriga-Tanaka RS2) gives a robust O(1) enhancement η=E_G(5D)/E_G(4D) growing as the object shrinks below L: η≈1.2 at R=4L, ≈3 at R=L, ≈5 (bracket 4.8-6.9) at R=100nm=0.5L, ≈10 at R=50nm. For a 100nm silica nanosphere τ_4D≈5.8×10³ s (matches Penrose's canonical 10⁻⁵cm estimate) → τ_5D~10³ s. FALSIFIABLE SIGNATURE: collapse-rate size-scan turning up below R~0.2μm. CAVEATS (4, all real): (1) conditional on Penrose-Diósi objective collapse being real (unconfirmed hypothesis); (2) needs DP-level coherence (~10³ s, vs current ms-s) — far-future sensitivity; (3) O(1) factor kernel-dependent at ~30%, only the size-scan SHAPE is robust; (4) scale-distinctive (tests an extra dim at 0.2μm, OBT's scale) but the 5D mechanism is generic braneworld. This is the dynamical re-cast of the DEAD static qBOUNCE Yukawa shift (δE/E~10⁻⁸): O(1) not 10⁻⁸. Inscribed in laboratory.md (after the Diósi-Penrose Lindblad eq). The most promising terrestrial falsifiable avenue alongside SKA 21cm. Script: /tmp/penrose_diosi_5d_refined.py (MC, injection-tested: η→1 large object, τ_4D matches Penrose)
- **Galactic Center 'No-Spike' Theorem (Pillar G)**: GRAVITY 2022/2024 S2 orbit constrains extended mass within apocenter to ≲ 1200 M☉ at 1σ. Excludes Gondolo-Silk γ≥0.83 at 95% CL and Gnedin-Primack γ≈1.5 (joint S2/S29/S38/S55 multi-star fit). OBT prediction: cored Weyl-fluid profile (ρ→const as r→0) is **topologically forbidden** from Gondolo-Silk adiabatic contraction because individual sub-critical capillaries lack 1/r cusps (softened topological wrinkles, Pillar E). Sgr A* (4×10⁶ M☉ >> M_crit) is 4D-anchored but the surrounding Weyl fluid is collectively cored. Falsifiable: future astrometric campaigns detecting extended mass ≳ 100 M☉ within 1000 AU with γ>0 would constrain the no-cusp theorem
- **Generalized Kinematic Blockade Theorem (V8.2 self-consistency)**: The same kinematic principle has DUAL consequences. (1) Cosmologically: continuous Nambu-Goto brane oscillating at ω<<m_mode cannot dissipate into bulk via classical channels → exponential DOS theorem → PBHs are thermodynamically MANDATORY as anchors (DeepThink Series 2, P1). (2) Locally for SMBH-EMRI systems: the same kinematic mismatch FORBIDS classical bulk dissipation channels (Weyl drag, radion zero-mode, membrane paradigm) from bridging dot{P}_GW~10⁻⁶ to observed partial-TDE anomalies dot{P}~10⁻³ (DeepThink #3 audit). The theory is rigid in both directions: it MANDATES the discrete PBH network and FORBIDS itself from explaining ASASSN-14ko-class orbital decay. Both results derive from identical mass-gap kinematics across all massive bulk modes (m₁=1.87 eV KK, m_φ=0.36 eV radion). This dual rigidity is the strongest internal consistency test of the framework
- **Theorem of Exhaustive Exclusion (DeepThink #1 + #3 + #4 audits, May 2026)**: ALL conceivable bulk-mediated channels for explaining ASASSN-14ko-class partial-TDE orbital decay (observed dot{P}~10⁻³, dot{P}/P~2.6×10⁻¹⁰ s⁻¹) within OBT V8.2 are individually suppressed by ≥7 orders of magnitude. **Three independent classes systematically eliminated**: (1) **Quantum KK channels** (DeepThink #1): direct Schwinger exp(-10²⁹), Hawking-KK exp(-10¹⁴), virtual KK Yukawa exp(-10¹⁹), Floquet forbidden by 22-order frequency gap. (2) **Classical spatial channels** (DeepThink #3): Chandrasekhar Weyl drag ~10⁻²⁶ (extreme mass ratio), membrane paradigm tidal heating (M_*/M_SMBH)²~10⁻¹⁵, radion scalar dipole ≤10⁻⁹ (Cassini ω_BD>40000) AND blockaded by m_φ=0.36 eV Goldberger-Wise gap. (3) **Global temporal channels** (DeepThink #4): G_eff(t) cosmological modulation max |dot{G}/G|=f_osc/Δt_slip~1.58×10⁻¹⁷ s⁻¹ (factor 10⁷ short), Fourier harmonics at n~10¹⁷ exponentially killed by slip duration cutoff (n_cut≈10), spatial phase gradient ~10⁻²⁶ m⁻¹ purely conservative, proper-time dilation correction ~10⁻¹⁸ s⁻¹, z=0.0214 redshift phase beat no kinematic enhancement. **Total verdict**: dot{P}_OBT_total << 10⁻¹⁵ s⁻¹ << observed 10⁻¹⁰ s⁻¹. The framework is mathematically COMPLETE in its prohibition. ASASSN-14ko's anomaly is definitively 4D astrophysical (Roche overflow, tidally inflated stellar envelope, non-conservative mass transfer per Linial-Sari 2023, Yao+ 2023, Bandopadhyay+ 2024). This exhaustive rigidity is the ultimate epistemological proof: OBT V8.2 cannot be parametrically tuned to overfit unrelated astrophysical anomalies. The theory's refusal to explain everything is the proof it explains anything correctly
- **ER=EPR Epistemological Firewall**: ODE requires ONLY (1) inflation ℓ=0 + (2) local PBH thermodynamics (MSS scrambling). ER=EPR = optional UV-completion for decoherence protection. If ER=EPR false → all T1/T2 predictions survive 100%. Sections marked [Theoretical Extension]
- **GW170817 compatibility**: tensor GW modes (KK zero mode) propagate at c on brane, orthogonal to scalar radion oscillation
- **Hawking immunity**: T_H ~ 900 K at M_crit, t_evap ~ 10^37 yr, immune to INTEGRAL/Fermi-LAT
- **QCD connection**: τ₀^{1/3} ≈ 257 MeV — phenomenological Ansatz bottom-up (period constrains τ₀ independently of QCD), derived ab initio top-down via KS (K=21, M=10 → 257 MeV). Both approaches converge.
- **Limit cycle uniqueness**: Liouville-Filippov contraction κ = e^{-4.74} ≈ 8.7×10⁻³ (Banach fixed-point, ×115/cycle — NOT the numerical MLE of -0.016). Note: C_slip = 3H + γ_slip (NOT +Γ_rad+γ_slip, which would double-count the PBH scrambling)
- **Fenichel-Neishtadt persistence**: spectral gap |λ_trans|/ε = 2.37/0.14 ≈ 17 → NHIC survives non-autonomous drift
- **Airy-Yukawa ab initio**: ⟨1|δV|6⟩ = -2V₀(L/z₀)³, perturbative series to O(α⁶) with 5 decimal convergence (0.97460)
- **Yukawa-Robin mapping**: λ_n(L) = (mg/2V₀)(z₀/L)³[1+4ε_n(L/z₀)²], spectroscopic splitting 3.1% in SHAPE only — but rides on an unobservable amplitude δE/E~10⁻⁶ to 10⁻⁸ (overlap suppression 2(L/z₀)³~8×10⁻⁵). NOT a smoking gun: ≪10⁻⁴ GRS sensitivity. The "55× amplification with resolution" was a category error (resolution ≠ wavefunction scale)
- **KS UV completion**: K=21, M=10, g_s=0.1 → τ₀^{1/3} = 257 MeV with zero fine-tuning
- **KK spectrum**: J₁(m_nL)=0 (graviton), exact transcendental equation for all ν
- **Branching ratio**: B ≈ 9.7×10⁻¹¹ (N_max ≈ 8.3×10⁷ KK modes = AdS₅ heat sink)
- **BSSN 5D**: d=4 conformal weights (1/8 in ∂_tψ, 1/4 in K²), ΔK_μν = -(1/3)κ₅²τ₀h_μν
- **CMPP extraction**: Ψ_ij^(5) = 3×3 STF matrix (5 polarizations), NOT scalar Ψ₄
- **Billion-step**: κ_Z4^(ℓ) = 1.4/Δt_ℓ (AMR-indexed) + Kreiss-Oliger order 9
- **IMEX + HMM**: mandatory for 10³² scale ratio (explicit Berger-Oliger physically impossible)
- **Γ_rad = ln(S_BH)/(2π) ≈ 20.7**: Key ab initio result — not a free parameter but Bekenstein-Hawking entropy ÷ 2π
- **Retarded 5D Green's function**: V_eff = 15/(4z²), UV censorship ψ_n(0) ∝ z⁴→0, IR coupling ψ_n(L) ∝ J₂(m_nL) ≠ 0
- **KK spectrum exact**: Bessel quantization m_n = j_{1,n}ℏc/L, graviton m₁ = 3.832×0.197/0.2 ≈ 3.78 eV (flat-space; warped: 1.892k ≈ 1.87 eV), Sturm-Liouville kinematic pumping
- **Spectral zeta**: ζ_Δ(s) → Riemann mapping, Weyl-McMahon baseline -M₀/12 + **exact transcendental correction** from Bessel roots (2.1% inharmonic shift, δE converges O(n⁻³)). Higher poles s=-3/2,-5/2 map bijectively onto Seeley-DeWitt a₂,a₀. **Physical bound**: δ_phys/Λ_QCD ≪ 10⁻³⁰ (one-loop formal ratio ~10⁻³⁸, QFT error budget: two-loop ε_loop~10⁻³⁷, PBH backreaction ~10⁻⁴⁷, non-perturbative ~10⁻⁹²¹ → robust 10⁻³⁰ sanctuary)
- **Seeley-DeWitt a₀-a₅**: exact for AdS₅ orbifold, Gilkey-Branson-Kirsten boundary terms. Numerically evaluated: ā₀=0.249 eV⁻¹, ā₁=0.902, ā₂=-2.67 eV, ā₃=4.13 eV² (induces Einstein-Hilbert/M_P), ā₄=12.7 eV³. **a₅ (The Holographic Grail)**: a₅_bulk≡0 in D=5 (odd dim), entire log anomaly from branes only. Cubic extrinsic invariants (K³=±64k³, KK_μν²=±16k³, K_μνK^νρK_ρ^μ=±4k³) contract to P₅∝k⁴. **ā₅(UV)=2.845 eV⁴, ā₅(IR)=0.0521 eV⁴** (98.2% confined to Planck brane, ×55 crushing via e⁻⁴ᵏᴸ). c_log counterterm (Skenderis) localized exclusively on UV brane → IR sanctuary.
- **Skenderis holographic renormalization**: Fefferman-Graham inversion, counterterm dictionary c₁(tension), c₂(G_N), c_log(anomaly)
- **δ_phys/Λ_QCD ≪ 10⁻³⁰**: inverse hierarchy, IR bulk (1 eV) cannot destabilize UV brane (257 MeV). One-loop formal ~10⁻³⁸, two-loop ε_loop~10⁻³⁷, PBH backreaction ~10⁻⁴⁷
- **MERA/HaPPY**: 109 layers, bond dim ln χ = S_BH ≈ 4.8×10⁵⁶, RT phase transition → expander graph → ∂S_EE/∂d = 0
- **OTOCs/MSS**: λ_L = 7.4×10¹⁴ s⁻¹, t* ≈ 0.2 ps, cosmic scrambling ¼ picosecond, t* ≪ t_QCD by 8 orders
- **Dirac collapse**: σ/L ~ 10⁻¹⁰, multipole hierarchy e^{-2×10²⁰}, ODE = exact corollary of path integral. Finite-N corrections: expander graph spectral gap λ₁≈c ln N, σ₁/L ~ 10⁻³⁸·⁵, dipole P ~ exp(-10⁷⁴). N_min ≈ 4500 (topology only) or O(1) (with κ~10⁵⁶). Period correction ω₀(N) ~ 10⁻⁷⁶. RT phase transition survives for all N > e^{2/c}.
- **On-shell ER action**: δS_ij bilocal, c ~ S_BH ~ 10⁵⁶, freeze-out at 10⁷⁴
- **Dyson horizon**: k_div ≈ 6,360 (hyper-asymptotic immunity)
- **Schwinger → Kampé de Fériet**: F_{0:1;1}^{3:0;0}, I_{1,6} = 0.002074 (5×10⁻⁷ precision). Dirichlet anomaly RESOLVED: Δ=0.000044 (2.1%) from 4-branch holographic tensor (Ai = c₁f - c₂g → [ff],[fg],[gf],[gg]). Destructive interference under Dirichlet constraint telescopes cross-branches. Anomaly = O(α⁴), exact shadow of brane.
- **CY concrete**: P⁴[18]_{1,1,1,6,9}, χ=23328, tadpole 210≤972
- **No-Go isotrope**: V ~ 10¹⁶³ → χ=-64000 → Swampland + M_Pl ~ 10⁹⁹
- **KKLT uplift**: 763-1+210=972, D3 budget +762. Multi-throat architecture: V_min ~ -10⁻³¹ M_Pl⁴, QCD throat (10⁻⁷⁶ M_Pl⁴) 45 orders too weak → REQUIRES second shallow throat at ~5×10¹⁰ GeV for uplift. Geometric selection theorem.
- **LVS mass spectrum**: m_τs ~ 10⁶ GeV (frozen), m_V ~ 10⁻⁶ eV (ultra-light). M_s = 1.19×10¹² GeV (intermediate string scale). m_{3/2} = 1.75×10⁹ GeV (SUSY above LHC → null results predicted)
- **Fisher Jacobian**: condition number 2.8, SVD σ={2.51,1.00,0.90}
- **Fisher forecast**: σ(T)/T=6.7%, σ(L)/L=15%, τ₀-L anti-correlation r=-0.76 broken by PTA
- **Cobaya module**: obt_v82_likelihood.py + obt_v82_mcmc.yaml
- **n_σ metrics**: 1.25σ (FLAG MS̄) and 0.11σ (chiral condensate)
- **Fourier stick-slip spectrum**: A_n/A₁ = {1, 0.476, 0.293, 0.197, 0.138} — locked by bulk topology (D=0.9, τ=1/30), zero extra free params
- **DESI aliasing**: LRG3 bin z=0.93 at phase 82.8% of cycle — "phantom crossing" is geometric shock aliasing on CPL linear template. ΔBIC ≈ -6.4 (DR2, Strong — k=1 vs CPL k=2, Occam REWARDS OBT), forecast ΔBIC ≈ -22 (Year 5, Decisive). Chronologically anchored stick-slip: k=1 effective param (A_w only, T and phase locked)
- **S₈ cross-observational consistency** (NOT "rigidity"): growth suppression order 4–10% (S₈≈0.79), consistent with tension, δ_bulk=1.36 rad (BKM, genuinely derived). NOT ±0.002 — waveform-shape dependent at factor-~2 (audit May 2026). f_osc/D anchored to DESI w(z), itself small (A_w=0.003)
- **eROSITA non-linear** [⚠️ SUPERSEDED → T3 exploratory, May 2026; see BANNED "eROSITA γ=1.19"]: ~~γ_eff≈0.80 (linear), amplified to 1.19 by Press-Schechter; mass-dependent γ(M): groups 0.88, clusters 1.19, monsters 1.47~~. Mechanism retained as illustration only — NOT a confirmation (eROSITA's real S8=0.86 is cluster-abundant, opposite to OBT's needed deficit), NOT a discriminant (f(R) is scale/mass-dependent, γ(M) degenerate with systematics), sign is a free bulk BC
- **eROSITA falsifiable prediction** [⚠️ SUPERSEDED May 2026 — see BANNED "eROSITA γ=1.19 confirms OBT"; theory-file reframe pending]: ~~γ(M) is monotonically increasing with mass (strict proof via Tinker sensitivity kernel A(ν) = cν² + a/(1+(ν/b)^a)). GR root γ=0.55 unreachable. 4-bin grid: groups 0.88, light clusters 0.99, massive 1.19, monsters 1.47. Exclusion theorem: f(R)/scalar-tensor predict universal γ — OBT predicts ascending spectrum.~~ The f(R)-universal-γ premise is FALSE (f(R) is scale/mass-dependent), γ(M) is degenerate with baryonic systematics, eROSITA's real S8=0.86 is cluster-abundant (opposite to OBT's needed deficit), and the growth SIGN is a free bulk BC (see closure entry above). Demote to T3 exploratory "mass/z-dependent abundance modulation", not a falsifiable discriminant
- **MOND ab initio**: a₀ = cH₀/2π from Gibbons-Hawking + Unruh (2π = Euclidean time circle S¹)
- **MOND μ(x)**: x/√(1+x²) from 5D Gauss-Codazzi orthogonality theorem (g∈tangent bundle ⊥ a₀∈normal bundle, exact geometric identity) → Pythagorean quadrature g_5D = √(g²+a₀²) → cosine projection
- **Cluster resonance (sinc theorem)**: ⟨a₀⟩ = a₀^max × sinc(πt_dyn/T). Dwarfs: sinc≈0.996 (99.6% MOND). Clusters: resonant suppression envelope — sinc(π)=0 at exact t_dyn=T, but physical dispersion t_dyn∈[1.5,2.5] Gyr gives 70-100% attenuation (residual 0-30% insufficient for virial → Weyl fluid mandatory). **Bullet Cluster 3-component resolution**: sinc(0.053π)≈0.995 (MOND survives at 99.5% → 4700 km/s velocity), Weyl fluid decouples ballistically → Δr≈150 kpc offset. Three-component gravity: g_N + MOND×sinc + Weyl
- **Dynamical Schwinger**: slip shock at v_max=0.05c collapses static exponent 10³¹ → 10⁹ (22 orders), but exp(-7.2×10⁹) ≡ 0. Full KK tower N_total ≡ 0. Dissipation 100% via holographic viscosity (Γ_rad), 0% quantum pair production.
- **Filippov invulnerability**: shock fierce enough for DE harmonics yet 9 orders below Schwinger threshold — thermodynamic masterpiece
- **Kinematic Blockade theorem**: Classical 5D GR gives Γ_rad^{5D-GR} ≡ 0 (m₁T_slip ~ 3.6×10³¹, exp(-3.6×10³¹) = 0). Continuous Nambu-Goto membrane CANNOT dissipate. Combined with Fermi's Golden Rule + exponential DOS theorem → PBHs thermodynamically MANDATORY (not optional, not ER=EPR-dependent)
- **Local informational viscosity**: Γ_rad is NOT classical Bremsstrahlung but local quantum informational viscosity — each PBH absorbs brane kinetic energy at its horizon, thermalizes via MSS-saturated fast scrambling, emits via 5D Hawking into KK modes. Entirely local and causal, zero wormhole transmission
- **Spectral flattening (NANOGrav)**: tensor TT projection sources from φ̈(t) not φ(t) → Filippov shock = Dirac δ impulses → flat (white noise) acceleration spectrum. f₀ = 1.58×10⁻¹⁷ Hz (16 attoHz), NANOGrav at 16 nHz listens to the n ≈ 10⁹ harmonic. h_c(16 nHz) ~ 10⁻¹⁵ (matches NANOGrav 15yr, zero additional free params beyond global EFT set)
- **f₀ correction**: fundamental brane frequency is 16 attoHertz (NOT 16 nanoHertz). NANOGrav band = billionth overtone
- **AdS₅ viscoelastic retardation**: δ_bulk = 1.36 rad (BKM theorem). Analytically derived from L→Γ_slip and z_eff→Γ_stick. **Arctan saturation theorem**: ω/Γ_stick ≈ 9-15 → arctan at 93-96% of π/2 → ΔS₈ < 0.002 across z_eff ∈ [0.1, 1.0] (order of magnitude below DES ±0.018). NOT a hidden degree of freedom. G_eff(t) = G_N[1 + f_osc × W(t/T + δ_bulk/(2π))], PLUS sign
- **Kesten-McKay spectrum**: DOS of ER=EPR graph → ρ(λ) = d/(2π(d²-λ²))√(4(d-1)-λ²). Continuum convergence O(1/√N) ~ 10⁻¹⁰. Discrete holographic spacetime = smooth GR manifold to 10 decimal places
- **Percolation immunity**: site percolation threshold p_c ≈ 1/(d-1) ≈ 2.2% for d=46. Universe survives 98% PBH destruction. Safety hierarchy: N_perc≈46 ≪ N_min≈4500 ≪ N_actual~10²⁰ (19 orders margin). ER=EPR network = most robust quantum error-correcting code physically conceivable
- **KS landscape statistics**: 2,437 valid flux pairs (1≤M≤30, M<K≤50, g_s∈[0.05,0.2]), f_QCD = 0.49% per throat, P_CY = 1-(1-f_QCD)^50 ≈ 21.8% per manifold. QCD-scale throat is generic (1 in 5 CY manifolds), NOT fine-tuned
- **ER=EPR ab initio genesis**: PBHs from inflationary squeezed vacuum states (Martin & Vennin 2015). Entanglement from shared Bunch-Davies vacuum. Page's theorem (post-scrambling, t > t_Page) guarantees maximal bipartite entanglement. ER=EPR (Maldacena-Susskind) promotes entanglement to wormhole topology. Expander graph structure MANDATORY (not postulated) from random matrix universality
- **Scrambling regularization**: Filippov Dirac δ impulse is regularized by scrambling timescale t* ~ 10⁻¹³ s < 1/ν_KK ~ 10⁻¹⁴ Hz. Branching ratio B ~ 10⁻¹⁰ from 5D Hawking emission (not classical KK excitation). Resolves apparent Kinematic Blockade vs Filippov shock contradiction
- **Tier system (epistemological)**: T1 = exact ODE/analytical proof (DESI w(z), S₈ linear suppression, MOND μ(x)+a₀ derivation). T2 = semi-analytic/closed-form (ISW semi-analytic pending CLASS, neutrinos, birefringence, JWST, SMBHs, Λ, NANOGrav, DF2/DF4, Amaterasu, etc). T3 = qualitative mechanistic (eROSITA γ(M) DEMOTED here May 2026, Li-7 BBN network pending, baryogenesis Boltzmann pending, Hubble tension, dipole, KBC, Dark Flow, Space Roar, ORCs, Methuselah, WD Q-branch, Planet 9, Flyby). ~3 T1 + 15 T2 + 14 T3 (eROSITA moved T2→T3)
- **MOND scope note**: MOND phenomenology is Milgrom (1983). The thermodynamic derivation a₀=cH₀/2π has prior art: Verlinde (2016), Pazy (2013), McCulloch (2007). OBT V8.2 does NOT claim to have discovered this relation. **OBT's genuine novelty** is: (a) embedding a₀ into exact SMS 5D geometry, (b) deriving μ(x)=x/√(1+x²) as Gauss-Codazzi trigonometric projection (strict orthogonality theorem, not heuristic), (c) sinc extinction at cluster scales. SPARC fit uses identical formula to existing literature; novelty = zero free parameters from geometric first principles + cluster failure mechanism
- **Dynamical Naturalness (Dirac LNH)**: OBT V8.2 realizes Dirac's Large Numbers Hypothesis (1937) — time-varying G_eff(t) from stick-slip dynamics, without violating local GR (trace coupling (1-3w) confines variation to cosmological scales). Fine-tuning problem resolved: static parameters → dynamic attractors (Λ from thermodynamic relaxation, T from PLL eigenvalue, a₀ from Gibbons-Hawking, η_B from dynamic θ_QCD). Brans-Dicke distinction: OBT preserves local GR exactly
- **Bayesian Occam's Miracle**: T promotion to eigenvalue refunds prior volume penalty → Δln K ≈ 5.8 (Decisive, both priors converge: 2.8+3.11=5.91, 4.13+1.61=5.74). ΔBIC = -6.4 (Strong, k=1 vs CPL k=2). Prior-dependency eradicated. Theory is 330× more probable than ΛCDM on current data
- **Exponential Density of States Theorem**: Fermi's Golden Rule + Kinematic Blockade (|M|²~exp(-3.6×10³¹)) proves polynomial DOS QFT cannot dissipate brane. Only exponential DOS (black holes, S_BH~10⁵⁶) opens channel. PBHs are THERMODYNAMICALLY MANDATORY, zero wormhole dependence
- **ℓ=0 inflationary fossil**: Global phase coherence from inflation homogenizing the radion field (like CMB isotropy). NOT from ER=EPR wormhole synchronization. Standard cosmology, not conjecture
- **ER=EPR = optional UV-completion**: Provides elegant geometric description of PBH entanglement (squeezed vacuum → expander graph). Adds topological decoherence protection. If ER=EPR is false, ODE + Γ_rad + ℓ=0 all survive intact
- **Chronological anchoring (Observationally Anchored)**: Phase 0.0 at QCD ignition (physics-derived), Phase 0.9 today (empirical from DESI w_max at z=0). Universe completed N+0.9 cycles, ξRφ PLL selects N=6 → T=13.80/6.9=2.000±0.003 Gyr. Falsifiable: if DESI Y5 moves w_max to z=0.05, T generalizes to (13.80-t_max)/(N+D)≈1.90 Gyr
- **Diagnostic table (March 2026)**: Systematic test of ALL sign/coupling combinations in growth ODE with exact stick-slip waveform. Results: Israel MINUS→+12.1% enhancement, PLUS→-11.0% suppression, w(z) in H(a)→negligible (0.002%). Proved: phase delay is continuous (not algebraic sign), leading to discovery of AdS₅ viscoelastic retardation. Credits: Claude Opus (diagnostic), Gemini DeepThink (arctan deduction)
- **δ_bulk (Bulk Transfer Function)**: viscoelastic retardation of AdS₅. δ_BKM = 0.9×arctan(π/0.243)+0.1×arctan(π/20.7) = 1.36 rad — **GENUINELY DERIVED** (arctan viscoelastic phase lag, z_eff-robust via saturation). This part is solid (unlike α for qBOUNCE which is just posed). BUT the S₈ value it feeds is NOT ±0.002: independent recompute gives ~10% (triangular slip) vs 4.5% (exponential) at the SAME δ_bulk, sinusoid sign-flips → S₈ suppression is order 4–10%, waveform-dependent, consistency-with-tension not precision (audit May 2026)
- **Exascale NR = verification not necessity**: 5D numerical relativity would provide independent validation but is NOT required for the theory's mathematical consistency (all 60 derivations are analytical/semi-analytical). Current feasibility limited by 10³² scale ratio → IMEX+HMM mandatory

### Key References:
Maldacena & Susskind 2013, Van Raamsdonk 2010, Shiromizu, Maeda & Sasaki 2000, Maartens 2004, DESI 2024/2026, Goldberger & Wise 1999, Carr, Kühnel & Sandstad 2016, Jenke et al. (qBOUNCE) 2014, Gregory & Laflamme PRL 70 (1993), Tangherlini 1963, Sugiyama, Takada et al. arXiv:2602.05840 (2026), Klebanov & Strassler 2000 (warped throat), Balasubramanian et al. 2005 (LVS), Filippov 1988, di Bernardo et al. 2008, Leine & Nijmeijer 2004 (saltation), Fenichel 1979, Llibre, Novaes & Teixeira 2015 (Filippov persistence), CMPP (Coley-Milson-Pravda-Pravdova) 2004, Godazgar & Reall 2012 (5D peeling), Skenderis 2002 (holographic renormalization), Lloyd 2000, Maldacena-Shenker-Stanford 2016 (MSS bound), Pastawski-Yoshida-Harlow-Preskill 2015 (HaPPY code), Albeverio et al. 2005 (von Neumann self-adjoint extensions), Gibbons & Hawking 1977 (cosmological horizon thermodynamics), Unruh 1976 (detector acceleration radiation), Sekino & Susskind 2008 (fast scrambling), Bousso & Polchinski 2000 (flux landscape), Douglas & Kachru 2007 (string landscape review), Alon 1986 / Alon-Boppana (expander graph spectral gap), Kesten 1959 / McKay 1981 (regular graph spectral density), Friedman 2003 (Ramanujan graph proof), Bordenave 2015 (sparse random graph universality), Martin & Vennin 2015 (inflationary PBH squeezed vacuum genesis), Page 1993 (Page's theorem, maximal entanglement post-scrambling), Milgrom 1983 (MOND empirical phenomenology), Verlinde 2016 (emergent gravity, a₀ from holographic thermodynamics), Pazy 2013 (MOND from Unruh effect), McCulloch 2007 (modified inertia), Chae 2025 (Gaia DR3 wide binary gravitational anomaly, arXiv:2502.09373), Tinker et al. 2008 (halo mass function), Clowe et al. 2006 (Bullet Cluster lensing offset), Ulmer & Goodman 1995 (femtolensing), Matsunaga & Yamamoto 2006 (wave-optics PBH lensing), Brandt 2016 (PBH dynamical heating constraints), Green 2016 (PBH wide binary disruption), Dirac 1937 (Large Numbers Hypothesis, time-varying G), Brans & Dicke 1961 (scalar-tensor gravity), Gondolo & Silk 1999 (adiabatic dark matter spike around SMBH), Gnedin & Primack 2004 (stellar heating of DM spike), GRAVITY Collaboration 2022/2024 (S2 orbit precession, extended mass ≲ 1200 M☉ at apocenter, exclusion of Gondolo-Silk DM spike around Sgr A*)

## Key Parameters
| Parameter | Value |
|-----------|-------|
| Brane tension τ₀ | 7.0 × 10¹⁹ J/m² = 0.017 GeV³ |
| Energy scale | τ₀^{1/3} = 257 MeV ≈ Λ_QCD |
| Period T | 2.000 ± 0.003 Gyr (derived chronodynamic eigenvalue: 13.80/6.9, N=6 mode selected by ξRφ PLL) |
| Phase φ₀ | π/2 (at w maximum → w_a < 0) |
| Extra dimension L | 0.2 μm (NEVER "0.2 m") |
| φ_crit | ~0.1 L (QCD threshold) |
| f_osc | 0.10 |
| A_w | 0.003 |
| S₈ suppression | order 4–10% (S₈≈0.79), waveform-shape dependent — NOT ±0.002; δ_bulk=1.36 rad (BKM, derived). Consistent with tension, not precision |
| ISW significance | ~1σ realistic (cosmic-variance-capped, Δχ²_max~11.5 over ℓ=10-20); the Δχ²=32.9/6σ was a covariance-omission artifact (DeepSearch audit May 2026), NOT a data-fit |
| Micro-PBH EMF | Log-normal, 10⁻¹⁴ to 10⁻¹⁰ M☉ |
| f_PBH | 0.01 (1%) — NOT 10% |
| M_crit (Gregory-Laflamme) | Lc²/(2G) ≈ 6.77 × 10⁻¹¹ M☉ (from r_s = L) |
| ξ (non-minimal coupling) | ~0.15 |
| Fresnel parameter (PBH) | w_F = 2πr_s/λ ≈ 0.03 ≪ 1 (wave-optics immune) |
| SPARC rotation curves | RMS = 29.3 km/s (0 params) vs NFW 35.0 km/s (270 params). Exact RAR: g_obs=√((g²_bar+g_bar√(g²_bar+4a₀²))/2). Sinc(0.11π)≈0.98 (1% galactic correction) |
| Banach contraction κ | e^{-4.74} ≈ 8.7×10⁻³ (contraction ×115/cycle) |
| Spectral gap (Fenichel) | \|λ_trans\|/ε = 2.37/0.14 ≈ 17 (NHIC persistence) |
| Branching ratio B | ≈ 9.7×10⁻¹¹ (N_max ≈ 8.3×10⁷ KK modes) |
| First KK graviton mass | m₁ = j_{1,1}ℏc/L ≈ 3.78 eV flat-space (warped: 1.87 eV) |
| Radion mass (Goldberger-Wise) | m_φ ≈ 0.36 eV (warped IR stabilization scale; locally Yukawa-suppressed for ω<<m_φ; cosmological 2 Gyr is forced stick-slip, NOT free oscillation) |
| KS flux integers | K=21, M=10, g_s=0.1 → τ₀^{1/3} = 257 MeV |
| AdS₅ bulk transfer delay δ_bulk | 1.36 rad (BKM theorem, analytically derived from L + z_eff, zero additional free params) |
| Dual-damping parameters | Γ_stick = 3H ≈ 0.25 Gyr⁻¹, Γ_slip = Γ_rad ≈ 20.7 Gyr⁻¹, ω = π ≈ 3.14 Gyr⁻¹ |
| Robin splitting | Δλ/λ = 3.1% between n=1 and n=6 (SHAPE only; amplitude δE/E~10⁻⁶–10⁻⁸ unobservable, NOT a smoking gun — consistency check) |

## ABSOLUTE RULE: Site = PDF symmetry
**Every scientific page on the site MUST be a chapter in the PDF. No exceptions.**
Pages excluded from PDF (non-scientific): about.md, downloads.md, research.md, refutation.md, videos.md.
Note: index.md IS in the PDF as Chapter 1 (introduction), but is not a theory source file.
ALL other .md pages with scientific content MUST be in generate_pdf.py doc_order.
**If you add a new scientific page to the site, add it to the PDF immediately.**
**If you remove a page from the PDF, you are BREAKING the symmetry. Do NOT do this.**

## PDF Generation — CRITICAL WORKFLOW
**The CI does NOT auto-push the PDF.** You MUST regenerate and push it manually after ANY .md file change. If you forget, the site will have a stale PDF.

**After modifying any .md file that is in the PDF (index.md, discoveries.md, theory.md, chronology.md, predictions.md, docs/theoretical_foundations.md, laboratory.md, tools.md), ALWAYS do:**
```bash
python3 scripts/generate_pdf.py
git add oscillating_brane_theory_latest.pdf oscillating_brane_theory_latest.md.txt output/oscillating_brane_theory_latest.pdf output/oscillating_brane_theory_latest.combined.md
git commit -m "Regenerate PDF + markdown"
git push
```

The CI only generates the PDF as an artifact (for verification). It does NOT push it to the repo.

### PDF Pipeline Pre-Processor (generate_pdf.py)
The script applies a 3-step sanitization pipeline before pandoc:
1. **Unicode→LaTeX** (`sanitize_unicode_for_latex`): Greek letters, operators, super/subscripts, typographic chars → LaTeX commands. Only operates outside `$...$` and `$$...$$` blocks.
2. **HTML→Markdown** (`convert_html_tables_to_markdown`): Converts `<table>` to pipe-tables, strips `<div>`, `<h3>`, Jekyll Liquid templates, emojis. Fixes indented headers.
3. **Polish** (`polish_combined_markdown`): Merges split exponents (`10$^{1}$$^{9}$` → `$10^{19}$`), fixes hybrid notation (`tau$_{0}$` → `$\tau_0$`), converts image paths to relative `./plots/`.

**Engine**: pdflatex (first attempt), xelatex (fallback, currently used — pdflatex fails on HTML table remnants). xelatex handles remaining Unicode natively and fixes fi/fl ligature issues.
**Output**: PDF + `.md.txt` (same content, AI/text-parser friendly, downloadable from site).

### Compression
PDF pipeline includes Ghostscript post-processing (JPEG/DCT at 200 dpi).
Reduces ~3 MB → ~1.9 MB without quality loss. Requires `ghostscript` package locally.

### Ghost grep (V8.2 + March 2026 audit):
```bash
pdftotext oscillating_brane_theory_latest.pdf - | grep -i "Ringermacher\|Point Unique\|tiny hammers\|momentum hit\|Block Universe\|dark matter impacts\|LRDs.*anchor\|holographic thermodynamics\|entropic force\|thermodynamic backreaction\|EDGES.*confirm\|CatWISE.*confirm\|single.*PBH.*mass\|global.*5.2\|MORRIS\|Farrah\|cosmological coupling.*k.*3\|scale.dependent.*Yukawa\|Bottle.*Beam\|Neutron Lifetime"
```

### CRITICAL: Jekyll/Liquid Traps
- **NEVER write literal Liquid tags** in any .md file (including CLAUDE.md). Jekyll interprets them and the build crashes.
- Bad: writing the characters percent-brace literally in documentation
- Good: describe as "Jekyll Liquid templates" or "Liquid tags" in prose
- This crashed the entire site deployment on 2026-03-25 until fixed.

## Document Architecture
- **Site pages = PDF chapters** (one file, one page, one chapter)
- PDF is generated by `scripts/generate_pdf.py` which assembles these files:
  1. `index.md` → Ch 1: Home
  2. `discoveries.md` → Ch 2: Discovery & Correction (30 anomalies + 10 collateral discoveries)
  3. `theory.md` → Ch 3: Complete Theoretical Framework
  4. `chronology.md` → Ch 4: Cosmic Chronology
  5. `predictions.md` → Ch 5: Observational Predictions
  6. `laboratory.md` → Ch 6: Laboratory Proofs (qBOUNCE + 5D Geometric Bypass)
  7. `tools.md` → Ch 7: Computational Tools
  8. `docs/theoretical_foundations.md` → Appendix A: Simplified 4D EFT (Linearized Toy Model)
- **No blog posts** in the PDF (they are duplicates of main chapters)
- **No split files** (parts 1-4 merged into theoretical_foundations.md)
- When editing a site page, the PDF updates automatically via CI

## explorations/ — Out-of-Scope Research Seeds (NOT V8.2)
The `explorations/` folder (created May 2026) holds heuristic, speculative work **STRICTLY OUTSIDE OBT V8.2**: not in the PDF, not in `generate_pdf.py` doc_order, not in the validation pipeline, not theory content, carrying no academic claim of V8.2. It is a sanctioned exception to the "no new .md files" Sacred Rule — `explorations/README.md` is a folder readme, not a site page or a theory file.
- **Two V9.0 seeds consigned (May 2026), each with verified facts + the gates that keep it a direction not a result** (see `explorations/README.md`):
  - **Seed 1 — Riemann zeros as a PBH AdS₂ throat spectrum (Hilbert-Pólya).** Scripts: `decoherence_riemann.py` (explicit-formula ψ(x) staircase), `riemann_berry_keating.py` (Berry-Keating smooth count vs zeros, verified), `tidal_charge_ads2.py` (tidal-charge BH horizons + AdS₂×S² at extremality). Chain: Riemann zeros ↔ Berry-Keating H=xp ↔ CQM ↔ AdS₂ ↔ near-extremal tidal-charge PBH throat. **Three gates**: (1) needs q>0 near-extremal tidal charge — default braneworld sign is NEGATIVE, sign is a 5D bulk integration constant (brane eqs not closed), AND near-extremal T_H→0 contradicts the hot T_H~900K fast-scrambler PBHs Γ_rad relies on; (2) GUE statistics are generic to quantum chaos, not OBT-specific; (3) Hilbert-Pólya operator unsolved by anyone. Verified: Berry-Keating smooth density matches zeros; extremal q=(GM)² → AdS₂(r₀)×S²(r₀); ζ(−1)=−1/12 via functional equation.
  - **Seed 2 — Void "entanglement" signature.** Script: `void_entanglement.py`. **Verdict: NOT falsifiable as entanglement.** Thermal route T=ℏH₀/2πk_B≈2.7×10⁻³⁰ K (10⁻³⁰ of CMB, unobservable); the only falsifiable handle is the CLASSICAL cymatic scale λ=cT≈613 Mpc (k≈0.0103 Mpc⁻¹, Euclid/DESI) — but that is classical Chladni, already in V8.2 (KBC/Big Ring/Giant Arc), NOT entanglement; discriminant (fixed nodes vs position-independent correlation) killed by cosmic variance + Maldacena 2015. Metaphysical interpretation, not prediction.
- **Bulk perturbation solver (`explorations/bulk_solver/`, May 2026)** — the active V9.0 calculation that would turn the growth-sector SIGN from an input into a prediction (see REQUIRED "Growth-sector SIGN is a free bulk BC"). Goal: solve the linear scalar-perturbation master equation in AdS5 with a MOVING brane + a regularity/causal bulk BC, and read whether it IMPOSES enhancement or suppression. This is a 1+1D-per-k PDE (NOT the exascale nonlinear slip-shock) — runs on a workstation; reproduces the Cardoso-Hiramatsu-Koyama-Seahra (0705.1685) class of calc. Files: `double_null.py` (Gundlach-Price-Pullin marcher), `cardoso_ads.py` (verified AdS5 reduced potential V_ψ=k²−1/(4z²)), `obt_bulk.py` (background + flagged-`VERIFY` physics), `run_validation.py`. Strict validation GATES: **Gate 0 PASSED** (free-field exact 1e-13 + 2nd-order convergence); **Gate 0.5 PASSED** (reproduces analytic Bessel mode cos(ωτ)√z J₀(qz) at order 2 → AdS5 potential validated, coefficient +1 confirmed verbatim ×2 vs Cardoso Eq.18); **Gate 1 PENDING** (moving-brane junction BC + radiation-era trajectory → reproduce Cardoso amplification); then Gate 2 (GR recovery) → Gate 3 (OBT late-time sign) → Gate 4 (robustness). Trust NO sign until Gate 1 passes. Needs numba (installed in venv)
- **Consilience engine — the "OBT-Game" (`explorations/chercheur-game.md` + `explorations/bootstrap_journal.md`, May 2026)** — Romain's recursive method to harden OBT by debunking the FLAWED EXTERNAL theories around it. Presuppose OBT is true → find where it *appears* to fail in a configuration type (+ its variants) → fix the misfit by correcting ONE parameter of an ADJACENT (non-OBT) theory → if a batch of variants fits AND one variant reveals the mechanistic WHY (the debunk), that becomes a **card**. The game = **OBT + {cards}**, grown until everything works with no unexplained parameter ("the magic": more cards → easier to find the missing ones; abandoned cases resurface as each card peels one entangled defect). `chercheur-game.md` is the CLAUDE.md of the (to-be-built) software (method spec, 4-stage architecture pre-sieve→auto-compute→agent-triage→synthesis, NON-NEGOTIABLE invariants incl. *never glue OBT*, *predict before you sieve*, *the "why" barrier*, *a card REQUIRES CERTAINTY*, and the **Monster Registry §9** for promising-but-uncertain leads). `bootstrap_journal.md` = verified-sure findings only (V1–V13): closure-sign-is-a-free-BC, a₀=cH(z)/2π instantaneous, G-variation is structurally non-local, the 2 Gyr cross-domain consilience, etc. **Monster #1** = the λ=c·T=613 Mpc cymatic fundamental (KBC/Big Ring/Giant Arc/BAO): tested on BOSS DR12 CMASS (`xi_613_analysis/`, Landy-Szalay, BAO injection ✅, no clean 413 Mpc/h peak but INCONCLUSIVE — cosmic-variance floor ~11% in one volume) → NOT a card (it's a direct OBT prediction, not an external debunk, and not certain); resolution needs replication on DESI/Euclid. **Site/PDF rule for cards:** the GAME never goes on the site; only a CONFIRMED card (an external-theory correction that integrates into OBT) would later become theory content in the 7 sacred files — there are ZERO confirmed cards yet, so nothing to add to the site/PDF now. Method memories: `feedback_bootstrap_search_strategy`, `project_bootstrap_consilience_audit`.
- **Purpose**: seeds a possible future V9.0 on holographic quantum gravity. Status of both seeds: "serious conjecture / metaphysical interpretation, not a result." The bulk_solver is a concrete in-progress calculation, not a seed.
- **Rules**: do NOT pull anything from `explorations/` into the 7 sacred files or the PDF. Do NOT delete the folder. It is deliberately quarantined — V8.2 stays a pure macroscopic phenomenological cosmology paper; V9.0 holographic-QG ideas live here until formally derived and cleared of their gates.

## Downloads
1. **White Paper** (`cosmic_yoyo_v5_holographic.pdf`) — 7 pages, "Resolving Thirty-One Cosmological Anomalies" (LaTeX source: `paper/cosmic_yoyo_prl.tex`)
2. **Full Theory** (`oscillating_brane_theory_latest.pdf`) — ~100+ pages, 7 chapters + Appendix A (~1.9 MB compressed)
3. **Full Theory (Markdown)** (`oscillating_brane_theory_latest.md.txt`) — same content as PDF, AI/text-parser friendly, downloadable from site

## Computational Validation Results (March 2026)
| Validation | Method | Key Result |
|-----------|--------|------------|
| w(z) phantom crossing | BDF stiff solver, exact lookback time | w ∈ [-1.003, -0.997], matches DESI DR2 |
| S₈ tension (consistency) | ODE D₊(a) with BKM-derived G_eff(t) | order 4–10% suppression (S₈≈0.79), δ_bulk=1.36 rad derived; value waveform-dependent, NOT ±0.002 (audit May 2026) |
| Bayesian evidence | dynesty nested sampling, 500 live points | Original 3-param: Δln K ∈ [2.8, 4.13]. After T promotion: Δln K ≈ 5.8 (Decisive, prior-independent) |
| SKA 21cm prediction | Reionization mock, z=6-15 | 5.46 mK peak, SNR = 5.5σ |
| Lithium-7 problem | BBN conformal tolerance, BDF solver | 3.5× suppression, D/⁴He preserved |
| Baryon asymmetry | Spontaneous QCD baryogenesis | η_B = 6.1×10⁻¹⁰, c_QCD = O(1), no fine-tuning |
| Big Ring / Giant Arc | Chladni resonance nodes | Peaks at ~816 Mpc and ~2041 Mpc (> ΛCDM 370 Mpc) |
| CMB birefringence | 5D geometric Chern-Simons | Δβ = 0.250°, c_top = 75 (natural), no fine-tuning |
| Hubble 43 anomalies | ER=EPR topological scarring | Disk → hazy blob (7.4× expansion), no SMBH |
| Dark flow unification | 5D kinematic brane drift | v_bulk = 300 km/s → δH/H = 10⁻³ AND Δβ = 0.25° |
| qBOUNCE level shift (DEMOTED May 2026) | Airy wavefunctions + Yukawa overlap (audited, injection-tested) | δE/E~2×10⁻⁸ (α=−0.005) to ~10⁻⁶ (natural α~O(1)), ≪10⁻⁴ GRS → consistency check. "55× amplification" was a category error |
| 5D Geometric Bypass | Levitated nanosphere + Yukawa Hamiltonian | 0.4% enhancement at r=L, commuting operators bypass Heisenberg |
| Airy-Yukawa matrix element | Perturbative series O(α⁶) + contour integral | ⟨1\|δV\|6⟩ = -2V₀(L/z₀)³, 5 decimal convergence (0.97460) |
| Yukawa-Robin mapping | Closed-form λ_n(L) from von Neumann isomorphism | λ_n = (mg/2V₀)(z₀/L)³[1+4ε_n(L/z₀)²], splitting 3.1% in shape only (amplitude unobservable) |
| Limit cycle uniqueness | Liouville-Filippov trace formula (analytical) | κ = e^{-4.74} ≈ 8.7×10⁻³ (contraction ×115, double-count corrected) |
| Non-autonomous persistence | Fenichel-Neishtadt spectral gap | \|λ_trans\|/ε ≈ 17, NHIC survives Hubble drift |
| KK branching ratio | Phase space summation + Filippov shock | B ≈ 9.7×10⁻¹¹ (83M KK modes = AdS₅ heat sink) |
| KK mass spectrum | Transcendental Bessel quantization (3 sectors) | Graviton: m_n/k = {1.892, 3.692, 5.510...}, gap ≈ 1.87 eV |
| KS naturalness | Flux integers K=21, M=10, g_s=0.1 | τ₀^{1/3} = M_Pl·e^{-2πK/(3g_sM)} = 257 MeV, zero fine-tuning |
| Fourier stick-slip | Analytical integration of asymmetric sawtooth | A₂/A₁=47.6%, A₃/A₁=29.3%, slip low-pass at n≈5 |
| DESI LRG3 aliasing | Phase mapping of tomographic bins | z=0.93 at phase 82.8% — phantom crossing = geometric shock |
| S₈ ODE | Growth factor D₊(a) with BKM-derived G_eff | suppression order 4–10% (waveform-dependent), δ_bulk=1.36 rad derived; not a ±0.002 precision figure |
| eROSITA non-linear [SUPERSEDED→T3] | Press-Schechter with oscillating δ_c(t) | Mechanism illustration only; γ=1.19 NOT a confirmation (eROSITA high-S8) nor discriminant (f(R) not universal); sign is a free bulk BC (audit May 2026) |
| MOND ab initio | Gibbons-Hawking + Unruh + 5D quadrature | a₀=cH₀/2π, μ(x)=x/√(1+x²), cluster resonance at T=2 Gyr |
| Seeley-DeWitt numerical | V8.2 parameters (k=0.987 eV, kL=1, N_dof=6) | ā₀-ā₅ table, a₅_bulk≡0, **ā₅(UV)=2.845 eV⁴, ā₅(IR)=0.0521 eV⁴** (98.2% UV-confined) |
| Dirichlet anomaly resolution | 4-branch holographic tensor (Ai=c₁f-c₂g) | Δ=0.000044 (2.1%), O(α⁴), destructive interference exact |
| LVS explicit minimization | V_LVS(τ_large, τ_small) analytical | τ_s=3.65, W₀≈3030, both eigenvalues positive (stable) |
| Multi-throat architecture | V_min vs QCD uplift energy comparison | 45-order gap proves multi-throat necessity (geometric theorem) |
| LVS mass spectrum | Hessian eigenvalues at minimum | M_s≈1.19×10¹² GeV, m_{3/2}≈1.75×10⁹ GeV, LHC null predicted |
| Full 3D Floquet | Non-autonomous monodromy without adiabatic projection | ε₀=4.30, margin ×30, Neishtadt 2nd order: residual ≤2% |
| Dynamical Schwinger | Filippov shock kinematics (v_max=0.05c) | Exponent 10³¹→10⁹, exp(-7.2×10⁹)≡0, N_total≡0 per cycle |
| Finite-N Dirac collapse | Expander graph spectra + Cheeger inequality | σ₁/L~10⁻³⁸·⁵, N_min≈4500, ω₀ correction ~10⁻⁷⁶, RT survives |
| Kinematic Blockade | 5D Bondi flux for continuous membrane | Γ_rad^{5D-GR}≡0, m₁T_slip~3.6×10³¹, exp(-3.6×10³¹)=0. Proves PBH necessity |
| NANOGrav spectral flattening | Tensor TT projection of Filippov shock | φ̈ = Dirac δ → flat spectrum, n_PTA ≈ 10⁹, h_c(16 nHz) ~ 10⁻¹⁵ |
| AdS₅ viscoelastic retardation | BKM Averaging Theorem (analytically derived) | δ_BKM=1.36 rad (derived, solid); S₈ suppression order 4–10% (waveform-dependent, not ±0.002) |
| Press-Schechter γ(M) | Non-linear spherical collapse + oscillating δ_c | A(M)≈ν²/ln(Ω_m⁻¹), γ(groups)≈0.88, γ(clusters)≈1.19, γ(monsters)≈1.47 |
| MOND sinc theorem | Orbital averaging of oscillating a₀(t) | sinc(πt_dyn/T): dwarfs 0.996, spirals 0.981, groups 0.637, clusters 0.000 |
| ΔBIC (current + forecast) | Anchored stick-slip (k=1) vs CPL (k=2) | DR2: ΔBIC≈-6.4 (Strong), Y5 forecast: ΔBIC≈-22 (Decisive) |
| Analytical Fisher 3×3 | DESI+Planck ISW+DES Y6 Jacobian | σ(T)/T=6.7%, σ(L)/L=15%, τ₀-L anti-corr r=-0.76, QCD 0.11σ |
| KdF 4-branch exact | All 4 Kampé de Fériet tensors to O(N=10) | Δ=0.000044 (6 sig figs), O(α⁴) scaling, shadow peak at z≈2L, Δ_{1,m} non-monotone |
| Kesten-McKay + percolation | ER=EPR graph spectra + site percolation | Continuum O(1/√N)~10⁻¹⁰, p_c≈2.2%, 98% destruction resilience, 19-order safety margin |
| KS landscape scan | Monte Carlo flux pair enumeration | 2,437 valid pairs, f_QCD=0.49% per throat, P_CY=21.8% (1 in 5 CY manifolds host QCD throat) |
| Exact a₅ (S3/P1) | Cubic extrinsic curvature invariants on AdS₅ orbifold | ā₅(UV)=2.845 eV⁴, ā₅(IR)=0.0521 eV⁴, 98.2% UV-confined |
| Exact spectral zeta (S3/P2) | Transcendental Bessel correction to Weyl-McMahon | 2.1% inharmonic shift, δ_phys/Λ_QCD ≪ 10⁻³⁰ (one-loop ~10⁻³⁸, QFT error budget bounded) |
| Continuous γ(M) (S3/P3) | Tinker sensitivity kernel strict monotonicity | f(R)/scalar-tensor exclusion theorem, 4-bin mass grid |
| 3-component Bullet Cluster (S3/P4) | sinc(0.053π)+Weyl offset+cored Σ | MOND 99.5% + 150 kpc Weyl offset, falsifiable vs NFW |
| Ab initio SPARC (S3/P5) | Exact RAR from 5D geometry | 29.3 km/s RMS, 0 free params, 135 galaxies |
| Wide binary γ_g (Chae 2025) — CONTESTED, T2 | γ_g(u)=[(1+√(1+4/u²))/2]^{1/2} closed form | OBT reproduces MOND's γ_g(u) ab initio (1.58-1.80 vs Chae 1.48^{+0.33}_{-0.23}, <1σ IF real). CAVEAT (audit May 2026): the anomaly is DISPUTED — Pittordis-Sutherland/Banik find Newtonian fits better (hidden-triple contamination, unresolved); and γ_g(u) is MOND's boost (OBT inherits, NOT OBT-distinctive). Consistency with one contested analysis, not a decisive validation. **OBT-Game card #1 (June 2026, exploratory cross-check integrated in discoveries.md §3.6)**: a this-work re-analysis of El-Badry 2021 (29112 binaries) finds the deep-MOND excess RUWE-STABLE (median v_sky/v_N 0.92→0.89 as RUWE<1.4→1.05, does NOT collapse to Newton ~0.65) + a Keplerian forward model inconsistent with flat-Newton → disfavors the PURE hidden-triple artifact (debunk of the external triple model, framed within OBT; universality+RUWE are OBT-independent). EXPLORATORY: approximate masses, statistical v-proxy, ~0.13 forward-model baseline offset → does NOT resolve the amplitude controversy; stays T2. Scripts: explorations/probes.py (probe wb_boost, wb_forward). **OBT-Game card #2 (June 2026, discoveries.md §3.7)**: gas-rich UDGs reported "off the BTFR / Newtonian" (Mancera-Piña 2019/2022) are reconciled with OBT μ(x)/BTFR by ONE external mechanism = under-estimated observational uncertainties (inclination and/or distance) in face-on low-SB disks. This-work probe udg_sample: all 6/6 return to the BTFR with lower i (i_true~9-23°, clean for the 4 face-on i_pub≤42; the 2 inclined ones via distance). Independent confirmation: 2024 A&A reanalysis arXiv:2408.05269 (AGC 114905 i=15°, matches round optical image). CONTESTED (Mancera-Piña defend higher i), MOND-shared (not OBT-distinctive), T2. Probe: udg_sample, udg_inclination. **OBT-Game card #3 (June 2026, discoveries.md §3.8)**: declining/Keplerian outer rotation curves do NOT challenge μ(x) — a declining RC is the baryonic curve settling onto the deep-MOND plateau (G M_bar a0)^1/4. This-work probe sparc_decline: 20 SPARC declining-RC galaxies (slope<-1 km/s/kpc) lie on OBT RAR at median residual +0.000 dex, tightest scatter 0.089 (vs flat 0.19, rising 0.22). MW (Jiao 2023 Gaia DR3 decline) reproduced by μ(x) at chi2/N≈0.9 for M_bar~1e11 (probe mw_rotation). Debunks the "MW Keplerian decline challenges modified gravity" framing. SPARC leg solid+OBT-independent; MW leg has baryonic-mass caveat (M_bar high-ish vs ~0.65e11); MOND-shared; T2. Probe: sparc_decline, mw_rotation. **OBT-Game card #4 (June 2026, discoveries.md §3.9)**: NGC 2419 "crucible" (Ibata 2011, claimed to falsify MOND via a steeply declining dispersion) debunked — Ibata assumed ISOTROPY; modest RADIAL anisotropy (r_a~r_eff) steepens the projected μ(x) dispersion decline. This-work probe gc_jeans (anisotropic Jeans in μ(x)): beta-scan steepens the 5→40 pc decline 22%(iso)→46%(β=0.7~Sanders n=10-12 polytrope), reaching the observed; generic (also Pal 14: 10%→34%). HARDENED (June 2026, probe ngc2419_dispersion): built NGC 2419's dispersion profile from the 197 raw stellar RVs myself (Ibata 2011 table3) — 183 members, σ_p 5.6→2.4 km/s over r~14-91 pc = 56% decline, matching anisotropic μ(x) (β~0.7-0.8) NOT isotropic (22%). Card rests on MY data + MY model; Sanders 2012 = corroboration. MOND-shared, T2. Probe: gc_jeans, ngc2419_dispersion. **OBT-Game card #5 — BRIDGE card (June 2026, discoveries.md §3.10)**: first card OUTSIDE galaxy kinematics — extends μ(x) into weak LENSING + cosmic ENVIRONMENT. Brouwer 2021 (KiDS) finds the weak-lensing RAR depends on morphology at ≥6σ (early vs late, Sérsic + u-r colour), claimed to break universal μ(x). Debunked: it's the 2-HALO (environment) term, g_obs=g_1halo[μ(x)]+4G·b·ΔΣ_mm; early-types more clustered (higher bias) → bigger 2-halo at low-g → the split. **COMPLETED (June 2026) with Brouwer's REAL split data** (KiDS data release, probe brouwer_split): I measured the observed early/late RAR split myself from the public ESD profiles (g_obs=4G·ESD_t/bias): Sérsic +0.177±0.027 dex (6.7σ), Colour +0.222±0.028 dex (8.0σ), early/red>late/blue. My 2-halo (probe lensing_2halo, colossus): realistic CENTRAL bias (b 1.06/0.81) → ~0.1 dex = ~HALF; satellite-inclusive effective bias (b~1.5-1.8, early stacks include group/cluster satellites) → ~0.15-0.19 dex = MOST; baryonic branch for the residual. So the environment (2-halo) is the DOMINANT, right-direction driver, magnitude consistent with the data once satellite effective bias is included. 1-halo μ(x) stays universal → the split is environmental, NOT a μ(x) failure. Order-of-magnitude (full HOD+baryon + 2nd survey would pin the residual), MOND-shared, T2. BRIDGE: kinematics→lensing→environment. Probe: lensing_2halo, brouwer_split. **OBT-Game card #6 (June 2026, discoveries.md §3.11)**: debunk Rodrigues et al. 2018 ("Absence of a fundamental acceleration scale" — per-galaxy a0 varies >5σ → no universal a0 → μ(x) falsified). This-work SPARC per-galaxy a0 posteriors (probes sparc_a0_posteriors, sparc_a0_fullbudget): fixing M/L gives chi2/dof=3516 vs a common a0; restoring the full budget Rodrigues froze — M/L (log-normal) + inclination + distance + the INDEPENDENTLY-measured RAR intrinsic scatter (~0.13 dex in g, McGaugh-Lelli, NOT a0 variation) — collapses chi2/dof to ~4 (~880×), per-galaxy a0 MEDIAN = canonical universal value (1.07-1.25e-10), 77% within 2σ. NON-CIRCULAR (reconciling σ_int = measured RAR scatter). Residual chi2/dof~4 (not 1) approximation-limited (3-pt grids/Gaussian posteriors; full MCMC reaches ~1). MOND-shared, T2. Probe: sparc_a0_posteriors, sparc_a0_fullbudget. **OBT-Game card #7 — FIRST OBT-DISTINCTIVE card (June 2026, discoveries.md §3.12 + predictions.md §6)**: debunks "a0 is a universal CONSTANT" (Milgrom). OBT WHY: a0=cH(z)/2π (Gibbons-Hawking horizon temperature) → a0 EVOLVES with z. MUSE-DARK III 2026 (arXiv:2604.22613) measures RAR a0 rising 1.0→1.99→2.38→2.71e-10 at z~0,0.5,0.9,1.2 → constant-a0 MOND REFUTED, OBT's evolving-a0 confirmed in DIRECTION+factor (E(z)~3 to z=2). NOT MOND-shared (a0(z) is OBT's horizon signature) → first card distinguishing OBT from MOND. HONEST: observed rate ~30-45% steeper than cH(z)/2π ("a0 faster than H(z)"); per rule#1 attributed to high-z baryonic/measurement systematics (a0 horizon-fixed), so direction is the robust result, rate is a calibration question. T2. inline a0(z) check |
| Multi-harmonic sinc (S3/P6) | Fourier averaging with asymmetric waveform | W_exact(1)≡0 (topological), group extinction from n=2 harmonic |
| Non-perturbative steepest descent (S3/P7) | Instanton action for KS flux transition | S_inst≈2122, tunneling ~10⁻⁹²¹, Borel-summable |
| Graph Laplacian determinant (S3/P8) | Kirchhoff + Kesten-McKay closed form | I_KM(46)=3.8175, δω/ω₀≈10⁻⁷⁶ |
| Exact RT finite-N (S3/P9) | Friedman spectral gap + percolation shift | λ₁≈0.708, p_c(N) shift 10⁻⁷, P_fail~10⁻¹⁰²¹ |
| Popperian Falsifiability Shield (honest tiering, audit May 2026) | NOT 6 uniform pillars — tiered by strength | (B) GL microlensing cliff = ONLY genuinely distinctive/testable (caveat: optically degenerate with wave-optics edge); (A) Bullet offset + (F) no-spike = consistency checks shared with ΛCDM; (C) femtolensing = speculative (finite-source washout, Katz 2018); (D) dynamical heating = empty (~10¹³ below threshold at asteroid mass, null=ΛCDM); (E) astrometric = unobservable (8 orders below Gaia) + non-distinctive. Distinctive falsifiability rests on (B); eROSITA γ(M) — once billed as the strongest prediction outside the shield — is itself DEMOTED to T3 (May 2026); distinctive future test = SKA 21cm. EM silence (G_KK→γγ NIR + PBH X-ray darkness) = mundane/unfalsifiable consistency, not pillars |

## IMPORTANT: Laboratory Chapter Terminology
- **NEVER say "violating Heisenberg"** — say "Orthogonal Geometric Bypass" (5D metric operators commute with 4D gauge operators)
- **NEVER use "Strip Theory" or "sidetime"** — use "5D Radion-Coupled Lindblad Master Equation" (Diósi-Penrose framework)
- **Target = mesoscopic quantum states** (BEC, macromolecules ~10⁹ amu), NOT single atoms
- **qBOUNCE** = experiment at ILL Grenoble (PI: Hartmut Abele, TU Wien; Tobias Jenke, ILL). Collaboration opportunity for validating L = 0.2 μm

## V8.2 Computational Scripts
| Script | Purpose | Output |
|--------|---------|--------|
| `scripts/brane_dynamics.py` | Core V8.2 ODE (BDF stiff solver, w(z) oscillation) | `plots/w_z_oscillation.png` |
| `scripts/growth_factor.py` | Ab initio S₈ with BKM-derived δ_bulk (zero calibration) | `plots/s8_yukawa_suppression.png` |
| `scripts/bayesian_analysis.py` | Nested sampling Bayesian evidence (dynesty) | `plots/nested_sampling_posteriors.png` |
| `scripts/ska_21cm_mock.py` | SKA 21cm reionization modulation prediction | `plots/ska_prediction.png` |
| `scripts/lithium_bbn_solver.py` | Lithium-7 BBN conformal tolerance | `plots/lithium_resolution.png` |
| `scripts/spontaneous_baryogenesis.py` | QCD baryogenesis (radion = dynamic θ_QCD) | `plots/baryon_asymmetry.png` |
| `scripts/ultra_large_structures.py` | Big Ring / Giant Arc resonance | `plots/big_ring_resonance.png` |
| `scripts/cmb_birefringence.py` | CMB birefringence (5D geometric, c_top=75) | `plots/cmb_birefringence.png` |
| `scripts/chladni_nodes.py` | Chladni mega-structure standing waves | `plots/chladni_mega_structures.png` |
| `scripts/er_epr_scarring.py` | ER=EPR topological scarring (Hubble 43) | `plots/hubble_scar_morphology.png` |
| `scripts/kinematic_brane_drift.py` | 5D drift unification (dark flow + birefringence) | `plots/drift_unification.png` |
| `scripts/radion_attractor.py` | Dynamical attractor demonstration | `plots/radion_attractor_*.png` |
| `scripts/pbh_emf_constraints.py` | PBH EMF vs microlensing (wave-optics) | `plots/pbh_emf_constraints.png` |
| `scripts/gregory_laflamme_hierarchy.py` | GL perforation hierarchy (M_crit, 5D vs 4D) | `plots/gregory_laflamme_*.png` |
| `scripts/bbn_thermal_freezeout.py` | BBN via conformal symmetry & trace anomaly | `plots/bbn_thermal_freezeout.png` |
| `scripts/growth_scale_dependent.py` | Scale-dependent S₈ Yukawa (legacy) | `plots/growth_scale_dependent.png` |
| `scripts/numerical_relativity_1d.py` | 5D radiative damping (1+1)D MoL | `plots/warped_shielding_1D.png` |
| `scripts/qbounce_yukawa_lambda.py` | qBOUNCE Robin parameter from Yukawa | `plots/qbounce_lambda_prediction.png` |
| `scripts/qbounce_airy_yukawa.py` | Ab initio Airy-Yukawa matrix elements (97.5% analytical) | `plots/qbounce_airy_yukawa.png` |
| `scripts/lyapunov_mle.py` | Phase portrait + MLE computation (orbital stability) | `plots/lyapunov_mle.png`, `plots/lyapunov_phase_portrait.png` |
| `scripts/fisher_jacobian.py` | Numerical Jacobian (mock ODE), SVD, Fisher proxy | `plots/fisher_jacobian.png` |
| `scripts/fisher_jacobian_real.py` | Numerical Jacobian (REAL ODE via lyapunov_mle), find_peaks | `plots/fisher_jacobian_real.png` |
| `scripts/fisher_forecast.py` | Multi-probe Fisher forecast (Planck+DESI+Euclid+SKA+PTA) | `plots/fisher_forecast.png` |
| `scripts/obt_v82_likelihood.py` | Cobaya MCMC likelihood (BDF stiff ODE at each step) | N/A (inference engine) |
| `scripts/obt_v82_mcmc.yaml` | Cobaya YAML config (mock data, priors, R-1<0.01) | `chains/obt_v82` |
| `scripts/obt_desi_planck.yaml` | PRODUCTION Cobaya (DESI DR2 + Planck ISW + DES Y6) | `chains_real/obt_v82_production` |
| `scripts/plot_mcmc_results.py` | GetDist triangle plot from converged chains | `plots/obt_v82_corner_plot.pdf` |
| `scripts/verify_casimir_regularization.py` | UV catastrophe demo + zeta-regularized Casimir verification | `plots/casimir_regularization.png` |
| `scripts/laplace_demon_hamiltonian.py` | 5D Geometric Bypass Hamiltonian | `plots/laplace_demon_readout.png` |
| `scripts/ks_landscape_scan.py` | KS landscape statistics (Monte Carlo 2437 flux pairs) | `plots/ks_landscape_distribution.png` |

## MathJax — DO NOT TOUCH
- MathJax 3 is configured in `_layouts/dark.html` with inline math `$...$` and display math `$$...$$`
- **It works. Do NOT replace LaTeX with plain text** (e.g., do NOT change `$\lambda$` to "Lambda")
- **Do NOT remove or modify the MathJax config block** in `_layouts/dark.html`
- LaTeX renders correctly on ALL site pages and in the PDF (xelatex handles it natively)
- **PDF pipeline pre-processor** (`generate_pdf.py`) sanitizes Unicode→LaTeX, converts HTML tables→markdown, strips Jekyll templates, emojis, and fixes indented headers before pandoc
- The `\vert` workaround applies to ALL absolute values and norms in inline math, not just bra-kets. kramdown interprets `|` as table pipe in inline `$...$`. ALWAYS use `$\vert x\vert$` instead of `$|x|$` for any variable (φ, λ, χ, ψ, etc.). Display math `$$...$$` is safe.
- **LaTeX prime notation** — NEVER write `\text{Ai}'` or `\operatorname{Ai}'` in .md files — the prime character crashes both pdflatex and xelatex. Use `{\text{Ai}}^{\prime}` in display math or `\partial_x\text{Ai}` in inline math instead. Also applies to derivatives like `D_+'(a)` — must write `D_+^{\prime}(a)` in display math formulas.
- **scipy `ai_zeros` return order** — `ai_zeros(N)` returns `(a, ap, ai, aip)` where the normalization constant Ai'(a_n) is in the **4th return** `aip`, NOT the 3rd `ai`. Always unpack as: `a_zeros, _, _, deriv_at_zeros = ai_zeros(N)`.

## CI / Code Quality
- **black + isort**: All scripts must pass `black --check scripts/` and `isort --check-only scripts/`
- After adding/modifying any `.py` file: run `black scripts/*.py && isort scripts/*.py` before commit
- CI job `test` will fail if formatting is wrong — does not affect PDF or site deployment
- **NEVER pin black to an exact version** in ci.yml (e.g., `black==26.3.1`) — it breaks when CI uses a different Python version. Just use `black` (latest).

## TODO: Visual Page & Video Expansion
### Phase 1: visual.md (PDF embeds)
- Create `visual.md` (non-PDF site page, excluded from `generate_pdf.py`)
- 17 discovery PDFs (EN) + 3 prediction PDFs (EN) = 20 iframe embeds
- File convention: `assets/pdf/discovery_XX_slug.pdf`, `assets/pdf/prediction_XX_slug.pdf`
- User will provide a single PDF with all PowerPoint images first, then individual files
- Same titles/descriptions as corresponding videos
- FR versions later

### Phase 2: videos.md expansion
- Current: 6 discovery + 3 prediction = 9 videos (EN+FR)
- Target: 17 discoveries × 2 langs + 3 predictions × 2 langs = 40 videos total
- User will provide additional YouTube links when ready

### Phase 3: FR visual PDFs
- Add FR versions of all 20 visual PDFs once available

## ACTION PLAN: Scripts to Execute and Their Consequences

### PRIORITY 1 — Production MCMC (the Big Test)
**Script**: `mpirun -n 4 cobaya-run scripts/obt_desi_planck.yaml -f`
**Requires**: Cobaya + mpi4py installed (`pip install cobaya mpi4py`)
**Duration**: ~2.8h wall-clock on 4 cores
**What it produces**: Converged MCMC chains with τ₀, T, L posteriors against REAL DESI+Planck+DES data
**Post-process**: `python scripts/plot_mcmc_results.py` → triangle plot for arXiv
**Consequence for theory**: If R-1 < 0.01 converges with τ₀^{1/3} ≈ 257 MeV and n_σ < 2 vs FLAG → **the QCD-cosmology unification is statistically proven**. If it diverges → we learn which parameter tension breaks the model.

### PRIORITY 2 — Fisher Jacobian on Real ODE
**Script**: `python scripts/fisher_jacobian_real.py`
**Duration**: ~5 min (7 ODE integrations)
**What it produces**: True sensitivity matrix from Filippov dynamics, SVD, condition number
**Result already obtained**: T column = 0 (attractor autonomy confirmed). τ₀ and L are the only true DOF.
**Consequence**: Independently confirms the 2-parameter paradigm (now also proven by chronological anchoring: T=13.80/6.9=2.000 Gyr eigenvalue).

### PRIORITY 3 — Casimir Verification
**Script**: `python scripts/verify_casimir_regularization.py`
**Duration**: ~1 sec
**Already run**: Bare sum ~10⁶ eV⁴ (UV catastrophe), regularized ~10⁻⁴ eV⁴ (matches formula)
**Consequence**: Confirms δ_phys/Λ_QCD ≪ 10⁻³⁰ numerically → quantum stability is absolute (one-loop ~10⁻³⁸, bounded by QFT error budget).

### PRIORITY 4 — All Existing Validation Scripts (re-run for fresh plots)
Run all scripts to regenerate plots for the latest version:
```bash
python scripts/brane_dynamics.py
python scripts/growth_factor.py
python scripts/bayesian_analysis.py
python scripts/ska_21cm_mock.py
python scripts/lithium_bbn_solver.py
python scripts/spontaneous_baryogenesis.py
python scripts/ultra_large_structures.py
python scripts/cmb_birefringence.py
python scripts/chladni_nodes.py
python scripts/er_epr_scarring.py
python scripts/kinematic_brane_drift.py
python scripts/radion_attractor.py
python scripts/pbh_emf_constraints.py
python scripts/gregory_laflamme_hierarchy.py
python scripts/bbn_thermal_freezeout.py
python scripts/numerical_relativity_1d.py
python scripts/qbounce_yukawa_lambda.py
python scripts/qbounce_airy_yukawa.py
python scripts/lyapunov_mle.py
python scripts/fisher_jacobian.py
python scripts/fisher_forecast.py
python scripts/laplace_demon_hamiltonian.py
python scripts/ks_landscape_scan.py
```

### OPEN MATHEMATICAL WORK (0 items remaining — ALL COMPLETE)
All 60 mathematical derivations have been completed and integrated into theory.md + predictions.md (March 2026):
- **33 original derivations** (V8.2 core): Filippov-Banach, Fenichel, Γ_rad ab initio, KK spectrum, spectral zeta, Seeley-DeWitt, Skenderis, MERA/HaPPY, OTOCs, Dirac collapse, Kampé de Fériet, Dyson horizon, KS UV completion, Swiss-Cheese LVS, No-Go isotrope, KKLT tadpole, Fisher Jacobian/forecast, Cobaya module, Robin mapping, Airy-Yukawa series
- **9 DeepThink Series 1** (March 2026): (1) Fourier stick-slip spectrum, (2) exact S₈ ODE + eROSITA non-linear, (3) MOND ab initio from 5D, (4) Seeley-DeWitt numerical evaluation, (5) Dirichlet anomaly 4-branch resolution, (6) full 3D Floquet without adiabatic projection, (7) LVS minimization + multi-throat, (8) dynamical Schwinger invulnerability, (9) finite-N corrections to Dirac collapse
- **9 DeepThink Series 2** (March 2026): (1) Kinematic Blockade (Γ_rad^{5D-GR}≡0, PBH necessity proof), (2) NANOGrav spectral flattening (n≈10⁹ overtone, h_c~10⁻¹⁵), (3) AdS₅ viscoelastic retardation (dual-damping arctan δ_bulk=1.30 rad), (4) Press-Schechter γ(M) spectrum (mass-dependent eROSITA), (5) MOND sinc theorem (orbital averaging, cluster resonance), (6) ΔBIC forecast (DR2: -6.4 Strong, Y5: -22 Decisive — updated after chronological anchoring k=1), (7) Analytical Fisher 3×3 (QCD 0.11σ), (8) KdF 4-branch exact tensor (holographic shadow), (9) Kesten-McKay percolation immunity (98% destruction resilience)
- **9 DeepThink Series 3** (March 2026 — Mathematical Completion): (1) Exact a₅ Seeley-DeWitt (ā₅(UV)=2.845 eV⁴, ā₅(IR)=0.0521 eV⁴, 98.2% UV-confined), (2) Exact spectral zeta ζ_Δ(-1/2) from transcendental Bessel roots (2.1% inharmonic shift, δ_phys/Λ_QCD ≪ 10⁻³⁰), (3) Continuous γ(M) spectrum (Tinker kernel A(ν)=cν²+a/(1+(ν/b)^a), strict monotonicity, f(R) exclusion theorem), (4) 3-component Bullet Cluster (MOND sinc(0.053π)≈0.995 + Weyl offset 150 kpc + cored Σ profile), (5) Ab initio SPARC rotation curves (29.3 km/s, 0 params, exact RAR formula), (6) Multi-harmonic sinc topological protection (W_exact(1)≡0, group-scale W≈0.54 from n=2 harmonic extinction), (7) Non-perturbative steepest descent (S_inst=1/(12α³)≈2122, tunneling 10⁻⁹²¹, Borel-summable), (8) Graph Laplacian functional determinant (Kirchhoff + Kesten-McKay closed form I_KM(46)=3.8175, δω/ω₀≈10⁻⁷⁶), (9) Exact RT phase boundary at finite-N (Friedman λ₁≈0.708, p_c(N) shift 10⁻⁷, P_fail~10⁻¹⁰²¹)

### DEEPTHINK SERIES 4 TODO — Tier 3 → Tier 2 Promotion (11 prompts)
**Goal:** Promote the 11 qualitative Tier 3 anomalies to Tier 2 (analytical framework) or Tier 1 (exact) via dedicated DeepThink derivations. No 5D NR simulation needed — all are analytical/semi-analytical calculations.

| # | Anomaly | Current Tier | Calculation needed | Difficulty |
|---|---------|:---:|---|:---:|
| P1 | **Hubble tension** | T3 | Cepheid luminosity with oscillating G_eff(t): L∝G⁷M⁵, cumulative δH₀ over 7 cycles | Medium |
| P2 | **Cosmic dipole** | T3 | 5D drift vector projection onto 4D brane: δH/H = v_drift·n̂/c, angular power spectrum | Medium |
| P3 | **KBC Void** | T3→T2 | Density profile from cymatic standing wave: δρ/ρ(r) from λ=cT=613 Mpc mode | Easy |
| P4 | **Quasar alignment** | T3 | Weyl shear tensor E_μν along filaments: quadrupolar torque on BH spin axes | Hard |
| P5 | **Dark Flow** | T3 | Inertial drag force on clusters from brane drift: F_drag(M, v_bulk) | Medium |
| P6 | **Space Roar** | T3 | Cumulative synchrotron spectrum from 7 stick-slip shocks: T_radio(ν) power law | Medium |
| P7 | **ORCs** | T3 | Spherical shock profile from PBH node relaxation: R(t), B-field amplification | Hard |
| P8 | **Methuselah star** | T3→T2 | Already have ×1.105 factor. Need: stellar evolution with periodic G_eff(t) | Easy |
| P9 | **WD Q-branch** | T3 | Thermo-gravitational PdV pumping rate: dE/dt in degenerate core with G_eff(t) | Medium |
| P10 | **Planet 9 illusion** | T3 | MOND-EFE secular torque on ETNOs: orbital integration with a₀ + galactic EFE | Medium |
| P11 | **Flyby anomaly** | T3 | Hyperbolic trajectory in 5D drift vortex: ΔV(inclination) from Lense-Thirring | Hard |

**Priority order:** P3, P8 (almost done) → P1, P6, P9 (medium, high impact) → P2, P5, P10 (medium) → P4, P7, P11 (hard, lower priority)

**Expected outcome:** 60 + 11 = 71 derivations. Tier breakdown: T1=5, T2=26, T3=0 (all promoted).

### SITE & INFRASTRUCTURE TODO
- Visual page (visual.md) with PDF embeds — waiting for user's PowerPoint PDF
- Videos.md expansion to 40 videos — waiting for user's YouTube links
- Google OAuth: pass from test to production mode (needs Google review)
- Optimize Romain AI system prompt (ongoing tuning)
- Update Romain AI knowledge base with latest .md.txt (theory.md is now ~2300+ lines after 27 DeepThink prompts (S1+S2+S3) + epistemological hardening)
- Plot display in chat: works via `files` event + URL serving (NPM `/sandbox-images/`)

## Site Structure (Jekyll + GitHub Pages)
- **Layout**: `_layouts/dark.html` — two-column grid (45% text left, 55% video right)
- **Navigation**: defined in `_config.yml` (navigation array), rendered in `dark.html` lines 46-60
- **Video carousel**: 6 videos in `.video-column` (right side), sticky, scroll-synced to text via `assets/js/video-carousel.js`
- **CSS**: `assets/css/dark-theme.css` — dark theme, fixed header with blur, responsive (mobile hides video column)
- **Mobile**: single column, hamburger menu (`.mobile-nav`), video hidden
- **Section markers**: `<div class="section-marker" data-section="...">` in content triggers video switching via IntersectionObserver
- **Romain AI toggle**: "Romain AI" button in nav swaps `.video-column` between video carousel and Open WebUI iframe. State persists across page navigation via `sessionStorage` (resets on new tab/visit). Auth state also cached — no re-auth on page change. Iframe URL uses cache-buster (`?_=timestamp`) to avoid stale SvelteKit assets.
- **Non-PDF pages**: about.md, downloads.md, research.md, refutation.md, videos.md, agent.md (if created). Note: index.md is in the PDF as Ch 1 intro.

## Agent Infrastructure (Romain AI)
- **URL**: https://agent.higgs-cosmology.com
- **VM**: Debian 12 (kernel 6.1.0-44 stock), 4 CPU, 8 GB RAM, 48 GB disk — IP: 51.254.22.29
- **Stack**: Open WebUI v0.8.11 on host (venv: `/opt/open-webui-host/venv/`) + NPM in Docker + gVisor on host
- **Systemd service**: `open-webui.service` (port 8081), env in `/opt/open-webui-host/.env`
- **Data**: `/opt/open-webui-host/data/webui.db` (copied from Docker volume)
- **Old Docker container**: `cosmic-yoyo-agent` stopped, `restart: "no"` — kept as backup, does NOT start at boot
- **ALWAYS use venv for Python installs, NEVER --break-system-packages**
- **LLM**: Kimi K2.5 via Ollama Cloud (96.1% AIME, 87.6% GPQA, +20% agentic boost, thinking mode, fast)
- **Auth**: GitHub OAuth + Google OAuth (SSO), admin = Romain's account
- **Model**: Custom "Romain" model (kimi-k2.5) with system prompt + knowledge base (.md.txt)
- **Site integration**: iframe in `.video-column` toggled by "Romain AI" nav button
- **Config**: `/opt/cosmic-yoyo-agent/docker-compose.yml`
- **Secrets**: `.env` (gitignored) — Ollama token, GitHub OAuth, Google OAuth
- **SSL**: Let's Encrypt via NPM, domain: agent.higgs-cosmology.com
- **NEVER modify the VM docker-compose without explicit user approval**

### Code Execution Sandbox (gVisor)
- **Engine**: gVisor (`runsc`) in rootless mode with `--directfs=false --network=host`
- **Tool**: Community `run_code` tool (patched), stored in `webui.db` table `tool` (id: `run_code`)
- **Local copy**: `run_code.json` (original), `/tmp/run_code_original.py` (extracted for editing)
- **Key patch**: Removed `unshare --map-user=1000` inside gVisor (caused nested user namespace failure). Process runs as uid 0 (fake root in user namespace), gVisor provides full isolation
- **Packages**: numpy, scipy, matplotlib installed in venv
- **Image pipeline**: `plt.savefig('result.png')` in sandbox → `cp *.png /sandbox/` (gVisor bash cmd) → copy to `/opt/open-webui-host/data/sandbox-images/{uuid}.png` → served by NPM at `https://agent.higgs-cosmology.com/sandbox-images/{uuid}.png` → `emitter._emit("files", ...)` displays in chat
- **Cleanup**: Cron daily at 08:00 Paris (23:00 US Pacific), deletes images > 24h
- **Deploy workflow**: Edit `/tmp/run_code_original.py` → repack JSON → `scp` to VM → `UPDATE tool SET content=... WHERE id='run_code'` in SQLite → `systemctl restart open-webui`
- **Model prompt rules**: Uses calibrated V8.2 formulas only (`lambda(z) = lambda_ref * exp((z_ref - z) / L)`), refuses to recalculate from Airy functions, respects BANNED concepts list

## Human-AI Collaboration
Romain = conceptual architect (Faraday). AI = mathematical co-processors (Maxwell). Radically transparent acknowledgments. Never minimize AI involvement.

## Contact
- provencal.romain@teleadmin.net
- https://github.com/Teleadmin-ai/oscillating-brane-DM/issues
