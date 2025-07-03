---
layout: dark
title: Complete Theoretical Framework
permalink: /theory/
---

The oscillating brane dark matter theory represents a paradigm shift in our understanding of the cosmos. Here we present the complete mathematical framework and physical insights.

## Core Concepts

### The Brane Universe
Our 4D spacetime is an elastic membrane floating in a 5D bulk. This isn't merely a mathematical abstraction—it's the fundamental nature of reality.

### Gravitational Funnels
Black holes serve as conduits between our brane and the bulk, allowing dark matter to oscillate through the extra dimension.

### Fundamental Oscillation
The entire universe vibrates as a single entity with a period of approximately 2 billion years, creating the effects we attribute to dark energy.

## Mathematical Framework

### Microscopic Excitation

The surface pressure induced by dark matter impacts writes:

$$\Pi(t) = \sum_i \dot{N}_i m_{MN} v_{\perp} \simeq f_{osc} \rho_{DM} v_{\perp}^2 [1 + \sin(\omega_0 t)]$$

Key features:
- **Coherent phase**: Bulk crossing time ≪ 1 Gyr ensures identical phase across the sky
- **ℓ=0 selectivity**: The coupling integral $$\int Y_{\ell m} d\Omega$$ vanishes for ℓ > 0
- **Fundamental mode dominance**: Only the spherically symmetric mode is excited

### Energy of the Membrane

The deformation energy of the cosmic membrane is:

$$E_{tens} = \frac{1}{2} τ_0 A \left(\frac{2πz}{λ}\right)^2$$

Where:
- τ₀ = 7.0 × 10¹⁹ J/m² is the brane tension
- A ≃ R_H² is the area of the observable universe
- z is the displacement in the extra dimension
- λ ≃ 2R_H is the fundamental wavelength

### Dark Energy Equation of State

The oscillating membrane creates a time-varying dark energy:

$$w(z) = -1 + A_w \sin\left(\frac{2π t_{lb}(z)}{T}\right)$$

With amplitude A_w ≃ 0.003 and period T = 2.0 Gyr.

### Modified Gravity

At low accelerations, the membrane's properties create MOND-like effects:

$$a_0 = \frac{cH_0}{2π} × ξ ≃ 1.1 × 10^{-10} \text{ m/s}^2$$

## Stability and Higher Resonances

### Mode Damping Analysis

The coupling factor for higher modes scales as:

$$g_{\ell} \propto [\omega_{\ell}^2 - \omega_0^2]^{-1}$$

For the ℓ=2 mode: $$g_2/g_0 \sim (3\omega_0^2)^{-1} \approx 0.11$$

With Kelvin-Voigt damping γ ~ 10⁻² Gyr⁻¹:
- Fundamental mode Q-factor: Q₀ > 200
- First harmonic: Q₁ < 4
- **Result**: The fundamental mode dominates by factor > 50

### Why Only ℓ=0 Survives

1. **Geometric coupling**: Dark matter flux is isotropic, coupling only to spherically symmetric modes
2. **Damping hierarchy**: Higher modes experience stronger dissipation
3. **Energy cascade**: Non-linear interactions transfer energy to ℓ=0

## Key Predictions

1. **Oscillating dark energy** detectable by Euclid and DESI
2. **Gravitational wave signature** at f₀ ≈ 1.6 × 10⁻¹⁷ Hz
3. **Growth suppression** reconciling Planck and weak lensing
4. **Hubble anisotropy** mapping cosmic tension variations

## Further Reading

- [Introduction to the Universe as a Membrane]({{ site.baseurl }}{% post_url 2024-01-15-introduction-universe-membrane %})
- [How Dark Matter Excites the Membrane]({{ site.baseurl }}{% post_url 2024-01-16-microscopic-excitation %})
- [Cosmic Evolution and Chronology]({{ site.baseurl }}{% post_url 2024-01-17-cosmic-chronology %})
- [Experimental Tests and Predictions]({{ site.baseurl }}{% post_url 2024-01-18-observational-tests %})

For the complete mathematical derivations and detailed analysis, see our [technical documentation](https://github.com/{{ site.github_username }}/oscillating-brane-DM/tree/main/docs).