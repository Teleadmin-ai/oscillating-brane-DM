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
5. `docs/theoretical_foundations.md` — rigorous mathematical foundations
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
git add oscillating_brane_theory_latest.pdf output/oscillating_brane_theory_latest.pdf
git commit -m "Regenerate PDF" && git push
```
**If you forget, the PDF on the site will be stale and inconsistent with the site pages.**

**Breaking these rules causes data loss in INPI deposits and costs the user money.**

## Project Overview
**Oscillating Brane Cosmology V8.0 (Hybrid Topology Edition)** - The universe is a vibrating 4D membrane in 5D AdS space, driven by a hybrid stick-slip motor: macroscopic Cosmic Web forcing via Israel junction conditions (the muscle) + microscopic ER=EPR-entangled PBH network for quantum synchronization (the metronome).

**Author**: Romain Provencal (provencal.romain@teleadmin.net) - Independent conceptual researcher
**AI Collaborators**: Claude (Anthropic) & Gemini DeepThink (Google) as theoretical co-processors

## Repository
- **GitHub**: https://github.com/Teleadmin-ai/oscillating-brane-DM
- **Website**: https://higgs-cosmology.com/
- **Owner**: Teleadmin-ai (NOT "Teleadmin")
- **Version**: V8.0 Hybrid Topology Edition (March 2026)

## CRITICAL: Theory V8.0 Paradigm

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
- **Dark energy**: w(z) = -1 + A_w sin(2πt_lb/T + φ₀) with **φ₀ = π/2** → w_a < 0 (DESI)
- **S₈ suppression**: Via **time-dependent growth suppression** G_eff(t) = G_N(1 + f_osc sin(2πt/T + φ₀)). Temporal, not spatial
- **ISW resonance**: CMB ℓ = 10-20, Δχ² = 32.9 (6σ)
- **Anchors**: Micro-PBHs with **extended log-normal mass function** (10⁻¹⁴ to 10⁻¹⁰ M☉). Dual role: topological capillaries AND quantum synchronization nodes (ER=EPR)
- **Laboratory tests**: qBOUNCE (ultra-cold quantum neutrons, ILL) + levitated nanoscale optomechanics. Bypass Casimir at sub-micron scale

### Epistemological Framework:
- **31 anomalies resolved** (numerically validated, no fine-tuning):
  - 3 core: DESI phantom crossing, S₈ tension (time-dependent growth suppression), Planck ISW (Δχ²=32.9)
  - 8 established: neutrino masses, DM invisibility (LZ), emergent MOND (SPARC 135 galaxies: RMS 29.3 km/s, 0 free params vs NFW 35.0 km/s, 270 params), JWST early galaxies, early SMBHs, cosmological constant, cosmic dipole, Hubble tension
  - 4 validated connections: Lithium-7 (BBN conformal tolerance), baryon asymmetry (spontaneous QCD baryogenesis, c_QCD=O(1)), Big Ring/Giant Arc (Chladni resonance), CMB birefringence (5D geometric Chern-Simons, c_top=75)
  - 3 astrophysical signatures: Hubble's 43 anomalous objects (ER=EPR topological scarring), dark flow unification (v_bulk=300 km/s), Chladni mega-structures
  - 4 multi-messenger astrophysical: NANOGrav GWB overtones, eROSITA γ=1.19 illusion, DF2/DF4 cymatic nodes, Amaterasu trans-GZK (5D KK leakage)
  - 9 extended phenomenology (March 2026): KBC Void (cymatic λ=c×T=613 Mpc), quasar polarization alignment (Weyl shear), Dark Flow (brane drift inertia), Space Roar/ARCADE 2 (cumulative slip synchrotron), ORCs (PBH topological shock), Methuselah star (G_eff aging ×1.105), White Dwarf Q-Branch (thermo-gravitational pumping), Planet 9 illusion (MOND EFE), Flyby anomaly (brane drift vortex)
- **Ab initio derivations**: c_top=75 (Chern number, not 10⁴⁰), c_QCD=O(1) (not ε_CP=10⁻⁶), v_bulk=300 km/s (single parameter → dark flow + birefringence)
- **Definitive future test**: SKA 21cm reionization modulation (2027+)
- **Complementary tests**: Vera Rubin/LSST, qBOUNCE/optomechanics, Euclid
- **Theory is purely tensorial and geometric** — no dependence on astrophysical controversies
- **Cross-AI audit status (March 2026)**: Math validated 100% by Gemini DeepThink (independent recalculation of τ₀→257 MeV, a₀=cH₀/2π, Fresnel w_F=0.031, Δβ=0.25°, Schwinger 10⁻³¹). Physics validated: trace anomaly ignition, von Neumann self-adjoint extensions, Higgs-Radion mixing, 5D QND bypass, temporal S₈ resolution. Primary peer-review attack vector (chirp stability) addressed via ξRφ PLL attractor.
- **Audit-driven corrections (March 2026)**: S₈ spatial→temporal, neutron lifetime removed, MOND formula corrected (cH₀/2π), 6 Unicode-in-math formulas fixed

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
- **"global S₈ suppression of 5.2%"** (must be time-dependent, ~5% during current weakened-gravity phase)
- **"Scale-Dependent Yukawa Screening" for S₈** (k/k_L ~ 10⁻²⁹ at cosmological scales → no spatial dependence)
- **Neutron Lifetime Anomaly / Bottle vs Beam** (double counting error + T^μ_μ=0 for EM fields → removed)
- **"temperature-dependent brane tension" / "τ(T)"** (replaced by conformal symmetry)
- **"MORRIS" experiment** (operates at 1 mm, blinded by Casimir)
- **"Warped Shielding" as mere geometric filter** (replaced by radiative damping)
- **Farrah et al. (2023)** / **BH cosmological coupling** / **k = 3.11** (refuted by JWST at 11σ, incompatible with virialized systems)
- **"Little Red Dots"** as relevant to anchor mechanism

### REQUIRED Concepts (V8.0):
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

### Key References:
Maldacena & Susskind 2013, Van Raamsdonk 2010, Shiromizu, Maeda & Sasaki 2000, Maartens 2004, DESI 2024/2026, Goldberger & Wise 1999, Carr, Kühnel & Sandstad 2016, Jenke et al. (qBOUNCE) 2014

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
| S₈ suppression | ~5% during current weakened-gravity phase (temporal) |
| ISW Δχ² | 32.9 (6σ) |
| Micro-PBH EMF | Log-normal, 10⁻¹⁴ to 10⁻¹⁰ M☉ |
| ξ (non-minimal coupling) | ~0.15 |
| Fresnel parameter (PBH) | w_F = 2πr_s/λ ≈ 0.03 ≪ 1 (wave-optics immune) |
| SPARC rotation curves | RMS = 29.3 km/s (0 params) vs NFW 35.0 km/s (270 params) |

## ABSOLUTE RULE: Site = PDF symmetry
**Every scientific page on the site MUST be a chapter in the PDF. No exceptions.**
Pages excluded from PDF (non-scientific): index.md (Home), about.md, downloads.md, research.md, refutation.md.
ALL other .md pages with scientific content MUST be in generate_pdf.py doc_order.
**If you add a new scientific page to the site, add it to the PDF immediately.**
**If you remove a page from the PDF, you are BREAKING the symmetry. Do NOT do this.**

## PDF Generation — CRITICAL WORKFLOW
**The CI does NOT auto-push the PDF.** You MUST regenerate and push it manually after ANY .md file change. If you forget, the site will have a stale PDF.

**After modifying any .md file that is in the PDF (index.md, discoveries.md, theory.md, docs/theoretical_foundations.md, tools.md), ALWAYS do:**
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
Reduces ~2 MB → ~1.1 MB without quality loss. Requires `ghostscript` package locally.

### Ghost grep (V8.0 + March 2026 audit):
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
  4. `docs/theoretical_foundations.md` → Ch 4: Theoretical Foundations
  5. `laboratory.md` → Ch 5: Laboratory Proofs (qBOUNCE + 5D Geometric Bypass)
  6. `tools.md` → Ch 6: Computational Tools
- **No blog posts** in the PDF (they are duplicates of main chapters)
- **No split files** (parts 1-4 merged into theoretical_foundations.md)
- When editing a site page, the PDF updates automatically via CI

## Downloads
1. **White Paper** (`cosmic_yoyo_v5_holographic.pdf`) — 6 pages, "Resolving Thirty-One Cosmological Anomalies" (LaTeX source: `paper/cosmic_yoyo_prl.tex`)
2. **Full Theory** (`oscillating_brane_theory_latest.pdf`) — ~72 pages, 8 chapters (~1.3 MB compressed)
3. **Full Theory (Markdown)** (`oscillating_brane_theory_latest.md.txt`) — same content as PDF, AI/text-parser friendly, downloadable from site

## Computational Validation Results (March 2026)
| Validation | Method | Key Result |
|-----------|--------|------------|
| w(z) phantom crossing | BDF stiff solver, exact lookback time | w ∈ [-1.003, -0.997], matches DESI DR2 |
| S₈ tension resolution | Time-dependent G_eff(t) oscillation | ~5% during current weakened-gravity phase |
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

## IMPORTANT: Laboratory Chapter Terminology
- **NEVER say "violating Heisenberg"** — say "Orthogonal Geometric Bypass" (5D metric operators commute with 4D gauge operators)
- **NEVER use "Strip Theory" or "sidetime"** — use "5D Radion-Coupled Lindblad Master Equation" (Diósi-Penrose framework)
- **Target = mesoscopic quantum states** (BEC, macromolecules ~10⁹ amu), NOT single atoms
- **qBOUNCE** = experiment at ILL Grenoble (PI: Hartmut Abele, TU Wien; Tobias Jenke, ILL). Collaboration opportunity for validating L = 0.2 μm

## V8.0 Computational Scripts
| Script | Purpose | Output |
|--------|---------|--------|
| `scripts/brane_dynamics.py` | Core V8.0 ODE (BDF stiff solver, w(z) oscillation) | `plots/w_z_oscillation.png` |
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
| `scripts/bbn_thermal_freezeout.py` | BBN via conformal symmetry & trace anomaly | `plots/bbn_thermal_freezeout.png` |
| `scripts/growth_scale_dependent.py` | Scale-dependent S₈ Yukawa (legacy) | `plots/growth_scale_dependent.png` |
| `scripts/numerical_relativity_1d.py` | 5D radiative damping (1+1)D MoL | `plots/warped_shielding_1D.png` |
| `scripts/qbounce_yukawa_lambda.py` | qBOUNCE Robin parameter from Yukawa | `plots/qbounce_lambda_prediction.png` |
| `scripts/laplace_demon_hamiltonian.py` | 5D Geometric Bypass Hamiltonian | `plots/laplace_demon_readout.png` |

## MathJax — DO NOT TOUCH
- MathJax 3 is configured in `_layouts/dark.html` with inline math `$...$` and display math `$$...$$`
- **It works. Do NOT replace LaTeX with plain text** (e.g., do NOT change `$\lambda$` to "Lambda")
- **Do NOT remove or modify the MathJax config block** in `_layouts/dark.html`
- LaTeX renders correctly on ALL site pages and in the PDF (xelatex handles it natively)
- **PDF pipeline pre-processor** (`generate_pdf.py`) sanitizes Unicode→LaTeX, converts HTML tables→markdown, strips Jekyll templates, emojis, and fixes indented headers before pandoc
- The `\vert` workaround for bra-ket notation (`$\vert 1\rangle$` instead of `$|1\rangle$`) is still needed because kramdown confuses `|` with table delimiters

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

## TODO: Interactive Theory Agent
- **Purpose**: Chatbot on the site that knows the full V8.0 theory and can do math (Python sandbox)
- **Infrastructure**: Dedicated Debian 12 VM on OVH — 4 CPU, 8 GB RAM, 48 GB disk — IP: 51.254.22.29
- **LLM**: Kimi K2.5 via Ollama Cloud (96.1% AIME, 87.6% GPQA, +20% agentic boost, thinking mode, fast) (99.1% AIME, Agent Swarm, 256K context)
- **Token**: stored in `.env` (gitignored, NEVER commit)
- **Architecture**: Open WebUI (multi-user sessions) + Ollama Cloud API + Docker ephemeral containers (numpy/scipy/matplotlib sandbox) + iframe embed on higgs-cosmology.com
- **Context**: Inject `oscillating_brane_theory_latest.md.txt` as system prompt (~140 KB)
- **Isolation**: Each user gets ephemeral Docker container for code execution, destroyed after session
- **Status**: VM ready, token stored. Next: install Docker + Open WebUI + configure Ollama Cloud backend.

## Site Structure (Jekyll + GitHub Pages)
- **Layout**: `_layouts/dark.html` — two-column grid (45% text left, 55% video right)
- **Navigation**: defined in `_config.yml` (navigation array), rendered in `dark.html` lines 46-60
- **Video carousel**: 6 videos in `.video-column` (right side), sticky, scroll-synced to text via `assets/js/video-carousel.js`
- **CSS**: `assets/css/dark-theme.css` — dark theme, fixed header with blur, responsive (mobile hides video column)
- **Mobile**: single column, hamburger menu (`.mobile-nav`), video hidden
- **Section markers**: `<div class="section-marker" data-section="...">` in content triggers video switching via IntersectionObserver
- **Non-PDF pages**: index.md, about.md, downloads.md, research.md, refutation.md, videos.md

## Agent Infrastructure (Romain AI)
- **URL**: https://agent.higgs-cosmology.com
- **VM**: Debian 12, 4 CPU, 8 GB RAM, 48 GB disk — IP: 51.254.22.29
- **Stack**: Docker (Open WebUI v0.8.10 + Nginx Proxy Manager)
- **LLM**: Kimi K2.5 via Ollama Cloud (96.1% AIME, 87.6% GPQA, +20% agentic boost, thinking mode, fast)
- **Auth**: GitHub OAuth + Google OAuth (SSO), admin = Romain's account
- **Model**: Custom "Romain" model with system prompt + knowledge base
- **Config**: `/opt/cosmic-yoyo-agent/docker-compose.yml`
- **Secrets**: `.env` (gitignored) — Ollama token, GitHub OAuth, Google OAuth
- **SSL**: Let's Encrypt via NPM, domain: agent.higgs-cosmology.com
- **NEVER modify the VM docker-compose without explicit user approval**

## Human-AI Collaboration
Romain = conceptual architect (Faraday). AI = mathematical co-processors (Maxwell). Radically transparent acknowledgments. Never minimize AI involvement.

## Contact
- provencal.romain@teleadmin.net
- https://github.com/Teleadmin-ai/oscillating-brane-DM/issues
