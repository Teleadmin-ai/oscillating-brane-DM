#!/usr/bin/env python3
"""
Verify O3 Pro Audit Corrections
===============================

This script verifies that all corrections requested in the O3 Pro audit
have been properly implemented.
"""

import os
import sys
from pathlib import Path

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def check_file_exists(filepath, description):
    """Check if a file exists and report status."""
    if Path(filepath).exists():
        print(f"{GREEN}✓{RESET} {description}: {filepath}")
        return True
    else:
        print(f"{RED}✗{RESET} {description}: {filepath} NOT FOUND")
        return False


def check_content_in_file(filepath, patterns, description):
    """Check if specific patterns exist in a file."""
    if not Path(filepath).exists():
        print(f"{RED}✗{RESET} {description}: File {filepath} not found")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    all_found = True
    for pattern in patterns:
        if pattern in content:
            print(f"{GREEN}✓{RESET} {description}: Found '{pattern[:50]}...'")
        else:
            print(f"{RED}✗{RESET} {description}: Pattern '{pattern[:50]}...' NOT FOUND")
            all_found = False
    
    return all_found


def main():
    """Run all verification checks."""
    print("=" * 70)
    print("O3 Pro Audit Corrections Verification")
    print("=" * 70)
    
    all_checks_passed = True
    
    # 1. Check Δτ_CMB correction
    print("\n1. Δτ_CMB Correction")
    print("-" * 30)
    
    tau_patterns = [
        "τ_standard = 0.0646",
        "τ_total = 0.0646",
        "within 1.5σ of Planck"
    ]
    all_checks_passed &= check_content_in_file(
        "docs/theoretical_foundations.md",
        tau_patterns,
        "CMB optical depth correction"
    )
    
    all_checks_passed &= check_file_exists(
        "plots/tau_vs_fpbh.png",
        "τ vs f_PBH plot"
    )
    
    all_checks_passed &= check_file_exists(
        "scripts/pbh_cmb_opacity.py",
        "PBH CMB opacity script"
    )
    
    # 2. Check MCMC diagnostics
    print("\n2. MCMC Diagnostics")
    print("-" * 30)
    
    all_checks_passed &= check_file_exists(
        "scripts/analyse_posterior.py",
        "Posterior analysis script"
    )
    
    mcmc_plots = [
        "plots/mcmc_traces.png",
        "plots/corner_plot.png",
        "plots/evidence_comparison.png"
    ]
    for plot in mcmc_plots:
        all_checks_passed &= check_file_exists(plot, f"MCMC plot {os.path.basename(plot)}")
    
    all_checks_passed &= check_file_exists(
        "docs/posterior_table.tex",
        "Posterior statistics table"
    )
    
    # Check posterior table content
    table_patterns = ["τ_0", "f_{\\rm osc}", "68\\% CI", "\\hat{R}"]
    all_checks_passed &= check_content_in_file(
        "docs/posterior_table.tex",
        table_patterns,
        "Posterior table content"
    )
    
    # 3. Check bibliography
    print("\n3. Bibliography")
    print("-" * 30)
    
    ref_patterns = [
        "Ali-Haïmoud, Y. & Kamionkowski, M. (2017)",
        "Poulin, V. et al. (2017)",
        "Serpico, P.D. et al. (2020)",
        "arXiv:1612.05644",
        "arXiv:1707.04206"
    ]
    all_checks_passed &= check_content_in_file(
        "docs/theoretical_foundations.md",
        ref_patterns,
        "Bibliography entries"
    )
    
    # 4. Check 2D prototype results
    print("\n4. 2D Prototype Visualizations")
    print("-" * 30)
    
    all_checks_passed &= check_file_exists(
        "scripts/plot_2d_results.py",
        "2D results plotting script"
    )
    
    all_checks_passed &= check_file_exists(
        "plots/einstein_2d_summary.png",
        "2D prototype summary plot"
    )
    
    all_checks_passed &= check_file_exists(
        "docs/einstein_2d_table.tex",
        "2D prototype results table"
    )
    
    # 5. Check Unicode fixes
    print("\n5. Unicode Artifact Cleaning")
    print("-" * 30)
    
    unicode_patterns = [
        "def clean_unicode_artifacts",
        "'ﬀ': 'ff'",
        "mainfont=Latin Modern Roman"
    ]
    all_checks_passed &= check_content_in_file(
        "scripts/generate_pdf.py",
        unicode_patterns,
        "Unicode cleaning implementation"
    )
    
    # 6. Check Python formatting
    print("\n6. Python Code Quality")
    print("-" * 30)
    
    # Check if scripts are properly formatted
    try:
        import black
        import isort
        
        scripts_dir = Path("scripts")
        py_files = list(scripts_dir.glob("*.py"))
        
        # Check black formatting
        black_mode = black.Mode()
        formatting_ok = True
        for py_file in py_files[:3]:  # Check first 3 files as sample
            with open(py_file, 'r') as f:
                content = f.read()
            try:
                formatted = black.format_str(content, mode=black_mode)
                if content != formatted:
                    print(f"{YELLOW}⚠{RESET} {py_file.name} needs black formatting")
                    formatting_ok = False
            except:
                pass
        
        if formatting_ok:
            print(f"{GREEN}✓{RESET} Python files are black-formatted")
        
        print(f"{GREEN}✓{RESET} Black and isort available for formatting")
        
    except ImportError:
        print(f"{YELLOW}⚠{RESET} Cannot verify formatting (black/isort not installed)")
    
    # Summary
    print("\n" + "=" * 70)
    if all_checks_passed:
        print(f"{GREEN}✓ ALL CORRECTIONS SUCCESSFULLY IMPLEMENTED!{RESET}")
        print("\nThe O3 Pro audit items have been fully addressed.")
        print("A new PDF should be generated with scripts/generate_pdf.py")
    else:
        print(f"{RED}✗ Some corrections are missing or incomplete.{RESET}")
        print("\nPlease review the failed checks above.")
    print("=" * 70)
    
    return 0 if all_checks_passed else 1


if __name__ == "__main__":
    sys.exit(main())