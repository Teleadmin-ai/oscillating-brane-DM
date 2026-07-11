# a0(z) serious attack — reviewer-mode analysis (June 2026)

OBT's crown-jewel prediction is the **evolving MOND scale** `a0(z) = cH(z)/2pi = a0_0 * E(z)` (Milgrom's MOND
takes `a0` constant; OBT derives it from the Gibbons-Hawking horizon temperature, so it must grow with z). This
folder attacks it as a **skeptical reviewer** (axiom: OBT can be false; verify both ways), answering Romain's
three questions, in order: **(1) harden the forecast → (2) dissect the ×1.5 → (3) the over-determination.**

NOT promoted to the 7 sacred files: this is V8.2-validation analysis, quarantined here pending Romain's call.

## The physics it all rests on (deep-MOND `a0 = V_c^4/(G M_bar)`; RAR `a0 = g_obs^2/g_bar`)
A coherent fractional bias in a measured quantity maps to `dln a0` through a **lever**:
`V_c → 4×`, `M_bar → 1×`, `lensing g_obs → 2×`. A bias that *grows with z* biases the fitted slope
`alpha` (where `a0 ~ E^alpha`; OBT: `alpha=1`) by `beta_sys = Cov(b, lnE)/Var(lnE)`, which does **not** average
down. BTFR has the *same* V/M_bar levers as the kinematic RAR → the two are systematically degenerate.

## Scripts & verdicts
| script | question | verdict |
|---|---|---|
| `hardened_forecast.py` | (1) the published forecast's `sqrt(N)` is wrong for a coherent bias | **Evolution test robust** (needs implausible `beta_sys~-1` to erase → Euclid/Rubin settle OBT-vs-constant-MOND, ~tens of σ). **Rate test systematics-limited**: `alpha_hat = 1 + beta_sys`; a ~10% V_c (4×) or ~40% M_bar (1×) coherent high-z bias injects `beta_sys~0.5` = the observed "1.5×". More lenses don't help. |
| `systematics_dissection.py` | (2) is the ×1.5 systematic or real? | **Both ways, honest.** The observed `Delta_alpha ~ +0.4..+0.9` (scattered down to ~0) sits **fully inside** the local-anchor shift (~0.3) + the high-z coherent budget (gas up to +0.8 if M*-only; V/incl ±0.65). → OBT's `alpha=1` **not refuted** (the ×1.5 is consistent with `alpha=1` + a coherent bias; OBT sits at the low edge, KROSS@MOND-anchor = 0.99). But **not confirmed-systematic** either — a real `alpha~1.5` also fits; the rate is **undetermined**. **New honest caveat:** `a0_0=cH0/2pi ≈ 1.04` (H0=67.4) is ~15% **below** MOND's measured `1.2` — a mild ~1σ tension on OBT's *absolute* local a0 (H0=73 → 1.13, closer). |
| `overdetermination.py` | (3) the strongest internal falsifier | Every observable `X ∝ a0^p` must give the **same** `alpha` (powers `a0:+1, BTFR:-1, V_flat:+1/4, Σ†:+1, r_t:-1/2`). **But currently UNFULFILLED**: the only measured high-z handles (kinematic a0 + BTFR) **share** the V 4× lever → their ~1.5 agreement is degenerate, not independent proof (and the 0.7 inter-method spread already hints at extra method-specific systematics). |

## The bottom line (what "attacking a0(z) seriously" found)
- **The evolution is the distinctive, robust claim** — Euclid/Rubin will settle OBT-vs-constant-MOND decisively,
  and it cannot be faked away by any plausible systematic. This is the pépite and it stands.
- **The cH(z)/2pi *rate* is the real frontier, and it is currently UNDECIDED** — the observed ×1.5 is buried in
  (a) the local cH0/2pi-vs-MOND anchor and (b) high-z V_c (4× lever!) + gas systematics. It neither refutes nor
  confirms OBT's Gibbons-Hawking rate.
- **THE decisive near-term experiment** = a **cross-lever** measurement: **Euclid lensing-a0(z)** (g_obs 2×, *no*
  V lever) vs **kinematic-a0(z)** (V 4×), plus `Sigma_dagger(z)` (no V), plus **measured-gas** (ALMA). The split
  (or its absence) and the gas-response cleanly separate **real-rate / V-systematic / gas-systematic**. That one
  measurement turns a0(z) from "evolution confirmed, rate ambiguous" into a *decided rate*.

## Two findings that bear on the PUBLISHED files (Romain's call to promote)
1. `scripts/a0z_forecast.py` adds the systematic in quadrature and divides by `sqrt(N)` — **correct for random
   scatter, wrong for the coherent z-dependent bias** that actually limits the rate test. The hardened version
   here (random vs coherent) is the honest replacement.
2. `predictions.md §6` does not state (a) the mild ~15% **local-anchor tension** (cH0/2pi vs MOND 1.2), nor (b)
   that the current over-determination (a0-RAR + BTFR) is **degenerate** (shared V lever). Both are honest
   caveats that would strengthen the section's "que ce soit vrai."

Run: `for s in hardened_forecast systematics_dissection overdetermination; do python explorations/a0z_analysis/$s.py; done`

## Step 4 (July 2026) — the strong-lensing lever, computed and CLOSED (`slacs_a0z.py` + `step4_strong_lensing.md`)
The amplifier-surfaced "SLACS strong-lensing a0(z), doable NOW" lead is refuted by calculation: (i) THEOREM —
g(R_E) = pi*G*Sigma_cr is a constant of the (z_l,z_s) geometry, floor x_E~2.8-3.3, SLACS sits at ~15: the g~a0
subset cannot exist at theta_E; (ii) the lead's kernel WAS right — projection resurrects the outer deep-MOND
phantom (~7% of M_E, d ln M_E/d ln a0 = 0.067 = x16 the naive local); (iii) but the a0(z)-vs-const signal is
0.025 dex/z = 0.23 sigma in SLACS (dead now), with the coherent IMF/M*-L drift class (0.05-0.1 dex/z) a factor
2-4 above it — at Euclid-N statistics heal (~28 sigma) but the wall stays: an IMF-systematics RACE, not a clean
lever. The decisive cross-lever remains the WEAK-lensing RAR a0(z) (euclid_case.md), exactly as step 2 concluded.
