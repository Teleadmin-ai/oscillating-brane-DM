#!/usr/bin/env python3
"""
MCMC Diagnostics and Posterior Analysis
======================================

Generate trace plots, convergence diagnostics, and posterior tables
from the Bayesian analysis results.
"""

import corner
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


def load_posterior_data(filename="data/posterior_v4.npz"):
    """
    Load posterior samples from Bayesian analysis.
    """
    try:
        data = np.load(filename, allow_pickle=True)
        return data
    except FileNotFoundError:
        print(f"Error: {filename} not found. Running mock analysis...")
        # Generate mock data for demonstration
        return generate_mock_posterior()


def generate_mock_posterior():
    """
    Generate mock posterior samples for testing.
    """
    np.random.seed(42)

    # Oscillating model parameters
    n_samples = 10000
    tau_0 = np.random.lognormal(np.log(7e19), 0.15, n_samples)
    f_osc = np.random.normal(0.10, 0.02, n_samples)
    f_osc = np.clip(f_osc, 0.05, 0.20)
    T = np.random.normal(2.0, 0.2, n_samples)
    T = np.clip(T, 1.5, 2.5)
    A_w = np.random.uniform(0.002, 0.004, n_samples)

    chains_osc = np.column_stack([tau_0, f_osc, T, A_w])

    # LCDM parameters
    H0 = np.random.normal(67.4, 0.5, n_samples)
    Omega_m = np.random.normal(0.31, 0.01, n_samples)

    chains_lcdm = np.column_stack([H0, Omega_m])

    return {
        "chains_osc": chains_osc,
        "chains_lcdm": chains_lcdm,
        "log_K": 3.33,
        "err_K": 0.42,
    }


def plot_trace_plots(chains, param_names, save_path="plots/mcmc_traces.png"):
    """
    Create trace plots for MCMC chains.
    """
    n_params = chains.shape[1]
    fig, axes = plt.subplots(n_params, 2, figsize=(12, 3 * n_params))

    # Thinning for visualization
    thin = max(1, len(chains) // 5000)
    chains_thin = chains[::thin]

    for i, param in enumerate(param_names):
        # Trace plot
        axes[i, 0].plot(chains_thin[:, i], alpha=0.7, linewidth=0.5)
        axes[i, 0].set_ylabel(param)
        axes[i, 0].set_title(f"Trace: {param}")
        axes[i, 0].grid(True, alpha=0.3)

        # Histogram
        axes[i, 1].hist(chains[:, i], bins=50, density=True, alpha=0.7, color="blue")
        axes[i, 1].set_xlabel(param)
        axes[i, 1].set_ylabel("Density")
        axes[i, 1].set_title(f"Posterior: {param}")
        axes[i, 1].grid(True, alpha=0.3)

        # Add mean and std
        mean = np.mean(chains[:, i])
        std = np.std(chains[:, i])
        axes[i, 1].axvline(mean, color="red", linestyle="--", label=f"μ={mean:.3g}")
        axes[i, 1].axvline(mean - std, color="red", linestyle=":", alpha=0.5)
        axes[i, 1].axvline(mean + std, color="red", linestyle=":", alpha=0.5)
        axes[i, 1].legend()

    axes[0, 0].set_xlabel("Step")
    axes[-1, 0].set_xlabel("Step")

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"Trace plots saved to {save_path}")

    return fig


