# CLAUDE.md - Project Information for AI Assistants

## Project Overview
This is the **Oscillating Brane Dark Matter Theory V5.0 (Holographic Edition)** - a cosmological theory where the universe is a vibrating 4D membrane in 5D Anti-de Sitter space, with black holes connected via ER=EPR holographic entanglement.

## Repository Information
- **GitHub URL**: https://github.com/Teleadmin-ai/oscillating-brane-DM
- **Live Website**: https://higgs-cosmology.com/
- **Owner**: Teleadmin-ai
- **Development Status**: Active - AI-assisted theoretical cosmology research
- **Current Version**: V5.0 Holographic Edition (March 2026)
- **AI Collaborators**: Claude (Anthropic) & Gemini DeepThink (Google) as cognitive prostheses

## GitHub Authentication
- The GitHub user is `Teleadmin-ai` (not `Teleadmin`)
- Always use `gh` commands for GitHub operations
- Remote is already configured with authentication

## CRITICAL: Theory V5.0 Paradigm (MUST FOLLOW)

### What the theory IS (V5.0):
- The bulk is a **non-local topological state** where spacetime is emergent (Van Raamsdonk 2010)
- Black holes are connected via **ER=EPR wormhole network** (Maldacena & Susskind 2013)
- Distance and time are properties of the 4D brane only; in the bulk they have no meaning
- Oscillation period T = 2.0 Gyr is calibrated from **DESI BAO + Planck ISW resonance**
- Quantum stability ensured by **one-loop effective potential corrections** (Goldberger-Wise + Casimir)
- The "smoking gun" is the **ISW resonance** in CMB at ℓ = 10-20 (NOT gravitational waves)

### What the theory is NOT (BANNED concepts from old versions):
- **"Point Unique" as a 0D geometric point** - BANNED (divergent curvature, violates Einstein 5D)
- **Ringermacher & Mead (2014)** - BANNED (debunked by Brownsberger et al. 2020 as windowing artifact)
- **GW doublet detection via PTA/NANOGrav/LISA** - BANNED (2 Gyr frequency far too low)
- **"Bulk-Infinity" vs "Bulk-Point" debate** - BANNED (replaced by non-local state)
- **"Two Limiting Visions of the Bulk"** - BANNED (deleted section)
- **"Convergent Funnels vs Infinite Ocean"** - BANNED (deleted section)
- **"Block Universe topology"** - BANNED (replaced by ER=EPR holographic topology)
- **Version 4.0 / 4.1 references** - BANNED (current version is 5.0)

### Key references for V5.0:
- Maldacena & Susskind (2013) - ER=EPR conjecture
- Van Raamsdonk (2010) - Emergent spacetime from entanglement
- Brownsberger, Stubbs & Scolnic (2020) - Debunking of Ringermacher
- DESI Collaboration (2024, 2026) - Evolving dark energy evidence
- Farrah et al. (2023) - Black hole cosmological coupling

## Key Technical Parameters

- **Brane tension**: τ₀ = 7.0 × 10¹⁹ J/m²
- **Oscillation period**: T = 2.0 ± 0.3 Gyr (from DESI/Planck, NOT Ringermacher)
- **Extra dimension size**: L = 2.0 × 10⁻⁷ m (0.2 μm) — NEVER write "L = 0.2 m" without μ
- **Oscillating fraction**: f_osc = 0.10
- **MOND acceleration**: a₀ = 1.1 × 10⁻¹⁰ m/s² — ALWAYS negative exponent (10⁻¹⁰, NEVER 10¹⁰)
- **Dark energy amplitude**: A_w ≃ 0.003 (±0.3% oscillation)
- **S₈ suppression**: -5.2% (resolves tension)
- **Bayesian evidence**: Δln K = 3.33 ± 0.24 (strong evidence)
- **ISW χ² improvement**: 32.9 (6σ over ΛCDM)

## PDF Generation — KNOWN RACE CONDITION

### The Problem
The CI workflow (`.github/workflows/ci.yml`) has a `generate-pdf` job that:
1. Clones the repo
2. Runs `python scripts/generate_pdf.py`
3. **Commits and pushes the PDF automatically** (lines 129-145)

This creates a **race condition**: when you push corrections, CI triggers, regenerates the PDF from the new code, and pushes it. But timing conflicts with other pushes can cause merge conflicts or stale PDFs.

### The Solution
After modifying any source `.md` file:
1. Always regenerate the PDF locally: `python3 scripts/generate_pdf.py`
2. Verify the PDF content: `pdftotext oscillating_brane_theory_latest.pdf - | grep -i "GHOST_PATTERN"`
3. Force-add and commit the PDF: `git add -f oscillating_brane_theory_latest.pdf`
4. If push is rejected, always `git pull --rebase` then `git push`
5. After push, check if CI overwrites your PDF with `git log --oneline -3 -- oscillating_brane_theory_latest.pdf`

### Files the PDF generator reads (in order):
```
index.md, theory.md, chronology.md, predictions.md, tools.md, about.md,
docs/theory_v4_complete.md,
docs/foundations_parts/part1_mathematical_framework.md,
docs/foundations_parts/part2_comparative_predictions.md,
docs/foundations_parts/part3_current_limitations.md,
docs/foundations_parts/part4_development_roadmap.md,
_posts/*.md (all blog posts, sorted reverse chronological)
```
**ALL these files must be checked** when hunting for ghost content. Missing even one blog post will leave ghosts in the PDF.

