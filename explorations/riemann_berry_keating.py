"""Coherence check of the AdS2 / Berry-Keating / Riemann thread.

Verifiable claim: the semiclassical phase-space counting of an xp-type
(conformal / AdS2) Hamiltonian reproduces the SMOOTH Riemann zero-counting
density N(T) = (T/2pi) log(T/2pi) - T/2pi + 7/8.  We test it against the
actual non-trivial zeros. This is the REAL, established part of the bridge
(Berry-Keating 1999). What it does NOT give: the individual zeros themselves
(the fluctuating arithmetic part) -> that is the unsolved Hilbert-Polya operator.
"""
import mpmath
import math

mpmath.mp.dps = 30


def N_smooth(T):
    # Riemann-von Mangoldt smooth term = Berry-Keating semiclassical count
    x = T / (2 * math.pi)
    return x * math.log(x) - x + 7.0 / 8.0


print("n :   t_n (actual zero height)   N_smooth(t_n)   n-0.5   residual(arithmetic)")
print("-" * 78)
max_res = 0.0
for n in range(1, 31):
    t_n = float(mpmath.im(mpmath.zetazero(n)))
    Ns = N_smooth(t_n)
    # the zero sits where the staircase jumps n-1 -> n; smooth count ~ n-0.5
    resid = Ns - (n - 0.5)
    max_res = max(max_res, abs(resid))
    print(f"{n:2d} : {t_n:14.5f}        {Ns:10.4f}     {n-0.5:6.1f}   {resid:+8.4f}")

print("-" * 78)
print(f"max |N_smooth(t_n) - (n-0.5)| over first 30 zeros = {max_res:.4f}")
print("\nInterpretation:")
print(" - N_smooth tracks the zero index to <1: the AdS2/xp PHASE-SPACE DENSITY")
print("   reproduces the AVERAGE density of Riemann zeros. (Berry-Keating, real.)")
print(" - The residual is the FLUCTUATING arithmetic part (the primes' fingerprint).")
print("   No xp/CQM operator is known to reproduce it -> Hilbert-Polya still open.")
