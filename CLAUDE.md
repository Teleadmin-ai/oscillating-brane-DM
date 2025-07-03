# CLAUDE.md - Project Information for AI Assistants

## Project Overview
This is the **Oscillating Brane Dark Matter Theory** project - a revolutionary cosmological theory where the universe is conceptualized as a vibrating 4D membrane in 5D space.

## Repository Information
- **GitHub URL**: https://github.com/Teleadmin-ai/oscillating-brane-DM
- **GitHub Pages URL**: https://teleadmin-ai.github.io/oscillating-brane-DM/
- **Owner**: Teleadmin-ai

## GitHub Authentication
When working with this repository, use GitHub CLI (`gh`) for authentication. The user has personal access tokens configured.

### Important Notes:
1. The GitHub user is `Teleadmin-ai` (not `Teleadmin`)
2. Always use `gh` commands for GitHub operations
3. For git push/pull, the remote is already configured with authentication

## Project Structure
```
oscillating-brane-DM/
├── _posts/              # Blog posts explaining the theory
├── _layouts/            # Jekyll layouts
├── assets/css/          # Custom styling
├── docs/                # Technical documentation
├── scripts/             # Python computational tools
├── index.md            # Homepage
├── theory.md           # Theory page
├── predictions.md      # Predictions page
├── tools.md            # Tools documentation
├── about.md            # About page
└── _config.yml         # Jekyll configuration
```

## Jekyll/GitHub Pages Configuration

### Current Setup
- **Theme**: `jekyll-theme-minimal` (GitHub Pages supported theme)
- **Base URL**: `/oscillating-brane-DM`
- **Deployment**: GitHub Pages from main branch

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

## Python Scripts
The repository includes three main computational tools:
1. `brane_dynamics.py` - Membrane oscillation calculations
2. `growth_factor.py` - Structure formation with oscillating w(z)
3. `bayesian_analysis.py` - Model comparison and evidence

## Blog Post Topics
1. Introduction to the universe as a vibrating membrane
2. How dark matter makes the universe vibrate
3. Cosmic chronology from inflation to current oscillations
4. Experimental tests and future predictions

## Maintenance Tasks
- Keep blog posts updated with latest theoretical developments
- Update predictions as new observational data arrives
- Maintain compatibility with GitHub Pages requirements
- Ensure all mathematical equations render correctly with MathJax

## Contact
- GitHub Issues: https://github.com/Teleadmin-ai/oscillating-brane-DM/issues
- Repository owner: @Teleadmin-ai