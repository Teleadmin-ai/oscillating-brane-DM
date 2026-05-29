"""
Brane boundary dynamics: the high-energy coupled (Delta, Omega_b) ODE system
(Cardoso-Hiramatsu-Koyama-Seahra 2007, Eq. 38). Units ell = a0 = 1.

This is the MOVING-BRANE boundary dynamics that the full bulk solver (Gate 1b)
needs. Here it is integrated on its own (Gate 1a) to (i) check the transcription
against the growing-mode initial data (Eq. 40a) and (ii) exhibit the short-scale
AMPLIFICATION of the brane density contrast by the bulk-graviton source Omega_b.

System (Eq. 38), ' = d/d eta:
  Delta'' + [ k^2/3 - 4 k^{1/3}/(3 eta^{2/3}) - 2/eta^2 ] Delta = (4 k^3/(9 eta)) Omega_b
  Omega_b'  = (1/(3 eta)) [ 1 + 3 k^{1/3} eta^{4/3} ] Omega_b + 2 Delta / k

Growing mode (Eq. 40a):  Delta ~ (4/3)(k eta)^2 ,  Omega_b ~ k eta^3   (a0=ell=1).
Verified analytically that these satisfy the ODEs at leading order in eta.
"""
import numpy as np
from scipy.integrate import solve_ivp


def rhs(eta, y, k, bulk_coupling=1.0):
    D, dD, Ob = y
    bracket = k ** 2 / 3.0 - 4.0 * k ** (1.0 / 3.0) / (3.0 * eta ** (2.0 / 3.0)) - 2.0 / eta ** 2
    ddD = -bracket * D + bulk_coupling * (4.0 * k ** 3 / (9.0 * eta)) * Ob
    dOb = (1.0 / (3.0 * eta)) * (1.0 + 3.0 * k ** (1.0 / 3.0) * eta ** (4.0 / 3.0)) * Ob + 2.0 * D / k
    return [dD, ddD, dOb]


def growing_mode_ic(eta_i, k):
    """Eq. 40a growing-mode initial data (a0=ell=1)."""
    D = (4.0 / 3.0) * (k * eta_i) ** 2
    dD = (8.0 / 3.0) * k ** 2 * eta_i
    Ob = k * eta_i ** 3
    return [D, dD, Ob]


def integrate(k, eta_i=1e-2, eta_f=10.0, bulk_coupling=1.0, n_out=400):
    y0 = growing_mode_ic(eta_i, k)
    eta = np.linspace(eta_i, eta_f, n_out)
    sol = solve_ivp(rhs, [eta_i, eta_f], y0, t_eval=eta, args=(k, bulk_coupling),
                    rtol=1e-9, atol=1e-12, method="LSODA")
    return sol.t, sol.y  # y = [Delta, dDelta, Omega_b]


# --------------------------------------------------------------------------
# Gate 1a checks
# --------------------------------------------------------------------------
def check_growing_mode(k=5.0):
    """Early-time: integrated Delta, Omega_b must track the analytic growing mode
    before amplification sets in. Returns max relative deviation over eta in
    [eta_i, 10*eta_i]."""
    eta_i = 1e-3
    eta, y = integrate(k, eta_i=eta_i, eta_f=20 * eta_i, bulk_coupling=1.0, n_out=200)
    D_an = (4.0 / 3.0) * (k * eta) ** 2
    Ob_an = k * eta ** 3
    devD = np.max(np.abs(y[0] - D_an) / np.abs(D_an))
    devOb = np.max(np.abs(y[2] - Ob_an) / np.abs(Ob_an))
    return devD, devOb


def amplification_scan(ks):
    """For each k, amplification = |Delta_coupled(eta_f)| / |Delta_decoupled(eta_f)|,
    where decoupled sets the Omega_b -> Delta bulk source to zero. Isolates the
    bulk-graviton pumping of the brane density contrast."""
    amp = []
    for k in ks:
        _, yc = integrate(k, bulk_coupling=1.0)
        _, yd = integrate(k, bulk_coupling=0.0)
        amp.append(abs(yc[0, -1]) / abs(yd[0, -1]))
    return np.array(amp)
