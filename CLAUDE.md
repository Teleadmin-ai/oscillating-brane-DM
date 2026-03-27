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
1. `discoveries.md` — 31 anomalies resolved (22 core + 9 extended phenomenology)
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

**Breaking these rules causes data loss and inconsistency between the site and the PDF.**

## Project Overview
**Oscillating Brane Cosmology V8.2 (Hybrid Topology Edition)** - The universe is a vibrating 4D membrane in 5D AdS space, driven by a hybrid stick-slip motor: macroscopic Cosmic Web forcing via Israel junction conditions (the muscle) + microscopic ER=EPR-entangled PBH network for quantum synchronization (the metronome). Gregory-Laflamme instability provides an ab initio derivation of the PBH mass window.

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
- **Connectivity**: ER=EPR wormhole network (Maldacena & Susskind 2013)
- **Oscillation ODE** (hybrid stick-slip, NOT harmonic):
  `φ̈ + (3H + Γ_rad)φ̇ + ξRφ + ∂V_GW/∂φ = F_web[E_μν]·(1-3w) - R_PBH(φ,φ̇)Θ(|φ|-φ_crit)`
  - **F_web[E_μν] (the Muscle)**: Macroscopic forcing from the Cosmic Web. Superclusters, filaments, and voids create inhomogeneous stress S_μν on the brane. Via Israel junction conditions ΔK_μν = -κ₅²(S_μν - ⅓S h_μν), this generates the projected Weyl tensor E_μν — a continuous 5D tidal force pressing the brane toward the bulk
  - **R_PBH·Θ (the Metronome)**: Microscopic release orchestrated by the ER=EPR-entangled network of asteroid-mass PBHs. When φ reaches φ_crit, the holographic wormhole network releases tension simultaneously everywhere (ℓ=0 mode) — quantum synchronization
  - **(3H + Γ_rad)φ̇**: Hubble friction + radiative damping via bulk graviton emission (KK modes) during slip phase
  - **ξRφ**: Non-minimal coupling → dynamical attractor locking T = 2 Gyr
  - **(1-3w)**: Trace coupling. = 0 for radiation (conformal symmetry, BBN safe), = 1 after QCD (trace anomaly, motor ON)
- **BBN protection**: Via **conformal symmetry** (T^μ_μ = 0 for radiation w=1/3). QCD chiral symmetry breaking ignites motor at Λ_QCD = 257 MeV
- **5D stability**: **Radiative damping** via bulk graviton emission during slip phase caps amplitude
- **Period stability (anti-chirp)**: ξRφ non-minimal coupling acts as **geometric Phase-Locked Loop**. Three competing decays (Hubble friction ↓, Cosmic Web forcing ↓, curvature feedback ↓) cancel on attractor manifold. |dT/T| < 10⁻³ per Hubble time. Van der Pol oscillator analogy.
- **PBH wave-optics immunity**: For M ~ 10⁻¹² M☉, r_s ≈ 3 nm ≪ λ_opt ≈ 600 nm. Fresnel parameter w_F = 2πr_s/λ ≈ 0.03 ≪ 1. Subaru-HSC is physically blind (deep wave-optics regime). Micro-PBH capillaries rehabilitated
- **Dark energy**: w(z) = -1 + Σ A_n sin(2πn t_lb/T + φ_n) — exact Fourier decomposition of stick-slip sawtooth (not just fundamental). A₂/A₁=47.6%, A₃/A₁=29.3%. DESI's "phantom crossing" is aliasing of geometric shock at z≈0.93 (phase 82.8%, just before QCD cliff). ΔBIC ≈ -5 to -8 vs CPL.
- **S₈ suppression**: Exact ODE integration: S₈ = 0.836 × 0.9521 = **0.796** (4.79% suppression). Geometric dephasing φ_eff ≈ 4.24 rad between scalar w(z) (φ₀=π/2) and tensor G_eff (Israel junction). eROSITA γ=1.19 via non-linear Press-Schechter resonance (not linear growth).
- **ISW resonance**: CMB ℓ = 10-20, Δχ² = 32.9 (6σ)
- **Anchors**: Micro-PBHs with **extended log-normal mass function** (10⁻¹⁴ to 10⁻¹⁰ M☉). Dual role: topological capillaries AND quantum synchronization nodes (ER=EPR)
- **Laboratory tests**: qBOUNCE (ultra-cold quantum neutrons, ILL) + levitated nanoscale optomechanics. Bypass Casimir at sub-micron scale