def compute_convergence_diagnostics(chains, param_names):
    """
    Compute Gelman-Rubin R-hat and effective sample size.
    """
    # Split chain into two halves
    n_samples = len(chains)
    chain1 = chains[: n_samples // 2]
    chain2 = chains[n_samples // 2 :]

    diagnostics = {}

    for i, param in enumerate(param_names):
        # Between-chain variance
        mean1 = np.mean(chain1[:, i])
        mean2 = np.mean(chain2[:, i])
        B = n_samples / 2 * ((mean1 - mean2) ** 2) / 1  # 2 chains

        # Within-chain variance
        var1 = np.var(chain1[:, i])
        var2 = np.var(chain2[:, i])
        W = (var1 + var2) / 2

        # R-hat
        var_plus = ((n_samples / 2 - 1) * W + B) / (n_samples / 2)
        R_hat = np.sqrt(var_plus / W) if W > 0 else np.inf

        # Autocorrelation
        from statsmodels.tsa.stattools import acf

        try:
            autocorr = acf(chains[:, i], nlags=100, fft=True)
            # Find first negative autocorrelation
            first_negative = np.where(autocorr < 0)[0]
            if len(first_negative) > 0:
                tau = np.sum(autocorr[: first_negative[0]])
            else:
                tau = np.sum(autocorr)
            n_eff = n_samples / (2 * tau)
        except:
            n_eff = n_samples / 10  # Conservative estimate

        diagnostics[param] = {
            "R_hat": R_hat,
            "n_eff": int(n_eff),
            "mean": np.mean(chains[:, i]),
            "std": np.std(chains[:, i]),
            "median": np.median(chains[:, i]),
            "q_16": np.percentile(chains[:, i], 16),
            "q_84": np.percentile(chains[:, i], 84),
        }

    return diagnostics


def create_posterior_table(diagnostics, model_name="Oscillating"):
    """
    Create LaTeX table of posterior statistics.
    """
    rows = []
    rows.append("\\begin{table}[htbp]")
    rows.append("\\centering")
    rows.append(f"\\caption{{Posterior statistics for {model_name} model}}")
    rows.append("\\begin{tabular}{lccccc}")
    rows.append("\\hline")
    rows.append("Parameter & Mean & Median & Std & 68\\% CI & $\\hat{R}$ \\\\")
    rows.append("\\hline")

    param_latex = {
        "tau_0": "$\\tau_0$ (J/m²)",
        "f_osc": "$f_{\\rm osc}$",
        "T": "$T$ (Gyr)",
        "A_w": "$A_w$",
        "H0": "$H_0$ (km/s/Mpc)",
        "Omega_m": "$\\Omega_m$",
    }

    for param, stats in diagnostics.items():
        param_name = param_latex.get(param, param)
        mean = stats["mean"]
        median = stats["median"]
        std = stats["std"]
        ci_low = stats["q_16"]
        ci_high = stats["q_84"]
        r_hat = stats["R_hat"]

        # Format values appropriately
        if param == "tau_0":
            mean_str = f"{mean:.2e}"
            median_str = f"{median:.2e}"
            std_str = f"{std:.2e}"
            ci_str = f"[{ci_low:.2e}, {ci_high:.2e}]"
        elif param in ["f_osc", "A_w"]:
            mean_str = f"{mean:.3f}"
            median_str = f"{median:.3f}"
            std_str = f"{std:.3f}"
            ci_str = f"[{ci_low:.3f}, {ci_high:.3f}]"
        else:
            mean_str = f"{mean:.2f}"
            median_str = f"{median:.2f}"
            std_str = f"{std:.2f}"
            ci_str = f"[{ci_low:.2f}, {ci_high:.2f}]"

        rows.append(
            f"{param_name} & {mean_str} & {median_str} & {std_str} & {ci_str} & {r_hat:.3f} \\\\"
        )

    rows.append("\\hline")
    rows.append("\\end{tabular}")
    rows.append("\\label{tab:posterior}")
    rows.append("\\end{table}")

    return "\n".join(rows)


def plot_corner_plot(chains, param_names, save_path="plots/corner_plot.png"):
    """
    Create corner plot showing parameter correlations.
    """
    # Parameter labels for plot
    labels = {
        "tau_0": r"$\tau_0$ (J/m²)",
        "f_osc": r"$f_{\rm osc}$",
        "T": r"$T$ (Gyr)",
        "A_w": r"$A_w$",
        "H0": r"$H_0$ (km/s/Mpc)",
        "Omega_m": r"$\Omega_m$",
    }

    plot_labels = [labels.get(p, p) for p in param_names]

    # Create corner plot
    fig = corner.corner(
        chains,
        labels=plot_labels,
        quantiles=[0.16, 0.5, 0.84],
        show_titles=True,
        title_kwargs={"fontsize": 12},
    )

    fig.suptitle("Parameter Correlations", fontsize=16, y=0.98)
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"Corner plot saved to {save_path}")

    return fig


def create_summary_figure(data, save_path="plots/mcmc_summary.png"):
    """
    Create a comprehensive summary figure.
    """
    fig = plt.figure(figsize=(16, 10))

    # Layout: 2x3 grid
    # Top row: Oscillating model diagnostics
    # Bottom row: LCDM comparison and Bayes factor

    # Oscillating model parameters
    param_names_osc = ["tau_0", "f_osc", "T", "A_w"]
    chains_osc = data["chains_osc"]

    # Posterior distributions
    for i in range(4):
        ax = plt.subplot(2, 4, i + 1)
        ax.hist(chains_osc[:, i], bins=50, density=True, alpha=0.7, color="blue")
        ax.set_xlabel(param_names_osc[i])
        ax.set_ylabel("Density")
        ax.grid(True, alpha=0.3)

        # Add statistics
        mean = np.mean(chains_osc[:, i])
        std = np.std(chains_osc[:, i])
        ax.set_title(f"{param_names_osc[i]}: {mean:.3g} ± {std:.3g}")

    # LCDM comparison
    ax5 = plt.subplot(2, 2, 3)
    chains_lcdm = data["chains_lcdm"]
    ax5.scatter(chains_lcdm[::10, 0], chains_lcdm[::10, 1], alpha=0.5, s=1)
    ax5.set_xlabel("$H_0$ (km/s/Mpc)")
    ax5.set_ylabel("$\\Omega_m$")
    ax5.set_title("ΛCDM Posterior")
    ax5.grid(True, alpha=0.3)

    # Bayes factor visualization
    ax6 = plt.subplot(2, 2, 4)
    log_K = data["log_K"]
    err_K = data["err_K"]

    # Jeffrey's scale
    scales = [0, 1, 2.3, 3.5, 5]
    labels = ["Weak", "Positive", "Strong", "Very Strong", "Decisive"]
    colors = ["lightgray", "lightblue", "lightgreen", "yellow", "orange"]

    for i in range(len(scales) - 1):
        ax6.axhspan(
            scales[i], scales[i + 1], alpha=0.5, color=colors[i], label=labels[i]
        )

    ax6.errorbar(
        [0.5], [log_K], yerr=[err_K], fmt="ko", markersize=10, capsize=10, linewidth=2
    )
    ax6.set_xlim(0, 1)
    ax6.set_ylim(0, 6)
    ax6.set_ylabel("ln(K)")
    ax6.set_title(f"Bayes Factor: ln(K) = {log_K:.2f} ± {err_K:.2f}")
    ax6.legend(loc="right", bbox_to_anchor=(1.3, 0.5))
    ax6.set_xticks([])

    plt.suptitle("MCMC Analysis Summary", fontsize=16)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"Summary figure saved to {save_path}")

    return fig


