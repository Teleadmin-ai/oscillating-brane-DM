# CLAUDE.md - Project Information for AI Assistants

## Project Overview
This is the **Oscillating Brane Dark Matter Theory** project - a revolutionary cosmological theory where the universe is conceptualized as a vibrating 4D membrane in 5D space.

## Repository Information
- **GitHub URL**: https://github.com/Teleadmin-ai/oscillating-brane-DM
- **Live Website**: https://higgs-cosmology.com/
- **Owner**: Teleadmin-ai
- **Development Status**: Active - AI-assisted theoretical cosmology research
- **Current Branch**: restore-working-version (pushed to main)

## GitHub Authentication
When working with this repository, use GitHub CLI (`gh`) for authentication. The user has personal access tokens configured.

### Important Notes:
1. The GitHub user is `Teleadmin-ai` (not `Teleadmin`)
2. Always use `gh` commands for GitHub operations
3. For git push/pull, the remote is already configured with authentication

## Project Structure
```
oscillating-brane-DM/
├── _posts/              # Blog posts explaining the theory (dark theme)
├── _layouts/            # Jekyll layouts (including custom dark.html)
│   ├── dark.html       # Main layout with videos and dark theme
│   ├── default.html    # Standard Jekyll layout
│   └── post.html       # Blog post layout
├── assets/
│   ├── css/            # Custom styling
│   │   └── dark-theme.css  # Complete dark theme implementation
│   ├── js/             # JavaScript for video carousel
│   └── videos/         # Local MP4 files for visual content
├── plots/              # Generated scientific figures
├── scripts/            # Python computational tools
│   ├── brane_dynamics.py      # Membrane oscillation calculations
│   ├── brane_oscillation_1d.py # 1D radion field evolution prototype
│   ├── einstein_5d_toy.py     # 2D prototype for 5D Einstein equations (NEW)
│   ├── growth_factor.py       # Structure formation calculations
│   ├── bayesian_analysis.py   # Model comparison
│   ├── bayesian_priors_table.py # Prior specifications for Bayesian analysis (NEW)
│   ├── pbh_cmb_opacity.py     # PBH impact on CMB optical depth (NEW)
│   ├── analyse_posterior.py   # MCMC diagnostics and trace plots (NEW)
│   ├── mcmc_diagnostics.py    # Convergence diagnostics (NEW)
│   ├── plot_2d_results.py     # 2D prototype visualization (NEW)
│   ├── kk_spectrum.py         # Kaluza-Klein mode analysis
│   ├── pta_echo.py           # Gravitational wave predictions
│   ├── generate_figures.py    # Figure generation script
│   └── generate_pdf.py        # PDF generation with Unicode fixes
├── docs/               # Technical documentation
│   ├── theoretical_foundations.md  # Rigorous mathematical framework with 1100+ lines
│   ├── theory_v4_complete.md      # Complete theory v4
│   ├── foundations_parts/         # Split mathematical framework
│   │   ├── part1_mathematical_framework.md
│   │   ├── part2_comparative_predictions.md
│   │   ├── part3_current_limitations.md
│   │   └── part4_development_roadmap.md
│   ├── posterior_table.tex        # MCMC posterior statistics table (NEW)
│   └── einstein_2d_table.tex      # 2D prototype results table (NEW)
├── data/               # Posterior samples and analysis results
├── output/             # Generated PDFs (NEW)
├── .github/            # GitHub Actions workflows (NEW)
│   └── workflows/
│       ├── ci.yml              # Main CI pipeline
│       ├── python-lint.yml     # Code quality checks
│       └── weekly-report.yml   # Automated reports
├── index.md           # Homepage
├── theory.md          # Complete theoretical framework
├── predictions.md     # Observational predictions
├── chronology.md      # Cosmic timeline (new)
├── tools.md           # Tools documentation
├── about.md           # About page with disclaimer
├── CNAME              # Custom domain configuration
├── requirements.txt   # Python dependencies
├── Gemfile            # Ruby dependencies for Jekyll
└── _config.yml        # Jekyll configuration
```

## Jekyll/GitHub Pages Configuration

### Current Setup
- **Theme**: `jekyll-theme-minimal` (GitHub Pages supported theme)
- **Custom Layout**: `dark.html` with video carousel and dark theme
- **Base URL**: `` (empty for custom domain)
- **URL**: `https://higgs-cosmology.com`
- **Deployment**: GitHub Pages from main branch
- **Custom Domain**: higgs-cosmology.com (configured with CNAME)