### Epistemological Framework:
- **31 anomalies resolved** (numerically validated, no fine-tuning):
  - 3 core: DESI phantom crossing, S₈ tension (time-dependent growth suppression), Planck ISW (Δχ²=32.9)
  - 8 established: neutrino masses, DM invisibility (LZ), emergent MOND (ab initio: a₀=cH₀/2π from Gibbons-Hawking thermodynamics, μ(x)=x/√(1+x²) from 5D geometric tilt, cluster failure via 2 Gyr resonance; SPARC 135 galaxies: RMS 29.3 km/s, 0 free params vs NFW 35.0 km/s, 270 params), JWST early galaxies, early SMBHs, cosmological constant, cosmic dipole, Hubble tension
  - 4 validated connections: Lithium-7 (BBN conformal tolerance), baryon asymmetry (spontaneous QCD baryogenesis, c_QCD=O(1)), Big Ring/Giant Arc (Chladni resonance), CMB birefringence (5D geometric Chern-Simons, c_top=75)
  - 3 astrophysical signatures: Hubble's 43 anomalous objects (ER=EPR topological scarring), dark flow unification (v_bulk=300 km/s), Chladni mega-structures
  - 4 multi-messenger astrophysical: NANOGrav GWB overtones, eROSITA γ=1.19 illusion, DF2/DF4 cymatic nodes, Amaterasu trans-GZK (5D KK leakage)
  - 9 extended phenomenology (March 2026): KBC Void (cymatic λ=c×T=613 Mpc), quasar polarization alignment (Weyl shear), Dark Flow (brane drift inertia), Space Roar/ARCADE 2 (cumulative slip synchrotron), ORCs (PBH topological shock), Methuselah star (G_eff aging ×1.105), White Dwarf Q-Branch (thermo-gravitational pumping), Planet 9 illusion (MOND EFE), Flyby anomaly (brane drift vortex)
- **Ab initio derivations**: c_top=75 (Chern number, not 10⁴⁰), c_QCD=O(1) (not ε_CP=10⁻⁶), v_bulk=300 km/s (single parameter → dark flow + birefringence)
- **Definitive future test**: SKA 21cm reionization modulation (2027+)
- **Complementary tests**: Vera Rubin/LSST, qBOUNCE/optomechanics, Euclid
- **Theory is purely tensorial and geometric** — no dependence on astrophysical controversies
- **Cross-AI audit status (March 2026)**: Math validated 100% by Gemini DeepThink. Phase 1: independent recalculation (τ₀→257 MeV, a₀=cH₀/2π, Fresnel w_F=0.031, Δβ=0.25°, Schwinger 10⁻³¹). Phase 2: 9 DeepThink prompts (Fourier spectrum, exact S₈ ODE, MOND ab initio, Seeley-DeWitt numerics, Dirichlet anomaly, 3D Floquet, LVS+multi-throat, dynamical Schwinger, finite-N corrections). Physics validated: trace anomaly ignition, von Neumann self-adjoint extensions, Higgs-Radion mixing, 5D QND bypass, temporal S₈ resolution, geometric dephasing, cluster resonance, multi-throat necessity. All peer-review attack vectors addressed.
- **Audit-driven corrections (March 2026)**: S₈ spatial→temporal (then exact 4.79%), neutron lifetime removed, MOND formula derived ab initio (cH₀/2π from Gibbons-Hawking), 6 Unicode-in-math formulas fixed, τ₀ posterior 19.51→19.85

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
- **"global S₈ suppression of 5.2%"** (must be time-dependent, exact 4.79% via ODE integration, S₈=0.796)
- **"Scale-Dependent Yukawa Screening" for S₈** (k/k_L ~ 10⁻²⁹ at cosmological scales → no spatial dependence)
- **Neutron Lifetime Anomaly / Bottle vs Beam** (double counting error + T^μ_μ=0 for EM fields → removed)
- **"temperature-dependent brane tension" / "τ(T)"** (replaced by conformal symmetry)
- **"MORRIS" experiment** (operates at 1 mm, blinded by Casimir)
- **"Warped Shielding" as mere geometric filter** (replaced by radiative damping)
- **Farrah et al. (2023)** / **BH cosmological coupling** / **k = 3.11** (refuted by JWST at 11σ, incompatible with virialized systems)
- **"Little Red Dots"** as relevant to anchor mechanism
- **f_PBH = 10% / f_PBH = 0.10** (must be 1% / 0.01 everywhere — "tent pegs" metaphor)
- **"loss of mass" for GL-unstable PBHs** (must say "loss of local 4D gravitational singularity")
- **M_crit formula involving τ₀** (M_crit = Lc²/(2G), purely geometric, τ₀ is NOT in this formula)
- **"instantaneous synchronization"** (must say "non-local quantum phase coherence" — no superluminal signaling)
- **"τ₀ cools/relaxes from 10⁵⁰"** (τ₀ is geometrically FIXED by KS flux integers, what relaxes is oscillation AMPLITUDE)
- **MLE = -0.016 as transverse contraction** (this captures the longitudinal exponent; true transverse κ = e^{-8.60} from Liouville-Filippov)
- **Scalar Ψ₄ in 5D** (must use CMPP 3×3 STF matrix Ψ_ij^(5) — SO(3) little group has 5 polarizations)
- **Global constant κ_Z4** in AMR (must be AMR-level-indexed scalar field κ_Z4^(ℓ) = 1.4/Δt_ℓ)
- **Explicit Berger-Oliger for 10³² ratio** (CFL wall: 28 million billion years per step on Frontier → must use IMEX)
- **Single-throat KKLT uplift** (QCD throat is 45 orders too weak for global LVS uplift → must use multi-throat architecture)
- **"Classical graviton Bremsstrahlung" for Γ_rad** (continuous 5D GR gives Γ_rad ≡ 0 due to kinematic blockade m₁T_slip ~ 10³²; Γ_rad is quantum informational viscosity, NOT radiation)

