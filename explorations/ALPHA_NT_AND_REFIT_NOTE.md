# The α_NT budget and the card-#22 lensing re-fit — monster [62b7f086], part 2

**Mode chercheur.** Romain, after the N-arcs battery: *« vas y pour la note α_NT et le re-fit #22
lentillage »*. These were the two card-path items the battery left open. Both are now computed.
**Net result: the monster is DOWNGRADED by its own follow-up — the arc-core failure mode is not
established.** Scripts: `alpha_nt_budget.py`, `card22_lensing_refit.py` (quarantined, not sacred,
not in the PDF).

---

## 0. What the monster claimed

Monster [62b7f086] (`arcs_obt.py` → `arcs_battery.py`): κ_OBT(R_arc) saturates at ~0.63–0.70 across
11 lenses while every giant arc demands κ = 1, with an "OBT-proper" deficit growing from ×1.15
(Abell 370, merger) to ×1.56 (MS 2137, relaxed). Proposed external patch: the X-ray hydrostatic
mass pipeline — which calibrated card #22's global cored Weyl (f_W = 0.70, β = 0.043) — under-weighs
clusters because non-thermal pressure is unbudgeted. The battery relocated the problem from the
Weyl *profile* (vindicated on 9 lensing cores) to the mass *anchor*: M500(M-T) / M500(lensing) =
0.59.

## 1. The α_NT budget — the patch cannot carry its own amplitude

**Step 1, suspect my own application first.** The 0.59 used *my* 40″-M2D → M500 extrapolation at the
ensemble c = 3.79. Replacing it with published per-cluster joint strong+weak lensing masses
(Merten et al. 2015, SaWLens, Table 7) gives **0.65** — my extrapolation carried a factor 1.10 of
the gap, and it was a noisy estimator (0.61–1.74 per cluster against Merten).

**Step 2, validate the bridge.** Is the M-T relation really card #22's calibration class? Tested
against X-COP's *own* masses using core-excised temperatures computed here from X-COP's own spectra
(0.15–0.75 R500): M-T / X-COP-hydrostatic = **0.87 ± 0.17** over 12 clusters. The bridge holds to
13% — but it is not 1, so the raw gap must be de-biased by that factor before being charged to the
hydrostatic pipeline. **Corrected gap: 0.75, i.e. ×1.34** (this correction works against the
monster; it is applied).

**Step 3, price the patch.** Exact hydrostatic algebra with a non-thermal fraction α(r):

    M_HSE/M_true = (1 − α) − (dlnα/dlnr)/(dlnP_tot/dlnr)   →   b = α(1 − s/|dlnP/dlnr|) for α ~ r^s

A *rising* α makes the bias **smaller** than α, so the required α is **larger** than the required b.
For b = 0.25: **α_NT = 0.25 (constant α) to 0.35 (α ~ r^0.8)**.

| non-thermal fraction at R500 | value | vs the requirement |
|---|---|---|
| X-COP's own analysis (Eckert+19) — **the card's own sample** | ~0.06 | short by ×4–6 |
| hydrodynamical simulations (spread across codes) | 0.10–0.30 | requirement sits at or above the top |

Same statement in bias units: X-COP publishes (1−b) = 0.85–0.87; the gap needs 0.75. And a **radius
caveat that works against the patch**: the gap is a normalisation statement at R500 while the arcs
probe 0.05–0.10 R500, where α_NT is measured and simulated to be *lower*.