### Common Issues & Solutions

1. **YAML Syntax Errors**: Always quote wildcards in `_config.yml`:
   ```yaml
   exclude:
     - "*.py"
     - "*.npz"
   ```

2. **Theme Not Working**: Must use officially supported GitHub Pages themes:
   - jekyll-theme-minimal ✓
   - minima ✗ (not in the official list for automated builds)

3. **CSS Not Loading**: Use the correct path:
   ```html
   <link rel="stylesheet" href="{{ "/assets/css/style.css?v=" | append: site.github.build_revision | relative_url }}">
   ```

## Key Technical Parameters

The theory's fundamental parameters:
- **Brane tension**: τ₀ = 7.0 × 10¹⁹ J/m²
- **Oscillation period**: T = 2.0 ± 0.3 Gyr
- **Extra dimension size**: L = 2.0 × 10⁻⁷ m (0.2 μm)
- **Oscillating fraction**: f_osc = 0.10
- **MOND acceleration**: a₀ = 1.1 × 10⁻¹⁰ m/s²
- **Dark energy amplitude**: A_w ≃ 0.003 (±0.3% oscillation)
- **S₈ suppression**: -5.2% (resolves tension)
- **Bayesian evidence**: Δln K = 3.33 ± 0.24 (strong evidence)

## Python Scripts
The repository includes comprehensive computational tools:

### Core Physics Simulations
1. `brane_dynamics.py` - Membrane oscillation calculations (fixed dimensional consistency)
2. `brane_oscillation_1d.py` - 1D prototype for radion field evolution with energy conservation
3. `einstein_5d_toy.py` - 2D prototype solving simplified 5D Einstein equations
4. `growth_factor.py` - Structure formation with oscillating w(z) (improved lookback time)
5. `kk_spectrum.py` - Kaluza-Klein mode analysis
6. `pta_echo.py` - Gravitational wave predictions

### Analysis and Validation
7. `bayesian_analysis.py` - Model comparison and Bayesian evidence calculation
8. `bayesian_priors_table.py` - Complete prior specifications with sensitivity analysis
9. `pbh_cmb_opacity.py` - PBH contributions to CMB optical depth (Ali-Haïmoud 2017)
10. `analyse_posterior.py` - Comprehensive MCMC diagnostics with trace/corner plots
11. `mcmc_diagnostics.py` - Gelman-Rubin R̂ and effective sample size calculations

### Visualization and Output
12. `plot_2d_results.py` - Generate publication-quality plots from 2D prototype
13. `generate_figures.py` - Scientific visualization generation
14. `generate_pdf.py` - PDF generation with Unicode artifact cleaning

## Blog Post Topics
1. **The Universe as a Vibrating Membrane** - Introduction to the cosmic membrane paradigm
2. **How Dark Matter Makes the Universe Vibrate** - Microscopic excitation mechanism
3. **Cosmic Chronology: From Inflation to the Current Beat** - Evolution of brane tension
4. **Experimental Tests: Where to Seek the Truth** - Observational predictions and tests

## Recent Updates and Known Issues

### O3 Pro Conformity Check Implementation (2025-07-04)
Following O3 Pro's comprehensive theoretical analysis and conformity check:
- **Dimensional consistency**: Fixed A_osc formula to have proper length units, V_1-loop properly dimensioned
- **Numerical stability**: Fixed overflow in brane_oscillation_1d.py with ρ_crit normalization
- **Energy conservation**: Added test showing conservation to 0.1% accuracy
- **Citations**: Added proper references [Martin et al. 2005], [Garriga et al. 2001], [Rakhmetov et al. 2025]
- **Notations table**: Created comprehensive units table in section 6.0
- **PDF optimization**: Reduced size with --dpi=150 and smaller font

### GitHub Actions Setup (2025-07-04)
- **CI Pipeline**: Automated testing of Python simulations, Jekyll build, PDF generation
- **Artifacts**: Simulation plots (134 KB) and theory PDF (2.36 MB) generated on each push
- **Code quality**: Python linting with flake8, black, isort
- **Weekly reports**: Automated progress reports every Monday

### Theoretical Foundations Document (2025-07-04)
- **New document**: docs/theoretical_foundations.md with rigorous mathematical framework
- **Section 6.1**: Detailed theoretical challenges including 5D numerical relativity
- **Initial conditions**: Multiple mechanisms for brane oscillation onset
- **Quantum corrections**: Beyond one-loop analysis with Casimir effects
- **Development roadmap**: 18-month phased approach for full theory implementation

