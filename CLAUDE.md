# CLAUDE.md - Project Information for AI Assistants

## Project Overview
This is the **Oscillating Brane Dark Matter Theory V5.0 (Holographic Edition)** - a cosmological theory where the universe is a vibrating 4D membrane in 5D Anti-de Sitter space, with black holes connected via ER=EPR holographic entanglement.

**Author**: Romain Provencal (provencal.romain@teleadmin.net) - Independent conceptual researcher
**AI Collaborators**: Claude (Anthropic) & Gemini DeepThink (Google) as theoretical co-processors

## Repository Information
- **GitHub URL**: https://github.com/Teleadmin-ai/oscillating-brane-DM
- **Live Website**: https://higgs-cosmology.com/
- **Owner**: Teleadmin-ai (NOT "Teleadmin")
- **Current Version**: V5.0 Holographic Edition (March 2026)
- Always use `gh` commands for GitHub operations

## CRITICAL: Theory V5.0 Paradigm (MUST FOLLOW)

### Core Physics (V5.0):
- The bulk is a **non-local topological state** where spacetime is emergent (Van Raamsdonk 2010)
- Black holes are connected via **ER=EPR wormhole network** (Maldacena & Susskind 2013)
- Distance and time are properties of the 4D brane only; in the bulk they have no meaning
- Oscillation period T = 2.0 Gyr calibrated from **DESI BAO + Planck ISW resonance**
- **Excitation mechanism**: Susskind's Complexity=Volume — wormhole interiors grow as BHs absorb DM, exerting topological traction (backreaction) on the brane. NOT ballistic impacts/"tiny hammers"
- **S₈ suppression**: Via G_eff = G_N × e^{-2k|z|} — gravity "leaks" into 5th dimension (⟨z²⟩ > 0 → ⟨G_eff⟩ < G_N). NOT just w(z) friction
- **Quantum stability**: Adiabatic theorem — ν_brane/ν_KK ~ 10⁻³¹, Schwinger factor e^{-10³¹} ≈ 0. No quantum friction
- **QCD connection**: τ₀ = 0.017 GeV³, so τ₀^{1/3} = 257 MeV ≈ Λ_QCD (brane tension set by strong force vacuum)
- The "smoking gun" is the **ISW resonance** in CMB at ℓ = 10-20 (NOT gravitational waves)
- **JWST LRDs** explained as "cosmic pushpins" — primordial topological defects anchoring the brane

### BANNED Concepts (old versions — NEVER use):
- **"Point Unique" as a 0D geometric point** — divergent curvature, violates Einstein 5D
- **Ringermacher & Mead (2014)** — debunked by Brownsberger et al. 2020 (windowing artifact)
- **GW doublet detection via PTA/NANOGrav/LISA** — 2 Gyr frequency far too low
- **"Bulk-Infinity" / "Bulk-Point" debate / "Two Limiting Visions"** — replaced by non-local state
- **"Convergent Funnels vs Infinite Ocean"** — deleted section
- **"Block Universe topology"** — replaced by ER=EPR holographic topology
- **"tiny hammers" / "momentum hit" / ballistic impacts** — replaced by Complexity=Volume traction
- **"dark matter impacts the brane"** — replaced by topological backreaction
- **Version 4.0 / 4.1 references** — current version is 5.0
- **τ₀ = 2.2 × 10⁻⁵ GeV³** — WRONG old conversion. Correct: τ₀ = 0.017 GeV³
- **contact@higgs-cosmology.com** — does not exist. Use provencal.romain@teleadmin.net

### Key references:
- Maldacena & Susskind (2013) - ER=EPR conjecture
- Van Raamsdonk (2010) - Emergent spacetime from entanglement
- Susskind - Complexity=Volume conjecture
- Brownsberger, Stubbs & Scolnic (2020) - Debunking of Ringermacher
- DESI Collaboration (2024, 2026) - Evolving dark energy evidence
- Farrah et al. (2023) - Black hole cosmological coupling

## Key Technical Parameters

- **Brane tension**: τ₀ = 7.0 × 10¹⁹ J/m² = 0.017 GeV³
- **Energy scale**: τ₀^{1/3} = 257 MeV ≈ Λ_QCD
- **Oscillation period**: T = 2.0 ± 0.3 Gyr (from DESI/Planck, NOT Ringermacher)
- **Extra dimension size**: L = 2.0 × 10⁻⁷ m (0.2 μm) — NEVER write "L = 0.2 m" without μ
- **Oscillating fraction**: f_osc = 0.10
- **MOND acceleration**: a₀ = 1.1 × 10⁻¹⁰ m/s² — ALWAYS negative exponent
- **Dark energy amplitude**: A_w ≃ 0.003
- **S₈ suppression**: -5.2% via G_eff leak
- **ISW χ² improvement**: 32.9 (6σ over ΛCDM)
- **Bayesian evidence**: Δln K = 3.33 ± 0.24

## PDF Generation — KNOWN RACE CONDITION

The CI workflow (`.github/workflows/ci.yml`) auto-regenerates and pushes the PDF on every commit. This creates merge conflicts.