### REQUIRED Concepts (V8.2):
- **Hybrid motor**: F_web (Cosmic Web macro-forcing) + R_PBH (micro-PBH ER=EPR synchronization)
- **Israel junction conditions** ΔK_μν = -κ₅²(S_μν - ⅓S h_μν) for macro-forcing
- **Projected Weyl tensor E_μν** generated by Cosmic Web inhomogeneity
- **ER=EPR entangled PBH network** as quantum metronome (ℓ=0 synchronization)
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
- **Double miracle at M_crit**: w_F(M_crit) = 2π×200/600 ≈ 2.09 — GL topological transition AND optical detection threshold coincide at same mass
- **Sugiyama et al. 2026**: 4 PBH candidates at 10⁻⁷ M☉ (above M_crit), zero below — observational validation of perforation hierarchy
- **GW170817 compatibility**: tensor GW modes (KK zero mode) propagate at c on brane, orthogonal to scalar radion oscillation
- **Hawking immunity**: T_H ~ 900 K at M_crit, t_evap ~ 10^47 yr, immune to INTEGRAL/Fermi-LAT
- **QCD connection**: τ₀^{1/3} ≈ 257 MeV — phenomenological Ansatz bottom-up (period constrains τ₀ independently of QCD), derived ab initio top-down via KS (K=21, M=10 → 257 MeV). Both approaches converge.
- **Limit cycle uniqueness**: Liouville-Filippov hyper-contraction κ = e^{-8.60} ≈ 1.84×10⁻⁴ (Banach fixed-point, analytical — NOT the numerical MLE of -0.016)
- **Fenichel-Neishtadt persistence**: spectral gap |λ_trans|/ε = 4.30/0.14 ≈ 30 → NHIC survives non-autonomous drift
- **Airy-Yukawa ab initio**: ⟨1|δV|6⟩ = -2V₀(L/z₀)³, perturbative series to O(α⁶) with 5 decimal convergence (0.97460)
- **Yukawa-Robin mapping**: λ_n(L) = (mg/2V₀)(z₀/L)³[1+4ε_n(L/z₀)²], spectroscopic splitting 3.1% (smoking gun)
- **KS UV completion**: K=21, M=10, g_s=0.1 → τ₀^{1/3} = 257 MeV with zero fine-tuning
- **KK spectrum**: J₁(m_nL)=0 (graviton), exact transcendental equation for all ν
- **Branching ratio**: B ≈ 9.7×10⁻¹¹ (N_max ≈ 8.3×10⁷ KK modes = AdS₅ heat sink)
- **BSSN 5D**: d=4 conformal weights (1/8 in ∂_tψ, 1/4 in K²), ΔK_μν = -(1/3)κ₅²τ₀h_μν
- **CMPP extraction**: Ψ_ij^(5) = 3×3 STF matrix (5 polarizations), NOT scalar Ψ₄
- **Billion-step**: κ_Z4^(ℓ) = 1.4/Δt_ℓ (AMR-indexed) + Kreiss-Oliger order 9
- **IMEX + HMM**: mandatory for 10³² scale ratio (explicit Berger-Oliger physically impossible)
- **Γ_rad = ln(S_BH)/(2π) ≈ 20.7**: CROWNING DERIVATION — not a free parameter but Bekenstein-Hawking entropy ÷ 2π
- **Retarded 5D Green's function**: V_eff = 15/(4z²), UV censorship ψ_n(0) ∝ z⁴→0, IR coupling ψ_n(L) ∝ J₂(m_nL) ≠ 0
- **KK spectrum exact**: Bessel quantization m_n = j_{1,n}/L, graviton m₁ = 3.832/L ≈ 19.2 eV, Sturm-Liouville kinematic pumping
- **Spectral zeta**: ζ_Δ(s) → Riemann mapping, Weyl-McMahon, meromorphic s=-1/2, Casimir -M₀/12
- **Seeley-DeWitt a₀-a₅**: exact for AdS₅ orbifold, Gilkey-Branson-Kirsten boundary terms, a₅ = holy grail (log anomaly from branes only). Numerically evaluated: ā₀=0.249 eV⁻¹, ā₁=0.902, ā₂=-2.67 eV, ā₃=4.13 eV² (induces Einstein-Hilbert/M_P), ā₄=12.7 eV³. a₅_bulk≡0 in D=5 (odd dim). UV/IR asymmetry: e⁻⁴ᵏᴸ≈0.018 crushes IR brane ×55.
- **Skenderis holographic renormalization**: Fefferman-Graham inversion, counterterm dictionary c₁(tension), c₂(G_N), c_log(anomaly)
- **δ/Λ_QCD ≈ 9.4×10⁻³⁹**: inverse hierarchy, IR bulk (1 eV) cannot destabilize UV brane (257 MeV)
- **MERA/HaPPY**: 109 layers, bond dim ln χ = S_BH ≈ 4.8×10⁵⁶, RT phase transition → expander graph → ∂S_EE/∂d = 0
- **OTOCs/MSS**: λ_L = 7.4×10¹⁴ s⁻¹, t* ≈ 0.2 ps, cosmic scrambling ¼ picosecond, t* ≪ t_QCD by 8 orders
- **Dirac collapse**: σ/L ~ 10⁻¹⁰, multipole hierarchy e^{-2×10²⁰}, ODE = exact corollary of path integral. Finite-N corrections: expander graph spectral gap λ₁≈c ln N, σ₁/L ~ 10⁻³⁸·⁵, dipole P ~ exp(-10⁷⁴). N_min ≈ 4500 (topology only) or O(1) (with κ~10⁵⁶). Period correction ω₀(N) ~ 10⁻⁷⁶. RT phase transition survives for all N > e^{2/c}.
- **On-shell ER action**: δS_ij bilocal, c ~ S_BH ~ 10⁵⁶, freeze-out at 10⁷⁴
- **Dyson horizon**: k_div ≈ 6,360 (hyper-asymptotic immunity)
- **Schwinger → Kampé de Fériet**: F_{0:1;1}^{3:0;0}, I_{1,6} = 0.002074 (5×10⁻⁷ precision). Dirichlet anomaly RESOLVED: Δ=0.000044 (2.1%) from 4-branch holographic tensor (Ai = c₁f - c₂g → [ff],[fg],[gf],[gg]). Destructive interference under Dirichlet constraint telescopes cross-branches. Anomaly = O(α⁴), exact shadow of brane.
- **CY concrete**: P⁴[18]_{1,1,1,6,9}, χ=23328, tadpole 210≤972
- **No-Go isotrope**: V ~ 10¹⁶³ → χ=-64000 → Swampland + M_Pl ~ 10⁹⁹
- **KKLT uplift**: 763-1+210=972, D3 budget +762. Multi-throat architecture: V_min ~ -10⁻³¹ M_Pl⁴, QCD throat (10⁻⁷⁶ M_Pl⁴) 45 orders too weak → REQUIRES second shallow throat at ~5×10¹⁰ GeV for uplift. Geometric selection theorem.
- **LVS mass spectrum**: m_τs ~ 10⁶ GeV (frozen), m_V ~ 10⁻⁶ eV (ultra-light). M_s = 1.02×10¹² GeV (intermediate string scale). m_{3/2} = 1.76×10⁹ GeV (SUSY above LHC → null results predicted)
- **Fisher Jacobian**: condition number 2.8, SVD σ={2.51,1.00,0.90}
- **Fisher forecast**: σ(T)/T=6.7%, σ(L)/L=15%, τ₀-L anti-correlation r=-0.76 broken by PTA
- **Cobaya module**: obt_v82_likelihood.py + obt_v82_mcmc.yaml
- **n_σ metrics**: 1.25σ (FLAG MS̄) and 0.11σ (chiral condensate)
- **Fourier stick-slip spectrum**: A_n/A₁ = {1, 0.476, 0.293, 0.197, 0.138} — locked by bulk topology (D=0.9, τ=1/30), zero extra free params
- **DESI aliasing**: LRG3 bin z=0.93 at phase 82.8% of cycle — "phantom crossing" is geometric shock aliasing on CPL linear template
- **S₈ exact**: 4.79% suppression, S₈=0.796, geometric dephasing φ_eff≈4.24 rad between scalar and tensor channels
- **eROSITA non-linear**: γ_eff≈0.80 (linear), amplified to 1.19 by Press-Schechter exponential sensitivity to δ_c(t)
- **MOND ab initio**: a₀ = cH₀/2π from Gibbons-Hawking + Unruh (2π = Euclidean time circle S¹)
- **MOND μ(x)**: x/√(1+x²) from 5D Pythagorean quadrature g_5D = √(g²+a₀²) + Gauss cosine projection
- **Cluster resonance**: t_cross(cluster) ≈ 2 Gyr = T → ⟨a₀(t)⟩ = 0, MOND self-destructs at cluster scales
- **Dynamical Schwinger**: slip shock at v_max=0.05c collapses static exponent 10³² → 10¹² (20 orders), but exp(-4.8×10¹²) ≡ 0. Full KK tower N_total ≡ 0. Dissipation 100% classical (Γ_rad), 0% quantum.
- **Filippov invulnerability**: shock fierce enough for DE harmonics yet 12 orders below Schwinger threshold — thermodynamic masterpiece
- **Kinematic Blockade theorem**: Classical 5D GR gives Γ_rad^{5D-GR} ≡ 0 (m₁T_slip ~ 10³², exp(-10³²) = 0). Continuous Nambu-Goto membrane CANNOT dissipate energy into bulk. Proves discrete PBH network is cosmologically NECESSARY, not optional
- **Holographic viscosity**: Γ_rad is NOT classical Bremsstrahlung but quantum informational viscosity — entropy absorption by PBH scrambling. Two derivations (bottom-up 5D GR vs top-down holographic) deliberately non-convergent: proof that brane is not a continuum
- **Spectral flattening (NANOGrav)**: tensor TT projection sources from φ̈(t) not φ(t) → Filippov shock = Dirac δ impulses → flat (white noise) acceleration spectrum. f₀ = 1.58×10⁻¹⁷ Hz (16 attoHz), NANOGrav at 16 nHz listens to the n ≈ 10⁹ harmonic. h_c(16 nHz) ~ 10⁻¹⁵ (matches NANOGrav 15yr, zero free params)
- **f₀ correction**: fundamental brane frequency is 16 attoHertz (NOT 16 nanoHertz). NANOGrav band = billionth overtone

