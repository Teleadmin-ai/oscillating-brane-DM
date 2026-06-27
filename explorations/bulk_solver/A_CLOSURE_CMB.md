# A-phase (V9.0 closure): the CMB-background question for geometric DM

**Status: V9.0 auditor finding, quarantined (NOT V8.2, NOT theory, NOT PDF).**
June 2026. Romain's "attack A", task (1): is the closure wall (b) — the CMB BACKGROUND — fatal, or can a
**halo-free homogeneous a⁻³ sector** exist? Mode: reviewer/auditor, prudence BOTH ways (test, don't glue —
and self-correct when a first pass over-states). Companions: `QUBIT_HOLOGRAPHY_NOTE.md` (the
inflation-entanglement thread), `a_closure_cmb.py` (the z_eq numbers).

## The requirement
The CMB acoustic peaks need a homogeneous **a⁻³** matter component ~5× baryons (Ω_m h²≈0.143) so that
matter-radiation equality z_eq=Ω_m h²/Ω_r h²−1≈3400 puts recombination (z≈1090) in the **matter** era
(constant potentials → the observed peak heights). Whatever plays the DM must (i) be homogeneous + a⁻³ for
z_eq, (ii) cluster on ~100 Mpc at recombination to source the wells, **and** (iii) stay halo-free in
galaxies to preserve OBT's MOND rotation curves. (i)+(iii) is the MOND-CMB tension.

## Three scenarios (`a_closure_cmb.py`)
- **S1 — Weyl as the background DM: FAILS.** The projected Weyl E_μν is **traceless** (Shiromizu-Maeda-
  Sasaki) ⇒ a homogeneous isotropic Weyl has w=1/3 (radiation, a⁻⁴), *not* a⁻³ matter. Matter = baryons
  only ⇒ z_eq≈**535** ⇒ recombination in the **radiation** era ⇒ grossly wrong peaks. The inhomogeneous
  (geometric) Weyl is mean-zero ⇒ 0 contribution to H(z). **So the Weyl cannot be the CMB background DM.**
- **S2 — radion condensate (a⁻³, Gate 10 misalignment, Ω_cond h²≈0.12 at φ₀=M_s): does z_eq, breaks
  galaxies.** With baryons + condensate, Ω_m h²≈0.142 ⇒ z_eq≈**3407** ⇒ recombination in the matter era ✓.
  **But** Gate 11: the 0.36 eV condensate clusters into galaxy halos ⇒ kills the zero-halo MOND success.
  So the wall is **not** "no a⁻³ background" — it is the a⁻³ sector's **galactic clustering** (the tension).
- **S3 — AeST (Skordis-Złošnik 2021, PRL 127, 161302): the resolution exists.** A relativistic-MOND scalar
  whose homogeneous energy density behaves as **dust (a⁻³)** → fits the Planck CMB + matter power spectrum,
  *while* giving MOND (halo-free) in galaxies. Proof by construction that the MOND-CMB tension is
  **surmountable by a single field**.

## Self-correction (prudence both ways)
My first pass tested only S1 ("Weyl-only") and called the CMB an almost-fatal structural wall. That
**over-stated** it. OBT has S2 (a real a⁻³ candidate that pays the z_eq bill), and S3 proves the tension is
surmountable in principle. The honest statement is narrower and sharper: *the Weyl cannot be the background
DM (a⁻⁴); the only open problem is finding a halo-free a⁻³ sector — which is known to be possible (AeST).*

## Verdict
- The CMB is **not** a proven-fatal wall for OBT. What is solid: the **Weyl alone cannot** supply the
  homogeneous a⁻³ background (tracelessness). What is open but **surmountable**: a halo-free a⁻³ sector
  (AeST exists; OBT must realize it).
- **OBT's concrete A target:** realize the AeST mechanism inside the bulk — a **shift-symmetric radion /
  brane-bending mode that is a⁻³ dust cosmologically AND MOND/halo-free galactically.** The massive 0.36 eV
  condensate is *not* it (clusters, Gate 11); the Weyl is *not* it (a⁻⁴). OBT already gets a₀=cH/2π + μ(x)
  from the radion/bulk MOND sector — the question is whether that same sector carries an AeST-class dust mode.
  **Mapping now DONE (`a_radion_aest.py`): it FAILS.** AeST's halo-free a⁻³ dust is the conserved charge of a
  *massless, shift-symmetric* scalar. OBT has no such mode: the radion is **massive** (0.36 eV, Goldberger-Wise
  — required for extra-dim stabilization + the KK spectrum), so its a⁻³ is an axion-like condensate that
  **clusters** (de Broglie ≈ 0.8 mm ≪ kpc; ~22-23 orders above the fuzzy ~10⁻²³ eV threshold) = the Gate-11
  galaxy-halo result; the Weyl is a⁻⁴; the KK are massive. The radion **mass** is structurally incompatible
  with the AeST **shift symmetry**. **⇒ OBT does NOT inherit AeST's CMB fit.**
