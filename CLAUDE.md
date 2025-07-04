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
│   ├── growth_factor.py       # Structure formation calculations
│   ├── bayesian_analysis.py   # Model comparison
│   ├── kk_spectrum.py         # Kaluza-Klein mode analysis
│   ├── pta_echo.py           # Gravitational wave predictions
│   └── generate_figures.py    # Figure generation script
├── docs/               # Technical documentation (PDFs, theory details)
├── data/               # Posterior samples and analysis results
├── index.md           # Homepage
├── theory.md          # Complete theoretical framework
├── predictions.md     # Observational predictions
├── chronology.md      # Cosmic timeline (new)
├── tools.md           # Tools documentation
├── about.md           # About page with disclaimer
├── CNAME              # Custom domain configuration
├── requirements.txt   # Python dependencies
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
2. `growth_factor.py` - Structure formation with oscillating w(z) (improved lookback time)
3. `bayesian_analysis.py` - Model comparison and evidence
4. `kk_spectrum.py` - Kaluza-Klein mode analysis
5. `pta_echo.py` - Gravitational wave predictions
6. `generate_figures.py` - Scientific visualization generation

## Blog Post Topics
1. Introduction to the universe as a vibrating membrane
2. How dark matter makes the universe vibrate
3. Cosmic chronology from inflation to current oscillations
4. Experimental tests and future predictions

## Recent Updates and Known Issues

### Version 4.0.2 Editorial Corrections (2025-07-04)
Following comprehensive o3 pro audit:
- **H₀ anisotropy**: Harmonized to ~0.01% (was inconsistently showing 1.5%)
- **arXiv placeholder**: Changed to "in preparation, 2025"
- **README H0LiCOW++**: Updated to 0.1% anisotropy threshold

### Scientific Corrections (2025-07-04)
Based on thorough scientific review:
- **Kaluza-Klein mass**: Corrected from 10⁻³ eV to 1 eV (consistent with L = 0.2 μm)
- **PBH mass**: Corrected from 10⁻¹² M_⊙ to 10⁻¹¹ M_⊙ (to match r_s ≈ 30 nm)
- **K_MW notation**: Clarified as local tension contrast δτ/τ₀ ≈ 2×10⁻⁴
- **GitHub links**: Updated from YoyoCosmo to Teleadmin-ai repository

### Header Overlap Fix (2025-07-04)
- Increased content-wrapper padding-top to 200px
- Added text-content padding-top of 40px
- Ensures first line of text is fully visible below fixed header

### CSS Implementation Details
- Dark theme with video carousel on 40/60 split
- Fixed header with navigation
- Responsive design for mobile devices
- Custom dark layout for all pages including blog posts

## Maintenance Tasks
- Keep blog posts updated with latest theoretical developments
- Update predictions as new observational data arrives
- Maintain compatibility with GitHub Pages requirements
- Ensure all mathematical equations render correctly with MathJax
- Monitor header spacing to prevent text overlap

## Contact
- GitHub Issues: https://github.com/Teleadmin-ai/oscillating-brane-DM/issues
- Repository owner: @Teleadmin-ai