### Key References:
Maldacena & Susskind 2013, Van Raamsdonk 2010, Shiromizu, Maeda & Sasaki 2000, Maartens 2004, DESI 2024/2026, Goldberger & Wise 1999, Carr, Kühnel & Sandstad 2016, Jenke et al. (qBOUNCE) 2014, Gregory & Laflamme PRL 70 (1993), Tangherlini 1963, Sugiyama, Takada et al. arXiv:2602.05840 (2026), Klebanov & Strassler 2000 (warped throat), Balasubramanian et al. 2005 (LVS), Filippov 1988, di Bernardo et al. 2008, Leine & Nijmeijer 2004 (saltation), Fenichel 1979, Llibre, Novaes & Teixeira 2015 (Filippov persistence), CMPP (Coley-Milson-Pravda-Pravdova) 2004, Godazgar & Reall 2012 (5D peeling), Skenderis 2002 (holographic renormalization), Lloyd 2000, Maldacena-Shenker-Stanford 2016 (MSS bound), Pastawski-Yoshida-Harlow-Preskill 2015 (HaPPY code), Albeverio et al. 2005 (von Neumann self-adjoint extensions), Gibbons & Hawking 1977 (cosmological horizon thermodynamics), Unruh 1976 (detector acceleration radiation), Sekino & Susskind 2008 (fast scrambling), Bousso & Polchinski 2000 (flux landscape), Douglas & Kachru 2007 (string landscape review), Alon 1986 / Alon-Boppana (expander graph spectral gap)

