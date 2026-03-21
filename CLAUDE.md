# CLAUDE.md - Project Information for AI Assistants

## Project Overview
**Oscillating Brane Dark Matter Theory V6.0 (Stick-Slip Motor Edition)** - The universe is a vibrating 4D membrane in 5D AdS space, driven by a non-linear stick-slip relaxation motor with ER=EPR holographic entanglement.

**Author**: Romain Provencal (provencal.romain@teleadmin.net) - Independent conceptual researcher
**AI Collaborators**: Claude (Anthropic) & Gemini DeepThink (Google) as theoretical co-processors

## Repository
- **GitHub**: https://github.com/Teleadmin-ai/oscillating-brane-DM
- **Website**: https://higgs-cosmology.com/
- **Owner**: Teleadmin-ai (NOT "Teleadmin")
- **Version**: V6.0 Stick-Slip Motor (March 2026)

## CRITICAL: Theory V6.0 Paradigm

### Core Physics:
- **Bulk**: Non-local topological state, spacetime is emergent (Van Raamsdonk 2010)
- **Connectivity**: ER=EPR wormhole network (Maldacena & Susskind 2013)
- **Oscillation ODE** (stick-slip, NOT harmonic):
  `φ̈ + 3Hφ̇ + ∂V_GW/∂φ = γṀ_DM - R(φ,φ̇)Θ(|φ|-φ_crit)`
  - Stick phase: CV forcing charges φ toward φ_crit
  - Slip phase: Threshold release snaps brane back
  - Survives Hubble friction because continuously driven
- **Forcing term** (γṀ_DM): Formalized via **holographic thermodynamics** — entropic force F_ent = T_bulk ∇S_ent from wormhole volume growth. Not ad-hoc but strict thermodynamic backreaction of bulk information processing
- **Dark energy**: w(z) = -1 + A_w sin(2πt_lb/T + φ₀) with **φ₀ = π/2** → w_a < 0 (DESI)
- **S₈ suppression**: Via G_eff = G_N × e^{-2k|z|}, adjustable via ⟨z²⟩
- **Quantum stability**: Adiabatic theorem (ν_brane/ν_KK ~ 10⁻³¹) + CV forcing double guarantee
- **QCD connection**: τ₀ = 0.017 GeV³, τ₀^{1/3} = 257 MeV ≈ Λ_QCD. Sets both tension AND φ_crit
- **ISW resonance**: CMB ℓ = 10-20, Δχ² = 32.9 (6σ)
- **Anchors**: Micro-PBHs (~10⁻¹² M☉, r_s ~ 3-30 nm) are the **SOLE** topological capillaries. r_s/L ~ 0.01-0.15
- **Warped Shielding**: 320% warp in (1+1)D prototypes = dimensional reduction artifact. In (3+1)+1D, QCD-scale tension acts as geometric low-pass filter (Israel junction conditions). Macroscopic w(z) stays at A_w ~ O(10⁻³)

### Epistemological Framework:
- **3 established anomalies resolved**: DESI phantom crossing, S₈ tension, Planck ISW
- **2 retroactive conditional predictions**: CatWISE dipole + EDGES 21cm
  - If confirmed: additional validations
  - If refuted (SARAS 3, kinematic systematics): model structurally intact
  - Definitive falsification deferred to **SKA** (21cm modulation) and **Vera Rubin/LSST** (structural anisotropies)
- **Laboratory test**: MORRIS experiment at sub-micron scales

### BANNED Concepts (NEVER use):
- "Point Unique" 0D, Ringermacher, GW doublet/NANOGrav, Bulk-Infinity/Two Limiting Visions/Convergent Funnels
- "Block Universe", "tiny hammers"/"momentum hit"/"dark matter impacts"
- "Simple harmonic oscillator"/"SHO"/"z = z_max sin(ωt)" as the dynamics
- "T = 2π√(f_osc M_DM/τ₀)" as exact formula
- JWST LRDs as anchors (Chisholm 2026: may be stellar clusters)
- "PBHs could enhance" (speculative) — they ARE the sole anchors
- τ₀ = 2.2 × 10⁻⁵ GeV³ (wrong), contact@higgs-cosmology.com (nonexistent)
- w(z) without phase φ₀, Version 4/5 references
- EDGES/CatWISE presented as **firm** confirmations (must be "retroactive conditional")
- γṀ_DM described as "ad-hoc" (it is thermodynamic backreaction)

### Key References:
Maldacena & Susskind 2013, Van Raamsdonk 2010, Susskind CV conjecture, Brownsberger 2020, DESI 2024/2026, Farrah 2023, Chisholm 2026, Secrest 2021/2022, Bowman 2018 (EDGES), Goldberger & Wise 1999, Carr 2016

## Key Parameters
| Parameter | Value |
|-----------|-------|
| Brane tension τ₀ | 7.0 × 10¹⁹ J/m² = 0.017 GeV³ |
| Energy scale | τ₀^{1/3} = 257 MeV ≈ Λ_QCD |
| Period T | 2.0 ± 0.3 Gyr (stick + slip) |
| Phase φ₀ | π/2 (at w maximum → w_a < 0) |
| Extra dimension L | 0.2 μm (NEVER "0.2 m") |
| φ_crit | ~0.1 L (QCD threshold) |
| f_osc | 0.10 |
| MOND a₀ | 1.1 × 10⁻¹⁰ m/s² (ALWAYS negative exp) |
| A_w | 0.003 |
| S₈ suppression | ~5.2% via G_eff (adjustable) |
| ISW Δχ² | 32.9 (6σ) |
| Micro-PBH | ~10⁻¹² M☉, r_s ~ 3 nm |

## PDF Generation — Race Condition
CI auto-pushes PDF. After modifying .md files:
1. `python3 scripts/generate_pdf.py`
2. Verify: `pdftotext oscillating_brane_theory_latest.pdf - | grep -i "GHOST"`
3. Resolve conflicts: `git checkout --ours oscillating_brane_theory_latest.pdf`

### Source files for PDF (in order):
```
index.md, theory.md, chronology.md, predictions.md, tools.md, about.md,
docs/theory_v4_complete.md, docs/foundations_parts/part1-4, _posts/*.md (5)
```

### Ghost grep:
```bash
pdftotext oscillating_brane_theory_latest.pdf - | grep -i "Ringermacher\|Point Unique\|tiny hammers\|momentum hit\|NANOGrav\|Block Universe\|Version 4\|Version 5\|Infinite Ocean\|dark matter impacts\|simple harmonic\|LRDs.*anchor"
```

## Downloads
1. **White Paper** (`cosmic_yoyo_v5_holographic.pdf`) — 5 pages, 15 refs (filename kept for link stability)
2. **Full Theory** (`oscillating_brane_theory_latest.pdf`) — 77 pages

## Human-AI Collaboration
Romain = conceptual architect (Faraday). AI = mathematical co-processors (Maxwell). Radically transparent acknowledgments. Never minimize AI involvement.

## Contact
- provencal.romain@teleadmin.net
- https://github.com/Teleadmin-ai/oscillating-brane-DM/issues
