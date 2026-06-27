# A-phase (V9.0 closure): the CMB-background wall for geometric DM

**Status: V9.0 auditor finding, quarantined (NOT V8.2, NOT theory, NOT PDF).**
June 2026. Romain's "attack A" = can the inflation/holographic (it-from-qubit) route fix the closure
datum (the DM amount/clustering)? Mode: reviewer/auditor — axiom "it may fail", test don't glue.
Companion: `QUBIT_HOLOGRAPHY_NOTE.md` (the inflation-entanglement thread). Calc: `a_closure_cmb.py`.

## Where the bit lives, and what the qubit thread addresses
The gate program (CLAUDE.md, Gates 0–24) established: the brane DERIVES the FORM (a₀=cH/2π, μ(x), sinc,
mass-tracking-not-depth, saturated transition, mode structure); the **bulk holds the AMOUNT** (5:1, cluster
factor-2, abundance) as a closure/IC datum. Gate 9 derived the growth *sign* (Indicial Theorem). Gate 7
localized the remaining bit: **the bulk dark-radiation sector's primordial PERTURBATION spectrum** (IC at
the epistemic level of ΛCDM's primordial spectrum).

The qubit note's genuinely-new thread — fix the boundary entanglement (the CFT state, E_μν=⟨T_μν⟩_CFT) **by
inflation** — would turn that PERTURBATION datum into a prediction (the inflationary squeezed vacuum of the
bulk modes → the δE_μν spectrum). That is the right target *for the perturbations*.

## The deeper, structural finding: the CMB BACKGROUND, forced by tracelessness
Auditing one level down, there is an obstruction the inflation thread does **not** touch — the **background**,
not the perturbations:

- **Tracelessness (Shiromizu-Maeda-Sasaki 2000):** the projected Weyl E_μν is traceless, E^μ_μ=0. A
  *homogeneous, isotropic* Weyl therefore has −ρ+3p=0 ⇒ **w=1/3 = radiation (a⁻⁴)**, BBN-limited via ΔN_eff.
  By symmetry there is **no homogeneous a⁻³ (CDM-like) Weyl background**.
- **The CMB needs one.** Matter-radiation equality z_eq=Ω_m/Ω_r−1 must sit at ~3400 so recombination
  (z≈1090) falls in the **matter** era (constant potentials → the observed acoustic-peak heights). That
  needs a homogeneous a⁻³ component Ω_m h²≈0.143 (~5× baryons).
- **Weyl-only DM fails it (`a_closure_cmb.py`):** with baryons the only homogeneous matter, z_eq≈**535** →
  recombination at z=1090 is in the **radiation** era → potentials decay → wrong peaks + huge early ISW.
  The *inhomogeneous* Weyl (the geometric DM) is **mean-zero by construction** → contributes nothing to the
  background H(z) → cannot move z_eq. The homogeneous Weyl is ~3×10⁴ too small AND a⁻⁴ (wrong scaling).

So **pure geometric (Weyl) DM is structurally incompatible with the CMB background.** This is deeper than the
growth-sign (Gate 9, done) and deeper than the inflation-entanglement perturbation chain (the qubit thread):
those concern perturbations; this is H(z) itself.

## Escapes, weighed (both ways)
1. **Radion condensate** (a⁻³, homogeneous, Gate 10 misalignment gives the right Ω) — **refused** (Gate 11):
   a 0.36 eV scalar clusters into galaxy halos, killing the zero-halo MOND success that is OBT's galactic win.
2. **A separate cold KK/particle component** for z_eq — same galaxy-halo problem, and it dilutes "DM is
   geometry" into "geometry + a particle background".
3. **Quadratic backreaction** ⟨E_μν²⟩ ~ the π_μν term ~10⁻⁴⁰ (theory.md) → negligible.
4. **Anisotropic homogeneous Weyl** (w≠1/3) — forbidden by cosmological isotropy at the background level.

## Honest caveat (don't over-claim the negative either)
z_eq=Ω_m/Ω_r is a **density ratio**, independent of the gravity theory → the qualitative obstruction (no
homogeneous a⁻³ matter ⇒ recombination in the radiation era) is **robust**. The *quantitative* peak fit needs
a full modified-gravity Boltzmann solve (CLASS/CAMB with the brane high-energy term, G_eff(t), and the Weyl
sector) — that is the rigorous test, and the proper next step. But this **is** the well-known MOND-CMB problem
(MOND-like gravity fails the 3rd peak without a DM-like component); OBT inherits it, here **sharpened**: the
component OBT hoped would supply it (the Weyl) is forbidden from being a homogeneous a⁻³ background by its own
tracelessness.

## What this means for A (the reframe)
The DM closure problem splits cleanly into two:
- **(a) perturbations / clustering** (the inhomogeneous Weyl, a⁻³, factor-2): the qubit/inflation-entanglement
  thread is the right tool — squeezed-vacuum bulk modes → δE_μν spectrum, cross-checked against Gate 9's sign.
  *Tractable; the genuine V9.0 calculation.*
- **(b) the background z_eq** (a homogeneous a⁻³ source ~5× baryons): **the wall.** Tracelessness forbids the
  Weyl from supplying it; every particle/condensate substitute reintroduces galaxy halos. A real resolution
  needs either a non-Weyl homogeneous sector (a hybrid, diluting the geometric-DM claim) or genuinely new
  physics (e.g. a bulk mechanism that mimics a⁻³ at the background while staying halo-free in galaxies —
  unknown).

**Verdict:** the qubit route helps (a) and **relocates** its datum to inflation (as the note already said);
it does **not** address (b), which is the deeper, structural closure wall for "DM is purely geometric." A
should attack (b) head-on — it is the make-or-break, and naming it precisely (tracelessness ⇒ no homogeneous
a⁻³ Weyl ⇒ z_eq wall) is the first real progress, even though it is a hard/negative result.

## Concrete next steps
1. The full MG-CMB solve (CLASS/CAMB + brane + Weyl) to turn the z_eq estimate into a quantitative peak
   prediction — confirm/quantify the wall.
2. Search for a halo-free homogeneous a⁻³ bulk sector (the only thing that would save pure geometric DM) —
   if none exists, OBT's honest position is a *hybrid* (geometric for galaxies/clusters, a homogeneous sector
   for the CMB), which should be stated openly.
3. Only then is the inflation-entanglement (a)-thread worth the full calculation — it is moot if (b) is fatal.
