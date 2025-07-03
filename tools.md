---
layout: dark
title: Computational Tools
permalink: /tools/
---

We provide a suite of Python tools for exploring the oscillating brane theory and computing its predictions.

## Quick Start

```python
from scripts.brane_dynamics import BraneOscillator

# Initialize with default parameters
brane = BraneOscillator(
    tau_0=7.0e19,  # Brane tension (J/m²)
    f_osc=0.10,    # Oscillating fraction
    T=2.0          # Period (Gyr)
)

# Calculate dark energy equation of state
z = 0.5  # redshift
w_de = brane.equation_of_state(z)
print(f"w(z={z}) = {w_de:.3f}")
```

## Available Scripts

### 1. Brane Dynamics Calculator
**File**: `scripts/brane_dynamics.py`

Computes membrane oscillations and dark energy equation of state.

```python
# Example: Plot w(z)
brane = BraneOscillator()
fig = brane.plot_equation_of_state(z_min=0, z_max=2)
```

**Key functions**:
- `equation_of_state(z)`: Calculate w(z) at given redshift
- `membrane_displacement(t)`: Compute brane position
- `gravitational_wave_spectrum(f)`: GW signature
- `growth_suppression()`: Structure formation effects

### 2. Growth Factor Calculator
**File**: `scripts/growth_factor.py`

Computes linear growth factor D₊(z) including oscillation effects.

```bash
# Command line usage
python scripts/growth_factor.py --redshift 0 0.5 1.0 --compare

# With exact ODE integration
python scripts/growth_factor.py --exact --redshift 0 1 2
```

**Features**:
- Fast fitting formula or exact ODE integration
- Comparison between oscillating and ΛCDM models
- S₈ parameter calculation

### 3. Bayesian Analysis
**File**: `scripts/bayesian_analysis.py`

Performs model comparison using MCMC and computes Bayesian evidence.

```python
from scripts.bayesian_analysis import BayesianAnalyzer

# Run analysis with your data
analyzer = BayesianAnalyzer(observational_data)
sampler = analyzer.run_mcmc(model='oscillating')
log_evidence, error = analyzer.compute_evidence(sampler)
```

**Capabilities**:
- MCMC sampling with emcee
- Evidence calculation
- Parameter constraints
- Model comparison statistics

## Interactive Notebooks

Coming soon: Jupyter notebooks for interactive exploration
- Parameter space visualization
- Real-time equation of state plotting
- Gravitational wave signal analysis
- Structure formation animations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Teleadmin-ai/oscillating-brane-DM.git
cd oscillating-brane-DM
```

2. Install dependencies:
```bash
pip install numpy scipy matplotlib emcee corner
```

3. Run example:
```bash
python scripts/brane_dynamics.py
```

## API Documentation

### BraneOscillator Class

```python
class BraneOscillator:
    def __init__(self, tau_0=7.0e19, f_osc=0.10, T=2.0, L=2.0e-7):
        """
        Parameters:
        - tau_0: Brane tension (J/m²)
        - f_osc: Oscillating DM fraction
        - T: Period (Gyr)
        - L: Extra dimension size (m)
        """
```

### GrowthFactorCalculator Class

```python
class GrowthFactorCalculator:
    def __init__(self, omega_m=0.315, oscillating=True, A_w=0.003):
        """
        Parameters:
        - omega_m: Matter density
        - oscillating: Include oscillations
        - A_w: w(z) amplitude
        """
```

## Contributing

We welcome contributions! Please submit pull requests for:
- New analysis tools
- Visualization improvements
- Performance optimizations
- Additional observational tests

See our [GitHub repository](https://github.com/{{ site.github_username }}/oscillating-brane-DM) for more details.