## Key Parameters
| Parameter | Value |
|-----------|-------|
| Brane tension τ₀ | 7.0 × 10¹⁹ J/m² = 0.017 GeV³ |
| Energy scale | τ₀^{1/3} = 257 MeV ≈ Λ_QCD |
| Period T | 2.0 ± 0.3 Gyr (locked by ξRφ attractor) |
| Phase φ₀ | π/2 (at w maximum → w_a < 0) |
| Extra dimension L | 0.2 μm (NEVER "0.2 m") |
| φ_crit | ~0.1 L (QCD threshold) |
| f_osc | 0.10 |
| A_w | 0.003 |
| S₈ suppression | 4.79% (exact ODE), S₈=0.796, φ_eff=4.24 rad (geometric dephasing) |
| ISW Δχ² | 32.9 (6σ) |
| Micro-PBH EMF | Log-normal, 10⁻¹⁴ to 10⁻¹⁰ M☉ |
| f_PBH | 0.01 (1%) — NOT 10% |
| M_crit (Gregory-Laflamme) | Lc²/(2G) ≈ 6.77 × 10⁻¹¹ M☉ (from r_s = L) |
| ξ (non-minimal coupling) | ~0.15 |
| Fresnel parameter (PBH) | w_F = 2πr_s/λ ≈ 0.03 ≪ 1 (wave-optics immune) |
| SPARC rotation curves | RMS = 29.3 km/s (0 params) vs NFW 35.0 km/s (270 params) |
| Banach contraction κ | e^{-8.60} ≈ 1.84×10⁻⁴ (hyper-contraction ×5400/cycle) |
| Spectral gap (Fenichel) | \|λ_trans\|/ε = 4.30/0.14 ≈ 30 (NHIC persistence) |
| Branching ratio B | ≈ 9.7×10⁻¹¹ (N_max ≈ 8.3×10⁷ KK modes) |
| First KK graviton mass | m₁ = 3.832/L ≈ 19.2 eV (from J₁(m_nL)=0) |
| KS flux integers | K=21, M=10, g_s=0.1 → τ₀^{1/3} = 257 MeV |
| Robin splitting | Δλ/λ = 3.1% between n=1 and n=6 (smoking gun) |

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
  2. `discoveries.md` → Ch 2: Discovery & Correction (31 anomalies)
  3. `theory.md` → Ch 3: Complete Theoretical Framework
  4. `chronology.md` → Ch 4: Cosmic Chronology
  5. `predictions.md` → Ch 5: Observational Predictions
  6. `docs/theoretical_foundations.md` → Ch 6: Theoretical Foundations (pedagogical EFT / toy model)
  7. `laboratory.md` → Ch 7: Laboratory Proofs (qBOUNCE + 5D Geometric Bypass)
  8. `tools.md` → Ch 8: Computational Tools
