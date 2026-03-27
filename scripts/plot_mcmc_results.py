#!/usr/bin/env python3
"""
MCMC Post-Processing — V8.2
=============================

Generates triangle plot (corner plot) from Cobaya MCMC chains.

Usage: python scripts/plot_mcmc_results.py
Requires: getdist (pip install getdist)

Version: 8.2
"""

import os
import sys

try:
    import matplotlib.pyplot as plt
    from getdist import MCSamples, loadMCSamples, plots
except ImportError:
    print("ERROR: getdist not installed. Run: pip install getdist")
    sys.exit(1)

CHAIN_ROOT = "chains_real/obt_v82_production"
OUTPUT = "plots/obt_v82_corner_plot.pdf"


def main():
    if not os.path.exists(CHAIN_ROOT + ".1.txt"):
        print(f"ERROR: No chains found at {CHAIN_ROOT}")
        print("Run: mpirun -n 4 cobaya-run scripts/obt_desi_planck.yaml -f")
        sys.exit(1)

    print("Loading MCMC chains...")
    samples = loadMCSamples(CHAIN_ROOT, settings={"ignore_rows": 0.3})

    print("\n=== MARGINALIZED POSTERIORS ===")
    print(samples.getTable().tableTex())

    # Triangle plot
    g = plots.get_subplot_plotter(width_inch=8)
    g.settings.axes_fontsize = 14
    g.settings.lab_fontsize = 16

    g.triangle_plot(
        [samples],
        ["tau0", "T", "L"],
        filled=True,
        title_limit=1,
        contour_colors=["darkblue"],
    )

    plt.suptitle(
        "OBT V8.2 Posteriors vs DESI DR2 + Planck ISW + DES Y6",
        fontsize=16,
        y=1.02,
    )

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    plt.savefig(OUTPUT, bbox_inches="tight", dpi=300)
    print(f"\nSaved: {OUTPUT}")


if __name__ == "__main__":
    main()
