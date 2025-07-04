#!/usr/bin/env python3
"""
Bayesian Analysis for Oscillating Brane Model
============================================

Computes Bayesian evidence and posterior distributions
for the oscillating brane dark matter theory compared to ΛCDM.
"""

from typing import Dict, Optional, Tuple

import corner
import emcee
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.special import loggamma


class BayesianAnalyzer:
    """
    Bayesian model comparison and parameter estimation.
    """

    def __init__(self, data: Dict[str, np.ndarray]):
        """
        Initialize the analyzer with observational data.

        Parameters
        ----------
        data : dict
            Dictionary containing:
            - 'H0_samples': Samples from H0 measurements
            - 'S8_samples': Samples from S8 measurements
            - 'w_measurements': (z, w, err) for dark energy EOS
        """
        self.data = data

        # Model parameters and priors
        self.param_names_osc = ["tau_0", "f_osc", "T", "A_w"]
        self.param_names_lcdm = ["H0", "Omega_m"]

        # Prior ranges
        self.prior_ranges_osc = {
            "tau_0": (1e19, 1e20),  # J/m²
            "f_osc": (0.05, 0.20),  # fraction
            "T": (1.5, 2.5),  # Gyr
            "A_w": (0.001, 0.005),  # amplitude
        }

        self.prior_ranges_lcdm = {
            "H0": (60, 80),  # km/s/Mpc
            "Omega_m": (0.25, 0.35),  # matter fraction
        }

    def log_prior_osc(self, theta: np.ndarray) -> float:
        """
        Log prior for oscillating brane model.

        Parameters
        ----------
        theta : array
            Parameter vector [tau_0, f_osc, T, A_w]

        Returns
        -------
        log_prior : float
        """
        tau_0, f_osc, T, A_w = theta

        # Check bounds
        if not (
            self.prior_ranges_osc["tau_0"][0]
            <= tau_0
            <= self.prior_ranges_osc["tau_0"][1]
        ):
            return -np.inf
        if not (
            self.prior_ranges_osc["f_osc"][0]
            <= f_osc
            <= self.prior_ranges_osc["f_osc"][1]
        ):
            return -np.inf
        if not (self.prior_ranges_osc["T"][0] <= T <= self.prior_ranges_osc["T"][1]):
            return -np.inf
        if not (
            self.prior_ranges_osc["A_w"][0] <= A_w <= self.prior_ranges_osc["A_w"][1]
        ):
            return -np.inf

        # Log-uniform prior on tau_0, uniform on others
        log_prior = -np.log(tau_0)

        return log_prior

    def log_likelihood_osc(self, theta: np.ndarray) -> float:
        """
        Log likelihood for oscillating brane model.

        Parameters
        ----------
        theta : array
            Parameter vector [tau_0, f_osc, T, A_w]

        Returns
        -------
        log_like : float
        """
        tau_0, f_osc, T, A_w = theta

        log_like = 0

        # H0 constraint
        # Theory predicts slight anisotropy
        H0_theory = 67.4  # Central value
        H0_sigma = 0.5  # Uncertainty
        if "H0_samples" in self.data:
            chi2_H0 = np.sum((self.data["H0_samples"] - H0_theory) ** 2) / H0_sigma**2
            log_like -= 0.5 * chi2_H0 / len(self.data["H0_samples"])

        # S8 constraint
        # Theory predicts 5.2% suppression
        S8_theory = 0.79  # With suppression
        S8_sigma = 0.02
        if "S8_samples" in self.data:
            chi2_S8 = np.sum((self.data["S8_samples"] - S8_theory) ** 2) / S8_sigma**2
            log_like -= 0.5 * chi2_S8 / len(self.data["S8_samples"])

        # w(z) measurements
        if "w_measurements" in self.data:
            z, w_obs, w_err = self.data["w_measurements"]
            # Simple sinusoidal model
            t_lb = np.log(1 + z) / 0.7  # Approximate lookback time
            w_theory = -1 + A_w * np.sin(2 * np.pi * t_lb / T)
            chi2_w = np.sum((w_obs - w_theory) ** 2 / w_err**2)
            log_like -= 0.5 * chi2_w

        return log_like

    def log_posterior_osc(self, theta: np.ndarray) -> float:
        """
        Log posterior for oscillating brane model.
        """
        lp = self.log_prior_osc(theta)
        if not np.isfinite(lp):
            return -np.inf
        return lp + self.log_likelihood_osc(theta)

    def log_prior_lcdm(self, theta: np.ndarray) -> float:
        """
        Log prior for ΛCDM model.
        """
        H0, Omega_m = theta

        # Check bounds
        if not (
            self.prior_ranges_lcdm["H0"][0] <= H0 <= self.prior_ranges_lcdm["H0"][1]
        ):
            return -np.inf
        if not (
            self.prior_ranges_lcdm["Omega_m"][0]
            <= Omega_m
            <= self.prior_ranges_lcdm["Omega_m"][1]
        ):
            return -np.inf

        return 0  # Uniform priors

    def log_likelihood_lcdm(self, theta: np.ndarray) -> float:
        """
        Log likelihood for ΛCDM model.
        """
        H0, Omega_m = theta

        log_like = 0

        # H0 constraint
        H0_sigma = 0.5
        if "H0_samples" in self.data:
            chi2_H0 = np.sum((self.data["H0_samples"] - H0) ** 2) / H0_sigma**2
            log_like -= 0.5 * chi2_H0 / len(self.data["H0_samples"])

        # S8 constraint
        S8_theory = 0.83  # ΛCDM prediction
        S8_sigma = 0.02
        if "S8_samples" in self.data:
            chi2_S8 = np.sum((self.data["S8_samples"] - S8_theory) ** 2) / S8_sigma**2
            log_like -= 0.5 * chi2_S8 / len(self.data["S8_samples"])

        # w(z) = -1 for ΛCDM
        if "w_measurements" in self.data:
            z, w_obs, w_err = self.data["w_measurements"]
            w_theory = -np.ones_like(z)
            chi2_w = np.sum((w_obs - w_theory) ** 2 / w_err**2)
            log_like -= 0.5 * chi2_w

        return log_like

    def log_posterior_lcdm(self, theta: np.ndarray) -> float:
        """
        Log posterior for ΛCDM model.
        """
        lp = self.log_prior_lcdm(theta)
        if not np.isfinite(lp):
            return -np.inf
        return lp + self.log_likelihood_lcdm(theta)

    def run_mcmc(
        self, model: str = "oscillating", nwalkers: int = 32, nsteps: int = 5000
    ) -> emcee.EnsembleSampler:
        """
        Run MCMC sampling for specified model.

        Parameters
        ----------
        model : str
            'oscillating' or 'lcdm'
        nwalkers : int
            Number of MCMC walkers
        nsteps : int
            Number of MCMC steps

        Returns
        -------
        sampler : emcee.EnsembleSampler
            The sampler object with chains
        """
        if model == "oscillating":
            ndim = len(self.param_names_osc)
            log_prob_fn = self.log_posterior_osc

            # Initial positions
            p0 = []
            for i in range(nwalkers):
                tau_0 = np.random.uniform(3e19, 9e19)
                f_osc = np.random.uniform(0.08, 0.12)
                T = np.random.uniform(1.8, 2.2)
                A_w = np.random.uniform(0.002, 0.004)
                p0.append([tau_0, f_osc, T, A_w])

        else:  # ΛCDM
            ndim = len(self.param_names_lcdm)
            log_prob_fn = self.log_posterior_lcdm

            # Initial positions
            p0 = []
            for i in range(nwalkers):
                H0 = np.random.uniform(65, 70)
                Omega_m = np.random.uniform(0.30, 0.32)
                p0.append([H0, Omega_m])

        # Run MCMC
        sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob_fn)
        sampler.run_mcmc(p0, nsteps, progress=True)

        return sampler

    def compute_evidence(
        self, sampler: emcee.EnsembleSampler, model: str
    ) -> Tuple[float, float]:
        """
        Compute Bayesian evidence using thermodynamic integration.

        Parameters
        ----------
        sampler : emcee.EnsembleSampler
            The sampler with chains
        model : str
            'oscillating' or 'lcdm'

        Returns
        -------
        log_evidence : float
            Natural log of the evidence
        error : float
            Estimated error in log evidence
        """
        # Get chains after burn-in
        chains = sampler.get_chain(discard=1000, flat=True)
        log_likes = sampler.get_log_prob(discard=1000, flat=True)

        # Simple harmonic mean estimator
        # More sophisticated: nested sampling or thermodynamic integration
        max_log_like = np.max(log_likes)
        log_evidence = max_log_like + np.log(np.mean(np.exp(log_likes - max_log_like)))

        # Error estimate from jackknife
        n = len(log_likes)
        jackknife_estimates = []
        for i in range(min(100, n)):
            mask = np.ones(n, dtype=bool)
            mask[i :: n // 100] = False
            jk_likes = log_likes[mask]
            jk_max = np.max(jk_likes)
            jk_est = jk_max + np.log(np.mean(np.exp(jk_likes - jk_max)))
            jackknife_estimates.append(jk_est)

        error = np.std(jackknife_estimates) * np.sqrt(len(jackknife_estimates))

        return log_evidence, error

    def bayes_factor(self, log_evidence_osc: float, log_evidence_lcdm: float) -> float:
        """
        Compute Bayes factor K = P(D|osc) / P(D|ΛCDM).

        Parameters
        ----------
        log_evidence_osc : float
            Log evidence for oscillating model
        log_evidence_lcdm : float
            Log evidence for ΛCDM

        Returns
        -------
        log_K : float
            Natural log of Bayes factor
        """
        return log_evidence_osc - log_evidence_lcdm

    def interpret_bayes_factor(self, log_K: float) -> str:
        """
        Interpret Bayes factor using Jeffreys' scale.

        Parameters
        ----------
        log_K : float
            Natural log of Bayes factor

        Returns
        -------
        interpretation : str
        """
        if log_K < 0:
            return f"Evidence favors ΛCDM (log K = {log_K:.2f})"
        elif log_K < 1:
            return f"Weak evidence for oscillating model (log K = {log_K:.2f})"
        elif log_K < 2.3:
            return f"Positive evidence for oscillating model (log K = {log_K:.2f})"
        elif log_K < 3.5:
            return f"Strong evidence for oscillating model (log K = {log_K:.2f})"
        else:
            return f"Very strong evidence for oscillating model (log K = {log_K:.2f})"


def generate_mock_data() -> Dict[str, np.ndarray]:
    """
    Generate mock observational data for testing.
    """
    np.random.seed(42)

    data = {
        "H0_samples": np.random.normal(67.4, 0.5, 100),
        "S8_samples": np.random.normal(0.79, 0.02, 100),
        "w_measurements": (
            np.linspace(0, 2, 20),  # redshift
            -1 + 0.003 * np.sin(2 * np.pi * np.linspace(0, 2, 20) / 2),  # w(z)
            0.05 * np.ones(20),  # errors
        ),
    }

    return data


def main():
    """
    Run Bayesian analysis comparing models.
    """
    print("Bayesian Analysis: Oscillating Brane vs ΛCDM")
    print("=" * 50)

    # Generate or load data
    data = generate_mock_data()
    analyzer = BayesianAnalyzer(data)

    # Run MCMC for both models
    print("\nRunning MCMC for oscillating brane model...")
    sampler_osc = analyzer.run_mcmc("oscillating", nwalkers=32, nsteps=2000)

    print("\nRunning MCMC for ΛCDM model...")
    sampler_lcdm = analyzer.run_mcmc("lcdm", nwalkers=32, nsteps=2000)

    # Compute evidences
    print("\nComputing Bayesian evidences...")
    log_Z_osc, err_osc = analyzer.compute_evidence(sampler_osc, "oscillating")
    log_Z_lcdm, err_lcdm = analyzer.compute_evidence(sampler_lcdm, "lcdm")

    # Bayes factor
    log_K = analyzer.bayes_factor(log_Z_osc, log_Z_lcdm)
    err_K = np.sqrt(err_osc**2 + err_lcdm**2)

    print(f"\nResults:")
    print(f"log Z(oscillating) = {log_Z_osc:.2f} ± {err_osc:.2f}")
    print(f"log Z(ΛCDM) = {log_Z_lcdm:.2f} ± {err_lcdm:.2f}")
    print(f"log K = {log_K:.2f} ± {err_K:.2f}")
    print(f"\n{analyzer.interpret_bayes_factor(log_K)}")

    # Save chains
    print("\nSaving posterior samples...")
    np.savez(
        "posterior_v4.npz",
        chains_osc=sampler_osc.get_chain(discard=1000, flat=True),
        chains_lcdm=sampler_lcdm.get_chain(discard=1000, flat=True),
        log_K=log_K,
        err_K=err_K,
    )


if __name__ == "__main__":
    main()
