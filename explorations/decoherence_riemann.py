"""
Geometric Decoherence Simulator — Riemann Explicit Formula
==========================================================
HEURISTIC EXPLORATION — NOT part of Oscillating Brane Theory V8.2.
Not in the PDF, not in the validation pipeline. See explorations/README.md.

Visualizes the Riemann explicit formula: a truncated sum over the non-trivial
zeros of the Riemann zeta function reconstructs the Chebyshev psi(x) staircase
(the counting function of prime powers). As more zeros are added, the
continuous oscillatory sum converges toward the discrete step function.

Run:  pip install numpy matplotlib mpmath  &&  python decoherence_riemann.py
"""

import math

import matplotlib.pyplot as plt
import mpmath
import numpy as np

# Working precision
mpmath.mp.dps = 25

print("Computing the first 200 non-trivial Riemann zeros (resonant modes)...")
N_zeros = 200
zeros = [mpmath.zetazero(i) for i in range(1, N_zeros + 1)]
print(f"{N_zeros} zeros computed. Building the explicit-formula reconstruction...\n")


def von_mangoldt(n):
    """Von Mangoldt function: log(p) if n = p^k is a prime power, else 0."""
    if n <= 1:
        return 0
    for p in range(2, n + 1):
        if n % p == 0:
            temp = n
            while temp % p == 0:
                temp //= p
            if temp == 1:
                return math.log(p)
            return 0
    return 0


def exact_psi(x):
    """Exact Chebyshev psi(x) = sum of von Mangoldt over n <= x (the staircase)."""
    return sum(von_mangoldt(n) for n in range(2, int(x) + 1))


def riemann_wave_interference(x, num_zeros):
    """Riemann explicit formula: psi0(x) = x - sum_rho x^rho/rho - log(2pi)
    - 0.5*log(1 - x^-2). Zeros are summed in conjugate pairs."""
    if x <= 1.0:
        return 0.0
    result = float(x)
    wave_sum = 0.0
    for rho in zeros[:num_zeros]:
        term = mpmath.power(x, rho) / rho
        term_conj = mpmath.power(x, mpmath.conj(rho)) / mpmath.conj(rho)
        wave_sum += float(mpmath.re(term + term_conj))
    result -= wave_sum
    result -= float(math.log(2 * math.pi))
    if x > 1:
        result -= float(0.5 * math.log(1 - x**-2))
    return result


x_vals = np.linspace(2, 30, 1000)

print("Computing exact staircase and explicit-formula sums (10, 50, 200 modes)...")
psi_exact = [exact_psi(x) for x in x_vals]
psi_10 = [riemann_wave_interference(x, 10) for x in x_vals]
psi_50 = [riemann_wave_interference(x, 50) for x in x_vals]
psi_200 = [riemann_wave_interference(x, N_zeros) for x in x_vals]

plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(14, 8))

ax.step(
    x_vals,
    psi_exact,
    color="white",
    linewidth=2,
    where="post",
    label="Discrete staircase: exact Chebyshev psi(x)",
    zorder=10,
)
ax.plot(x_vals, psi_10, color="#f15a60", alpha=0.8, linewidth=1.5, label="10 modes")
ax.plot(x_vals, psi_50, color="#73c03c", alpha=0.8, linewidth=1.5, label="50 modes")
ax.plot(x_vals, psi_200, color="cyan", alpha=0.9, linewidth=2, label="200 modes")

ax.set_title(
    "Riemann Explicit Formula: continuous modes reconstruct the discrete staircase",
    fontsize=15,
    fontweight="bold",
)
ax.set_xlabel("x", fontsize=13)
ax.set_ylabel("Chebyshev psi(x)", fontsize=13)
ax.legend(loc="upper left", fontsize=11)
ax.grid(color="white", linestyle=":", alpha=0.2)

# The ~9% overshoot near each step is the Gibbs phenomenon (non-uniform
# convergence of a truncated mode sum) — it narrows but never vanishes.
ax.text(
    11.5,
    3.5,
    "Gibbs ringing: ~9% overshoot,\nnarrows but never vanishes.",
    fontsize=10,
    color="white",
    bbox=dict(facecolor="black", alpha=0.7),
)

plt.tight_layout()
plt.show()