- **Honest fallback — now the DEFAULT (the mapping failed):** OBT's position is a **hybrid** (geometric Weyl for
  galaxies/clusters + a homogeneous, ~shift-symmetric/screened sector for the CMB background) — to be stated
  openly, at the cost of "DM is purely geometric". The geometric win stays at galaxy/cluster scales (where OBT
  is strong); the CMB needs an added homogeneous sector that OBT's current field content does not supply.

## How this relates to the qubit thread
The qubit/inflation-entanglement thread addresses the **perturbation spectrum** (clustering, Gate 7). It is
orthogonal to (and moot until) the **background** question here is settled: there is no point predicting the
δE_μν spectrum from inflation if the homogeneous a⁻³ sector that the CMB needs is not identified. So the
ordering is: **first settle the AeST-mode mapping (this note), then the inflation perturbation chain.**

## Next steps
1. ~~The AeST mapping (the make-or-break)~~ **DONE (`a_radion_aest.py`): the mapping FAILS** — OBT has no
   massless shift-symmetric scalar (the radion is massive → its a⁻³ condensate clusters; the Weyl is a⁻⁴).
   So OBT does **not** inherit AeST's CMB fit → the **hybrid** is the honest default. *Open sub-question for a
   future turn:* can a shift-symmetric brane-bending Goldstone survive with MOND-screening *instead of* a hard
   Goldberger-Wise mass (so it is halo-free a⁻³ dust)? This conflicts with the KK spectrum + stabilization as
   currently built — likely a major reformulation, not a free inheritance.
2. **Quantitative confirmation (task 2):** an MG-CMB Boltzmann solve (CLASS/CAMB + brane + a homogeneous a⁻³
   sector) to turn z_eq into an actual peak prediction — now framed for the *hybrid* (the added sector), since
   OBT's native fields do not supply it.
3. The inflation-entanglement perturbation chain — **moot** for the background; still relevant for the
   clustering spectrum *if* the hybrid's homogeneous sector is fixed.

## Task (1) result (`a_radion_reformulation.py`): the Goldstone-screened reformulation FAILS too
The only escape from the hybrid would be to make the radion *itself* the AeST field (massless,
shift-symmetric, halo-free a⁻³ dust) instead of a massive Goldberger-Wise radion. It fails on both horns,
because the radion is the extra-dimension **modulus** (it sets G + the masses via the warp):
- **Stabilized** (massive, the actual radion): its a⁻³ condensate **clusters** (de Broglie ≈ 0.8 mm ≪ kpc)
  → galaxy halos (Gate 11) → not halo-free.
- **Rolling** (massless, AeST-like): carrying Ω_DM as dust needs Δφ ~ √Ω_DM·M_Pl ~ 0.5 M_Pl over a Hubble
  time → Δ(lnG) ~ 0.5 → **Ġ/G ~ 0.5 H₀ ~ 3.5×10⁻¹¹/yr, ~350× the LLR bound** (10⁻¹³/yr) → ruled out (only
  worse for a warp-enhanced coupling).
- **Structural root:** OBT's MOND is **geometric** (a₀=cH/2π horizon + Weyl a⁻⁴), not a scalar field (a⁻³
  dust). The geometric origin — OBT's distinctive a₀=cH/2π — is *exactly* why it cannot do AeST's one-field
  (MOND + a⁻³ dust) trick.

**⇒ The hybrid is confirmed as the honest default.** OBT is modified-gravity-for-galaxies/clusters (its
geometric wins — a₀=cH/2π, μ(x), sinc, Bullet 150 kpc, the cluster two-scale anatomy — all UNAFFECTED)
**plus an added homogeneous a⁻³ sector for the CMB** that its native fields do not supply. "DM is purely
geometric" holds up to cluster scales, not at the CMB. *(Loop discipline: two clean re-read passes + a
re-run; a √Ω_DM refinement to Horn B and a kpc→nm units bug were caught on re-read.)*

