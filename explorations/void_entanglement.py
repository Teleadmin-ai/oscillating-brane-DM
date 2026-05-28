"""Void entanglement signature — order-of-magnitude anchors.
(1) Thermofield-double route: a brane entangled with a partner through the bulk
    sees a thermal vacuum at the de Sitter / horizon entanglement temperature
    T = hbar H / (2 pi k_B). How big is it? -> is a thermal void signal observable?
(2) Classical standing-wave route: OBT's cymatic scale lambda = c*T_period.
    A *falsifiable* preferred scale in void clustering / void-ISW.
Injection of known quantities validates the unit machinery first.
"""
import math

PASS, FAIL = "PASS", "**FAIL**"
hbar = 1.054571817e-34      # J s
kB   = 1.380649e-23         # J/K
c_km = 299792.458           # km/s
Gyr_s = 3.15576e16          # s
Mpc_km = 3.0856775814913673e19

H0_kmsMpc = 67.4
# H0 in 1/s : (km/s/Mpc) -> divide by (km per Mpc)
H0_s = H0_kmsMpc / Mpc_km
invH0_Gyr = (1.0/H0_s)/Gyr_s

print("="*64)
print("INJECTION / KNOWN ANCHORS")
print(f"  [I0] 1/H0 = {invH0_Gyr:.3f} Gyr (expect ~14.5) -> {PASS if abs(invH0_Gyr-14.5)<0.2 else FAIL}")
# Hubble radius c/H0 in Mpc
R_H = (c_km/H0_s)/Mpc_km
print(f"  [I1] Hubble radius c/H0 = {R_H:.1f} Mpc (expect ~4400) -> {PASS if abs(R_H-4400)<150 else FAIL}")
# CMB temperature reference
T_CMB = 2.725
print(f"  [I2] T_CMB reference = {T_CMB} K")

print("="*64)
print("(1) THERMOFIELD-DOUBLE / HORIZON ENTANGLEMENT TEMPERATURE")
T_dS = hbar*H0_s/(2*math.pi*kB)        # de Sitter / Gibbons-Hawking temperature
print(f"  T_entangle = hbar*H0/(2 pi kB) = {T_dS:.3e} K")
print(f"  ratio T_entangle / T_CMB = {T_dS/T_CMB:.2e}")
print("  -> a brane-entanglement thermal floor sits ~30 orders below the CMB.")
print("     UNOBSERVABLE as a temperature/noise signal, even in the cleanest voids.")

print("="*64)
print("(2) CLASSICAL CYMATIC SCALE (the falsifiable handle OBT already has)")
T_period_Gyr = 2.0
lam_Mpc = (c_km * (T_period_Gyr*Gyr_s)) / Mpc_km   # lambda = c * T_period
print(f"  lambda = c * T_period (T=2 Gyr) = {lam_Mpc:.1f} Mpc (OBT KBC/Chladni: ~613) "
      f"-> {PASS if abs(lam_Mpc-613)<5 else FAIL}")
k_peak = 2*math.pi/lam_Mpc
print(f"  -> preferred wavenumber k = 2 pi / lambda = {k_peak:.5f} Mpc^-1")
print(f"     (a bump/oscillation in the void power spectrum or void-ISW at this k:")
print(f"      THIS is testable by Euclid/DESI void catalogs. It is CLASSICAL standing-wave,")
print(f"      not entanglement.)")

print("="*64)
print("DISCRIMINANT (classical Chladni vs quantum entanglement)")
print("  Classical standing wave : nodes at FIXED comoving positions (a template).")
print("  Quantum entanglement    : excess CORRELATION at separation ~lambda, NO fixed")
print("                            positions (statistical, position-independent).")
print("  -> In principle distinct. In practice cosmic variance (one universe, few")
print("     independent ~600 Mpc cells in the sky) makes the distinction ~impossible.")