**Step 4, the rest of the budget.** Temperature provenance does not rescue — a Chandra-class kT
offset fed into an XMM-calibrated M-T *inflates* M_MT (×1.18 at +10%, ×1.27 at +15%), so the true
hydrostatic-class mass is lower and the gap deeper. The M-T normalisation is no longer a free ±25%
bracket once step 2 pins it on the card's own data: standard error ~6%, not the 34% the gap needs.
Lensing triaxiality/CLASH selection is a few percent (Merten+15's own tailored-simulation section).

**Budget verdict: the proposed WHY does not close.** The gap is real (×1.34, survives my own error
and the bridge de-biasing) but the mechanism offered for it is quantitatively short by ×4–6 on the
very sample card #22 came from. And the external literature disagrees with itself at exactly this
amplitude — Planck's SZ counts require (1−b) ~ 0.6, X-COP's gas fraction gives 0.85–0.87. **The
monster is hostage to an unresolved external measurement that is not mine to arbitrate.**

## 2. The card-#22 lensing re-fit — a decomposition ladder

Same functional form, one change per rung, so nothing is confounded.

| rung | configuration | f_W | r_c / R500 |
|---|---|---|---|
| (0) | card reproduction: X-COP, sinc W(r), the fit's ν, a₀ = 1.2e-10 | **0.70** | **0.043** |
| (1) | + OBT's **derived** μ(x) = x/√(1+x²) (Gauss-Codazzi) | 0.72 | 0.040 |
| (2) | + a₀(z) = cH(z)/2π instead of the measured 1.2e-10 | 0.73 | 0.039 |
| (3) | **lensing masses + W = 1 (photon channel)** ← new globals | **0.59** | **0.037** |

Rung (0) is asserted, and it reproduces the published card exactly.

Rung (1) prices a real inconsistency the ladder exposed: the card's fit used ν(y) = ½+√(¼+1/y)
(μ = x/(1+x)), which boosts ×1.62 at g = a₀, where **OBT's derived** quadrature boosts ×1.27. The
cost is only +0.02 in f_W because cluster bins sit mostly in the deep-MOND regime where the two
forms coincide — but the derived law is the one OBT owns, and it is now the fit's law.

Rung (3) carries the whole move, and **the biggest single term is the ARA channel, not the mass
scale**: X-COP is a *dynamical* tracer (the sinc W(r) applies), lensing is *photons* (W = 1), so the
MOND boost the sinc had suppressed comes back and the Weyl needs less. Switching only the channel on
X-COP itself moves f_W by 0.19.

**New globals: f_W = 0.59, r_c = 0.037 R500 (~47 kpc).** Absolute Weyl amplitude at a fixed cluster,
lensing vs card, at the ×1.34 mass ratio: **×1.12** — *not* the ×1.7 I hand-waved in the battery
commit message. That hand-wave is corrected. Sensitivity: f_gas(R500) = 0.10 → f_W = 0.63;
f_gas = 0.16 → 0.56.

## 3. The finding that matters — the arc test

| | median κ at the observed effective θ_E |
|---|---|
| OBT, card globals | 0.85 |
| OBT, re-fitted globals | 0.78 |
| **published lensing NFW (Merten), spherical** | **0.79** |
| **OBT-proper (κ_NFW / κ_OBT)** | **0.93** (range 0.76–1.12) |

**The published lensing NFW, evaluated spherically, only reaches κ = 0.79 at the observed Einstein
radii — a ×1.27 deficit for the *standard model*.** Neither model makes the arcs in spherical
symmetry. The missing factor is the ellipticity/substructure boost that the 2D models measuring θ_E
contain by construction: Meneghetti et al. 2007 budget the lensing cross-section as ~40% ellipticity,
~30% substructure, ~10% asymmetries, find spherical modelling misestimates the inner slope by ~0.4 in
the mean, and state that spherically symmetric halos "fail to reproduce the lensing signal".

At the same calibration and the same geometry, **OBT-proper = 0.93 — no OBT-proper deficit**, robust
to a factor 6 in BCG mass (0.91–0.94).

**Post-mortem — where the monster's number came from.** For MS 2137 the two published mass models of
the *same* cluster differ by ×3.4 in M200:

| model | M200 | c | κ_NFW(arc) |
|---|---|---|---|
| Donnarumma+09 Chandra X-ray (used by `arcs_obt`) | 4.4e14 | 9.6 | **0.97** |
| Merten+15 SaWLens lensing (used here) | 1.49e15 | 3.1 | **0.79** |

The high-concentration X-ray model puts the critical line on the arc; the lensing model does not.
`arcs_obt` measured OBT against the former. **That choice, not OBT, produced the ×1.56 "OBT-proper"
deficit that flipped the verdict to MONSTER.**

## 4. Verdict and what survives

**The monster is DOWNGRADED, not promoted. No card.** Its premise — "the global cored Weyl saturates
arc convergence and cannot make giant arcs" — is not established: it rested on a per-object
high-concentration X-ray mass model on one cluster, and on published lensing masses the standard
model shows the same deficit for the same (spherical) reason.

Two things survive and are worth keeping:

1. **The hydrostatic-vs-lensing mass gap, ×1.34** — real, external, unresolved, and priced (§1). It
   is a live controversy in the literature (Planck 0.6 vs X-COP 0.85–0.87), not an OBT result.
2. **An OBT-internal channel tension** — a single global Weyl calibrated on the *photon* channel
   under-predicts the *dynamical* channel by ~0.10 dex as published, ~0.17 dex with the mass gap
   applied. This is the **lensing-vs-dynamics scissor**, measured here on clusters. It is an OBT
   question (the ARA sinc channel vs the Weyl amplitude), not a debunk of anyone — **out of the game,
   into the reviewer ledger**, alongside [[project_lensing_dynamics_scissor]].

**Scope carried openly:** the lensing "data" are published NFW fits, not the raw non-parametric
reconstruction; the gas is a universal-closure model, not measured; both arms are spherical; the
samples differ (X-COP z~0.06 vs CLASH z~0.2–0.4); MS 2137's mass model is contested in the
literature at the factor-3 level.