## Verification of the escapes (Romain: "cherche la vérité"; web-confirmed June 2026, `a_verify_options.py`)
Before accepting the hybrid, the dismissed escapes were **verified, not asserted**:
- **FACT 1 (web): modified gravity ALONE fails the CMB.** TeVeS / relativistic MOND without a
  dark-matter-like component cannot fit the CMB third acoustic peak (over-enhanced ISW; *"acceptable fits to
  the CMB in TeVeS still need to appeal to non-baryonic mass"*). ⇒ OBT's geometric MOND (a⁻⁴ Weyl) would fail
  the same way → the homogeneous a⁻³ dust is genuinely required. *(physicsworld; astroweb ssm/mond/CMB6)*
- **FACT 2 (web): the resolution is a FIELD, not a particle.** AeST (Skordis-Złošnik 2021): *"the
  time-dependent term behaves like gravitating dust, allowing AeST to reproduce the CMB ... while retaining a
  MOND limit"*. So the added a⁻³ dust can be a scalar-tensor **gravity-sector** field. *(aanda AeST; MNRAS 531/272)*
- **FACT 3 (web+calc): a natural string/fuzzy axion is NOT halo-free.** Fuzzy DM *"produces flat halo cores"*
  → it clusters. To be all the DM it needs m_a > ~10⁻²¹ eV (Lyman-α); at that mass its de Broglie core is
  ~10 pc ≪ galaxy → it makes galaxy halos → double-counts with the MOND phantom → breaks the zero-halo
  galaxies. Halo-free needs m_a < ~10⁻²⁴ eV — ~3 orders below the all-DM floor → no overlap. *(ar5iv 1609.09414)*

**Escape table — every natural OBT field fails as the CMB a⁻³ dust:** Weyl (a⁻⁴), massive radion (clusters),
rolling radion (varies G, ~350× LLR), KK gravitons (massive→cluster), string/fuzzy axion (cored halos /
ruled out). **⇒ the hybrid is CONFIRMED by verification, not a lazy default.**

**The verified nuance (and it is good for OBT):** because the AeST dust is a gravity-sector FIELD (not a
WIMP), **"DM is gravitational/geometric" (no particle dark matter) survives** — OBT only needs a V9.0
extension (a new AeST-class gravity scalar) that its V8.2 fields do not supply, while the galaxy/cluster
geometric wins are untouched. A's honest end-state: OBT's galaxy/cluster DM is the geometric Weyl + the MOND
phantom (its strength), and its CMB needs an added gravity-sector a⁻³ field — a precise, verified scope, not
a defeat.

## (1)-deep: does OBT's bulk NATURALLY contain the AeST/Khronon fields? (`a_obt_aest_content.py`)
Could the CMB sector be a *free* inheritance from OBT's existing fields? No.
- **Aether (unit-timelike vector):** OBT's natural vector is the brane normal n^μ, which is **spacelike**
  (the extra dimension), not timelike → not the aether. *But* the **Khronon route** (Blanchet-Marsat 2011;
  Blanchet 2024, JCAP11(2024)040) gets MOND + the CMB with a **scalar foliation alone, no aether vector** —
  so the aether is not the obstacle.
- **Khronon (preferred-time scalar):** OBT's radion ∂_μφ *does* define a preferred time → structurally a
  khronon candidate. But the khronon/MOND scalar is **~massless** (its scale is the cosmological/MOND scale
  ~H₀ ~ 10⁻³³ eV, via the shift-symmetric k-essence function, not a mass), whereas OBT's radion is a **hard
  0.36 eV** Goldberger-Wise modulus — **~32 orders too heavy**, and the GW mass breaks the shift symmetry the
  khronon needs. The radion is the right *type* (a preferred-time scalar) but the wrong *field*.

**⇒ OBT does NOT naturally contain the AeST/Khronon structure**, so the V9.0 extension is now precisely
named: a **new ~massless (~H₀-scale) shift-symmetric khronon scalar** (a gravity-sector field — no aether
needed), NOT the radion (32 orders too heavy) and NOT the spacelike normal. This confirms the
hybrid/added-gravity-scalar conclusion from the field-content side, and pins exactly what V9.0 must build.
