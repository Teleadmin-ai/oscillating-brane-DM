# Step 3 — dissecting the ×1.5 against the REAL survey papers (June 2026)

Reviewer mode, both ways. Script B (`systematics_dissection.py`) showed the ×1.5 fits inside a *plausible* high-z
systematic budget. Step 3 checks that against what the three surveys ACTUALLY did — and sharpens the verdict.

## What the papers actually measure (all three are KINEMATIC — the key finding)

| Survey | a0 probe | gas / M_bar | V corrections | a0(z) fit |
|---|---|---|---|---|
| **MUSE-DARK III** (arXiv:2604.22613) | **kinematic** 3D forward-modelling of **lensing-MAGNIFIED** galaxies (the lensing RESOLVES them; it is *not* a weak-lensing g_obs RAR) | gas **assumed/scaled** (no ALMA CO) | pressure support corrected; no explicit a0 systematic budget in the abstract | **linear in z**: a0(z)=a0(0)+a1·z, a1=1.59×10⁻¹⁰; attributed to "evolution of the baryon-missing-mass connection," **cH(z)/2π never invoked** |
| **KROSS** (Harrison 2017, MNRAS 467, 1965) | kinematic Hα, V at ~3.4 r_d | stellar masses; gas/DM fractions studied (Tiley/Stott, MNRAS 457, 1888) | **beam-smearing + inclination corrected** | — |
| **Übler 2017** (KMOS3D, ApJ 842, 121) | kinematic BTFR | **gas modelled** (gas/stellar ratios decreasing with z) | **pressure support corrected** (circular velocity with a dispersion term) | BTFR zero-point evolves negatively z=0→0.9 |

## Consequences (both ways)

1. **The over-determination is FULLY degenerate — stronger than the published §6 caveat knew.** All three current
   "independent confirmations" are KINEMATIC → all ride the **V_c⁴ (4×) lever**. There is **no lensing-a0(z)
   measurement in existence**. So the cross-lever test (lensing-a0, no V, vs kinematic-a0, 4× V) is **entirely
   future** (Euclid). The §6 line-123 description of MUSE-DARK as "lensing + dynamics RAR" is **misleading**:
   the lensing is *magnification to resolve faint high-z disks*, the RAR is *kinematic*. → small §6 clarification.

2. **The ×1.5 is MORE robust than a naive budget suggested (honest, slightly less comfortable for OBT).** The
   surveys DO apply the V corrections (beam, inclination, pressure/asymmetric-drift) and DO handle gas (Übler
   models its evolution). So the ×1.5 lives in the **RESIDUAL of corrections that were applied**, not in gross
   omissions. The residual budget is tighter than Script B's uncorrected ±0.65: the model-dependence of the
   AD/pressure correction (4× lever on a few-% residual → β~0.1–0.3) plus MUSE's *assumed* gas (β~0.1–0.2) still
   span the observed Δα~0.4 at z~0.9 — but **at the edge, not comfortably inside**. The ×1.5 is harder to dismiss
   as a trivial systematic than the wide budget implied; it remains undetermined, leaning "watch this."

3. **Part of the ×1.5 is parametrization.** MUSE fits a0(z) **linear in z** (a1=1.59), while OBT predicts the
   **E(z)** shape. Linear-in-z over-rises at low z (its low-z slope is ~3× the OBT E(z) slope), so quoting the
   linear a1 exaggerates the discrepancy. The **robust, parametrization-free statement is the ratio at a fixed z**:
   a0(z~0.9) ≈ 2.4 vs cH(z~0.9)/2π ≈ 1.7 → **~1.4×** (matches card #7's "30–45% steeper").

## Step-3 verdict
Script B's conclusion stands and is **sharpened**: (a) the over-determination is fully degenerate (all current
data kinematic; lensing-a0(z) does not yet exist) — the cross-lever is the *only* clean break and it is future;
(b) the ×1.5 sits in the *residual* of corrections the surveys actually applied (not omissions), so it is at the
edge of the systematic budget — undetermined but not comfortably dismissible; (c) the robust number is the ~1.4×
ratio at z~0.9, not the linear a1. The EVOLUTION (pépite) is untouched and robust; the RATE remains the open
frontier, now with a clearer "the surveys did correct, so the residual ×1.5 deserves the cross-lever test."

## §6 refinement proposed to Romain (shown before committing)
Clarify line 123: MUSE-DARK III is a **kinematic** RAR of lensing-*magnified* galaxies (not a weak-lensing a0),
and note that **all three current confirmations are kinematic** (so the over-determination degeneracy is total
and the lensing-a0 cross-lever leg is entirely future).

Sources: MUSE-DARK III arXiv:2604.22613; MUSE-DARK II A&A aa59953-26 (2026); Harrison et al. 2017 MNRAS 467,1965
(arXiv:1701.05561); Tiley/Stott KROSS gas/DM MNRAS 457,1888; Übler et al. 2017 ApJ 842,121 (arXiv:1703.04321).