- **No blog posts** in the PDF (they are duplicates of main chapters)
- **No split files** (parts 1-4 merged into theoretical_foundations.md)
- When editing a site page, the PDF updates automatically via CI

## Downloads
1. **White Paper** (`cosmic_yoyo_v5_holographic.pdf`) — 7 pages, "Resolving Thirty-One Cosmological Anomalies" (LaTeX source: `paper/cosmic_yoyo_prl.tex`)
2. **Full Theory** (`oscillating_brane_theory_latest.pdf`) — ~100+ pages, 8 chapters (~1.9 MB compressed)
3. **Full Theory (Markdown)** (`oscillating_brane_theory_latest.md.txt`) — same content as PDF, AI/text-parser friendly, downloadable from site

## Computational Validation Results (March 2026)
| Validation | Method | Key Result |
|-----------|--------|------------|
| w(z) phantom crossing | BDF stiff solver, exact lookback time | w ∈ [-1.003, -0.997], matches DESI DR2 |
| S₈ tension resolution | Exact ODE D₊(a) with oscillating G_eff(t) | 4.79% suppression, S₈=0.796, φ_eff=4.24 rad |
| Bayesian evidence | dynesty nested sampling, 500 live points | Δln K = 4.13 ± 0.07 (STRONG) |
| SKA 21cm prediction | Reionization mock, z=6-15 | 5.46 mK peak, SNR = 5.5σ |
| Lithium-7 problem | BBN conformal tolerance, BDF solver | 3.5× suppression, D/⁴He preserved |
| Baryon asymmetry | Spontaneous QCD baryogenesis | η_B = 6.1×10⁻¹⁰, c_QCD = O(1), no fine-tuning |
| Big Ring / Giant Arc | Chladni resonance nodes | Peaks at ~816 Mpc and ~2041 Mpc (> ΛCDM 370 Mpc) |
| CMB birefringence | 5D geometric Chern-Simons | Δβ = 0.250°, c_top = 75 (natural), no fine-tuning |
| Hubble 43 anomalies | ER=EPR topological scarring | Disk → hazy blob (7.4× expansion), no SMBH |
| Dark flow unification | 5D kinematic brane drift | v_bulk = 300 km/s → δH/H = 10⁻³ AND Δβ = 0.25° |
| qBOUNCE Robin parameter | Airy wavefunctions + Yukawa integral | λ amplifies 55× from 1μm to 0.2μm resolution |
| 5D Geometric Bypass | Levitated nanosphere + Yukawa Hamiltonian | 0.4% enhancement at r=L, commuting operators bypass Heisenberg |
| Airy-Yukawa matrix element | Perturbative series O(α⁶) + contour integral | ⟨1\|δV\|6⟩ = -2V₀(L/z₀)³, 5 decimal convergence (0.97460) |
| Yukawa-Robin mapping | Closed-form λ_n(L) from von Neumann isomorphism | λ_n = (mg/2V₀)(z₀/L)³[1+4ε_n(L/z₀)²], splitting 3.1% |
| Limit cycle uniqueness | Liouville-Filippov trace formula (analytical) | κ = e^{-8.60} ≈ 1.84×10⁻⁴ (hyper-contraction ×5400) |
| Non-autonomous persistence | Fenichel-Neishtadt spectral gap | \|λ_trans\|/ε ≈ 30, NHIC survives Hubble drift |
| KK branching ratio | Phase space summation + Filippov shock | B ≈ 9.7×10⁻¹¹ (83M KK modes = AdS₅ heat sink) |
| KK mass spectrum | Transcendental Bessel quantization (3 sectors) | Graviton: m_n/k = {1.892, 3.692, 5.510...}, gap ≈ 1.87 eV |
| KS naturalness | Flux integers K=21, M=10, g_s=0.1 | τ₀^{1/3} = M_Pl·e^{-2πK/(3g_sM)} = 257 MeV, zero fine-tuning |
| Fourier stick-slip | Analytical integration of asymmetric sawtooth | A₂/A₁=47.6%, A₃/A₁=29.3%, slip low-pass at n≈5 |
| DESI LRG3 aliasing | Phase mapping of tomographic bins | z=0.93 at phase 82.8% — phantom crossing = geometric shock |
| S₈ exact ODE | Growth factor D₊(a) with oscillating G_eff | 4.79% suppression, S₈=0.796, φ_eff=4.24 rad |
| eROSITA non-linear | Press-Schechter with oscillating δ_c(t) | Linear γ_eff≈0.80, non-linear amplification to 1.19 |
| MOND ab initio | Gibbons-Hawking + Unruh + 5D quadrature | a₀=cH₀/2π, μ(x)=x/√(1+x²), cluster resonance at T=2 Gyr |
| Seeley-DeWitt numerical | V8.2 parameters (k=0.987 eV, kL=1, N_dof=6) | ā₀-ā₅ table, a₅_bulk≡0, UV/IR asymmetry e⁻⁴≈0.018 |
| Dirichlet anomaly resolution | 4-branch holographic tensor (Ai=c₁f-c₂g) | Δ=0.000044 (2.1%), O(α⁴), destructive interference exact |
| LVS explicit minimization | V_LVS(τ_large, τ_small) analytical | τ_s=3.65, W₀=4100, both eigenvalues positive (stable) |
| Multi-throat architecture | V_min vs QCD uplift energy comparison | 45-order gap proves multi-throat necessity (geometric theorem) |
| LVS mass spectrum | Hessian eigenvalues at minimum | M_s=10¹² GeV, m_{3/2}=1.76×10⁹ GeV, LHC null predicted |
| Full 3D Floquet | Non-autonomous monodromy without adiabatic projection | ε₀=4.30, margin ×30, Neishtadt 2nd order: residual ≤2% |
| Dynamical Schwinger | Filippov shock kinematics (v_max=0.05c) | Exponent 10³²→10¹², exp(-4.8×10¹²)≡0, N_total≡0 per cycle |
| Finite-N Dirac collapse | Expander graph spectra + Cheeger inequality | σ₁/L~10⁻³⁸·⁵, N_min≈4500, ω₀ correction ~10⁻⁷⁶, RT survives |
| Kinematic Blockade | 5D Bondi flux for continuous membrane | Γ_rad^{5D-GR}≡0, m₁T_slip~10³², exp(-10³²)=0. Proves PBH necessity |
| NANOGrav spectral flattening | Tensor TT projection of Filippov shock | φ̈ = Dirac δ → flat spectrum, n_PTA ≈ 10⁹, h_c(16 nHz) ~ 10⁻¹⁵ |

