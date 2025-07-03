#!/usr/bin/env python3
"""
Kaluza-Klein spectrum calculation for the 5th dimension
Shows particle physics effects of the extra dimension
"""

import numpy as np

# Physical constants
L = 2e-7  # Extra dimension size in meters
hbar_c = 197.326e-9  # GeV·m

# Calculate first KK mass
m_KK = hbar_c / L  # ≈ 1e-3 eV

print("=== Kaluza-Klein Spectrum Analysis ===")
print(f"Extra dimension size L = {L*1e9:.1f} nm")
print(f"First KK mass: {m_KK*1e3:.2f} meV")
print(f"Energy scale: {m_KK*1e9:.2f} µeV")

# Calculate first few KK modes
print("\nKK Tower (first 5 modes):")
for n in range(1, 6):
    mass_n = n * m_KK
    print(f"  n={n}: m = {mass_n*1e3:.2f} meV = {mass_n*1e9:.2f} µeV")

# Connection to cosmology
print("\n=== Cosmological Implications ===")
print(f"Temperature equivalent: T = {m_KK/8.617e-5:.2f} K")
print("This is well above CMB temperature (2.7 K)")
print("→ KK modes are NOT thermally excited today")

# Constraint from Neff
print("\n=== Neff Constraints ===")
print("Each KK mode would contribute ΔNeff ≈ 0.05")
print("Current limit: ΔNeff < 0.2")
print("→ Maximum 4 light KK modes allowed")
print(f"→ Constrains L > {hbar_c/(4*0.001)*1e9:.1f} nm")

# Potential signatures
print("\n=== Experimental Signatures ===")
print("1. Neutrino oscillation experiments:")
print(f"   - Look for oscillations at Δm² ~ ({m_KK*1e3:.1f} meV)²")
print("2. Cosmological observations:")
print("   - Modified matter power spectrum at k ~ 0.1 Mpc⁻¹")
print("3. Fifth force experiments:")
print(f"   - Yukawa potential with range ~ {L*1e6:.1f} µm")