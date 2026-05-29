"""
Validation driver for the bulk perturbation solver.

  --gate 0 : numerics self-test (free-field exactness + 2nd-order convergence).
             Fully runnable now (after numba install). No physics.
  --gate 1 : reproduce Cardoso-Hiramatsu-Koyama-Seahra (2007) radiation-era
             short-scale amplification. Requires the VERIFIED master potential
             and the Cardoso setup (fetched from arXiv:0705.1685). STRUCTURED
             STUB until then.

Run order is mandatory: Gate 0 must pass before Gate 1; Gates 0-2 before any
OBT sign reading (Gate 3). See README.md.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import double_null as dn  # noqa: E402


def gate0():
    print("=" * 64)
    print("GATE 0 — double-null numerics (no physics)")
    print("=" * 64)
    print(f"  numba JIT active: {dn._HAVE_NUMBA}")
    err = dn.gate0_free_field()
    ok_free = err < 1e-11
    print(f"  free-field (V=0) exactness: max|err| = {err:.2e}  "
          f"[{'PASS' if ok_free else 'FAIL'}]  (expect <1e-11)")
    p = dn.gate0_convergence()
    ok_conv = 1.7 < p < 2.3
    print(f"  convergence order p = {p:.3f}  "
          f"[{'PASS' if ok_conv else 'FAIL'}]  (expect ~2.0)")
    ok = ok_free and ok_conv
    print(f"\n  GATE 0: {'PASS — numerics validated' if ok else 'FAIL — fix solver before proceeding'}")
    return ok


def gate05():
    import cardoso_ads as ca
    print("=" * 64)
    print("GATE 0.5 — AdS5 master potential vs analytic Bessel mode")
    print("=" * 64)
    (e1, e2, e3), order = ca.gate05()
    print(f"  max|err| at n=129/257/513: {e1:.2e} / {e2:.2e} / {e3:.2e}")
    print(f"  convergence order = {order:.3f}  (expect ~2.0)")
    ok = (e3 < e2 < e1) and (1.7 < order < 2.3)
    print(f"\n  GATE 0.5: {'PASS — AdS5 potential validated' if ok else 'FAIL'}")
    return ok


def gate1():
    print("=" * 64)
    print("GATE 1 — reproduce Cardoso-Hiramatsu-Koyama-Seahra (2007)")
    print("=" * 64)
    print("""\
  PREREQUISITES (not yet satisfied — this is a structured stub):
    1. obt_bulk.V_scalar must be VERIFIED (exact Kodama-Ishibashi potential).
    2. Implement their radiation-era brane trajectory a(tau) ~ tau^(1/2) and
       their initial bulk data (a localized pulse on the initial null segment).
    3. Impose regularity (zero incoming data) on the null line from the bulk
       Cauchy horizon; junction BC on the moving brane.
    4. TARGET: reproduce their reported short-scale amplification of the
       matter power spectrum (~order of magnitude above GR for k > k_crit set
       by the bulk curvature length). Match within a few percent.
  Until (1)-(3) are in place, Gate 1 cannot run. Do NOT read any OBT sign.""")
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", type=str, required=True, choices=["0", "0.5", "1"])
    args = ap.parse_args()
    if args.gate == "0":
        ok = gate0()
    elif args.gate == "0.5":
        ok = gate05()
    elif args.gate == "1":
        ok = gate1()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