## IMPORTANT: Laboratory Chapter Terminology
- **NEVER say "violating Heisenberg"** — say "Orthogonal Geometric Bypass" (5D metric operators commute with 4D gauge operators)
- **NEVER use "Strip Theory" or "sidetime"** — use "5D Radion-Coupled Lindblad Master Equation" (Diósi-Penrose framework)
- **Target = mesoscopic quantum states** (BEC, macromolecules ~10⁹ amu), NOT single atoms
- **qBOUNCE** = experiment at ILL Grenoble (PI: Hartmut Abele, TU Wien; Tobias Jenke, ILL). Collaboration opportunity for validating L = 0.2 μm

## V8.2 Computational Scripts
| Script | Purpose | Output |
|--------|---------|--------|
| `scripts/brane_dynamics.py` | Core V8.2 ODE (BDF stiff solver, w(z) oscillation) | `plots/w_z_oscillation.png` |
| `scripts/growth_factor.py` | Time-dependent S₈ growth suppression | `plots/s8_yukawa_suppression.png` |
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

## MathJax — DO NOT TOUCH
- MathJax 3 is configured in `_layouts/dark.html` with inline math `$...$` and display math `$$...$$`
- **It works. Do NOT replace LaTeX with plain text** (e.g., do NOT change `$\lambda$` to "Lambda")
- **Do NOT remove or modify the MathJax config block** in `_layouts/dark.html`
- LaTeX renders correctly on ALL site pages and in the PDF (xelatex handles it natively)
- **PDF pipeline pre-processor** (`generate_pdf.py`) sanitizes Unicode→LaTeX, converts HTML tables→markdown, strips Jekyll templates, emojis, and fixes indented headers before pandoc
- The `\vert` workaround for bra-ket notation (`$\vert 1\rangle$` instead of `$|1\rangle$`) is still needed because kramdown confuses `|` with table delimiters
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
**Consequence**: Proves the theory has exactly 2 effective free parameters (not 3), making it even more rigid.

