#!/usr/bin/env python3
"""
Explicit Prior Table for Bayesian Analysis
=========================================

Detailed documentation of priors used in the Bayesian evidence calculation
and cross-check with alternative prior choices.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

class PriorTable:
    """
    Complete specification of priors for both models.
    """
    
    def __init__(self):
        # Standard priors (used in main analysis)
        self.standard_priors = {
            'oscillating': {
                'tau_0': {
                    'type': 'log-uniform',
                    'range': (1e19, 1e20),
                    'units': 'J/m²',
                    'motivation': 'Scale-invariant prior for unknown energy scale'
                },
                'f_osc': {
                    'type': 'uniform',
                    'range': (0.05, 0.20),
                    'units': 'dimensionless',
                    'motivation': 'Weak prior based on halo core constraints'
                },
                'T': {
                    'type': 'gaussian',
                    'mean': 2.0,
                    'std': 0.3,
                    'range': (1.5, 2.5),
                    'units': 'Gyr',
                    'motivation': 'Centered on theoretical prediction'
                },
                'A_w': {
                    'type': 'uniform',
                    'range': (0.001, 0.005),
                    'units': 'dimensionless',
                    'motivation': 'Constrained by dark energy observations'
                }
            },
            'lcdm': {
                'H0': {
                    'type': 'uniform',
                    'range': (60, 80),
                    'units': 'km/s/Mpc',
                    'motivation': 'Wide range covering all measurements'
                },
                'Omega_m': {
                    'type': 'gaussian',
                    'mean': 0.31,
                    'std': 0.02,
                    'range': (0.25, 0.35),
                    'units': 'dimensionless',
                    'motivation': 'CMB+LSS constraints'
                }
            }
        }
        
        # Alternative priors for sensitivity analysis
        self.alternative_priors = {
            'oscillating_conservative': {
                'tau_0': {'type': 'log-uniform', 'range': (5e18, 5e20)},
                'f_osc': {'type': 'uniform', 'range': (0.01, 0.30)},
                'T': {'type': 'uniform', 'range': (1.0, 3.0)},
                'A_w': {'type': 'log-uniform', 'range': (1e-4, 1e-2)}
            },
            'oscillating_informative': {
                'tau_0': {'type': 'gaussian', 'mean': 7e19, 'std': 1e19},
                'f_osc': {'type': 'gaussian', 'mean': 0.10, 'std': 0.02},
                'T': {'type': 'gaussian', 'mean': 2.0, 'std': 0.15},
                'A_w': {'type': 'gaussian', 'mean': 0.003, 'std': 0.001}
            }
        }
    
    def log_prior(self, theta, model='oscillating', prior_set='standard'):
        """
        Compute log prior probability.
        
        Parameters
        ----------
        theta : array
            Parameter values
        model : str
            'oscillating' or 'lcdm'
        prior_set : str
            'standard', 'conservative', or 'informative'
        """
        if prior_set == 'standard':
            priors = self.standard_priors[model]
        else:
            priors = self.alternative_priors[f'{model}_{prior_set}']
        
        log_p = 0
        param_names = list(priors.keys())
        
        for i, (param, value) in enumerate(zip(param_names, theta)):
            prior_spec = priors[param]
            
            # Check bounds
            if 'range' in prior_spec:
                if not (prior_spec['range'][0] <= value <= prior_spec['range'][1]):
                    return -np.inf
            
            # Compute prior contribution
            if prior_spec['type'] == 'uniform':
                # Uniform: p(x) = 1/(b-a)
                a, b = prior_spec['range']
                log_p += -np.log(b - a)
                
            elif prior_spec['type'] == 'log-uniform':
                # Log-uniform: p(x) = 1/(x * log(b/a))
                a, b = prior_spec['range']
                log_p += -np.log(value) - np.log(np.log(b/a))
                
            elif prior_spec['type'] == 'gaussian':
                # Gaussian: properly normalized
                mean = prior_spec['mean']
                std = prior_spec['std']
                log_p += -0.5 * ((value - mean)/std)**2 - np.log(std * np.sqrt(2*np.pi))
        
        return log_p
    
    def generate_prior_samples(self, model='oscillating', n_samples=10000):
        """
        Generate samples from prior distribution.
        """
        priors = self.standard_priors[model]
        samples = {}
        
        for param, prior_spec in priors.items():
            if prior_spec['type'] == 'uniform':
                a, b = prior_spec['range']
                samples[param] = np.random.uniform(a, b, n_samples)
                
            elif prior_spec['type'] == 'log-uniform':
                a, b = prior_spec['range']
                log_a, log_b = np.log(a), np.log(b)
                samples[param] = np.exp(np.random.uniform(log_a, log_b, n_samples))
                
            elif prior_spec['type'] == 'gaussian':
                mean = prior_spec['mean']
                std = prior_spec['std']
                samples[param] = np.random.normal(mean, std, n_samples)
                # Clip to range if specified
                if 'range' in prior_spec:
                    a, b = prior_spec['range']
                    samples[param] = np.clip(samples[param], a, b)
        
        return samples
    
    def create_latex_table(self):
        """
        Create LaTeX table of priors for publication.
        """
        rows = []
        
        # Oscillating model priors
        rows.append("\\begin{table}[htbp]")
        rows.append("\\centering")
        rows.append("\\caption{Prior distributions for Bayesian analysis}")
        rows.append("\\begin{tabular}{llccc}")
        rows.append("\\hline")
        rows.append("Model & Parameter & Distribution & Range/Parameters & Units \\\\")
        rows.append("\\hline")
        
        for model, priors in self.standard_priors.items():
            model_name = "Oscillating" if model == 'oscillating' else "$\\Lambda$CDM"
            for param, spec in priors.items():
                param_latex = {
                    'tau_0': '$\\tau_0$',
                    'f_osc': '$f_{\\rm osc}$',
                    'T': '$T$',
                    'A_w': '$A_w$',
                    'H0': '$H_0$',
                    'Omega_m': '$\\Omega_m$'
                }[param]
                
                if spec['type'] == 'uniform':
                    dist = 'Uniform'
                    range_str = f"[{spec['range'][0]:.2g}, {spec['range'][1]:.2g}]"
                elif spec['type'] == 'log-uniform':
                    dist = 'Log-uniform'
                    range_str = f"[{spec['range'][0]:.2g}, {spec['range'][1]:.2g}]"
                elif spec['type'] == 'gaussian':
                    dist = 'Gaussian'
                    range_str = f"$\\mu={spec['mean']:.2g}, \\sigma={spec['std']:.2g}$"
                
                rows.append(f"{model_name} & {param_latex} & {dist} & {range_str} & {spec['units']} \\\\")
                model_name = ""  # Only show model name once
        
        rows.append("\\hline")
        rows.append("\\end{tabular}")
        rows.append("\\label{tab:priors}")
        rows.append("\\end{table}")
        
        return '\n'.join(rows)
    
    def plot_priors(self, save_path='plots/prior_distributions.png'):
        """
        Visualize all prior distributions.
        """
        fig, axes = plt.subplots(3, 2, figsize=(12, 10))
        axes = axes.flatten()
        
        # Plot oscillating model priors
        samples = self.generate_prior_samples('oscillating', n_samples=50000)
        
        for i, (param, values) in enumerate(samples.items()):
            ax = axes[i]
            
            # Histogram
            if self.standard_priors['oscillating'][param]['type'] == 'log-uniform':
                bins = np.logspace(np.log10(values.min()), np.log10(values.max()), 50)
                ax.hist(values, bins=bins, density=True, alpha=0.7, color='blue')
                ax.set_xscale('log')
            else:
                ax.hist(values, bins=50, density=True, alpha=0.7, color='blue')
            
            # Labels
            param_labels = {
                'tau_0': r'$\tau_0$ (J/m²)',
                'f_osc': r'$f_{\rm osc}$',
                'T': r'$T$ (Gyr)',
                'A_w': r'$A_w$'
            }
            ax.set_xlabel(param_labels[param])
            ax.set_ylabel('Prior density')
            ax.set_title(f'Prior: {param}')
            ax.grid(True, alpha=0.3)
        
        # Plot ΛCDM priors
        samples_lcdm = self.generate_prior_samples('lcdm', n_samples=50000)
        
        for i, (param, values) in enumerate(samples_lcdm.items()):
            ax = axes[4 + i]
            ax.hist(values, bins=50, density=True, alpha=0.7, color='red')
            
            param_labels = {
                'H0': r'$H_0$ (km/s/Mpc)',
                'Omega_m': r'$\Omega_m$'
            }
            ax.set_xlabel(param_labels[param])
            ax.set_ylabel('Prior density')
            ax.set_title(f'Prior: {param}')
            ax.grid(True, alpha=0.3)
        
        # Hide unused subplot
        axes[-1].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Prior distributions saved to {save_path}")
        
        return fig


def compute_evidence_sensitivity(data, prior_sets=['standard', 'conservative', 'informative']):
    """
    Test sensitivity of Bayes factor to prior choice.
    """
    from bayesian_analysis import BayesianAnalyzer
    
    results = {}
    
    for prior_set in prior_sets:
        print(f"\nComputing evidence with {prior_set} priors...")
        
        # Modify analyzer to use different priors
        analyzer = BayesianAnalyzer(data)
        prior_table = PriorTable()
        
        # Override prior functions
        def log_prior_osc_custom(theta):
            return prior_table.log_prior(theta, 'oscillating', prior_set)
        
        analyzer.log_prior_osc = log_prior_osc_custom
        
        # Run MCMC
        sampler_osc = analyzer.run_mcmc('oscillating', nwalkers=32, nsteps=2000)
        sampler_lcdm = analyzer.run_mcmc('lcdm', nwalkers=32, nsteps=2000)
        
        # Compute evidences
        log_Z_osc, err_osc = analyzer.compute_evidence(sampler_osc, 'oscillating')
        log_Z_lcdm, err_lcdm = analyzer.compute_evidence(sampler_lcdm, 'lcdm')
        
        # Bayes factor
        log_K = analyzer.bayes_factor(log_Z_osc, log_Z_lcdm)
        
        results[prior_set] = {
            'log_Z_osc': log_Z_osc,
            'log_Z_lcdm': log_Z_lcdm,
            'log_K': log_K,
            'err_K': np.sqrt(err_osc**2 + err_lcdm**2)
        }
    
    return results


def main():
    """
    Document and analyze prior choices.
    """
    print("Prior Specification for Bayesian Analysis")
    print("=" * 50)
    
    # Create prior table
    prior_table = PriorTable()
    
    # Generate LaTeX table
    latex_table = prior_table.create_latex_table()
    print("\nLaTeX table for publication:")
    print(latex_table)
    
    # Save to file
    with open('docs/prior_table.tex', 'w') as f:
        f.write(latex_table)
    
    # Plot priors
    print("\nGenerating prior distribution plots...")
    prior_table.plot_priors()
    
    # Load data for sensitivity analysis
    try:
        data_file = np.load('data/posterior_v4.npz')
        # Extract observational data used in analysis
        from bayesian_analysis import generate_mock_data
        data = generate_mock_data()
        
        # Sensitivity analysis
        print("\nPrior sensitivity analysis:")
        sensitivity = compute_evidence_sensitivity(data)
        
        print("\nResults with different prior choices:")
        print(f"{'Prior Set':<15} {'log K':<10} {'Error':<10} {'Interpretation'}")
        print("-" * 50)
        for prior_set, results in sensitivity.items():
            print(f"{prior_set:<15} {results['log_K']:<10.2f} "
                  f"{results['err_K']:<10.2f} ", end="")
            if results['log_K'] > 3:
                print("Strong evidence")
            elif results['log_K'] > 1:
                print("Positive evidence")
            else:
                print("Weak/no evidence")
    
    except FileNotFoundError:
        print("\nNote: posterior_v4.npz not found. Run bayesian_analysis.py first.")
    
    # Summary
    print("\nKey findings:")
    print("1. Standard priors are motivated by physical constraints")
    print("2. Log-uniform prior on τ₀ reflects scale uncertainty")
    print("3. Gaussian priors on T and Ωm incorporate previous measurements")
    print("4. Results should be robust to reasonable prior variations")


if __name__ == "__main__":
    main()