### After modifying any source .md file:
1. Regenerate locally: `python3 scripts/generate_pdf.py`
2. Verify: `pdftotext oscillating_brane_theory_latest.pdf - | grep -i "GHOST_PATTERN"`
3. Commit the PDF explicitly
4. If push rejected: `git pull origin main` then resolve PDF conflict with `git checkout --ours oscillating_brane_theory_latest.pdf`

### Files the PDF generator reads (in order):
```
index.md, theory.md, chronology.md, predictions.md, tools.md, about.md,
docs/theory_v4_complete.md,
docs/foundations_parts/part1_mathematical_framework.md,
docs/foundations_parts/part2_comparative_predictions.md,
docs/foundations_parts/part3_current_limitations.md,
docs/foundations_parts/part4_development_roadmap.md,
_posts/*.md (all 5 blog posts, sorted reverse chronological)
```
**ALL these files must be checked** when hunting for ghost content.

### Ghost verification command:
```bash
pdftotext oscillating_brane_theory_latest.pdf - | grep -i "Ringermacher\|Point Unique\|tiny hammers\|momentum hit\|NANOGrav\|Block Universe\|Version 4\|Infinite Ocean\|dark matter impacts"
```

## Project Structure
```
oscillating-brane-DM/
├── _posts/              # 5 blog posts (all updated V5.0)
├── _layouts/dark.html   # Main layout (NO polyfill.io)
├── assets/
│   ├── css/dark-theme.css  # 45%/55% text/video grid
│   ├── js/video-carousel.js
│   └── videos/
├── plots/               # 23 figures (8 referenced by served pages)
├── scripts/
│   ├── generate_pdf.py         # PDF generator (reads ALL .md files)
│   ├── desi_w_evolution.py     # DESI plot generator (label: ER=EPR)
│   ├── brane_dynamics.py       # Core physics
│   └── ...
├── paper/
│   └── cosmic_yoyo_prl.tex    # V5.0 white paper LaTeX (5 pages)
├── docs/
│   ├── theory_v4_complete.md       # Complete theory (V5.0 content)
│   ├── theoretical_foundations.md  # Mathematical framework
│   └── foundations_parts/          # Split framework (4 parts)
├── output/              # Generated PDFs (excluded from Jekyll, contains stale combined.md files)
├── cosmic_yoyo_v5_holographic.pdf  # White paper (5 pages)
├── oscillating_brane_theory_latest.pdf  # Full theory (72 pages)
├── index.md, theory.md, predictions.md, chronology.md, tools.md, about.md, downloads.md
├── _config.yml          # Jekyll config
├── CNAME                # higgs-cosmology.com
└── .github/workflows/ci.yml  # CI with PDF auto-generation (race condition!)
```

## Jekyll/GitHub Pages
- **Theme**: jekyll-theme-minimal
- **Domain**: higgs-cosmology.com (CNAME)
- **MathJax**: Direct CDN (polyfill.io REMOVED — compromised in 2024)
- **CSS**: 45%/55% text/video grid, images 100% column width
- **OpenGraph image**: /plots/cosmic_yoyo_simple.gif
- **Navigation**: Home, Theory, Complete Theory, Theoretical Foundations, Chronology, Predictions, Tools, Downloads, About

## Downloads (2 PDFs only)
1. **White Paper V5.0** (`cosmic_yoyo_v5_holographic.pdf`) — 5 pages, LaTeX
2. **Full Theory** (`oscillating_brane_theory_latest.pdf`) — 72 pages
- Old V4 white paper: DELETED

## Human-AI Collaboration Model
The author (Romain) is the conceptual architect — geometric intuition, synthesis of anomalies, direction of research. The AI systems (Claude, Gemini) serve as mathematical co-processors — translating concepts into formal frameworks, executing derivations, verifying physical consistency. This is the Faraday-Maxwell model: vision + formalization. The acknowledgments in the white paper are radically transparent about this methodology.

## Observational Confirmations (2024-2026)
- **DESI 2024-2026**: Dark energy evolves (4σ) — matches oscillating w(z)
- **JWST "Little Red Dots"**: Primordial massive BHs at z>6 — our "Cosmic Pushpins"
- **Farrah et al. 2023-2024**: BH mass coupled to expansion (k=3.11±0.19)
- **S₈ tension**: 5.2% growth suppression via G_eff leak bridges CMB/lensing gap
- **Planck low-ℓ anomaly**: ISW resonance explains it (Δχ²=32.9)

## Maintenance Checklist
- Check ALL source files in PDF generator list when hunting ghosts
- After PDF generation, ALWAYS verify with pdftotext grep
- Never use ballistic/impact language for brane excitation — use Complexity=Volume
- Run `black` and `isort` before committing Python code
- Watch for CI auto-overwriting PDF after push
- Keep downloads.md in sync with available PDFs

## Contact
- **Author**: provencal.romain@teleadmin.net
- **GitHub Issues**: https://github.com/Teleadmin-ai/oscillating-brane-DM/issues
- **Repository owner**: @Teleadmin-ai