## Project Structure
```
oscillating-brane-DM/
├── _posts/              # Blog posts (5 total, dark theme)
├── _layouts/
│   └── dark.html        # Main layout (NO polyfill.io - removed for security)
├── assets/
│   ├── css/dark-theme.css  # 45%/55% text/video split layout
│   ├── js/video-carousel.js
│   └── videos/          # Local MP4 files
├── plots/               # Scientific figures (23 files, 8 referenced)
├── scripts/
│   ├── generate_pdf.py         # Main PDF generator (reads ALL .md files)
│   ├── generate_whitepaper.py  # V4 white paper generator (OBSOLETE)
│   ├── brane_dynamics.py       # Membrane oscillation calculations
│   ├── brane_oscillation_1d.py # 1D radion field evolution
│   ├── growth_factor.py        # Structure formation
│   ├── bayesian_analysis.py    # Model comparison
│   └── ...                     # Other analysis scripts
├── paper/
│   └── cosmic_yoyo_prl.tex    # V5.0 white paper LaTeX source
├── docs/
│   ├── theory_v4_complete.md       # Complete theory (now V5.0)
│   ├── theoretical_foundations.md  # Mathematical framework
│   └── foundations_parts/          # Split framework (4 parts)
├── output/              # Generated PDFs (excluded from Jekyll build)
├── cosmic_yoyo_v5_holographic.pdf  # V5.0 white paper (4 pages)
├── oscillating_brane_theory_latest.pdf  # Full theory (70 pages)
├── index.md, theory.md, predictions.md, chronology.md, tools.md, about.md, downloads.md
├── _config.yml          # Jekyll config (navigation, theme)
├── CNAME                # higgs-cosmology.com
└── .github/workflows/ci.yml  # CI with PDF auto-generation
```

## Jekyll/GitHub Pages Configuration

- **Theme**: `jekyll-theme-minimal` (GitHub Pages supported)
- **Custom Layout**: `dark.html` with video carousel
- **Domain**: higgs-cosmology.com (CNAME)
- **MathJax**: Loaded directly from CDN (polyfill.io REMOVED - was compromised)
- **CSS**: 45%/55% text/video grid split, images use 100% of text column width
- **OpenGraph image**: `/plots/cosmic_yoyo_simple.gif`

### Navigation pages (in _config.yml):
Home, Theory, Complete Theory (/theory-complete/), Theoretical Foundations (/theoretical-foundations/), Chronology, Predictions, Tools, Downloads, About

### Blog Posts (5 total):
1. `2025-07-03-introduction-universe-membrane.md` - Introduction (updated V5.0)
2. `2025-07-03-microscopic-excitation.md` - Excitation mechanism (updated V5.0 ER=EPR)
3. `2025-07-03-cosmic-chronology.md` - Timeline (Ringermacher removed)
4. `2025-07-03-observational-tests.md` - Tests (NANOGrav removed)
5. `2026-03-20-observational-confirmations.md` - 2024-2026 confirmations

## Key Observational Confirmations (2024-2026)
- **DESI 2024-2026**: Dark energy evolves (4σ) — matches oscillating w(z)
- **JWST "Little Red Dots"**: Primordial massive BHs at z>6 — our "Cosmic Pushpins"
- **Farrah et al. 2023-2024**: BH mass coupled to expansion (k=3.11±0.19)
- **S₈ tension**: Our 5.2% growth suppression bridges CMB/lensing gap
- **Planck low-ℓ anomaly**: Our ISW resonance explains it (Δχ²=32.9)

## Downloads Structure
Two PDFs available on the site:
1. **White Paper V5.0** (`cosmic_yoyo_v5_holographic.pdf`) - 4 pages, LaTeX, full-width figures
2. **Full Theory** (`oscillating_brane_theory_latest.pdf`) - 70 pages, all chapters

The old V4 white paper (`whitepaper_oscillating_brane.pdf`) has been DELETED.

## Common Commands
```bash
# Generate the big PDF
python3 scripts/generate_pdf.py

# Compile the white paper
cd paper && pdflatex cosmic_yoyo_prl.tex && pdflatex cosmic_yoyo_prl.tex
cp cosmic_yoyo_prl.pdf ../cosmic_yoyo_v5_holographic.pdf

# Verify PDF is clean of ghosts
pdftotext oscillating_brane_theory_latest.pdf - | grep -i "Ringermacher\|Point Unique\|NANOGrav.*doublet\|Block Universe\|Version 4\|Infinite Ocean"

# Build Jekyll site locally
bundle exec jekyll build
```

## Maintenance Checklist
- When editing theory content, check ALL source files listed in PDF generator
- After PDF generation, always verify with pdftotext grep for banned terms
- Run `black` and `isort` before committing Python code
- Never reference Ringermacher, Point Unique (0D), or GW doublets
- Keep downloads.md in sync with available PDFs
- Watch for CI auto-updating the PDF after your push

## Contact
- GitHub Issues: https://github.com/Teleadmin-ai/oscillating-brane-DM/issues
- Repository owner: @Teleadmin-ai