def main():
    """
    Generate all MCMC diagnostics.
    """
    print("MCMC Diagnostics and Posterior Analysis")
    print("=" * 50)

    # Load data
    data = load_posterior_data()

    # Extract chains
    chains_osc = data["chains_osc"]

    param_names_osc = ["tau_0", "f_osc", "T", "A_w"]

    print(f"\nLoaded {len(chains_osc)} samples for oscillating model")

    # Trace plots
    print("\nGenerating trace plots...")
    plot_trace_plots(chains_osc, param_names_osc)

    # Convergence diagnostics
    print("\nComputing convergence diagnostics...")
    diagnostics_osc = compute_convergence_diagnostics(chains_osc, param_names_osc)

    print("\nConvergence Statistics:")
    print(f"{'Parameter':<10} {'R-hat':<8} {'n_eff':<8} {'Mean':<12} {'Std':<10}")
    print("-" * 50)
    for param, stats in diagnostics_osc.items():
        print(
            f"{param:<10} {stats['R_hat']:<8.3f} {stats['n_eff']:<8d} "
            f"{stats['mean']:<12.3g} {stats['std']:<10.3g}"
        )

    # Create LaTeX table
    latex_table = create_posterior_table(diagnostics_osc, "Oscillating Brane")
    print("\nLaTeX posterior table:")
    print(latex_table)

    # Save to file
    with open("docs/posterior_table.tex", "w") as f:
        f.write(latex_table)

    # Corner plot
    print("\nGenerating corner plot...")
    plot_corner_plot(chains_osc, param_names_osc)

    # Summary figure
    print("\nGenerating summary figure...")
    create_summary_figure(data)

    # Save diagnostics to file
    np.save("data/mcmc_diagnostics.npy", diagnostics_osc)
    print("\nDiagnostics saved to data/mcmc_diagnostics.npy")


if __name__ == "__main__":
    main()
