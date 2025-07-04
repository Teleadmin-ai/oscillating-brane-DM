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
│   ├── brane_oscillation_1d.py # 1D radion field evolution prototype (NEW)
│   ├── growth_factor.py       # Structure formation calculations
│   ├── bayesian_analysis.py   # Model comparison
│   ├── kk_spectrum.py         # Kaluza-Klein mode analysis
│   ├── pta_echo.py           # Gravitational wave predictions
│   ├── generate_figures.py    # Figure generation script
│   └── generate_pdf.py        # PDF generation from all docs
├── docs/               # Technical documentation
│   ├── theoretical_foundations.md  # Rigorous mathematical framework (NEW)
│   └── theory_v4_complete.md      # Complete theory v4
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
- **Extra dimension size**: L = 2.0 × 10⁻⁷ m
- **Oscillating fraction**: f_osc = 0.10
- **MOND acceleration**: a₀ = 1.1 × 10⁻¹⁰ m/s²
- **Dark energy amplitude**: A_w ≃ 0.003 (±0.3% oscillation)

## Python Scripts
The repository includes comprehensive computational tools:
1. `brane_dynamics.py` - Membrane oscillation calculations (fixed dimensional consistency)
2. `brane_oscillation_1d.py` - 1D prototype for radion field evolution with energy conservation
3. `growth_factor.py` - Structure formation with oscillating w(z) (improved lookback time)
4. `bayesian_analysis.py` - Model comparison and evidence
5. `kk_spectrum.py` - Kaluza-Klein mode analysis
6. `pta_echo.py` - Gravitational wave predictions
7. `generate_figures.py` - Scientific visualization generation
8. `generate_pdf.py` - Comprehensive PDF generation with all documentation

## Blog Post Topics
1. Introduction to the universe as a vibrating membrane
2. How dark matter makes the universe vibrate
3. Cosmic chronology from inflation to current oscillations
4. Experimental tests and future predictions

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

## Maintenance Tasks
- Keep blog posts updated with latest theoretical developments
- Update predictions as new observational data arrives
- Maintain compatibility with GitHub Pages requirements
- Ensure all mathematical equations render correctly with MathJax
- Monitor GitHub Actions for any failures
- Update CLAUDE.md when significant changes are made

## Contact
- GitHub Issues: https://github.com/Teleadmin-ai/oscillating-brane-DM/issues
- Repository owner: @Teleadmin-ai