### PRIORITY 3 — Casimir Verification
**Script**: `python scripts/verify_casimir_regularization.py`
**Duration**: ~1 sec
**Already run**: Bare sum ~10⁶ eV⁴ (UV catastrophe), regularized ~10⁻⁴ eV⁴ (matches formula)
**Consequence**: Confirms δ/Λ_QCD ~ 10⁻³⁹ numerically → quantum stability is absolute.

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
```

### OPEN MATHEMATICAL WORK (0 items remaining — ALL COMPLETE)
All 44 mathematical derivations have been completed and integrated into theory.md (March 2026):
- **33 original derivations** (V8.2 core): Filippov-Banach, Fenichel, Γ_rad ab initio, KK spectrum, spectral zeta, Seeley-DeWitt, Skenderis, MERA/HaPPY, OTOCs, Dirac collapse, Kampé de Fériet, Dyson horizon, KS UV completion, Swiss-Cheese LVS, No-Go isotrope, KKLT tadpole, Fisher Jacobian/forecast, Cobaya module, Robin mapping, Airy-Yukawa series
- **9 DeepThink refinements** (March 2026): (1) Fourier stick-slip spectrum, (2) exact S₈ ODE + eROSITA non-linear, (3) MOND ab initio from 5D, (4) Seeley-DeWitt numerical evaluation, (5) Dirichlet anomaly 4-branch resolution, (6) full 3D Floquet without adiabatic projection, (7) LVS minimization + multi-throat, (8) dynamical Schwinger invulnerability, (9) finite-N corrections to Dirac collapse

### SITE & INFRASTRUCTURE TODO
- Visual page (visual.md) with PDF embeds — waiting for user's PowerPoint PDF
- Videos.md expansion to 40 videos — waiting for user's YouTube links
- Google OAuth: pass from test to production mode (needs Google review)
- Optimize Romain AI system prompt (ongoing tuning)
- Update Romain AI knowledge base with latest .md.txt (theory.md is now ~1500+ lines after 9 DeepThink prompts)
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