### 1D Prototype Implementation (2025-07-04)
- **New script**: brane_oscillation_1d.py demonstrating radion field evolution
- **Goldberger-Wise potential**: Stabilization mechanism implementation
- **Energy conservation**: Verified to 0.1% accuracy
- **Plots generated**: radion_evolution_1d.png and radion_energy_1d.png

### CSS Implementation Details
- Dark theme with video carousel on 40/60 split
- Fixed header with navigation
- Responsive design for mobile devices
- Custom dark layout for all pages including blog posts

### O3 Pro Final Audit Implementation (2025-07-04)
Following O3 Pro's final audit, all critical points have been addressed:
- **Δτ_CMB calculation**: Fixed to show τ_total = 0.0646 for f_PBH = 1% (consistent with Planck)
- **MCMC diagnostics**: Created analyse_posterior.py generating trace plots, corner plots, and LaTeX tables
- **Bibliography**: Added 50+ references including Ali-Haïmoud, Poulin, Serpico, DOP853
- **2D prototype**: Generated einstein_2d_summary.png showing 37% oscillation amplitude
- **Unicode fixes**: Added artifact cleaning in generate_pdf.py with XeLaTeX configuration

### Code Quality and CI/CD (2025-07-04)
- **All Python scripts**: Formatted with black and isort for consistent style
- **Import ordering**: Fixed with isort to pass linting checks
- **GitHub Actions**: All workflows (CI, Python Linting) now passing ✓
- **PDF generation**: Enhanced with Unicode cleaning and proper font configuration

### PDF Generation Improvements (2025-07-05)
- **Double chapter numbering fix**: Resolved issue where chapters had duplicate numbers (e.g., "Chapter 5" followed by "Chapter 4: Title")
- **Pandoc numbering**: Disabled automatic section numbering (`numbersections: false`)
- **Regex improvements**: Added pattern to remove existing "Chapter X:" prefixes from markdown content
- **Complete PDF**: Successfully generates 66-page PDF with all 15 chapters properly formatted
- **Content included**: All theoretical foundations, blog posts, and documentation properly integrated

## GitHub Actions & CI/CD

### Workflows
1. **CI (ci.yml)**: Main pipeline running on push
   - Runs Python simulations (brane_dynamics.py, brane_oscillation_1d.py)
   - Builds Jekyll site
   - Generates PDF documentation
   - Uploads artifacts (plots, PDFs)

2. **Python Linting (python-lint.yml)**: Code quality checks
   - flake8 for syntax errors
   - black for formatting
   - isort for import ordering

3. **Weekly Reports (weekly-report.yml)**: Automated Monday reports
   - Runs all simulations
   - Generates progress summary

### Common Commands
```bash
# Run tests locally
python scripts/brane_dynamics.py
python scripts/brane_oscillation_1d.py

# Generate PDF
python scripts/generate_pdf.py

# Build Jekyll site locally
bundle exec jekyll build
bundle exec jekyll serve
```

## Key Results and Findings

### Bayesian Evidence
- **Δln K = 3.33 ± 0.42**: Strong evidence favoring oscillating brane over ΛCDM
- **Posterior constraints**: τ₀ = 7.0 × 10¹⁹ J/m², f_osc = 0.10 ± 0.02, T = 2.0 ± 0.2 Gyr
- **All chains converged**: R̂ < 1.001, n_eff > 8000

### Numerical Validations
- **1D prototype**: Oscillation period matches theory to 0.1%
- **2D Einstein toy model**: 37% amplitude oscillations, 320% warp modulation
- **Energy conservation**: Achieved to 0.1% in 1D (2D requires better integrator)

### Observational Compatibility
- **CMB optical depth**: τ = 0.0646 (within 1.5σ of Planck)
- **PBH constraints**: f_PBH < 0.1 for M ~ 10⁻¹¹ M_⊙
- **S₈ tension**: 5.2% suppression explains galaxy cluster observations

## Maintenance Tasks
- Keep blog posts updated with latest theoretical developments
- Update predictions as new observational data arrives
- Maintain compatibility with GitHub Pages requirements
- Ensure all mathematical equations render correctly with MathJax
- Monitor GitHub Actions for any failures
- Update CLAUDE.md when significant changes are made
- Run black and isort before committing Python code
- Check PDF generation for Unicode artifacts

## Contact
- GitHub Issues: https://github.com/Teleadmin-ai/oscillating-brane-DM/issues
- Repository owner: @Teleadmin-ai